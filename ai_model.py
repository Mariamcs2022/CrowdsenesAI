import os
import uuid
import cv2
import numpy as np
from ultralytics import YOLO
from lwcc import LWCC
from db import save_detection_image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MODEL = os.path.join(BASE_DIR, "best.pt")

# تحميل المودل مرة واحدة فقط
_YOLO_MODELS = {}

def get_yolo_model(weights_path: str):
    if weights_path not in _YOLO_MODELS:
        _YOLO_MODELS[weights_path] = YOLO(weights_path)
    return _YOLO_MODELS[weights_path]


def analyze_image(
    img_path: str,
    result_dir: str,
    yolo_weights: str = DEFAULT_MODEL,
    conf: float = 0.2,
    imgsz: int = 1280,
    overlay_alpha: float = 0.22,
):
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError(f"Image not found or unreadable: {img_path}")

    h, w = img.shape[:2]

    y_split = int(0.58 * h)
    x_split = int(0.48 * w)
    apex_x = int(0.56 * w)
    apex_y = int(0.22 * h)

    TL = np.array([(0, 0), (0, y_split), (x_split, y_split), (apex_x, apex_y)], dtype=np.int32)
    TR = np.array([(w, 0), (w, y_split), (x_split, y_split), (apex_x, apex_y)], dtype=np.int32)
    BL = np.array([(0, y_split), (x_split, y_split), (x_split, h), (0, h)], dtype=np.int32)
    BR = np.array([(x_split, y_split), (w, y_split), (w, h), (x_split, h)], dtype=np.int32)

    zones = [("TL", TL), ("TR", TR), ("BL", BL), ("BR", BR)]

    def poly_mask(poly):
        m = np.zeros((h, w), dtype=np.uint8)
        cv2.fillPoly(m, [poly], 1)
        return m

    zone_masks = {name: poly_mask(poly) for name, poly in zones}

    # LWCC
    try:
        lwcc_total, density = LWCC.get_count(img_path, return_density=True)
        density = density.astype(np.float32)
        density = cv2.resize(density, (w, h), interpolation=cv2.INTER_CUBIC)
    except Exception:
        lwcc_total = 0.0
        density = np.zeros((h, w), dtype=np.float32)

    zone_sum = {
        name: float((density * zone_masks[name]).sum())
        for name, _ in zones
    }

    total_sum = sum(zone_sum.values()) + 1e-6

    zone_count = {
        name: float(lwcc_total) * (zone_sum[name] / total_sum)
        for name, _ in zones
    }

    def level_from_count(v):
        if v >= 60:
            return "CRITICAL"
        if v >= 35:
            return "HIGH"
        if v >= 15:
            return "MED"
        return "LOW"

    zone_level = {
        name: level_from_count(zone_count[name])
        for name, _ in zones
    }

    priority = {"LOW": 1, "MED": 2, "HIGH": 3, "CRITICAL": 4}
    overall_level = max(zone_level.values(), key=lambda x: priority[x])

    # YOLO
    model = get_yolo_model(yolo_weights)
    res = model.predict(
        img_path,
        classes=[0],
        conf=conf,
        imgsz=imgsz,
        verbose=False
    )[0]

    yolo_boxes = int(len(res.boxes))

    # الرسم
    out = img.copy()
    overlay = out.copy()

    colors = {
        "CRITICAL": (0, 0, 255),
        "HIGH": (0, 165, 255),
        "MED": (0, 255, 255),
        "LOW": (0, 255, 0),
    }

    for name, poly in zones:
        cv2.fillPoly(overlay, [poly], colors[zone_level[name]])

    out = cv2.addWeighted(overlay, overlay_alpha, out, 1 - overlay_alpha, 0)

    for name, poly in zones:
        lvl = zone_level[name]
        c = int(round(zone_count[name]))

        cv2.polylines(out, [poly], True, (255, 255, 255), 2)

        cx = int(np.mean(poly[:, 0]))
        cy = int(np.mean(poly[:, 1]))

        txt = f"{name}: {lvl} | Count: {c}"

        text_x = max(10, min(cx - 190, w - 300))
        text_y = max(30, min(cy, h - 10))

        cv2.putText(
            out, txt, (text_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 3, cv2.LINE_AA
        )
        cv2.putText(
            out, txt, (text_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 1, cv2.LINE_AA
        )

    for b in res.boxes:
        x1, y1, x2, y2 = map(int, b.xyxy[0].tolist())
        cv2.rectangle(out, (x1, y1), (x2, y2), (255, 0, 0), 2)

    os.makedirs(result_dir, exist_ok=True)

    out_name = f"result_{uuid.uuid4().hex}.jpg"
    out_path = os.path.join(result_dir, out_name)

    saved = cv2.imwrite(out_path, out)
    if not saved:
        raise ValueError(f"Failed to save output image: {out_path}")

    module_id = save_detection_image(out_path, model_name="best.pt")

    stats = {
        "lwcc_total": float(lwcc_total),
        "yolo_boxes": yolo_boxes,
        "zone_count": {k: int(round(v)) for k, v in zone_count.items()},
        "zone_level": zone_level,
        "overall_level": overall_level,
    }

    out_rel = f"results/{out_name}"
    return out_rel, stats, module_id
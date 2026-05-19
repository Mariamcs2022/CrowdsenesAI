import sqlite3

DB_PATH = "database2.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
def get_module_image_path(module_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT result_image FROM DetectionModule WHERE module_id=?", (module_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return row[0]  # إذا كنتي مخزنة path
    return None
def save_detection_image(image_path: str, model_name: str = "yolov8m") -> int:
    with open(image_path, "rb") as f:
        img_bytes = f.read()

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO DetectionModule (model_name, result_image)
        VALUES (?, ?)
    """, (model_name, sqlite3.Binary(img_bytes)))
    module_id = cur.lastrowid
    conn.commit()
    conn.close()
    return module_id


# ❗ حذف sender_user_id و receiver_user_id فقط
def create_alert(level: str, module_id: int, note: str = "") -> int:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Alert (level, time, module_id, note)
        VALUES (?, datetime('now'), ?, ?)
    """, (level, module_id, note))
    alert_id = cur.lastrowid
    conn.commit()
    conn.close()
    return alert_id


# ❗ حذف organiser_id
def get_alerts_for_organiser():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT alert_id, level, time, module_id, note
        FROM Alert
        ORDER BY alert_id DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def get_module_image_bytes(module_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT result_image FROM DetectionModule WHERE module_id = ?", (module_id,))
    row = cur.fetchone()
    conn.close()
    return None if row is None else row["result_image"]


# ❗ حذف security_id
def get_alerts_for_security():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT alert_id, level, time, module_id, note
        FROM Alert
        ORDER BY alert_id DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

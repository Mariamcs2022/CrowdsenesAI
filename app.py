import os
import uuid
import sqlite3

from flask import (
    Flask, render_template, request, redirect,
    url_for, send_file, flash, session
)
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import io
from flask import send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from ai_model import analyze_image
from db import create_alert, get_alerts_for_organiser, get_module_image_bytes, get_alerts_for_security
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from fform import RegisterForm, LoginForm, ApplicationForm, SupervisorLoginForm,SupervisorRegisterForm

from db import create_alert, get_alerts_for_organiser, get_module_image_bytes, get_alerts_for_security
app = Flask(__name__)
app.secret_key = "supersecretkey"


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads")
RESULT_DIR = os.path.join(BASE_DIR, "static", "results")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

ALLOWED_EXT = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}

ASH_DB = "database2.db"

@app.route("/generate_pdf/<int:module_id>", methods=["POST"])
def generate_pdf(module_id):
    img_bytes = get_module_image_bytes(module_id)

    if not img_bytes:
        return "Image not found", 404

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    data = {
        "Total People": request.form.get("people_count", "N/A"),
        "Overall Level": request.form.get("level", "N/A"),
    }

    elements = [
        Paragraph("CrowdSense AI Report", styles["Title"]),
        Spacer(1, 15),
        Image(io.BytesIO(img_bytes), width=350, height=280),
        Spacer(1, 15),
    ]

    for key, value in data.items():
        elements.append(Paragraph(f"{key}: {value}", styles["Normal"]))

    elements.append(Spacer(1, 15))
    elements.append(Paragraph("Zone Details", styles["Heading2"]))

    for zone in ["TL", "TR", "BL", "BR"]:
        count = request.form.get(f"{zone}_count", "N/A")
        level = request.form.get(f"{zone}_level", "N/A")
        elements.append(
            Paragraph(f"{zone}: Count = {count}, Level = {level}", styles["Normal"])
        )

    doc.build(elements)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="crowdsense_report.pdf",
        mimetype="application/pdf"
    )
# =========================
# الصفحة الرئيسية
# =========================
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():

        conn = sqlite3.connect(ASH_DB)
        cursor = conn.cursor()

        # 🔥 التحقق من الإيميل
        cursor.execute(
            "SELECT 1 FROM User WHERE email=?",
            (form.email.data,)
        )
        exists = cursor.fetchone()

        if exists:
            form.email.errors.append("هذا الإيميل مستخدم مسبقاً")
            conn.close()
            return render_template("register.html", form=form)

        hashed_password = generate_password_hash(form.password.data)

        cursor.execute("""
            INSERT INTO User (fullname, email, password)
            VALUES (?, ?, ?)
        """, (
            form.fullname.data,
            form.email.data,
            hashed_password
        ))

        conn.commit()

        # 🔥 جلب المستخدم بعد التسجيل
        cursor.execute(
            "SELECT * FROM User WHERE email=?",
            (form.email.data,)
        )
        user = cursor.fetchone()

        conn.close()

        session["user_id"] = user[0]
        session["user_name"] = user[1]
        session["user_email"] = user[2]

        return redirect(url_for("application_page"))

    return render_template("register.html", form=form)
# =========================
# Login
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        con = sqlite3.connect(ASH_DB)
        cursor = con.cursor()

        cursor.execute("SELECT * FROM User WHERE email=?", (email,))
        user = cursor.fetchone()

        if not user:
            con.close()
            flash("كلمة المرور او الايميل غير صحيح", "danger")
            return redirect(url_for("login"))

        # user[3] = password
        if not check_password_hash(user[3], password):
            con.close()
            flash("كلمة المرور او الايميل غير صحيح", "danger")
            return redirect(url_for("login"))

        session.clear()
        session["user_id"] = user[0]
        session["user_name"] = user[1]
        session["user_email"] = user[2]

        cursor.execute("""
            SELECT role, status
            FROM applications
            WHERE email=?
        """, (email,))

        app_data = cursor.fetchone()
        con.close()

        if not app_data:
            return redirect(url_for("application_page"))

        role = app_data[0]
        status = app_data[1]

        if status in ["In Progress", "Rejected"]:
            return redirect(url_for("requesst"))

        if status == "Accepted":
            if role == "security":
                return redirect(url_for("security"))
            if role == "organiser":
                return redirect(url_for("organizer"))

        return redirect(url_for("requesst"))

    return render_template("login.html", form=form)

# =========================
# Supervisor Login
# =========================
@app.route("/soregister", methods=["GET", "POST"])
def soregister():
    form = SupervisorRegisterForm()

    if form.validate_on_submit():

        fullname = form.fullname.data
        username = form.username.data
        email = form.email.data
        password = form.password.data

        conn = sqlite3.connect(ASH_DB)
        cursor = conn.cursor()

        # التحقق من التكرار
        cursor.execute(
            "SELECT 1 FROM supervisors WHERE email=? OR username=?",
            (email, username)
        )
        exists = cursor.fetchone()

        if exists:
            conn.close()
            form.email.errors.append("الإيميل أو اسم المستخدم مستخدم مسبقاً")
            return render_template("soregister.html", form=form)

        hashed_password = generate_password_hash(password)

        cursor.execute("""
            INSERT INTO supervisors (email, fullname, username, password)
            VALUES (?, ?, ?, ?)
        """, (email, fullname, username, hashed_password))

        conn.commit()
        conn.close()

        session["supervisor_email"] = email
        session["supervisor_name"] = fullname
        session["supervisor_username"] = username

        return redirect(url_for("supervisor"))

    return render_template("soregister.html", form=form)

@app.route("/supervisor_login", methods=["GET", "POST"])
def supervisor_login():
    form = SupervisorLoginForm()

    if form.validate_on_submit():

        email = form.email.data
        password = form.password.data

        conn = sqlite3.connect(ASH_DB)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT email, fullname, username, password FROM supervisors WHERE email=?",
            (email,)
        )
        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user[3], password):
            session.clear()
            session["supervisor_email"] = user[0]
            session["supervisor_name"] = user[1]

            return redirect(url_for("supervisor"))

        flash("الإيميل أو كلمة المرور غير صحيحة", "error")

    # 🔥 هذا مهم جدًا لإظهار أخطاء الفورم
    return render_template("supervisor_login.html", form=form)

@app.route("/submit_application", methods=["GET", "POST"])
def submit_application():

    if "user_email" not in session:
        return redirect(url_for("login"))

    form = ApplicationForm()

    # تعبئة تلقائية + readonly
    if request.method == "GET":
        form.fullname.data = session.get("user_name")
        form.email.data = session.get("user_email")

        form.fullname.render_kw = {"readonly": True}
        form.email.render_kw = {"readonly": True}

    if form.validate_on_submit():

        conn = sqlite3.connect(ASH_DB)
        cursor = conn.cursor()

        user_email = session["user_email"]

        # تحقق إذا قدم مسبقًا
        cursor.execute(
            "SELECT id FROM applications WHERE email=?",
            (user_email,)
        )
        existing_application = cursor.fetchone()

        if existing_application:
            conn.close()
            flash("لقد قمت بتقديم طلب مسبقًا", "warning")
            return redirect(url_for("requesst"))

        cursor.execute("""
            INSERT INTO applications
            (fullname, email, phone, age,
             gender_section, role, organization_name,
             crowd_experience, event_experience,
             security_experience, emergency_handling,
             volunteer_before)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (

            session.get("user_name"),   # بدل الفورم
            session.get("user_email"),  # بدل الفورم

            form.phone.data,
            form.age.data,
            form.gender_section.data,
            form.role.data,
            form.organization_name.data,
            form.crowd_experience.data,
            form.event_experience.data,
            form.security_experience.data,
            form.emergency_handling.data,
            form.volunteer_before.data
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("requesst"))

    print("FORM ERRORS:", form.errors)

    return render_template(
        "submit_application.html",
        form=form
    )
# =========================
# Request Status
# =========================
@app.route("/requesst")
def requesst():
    if "user_email" not in session:
        return redirect(url_for("login"))

    email = session["user_email"]
    name = session.get("user_name", "")

    con = sqlite3.connect(ASH_DB)
    cursor = con.cursor()

    cursor.execute(
        "SELECT status FROM applications WHERE email=?",
        (email,)
    )

    result = cursor.fetchone()
    con.close()

    if result:
        status = result[0]
    else:
        status = "No Request Submitted"

    return render_template(
        "requesst.html",
        name=name,
        email=email,
        status=status
    )
def build_pdf_report(module_id, people_count, level, zones_data):
    img_bytes = get_module_image_bytes(module_id)

    if not img_bytes:
        return None

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    elements = [
        Paragraph("CrowdSense AI Report", styles["Title"]),
        Spacer(1, 15),
        Image(io.BytesIO(img_bytes), width=350, height=280),
        Spacer(1, 15),
        Paragraph(f"Total People: {people_count}", styles["Normal"]),
        Paragraph(f"Overall Level: {level}", styles["Normal"]),
        Spacer(1, 15),
        Paragraph("Zone Details", styles["Heading2"])
    ]

    for zone, data in zones_data.items():
        elements.append(
            Paragraph(
                f"{zone}: Count = {data['count']}, Level = {data['level']}",
                styles["Normal"]
            )
        )

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()


@app.route("/security/send_report", methods=["POST"])
def send_report_to_supervisor():
    if "user_email" not in session:
        return redirect(url_for("login"))

    module_id = int(request.form.get("module_id"))
    people_count = request.form.get("people_count", "N/A")
    level = request.form.get("level", "N/A")

    zones_data = {}
    for zone in ["TL", "TR", "BL", "BR"]:
        zones_data[zone] = {
            "count": request.form.get(f"{zone}_count", "N/A"),
            "level": request.form.get(f"{zone}_level", "N/A")
        }

    pdf_bytes = build_pdf_report(module_id, people_count, level, zones_data)

    if not pdf_bytes:
        return "PDF could not be created", 400

    conn = sqlite3.connect(ASH_DB)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reports (pdf_file, sender_email)
        VALUES (?, ?)
    """, (
        pdf_bytes,
        session["user_email"]
    ))

    conn.commit()
    conn.close()
    flash("تم إرسال التقرير للمشرف بنجاح ✅", "success")

    return redirect(url_for("security"))
# =========================
# Application Page
# =========================
# =========================
# Application Page
# =========================
@app.route("/application_page")
def application_page():
    if "user_email" not in session:
        return redirect(url_for("login"))
    return render_template("application_page.html")

# =========================
# Organizer Dashboard
# =========================
@app.route("/organizer")
def organizer():
    if "user_email" not in session:
        return redirect(url_for("login"))

    alerts = get_alerts_for_organiser()

    return render_template(
        "organizer.html",
        alerts=alerts,
        user_name=session.get("user_name", "")
    )


# =========================
# Security Dashboard
# =========================
@app.route("/security")
def security():
    if "user_email" not in session:
        return redirect(url_for("login"))

    sent = request.args.get("sent")
    alerts = get_alerts_for_security()

    return render_template(
        "security.html",
        sent=sent,
        alerts=alerts,
        user_name=session.
get("user_name", "")
    )


# =========================
# Analyze Image
# =========================
@app.route("/security/analyze", methods=["POST"])
def security_analyze():
    if "user_email" not in session:
        return redirect(url_for("login"))

    if "image" not in request.files:
        return "No image uploaded", 400

    f = request.files["image"]

    if f.filename == "":
        return "No file selected", 400

    filename = secure_filename(f.filename)
    ext = os.path.splitext(filename)[1].lower()

    if ext not in ALLOWED_EXT:
        return "File type not allowed", 400

    new_name = f"{uuid.uuid4().hex}{ext}"
    save_path = os.path.join(UPLOAD_DIR, new_name)
    f.save(save_path)

    out_rel, stats, module_id = analyze_image(
    img_path=save_path,
    result_dir=RESULT_DIR
)

    return render_template(
        "result.html",
        out_rel=out_rel,
        stats=stats,
        module_id=module_id,
        user_name=session.get("user_name", "")
    )


# =========================
# Send Alert
# =========================# =========================
# Send Alert
# =========================
@app.route("/security/send_alert", methods=["POST"])
def security_send_alert():
    if "user_email" not in session:
        return redirect(url_for("login"))

    level = (request.form.get("level") or "").strip()
    note = (request.form.get("note") or "").strip()
    module_id_raw = request.form.get("module_id")
    print("module_id_raw =", module_id_raw)
    if not module_id_raw:
        flash("لم يتم العثور على رقم التحليل", "danger")
        return redirect(url_for("security"))

    try:
        module_id = int(module_id_raw)
    except ValueError:
        flash("رقم التحليل غير صالح", "danger")
        return redirect(url_for("security"))

    create_alert(
        level=level,
        module_id=module_id,
        note=note
    )
    flash("تم إرسال التنبيه للمنظم بنجاح ✅", "success")

    return redirect(url_for("security", sent=1))
# =========================
# View Image From DB
# =========================
@app.route("/image/<int:module_id>")
def image(module_id):
    img = get_module_image_bytes(module_id)

    if not img:
        return "Image not found", 404

    import io
    return send_file(io.BytesIO(img), mimetype="image/jpeg")


# =========================
# Supervisor Dashboard
# =========================
@app.route("/supervisor")
def supervisor():
    if "supervisor_email" not in session:
        return redirect(url_for("supervisor_login"))

    conn = sqlite3.connect(ASH_DB)
    cursor = conn.cursor()

    # جميع الطلبات
    cursor.execute("""
        SELECT id, fullname, email, phone, organization_name, role, status
        FROM applications
    """)
    applications = cursor.fetchall()

    # إجمالي
    cursor.execute("SELECT COUNT(*) FROM applications")
    total = cursor.fetchone()[0]

    # قيد الانتظار (In Progress)
    cursor.execute("""
    SELECT COUNT(*) FROM applications 
    WHERE status='In Progress'
""")
    pending = cursor.fetchone()[0]

    # المقبول
    cursor.execute("SELECT COUNT(*) FROM applications WHERE status='Accepted'")
    accepted = cursor.fetchone()[0]

    # المرفوض
    cursor.execute("SELECT COUNT(*) FROM applications WHERE status='Rejected'")
    rejected = cursor.fetchone()[0]
    cursor.execute("""
    SELECT id, sender_email, created_at
    FROM reports
    ORDER BY id DESC
""")
    reports = cursor.fetchall()
    conn.close()

    return render_template(
        "supervisor.html",
        applications=applications,
        reports=reports,
        supervisor_name=session.get("supervisor_name", ""),
        total=total,
        pending=pending,
        accepted=accepted,
        rejected=rejected
    )
@app.route("/security/send_both", methods=["POST"])
def send_both():
    if "user_email" not in session:
        return redirect(url_for("login"))

    module_id = int(request.form.get("module_id"))
    people_count = request.form.get("people_count", "N/A")
    level = request.form.get("level", "N/A")
    note = request.form.get("note", "")

    zones_data = {
        zone: {
            "count": request.form.get(f"{zone}_count", "N/A"),
            "level": request.form.get(f"{zone}_level", "N/A")
        }
        for zone in ["TL", "TR", "BL", "BR"]
    }

    pdf_bytes = build_pdf_report(module_id, people_count, level, zones_data)

    conn = sqlite3.connect(ASH_DB)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO reports (pdf_file, sender_email) VALUES (?, ?)",
        (pdf_bytes, session["user_email"])
    )
    conn.commit()
    conn.close()

    create_alert(level=level, module_id=module_id, note=note)

    flash("تم إرسال التقرير للمشرف والتنبيه للمنظم بنجاح ✅", "success")
    return redirect(url_for("security"))

@app.route("/view_report/<int:report_id>")
def view_report(report_id):
    if "supervisor_email" not in session:
        return redirect(url_for("supervisor_login"))

    conn = sqlite3.connect(ASH_DB)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT pdf_file
        FROM reports
        WHERE id=?
    """, (report_id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return "Report not found", 404

    return send_file(
        io.BytesIO(row[0]),
        mimetype="application/pdf",
        as_attachment=False,
        download_name="crowdsense_report.pdf"
    )
# =========================
# Update Application Status
# =========================
# =========================
# Update Application Status
# =========================
@app.route("/update_status/<int:app_id>/<string:new_status>")
def update_status(app_id, new_status):
    if "supervisor_email" not in session:
        return redirect(url_for("supervisor_login"))

    conn = sqlite3.connect(ASH_DB)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE applications
        SET status=?
        WHERE id=?
    """, (new_status, app_id))

    conn.commit()
    conn.close()

    return redirect(url_for("supervisor"))

# =========================
# Logout
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0",port=8080)

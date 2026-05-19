import sqlite3

def create_database():

    conn = sqlite3.connect("database2.db")
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS User (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    """)
# جدول المشرفين
    cursor.execute('''
CREATE TABLE IF NOT EXISTS supervisors (
    email TEXT PRIMARY KEY,
    fullname TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')
    cursor.execute('''
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,

    age INTEGER NOT NULL,
    gender_section TEXT NOT NULL,

    role TEXT NOT NULL,  -- Organiser / Security

    organization_name TEXT NOT NULL,  -- اسم الجهة

    crowd_experience TEXT,        -- هل سبق تعاملت مع حشود
    event_experience TEXT,        -- هل شاركت بتنظيم فعاليات
    security_experience TEXT,     -- هل عندك خبرة أمنية
    emergency_handling TEXT,      -- هل تعرف تتعامل مع الطوارئ
    volunteer_before TEXT,        -- هل تطوعت قبل

    status TEXT DEFAULT 'In Progress'  -- In Progress / Accepted / Rejected
)
''')
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS DetectionModule (
        module_id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_name TEXT NOT NULL,
        result_image BLOB,              -- صورة النتيجة
        supervisor_id INTEGER,
        FOREIGN KEY (supervisor_id) REFERENCES User(user_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Alert (
        alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
        level TEXT NOT NULL,
        time DATETIME NOT NULL,
        module_id INTEGER NOT NULL,
        note TEXT,  -- ✅ إضافة الملاحظة
        FOREIGN KEY (module_id) REFERENCES DetectionModule(module_id)
    );
    """)
    cursor.execute("""
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pdf_file BLOB,
    sender_email TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
""")
    conn.commit()
    conn.close()

    print("✅ Database created successfully!")


if __name__ == "__main__":
    create_database()
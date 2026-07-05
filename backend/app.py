from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "eventguard.db")


# إنشاء قاعدة البيانات والجداول والبيانات الأولية
def init_db():
    os.makedirs(DB_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # جدول الفعاليات
    c.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        location TEXT,
        date TEXT,
        type TEXT,
        crowd_level INTEGER,
        traffic_needed INTEGER DEFAULT 0
    )
    """)

    # جدول الوظائف
    c.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        description TEXT,
        location TEXT,
        date TEXT,
        workers_needed INTEGER,
        source_link TEXT
    )
    """)

    # جدول الإشعارات
    c.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        message TEXT,
        status TEXT DEFAULT 'unread'
    )
    """)

    # إضافة بيانات أولية مرة واحدة فقط
    events_count = c.execute(
        "SELECT COUNT(*) FROM events"
    ).fetchone()[0]

    if events_count == 0:
        c.execute("""
        INSERT INTO events
        (title, location, date, type, crowd_level, traffic_needed)
        VALUES
        ('Amsterdam Marathon',
         'Amsterdam',
         '2026-07-10',
         'sport',
         9,
         1)
        """)

        c.execute("""
        INSERT INTO events
        (title, location, date, type, crowd_level, traffic_needed)
        VALUES
        ('Summer Festival',
         'Rotterdam',
         '2026-07-15',
         'festival',
         8,
         1)
        """)

        c.execute("""
        INSERT INTO jobs
        (company, description, location, date, workers_needed, source_link)
        VALUES
        ('Gemeente Amsterdam',
         'Traffic controllers needed',
         'Amsterdam',
         '2026-07-10',
         12,
         'https://example.com')
        """)

        c.execute("""
        INSERT INTO notifications
        (type, message)
        VALUES
        ('info',
         'EventGuard system initialized 🚦')
        """)

    conn.commit()
    conn.close()


# تشغيل إنشاء قاعدة البيانات تلقائياً
init_db()


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/")
def home():
    return jsonify({
        "status": "EventGuard API running 🚦"
    })


@app.get("/api/events")
def get_events():
    try:
        db = get_db()
        rows = db.execute(
            "SELECT * FROM events ORDER BY id DESC"
        ).fetchall()
        return jsonify([dict(r) for r in rows])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.get("/api/jobs")
def get_jobs():
    try:
        db = get_db()
        rows = db.execute(
            "SELECT * FROM jobs ORDER BY id DESC"
        ).fetchall()
        return jsonify([dict(r) for r in rows])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.get("/api/notifications")
def get_notifications():
    try:
        db = get_db()
        rows = db.execute(
            "SELECT * FROM notifications ORDER BY id DESC"
        ).fetchall()
        return jsonify([dict(r) for r in rows])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

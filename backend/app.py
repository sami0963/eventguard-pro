from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "eventguard.db")


# 🟢 إنشاء قاعدة البيانات والجداول
def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

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

    c.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        message TEXT,
        status TEXT DEFAULT 'unread'
    )
    """)

    conn.commit()
    conn.close()


# 🟢 تشغيل DB عند بداية السيرفر (مهم جداً)
with app.app_context():
    init_db()


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/")
def home():
    return jsonify({"status": "EventGuard API running 🚦"})


@app.get("/api/events")
def get_events():
    try:
        db = get_db()
        rows = db.execute("SELECT * FROM events ORDER BY id DESC").fetchall()
        return jsonify([dict(r) for r in rows])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.get("/api/jobs")
def get_jobs():
    db = get_db()
    rows = db.execute("SELECT * FROM jobs ORDER BY id DESC").fetchall()
    return jsonify([dict(r) for r in rows])


@app.get("/api/notifications")
def get_notifications():
    db = get_db()
    rows = db.execute("SELECT * FROM notifications ORDER BY id DESC").fetchall()
    return jsonify([dict(r) for r in rows])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

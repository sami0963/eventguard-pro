from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "eventguard.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/")
def home():
    return jsonify({"status": "EventGuard API running 🚦"})


# 🟢 أول API حقيقي: events
@app.get("/api/events")
def get_events():
    db = get_db()
    rows = db.execute("SELECT * FROM events ORDER BY id DESC").fetchall()
    return jsonify([dict(r) for r in rows])


# 🟢 أول API للوظائف
@app.get("/api/jobs")
def get_jobs():
    db = get_db()
    rows = db.execute("SELECT * FROM jobs ORDER BY id DESC").fetchall()
    return jsonify([dict(r) for r in rows])


# 🟢 notifications
@app.get("/api/notifications")
def get_notifications():
    db = get_db()
    rows = db.execute("SELECT * FROM notifications ORDER BY id DESC").fetchall()
    return jsonify([dict(r) for r in rows])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "eventguard.db")


def save_event(event):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    INSERT INTO events
    (title, location, date, type, crowd_level, traffic_needed)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        event["title"],
        event["location"],
        event["date"],
        event["type"],
        event["crowd_level"],
        event["traffic_needed"]
    ))

    conn.commit()
    conn.close()


def run_scraper():

    events = [
        {
            "title": "Amsterdam Dance Event",
            "location": "Amsterdam",
            "date": "2026-08-20",
            "type": "festival",
            "crowd_level": 10,
            "traffic_needed": 1
        },
        {
            "title": "Rotterdam Summer Concert",
            "location": "Rotterdam",
            "date": "2026-08-25",
            "type": "concert",
            "crowd_level": 8,
            "traffic_needed": 1
        }
    ]

    for e in events:
        save_event(e)

    print("Scraper finished")

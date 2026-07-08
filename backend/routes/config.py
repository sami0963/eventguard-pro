import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "database",
    "eventguard.db"
)

PROJECT_NAME = "EventGuard Pro NL"
VERSION = "1.0.0"
import sqlite3
from pathlib import Path

#------------------------------creating Database manager class---------------------------

class DatabaseManager:

    def __init__(self, db_path=r"C:\Users\PC\Documents\CW2_M01086284_CST1510\DATA\intelligence_platform.db"):
        """Initialize the DatabaseManager and ensure the database directory exists."""

        self.db_path = Path(db_path)
        self._ensure_directory()

    def _ensure_directory(self):
        """Ensure the parent directory of the database exists."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def connect(self):
        """Return a fresh SQLite connection."""

        conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        conn.execute("PRAGMA foreign_keys = ON")  # enable foreign key support
        print("Using DB:", self.db_path.resolve())
        return conn

    # Context manager support
    def __enter__(self):
        return self.connect()
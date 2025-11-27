import sqlite3
from pathlib import Path

# Define the path to the database file
DB_PATH = Path("DATA") / "intelligence_platform.db"

def connect_database(db_path=DB_PATH):
    """
    Connect to the SQLite database.
    Creates the database file if it doesn't exist.
    """
    db_path = Path(db_path)

    # Ensure parent directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Create connection
    conn = sqlite3.connect(str(db_path))

    # Enable foreign key enforcement
    conn.execute("PRAGMA foreign_keys = ON")

    return conn





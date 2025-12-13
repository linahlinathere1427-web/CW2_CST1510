import sqlite3
from app.data.db import DatabaseManager

db = DatabaseManager()

#----------------------------creating user manager class-------------------------------

class UserManager:
    def __init__(self):
        """Initialize the database connection."""
        self.conn = None

    def _connect(self):
        """Open a database connection."""
        self.conn = db.connect()

    def _close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None

    # -------------------------- Get User --------------------------
    def get_user_by_username(self, username):
        """Retrieve a user by username."""
        self._connect()
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            return user
        finally:
            self._close()

    # -------------------------- Insert User --------------------------
    def insert_user(self, username, password_hash, role='user'):
        """Insert a new user."""
        self._connect()
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, password_hash, role)
            )
            self.conn.commit()
            print(f"User {username} was successfully inserted.")
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            self._close()

    # -------------------------- Update User --------------------------
    def update_user(self, username, password_hash, role='user'):
        """Update an existing user's password and role."""
        self._connect()
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE users SET password_hash = ?, role = ? WHERE username = ?",
                (password_hash, role, username)
            )
            self.conn.commit()
            return "User was successfully updated."
        except sqlite3.IntegrityError:
            return False
        finally:
            self._close()

    # -------------------------- Delete User --------------------------
    def delete_user(self, username):
        """Delete a user by username."""
        self._connect()
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM users WHERE username = ?", (username,))
            self.conn.commit()
            return "User was successfully deleted."
        except sqlite3.IntegrityError:
            return False
        finally:
            self._close()
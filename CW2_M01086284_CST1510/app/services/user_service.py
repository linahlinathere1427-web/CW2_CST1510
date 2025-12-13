import csv
import re
from pathlib import Path
import bcrypt
import sqlite3
from app.data.db import DatabaseManager


class UserService:
    def __init__(self):
        self.db = DatabaseManager()

    # ------------------ Register User ------------------
    def register(self, username: str, password: str, role: str ) -> tuple[bool, str]:
        """Register a new user with hashed password."""
        conn = self.db.connect()
        cursor = conn.cursor()

        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            return False, f"User '{username}' already exists."

        # Hash password
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        password_hash = hashed.decode('utf-8')

        # Insert user
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role)
        )
        conn.commit()
        conn.close()
        return True, f"User '{username}' registered successfully."

    # ------------------ User Login ------------------
    def login(self, username: str, password: str) -> tuple[bool, str]:
        """Authenticate a user."""
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            return False, "Username not found."

        stored_hash = user[2]  # password_hash column
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
            return True, "Login successful!"
        return False, "Incorrect password."

    # ------------------ Validate Username ------------------
    @staticmethod
    def validate_username(username: str) -> tuple[bool, str]:
        if not (3 <= len(username) <= 20):
            return False, "Username must be between 3 and 20 characters."
        if not re.match("^[A-Za-z0-9_]+$", username):
            return False, "Username must contain only letters, numbers, and underscores."
        return True, ""

    # ------------------ Validate Password ------------------
    @staticmethod
    def validate_password(password: str) -> tuple[bool, str]:
        if len(password) < 8:
            return False, "Password must be at least 8 characters."
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter."
        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter."
        if not re.search(r"\d", password):
            return False, "Password must contain at least one digit."
        if not re.search(r"[!@#$%^&*]", password):
            return False, "Password must contain at least one special character (!@#$%^&*)."
        return True, ""

    # ------------------ Migrate Users from CSV ------------------
    def migrate_users_from_file(self, file_path: str) -> int:
        """Migrate users from CSV file into database."""
        conn = self.db.connect()
        cursor = conn.cursor()
        file_path = Path(file_path)

        if not file_path.exists():
            print(f"File not found: {file_path}")
            return 0

        migrated_count = 0
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                username = row.get("username")
                password_hash = row.get("password_hash")
                role = row.get("role", "user")

                if not username or not password_hash:
                    print(f"Skipping invalid row: {row}")
                    continue

                try:
                    cursor.execute(
                        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, password_hash, role)
                    )
                    if cursor.rowcount > 0:
                        migrated_count += 1
                except sqlite3.Error as e:
                    print(f"Error migrating user {username}: {e}")

        conn.commit()
        conn.close()
        print(f"Migrated {migrated_count} users from {file_path.name}")
        return migrated_count

    # ------------------ List Users ------------------
    def list_users(self):
        """Print all users in database."""
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role FROM users")
        users = cursor.fetchall()
        conn.close()

        print("Users in database:")
        print(f"{'ID':<5} {'Username':<15} {'Role':<10}")
        print("-" * 35)
        for user in users:
            print(f"{user[0]:<5} {user[1]:<15} {user[2]:<10}")
        print(f"\nTotal users: {len(users)}")
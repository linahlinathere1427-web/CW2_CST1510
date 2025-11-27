import bcrypt
import csv
import sqlite3
from pathlib import Path
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user
from app.data.schema import create_users_table

#registering users
def register_user(username, password, role='user'):
    """Register new user in the database."""
    conn = connect_database()
    cursor = conn.cursor()

    #check if user exist
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False,f"User {username} already exists"

    #hash password
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    password_hash = hashed.decode('utf-8')

    # Inserting new user
    cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                   (username, password_hash, role))
    conn.commit()
    conn.close()

    return True, f"User '{username}' registered successfully."


#loging user in
def login_user(username, password):
    """Authentication of a user against the database."""
    user = get_user_by_username(username)
    if not user:
        return False, "Username not found."

    # Verify password
    stored_hash = user[2]  # password_hash column
    password_bytes = password.encode('utf-8')
    hash_bytes = stored_hash.encode('utf-8')
    if bcrypt.checkpw(password_bytes, hash_bytes):
        return True, f"Login successful!"
    return False, "Incorrect password."

DATA_DIR = Path("DATA")

#migrating data of users.txt to new database
def migrate_users_from_file(conn, file_path):
    file_path = Path(file_path)   # ✅ make sure it’s a Path object

    if not file_path.exists():
        print(f"File not found: {file_path}")
        return 0

    cursor = conn.cursor()
    migrated_count = 0

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)  # reads header automatically

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
    print(f"Migrated {migrated_count} users from {file_path.name}")
    return migrated_count



# Verify users were migrated
conn = connect_database()
cursor = conn.cursor()

# Query all users
cursor.execute("SELECT id, username, role FROM users")
users = cursor.fetchall()

print(" Users in database:")
print(f"{'ID':<5} {'Username':<15} {'Role':<10}")
print("-" * 35)
for user in users:
    print(f"{user[0]:<5} {user[1]:<15} {user[2]:<10}")

print(f"\nTotal users: {len(users)}")
conn.close()



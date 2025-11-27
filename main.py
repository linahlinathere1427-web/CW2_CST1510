from app.data.db import connect_database, DB_PATH
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import insert_incident, get_all_incidents
from app.data.datasets import load_all_csv_data


def main():
    print("=" * 60)
    print("Week 8: Database Demo")
    print("=" * 60)

    def setup_database_complete():
        """
        Complete database setup:
        1. Connect to database
        2. Create all tables
        3. Migrate users from users.txt
        4. Load CSV data for all domains
        5. Verify setup
        """
        print("\n" + "=" * 60)
        print("STARTING COMPLETE DATABASE SETUP")
        print("=" * 60)

        # Step 1: Connect
        print("\n[1/5] Connecting to database...")
        conn = connect_database()
        print("       Connected")

        # Step 2: Create tables
        print("\n[2/5] Creating database tables...")
        create_all_tables(conn)

        # Step 3: Migrate users
        print("\n[3/5] Migrating users from users.txt...")
        file_path = ("C:/Users/PC/Documents/CW2_M01086284_CST1510/DATA/users.txt")
        user_count = migrate_users_from_file(conn, file_path)
        print(f"       Migrated {user_count} users")

        # Step 4: Load CSV data (skip users.csv to avoid duplicates)
        print("\n[4/5] Loading CSV data...")
        total_rows = load_all_csv_data(conn)

        # Step 5: Verify
        print("\n[5/5] Verifying database setup...")
        cursor = conn.cursor()

        # Count rows in each table
        tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']
        print("\n Database Summary:")
        print(f"{'Table':<25} {'Row Count':<15}")
        print("-" * 40)

        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"{table:<25} {count:<15}")

        conn.close()

        print("\n" + "=" * 60)
        print(" DATABASE SETUP COMPLETE!")
        print("=" * 60)
        print(f"\n Database location: {DB_PATH.resolve()}")
        print("\nYou're ready for Week 9 (Streamlit web interface)!")


    # 1. Setup database
    setup_database_complete()  # Call once, handles tables + users

    # 2. Test authentication
    success, msg = register_user("alice", "SecurePass123!", "analyst")
    print(msg)

    success, msg = login_user("alice", "SecurePass123!")
    print(msg)

    # 3. Test CRUD
    incident_id = insert_incident(
        "2024-11-05",
        "Phishing",
        "High",
        "Open",
        "Suspicious email detected",
        "alice"
    )
    print(f"Created incident #{incident_id}")

    # 4. Query data
    df = get_all_incidents()
    print(f"Total incidents: {len(df)}")

if __name__ == "__main__":
    main()


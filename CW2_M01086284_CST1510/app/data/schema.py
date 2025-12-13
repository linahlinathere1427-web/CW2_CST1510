from app.data.db import DatabaseManager

db = DatabaseManager()

#-----------------------------creating database setup class---------------------------

class DatabaseSetup:
    def __init__(self):
        """Initialize the DatabaseSetup with a connection placeholder."""
        self.conn = None

    def _connect(self):
        """Open database connection if not already connected."""
        if self.conn is None:
            self.conn = db.connect()

    def _close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None

    # -------------------------- Users Table --------------------------
    def create_users_table(self):
        cursor = self.conn.cursor()
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_sql)
        self.conn.commit()
        print("Users table created successfully")

    # -------------------------- Cyber Incidents Table --------------------------
    def create_cyber_incidents_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            severity TEXT,
            category TEXT,
            status TEXT,
            description TEXT,
            reported_by TEXT,
            FOREIGN KEY (reported_by) REFERENCES users (username)
        );
        """)
        self.conn.commit()
        print("Cyber incidents table created successfully")

    # -------------------------- Datasets Metadata Table --------------------------
    def create_datasets_metadata_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            dataset_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            source TEXT,
            last_updated TEXT,
            record_count INTEGER,
            file_size_mb REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        self.conn.commit()
        print("Dataset metadata table created successfully")

    # -------------------------- IT Tickets Table --------------------------
    def create_it_tickets_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT UNIQUE NOT NULL,
            priority TEXT,
            description TEXT,
            status TEXT,
            assigned_to TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resolution_time_hours INTEGER
        );
        """)
        self.conn.commit()
        print("IT tickets table created successfully")

    # -------------------------- Master Function --------------------------
    def create_all_tables(self):
        """Create all tables in the correct order with foreign keys enabled."""
        self._connect()
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.create_users_table()
        self.create_cyber_incidents_table()
        self.create_datasets_metadata_table()
        self.create_it_tickets_table()
        print("All tables created successfully!")
        self._close()
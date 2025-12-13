import pandas as pd
from app.data.db import DatabaseManager

db = DatabaseManager()

class CyberIncidentManager:
    def __init__(self):
        """Initialize database connection"""
        self.conn = None

    def _connect(self):
        """Open a database connection"""
        self.conn = db.connect()

    def _close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None

    # -------------------------- Insert New Incident --------------------------
    def insert_incident(self, timestamp, category, severity, status, description, reported_by=None):
        self._connect()
        try:
            cursor = self.conn.cursor()
            query = """INSERT INTO cyber_incidents 
                       (timestamp, category, severity, status, description, reported_by)
                       VALUES (?,?,?,?,?,?)"""
            cursor.execute(query, (timestamp, category, severity, status, description, reported_by))
            self.conn.commit()
            return cursor.lastrowid
        finally:
            self._close()

    # -------------------------- Get All Incidents --------------------------
    def get_all_incidents(self):
        self._connect()
        try:
            df = pd.read_sql_query(
                "SELECT * FROM cyber_incidents ORDER BY incident_id DESC", self.conn
            )
            return df
        finally:
            self._close()

    # -------------------------- Update Incident Status --------------------------
    def update_incident_status(self, incident_id, new_status):
        self._connect()
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE cyber_incidents SET status = ? WHERE incident_id = ?",
                (new_status, incident_id)
            )
            self.conn.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Error updating incident {incident_id}: {e}")
            return 0
        finally:
            self._close()

    # -------------------------- Delete Incident --------------------------
    def delete_incident(self, incident_id):
        self._connect()
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "DELETE FROM cyber_incidents WHERE incident_id = ?",
                (incident_id,)
            )
            self.conn.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Error deleting incident {incident_id}: {e}")
            return 0
        finally:
            self._close()

    # -------------------------- Get Incidents Count by Type --------------------------
    def get_incidents_by_type_count(self):
        self._connect()
        try:
            query = """
            SELECT category, COUNT(*) AS count 
            FROM cyber_incidents
            GROUP BY category
            ORDER BY count DESC
            """
            df = pd.read_sql_query(query, self.conn)
            return df
        finally:
            self._close()

    # -------------------------- High Severity Count by Status --------------------------
    def get_high_severity_by_status(self):
        self._connect()
        try:
            query = """
            SELECT status, COUNT(*) as count
            FROM cyber_incidents
            WHERE severity = 'High'
            GROUP BY status
            ORDER BY count DESC
            """
            df = pd.read_sql_query(query, self.conn)
            return df
        finally:
            self._close()

    # -------------------------- Incident Types with Many Cases --------------------------
    def get_incident_types_with_many_cases(self, min_count=5):
        self._connect()
        try:
            query = """
            SELECT category, COUNT(*) as count
            FROM cyber_incidents
            GROUP BY category
            HAVING COUNT(*) > ?
            ORDER BY count DESC
            """
            df = pd.read_sql_query(query, self.conn, params=[min_count])
            return df
        finally:
            self._close()
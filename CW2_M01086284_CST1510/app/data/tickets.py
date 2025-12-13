import pandas as pd
from app.data.db import DatabaseManager

db = DatabaseManager()

#-------------------------------creating IT Tickets class-----------------------------

class ITTicketManager:
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

    # -------------------------- Insert New Ticket --------------------------
    def insert_ticket(self, priority, description, status, assigned_to, created_at, resolution_time_hour):
        self._connect()
        try:
            cursor = self.conn.cursor()
            query = """
                INSERT INTO it_tickets (priority, description, status, assigned_to, created_at, resolution_time_hour)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (priority, description, status, assigned_to, created_at, resolution_time_hour))
            self.conn.commit()
            return cursor.lastrowid
        finally:
            self._close()

    # -------------------------- Get All Tickets --------------------------
    def get_all_tickets(self):
        self._connect()
        try:
            df = pd.read_sql_query(
                "SELECT * FROM it_tickets ORDER BY ticket_id DESC", self.conn
            )
            return df
        finally:
            self._close()

    # -------------------------- Update Ticket Status --------------------------
    def update_ticket_status(self, ticket_id, new_status):
        self._connect()
        try:
            cursor = self.conn.cursor()
            query = "UPDATE it_tickets SET status = ? WHERE ticket_id = ?"
            cursor.execute(query, (new_status, ticket_id))
            self.conn.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Error updating ticket {ticket_id}: {e}")
            return 0
        finally:
            self._close()

    # -------------------------- Delete Ticket --------------------------
    def delete_ticket(self, ticket_id):
        self._connect()
        try:
            cursor = self.conn.cursor()
            query = "DELETE FROM it_tickets WHERE ticket_id = ?"
            cursor.execute(query, (ticket_id,))
            self.conn.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Error deleting ticket {ticket_id}: {e}")
            return 0
        finally:
            self._close()
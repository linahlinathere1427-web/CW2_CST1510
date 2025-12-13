import pandas as pd
from app.data.db import DatabaseManager

db = DatabaseManager()

#----------------------------creating dataset manager set--------------------------------

class DatasetManager:
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

    # -------------------------- Insert New Dataset --------------------------
    def insert_dataset(self, name, category, source, last_updated, record_count, file_size_mb, created_at):
        self._connect()
        try:
            cursor = self.conn.cursor()
            query = """
                INSERT INTO datasets_metadata 
                (name, category, source, last_updated, record_count, file_size_mb, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (name, category, source, last_updated, record_count, file_size_mb, created_at))
            self.conn.commit()
            return cursor.lastrowid
        finally:
            self._close()

    # -------------------------- Get All Datasets --------------------------
    def get_all_datasets(self):
        self._connect()
        try:
            df = pd.read_sql_query(
                "SELECT * FROM datasets_metadata ORDER BY dataset_id DESC", self.conn
            )
            return df
        finally:
            self._close()

    # -------------------------- Update Dataset Category --------------------------
    def update_dataset_category(self, dataset_id, new_category):
        self._connect()
        try:
            cursor = self.conn.cursor()
            query = "UPDATE datasets_metadata SET category = ? WHERE dataset_id = ?"
            cursor.execute(query, (new_category, dataset_id))
            self.conn.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Error updating dataset {dataset_id}: {e}")
            return 0
        finally:
            self._close()

    # -------------------------- Delete Dataset --------------------------
    def delete_dataset(self, dataset_id):
        self._connect()
        try:
            cursor = self.conn.cursor()
            query = "DELETE FROM datasets_metadata WHERE dataset_id = ?"
            cursor.execute(query, (dataset_id,))
            self.conn.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Error deleting dataset {dataset_id}: {e}")
            return 0
        finally:
            self._close()
from pathlib import Path
import pandas as pd
from app.data.db import DatabaseManager

db = DatabaseManager()

#--------------------------making class CSV loader--------------------------------------

class CSVLoader:
    def __init__(self, data_dir="DATA"):
        """ Initialize the CSV loader."""
        self.data_dir = Path(data_dir)
        self.conn = None

    def _connect(self):
        """Open a database connection."""
        self.conn = db.connect()

    def _close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None

    # -------------------------- Load a single CSV to table --------------------------
    def load_csv_to_table(self, csv_path, table_name):
        """Load CSV file into database table."""

        self._connect()
        try:
            df = pd.read_csv(csv_path)
            df.to_sql(table_name, self.conn, if_exists='append', index=False)
            return df
        finally:
            self._close()

    # -------------------------- Load multiple CSVs --------------------------
    def load_all_csv_data(self):
        """Load all predefined CSV files into their respective tables."""

        csv_files = {
            "cyber_incidents": self.data_dir / "cyber_incidents.csv",
            "datasets": self.data_dir / "datasets_metadata.csv",
            "it_tickets": self.data_dir / "it_tickets.csv"
        }

        total_rows = 0
        for table, csv_file in csv_files.items():
            df = self.load_csv_to_table(csv_file, table)
            total_rows += len(df)

        return total_rows
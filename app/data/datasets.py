import pandas as pd
import os
from pathlib import Path

#creating csv loading table
def load_csv_to_table(conn, csv_path, table_name):
    df = pd.read_csv(csv_path)

    # Drop columns that do not exist in DB table
    cols_in_db = pd.read_sql(f"PRAGMA table_info({table_name});", conn)['name'].tolist()
    df = df[[c for c in df.columns if c in cols_in_db]]

    df.to_sql(table_name, conn, if_exists="append", index=False)
    return len(df)



def load_all_csv_data(conn):
    total_rows = 0

    # Base directory of the project
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DATA_DIR = BASE_DIR / "DATA"

    # List of CSV files and their target tables
    csv_files = [
        # (DATA_DIR / "users.txt", "users"),  # ❌ skip users for CSV import
        (DATA_DIR / "cyber_incidents.csv", "cyber_incidents"),
        (DATA_DIR / "datasets_metadata.csv", "datasets_metadata"),
        (DATA_DIR / "it_tickets.csv", "it_tickets"),
    ]

    # Loop through files and load them
    for csv_path, table_name in csv_files:
        rows = load_csv_to_table(conn, csv_path, table_name)
        total_rows += rows

    return total_rows
import pandas as pd
from app.data.db import connect_database

def insert_incident(date, incident_type, severity, status, description, reported_by=None):
    """Insert new cyber incident."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_incidents 
        (date, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, incident_type, severity, status, description, reported_by))
    conn.commit()
    incident_id = cursor.lastrowid
    conn.close()
    return incident_id

def get_all_incidents():
    """retrive all incidents from DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY id DESC",
        conn
    )
    conn.close()
    return df

#updating status of incident
def update_incident_status(conn,incident_id,new_status):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE cyber_incidents SET status = ? WHERE id = ?",
            (new_status, incident_id)
        )
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"error updating incident {incident_id}: {e}")
        return 0

#deleting an incident from database
def delete_incident(conn,incident_id):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM cyber_incidents WHERE id = ?",
            (incident_id,)
        )
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"error deleting incident {incident_id}: {e}")
        return 0

#counting incidents by type
def get_incidents_by_type_count(conn):
    query = """
    SELECT incident_type, COUNT(*) AS count 
    FROM cyber_incidents
    GROUP BY incident_type
    ORDER BY count DESC"""
    df = pd.read_sql_query(query, conn)
    return df

#count high seveirity incidents by status
def get_high_severity_by_status(conn):
    query = """
            SELECT status, COUNT(*) as count
            FROM cyber_incidents
            WHERE severity = 'High'
            GROUP BY status
            ORDER BY count DESC \
            """
    df = pd.read_sql_query(query, conn)
    return df

def get_incident_types_with_many_cases(conn, min_count=5):
    """
    Find incident types with more than min_count cases.
    Uses: SELECT, FROM, GROUP BY, HAVING, ORDER BY
    """
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df

# Test: Run analytical queries
conn = connect_database()

print("\n Incidents by Type:")
df_by_type = get_incidents_by_type_count(conn)
print(df_by_type)

print("\n High Severity Incidents by Status:")
df_high_severity = get_high_severity_by_status(conn)
print(df_high_severity)

print("\n Incident Types with Many Cases (>5):")
df_many_cases = get_incident_types_with_many_cases(conn, min_count=5)
print(df_many_cases)

conn.close()


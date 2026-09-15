"""
db_connection.py
Handles the MySQL connection for the whole MindNest application.
Update DB_CONFIG with your own MySQL credentials before running.
"""

import mysql.connector
from mysql.connector import Error


DB_CONFIG = {
    "host": "localhost",
    "user": "root",          # <-- change to your MySQL username
    "password": "security",          # <-- change to your MySQL password
    "database": "mindnest_db"
}


def get_connection():
    """Returns a new MySQL connection, or None if it fails."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"[Database Error] Could not connect to MySQL: {e}")
        return None


def run_query(query, params=None, fetch=False, fetchone=False):
    """
    Generic helper to run a query.
    - fetch=True returns all rows
    - fetchone=True returns a single row
    - otherwise commits (INSERT/UPDATE/DELETE) and returns the cursor's lastrowid
    """
    conn = get_connection()
    if conn is None:
        return None

    result = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())

        if fetch:
            result = cursor.fetchall()
        elif fetchone:
            result = cursor.fetchone()
        else:
            conn.commit()
            result = cursor.lastrowid

        cursor.close()
    except Error as e:
        print(f"[Database Error] {e}")
        result = None
    finally:
        conn.close()

    return result

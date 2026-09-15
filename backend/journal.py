"""
journal.py
Personal journal: create, read, and list reflection entries.
"""

from datetime import datetime
from db_connection import run_query


def add_journal_entry(user_id, entry_text, title=""):
    if not entry_text or not entry_text.strip():
        return False, "Journal entry cannot be empty."

    today = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%H:%M:%S")
    run_query(
        """INSERT INTO journal_entries (user_id, title, entry_text, entry_date, entry_time)
           VALUES (%s, %s, %s, %s, %s)""",
        (user_id, title, entry_text, today, now_time)
    )
    return True, "Journal entry saved."


def get_journal_entries(user_id, limit=50):
    rows = run_query(
        """SELECT entry_id, title, entry_text, entry_date, entry_time
           FROM journal_entries WHERE user_id = %s
           ORDER BY entry_date DESC, entry_time DESC LIMIT %s""",
        (user_id, limit),
        fetch=True
    )
    return rows or []


def delete_journal_entry(entry_id, user_id):
    run_query(
        "DELETE FROM journal_entries WHERE entry_id = %s AND user_id = %s",
        (entry_id, user_id)
    )
    return True, "Entry deleted."

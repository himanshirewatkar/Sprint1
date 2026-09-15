"""
mood.py
Daily mood check-in, mood history, and self-care tips logic.
"""

from datetime import datetime
from db_connection import run_query

MOODS = {
    "Happy":   {"score": 5, "emoji": "😊"},
    "Calm":    {"score": 4, "emoji": "😌"},
    "Tired":   {"score": 3, "emoji": "😴"},
    "Anxious": {"score": 2, "emoji": "😟"},
    "Sad":     {"score": 2, "emoji": "😢"},
    "Angry":   {"score": 1, "emoji": "😠"},
}


def submit_mood_checkin(user_id, mood_name, notes=""):
    """
    Inserts (or updates, if already checked in today) the user's mood for today.
    Returns (success: bool, message: str)
    """
    if mood_name not in MOODS:
        return False, "Invalid mood selected."

    today = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%H:%M:%S")
    score = MOODS[mood_name]["score"]

    existing = run_query(
        "SELECT mood_id FROM mood_entries WHERE user_id = %s AND entry_date = %s",
        (user_id, today),
        fetchone=True
    )

    if existing:
        run_query(
            """UPDATE mood_entries SET mood_name=%s, mood_score=%s, notes=%s, entry_time=%s
               WHERE mood_id=%s""",
            (mood_name, score, notes, now_time, existing["mood_id"])
        )
        return True, "Today's mood check-in updated."
    else:
        run_query(
            """INSERT INTO mood_entries (user_id, mood_name, mood_score, notes, entry_date, entry_time)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (user_id, mood_name, score, notes, today, now_time)
        )
        return True, "Mood check-in recorded for today."


def get_mood_history(user_id, limit=30):
    """Returns the user's most recent mood entries, newest first."""
    rows = run_query(
        """SELECT mood_name, mood_score, notes, entry_date, entry_time
           FROM mood_entries WHERE user_id = %s
           ORDER BY entry_date DESC, entry_time DESC LIMIT %s""",
        (user_id, limit),
        fetch=True
    )
    return rows or []


def get_self_care_tips(mood_name):
    """Returns a list of self-care tip strings for the given mood."""
    rows = run_query(
        "SELECT tip_text FROM self_care_tips WHERE mood_name = %s",
        (mood_name,),
        fetch=True
    )
    return [r["tip_text"] for r in rows] if rows else [
        "Take a deep breath. You're doing better than you think."
    ]


def get_mood_trend_data(user_id, days=14):
    """Returns (dates, scores) lists for charting mood trend over recent days."""
    rows = run_query(
        """SELECT entry_date, mood_score FROM mood_entries
           WHERE user_id = %s ORDER BY entry_date DESC LIMIT %s""",
        (user_id, days),
        fetch=True
    )
    rows = list(reversed(rows or []))
    dates = [str(r["entry_date"]) for r in rows]
    scores = [r["mood_score"] for r in rows]
    return dates, scores

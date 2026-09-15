"""
meditation.py
Guided meditation timer logic and session logging.
"""

from datetime import datetime
from db_connection import run_query


def log_meditation_session(user_id, duration_minutes):
    """Records a completed meditation session."""
    today = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%H:%M:%S")
    run_query(
        """INSERT INTO meditation_sessions (user_id, duration_minutes, session_date, session_time, completed)
           VALUES (%s, %s, %s, %s, TRUE)""",
        (user_id, duration_minutes, today, now_time)
    )


def get_meditation_history(user_id, limit=20):
    rows = run_query(
        """SELECT duration_minutes, session_date, session_time FROM meditation_sessions
           WHERE user_id = %s ORDER BY session_date DESC, session_time DESC LIMIT %s""",
        (user_id, limit),
        fetch=True
    )
    return rows or []


def get_total_meditation_minutes(user_id):
    row = run_query(
        "SELECT SUM(duration_minutes) AS total FROM meditation_sessions WHERE user_id = %s",
        (user_id,),
        fetchone=True
    )
    return row["total"] if row and row["total"] else 0


GUIDED_SCRIPT = [
    (0,  "Find a comfortable position and gently close your eyes."),
    (10, "Take a slow, deep breath in... and let it out."),
    (25, "Let your shoulders relax. Notice the weight of your body."),
    (45, "Breathe in calm... breathe out tension."),
    (70, "There is nowhere else you need to be right now."),
    (100, "Notice any thoughts, and let them drift by like clouds."),
    (130, "Bring your attention back to your breath, in and out."),
    (160, "Slowly begin to wiggle your fingers and toes."),
    (175, "When you're ready, gently open your eyes."),
]

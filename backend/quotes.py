"""
quotes.py
Daily motivational quotes and affirmations.
"""

import random
from datetime import date
from db_connection import run_query

AFFIRMATIONS = [
    "I am allowed to take up space and rest when I need to.",
    "My feelings are valid, and they do not define me.",
    "I am capable of handling whatever today brings.",
    "I choose peace over worry.",
    "I am proud of how far I've come.",
    "It's okay to go at my own pace.",
    "I trust myself to make good decisions for my wellbeing.",
]


def get_quote_of_the_day():
    """Deterministically picks a quote for today so it stays the same all day."""
    rows = run_query("SELECT quote_text, author FROM quotes", fetch=True)
    if not rows:
        return {"quote_text": "This too shall pass.", "author": "Persian Proverb"}
    index = date.today().toordinal() % len(rows)
    return rows[index]


def get_random_quote():
    rows = run_query("SELECT quote_text, author FROM quotes", fetch=True)
    if not rows:
        return {"quote_text": "This too shall pass.", "author": "Persian Proverb"}
    return random.choice(rows)


def get_affirmation_of_the_day():
    index = date.today().toordinal() % len(AFFIRMATIONS)
    return AFFIRMATIONS[index]

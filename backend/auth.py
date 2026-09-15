"""
auth.py
Handles user registration and login logic (hashing, validation, DB lookup).
"""

import hashlib
import re
from db_connection import run_query


def hash_password(password: str) -> str:
    """Simple SHA-256 hash. For production use bcrypt/argon2 instead."""
    return hashlib.sha256(password.encode()).hexdigest()


def is_valid_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


def register_user(username, email, password, full_name="", dob=None):
    """
    Attempts to register a new user.
    Returns (success: bool, message: str)
    """
    if not username or not email or not password:
        return False, "Username, email, and password are required."

    if not is_valid_email(email):
        return False, "Please enter a valid email address."

    if len(password) < 6:
        return False, "Password must be at least 6 characters long."

    existing = run_query(
        "SELECT user_id FROM users WHERE username = %s OR email = %s",
        (username, email),
        fetchone=True
    )
    if existing:
        return False, "Username or email already exists."

    password_hash = hash_password(password)
    user_id = run_query(
        """INSERT INTO users (username, email, password_hash, full_name, date_of_birth)
           VALUES (%s, %s, %s, %s, %s)""",
        (username, email, password_hash, full_name, dob)
    )

    if user_id:
        return True, "Registration successful! You can now log in."
    return False, "Registration failed. Please check your database connection."


def login_user(username, password):
    """
    Attempts to log in a user.
    Returns (success: bool, user_dict_or_message)
    """
    if not username or not password:
        return False, "Please enter both username and password."

    password_hash = hash_password(password)
    user = run_query(
        "SELECT user_id, username, full_name, email FROM users WHERE username = %s AND password_hash = %s",
        (username, password_hash),
        fetchone=True
    )

    if user:
        return True, user
    return False, "Invalid username or password."

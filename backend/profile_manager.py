"""
profile_manager.py
View and update user profile details.
"""

from db_connection import run_query
from auth import hash_password, is_valid_email


def get_profile(user_id):
    return run_query(
        "SELECT username, email, full_name, date_of_birth, created_at FROM users WHERE user_id = %s",
        (user_id,),
        fetchone=True
    )


def update_profile(user_id, full_name=None, email=None):
    if email and not is_valid_email(email):
        return False, "Please enter a valid email address."

    fields, values = [], []
    if full_name is not None:
        fields.append("full_name = %s")
        values.append(full_name)
    if email is not None:
        fields.append("email = %s")
        values.append(email)

    if not fields:
        return False, "Nothing to update."

    values.append(user_id)
    run_query(f"UPDATE users SET {', '.join(fields)} WHERE user_id = %s", tuple(values))
    return True, "Profile updated successfully."


def change_password(user_id, old_password, new_password):
    if len(new_password) < 6:
        return False, "New password must be at least 6 characters."

    user = run_query(
        "SELECT password_hash FROM users WHERE user_id = %s", (user_id,), fetchone=True
    )
    if not user or user["password_hash"] != hash_password(old_password):
        return False, "Current password is incorrect."

    run_query(
        "UPDATE users SET password_hash = %s WHERE user_id = %s",
        (hash_password(new_password), user_id)
    )
    return True, "Password changed successfully."

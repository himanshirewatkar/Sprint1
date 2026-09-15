# 🌿 MindNest – A Safe Place for Your Mind

A Python + MySQL desktop wellness application for daily mindfulness, mood tracking,
and self-care.

## Features Implemented

- User Registration & Login (with SHA-256 password hashing)
- Daily Mood Check-in (one per day, editable)
- Mood History Tracking (table view of all past check-ins)
- Personalized Self-Care Tips based on selected mood
- Guided Meditation Timer (1/3/5/10/15 min, with a guided script and session logging)
- Nature Sounds player (Rain, Birds, Ocean, Instrumental, Forest Wind — via pygame)
- Daily Motivational Quotes & Positive Affirmations (rotate once per day)
- Personal Journal for daily thoughts and reflections
- Progress Dashboard (mood check-in count, meditation minutes, journal entry count, mood history table)
- User Profile Management (update name/email, change password)

## Project Structure

```
MindNest/
├── main.py                # GUI entry point (Tkinter)
├── db_connection.py       # MySQL connection helper
├── auth.py                # Register/login logic
├── mood.py                # Mood check-in, history, self-care tips
├── meditation.py          # Meditation timer logic + session logging
├── sounds.py               # Nature sound playback (pygame)
├── quotes.py               # Quotes & affirmations
├── journal.py              # Journal entries
├── profile_manager.py      # Profile view/update, password change
├── database/
│   └── schema.sql          # MySQL schema + seed data
├── assets/
│   └── sounds/              # Put your .mp3/.wav files here
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Install MySQL
Make sure MySQL Server is installed and running on your machine.

### 2. Create the database
Run the schema file in MySQL Workbench, phpMyAdmin, or the CLI:

```bash
mysql -u root -p < database/schema.sql
```

This creates the `mindnest_db` database, all tables, and seeds default
self-care tips, nature sound entries, and quotes.

### 3. Configure your database credentials
Open `db_connection.py` and update:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_MYSQL_PASSWORD",
    "database": "mindnest_db"
}
```

### 4. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 5. Add nature sound files (optional)
Drop `.mp3` or `.wav` files into `assets/sounds/` named to match `database/schema.sql`
(`rain.mp3`, `birds.mp3`, `ocean.mp3`, `instrumental.mp3`, `forest_wind.mp3`), or
update the `nature_sounds` table with your own filenames. Playback will fail
silently (with a console message) if a file is missing.

### 6. Run the app

```bash
python main.py
```

## Notes for extending this project (Future Enhancements)

- **Daily Reminders**: use the `schedule` library or OS-level task scheduler to
  trigger a popup or notification at a set time.
- **Dark Mode**: swap the color constants at the top of `main.py` (`BG_MAIN`,
  `BG_CARD`, `TEXT_DARK`, etc.) between a light and dark palette, stored per-user
  in a new `theme_preference` column on `users`.
- **Goal & Habit Tracking**: add a `habits` table (habit_id, user_id, habit_name,
  frequency) and a `habit_logs` table for daily completion checkmarks.
- **Favorite Quotes & Sounds**: add a `user_favorites` table
  (user_id, item_type, item_id) and a star/heart toggle button in the UI.
- **Weekly/Monthly Wellness Reports**: aggregate `mood_entries`,
  `meditation_sessions`, and `journal_entries` by week/month (SQL `GROUP BY`)
  and optionally export as PDF using a library like `reportlab`.
- **Emergency Calm Mode**: a full-screen Toplevel window with a large animated
  breathing circle (expand/contract via `after()`) and calming color transitions.

## Security Note

Passwords are hashed with SHA-256 for this project's scope. For a
production-grade application, use a salted algorithm like **bcrypt** or
**argon2** instead (e.g. `pip install bcrypt`).

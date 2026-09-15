-- ============================================================
-- MindNest Database Schema
-- A Safe Place for Your Mind
-- ============================================================

CREATE DATABASE IF NOT EXISTS mindnest_db;
USE mindnest_db;

-- ------------------------------------------------------------
-- Users table
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    date_of_birth DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Mood check-ins (Daily Mood Check-in + Mood History Tracking)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS mood_entries (
    mood_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    mood_name VARCHAR(30) NOT NULL,        -- e.g. Happy, Sad, Anxious, Calm, Angry, Tired
    mood_score INT NOT NULL,               -- 1 (very low) to 5 (very high)
    notes TEXT,
    entry_date DATE NOT NULL,
    entry_time TIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE KEY unique_daily_mood (user_id, entry_date)   -- one check-in per day
);

-- ------------------------------------------------------------
-- Self-care tips, mapped to a mood
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS self_care_tips (
    tip_id INT AUTO_INCREMENT PRIMARY KEY,
    mood_name VARCHAR(30) NOT NULL,
    tip_text VARCHAR(255) NOT NULL
);

-- ------------------------------------------------------------
-- Guided meditation sessions
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS meditation_sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    duration_minutes INT NOT NULL,
    session_date DATE NOT NULL,
    session_time TIME NOT NULL,
    completed BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ------------------------------------------------------------
-- Nature sounds catalogue
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS nature_sounds (
    sound_id INT AUTO_INCREMENT PRIMARY KEY,
    sound_name VARCHAR(50) NOT NULL,
    file_path VARCHAR(255) NOT NULL
);

-- ------------------------------------------------------------
-- Motivational quotes / affirmations
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS quotes (
    quote_id INT AUTO_INCREMENT PRIMARY KEY,
    quote_text VARCHAR(255) NOT NULL,
    author VARCHAR(100) DEFAULT 'Unknown'
);

-- ------------------------------------------------------------
-- Personal journal entries
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS journal_entries (
    entry_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(150),
    entry_text TEXT NOT NULL,
    entry_date DATE NOT NULL,
    entry_time TIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ============================================================
-- Seed data
-- ============================================================

INSERT INTO self_care_tips (mood_name, tip_text) VALUES
('Happy', 'Savor this moment - write down what made you happy today.'),
('Happy', 'Share your good mood with someone you care about.'),
('Sad', 'Be gentle with yourself. It is okay to not be okay.'),
('Sad', 'Try a short walk outside, even 5 minutes can help.'),
('Anxious', 'Try the 4-7-8 breathing technique: inhale 4s, hold 7s, exhale 8s.'),
('Anxious', 'Ground yourself: name 5 things you can see, 4 you can hear, 3 you can touch.'),
('Angry', 'Step away for a moment before reacting. Let your body cool down first.'),
('Angry', 'Try writing down what triggered you without judging yourself.'),
('Calm', 'Great state to journal or plan something meaningful.'),
('Calm', 'Use this clarity to set an intention for tomorrow.'),
('Tired', 'Rest is productive too. Consider a short nap or early night.'),
('Tired', 'Hydrate and stretch - fatigue is often more than just sleep.');

INSERT INTO nature_sounds (sound_name, file_path) VALUES
('Rain', 'assets/sounds/rain.mp3'),
('Birds', 'assets/sounds/birds.mp3'),
('Ocean Waves', 'assets/sounds/ocean.mp3'),
('Soft Instrumental', 'assets/sounds/instrumental.mp3'),
('Forest Wind', 'assets/sounds/forest_wind.mp3');

INSERT INTO quotes (quote_text, author) VALUES
('The only way out is through.', 'Robert Frost'),
('You do not have to control your thoughts. You just have to stop letting them control you.', 'Dan Millman'),
('Every day may not be good, but there is something good in every day.', 'Alice Morse Earle'),
('Peace comes from within. Do not seek it without.', 'Buddha'),
('This too shall pass.', 'Persian Proverb'),
('Almost everything will work again if you unplug it for a few minutes, including you.', 'Anne Lamott'),
('You are allowed to be both a masterpiece and a work in progress.', 'Sophia Bush'),
('Small steps every day.', 'Unknown');

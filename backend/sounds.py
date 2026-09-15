"""
sounds.py
Nature sound playback using pygame's mixer.
Place matching audio files in assets/sounds/ (mp3 or wav).
"""

import os
from db_connection import run_query

try:
    import pygame
    pygame.mixer.init()
    SOUND_AVAILABLE = True
except Exception as e:
    print(f"[Sounds] pygame not available ({e}). Nature sounds will be disabled until it's installed.")
    pygame = None
    SOUND_AVAILABLE = False

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "sounds")


def get_all_sounds():
    """Fetch the catalogue of nature sounds from the DB."""
    rows = run_query("SELECT sound_name, file_path FROM nature_sounds", fetch=True)
    return rows or []


def play_sound(file_path, loop=True):
    """Plays a sound file on loop (or once). Fails silently with a message if file missing or pygame unavailable."""
    if not SOUND_AVAILABLE:
        print("[Sounds] pygame is not installed, so playback is disabled.")
        return False
    full_path = file_path if os.path.isabs(file_path) else os.path.join(os.path.dirname(__file__), "..", file_path)
    if not os.path.exists(full_path):
        print(f"[Sounds] File not found: {full_path}. Add your audio file to assets/sounds/.")
        return False
    try:
        pygame.mixer.music.load(full_path)
        pygame.mixer.music.play(-1 if loop else 0)
        return True
    except pygame.error as e:
        print(f"[Sounds] Playback error: {e}")
        return False


def stop_sound():
    if SOUND_AVAILABLE:
        pygame.mixer.music.stop()


def set_volume(level: float):
    """level should be between 0.0 and 1.0"""
    if SOUND_AVAILABLE:
        pygame.mixer.music.set_volume(max(0.0, min(1.0, level)))

"""
main.py
MindNest - A Safe Place for Your Mind
Main Tkinter desktop application entry point.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

import auth
import mood
import meditation
import sounds
import quotes
import journal
import profile_manager

# ---------------------------------------------------------------
# Color palette - calm, soft tones
# ---------------------------------------------------------------
BG_MAIN = "#EAF2EF"
BG_CARD = "#FFFFFF"
ACCENT = "#7CA982"
ACCENT_DARK = "#5C8A66"
TEXT_DARK = "#33413A"
TEXT_MUTED = "#7A8C83"
FONT_TITLE = ("Georgia", 22, "bold")
FONT_HEADING = ("Segoe UI", 14, "bold")
FONT_BODY = ("Segoe UI", 11)
FONT_SMALL = ("Segoe UI", 9)


class MindNestApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MindNest - A Safe Place for Your Mind")
        self.geometry("900x650")
        self.configure(bg=BG_MAIN)
        self.minsize(800, 600)

        self.current_user = None  # dict with user_id, username, full_name, email

        # Container that holds all frames (pages)
        self.container = tk.Frame(self, bg=BG_MAIN)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        self.show_frame(LoginPage)

    def show_frame(self, page_class):
        for widget in self.container.winfo_children():
            widget.destroy()
        frame = page_class(self.container, self)
        frame.pack(fill="both", expand=True)

    def logout(self):
        self.current_user = None
        sounds.stop_sound()
        self.show_frame(LoginPage)


# =================================================================
# LOGIN PAGE
# =================================================================
class LoginPage(tk.Frame):
    def __init__(self, parent, controller: MindNestApp):
        super().__init__(parent, bg=BG_MAIN)
        self.controller = controller

        card = tk.Frame(self, bg=BG_CARD, padx=40, pady=40)
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(card, text="🌿 MindNest", font=FONT_TITLE, bg=BG_CARD, fg=ACCENT_DARK).pack(pady=(0, 5))
        tk.Label(card, text="A Safe Place for Your Mind", font=FONT_SMALL, bg=BG_CARD, fg=TEXT_MUTED).pack(pady=(0, 25))

        tk.Label(card, text="Username", font=FONT_BODY, bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w")
        self.username_entry = tk.Entry(card, font=FONT_BODY, width=30)
        self.username_entry.pack(pady=(0, 12))

        tk.Label(card, text="Password", font=FONT_BODY, bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w")
        self.password_entry = tk.Entry(card, font=FONT_BODY, width=30, show="*")
        self.password_entry.pack(pady=(0, 20))

        tk.Button(card, text="Log In", font=FONT_HEADING, bg=ACCENT, fg="white",
                  activebackground=ACCENT_DARK, relief="flat", padx=10, pady=8,
                  command=self.attempt_login).pack(fill="x")

        tk.Button(card, text="Create an account", font=FONT_SMALL, bg=BG_CARD, fg=ACCENT_DARK,
                  relief="flat", command=lambda: controller.show_frame(RegisterPage)).pack(pady=(15, 0))

    def attempt_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        success, result = auth.login_user(username, password)
        if success:
            self.controller.current_user = result
            self.controller.show_frame(DashboardPage)
        else:
            messagebox.showerror("Login Failed", result)


# =================================================================
# REGISTER PAGE
# =================================================================
class RegisterPage(tk.Frame):
    def __init__(self, parent, controller: MindNestApp):
        super().__init__(parent, bg=BG_MAIN)
        self.controller = controller

        card = tk.Frame(self, bg=BG_CARD, padx=40, pady=30)
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(card, text="Create your MindNest account", font=FONT_HEADING,
                 bg=BG_CARD, fg=ACCENT_DARK).pack(pady=(0, 20))

        fields = [("Full Name", False), ("Username", False), ("Email", False), ("Password", True)]
        self.entries = {}
        for label, is_password in fields:
            tk.Label(card, text=label, font=FONT_BODY, bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w")
            entry = tk.Entry(card, font=FONT_BODY, width=32, show="*" if is_password else "")
            entry.pack(pady=(0, 10))
            self.entries[label] = entry

        tk.Button(card, text="Register", font=FONT_HEADING, bg=ACCENT, fg="white",
                  relief="flat", padx=10, pady=8, command=self.attempt_register).pack(fill="x", pady=(10, 0))

        tk.Button(card, text="Back to Login", font=FONT_SMALL, bg=BG_CARD, fg=ACCENT_DARK,
                  relief="flat", command=lambda: controller.show_frame(LoginPage)).pack(pady=(15, 0))

    def attempt_register(self):
        full_name = self.entries["Full Name"].get().strip()
        username = self.entries["Username"].get().strip()
        email = self.entries["Email"].get().strip()
        password = self.entries["Password"].get()

        success, message = auth.register_user(username, email, password, full_name)
        if success:
            messagebox.showinfo("Success", message)
            self.controller.show_frame(LoginPage)
        else:
            messagebox.showerror("Registration Failed", message)


# =================================================================
# DASHBOARD PAGE (with sidebar navigation)
# =================================================================
class DashboardPage(tk.Frame):
    def __init__(self, parent, controller: MindNestApp):
        super().__init__(parent, bg=BG_MAIN)
        self.controller = controller
        user = controller.current_user

        # --- Sidebar ---
        sidebar = tk.Frame(self, bg=ACCENT_DARK, width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="🌿 MindNest", font=("Georgia", 16, "bold"),
                 bg=ACCENT_DARK, fg="white").pack(pady=(25, 5))
        tk.Label(sidebar, text=f"Hi, {user['full_name'] or user['username']}!", font=FONT_SMALL,
                 bg=ACCENT_DARK, fg="#DDEFE2", wraplength=180).pack(pady=(0, 25))

        nav_items = [
            ("🏠  Home", HomeTab),
            ("📝  Mood Check-in", MoodTab),
            ("📊  Progress", ProgressTab),
            ("🧘  Meditation", MeditationTab),
            ("🎧  Nature Sounds", SoundsTab),
            ("📔  Journal", JournalTab),
            ("👤  Profile", ProfileTab),
        ]
        self.content_area = tk.Frame(self, bg=BG_MAIN)
        self.content_area.pack(side="right", fill="both", expand=True)

        for label, tab_class in nav_items:
            tk.Button(sidebar, text=label, font=FONT_BODY, bg=ACCENT_DARK, fg="white",
                      activebackground=ACCENT, relief="flat", anchor="w", padx=20, pady=10,
                      command=lambda t=tab_class: self.load_tab(t)).pack(fill="x")

        tk.Button(sidebar, text="🚪  Log Out", font=FONT_BODY, bg=ACCENT_DARK, fg="#F3D2D2",
                  relief="flat", anchor="w", padx=20, pady=10,
                  command=controller.logout).pack(fill="x", side="bottom", pady=20)

        self.load_tab(HomeTab)

    def load_tab(self, tab_class):
        for widget in self.content_area.winfo_children():
            widget.destroy()
        tab_class(self.content_area, self.controller).pack(fill="both", expand=True, padx=30, pady=25)


# =================================================================
# HOME TAB - quote of the day + affirmation + quick mood glance
# =================================================================
class HomeTab(tk.Frame):
    def __init__(self, parent, controller: MindNestApp):
        super().__init__(parent, bg=BG_MAIN)
        user = controller.current_user

        tk.Label(self, text=f"Welcome back, {user['full_name'] or user['username']} 🌸",
                 font=FONT_TITLE, bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w", pady=(0, 20))

        quote = quotes.get_quote_of_the_day()
        quote_card = tk.Frame(self, bg=BG_CARD, padx=25, pady=20)
        quote_card.pack(fill="x", pady=(0, 15))
        tk.Label(quote_card, text="✨ Quote of the Day", font=FONT_HEADING, bg=BG_CARD, fg=ACCENT_DARK).pack(anchor="w")
        tk.Label(quote_card, text=f'"{quote["quote_text"]}"', font=("Segoe UI", 12, "italic"),
                 bg=BG_CARD, fg=TEXT_DARK, wraplength=600, justify="left").pack(anchor="w", pady=(8, 2))
        tk.Label(quote_card, text=f"— {quote['author']}", font=FONT_SMALL, bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w")

        affirmation = quotes.get_affirmation_of_the_day()
        affirm_card = tk.Frame(self, bg=BG_CARD, padx=25, pady=20)
        affirm_card.pack(fill="x", pady=(0, 15))
        tk.Label(affirm_card, text="💚 Today's Affirmation", font=FONT_HEADING, bg=BG_CARD, fg=ACCENT_DARK).pack(anchor="w")
        tk.Label(affirm_card, text=affirmation, font=FONT_BODY, bg=BG_CARD, fg=TEXT_DARK,
                 wraplength=600, justify="left").pack(anchor="w", pady=(8, 0))

        history = mood.get_mood_history(user["user_id"], limit=1)
        status_card = tk.Frame(self, bg=BG_CARD, padx=25, pady=20)
        status_card.pack(fill="x")
        tk.Label(status_card, text="Today's Status", font=FONT_HEADING, bg=BG_CARD, fg=ACCENT_DARK).pack(anchor="w")
        today = datetime.now().strftime("%Y-%m-%d")
        if history and str(history[0]["entry_date"]) == today:
            m = history[0]
            emoji = mood.MOODS.get(m["mood_name"], {}).get("emoji", "")
            tk.Label(status_card, text=f"You checked in today: {emoji} {m['mood_name']}",
                     font=FONT_BODY, bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w", pady=(8, 0))
        else:
            tk.Label(status_card, text="You haven't checked in today yet. Head to Mood Check-in!",
                     font=FONT_BODY, bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w", pady=(8, 0))


# =================================================================
# MOOD CHECK-IN TAB
# =================================================================
class MoodTab(tk.Frame):
    def __init__(self, parent, controller: MindNestApp):
        super().__init__(parent, bg=BG_MAIN)
        self.controller = controller
        self.selected_mood = tk.StringVar(value="")

        tk.Label(self, text="How are you feeling today?", font=FONT_TITLE,
                 bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w", pady=(0, 20))

        mood_grid = tk.Frame(self, bg=BG_MAIN)
        mood_grid.pack(anchor="w", pady=(0, 20))

        for i, (name, data) in enumerate(mood.MOODS.items()):
            btn = tk.Radiobutton(
                mood_grid, text=f"{data['emoji']}\n{name}", variable=self.selected_mood, value=name,
                font=FONT_BODY, bg=BG_CARD, fg=TEXT_DARK, selectcolor=ACCENT,
                indicatoron=False, width=10, height=3, relief="flat", padx=5, pady=5
            )
            btn.grid(row=0, column=i, padx=6)

        tk.Label(self, text="Notes (optional)", font=FONT_BODY, bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w")
        self.notes_text = tk.Text(self, height=4, width=60, font=FONT_BODY)
        self.notes_text.pack(anchor="w", pady=(5, 15))

        tk.Button(self, text="Submit Check-in", font=FONT_HEADING, bg=ACCENT, fg="white",
                  relief="flat", padx=15, pady=8, command=self.submit).pack(anchor="w")

        self.tips_frame = tk.Frame(self, bg=BG_MAIN)
        self.tips_frame.pack(fill="x", pady=(25, 0), anchor="w")

    def submit(self):
        chosen = self.selected_mood.get()
        if not chosen:
            messagebox.showwarning("No mood selected", "Please select a mood first.")
            return
        notes = self.notes_text.get("1.0", "end").strip()
        success, message = mood.submit_mood_checkin(self.controller.current_user["user_id"], chosen, notes)
        if success:
            self.show_tips(chosen)
        else:
            messagebox.showerror("Error", message)

    def show_tips(self, mood_name):
        for widget in self.tips_frame.winfo_children():
            widget.destroy()

        tk.Label(self.tips_frame, text=f"💡 Self-Care Tips for feeling {mood_name}",
                 font=FONT_HEADING, bg=BG_MAIN, fg=ACCENT_DARK).pack(anchor="w", pady=(0, 8))
        for tip in mood.get_self_care_tips(mood_name):
            tk.Label(self.tips_frame, text=f"• {tip}", font=FONT_BODY, bg=BG_MAIN, fg=TEXT_DARK,
                     wraplength=650, justify="left").pack(anchor="w", pady=2)


# =================================================================
# PROGRESS TAB - mood history + meditation stats
# =================================================================
class ProgressTab(tk.Frame):
    def __init__(self, parent, controller: MindNestApp):
        super().__init__(parent, bg=BG_MAIN)
        user_id = controller.current_user["user_id"]

        tk.Label(self, text="Your Progress Dashboard", font=FONT_TITLE,
                 bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w", pady=(0, 20))

        stats_frame = tk.Frame(self, bg=BG_MAIN)
        stats_frame.pack(fill="x", pady=(0, 20))

        total_minutes = meditation.get_total_meditation_minutes(user_id)
        journal_count = len(journal.get_journal_entries(user_id, limit=1000))
        mood_count = len(mood.get_mood_history(user_id, limit=1000))

        for label, value in [
            ("Mood Check-ins", mood_count),
            ("Meditation Minutes", total_minutes),
            ("Journal Entries", journal_count),
        ]:
            card = tk.Frame(stats_frame, bg=BG_CARD, padx=20, pady=15, width=180)
            card.pack(side="left", padx=(0, 15))
            tk.Label(card, text=str(value), font=("Segoe UI", 22, "bold"), bg=BG_CARD, fg=ACCENT_DARK).pack()
            tk.Label(card, text=label, font=FONT_SMALL, bg=BG_CARD, fg=TEXT_MUTED).pack()

        tk.Label(self, text="Mood History (most recent first)", font=FONT_HEADING,
                 bg=BG_MAIN, fg=ACCENT_DARK).pack(anchor="w", pady=(10, 8))

        history_frame = tk.Frame(self, bg=BG_CARD)
        history_frame.pack(fill="both", expand=True)

        columns = ("date", "mood", "notes")
        tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=12)
        tree.heading("date", text="Date")
        tree.heading("mood", text="Mood")
        tree.heading("notes", text="Notes")
        tree.column("date", width=110)
        tree.column("mood", width=100)
        tree.column("notes", width=400)
        tree.pack(fill="both", expand=True)

        for entry in mood.get_mood_history(user_id, limit=100):
            emoji = mood.MOODS.get(entry["mood_name"], {}).get("emoji", "")
            tree.insert("", "end", values=(entry["entry_date"], f"{emoji} {entry['mood_name']}", entry["notes"] or ""))


# =================================================================
# MEDITATION TAB - simple countdown timer with guided script
# =================================================================
class MeditationTab(tk.Frame):
    DURATIONS = [1, 3, 5, 10, 15]  # minutes

    def __init__(self, parent, controller: MindNestApp):
        super().__init__(parent, bg=BG_MAIN)
        self.controller = controller
        self.remaining_seconds = 0
        self.total_seconds = 0
        self.timer_running = False
        self.after_id = None

        tk.Label(self, text="Guided Meditation Timer", font=FONT_TITLE,
                 bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w", pady=(0, 20))

        duration_frame = tk.Frame(self, bg=BG_MAIN)
        duration_frame.pack(anchor="w", pady=(0, 20))
        tk.Label(duration_frame, text="Choose duration:", font=FONT_BODY, bg=BG_MAIN, fg=TEXT_DARK).pack(side="left")

        self.duration_var = tk.IntVar(value=5)
        for d in self.DURATIONS:
            tk.Radiobutton(duration_frame, text=f"{d} min", variable=self.duration_var, value=d,
                            font=FONT_BODY, bg=BG_MAIN, fg=TEXT_DARK, selectcolor=ACCENT).pack(side="left", padx=8)

        self.timer_label = tk.Label(self, text="05:00", font=("Segoe UI", 48, "bold"),
                                     bg=BG_MAIN, fg=ACCENT_DARK)
        self.timer_label.pack(pady=20)

        self.script_label = tk.Label(self, text="Press Start when you're ready.", font=("Segoe UI", 13, "italic"),
                                      bg=BG_MAIN, fg=TEXT_DARK, wraplength=600)
        self.script_label.pack(pady=(0, 20))

        btn_frame = tk.Frame(self, bg=BG_MAIN)
        btn_frame.pack()
        self.start_btn = tk.Button(btn_frame, text="Start", font=FONT_HEADING, bg=ACCENT, fg="white",
                                    relief="flat", padx=20, pady=8, command=self.start_timer)
        self.start_btn.pack(side="left", padx=5)
        tk.Button(btn_frame, text="Reset", font=FONT_HEADING, bg=TEXT_MUTED, fg="white",
                  relief="flat", padx=20, pady=8, command=self.reset_timer).pack(side="left", padx=5)

    def start_timer(self):
        if self.timer_running:
            return
        self.total_seconds = self.duration_var.get() * 60
        self.remaining_seconds = self.total_seconds
        self.timer_running = True
        self.tick()

    def tick(self):
        if self.remaining_seconds <= 0:
            self.timer_running = False
            self.timer_label.config(text="00:00")
            self.script_label.config(text="Session complete. Well done. 🌿")
            meditation.log_meditation_session(self.controller.current_user["user_id"], self.total_seconds // 60)
            return

        mins, secs = divmod(self.remaining_seconds, 60)
        self.timer_label.config(text=f"{mins:02d}:{secs:02d}")

        elapsed = self.total_seconds - self.remaining_seconds
        for cue_time, text in meditation.GUIDED_SCRIPT:
            if elapsed == cue_time:
                self.script_label.config(text=text)

        self.remaining_seconds -= 1
        self.after_id = self.after(1000, self.tick)

    def reset_timer(self):
        if self.after_id:
            self.after_cancel(self.after_id)
        self.timer_running = False
        self.remaining_seconds = 0
        self.timer_label.config(text=f"{self.duration_var.get():02d}:00")
        self.script_label.config(text="Press Start when you're ready.")


# =================================================================
# NATURE SOUNDS TAB
# =================================================================
class SoundsTab(tk.Frame):
    def __init__(self, parent, controller: MindNestApp):
        super().__init__(parent, bg=BG_MAIN)

        tk.Label(self, text="Peaceful Nature Sounds", font=FONT_TITLE,
                 bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w", pady=(0, 20))
        tk.Label(self, text="Add your own audio files to the assets/sounds/ folder to enable playback.",
                 font=FONT_SMALL, bg=BG_MAIN, fg=TEXT_MUTED, wraplength=600).pack(anchor="w", pady=(0, 15))

        sounds_list = sounds.get_all_sounds()
        for s in sounds_list:
            row = tk.Frame(self, bg=BG_CARD, padx=15, pady=12)
            row.pack(fill="x", pady=5)
            tk.Label(row, text=s["sound_name"], font=FONT_BODY, bg=BG_CARD, fg=TEXT_DARK).pack(side="left")
            tk.Button(row, text="▶ Play", font=FONT_SMALL, bg=ACCENT, fg="white", relief="flat",
                      padx=10, command=lambda p=s["file_path"]: sounds.play_sound(p)).pack(side="right", padx=5)
            tk.Button(row, text="⏹ Stop", font=FONT_SMALL, bg=TEXT_MUTED, fg="white", relief="flat",
                      padx=10, command=sounds.stop_sound).pack(side="right")

        vol_frame = tk.Frame(self, bg=BG_MAIN)
        vol_frame.pack(fill="x", pady=(20, 0))
        tk.Label(vol_frame, text="Volume", font=FONT_BODY, bg=BG_MAIN, fg=TEXT_DARK).pack(side="left")
        vol_slider = tk.Scale(vol_frame, from_=0, to=100, orient="horizontal", bg=BG_MAIN,
                               command=lambda v: sounds.set_volume(int(v) / 100))
        vol_slider.set(70)
        vol_slider.pack(side="left", padx=10, fill="x", expand=True)


# =================================================================
# JOURNAL TAB
# =================================================================
class JournalTab(tk.Frame):
    def __init__(self, parent, controller: MindNestApp):
        super().__init__(parent, bg=BG_MAIN)
        self.controller = controller

        tk.Label(self, text="Personal Journal", font=FONT_TITLE,
                 bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w", pady=(0, 20))

        form = tk.Frame(self, bg=BG_CARD, padx=20, pady=15)
        form.pack(fill="x", pady=(0, 20))

        tk.Label(form, text="Title (optional)", font=FONT_BODY, bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w")
        self.title_entry = tk.Entry(form, font=FONT_BODY, width=50)
        self.title_entry.pack(anchor="w", pady=(0, 10))

        tk.Label(form, text="What's on your mind?", font=FONT_BODY, bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w")
        self.entry_text = tk.Text(form, height=6, width=60, font=FONT_BODY)
        self.entry_text.pack(anchor="w", pady=(0, 10))

        tk.Button(form, text="Save Entry", font=FONT_HEADING, bg=ACCENT, fg="white",
                  relief="flat", padx=15, pady=6, command=self.save_entry).pack(anchor="w")

        tk.Label(self, text="Past Entries", font=FONT_HEADING, bg=BG_MAIN, fg=ACCENT_DARK).pack(anchor="w", pady=(10, 8))

        self.entries_frame = tk.Frame(self, bg=BG_MAIN)
        self.entries_frame.pack(fill="both", expand=True)
        self.refresh_entries()

    def save_entry(self):
        title = self.title_entry.get().strip()
        text = self.entry_text.get("1.0", "end").strip()
        success, message = journal.add_journal_entry(self.controller.current_user["user_id"], text, title)
        if success:
            self.title_entry.delete(0, "end")
            self.entry_text.delete("1.0", "end")
            self.refresh_entries()
        else:
            messagebox.showwarning("Journal", message)

    def refresh_entries(self):
        for widget in self.entries_frame.winfo_children():
            widget.destroy()

        entries = journal.get_journal_entries(self.controller.current_user["user_id"], limit=20)
        if not entries:
            tk.Label(self.entries_frame, text="No entries yet. Start writing above.",
                     font=FONT_BODY, bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w")
            return

        canvas = tk.Canvas(self.entries_frame, bg=BG_MAIN, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.entries_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=BG_MAIN)
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for e in entries:
            card = tk.Frame(scroll_frame, bg=BG_CARD, padx=15, pady=10)
            card.pack(fill="x", pady=5, padx=2)
            header = f"{e['title'] or 'Untitled'}  ·  {e['entry_date']}"
            tk.Label(card, text=header, font=("Segoe UI", 10, "bold"), bg=BG_CARD, fg=ACCENT_DARK).pack(anchor="w")
            tk.Label(card, text=e["entry_text"], font=FONT_BODY, bg=BG_CARD, fg=TEXT_DARK,
                     wraplength=650, justify="left").pack(anchor="w", pady=(4, 0))


# =================================================================
# PROFILE TAB
# =================================================================
class ProfileTab(tk.Frame):
    def __init__(self, parent, controller: MindNestApp):
        super().__init__(parent, bg=BG_MAIN)
        self.controller = controller
        user_id = controller.current_user["user_id"]
        profile = profile_manager.get_profile(user_id) or {}

        tk.Label(self, text="Your Profile", font=FONT_TITLE, bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w", pady=(0, 20))

        form = tk.Frame(self, bg=BG_CARD, padx=25, pady=20)
        form.pack(fill="x", pady=(0, 20))

        tk.Label(form, text="Full Name", font=FONT_BODY, bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w")
        self.name_entry = tk.Entry(form, font=FONT_BODY, width=40)
        self.name_entry.insert(0, profile.get("full_name") or "")
        self.name_entry.pack(anchor="w", pady=(0, 10))

        tk.Label(form, text="Email", font=FONT_BODY, bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w")
        self.email_entry = tk.Entry(form, font=FONT_BODY, width=40)
        self.email_entry.insert(0, profile.get("email") or "")
        self.email_entry.pack(anchor="w", pady=(0, 15))

        tk.Button(form, text="Update Profile", font=FONT_HEADING, bg=ACCENT, fg="white",
                  relief="flat", padx=15, pady=6, command=self.update_profile).pack(anchor="w")

        pw_form = tk.Frame(self, bg=BG_CARD, padx=25, pady=20)
        pw_form.pack(fill="x")

        tk.Label(pw_form, text="Change Password", font=FONT_HEADING, bg=BG_CARD, fg=ACCENT_DARK).pack(anchor="w", pady=(0, 10))
        tk.Label(pw_form, text="Current Password", font=FONT_BODY, bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w")
        self.old_pw_entry = tk.Entry(pw_form, font=FONT_BODY, width=40, show="*")
        self.old_pw_entry.pack(anchor="w", pady=(0, 10))

        tk.Label(pw_form, text="New Password", font=FONT_BODY, bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w")
        self.new_pw_entry = tk.Entry(pw_form, font=FONT_BODY, width=40, show="*")
        self.new_pw_entry.pack(anchor="w", pady=(0, 15))

        tk.Button(pw_form, text="Change Password", font=FONT_HEADING, bg=ACCENT_DARK, fg="white",
                  relief="flat", padx=15, pady=6, command=self.change_password).pack(anchor="w")

    def update_profile(self):
        success, message = profile_manager.update_profile(
            self.controller.current_user["user_id"],
            full_name=self.name_entry.get().strip(),
            email=self.email_entry.get().strip()
        )
        if success:
            self.controller.current_user["full_name"] = self.name_entry.get().strip()
            messagebox.showinfo("Profile", message)
        else:
            messagebox.showerror("Profile", message)

    def change_password(self):
        success, message = profile_manager.change_password(
            self.controller.current_user["user_id"],
            self.old_pw_entry.get(),
            self.new_pw_entry.get()
        )
        if success:
            self.old_pw_entry.delete(0, "end")
            self.new_pw_entry.delete(0, "end")
        messagebox.showinfo("Password", message) if success else messagebox.showerror("Password", message)


if __name__ == "__main__":
    app = MindNestApp()
    app.mainloop()

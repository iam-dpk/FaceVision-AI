import tkinter as tk
from tkinter import ttk, messagebox
from src.config import load_config, save_config

class SettingsView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Settings")
        self.geometry("500x360")
        c = load_config()

        tk.Label(self, text="Application Settings",
                 font=("Segoe UI", 19, "bold")).pack(pady=(20, 15))
        form = tk.Frame(self)
        form.pack()

        fields = [
            ("Camera index", "camera", c["camera_index"]),
            ("Recognition threshold", "threshold", c["recognition_threshold"]),
            ("Attendance cooldown (min)", "cooldown", c["attendance_cooldown_minutes"]),
        ]
        self.entries = {}
        for row, (label, key, value) in enumerate(fields):
            tk.Label(form, text=label).grid(row=row, column=0, sticky="e", padx=10, pady=10)
            e = tk.Entry(form, width=25)
            e.insert(0, str(value))
            e.grid(row=row, column=1, pady=10)
            self.entries[key] = e

        tk.Label(self, text="Tip: If your webcam does not open, try camera index 1.",
                 fg="#64748b").pack(pady=10)
        ttk.Button(self, text="Save Settings", command=self.save).pack(pady=12)

    def save(self):
        try:
            c = load_config()
            c["camera_index"] = int(self.entries["camera"].get())
            c["recognition_threshold"] = float(self.entries["threshold"].get())
            c["attendance_cooldown_minutes"] = int(self.entries["cooldown"].get())
            if not 0 <= c["recognition_threshold"] <= 1:
                raise ValueError("Threshold must be between 0 and 1.")
            if c["camera_index"] < 0:
                raise ValueError("Camera index must be 0 or higher.")
            save_config(c)
            messagebox.showinfo("Saved", "Settings updated.", parent=self)
            self.destroy()
        except ValueError as exc:
            messagebox.showerror("Invalid Settings", str(exc), parent=self)

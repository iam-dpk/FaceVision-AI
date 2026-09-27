import tkinter as tk
from tkinter import ttk, messagebox
from src.database import init_db, list_persons, list_attendance
from src.demo import seed_demo
from src.exporter import export_csv
from src.report_generator import generate_report
from .registration import RegistrationView
from .attendance_view import AttendanceView
from .face_manager import FaceManager
from .settings import SettingsView
from .live_view import LiveView

class Dashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        init_db()
        self.title("FaceVision AI — Face Recognition & Attendance")
        self.geometry("1180x760")
        self.minsize(1000, 650)
        self.configure(bg="#0f1720")
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass
        self.style.configure("TButton", padding=9, font=("Segoe UI", 10))
        self.style.configure("Treeview", rowheight=30)
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        self._build()

    def _build(self):
        sidebar = tk.Frame(self, bg="#17212b", width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="FaceVision AI", bg="#17212b", fg="#4ade80",
                 font=("Segoe UI", 20, "bold")).pack(pady=(28, 3))
        tk.Label(sidebar, text="Smart Face Attendance", bg="#17212b", fg="#94a3b8",
                 font=("Segoe UI", 9)).pack(pady=(0, 25))

        buttons = [
            ("Dashboard", self.refresh),
            ("Live Recognition", self.live),
            ("Register Face", self.register),
            ("Attendance", self.attendance),
            ("Face Manager", self.faces),
            ("Settings", self.settings),
        ]
        for label, command in buttons:
            ttk.Button(sidebar, text=label, command=command).pack(
                fill="x", padx=18, pady=5
            )

        ttk.Separator(sidebar).pack(fill="x", padx=18, pady=20)
        ttk.Button(sidebar, text="Seed Demo Data", command=self.demo).pack(fill="x", padx=18, pady=5)
        ttk.Button(sidebar, text="Export CSV", command=self.export).pack(fill="x", padx=18, pady=5)
        ttk.Button(sidebar, text="Generate Report", command=self.report).pack(fill="x", padx=18, pady=5)

        main = tk.Frame(self, bg="#0f1720")
        main.pack(side="left", fill="both", expand=True, padx=28, pady=25)

        self.heading = tk.Label(main, text="Dashboard", bg="#0f1720", fg="#f8fafc",
                                font=("Segoe UI", 26, "bold"))
        self.heading.pack(anchor="w")
        self.subtitle = tk.Label(main, text="Local computer-vision attendance system",
                                 bg="#0f1720", fg="#94a3b8", font=("Segoe UI", 10))
        self.subtitle.pack(anchor="w", pady=(2, 18))

        self.cards = tk.Frame(main, bg="#0f1720")
        self.cards.pack(fill="x", pady=(0, 20))
        self.body = tk.Frame(main, bg="#0f1720")
        self.body.pack(fill="both", expand=True)
        self.refresh()

    def clear_body(self):
        for w in self.body.winfo_children():
            w.destroy()

    def refresh(self):
        self.heading.config(text="Dashboard")
        self.subtitle.config(text="Local computer-vision attendance system")
        for w in self.cards.winfo_children():
            w.destroy()

        people, records = list_persons(), list_attendance()
        metrics = [
            ("Registered Faces", len(people)),
            ("Attendance Records", len(records)),
            ("System", "READY"),
        ]
        for title, value in metrics:
            f = tk.Frame(self.cards, bg="#17212b", height=105)
            f.pack(side="left", fill="x", expand=True, padx=5)
            tk.Label(f, text=title, bg="#17212b", fg="#94a3b8",
                     font=("Segoe UI", 10)).pack(anchor="w", padx=18, pady=(17, 3))
            tk.Label(f, text=str(value), bg="#17212b", fg="#f8fafc",
                     font=("Segoe UI", 21, "bold")).pack(anchor="w", padx=18)

        self.clear_body()
        tk.Label(self.body, text="Recent Attendance", bg="#0f1720", fg="#f8fafc",
                 font=("Segoe UI", 15, "bold")).pack(anchor="w", pady=(0, 10))

        tree = ttk.Treeview(self.body, columns=("pid","name","time","status"), show="headings")
        for c, t in zip(("pid","name","time","status"),
                        ("Person ID","Name","Timestamp","Status")):
            tree.heading(c, text=t)
            tree.column(c, width=190)
        tree.pack(fill="both", expand=True)
        for _, pid, name, ts, status in records[:30]:
            tree.insert("", "end", values=(pid, name, ts, status))

    def live(self):
        LiveView(self, self.refresh)

    def register(self):
        RegistrationView(self, self.refresh)

    def attendance(self):
        AttendanceView(self)

    def faces(self):
        FaceManager(self, self.refresh)

    def settings(self):
        SettingsView(self)

    def demo(self):
        seed_demo()
        self.refresh()
        messagebox.showinfo("Demo Data", "Sample data has been added.")

    def report(self):
        p = generate_report()
        messagebox.showinfo("Report Generated", str(p))

    def export(self):
        p = export_csv()
        messagebox.showinfo("CSV Exported", str(p))

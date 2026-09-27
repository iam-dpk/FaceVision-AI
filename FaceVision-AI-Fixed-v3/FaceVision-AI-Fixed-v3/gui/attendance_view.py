import tkinter as tk
from tkinter import ttk
from src.database import list_attendance

class AttendanceView(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent); self.title("Attendance"); self.geometry("900x520")
        top=tk.Frame(self); top.pack(fill="x",padx=15,pady=15)
        tk.Label(top,text="Search").pack(side="left")
        self.query=tk.Entry(top,width=35); self.query.pack(side="left",padx=8)
        ttk.Button(top,text="Filter",command=self.refresh).pack(side="left")
        self.tree=ttk.Treeview(self,columns=("rid","pid","name","time","status"),show="headings")
        for c,t in zip(self.tree["columns"],("Record","Person ID","Name","Timestamp","Status")):
            self.tree.heading(c,text=t); self.tree.column(c,width=150)
        self.tree.pack(fill="both",expand=True,padx=15,pady=10)
        self.refresh()
    def refresh(self):
        for x in self.tree.get_children(): self.tree.delete(x)
        for row in list_attendance(self.query.get().strip()):
            self.tree.insert("", "end", values=row)

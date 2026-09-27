import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from src.database import list_persons, remove_person

class FaceManager(tk.Toplevel):
    def __init__(self, parent, on_done):
        super().__init__(parent)
        self.title("Face Manager")
        self.geometry("820x520")
        self.on_done = on_done

        self.tree = ttk.Treeview(
            self, columns=("pid","name","created"), show="headings"
        )
        for c, t in zip(self.tree["columns"], ("Person ID","Name","Created")):
            self.tree.heading(c, text=t)
            self.tree.column(c, width=240)
        self.tree.pack(fill="both", expand=True, padx=15, pady=15)

        ttk.Button(self, text="Delete Selected", command=self.delete).pack(pady=(0, 15))
        self.refresh()

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for pid, name, _, _, created in list_persons():
            self.tree.insert("", "end", iid=pid, values=(pid, name, created))

    def delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Select a registered person first.", parent=self)
            return
        pid = selected[0]
        row = next((r for r in list_persons() if r[0] == pid), None)
        if not row:
            return
        if messagebox.askyesno("Confirm Delete",
                               f"Delete {row[1]} ({pid})?", parent=self):
            for p in (row[2], row[3]):
                if p:
                    try: Path(p).unlink(missing_ok=True)
                    except OSError: pass
            remove_person(pid)
            self.refresh()
            self.on_done()

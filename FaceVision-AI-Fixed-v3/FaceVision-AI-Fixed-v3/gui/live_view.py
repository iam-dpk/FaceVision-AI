import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from src.live_recognition import LiveRecognition

class LiveView(tk.Toplevel):
    def __init__(self, parent, on_close=None):
        super().__init__(parent)
        self.parent = parent
        self.on_close = on_close
        self.title("FaceVision AI — Live Recognition")
        self.geometry("980x700")
        self.configure(bg="#0f1720")
        self.protocol("WM_DELETE_WINDOW", self.close)

        tk.Label(self, text="Live Recognition", bg="#0f1720", fg="#f8fafc",
                 font=("Segoe UI", 20, "bold")).pack(anchor="w", padx=20, pady=(15, 2))
        tk.Label(self, text="Press Stop or close this window to release the camera.",
                 bg="#0f1720", fg="#94a3b8").pack(anchor="w", padx=20)

        self.preview = tk.Label(self, bg="black")
        self.preview.pack(fill="both", expand=True, padx=20, pady=15)

        bottom = tk.Frame(self, bg="#0f1720")
        bottom.pack(fill="x", padx=20, pady=(0, 15))
        self.status = tk.Label(bottom, text="Starting camera...", bg="#0f1720",
                               fg="#4ade80", font=("Segoe UI", 10))
        self.status.pack(side="left")
        ttk.Button(bottom, text="Stop Camera", command=self.close).pack(side="right")

        self.engine = LiveRecognition(self.event)
        try:
            self.engine.start()
        except Exception as exc:
            messagebox.showerror("Camera Error", str(exc), parent=self)
            self.destroy()
            return
        self.after(30, self.update_frame)

    def event(self, message):
        self.status.config(text=message)

    def update_frame(self):
        if not self.winfo_exists() or not self.engine.running:
            return
        result = self.engine.read()
        if result is None:
            self.status.config(text="Camera frame unavailable.")
            self.after(100, self.update_frame)
            return

        frame, results = result
        import cv2
        for box, name, pid, score in results:
            x, y, w, h = map(int, box)
            known = pid is not None
            cv2.rectangle(frame, (x,y), (x+w,y+h),
                          (70, 220, 120) if known else (70, 80, 255), 2)
            label = f"{name} | {score:.2f}"
            cv2.rectangle(frame, (x, max(0,y-30)), (x+w, y), (20,25,30), -1)
            cv2.putText(frame, label, (x+5, y-8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255,255,255), 1, cv2.LINE_AA)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb)
        max_w = max(600, self.preview.winfo_width())
        max_h = max(400, self.preview.winfo_height())
        img.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        self.preview.configure(image=photo)
        self.preview.image = photo
        self.status.config(text=f"Camera running • {len(results)} face(s) detected")
        self.after(30, self.update_frame)

    def close(self):
        try:
            self.engine.stop()
        finally:
            if self.on_close:
                self.on_close()
            self.destroy()

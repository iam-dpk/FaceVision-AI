import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import cv2
from src.config import FACES_DIR
from src.database import add_person
from src.face_detector import FaceDetector
from src.face_encoder import FaceEncoder

class RegistrationView(tk.Toplevel):
    def __init__(self, parent, on_done):
        super().__init__(parent)
        self.title("Register Face")
        self.geometry("560x400")
        self.on_done = on_done
        self.detector = FaceDetector()
        self.encoder = FaceEncoder()
        self.image_path = None

        tk.Label(self, text="Register a Face", font=("Segoe UI", 20, "bold")).pack(pady=(20, 5))
        tk.Label(self, text="Use a clear, front-facing image with one person.",
                 fg="#64748b").pack(pady=(0, 15))

        form = tk.Frame(self)
        form.pack()
        tk.Label(form, text="Person ID").grid(row=0, column=0, sticky="e", padx=10, pady=9)
        self.pid = tk.Entry(form, width=34)
        self.pid.grid(row=0, column=1, pady=9)
        tk.Label(form, text="Name").grid(row=1, column=0, sticky="e", padx=10, pady=9)
        self.name = tk.Entry(form, width=34)
        self.name.grid(row=1, column=1, pady=9)

        ttk.Button(self, text="Choose Face Image", command=self.choose).pack(pady=10)
        self.status = tk.Label(self, text="No image selected", fg="#64748b")
        self.status.pack()

        ttk.Button(self, text="Register Face", command=self.register).pack(pady=22)

    def choose(self):
        p = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if p:
            self.image_path = p
            self.status.config(text=Path(p).name)

    def register(self):
        pid, name = self.pid.get().strip(), self.name.get().strip()
        if not pid or not name or not self.image_path:
            messagebox.showwarning("Missing Information",
                                   "Enter Person ID, Name and choose an image.", parent=self)
            return

        image = cv2.imread(self.image_path)
        if image is None:
            messagebox.showerror("Image Error", "The selected image could not be opened.", parent=self)
            return

        faces = self.detector.detect(image)
        if len(faces) != 1:
            messagebox.showwarning(
                "Face Detection",
                f"Expected exactly 1 face, but detected {len(faces)}. "
                "Use a clear image containing one face.",
                parent=self
            )
            return

        face = self.encoder.crop(image, faces[0])
        dst = FACES_DIR / f"{pid}.jpg"
        emb = FACES_DIR / f"{pid}.npy"
        cv2.imwrite(str(dst), face)
        self.encoder.save(self.encoder.encode(face), emb)
        add_person(pid, name, str(dst), str(emb))
        self.on_done()
        messagebox.showinfo("Success", f"{name} has been registered.", parent=self)
        self.destroy()

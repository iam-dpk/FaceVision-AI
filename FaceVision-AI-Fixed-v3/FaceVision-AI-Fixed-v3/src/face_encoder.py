import cv2
import numpy as np

class FaceEncoder:
    """Dependency-light deterministic face descriptor.

    This is suitable for a local portfolio/demo application.
    For production biometrics, replace this class with a validated deep
    embedding model while keeping its encode/save/load interface.
    """
    def __init__(self, size=(80, 80)):
        self.size = size

    def crop(self, frame, box, padding=0.15):
        x, y, w, h = [int(v) for v in box]
        px, py = int(w * padding), int(h * padding)
        x1, y1 = max(0, x-px), max(0, y-py)
        x2, y2 = min(frame.shape[1], x+w+px), min(frame.shape[0], y+h+py)
        return frame[y1:y2, x1:x2]

    def encode(self, face):
        if face is None or face.size == 0:
            raise ValueError("Empty face image")
        gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY) if face.ndim == 3 else face
        gray = cv2.resize(gray, self.size, interpolation=cv2.INTER_AREA)
        gray = cv2.equalizeHist(gray)
        # Histogram equalized pixels + gradient magnitude descriptor.
        pixels = gray.astype(np.float32).reshape(-1)
        gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
        gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
        grad = cv2.magnitude(gx, gy).reshape(-1)
        vec = np.concatenate([pixels, grad]).astype(np.float32)
        vec -= vec.mean()
        norm = np.linalg.norm(vec)
        return vec / norm if norm > 1e-8 else vec

    def save(self, embedding, path):
        np.save(str(path), embedding)

    def load(self, path):
        return np.load(str(path))

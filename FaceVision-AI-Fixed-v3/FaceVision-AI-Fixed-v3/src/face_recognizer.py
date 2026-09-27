from pathlib import Path
import numpy as np
from .database import list_persons
from .face_encoder import FaceEncoder

class FaceRecognizer:
    def __init__(self, threshold=0.72):
        self.encoder = FaceEncoder()
        self.threshold = float(threshold)

    @staticmethod
    def similarity(a, b):
        a = np.asarray(a, dtype=np.float32)
        b = np.asarray(b, dtype=np.float32)
        denom = np.linalg.norm(a) * np.linalg.norm(b)
        return float(np.dot(a, b) / denom) if denom else -1.0

    def recognize(self, face):
        probe = self.encoder.encode(face)
        best = ("Unknown", None, -1.0)
        for pid, name, _, emb_path, _ in list_persons():
            if not emb_path or not Path(emb_path).exists():
                continue
            try:
                score = self.similarity(probe, self.encoder.load(emb_path))
            except Exception:
                continue
            if score > best[2]:
                best = (name, pid, score)
        return best if best[2] >= self.threshold else ("Unknown", None, best[2])

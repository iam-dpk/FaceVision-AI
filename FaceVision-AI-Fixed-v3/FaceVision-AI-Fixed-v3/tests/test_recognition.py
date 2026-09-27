import numpy as np
from src.face_recognizer import FaceRecognizer

def test_similarity():
    a = np.array([1., 0., 0.])
    b = np.array([1., 0., 0.])
    assert FaceRecognizer.similarity(a, b) > .99

def test_unknown():
    import src.face_recognizer as mod
    old = mod.list_persons
    mod.list_persons = lambda: []
    try:
        r = FaceRecognizer()
        name, pid, score = r.recognize(np.zeros((100,100,3), dtype=np.uint8))
        assert name == "Unknown"
        assert pid is None
    finally:
        mod.list_persons = old

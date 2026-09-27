import numpy as np
from src.face_detector import FaceDetector

def test_detector_loads():
    d=FaceDetector()
    assert d.classifier is not None

def test_detector_accepts_frame():
    d=FaceDetector()
    frame=np.zeros((240,320,3),dtype=np.uint8)
    result=d.detect(frame)
    assert hasattr(result, "__len__")

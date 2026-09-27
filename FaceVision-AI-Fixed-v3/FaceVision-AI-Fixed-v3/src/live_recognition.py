import cv2
from .attendance import mark_attendance
from .config import load_config
from .face_detector import FaceDetector
from .face_encoder import FaceEncoder
from .face_recognizer import FaceRecognizer

class LiveRecognition:
    def __init__(self, on_event=None):
        self.config = load_config()
        self.detector = FaceDetector()
        self.encoder = FaceEncoder()
        self.recognizer = FaceRecognizer(self.config["recognition_threshold"])
        self.on_event = on_event
        self.cap = None
        self.running = False

    def start(self):
        self.cap = cv2.VideoCapture(self.config["camera_index"], cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            self.cap.release()
            self.cap = cv2.VideoCapture(self.config["camera_index"])
        if not self.cap.isOpened():
            raise RuntimeError(
                f"Camera {self.config['camera_index']} could not be opened. "
                "Try Camera index 1 in Settings."
            )
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config["camera_width"])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config["camera_height"])
        self.running = True

    def read(self):
        if not self.running or self.cap is None:
            return None
        ok, frame = self.cap.read()
        if not ok:
            return None

        faces = self.detector.detect(frame)
        results = []
        for box in faces:
            face = self.encoder.crop(frame, box)
            name, pid, score = self.recognizer.recognize(face)
            if pid:
                added = mark_attendance(
                    pid, name, self.config["attendance_cooldown_minutes"]
                )
                if added and self.on_event:
                    self.on_event(f"Attendance marked: {name} ({pid})")
            results.append((box, name, pid, score))
        return frame, results

    def stop(self):
        self.running = False
        if self.cap is not None:
            self.cap.release()
            self.cap = None

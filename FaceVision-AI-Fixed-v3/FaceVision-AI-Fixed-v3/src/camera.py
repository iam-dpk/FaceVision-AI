import cv2

class Camera:
    def __init__(self, index=0):
        self.index = index
        self.cap = None

    def open(self):
        self.cap = cv2.VideoCapture(self.index)
        if not self.cap.isOpened():
            raise RuntimeError(f"Could not open camera index {self.index}")
        return self.cap

    def read(self):
        if self.cap is None:
            self.open()
        ok, frame = self.cap.read()
        if not ok:
            raise RuntimeError("Could not read frame from camera")
        return frame

    def release(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

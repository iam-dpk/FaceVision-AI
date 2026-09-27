import cv2

CASCADE = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

class FaceDetector:
    def __init__(self, cascade_path=CASCADE):
        self.classifier = cv2.CascadeClassifier(str(cascade_path))
        if self.classifier.empty():
            raise RuntimeError("OpenCV face detector could not be loaded.")

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        return self.classifier.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5,
            minSize=(70, 70)
        )

import cv2
import numpy as np

class FingerTracker:
    def __init__(self):
        self.prev_gray = None
        self.prev_points = None

    def detect_fingers(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detecta cantos (pontas dos dedos costumam gerar bons cantos)
        points = cv2.goodFeaturesToTrack(
            gray,
            maxCorners=30,
            qualityLevel=0.01,
            minDistance=15
        )

        self.prev_gray = gray
        self.prev_points = points
        return points

    def track(self, frame):
        if self.prev_points is None:
            return self.detect_fingers(frame)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        new_points, status, _ = cv2.calcOpticalFlowPyrLK(
            self.prev_gray,
            gray,
            self.prev_points,
            None
        )

        good = new_points[status == 1]

        self.prev_gray = gray
        self.prev_points = good.reshape(-1, 1, 2)

        return self.prev_points

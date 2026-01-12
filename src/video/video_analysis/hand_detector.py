import cv2


class HandDetector:
    def __init__(self):
        self.bg = cv2.createBackgroundSubtractorMOG2(
            history=400,
            varThreshold=30,
            detectShadows=False
        )

    def detect(self, frame):
        fg = self.bg.apply(frame)
        fg = cv2.medianBlur(fg, 7)
        _, mask = cv2.threshold(fg, 200, 255, cv2.THRESH_BINARY)
        return mask

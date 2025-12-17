import cv2
import numpy as np

class ORBStabilizer:
    def __init__(self):
        self.orb = cv2.ORB_create(1000)
        self.prev_gray = None
        self.prev_kp = None
        self.prev_des = None

    def stabilize(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        kp, des = self.orb.detectAndCompute(gray, None)

        if self.prev_des is None:
            self.prev_gray = gray
            self.prev_kp = kp
            self.prev_des = des
            return frame, None

        matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = matcher.match(self.prev_des, des)

        if len(matches) < 10:
            return frame, None

        src_pts = np.float32([self.prev_kp[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

        H, _ = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)

        stabilized = frame
        if H is not None:
            h, w = frame.shape[:2]
            stabilized = cv2.warpPerspective(frame, H, (w, h))

        self.prev_gray = gray
        self.prev_kp = kp
        self.prev_des = des

        return stabilized, H

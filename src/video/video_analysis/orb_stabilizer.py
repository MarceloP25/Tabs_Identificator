import cv2
import numpy as np
from collections import deque

class ORBStabilizer:
    def __init__(self, max_history=5):
        self.orb = cv2.ORB_create(1500)
        self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        self.prev_kp = None
        self.prev_des = None
        self.H_history = deque(maxlen=max_history)

    def stabilize(self, frame, mask=None):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        kp, des = self.orb.detectAndCompute(gray, mask)

        if des is None or self.prev_des is None:
            self.prev_kp = kp
            self.prev_des = des
            return frame, None

        matches = self.matcher.match(self.prev_des, des)
        matches = sorted(matches, key=lambda m: m.distance)

        if len(matches) < 12:
            return frame, None

        src_pts = np.float32(
            [self.prev_kp[m.queryIdx].pt for m in matches]
        ).reshape(-1, 1, 2)

        dst_pts = np.float32(
            [kp[m.trainIdx].pt for m in matches]
        ).reshape(-1, 1, 2)

        H, inliers = cv2.findHomography(
            dst_pts, src_pts, cv2.RANSAC, 4.0
        )

        if H is None:
            return frame, None

        # Suavização temporal
        self.H_history.append(H)
        H_smooth = np.mean(self.H_history, axis=0)

        h, w = frame.shape[:2]
        stabilized = cv2.warpPerspective(frame, H_smooth, (w, h))

        self.prev_kp = kp
        self.prev_des = des

        return stabilized, H_smooth

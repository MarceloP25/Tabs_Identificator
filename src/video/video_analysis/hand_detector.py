import cv2
import mediapipe as mp
import numpy as np


class HandDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )

    def detect(self, frame):
        """
        Retorna:
          - mask (binária)
          - bbox (x1, y1, x2, y2) ou None
        """

        h, w = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)

        mask = np.zeros((h, w), dtype=np.uint8)

        if not result.multi_hand_landmarks:
            return mask, None

        hand = result.multi_hand_landmarks[0]

        pts = []
        for lm in hand.landmark:
            pts.append((int(lm.x * w), int(lm.y * h)))

        hull = cv2.convexHull(np.array(pts))
        cv2.fillConvexPoly(mask, hull, 255)

        x, y, bw, bh = cv2.boundingRect(hull)
        bbox = (x, y, x + bw, y + bh)

        return mask, bbox

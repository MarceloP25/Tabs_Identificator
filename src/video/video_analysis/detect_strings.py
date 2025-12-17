import cv2
import numpy as np


def detect_strings(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 80, 200)


    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=150,
    minLineLength=img.shape[1] * 0.6, maxLineGap=10)


    strings = []
    if lines is not None:
        for l in lines:
            x1, y1, x2, y2 = l[0]
            if abs(y1 - y2) < 10:
                strings.append(y1)


    strings = sorted(list(set(strings)))
    return strings
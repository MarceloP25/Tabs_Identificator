import cv2
import numpy as np


def detect_frets(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 80, 200)


    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=150,
    minLineLength=img.shape[0] * 0.6, maxLineGap=10)


    frets = []
    if lines is not None:
        for l in lines:
            x1, y1, x2, y2 = l[0]
        if abs(x1 - x2) < 10:
            frets.append(x1)


    frets = sorted(list(set(frets)))
    return frets
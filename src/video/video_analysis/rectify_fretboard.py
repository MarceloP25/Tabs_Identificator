import cv2
import numpy as np


def rectify_fretboard(roi):
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)


    coords = np.column_stack(np.where(edges > 0))
    angle = cv2.fitLine(coords, cv2.DIST_L2, 0, 0.01, 0.01)[1]
    angle = np.degrees(np.arctan(angle))


    h, w = roi.shape[:2]
    M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
    rotated = cv2.warpAffine(roi, M, (w, h))


    return rotated
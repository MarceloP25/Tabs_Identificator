import cv2
import numpy as np
from fretboard_state import Fret

def detect_frets(fretboard_img, max_frets=24):
    gray = cv2.cvtColor(fretboard_img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 80, 160)

    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=120,
        minLineLength=fretboard_img.shape[0] * 0.6,
        maxLineGap=10
    )

    if lines is None:
        return []

    xs = []
    for x1, y1, x2, y2 in lines[:, 0]:
        if abs(x1 - x2) < 10:
            xs.append(x1)

    if not xs:
        return []

    xs = sorted(xs)

    frets = []
    last_dist = None
    index = 0

    for x in xs:
        if not frets:
            frets.append(Fret(index=index, x=x))
            index += 1
            continue

        dist = x - frets[-1].x
        if dist < 8:
            continue

        if last_dist is None or dist < last_dist * 1.1:
            frets.append(Fret(index=index, x=x))
            last_dist = dist
            index += 1

        if len(frets) >= max_frets:
            break

    return frets

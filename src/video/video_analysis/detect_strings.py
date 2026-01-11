import cv2
from fretboard_state import String

def detect_strings(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 80, 200)

    lines = cv2.HoughLinesP(
        edges,
        1,
        3.14159 / 180,
        threshold=150,
        minLineLength=img.shape[1] * 0.6,
        maxLineGap=10
    )

    ys = []
    if lines is not None:
        for l in lines:
            x1, y1, x2, y2 = l[0]
            if abs(y1 - y2) < 10:
                ys.append(y1)

    ys = sorted(set(ys))

    return [String(index=i, y=y) for i, y in enumerate(ys)]

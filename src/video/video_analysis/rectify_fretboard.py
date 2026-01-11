import cv2
import numpy as np

def rectify_fretboard(fretboard_img):
    gray = cv2.cvtColor(fretboard_img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 60, 140)

    lines = cv2.HoughLines(edges, 1, np.pi / 180, 160)

    angle = 0.0
    if lines is not None:
        valid_angles = []
        for rho, theta in lines[:, 0]:
            # linhas quase verticais
            if abs(theta - np.pi / 2) < np.pi / 6:
                valid_angles.append(theta)

        if valid_angles:
            angle = np.mean(valid_angles) - np.pi / 2

    h, w = fretboard_img.shape[:2]
    center = (w // 2, h // 2)

    rot_matrix = cv2.getRotationMatrix2D(
        center, angle * 180 / np.pi, 1.0
    )

    rotated = cv2.warpAffine(
        fretboard_img,
        rot_matrix,
        (w, h),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REPLICATE
    )

    return rotated


def refine_homography(frame, frets, strings):
    if len(frets) < 2 or len(strings) < 2:
        return frame

    frets = sorted(frets)
    strings = sorted(strings)

    src = np.float32([
        [frets[0], strings[0]],
        [frets[-1], strings[0]],
        [frets[-1], strings[-1]],
        [frets[0], strings[-1]]
    ])

    w = frets[-1] - frets[0]
    h = strings[-1] - strings[0]

    if w < 50 or h < 20:
        return frame

    dst = np.float32([
        [0, 0],
        [w, 0],
        [w, h],
        [0, h]
    ])

    H = cv2.getPerspectiveTransform(src, dst)
    return cv2.warpPerspective(frame, H, (int(w), int(h)))

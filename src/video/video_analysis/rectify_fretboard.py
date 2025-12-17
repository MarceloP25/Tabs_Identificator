import cv2
import numpy as np

def rectify_fretboard(fretboard_img):
    """
    Recebe imagem recortada do braço
    Retorna imagem retificada (horizontal + perspectiva reduzida)
    """

    gray = cv2.cvtColor(fretboard_img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    # Detectar linhas principais (eixo do braço)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 150)

    angle = 0.0
    if lines is not None:
        angles = []
        for rho, theta in lines[:, 0]:
            angles.append(theta)
        angle = np.mean(angles) - np.pi / 2

    # Rotação
    h, w = fretboard_img.shape[:2]
    center = (w // 2, h // 2)
    rot_matrix = cv2.getRotationMatrix2D(center, angle * 180 / np.pi, 1.0)
    rotated = cv2.warpAffine(fretboard_img, rot_matrix, (w, h))

    # Retificação projetiva simples (retângulo ideal)
    src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    dst = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    H = cv2.getPerspectiveTransform(src, dst)
    rectified = cv2.warpPerspective(rotated, H, (w, h))

    return rectified

def refine_homography(frame, frets, strings):
    if len(frets) < 2 or len(strings) < 2:
        return frame

    src = np.float32([
        [frets[0], strings[0]],
        [frets[-1], strings[0]],
        [frets[-1], strings[-1]],
        [frets[0], strings[-1]]
    ])

    w = frets[-1] - frets[0]
    h = strings[-1] - strings[0]

    dst = np.float32([
        [0, 0],
        [w, 0],
        [w, h],
        [0, h]
    ])

    H = cv2.getPerspectiveTransform(src, dst)
    refined = cv2.warpPerspective(frame, H, (int(w), int(h)))

    return refined

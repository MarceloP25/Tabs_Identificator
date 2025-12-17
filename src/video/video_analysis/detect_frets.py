import cv2
import numpy as np

def detect_frets(fretboard_img, max_frets=24):
    """
    Detecta trastes usando Hough + heurística musical
    Retorna lista de coordenadas x (em pixels)
    """

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

    # Coletar linhas quase verticais
    xs = []
    for x1, y1, x2, y2 in lines[:, 0]:
        if abs(x1 - x2) < 10:
            xs.append(x1)

    if not xs:
        return []

    xs = sorted(xs)

    # Heurística musical:
    # espaçamento deve diminuir progressivamente
    filtered = [xs[0]]
    last_dist = None

    for x in xs[1:]:
        dist = x - filtered[-1]
        if dist < 8:
            continue

        if last_dist is None or dist < last_dist * 1.1:
            filtered.append(x)
            last_dist = dist

        if len(filtered) >= max_frets:
            break

    return filtered

import cv2

def draw_fretboard_grid(frame, frets, strings):
    """
    frets: lista de coordenadas x
    strings: lista de coordenadas y
    """

    vis = frame.copy()

    for x in frets:
        cv2.line(vis, (int(x), 0), (int(x), vis.shape[0]), (0, 255, 0), 1)

    for y in strings:
        cv2.line(vis, (0, int(y)), (vis.shape[1], int(y)), (255, 0, 0), 1)

    return vis

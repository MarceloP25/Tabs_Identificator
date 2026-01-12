import cv2


def draw_hand_mask(frame, hand_mask):
    vis = frame.copy()
    vis[hand_mask > 0] = (0, 0, 255)
    return vis


def draw_pressure(frame, frets, strings, pressed_cells):
    vis = frame.copy()

    for c in pressed_cells:
        x1 = int(frets[c["fret"]])
        x2 = int(frets[c["fret"] + 1])
        y = int(strings[c["string"]])

        cv2.rectangle(
            vis,
            (x1, y - 8),
            (x2, y + 8),
            (0, 255, 255),
            1
        )

    return vis

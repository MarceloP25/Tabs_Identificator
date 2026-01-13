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


STRING_LABEL_Y_OFFSET = 15


def draw_notes(frame, strings, notes):
    """
    Desenha a nota inferida sobre cada corda
    """
    for string_id, string_line in enumerate(strings):
        y = int(string_line.mean())
        note = notes[string_id]["note"]
        fret = notes[string_id]["fret"]

        label = note if fret is None else f"{note} (fret {fret})"

        cv2.putText(
            frame,
            label,
            (10, y - STRING_LABEL_Y_OFFSET),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 255),
            1,
            cv2.LINE_AA
        )

    return frame

import numpy as np


def build_pressure_map(hand_mask, frets, strings, tolerance_px=5):
    """
    Retorna:
      pressure_map[string_id] = [frets pressionados]

    A pressão é detectada se a mão cobre
    a região próxima à interseção corda × traste.
    """

    pressure_map = {}

    h, w = hand_mask.shape[:2]

    for si, y in enumerate(strings):
        y = int(y)
        pressed_frets = []

        for fi, x in enumerate(frets):
            x = int(x)

            x_min = max(0, x - tolerance_px)
            x_max = min(w, x + tolerance_px)
            y_min = max(0, y - tolerance_px)
            y_max = min(h, y + tolerance_px)

            region = hand_mask[y_min:y_max, x_min:x_max]

            if region.size == 0:
                continue

            if np.any(region > 0):
                pressed_frets.append(fi)

        pressure_map[si] = pressed_frets

    return pressure_map

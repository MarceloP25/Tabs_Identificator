import numpy as np


def compute_pressure_map(
    hand_mask,
    frets,
    strings,
    string_band=8,
    coverage_threshold=0.15
):
    """
    Detecta células (corda x traste) pressionadas pela mão.
    """

    pressed = []
    h, w = hand_mask.shape

    for s_idx, y in enumerate(strings):
        y1 = max(0, int(y - string_band))
        y2 = min(h, int(y + string_band))

        for f_idx in range(len(frets) - 1):
            x1 = int(frets[f_idx])
            x2 = int(frets[f_idx + 1])

            if x2 <= x1:
                continue

            cell = hand_mask[y1:y2, x1:x2]

            if cell.size == 0:
                continue

            coverage = np.mean(cell > 0)

            if coverage >= coverage_threshold:
                pressed.append({
                    "string": s_idx,
                    "fret": f_idx,
                    "coverage": float(coverage)
                })

    return pressed


def resolve_fret_per_string(pressed_cells):
    """
    Para cada corda, mantém apenas o MAIOR traste pressionado.
    """

    resolved = {}

    for cell in pressed_cells:
        s = cell["string"]
        f = cell["fret"]

        if s not in resolved or f > resolved[s]["fret"]:
            resolved[s] = {
                "fret": f,
                "coverage": cell["coverage"]
            }

    return resolved

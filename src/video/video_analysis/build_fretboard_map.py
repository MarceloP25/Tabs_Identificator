import json


def build_fretboard_map(frets, strings, shape):
    h, w = shape[:2]
    grid = []


    for s_idx, y in enumerate(strings):
        for f_idx in range(len(frets) - 1):
            x_center = (frets[f_idx] + frets[f_idx + 1]) / 2
            grid.append({
                "string": s_idx,
                "fret": f_idx,
                "x_norm": x_center / w,
                "y_norm": y / h
            })


    return grid
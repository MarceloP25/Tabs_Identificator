from detect_fretboard import detect_fretboard
from rectify_fretboard import rectify_fretboard, refine_homography
from orb_stabilizer import ORBStabilizer
from detect_frets import detect_frets
from detect_strings import detect_strings
from grid_visualization import draw_fretboard_grid
from fretboard_state import FretboardState

stabilizer = ORBStabilizer()
frame_counter = 0

def process_frame(frame):
    global frame_counter

    roi, bbox = detect_fretboard(frame)
    if roi is None:
        return None

    stabilized, _ = stabilizer.stabilize(roi)
    rectified = rectify_fretboard(stabilized)

    frets = detect_frets(rectified)
    strings = detect_strings(rectified)

    refined = refine_homography(
        rectified,
        [f.x for f in frets],
        [s.y for s in strings]
    )

    state = FretboardState(
        frame_index=frame_counter,
        rectified_image=refined,
        bbox_original=bbox,
        frets=frets,
        strings=strings
    )

    frame_counter += 1
    return state

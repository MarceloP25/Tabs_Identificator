from detect_fretboard import detect_fretboard
from rectify_fretboard import rectify_fretboard, refine_homography
from orb_stabilizer import ORBStabilizer
from detect_frets import detect_frets
from detect_strings import detect_strings
from grid_visualization import draw_fretboard_grid

stabilizer = ORBStabilizer()

def process_frame(frame):
    roi, bbox = detect_fretboard(frame)
    if roi is None:
        return None, None, None

    stabilized, _ = stabilizer.stabilize(roi)

    rectified = rectify_fretboard(stabilized)

    frets = detect_frets(rectified)
    strings = detect_strings(rectified)

    refined = refine_homography(rectified, frets, strings)

    debug = draw_fretboard_grid(refined, frets, strings)

    return debug, frets, strings

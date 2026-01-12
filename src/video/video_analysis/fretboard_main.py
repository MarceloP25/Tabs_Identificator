import cv2
import random

from detect_fretboard import detect_fretboard
from rectify_fretboard import rectify_fretboard, refine_homography
from orb_stabilizer import ORBStabilizer
from detect_frets import detect_frets
from detect_strings import detect_strings
from grid_visualization import draw_fretboard_grid
from fretboard_grid_tracker import FretboardGridTracker


# ----------------------------
# Inicializações globais
# ----------------------------
stabilizer = ORBStabilizer()
grid_tracker = FretboardGridTracker(alpha=0.7)

# Buffer para visualização
VIS_BUFFER = []
VIS_MAX = 20


def process_frame(frame, frame_id=None):
    """
    Processa um único frame.
    Retorna:
      - frame_debug (ou None)
      - dados estruturais (frets, strings)
    """

    roi, bbox = detect_fretboard(frame)
    if roi is None:
        return None, None

    # ----------------------------
    # Estabilização temporal
    # ----------------------------
    stabilized, _ = stabilizer.stabilize(roi)

    # ----------------------------
    # Retificação geométrica
    # ----------------------------
    rectified = rectify_fretboard(stabilized)

    # ----------------------------
    # Detecção estrutural (frame-local)
    # ----------------------------
    frets_raw = detect_frets(rectified)
    strings_raw = detect_strings(rectified)

    # ----------------------------
    # Fixação de identidade temporal
    # ----------------------------
    frets, strings = grid_tracker.update(frets_raw, strings_raw)

    # ----------------------------
    # Refinamento da homografia usando o grid
    # ----------------------------
    refined = refine_homography(rectified, frets, strings)

    # ----------------------------
    # Visualização diagnóstica
    # ----------------------------
    debug = draw_fretboard_grid(refined, frets, strings)

    # ----------------------------
    # Buffer de visualização
    # ----------------------------
    if frame_id is not None and len(VIS_BUFFER) < VIS_MAX:
        VIS_BUFFER.append((frame_id, debug.copy()))

    return debug, (frets, strings)


def show_visual_diagnostics():
    """
    Mostra até 20 frames aleatórios.
    Execução pausa até o usuário fechar.
    """
    if not VIS_BUFFER:
        return

    samples = random.sample(VIS_BUFFER, min(len(VIS_BUFFER), VIS_MAX))

    for frame_id, img in samples:
        cv2.imshow(f"Diagnóstico - Frame {frame_id}", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

import cv2
import random

from detect_fretboard import detect_fretboard
from rectify_fretboard import rectify_fretboard, refine_homography
from orb_stabilizer import ORBStabilizer
from detect_frets import detect_frets
from detect_strings import detect_strings
from grid_visualization import draw_fretboard_grid, draw_notes
from fretboard_grid_tracker import FretboardGridTracker
from hand_detector import detect_hand_mask
from pressure_map import build_pressure_map
from note_inference import infer_notes_from_pressure
from pipeline_observer import PipelineObserver


# ----------------------------
# Inicializações globais
# ----------------------------
stabilizer = ORBStabilizer()
grid_tracker = FretboardGridTracker(alpha=0.7)
observer = PipelineObserver(max_frames=200)

VIS_BUFFER = []
VIS_MAX = 20


def process_frame(frame, frame_id=None):
    """
    Processa um único frame.
    Retorna:
      - frame_debug
      - estrutura de notas inferidas
    """

    # ----------------------------
    # Passo 1 — Detecção da escala
    # ----------------------------
    roi, bbox = detect_fretboard(frame)
    if roi is None:
        return None, None

    observer.store(frame_id, "roi", roi)

    # ----------------------------
    # Passo 2 — Estabilização
    # ----------------------------
    stabilized, _ = stabilizer.stabilize(roi)
    observer.store(frame_id, "stabilized", stabilized)

    # ----------------------------
    # Passo 3 — Retificação
    # ----------------------------
    rectified = rectify_fretboard(stabilized)
    observer.store(frame_id, "rectified", rectified)

    # ----------------------------
    # Passo 4 — Detecção estrutural
    # ----------------------------
    frets_raw = detect_frets(rectified)
    strings_raw = detect_strings(rectified)

    frets, strings = grid_tracker.update(frets_raw, strings_raw)

    observer.store(frame_id, "frets", frets)
    observer.store(frame_id, "strings", strings)

    # ----------------------------
    # Refinamento geométrico
    # ----------------------------
    refined = refine_homography(rectified, frets, strings)
    observer.store(frame_id, "refined", refined)

    # ----------------------------
    # Passo 4 — Detecção da mão
    # ----------------------------
    hand_mask = detect_hand_mask(refined)
    observer.store(frame_id, "hand_mask", hand_mask)

    # ----------------------------
    # Passo 4 — Mapa de pressão
    # ----------------------------
    pressure_map = build_pressure_map(
        hand_mask=hand_mask,
        frets=frets,
        strings=strings
    )
    observer.store(frame_id, "pressure_map", pressure_map)

    # ----------------------------
    # Passo 5 — Inferência de notas
    # ----------------------------
    notes = infer_notes_from_pressure(pressure_map)
    observer.store(frame_id, "notes", notes)

    # ----------------------------
    # Visualização
    # ----------------------------
    debug = draw_fretboard_grid(refined, frets, strings)
    debug = draw_notes(debug, strings, notes)

    if frame_id is not None and len(VIS_BUFFER) < VIS_MAX:
        VIS_BUFFER.append((frame_id, debug.copy()))

    return debug, notes


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

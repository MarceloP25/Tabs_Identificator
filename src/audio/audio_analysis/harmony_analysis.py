"""
harmony_analysis.py
- Recebe frames (output de note_detection) e decide:
    - role por frame: 'silence', 'solo', 'base', 'mix'
    - chord label (via music21) quando aplicável
- Exporta lista de events por frame para ser consolidado posteriormente.
"""

from typing import List, Dict, Any
import numpy as np

# music21 import
try:
    from music21 import chord, pitch, note as m21note
except Exception:
    raise ImportError("music21 não encontrada. Instale com `pip install music21`")

# mapping index -> note name (C=0)
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def chroma_to_top_notes(frame_chroma: List[float], top_k: int = 3) -> List[str]:
    arr = np.array(frame_chroma)
    # pegar top_k bins
    idx = np.argsort(arr)[-top_k:]
    notes = []
    for i in sorted(idx):
        name = NOTE_NAMES[int(i % 12)]
        # sem octave (music21 vai assumir sem oitava) - para chord recognition é suficiente
        notes.append(name)
    return notes

def notes_from_f0(f0_hz: float):
    """Converte frequência em nome nota com oitava exata (ex: 'E4')."""
    if f0_hz is None:
        return None
    p = pitch.Pitch()
    p.frequency = float(f0_hz)
    return p.nameWithOctave  # ex 'E4'

def classify_frame(frame: Dict[str, Any],
                   voiced_threshold: float = 0.25,
                   chroma_energy_threshold: float = 0.15) -> Dict[str, Any]:
    """
    Classifica um único frame como solo/base/mix/silence.
    - Se f0 presente com prob > voiced_threshold e chroma com único pico forte -> solo
    - Se chroma mostra >=2 bins fortes -> base
    - Se f0 presente e chroma múltipla -> mix
    """
    f0 = frame.get("f0")
    vprob = frame.get("voiced_prob", 0.0)
    chroma = np.array(frame.get("chroma", [0.0]*12))
    chroma_sum = float(np.sum(chroma))
    # medir quantos bins acima de fracção da média
    mean = float(np.mean(chroma)) if chroma.sum() > 0 else 0.0
    strong_bins = np.where(chroma > max(mean * 1.5, chroma_energy_threshold))[0]

    role = "silence"
    label = None
    notes_list = []

    if f0 is not None and vprob >= voiced_threshold and len(strong_bins) <= 1:
        # monofonia provável
        role = "solo"
        notes_list = [notes_from_f0(f0)]
        label = notes_list[0]
    elif len(strong_bins) >= 2:
        # polifonia provável --> tentar extrair notas do chroma
        role = "base"
        top_notes = chroma_to_top_notes(chroma, top_k=3)
        notes_list = top_notes
        # tentar rotular acorde via music21
        try:
            ch = chord.Chord(top_notes)
            label = ch.commonName if ch.commonName is not None else ch.quality
        except Exception:
            label = "+".join(top_notes)
    elif f0 is not None and vprob >= voiced_threshold and len(strong_bins) > 1:
        role = "mix"
        notes_list = [notes_from_f0(f0)] + chroma_to_top_notes(chroma, top_k=2)
        try:
            ch = chord.Chord(notes_list)
            label = ch.commonName if ch.commonName is not None else ch.quality
        except Exception:
            label = ",".join([n for n in notes_list if n])
    else:
        role = "silence"
        label = None

    return {
        "time": float(frame.get("time", 0.0)),
        "role": role,
        "label": label,
        "notes": notes_list,
        "f0": float(f0) if f0 is not None else None,
        "voiced_prob": float(vprob),
        "chroma": frame.get("chroma")
    }

def analyze_frames(frames: List[Dict[str, Any]],
                   voiced_threshold: float = 0.25,
                   chroma_energy_threshold: float = 0.15) -> List[Dict[str, Any]]:
    return [classify_frame(f, voiced_threshold, chroma_energy_threshold) for f in frames]

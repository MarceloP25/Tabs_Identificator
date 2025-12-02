"""
Arquivo: detect_notes.py
Função: Detectar notas e acordes no áudio, de acordo com a textura musical.
Entradas:
  - data/processed/audio/audio_clean.wav
  - data/interim/texture_map.json
Saídas:
  - data/interim/notes_chords.json
Descrição:
  Aplica diferentes métodos de análise espectral conforme a classificação
  (solo, base ou solo+base), gerando eventos musicais com timestamps.
"""

import os
import json
import numpy as np
import librosa
import librosa.display
from librosa import effects
import matplotlib.pyplot as plt

def detect_notes_in_segment(y, sr, start, end):
    """Detecção monofônica de notas em trechos de solo."""
    y_seg = y[int(start * sr):int(end * sr)]
    pitches, magnitudes = librosa.piptrack(y=y_seg, sr=sr)
    notas = []
    for i in range(pitches.shape[1]):
        idx = magnitudes[:, i].argmax()
        pitch = pitches[idx, i]
        if pitch > 0:
            nota = librosa.hz_to_note(pitch)
            notas.append(nota)
    return list(set(notas))

def detect_chords_in_segment(y, sr, start, end):
    """Detecção simplificada de acordes por análise de cromas."""
    y_seg = y[int(start * sr):int(end * sr)]
    chroma = librosa.feature.chroma_cqt(y=y_seg, sr=sr)
    avg_chroma = np.mean(chroma, axis=1)
    top_notes = np.argsort(avg_chroma)[-3:]  # notas mais fortes
    notas = [librosa.midi_to_note(12 + n) for n in top_notes]
    acorde = "+".join(sorted(notas))
    return acorde

def detect_notes_and_chords(audio_path="data/processed/audio/audio_clean.wav",
                            texture_path="data/interim/texture_map.json"):
    if not os.path.exists(audio_path) or not os.path.exists(texture_path):
        raise FileNotFoundError("Arquivos de entrada não encontrados.")

    y, sr = librosa.load(audio_path, sr=44100)
    with open(texture_path, "r") as f:
        segments = json.load(f)

    eventos = []
    for seg in segments:
        tipo = seg["tipo"]
        inicio, fim = seg["inicio"], seg["fim"]

        if tipo == "solo":
            notas = detect_notes_in_segment(y, sr, inicio, fim)
            for n in notas:
                eventos.append({"inicio": inicio, "fim": fim, "tipo": tipo, "nota": n})
        elif tipo == "base":
            acorde = detect_chords_in_segment(y, sr, inicio, fim)
            eventos.append({"inicio": inicio, "fim": fim, "tipo": tipo, "acorde": acorde})
        else:
            notas = detect_notes_in_segment(y, sr, inicio, fim)
            acorde = detect_chords_in_segment(y, sr, inicio, fim)
            eventos.append({"inicio": inicio, "fim": fim, "tipo": tipo, "nota": notas, "acorde": acorde})

    os.makedirs("data/interim", exist_ok=True)
    output_path = "data/interim/notes_chords.json"
    with open(output_path, "w") as f:
        json.dump(eventos, f, indent=2)

    print(f"✅ Notas e acordes detectados salvos em: {output_path}")
    return output_path

if __name__ == "__main__":
    detect_notes_and_chords()

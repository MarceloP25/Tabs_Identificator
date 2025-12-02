"""
Arquivo: identify_texture.py
Função: Identificar a textura musical do áudio — solo, base ou solo+base.
Entradas:
  - data/processed/audio/audio_clean.wav
Saídas:
  - data/interim/texture_map.json
Descrição:
  Divide o áudio em janelas curtas e extrai características espectrais
  para classificar a textura musical de cada trecho.
"""

import os
import json
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

def extract_features(y, sr, frame_length=2048, hop_length=512):
    """Extrai as principais features espectrais e harmônicas do áudio."""
    flatness = librosa.feature.spectral_flatness(y=y, n_fft=frame_length, hop_length=hop_length)[0]
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr, n_fft=frame_length, hop_length=hop_length)[0]
    zcr = librosa.feature.zero_crossing_rate(y, frame_length=frame_length, hop_length=hop_length)[0]
    rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
    return flatness, centroid, zcr, rms

def classify_texture(flatness, zcr):
    """Classifica a textura musical com base em thresholds heurísticos."""
    textura = []
    for f, z in zip(flatness, zcr):
        if f < 0.25 and z < 0.05:
            textura.append("solo")
        elif f > 0.4 and z > 0.1:
            textura.append("base")
        else:
            textura.append("solo+base")
    return np.array(textura)

def smooth_labels(labels, hop_duration, min_duration=0.5):
    """Agrupa janelas consecutivas de mesmo tipo."""
    segments = []
    current_label = labels[0]
    start_time = 0
    for i, label in enumerate(labels[1:], start=1):
        if label != current_label:
            end_time = i * hop_duration
            duration = end_time - start_time
            if duration >= min_duration:
                segments.append({"inicio": start_time, "fim": end_time, "tipo": current_label})
            start_time = end_time
            current_label = label
    segments.append({"inicio": start_time, "fim": (len(labels) * hop_duration), "tipo": current_label})
    return segments

def identify_texture(audio_path="data/processed/audio/audio_clean.wav"):
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Áudio não encontrado: {audio_path}")

    print("🔊 Carregando áudio para análise de textura...")
    y, sr = librosa.load(audio_path, sr=44100)

    flatness, centroid, zcr, rms = extract_features(y, sr)
    hop_duration = 512 / sr

    print("🎼 Classificando trechos...")
    labels = classify_texture(flatness, zcr)
    segments = smooth_labels(labels, hop_duration)

    os.makedirs("data/interim", exist_ok=True)
    output_path = "data/interim/texture_map.json"
    with open(output_path, "w") as f:
        json.dump(segments, f, indent=2)

    print(f"✅ Mapa de textura gerado em: {output_path}")

    # Visualização opcional
    plt.figure(figsize=(10, 3))
    t = np.arange(len(labels)) * hop_duration
    plt.plot(t, flatness, label="Flatness", alpha=0.6)
    plt.plot(t, zcr, label="ZCR", alpha=0.6)
    plt.title("Características de textura ao longo do tempo")
    plt.legend()
    plt.tight_layout()
    plt.show()

    return output_path

if __name__ == "__main__":
    identify_texture()

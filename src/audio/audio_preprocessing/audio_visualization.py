"""
Arquivo: audio_visualization.py
Função: Gerar visualizações (forma de onda e espectrograma) do áudio
Entradas:
  - caminho de um arquivo WAV
Saídas:
  - duas janelas matplotlib: waveform e espectrograma
"""

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


# ------------------------------------------------------------
# 🔹 Exibir forma de onda (waveform)
# ------------------------------------------------------------
def plot_waveform(y, sr, title="Forma de Onda"):
    plt.figure(figsize=(12, 4))
    librosa.display.waveshow(y, sr=sr, alpha=0.8)
    plt.title(title)
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# 🔹 Exibir espectrograma logarítmico
# ------------------------------------------------------------
def plot_spectrogram(y, sr, title="Espectrograma (dB)"):
    S = np.abs(librosa.stft(y, n_fft=2048, hop_length=512))
    S_db = librosa.amplitude_to_db(S, ref=np.max)

    plt.figure(figsize=(12, 5))
    librosa.display.specshow(S_db, sr=sr, x_axis="time", y_axis="log", cmap="magma")
    plt.colorbar(format="%+2.0f dB")
    plt.title(title)
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# 🔹 Função principal para carregar e visualizar áudio
# ------------------------------------------------------------
def visualize_audio(audio_path: str):
    print(f"🔍 Carregando áudio: {audio_path}")
    y, sr = librosa.load(audio_path, sr=44100)

    print("🎨 Exibindo forma de onda...")
    plot_waveform(y, sr, title="Forma de Onda")

    print("🌈 Exibindo espectrograma...")
    plot_spectrogram(y, sr, title="Espectrograma (Escala Logarítmica)")


# ------------------------------------------------------------
# 🚀 Execução direta
# ------------------------------------------------------------
if __name__ == "__main__":
    visualize_audio("data/processed/audio/audio_clean.wav")

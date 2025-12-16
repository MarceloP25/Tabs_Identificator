import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


def plot_waveform(y, sr, title="Forma de Onda"):
    plt.figure(figsize=(12, 3))
    librosa.display.waveshow(y, sr=sr)
    plt.title(title)
    plt.xlabel("Tempo (s)")
    plt.tight_layout()
    plt.show()


def plot_spectrogram(y, sr, title="Espectrograma (log-freq)"):
    S = np.abs(librosa.stft(y, n_fft=2048, hop_length=512))
    S_db = librosa.amplitude_to_db(S, ref=np.max)

    plt.figure(figsize=(12, 4))
    librosa.display.specshow(
        S_db,
        sr=sr,
        hop_length=512,
        x_axis="time",
        y_axis="log",
        cmap="magma"
    )
    plt.colorbar(format="%+2.0f dB")
    plt.title(title)
    plt.tight_layout()
    plt.show()


def plot_chromagram(y, sr, title="Cromagrama"):
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)

    plt.figure(figsize=(12, 3))
    librosa.display.specshow(
        chroma,
        x_axis="time",
        y_axis="chroma",
        sr=sr,
        cmap="coolwarm"
    )
    plt.colorbar()
    plt.title(title)
    plt.tight_layout()
    plt.show()


def plot_onset_strength(y, sr, title="Força de Transientes"):
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)

    times = librosa.times_like(onset_env, sr=sr)
    plt.figure(figsize=(12, 3))
    plt.plot(times, onset_env)
    plt.title(title)
    plt.xlabel("Tempo (s)")
    plt.ylabel("Força")
    plt.tight_layout()
    plt.show()


def visualize_audio(audio_path):
    print(f"🔍 Visualizando: {audio_path}")
    y, sr = librosa.load(audio_path, sr=44100)

    plot_waveform(y, sr)
    plot_spectrogram(y, sr)
    plot_chromagram(y, sr)
    plot_onset_strength(y, sr)

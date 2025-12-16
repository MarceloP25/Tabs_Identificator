import os
import numpy as np
import librosa
import soundfile as sf
from scipy.signal import butter, lfilter

# visualização é opcional
try:
    from audio_visualization import visualize_audio
    HAS_VIZ = True
except ImportError:
    HAS_VIZ = False


def highpass_filter(data, cutoff, sr, order=2):
    nyq = 0.5 * sr
    high = cutoff / nyq
    b, a = butter(order, high, btype='high')
    return lfilter(b, a, data)


def preprocess_audio(
    audio_path="data/raw/audio/audio_raw.wav",
    output_path="data/processed/audio/audio_clean.wav",
    show_plots=False
):
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Áudio não encontrado: {audio_path}")

    print("🔊 Carregando áudio...")
    y, sr = librosa.load(audio_path, sr=44100)

    print("🎛️ High-pass leve (50 Hz)...")
    y_hp = highpass_filter(y, cutoff=50, sr=sr)

    print("📏 Normalização por pico (conservadora)...")
    peak = np.max(np.abs(y_hp))
    y_norm = y_hp / peak * 0.9 if peak > 0 else y_hp

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    sf.write(output_path, y_norm, sr)

    print(f"✅ Áudio salvo em: {output_path}")

    if show_plots and HAS_VIZ:
        visualize_audio(output_path)

    return {
        "audio_path": output_path,
        "sr": sr,
        "duration_sec": librosa.get_duration(y=y_norm, sr=sr),
    }


if __name__ == "__main__":
    preprocess_audio(show_plots=True)

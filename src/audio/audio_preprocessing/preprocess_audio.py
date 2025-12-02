import os
import numpy as np
import librosa
import soundfile as sf
from scipy.signal import butter, lfilter
from audio_visualization import visualize_audio


# ------------------------------------------------------------
# 🔹 Filtro high-pass suave (remove hum sem afetar harmônicos)
# ------------------------------------------------------------
def highpass_filter(data, cutoff, sr, order=2):
    nyq = 0.5 * sr
    high = cutoff / nyq
    b, a = butter(order, high, btype='high')
    return lfilter(b, a, data)


# ------------------------------------------------------------
# 🔹 Pré-processamento minimalista (ideal para análise musical)
# ------------------------------------------------------------
def preprocess_audio(
        audio_path="data/raw/audio/audio_raw.wav",
        output_path="data/processed/audio/audio_clean.wav",
    ):

    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Áudio não encontrado: {audio_path}")

    print("🔊 Carregando áudio...")
    y, sr = librosa.load(audio_path, sr=44100)

    # ----------------------------------------------------------------
    # 🎚️ 1. High-pass leve (remove hum e ruído grave sem afetar harmônicos)
    # ----------------------------------------------------------------
    print("🎛️ Aplicando high-pass (cutoff 50 Hz)...")
    y_hp = highpass_filter(y, cutoff=50, sr=sr)

    # ----------------------------------------------------------------
    # ⚙️ 2. Normalização por pico (não destrói dinâmica)
    # ----------------------------------------------------------------
    print("📏 Normalizando (peak)...")
    peak = np.max(np.abs(y_hp))
    if peak > 0:
        y_norm = y_hp / peak * 0.9
    else:
        y_norm = y_hp

    # ----------------------------------------------------------------
    # 💾 3. Salvamento
    # ----------------------------------------------------------------
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    sf.write(output_path, y_norm, sr)

    print(f"✅ Áudio limpo salvo em: {output_path}")
    visualize_audio(output_path)

    return {
        "audio_path": output_path,
        "sr": sr,
        "duration_sec": librosa.get_duration(y=y_norm, sr=sr),
    }


if __name__ == "__main__":
    r = preprocess_audio()
    print(r)

"""
Arquivo: preprocess_audio.py
Função: Processar o áudio cru extraído do vídeo, aplicando filtragem, redução de ruído e normalização.
Entradas:
  - data/raw/audio/audio_raw.wav
Saídas:
  - data/processed/audio/audio_clean.wav
"""

import os
import numpy as np
import librosa
import librosa.display
import noisereduce as nr
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter


# ------------------------------------------------------------
# 🔹 Função para aplicar filtro passa-faixa (Guitarra: 80–5000 Hz)
# ------------------------------------------------------------
def butter_bandpass_filter(data, lowcut, highcut, sr, order=5):
    nyq = 0.5 * sr
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, data)


# ------------------------------------------------------------
# 🔹 Função principal de pré-processamento
# ------------------------------------------------------------
def preprocess_audio(audio_path: str = "data/raw/audio/audio_raw.wav",
                     output_path: str = "data/processed/audio/audio_clean.wav"):
    
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Áudio não encontrado: {audio_path}")

    print("🔊 Carregando áudio...")
    y, sr = librosa.load(audio_path, sr=44100)

    # --------------------------------------------------------
    # 🎚️ 1. Aplicar filtro passa-faixa (peso espectral)
    # --------------------------------------------------------
    print("🎛️ Aplicando filtro passa-faixa (80–5000 Hz)...")
    y_filtered = butter_bandpass_filter(y, 80, 5000, sr)

    # --------------------------------------------------------
    # 🧹 2. Reduzir ruído
    # --------------------------------------------------------
    print("🧹 Reduzindo ruído...")
    y_denoised = nr.reduce_noise(y=y_filtered, sr=sr, stationary=True)

    # --------------------------------------------------------
    # ⚙️ 3. Normalização RMS ponderada (peso de energia)
    # --------------------------------------------------------
    print("📏 Normalizando áudio...")
    target_rms = 0.1
    rms = np.sqrt(np.mean(y_denoised**2))
    y_normalized = y_denoised * (target_rms / (rms + 1e-6))

    # --------------------------------------------------------
    # 📈 4. Visualizações: onda + espectrograma
    # --------------------------------------------------------
    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    librosa.display.waveshow(y, sr=sr, alpha=0.5, label='Original')
    librosa.display.waveshow(y_normalized, sr=sr, color='r', alpha=0.6, label='Processado')
    plt.title("Forma de Onda: Original vs. Processado")
    plt.legend()

    plt.subplot(2, 1, 2)
    D_original = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    D_processed = librosa.amplitude_to_db(np.abs(librosa.stft(y_normalized)), ref=np.max)
    librosa.display.specshow(D_processed, sr=sr, x_axis='time', y_axis='log', cmap='magma')
    plt.title("Espectrograma (Processado)")
    plt.colorbar(format="%+2.0f dB")

    plt.tight_layout()
    plt.show()

    # --------------------------------------------------------
    # 💾 5. Salvamento
    # --------------------------------------------------------
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    sf.write(output_path, y_normalized, sr)
    print(f"✅ Áudio processado salvo em: {output_path}")

    # --------------------------------------------------------
    # 🔙 6. Retornar informações úteis
    # --------------------------------------------------------
    return {
        "audio_path": output_path,
        "sr": sr,
        "duration_sec": librosa.get_duration(y=y_normalized, sr=sr),
        "rms": target_rms,
    }


# ------------------------------------------------------------
# 🚀 Execução direta
# ------------------------------------------------------------
if __name__ == "__main__":
    results = preprocess_audio()
    print("\n📊 Resultado do processamento:")
    for k, v in results.items():
        print(f"  {k}: {v}")

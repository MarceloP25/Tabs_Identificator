import numpy as np
import librosa


def extract_features(y, sr, hop_length=512):
    f0, voiced_flag, voiced_prob = librosa.pyin(
        y,
        sr=sr,
        fmin=82.0,     # E2 (corda mais grave da guitarra)
        fmax=1200.0,   # região aguda segura
        hop_length=hop_length
    )

    chroma = librosa.feature.chroma_cqt(
        y=y,
        sr=sr,
        hop_length=hop_length
    ).T

    times = librosa.frames_to_time(
        np.arange(len(chroma)),
        sr=sr,
        hop_length=hop_length
    )

    frames = []

    for i, t in enumerate(times):
        frames.append({
            "frame_idx": int(i),
            "time": float(t),
            "f0": None if f0[i] is None else float(f0[i]),
            "voiced_prob": float(voiced_prob[i]),
            "chroma": chroma[i].tolist()
        })

    return frames


def detect_notes(audio_path):
    print(f"🎼 Extraindo features de: {audio_path}")
    y, sr = librosa.load(audio_path, sr=44100)
    return extract_features(y, sr)


if __name__ == "__main__":
    frames = detect_notes("data/processed/audio/audio_clean.wav")
    print(frames[:5])

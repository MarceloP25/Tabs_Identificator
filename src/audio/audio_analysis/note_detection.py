"""
Arquivo: note_detection.py
Função: Detectar notas, acordes e textura (solo/base) a partir de um áudio já pré-processado.
Entradas:
    - audio_clean.wav (pré-processado)
Saídas:
    - Lista temporal de notas
    - Lista temporal de acordes
    - Classificação de textura: solo, base ou híbrido
    - Pitch track (Hz)
"""

import numpy as np
import librosa
import music21 as m21

# -------------------------------------------------------------------------
# 1. ESTIMATIVA DE PITCH (Hz)
# -------------------------------------------------------------------------

def compute_pitch_track(y, sr, hop_length=512):
    """Retorna o pitch estimado ao longo do tempo em Hz."""
    f0, voiced_flag, _ = librosa.pyin(
        y,
        sr=sr,
        fmin=82.0,      # E2 – limite inferior da guitarra
        fmax=1200.0,    # Bem acima da 24ª casa
        hop_length=hop_length
    )

    pitch = np.where(voiced_flag, f0, np.nan)
    return pitch


# -------------------------------------------------------------------------
# 2. CONVERSÃO Hz → NOME DA NOTA (com Music21)
# -------------------------------------------------------------------------

def hz_to_note_name(freq):
    """Converte frequência (Hz) para nome de nota usando Music21."""
    if np.isnan(freq):
        return None
    try:
        pitch_obj = m21.pitch.Pitch()
        pitch_obj.frequency = freq
        return pitch_obj.nameWithOctave
    except:
        return None


# -------------------------------------------------------------------------
# 3. AGRUPAMENTO TEMPORAL PARA GERAR NOTAS ESTÁVEIS
# -------------------------------------------------------------------------

def detect_notes_from_pitch(pitch_track, sr, hop_length=512, stability_frames=4):
    """
    Constrói uma linha temporal de notas estáveis.
    stability_frames define quantos frames consecutivos são necessários para 
    considerar que uma nota "existe".
    """

    notes = []
    current_note = None
    dur_count = 0
    t_per_frame = hop_length / sr

    for i, f in enumerate(pitch_track):
        note_name = hz_to_note_name(f)

        if note_name == current_note:
            dur_count += 1
        else:
            if current_note is not None:
                duration = dur_count * t_per_frame
                if duration > 0.03:       # 30ms = mínimo perceptível musicalmente
                    notes.append({
                        "note": current_note,
                        "start": (i - dur_count) * t_per_frame,
                        "end": i * t_per_frame,
                        "duration": duration
                    })
            current_note = note_name
            dur_count = 1

    # Finaliza a última nota
    if current_note is not None and dur_count > stability_frames:
        notes.append({
            "note": current_note,
            "start": (len(pitch_track) - dur_count) * t_per_frame,
            "end": len(pitch_track) * t_per_frame,
            "duration": dur_count * t_per_frame
        })

    return notes


# -------------------------------------------------------------------------
# 4. DETECÇÃO DE TEXTURA (solo / base / híbrido)
# -------------------------------------------------------------------------

def classify_texture(y, sr, window=2048):
    """
    Usa densidade harmônica e distribuição de energia para detectar textura.
    - solo → notas isoladas, pouca energia em bandas largas
    - base → acordes, múltiplas harmônicas ativas
    - híbrido → combinação
    """

    S = np.abs(librosa.stft(y, n_fft=window))
    harmonic_energy = np.mean(S, axis=0)

    # Limiares empíricos refináveis depois
    spread = np.std(harmonic_energy)
    mean_energy = np.mean(harmonic_energy)

    if spread < 20:
        return "solo"
    elif spread > 60:
        return "base"
    else:
        return "híbrido"


# -------------------------------------------------------------------------
# 5. PIPELINE PRINCIPAL
# -------------------------------------------------------------------------

def detect_notes(audio_path="data/processed/audio/audio_clean.wav"):
    y, sr = librosa.load(audio_path, sr=44100)

    print(">> Calculando pitch track...")
    pitch_track = compute_pitch_track(y, sr)

    print(">> Convertendo pitch para notas...")
    notes = detect_notes_from_pitch(pitch_track, sr)

    print(">> Classificando textura musical...")
    texture = classify_texture(y, sr)

    return {
        "pitch_track": pitch_track,
        "notes": notes,
        "texture": texture
    }


# -------------------------------------------------------------------------
# EXECUÇÃO DIRETA
# -------------------------------------------------------------------------

if __name__ == "__main__":
    result = detect_notes()
    print("\nNotas detectadas:")
    for n in result["notes"][:20]:   # evita prints gigantes
        print(n)

    print("\nTextura:", result["texture"])

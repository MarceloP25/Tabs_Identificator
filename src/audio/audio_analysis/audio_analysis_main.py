import os
import json

from note_detection import detect_notes
from harmony_analysis import analyze_frames
from identify_texture import frames_to_segments, save_texture_map
from generate_timeline import generate_timeline
from audio_observer import AudioObserver


def run_audio_analysis(processed_audio_dir, output_dir):
    print("🎧 Iniciando análise de áudio...")

    audio_files = [
        os.path.join(processed_audio_dir, f)
        for f in os.listdir(processed_audio_dir)
        if f.endswith(".wav")
    ]

    if not audio_files:
        raise FileNotFoundError("Nenhum WAV encontrado.")

    observer = AudioObserver()
    all_frames = []

    # ----------------------------
    # Extração de notas (frame-level)
    # ----------------------------
    for audio in audio_files:
        frames = detect_notes(audio)
        all_frames.extend(frames)

    print("🎼 Analisando harmonia e papel musical...")
    analyzed_frames = analyze_frames(all_frames)

    # ----------------------------
    # Observabilidade (histórico)
    # ----------------------------
    for frame in analyzed_frames:
        observer.log_frame(frame)

    observer.flush(run_id="audio_pass_3")

    # ----------------------------
    # Textura musical (segmentação)
    # ----------------------------
    print("🧩 Identificando textura (segmentos)...")
    segments = frames_to_segments(analyzed_frames)
    texture_path = save_texture_map(segments)

    # ----------------------------
    # Persistência intermediária
    # ----------------------------
    notes_path = "data/interim/notes_chords.json"
    os.makedirs(os.path.dirname(notes_path), exist_ok=True)

    with open(notes_path, "w", encoding="utf-8") as f:
        json.dump(analyzed_frames, f, indent=2, ensure_ascii=False)

    # ----------------------------
    # Timeline final
    # ----------------------------
    print("🧱 Gerando timeline final...")
    timeline = generate_timeline(
        notes_chords_path=notes_path,
        texture_map_path=texture_path,
        out_path=os.path.join(output_dir, "timeline_music.json")
    )

    print("✅ Pipeline de áudio finalizado.")
    return timeline


if __name__ == "__main__":
    run_audio_analysis(
        processed_audio_dir="../../data/processed/audio",
        output_dir="../../data/processed/audio"
    )

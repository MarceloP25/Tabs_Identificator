import os
from note_detection import detect_notes
from harmony_analysis import analyze_harmony
from identify_texture import identify_texture
from generate_timeline import generate_timeline

def run_audio_analysis(processed_audio_dir, output_dir):
    """
    Executa a pipeline completa de análise de áudio:
    1. Detecção de notas (Music21)
    2. Análise de harmonia
    3. Identificação de textura
    4. Geração de linha do tempo analítica
    """

    print("Iniciando análise de áudio...")

    # --- ETAPA 1: COLETA DOS ARQUIVOS DE ÁUDIO PROCESSADOS ---
    audio_files = [
        os.path.join(processed_audio_dir, f)
        for f in os.listdir(processed_audio_dir)
        if f.lower().endswith(".wav")
    ]

    if not audio_files:
        raise FileNotFoundError(
            f"Nenhum arquivo WAV encontrado em {processed_audio_dir}"
        )

    print(f"{len(audio_files)} arquivos localizados para análise.")

    # --- ETAPA 2: DETECÇÃO DE NOTAS ---
    all_detected_notes = []

    for audio_file in audio_files:
        print(f"Detectando notas em: {audio_file}...")
        notes = detect_notes(audio_file)
        all_detected_notes.append({
            "file": audio_file,
            "notes": notes
        })

    # --- ETAPA 3: ANÁLISE DE HARMONIA ---
    print("Executando análise de harmonia...")
    harmony_result = analyze_harmony(all_detected_notes)

    # --- ETAPA 4: IDENTIFICAÇÃO DE TEXTURA ---
    print("Identificando textura musical...")
    texture_result = identify_texture(all_detected_notes)

    # --- ETAPA 5: GERAÇÃO DE LINHA DO TEMPO ---
    print("Gerando timeline analítica...")
    timeline_path = generate_timeline(
        all_detected_notes,
        harmony_result,
        texture_result,
        output_dir
    )

    print("\nAnálise de áudio concluída!")
    return {
        "notes": all_detected_notes,
        "harmony": harmony_result,
        "texture": texture_result,
        "timeline": timeline_path,
    }


if __name__ == "__main__":
    processed_audio_dir = "../../data/processed/audio"
    output_dir = "../../data/processed/audio"

    results = run_audio_analysis(processed_audio_dir, output_dir)
    print("\nResumo final da análise:")
    print(results)

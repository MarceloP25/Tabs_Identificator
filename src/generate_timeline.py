"""
Arquivo: generate_timeline.py
Função: Unificar textura musical, notas e acordes em uma linha temporal completa.
Entradas:
  - data/interim/texture_map.json
  - data/interim/notes_chords.json
Saídas:
  - data/processed/audio/timeline_music.json
Descrição:
  Combina a estrutura e o conteúdo musical, gerando um mapa temporal consolidado
  para uso posterior na geração de tablaturas e sincronização com vídeo.
"""

import os
import json

def generate_timeline(texture_path="data/interim/texture_map.json",
                      notes_chords_path="data/interim/notes_chords.json"):
    if not os.path.exists(texture_path) or not os.path.exists(notes_chords_path):
        raise FileNotFoundError("Arquivos de entrada não encontrados.")

    with open(texture_path, "r") as f:
        texture_map = json.load(f)
    with open(notes_chords_path, "r") as f:
        notes_chords = json.load(f)

    timeline = []
    for event in notes_chords:
        for seg in texture_map:
            if seg["inicio"] <= event["inicio"] < seg["fim"]:
                combined = {**seg, **event}
                timeline.append(combined)
                break

    os.makedirs("data/processed/audio", exist_ok=True)
    output_path = "data/processed/audio/timeline_music.json"
    with open(output_path, "w") as f:
        json.dump(timeline, f, indent=2)

    print(f"✅ Linha temporal musical gerada em: {output_path}")
    return output_path

if __name__ == "__main__":
    generate_timeline()

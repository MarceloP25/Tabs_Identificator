"""
generate_timeline.py
- Consolida notes_chords.json e (opcional) texture_map.json numa timeline final:
  data/processed/audio/timeline_music.json
- Cada evento contém: inicio, fim, tipo (solo/base/mix), label, notes, voiced_prob
"""

import os
import json
from typing import List, Dict, Any

def generate_timeline(notes_chords_path: str = "data/interim/notes_chords.json",
                      texture_map_path: str = "data/interim/texture_map.json",
                      out_path: str = "data/processed/audio/timeline_music.json"):
    if not os.path.exists(notes_chords_path):
        raise FileNotFoundError("notes_chords.json não encontrado. Execute detect_notes primeiro.")

    with open(notes_chords_path, "r", encoding="utf-8") as fh:
        frames = json.load(fh)

    # try to load texture_map; if not present, generate from frames (merge contiguous roles)
    texture_map = None
    if os.path.exists(texture_map_path):
        with open(texture_map_path, "r", encoding="utf-8") as fh:
            texture_map = json.load(fh)

    # If texture_map exists, align frame events inside segments
    timeline = []
    if texture_map:
        for seg in texture_map:
            seg_start = seg["inicio"]
            seg_end = seg["fim"]
            seg_role = seg["tipo"]
            # collect frames inside this segment
            seg_frames = [f for f in frames if f["time"] >= seg_start and f["time"] < seg_end]
            if not seg_frames:
                continue
            # combine into one event per segment, but keep list of sub-events
            event = {
                "inicio": seg_start,
                "fim": seg_end,
                "tipo": seg_role,
                "subevents": seg_frames
            }
            timeline.append(event)
    else:
        # group contiguous frames by role
        if frames:
            cur = frames[0]
            start = cur["time"]
            role = cur["role"]
            sub = [cur]
            for fr in frames[1:]:
                if fr["role"] == role:
                    sub.append(fr)
                else:
                    timeline.append({
                        "inicio": start,
                        "fim": fr["time"],
                        "tipo": role,
                        "subevents": sub
                    })
                    start = fr["time"]
                    role = fr["role"]
                    sub = [fr]
            # close last
            timeline.append({
                "inicio": start,
                "fim": frames[-1]["time"] + 512/44100.0,
                "tipo": role,
                "subevents": sub
            })

    # save
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(timeline, fh, indent=2, ensure_ascii=False)

    print(f"✅ Timeline gerada em: {out_path}")
    return out_path

if __name__ == "__main__":
    generate_timeline()

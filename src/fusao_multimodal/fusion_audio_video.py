"""
fusion_audio_video.py
- Cruza timeline de áudio e vídeo por interseção temporal
- Gera eventos multimodais consolidados
"""

import json
import os
from typing import List, Dict, Any


def overlap(a_start, a_end, b_start, b_end):
    return max(0.0, min(a_end, b_end) - max(a_start, b_start))


def fuse_timelines(
    audio_timeline_path: str,
    video_timeline_path: str,
    out_path: str,
    min_overlap: float = 0.1
):
    with open(audio_timeline_path, "r", encoding="utf-8") as f:
        audio_events = json.load(f)

    with open(video_timeline_path, "r", encoding="utf-8") as f:
        video_events = json.load(f)

    fused_events = []

    for a in audio_events:
        for v in video_events:
            ov = overlap(a["inicio"], a["fim"], v["inicio"], v["fim"])
            if ov < min_overlap:
                continue

            duration = min(a["fim"], v["fim"]) - max(a["inicio"], v["inicio"])

            fused = {
                "inicio": max(a["inicio"], v["inicio"]),
                "fim": min(a["fim"], v["fim"]),
                "duration": duration,
                "audio": {
                    "tipo": a.get("tipo"),
                    "subevents": a.get("subevents", [])
                },
                "video": {
                    "tipo": v.get("tipo"),
                    "data": v.get("data", {})
                }
            }

            # confiança simples (pode evoluir depois)
            fused["confidence"] = round(
                min(
                    len(a.get("subevents", [])) / 10.0,
                    v.get("confidence", 1.0)
                ),
                2
            )

            fused_events.append(fused)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(fused_events, f, indent=2, ensure_ascii=False)

    print(f"🔗 Fusão áudio-vídeo salva em: {out_path}")
    return fused_events

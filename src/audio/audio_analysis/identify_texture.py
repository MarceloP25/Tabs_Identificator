"""
identify_texture.py
- Recebe lista de frame classifications (from harmony_analysis.analyze_frames)
- Agrupa frames contíguos por role (solo/base/mix/silence) gerando segments com start,end,type
- Salva em data/interim/texture_map.json
"""

import os
import json
from typing import List, Dict, Any

def frames_to_segments(frame_results: List[Dict[str, Any]],
                       min_duration: float = 0.25,
                       frame_hop: float = 512/44100.0) -> List[Dict[str, Any]]:
    """
    Agrupa frames consecutivos com mesmo role em segmentos.
    """
    if not frame_results:
        return []

    segments = []
    current_role = frame_results[0]['role']
    start_time = frame_results[0]['time']
    for i in range(1, len(frame_results)):
        fr = frame_results[i]
        if fr['role'] != current_role:
            end_time = frame_results[i]['time']
            duration = end_time - start_time
            if duration >= min_duration:
                segments.append({"inicio": start_time, "fim": end_time, "tipo": current_role})
            start_time = end_time
            current_role = fr['role']
    # close last
    end_time = frame_results[-1]['time'] + frame_hop
    duration = end_time - start_time
    if duration >= min_duration:
        segments.append({"inicio": start_time, "fim": end_time, "tipo": current_role})
    return segments

def save_texture_map(segments: List[Dict[str, Any]], out_path: str = "data/interim/texture_map.json"):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(segments, fh, indent=2, ensure_ascii=False)
    return out_path

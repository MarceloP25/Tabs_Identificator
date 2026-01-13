import json
import os
from datetime import datetime


def log_fusion_run(meta: dict, log_path="data/processed/fusion/fusion_runs.json"):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    runs = []
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            runs = json.load(f)

    meta["timestamp"] = datetime.now().isoformat()
    runs.append(meta)

    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(runs, f, indent=2, ensure_ascii=False)

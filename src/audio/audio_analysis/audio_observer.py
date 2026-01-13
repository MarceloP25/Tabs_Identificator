import os
import json
from datetime import datetime


class AudioObserver:
    """
    Observador de execução do pipeline de áudio.
    Armazena todos os frames analisados para inspeção futura,
    debug e fusão com visão (Passo 6).
    """

    def __init__(self, out_dir="data/debug/audio_runs"):
        self.out_dir = out_dir
        os.makedirs(self.out_dir, exist_ok=True)
        self.frames = []

    def log_frame(self, frame):
        """
        Armazena um frame analisado.
        """
        self.frames.append(frame)

    def flush(self, run_id=None):
        """
        Salva todos os frames em disco.
        """
        if run_id is None:
            run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        path = os.path.join(self.out_dir, f"{run_id}_audio_frames.json")

        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.frames, f, indent=2, ensure_ascii=False)

        print(f"🧠 Execução de áudio salva em: {path}")
        return path

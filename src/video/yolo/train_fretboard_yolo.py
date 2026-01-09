"""
Arquivo: train_fretboard_yolo.py

Objetivo:
Treinar um modelo YOLO para detectar o braço da guitarra (fretboard)
em frames de vídeo, em múltiplos ângulos e perspectivas.

Pré-requisitos:
- Dataset anotado no formato YOLO
- fretboard.yaml configurado corretamente
"""

from ultralytics import YOLO
import os


def train_fretboard_yolo():
    # --------------------------------------------------
    # Caminhos principais
    # --------------------------------------------------
    DATA_YAML = "data/yolo_dataset/fretboard.yaml"
    OUTPUT_DIR = "models"

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # --------------------------------------------------
    # Carregar modelo base (pré-treinado)
    # --------------------------------------------------
    # yolo11n.pt ou yolov8n.pt (dependendo da versão instalada)
    model = YOLO("yolo11n.pt")

    # --------------------------------------------------
    # Treinamento
    # --------------------------------------------------
    model.train(
        data=DATA_YAML,      # <-- dataset + labels
        epochs=100,          # ajuste conforme dataset
        imgsz=640,
        batch=8,
        device="cuda",       # ou "cpu"
        project=OUTPUT_DIR,
        name="fretboard_yolo",
        exist_ok=True
    )

    # --------------------------------------------------
    # Salvamento final explícito
    # --------------------------------------------------
    model.save(os.path.join(OUTPUT_DIR, "fretboard_yolo.pt"))


if __name__ == "__main__":
    train_fretboard_yolo()

"""
Arquivo: preprocess_frames.py
Função: Pré-processar frames para o Passo 2 (detecção do braço da guitarra).
Objetivo:
  - preservar geometria
  - reduzir ruído
  - manter linhas longas (trastes e cordas)
Entradas:
  - data/raw/frames/*.jpg
Saídas:
  - data/processed/frames/base/*.jpg
  - data/processed/frames/structural/*.jpg
"""

import os
import cv2
import numpy as np
from tqdm import tqdm


RAW_DIR = "data/raw/frames"
OUT_BASE = "data/processed/frames/base"
OUT_STRUCT = "data/processed/frames/structural"


def preprocess_frames(frames_dir: str = RAW_DIR):
    os.makedirs(OUT_BASE, exist_ok=True)
    os.makedirs(OUT_STRUCT, exist_ok=True)

    frame_files = sorted(f for f in os.listdir(frames_dir) if f.endswith(".jpg"))
    print(f"🖼️ Pré-processando {len(frame_files)} frames para o Passo 2...")

    for file in tqdm(frame_files):
        path = os.path.join(frames_dir, file)
        img = cv2.imread(path)

        # -------------------------------------------------
        # 1. Conversão para escala de cinza
        # -------------------------------------------------
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # -------------------------------------------------
        # 2. Redução suave de ruído (preserva estruturas)
        # -------------------------------------------------
        denoised = cv2.GaussianBlur(gray, (5, 5), 0)

        # -------------------------------------------------
        # 3. Contraste local controlado (CLAHE)
        # -------------------------------------------------
        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8, 8)
        )
        contrast = clahe.apply(denoised)

        # -------------------------------------------------
        # FRAME BASE (para CNN / detecção do braço)
        # -------------------------------------------------
        base_frame = contrast

        # -------------------------------------------------
        # FRAME ESTRUTURAL (para trastes e cordas)
        # -------------------------------------------------
        # Realça linhas longas sem fragmentar
        grad_x = cv2.Sobel(contrast, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(contrast, cv2.CV_64F, 0, 1, ksize=3)

        structural = cv2.convertScaleAbs(
            cv2.addWeighted(grad_x, 0.5, grad_y, 0.5, 0)
        )

        # -------------------------------------------------
        # Salvamento
        # -------------------------------------------------
        cv2.imwrite(os.path.join(OUT_BASE, file), base_frame)
        cv2.imwrite(os.path.join(OUT_STRUCT, file), structural)

    print("✅ Frames preparados para o Passo 2")
    print(f" - Base geométrica: {OUT_BASE}")
    print(f" - Estrutural (linhas): {OUT_STRUCT}")


if __name__ == "__main__":
    preprocess_frames()

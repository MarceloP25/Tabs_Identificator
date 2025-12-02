"""
Arquivo: preprocess_frames.py
Função: Processar os frames extraídos, aplicando filtros de ruído, correção e realce.
Entradas:
  - data/raw/frames/*.jpg
Saídas:
  - data/processed/frames/*.jpg
"""

import os
import cv2
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

def preprocess_frames(frames_dir: str = "data/raw/frames"):
    output_dir = "data/processed/frames"
    os.makedirs(output_dir, exist_ok=True)
    frame_files = sorted([f for f in os.listdir(frames_dir) if f.endswith(".jpg")])

    print(f"🎨 Processando {len(frame_files)} frames...")
    for file in tqdm(frame_files):
        path = os.path.join(frames_dir, file)
        img = cv2.imread(path)

        # --- Conversão para escala de cinza ---
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # --- Correção de iluminação ---
        gray = cv2.equalizeHist(gray)

        # --- Filtro bilateral (preserva bordas) ---
        filtered = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)

        # --- Realce de bordas (Canny) ---
        edges = cv2.Canny(filtered, 50, 150)

        # --- Combinação ---
        combined = cv2.addWeighted(filtered, 0.8, edges, 0.2, 0)

        # --- Salvamento ---
        output_path = os.path.join(output_dir, file)
        cv2.imwrite(output_path, combined)

    print(f"✅ Frames tratados salvos em: {output_dir}")

    # Exemplo visual
    sample = cv2.imread(os.path.join(output_dir, frame_files[0]))
    plt.imshow(cv2.cvtColor(sample, cv2.COLOR_BGR2RGB))
    plt.title("Exemplo de Frame Processado")
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    preprocess_frames()

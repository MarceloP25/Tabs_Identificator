"""
Arquivo: extract_audio_frames.py
Função: Receber um vídeo de entrada, extrair os frames e o áudio separadamente.
Entradas:
  - Caminho do vídeo: data/raw/video_original.mp4
Saídas:
  - Frames extraídos: data/raw/frames/frame_XXXX.jpg
  - Áudio extraído: data/raw/audio/audio_raw.wav
"""

import os
from moviepy import VideoFileClip
import cv2
from tqdm import tqdm

def extract_video_and_frames(video_path: str):
    # --- Configurações de diretórios ---
    os.makedirs("data/raw/audio", exist_ok=True)
    os.makedirs("data/raw/frames", exist_ok=True)

    # --- Verifica o arquivo ---
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {video_path}")
    
    # --- Extrai áudio ---
    print("🎵 Extraindo áudio do vídeo...")
    video = VideoFileClip(video_path)
    audio = video.audio
    audio_output = "data/raw/audio/audio_raw.wav"
    audio.write_audiofile(audio_output, codec='pcm_s16le')
    print(f"✅ Áudio salvo em: {audio_output}")

    # --- Extrai frames ---
    print("🎞️ Extraindo frames...")
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    frame_dir = "data/raw/frames"
    count = 0
    success = True

    for i in tqdm(range(frame_count)):
        success, frame = cap.read()
        if not success:
            break
        frame_name = os.path.join(frame_dir, f"frame_{count:05d}.jpg")
        cv2.imwrite(frame_name, frame)
        count += 1
    
    cap.release()
    print(f"✅ {count} frames salvos em: {frame_dir}")

if __name__ == "__main__":
    extract_video_and_frames("data/raw/exemplo_01.mp4")

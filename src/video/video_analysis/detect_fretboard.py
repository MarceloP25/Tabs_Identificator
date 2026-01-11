import cv2
import csv
import os
import random
from inference_sdk import InferenceHTTPClient

# ----------------------------
# Configurações
# ----------------------------
MODEL_ID = "guitar-object-detection-9ct1j/1"
CSV_PATH = "logs/roboflow_detections.csv"
VISUAL_SAMPLE_SIZE = 20
CONF_THRESHOLD = 0.5

os.makedirs("logs", exist_ok=True)

# Inicializa CSV (header único)
if not os.path.exists(CSV_PATH):
    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "frame_id", "x1", "y1", "x2", "y2", "confidence", "model_id"
        ])


# Inicializa cliente Roboflow (uma vez só)
CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="sVdBA38eeBKfkK7U5Hb0"
)


# Buffer para visualização aleatória
_visual_buffer = []
_frame_counter = 0
_visualized = False

def detect_fretboard(frame):
    global _frame_counter, _visualized

    result = CLIENT.infer(frame, model_id=MODEL_ID)

    predictions = result.get("predictions", [])
    if not predictions:
        _frame_counter += 1
        return None, None

    # Pega a maior box (área)
    pred = max(predictions, key=lambda p: p["width"] * p["height"])

    x_center, y_center = pred["x"], pred["y"]
    w, h = pred["width"], pred["height"]
    conf = pred["confidence"]

    x1 = int(x_center - w / 2)
    y1 = int(y_center - h / 2)
    x2 = int(x_center + w / 2)
    y2 = int(y_center + h / 2)

    # Clamp
    h_img, w_img = frame.shape[:2]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w_img, x2), min(h_img, y2)

    roi = frame[y1:y2, x1:x2]

    # ----------------------------
    # Log CSV
    # ----------------------------
    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            _frame_counter, x1, y1, x2, y2, conf, MODEL_ID
        ])

    # ----------------------------
    # Coleta para visualização
    # ----------------------------
    if not _visualized:
        vis = frame.copy()
        cv2.rectangle(vis, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            vis,
            f"{conf:.2f}",
            (x1, y1 - 8),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            1
        )
        _visual_buffer.append(vis)

        # Quando atingir 20 frames aleatórios
        if len(_visual_buffer) >= VISUAL_SAMPLE_SIZE:
            _show_visual_samples()
            _visualized = True

    _frame_counter += 1
    return roi, (x1, y1, x2, y2)


def _show_visual_samples():
    print("🖼️ Mostrando amostra de detecções do Roboflow...")

    samples = random.sample(_visual_buffer, VISUAL_SAMPLE_SIZE)

    for i, img in enumerate(samples):
        cv2.imshow(f"Roboflow Sample {i+1}", img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
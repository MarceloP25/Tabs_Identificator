from ultralytics import YOLO
import cv2


model = YOLO("models/fretboard_yolo.pt") # placeholder


def detect_fretboard(frame):
    results = model(frame, conf=0.4)
    if not results or len(results[0].boxes) == 0:
        return None, None

    box = max(results[0].boxes, key=lambda b: b.xywh[0][2] * b.xywh[0][3])

    x1, y1, x2, y2 = map(int, box.xyxy[0])
    roi = frame[y1:y2, x1:x2]


    return roi, (x1, y1, x2, y2)
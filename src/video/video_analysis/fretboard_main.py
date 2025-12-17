import cv2
from detect_fretboard import detect_fretboard
from rectify_fretboard import rectify_fretboard
from detect_frets import detect_frets
from detect_strings import detect_strings
from build_fretboard_map import build_fretboard_map


cap = cv2.VideoCapture("sample.mp4")


ret, frame = cap.read()
roi, bbox = detect_fretboard(frame)
rectified = rectify_fretboard(roi)
frets = detect_frets(rectified)
strings = detect_strings(rectified)


fretboard_map = build_fretboard_map(frets, strings, rectified.shape)


print(f"Grid gerado com {len(fretboard_map)} posições")
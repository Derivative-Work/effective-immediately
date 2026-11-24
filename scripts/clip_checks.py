"""M3: a frame-by-frame guardrail scan of the picked clips (brief: faces, green light). A screen, not a verdict: it
flags frames for a person to look at, and a clean result doesn't prove a clip is clean.

- faces: OpenCV's frontal and profile Haar cascades on every second frame (profile also mirrored).
- green: the most bright, saturated green pixels in any frame, as a share of the picture.
Usage: .venv/bin/python -I scripts/clip_checks.py [clip ...]  ->  review/m3_clip_checks.json
"""
import json
import sys

import cv2
import numpy as np

PICKS = json.load(open("config/picks.json"))["clips"]
front = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
profile = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")
out = {}
for clip in sys.argv[1:] or list(PICKS):
    path = f"assets/gen/clips/{clip}/{PICKS[clip]}.mp4"
    cap = cv2.VideoCapture(path)
    n, faces, worst = 0, [], 0.0
    while True:
        ok, f = cap.read()
        if not ok:
            break
        hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
        worst = max(worst, float((cv2.inRange(hsv, (38, 105, 80), (84, 255, 255)) > 0).mean()))
        if n % 2 == 0:
            g = cv2.equalizeHist(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY))
            hits = 0
            for det, im in ((front, g), (profile, g), (profile, cv2.flip(g, 1))):
                hits += len(det.detectMultiScale(im, 1.1, 7, minSize=(48, 48)))
            if hits:
                faces.append(n)
        n += 1
    cap.release()
    out[clip] = {"take": PICKS[clip], "frames": n, "face_flag_frames": faces, "max_green_share": round(worst, 5)}
    print(clip, PICKS[clip], n, "frames; face flags:", len(faces), faces[:8], "; max green", f"{worst:.3%}", flush=True)
json.dump(out, open("review/m3_clip_checks.json", "w"), indent=1)

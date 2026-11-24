"""M3: small deterministic guardrail fixes on picked keyframes, before they become clips (config/retouch.json).

- "desaturate": take the colour out of a box [x0, y0, x1, y1], so a green exit sign reads as a blank unlit panel.
- "blur": soften boxes [[x0, y0, x1, y1], ...], so generated digits on a keypad can't be read.
- "degreen": turn bright green LEDs into pale cool ones anywhere in the frame.
- "crush": take dim detail inside a box down to solid shadow [x0, y0, x1, y1, luma threshold], so a silhouette's profile
  shows no facial features. The bright rim light above the threshold is untouched.
The original take is kept; the result is assets/gen/stills/<item>/<item>_r_s<seed>.png.
Usage: .venv/bin/python -I scripts/retouch.py [stem ...]
"""
import json
import sys
from pathlib import Path

import cv2
import numpy as np

CFG = json.load(open("config/retouch.json"))["takes"]


for stem in sys.argv[1:] or list(CFG):
    spec = CFG[stem]
    item = stem.split("_")[0]
    src = Path(f"assets/gen/stills/{item}/{stem}.png")
    im = cv2.imread(str(src), cv2.IMREAD_COLOR)
    notes = []
    if "desaturate" in spec:  # an unlit blank panel instead of a green sign
        x0, y0, x1, y1 = spec["desaturate"]
        roi = im[y0:y1, x0:x1]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        im[y0:y1, x0:x1] = cv2.merge([gray, gray, gray])
        notes.append(f"desaturated box {x0},{y0},{x1},{y1}")
    for x0, y0, x1, y1 in spec.get("blur", []):  # generated digits on keys: soft, unreadable pads
        a = np.zeros(im.shape[:2], np.float32)
        a[y0:y1, x0:x1] = 1
        a = cv2.GaussianBlur(a, (0, 0), 2.5)[..., None]
        soft = cv2.GaussianBlur(im, (0, 0), 6.5)
        im = np.clip(im * (1 - a) + soft * a, 0, 255).astype(np.uint8)
        notes.append(f"blurred box {x0},{y0},{x1},{y1}")
    if spec.get("degreen"):  # bright, saturated, clearly green points only: the LEDs, not the teal-grey rack frames
        hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        m = cv2.inRange(hsv, (38, 105, 80), (84, 255, 255))
        m = cv2.dilate(m, np.ones((3, 3), np.uint8))
        hsv[m > 0, 0] = 104
        hsv[m > 0, 1] = (hsv[m > 0, 1] * 0.3).astype(np.uint8)
        im = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        notes.append(f"recoloured {int((m > 0).sum())} green LED px")
    if "crush" in spec:  # feathered, so no box edge shows in the hair or at the neck
        x0, y0, x1, y1, t = spec["crush"]
        pad = 30
        X0, Y0, X1, Y1 = max(x0 - pad, 0), max(y0 - pad, 0), x1 + pad, y1 + pad
        roi = im[Y0:Y1, X0:X1].astype(np.float32)
        luma = cv2.cvtColor(roi.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)
        box = np.zeros(luma.shape, np.float32)
        box[y0 - Y0:y1 - Y0, x0 - X0:x1 - X0] = 1
        box = cv2.GaussianBlur(box, (0, 0), 7)
        dark = 1 - np.clip((luma - t) / 28, 0, 1)
        a = (cv2.GaussianBlur(dark, (0, 0), 1.0) * box)[..., None]
        shadow = np.median(roi[luma < t * 0.3], axis=0)
        im[Y0:Y1, X0:X1] = np.clip(roi * (1 - a) + shadow * a, 0, 255).astype(np.uint8)
        notes.append(f"crushed detail under luma {t} in box {x0},{y0},{x1},{y1}, feathered")
    dest = src.with_name(f"{item}_r_s{stem.rsplit('_s', 1)[1]}.png")
    cv2.imwrite(str(dest), im)
    print(dest, "; ".join(notes) or "no change", flush=True)

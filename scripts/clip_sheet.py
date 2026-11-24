"""M3: a contact sheet of clip takes: one row per take, five frames across it (first, quarter, middle, three-quarter, last).

Usage: .venv/bin/python -I scripts/clip_sheet.py <out.jpg> <clip> [clip ...] [--w 360]
"""
import argparse
import json
from pathlib import Path

import cv2
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("out")
ap.add_argument("clips", nargs="+")
ap.add_argument("--w", type=int, default=360)
a = ap.parse_args()
PICKS = json.load(open("config/picks.json"))["clips"]
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 17)
TW, TH, N, LABEL = a.w, round(a.w * 512 / 1280), 5, 92
takes = [p for c in a.clips for p in sorted(Path(f"assets/gen/clips/{c}").glob("*.mp4"))]
sheet = Image.new("RGB", (LABEL + N * (TW + 3), len(takes) * (TH + 3)), (18, 18, 20))
d = ImageDraw.Draw(sheet)
for r, p in enumerate(takes):
    cap = cv2.VideoCapture(str(p))
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    y = r * (TH + 3)
    clip, seed = p.stem.split("_")[0], p.stem.rsplit("_s", 1)[1]
    d.text((6, y + 6), clip, fill=(255, 255, 255), font=font)
    picked = PICKS.get(clip) == p.stem
    d.text((6, y + 28), seed, fill=(120, 255, 150) if picked else (255, 210, 0), font=font)
    for k in range(N):
        cap.set(cv2.CAP_PROP_POS_FRAMES, round((n - 1) * k / (N - 1)))
        ok, f = cap.read()
        if ok:
            sheet.paste(Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)).resize((TW, TH), Image.LANCZOS), (LABEL + k * (TW + 3), y))
    cap.release()
Path(a.out).parent.mkdir(parents=True, exist_ok=True)
sheet.save(a.out, quality=87)
print(a.out, sheet.size, len(takes), "takes")

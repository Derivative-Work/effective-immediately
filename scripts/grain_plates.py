"""M2: pre-render the 35mm-style grain loop once (adapted from Buy It on Margin's scripts/grain_plates.py).

24 grayscale PNGs at 1280x536 (shown at 1920x804, so each grain is about 1.5 px), mid-gray 128 +- noise, blurred
slightly so it reads as clumped grain rather than digital noise. Seed from config/seeds.json.
Usage: .venv/bin/python -I scripts/grain_plates.py  ->  remotion/public/grain/grain_00.png ... grain_23.png
"""
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

seed = json.load(open("config/seeds.json"))["main"]
plates = json.load(open("config/look.json"))["grain"]["plates"]
rng = np.random.default_rng(seed)
out = Path("remotion/public/grain")
out.mkdir(parents=True, exist_ok=True)
for i in range(plates):
    n = rng.normal(0, 1, (536, 1280))
    im = Image.fromarray(np.clip(128 + n * 60, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7))
    a = np.asarray(im).astype(float)
    a = 128 + (a - 128) * (34 / (a.std() + 1e-9))  # fixed contrast after the blur
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(out / f"grain_{i:02d}.png", optimize=True)
print(plates, "plates")

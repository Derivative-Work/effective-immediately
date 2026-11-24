"""M2: one contact sheet of the rendered component stills in review/m2/.

Usage: .venv/bin/python -I scripts/m2_sheet.py  ->  review/m2_components.jpg
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

paths = sorted(Path("review/m2").glob("*.png"))
COLS, TW, TH, GAP, LABEL = 3, 640, 360, 8, 28
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
rows = (len(paths) + COLS - 1) // COLS
sheet = Image.new("RGB", (COLS * (TW + GAP) + GAP, rows * (TH + LABEL + GAP) + GAP), (30, 30, 34))
d = ImageDraw.Draw(sheet)
for i, p in enumerate(paths):
    x = GAP + (i % COLS) * (TW + GAP)
    y = GAP + (i // COLS) * (TH + LABEL + GAP)
    d.text((x + 2, y + 3), p.stem, fill=(255, 220, 120), font=font)
    sheet.paste(Image.open(p).convert("RGB").resize((TW, TH), Image.LANCZOS), (x, y + LABEL))
sheet.save("review/m2_components.jpg", quality=88)
print("review/m2_components.jpg", sheet.size, len(paths))

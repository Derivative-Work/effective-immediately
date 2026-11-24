"""M3: a contact sheet of still items, one row per item, takes labelled with their seeds and the pick marked.

Adapted from Buy It on Margin's scripts/contact_sheet.py.
Usage: .venv/bin/python -I scripts/contact_sheet.py <out.jpg> [thumb_h=300] [item ...]
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

CFG = json.load(open("config/stills.json"))
PICKS = json.load(open("config/picks.json"))["stills"]
OUT = Path(sys.argv[1])
TH = int(sys.argv[2]) if len(sys.argv) > 2 else 300
names = sys.argv[3:] or list(CFG["items"])
F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", max(15, TH // 14))
rows = []
for item in names:
    paths = sorted(Path(f"assets/gen/stills/{item}").glob("*.png"))
    if paths:
        rows.append((item, CFG["items"][item], paths))
LABEL_W = 170
sizes = {p: Image.open(p).size for _, _, ps in rows for p in ps}
widths = [LABEL_W + sum(round(TH * sizes[p][0] / sizes[p][1]) + 6 for p in ps) for _, _, ps in rows]
sheet = Image.new("RGB", (max(widths) + 6, len(rows) * (TH + 6) + 6), (18, 18, 20))
d = ImageDraw.Draw(sheet)
for r, (item, spec, paths) in enumerate(rows):
    y = 6 + r * (TH + 6)
    d.text((8, y + 4), item, fill=(255, 255, 255), font=F)
    d.text((8, y + 8 + F.size), spec["shot"][:18], fill=(170, 170, 170), font=F)
    x = LABEL_W
    for p in paths:
        w = round(TH * sizes[p][0] / sizes[p][1])
        sheet.paste(Image.open(p).convert("RGB").resize((w, TH), Image.LANCZOS), (x, y))
        picked = PICKS.get(item) == p.stem
        label = p.stem.rsplit("_s", 1)[-1]
        d.rectangle((x, y, x + F.size * 3.4, y + F.size + 6), fill=(0, 120, 60) if picked else (0, 0, 0))
        d.text((x + 4, y + 2), label, fill=(255, 255, 255) if picked else (255, 210, 0), font=F)
        x += w + 6
OUT.parent.mkdir(parents=True, exist_ok=True)
sheet.save(OUT, quality=88)
print(OUT, sheet.size, len(rows), "items")

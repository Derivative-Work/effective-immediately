"""Link the picked stills and clips into Remotion's public folder under stable names (hard links: no extra disk).

remotion/public/gen/plates/<item>.png and remotion/public/gen/clips/<clip>.mp4, from config/picks.json.
Usage: .venv/bin/python -I scripts/sync_picks.py
"""
import json
import os
from pathlib import Path

P = json.load(open("config/picks.json"))
OUT = Path("remotion/public/gen")
for sub, picks, root, ext in (("plates", P["stills"], "assets/gen/stills", "png"), ("clips", P["clips"], "assets/gen/clips", "mp4")):
    (OUT / sub).mkdir(parents=True, exist_ok=True)
    for item, stem in picks.items():
        src, dest = Path(root) / item / f"{stem}.{ext}", OUT / sub / f"{item}.{ext}"
        dest.unlink(missing_ok=True)
        os.link(src, dest)
    print(sub, len(picks))

# The boardroom's encoded shots and the probe's alpha still.
board = OUT / "boardroom"
board.mkdir(parents=True, exist_ok=True)
sources = {p.name: p for p in Path("renders/m3/boardroom").glob("*.mp4")}
probe = Path("renders/m3/boardroom/E22_probe/0001.png")
if probe.exists():
    sources["E22_probe.png"] = probe
for name, src in sources.items():
    dest = board / name
    dest.unlink(missing_ok=True)
    os.link(src, dest)
print("boardroom", len(sources))

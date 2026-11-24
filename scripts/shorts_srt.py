"""Captions for each vertical Short: the main edit's subtitle cues that fall inside the Short, timed from its first frame.
Writes deliverables/effective_immediately_short_<id>.en.srt for every entry in config/shorts.json.
Usage: .venv/bin/python -I scripts/shorts_srt.py
"""
import json
from pathlib import Path

FPS = 24
SUBS = json.load(open("remotion/public/gen/timing/subs.json"))
SUBS = SUBS["cues"] if isinstance(SUBS, dict) else SUBS
SHORTS = json.load(open("config/shorts.json"))["shorts"]


def ts(frames):
    ms = round(frames * 1000 / FPS)
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def main():
    for sid, c in SHORTS.items():
        a, b = c["from"], c["to"]
        # cues inside the Short; a fragment under 0.7 s at either edge is left out
        cues = [s for s in SUBS if min(b, s["to"]) - max(a, s["from"]) >= 0.7 * FPS]
        lines = []
        for i, s in enumerate(cues, 1):
            lines += [str(i), f"{ts(max(0, s['from'] - a))} --> {ts(min(b, s['to']) - a)}", s["text"], ""]
        out = Path(f"deliverables/effective_immediately_short_{sid}.en.srt")
        out.write_text("\n".join(lines))
        print(f"{out}: {len(cues)} cues, {(b - a) / FPS:.1f} s")


if __name__ == "__main__":
    main()

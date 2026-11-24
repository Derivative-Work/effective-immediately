"""Compare the subtitle styles: one passage in each (review/m4_sub_styles.mp4) and a sheet of four scenes in each
(review/m4_sub_styles.jpg). The passage runs from the pre-chorus into the chorus, where the set-matched style changes.
Usage: .venv/bin/python -I scripts/sub_styles.py
"""
import json
import subprocess
import tempfile
from pathlib import Path

import cv2
import numpy as np

STYLES = [("set", "A · Matched to each scene"), ("filing", "B · SEC filing typewriter"), ("broadcast", "C · TV closed captions"),
          ("lcd", "D · Desk phone display"), ("disco", "E · Boogie-funk lettering")]
SUBS = json.load(open("remotion/public/gen/timing/subs.json"))
ENTRY = "remotion/src/index.ts"


def seg(text):
    return next(s for s in SUBS if text in s["text"])


def run(*args):
    subprocess.run(["npx", "remotion", *args, "--log=error"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    a, b = seg("Unanimous")["from"] - 6, seg("Out of the building")["from"] + 34
    scenes = [seg("Took your jacket"), seg("Out of the building"), seg("Then a call comes"), seg("Came down the day")]
    tmp = Path(tempfile.mkdtemp(dir="renders"))
    parts, rows = [], []
    for style, label in STYLES:
        props = json.dumps({"stillFrame": 0, "subStyle": style, "label": label})
        out = tmp / f"{style}.mp4"
        run("render", ENTRY, "Animatic", str(out), f"--frames={a}-{b}", "--scale=0.5", "--concurrency=8", "--crf=20", "--audio-bitrate=160k", f"--props={props}")
        parts.append(out)
        cells = []
        for s in scenes:
            f = s["words"][-1]["at"] + 6
            png = tmp / f"{style}_{f}.png"
            run("still", ENTRY, "Animatic", str(png), f"--frame={f}", "--scale=0.5", f"--props={props}")
            cells.append(cv2.imread(str(png)))
        rows.append(np.hstack(cells))
    cv2.imwrite("review/m4_sub_styles.jpg", np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 86])
    inputs = sum((["-i", str(p)] for p in parts), [])
    graph = "".join(f"[{i}:v][{i}:a]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=1:a=1[v][a]"
    subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", graph, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "22",
                    "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "review/m4_sub_styles.mp4"], check=True)
    for p in tmp.iterdir():
        p.unlink()
    tmp.rmdir()
    print(f"{len(STYLES)} styles, {(b - a + 1) / 24:.1f} s each")


if __name__ == "__main__":
    main()

"""M1: one listening file of the passages to check by ear, from the master, with an index of where each one starts.

Usage: .venv/bin/python -I scripts/m1_check_clips.py  ->  review/m1_check_lines.mp3, review/m1_check_lines.md
"""
import subprocess
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf

CLIPS = [
    ("Sings \"Signed the paper\"; v2.2 has \"Filed\"", 21.3, 24.1),
    ("Sings \"Every friend from every stage\"; v2.2 has \"Ticker falling, center stage\"", 37.3, 42.2),
    ("Sings \"Dancing in the aisles\"; v2.2 has \"All booked in October, before you left me\"", 96.0, 100.4),
    ("The asides, \"Don't ask when the quarter closed\"", 100.4, 106.4),
    ("Post-chorus: \"Nobody's asking who approved it\" is missing", 111.2, 116.6),
    ("Sings \"Senior levels, oh, senior levels\"; v2.2 ends \"said it on the morning news\"", 179.7, 184.0),
    ("Sings \"says you're good enough for me\"; v2.2 has \"reasons to reconsider me\"", 204.2, 211.2),
    ("The compliance line: should sound like fast fine print", 211.4, 219.5),
    ("The cut-off zone (candidate about 226.9 s) into the outro, which has drums under it", 219.0, 236.0),
    ("The ending", 245.0, 252.0),
]
GAP_S = 0.8
FADE_S = 0.01

y, sr = sf.read("audio/track/effective-immediately.wav", always_2d=True)
gap = np.zeros((int(GAP_S * sr), y.shape[1]))
fade = int(FADE_S * sr)
ramp = np.linspace(0, 1, fade)[:, None]
parts, rows, pos = [], [], 0.0
for i, (label, a, b) in enumerate(CLIPS, 1):
    c = y[int(a * sr):int(b * sr)].copy()
    c[:fade] *= ramp
    c[-fade:] *= ramp[::-1]
    rows.append(f"| {i} | {int(pos // 60)}:{pos % 60:04.1f} | {a:.1f}–{b:.1f} | {label} |")
    parts += [c, gap]
    pos += len(c) / sr + GAP_S

Path("review").mkdir(exist_ok=True)
with tempfile.TemporaryDirectory() as t:
    wav = Path(t) / "check.wav"
    sf.write(wav, np.concatenate(parts), sr, subtype="PCM_16")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(wav), "-c:a", "libmp3lame", "-q:a", "2",
                    "review/m1_check_lines.mp3"], check=True)
Path("review/m1_check_lines.md").write_text(
    "# M1: passages to check by ear\n\n`review/m1_check_lines.mp3`, cut from the master with 0.8 s gaps.\n\n"
    "| # | In this file | In the song (s) | Check |\n| --- | --- | --- | --- |\n" + "\n".join(rows) + "\n")
print(f"{len(CLIPS)} clips, {pos:.1f} s")

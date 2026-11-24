"""The animatic's soundtrack, assembled to the sample instead of re-rendered: the edit audio from the music's first frame
and the credits instrumental from its first card, as remotion/src/Animatic.tsx places them (cut.json `musicFrom`,
`creditsFrom`). Used to swap in a new master or credits mix without re-rendering pictures that haven't changed.
Usage: .venv/bin/python -I scripts/soundtrack.py out.wav [edit_audio.wav]
"""
import json
import sys

import numpy as np
import soundfile as sf

A = json.load(open("config/audio.json"))
CUT = json.load(open("remotion/public/gen/timing/cut.json"))
SR, FPS = 48000, 24


def place(track, path, frame):
    y, sr = sf.read(path, dtype="float32", always_2d=True)
    assert sr == SR, (path, sr)
    at = frame * SR // FPS
    n = min(len(y), len(track) - at)
    track[at:at + n] += y[:n, :2]


def main():
    out, edit = sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else A["edit_audio"]
    track = np.zeros((CUT["frames"] * SR // FPS, 2), np.float32)
    place(track, edit, CUT["musicFrom"])
    place(track, A["credits"]["postfiltered"], CUT["creditsFrom"])
    sf.write(out, track, SR, subtype="PCM_24")
    print(f"{out}: {len(track) / SR:.3f} s, peak {20 * np.log10(np.abs(track).max()):.2f} dBFS")


if __name__ == "__main__":
    main()

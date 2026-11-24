"""The human's locked master, post-filtered, onto the edit's timeline (production log 18).

The master (audio/master/, human interventions 15) is generation 2 with a lead-in, the intro riff, the bass lift and the
cut. Measured against generation 2's lead vocal stem to the sample: up to the cut it is the take plus `lead_in_samples`;
after it, the take minus one bar (`offset_s`). So the timing map stays on the take, and config/audio.json carries the two
numbers.
- Checks both offsets again at several points, and stops if any has moved.
- Edit audio: the post-filtered master (music-deslop, audio/postfilter/) without its lead-in, so edit time 0 is the take's
  time 0. It is hard-linked to remotion/public/gen/audio/working.wav.
- Bass envelope from the master's own bass stem (the human lifted the bass), on the edit's timeline: timing/bass_edit.json.
Usage: .venv/bin/python -I scripts/master_audio.py
"""
import json
import os
from pathlib import Path

import numpy as np
import soundfile as sf

A = json.load(open("config/audio.json"))
FPS = 24
LEAD = "0 Lead Vocals"


def mono(path):
    y, sr = sf.read(path, dtype="float32", always_2d=True)
    return y.mean(1), sr


def lag(new, old, sr, t, guess, win=2.0, search=0.01):
    i = int(t * sr)
    x = new[i:i + int(win * sr)]
    j0 = int((t - guess - search) * sr)
    ref = old[j0:j0 + len(x) + int(2 * search * sr)]
    return i - (j0 + int(np.argmax(np.correlate(ref, x, "valid"))))


def check(sr):
    new, _ = mono(Path(A["master_stems"]) / f"{LEAD}.aif")
    old, _ = mono(Path(A["stems"]) / f"{LEAD}.wav")
    lead_in, post = A["lead_in_samples"], A["lead_in_samples"] - round(A["offset_s"] * sr)
    pre = {t: lag(new, old, sr, t, lead_in / sr) for t in (30, 90, 150, 210, 236)}
    after = {t: lag(new, old, sr, t, post / sr) for t in (242, 247, 252, 255)}
    bad = {t: v for t, v in pre.items() if v != lead_in} | {t: v for t, v in after.items() if v != post}
    if bad:
        raise SystemExit(f"offsets moved (samples): {bad}; expected {lead_in} before the cut and {post} after")
    print(f"offsets hold: +{lead_in} samples before the cut, {post} after (cut removes {A['offset_s']} s)")


def main():
    info = sf.info(A["master"])
    sr = info.samplerate
    check(sr)
    y, _ = sf.read(A["master"], dtype="float32", always_2d=True)
    head = y[:A["lead_in_samples"]]
    print(f"lead-in removed: {len(head) / sr:.3f} s, peak {20 * np.log10(np.abs(head).max() + 1e-12):.1f} dBFS")
    edit = Path(A["edit_audio"])
    edit.parent.mkdir(parents=True, exist_ok=True)
    sf.write(edit, y[A["lead_in_samples"]:], sr, subtype="PCM_24")
    pub = Path("remotion/public/gen/audio/working.wav")
    if pub.exists():
        pub.unlink()   # only the link; the earlier stand-in stays in audio/working/
    os.link(edit, pub)
    bass, _ = mono(Path(A["master_stems"]) / "3 Bass.aif")
    bass = bass[A["lead_in_samples"]:]
    h = sr // FPS
    n = len(bass) // h
    e = np.sqrt((bass[:n * h].reshape(n, h) ** 2).mean(1))
    e = np.minimum(e / max(float(np.percentile(e, 99)), 1e-6), 1.0)
    Path("timing/bass_edit.json").write_text(json.dumps({"fps": FPS, "timeline": "edit", "bass": [round(float(v), 3) for v in e]}) + "\n")
    print(f"{edit}: {(len(y) - A['lead_in_samples']) / sr:.3f} s; bass envelope {n} frames")


if __name__ == "__main__":
    main()

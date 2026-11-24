"""The credits instrumental under the fact card and disclosure (human interventions 17, decisions 31).

The human's instrumental cover (Suno, docs/suno/credits/), post-filtered with music-deslop like the master, plays from
the first fact card to the end. This links it into Remotion and writes timing/credits_map.json: its beats (so the cards
change on them) and where the music stops.
Usage: .venv/bin/python -I scripts/credits_audio.py
"""
import json
import os
from pathlib import Path

import librosa
import numpy as np

A = json.load(open("config/audio.json"))["credits"]


def main():
    src = Path(A["postfiltered"])
    pub = Path("remotion/public/gen/audio/credits.wav")
    if pub.exists():
        pub.unlink()
    os.link(src, pub)
    y, sr = librosa.load(src, sr=22050, mono=True)
    _, beats = librosa.beat.beat_track(y=y, sr=sr, trim=False)
    bt = librosa.frames_to_time(beats, sr=sr)
    hop = 256
    db = librosa.amplitude_to_db(librosa.feature.rms(y=y, frame_length=2048, hop_length=hop)[0], ref=np.max)
    t = librosa.frames_to_time(np.arange(len(db)), sr=sr, hop_length=hop)
    stop = float(t[len(db) - 1 - np.argmax(db[::-1] > -12)])   # the last moment still near full level
    out = {"source": str(src), "duration_s": round(len(y) / sr, 3), "music_stops_s": round(stop, 3),
           "bpm": round(float(60 / np.median(np.diff(bt))), 2), "beats": [round(float(b), 3) for b in bt]}
    Path("timing/credits_map.json").write_text(json.dumps(out) + "\n")
    print(f"{src}: {out['duration_s']} s, music stops at {out['music_stops_s']} s, {len(bt)} beats at {out['bpm']} bpm")


if __name__ == "__main__":
    main()

"""A listening file for the second Suno generation, so the human can judge it before it becomes the master.

Nothing here touches audio/track/ or audio/stems/. The third clip is a rough preview of the edit the take would need: the
master up to the middle of "in-tend", a short gap, then the outro from the lead and guitar stems alone, ending before the
band comes back in. The cut points come from measured levels and need checking by ear.
Usage: .venv/bin/python -I scripts/candidate_preview.py
"""
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf

C = Path("audio/candidates/gen2")
SR = 48000
CUT, OUTRO, END, FADE = 237.15, 241.40, 258.35, 0.5   # seconds in the candidate
GAP = 0.35
OUT = Path("review/gen2_check")


def main():
    mix, sr = sf.read(C / "master.wav", dtype="float32", always_2d=True)
    lead, _ = sf.read(C / "stems/0 Lead Vocals.wav", dtype="float32", always_2d=True)
    guitar, _ = sf.read(C / "stems/4 Guitar.wav", dtype="float32", always_2d=True)
    assert sr == SR
    at = lambda t: int(round(t * SR))
    silence = lambda s: np.zeros((int(s * SR), 2), np.float32)

    def edge(y, fade_in=0.004, fade_out=0.004):
        y = y.copy()
        a, b = int(fade_in * SR), int(fade_out * SR)
        y[:a] *= np.linspace(0, 1, a)[:, None]
        y[-b:] *= np.linspace(1, 0, b)[:, None]
        return y

    before = edge(mix[at(224.0):at(CUT)], 0.02, 0.005)       # a hard stop on the word
    outro = (lead + guitar)[at(OUTRO):at(END)]
    outro = edge(outro, 0.008, FADE)
    clips = [("0:29", "\"Took your jacket\": the transcripts hear \"the\" or \"her\"", edge(mix[at(29.0):at(33.5)], 0.02, 0.05)),
             ("2:49", "\"a call comes down\": the transcripts hear \"car\"", edge(mix[at(169.5):at(174.0)], 0.02, 0.05)),
             ("3:44", "Rough edit: cut on \"in-\", then the outro as voice and guitar only, ending before the band returns",
              np.concatenate([before, silence(GAP), outro]))]
    parts, rows, t = [], [], 0.0
    for when, what, y in clips:
        rows.append(f"| {int(t // 60)}:{t % 60:04.1f} | {when} | {what} |")
        parts += [y, silence(1.2)]
        t += len(y) / SR + 1.2
    out = np.concatenate(parts)
    peak = float(np.abs(out).max())
    if peak > 0.97:
        out *= 0.97 / peak
    wav = OUT.with_suffix(".wav")
    sf.write(wav, out, SR, subtype="PCM_16")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(wav), "-b:a", "192k", str(OUT.with_suffix(".mp3"))], check=True)
    wav.unlink()
    OUT.with_suffix(".md").write_text(
        "# Generation 2: what to check by ear\n\nFile: `review/gen2_check.mp3`. Full lyric comparison: `review/gen2_lyric_check.md`.\n\n"
        "| In this file | In the take | Check |\n| --- | --- | --- |\n" + "\n".join(rows) + "\n")
    print(f"{len(out) / SR:.1f} s, source peak {peak:.3f}")
    print("\n".join(rows))


if __name__ == "__main__":
    main()

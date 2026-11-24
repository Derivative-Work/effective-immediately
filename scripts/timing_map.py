"""M1: timing/timing_map.json, on the source take's timeline (adapted from Buy It on Margin's scripts/timing_map.py).

- Words: WhisperX forced alignment of lyrics/as_sung.txt against the lead vocal stem, one segment per lyric line, with
  line windows anchored on the take's transcript (timing/candidates/gen2_lead.json).
- Beats: librosa tracks the backbeat on the drums and percussion stems. The take drifts from about 115.0 to 115.5 bpm,
  so the grid follows it; pulses in the stretch with no drums (the spoken line) are put back on the local line.
- Claps: the backbeats, kept only where the drums and percussion really hit.
- Bass: a 24 fps envelope from the bass stem for the scoreboard and boardroom screen.
Everything stays in source time. config/audio.json holds the one offset that maps it onto the edit, so the human's locked
master changes that number and nothing else.
Usage: NLTK_DATA=$PWD/.venv/nltk_data .venv/bin/python scripts/timing_map.py
"""
import difflib
import hashlib
import json
import re
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf
import whisperx

AUDIO = json.load(open("config/audio.json"))
STEMS = Path(AUDIO["stems"])
LEAD = STEMS / "0 Lead Vocals.wav"
LYRICS = Path("lyrics/as_sung.txt")
TRANSCRIPT = Path("timing/candidates/gen2_lead.json")
OUT = Path("timing/timing_map.json")
SR_BEAT, HOP = 22050, 256
FPS = 24
# Lines the lead transcript has no words for (sung in the backing vocals), as [start, end] in source seconds.
WINDOWS = {"Post-Chorus|3": [117.05, 119.2]}
# Lines whose first word the aligner placed inside the line before it; the transcript heard them here (production log 14).
FIRST_WORD = {"Verse 2|2": 92.43, "Post-Chorus|0": 107.54}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def norm(word):
    return re.sub(r"[^a-z']", "", word.lower().replace("’", "'"))


def parse_lyrics():
    sections = []
    for raw in LYRICS.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        m = re.match(r"\[(.+?)\]$", line)
        if m:
            sections.append({"name": m.group(1), "lines": []})
        else:
            sections[-1]["lines"].append(line)
    return sections


def line_windows(keys, lines, words, duration):
    tokens = [(i, norm(w)) for i, text in enumerate(lines) for w in text.split() if keys[i] not in WINDOWS]
    trans = [w for w in words if w["start"] >= 0]
    sm = difflib.SequenceMatcher(a=[t for _, t in tokens], b=[norm(w["w"]) for w in trans], autojunk=False)
    first, last = {}, {}
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            li, w = tokens[a + k][0], trans[b + k]
            first.setdefault(li, w["start"])
            last[li] = w["end"]
    for i, key in enumerate(keys):
        if key in WINDOWS:
            first[i], last[i] = WINDOWS[key]
    missing = [lines[i] for i in range(len(lines)) if i not in first]
    if missing:
        raise SystemExit(f"no transcript anchor for lines {missing}")
    out = []
    for i, key in enumerate(keys):
        if key in WINDOWS:
            out.append(tuple(WINDOWS[key]))
            continue
        a = last[i - 1] + 0.02 if i > 0 else max(0.0, first[i] - 2.0)
        b = first[i + 1] - 0.02 if i + 1 < len(lines) else min(duration, last[i] + 1.0)
        out.append((a, max(b, a + 0.3)))
    return out


def align(sections, duration):
    keys = [f"{s['name']}|{j}" for s in sections for j in range(len(s["lines"]))]
    lines = [t for s in sections for t in s["lines"]]
    twords = [w for seg in json.load(open(TRANSCRIPT))["segments"] for w in seg["words"]]
    windows = line_windows(keys, lines, twords, duration)
    audio = whisperx.load_audio(str(LEAD))
    model, meta = whisperx.load_align_model(language_code="en", device="cuda")
    segs = [{"start": a, "end": b, "text": t} for t, (a, b) in zip(lines, windows)]
    flat = [w for seg in whisperx.align(segs, model, meta, audio, "cuda", return_char_alignments=False)["segments"] for w in seg["words"]]
    if len(flat) != sum(len(t.split()) for t in lines):
        raise SystemExit("aligned word count differs from the lyrics")
    pos, k = 0, 0
    for s in sections:
        out = []
        for text in s["lines"]:
            n = len(text.split())
            ws = []
            for w in flat[pos:pos + n]:
                # A word the aligner couldn't place takes its line window's start; it's flagged by its zero score.
                ws.append({"w": w["word"], "start": round(w.get("start", windows[k][0]), 3),
                           "end": round(w.get("end", w.get("start", windows[k][0]) + 0.2), 3), "score": round(w.get("score", 0.0), 3)})
            pos += n
            if keys[k] in FIRST_WORD:
                ws[0]["start_aligner"], ws[0]["start"] = ws[0]["start"], FIRST_WORD[keys[k]]
                ws[0]["end"] = max(ws[0]["end"], round(FIRST_WORD[keys[k]] + 0.2, 3))
            out.append({"text": text, "start": ws[0]["start"], "end": ws[-1]["end"],
                        "window": [round(windows[k][0], 3), round(windows[k][1], 3)], "words": ws})
            k += 1
        s["lines"] = out
        s["start"], s["end"] = out[0]["start"], out[-1]["end"]


def clap_band():
    d, _ = librosa.load(STEMS / "2 Drums.wav", sr=SR_BEAT, mono=True)
    p, _ = librosa.load(STEMS / "6 Percussion.wav", sr=SR_BEAT, mono=True)
    end = int(AUDIO["cut_source"] * SR_BEAT)
    S = np.abs(librosa.stft(d[:end] + p[:end], n_fft=1024, hop_length=HOP))
    f = librosa.fft_frequencies(sr=SR_BEAT, n_fft=1024)
    e = np.maximum(0, np.diff(np.log1p(20 * S[(f >= 1500) & (f <= 7000)]).mean(0), prepend=0))
    return e / np.percentile(e, 99.5)


def strength(env, times):
    f = librosa.time_to_frames(times, sr=SR_BEAT, hop_length=HOP)
    return np.array([env[max(0, x - 3):x + 4].max() if x < len(env) else 0.0 for x in f])


def beat_grid():
    """The take's tempo drifts from about 115.0 to 115.5 bpm, so the grid follows the backbeat instead of one constant
    tempo. Pulses that stray from their neighbours' local line (the stretch with no drums) are put back on it."""
    env = clap_band()
    _, frames = librosa.beat.beat_track(onset_envelope=env, sr=SR_BEAT, hop_length=HOP, start_bpm=57.4, tightness=600, trim=False)
    t = librosa.frames_to_time(frames, sr=SR_BEAT, hop_length=HOP)
    fixed = t.copy()
    repaired = 0
    for i in range(len(t)):
        idx = np.arange(max(0, i - 8), min(len(t), i + 9))
        keep = idx[idx != i]
        for _ in range(3):
            m, c = np.polyfit(keep, t[keep], 1)
            r = np.abs(t[keep] - (m * keep + c))
            keep = keep[r <= max(0.03, np.median(r) * 3)]
        pred = m * i + c
        if abs(t[i] - pred) > 0.035:
            fixed[i] = pred
            repaired += 1
    mid = (fixed[:-1] + fixed[1:]) / 2
    if np.median(strength(env, mid)) > np.median(strength(env, fixed)):   # the tracker locked to the off-beats: swap them
        fixed, mid = mid, fixed[1:-1]
    grid = np.sort(np.concatenate([fixed, (fixed[:-1] + fixed[1:]) / 2]))
    local = np.diff(fixed)
    return grid, fixed, env, {"pulses": int(len(fixed)), "repaired": repaired, "bpm_range": [round(float(120 / np.percentile(local, 95)), 2),
                                                                                       round(float(120 / np.percentile(local, 5)), 2)]}


def bass_env():
    y, sr = sf.read(STEMS / "3 Bass.wav", dtype="float32", always_2d=True)
    y = y.mean(1)
    h = sr // FPS
    n = len(y) // h
    e = np.sqrt((y[:n * h].reshape(n, h) ** 2).mean(1))
    e = e / max(float(np.percentile(e, 99)), 1e-6)
    return [round(float(min(v, 1.0)), 3) for v in e]


def main():
    info = sf.info(AUDIO["source"])
    duration = round(info.frames / info.samplerate, 3)
    sections = parse_lyrics()
    align(sections, duration)
    grid, back, env, fit = beat_grid()
    bpm = 60 / float(np.median(np.diff(grid)))
    # Bars: the backbeats are 2 and 4. Of the two ways to pair them, take the one that puts the choruses on a downbeat.
    chorus = [s["start"] for s in sections if s["name"].startswith(("Chorus", "Final Chorus"))]
    candidates = [(back[i::2] - (back[i + 1] - back[i]) / 2) for i in (0, 1)]
    miss = [sum(float(np.abs(c - d).min()) for c in chorus) for d in candidates]
    downbeats = candidates[int(np.argmin(miss))]
    phase = int(np.argmin(miss))
    level = float(np.median(strength(env, back)))
    claps = back[strength(env, back) >= 0.45 * level]
    tm = {
        "generated_by": "scripts/timing_map.py", "fps": FPS,
        "audio": {"source": AUDIO["source"], "sha256": sha256(AUDIO["source"]), "duration_s": duration, "suno_id": AUDIO["suno_id"]},
        "note": "All times are in the source take. Map to the edit with config/audio.json.",
        "beats": {"bpm": round(bpm, 3), "fit": fit, "beats": [round(float(t), 3) for t in grid], "bar_phase": phase,
                  "downbeats": [round(float(t), 3) for t in downbeats], "claps": [round(float(t), 3) for t in claps]},
        "sections": sections,
        "events": {"first_vocal": sections[0]["start"], "cut": AUDIO["cut_source"], "resume": AUDIO["resume_source"], "end": AUDIO["end_source"]},
    }
    OUT.parent.mkdir(exist_ok=True)
    json.dump(tm, open(OUT, "w"), indent=1, ensure_ascii=False)
    json.dump({"fps": FPS, "bass": bass_env()}, open(OUT.parent / "bass_env.json", "w"))
    print(f"{bpm:.3f} bpm, {len(grid)} beats, {len(downbeats)} bars, {len(claps)} claps, fit {fit}, bar phase {phase}")
    for s in sections:
        print(f"{s['name']:13s} {s['start']:7.2f}-{s['end']:7.2f}  {len(s['lines'])} lines")
    low = [(w["w"], w["start"], w["score"]) for s in sections for l in s["lines"] for w in l["words"] if w["score"] < 0.25]
    print(f"{sum(len(l['words']) for s in sections for l in s['lines'])} words; low alignment score: {low}")


if __name__ == "__main__":
    main()

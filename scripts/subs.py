"""The burned-in lyric subtitles, from the timing map: remotion/public/gen/timing/subs.json and timing/subtitles.srt.

One or two phrases per sung line, split at a comma when a line is too long for the letterbox. Times go through the same
source-to-edit mapping as the picture. The wording is lyrics/as_sung.txt (v2.2). The last line is split by hand, because
the take holds the first "intend" and the cut lands on the second "in-".
Usage: .venv/bin/python -I scripts/subs.py
"""
import json
import re
from pathlib import Path

TM = json.load(open("timing/timing_map.json"))
A = json.load(open("config/audio.json"))
FPS = 24
PRE = json.load(open("remotion/public/gen/timing/cut.json"))["musicFrom"]   # run scripts/cut_list.py first
CUT, OFFSET = A["cut_source"], A["offset_s"]
MAX_CHARS = 44
SET = {"Verse 1": "filing", "Pre-Chorus": "broadcast", "Chorus 1": "disco", "Verse 2": "broadcast", "Post-Chorus": "broadcast",
       "Chorus 2": "disco", "Bridge": "lcd", "Final Chorus": "discoWarm", "Spoken": "filingWarm", "Final Tag": "discoWarm", "Outro": "brass"}


def fr(t):
    return PRE + int(round((t if t <= CUT else t - OFFSET) * FPS))


def split(words):
    text = " ".join(w["w"] for w in words)
    if len(text) <= MAX_CHARS:
        return [words]
    mid, best, at = len(text) / 2, None, 0
    for i, w in enumerate(words[:-1]):
        at += len(w["w"]) + 1
        cost = abs(at - mid) - (14 if w["w"].endswith(",") else 0)
        if best is None or cost < best[0]:
            best = (cost, i + 1)
    return split(words[:best[1]]) + split(words[best[1]:])


def main():
    segs = []
    for s in TM["sections"]:
        for line in s["lines"]:
            words = line["words"]
            if s["name"] == "Final Tag":      # sung as two phrases, the second cut off mid-word
                parts = [[{"w": "We", "start": 225.03, "end": 225.2}, {"w": "did", "start": 225.14, "end": 225.3}, {"w": "not", "start": 225.24, "end": 225.45},
                          {"w": "intend,", "start": 225.48, "end": 231.6}],
                         [{"w": "we", "start": 232.44, "end": 233.8}, {"w": "did", "start": 233.84, "end": 235.2}, {"w": "not", "start": 235.24, "end": 236.25},
                          {"w": "in—", "start": 236.3, "end": CUT}]]
            else:
                parts = split(words)
            for p in parts:
                segs.append({"section": s["name"], "style": SET[s["name"]], "from": fr(p[0]["start"]) - 2, "to": fr(p[-1]["end"]) + 12,
                             "text": " ".join(w["w"] for w in p).replace(" - ", " "),
                             "words": [{"w": w["w"], "at": fr(w["start"]) - 2} for w in p]})
    for a, b in zip(segs, segs[1:]):
        a["to"] = min(a["to"], b["from"] - 1)
    cut = fr(CUT)
    for x in segs:
        if x["from"] < cut:
            x["to"] = min(x["to"], cut)
        x["to"] = max(x["to"], x["from"] + 12)
    Path("remotion/public/gen/timing").mkdir(parents=True, exist_ok=True)
    Path("remotion/public/gen/timing/subs.json").write_text(json.dumps(segs, ensure_ascii=False) + "\n")
    stamp = lambda f: f"{int(f / FPS // 3600):02d}:{int(f / FPS // 60 % 60):02d}:{int(f / FPS % 60):02d},{int(round((f / FPS % 1) * 1000)) % 1000:03d}"
    Path("timing/subtitles.srt").write_text("".join(f"{i}\n{stamp(x['from'])} --> {stamp(x['to'])}\n{x['text']}\n\n" for i, x in enumerate(segs, 1)), encoding="utf-8")
    print(len(segs), "subtitles; longest", max(len(x["text"]) for x in segs), "characters")
    for x in segs:
        if re.search(r"in—|Chief|Corporate", x["text"]):
            print(f"  {x['from']}-{x['to']} {x['text']}")


if __name__ == "__main__":
    main()

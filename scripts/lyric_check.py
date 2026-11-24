"""Compare a transcribed take with the approved lyrics, line by line, in order.

Whisper mishears sung words, so this is evidence for a human's ear: it flags lines to listen to and proves nothing alone.
Each lyric line is matched to the best run of sung words after the previous match.
Usage: .venv/bin/python -I scripts/lyric_check.py <whisper.json> <lyrics.txt> <out.md>
"""
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

NUM = {"33": "thirty three", "8k": "eight k", "8": "eight", "600": "six hundred", "115": "a hundred fifteen",
       "103": "a hundred and three", "5": "five", "2": "two", "11": "eleven"}
LOOKAHEAD = 90


def words(text):
    text = text.lower().replace("’", "'").replace("-", " ")
    out = []
    for w in re.findall(r"[a-z0-9']+", text):
        out += NUM.get(w, w).split()
    return out


def stamp(t):
    return f"{int(t // 60)}:{t % 60:04.1f}"


def main():
    src, lyr, dest = sys.argv[1:4]
    sung = []
    for seg in json.load(open(src))["segments"]:
        for w in seg["words"]:
            for part in words(w["w"]):
                sung.append((part, w.get("start", -1), w.get("end", -1)))
    lines, section = [], ""
    for raw in Path(lyr).read_text().splitlines():
        s = raw.strip()
        if not s:
            continue
        if s.startswith("["):
            section = s.strip("[]").split(" - ")[0]
            continue
        lines.append((section, s.strip("()")))
    rows, at = [], 0
    for section, line in lines:
        want = words(line)
        best = (0.0, at, at)
        for i in range(at, min(at + LOOKAHEAD, len(sung))):
            for n in range(max(1, len(want) - 3), len(want) + 4):
                got = [x[0] for x in sung[i:i + n]]
                r = SequenceMatcher(None, " ".join(want), " ".join(got), autojunk=False).ratio() - (i - at) * 0.0007
                if r > best[0]:
                    best = (r, i, i + n)
        r, i, j = best
        found = r >= 0.55 and j > i
        start = next((x[1] for x in sung[i:j] if x[1] >= 0), -1) if found else -1
        rows.append((section, line, " ".join(x[0] for x in sung[i:j]) if found else "(not found)", r if found else 0.0, start))
        if found:
            at = j
    with open(dest, "w") as f:
        f.write(f"# Sung vs approved lyrics\n\nTranscript: `{src}`. Approved: `{lyr}`. Machine transcription: confirm flagged lines by ear.\n\n")
        f.write("| Time | Section | Approved | Heard | Match |\n| --- | --- | --- | --- | --- |\n")
        for sec, line, heard, r, t in rows:
            mark = "" if r >= 0.86 else " **check**"
            f.write(f"| {stamp(t) if t >= 0 else '—'} | {sec} | {line} | {heard} | {r:.2f}{mark} |\n")
    flagged = [x for x in rows if x[3] < 0.86]
    print(f"{len(rows)} lines, {len(flagged)} flagged")
    for sec, line, heard, r, t in flagged:
        print(f"{stamp(t) if t >= 0 else '  — '} [{sec}] {r:.2f}\n   want: {line}\n   hear: {heard}")


if __name__ == "__main__":
    main()

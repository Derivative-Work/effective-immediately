"""M4: the cut list. Every shot's frame range, and the cues inside it, from the timing map.

Times are read in the source take and mapped onto the edit through config/audio.json (`offset_s` after the cut; the
human's master is measured against the take in scripts/master_audio.py). Writes remotion/public/gen/timing/{cut,bass}.json for the Animatic composition and
timing/board_cues.json for the Blender renders.

Human note on the first animatic: no repeated or time-stretched scenes. Every clip plays once, at full speed, and the
script stops with an error if a take is used twice or a slot is longer than the takes that fill it.
Usage: .venv/bin/python -I scripts/cut_list.py
"""
import json
import os
from pathlib import Path

import cv2
import numpy as np

TM = json.load(open("timing/timing_map.json"))
A = json.load(open("config/audio.json"))
BOARD = json.load(open("config/boardroom.json"))
PICK = json.load(open("config/picks.json"))["clips"]
FPS = 24
EDIT = json.load(open("config/edit.json"))
SHOT, TERM = EDIT["screenshot_frames"], EDIT["terminal_frames"]
PRE = SHOT + TERM     # before the music: E01 (the Nov 12 screenshot) and E01t (the terminal)
MUSIC_END = 276.05    # the band's last hit
OUT = Path("remotion/public/gen/timing")
TAKES = Path("remotion/public/gen/takes")
SEC = {s["name"]: s for s in TM["sections"]}
BEATS = np.array(TM["beats"]["beats"])
CLAPS = np.array(TM["beats"]["claps"])
CUT, RESUME, OFFSET = A["cut_source"], A["resume_source"], A["offset_s"]
# The master's reverb throw on "in-" dies away here (edit time); the picture fades to black over it. Written as the
# take time that edit() maps back to it.
THROW = A["throw_end_edit_s"] + OFFSET
USED = set()


def edit(t):
    return t if t <= CUT else t - OFFSET


def fr(t):
    return PRE + int(round(edit(t) * FPS))


def L(name, i):
    return SEC[name]["lines"][i]["start"]


def W(name, i, k):
    return SEC[name]["lines"][i]["words"][k]["start"]


def snap(t, within=0.16):
    """Cuts land on the nearest beat when one is close; the song's phrasing wins when none is."""
    if t > CUT:
        return t
    b = BEATS[np.abs(BEATS - t).argmin()]
    return float(b) if abs(b - t) <= within else t


def take(x):
    return PICK.get(x, x)


def frames_of(stem):
    cap = cv2.VideoCapture(f"assets/gen/clips/{stem.split('_')[0]}/{stem}.mp4")
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    if n <= 0:
        raise SystemExit(f"no clip for {stem}")
    return n


def seq(ids, a, b):
    """The takes in order at full speed, cut on beats. Each plays from about a third of its spare length."""
    TAKES.mkdir(parents=True, exist_ok=True)
    stems = [take(x) for x in ids]
    lengths = [frames_of(s) for s in stems]
    n = b - a
    if sum(lengths) < n:
        raise SystemExit(f"{ids}: {sum(lengths)} frames of clip for a {n}-frame slot")
    beat_frames = sorted({fr(float(t)) - a for t in BEATS if 0 < fr(float(t)) - a < n})
    segs, at = [], 0
    for i, (s, l) in enumerate(zip(stems, lengths)):
        if s in USED:
            raise SystemExit(f"{s} is used twice")
        USED.add(s)
        rest = sum(lengths[i + 1:])
        if i == len(stems) - 1:
            k = n - at
        else:
            want = at + round((n - at) * l / (l + rest))
            near = [x for x in beat_frames if at + 24 <= x <= at + l]
            cut = min(near, key=lambda x: abs(x - want)) if near else want
            k = max(n - at - rest, min(l, cut - at))
        dest = TAKES / f"{s}.mp4"
        if not dest.exists():
            os.link(f"assets/gen/clips/{s.split('_')[0]}/{s}.mp4", dest)
        segs.append({"src": f"gen/takes/{s}.mp4", "from": at, "frames": k, "rate": 1, "trim": (l - k) // 3})
        at += k
    return segs


def project(shot, p):
    """World point to picture pixels for a boardroom camera (1920 wide, horizontal sensor fit)."""
    c, target = np.array(shot["loc"], float), np.array(shot["target"], float)
    f = target - c
    f /= np.linalg.norm(f)
    r = np.cross(f, (0, 0, 1))
    r /= np.linalg.norm(r)
    u = np.cross(r, f)
    d = np.array(p, float) - c
    k = shot["lens"] / 36 * 1920
    return [round(float(960 + k * d @ r / (d @ f)), 2), round(float(402 - k * d @ u / (d @ f)), 2)]


def screen_quad(name):
    w, h = 1.71, 0.715
    sh = BOARD["shots"][name]
    return [project(sh, (5.95, w, 1.55 + h)), project(sh, (5.95, -w, 1.55 + h)), project(sh, (5.95, -w, 1.55 - h)), project(sh, (5.95, w, 1.55 - h))]


def voters(name):
    arms = BOARD["shots"][name]["arms"]
    n = len(arms["xs"]) if "xs" in arms else arms.get("per_side", 5)
    return {"none": 0, "near": n, "far": n, "both": 2 * n, "ring": 2 * n + 2}[arms["sides"]]


def main():
    v1, pre, ch1, v2, post, ch2, br, fin, tag, out = ("Verse 1", "Pre-Chorus", "Chorus 1", "Verse 2", "Post-Chorus", "Chorus 2",
                                                      "Bridge", "Final Chorus", "Final Tag", "Outro")
    e08 = snap(L(pre, 2))
    g02 = frames_of(take("G02")) / FPS
    e06 = min((float(b) for b in BEATS if b >= e08 - g02), default=e08 - g02)
    e22p = snap(L(fin, 4))
    plan = [
        ("E02", 0.0, "cold", {"clips": ["G14", "G13", "G01", "G15", "G16"]}),
        ("E03", snap(L(v1, 1)), "cold", {}), ("E04", snap(L(v1, 2)), "cold", {}), ("E05", snap(L(v1, 3)), "cold", {}),
        ("E07", snap(L(pre, 0)), "cold", {}),                 # E06 follows E07: this take has no gap before the pre-chorus
        ("E06", e06, "cold", {"clips": ["G02"]}),
        ("E08", e08, "cold", {"board": "E08"}),
        ("E09", snap(L(ch1, 0)), "cold", {"board": "E09", "lower": True}),
        ("E10", snap(L(ch1, 1)), "cold", {"clips": ["G03"]}),
        ("E09 strut", snap(L(ch1, 2)), "cold", {"clips": ["G17"]}),
        ("E09 row", snap(L(ch1, 3)), "cold", {"board": "B1"}),
        ("E09 window", snap(L(ch1, 4)), "cold", {"clips": ["G18"]}),
        ("E11", snap(L(ch1, 5)), "cold", {"board": "E11", "screen": "drop"}),
        ("E10 door", snap(L(ch1, 6)), "cold", {"clips": ["G19"]}),
        ("E09 side", snap(L(ch1, 7)), "cold", {"board": "B2"}),
        ("E09 top", snap(81.95), "cold", {"board": "E09"}),
        ("E12", snap(L(v2, 0)), "cold", {"clips": ["G04"]}),
        ("E13", snap(L(v2, 1)), "cold", {"clips": ["G04_s1124"]}),
        ("E14", snap(91.75), "cold", {"clips": ["G05b"]}),
        ("E15", snap(L(v2, 3)), "cold", {"clips": ["G06"], "trimFirst": 14}),
        ("E15i", snap(W(v2, 3, 4)), "cold", {}),
        ("E12 spin", snap(SEC[v2]["lines"][4]["end"]), "cold", {"clips": ["G20", "G21"]}),
        ("E16", snap(L(post, 1)), "cyan", {"clips": ["G07", "G22"]}),
        ("E17", snap(L(ch2, 0)), "cyan", {"clips": ["G08", "G23", "G24", "G25", "G26"]}),
        ("E11 close", snap(L(ch2, 5)), "cold", {"board": "E11c", "screen": "drop"}),
        ("E17 end", snap(L(ch2, 6)), "cyan", {"clips": ["G34", "G35"]}),
        ("E18", snap(SEC[ch2]["end"]), "cyan", {"clips": ["G09"]}), ("E18p", snap(W(br, 0, 3)), "cyan", {}),
        ("E18 hand", snap(L(br, 2)), "cyan", {"clips": ["G27"]}), ("E19", snap(L(br, 3)), "cyan", {}),
        ("E20", snap(L(br, 4)), "cyan", {}), ("E21", snap(L(br, 5)), "cyan", {"clips": ["G10", "G28", "G29", "G30"]}),
        ("E22", snap(L(fin, 0)), "warm", {}), ("E22s", snap(L(fin, 2)), "warm", {"board": "E22s", "screen": "recover"}),
        ("E22v", snap(L(fin, 3)), "warm", {"board": "E22", "probe": "E22"}),
        ("E22p", e22p, "warm", {"board": "E22p", "probe": "E22p"}),
        ("E23", snap(L(fin, 5)), "warm", {"clips": ["G31", "G32"]}),
        ("E23 sign", snap(L("Spoken", 0)), "warm", {}),
        ("E23 wide", snap(SEC["Spoken"]["end"]), "warm", {}),
        ("E22 top", snap(L(tag, 0)), "warm", {"board": "E22o"}),
        ("E22 side", snap(231.0), "warm", {"board": "E22b", "fadeAt": CUT}),
        ("black", THROW, None, {}), ("E24", RESUME, "warm", {}),
    ]
    end = fr(MUSIC_END)
    shots = []
    for i, (sid, t, grade, kw) in enumerate(plan):
        a, b = fr(t), fr(plan[i + 1][1]) if i + 1 < len(plan) else end
        s = {"id": sid, "from": a, "frames": b - a}
        if grade:
            s["grade"] = grade
        if "clips" in kw:
            s["segs"] = seq(kw["clips"], a, b)
            if kw.get("trimFirst"):
                s["segs"][0]["trim"] = min(kw["trimFirst"], frames_of(take(kw["clips"][0])) - s["segs"][0]["frames"])
        for k in ("board", "lower", "screen", "probe"):
            if k in kw:
                s[k] = kw[k]
        if "fadeAt" in kw:   # fade to black from this point to the shot's end
            s["fadeOut"] = fr(kw["fadeAt"]) - a
        shots.append(s)
    by = {s["id"]: s for s in shots}
    local = lambda sid, t: fr(t) - by[sid]["from"]
    in_shot = lambda sid, ts: [local(sid, float(t)) for t in ts if 0 <= local(sid, float(t)) < by[sid]["frames"]]

    by["E03"]["at"] = local("E03", W(v1, 1, 0)) + 2
    by["E05"]["at"] = max(2, local("E05", W(v1, 3, 3)) - 3)      # the lift starts on "put"
    by["E06"]["flashes"] = in_shot("E06", CLAPS)
    by["E15i"]["drawAt"] = 4
    by["E18p"]["at"] = 0
    by["E18p"]["textAt"] = max(0, local("E18p", W(br, 1, 3)) - 4)   # "honored"
    n = by["E19"]["frames"]
    by["E19"]["interval"] = max(8, int(min(local("E19", W(br, 3, 5)), n - 8) / 4))
    by["E21"]["tags"] = [max(2, local("E21", L(br, 5))), local("E21", L(br, 6)), local("E21", L(br, 7)), local("E21", W(br, 8, 3))]
    by["E21"]["segs"][0]["trim"] = 0                              # the pick-up is at the head of G10
    by["E21"]["displayFrames"] = by["E21"]["segs"][0]["frames"]
    by["E22"]["at"] = local("E22", L(fin, 1)) - 8                 # frame 8 of the sequence is the catch on the hook
    e = by["E24"]
    e["off"] = local("E24", L(out, 1))
    e["on"] = local("E24", L(out, 2))
    e["counter"] = local("E24", L(out, 3))
    e["counter2"] = local("E24", W(out, 3, 4))                    # "and two"
    e["dissolveAt"] = local("E24", SEC[out]["lines"][3]["end"])
    e["dissolveLen"] = int(1.5 * FPS)
    e["clipRate"] = 1
    beat = 60 / TM["beats"]["bpm"] * FPS
    e["creditsAt"] = e["dissolveAt"] + e["dissolveLen"]           # the credits come in over the band's last section
    e["creditStep"] = round(beat * 3)

    for s in shots:
        if "screen" in s:
            s["quad"] = screen_quad(s["board"])
            s["drop"] = max(0, local(s["id"], W(ch1, 5, 2)) - 11) if s["id"] == "E11" else (max(0, local(s["id"], W(ch2, 5, 2)) - 11) if s["id"] == "E11 close" else 8)
    claps_in = lambda start, k: sorted({fr(float(c)) - start for c in CLAPS if 0 <= fr(float(c)) - start < k})
    e09_start = by["E09"]["from"]
    by["E09"]["boardFrom"] = 0
    by["E09 top"]["boardFrom"] = by["E09 top"]["from"] - e09_start
    e09_n = by["E09 top"]["from"] + by["E09 top"]["frames"] - e09_start
    e17_start = by["E17"]["from"]
    e17_n = by["E18"]["from"] - e17_start
    e17_claps = claps_in(e17_start, e17_n)
    inserts = [{"at": c - 6, "boardFrom": max(0, c - 6), "frames": 15} for c in e17_claps[1::4]]   # one every two bars
    for k in ("E17", "E17 end"):
        s = by[k]
        off = s["from"] - e17_start
        s["inserts"] = [{"from": x["at"] - off, "boardFrom": x["boardFrom"], "frames": x["frames"]} for x in inserts
                        if x["at"] >= off and x["at"] - off + x["frames"] <= s["frames"]]
    cues = {"E09": {"frames": e09_n, "claps": claps_in(e09_start, e09_n)}, "E17i": {"frames": e17_n, "claps": e17_claps},
            "E08": {"frames": by["E08"]["frames"]}}
    for sid, name in (("E09 row", "B1"), ("E09 side", "B2"), ("E22 top", "E22o"), ("E22 side", "E22b")):
        cues[name] = {"frames": by[sid]["frames"], "claps": claps_in(by[sid]["from"], by[sid]["frames"])}
    for sid, name, rise in (("E11", "E11", max(local("E11", W(ch1, 5, 2)), 10)), ("E11 close", "E11c", max(local("E11 close", W(ch2, 5, 2)), 10)),
                            ("E22s", "E22s", min(14, by["E22s"]["frames"] // 3)), ("E22v", "E22", 8), ("E22p", "E22p", 8)):
        cues[name] = {"frames": by[sid]["frames"], "rise": rise}
    origin = {"E08": by["E08"]["from"], "E09": e09_start, "E17i": e17_start, "B1": by["E09 row"]["from"], "B2": by["E09 side"]["from"], "E22o": by["E22 top"]["from"],
              "E22b": by["E22 side"]["from"], "E11": by["E11"]["from"], "E11c": by["E11 close"]["from"], "E22s": by["E22s"]["from"], "E22": by["E22v"]["from"], "E22p": by["E22p"]["from"]}
    for name, q in cues.items():         # the beats inside each render, for the one-hand-at-a-time vote
        q["beats"] = sorted({fr(float(t)) - origin[name] for t in BEATS if 0 <= fr(float(t)) - origin[name] < q["frames"]})
    # Human note: one hand per beat only where the shot is on screen long enough to see the whole count; everywhere else
    # all up and all down on the beat. Inserts and shots cut from one long render are judged by what's on screen.
    beat = 60 / TM["beats"]["bpm"] * FPS
    on_screen = {"E09": max(by["E09"]["frames"], by["E09 top"]["frames"]), "E17i": 15}
    for name, q in cues.items():
        if q.get("rise") is not None and q["beats"]:     # the event lands on the beat nearest its word
            q["rise"] = min(q["beats"], key=lambda x: abs(x - q["rise"]))
        need = (voters(name) + 2 + (6 if name == "E22" else 0)) * beat      # everyone up, a moment to read it, and E22's gag
        q["vote"] = "one_by_one" if name == "E08" or (voters(name) and on_screen.get(name, q["frames"]) >= need) else "unison"
    for sid, name in (("E11", "E11"), ("E11 close", "E11c")):
        by[sid]["drop"] = max(0, cues[name]["rise"] - 11)
    print("one hand per beat:", [k for k, q in cues.items() if q["vote"] == "one_by_one" and voters(k)])
    Path("timing/board_cues.json").write_text(json.dumps(cues) + "\n")

    # After the music: E25, then the cards over the credits instrumental (human interventions 17). Each card's length is its
    # share of the words at an even reading pace, so that the last card lands a few seconds before the instrumental stops;
    # every change falls on one of its beats.
    CM = json.load(open("timing/credits_map.json"))
    CB = np.array(CM["beats"])
    C = json.load(open("config/cards.json"))
    nwords = lambda xs: sum(len(x.split()) for x in xs)
    reading = [("Fact card 1", nwords(C["facts"][0:4])), ("Fact card 2", nwords(C["facts"][4:8])), ("Fact card 3", nwords(C["facts"][8:])),
               ("Disclosure", nwords([C["disclosure"], C["probe_note"]]))]
    DATED_S, FINAL_S = 7.0, 6.0
    per_word = (CM["music_stops_s"] - DATED_S - FINAL_S) / sum(k for _, k in reading)
    on_beat = lambda t: float(CB[np.abs(CB - t).argmin()])
    tail = [{"id": "E25", "from": end, "frames": EDIT["e25_frames"]}]
    credits_from = end + EDIT["e25_frames"]
    bounds, t = [0.0], 0.0
    for _, k in reading:
        t += k * per_word
        bounds.append(on_beat(t))
    bounds.append(on_beat(CM["music_stops_s"] - FINAL_S))
    bounds.append(CM["duration_s"] + 0.5)
    names = [n for n, _ in reading] + ["Dated cards", "Final card"]
    bar = round(4 * 60 / CM["bpm"] * FPS)
    for i, sid in enumerate(names):
        a_, b_ = credits_from + round(bounds[i] * FPS), credits_from + round(bounds[i + 1] * FPS)
        tail.append({"id": sid, "from": a_, "frames": b_ - a_, **({"interval": bar} if sid == "Dated cards" else {})})
    at = tail[-1]["from"] + tail[-1]["frames"]
    print("reading pace", round(1 / per_word * 60), "words a minute;", " ".join(f"{x['id']}:{x['frames'] / FPS:.1f}s" for x in tail))
    all_shots = [{"id": "E01", "from": 0, "frames": SHOT}, {"id": "E01t", "from": SHOT, "frames": TERM}] + shots + tail
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "cut.json").write_text(json.dumps({"fps": FPS, "musicFrom": PRE, "creditsFrom": credits_from, "frames": at, "shots": all_shots}) + "\n")
    src = json.load(open("timing/bass_edit.json"))["bass"]   # the master's bass stem, already on the edit's timeline
    bass = [0.0] * at
    for i, v in enumerate(src):
        if 0 <= PRE + i < at:
            bass[PRE + i] = v
    (OUT / "bass.json").write_text(json.dumps(bass) + "\n")
    bad = [s["id"] for s in all_shots if s["frames"] <= 0]
    if bad:
        raise SystemExit(f"empty shots: {bad}")
    print(f"{len(all_shots)} shots, {at} frames, {at / FPS:.1f} s; music from frame {PRE} to {end}; {len(USED)} takes, each used once, all at full speed")
    print(" ".join(f"{s['id'].replace(' ', '_')}:{s['frames'] / FPS:.1f}" for s in all_shots))


if __name__ == "__main__":
    main()

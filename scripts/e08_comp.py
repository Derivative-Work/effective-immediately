"""E08: the narrator as generated footage (G36) instead of a Blender figure (human note: "still obviously a render").

G36 is her walking on plain white with the camera tracking her. Its luminance gives a matte; each frame is stabilised on
her body, scaled to her height at her place behind the table, and laid over the room. The board, chairs and table
(the Blender "matte" pass) stay in front of her. Output: renders/m3/boardroom/E08_comp/%04d.png
Usage: .venv/bin/python -I scripts/e08_comp.py
"""
import json
from pathlib import Path

import cv2
import numpy as np
from scipy.ndimage import gaussian_filter1d

CFG = json.load(open("config/boardroom.json"))
SHOT = CFG["shots"]["E08"]
PICK = json.load(open("config/picks.json"))["clips"]["G36"]
FRAMES = json.load(open("timing/board_cues.json"))["E08"]["frames"]
ROOT = Path("renders/m3/boardroom")
OUT = ROOT / "E08_comp"
WALK_Y, HEIGHT = 2.1, 1.72           # metres: her line behind the far chairs, and her height
INK = np.array([6, 5, 5], np.float32)  # BGR, the board's black


def camera(x_offset):
    c = np.array(SHOT["loc"], float)
    t = np.array(SHOT["target"], float)
    f = (t - c) / np.linalg.norm(t - c)
    r = np.cross(f, (0, 0, 1))
    r /= np.linalg.norm(r)
    u = np.cross(r, f)
    c = c + np.array([x_offset, 0, 0])
    k = SHOT["lens"] / 36 * 1920
    return lambda p: (960 + k * (np.array(p) - c) @ r / ((np.array(p) - c) @ f), 402 - k * (np.array(p) - c) @ u / ((np.array(p) - c) @ f))


def read_matte():
    cap = cv2.VideoCapture(f"assets/gen/clips/G36/{PICK}.mp4")
    out = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32)
        out.append(np.clip((205 - g) / 150, 0, 1))
    cap.release()
    return out


def main():
    mattes = read_matte()
    if len(mattes) < FRAMES:
        raise SystemExit(f"G36 has {len(mattes)} frames for a {FRAMES}-frame shot")
    boxes = []
    for a in mattes:
        ys, xs = np.nonzero(a > 0.5)
        body = xs[ys > ys.min() + 0.3 * (ys.max() - ys.min())]   # below the pointing arm, so the arm doesn't move her centre
        boxes.append((float(np.median(body)), float(ys.min()), float(ys.max())))
    boxes = np.array(boxes)
    cx, top = gaussian_filter1d(boxes[:, 0], 4), gaussian_filter1d(boxes[:, 1], 4)
    tall = float(np.median(boxes[:, 2] - boxes[:, 1]))
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.png"):
        old.unlink()
    for f in range(FRAMES):
        name = f"{f + 1:04d}.png"
        bg = cv2.imread(str(ROOT / "E08" / name)).astype(np.float32)
        fg = cv2.imread(str(ROOT / "E08_matte" / name), cv2.IMREAD_UNCHANGED)[..., 3].astype(np.float32) / 255
        fg = cv2.erode(fg, np.ones((3, 3), np.uint8))   # so the bright window in a soft foreground edge can't ring round her
        h, w = bg.shape[:2]
        s = w / 1920
        x = -3.5 + 7.0 * f / max(1, FRAMES)
        proj = camera(SHOT.get("track", 0) * x)
        hx, hy = proj((x, WALK_Y, HEIGHT))
        _, fy = proj((x, WALK_Y, 0.0))
        k = (fy - hy) * s / tall
        M = np.float32([[k, 0, hx * s - k * cx[f]], [0, k, hy * s - k * top[f]]])
        a = cv2.warpAffine(mattes[f], M, (w, h), flags=cv2.INTER_AREA if k < 1 else cv2.INTER_LINEAR)[..., None]
        a = a * (1 - fg[..., None])
        cv2.imwrite(str(OUT / name), np.clip(bg * (1 - a) + INK * a, 0, 255).astype(np.uint8))
    print(f"E08 comp: {FRAMES} frames, G36 {PICK}, scale at the start {k:.3f}")


if __name__ == "__main__":
    main()

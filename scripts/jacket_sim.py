"""E05 and E22: the jacket comes off its hook and drops back on it, with weight (human note on the first-pass reel).

The cutout is warped along a simulated hanging chain, so it unhooks, pulls away from the wall, stretches, lags behind the
lift and swings. Each sleeve has its own damped spring. On the return it falls, catches on the hook, swings and settles
slightly crooked (brief, E22). The cast shadow moves off the wall with it. Deterministic: there is no randomness.

Writes straight-alpha PNGs the size of the S01 plate to remotion/public/gen/jacket_sim/{lift,return}/ and meta.json.
Usage: .venv/bin/python -I scripts/jacket_sim.py
"""
import json
from pathlib import Path

import cv2
import numpy as np

GEN = Path("remotion/public/gen")
LAYOUT = json.load(open(GEN / "s01_layout.json"))
PW, PH = LAYOUT["plate"]
J = LAYOUT["jacket"]
OUT = GEN / "jacket_sim"
NODES, ROWS, SUB, ITER = 26, 64, 10, 12
COLS = np.array([0, 0.2, 0.3, 0.7, 0.8, 1.0])
SLEEVE = np.array([-1, -0.6, 0, 0, 0.6, 1])
GRAVITY = 7500.0      # px/s^2: the jacket's 495 px stand for about 65 cm
STRETCH, BEND, DAMP = 0.62, 0.11, 0.992
CROOKED_DEG = 3.2
DT = 1 / 24 / SUB
HOOK = np.array([J["x"] + J["w"] / 2, J["y"], 0.0])
REST = J["h"] / (NODES - 1)


def smooth(t):
    t = np.clip(t, 0, 1)
    return t * t * (3 - 2 * t)


def lift_path(t):
    """Up off the hook, out from the wall, then away and out of the top of the frame."""
    up = 20 * smooth(t / 4) + 24 * smooth((t - 4) / 6)
    out = 8 * smooth(t / 4) + 86 * smooth((t - 4) / 6) + 50 * smooth((t - 10) / 20)
    side = 14 * smooth((t - 4) / 6) + 120 * np.clip((t - 10) / 22, 0, 1) ** 2
    away = (J["y"] + J["h"] * 1.42) * np.clip((t - 10) / 20, 0, 1) ** 2.4
    return HOOK + np.array([side, -(up + away), out])


def return_path(t):
    """Falls in from above and stops dead on the hook at frame 8."""
    u = np.clip(t / 8, 0, 1)
    return HOOK + np.array([34 * (1 - u), -(J["y"] + J["h"] * 1.2) * (1 - u * u), 64 * (1 - u)])


def relax(p, root):
    for _ in range(ITER):
        p[0] = root
        d = p[1:] - p[:-1]
        length = np.maximum(np.linalg.norm(d, axis=1, keepdims=True), 1e-6)
        fix = d * (length - REST) / length * STRETCH
        p[1:] -= fix * 0.5
        p[:-1] += fix * 0.5
        p[0] = root
        p[1:-1] += BEND * ((p[:-2] + p[2:]) / 2 - p[1:-1])
        p[:, 2] = np.maximum(p[:, 2], 0)      # the wall
    p[0] = root
    for i in range(1, NODES):                 # leather barely stretches and doesn't concertina
        d = p[i] - p[i - 1]
        length = max(float(np.linalg.norm(d)), 1e-6)
        p[i] = p[i - 1] + d / length * np.clip(length, REST * 0.93, REST * 1.05)


def step(p, prev, root, tilt):
    g = np.array([np.sin(tilt), np.cos(tilt), 0.0]) * GRAVITY
    nxt = p + (p - prev) * DAMP + g * DT * DT
    relax(nxt, root)
    return nxt, p


def settled():
    """The chain at rest on the hook. Its small stretch is subtracted later, so frame 0 is the still exactly."""
    p = np.array([HOOK + [0, i * REST, 0] for i in range(NODES)])
    prev = p.copy()
    for _ in range(1200):
        p, prev = step(p, prev, HOOK, 0.0)
        prev = p + (prev - p) * 0.9
    return p


def simulate(path, frames, start, tilt_at=None, catch=None):
    p = start.copy() + (path(0.0) - start[0])
    prev = p.copy()
    states, sleeves = [], []
    s = np.zeros(2)
    sv = np.zeros(2)
    for f in range(frames):
        for k in range(SUB):
            t = f + k / SUB
            root = path(t)
            acc = (path(t + 1 / SUB) - 2 * root + path(t - 1 / SUB)) / DT ** 2 if t > 0 else np.zeros(3)
            tilt = np.radians(CROOKED_DEG) * smooth((t - tilt_at) / 3) if tilt_at is not None else 0.0
            p, prev = step(p, prev, root, tilt)
            if catch is not None and abs(t - catch) < 1e-6:  # the hook takes the fall: most of the speed goes at once
                prev = p + (prev - p) * 0.22
            if catch is not None and t > catch:              # and the swing dies away quickly
                prev = p + (prev - p) * 0.985
            drive = np.array([acc[0] * 0.012 + acc[1] * 0.006, -acc[0] * 0.012 + acc[1] * 0.006])
            w = np.array([24.0, 21.0])
            sv += (drive * 34 - w * w * s - 2 * 0.24 * w * sv) * DT
            s = np.clip(s + sv * DT, -30, 30)
        states.append(p.copy())
        sleeves.append(s.copy())
    return states, sleeves


def along(nodes):
    """Row positions and unit tangents along the chain (Catmull-Rom through the nodes)."""
    u = np.linspace(0, NODES - 1, ROWS + 1)
    i = np.clip(u.astype(int), 0, NODES - 2)
    t = (u - i)[:, None]
    p0, p1, p2, p3 = nodes[np.maximum(i - 1, 0)], nodes[i], nodes[i + 1], nodes[np.minimum(i + 2, NODES - 1)]
    pos = 0.5 * (2 * p1 + (p2 - p0) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2 + (3 * p1 - p0 - 3 * p2 + p3) * t ** 3)
    tan = np.gradient(pos[:, :2], axis=0)
    return pos, tan / np.maximum(np.linalg.norm(tan, axis=1, keepdims=True), 1e-6)


def draw(src, nodes, sleeve):
    """Premultiplied BGRA of the plate with the jacket warped onto its chain."""
    canvas = np.zeros((PH, PW, 4), np.float32)
    pos, tan = along(nodes)
    h, w = src.shape[:2]
    r = np.linspace(0, 1, ROWS + 1)
    grid = np.zeros((ROWS + 1, len(COLS), 2), np.float32)
    for j in range(ROWS + 1):
        k = 1 + pos[j, 2] / 1600
        n = np.array([tan[j, 1], -tan[j, 0]])
        for c, u in enumerate(COLS):
            side = sleeve[0] if SLEEVE[c] < 0 else sleeve[1]
            swing = abs(SLEEVE[c]) * side * r[j] ** 1.4
            grid[j, c] = pos[j, :2] + n * (u - 0.5) * J["w"] * k + np.array([swing, -abs(swing) * 0.22])
    for j in range(ROWS):
        y0, y1 = r[j] * h, r[j + 1] * h
        shade = 1 - 0.24 * min(1.0, abs(float(tan[j, 0]))) + min(0.06, pos[j, 2] / 2400)
        for c in range(len(COLS) - 1):
            x0, x1 = COLS[c] * w, COLS[c + 1] * w
            a = np.float32([[x0, y0], [x1, y0], [x1, y1], [x0, y1]])
            b = np.float32([grid[j, c], grid[j, c + 1], grid[j + 1, c + 1], grid[j + 1, c]])
            lo, hi = np.floor(b.min(0)).astype(int) - 2, np.ceil(b.max(0)).astype(int) + 3
            lo, hi = np.maximum(lo, 0), np.minimum(hi, [PW, PH])
            if (hi <= lo).any():
                continue
            M = cv2.getPerspectiveTransform(a, b - lo.astype(np.float32))
            cell = cv2.warpPerspective(src, M, (int(hi[0] - lo[0]), int(hi[1] - lo[1])), flags=cv2.INTER_LINEAR)
            cell[..., :3] *= shade
            roi = canvas[lo[1]:hi[1], lo[0]:hi[0]]
            roi[:] = cell + roi * (1 - cell[..., 3:])
    return canvas


def with_shadow(fg, z):
    """The soft shadow on the wall: it slides, spreads and fades as the jacket leaves it."""
    s = cv2.warpAffine(fg[..., 3], np.float32([[1, 0, 8 + 0.5 * z], [0, 1, 14 + 0.55 * z]]), (PW, PH))
    s = cv2.GaussianBlur(s, (0, 0), 7 + 0.12 * z) * 0.42 * (1 - min(z / 260, 0.7))
    a = fg[..., 3] + s * (1 - fg[..., 3])
    rgb = fg[..., :3] / np.maximum(a[..., None], 1e-4)
    return np.dstack([np.clip(rgb, 0, 1), a])


def main():
    im = cv2.imread(str(GEN / "jacket.png"), cv2.IMREAD_UNCHANGED)
    im = cv2.resize(im, (J["w"], J["h"]), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    im[..., :3] *= im[..., 3:] * 0.86          # the plate's exposure, premultiplied
    base = settled()
    true_rest = np.array([HOOK + [0, i * REST, 0] for i in range(NODES)])
    offset = base - true_rest
    print(f"rest stretch at the hem: {offset[-1, 1]:.1f} px", flush=True)
    meta = {}
    for name, path, frames, tilt, catch in (("lift", lift_path, 40, None, None), ("return", return_path, 44, 8.0, 8.0)):
        d = OUT / name
        d.mkdir(parents=True, exist_ok=True)
        states, sleeves = simulate(path, frames, base, tilt, catch)
        for f, (p, s) in enumerate(zip(states, sleeves)):
            nodes = p - offset
            nodes[:, 2] = np.maximum(nodes[:, 2], 0)
            z = float(nodes[:, 2].mean())
            rgba = with_shadow(draw(im, nodes, s), z)
            cv2.imwrite(str(d / f"{f:04d}.png"), (rgba * 255 + 0.5).astype(np.uint8), [cv2.IMWRITE_PNG_COMPRESSION, 2])
        meta[name] = {"frames": frames}
        drift = np.abs(np.diff(np.array(states[-5:]), axis=0)).max()
        print(name, frames, f"frames; last-frame motion {drift:.2f} px", flush=True)
    (OUT / "meta.json").write_text(json.dumps(meta) + "\n")


if __name__ == "__main__":
    main()

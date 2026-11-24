"""Track a blank glowing screen so on-screen text can be corner-pinned to it (E20, E21's caller ID; the phone plates).

New code for this video, following the method the human pointed to: find the screen's quad from lines fitted to its
four edges, register every frame to one clean reference frame with a homography (ECC) so the shape can't drift or warp,
smooth the corners with a zero-lag filter, then corner-pin in Remotion (remotion/src/look/pin.ts).

Corners are written in picture pixels (1920x804), after the same object-fit: cover the reel applies.
Usage: .venv/bin/python -I scripts/track_display.py clip <video> <out.json> [--ref 40]
       .venv/bin/python -I scripts/track_display.py still <image> <out.json>
"""
import argparse
import json
from pathlib import Path

import cv2
import numpy as np
from scipy.ndimage import gaussian_filter1d

PIC_W, PIC_H = 1920, 804


def to_picture(q, w, h):
    k = max(PIC_W / w, PIC_H / h)
    return q * k + np.array([(PIC_W - w * k) / 2, (PIC_H - h * k) / 2])


def order(pts):
    pts = np.asarray(pts, np.float32).reshape(4, 2)
    c = pts.mean(0)
    pts = pts[np.argsort(np.arctan2(pts[:, 1] - c[1], pts[:, 0] - c[0]))]
    return np.roll(pts, -int(np.argmin(pts.sum(1))), axis=0)  # TL, TR, BR, BL


def screen_mask(bgr, v_min, s_max):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    m = ((hsv[..., 2] >= v_min) & (hsv[..., 1] <= s_max)).astype(np.uint8) * 255
    return cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))


def fit_quad(mask):
    """The largest bright, nearly rectangular region, as the intersection of lines fitted to its four sides."""
    cs, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cs = [c for c in cs if cv2.contourArea(c) > 0.004 * mask.size]
    cs = [c for c in cs if cv2.contourArea(c) / max(cv2.minAreaRect(c)[1][0] * cv2.minAreaRect(c)[1][1], 1) > 0.72]
    if not cs:
        return None
    c = max(cs, key=cv2.contourArea)
    # A screen seen in perspective is not a rectangle, so its rough corners come from the outline, not a bounding box.
    hull = cv2.convexHull(c)
    per = cv2.arcLength(hull, True)
    box = next((order(ap) for ap in (cv2.approxPolyDP(hull, e * per, True) for e in (0.01, 0.02, 0.03, 0.045, 0.06, 0.08))
                if len(ap) == 4), order(cv2.boxPoints(cv2.minAreaRect(c))))
    pts = c.reshape(-1, 2).astype(np.float32)
    lines = []
    for i in range(4):
        a, b = box[i], box[(i + 1) % 4]
        d = b - a
        L = np.linalg.norm(d)
        n = np.array([-d[1], d[0]]) / L
        t = ((pts - a) @ d) / (L * L)
        near = pts[(np.abs((pts - a) @ n) < max(4, 0.06 * L)) & (t > 0.12) & (t < 0.88)]
        if len(near) < 8:
            return None
        vx, vy, x0, y0 = cv2.fitLine(near, cv2.DIST_HUBER, 0, 0.01, 0.01).ravel()
        lines.append((np.array([x0, y0]), np.array([vx, vy])))
    out = []
    for i in range(4):
        (p1, d1), (p2, d2) = lines[i - 1], lines[i]
        A = np.array([d1, -d2]).T
        if abs(np.linalg.det(A)) < 1e-3:
            return None
        out.append(p1 + np.linalg.solve(A, p2 - p1)[0] * d1)
    return order(out)


def above_notch(mask, q):
    """A phone's notch makes the fit take the notch's lower edge as the top: refit it to the screen either side of it."""
    h = float(np.linalg.norm(q[3] - q[0]))
    pts = []
    for u in np.r_[np.linspace(0.1, 0.18, 14), np.linspace(0.82, 0.9, 14)]:
        x, y = q[0] + (q[1] - q[0]) * u
        cx, row = int(round(x)), int(y) + 1   # walk up from inside the screen, so a pale wall behind the phone can't count
        if mask[row, cx] == 0:
            continue
        stop = max(0, int(y - 0.09 * h))
        while row > stop and mask[row - 1, cx] > 0:
            row -= 1
        if row > stop:
            pts.append((x, row))
    if len(pts) < 16:
        raise SystemExit("couldn't find the screen either side of the notch")
    vx, vy, x0, y0 = cv2.fitLine(np.float32(pts), cv2.DIST_HUBER, 0, 0.01, 0.01).ravel()
    top_p, top_d = np.array([x0, y0]), np.array([vx, vy])
    out = q.copy()
    for corner, below in ((0, 3), (1, 2)):
        d = q[corner] - q[below]
        A = np.array([d, -top_d]).T
        out[corner] = q[below] + np.linalg.solve(A, top_p - q[below])[0] * d
    return out


def grow(q, frac):
    c = q.mean(0)
    return c + (q - c) * (1 + frac)


def register(ref_grey, grey, ref_quad, warp):
    """The homography taking the reference frame to this one, measured on the device round the screen."""
    h, w = ref_grey.shape
    mask = np.zeros((h, w), np.uint8)
    cv2.fillConvexPoly(mask, grow(ref_quad, 0.22).astype(np.int32), 255)
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 120, 1e-5)
    _, out = cv2.findTransformECC(ref_grey, grey, warp.copy(), cv2.MOTION_HOMOGRAPHY, crit, mask, 5)
    return out


def track_clip(path, ref_i, v_min, s_max):
    cap = cv2.VideoCapture(str(path))
    frames = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        frames.append(f)
    cap.release()
    h, w = frames[0].shape[:2]
    grey = [cv2.GaussianBlur(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (0, 0), 1.2).astype(np.float32) for f in frames]
    ref_quad = fit_quad(screen_mask(frames[ref_i], v_min, s_max))
    if ref_quad is None:
        raise SystemExit(f"no screen found in reference frame {ref_i}")
    n = len(frames)
    quads = [None] * n
    quads[ref_i] = ref_quad
    failed = []
    for i in range(n):
        if i == ref_i:
            continue
        # Each frame starts from its own edge detection, so a fast camera move can't carry an error into the next frame.
        seen = fit_quad(screen_mask(frames[i], v_min, s_max))
        if seen is None:
            failed.append(i)
            continue
        start = cv2.getPerspectiveTransform(ref_quad, seen).astype(np.float32)
        quads[i] = seen
        try:
            warp = register(grey[ref_i], grey[i], ref_quad, start)
            q = cv2.perspectiveTransform(ref_quad.reshape(-1, 1, 2), warp.astype(np.float64)).reshape(4, 2)
            if np.linalg.norm(q - seen, axis=1).max() < 2.5:  # the finer fit is kept only if it agrees with the edges
                quads[i] = q
        except cv2.error:
            pass
    known = [i for i, q in enumerate(quads) if q is not None]
    arr = np.stack([np.stack([np.interp(range(n), known, [quads[i][c, a] for i in known]) for a in (0, 1)], 1)
                    for c in range(4)], 1)  # frames x corners x xy
    smooth = gaussian_filter1d(arr, 1.0, axis=0, mode="nearest")

    # Check each tracked quad against an independent per-frame detection of the screen's edges.
    errs = []
    for i, f in enumerate(frames):
        q = fit_quad(screen_mask(f, v_min, s_max))
        if q is not None:
            errs.append(float(np.linalg.norm(q - smooth[i], axis=1).max()))
    jerk = np.linalg.norm(np.diff(smooth, n=2, axis=0), axis=2)
    stats = {"frames": n, "ref": ref_i, "ecc_failures": failed, "detected_frames": len(errs),
             "corner_error_px_median": round(float(np.median(errs)), 2), "corner_error_px_p95": round(float(np.percentile(errs, 95)), 2),
             "corner_jerk_px_p95": round(float(np.percentile(jerk, 95)), 3)}
    return [to_picture(q, w, h).round(2).tolist() for q in smooth], stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", choices=["clip", "still"])
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--ref", type=int, default=40)
    ap.add_argument("--v-min", type=int, default=165)
    ap.add_argument("--s-max", type=int, default=110)
    ap.add_argument("--notch", action="store_true")
    a = ap.parse_args()
    if a.kind == "clip":
        quads, stats = track_clip(a.src, a.ref, a.v_min, a.s_max)
    else:
        img = cv2.imread(a.src)
        mask = screen_mask(img, a.v_min, a.s_max)
        q = fit_quad(mask)
        if q is None:
            raise SystemExit("no screen found")
        if a.notch:
            q = above_notch(mask, q)
        quads, stats = [to_picture(q, img.shape[1], img.shape[0]).round(2).tolist()], {"frames": 1}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps({"source": a.src, "picture": [PIC_W, PIC_H], "stats": stats, "quads": quads}) + "\n")
    print(json.dumps(stats))


if __name__ == "__main__":
    main()

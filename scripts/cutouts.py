"""M3: the composited assets from the picked stills (config/picks.json, config/composite.json), into remotion/public/gen/.

- jacket.png: the jacket cut out of its plain background, the hanger removed.
- plaque.png: the blank brass plaque cut out.
- S01b.png: the lobby wall with the jacket-shaped patch where the paint never faded (brief E05). The patch is the cutout's
  own silhouette at the position it hangs in, so the jacket drops back into it exactly (E22). S01 is S01b with the jacket
  composited on it, in Remotion, so nothing about the wall changes between the two.
Usage: .venv/bin/python -I scripts/cutouts.py
"""
import json
from pathlib import Path

import cv2
import numpy as np
from scipy import ndimage as ndi

PICKS = json.load(open("config/picks.json"))["stills"]
CFG = json.load(open("config/composite.json"))
OUT = Path("remotion/public/gen")
OUT.mkdir(parents=True, exist_ok=True)
still = lambda item: cv2.imread(f"assets/gen/stills/{item}/{PICKS[item]}.png", cv2.IMREAD_COLOR)


def largest(mask):
    lab, n = ndi.label(mask)
    if not n:
        raise SystemExit("empty mask")
    return lab == (np.argmax(ndi.sum(mask, lab, range(1, n + 1))) + 1)


def crop_rgba(bgr, alpha):
    ys, xs = np.nonzero(alpha > 8)
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    return np.dstack([bgr, alpha])[y0:y1, x0:x1]


# ---- the jacket: GrabCut for the outline, then only what's darker than the backdrop, so its soft cast shadow stays out.
# v1 thresholded alone, which cut holes where the leather catches the light (archive/m3/jacket_v1).
im = still("jacket")
H, W = im.shape[:2]
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
backdrop = np.median(gray[:, :40])
core = ndi.binary_fill_holes(ndi.binary_closing(largest(gray < backdrop * CFG["jacket"]["threshold"]), iterations=12))
gc = np.full((H, W), cv2.GC_BGD, np.uint8)
gc[ndi.binary_dilation(core, iterations=16)] = cv2.GC_PR_BGD
gc[core] = cv2.GC_PR_FGD
gc[ndi.binary_erosion(core, iterations=12)] = cv2.GC_FGD
cv2.setRNGSeed(json.load(open("config/seeds.json"))["main"])
cv2.grabCut(im, gc, None, np.zeros((1, 65)), np.zeros((1, 65)), 4, cv2.GC_INIT_WITH_MASK)
m = ((gc == cv2.GC_FGD) | (gc == cv2.GC_PR_FGD)) & (gray < backdrop * CFG["jacket"]["shadow_limit"])
m = ndi.binary_closing(m, iterations=5)
m = ndi.binary_fill_holes(largest(ndi.binary_opening(m, structure=np.ones((3, 3)), iterations=CFG["jacket"]["open_px"])))
# The hanger's wire crosses the open collar: paint it out from the lining around it.
x0, y0, x1, y1 = (round(v * s) for v, s in zip(CFG["jacket"]["wire_box"], (W, H, W, H)))
wire = np.zeros((H, W), np.uint8)
wire[y0:y1, x0:x1] = ((gray[y0:y1, x0:x1] > CFG["jacket"]["wire_level"]) & m[y0:y1, x0:x1]) * 255
im = cv2.inpaint(im, cv2.dilate(wire, np.ones((3, 3), np.uint8), iterations=2), 5, cv2.INPAINT_TELEA)
alpha = cv2.GaussianBlur((m * 255).astype(np.uint8), (0, 0), 1.1)
jacket = crop_rgba(im, alpha)
cv2.imwrite(str(OUT / "jacket.png"), jacket)
print("jacket", jacket.shape[1], "x", jacket.shape[0], "wire px", int((wire > 0).sum()))

# ---- the plaque: the saturated brass against the neutral grey
im = still("plaque")
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
m = ndi.binary_fill_holes(largest(ndi.binary_opening(hsv[..., 1] > 70, iterations=3)))
alpha = cv2.GaussianBlur((m * 255).astype(np.uint8), (0, 0), 0.9)
plaque = crop_rgba(im, alpha)
cv2.imwrite(str(OUT / "plaque.png"), plaque)
print("plaque", plaque.shape[1], "x", plaque.shape[0])

# ---- S01b: the wall, with the unfaded jacket shape
wall = still("S01").astype(np.float32)
H, W = wall.shape[:2]
p = CFG["jacket_on_wall"]
jh = round(p["height"] * H)
jw = round(jh * jacket.shape[1] / jacket.shape[0])
small = cv2.resize(jacket[..., 3], (jw, jh), interpolation=cv2.INTER_AREA)
x0, y0 = round(p["hook_x"] * W - jw / 2), round(p["hook_y"] * H + p["collar_drop"] * jh)
shape = np.zeros((H, W), np.float32)
shape[y0:y0 + jh, x0:x0 + jw] = small / 255
shape = cv2.GaussianBlur(shape, (0, 0), 2.0)[..., None]
# Paint as it was: the wall's own clean colour, keeping its large-scale shading.
ref = p["clean_patch"]
clean = np.median(wall[round(ref[1] * H):round(ref[3] * H), round(ref[0] * W):round(ref[2] * W)].reshape(-1, 3), axis=0)
luma = cv2.cvtColor(wall.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)
shade = cv2.GaussianBlur(luma, (0, 0), 90)
shade = (shade / max(1.0, float(np.median(shade[y0:y0 + jh, x0:x0 + jw]))))[..., None]
detail = (luma + 1) / (cv2.GaussianBlur(luma, (0, 0), 7) + 1)  # keep the wall's own fine texture in the patch
unfaded = np.clip(clean * p["clean_gain"] * shade * detail[..., None], 0, 255)
s01b = wall * (1 - shape) + unfaded * shape
cv2.imwrite(str(OUT / "S01b.png"), np.clip(s01b, 0, 255).astype(np.uint8))
json.dump({"plate": [W, H], "jacket": {"x": x0, "y": y0, "w": jw, "h": jh}}, open(OUT / "s01_layout.json", "w"), indent=1)
print("S01b", W, "x", H, "jacket at", x0, y0, jw, jh)

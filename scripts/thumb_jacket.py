"""Thumbnail A only: grade the jacket apart from the booth seat it lies on, in a copy of the S03 plate.

Human note (2026-11-24): "the jacket is blending in with the seat it's on. See about increasing the contrast between the
two for the thumbnail only". The plate itself is unchanged; the video never uses this copy.

1. Mask: Segment Anything (ViT-B, Meta, Apache 2.0), the checkpoint Share the Shares already has, read in place
   (`../share-the-shares/models/sam_vit_b_01ec64.pth`, the official download, sha256 ec2df627…; set SAM_CHECKPOINT to use
   another copy). It's run the way Share the Shares' `scripts/segment.py` runs it: a box around the jacket and points on
   the jacket and on the booth, wall, seat and table, three candidate masks. The kept one is picked by eye (CANDIDATE):
   the best-scored spills into the booth's dark side panel, and more negative points there made it worse. Its outline is
   smoothed (SAM's mask is upsampled from a coarse grid and comes out beaded), thin gaps such as the zipper's teeth are
   closed, specks and thin spurs are opened away, it is carried down to the frame's bottom edge where it reaches it (the
   zipper's end runs out of frame), and the edge is feathered.
2. Grade:
   - The booth is brightened, and its shadows are lifted to a warm brown with a screen layer. The lift starts below the
     wall, so "Nov 23" keeps its dark ground.
   - The jacket keeps its own pixels, but less saturated, with its shadows lifted (a power curve with gain), so it reads
     as a black leather jacket, its folds, collar and sleeve showing, not as a black shape against the orange.
   - A glow around the jacket (human note: "Use the mask to add a glow around the jacket"): the mask blurred at two
     widths, a tight halo and a wide soft light, kept outside the jacket and screened onto the booth in a warm white, as
     if lit from behind. The table stands in front of the jacket's lower right, so SAM cuts it too and the glow goes
     behind it.

Writes, beside the plate:
  remotion/public/gen/plates/S03_jacket_mask.png   the jacket's mask, 8-bit, plate size
  remotion/public/gen/plates/S03_table_mask.png    the table's (the glow goes behind it)
  remotion/public/gen/plates/S03_thumbA.png        the graded copy that thumbnail A uses

Usage: .venv/bin/python scripts/thumb_jacket.py [--preview out.png] [--regrade]
  --regrade: grade again from the saved masks, without running SAM.
"""
import argparse
import hashlib
import os
from pathlib import Path

import cv2
import numpy as np
import torch
from PIL import Image
from segment_anything import SamPredictor, sam_model_registry

ROOT = Path(__file__).resolve().parent.parent
PLATES = ROOT / 'remotion/public/gen/plates'
CHECKPOINT = Path(os.environ.get('SAM_CHECKPOINT', ROOT.parent / 'share-the-shares/models/sam_vit_b_01ec64.pth'))
CHECKPOINT_SHA256 = 'ec2df62732614e57411cdcf32a23ffdf28910380d03139ee0f4fcbe91eb8c912'

# Plate pixels (S03 is 1600x640; the jacket lies over the booth's seat back at the left edge).
BOX = [0, 150, 400, 640]
JACKET = [(150, 200), (100, 300), (110, 480), (250, 300), (300, 420), (200, 570), (230, 595)]
# Below the jacket's left side and hem the booth's seat is black in shadow, as black as the leather: the last four points
# keep it out (human note: "it's including part of the chair as the jacket at the bottom left").
NOT_JACKET = [(20, 330), (350, 290), (395, 600), (300, 120), (380, 520), (20, 220),
              (80, 500), (95, 580), (120, 625), (200, 632)]
# Of SAM's three: 0 (score 0.949) spills into the booth's side panel and seat; 1 (0.949) follows the jacket's edge.
CANDIDATE = 1
# The table stands in front of the jacket's lower right, so the glow goes behind it: SAM cuts the table the same way.
TABLE_BOX = [310, 335, 1275, 555]
TABLE = [(700, 450), (400, 515), (1150, 500), (900, 400)]
NOT_TABLE = [(380, 300), (250, 400), (700, 600), (1400, 400)]
SMOOTH = 3.0  # px, blur before re-thresholding the mask (smooths SAM's beaded outline)
CLOSE = 9  # px, morphological closing (the zipper's teeth)
OPEN = 7  # px, morphological opening (specks and spurs, which the carry below would drag down to the frame's edge)
BOTTOM = 14  # rows: the mask is carried down from this far above the frame's bottom edge (where the zipper's end is)
FEATHER = 1.5  # px, the final edge

# Grade. The lift ramps in between these fractions of the plate's height (the wall above stays as it is).
BOOTH_GAIN, BOOTH_SAT = 1.2, 1.15
LIFT_RGB, LIFT_FROM, LIFT_FULL = (92, 42, 18), 0.26, 0.36
# The jacket's shadows lifted so its folds, collar and sleeve show (human note: "increase the brightness on the jacket
# so it reads like a jacket rather than a black blob"): median luma 50 of 255, from 10 with the earlier gamma 1.25,
# which deepened them. 0.6 and below turn the leather grey; local contrast (CLAHE) made it look grungy.
JACKET_SAT, JACKET_GAMMA, JACKET_GAIN = 0.55, 0.65, 1.15
# The glow: (blur sigma in plate px, gain, opacity) for the halo and the soft light, and its colour.
GLOW = [(4.0, 2.2, 0.7), (20.0, 1.7, 0.7)]  # a softer (3, 2.0, 0.55), (16, 1.6, 0.6) was too faint at phone size
GLOW_RGB = (255, 214, 160)


def segment(plate: Image.Image) -> tuple[np.ndarray, np.ndarray]:
    """The jacket's mask (candidate CANDIDATE) and the table's (best-scored), as 0/1 floats."""
    digest = hashlib.sha256(CHECKPOINT.read_bytes()).hexdigest()
    if digest != CHECKPOINT_SHA256:
        raise SystemExit(f'{CHECKPOINT}: sha256 {digest[:16]}…, expected {CHECKPOINT_SHA256[:16]}…')
    torch.manual_seed(0)
    pred = SamPredictor(sam_model_registry['vit_b'](checkpoint=str(CHECKPOINT)))
    pred.set_image(np.asarray(plate))

    def cut(box, pos, neg):
        return pred.predict(point_coords=np.array(pos + neg, np.float32), point_labels=np.array([1] * len(pos) + [0] * len(neg)),
                            box=np.array(box, np.float32), multimask_output=True)

    masks, scores, _ = cut(BOX, JACKET, NOT_JACKET)
    print('SAM ViT-B, jacket: scores %s, kept %d' % (' '.join('%.3f' % s for s in scores), CANDIDATE))
    tmasks, tscores, _ = cut(TABLE_BOX, TABLE, NOT_TABLE)
    best = int(np.argmax(tscores))
    print('SAM ViT-B, table: scores %s, kept %d' % (' '.join('%.3f' % s for s in tscores), best))
    return masks[CANDIDATE].astype(np.float32), tmasks[best].astype(np.float32)


def refine(m: np.ndarray, to_bottom: bool = True) -> np.ndarray:
    m = (cv2.GaussianBlur(m, (0, 0), SMOOTH) > 0.5).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (CLOSE, CLOSE)))
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (OPEN, OPEN)))
    if to_bottom:
        m[-BOTTOM:] = m[-BOTTOM - 1]
    return np.clip(cv2.GaussianBlur(m.astype(np.float32), (0, 0), FEATHER), 0, 1)


def saturate(rgb: np.ndarray, k: float) -> np.ndarray:
    grey = (rgb @ np.array([0.2126, 0.7152, 0.0722], np.float32))[..., None]
    return grey + (rgb - grey) * k


def grade(plate: Image.Image, a: np.ndarray, table: np.ndarray) -> np.ndarray:
    p = np.asarray(plate, np.float32) / 255
    h = p.shape[0]
    ramp = np.clip((np.arange(h) / h - LIFT_FROM) / (LIFT_FULL - LIFT_FROM), 0, 1)[:, None, None]
    lift = np.array(LIFT_RGB, np.float32) / 255 * ramp
    booth = np.clip(saturate(p * BOOTH_GAIN, BOOTH_SAT), 0, 1)
    booth = 1 - (1 - booth) * (1 - lift)  # screen
    light = glow(a) * (1 - table)  # behind the table, not over it
    booth = 1 - (1 - booth) * (1 - light[..., None] * np.array(GLOW_RGB, np.float32) / 255)  # screen
    jacket = np.clip(saturate(p, JACKET_SAT), 0, 1) ** JACKET_GAMMA * JACKET_GAIN
    a = a[..., None]
    return np.clip(booth * (1 - a) + jacket * a, 0, 1)


def glow(a: np.ndarray) -> np.ndarray:
    """The glow's strength, 0-1, outside the jacket only: each layer is the mask blurred, raised by its gain (so it is
    full strength at the edge and falls off outward), times its opacity; the layers combine like light (screen)."""
    out = np.zeros_like(a)
    for sigma, gain, opacity in GLOW:
        layer = np.clip(cv2.GaussianBlur(a, (0, 0), sigma) * gain, 0, 1) * opacity
        out = 1 - (1 - out) * (1 - layer)
    return out * (1 - a)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--preview', help='also write the mask over the plate, for checking')
    ap.add_argument('--regrade', action='store_true', help='grade again from the saved masks, without running SAM')
    args = ap.parse_args()

    plate = Image.open(PLATES / 'S03.png').convert('RGB')
    if args.regrade:
        a, table = (np.asarray(Image.open(PLATES / f'S03_{k}_mask.png'), np.float32) / 255 for k in ('jacket', 'table'))
    else:
        jm, tm = segment(plate)
        a, table = refine(jm), refine(tm, to_bottom=False)
        for k, m in (('jacket', a), ('table', table)):
            Image.fromarray((m * 255).round().astype(np.uint8)).save(PLATES / f'S03_{k}_mask.png')
    print('masks: jacket %.1f%%, table %.1f%% of the plate' % (100 * a.mean(), 100 * table.mean()))
    Image.fromarray((grade(plate, a, table) * 255).round().astype(np.uint8)).save(PLATES / 'S03_thumbA.png')

    if args.preview:
        p = np.asarray(plate, np.float32)
        tint = p * (1 - 0.55 * a[..., None]) + np.array([40, 160, 255], np.float32) * 0.55 * a[..., None]
        Image.fromarray(tint.clip(0, 255).astype(np.uint8)).crop((0, 0, 460, 640)).save(args.preview)


if __name__ == '__main__':
    main()

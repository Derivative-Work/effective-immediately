"""Thumbnail A only: grade the jacket apart from the booth seat it lies on, in a copy of the S03 plate.

Human note (2026-11-24): "the jacket is blending in with the seat it's on. See about increasing the contrast between the
two for the thumbnail only". The plate itself is unchanged; the video never uses this copy.

1. Mask: Segment Anything (ViT-B, Meta, Apache 2.0), the checkpoint Share the Shares already has, read in place
   (`../share-the-shares/models/sam_vit_b_01ec64.pth`, the official download, sha256 ec2df627…; set SAM_CHECKPOINT to use
   another copy). It's run the way Share the Shares' `scripts/segment.py` runs it: a box around the jacket and points on
   the jacket and on the booth, wall and table, three candidate masks. The kept one is picked by eye (CANDIDATE): the
   best-scored spills into the booth's dark side panel, and more negative points there made it worse. Its outline is smoothed
   (SAM's mask is upsampled from a coarse grid and comes out beaded), thin gaps such as the zipper's teeth are closed, it
   is carried down to the frame's bottom edge (the jacket runs out of frame), and the edge is feathered.
2. Grade:
   - The booth is brightened, and its shadows are lifted to a warm brown with a screen layer. The lift starts below the
     wall, so "Nov 23" keeps its dark ground.
   - The jacket keeps its own pixels, but less saturated, with deeper shadows and brighter highlights (a power curve
     with gain): a neutral black with its leather sheen, against the orange.

Writes, beside the plate:
  remotion/public/gen/plates/S03_jacket_mask.png   the mask, 8-bit, plate size
  remotion/public/gen/plates/S03_thumbA.png        the graded copy that thumbnail A uses

Usage: .venv/bin/python scripts/thumb_jacket.py [--preview out.png]
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
JACKET = [(150, 200), (100, 300), (110, 480), (250, 300), (300, 420), (200, 570), (60, 600)]
NOT_JACKET = [(20, 330), (350, 290), (395, 600), (300, 120), (380, 520), (20, 220)]
CANDIDATE = 1  # of SAM's three: 0 (score 0.962) spills into the booth's side panel; 1 (0.959) follows the jacket's edge
SMOOTH = 3.0  # px, blur before re-thresholding the mask (smooths SAM's beaded outline)
CLOSE = 9  # px, morphological closing (the zipper's teeth)
BOTTOM = 14  # rows: the mask is carried down from this far above the frame's bottom edge
FEATHER = 1.5  # px, the final edge

# Grade. The lift ramps in between these fractions of the plate's height (the wall above stays as it is).
BOOTH_GAIN, BOOTH_SAT = 1.2, 1.15
LIFT_RGB, LIFT_FROM, LIFT_FULL = (92, 42, 18), 0.26, 0.36
JACKET_SAT, JACKET_GAMMA, JACKET_GAIN = 0.55, 1.25, 1.15  # deeper shadows, brighter highlights (the sheen)


def segment(plate: Image.Image) -> np.ndarray:
    digest = hashlib.sha256(CHECKPOINT.read_bytes()).hexdigest()
    if digest != CHECKPOINT_SHA256:
        raise SystemExit(f'{CHECKPOINT}: sha256 {digest[:16]}…, expected {CHECKPOINT_SHA256[:16]}…')
    torch.manual_seed(0)
    pred = SamPredictor(sam_model_registry['vit_b'](checkpoint=str(CHECKPOINT)))
    pred.set_image(np.asarray(plate))
    masks, scores, _ = pred.predict(point_coords=np.array(JACKET + NOT_JACKET, np.float32),
                                    point_labels=np.array([1] * len(JACKET) + [0] * len(NOT_JACKET)),
                                    box=np.array(BOX, np.float32), multimask_output=True)
    print('SAM ViT-B scores %s, kept %d' % (' '.join('%.3f' % s for s in scores), CANDIDATE))
    return masks[CANDIDATE].astype(np.float32)


def refine(m: np.ndarray) -> np.ndarray:
    m = (cv2.GaussianBlur(m, (0, 0), SMOOTH) > 0.5).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (CLOSE, CLOSE)))
    m[-BOTTOM:] = m[-BOTTOM - 1]
    return np.clip(cv2.GaussianBlur(m.astype(np.float32), (0, 0), FEATHER), 0, 1)


def saturate(rgb: np.ndarray, k: float) -> np.ndarray:
    grey = (rgb @ np.array([0.2126, 0.7152, 0.0722], np.float32))[..., None]
    return grey + (rgb - grey) * k


def grade(plate: Image.Image, a: np.ndarray) -> np.ndarray:
    p = np.asarray(plate, np.float32) / 255
    h = p.shape[0]
    ramp = np.clip((np.arange(h) / h - LIFT_FROM) / (LIFT_FULL - LIFT_FROM), 0, 1)[:, None, None]
    lift = np.array(LIFT_RGB, np.float32) / 255 * ramp
    booth = np.clip(saturate(p * BOOTH_GAIN, BOOTH_SAT), 0, 1)
    booth = 1 - (1 - booth) * (1 - lift)  # screen
    jacket = np.clip(saturate(p, JACKET_SAT), 0, 1) ** JACKET_GAMMA * JACKET_GAIN
    a = a[..., None]
    return np.clip(booth * (1 - a) + jacket * a, 0, 1)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--preview', help='also write the mask over the plate, for checking')
    args = ap.parse_args()

    plate = Image.open(PLATES / 'S03.png').convert('RGB')
    a = refine(segment(plate))
    print('mask: %.1f%% of the plate' % (100 * a.mean()))
    Image.fromarray((a * 255).round().astype(np.uint8)).save(PLATES / 'S03_jacket_mask.png')
    Image.fromarray((grade(plate, a) * 255).round().astype(np.uint8)).save(PLATES / 'S03_thumbA.png')

    if args.preview:
        p = np.asarray(plate, np.float32)
        tint = p * (1 - 0.55 * a[..., None]) + np.array([40, 160, 255], np.float32) * 0.55 * a[..., None]
        Image.fromarray(tint.clip(0, 255).astype(np.uint8)).crop((0, 0, 460, 640)).save(args.preview)


if __name__ == '__main__':
    main()

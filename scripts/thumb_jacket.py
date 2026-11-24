"""Thumbnail A only: grade the jacket apart from the booth seat it lies on, in a copy of the S03 plate.

Human note (2026-11-24): "the jacket is blending in with the seat it's on. See about increasing the contrast between the
two for the thumbnail only". The plate itself is unchanged; the video never uses this copy.

1. Mask: SAM 2.1 (facebook/sam2.1-hiera-large, Apache 2.0, from Hugging Face), prompted with a box around the jacket and
   points on the jacket and on the booth, wall and table. Its outline is smoothed (SAM's mask is upsampled from a coarse
   grid and comes out beaded), thin gaps such as the zipper's teeth are closed, it is carried down to the frame's bottom
   edge (the jacket runs out of frame), and the edge is feathered.
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
from pathlib import Path

import cv2
import numpy as np
import torch
from PIL import Image
from transformers import Sam2Model, Sam2Processor

ROOT = Path(__file__).resolve().parent.parent
PLATES = ROOT / 'remotion/public/gen/plates'
MODEL = 'facebook/sam2.1-hiera-large'

# Plate pixels (S03 is 1600x640; the jacket lies over the booth's seat back at the left edge).
BOX = [0, 150, 400, 640]
JACKET = [(150, 200), (100, 300), (110, 480), (250, 300), (300, 420), (200, 570), (60, 600)]
NOT_JACKET = [(20, 330), (350, 290), (395, 600), (300, 120), (380, 520), (20, 220)]
SMOOTH = 3.0  # px, blur before re-thresholding the mask (smooths SAM's beaded outline)
CLOSE = 9  # px, morphological closing (the zipper's teeth)
BOTTOM = 14  # rows: the mask is carried down from this far above the frame's bottom edge
FEATHER = 1.5  # px, the final edge

# Grade. The lift ramps in between these fractions of the plate's height (the wall above stays as it is).
BOOTH_GAIN, BOOTH_SAT = 1.2, 1.15
LIFT_RGB, LIFT_FROM, LIFT_FULL = (92, 42, 18), 0.26, 0.36
JACKET_SAT, JACKET_GAMMA, JACKET_GAIN = 0.55, 1.25, 1.15  # deeper shadows, brighter highlights (the sheen)


def segment(plate: Image.Image) -> np.ndarray:
    dev = 'cuda' if torch.cuda.is_available() else 'cpu'
    proc = Sam2Processor.from_pretrained(MODEL)
    model = Sam2Model.from_pretrained(MODEL).to(dev).eval()
    pts = [[list(map(list, JACKET + NOT_JACKET))]]
    labels = [[[1] * len(JACKET) + [0] * len(NOT_JACKET)]]
    inputs = proc(images=plate, input_points=pts, input_labels=labels, input_boxes=[[BOX]], return_tensors='pt').to(dev)
    with torch.no_grad():
        out = model(**inputs, multimask_output=False)
    m = proc.post_process_masks(out.pred_masks.cpu(), inputs['original_sizes'])[0][0, 0].numpy().astype(np.float32)
    print('SAM score %.3f' % float(out.iou_scores[0, 0, 0]))
    del model
    torch.cuda.empty_cache()
    return m


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

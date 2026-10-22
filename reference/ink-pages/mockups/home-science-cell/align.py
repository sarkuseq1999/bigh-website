"""Mockup only (October 22, 2026): line the older paintings up on the young one.

Codex paints each age from the young painting, but it moves and resizes the cell a little, so the
slider's cross-fade would jump. This finds the scale and shift that best lay each older painting's
heavy ink (the cell body and main branches) over the young one's, and writes the moved copy
(paper filled in) into the git-ignored plates folder as <name>-aligned.png.

usage: python -X utf8 reference/ink-pages/mockups/home-science-cell/align.py <young> <older> [...]
"""

import sys
from pathlib import Path

import cv2
import numpy as np

ORIG = Path(__file__).resolve().parents[2] / "home-science" / "originals"
PLATES = ORIG.parent / "plates"
SMALL = 400


def ink(path):
    """Ink density 0..1 (paper divided out) and the paper colour."""
    im = cv2.imread(str(path), cv2.IMREAD_COLOR).astype(np.float32)
    b = 24
    border = np.concatenate([im[:b].reshape(-1, 3), im[-b:].reshape(-1, 3)])
    paper = np.median(border, axis=0)
    g = (im / paper).mean(axis=2)
    return im, paper, np.clip(1.0 - g, 0, 1)


def small(dens):
    h, w = dens.shape
    s = cv2.resize(dens, (SMALL, round(h * SMALL / w)), interpolation=cv2.INTER_AREA)
    s = cv2.GaussianBlur(s, (0, 0), 3)
    return s**2  # weight the heavy strokes: the cell body and main branches


def warp(a, scale, dx, dy, w, h, border=0):
    m = np.float32([[scale, 0, (1 - scale) * w / 2 + dx], [0, scale, (1 - scale) * h / 2 + dy]])
    return cv2.warpAffine(a, m, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=border)


def best_fit(ref, mov):
    h, w = ref.shape
    win = cv2.createHanningWindow((w, h), cv2.CV_32F)
    best = None
    for scale in np.arange(0.84, 1.17, 0.01):
        m = warp(mov, scale, 0, 0, w, h)
        (dx, dy), _ = cv2.phaseCorrelate(ref.astype(np.float32), m.astype(np.float32), win)
        # score the overlap after the shift (either sign), not the phase response alone
        for sx, sy in ((-dx, -dy), (dx, dy)):
            moved = warp(mov, scale, sx, sy, w, h)
            score = float((ref * moved).sum() / np.sqrt((ref**2).sum() * (moved**2).sum() + 1e-9))
            if best is None or score > best[0]:
                best = (score, scale, sx, sy)
    return best


if __name__ == "__main__":
    young = sys.argv[1]
    _, _, yd = ink(ORIG / f"{young}.png")
    ref = small(yd)
    for name in sys.argv[2:]:
        im, paper, dens = ink(ORIG / f"{name}.png")
        score, scale, dx, dy = best_fit(ref, small(dens))
        k = im.shape[1] / SMALL
        h, w = im.shape[:2]
        out = warp(im, scale, dx * k, dy * k, w, h, border=tuple(float(c) for c in paper))
        PLATES.mkdir(exist_ok=True)
        cv2.imwrite(str(PLATES / f"{name}-aligned.png"), np.clip(out, 0, 255).astype(np.uint8))
        print(f"{name}: scale {scale:.2f}, shift {dx * k:+.0f},{dy * k:+.0f}px, overlap {score:.3f}")

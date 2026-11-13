"""Cut each "Curious about the science?" take for the mockups (November 13, 2026).

Each Codex painting is one vignette on bare paper. The paper is divided out (so the painting
multiplies onto the page, as the grey glasses do), the painting is cropped to its paint with a
little room round it, and the crop's own edge is faded to white so no line can show.

    python -X utf8 reference/ink-pages/about-closing/cut_closing.py take [take ...]

Out: plates/img/<take>.png (git-ignored), at most 1400px wide; prints each one's size and shape.
"""

import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
IMG = HERE / "plates" / "img"
WIDE = 1400
# Room round the paint, as a share of its box's larger side.
ROOM = 0.04


def load(name):
    img = Image.open(HERE / "originals" / f"{name}.png")
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        paper = Image.new("RGBA", img.size, (255, 255, 255, 255))
        img = Image.alpha_composite(paper, img)
    return np.asarray(img.convert("RGB")).astype(float)


def divide_paper(a):
    """Paper to white: each channel divided by the paper's own colour (a bright percentile)."""
    paper = np.percentile(a.reshape(-1, 3), 90, axis=0)
    return np.clip(a / paper * 255.0, 0, 255)


def paint_box(a):
    """The box round the paint: rows and columns that hold more than a few painted pixels."""
    lo = a.min(axis=2)
    hi = a.max(axis=2)
    mask = (((255 - lo) > 20) | ((hi - lo) > 18)).astype(np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    cols = np.nonzero(mask.sum(axis=0) > 6)[0]
    rows = np.nonzero(mask.sum(axis=1) > 6)[0]
    return cols.min(), rows.min(), cols.max() + 1, rows.max() + 1


def cut(take):
    a = divide_paper(load(take))
    x0, y0, x1, y1 = paint_box(a)
    room = int(max(x1 - x0, y1 - y0) * ROOM)
    H, W = a.shape[:2]
    x0, y0, x1, y1 = max(0, x0 - room), max(0, y0 - room), min(W, x1 + room), min(H, y1 + room)
    out = a[y0:y1, x0:x1]
    h, w = out.shape[:2]
    edge = max(8, int(min(w, h) * 0.03))
    ramp_x = np.clip(np.minimum(np.arange(w), np.arange(w)[::-1]) / edge, 0, 1)
    ramp_y = np.clip(np.minimum(np.arange(h), np.arange(h)[::-1]) / edge, 0, 1)
    ramp = np.minimum.outer(ramp_y, ramp_x)
    out = 255 - (255 - out) * ramp[..., None]
    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
    if img.width > WIDE:
        img = img.resize((WIDE, round(img.height * WIDE / img.width)), Image.LANCZOS)
    return img


def main():
    IMG.mkdir(parents=True, exist_ok=True)
    for take in sys.argv[1:]:
        img = cut(take)
        img.save(IMG / f"{take}.png")
        print(take, img.size, f"shape {img.width / img.height:.3f}")


if __name__ == "__main__":
    main()

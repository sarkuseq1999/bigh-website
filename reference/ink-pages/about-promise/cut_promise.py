"""Cut the four small paintings out of each "Our promise" take for the mockups (November 12, 2026).

Each Codex sheet holds four paintings in a row on bare paper. The paper is divided out (so the
paintings multiply onto the page, as the four grey dots do), the four are found as the four largest
patches of paint, sorted left to right, and each is cut into a square with room round it, its
edges faded to white so no crop line shows.

    python -X utf8 reference/ink-pages/about-promise/cut_promise.py take [take ...]

Out: plates/img/<take>-<1..4>.png (git-ignored), 360px squares like the dots they stand in for.
"""

import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
IMG = HERE / "plates" / "img"
SIDE = 360
# How far round each painting's own box the square reaches (a share of its larger side).
ROOM = 0.10


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


def paint_mask(a):
    """Where there is paint: darker than the paper, or coloured."""
    lo = a.min(axis=2)
    hi = a.max(axis=2)
    dark = 255 - lo
    sat = (hi - lo)
    mask = ((dark > 24) | (sat > 22)).astype(np.uint8)
    # Paper grain and stray specks out.
    return cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))


def four(mask):
    """The four paintings, left to right: the four bands of columns that hold the most paint (the
    four stand in one row, so a column with paint belongs to one of them; gaps of a few columns
    inside one painting are bridged)."""
    cols = mask.astype(np.int64).sum(axis=0) > 3
    runs, start = [], None
    for x, on in enumerate(list(cols) + [False]):
        if on and start is None:
            start = x
        elif not on and start is not None:
            runs.append([start, x])
            start = None
    merged = []
    for r in runs:
        if merged and r[0] - merged[-1][1] < 5:
            merged[-1][1] = r[1]
        else:
            merged.append(r)
    merged.sort(key=lambda r: -int(mask[:, r[0] : r[1]].astype(np.int64).sum()))
    if len(merged) < 4:
        raise SystemExit(f"found only {len(merged)} paintings")
    boxes = []
    for x0, x1 in merged[:4]:
        own = np.zeros_like(mask, bool)
        own[:, x0:x1] = mask[:, x0:x1] > 0
        ys = np.nonzero(own.sum(axis=1) > 3)[0]
        boxes.append((x0, ys.min(), x1, ys.max() + 1, own))
    return sorted(boxes, key=lambda b: b[0])


def cut(a, box, side, cy):
    """One painting in a square of the given side: all four share one scale and one middle line,
    so a bud stays smaller than the open flower and the four stand on one line."""
    x0, y0, x1, y1, own = box
    cx = (x0 + x1) / 2
    sx, sy = int(round(cx - side / 2)), int(round(cy - side / 2))
    out = np.full((side, side, 3), 255.0)
    keep = np.zeros((side, side), bool)
    H, W = a.shape[:2]
    ax0, ay0 = max(0, sx), max(0, sy)
    ax1, ay1 = min(W, sx + side), min(H, sy + side)
    out[ay0 - sy : ay1 - sy, ax0 - sx : ax1 - sx] = a[ay0:ay1, ax0:ax1]
    keep[ay0 - sy : ay1 - sy, ax0 - sx : ax1 - sx] = own[ay0:ay1, ax0:ax1]
    # Only this painting: a neighbour's paint that reaches into the square goes back to paper.
    soft = cv2.GaussianBlur(cv2.dilate(keep.astype(np.uint8) * 255, np.ones((15, 15), np.uint8)).astype(float), (0, 0), 6) / 255.0
    out = 255 - (255 - out) * soft[..., None]
    # The square's own edge fades to paper, so no crop line can show.
    ramp = np.minimum.outer(*(np.minimum(np.arange(side), np.arange(side)[::-1]),) * 2) / (side * 0.06)
    ramp = np.clip(ramp, 0, 1)
    out = 255 - (255 - out) * ramp[..., None]
    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
    return img.resize((SIDE, SIDE), Image.LANCZOS)


def main():
    IMG.mkdir(parents=True, exist_ok=True)
    for take in sys.argv[1:]:
        a = divide_paper(load(take))
        boxes = four(paint_mask(a))
        side = int(max(max(b[2] - b[0], b[3] - b[1]) for b in boxes) * (1 + 2 * ROOM))
        cy = (min(b[1] for b in boxes) + max(b[3] for b in boxes)) / 2
        for k, box in enumerate(boxes, 1):
            cut(a, box, side, cy).save(IMG / f"{take}-{k}.png")
        print(take, [(b[0], b[1], b[2] - b[0], b[3] - b[1]) for b in boxes])


if __name__ == "__main__":
    main()

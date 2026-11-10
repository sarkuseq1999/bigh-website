"""Lift a painting's gold slivers off it, so a mock can let them drift.

  python -X utf8 reference/ink-pages/mockups/science-hero/split_gold.py <plate.webp|png> <name> [sat0]

sat0 (default 0.30) is where a warm yellow starts to count as gold; a paler gold needs a lower one.

Writes into reference/ink-pages/science/plates/hero/ (git-ignored):
  <name>-base.webp      the painting with its gold painted out (inpainted from its surroundings)
  <name>-gold/<i>.png   each sliver on its own, with soft edges
  <name>-gold.json      [{file, x, y, w, h}] as shares of the painting, plus the painting's size
  <name>-check.png      the base with every sliver put back: it should match the painting
Only for paintings whose only warm, strong colour is the gold (the cell and the inside view): the
hills' dry grass would be lifted too.

Two passes. First a colour key finds the gold roughly and the painting is filled in behind it.
Then each sliver's real shape is read from how far the painting differs from that filled-in
version, so a sliver keeps its pale highlights and stays in one piece (the colour key alone broke
the slivers into dashes).
"""

import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

SRC = Path(sys.argv[1])
NAME = sys.argv[2]
SAT0 = float(sys.argv[3]) if len(sys.argv) > 3 else 0.30
OUT = Path(__file__).resolve().parent.parent.parent / "science" / "plates" / "hero"
GOLD = OUT / f"{NAME}-gold"
GOLD.mkdir(parents=True, exist_ok=True)
for old in GOLD.glob("*.png"):
    old.unlink()

rgb = np.asarray(Image.open(SRC).convert("RGB"))
H, W = rgb.shape[:2]
hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
hue, sat, val = hsv[..., 0] * 2.0, hsv[..., 1] / 255.0, hsv[..., 2] / 255.0

# Pass 1: a warm yellow, strong and light.
warm = np.clip(1.0 - np.abs(hue - 44.0) / 16.0, 0, 1)
strong = np.clip((sat - SAT0) / 0.2, 0, 1)
light = np.clip((val - 0.55) / 0.15, 0, 1)
key = cv2.GaussianBlur(warm * strong * light, (0, 0), 0.8)
seed = (key > 0.35).astype(np.uint8)
seed = cv2.morphologyEx(seed, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))

# The painting without its gold, in two rounds. The hole is cut wide: it must swallow each sliver's
# pale middle and leave no gold-tinted edge to bleed back in. The second round widens it by what
# the first round showed to be sliver (and by any pale warm light beside it), then fills again.
ELLIPSE = lambda n: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (n, n))  # noqa: E731
pale = ((np.abs(hue - 47.0) < 12.0) & (sat > 0.10) & (val > 0.86)).astype(np.uint8)
hole = cv2.dilate(seed, ELLIPSE(23))
for _ in range(2):
    base = cv2.inpaint(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), hole * 255, 9, cv2.INPAINT_TELEA)
    base = cv2.cvtColor(base, cv2.COLOR_BGR2RGB)
    # A sliver is wherever the painting differs from that filled-in version.
    far = np.linalg.norm(rgb.astype(np.float32) - base.astype(np.float32), axis=2)
    alpha = np.clip((far - 10.0) / 30.0, 0, 1) * hole
    alpha = cv2.GaussianBlur(alpha, (0, 0), 0.7)
    # Its pieces are joined (its pale middle differs little from the wash behind it).
    body = cv2.morphologyEx((alpha > 0.3).astype(np.uint8), cv2.MORPH_CLOSE, ELLIPSE(11))
    beside = cv2.morphologyEx(pale * cv2.dilate(hole, ELLIPSE(41)), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    hole = np.maximum(hole, cv2.dilate(np.maximum(body, beside), ELLIPSE(19)))
Image.fromarray(base).save(OUT / f"{NAME}-base.webp", "WEBP", quality=88, method=6)
# The whole of a sliver is made solid, so it travels as one piece.
alpha = np.maximum(alpha, cv2.GaussianBlur(body.astype(np.float32), (0, 0), 1.0) * 0.95)

count, labels, stats, _ = cv2.connectedComponentsWithStats(body, connectivity=8)
items = []
for i in range(1, count):
    x, y, w, h, area = stats[i]
    if area < 70:
        continue
    pad = 8
    x0, y0, x1, y1 = max(0, x - pad), max(0, y - pad), min(W, x + w + pad), min(H, y + h + pad)
    own = cv2.dilate((labels[y0:y1, x0:x1] == i).astype(np.uint8), np.ones((7, 7), np.uint8))
    a = (alpha[y0:y1, x0:x1] * own * 255).clip(0, 255).astype(np.uint8)
    sprite = np.dstack([rgb[y0:y1, x0:x1], a])
    file = f"{len(items):02d}.png"
    Image.fromarray(sprite, "RGBA").save(GOLD / file)
    items.append({"file": file, "x": x0 / W, "y": y0 / H, "w": (x1 - x0) / W, "h": (y1 - y0) / H, "area": int(area)})

(OUT / f"{NAME}-gold.json").write_text(json.dumps({"width": W, "height": H, "slivers": items}), encoding="utf-8")

# The check picture: the base with every sliver put back where it was.
a3 = (alpha * cv2.dilate(body, np.ones((7, 7), np.uint8)))[..., None]
back = base.astype(np.float32) * (1 - a3) + rgb.astype(np.float32) * a3
Image.fromarray(back.clip(0, 255).astype(np.uint8)).save(OUT / f"{NAME}-check.png")
print(NAME, "slivers:", len(items))

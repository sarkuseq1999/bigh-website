"""Idea B's walker is painted in small dabs; this lays real gold leaf on about one dab in eight.

  python -X utf8 reference/ink-pages/mockups/science-hero/gild_dabs.py

Reads plates/hero/dabs-1.webp (build_plates.py), finds the walker's dabs (the small separate marks
inside the figure's box), turns a chosen few into the site's gold leaf, and writes
plates/hero/dabs-gold.webp (the painting) and dabs-mask.png (the gilded dabs alone, for the light
that passes over them). Codex's own gold dabs were too close to the tan ones to read as gold.
"""

from pathlib import Path

import cv2
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent.parent
OUT = HERE.parent.parent / "science" / "plates" / "hero"
LEAF = REPO / "public" / "images" / "home-v2" / "ink" / "gold-leaf-word.webp"
# The walker's box in the 1536 x 1024 painting (hat to boots), by eye.
BOX = (868, 428, 1108, 905)

rgb = np.asarray(Image.open(OUT / "dabs-1.webp").convert("RGB")).copy()
H, W = rgb.shape[:2]
x0, y0, x1, y1 = BOX
part = rgb[y0:y1, x0:x1].astype(np.float32)
lum = part.mean(axis=2) / 255.0
marks = (lum < 0.90).astype(np.uint8)
marks = cv2.erode(marks, np.ones((2, 2), np.uint8))
count, labels, stats, cents = cv2.connectedComponentsWithStats(marks, connectivity=4)

rng = np.random.default_rng(5)
chosen = np.zeros(marks.shape, np.uint8)
picked = 0
for i in range(1, count):
    x, y, w, h, area = stats[i]
    if not (30 <= area <= 700) or max(w, h) > 40 or area / (w * h) < 0.4:
        continue
    cy = cents[i][1] / (y1 - y0)
    cx = cents[i][0] / (x1 - x0)
    # More gold at the head, the back near the heart, and the legs; none on the boots or the hand.
    if cy > 0.93 or cx < 0.12:
        continue
    weight = 0.34 if cy < 0.16 else 0.3 if 0.26 < cy < 0.44 else 0.26 if cy > 0.55 else 0.1
    if rng.random() < weight:
        chosen[labels == i] = 1
        picked += 1

chosen = cv2.dilate(chosen, np.ones((3, 3), np.uint8))
soft = cv2.GaussianBlur(chosen.astype(np.float32), (0, 0), 0.9)

# The leaf is a small square: tiled over the walker's box.
leaf = np.asarray(Image.open(LEAF).convert("RGB")).astype(np.float32)
reps = (-(-(y1 - y0) // leaf.shape[0]), -(-(x1 - x0) // leaf.shape[1]), 1)
gold = np.tile(leaf, reps)[: y1 - y0, : x1 - x0]
# The site's gold word is tinted a fifth toward a deep brown; the dabs take the same leaf.
gold = gold * 0.86 + np.array([110, 78, 20], np.float32) * 0.14
part = part * (1 - soft[..., None]) + gold * soft[..., None]
rgb[y0:y1, x0:x1] = part.clip(0, 255).astype(np.uint8)
Image.fromarray(rgb).save(OUT / "dabs-gold.webp", "WEBP", quality=90, method=6)

mask = np.zeros((H, W), np.uint8)
mask[y0:y1, x0:x1] = (soft * 255).clip(0, 255).astype(np.uint8)
Image.fromarray(np.dstack([np.full((H, W, 3), 255, np.uint8), mask]), "RGBA").save(OUT / "dabs-mask.png")
print("dabs found:", count - 1, "gilded:", picked)

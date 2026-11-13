"""Lay the site's gold leaf on a painting's flat ochre strokes (Codex paints what is to be gilded in
pale ochre; the site's gold is real leaf, never paint), inside one box of the painting.

  python -X utf8 reference/ink-pages/mockups/science-last/gild_ochre.py <take> <x0,y0,x1,y1> [thin]

<take> is reference/ink-pages/science/originals/<take>.png; the box is in its pixels. With "thin",
only thin strokes are gilded (ripple rings and wake lines), not broad ochre washes such as dry
grass in the same box. Writes science/plates/last/<take>-gold.png, paper divided out as the site
ships its paintings, and <take>-goldmask.png (the gilded strokes alone).
"""

import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

from gild_kite import ORIG, OUT, divided, gold_leaf, paper_of

take = sys.argv[1]
x0, y0, x1, y1 = (int(v) for v in sys.argv[2].split(","))
thin = "thin" in sys.argv[3:]

a = np.asarray(Image.open(ORIG / f"{take}.png").convert("RGB")).astype(np.float32)
h, w = a.shape[:2]
paper = paper_of(a)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
lum = a.mean(axis=2)
# Ochre: clearly warmer than the paper (red well above blue), light, yellow (not green, not coral).
ochre = ((r - b) > 40) & (lum > 120) & (g > b + 15) & (r >= g) & (g > r * 0.72)
box = np.zeros((h, w), bool)
box[y0:y1, x0:x1] = True
ochre &= box
if thin:
    # A stroke is thin where a small opening wipes it out; broad washes survive the opening.
    broad = cv2.morphologyEx(ochre.astype(np.uint8), cv2.MORPH_OPEN, np.ones((9, 9), np.uint8)).astype(bool)
    ochre &= ~cv2.dilate(broad.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
count, labels, stats, _ = cv2.connectedComponentsWithStats(ochre.astype(np.uint8), connectivity=8)
keep = np.zeros_like(ochre)
for i in range(1, count):
    if stats[i, cv2.CC_STAT_AREA] >= 12:
        keep |= labels == i
ochre = keep

ref = np.median(lum[ochre]) if ochre.any() else 200.0
shade = np.clip(0.65 + 0.35 * lum / ref, 0.9, 1.1)
gold = gold_leaf((h, w), shade)
soft = cv2.GaussianBlur(cv2.dilate(ochre.astype(np.uint8), np.ones((2, 2), np.uint8)).astype(np.float32), (0, 0), 0.7)
out = a * (1 - soft[..., None]) + gold * soft[..., None]
Image.fromarray(divided(out, paper).clip(0, 255).astype(np.uint8)).save(OUT / f"{take}-gold.png")
Image.fromarray((soft * 255).astype(np.uint8)).save(OUT / f"{take}-goldmask.png")
print(take, "gilded", int(ochre.sum()), "pixels")

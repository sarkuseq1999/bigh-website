"""The menu bar's Science scroll (round 5, October 6, 2026): the reading still life as a plate of the
same weight as the cell and the inkstone.

The homepage's story-reading-v2.webp is a tall room: the book, the glasses, the cup and a pencil
sit in its lower third under a lot of pale paper and a window dissolving into it. Shown in the
Science scroll beside Dr. Liu's print, the cell and the inkstone it read as a pale grey sketch.
This cuts the group itself out of the painting (no new painting, nothing invented) and gives its
washes body:

  - crop to the table group (the book, glasses, cup and pencil), at the painting's own pixels;
  - deepen the ink with a curve on darkness (white stays exactly white, so under multiply the
    paper never shows as a box; the pale washes and the mid greys darken, the blacks hold);
  - dissolve the crop's edges into white through a soft rounded falloff, so the plate has no edge
    of its own (the Multiply Rule: paper divided out, nothing on a box).

usage: python -X utf8 reference/nav/make_science_plates.py
writes public/images/home-v2/nav/inscription/reading-still-life.webp
"""

from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "public/images/home-v2/ink/story-reading-v2.webp"
OUT = ROOT / "public/images/home-v2/nav/inscription/reading-still-life.webp"

# The table group in the original's pixels (1744 x 2336): the cup's rim at about y 1200, the
# book's spine and the pencil's tip at about y 2060.
BOX = (24, 1090, 1720, 2190)
# The curve, on lightness (0 ink, 1 paper): lightness ** GAMMA. Paper stays 1; a pale wash at
# 0.9 goes to 0.80, a mid grey at 0.6 to 0.34. (1.75 still read light beside the cell; 2.4 turned
# the pages muddy.)
GAMMA = 2.1
# How far in from each edge the plate dissolves to white (share of the plate's size).
FADE_X, FADE_Y = 0.16, 0.2

img = Image.open(SRC).convert("RGB").crop(BOX)
a = np.asarray(img, dtype=np.float32) / 255.0
a = np.power(a, GAMMA)

h, w = a.shape[:2]
yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
# Distance into the plate from its nearest edge, per axis, as 0..1 over the fade band.
fx = np.clip(np.minimum(xx, w - 1 - xx) / (FADE_X * w), 0, 1)
fy = np.clip(np.minimum(yy, h - 1 - yy) / (FADE_Y * h), 0, 1)
# Smooth, and combined so the corners round off instead of meeting at a square.
sx, sy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
keep = sx * sy
a = 1 - (1 - a) * keep[..., None]

out = Image.fromarray(np.clip(a * 255 + 0.5, 0, 255).astype(np.uint8), "RGB")
OUT.parent.mkdir(parents=True, exist_ok=True)
out.save(OUT, "WEBP", quality=88, method=6)

before = 255 - np.asarray(Image.open(SRC).convert("L").crop(BOX), dtype=np.float32)
after = 255 - np.asarray(out.convert("L"), dtype=np.float32)
print(f"{OUT.relative_to(ROOT)} {out.size}: mean darkness {before.mean():.1f} -> {after.mean():.1f}")

"""Cut the four powder heaps out of the capsule painting's full-size original, one picture each,
their sides and the ground under them faded away so they stand alone (mockup only). The paper is
divided out (its colour taken from a bare corner), then each heap is un-multiplied from white (ink
over paper) so it sits on any paper and can move without a blend group round it. The heaps are
sized by amount: two at 400 mg, then 200 mg, then 100 mg.

usage: python -X utf8 make_heaps.py
writes art/heap-<key>.webp and prints each one's size and the CSS width to draw it at
"""

from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

HERE = Path(__file__).parent
REPO = HERE.parents[3]
img = np.asarray(Image.open(REPO / "reference/ink-pages/nuricell/originals/gpt25-P7-capsule.png").convert("RGB")).astype(np.float32)
paper = np.median(img[80:420, 80:420].reshape(-1, 3), axis=0)
ink = np.clip(img / paper, 0, 1) * 255
ink[ink > 246] = 255  # the paper's own fibre, not ink
# No gold on the heaps: the falling flecks near their tips go back to paper (they fly separately).
chroma = ink.max(axis=2) - ink.min(axis=2)  # on the paper-divided image: ink is grey there
gold = np.asarray(Image.fromarray(((chroma > 45) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7))) > 0
ink[gold] = 255

# left, top, right, bottom in the 2048 x 2048 original; the heap's key by its amount.
BOXES = {
    "alcar": (528, 1545, 850, 1772),
    "creatine": (832, 1590, 1170, 1768),
    "ala": (1150, 1612, 1398, 1770),
    "choline": (1380, 1650, 1556, 1768),
}

for key, (x0, y0, x1, y1) in BOXES.items():
    c = ink[y0:y1, x0:x1].copy()
    h, w = c.shape[:2]
    # Fade the sides (where the neighbouring heap or the ground runs on) and the bottom to paper.
    fx = np.minimum(np.linspace(0, 1, w) / 0.14, np.linspace(1, 0, w) / 0.14).clip(0, 1)
    fy = (np.linspace(1, 0, h) / 0.2).clip(0, 1)
    fade = (fx[None, :] * fy[:, None])[..., None]
    c = 255 - (255 - c) * fade
    a = 1 - c.min(axis=2, keepdims=True) / 255
    rgb = np.clip((c - 255 * (1 - a)) / np.maximum(a, 0.02), 0, 255)
    rgba = np.dstack([rgb, a * 255]).astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(HERE / f"art/heap-{key}.webp", quality=90)
    print(f"{key} {w}x{h}  --hw: {w * 0.586:.0f}px")

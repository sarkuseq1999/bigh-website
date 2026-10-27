"""Cut the handscroll band into its places for the 'one place per screen' mockup.

Each crop fades to paper (white: the band has its paper divided out) where it cuts through ink.
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(r"C:\Users\mcbig\Documents\codes\bigh-website")
BAND = REPO / "public/images/science/ink/scroll-v2.webp"
OUT = Path(__file__).parent / "mock"
OUT.mkdir(exist_ok=True)

# name: (left, right, fade_left, fade_right) in band px; fades as a share of the crop's width.
CROPS = {
    "okayama": (0, 1250, 0.0, 0.28),
    "berkeley": (1850, 2950, 0.30, 0.16),
    "salzburg": (3300, 4450, 0.16, 0.16),
    "california": (4420, 5756, 0.16, 0.0),
    "okayama-phone": (110, 1010, 0.06, 0.14),
    "berkeley-phone": (2080, 2960, 0.14, 0.12),
    "salzburg-phone": (3440, 4400, 0.10, 0.10),
    "california-phone": (4600, 5720, 0.10, 0.06),
}


def smooth(t):
    t = np.clip(t, 0, 1)
    return t * t * (3 - 2 * t)


band = np.asarray(Image.open(BAND).convert("RGB")).astype(np.float32)
for name, (a, b, fl, fr) in CROPS.items():
    crop = band[:, a:b].copy()
    w = crop.shape[1]
    x = np.arange(w, dtype=np.float32)
    keep = np.ones(w, dtype=np.float32)
    if fl:
        keep *= smooth(x / (fl * w))
    if fr:
        keep *= smooth((w - 1 - x) / (fr * w))
    crop = 255 - (255 - crop) * keep[None, :, None]
    # Trim the empty paper above and below the ink (rows with any real ink), with a small pad.
    rows = np.where((crop.min(axis=2) < 200).sum(axis=1) > w * 0.01)[0]
    pad = round(crop.shape[0] * 0.03)
    top, bottom = max(0, rows[0] - pad), min(crop.shape[0], rows[-1] + 1 + pad)
    crop = crop[top:bottom]
    img = Image.fromarray(np.clip(np.rint(crop), 0, 255).astype(np.uint8))
    img.save(OUT / f"{name}.webp", quality=92)
    print(name, img.size)
sys.exit(0)

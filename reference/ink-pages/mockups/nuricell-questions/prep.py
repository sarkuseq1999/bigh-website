"""Divide each painting's paper out (so it multiplies onto the page's own paper) and fade its outer
edge to white, as the page build scripts do. art/<name>.png -> art/div/<name>.png

usage: python -X utf8 prep.py [name ...]
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).parent
ART = HERE / "art"
OUT = ART / "div"
OUT.mkdir(exist_ok=True)

names = sys.argv[1:] or [p.stem for p in ART.glob("*.png")]
for name in names:
    im = np.asarray(Image.open(ART / f"{name}.png").convert("RGB")).astype(np.float32)
    h, w, _ = im.shape
    b = max(8, int(min(h, w) * 0.03))
    border = np.concatenate(
        [im[:b].reshape(-1, 3), im[-b:].reshape(-1, 3), im[:, :b].reshape(-1, 3), im[:, -b:].reshape(-1, 3)]
    )
    paper = np.percentile(border, 75, axis=0)
    out = np.clip(im / paper * 255.0, 0, 255)
    # Fade the outer 7% to white so no edge of the picture shows on the page.
    fy = np.clip(np.minimum(np.arange(h), np.arange(h)[::-1]) / (h * 0.07), 0, 1)
    fx = np.clip(np.minimum(np.arange(w), np.arange(w)[::-1]) / (w * 0.07), 0, 1)
    f = np.minimum.outer(fy, fx)[..., None]
    f = f * f * (3 - 2 * f)
    out = 255 - (255 - out) * f
    Image.fromarray(out.astype(np.uint8)).save(OUT / f"{name}.png", optimize=True)
    print(name, "paper", paper.round(1))

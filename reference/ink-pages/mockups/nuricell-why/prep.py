"""Get a Codex painting ready to lie on the page: the paper divided out (so it multiplies onto the
page's own paper with no box), cropped to its ink with a margin, the edges feathered to white.

usage: python -X utf8 prep.py <painting.png> <out-name>   -> art/<out-name>.png
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

HERE = Path(__file__).parent
ART = HERE / "art"
ART.mkdir(exist_ok=True)


def divided(path):
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.float32)
    # The paper: the brightest quarter of the picture, per channel.
    lum = a.mean(axis=2)
    paper = np.median(a[lum > np.percentile(lum, 75)], axis=0)
    d = np.clip(a / paper * 255.0, 0, 255)
    # The faintest 3% is paper fibre, not paint: lift it to white.
    d = np.where(d.mean(axis=2, keepdims=True) > 247, 255, d)
    return d.astype(np.uint8)


def crop_to_ink(d, pad=0.06):
    ink = d.mean(axis=2) < 235
    rows = np.where(ink.sum(axis=1) > 2)[0]
    cols = np.where(ink.sum(axis=0) > 2)[0]
    h, w = ink.shape
    py, px = int(h * pad), int(w * pad)
    y0, y1 = max(0, rows[0] - py), min(h, rows[-1] + py)
    x0, x1 = max(0, cols[0] - px), min(w, cols[-1] + px)
    return d[y0:y1, x0:x1]


def feathered(d):
    img = Image.fromarray(d)
    w, h = img.size
    m = Image.new("L", (w, h), 0)
    edge = int(min(w, h) * 0.05)
    m.paste(255, (edge, edge, w - edge, h - edge))
    m = m.filter(ImageFilter.GaussianBlur(edge / 2))
    return Image.composite(img, Image.new("RGB", (w, h), "white"), m)


src, out = sys.argv[1], sys.argv[2]
art = feathered(crop_to_ink(divided(src)))
art.save(ART / f"{out}.png")
print(out, art.size)

"""Get Codex paintings ready to lie on the page: paper divided out (so they multiply onto the page's
own paper with no box), cropped.

usage:
  python -X utf8 prep.py name <painting.png> <prefix>     -> art/<prefix>-nuri.png, art/<prefix>-cell.png
  python -X utf8 prep.py paint <painting.png> <out-name>   -> art/<out-name>.png (whole painting, edges feathered)
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


def name(path, prefix):
    d = divided(path)
    ink = d.mean(axis=2) < 150
    cols = np.where(ink.sum(axis=0) > 3)[0]
    # The widest run of empty columns inside the ink is the gap between the two words.
    gaps = np.diff(cols)
    split = cols[np.argmax(gaps)]
    for word, (x0, x1) in {
        "nuri": (cols[0], split + 1),
        "cell": (cols[np.argmax(gaps) + 1], cols[-1] + 1),
    }.items():
        part = ink[:, x0:x1]
        rows = np.where(part.sum(axis=1) > 3)[0]
        y0, y1 = rows[0], rows[-1] + 1
        pad = 6
        crop = d[max(0, y0 - pad) : y1 + pad, max(0, x0 - pad) : x1 + pad]
        Image.fromarray(crop).save(ART / f"{prefix}-{word}.png")
        print(word, crop.shape, "ink rows", y0, y1)


def paint(path, out):
    d = Image.fromarray(divided(path))
    w, h = d.size
    # Feather the edges into white so no edge of the sheet shows.
    m = Image.new("L", (w, h), 0)
    edge = int(min(w, h) * 0.06)
    m.paste(255, (edge, edge, w - edge, h - edge))
    m = m.filter(ImageFilter.GaussianBlur(edge / 2))
    white = Image.new("RGB", (w, h), "white")
    Image.composite(d, white, m).save(ART / f"{out}.png")
    print(out, d.size)


if __name__ == "__main__":
    {"name": name, "paint": paint}[sys.argv[1]](sys.argv[2], sys.argv[3])

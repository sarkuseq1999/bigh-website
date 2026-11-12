"""Cut the About "Our experience" round's paintings for the mockups (November 11, 2026).

    python -X utf8 reference/ink-pages/about-experience/cut_mockups.py [name ...]

Each originals/<name>.png gets its paper divided out (white = no paint, so it multiplies onto the
page's own paper, as the site's paintings do), its edges faded and its empty margins trimmed.
Out: plates/img/<name>.png (git-ignored) and one line per picture with its size and shape.
The same steps as reference/ink-pages/about-purpose/cut_mockups.py.
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
IMG = HERE / "plates" / "img"
FLOOR = 10
FADE = 40
PAD = 24


def load(path):
    """The painting as RGB; a picture with transparency is laid on white paper first."""
    img = Image.open(path)
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        paper = Image.new("RGBA", img.size, (255, 255, 255, 255))
        img = Image.alpha_composite(paper, img)
    return np.asarray(img.convert("RGB")).astype(float)


def paperless(a):
    """The painting with its paper divided out: white = no paint."""
    edge = np.concatenate([a[:40].reshape(-1, 3), a[:, :40].reshape(-1, 3), a[:, -40:].reshape(-1, 3)])
    paper = np.percentile(edge, 60, axis=0)
    dark = 255.0 - np.clip(a / paper * 255.0, 0, 255)
    dark = np.clip((dark - FLOOR) / (1 - FLOOR / 255.0), 0, 255)
    h, w = dark.shape[:2]
    ramp = lambda n: np.clip(np.minimum(np.arange(n), np.arange(n)[::-1]) / FADE, 0, 1)
    dark *= (ramp(h)[:, None] * ramp(w)[None, :])[..., None]
    return dark


def trim(dark):
    """Cut the empty paper round the painting, leaving a small margin."""
    ink = dark.max(axis=2) > 6
    rows = np.where(ink.mean(axis=1) > 0.004)[0]
    cols = np.where(ink.mean(axis=0) > 0.004)[0]
    h, w = ink.shape
    top, bottom = max(rows[0] - PAD, 0), min(rows[-1] + PAD, h)
    left, right = max(cols[0] - PAD, 0), min(cols[-1] + PAD, w)
    return dark[top:bottom, left:right]


def main():
    names = sys.argv[1:] or sorted(p.stem for p in (HERE / "originals").glob("*.png"))
    IMG.mkdir(parents=True, exist_ok=True)
    for name in names:
        dark = trim(paperless(load(HERE / "originals" / f"{name}.png")))
        img = Image.fromarray((255.0 - dark).astype(np.uint8))
        img.save(IMG / f"{name}.png")
        print(f"{name}: {img.width} x {img.height}, shape {img.width / img.height:.3f}")


main()

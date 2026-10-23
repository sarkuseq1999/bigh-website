"""Mockup only (October 23, 2026): three Free radicals samples that show harm (A burnt roof, B burnt
machine, C with and without the screen), each with its paper divided out so the page multiplies it
onto its rice paper.

usage: python -X utf8 reference/ink-pages/mockups/home-science-harm/plates.py <name> [<name> ...]
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ORIG = HERE.parents[1] / "home-science" / "originals"
OUT = HERE / "img"
W = 1600


def plate(im, fade=0.08):
    """The painting with its paper divided out and its edges dissolved."""
    im = np.asarray(im.convert("RGB")).astype(np.float32)
    h, w, _ = im.shape
    b = max(8, min(h, w) // 40)
    border = np.concatenate(
        [im[:b].reshape(-1, 3), im[-b:].reshape(-1, 3), im[:, :b].reshape(-1, 3), im[:, -b:].reshape(-1, 3)]
    )
    flat = np.clip(im / np.median(border, axis=0) * 255.0, 0, 255)
    yy = np.linspace(0, 1, h)[:, None]
    xx = np.linspace(0, 1, w)[None, :]
    d = np.minimum(np.minimum(yy, 1 - yy) / fade, np.minimum(xx, 1 - xx) / (fade * h / w))
    a = np.clip(d, 0, 1)
    a = (a * a * (3 - 2 * a))[..., None]
    return 255 - (255 - flat) * a


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name in sys.argv[1:]:
        im = Image.open(ORIG / f"{name}.png")
        im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
        Image.fromarray(plate(im).astype(np.uint8)).save(OUT / f"{name}.webp", quality=88)
        print(name, im.size)

"""Cut the About opening mockup pictures (Mo asked for new opening ideas, October 27, 2026).

Each painting's paper is turned to transparency (white to alpha, after dividing out the paper's
colour), so it lays over the live page's own paper with no box and no blend mode.

    python -X utf8 reference/ink-pages/about-opening/cut_mockups.py superbloom-a1 walk-b1 ...

Scenes come from originals/<take>.png; the letters (concept C) from the October 6 letter
paintings in ../about/originals/. Output: plates/img/<name>.png (git-ignored).
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
OUT = HERE / "plates" / "img"
LETTERS = HERE.parent / "about" / "originals"


def divided(img, top=False):
    """Paper -> white, ink kept. The paper colour is the median of the picture's outer frame (of
    its top tenth for a landscape, whose foot and sides are painted to the edge)."""
    arr = np.asarray(img.convert("RGB")).astype(np.float32)
    h, w, _ = arr.shape
    m = max(4, min(h, w) // 40)
    frame = arr[: h // 10].reshape(-1, 3) if top else np.concatenate(
        [arr[:m].reshape(-1, 3), arr[-m:].reshape(-1, 3), arr[:, :m].reshape(-1, 3), arr[:, -m:].reshape(-1, 3)]
    )
    paper = np.median(frame, axis=0)
    out = np.clip(arr / paper * 255.0, 0, 255)
    # Lift the paper's fibres to white: anything above KNEE ramps to pure white.
    knee, white = 228.0, 246.0
    lum = out.min(axis=2, keepdims=True)
    lift = np.clip((lum - knee) / (white - knee), 0, 1)
    return out + (255.0 - out) * lift


def to_alpha(arr):
    """White to transparency: alpha from the darkest channel, colour un-mixed from white."""
    a = 1.0 - arr.min(axis=2, keepdims=True) / 255.0
    safe = np.where(a > 1e-3, a, 1.0)
    rgb = np.clip((arr - 255.0 * (1.0 - a)) / safe, 0, 255)
    return Image.fromarray(np.concatenate([rgb, a * 255.0], axis=2).astype(np.uint8), "RGBA")


def ink_box(arr, level=170, pad=0.03):
    """The box around the ink: rows and columns holding at least a few clearly dark pixels (the
    paper's own fibres are scattered single specks)."""
    dark = arr.min(axis=2) < level
    rows, cols = np.nonzero(dark.sum(axis=1) >= 4)[0], np.nonzero(dark.sum(axis=0) >= 4)[0]
    y0, y1, x0, x1 = rows.min(), rows.max(), cols.min(), cols.max()
    p = int(max(y1 - y0, x1 - x0) * pad)
    h, w = dark.shape
    return max(0, x0 - p), max(0, y0 - p), min(w, x1 + p), min(h, y1 + p)


def scene(take, width=2400):
    img = Image.open(HERE / "originals" / f"{take}.png")
    out = to_alpha(divided(img, top=True))
    if out.width > width:
        out = out.resize((width, round(out.height * width / out.width)), Image.LANCZOS)
    out.save(OUT / f"{take}.png", optimize=True)
    print(take, out.size)


def letters():
    for key in "bigh":
        arr = divided(Image.open(LETTERS / f"gpt25-letter-{key}-v1.png"))
        box = ink_box(arr)
        out = to_alpha(arr).crop(box)
        out = out.resize((round(out.width * 600 / out.height), 600), Image.LANCZOS)
        out.save(OUT / f"letter-{key}.png", optimize=True)
        print("letter", key, out.size, "box", box)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name in sys.argv[1:]:
        letters() if name == "letters" else scene(name)

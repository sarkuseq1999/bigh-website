"""Build the homepage science section's steam-train paintings (October 21, 2026, idea A: one small
steam engine in the redwoods for all three topics) from the Codex originals.

Each painting ships as an ink plate: the paper is divided out (paper -> white, ink kept), so the
page lays it on with mix-blend-mode: multiply and its own rice paper shows through. Paint that runs
off an original's edge dissolves into the paper over the outer 8%. The originals are 4:3, the
stage's own shape (2000:1493), so each is only scaled into the stage's 1600 x 1195; the three ages
were painted from one picture, so they still line up for the age slider.

Output: public/images/home-v2/ink/science/train-<state>-v1.webp

usage: python -X utf8 reference/ink-pages/home-science/build_train.py
"""

from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
ORIG = HERE / "originals"
OUT = REPO / "public/images/home-v2/ink/science"
W, H = 1600, 1195

# shipped state -> original
TRAINS = {
    "fuel": "train-fuel-a2",
    "sparks": "train-sparks-c1",
    "new": "train-new-a1",
    "middle": "train-middle-a1",
    "old": "train-old-a1",
}


def plate(im, fade=0.08):
    """The painting with its paper divided out and its edges dissolved, floats 0..255."""
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


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for state, name in TRAINS.items():
        im = Image.open(ORIG / f"{name}.png").resize((W, H), Image.LANCZOS)
        out = OUT / f"train-{state}-v1.webp"
        Image.fromarray(plate(im).astype(np.uint8)).save(out, quality=86, method=6)
        print(out.name, f"{out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()

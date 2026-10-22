"""Build the homepage science section's "Aging cells" paintings (October 22, 2026: Mo found the
steam train did not relate to the age slider and picked B, one brain cell up close) from the
Codex originals.

Codex painted the middle-aged and old cell from the young one, but moved and resized the cell a
little; measured by reference/ink-pages/mockups/home-science-cell/align.py, each is scaled about
its centre and shifted back (paper filled in) so the three line up under the slider's cross-fade.
Then, as build_train.py does, the paper is divided out (paper -> white, ink kept) so the page lays
each on with mix-blend-mode: multiply, paint that runs off an edge dissolves over the outer 8%, and
the 4:3 original is scaled into the stage's 1600 x 1195. The young cell's branch tips reach the
top-right corner, where the stage's "Illustrations" tag sits, so they dissolve there too.

Output: public/images/home-v2/ink/science/cell-<age>-v2.webp (v2: the tag's corner cleared; v1
ran a branch tip through the tag)

usage: python -X utf8 reference/ink-pages/home-science/build_cell.py
"""

from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
ORIG = HERE / "originals"
OUT = REPO / "public/images/home-v2/ink/science"
W, H = 1600, 1195

# shipped age -> (original, scale about the centre, shift x, shift y in the original's pixels)
CELLS = {
    "young": ("close-young-a2", 1.0, 0, 0),
    "middle": ("close-middle-a1", 1.02, -3, -1),
    "old": ("close-old-a1", 1.05, -7, 3),
}


def paper_of(im):
    """The paper's colour: the median of the picture's outer band."""
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    h, w, _ = a.shape
    b = max(8, min(h, w) // 40)
    border = np.concatenate(
        [a[:b].reshape(-1, 3), a[-b:].reshape(-1, 3), a[:, :b].reshape(-1, 3), a[:, -b:].reshape(-1, 3)]
    )
    return np.median(border, axis=0)


def line_up(im, scale, dx, dy):
    """Scale the painting about its centre and shift it, filling the uncovered edge with paper."""
    if scale == 1.0 and dx == 0 and dy == 0:
        return im
    w, h = im.size
    fill = tuple(int(round(c)) for c in paper_of(im))
    # PIL maps each output pixel back to its source: x = (x' - (1 - s) w / 2 - dx) / s
    data = (1 / scale, 0, -((1 - scale) * w / 2 + dx) / scale, 0, 1 / scale, -((1 - scale) * h / 2 + dy) / scale)
    return im.convert("RGB").transform((w, h), Image.AFFINE, data, Image.BICUBIC, fillcolor=fill)


def plate(im, fade=0.08):
    """The painting with its paper divided out and its edges dissolved, floats 0..255."""
    paper = paper_of(im)
    im = np.asarray(im.convert("RGB")).astype(np.float32)
    h, w, _ = im.shape
    flat = np.clip(im / paper * 255.0, 0, 255)
    yy = np.linspace(0, 1, h)[:, None]
    xx = np.linspace(0, 1, w)[None, :]
    d = np.minimum(np.minimum(yy, 1 - yy) / fade, np.minimum(xx, 1 - xx) / (fade * h / w))
    a = np.clip(d, 0, 1)
    a = (a * a * (3 - 2 * a))[..., None]
    return 255 - (255 - flat) * a


def clear_tag(ink, left=0.70, bottom=0.13, soft=70):
    """Dissolve the branch tips that reach the top-right corner, where the stage's "Illustrations"
    tag sits (measured on the built page from 360 to 1920px wide: x 0.72-0.96, y 0.04-0.12 of
    the painting), so no stroke runs through its letters: the paint fades into the paper over
    `soft` pixels before the tag's corner, as it does at the painting's edges."""
    h, w, _ = ink.shape
    dx = np.clip(left * w - np.arange(w)[None, :], 0, None)
    dy = np.clip(np.arange(h)[:, None] - bottom * h, 0, None)
    a = np.clip(np.hypot(dx, dy) / soft, 0, 1)
    a = (a * a * (3 - 2 * a))[..., None]
    return 255 - (255 - ink) * a


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for age, (name, scale, dx, dy) in CELLS.items():
        im = line_up(Image.open(ORIG / f"{name}.png"), scale, dx, dy).resize((W, H), Image.LANCZOS)
        out = OUT / f"cell-{age}-v2.webp"
        Image.fromarray(clear_tag(plate(im)).astype(np.uint8)).save(out, quality=86, method=6)
        print(out.name, f"{out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()

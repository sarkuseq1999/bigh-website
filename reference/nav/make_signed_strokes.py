# Menu bar "Signed with one stroke" (Mo's pick A, October 21, 2026). Cuts the two painted strokes
# the bar uses from two Codex paintings (no API spend; prompts in reference/nav/prompts/):
#   - the loaded black swash Sign up and Menu are written on (originals/codex-swash-black.png),
#   - the pale wash a pointed-at word stands on (the streaky middle of originals/codex-band-pale-wash.png).
"""The bar's two new brush strokes, cut from real paintings.

The ink becomes alpha the way the other cut-outs do (each pixel's distance from the paper), so the
page's paper shows through the dry streaks; the colour is sumi ink, and the stylesheet paints
through the alpha with the bar's own ink.

Output:
  public/images/home-v2/nav/inscription/swash-v1.webp
  public/images/home-v2/nav/inscription/wash-v1.webp

usage: python -X utf8 reference/nav/make_signed_strokes.py
"""

from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
ORIGINALS = REPO / "reference/nav/originals"
OUT = REPO / "public/images/home-v2/nav/inscription"
INK = (12, 11, 10)


def alpha_of(grey, core=None):
    """Ink as alpha: paper (the white's own level) -> 0, the ink's core -> 1 (or, for a pale wash
    with no core, its own darkness, so it stays pale)."""
    paper = np.percentile(grey, 60)
    if core is None:
        core = 0.0
    a = np.clip((paper - 4 - grey) / (paper - 4 - core), 0, 1)
    a[a < 0.03] = 0
    return a


def trim(a, pad=4):
    rows = np.where(a.max(1) > 0.03)[0]
    cols = np.where(a.max(0) > 0.03)[0]
    return a[max(0, rows.min() - pad) : rows.max() + 1 + pad, max(0, cols.min() - pad) : cols.max() + 1 + pad]


def save(a, name, width):
    img = Image.fromarray((np.clip(a, 0, 1) * 255).round().astype(np.uint8), "L")
    img = img.resize((width, round(width * img.size[1] / img.size[0])), Image.LANCZOS)
    rgba = Image.merge("RGBA", (Image.new("L", img.size, INK[0]),) * 3 + (img,))
    rgba.save(OUT / name, lossless=True, method=6)
    print(OUT / name, img.size)


# The swash: one loaded stroke, its round pressed head at the left, dry streaks at the right.
grey = np.asarray(Image.open(ORIGINALS / "codex-swash-black.png").convert("L")).astype(np.float64)
core = np.percentile(grey[grey < 120], 20)
save(trim(alpha_of(grey, core)), "swash-v1.webp", 640)

# The wash: the band's even, streaky middle (no loaded head, no dry tail); the stylesheet softens
# its two ends.
grey = np.asarray(Image.open(ORIGINALS / "codex-band-pale-wash.png").convert("L")).astype(np.float64)
band = trim(alpha_of(grey))
w = band.shape[1]
save(band[:, int(w * 0.3) : int(w * 0.62)], "wash-v1.webp", 560)

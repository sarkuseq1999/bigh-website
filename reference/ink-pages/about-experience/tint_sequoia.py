"""The page's own sequoia, a little coloured, every stroke kept (November 11, 2026).

Mo kept the sequoia ("I think the sequoia tree is a good idea. Maybe just make it a little bit
colored."). This tints the painting that ships (public/images/about-bc/sequoia-v1.webp, ink on
white) the way the homepage's ink was tinted (reference/home-v2/ink/recolor/recolor.py): ink is a
pigment, optical density D = -ln(grey), and a coloured pigment absorbs each channel in its own
ratio, so the new colour is exp(-D * ratio). The giant's trunk (a hand-drawn soft mask) takes the
cinnamon of real sequoia bark; everything else takes greens, pale blue-green where the ink is thin
(the misty trees far off) and sage to olive where it is heavy (the crown, the young sequoia). The
gold leaf stays exactly as it is.

    python -X utf8 reference/ink-pages/about-experience/tint_sequoia.py

Out: originals/sequoia-tint-<strength>.png for each STRENGTH (1 = the full palette).
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "reference" / "home-v2" / "ink" / "recolor"))
from recolor import ramp, smooth  # noqa: E402

SRC = ROOT / "public" / "images" / "about-bc" / "sequoia-v1.webp"

# The giant's trunk in the 1200 x 1202 painting, from its crown down to its flared foot (the young
# sequoia, right of it from x 700, stays out).
TRUNK = [
    (398, 225), (470, 195), (560, 195), (632, 225), (660, 420), (690, 640), (720, 800),
    (770, 920), (840, 1000), (850, 1060), (560, 1090), (270, 1065), (255, 1000), (300, 880),
    (345, 650), (372, 420),
]

BARK = [(0.0, "#d3a587"), (0.5, "#b47555"), (1.2, "#8a5440"), (2.4, "#5a3d33")]
LEAF = [(0.0, "#a9bdb4"), (0.35, "#9db29a"), (0.8, "#7f9868"), (1.6, "#56663f"), (2.6, "#3f4532")]

STRENGTH = {"touch": 0.35, "light": 0.55}


def trunk_mask(w, h):
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).polygon(TRUNK, fill=255)
    m = m.filter(ImageFilter.GaussianBlur(14))
    return np.asarray(m, dtype=np.float64) / 255


def tint(a, D, m, s):
    def colour(stops):
        A = ramp(D, stops)
        A = 1 + s * (A - 1)
        # The blackest lines keep most of their ink, warmed a little.
        k = (smooth(D, 2.0, 3.4) * 0.5)[..., None]
        A = A * (1 - k) + k
        return np.exp(-D[..., None] * A)

    T = colour(BARK) * m[..., None] + colour(LEAF) * (1 - m[..., None])
    # The gold leaf stays exactly as it is.
    sat = a.max(axis=2) - a.min(axis=2)
    g = smooth(sat, 0.08, 0.18)[..., None]
    return T * (1 - g) + a * g


def main():
    a = np.asarray(Image.open(SRC).convert("RGB"), dtype=np.float64) / 255
    h, w = a.shape[:2]
    D = -np.log(np.clip(a.mean(axis=2), 1 / 255, 1))
    m = trunk_mask(w, h)
    for name, s in STRENGTH.items():
        T = tint(a, D, m, s)
        out = HERE / "originals" / f"sequoia-tint-{name}.png"
        Image.fromarray((np.clip(T, 0, 1) * 255 + 0.5).astype(np.uint8)).save(out)
        print(out.name)


main()

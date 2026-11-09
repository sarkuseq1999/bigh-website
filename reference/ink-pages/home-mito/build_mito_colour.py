"""The "Tiny power plants." mitochondrion in two new colourings (Mo, November 4, 2026).

Mo loves the cell's design, but the homepage has turned Californian and colourful around it (the
sequoia opening, the Big Sur close) and the heavy ink cell no longer fits. Both versions start
from the same painting (public/images/home-v2/ink/mito.webp, ink on white) and keep every stroke;
only the paint changes. The gold leaf is left exactly as it is (the page lays its gold layer over
the two folds as before).

  A  California colour: the opening's thin watercolour. The thick outer skin takes a calm redwood
     copper, the inside between the folds a soft sage green, and the ink of the folds a lighter,
     warm grey-green instead of black.
  B  Softer ink: no new colours. All the ink about a third lighter and warmed toward the sepia
     grey of the sequoias' shadows and the hummingbird's wings.

Ink is treated as pigment, as in reference/home-v2/ink/recolor/recolor.py: optical density
D = -ln(grey); a pigment absorbs each channel in its own ratio, so a colour is exp(-D * ratio).

    python -X utf8 build_mito_colour.py   (writes mito-a-v1.webp and mito-b-v1.webp next to it)

Mo picked B (compared live as /home-a and /home-b): mito-b-v1.webp ships unchanged as
public/images/home-v2/ink/mito-soft-v1.webp. A's picture is kept here only.
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "reference" / "home-v2" / "ink" / "recolor"))
from recolor import noise, pig, ramp, smooth  # noqa: E402

SRC = ROOT / "public" / "images" / "home-v2" / "ink" / "mito.webp"


def load():
    a = np.asarray(Image.open(SRC).convert("RGB"), dtype=np.float64) / 255
    D = -np.log(np.clip(a.mean(axis=2), 1 / 255, 1))
    return a, D


def keep_gold(T, a):
    """The painted gold stays exactly as it is."""
    sat = a.max(axis=2) - a.min(axis=2)
    g = smooth(sat, 0.06, 0.16)[..., None]
    return T * (1 - g) + a * g


def masks(D):
    """The cell's silhouette (holes filled), its inside, and its skin (silhouette minus inside),
    worked out small and softened, so a wash follows the painted body, not a round stain."""
    h, w = D.shape
    sw, sh = 500, round(500 * h / w)
    small = Image.fromarray((np.clip(D / 2, 0, 1) * 255).astype(np.uint8)).resize((sw, sh), Image.BILINEAR)
    small = np.asarray(small.filter(ImageFilter.GaussianBlur(2)))
    # The drawn body only: the pale wash that bleeds out round it stays outside (D under ~0.3).
    body = Image.fromarray(((small > 0.15 * 255) * 255).astype(np.uint8))
    body = body.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))
    # Fill the holes: everything the outside can't reach is the cell.
    flood = body.copy()
    ImageDraw.floodfill(flood, (0, 0), 128)
    sil = (np.asarray(flood) != 128).astype(np.uint8) * 255
    sil_img = Image.fromarray(sil)
    inside = sil_img
    for _ in range(4):
        inside = inside.filter(ImageFilter.MinFilter(9))

    def up(im, blur):
        return np.asarray(im.filter(ImageFilter.GaussianBlur(blur)).resize((w, h), Image.BICUBIC), dtype=np.float64) / 255

    S = up(sil_img, 3)
    I = up(inside, 6)
    skin = np.clip(S - I, 0, 1)
    return S, I, skin


def save(T, name):
    out = (np.clip(T, 0, 1) * 255 + 0.5).astype(np.uint8)
    Image.fromarray(out, "RGB").save(HERE / name, "WEBP", quality=88, method=6)
    print("wrote", name)


def softer(a, D):
    """B: the same ink, about a third lighter and warm (sepia grey), the blackest strokes a deep
    warm brown-grey instead of black."""
    Dl = D * 0.66
    A = ramp(Dl, [(0.0, "#c8b8a2"), (0.5, "#a89784"), (1.2, "#6e6155"), (2.2, "#3c332c")])
    T = np.exp(-Dl[..., None] * A)
    return keep_gold(T, a)


def california(a, D):
    """A: the folds in a lighter warm grey-green ink, the skin a calm redwood copper wash, the inside
    a soft sage green, each wash a little uneven like real watercolour."""
    h, w = D.shape
    S, I, skin = masks(D)
    Dl = D * 0.8
    A = ramp(Dl, [(0.0, "#bdb3a6"), (0.6, "#8f8578"), (1.4, "#4f4a42"), (2.4, "#2b2826")])
    T = np.exp(-Dl[..., None] * A)
    lumpy = 0.7 + 0.6 * noise(h, w, 7, 4)
    painted = smooth(D, 0.12, 0.55)
    # Redwood copper in the skin's own wash (the hummingbird's copper, calmed), never on bare paper.
    # Kept light: a dark brown skin round a green inside reads as a cut avocado.
    T = T * np.exp(-(skin * painted * lumpy * 0.32)[..., None] * pig("#b5805f"))
    # Sage green inside, only where the paint is pale (between the folds), not over the strokes,
    # and kept off the gold's warm light (green over it turns teal).
    pale = 1 - smooth(D, 0.3, 0.9)
    sat = a.max(axis=2) - a.min(axis=2)
    warm = np.asarray(
        Image.fromarray((smooth(sat, 0.02, 0.08) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(40)),
        dtype=np.float64,
    ) / 255
    T = T * np.exp(-(I * pale * (1 - np.clip(warm * 2.5, 0, 1)) * lumpy * 0.13)[..., None] * pig("#9fb28a"))
    return keep_gold(T, a)


def main():
    a, D = load()
    save(california(a, D), "mito-a-v1.webp")
    save(softer(a, D), "mito-b-v1.webp")


if __name__ == "__main__":
    main()

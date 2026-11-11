"""Build the About "Our purpose" painting (Mo picked A, the oak on a sunny afternoon, November 10,
2026).

Mo found the purpose's oak (black ink, bare roots hanging in empty paper, an empty swing) "a
little dark or scary". Of three painted ideas (A the same oak on a sunny afternoon, B Monterey Bay
above and below the water, C a San Francisco cable car over its hidden cable) he picked A: the
valley oak in soft colour, a child on the swing, a grandmother pushing, a dog and a picnic, the
roots inside a slice of warm earth and a patch of gold leaf among them (Codex, oak-1-b).

    python -X utf8 reference/ink-pages/about-purpose/build_about_purpose.py

Out: public/images/about-purpose/oak-afternoon-v1.webp, its gold-leaf light mask
oak-afternoon-v1-gold.webp (for the kit's glint) and src/components/about/purpose-art.ts. The
paper is divided out so the painting multiplies onto the page.

The kit's gold_mask (reference/home-v2/ink/build_assets.py) finds gold by colour alone; here the
dry grass and the earth are warm and saturated too, so the leaf is looked for only in the box
under the trunk (LEAF_BOX), by its yellower hue and stronger colour than the earth round it.
"""

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageFilter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SITE = ROOT / "public" / "images" / "about-purpose"
URL = "/images/about-purpose"
ART = ROOT / "src" / "components" / "about" / "purpose-art.ts"

TAKE = "oak-1-b"
NAME = "oak-afternoon-v1"
FLOOR = 10
FADE = 40
PAD = 24
# Where the gold leaf lies in the original (x0, y0, x1, y1), with room round it.
LEAF_BOX = (440, 690, 700, 860)
MASK_WIDTH = 1000


def load(name):
    """The painting as RGB; a picture with transparency is laid on white paper first."""
    img = Image.open(HERE / "originals" / f"{name}.png")
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        paper = Image.new("RGBA", img.size, (255, 255, 255, 255))
        img = Image.alpha_composite(paper, img)
    return np.asarray(img.convert("RGB")).astype(float)


def paperless(a):
    """How dark each pixel is once the paper is divided out (0 = bare paper)."""
    edge = np.concatenate([a[:40].reshape(-1, 3), a[:, :40].reshape(-1, 3), a[:, -40:].reshape(-1, 3)])
    paper = np.percentile(edge, 60, axis=0)
    dark = 255.0 - np.clip(a / paper * 255.0, 0, 255)
    dark = np.clip((dark - FLOOR) / (1 - FLOOR / 255.0), 0, 255)
    h, w = dark.shape[:2]
    ramp = lambda n: np.clip(np.minimum(np.arange(n), np.arange(n)[::-1]) / FADE, 0, 1)
    dark *= (ramp(h)[:, None] * ramp(w)[None, :])[..., None]
    return dark


def box_of(dark):
    """The painting's box: the empty paper round it cut, a small margin left."""
    ink = dark.max(axis=2) > 6
    rows = np.where(ink.mean(axis=1) > 0.004)[0]
    cols = np.where(ink.mean(axis=0) > 0.004)[0]
    h, w = ink.shape
    return max(cols[0] - PAD, 0), max(rows[0] - PAD, 0), min(cols[-1] + PAD, w), min(rows[-1] + PAD, h)


def leaf(a):
    """The gold leaf as a mask over the original (0..255): inside LEAF_BOX, the one patch that is
    yellower (hue 35 degrees or more; the earth and roots are about 29) and stronger in colour
    (saturation 0.46 or more; the earth about 0.4, the grass 0.2 to 0.3) than what lies round it."""
    rgb = a / 255.0
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    hi, lo = rgb.max(axis=2), rgb.min(axis=2)
    sat = (hi - lo) / np.maximum(hi, 1e-4)
    warm = (r >= g) & (g > b)
    hue = np.where(warm, 60 * (g - b) / np.maximum(hi - lo, 1e-4), 0)
    gold = ((hue >= 35) & (sat >= 0.46) & (hi >= 0.6)).astype(np.uint8)
    x0, y0, x1, y1 = LEAF_BOX
    boxed = np.zeros_like(gold)
    boxed[y0:y1, x0:x1] = gold[y0:y1, x0:x1]
    boxed = cv2.morphologyEx(boxed, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    count, labels, stats, _ = cv2.connectedComponentsWithStats(boxed, connectivity=8)
    if count < 2:
        raise SystemExit("no gold leaf found in LEAF_BOX")
    biggest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    patch = (labels == biggest).astype(np.uint8) * 255
    x, y, w, h, area = stats[biggest]
    if x <= x0 or y <= y0 or x + w >= x1 or y + h >= y1:
        raise SystemExit(f"the gold leaf runs into LEAF_BOX's edge: {(x, y, w, h)}")
    print(f"gold leaf: {w} x {h} at ({x}, {y}), {area} px")
    return patch


def main():
    a = load(TAKE)
    dark = paperless(a)
    x0, y0, x1, y1 = box_of(dark)
    ink = Image.fromarray((255.0 - dark[y0:y1, x0:x1]).astype(np.uint8))
    SITE.mkdir(parents=True, exist_ok=True)
    ink.save(SITE / f"{NAME}.webp", quality=90, method=6)

    mask = Image.fromarray(leaf(a)[y0:y1, x0:x1], "L")
    mask = mask.resize((MASK_WIDTH, round(mask.height * MASK_WIDTH / mask.width)), Image.LANCZOS)
    mask = mask.filter(ImageFilter.GaussianBlur(1.2))
    white = Image.new("L", mask.size, 255)
    Image.merge("RGBA", (white, white, white, mask)).save(SITE / f"{NAME}-gold.webp", "WEBP", quality=80, method=6)
    cover = float((np.asarray(mask) > 128).mean())

    ART.write_text(
        "// Generated by reference/ink-pages/about-purpose/build_about_purpose.py. Do not edit by hand.\n"
        "// The About page's purpose painting: the valley oak on a sunny afternoon (Mo picked A,\n"
        "// November 10, 2026), its paper divided out so it multiplies onto the page; `gold` is the\n"
        "// light mask over its gold leaf, for the kit's glint.\n"
        "export const purposeOak = {\n"
        f'  src: "{URL}/{NAME}.webp",\n'
        f"  width: {ink.width},\n"
        f"  height: {ink.height},\n"
        f'  gold: "{URL}/{NAME}-gold.webp",\n'
        "} as const;\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"{NAME}: {ink.width} x {ink.height}, shape {ink.width / ink.height:.4f}, gold {cover:.2%} of the picture")
    for f in (f"{NAME}.webp", f"{NAME}-gold.webp"):
        print(f"  {f}: {(SITE / f).stat().st_size // 1024} KB")


main()

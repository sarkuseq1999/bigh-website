"""Build the About page's two new chapters' pictures (DRAFT for Mo, November 4, 2026).

- Our ingredients: the botanist's four specimens (Codex), paper divided out so it multiplies onto
  the page.
- Our home: a Southern California morning (Codex), the five real approved bottles standing on its
  empty ground (public/images/products/*.png, unchanged, only scaled), a soft shadow under each,
  and a strip of golden grass and lupines (Codex) in front of their feet. Three layers of one size,
  stacked in the page: the painting (multiply), the bottles (normal), the grass (multiply).

    python -X utf8 reference/ink-pages/about-chapters/build_about_chapters.py

Out: public/images/about-chapters/*.webp and src/components/about/chapters-art.ts; lossless plates
in plates/ (git-ignored).
"""

from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SITE = ROOT / "public" / "images" / "about-chapters"
PRODUCTS = ROOT / "public" / "images" / "products"
PLATES = HERE / "plates"
ART = ROOT / "src" / "components" / "about" / "chapters-art.ts"

# The site's file names. The image optimizer caches by name: a changed picture needs a new one.
NAMES = {"plants": "plants-v1", "home": "home-v2", "bottles": "home-bottles-v2", "front": "home-front-v2"}
# Which take of each painting ships.
TAKES = {"plants": "plants-2-a", "home": "home-1-a", "front": "front-1-a"}
FLOOR = 10  # paper grain under this much ink is dropped (it showed as a pale box)
FADE = 40  # the painting's own edges fade out over this many pixels

# The bottles, left to right (NuriCell, the flagship, in the middle).
BOTTLES = ["turmerific", "advanced-opc", "nuricell", "green-bee-propolis", "nature-calm"]
# Placement on the home painting, as fractions of its size: the ground line under the bottles,
# each bottle's height, the centre of the row, the step between bottle centres.
GROUND = 0.86
BOTTLE_H = 0.33
ROW_X = 0.5
STEP = 0.128
# How far above the ground line the grass in front of the bottles reaches (fraction of the
# painting's height); the rest of the strip stands behind them, painted into the scene itself.
FRONT_REACH = 0.035
# Rows of empty sky cut from the top of the home picture (the palms' heads start below it).
SKY = 110
# The grass strip's own band (fractions of its picture's height), laid with its middle on GROUND.
GRASS_BAND = (0.74, 1.0)


def paperless(name):
    """The painting with its paper divided out: white = no paint, so it multiplies onto the page."""
    a = np.asarray(Image.open(HERE / "originals" / f"{name}.png").convert("RGB")).astype(float)
    edge = np.concatenate([a[:40].reshape(-1, 3), a[:, :40].reshape(-1, 3), a[:, -40:].reshape(-1, 3)])
    paper = np.percentile(edge, 60, axis=0)
    dark = 255.0 - np.clip(a / paper * 255.0, 0, 255)
    dark = np.clip((dark - FLOOR) / (1 - FLOOR / 255.0), 0, 255)
    h, w = dark.shape[:2]
    ramp = lambda n: np.clip(np.minimum(np.arange(n), np.arange(n)[::-1]) / FADE, 0, 1)
    dark *= (ramp(h)[:, None] * ramp(w)[None, :])[..., None]
    return Image.fromarray((255.0 - dark).astype(np.uint8))


def trim(img, pad=24):
    """Crop to the ink, keeping `pad` px of paper round it."""
    c = np.asarray(img)
    ys, xs = np.where((255 - c.min(axis=2)) > 14)
    box = (
        max(int(xs.min()) - pad, 0),
        max(int(ys.min()) - pad, 0),
        min(int(xs.max()) + 1 + pad, img.width),
        min(int(ys.max()) + 1 + pad, img.height),
    )
    return img.crop(box), box


def bottles_layer(size):
    """The five real bottles on a transparent sheet the painting's size, with soft shadows."""
    w, h = size
    sheet = Image.new("RGBA", size, (0, 0, 0, 0))
    shadow = Image.new("L", size, 0)
    draw = ImageDraw.Draw(shadow)
    n = len(BOTTLES)
    placed = []
    for i, slug in enumerate(BOTTLES):
        im = Image.open(PRODUCTS / f"{slug}.png").convert("RGBA")
        im = im.crop(im.getbbox())
        bh = round(h * BOTTLE_H)
        bw = round(im.width * bh / im.height)
        im = im.resize((bw, bh), Image.LANCZOS)
        cx = w * (ROW_X + (i - (n - 1) / 2) * STEP)
        x = round(cx - bw / 2)
        y = round(h * GROUND - bh)
        placed.append((im, x, y))
        # A low soft shadow on the ground, a little wider than the bottle's foot.
        sw, sh = bw * 0.62, bh * 0.05
        draw.ellipse((cx - sw, h * GROUND - sh * 0.9, cx + sw, h * GROUND + sh * 0.6), fill=120)
    shadow = shadow.filter(ImageFilter.GaussianBlur(h * 0.012))
    tint = Image.new("RGBA", size, (40, 34, 26, 0))
    tint.putalpha(shadow.point(lambda v: round(v * 0.55)))
    sheet = Image.alpha_composite(sheet, tint)
    for im, x, y in placed:
        sheet.alpha_composite(im, (x, y))
    return sheet


def grass_sheet(size):
    """The grass strip, cut to its band and laid with its middle on the bottles' ground line."""
    w, h = size
    grass = paperless(TAKES["front"])
    gw, gh = grass.size
    band = grass.crop((0, round(gh * GRASS_BAND[0]), gw, round(gh * GRASS_BAND[1])))
    band = band.resize((w, round(band.height * w / gw)), Image.LANCZOS)
    sheet = Image.new("RGB", size, "white")
    top = round(h * GROUND - band.height * 0.55)
    sheet.paste(band, (0, top))
    return sheet


def split_grass(grass):
    """The strip in two: what stands behind the bottles and what stands in front of their feet
    (below FRONT_REACH over the ground line), the seam softened over a few pixels so no blade ends
    in a cut. Together they are the strip once, so no blade is painted twice."""
    w, h = grass.size
    a = 255.0 - np.asarray(grass).astype(float)
    y = np.arange(h)[:, None, None]
    edge = h * (GROUND - FRONT_REACH)
    front = np.clip((y - edge) / (h * 0.02), 0, 1)
    paint = lambda k: Image.fromarray((255.0 - a * k).astype(np.uint8))
    return paint(1 - front), paint(front)


def save(img, name, quality=88):
    PLATES.mkdir(exist_ok=True)
    img.save(PLATES / f"{name}.png", optimize=True)
    out = SITE / f"{name}.webp"
    img.save(out, quality=quality, method=6)
    return out.stat().st_size


def main():
    SITE.mkdir(parents=True, exist_ok=True)
    plants, _ = trim(paperless(TAKES["plants"]))
    print("plants", plants.size, save(plants, NAMES["plants"]))

    # The grass strip's upper part is painted into the scene (behind the bottles); its lowest
    # blades stand in front of their feet, on their own layer.
    scene = paperless(TAKES["home"])
    behind, front = split_grass(grass_sheet(scene.size))
    home = ImageChops.multiply(scene, behind)
    bottles = bottles_layer(home.size)
    # The sky's empty top, cut from all three alike so they still stack.
    crop = (0, SKY, home.width, home.height)
    home, bottles, front = home.crop(crop), bottles.crop(crop), front.crop(crop)
    print("home", home.size, save(home, NAMES["home"]))
    print("bottles", bottles.size, save(bottles, NAMES["bottles"], quality=90))
    print("front", front.size, save(front, NAMES["front"]))

    ART.write_text(
        "// Generated by reference/ink-pages/about-chapters/build_about_chapters.py. Do not edit by\n"
        "// hand: change the script and run it again. The About page's two new chapters (DRAFT for\n"
        "// Mo, November 4, 2026): Codex paintings, the paper divided out so each multiplies onto the\n"
        "// page; the home's bottles are the real approved bottles, only scaled.\n\n"
        "export const plants = {\n"
        f'  src: "/images/about-chapters/{NAMES["plants"]}.webp",\n'
        f"  width: {plants.width},\n"
        f"  height: {plants.height},\n"
        "} as const;\n\n"
        "export const home = {\n"
        f'  src: "/images/about-chapters/{NAMES["home"]}.webp",\n'
        f'  bottles: "/images/about-chapters/{NAMES["bottles"]}.webp",\n'
        f'  front: "/images/about-chapters/{NAMES["front"]}.webp",\n'
        f"  width: {home.width},\n"
        f"  height: {home.height},\n"
        "} as const;\n",
        encoding="utf-8",
        newline="\n",
    )
    print("wrote", ART)


if __name__ == "__main__":
    main()

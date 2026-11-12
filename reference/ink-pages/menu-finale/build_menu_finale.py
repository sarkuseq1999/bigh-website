"""Build the phone menu's closing painting, the hummingbird at a California fuchsia (Mo picked E,
November 3, 2026, part 6 of the homepage's California pass: the crane at rest at the foot of the
phone menu was the last crane on the site; then the bird's beating wings were "annoying, like
flys" at the menu's size, so they rest), into the site's picture:

  public/images/home-v2/ink/menu-hummingbird-v1.webp   the phone and tablet menu's foot

The homepage's own Allen's hummingbird (hummingbird-v2.webp, never redrawn) with its two painted
wings on their first frame, raised as painted (the homepage's rest with reduced motion: the far wing
behind the body, the near wing over it), sipping from Codex's painting of California fuchsia
(originals/menu-fuchsia-1.png, the flower only). The fuchsia's paper is divided out and its coral
calmed a little so the bird leads; the bird is laid in with its bill tip at the lowest flower's
mouth; the picture is trimmed to its paint (white = no paint, so it multiplies onto the menu's
paper). The size the menu's CSS needs is printed (src/components/ink/nav/nav-inscription.module.css,
`.sheetStand`).

usage: python -X utf8 reference/ink-pages/menu-finale/build_menu_finale.py
"""

import json
from pathlib import Path

import numpy as np
from PIL import Image

from shoot_menu import BIRD, OPTIONS, bird_box, calmed, divide_paper

HERE = Path(__file__).parent
ROOT = HERE.parents[2]
INK = ROOT / "public" / "images" / "home-v2" / "ink"
NAME = "menu-hummingbird-v1.webp"
PICK = OPTIONS["e"]
# The opening's wings (src/components/home-v2/look-ink/assets.ts, openingWings.box): their box in
# the bird's frame, in percent; six frames side by side, the first raised as painted.
WINGS = (11.834, 14.174, 53.641, 55.425)  # the homepage's v4 wings (November 12, 2026)
FRAMES = 11  # rest, 8 haze, 2 settle; frame 0 is the rest pose
HEIGHT = 720  # drawn at most 230 CSS px tall: 720 covers a 3x screen


def bird():
    """The homepage's bird at rest: far wing, body, near wing, in its 1600 x 1062 frame."""
    body = Image.open(INK / "hummingbird-v2.webp").convert("RGBA")
    w, h = body.size
    assert (w, h) == (BIRD["w"], BIRD["h"])
    left, top, width, height = (round(v / 100 * s) for v, s in zip(WINGS, (w, h, w, h)))
    frame = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    def wing(side):
        strip = Image.open(INK / f"hummingbird-v4-{side}.webp").convert("RGBA")
        first = strip.crop((0, 0, strip.width // FRAMES, strip.height))
        layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        layer.paste(first.resize((width, height), Image.LANCZOS), (left, top))
        return layer

    frame = Image.alpha_composite(frame, wing("far"))
    frame = Image.alpha_composite(frame, body)
    return Image.alpha_composite(frame, wing("near"))


def main():
    src = Image.open(HERE / "originals" / f"{PICK['take']}.png").convert("RGB")
    paint = calmed(np.ascontiguousarray(divide_paper(np.asarray(src))), *PICK["calm"])
    sheet = Image.fromarray(paint).convert("RGBA")

    # Lay the bird in at its scale, its bill tip at the flower's mouth. Its frame runs past the
    # painting's left edge (only clear paper there), so it goes onto a canvas with room round it.
    (fx, fy, fw, fh), _ = bird_box(PICK["bird"])
    pad = 400
    canvas = Image.new("RGBA", (sheet.width + 2 * pad, sheet.height + 2 * pad), (255, 255, 255, 255))
    canvas.paste(sheet, (pad, pad))
    small = bird().resize((round(fw), round(fh)), Image.LANCZOS)
    canvas.alpha_composite(small, (round(fx) + pad, round(fy) + pad))
    rgb = np.asarray(canvas.convert("RGB"))

    # Trimmed to its paint, as the mockup's was.
    ink = (255 - rgb.min(axis=2)) > 10
    ys, xs = np.where(ink)
    edge = 12
    x0, x1 = max(xs.min() - edge, 0), min(xs.max() + edge, rgb.shape[1])
    y0, y1 = max(ys.min() - edge, 0), min(ys.max() + edge, rgb.shape[0])
    img = Image.fromarray(rgb[y0:y1, x0:x1])
    if img.height > HEIGHT:
        img = img.resize((round(img.width * HEIGHT / img.height), HEIGHT), Image.LANCZOS)
    out = INK / NAME
    img.save(out, "WEBP", quality=88, method=6)
    print(json.dumps({"file": str(out.relative_to(ROOT)), "size": img.size, "bytes": out.stat().st_size}))


if __name__ == "__main__":
    main()

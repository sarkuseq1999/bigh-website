"""Pack the shots Mo is shown into reference/ink-pages/mockups/about-promise/web/ as webp.

    python -X utf8 reference/ink-pages/about-promise/pack_review.py [web-name=shot ...]

Laptop and tablet shots keep their size; phone shots (taken at 2x) come down to 600px wide. Each
idea also gets a close-up strip of its four small paintings on the page's paper (strip-<key>.webp).
With no arguments, PICKS and STRIPS; each argument adds or replaces one shot.
"""

import sys
from pathlib import Path

from PIL import Image, ImageChops

HERE = Path(__file__).resolve().parent
SHOTS = HERE / "plates" / "shots"
IMG = HERE / "plates" / "img"
WEB = HERE.parent / "mockups" / "about-promise" / "web"
# The About page's paper, near enough for a close-up.
PAPER = (241, 236, 224)

# web name -> shot
PICKS = {
    "today-1440": "today-None-desk",
    "today-390": "today-None-phone",
    "a-1440": "a-dots-colour-2-desk",
    "a-390": "a-dots-colour-2-phone",
    "b-1440": "b-wildflowers-2-desk",
    "b-390": "b-wildflowers-2-phone",
    "c-1440": "c-poppy-count-1-desk",
    "c-1440-arrive": "c-poppy-count-1-desk-arrive",
    "c-768": "c-poppy-count-1-tablet",
    "c-390": "c-poppy-count-1-phone",
}

# key -> take whose four pieces make the close-up
STRIPS = {"a": "dots-colour-2", "b": "wildflowers-2", "c": "poppy-count-1"}


def strip(take):
    side = 240
    out = Image.new("RGB", (side * 4, side), PAPER)
    for k in range(4):
        piece = Image.open(IMG / f"{take}-{k + 1}.png").convert("RGB").resize((side, side), Image.LANCZOS)
        out.paste(ImageChops.multiply(Image.new("RGB", (side, side), PAPER), piece), (k * side, 0))
    return out


def main():
    picks = dict(PICKS)
    for arg in sys.argv[1:]:
        name, _, shot = arg.partition("=")
        picks[name] = shot
    WEB.mkdir(parents=True, exist_ok=True)
    for name, shot in picks.items():
        path = SHOTS / f"{shot}.png"
        if not path.exists():
            print("skip (no shot)", name, shot)
            continue
        img = Image.open(path).convert("RGB")
        if name.endswith("-390"):
            img = img.resize((600, round(img.height * 600 / img.width)), Image.LANCZOS)
        img.save(WEB / f"{name}.webp", quality=84, method=6)
        print(name, img.size, (WEB / f"{name}.webp").stat().st_size)
    for key, take in STRIPS.items():
        img = strip(take)
        img.save(WEB / f"strip-{key}.webp", quality=88, method=6)
        print("strip", key, img.size, (WEB / f"strip-{key}.webp").stat().st_size)


main()


# Mo asked to compare B and C (November 12, 2026): the part alone (shoot_parts.py), with a strip of
# its own paper round it, and the films of it arriving (film_compare.py).
def compare():
    for key in ("b", "c"):
        for size in ("desk", "phone"):
            img = Image.open(SHOTS / f"part-{key}-{size}.png").convert("RGB")
            if size == "desk":
                img = img.crop((80, 0, img.width - 80, img.height))
            pad = 28 if size == "desk" else 40
            paper = img.getpixel((4, img.height - 4))
            out = Image.new("RGB", (img.width, img.height + 2 * pad), paper)
            out.paste(img, (0, pad))
            if size == "phone":
                out = out.resize((450, round(out.height * 450 / out.width)), Image.LANCZOS)
            name = f"cmp-{key}-{'1440' if size == 'desk' else '390'}"
            out.save(WEB / f"{name}.webp", quality=86, method=6)
            print(name, out.size, (WEB / f"{name}.webp").stat().st_size)
            film = HERE / "plates" / "films" / f"{key}-{size}.mp4"
            dest = WEB / f"film-{key}-{size}.mp4"
            dest.write_bytes(film.read_bytes())
            print(dest.name, dest.stat().st_size)


compare()


# Mo said "Let's try A" (November 12, 2026): the coloured dots built into the page, shot on the
# built site (shoot_built.py) and filmed arriving (film_built.py).
def built():
    for size in ("1440", "768", "390"):
        img = Image.open(SHOTS / f"built-{size}.png").convert("RGB")
        if size == "390":
            img = img.resize((600, round(img.height * 600 / img.width)), Image.LANCZOS)
        img.save(WEB / f"built-{size}.webp", quality=84, method=6)
        print(f"built-{size}", img.size, (WEB / f"built-{size}.webp").stat().st_size)
    for size in ("desk", "phone"):
        film = HERE / "plates" / "films" / f"built-{size}.mp4"
        dest = WEB / f"film-built-{size}.mp4"
        dest.write_bytes(film.read_bytes())
        print(dest.name, dest.stat().st_size)


built()

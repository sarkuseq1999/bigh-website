"""Pack the shots Mo is shown into reference/ink-pages/mockups/about-closing/web/ as webp.

    python -X utf8 reference/ink-pages/about-closing/pack_review.py [built]

Laptop and tablet shots keep their size; phone shots (taken at 2x) come down to 600px wide. Each
idea also gets a close-up of its painting on the page's paper (art-<key>.webp, 960px wide).
"""

from pathlib import Path

from PIL import Image, ImageChops

HERE = Path(__file__).resolve().parent
SHOTS = HERE / "plates" / "shots"
IMG = HERE / "plates" / "img"
WEB = HERE.parent / "mockups" / "about-closing" / "web"
# The About page's paper, near enough for a close-up.
PAPER = (241, 236, 224)

# key -> take (its shots are <key>-<take>-<size>.png)
IDEAS = {"today": None, "a": "glasses-colour-1", "b": "tidepool-1", "c": "notebook-2"}
SIZES = {"desk": "1440", "tablet": "768", "phone": "390"}


def main():
    WEB.mkdir(parents=True, exist_ok=True)
    for key, take in IDEAS.items():
        for size, name in SIZES.items():
            path = SHOTS / f"{key}-{take}-{size}.png"
            img = Image.open(path).convert("RGB")
            if size == "phone":
                img = img.resize((600, round(img.height * 600 / img.width)), Image.LANCZOS)
            out = WEB / f"{key}-{name}.webp"
            img.save(out, quality=84, method=6)
            print(out.name, img.size, out.stat().st_size)
        art = IMG / f"{take}.png" if take else HERE.parent / "about-bc" / "plates" / "glasses-v1.png"
        piece = Image.open(art).convert("RGB")
        piece = piece.resize((960, round(piece.height * 960 / piece.width)), Image.LANCZOS)
        close = ImageChops.multiply(Image.new("RGB", piece.size, PAPER), piece)
        out = WEB / f"art-{key}.webp"
        close.save(out, quality=88, method=6)
        print(out.name, close.size, out.stat().st_size)



# Mo picked B (November 13, 2026): the tide pool built into the page, shot on the built site
# (shoot_built.py) and filmed arriving (film_built.py).
def built():
    for size in ("1440", "1024", "768", "390"):
        img = Image.open(SHOTS / f"built-{size}.png").convert("RGB")
        if size == "390":
            img = img.resize((600, round(img.height * 600 / img.width)), Image.LANCZOS)
        out = WEB / f"built-{size}.webp"
        img.save(out, quality=84, method=6)
        print(out.name, img.size, out.stat().st_size)
    for size in ("desk", "phone"):
        film = HERE / "plates" / "films" / f"built-{size}.mp4"
        dest = WEB / f"film-built-{size}.mp4"
        dest.write_bytes(film.read_bytes())
        print(dest.name, dest.stat().st_size)


if __name__ == "__main__":
    import sys

    built() if "built" in sys.argv[1:] else main()

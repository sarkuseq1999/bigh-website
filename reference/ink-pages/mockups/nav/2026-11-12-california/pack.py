"""Turn the shots into web pictures for the review page (page/img/)."""

from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
SHOTS = HERE / "shots"
OUT = HERE / "page" / "img"
OUT.mkdir(parents=True, exist_ok=True)

for v in ("today", "a", "b"):
    # The bar close up: the column only, at 2x.
    bar = Image.open(SHOTS / f"{v}-about-bar.png").convert("RGB")
    bar.crop((330, 0, 2742, 300)).save(OUT / f"{v}-bar.webp", quality=88)
    for name, width in (("home", 1600), ("home-settled", 1600), ("about", 1600)):
        im = Image.open(SHOTS / f"{v}-{name}.png").convert("RGB")
        im.resize((width, round(im.height * width / im.width)), Image.LANCZOS).save(
            OUT / f"{v}-{name}.webp", quality=84
        )
    for name in ("phone-home", "phone-menu"):
        im = Image.open(SHOTS / f"{v}-{name}.png").convert("RGB")
        im.resize((780, round(im.height * 780 / im.width)), Image.LANCZOS).save(
            OUT / f"{v}-{name}.webp", quality=84
        )
print(sorted(p.name for p in OUT.iterdir()))

"""Build the two closing paintings Mo is comparing on the live site (November 2, 2026): A Big Sur at
evening and B an evening walk on the ridge, each with the opening's gold-leaf sun on its horizon,
its gold mask (where the leaf is, for the band of light that crosses it), and the pelicans that fly
in where the cranes fly today. The cut is shoot_purpose.py's, the one Mo saw on the mockup page.

    python -X utf8 reference/ink-pages/home-purpose/build_home_purpose.py

Out: public/images/home-v2/ink/purpose-<scene>-v1.webp and purpose-<scene>-gold-v1.webp,
purpose-pelicans-v1.webp; lossless plates in plates/ (git-ignored).
"""

import numpy as np
from PIL import Image, ImageFilter

from shoot_purpose import HERE, cut, cut_birds

SITE = HERE.parents[2] / "public" / "images" / "home-v2" / "ink"
PLATES = HERE / "plates"
SCENES = ["big-sur", "ridge"]
MASK_W = 1000  # the gold masks' width (as the live purpose-gold.webp)
BIRDS_W = 800


def main():
    for scene in SCENES:
        img, mask = cut(scene, with_mask=True)
        img.save(PLATES / f"purpose-{scene}-v1.png", optimize=True)
        img.save(SITE / f"purpose-{scene}-v1.webp", quality=84, method=6)
        alpha = Image.fromarray((mask * 255).astype(np.uint8), "L")
        alpha = alpha.resize((MASK_W, round(MASK_W * img.height / img.width)), Image.LANCZOS)
        alpha = alpha.filter(ImageFilter.GaussianBlur(1.2))
        white = Image.new("L", alpha.size, 255)
        Image.merge("RGBA", (white, white, white, alpha)).save(
            SITE / f"purpose-{scene}-gold-v1.webp", "WEBP", quality=80, method=6
        )
    birds = cut_birds()
    birds = birds.resize((BIRDS_W, round(BIRDS_W * birds.height / birds.width)), Image.LANCZOS)
    birds.save(PLATES / "purpose-pelicans-v1.png", optimize=True)
    birds.save(SITE / "purpose-pelicans-v1.webp", quality=86, method=6)
    for name in SITE.glob("purpose-*-v1.webp"):
        print(name.name, Image.open(name).size, name.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()

"""Build the homepage opening's California pictures (Mo picked them October 28, 2026).

The giant sequoias in the morning (D, with the clearing for the sun) and Anna's hummingbird with
its wings repainted true, from the Codex originals in originals/:

- public/images/home-v2/ink/opening-sequoias-v1.webp: the whole first screen (2400 x 1600), its
  paper divided out to white, so the page multiplies it onto its own rice paper.
- public/images/home-v2/ink/hummingbird-v1.webp: the bird (1600 x 1062, the live crane's frame,
  in which it was painted), its paper turned to transparency.

Lossless plates go to plates/site/ (git-ignored).

    python -X utf8 reference/ink-pages/home-california/build_home_opening.py
"""

from pathlib import Path

import numpy as np
from PIL import Image

from cut_california import divided, to_alpha

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SITE = ROOT / "public" / "images" / "home-v2" / "ink"
PLATES = HERE / "plates" / "site"

LANDSCAPE = ("sequoia-2-clear-1", "opening-sequoias-v1", (2400, 1600))
BIRD = ("hummingbird-wings-1", "hummingbird-v1", (1600, 1062))


def save(img, name):
    img.save(PLATES / f"{name}.png", optimize=True)
    img.save(SITE / f"{name}.webp", quality=88, method=6)
    print(name, img.size, img.mode, f"{(SITE / f'{name}.webp').stat().st_size // 1024} KB")


def main():
    PLATES.mkdir(parents=True, exist_ok=True)
    take, name, size = LANDSCAPE
    land = divided(Image.open(HERE / "originals" / f"{take}.png"), top=True)
    save(Image.fromarray(land.astype(np.uint8), "RGB").resize(size, Image.LANCZOS), name)

    take, name, size = BIRD
    bird = divided(Image.open(HERE / "originals" / f"{take}.png"))
    bird = np.asarray(Image.fromarray(bird.astype(np.uint8), "RGB").resize(size, Image.LANCZOS)).astype(np.float32)
    save(to_alpha(bird), name)


if __name__ == "__main__":
    main()

"""Build the homepage opening's California pictures (Mo picked them October 28, 2026).

The giant sequoias in the morning (D, with the clearing for the sun) and Anna's hummingbird with
its wings repainted true, from the Codex originals in originals/:

- public/images/home-v2/ink/opening-sequoias-v1.webp: the whole first screen (2400 x 1600), its
  paper divided out to white, so the page multiplies it onto its own rice paper.
- public/images/home-v2/ink/hummingbird-v2.webp and hummingbird-v2-near.webp, -far.webp (October
  29, Mo picked C): Allen's hummingbird painted in a few wet washes, its beak one dry stroke,
  its wings always beating (build_wings.py, look "allens-few"). The body without its wings, in
  the live crane's frame (1600 x 1062), and each wing's six frames side by side; the page lays
  the far wing behind the body and the near wing over it, in the box build_wings.py prints.
  (hummingbird-v1, Anna's hummingbird as a still, was live from October 28.)

Lossless plates go to plates/site/ (git-ignored).

    python -X utf8 reference/ink-pages/home-california/build_home_opening.py
"""

from pathlib import Path

import numpy as np
from PIL import Image

import build_wings
from cut_california import divided

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SITE = ROOT / "public" / "images" / "home-v2" / "ink"
PLATES = HERE / "plates" / "site"

LANDSCAPE = ("sequoia-2-clear-1", "opening-sequoias-v1", (2400, 1600))
BIRD = ("allens-few", "hummingbird-v2", (1600, 1062))


def save(img, name):
    img.save(PLATES / f"{name}.png", optimize=True)
    img.save(SITE / f"{name}.webp", quality=88, method=6)
    print(name, img.size, img.mode, f"{(SITE / f'{name}.webp').stat().st_size // 1024} KB")


def main():
    PLATES.mkdir(parents=True, exist_ok=True)
    take, name, size = LANDSCAPE
    land = divided(Image.open(HERE / "originals" / f"{take}.png"), top=True)
    save(Image.fromarray(land.astype(np.uint8), "RGB").resize(size, Image.LANCZOS), name)

    look, name, size = BIRD
    build_wings.build(look)
    made = build_wings.OUT / look
    save(Image.open(made / "body.png").resize(size, Image.LANCZOS), name)
    for side in ("near", "far"):
        save(Image.open(made / f"{side}.png"), f"{name}-{side}")


if __name__ == "__main__":
    main()

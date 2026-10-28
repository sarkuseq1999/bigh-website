"""Build the About opening's painting for the site: the poppy meadow, its end painted into the paper
(Mo, October 28, 2026).

Mo compared A (the superbloom) and B (the morning walk) on the live site (October 27) and picked
A, but found that its first screen and the next part (Our purpose) "don't transition well": the
painting stopped in a straight line with its biggest poppies on it. Of two painted ends he picked
A, "the meadow thins out": Codex continued the painting's foot (join_foot.py,
originals/superbloom-foot-thin2.png) so the poppies grow fewer and smaller, then a few last ones
and dry grass, then bare paper.

The painting ships as two webps with its paper turned to transparency (cut_mockups.divided and
to_alpha), so it lies on the page's own paper with no box and no blend mode:

- superbloom-v2.webp, the painting with its gold taken down to a pale grey ghost (GHOST of its
  ink);
- superbloom-gold-v2.webp, only the gold, which the page lets in over it: the poppies bloom out
  from the old foot (src/components/about/scene.module.css).

Gold is told by colour: a pixel's chroma (its brightest channel less its darkest, on the
paper-divided picture), from none at CHROMA[0] to all at CHROMA[1]. The dry grass and the warm
sky wash stay under CHROMA[0]. The joined painting is cut EASE rows under its last painted row and
eased out over those rows (bare paper already): no feather over the painting itself.

    python -X utf8 reference/ink-pages/about-opening/build_about_opening.py [repo]

Writes public/images/about-opening/ and prints the sizes scene-art.ts and scene.module.css carry.
"""

import sys
from pathlib import Path

from PIL import Image

from join_foot import joined, layers, painted_to

HERE = Path(__file__).resolve().parent
FOOT = "superbloom-foot-thin2"
V = "v2"
EASE = 48


def main():
    repo = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parents[2]
    out = repo / "public" / "images" / "about-opening"
    out.mkdir(parents=True, exist_ok=True)
    whole = joined(FOOT)
    base, _ = layers(whole, ease=0)
    end = painted_to(base) + EASE
    whole = whole.crop((0, 0, whole.width, end))
    base, top = layers(whole, ease=EASE / end)
    for arr, name in ((base, f"superbloom-{V}"), (top, f"superbloom-gold-{V}")):
        img = Image.fromarray(arr.clip(0, 255).astype("uint8"), "RGBA")
        path = out / f"{name}.webp"
        img.save(path, quality=84, method=6)
        print(f"{path.name}: {img.width}x{img.height}, {path.stat().st_size // 1024} KB")
    print(f"  the old foot at row 1024 of {end} ({1024 / end:.4f}); painted down to row {end - EASE}")


if __name__ == "__main__":
    main()

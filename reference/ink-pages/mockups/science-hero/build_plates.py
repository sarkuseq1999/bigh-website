"""Working pictures for the Science hero mockups: each Codex original with its paper divided out.

  python -X utf8 reference/ink-pages/mockups/science-hero/build_plates.py [name ...]

Reads reference/ink-pages/science/originals/hero-<name>.png and writes
reference/ink-pages/science/plates/hero/<name>.webp (git-ignored), ready to multiply onto the
page's own paper like the site's paintings. With no names, every hero-*.png is built.
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
SCIENCE = HERE.parent.parent / "science"
ORIG = SCIENCE / "originals"
OUT = SCIENCE / "plates" / "hero"
OUT.mkdir(parents=True, exist_ok=True)


def plate(src: Path, dst: Path) -> None:
    a = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
    # The paper: the median of the brightest tenth of the picture.
    lum = a.mean(axis=2)
    paper = np.median(a[lum >= np.quantile(lum, 0.9)], axis=0)
    a = np.clip(a / paper * 255.0 * 1.04, 0, 255).astype(np.uint8)
    Image.fromarray(a).save(dst, "WEBP", quality=88, method=6)


names = sys.argv[1:] or [p.stem.removeprefix("hero-") for p in sorted(ORIG.glob("hero-*.png"))]
for name in names:
    plate(ORIG / f"hero-{name}.png", OUT / f"{name}.webp")
    print("plate", name)

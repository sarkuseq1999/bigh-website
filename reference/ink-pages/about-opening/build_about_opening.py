"""Build the About opening's two test paintings for the site (Mo, October 27, 2026).

Mo asked to compare A (the poppy superbloom) and B (the morning walk) on the live site. Each
painting ships as two webps with its paper turned to transparency (cut_mockups.divided and
to_alpha) and its foot feathered out over its last FEATHER, so they lie on the page's own paper
with no box and no blend mode:

- <name>-v1.webp, the painting with its gold taken down to a pale grey ghost (GHOST of its ink);
- <name>-gold-v1.webp, only the gold, which the page lets in over it: the poppies bloom (A), the
  morning sun reaches the ridge (B). Everything that is not gold is in the first picture alone,
  so nothing else changes while the gold comes in (src/components/about/scene.module.css).

Gold is told by colour: a pixel's chroma (its brightest channel less its darkest, on the
paper-divided picture), from none at CHROMA[0] to all at CHROMA[1]. The dry grass and the warm
sky wash stay under CHROMA[0].

    python -X utf8 reference/ink-pages/about-opening/build_about_opening.py [repo]

Writes public/images/about-opening/ and prints the sizes scene-art.ts carries.
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image

from cut_mockups import divided, to_alpha

HERE = Path(__file__).resolve().parent
TAKES = {"superbloom": "superbloom-a1", "walk": "walk-b1"}
V = "v1"
FEATHER = 0.14
CHROMA = (34.0, 80.0)
GHOST = 0.4


def smoothstep(x, lo, hi):
    t = np.clip((x - lo) / (hi - lo), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def foot(h):
    """1 down the picture, easing to 0 over its last FEATHER."""
    n = round(h * FEATHER)
    ramp = np.ones(h, dtype=np.float32)
    ramp[h - n :] = smoothstep(np.linspace(1.0, 0.0, n, dtype=np.float32), 0.0, 1.0)
    return ramp[:, None]


def rgba(arr):
    return Image.fromarray(arr.clip(0, 255).astype(np.uint8), "RGBA")


def layers(take):
    flat = divided(Image.open(HERE / "originals" / f"{take}.png"), top=True)
    gold = smoothstep(flat.max(axis=2) - flat.min(axis=2), *CHROMA)[..., None]
    grey = flat.mean(axis=2, keepdims=True).repeat(3, axis=2)
    # The ghost: where it is gold, the grey of the same strokes, its ink cut to GHOST.
    ghost = 255.0 - (255.0 - grey) * GHOST
    base = np.asarray(to_alpha(flat * (1 - gold) + ghost * gold)).astype(np.float32)
    top = np.asarray(to_alpha(flat)).astype(np.float32)
    ramp = foot(flat.shape[0])
    base[..., 3] *= ramp[:, :]
    top[..., 3] *= (gold[..., 0] * ramp[:, 0][:, None])
    return rgba(base), rgba(top), float(gold.mean())


def main():
    repo = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parents[2]
    out = repo / "public" / "images" / "about-opening"
    out.mkdir(parents=True, exist_ok=True)
    for name, take in TAKES.items():
        base, top, share = layers(take)
        for img, path in ((base, out / f"{name}-{V}.webp"), (top, out / f"{name}-gold-{V}.webp")):
            img.save(path, quality=84, method=6)
            print(f"{path.name}: {img.width}x{img.height}, {path.stat().st_size // 1024} KB")
        print(f"  {name}: gold covers {share:.1%} of the picture")


if __name__ == "__main__":
    main()

"""Build the footer's closing painting, the California quail by the park sign (Mo picked A1,
November 3, 2026: the red-crowned crane there read as Chinese; of a quail, a desert tortoise and a
black bear cub he picked the quail, then A1 of the quail painted two looser ways), from Codex's
painting originals/quail-wash-2.png into the site's picture:

  public/images/home-v2/ink/quail-sign-v1.webp   every page, the homepage too

Two quail, the state bird, in a few wet washes in the homepage hummingbird's hand: the one behind
keeps watch, the one in front bends toward the sign's poppy. It is painted in its own thin colour,
so unlike the crane it has no "green spring" twin. The paper is divided out (white = no paint, so
the picture multiplies onto the footer's paper), the picture is trimmed to its paint, and the
measurements the footer's CSS places it by are printed (src/components/ink/ink.module.css,
`.look .rest`).

usage: python -X utf8 reference/ink-pages/footer-crane/build_footer_quail.py
"""

import json
from pathlib import Path

import numpy as np
from PIL import Image

from cut_cranes import divide_paper

HERE = Path(__file__).parent
ROOT = HERE.parents[2]
INK = ROOT / "public" / "images" / "home-v2" / "ink"
NAME = "quail-sign-v1.webp"
TAKE = "quail-wash-2"
# Read off the painting: where the birds meet the ground (the point the CSS stands on the sign's
# ground) and the top of the watching bird's plume.
FEET = (620, 800)
TOP = 100
WIDTH = 800  # drawn at most about 200 CSS px wide: 800 covers a 3x screen


def main():
    src = Image.open(HERE / "originals" / f"{TAKE}.png").convert("RGB")
    c = divide_paper(np.asarray(src))
    ink = (255 - c.min(axis=2)) > 10
    ys, xs = np.where(ink)
    pad = 12
    x0, x1 = int(max(xs.min() - pad, 0)), int(min(xs.max() + pad, c.shape[1]))
    y0, y1 = int(max(ys.min() - pad, 0)), int(min(ys.max() + pad, c.shape[0]))
    w, h = x1 - x0, y1 - y0
    size = (WIDTH, round(WIDTH * h / w))
    out = INK / NAME
    img = Image.fromarray(c[y0:y1, x0:x1]).resize(size, Image.LANCZOS)
    img.save(out, "WEBP", quality=88, method=6)
    print("saved", out.relative_to(ROOT), img.size, out.stat().st_size, "bytes")

    feet_x, feet_y, top = FEET[0] - x0, FEET[1] - y0, TOP - y0
    tall = feet_y - top
    print(f"picture {w} x {h}; feet ({feet_x}, {feet_y}); feet to plume {tall}")
    print(f"  height / tall = {h / tall:.4f}, width / tall = {w / tall:.4f}")
    print(f"  feet from the left = {feet_x / tall:.4f} tall, below the feet = {(h - feet_y) / tall:.4f} tall")

    prompt = (HERE / "prompts" / f"{TAKE}.txt").read_text(encoding="utf-8")
    meta = {
        "prompt": prompt,
        "createdAt": "2026-11-03",
        "model": "Codex built-in image generation (ChatGPT plan)",
        "original": f"reference/ink-pages/footer-crane/originals/{TAKE}.png",
        "refs": ["reference/ink-pages/home-california/originals/allens-few-1.png"],
    }
    (INK / f"{NAME}.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()

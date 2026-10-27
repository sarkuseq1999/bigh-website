"""Build the footer's closing crane (Mo picked C, October 26, 2026: the crane bends toward the
park sign's poppy) from Codex's painting originals/crane-sign-c1.png into the site's pictures:

  public/images/home-v2/ink/crane-poppy-v1.webp          gold crown, every page but the homepage
  public/images/home-v2/ink/spring/crane-poppy-v1.webp   red crown, the homepage's "green spring"

The paper is divided out (white = no paint, so the picture multiplies onto the footer's paper), the
picture is trimmed to its paint, and the measurements the footer's CSS places it by are printed
(src/components/ink/ink.module.css, `.look .rest`).

usage: python -X utf8 reference/ink-pages/footer-crane/build_footer_crane.py
"""

import json
from pathlib import Path

import numpy as np
from PIL import Image

from cut_cranes import TAKES, divide_paper, spring

HERE = Path(__file__).parent
ROOT = HERE.parents[2]
INK = ROOT / "public" / "images" / "home-v2" / "ink"
NAME = "crane-poppy-v1.webp"
TAKE = "c1"
WIDTH = 800  # drawn at most about 245 CSS px wide: 800 covers a 3x screen


def main():
    info = TAKES[TAKE]
    src = Image.open(HERE / "originals" / f"crane-sign-{TAKE}.png").convert("RGB")
    c = divide_paper(np.asarray(src))
    ink = (255 - c.min(axis=2)) > 10
    ys, xs = np.where(ink)
    pad = 12
    x0, x1 = int(max(xs.min() - pad, 0)), int(min(xs.max() + pad, c.shape[1]))
    y0, y1 = int(max(ys.min() - pad, 0)), int(min(ys.max() + pad, c.shape[0]))
    w, h = x1 - x0, y1 - y0
    size = (WIDTH, round(WIDTH * h / w))
    for out, pixels in [(INK / NAME, c), (INK / "spring" / NAME, spring(c, info["crown"]))]:
        img = Image.fromarray(pixels[y0:y1, x0:x1]).resize(size, Image.LANCZOS)
        img.save(out, "WEBP", quality=88, method=6)
        print("saved", out.relative_to(ROOT), img.size, out.stat().st_size, "bytes")

    fx, fy = info["feet"]
    feet_x, feet_y, top = fx - x0, fy - y0, info["top"] - y0
    tall = feet_y - top
    print(f"picture {w} x {h}; feet ({feet_x}, {feet_y}); feet to crown {tall}")
    print(f"  height / tall = {h / tall:.4f}, width / tall = {w / tall:.4f}")
    print(f"  feet from the left = {feet_x / tall:.4f} tall, below the feet = {(h - feet_y) / tall:.4f} tall")

    prompt = (HERE / "prompts" / f"crane-sign-{TAKE}.txt").read_text(encoding="utf-8")
    meta = {
        "prompt": prompt,
        "createdAt": "2026-10-26",
        "model": "Codex built-in image generation (ChatGPT plan)",
        "original": f"reference/ink-pages/footer-crane/originals/crane-sign-{TAKE}.png",
        "refs": [
            "reference/home-v2/ink/originals/gpt25-crane-rest-v2.png",
            "reference/ink-pages/fda-sign/originals/sign-park-full-c5.png",
        ],
    }
    (INK / f"{NAME}.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()

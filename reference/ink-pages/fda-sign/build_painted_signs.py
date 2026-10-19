"""Cut the two painted trail signs Mo is comparing (October 19, 2026) into the site's pictures:

- A, the ink-wash sign (originals/sign-ink-wash-a1.png) -> Advanced OPC's footer,
  public/images/products/advanced-opc/ink/fda-sign-ink-wash-v1.webp
- C, the brushstroke sign (originals/sign-brushstroke-c1.png) -> Green Bee Propolis's footer,
  public/images/products/green-bee-propolis/ink/fda-sign-brushstroke-v1.webp

Both were painted by Codex (prompts/sign-*.txt). The paper becomes transparent: the paint is
un-multiplied from the paper, so over the site's paper it looks exactly as painted. Faint
unevenness in the generated paper is dropped (it would show as a pale box), and the cut edges fade
out (except along the board's own rows, so its ends stay whole).

The pictures are scaled so the footer's --k (0.48 on a computer) gives 0.40 CSS px per painting
px. Prints the 9-slice numbers for the pages' CSS (in the webp's pixels).

usage: python -X utf8 reference/ink-pages/fda-sign/build_painted_signs.py
"""

from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).parent
REPO = HERE.parents[2]
SCALE = 0.40 / 0.48

SIGNS = [
    {
        "src": "sign-ink-wash-a1.png",
        "out": REPO / "public/images/products/advanced-opc/ink/fda-sign-ink-wash-v1.webp",
        "crop": (0, 250, 1536, 860),  # posts' tops to the end of the grass
        "board_rows": (90, 305),  # in the crop: the board, never faded at the sides
        "fade": (160, 160, 0, 110),  # left, right, top, bottom
        "slice": (115, 376, 325, 380),  # top, right, bottom, left: only the board's middle stretches
        "reach": (180, 190),  # how far the words may run past the posts into the board's ends
    },
    {
        "src": "sign-brushstroke-c1.png",
        "out": REPO / "public/images/products/green-bee-propolis/ink/fda-sign-brushstroke-v1.webp",
        "crop": (60, 250, 1500, 880),
        "board_rows": (85, 310),
        "fade": (80, 60, 0, 80),
        "slice": (104, 366, 342, 340),
        "reach": (180, 166),
    },
]


def cutout(rgb, floor=0.045):
    a = rgb.astype(float)
    paper = np.percentile(a[:40].reshape(-1, 3), 60, axis=0)
    c = np.clip(a / paper * 255.0, 0, 255)
    alpha = 1.0 - c.min(axis=2) / 255.0
    colour = np.clip((c - 255.0 * (1.0 - alpha[..., None])) / np.maximum(alpha, 1e-3)[..., None], 0, 255)
    return colour, np.clip((alpha - floor) / (1 - floor), 0, 1)


def build(s):
    colour, alpha = cutout(np.asarray(Image.open(HERE / "originals" / s["src"]).convert("RGB")))
    x0, y0, x1, y1 = s["crop"]
    colour, alpha = colour[y0:y1, x0:x1], alpha[y0:y1, x0:x1].copy()
    h, w = alpha.shape
    left, right, top, bottom = s["fade"]
    rows = np.ones(h, bool)
    rows[s["board_rows"][0]:s["board_rows"][1]] = False
    if left:
        alpha[rows, :left] *= np.linspace(0, 1, left)[None, :] ** 1.5
    if right:
        alpha[rows, w - right:] *= np.linspace(1, 0, right)[None, :] ** 1.5
    if top:
        alpha[:top] *= (np.linspace(0, 1, top) ** 1.5)[:, None]
    if bottom:
        alpha[h - bottom:] *= (np.linspace(1, 0, bottom) ** 1.5)[:, None]
    img = Image.fromarray(np.dstack([colour, alpha * 255.0]).astype("uint8"), "RGBA")
    img = img.resize((round(w * SCALE), round(h * SCALE)), Image.LANCZOS)
    img.save(s["out"], "WEBP", quality=72, alpha_quality=70, method=6)
    t, r, b, l = (round(v * SCALE) for v in s["slice"])
    rl, rr = (round(v * SCALE) for v in s["reach"])
    print(f"{s['out'].name}: {img.width} x {img.height}, {s['out'].stat().st_size // 1024} KB")
    print(f"  slice (top right bottom left): {t} {r} {b} {l}; reach (left right): {rl} {rr}")


if __name__ == "__main__":
    for sign in SIGNS:
        build(sign)

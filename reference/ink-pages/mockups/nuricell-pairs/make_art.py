"""Paintings for the NuriCell pairs ideas page: the paper divided out (so they multiply onto the page
like the site's paintings) and sized for the page, as webp in art/. Also today's section, cut from a
screenshot of the live page, for the comparison at the top. The originals of the ideas Mo did not
pick (A, C) are in bigh-archive/nuricell-pairs-2026-10-27/ beside this repository: copy them back
into reference/ink-pages/nuricell-pairs/originals/ to run this again.

usage: python -X utf8 make_art.py [today-screenshot.webp]
"""

import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).parent
SRC = HERE.parent.parent / "nuricell-pairs" / "originals"
ART = HERE / "art"
ART.mkdir(exist_ok=True)

PICKS = {
    "hands-fuel": 900,
    "hands-store-v2": 900,
    "hands-join": 900,
    "ranch-stove": 900,
    "ranch-windmill-v2": 900,
    "ranch-rider": 900,
    "trail-map": 1600,
}


def divide_paper(im: Image.Image) -> Image.Image:
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    h, w, _ = a.shape
    edge = np.concatenate([a[: h // 20].reshape(-1, 3), a[-h // 20 :].reshape(-1, 3),
                           a[:, : w // 20].reshape(-1, 3), a[:, -w // 20 :].reshape(-1, 3)])
    paper = np.median(edge, axis=0)
    out = np.clip(a / paper * 255.0, 0, 255).astype(np.uint8)
    return Image.fromarray(out)


for name, width in PICKS.items():
    src = SRC / f"{name}.png"
    if not src.exists():
        print("missing", name)
        continue
    im = divide_paper(Image.open(src))
    if name == "trail-map":
        im = im.crop((0, 150, 1672, 860))  # the empty paper above and below the hills
    im = im.resize((width, round(width * im.height / im.width)), Image.LANCZOS)
    im.save(ART / f"{name}.webp", quality=86)
    print(name, im.size)

paper = HERE.parent / "nuricell-inside" / "art" / "paper.webp"
shutil.copy(paper, ART / "paper.webp")

if len(sys.argv) > 1:
    today = Image.open(sys.argv[1]).convert("RGB")
    # The three scenes of the 1440 x 900 screenshot, from their pictures to their titles.
    today.crop((100, 190, 1340, 520)).save(ART / "today.webp", quality=86)
    print("today", today.size)

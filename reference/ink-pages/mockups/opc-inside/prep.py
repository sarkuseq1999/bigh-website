"""Pictures for the Advanced OPC "What's inside" mockups (November 17, 2026).

The live chapter's painting is six plants in grey ink with a little colour (October 16), painted as
an East Asian ink painting. Two ideas in the grapes chapter's California colour and hand:

  A  six: the same six plants (grapes, pine bark, bilberries, tea, an orange slice, a marigold).
  B  nine: all nine plant sources, as the page says "Nine plant extracts" (grapes for red wine,
     grape seeds, pine bark, bilberries, the three teas, an orange slice, noni, a marigold, sweet
     clover).

Mo picked B (take nine-ah); the other three takes are now in
codes/bigh-archive/opc-inside-unused-2026-11-17/.

Each take is divided (paper to white), cropped to its ink and set on the live picture's shape
(1100 x 1151), so the mock can serve it in place of the live row.

usage: python -X utf8 prep.py
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "reference/ink-pages/about"))
import build_about as bd  # noqa: E402

ORIG = REPO / "reference/ink-pages/opc/originals"
ART = HERE / "art"
ART.mkdir(exist_ok=True)
W, H = 1100, 1151

for take in ["inside-color-ah", "inside-color-bh", "inside-nine-ah", "inside-nine-bh"]:
    img = bd.divided(Image.open(ORIG / f"{take}.png").convert("RGB"))
    x0, y0, x1, y1 = bd.ink_box(np.asarray(img), pad=0.04)
    w, h = x1 - x0, y1 - y0
    if w / h < W / H:
        nw = round(h * W / H)
        x0 -= (nw - w) // 2
        x1 = x0 + nw
    else:
        nh = round(w * H / W)
        y0 -= (nh - h) // 2
        y1 = y0 + nh
    canvas = Image.new("RGB", (x1 - x0, y1 - y0), (255, 255, 255))
    canvas.paste(img.crop((max(x0, 0), max(y0, 0), min(x1, img.width), min(y1, img.height))), (max(-x0, 0), max(-y0, 0)))
    bd.feathered(bd.levelled(canvas.resize((W, H), Image.LANCZOS)), 0.03).save(ART / f"{take}.png")
    print(take, "ok")

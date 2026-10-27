"""The Questions' month painting with only the first <days> ticks, for idea E's "while you scroll" frame.

usage: python -X utf8 prep_ideas.py <repo> <out.png> <days>
The grid was read off q-month-v1.webp (1200 x 800): six columns, five rows.
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

repo, out, days = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
img = np.asarray(Image.open(repo / "public/images/products/nuricell/ink/q-month-v1.webp").convert("RGB")).copy()

COLS = [290, 400, 510, 620, 725, 835, 945]
ROWS = [160, 265, 375, 485, 600, 705]
M = 9  # keep clear of the ruled lines
PAPER = int(np.median(img[620:690, 300:315]))  # the bare paper inside a square (253)

for k in range(days, 30):
    r, c = divmod(k, 6)
    x0, x1 = COLS[c] + M, COLS[c + 1] - M
    y0, y1 = ROWS[r] + M, ROWS[r + 1] - M
    if k == 29:  # the bottom row's last ruled line leans right, to about x 848
        x0 = COLS[c] + 24
    box = img[y0:y1, x0:x1]
    box[:] = np.maximum(box, PAPER)
    if k == 29:  # the last, black tick runs past its square's top right: lift only its black, not the paler ruled lines
        out_box = img[y0 - 20 : y1, x0 : x1 + 26]
        black = out_box.min(axis=2) < 125
        black = np.asarray(Image.fromarray(black.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(5))) > 0
        out_box[black] = PAPER

Image.fromarray(img).save(out)
print(out)

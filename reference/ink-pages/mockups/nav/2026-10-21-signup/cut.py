"""Cut each Codex stroke into an ink mask (as reference/nav/make_signed_strokes.py does) and preview
them side by side on paper.

usage: python -X utf8 cut.py [name ...]
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).parent
OUT = HERE / "cut"
OUT.mkdir(exist_ok=True)
INK = (12, 11, 10)
PAPER = (248, 243, 234)


def alpha_of(grey):
    paper = np.percentile(grey, 60)
    dark = grey[grey < 120]
    core = np.percentile(dark, 20) if dark.size else 0.0
    a = np.clip((paper - 4 - grey) / (paper - 4 - core), 0, 1)
    a[a < 0.03] = 0
    return a


def trim(a, pad=4):
    rows = np.where(a.max(1) > 0.03)[0]
    cols = np.where(a.max(0) > 0.03)[0]
    return a[max(0, rows.min() - pad) : rows.max() + 1 + pad, max(0, cols.min() - pad) : cols.max() + 1 + pad]


names = sys.argv[1:] or [p.name for p in sorted(HERE.iterdir()) if (p / "stroke.png").exists()]
previews = []
for name in names:
    src = HERE / name / "stroke.png"
    if not src.exists():
        print(name, "missing")
        continue
    a = trim(alpha_of(np.asarray(Image.open(src).convert("L")).astype(np.float64)))
    img = Image.fromarray((a * 255).round().astype(np.uint8), "L")
    img = img.resize((640, round(640 * img.size[1] / img.size[0])), Image.LANCZOS)
    rgba = Image.merge("RGBA", (Image.new("L", img.size, INK[0]),) * 3 + (img,))
    rgba.save(OUT / f"{name}.webp", lossless=True, method=6)
    print(name, img.size, f"aspect {img.size[0] / img.size[1]:.2f}")
    pv = Image.new("RGB", (img.width + 40, img.height + 40), PAPER)
    pv.paste(Image.new("RGB", img.size, INK), (20, 20), img)
    previews.append(pv)
if previews:
    sheet = Image.new("RGB", (max(p.width for p in previews), sum(p.height for p in previews)), PAPER)
    y = 0
    for p in previews:
        sheet.paste(p, (0, y))
        y += p.height
    sheet.save(OUT / "sheet.png")

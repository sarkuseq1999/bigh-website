"""Fit a Codex original (1536x1024, white paper) to the science stage's 4:3 frame for a mockup.

Usage: python -X utf8 prep.py <name> [scale]
Reads reference/ink-pages/home-science/originals/<name>.png, writes art/<name>.jpg (1448x1086,
white paper kept: the stage multiplies onto the page, so white vanishes). `scale` enlarges the
painting inside the frame (1.0 = whole width), cropping bare paper at its sides.
"""
import sys
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
SRC = HERE.parents[1] / "home-science" / "originals"
OUT = HERE / "art"
OUT.mkdir(exist_ok=True)
name = sys.argv[1]
scale = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
W, H = 1448, 1086
img = Image.open(SRC / f"{name}.png").convert("RGB")
# A little more body, so thin washes hold on the page's paper (white stays white).
DEEPEN = float(sys.argv[3]) if len(sys.argv) > 3 else 1.2
img = img.point(lambda v: round(255 * (v / 255) ** DEEPEN))
w = round(W * scale)
h = round(img.height * w / img.width)
img = img.resize((w, h), Image.LANCZOS)
canvas = Image.new("RGB", (W, H), "white")
canvas.paste(img, ((W - w) // 2, (H - h) // 2))
canvas.save(OUT / f"{name}.jpg", quality=92)
print(OUT / f"{name}.jpg", canvas.size)

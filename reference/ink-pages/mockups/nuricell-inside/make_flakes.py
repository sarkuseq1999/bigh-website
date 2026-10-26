"""Cut the gold leaf out of NuriCell's shipped capsule painting so each flake can move on its own
(mockup only, October 26, 2026). The painting ships with its paper divided out (white = paper), so
the flakes come out as clean RGBA sprites (un-multiplied from white) and the painting without them
keeps only the ink: the two capsule halves and the four heaps.

usage: python -X utf8 make_flakes.py
writes art/capsule-ink.webp, art/flakes/f<NN>.webp, art/flakes.json, art/check.png
"""

import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

HERE = Path(__file__).parent
REPO = HERE.parents[3]
SRC = REPO / "public/images/products/nuricell/ink/capsule-v1.webp"
OUT = HERE / "art"
(OUT / "flakes").mkdir(parents=True, exist_ok=True)

img = np.asarray(Image.open(SRC).convert("RGB")).astype(np.float32)
H, W = img.shape[:2]
hsv = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float32)
hue, sat, val = hsv[..., 0] * 2, hsv[..., 1] / 255, hsv[..., 2] / 255

# Gold: warm with real colour (chroma, not HSV saturation, which jumps on dark ink), and only in
# the band the leaf rises through (the capsule halves' dark rims are faintly warm too).
chroma = img.max(axis=2) - img.min(axis=2)
warm = (hue > 15) & (hue < 62)
band = np.zeros((H, W), bool)
band[:, int(W * 0.24) : int(W * 0.76)] = True
soft = np.clip((chroma - 22) / 40, 0, 1) * warm * band
core = (soft > 0.5).astype(np.uint8)
core = cv2.morphologyEx(core, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
# Fill holes inside each flake (pale highlights read as low saturation).
filled = core.copy()
cnts, _ = cv2.findContours(core, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(filled, cnts, -1, 1, thickness=-1)
alpha = np.maximum(soft, cv2.erode(filled, np.ones((2, 2), np.uint8)).astype(np.float32))

# The painting without its gold: every gold pixel (and a 2px ring) back to paper.
region = cv2.dilate(((alpha > 0.04) * 255).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
ink = img.copy()
ink[region] = 255
Image.fromarray(ink.astype(np.uint8)).save(OUT / "capsule-ink.webp", quality=92)

# Each flake: a connected piece of the gold, un-multiplied from white so it sits on any paper.
n, lab, stats, cents = cv2.connectedComponentsWithStats((alpha > 0.2).astype(np.uint8), 8)
flakes = []
pad = 3
for i in range(1, n):
    x, y, w, h, area = stats[i]
    if area < 5:
        continue
    x0, y0 = max(0, x - pad), max(0, y - pad)
    x1, y1 = min(W, x + w + pad), min(H, y + h + pad)
    own = cv2.dilate((lab[y0:y1, x0:x1] == i).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    a = alpha[y0:y1, x0:x1] * own
    c = img[y0:y1, x0:x1]
    safe = np.maximum(a, 0.06)[..., None]
    rgb = np.clip(255 - (255 - c) / safe, 0, 255)
    rgba = np.dstack([rgb, a * 255]).astype(np.uint8)
    name = f"f{len(flakes):02d}.webp"
    Image.fromarray(rgba, "RGBA").save(OUT / "flakes" / name, lossless=True)
    flakes.append(
        {
            "f": name,
            # left, top, width, height as fractions of the painting
            "x": round(x0 / W, 5),
            "y": round(y0 / H, 5),
            "w": round((x1 - x0) / W, 5),
            "h": round((y1 - y0) / H, 5),
            "a": int(area),
        }
    )

# Biggest first, so the page can give the large leaves the slow, heavy motion.
order = sorted(range(len(flakes)), key=lambda k: -flakes[k]["a"])
(OUT / "flakes.json").write_text(
    json.dumps({"w": W, "h": H, "flakes": [flakes[k] for k in order]}, indent=0),
    encoding="utf-8",
    newline="\n",
)

# Check: the ink layer with every flake put back, on the site's paper, beside the original.
paper = Image.open(REPO / "public/images/home-v2/ink/paper.webp").convert("RGB").resize((W, W))
paper = np.asarray(paper.crop((0, 0, W, H))).astype(np.float32)
orig = paper * img / 255
back = paper * ink / 255
for fl in flakes:
    s = np.asarray(Image.open(OUT / "flakes" / fl["f"])).astype(np.float32)
    x0, y0 = round(fl["x"] * W), round(fl["y"] * H)
    hh, ww = s.shape[:2]
    a = s[..., 3:] / 255
    back[y0 : y0 + hh, x0 : x0 + ww] = back[y0 : y0 + hh, x0 : x0 + ww] * (1 - a) + s[..., :3] * a
diff = np.abs(orig - back).mean()
Image.fromarray(np.hstack([orig, back]).astype(np.uint8)).save(OUT / "check.png")
print(f"{len(flakes)} flakes, ink layer {W}x{H}, mean difference when put back {diff:.2f}/255")

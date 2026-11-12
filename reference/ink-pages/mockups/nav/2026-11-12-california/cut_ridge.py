"""Cut a Codex ridge painting (paint on white) into a transparent strip for the menu bar's foot.

    python -X utf8 cut_ridge.py <in.png> <out.png> [squash] [taper_px]

Paper is divided out (alpha = how far the darkest channel is from white; colour unmultiplied), the
strip is cropped to the painted band, optionally squashed vertically, and its two ends tapered into
the paper. Prints the crop's size and where the ridge's valleys sit (as a fraction of its height),
so the page can stand that line on the bar's foot.
"""

import sys

import numpy as np
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
squash = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
taper = int(sys.argv[4]) if len(sys.argv) > 4 else 160

a = np.asarray(Image.open(src).convert("RGB"), dtype=np.float64) / 255
# Paper is not pure white in a generated picture: take the page's own white as 1.
white = np.percentile(a.reshape(-1, 3), 90, axis=0)
a = np.clip(a / white, 0, 1)
alpha = 1 - a.min(axis=2)
alpha = np.clip((alpha - 0.025) / 0.975, 0, 1)
rgb = 1 - (1 - a) / np.maximum(alpha[..., None], 1e-3)
rgb = np.clip(rgb, 0, 1)

# No trees: at the bar's size a little oak reads as a green bug on the line. Lift every greenish
# speck (green at least as strong as red) and a small ring round it.
green = (a[..., 1] >= a[..., 0] * 0.86) & (a.max(axis=2) < 0.8)
gi = Image.fromarray((green * 255).astype(np.uint8)).filter(__import__("PIL.ImageFilter").ImageFilter.MaxFilter(15))
M = np.asarray(gi) > 127
# Fill each tree's columns with the land just beside it, mirrored (so its texture isn't repeated)
# and lifted or lowered so its ridge line meets the slope between the two sides.
cols = M.any(axis=0)
clean = alpha * ~M
ridge_row = np.argmax(clean > 0.25, axis=0)
a0, c0 = alpha.copy(), rgb.copy()
x = 0
while x < cols.size:
    if not cols[x]:
        x += 1
        continue
    x0 = x
    while x < cols.size and cols[x]:
        x += 1
    L, R = x0 - 1, x
    n = x - x0
    for i, cx in enumerate(range(x0, x)):
        t = (i + 1) / (n + 1)
        target = ridge_row[L] * (1 - t) + ridge_row[R] * t
        s = L - i if t < 0.5 else R + (n - 1 - i)
        shift = int(round(target - ridge_row[s]))
        alpha[:, cx] = np.roll(a0[:, s], shift)
        rgb[:, cx] = np.roll(c0[:, s], shift, axis=0)
print(f"lifted {int(green.sum())} green pixels")

# Calmer: a little less colour, so the gold sun and "cells." keep the brightest gold on the page.
chroma = float(__import__("os").environ.get("CHROMA", "0.8"))
lum = (rgb * [0.2126, 0.7152, 0.0722]).sum(axis=2, keepdims=True)
rgb = lum + (rgb - lum) * chroma

rows = np.where(alpha.max(axis=1) > 0.06)[0]
top, bot = rows.min() - 4, rows.max() + 4
alpha, rgb = alpha[top:bot], rgb[top:bot]
h, w = alpha.shape

# The ridge line: for each column, the first row with real paint.
first = np.argmax(alpha > 0.25, axis=0).astype(float)
valid = (alpha > 0.25).any(axis=0)
ridge = first[valid]
print(f"crop {w}x{h} (rows {top}-{bot})")
print(f"ridge rows: min {ridge.min():.0f} (peak)  median {np.median(ridge):.0f}  max {ridge.max():.0f} (valley)")

# Keep the land's wash shallow: under each column's ridge line it fades out over `depth` rows.
depth = int(sys.argv[5]) if len(sys.argv) > 5 else 0
if depth:
    line = np.where(valid, first, np.median(ridge))
    # Smooth the line along x so the fade follows the land, not each speck.
    k = np.ones(31) / 31
    line = np.convolve(np.pad(line, 15, mode="edge"), k, mode="valid")
    yy = np.arange(h)[:, None] - line[None, :]
    f = np.clip(1 - (yy - depth * 0.35) / (depth * 0.65), 0, 1)
    f = f * f * (3 - 2 * f)
    alpha = alpha * f
    keep = np.where(alpha.max(axis=1) > 0.02)[0]
    alpha, rgb = alpha[: keep.max() + 3], rgb[: keep.max() + 3]
    h = alpha.shape[0]
    print(f"wash kept {depth} rows under the ridge; height now {h}")

# Taper both ends into the paper.
x = np.arange(w)
t = np.clip(np.minimum(x, w - 1 - x) / max(taper, 1), 0, 1)
t = t * t * (3 - 2 * t)
alpha = alpha * t[None, :]

img = Image.fromarray(
    np.dstack([rgb * 255, alpha[..., None] * 255]).astype(np.uint8), "RGBA"
)
if squash != 1.0:
    img = img.resize((w, max(1, round(h * squash))), Image.LANCZOS)
    print(f"squashed to {img.size[0]}x{img.size[1]}")
img.save(out)
H = img.size[1]
print(f"valley line at {np.median(ridge) * squash / H:.3f} of the height; peak at {ridge.min() * squash / H:.3f}")

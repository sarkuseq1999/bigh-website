# Menu bar "Inscription" (October 5, 2026). Made public/images/home-v2/nav/inscription/deckle.png (the torn edge). Its rule.webp
was later replaced by make_rule_stroke.py (round 3, a painted stroke).
"""Assets for menu bar option C, "Inscription" (October 5, 2026).

1. deckle.png  - a horizontally tileable torn rice-paper edge, used as a mask strip at the bottom
                 of the drop-down panels and the narrow window's sheet (white = paper).
                 Drawn at 2x: 2400 x 96 px, shown at 1200 x 48 CSS px.
2. rule.webp   - a long, very fine, lightly loaded dry-brush rule (ink alpha), drawn at 2x:
                 2800 x 24 px, shown stretched across the page's column at 12 CSS px tall.
3. dab.webp    - a small brush mark for the menu sheet's lines.
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy.ndimage import gaussian_filter, gaussian_filter1d, map_coordinates

out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(20261005)


def periodic_noise(width, cycles_from, cycles_to, amp, rng, falloff=1.0):
    """Sum of sines with integer cycles across the width (tiles seamlessly)."""
    x = np.arange(width) / width
    y = np.zeros(width)
    for k in range(cycles_from, cycles_to + 1):
        a = amp / (k**falloff)
        y += a * rng.normal(0, 1) * np.sin(2 * np.pi * k * x + rng.uniform(0, 2 * np.pi))
    return y


# ---------------------------------------------------------------- deckle (torn rice paper edge)
W, H = 2400, 112  # 2x
S = 4  # supersample for the fibres
w2, h2 = W * S, H * S
# The tear line: a few slow swells, a ragged middle, a fine tooth (all periodic).
edge = (
    periodic_noise(W, 2, 9, 7.0, rng, 0.6)
    + periodic_noise(W, 10, 60, 7.0, rng, 0.9)
    + periodic_noise(W, 61, 400, 9.0, rng, 1.0)
)
edge = edge - edge.mean()
edge = edge / np.abs(edge).max() * 13.0  # +-13 px at 2x (+-6.5 CSS px)
base = H * 0.34
line = base + edge  # y of the solid paper's edge for each x (2x px)

yy = np.arange(H)[:, None]
# Solid paper above the tear; under it the torn, thinner layer of the sheet (where the fibres
# were pulled apart): translucent and cloudy, its depth varying along the edge; then nothing.
fringe = 3.0 + 9.0 * (0.5 + 0.5 * np.tanh(periodic_noise(W, 6, 140, 3.4, rng, 0.6)))
d = yy - line[None, :]  # distance below the edge
alpha = np.where(d <= 0, 1.0, 0.0)
feather = np.clip(1 - d / fringe[None, :], 0, 1)
cloud = rng.random((H, W))
cloud = gaussian_filter(cloud, sigma=(1.2, 3.5))
cloud = (cloud - cloud.min()) / (cloud.max() - cloud.min())
layer = np.where(d > 0, feather**1.25 * (0.25 + 0.75 * cloud), 0.0)
alpha = np.maximum(alpha, layer)
# Soften the hard tear by half a pixel.
alpha = gaussian_filter(alpha, sigma=0.6)

# Loose fibres: fine, soft, curving hairs that leave the torn layer, most short, a few long.
fib = Image.new("L", (w2, h2), 0)
dr = ImageDraw.Draw(fib)
n_fibres = 1400
for _ in range(n_fibres):
    x0 = rng.uniform(0, W)
    y0 = np.interp(x0, np.arange(W), line) + rng.uniform(0, 1.0) * np.interp(
        x0, np.arange(W), fringe
    )
    length = rng.gamma(1.6, 3.2) + 1.5  # 2x px
    if rng.random() < 0.06:
        length += rng.uniform(8, 18)
    ang = np.deg2rad(rng.normal(90, 50))  # mostly downward, many sideways
    bend = rng.normal(0, 0.12)
    tone = int(np.clip(rng.normal(120, 45), 40, 210))
    width = max(1, int(round(rng.uniform(0.45, 0.95) * S)))
    pts = []
    x, y, a = x0, y0, ang
    steps = max(3, int(length / 1.5))
    for _s in range(steps):
        pts.append((x * S, y * S))
        x += np.cos(a) * length / steps
        y += np.sin(a) * length / steps
        a += bend
    for shift in (-W, 0, W):
        dr.line([(px + shift * S, py) for px, py in pts], fill=tone, width=width)
fibres = np.asarray(fib.resize((W, H), Image.LANCZOS), dtype=np.float64) / 255.0
fibres = gaussian_filter(fibres, 0.35)
alpha = np.clip(alpha + fibres * (1 - alpha) * 0.95, 0, 1)
alpha[: int(base - 16)] = 1.0

img = Image.fromarray((alpha * 255).astype(np.uint8), "L")
rgba = Image.merge("RGBA", (img.point(lambda v: 255),) * 3 + (img,))
rgba.save(out / "deckle.png", optimize=True)

# Preview on a washed page.
prev = Image.new("RGB", (1200, 120), (199, 194, 186))
paper = Image.open(Path(sys.argv[2])).convert("RGB").resize((800, 800))
tile = Image.new("RGB", (1200, 120))
tile.paste(paper.crop((0, 0, 800, 120)), (0, 0))
tile.paste(paper.crop((0, 0, 400, 120)), (800, 0))
m = img.resize((1200, 56), Image.LANCZOS)
mask = Image.new("L", (1200, 120), 255)
mask.paste(m, (0, 64))
mask.paste(Image.new("L", (1200, 0)), (0, 120))
blank = Image.new("L", (1200, 120), 0)
prev.paste(tile, (0, 0), mask)
prev.save(out / "_deckle_preview.png")
prev.crop((0, 40, 600, 120)).resize((1800, 240), Image.LANCZOS).save(out / "_deckle_zoom.png")
# 2x rendering (retina): the mask at full resolution over paper at 2x.
p2 = Image.new("RGB", (1200, 160), (199, 194, 186))
t2 = paper.resize((1600, 1600)).crop((0, 0, 1200, 160))
m2 = Image.new("L", (1200, 160), 255)
m2.paste(img.crop((0, 0, 1200, H)), (0, 160 - H))
p2.paste(t2, (0, 0), m2)
p2.save(out / "_deckle_2x.png")


# ---------------------------------------------------------------- rule (dry, lightly loaded brush)
RW, RH = 2800, 24
x = np.arange(RW)
t = x / RW
center = RH / 2 + 1.1 * np.sin(2 * np.pi * (t * 1.2) + 0.5) + 0.5 * np.sin(2 * np.pi * t * 3.4 + 2.1)
# Width (2x px): touches down, a light press near the start, a long even run, drying to the end.
w = 3.4 + 1.1 * np.exp(-(((t - 0.035) / 0.03) ** 2)) - 1.2 * t
w *= np.clip(t / 0.012, 0, 1) ** 0.6  # entry
w *= np.clip((1 - t) / 0.05, 0, 1) ** 0.8  # lift
w += gaussian_filter1d(rng.normal(0, 0.35, RW), 30)
w = np.clip(w, 0, None)
yy = np.arange(RH)[:, None]
d = np.abs(yy - center[None, :]) - w[None, :] / 2
edge_noise = gaussian_filter(rng.normal(0, 0.35, (RH, RW)), sigma=(0.5, 1.5))
band = np.clip(0.5 - (d + edge_noise) / 0.9, 0, 1)
# Bristle streaks along the stroke: the paper shows through as the ink runs out.
streak = gaussian_filter(rng.random((RH, RW)), sigma=(0.45, 14))
streak = (streak - streak.min()) / (streak.max() - streak.min())
dry = 0.12 + 0.62 * np.clip((t - 0.55) / 0.45, 0, 1) ** 1.6  # threshold: drier toward the end
ink = np.clip((streak - dry[None, :] + 0.18) / 0.18, 0, 1)
load = 0.92 - 0.25 * t  # lightly loaded, lighter toward the end
ra = np.clip(band * ink * load[None, :], 0, 1)
rule = Image.fromarray((ra * 255).astype(np.uint8), "L")
Image.merge("RGBA", (Image.new("L", (RW, RH), 12),) * 3 + (rule,)).save(
    out / "rule.webp", lossless=True
)
p = Image.new("RGB", (RW, 40), (248, 243, 234))
p.paste(Image.new("RGB", (RW, RH), (12, 11, 10)), (0, 8), rule)
p.save(out / "_rule_preview.png")
p.resize((1400, 20), Image.LANCZOS).save(out / "_rule_preview_1x.png")

# ---------------------------------------------------------------- dab (a small brush mark)
DW, DH = 160, 40
xx = np.arange(DW) / DW
c = DH / 2 + 2.0 * np.sin(np.pi * xx * 1.1 + 0.3)
wd = 15 * np.sin(np.pi * np.clip(xx * 1.02, 0, 1)) ** 0.7 * (1.05 - 0.45 * xx)
yy = np.arange(DH)[:, None]
dd = np.abs(yy - c[None, :]) - wd[None, :] / 2
en = gaussian_filter(rng.normal(0, 0.6, (DH, DW)), sigma=(0.8, 1.2))
bd = np.clip(0.5 - (dd + en) / 1.2, 0, 1)
st = gaussian_filter(rng.random((DH, DW)), sigma=(0.6, 6))
st = (st - st.min()) / (st.max() - st.min())
dry = 0.1 + 0.55 * np.clip((xx - 0.5) / 0.5, 0, 1) ** 1.3
ik = np.clip((st - dry[None, :] + 0.2) / 0.2, 0, 1)
da = np.clip(bd * ik, 0, 1)
dab = Image.fromarray((da * 255).astype(np.uint8), "L")
Image.merge("RGBA", (Image.new("L", (DW, DH), 12),) * 3 + (dab,)).save(
    out / "dab.webp", lossless=True
)
print("ok", out)

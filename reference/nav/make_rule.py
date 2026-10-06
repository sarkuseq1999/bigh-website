# Menu bar "Inscription" (October 5, 2026). Made public/images/home-v2/nav/inscription/rule.webp (the scrolled bar's brush line).
"""The scrolled bar's brush rule, round 3: painted, and legibly so at 1x.

2x drawing (2800 x 40 px, shown 1400 x 20 CSS px, stretched to the column). Features chosen to
survive at 1x: a loaded touch-down; a calm wave and two or three swells of pressure (body 3-6 CSS
px); in the second half the bristles part into separate strands with paper between them (flying
white), the strands running dry at different points, the last ones ending in hairs.
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, gaussian_filter1d

out = Path(sys.argv[1])
rng = np.random.default_rng(7)
W, H = 2800, 40
x = np.arange(W)
t = x / W

centre = (
    H / 2
    + 2.2 * np.sin(2 * np.pi * t * 1.05 + 0.3)
    + 0.9 * np.sin(2 * np.pi * t * 2.7 + 1.4)
    + gaussian_filter1d(rng.normal(0, 0.6, W), 80)
)
press = (
    1.0
    + 0.32 * np.exp(-(((t - 0.20) / 0.07) ** 2))
    + 0.22 * np.exp(-(((t - 0.47) / 0.08) ** 2))
    - 0.18 * np.exp(-(((t - 0.33) / 0.05) ** 2))
)
width = (9.0 + 5.5 * np.exp(-(((t - 0.022) / 0.02) ** 2)) - 3.5 * t) * press
width += gaussian_filter1d(rng.normal(0, 0.8, W), 50)
width *= np.clip(t / 0.008, 0, 1) ** 0.5
width *= np.clip((1 - t) / 0.05, 0, 1) ** 0.6
width = np.clip(width, 0, None)

# The bristles part as the ink runs out: from about halfway, the strands spread apart.
spread = 1 + 1.1 * np.clip((t - 0.5) / 0.4, 0, 1) ** 1.4

yy = np.arange(H)[:, None].astype(float)
alpha = np.zeros((H, W))
n = 7
for i in range(n):
    pos = (i + 0.5) / n - 0.5
    wob = gaussian_filter1d(rng.normal(0, 0.35, W), 25)
    off = pos * width * spread + wob
    thick = width / n * (1.6 - 0.55 * np.clip((t - 0.5) / 0.4, 0, 1))
    load = rng.uniform(0.82, 1.0)
    # Outer strands run dry first; one or two inner ones carry on to the end.
    dry_at = rng.uniform(0.86, 1.05) - 0.36 * abs(pos) * 2
    ink = load * np.clip(1 - (t - dry_at) / 0.14, 0, 1)
    skip = gaussian_filter1d(rng.random(W), rng.uniform(4, 10))
    skip = (skip - skip.min()) / (skip.max() - skip.min())
    keep = np.clip((skip - (0.1 + 0.55 * np.clip((t - 0.6) / 0.4, 0, 1))) / 0.1, 0, 1)
    # Two strands carry little ink from early on: thin streaks of paper along the body.
    early = i in (1, 4)
    keep_early = np.clip((skip - 0.38) / 0.1, 0, 1)
    ink = ink * np.where(
        t > 0.55, keep, np.where(early & (t > 0.12), 0.25 + 0.75 * keep_early, 0.75 + 0.25 * keep)
    )
    d = np.abs(yy - (centre + off)[None, :])
    prof = np.clip(1 - (d - thick / 2) / 0.8, 0, 1)
    alpha = np.maximum(alpha, prof * ink[None, :])

grain = gaussian_filter(rng.random((H, W)), sigma=(0.6, 1.2))
grain = (grain - grain.min()) / (grain.max() - grain.min())
alpha *= 0.8 + 0.2 * grain
alpha = np.clip(alpha, 0, 1)

img = Image.fromarray((alpha * 255).astype(np.uint8), "L")
Image.merge("RGBA", (Image.new("L", (W, H), 12),) * 3 + (img,)).save(out / "rule.webp", lossless=True)
for cw in (1300, 1083):
    m = img.resize((cw, 20), Image.LANCZOS).point(lambda v: int(v * 0.78))
    pv = Image.new("RGB", (cw, 44), (248, 243, 234))
    pv.paste(Image.new("RGB", (cw, 20), (12, 11, 10)), (0, 12), m)
    pv.save(out / f"_rule_{cw}.png")
    thirds = [pv.crop((0, 0, cw // 3, 44)), pv.crop((cw // 3, 0, 2 * cw // 3, 44)), pv.crop((2 * cw // 3, 0, cw, 44))]
    z = Image.new("RGB", (cw // 3 * 3, 44 * 3 * 3 + 12), (200, 0, 0))
    for k, part in enumerate(thirds):
        z.paste(part.resize((cw // 3 * 3, 132), Image.NEAREST), (0, k * 136))
    z.save(out / f"_rule_{cw}_zoom.png")
print("ok")

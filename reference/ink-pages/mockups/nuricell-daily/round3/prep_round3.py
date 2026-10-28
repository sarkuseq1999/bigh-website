"""Round 3 mockup plates for NuriCell's daily chapter, paper divided out so they multiply onto the page.

  day    the California day (day-a1): cropped to its ink, edges faded into the paper
  rings  the redwood round (rings-b1): one ring, about 20 in from the bark, laid in gold leaf;
         writes rings.json with where the ring and the bark are (fractions of the plate)

usage: python -X utf8 prep_round3.py <repo> <paint-dir> <out-dir>
"""

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, gaussian_filter1d, map_coordinates

repo, src, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(repo / "reference/ink-pages/about"))
import build_about as bd  # noqa: E402

GOLD = np.array([196, 154, 58], np.float32)  # gold-leaf, DESIGN.md


def flat(name):
    return np.asarray(bd.levelled(bd.divided(Image.open(src / f"{name}.png").convert("RGB")))).astype(np.float32)


def fade_edges(arr, frac=0.05, right=None, left=None):
    """Fade the plate into the paper at its edges; `left`/`right` widen a side (fractions of the width)."""
    h, w, _ = arr.shape
    f = max(2.0, min(h, w) * frac)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    fl = max(f, (left or 0) * w)
    fr = max(f, (right or 0) * w)
    keep = np.clip(np.minimum.reduce([xx / fl, yy / f, (w - 1 - xx) / fr, (h - 1 - yy) / f]), 0, 1)
    keep = (keep * keep * (3 - 2 * keep))[..., None]
    return 255 - (255 - arr) * keep


def leaf_patches(shape, seed):
    rng = np.random.default_rng(seed)
    patch = gaussian_filter(rng.normal(0, 1, shape), 14)
    return patch / (np.abs(patch).max() + 1e-6)


# The day: the long hillside band, its own height. The night sky's wash ran off the painting's right
# edge, so that side fades out over a wider stretch.
day = flat("day-a1")
x0, y0, x1, y1 = bd.ink_box(day.astype(np.uint8), pad=0.03)
day = fade_edges(day[y0:y1, x0:x1], right=0.1, left=0.03)
# The morning sun was a pale lemon wash with a soft rim (it read as a glow): lay it in gold leaf.
h, w, _ = day.shape
yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
sat = (day[..., 0] + day[..., 1]) / 2 - day[..., 2]
near = (xx < 0.3 * w) & (yy < 0.75 * h)
sy, sx = np.nonzero((sat > 40) & near)
cy, cx = sy.mean(), sx.mean()
rim = np.hypot(xx - cx, yy - cy)
sun = np.clip((sat - 20) / 14, 0, 1) * near * (rim < 80)
leaf = GOLD[None, None, :] * (1 + 0.14 * leaf_patches((h, w), 3)[..., None])
dark = day.mean(axis=2, keepdims=True) < 150  # the walker in front of it stays ink
day = np.where(dark, day, day * (1 - sun[..., None]) + leaf * sun[..., None])
Image.fromarray(day.clip(0, 255).astype(np.uint8)).save(out / "day.png")
print("day", w, "x", h, "from box", (x0, y0, x1, y1), "sun at", round(cx), round(cy))

# The rings: trace the dark ring line nearest RADIUS all the way round, smooth it, lay gold leaf on it.
rings = flat("rings-b1")
grey = gaussian_filter(rings.mean(axis=2), 1.2)
# The ring at about 142px is the clearest one round the whole log (the averaged profile), and about
# 20 ring lines lie between it and the bark.
CX, CY, RADIUS = 650.0, 605.0, 142.0
angles = np.radians(np.arange(0, 360, 0.5))
radii = []
for t in angles:
    rr = np.arange(RADIUS - 6, RADIUS + 6.5, 0.5)
    prof = map_coordinates(grey, [CY + rr * np.sin(t), CX + rr * np.cos(t)], order=1)
    radii.append(rr[int(np.argmin(prof))])
radii = gaussian_filter1d(np.array(radii), 16, mode="wrap")

h, w, _ = rings.shape
yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
theta = np.mod(np.arctan2(yy - CY, xx - CX), 2 * np.pi)
ring_r = np.interp(theta, np.mod(angles, 2 * np.pi), radii, period=2 * np.pi)
dist = np.abs(np.hypot(xx - CX, yy - CY) - ring_r)
rng = np.random.default_rng(7)
# A torn edge: the stroke's half-width wanders a little round the ring, and its rim breaks up.
wander = gaussian_filter1d(rng.normal(0, 1, angles.size), 6, mode="wrap")
half = 5.4 + 1.6 * np.interp(theta, np.mod(angles, 2 * np.pi), wander, period=2 * np.pi)
grain = gaussian_filter(rng.normal(0, 1, (h, w)), 1.0)
core = np.clip((half - dist) / 1.8 + 0.5 * grain, 0, 1)
# The painted ring line itself turns gold where it is dark, so the leaf keeps the brush's texture.
ink = np.clip((215 - grey) / 90, 0, 1) * np.clip((11 - dist) / 3, 0, 1)
cover = np.maximum(0.8 * core, ink)
# Leaf is flat metal: a little lighter and darker in patches, never a glow.
patch = gaussian_filter(rng.normal(0, 1, (h, w)), 14)
patch = patch / (np.abs(patch).max() + 1e-6)
leaf = GOLD[None, None, :] * (1 + 0.16 * patch[..., None])
rings = rings * (1 - cover[..., None]) + leaf * cover[..., None]

# Where the labels point: the ring's and the bark's rightmost points, as fractions of the plate.
bark_r = 401.0
plate = rings.clip(0, 255).astype(np.uint8)
Image.fromarray(plate).save(out / "rings.png")
spots = {
    "w": w,
    "h": h,
    "ring": [(CX + radii[0]) / w, CY / h],
    "bark": [(CX + bark_r) / w, CY / h],
    "centre": [CX / w, CY / h],
}
(out / "rings.json").write_text(json.dumps(spots, indent=1), encoding="utf-8")
print("rings", spots)

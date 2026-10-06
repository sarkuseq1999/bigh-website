# Menu bar "Inscription", round 6 (October 6, 2026). Cuts the current page's mark: a short, calm
# brush stroke laid under a link's word, cut from a real painting of short sumi strokes (GPT Image
# 2.5, reference/nav/originals/gpt25-brush-strokes.png; prompt in its .json). No new picture.
"""The current page's brush stroke, cut from a real painted stroke.

The source strokes are loaded and wavy (each lands on a round, pressed head and travels with a
clear S-wave before it dries out into flying-white streaks). Under a 20px word a wave reads as a
squiggle, so the stroke's middle is straightened (each column moved so the stroke's alpha-weighted
middle lies on one line; a whisper of the wave is kept so it is still a hand's line), and its
pressed head is drawn in toward the middle until it is at most 1.25 times the body's thickness, so
it reads as a light, sure stroke rather than a blot or a tadpole. (Lightening the head's ink instead
was tried: the smooth fade read as a printed gradient, not ink.)

The ink becomes alpha the way the other cut-outs do (each pixel's distance from the paper, the
paper's own speckle removed), so the page's paper shows through the stroke's dry streaks.

Output:
  public/images/home-v2/nav/inscription/current-stroke.webp

usage: python -X utf8 reference/nav/make_current_stroke.py [preview-dir] [--all]
       --all writes every stroke, straightened, to the preview folder to choose from.
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter1d, map_coordinates

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "reference/nav/originals/gpt25-brush-strokes.png"
OUT = REPO / "public/images/home-v2/nav/inscription/current-stroke.webp"
PREVIEW = next((Path(a) for a in sys.argv[1:] if not a.startswith("--")), None)
PAPER = (248, 243, 234)
INK = (12, 11, 10)

# The chosen stroke (0 = top: the fifth, the lightest loaded, with the longest dry end), how much
# of its wave is kept, and the finished file's width (its height follows the stroke).
CHOSEN = 4
KEEP_WAVE = 0.12
OUT_W = 880


def strokes(grey):
    """Each painted stroke's rows and columns (seven strokes on white, wide gaps between them)."""
    dark = (grey < 150).sum(1)
    ys = np.where(dark > 0)[0]
    groups, start, prev = [], ys[0], ys[0]
    for y in ys[1:]:
        if y - prev > 30:
            groups.append((start, prev))
            start = y
        prev = y
    groups.append((start, prev))
    out = []
    for y0, y1 in groups:
        y0, y1 = max(0, y0 - 30), y1 + 30
        cols = np.where((grey[y0:y1] < 235).any(0))[0]
        out.append((y0, y1, cols.min(), cols.max()))
    return out


def alpha_of(grey):
    """Ink as alpha: paper (the white's own level) -> 0, the ink's core -> 1."""
    paper = np.percentile(grey, 60)
    core = np.percentile(grey[grey < 120], 20) if (grey < 120).any() else 20.0
    a = np.clip((paper - 6 - grey) / (paper - 6 - core), 0, 1)
    a[a < 0.04] = 0
    return a


def straighten(a, keep):
    """Move each column so the stroke's middle lies on one straight line, keeping `keep` of the
    wave. The middle is the alpha-weighted row, smoothed over about a fifth of the stroke so the
    bristles' own texture is never moved, only the wave."""
    ys = np.arange(a.shape[0])[:, None]
    weight = a.sum(0)
    c = np.where(weight > 0.5, (a * ys).sum(0) / np.maximum(weight, 1e-6), np.nan)
    idx = np.arange(a.shape[1])
    good = ~np.isnan(c)
    c = np.interp(idx, idx[good], c[good])
    c = gaussian_filter1d(c, max(8.0, a.shape[1] / 22))
    # The line the middle is laid on: the stroke's own straight trend (a calm, slight rise is kept).
    fit = np.polyval(np.polyfit(idx[good], c[good], 1), idx)
    offset = (c - fit) * (1 - keep)
    # Room above and below for the shifted columns.
    pad = int(np.ceil(np.abs(offset).max())) + 4
    padded = np.pad(a, ((pad, pad), (0, 0)))
    yy, xx = np.mgrid[0 : padded.shape[0], 0 : padded.shape[1]].astype(np.float64)
    return map_coordinates(padded, [yy + offset[None, :], xx], order=1, mode="constant")


def even_head(a, most=1.25):
    """A lightly loaded brush lands without a blot: where the stroke is thicker than `most` times
    its body (the pressed head), each column is drawn in toward the stroke's middle until it is
    that thick. Only the shape moves; the torn edge and the bristles' texture are the painting's."""
    ys = np.arange(a.shape[0])[:, None]
    weight = a.sum(0)
    c = np.where(weight > 0.5, (a * ys).sum(0) / np.maximum(weight, 1e-6), np.nan)
    idx = np.arange(a.shape[1])
    good = ~np.isnan(c)
    c = gaussian_filter1d(np.interp(idx, idx[good], c[good]), 6)
    thick = gaussian_filter1d((a > 0.35).sum(0).astype(np.float64), 10)
    inked = thick > 1
    body = np.median(thick[inked][len(thick[inked]) // 5 : len(thick[inked]) * 3 // 5])
    squeeze = np.maximum(1.0, thick / (most * body))
    yy, xx = np.mgrid[0 : a.shape[0], 0 : a.shape[1]].astype(np.float64)
    src = c[None, :] + (yy - c[None, :]) * squeeze[None, :]
    return map_coordinates(a, [src, xx], order=1, mode="constant")


def trim(a, pad=2):
    rows = np.where(a.max(1) > 0.02)[0]
    cols = np.where(a.max(0) > 0.02)[0]
    return a[max(0, rows.min() - pad) : rows.max() + 1 + pad, max(0, cols.min() - pad) : cols.max() + 1 + pad]


def finish(a):
    """To the finished width, at the stroke's own proportions."""
    img = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8), "L")
    return img.resize((OUT_W, round(OUT_W * img.size[1] / img.size[0])), Image.LANCZOS)


def save_mask(img, path):
    Image.merge("RGBA", (Image.new("L", img.size, INK[0]),) * 3 + (img,)).save(
        path, lossless=True, method=6
    )


def preview(img, width, height, name, opacity=0.85, scale=1):
    """The mask as the bar would show it: `width` x `height` CSS px on the paper, at `scale`."""
    w, h = round(width * scale), round(height * scale)
    m = img.resize((w, h), Image.LANCZOS).point(lambda v: int(v * opacity))
    pv = Image.new("RGB", (w + 24 * scale, h + 24 * scale), PAPER)
    pv.paste(Image.new("RGB", (w, h), INK), (12 * scale, 12 * scale), m)
    pv.save(PREVIEW / name)


grey = np.asarray(Image.open(SRC).convert("L")).astype(np.float64)
found = strokes(grey)
print("strokes (y0, y1, x0, x1):", found)

if PREVIEW:
    PREVIEW.mkdir(parents=True, exist_ok=True)

if PREVIEW and "--all" in sys.argv:
    for i, (y0, y1, x0, x1) in enumerate(found):
        a = alpha_of(grey[y0:y1, x0 : x1 + 1])
        flat = trim(even_head(straighten(a, KEEP_WAVE)))
        img = finish(flat)
        save_mask(img, PREVIEW / f"_stroke{i}.webp")
        preview(img, 80, 7.3, f"_stroke{i}_80.png", scale=2)
        raw = Image.fromarray((trim(a) * 255).astype(np.uint8), "L")
        preview(raw, 300, 300 * raw.size[1] / raw.size[0], f"_stroke{i}_raw.png")
        preview(Image.fromarray((flat * 255).astype(np.uint8), "L"), 600, 600 * flat.shape[0] / flat.shape[1], f"_stroke{i}_flat.png")
    raise SystemExit

y0, y1, x0, x1 = found[CHOSEN]
a = alpha_of(grey[y0:y1, x0 : x1 + 1])
img = finish(trim(even_head(straighten(a, KEEP_WAVE))))
save_mask(img, OUT)
print(OUT, img.size)
if PREVIEW:
    for w in (56, 80, 100):
        preview(img, w, w / 11, f"_current_{w}.png")
        preview(img, w, w / 11, f"_current_{w}_2x.png", scale=2)
print("ok")

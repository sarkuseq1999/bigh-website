# Menu bar "Inscription", round 3 (October 6, 2026). Cuts the scrolled bar's brush rule from a real
# painted line (GPT Image 2.5, reference/nav/originals/gpt25-rule-lines-dry.png, prompt in
# reference/nav/prompts/rule-lines-dry.txt). Replaces make_rule.py's drawn rule.webp (kept for the
# record; no longer used).
"""The scrolled bar's brush rule, cut from a real painted line.

The ink becomes alpha the way the other cut-outs do (each pixel's distance from the paper, the
paper's own speckle removed), so the page's rice paper shows through the stroke's dry streaks.

Outputs:
  public/images/home-v2/nav/inscription/rule-whole.webp
      shipped: one long stroke across the page's column, under the mark (the thinnest of the four
      lines; the bar keeps it about 3px in body at 1536).
  reference/nav/alt/rule-half.webp
      the alternative Mo is shown, not shipped: one stroke that lands at its left end and dries out
      to nothing at its right end, laid twice (from the column's left edge toward the mark, and
      mirrored from the right edge) so the mark stands in the gap. Built and compared in round 3
      (scripts/qa/out/nav-r3/compare/); on a phone the two halves shrink to two short dabs and on
      desktop the gap reads as the line missing under the mark, so the continuous stroke shipped.
      To restore it: two spans in place of the one rule, each `width: calc(50% - var(--mark) / 2 -
      20px)`, `aspect-ratio: 2437 / 56`, `min-height: 8px`, the right one `scale: -1 1`.

The source line enters with a small angled hook (it read as an arrow's tail); it is cut away and
the entry is carved from the line's own ink into a short exposed tip, the way a quick brush lands.
Lines from the first try (gpt25-rule-lines.png) were not used: each lands on a round blob (a pin's
head) and dries out into broken dashes.

usage: python -X utf8 reference/nav/make_rule_stroke.py [preview-dir] [--all]
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter1d

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "reference/nav/originals/gpt25-rule-lines-dry.png"
OUT = REPO / "public/images/home-v2/nav/inscription"
PREVIEW = next((Path(a) for a in sys.argv[1:] if not a.startswith("--")), None)
PAPER = (248, 243, 234)
INK = (12, 11, 10)


def lines(grey):
    """Each painted line's rows and columns (four lines on white, wide gaps between them)."""
    dark = (grey < 150).sum(1)
    ys = np.where(dark > 0)[0]
    groups, start, prev = [], ys[0], ys[0]
    for y in ys[1:]:
        if y - prev > 40:
            groups.append((start, prev))
            start = y
        prev = y
    groups.append((start, prev))
    out = []
    for y0, y1 in groups:
        band = grey[max(0, y0 - 40) : y1 + 40]
        cols = np.where((band < 235).any(0))[0]
        out.append((max(0, y0 - 40), y1 + 40, cols.min(), cols.max()))
    return out


def alpha_of(grey):
    """Ink as alpha: paper (the white's own level) -> 0, the ink's core -> 1."""
    paper = np.percentile(grey, 60)
    core = np.percentile(grey[grey < 120], 20) if (grey < 120).any() else 20.0
    a = np.clip((paper - 6 - grey) / (paper - 6 - core), 0, 1)
    # A whisper of speckle on the white is not ink.
    a[a < 0.04] = 0
    return a


def centre_line(a):
    """The stroke's middle (alpha-weighted row) at each column, smoothed."""
    ys = np.arange(a.shape[0])[:, None]
    weight = a.sum(0)
    c = np.where(weight > 0.5, (a * ys).sum(0) / np.maximum(weight, 1e-6), np.nan)
    idx = np.arange(a.shape[1])
    good = ~np.isnan(c)
    c = np.interp(idx, idx[good], c[good])
    return gaussian_filter1d(c, 12)


def entry(a, cut, tip):
    """Cut the hook away (everything left of `cut`) and carve a short exposed tip from the line's
    own ink: over `tip` columns the stroke narrows to a point toward its start."""
    a = a.copy()
    a[:, :cut] = 0
    c = centre_line(a[:, cut:])
    c = np.concatenate([np.full(cut, c[0]), c])
    ys = np.arange(a.shape[0])[:, None]
    # The line's half-thickness where it is whole, a little past the tip.
    body = a[:, cut + tip : cut + tip + 200]
    half = max(2.0, (body > 0.35).sum(0).mean() / 2 + 1)
    x = np.arange(a.shape[1]) - cut
    reach = np.clip(x / tip, 0, 1) ** 0.55 * half
    lens = np.clip(1 - (np.abs(ys - c[None, :]) - reach[None, :]) / 1.5, 0, 1)
    a = np.where(x[None, :] < tip, a * lens, a)
    # Landing: the first touch is a shade lighter, the ink arriving as the brush comes down.
    a *= np.clip(0.55 + 0.45 * x / (tip * 0.8), 0.55, 1)[None, :]
    return a


def trim(a, pad=2):
    rows = np.where(a.max(1) > 0.02)[0]
    cols = np.where(a.max(0) > 0.02)[0]
    return a[max(0, rows.min() - pad) : rows.max() + 1 + pad, max(0, cols.min() - pad) : cols.max() + 1 + pad]


def save_mask(a, path):
    img = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8), "L")
    Image.merge("RGBA", (Image.new("L", img.size, INK[0]),) * 3 + (img,)).save(
        path, lossless=True, method=6
    )
    return img


def preview(img, width, height, name, opacity=0.75, scale=1):
    """The mask as the bar would show it: `width` x `height` CSS px on the paper, at `scale`."""
    w, h = round(width * scale), round(height * scale)
    m = img.resize((w, h), Image.LANCZOS).point(lambda v: int(v * opacity))
    pv = Image.new("RGB", (w + 24 * scale, h + 24 * scale), PAPER)
    pv.paste(Image.new("RGB", (w, h), INK), (12 * scale, 12 * scale), m)
    pv.save(PREVIEW / name)


grey = np.asarray(Image.open(SRC).convert("L")).astype(np.float64)
found = lines(grey)
print("lines (y0, y1, x0, x1):", found)

if PREVIEW and "--all" in sys.argv:
    # Every line, as the half at 1536 would show it, to choose from.
    PREVIEW.mkdir(parents=True, exist_ok=True)
    for i, (y0, y1, x0, x1) in enumerate(found):
        a = trim(alpha_of(grey[y0:y1, x0 : x1 + 1]))
        img = Image.fromarray((a * 255).astype(np.uint8), "L")
        preview(img, 570, 570 * a.shape[0] / a.shape[1], f"_line{i}_570.png")
        preview(img, 570, 570 * a.shape[0] / a.shape[1], f"_line{i}_570_2x.png", scale=2)
    raise SystemExit

HALF_LINE, WHOLE_LINE = 2, 0  # the chosen lines (0 = top)
ALT = REPO / "reference/nav/alt"
ALT.mkdir(parents=True, exist_ok=True)
for name, which, where in (("rule-whole.webp", WHOLE_LINE, OUT), ("rule-half.webp", HALF_LINE, ALT)):
    y0, y1, x0, x1 = found[which]
    a = alpha_of(grey[y0:y1, x0 : x1 + 1])
    a = trim(entry(a, cut=62, tip=70))
    img = save_mask(a, where / name)
    print(where / name, img.size)
    if PREVIEW:
        PREVIEW.mkdir(parents=True, exist_ok=True)
        stem = name.split(".")[0]
        for w in (570, 1083, 1300):
            preview(img, w, w * a.shape[0] / a.shape[1], f"_{stem}_{w}.png")
            preview(img, w, w * a.shape[0] / a.shape[1], f"_{stem}_{w}_2x.png", scale=2)
print("ok")

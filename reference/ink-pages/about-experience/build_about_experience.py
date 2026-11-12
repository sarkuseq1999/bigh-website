"""Build the About "Our experience" painting (Mo picked 3, the sequoia repainted with softer
colour, November 11, 2026).

Mo kept the giant sequoia ("I think the sequoia tree is a good idea. Maybe just make it a little
bit colored.") and, of three coloured versions on the real page, picked 3: Codex's repaint of the
shipped ink sequoia in thin watercolour (sequoia-colour-b: cinnamon bark, sage crown, pale
blue-green misty firs, the gold patch kept), its colour mixed SOFT of the way toward its own grey
so it reads as "a little coloured", the gold leaf left at full colour.

    python -X utf8 reference/ink-pages/about-experience/build_about_experience.py

Out: public/images/about-experience/sequoia-soft-v1.webp, its gold-leaf light mask
sequoia-soft-v1-gold.webp (for the kit's glint) and src/components/about/experience-art.ts. The
paper is divided out so the painting multiplies onto the page.

The bark is warm and orange-brown, its lit streaks almost as pale as the leaf, so a colour test
alone either leaves the leaf's pale right half out or takes the streaks in. So the leaf is cut in
two steps, only in the box round it on the trunk (LEAF_BOX): its core is the largest patch whose
hue is a clear yellow (44 degrees or more; the bark is about 25 to 36), then OpenCV's GrabCut grows
that core to the leaf's whole shape by its colours against the bark's.
"""

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageFilter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SITE = ROOT / "public" / "images" / "about-experience"
URL = "/images/about-experience"
ART = ROOT / "src" / "components" / "about" / "experience-art.ts"

TAKE = "sequoia-colour-b"
NAME = "sequoia-soft-v1"
# How far the colour is mixed toward its own grey (Mo's pick: 3, "repainted, softer").
SOFT = 0.35
FLOOR = 10
FADE = 40
PAD = 24
# Where the gold leaf lies in the original (x0, y0, x1, y1), with room round it.
LEAF_BOX = (410, 380, 530, 510)


def load(name):
    """The painting as RGB (0..255); a picture with transparency is laid on white paper first."""
    img = Image.open(HERE / "originals" / f"{name}.png")
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        paper = Image.new("RGBA", img.size, (255, 255, 255, 255))
        img = Image.alpha_composite(paper, img)
    return np.asarray(img.convert("RGB")).astype(float)


def largest(mask):
    """The largest patch of a 0/1 mask, its holes filled, and its box (x, y, w, h)."""
    count, labels, stats, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), connectivity=8)
    if count < 2:
        raise SystemExit("no gold leaf found in LEAF_BOX")
    biggest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    patch = (labels == biggest).astype(np.uint8)
    contours, _ = cv2.findContours(patch, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    patch = cv2.drawContours(np.zeros_like(patch), contours, -1, 1, thickness=cv2.FILLED)
    return patch, tuple(int(v) for v in stats[biggest][:4])


def leaf(a):
    """The gold leaf as a mask over the original (0..255)."""
    rgb = a / 255.0
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    hi, lo = rgb.max(axis=2), rgb.min(axis=2)
    sat = (hi - lo) / np.maximum(hi, 1e-4)
    warm = (r >= g) & (g > b)
    hue = np.where(warm, 60 * (g - b) / np.maximum(hi - lo, 1e-4), 0)
    x0, y0, x1, y1 = LEAF_BOX
    inside = np.zeros(hue.shape, bool)
    inside[y0:y1, x0:x1] = True

    # The core: the clearest yellow.
    core, (x, y, w, h) = largest(inside & (hue >= 44) & (sat >= 0.2) & (hi >= 0.45))
    # GrabCut: bark outside a box round the core; inside it, warm bright yellow is probably leaf.
    near = np.zeros_like(inside)
    near[y - 14 : y + h + 14, x - 14 : x + w + 20] = True
    marks = np.full(hue.shape, cv2.GC_BGD, np.uint8)
    marks[near] = cv2.GC_PR_BGD
    marks[near & (hue >= 38) & (hi >= 0.6)] = cv2.GC_PR_FGD
    marks[core == 1] = cv2.GC_FGD
    bgr = cv2.cvtColor(a.astype(np.uint8), cv2.COLOR_RGB2BGR)
    cv2.grabCut(bgr, marks, None, np.zeros((1, 65)), np.zeros((1, 65)), 8, cv2.GC_INIT_WITH_MASK)
    patch, (x, y, w, h) = largest((marks == cv2.GC_FGD) | (marks == cv2.GC_PR_FGD))
    if x <= x0 or y <= y0 or x + w >= x1 or y + h >= y1:
        raise SystemExit(f"the gold leaf runs into LEAF_BOX's edge: {(x, y, w, h)}")
    # Its pale rim and thin tips: one pixel more all round.
    patch = cv2.dilate(patch, np.ones((3, 3), np.uint8))
    print(f"gold leaf: {w} x {h} at ({x}, {y}), {int(patch.sum())} px")
    return patch * 255


def soften(a, patch):
    """The colour mixed SOFT of the way toward its own grey; the gold leaf keeps its full colour
    (the patch grown a pixel and feathered, so no grey rim is left round it)."""
    lum = (a * [0.299, 0.587, 0.114]).sum(axis=2, keepdims=True)
    soft = a * (1 - SOFT) + lum * SOFT
    m = Image.fromarray(patch.astype(np.uint8)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    m = np.asarray(m, dtype=float)[..., None] / 255
    return soft * (1 - m) + a * m


def paperless(a):
    """How dark each pixel is once the paper is divided out (0 = bare paper)."""
    edge = np.concatenate([a[:40].reshape(-1, 3), a[:, :40].reshape(-1, 3), a[:, -40:].reshape(-1, 3)])
    paper = np.percentile(edge, 60, axis=0)
    dark = 255.0 - np.clip(a / paper * 255.0, 0, 255)
    dark = np.clip((dark - FLOOR) / (1 - FLOOR / 255.0), 0, 255)
    h, w = dark.shape[:2]
    ramp = lambda n: np.clip(np.minimum(np.arange(n), np.arange(n)[::-1]) / FADE, 0, 1)
    dark *= (ramp(h)[:, None] * ramp(w)[None, :])[..., None]
    return dark


def box_of(dark):
    """The painting's box: the empty paper round it cut, a small margin left."""
    ink = dark.max(axis=2) > 6
    rows = np.where(ink.mean(axis=1) > 0.004)[0]
    cols = np.where(ink.mean(axis=0) > 0.004)[0]
    h, w = ink.shape
    return max(cols[0] - PAD, 0), max(rows[0] - PAD, 0), min(cols[-1] + PAD, w), min(rows[-1] + PAD, h)


def main():
    a = load(TAKE)
    patch = leaf(a)
    dark = paperless(soften(a, patch))
    x0, y0, x1, y1 = box_of(dark)
    ink = Image.fromarray((255.0 - dark[y0:y1, x0:x1] + 0.5).astype(np.uint8))
    SITE.mkdir(parents=True, exist_ok=True)
    ink.save(SITE / f"{NAME}.webp", quality=90, method=6)

    mask = Image.fromarray(patch[y0:y1, x0:x1].astype(np.uint8), "L")
    mask = mask.filter(ImageFilter.GaussianBlur(1.2))
    white = Image.new("L", mask.size, 255)
    Image.merge("RGBA", (white, white, white, mask)).save(SITE / f"{NAME}-gold.webp", "WEBP", quality=80, method=6)
    cover = float((np.asarray(mask) > 128).mean())

    ART.write_text(
        "// Generated by reference/ink-pages/about-experience/build_about_experience.py. Do not edit by\n"
        "// hand. The About page's experience painting: the giant sequoia beside a young one, repainted\n"
        "// with soft colour (Mo picked 3, November 11, 2026), its paper divided out so it multiplies\n"
        "// onto the page; `gold` is the light mask over its gold leaf, for the kit's glint.\n"
        "export const experienceSequoia = {\n"
        f'  src: "{URL}/{NAME}.webp",\n'
        f"  width: {ink.width},\n"
        f"  height: {ink.height},\n"
        f'  gold: "{URL}/{NAME}-gold.webp",\n'
        "} as const;\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"{NAME}: {ink.width} x {ink.height}, shape {ink.width / ink.height:.4f}, gold {cover:.2%} of the picture")
    for f in (f"{NAME}.webp", f"{NAME}-gold.webp"):
        print(f"  {f}: {(SITE / f).stat().st_size // 1024} KB")


main()

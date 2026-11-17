"""Pictures for the Advanced OPC "Why antioxidants matter" mockups (November 17, 2026).

The live chapter shows a bunch of grapes in grey ink that lights up with gold from the middle (Mo's
Why A, October 16). Its gold now sits in a pale yellow haze, a glow Mo's later rule refuses (October
19: gold leaf never glows), and the page has turned California colour since. Two ideas, each kept
to the chapter's own moment (the lit painting spreads over the unlit one from one point):

  A  ripe: the bunch painted in colour; as you arrive it ripens, from green to deep violet (the
     colour is the plant's own antioxidant pigments). No gold.
  B  seeds: a cluster up close and one grape cut in half; as you arrive its seeds turn to gold
     leaf (OPCs come from grape seeds).

Each take is divided (paper to white), cropped to its ink and set on the live picture's shape
(1100 x 1485), so the mock can serve it in place of the live grapes. The unlit layer is made from
the lit one: A's grapes turned unripe green, B's seeds turned plain seed brown.

Mo picked B (November 17). The four takes mocked here are now in
codes/bigh-archive/opc-why-unused-2026-11-17/ (copy them back into opc/originals/ to run this again).

usage: python -X utf8 prep.py
"""

import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "reference/ink-pages/about"))
import build_about as bd  # noqa: E402

ORIG = REPO / "reference/ink-pages/opc/originals"
ART = HERE / "art"
ART.mkdir(exist_ok=True)
W, H = 1100, 1485


def shaped(img):
    """Cropped to its ink, padded with white to the live picture's shape, at its size."""
    a = np.asarray(img)
    x0, y0, x1, y1 = bd.ink_box(a, pad=0.05)
    w, h = x1 - x0, y1 - y0
    if w / h < W / H:
        nw = round(h * W / H)
        x0 -= (nw - w) // 2
        x1 = x0 + nw
    else:
        nh = round(w * H / W)
        y0 -= (nh - h) // 2
        y1 = y0 + nh
    canvas = Image.new("RGB", (x1 - x0, y1 - y0), (255, 255, 255))
    canvas.paste(img.crop((max(x0, 0), max(y0, 0), min(x1, img.width), min(y1, img.height))), (max(-x0, 0), max(-y0, 0)))
    return canvas.resize((W, H), Image.LANCZOS)


def finished(img):
    return bd.feathered(bd.levelled(img), 0.03)


def unripe(img):
    """The violet grapes turned to unripe green-gold: hue moved, colour softened, lifted a little."""
    hsv = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2HSV_FULL).astype(np.float32)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    # Violet to red-violet (OpenCV full range: 0-255 round the wheel), with real colour in it.
    violet = (((h > 165) & (h < 256)) | (h < 8)) & (s > 28)
    m = cv2.GaussianBlur(violet.astype(np.float32), (0, 0), 2.5)
    hsv[..., 0] = np.where(m > 0.01, h * (1 - m) + 52 * m, h)
    hsv[..., 1] = s * (1 - 0.35 * m)
    hsv[..., 2] = np.clip(v * (1 - m) + (v * 0.55 + 105) * m, 0, 255)
    return Image.fromarray(cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB_FULL))


def plain_seeds(img):
    """The gold-leaf seeds turned to plain grape-seed brown (where the gold is, nothing else)."""
    a = np.asarray(img).astype(np.float32)
    hi, lo = a.max(axis=2), a.min(axis=2)
    sat = (hi - lo) / np.maximum(hi, 1)
    # Only the cut grape (the lower part of the picture), and only real leaf: strongly saturated
    # and bright, so the olive leaf, the stem and the pale flesh stay as painted.
    gold = bd.gold_pixels(a.astype(np.uint8)) & (sat > 0.42) & (hi > 150)
    gold[: int(a.shape[0] * 0.58)] = False
    gold = cv2.morphologyEx(gold.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((11, 11), np.uint8))
    n, labels, stats, _ = cv2.connectedComponentsWithStats(gold)
    keep = np.zeros_like(gold)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] > 150:
            keep[labels == i] = 1
    contours, _ = cv2.findContours(keep, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    gold = np.zeros_like(keep)
    cv2.drawContours(gold, contours, -1, 1, thickness=-1)
    gold = cv2.dilate(gold, np.ones((3, 3), np.uint8)).astype(np.float32)
    m = cv2.GaussianBlur(gold, (0, 0), 1.5)[..., None]
    lum = a.mean(axis=2, keepdims=True)
    brown = np.concatenate([lum * 0.62 + 40, lum * 0.48 + 28, lum * 0.34 + 18], axis=2)
    out = a * (1 - m) + brown * m
    ys, xs = np.nonzero(gold)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)), (float(np.median(xs)) / a.shape[1], float(np.median(ys)) / a.shape[0])


for take in ["why-ripe-ah", "why-ripe-bh"]:
    lit = shaped(bd.divided(Image.open(ORIG / f"{take}.png").convert("RGB")))
    finished(lit).save(ART / f"{take}-lit.png")
    finished(unripe(lit)).save(ART / f"{take}-unlit.png")
    print(take, "ok")

for take in ["why-seeds-ah", "why-seeds-bh"]:
    lit = shaped(bd.divided(Image.open(ORIG / f"{take}.png").convert("RGB")))
    unlit, at = plain_seeds(lit)
    finished(lit).save(ART / f"{take}-lit.png")
    finished(unlit).save(ART / f"{take}-unlit.png")
    (ART / f"{take}-spread.txt").write_text(f"{at[0]:.4f} {at[1]:.4f}\n", encoding="utf-8")
    print(take, "ok, seeds at", at)

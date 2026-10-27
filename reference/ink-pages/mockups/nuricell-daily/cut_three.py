"""Mockup cuts for NuriCell's How-to-take-it idea A, as ink on a clear ground (black, its alpha the
ink's darkness) so they sit on the page's paper with no box.

  three <repo> <out>          the brushed 3, from the full-size sum original
  whole <repo> <png> <out>    a whole Codex painting: paper divided out, cropped to its ink
"""

import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

mode, repo = sys.argv[1], Path(sys.argv[2])
sys.path.insert(0, str(repo / "reference/ink-pages/about"))
import build_about as bd  # noqa: E402


def to_rgba(grey, keep, out):
    alpha = np.clip((255 - grey.astype(np.float32)) * keep, 0, 255).astype(np.uint8)
    rgba = np.zeros((*alpha.shape, 4), np.uint8)
    rgba[..., 3] = alpha
    Image.fromarray(rgba, "RGBA").save(out)
    print(out, rgba.shape[1], "x", rgba.shape[0])


if mode == "three":
    img = Image.open(repo / "reference/ink-pages/nuricell/originals/gpt25-P7-sum.png").convert("RGB")
    grey = np.asarray(bd.levelled(bd.divided(img)).convert("L"))
    dark = (grey < 150).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(cv2.dilate(dark, np.ones((7, 7), np.uint8)), 8)
    comps = sorted((i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] > 1500), key=lambda i: st[i, 0])
    first = comps[0]
    x, y, w, h = st[first, :4]
    pad = 30
    x0, y0, x1, y1 = x - pad, y - pad, x + w + pad, y + h + pad
    own = (lab[y0:y1, x0:x1] == first).astype(np.uint8) * 255
    keep = cv2.GaussianBlur(cv2.dilate(own, np.ones((21, 21), np.uint8)), (0, 0), 6) / 255
    to_rgba(grey[y0:y1, x0:x1], keep, Path(sys.argv[3]))
else:
    img = Image.open(sys.argv[3]).convert("RGB")
    flat = bd.levelled(bd.divided(img))
    grey = np.asarray(flat.convert("L"))
    box = bd.ink_box(np.asarray(flat), pad=0.04)
    grey = grey[box[1] : box[3], box[0] : box[2]]
    h, w = grey.shape
    f = max(2.0, min(h, w) * 0.05)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    keep = np.clip(np.minimum.reduce([xx, yy, w - 1 - xx, h - 1 - yy]) / f, 0, 1)
    to_rgba(grey, keep, Path(sys.argv[4]))

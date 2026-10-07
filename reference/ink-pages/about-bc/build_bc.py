"""Build the paintings for About B "The album" and C "The circle" (Mo, October 7, 2026).

Originals: reference/ink-pages/about-bc/originals/gpt25-<take>.png (GPT Image 2.5 on rice paper;
prompts in prompts/, spend in reference/ink-pages/spend.md). Output: public/images/about-bc/*.webp
(lossless plates in plates/) and src/components/about/about-art.ts, which both pages import. The
treatments are D's (reference/ink-pages/about/build_about.py): the paper divided out and lifted to
pure white so a painting multiplies onto the page's paper with no box, gold leaf cut out (the
enso's start) or kept as a light mask (build_assets.gold_mask). D's pool and four dots are copied
in, so the pages depend on this folder only.

usage: python -X utf8 reference/ink-pages/about-bc/build_bc.py
"""

import json
import math
import shutil
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "reference/ink-pages/about"))
import build_about as bd  # noqa: E402

ba = bd.ba
OUT = REPO / "public/images/about-bc"
URL = "/images/about-bc"
TS = REPO / "src/components/about/about-art.ts"
# Bump when a shipped picture changes after it has been pushed (the image optimizer caches by URL).
V = "v1"
# The take of each painting that ships (the original's name after "gpt25-").
TAKES = {
    "book": "book-v1",
    "seedling": "seedling-v1",
    "desk": "desk-v1",
    "sequoia": "sequoia-v3",
    "palms": "palms-v1",
    "bee": "bee-v1",
    "moon": "moon-v1",
    "letter": "letter-v2",
    "lamp": "lamp-v1",
    "enso": "enso-v2",
    "hills": "hills-v1",
    "glasses": "glasses-v1",
}
# Takes that ship mirrored left to right. enso-v2 was brushed counter-clockwise (its wet head at
# 12 o'clock with the gold beside it, down the left, drying up the right, lifting at 12:30), but
# the circle page paints it with a clockwise conic sweep from the gold (enso.startDeg): mirrored,
# the sweep follows the brush, wet to dry, instead of painting the dry tail first.
MIRRORED = {"enso-v2"}

# D's helpers read these module globals at call time: point them at this folder.
bd.ORIG = HERE / "originals"
bd.URL = URL
bd.V = V
bd.TAKES = TAKES
ba.OUT = OUT
ba.PLATES = HERE / "plates"
_load = bd.load


def load(take):
    """D's load, with the MIRRORED takes flipped left to right (bd.painting calls bd.load)."""
    img = _load(take)
    return img.transpose(Image.Transpose.FLIP_LEFT_RIGHT) if take in MIRRORED else img


bd.load = load

# Every painting's outer edge fades to white over EDGE of its shorter side. ink_box leaves out the
# outermost 0.1% of the ink, so a pale wash blob or a root tip could run into the crop's edge and
# end in a straight line on the page (desk: a wash cut along the left edge over 22px; seedling:
# roots along the bottom; book, lamp, glasses, sequoia: a few px each). D's letters could not take
# this (their bristle tips run to the edge); these paintings' edges hold only pale wash and tips.
EDGE = 0.03
_levelled = bd.levelled


def levelled(img):
    """D's levelled, with the outer EDGE feathered to white (bd.painting calls bd.levelled)."""
    return bd.feathered(_levelled(img), EDGE)


bd.levelled = levelled


def split_gold(img):
    """D's split_dot, for a gold touch lying on bare paper beside a stroke (the enso's start). D's
    version inpaints the leaf dilated by a 15px kernel; here the stroke's edge runs a few px from
    the leaf, so that hole took 132 px of dark stroke and the inpaint smeared black into it (a
    grey smudge where the gold was), and the cut-out, a box around the leaf, took in the stroke
    beside it. Here the leaf, dilated by an 11px kernel over its torn edge and faint shadow (13
    dark px), is filled with the median of the bare paper around it, and the cut-out keeps only
    that blob."""
    arr = np.asarray(img)
    mask = cv2.morphologyEx(bd.gold_pixels(arr).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(mask, 8)
    if n < 2:
        raise SystemExit("no gold dot found")
    i = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    x, y, w, h = (int(v) for v in st[i, :4])
    blob = cv2.dilate((lab == i).astype(np.uint8), np.ones((11, 11), np.uint8)).astype(bool)
    ring = cv2.dilate(blob.astype(np.uint8), np.ones((41, 41), np.uint8)).astype(bool) & ~blob
    ring &= arr.max(axis=2) > 200  # bare paper only, never the stroke
    clean = arr.copy()
    clean[blob] = np.median(arr[ring], axis=0).astype(np.uint8)
    m = int(max(w, h) * 0.25)
    box = (max(0, x - m), max(0, y - m), min(arr.shape[1], x + w + m), min(arr.shape[0], y + h + m))
    dot = np.asarray(ba.leaf(img.crop(box))).copy()
    keep = cv2.GaussianBlur(blob.astype(np.float32), (0, 0), 2)[box[1] : box[3], box[0] : box[2]]
    dot[..., 3] = np.clip(dot[..., 3] * keep, 0, 255).astype(np.uint8)
    return Image.fromarray(clean), Image.fromarray(dot, "RGBA"), box


bd.split_dot = split_gold


def gilded(key, width, pad=0.04, sat_from=0.3):
    """A painting with gold leaf, and the light mask for the kit's glint over its leaf. `sat_from`
    is gold_mask's saturation floor: pale leaf (the lamp's light, the sequoia's crackled patch)
    needs a lower floor for the mask to cover the leaf rather than only its deepest flakes, as
    long as the mask stays off the ink."""
    art = bd.painting(key, key, width, pad=pad)
    ba.gold_mask(f"{key}-{V}", sat_from=sat_from)
    art["gold"] = f"{URL}/{key}-{V}-gold.webp"
    return art


def vignette(key):
    """A small promise picture: cropped to its ink, its edges feathered to white."""
    img = bd.load(TAKES[key])
    flat = bd.divided(img)
    x0, y0, x1, y1 = bd.ink_box(np.asarray(flat), pad=0.12)
    crop = bd.feathered(bd.levelled(flat.crop((x0, y0, x1, y1))), 0.06)
    return bd.art_of(crop, f"{key}-{V}", 480)


def enso():
    """The circle, its gold start as its own picture, and where the brush began: the angle of the
    gold's centre around the circle's centre (CSS conic degrees, clockwise from 12 o'clock)."""
    art = bd.painting("enso", "enso", 1400, with_dot=True)
    dot = art["dot"]
    w, h = art["width"], art["height"]
    cx = (dot["left"] + dot["size"] / 2) * w
    cy = dot["top"] * h + dot["size"] * w * dot["height"] / dot["width"] / 2
    angle = math.degrees(math.atan2(cx - w / 2, -(cy - h / 2))) % 360
    art["startDeg"] = round(angle, 1)
    return art


def copied(name):
    """One of D's pictures, copied in as it shipped."""
    src = REPO / "public/images/about-ink" / f"{name}-v1.webp"
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, OUT / f"{name}-v1.webp")
    with Image.open(src) as im:
        return {"src": f"{URL}/{name}-v1.webp", "width": im.width, "height": im.height}


def write_ts(entries):
    head = [
        "// Generated by reference/ink-pages/about-bc/build_bc.py. Do not edit by hand: change the",
        "// script (or its TAKES) and run it again. The paintings of About B (the album) and C (the",
        "// circle), October 7, 2026: GPT Image 2.5 on rice paper, the paper divided out so each multiplies",
        "// onto the page's own paper; gold leaf as a light mask (`gold`) or a cut-out (the enso's dot).",
        "",
        "export type Art = { src: string; width: number; height: number };",
        "/** A gold-leaf cut-out, placed by fractions of its painting's width and height. */",
        "export type Dot = Art & { left: number; top: number; size: number };",
        "",
    ]
    body = [f"export const {name} = {json.dumps(value, indent=2)} as const;\n" for name, value in entries]
    TS.write_text("\n".join(head) + "\n".join(body), encoding="utf-8", newline="\n")
    print(TS.relative_to(REPO))


if __name__ == "__main__":
    write_ts(
        [
            ("book", gilded("book", 1400)),
            ("seedling", gilded("seedling", 1200)),
            ("desk", bd.painting("desk", "desk", 1400)),
            # The sequoia's leaf is pale crackled gold: at 0.3 the mask held half the leaf's
            # outline (0.047% of the picture, the outline 0.092%), at 0.25 it holds 0.06% with no
            # alpha over 12 off the leaf; lower floors haze onto the sepia bark (0.15: alpha up to
            # 62 over 1.3% of the picture), where the glint would show.
            ("sequoia", gilded("sequoia", 1200, sat_from=0.25)),
            ("vignettes", {k: vignette(k) for k in ("palms", "bee", "moon", "letter")}),
            # The lamp's leaf is its pale pool of light (saturation 0.2-0.4): at 0.3 the mask held
            # 0.05% of the picture, a few flakes; at 0.2 it holds 0.6%, the crackled flakes in the
            # pool and on the lit page, with nothing on the ink.
            ("lamp", gilded("lamp", 1200, sat_from=0.2)),
            ("enso", enso()),
            # The hills' pale fringes run well past their body: a wide pad keeps them whole.
            ("hills", bd.painting("hills", "hills", 2400, pad=0.2)),
            ("glasses", bd.painting("glasses", "glasses", 1200)),
            ("pool", copied("pool")),
            ("dots", [copied(f"dot-{k}") for k in range(1, 5)]),
        ]
    )

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
import subprocess
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
# The take of each painting that ships (the original's name after "gpt25-"; an original made with
# another tool keeps its whole name, as Codex's oak does).
# The oak replaced the seedling in "Our purpose" (Mo, October 19, 2026: the seedling was too slight
# for the section's weight). The seedling's original stays in originals/; it no longer ships.
TAKES = {
    "book": "book-v1",
    "oak": "codex-oak-v1",
    "desk": "desk-v1",
    "sequoia": "sequoia-v3",
    "palms": "palms-v1",
    "bee": "bee-v1",
    "moon": "moon-v1",
    "letter": "letter-v2",
    "lamp": "lamp-v1",
    # Circle A, "heavy to dry" (Mo, October 19, 2026), in place of gpt25-enso-v2.
    "enso": "codex-enso-v3",
    "hills": "hills-v1",
    "glasses": "glasses-v1",
}
# Takes that ship mirrored left to right, for a circle brushed counter-clockwise: the page paints
# it with a clockwise sweep from its head, so mirrored the sweep follows the brush, wet to dry.
# The first circle (gpt25-enso-v2) shipped mirrored; circle A was brushed clockwise.
MIRRORED: set[str] = set()
# The circle's own version: bumped when circle A replaced the first (the image optimizer caches by
# URL). The gold flake keeps the first circle's enso-dot-v1.webp.
V2 = "v2"

# D's helpers read these module globals at call time: point them at this folder.
bd.ORIG = HERE / "originals"
bd.URL = URL
bd.V = V
bd.TAKES = TAKES
ba.OUT = OUT
ba.PLATES = HERE / "plates"
_load = bd.load


def load(take):
    """D's load, with the MIRRORED takes flipped left to right (bd.painting calls bd.load). An
    original named in full (codex-oak-v1.png) is read as it is."""
    own = bd.ORIG / f"{take}.png"
    img = Image.open(own).convert("RGB") if own.exists() else _load(take)
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
    """The circle (Mo, October 19, 2026: circle A, "heavy to dry", in place of the first circle,
    which was "too round, not artistic enough"). It was painted without gold: the gold leaf is the
    first circle's own flake (enso-dot-v1.webp, kept as it shipped), laid half on the stroke's
    outer edge just after its wet head. Also where the brush began, for the page's clockwise sweep
    (sweepDeg, CSS conic degrees clockwise from 12 o'clock round the picture's centre, a hair
    before the head), and the angle of the leaf's centre (startDeg).

    The head is found, not typed in: the stroke's gap (the longest run of near-bare degrees round
    a circle fitted to the ink), and of its two sides the one with the denser ink over 40 degrees
    is the wet head. The page sweeps clockwise from the head, so a take brushed the other way
    (its head counter-clockwise of the gap) stops the build: mirror it in MIRRORED."""
    img = bd.load(TAKES["enso"])
    flat = bd.divided(img)
    x0, y0, x1, y1 = bd.ink_box(np.asarray(flat), pad=0.07)
    # bd.levelled is this folder's: levelled, then its outer EDGE feathered to white.
    art = bd.art_of(bd.levelled(flat.crop((x0, y0, x1, y1))), f"enso-{V2}", 1400)
    with Image.open(OUT / f"enso-{V2}.webp") as im:
        a = 1 - np.asarray(im.convert("L")).astype(np.float32) / 255
    h, w = a.shape
    ys, xs = np.nonzero(a > 0.5)
    x, y = xs.astype(np.float64), ys.astype(np.float64)
    (cx, cy, c), *_ = np.linalg.lstsq(np.c_[2 * x, 2 * y, np.ones_like(x)], x * x + y * y, rcond=None)
    r0 = math.sqrt(c + cx * cx + cy * cy)
    rs = np.linspace(0.45 * r0, 1.45 * r0, 300)
    mass, dense, outer = [], [], []
    for deg in range(360):
        t = math.radians(deg)
        px = np.clip((cx + np.sin(t) * rs).astype(int), 0, w - 1)
        py = np.clip((cy - np.cos(t) * rs).astype(int), 0, h - 1)
        v = a[py, px]
        mass.append(float(v.sum()))
        dense.append(float((v > 0.8).sum()))
        inked = rs[v > 0.35]
        outer.append(float(inked.max()) if len(inked) else r0)
    mass = np.array(mass)
    smooth = np.convolve(np.r_[mass[-5:], mass, mass[:5]], np.ones(11) / 11, mode="same")[5:-5]
    bare = smooth < np.median(smooth) / 6
    best, run, first = (0, 0, 0), 0, 0
    for i in range(720):
        if bare[i % 360]:
            first = i if run == 0 else first
            run += 1
            if run > best[0]:
                best = (run, first % 360, i % 360)
        else:
            run = 0
    if best[0] < 8:
        raise SystemExit(f"enso: no gap where the brush lifted ({best[0]} bare degrees)")
    _, gap_from, gap_to = best
    after = sum(dense[(gap_to + k) % 360] for k in range(1, 41))
    before = sum(dense[(gap_from - k) % 360] for k in range(1, 41))
    if before > after:
        raise SystemExit("enso: brushed counter-clockwise (its head is before the gap): mirror it")
    head = (gap_to + 1) % 360
    # The leaf: centred on the stroke's outer edge 23 degrees after the head, so the sweep, which
    # starts 3 degrees before the head, still begins 26 degrees before the leaf as it always has.
    leaf_deg = (head + 23) % 360
    t = math.radians(leaf_deg)
    lr = outer[leaf_deg] + 0.005 * w
    size = 0.1513  # the leaf's width as a share of the circle's picture, as before
    with Image.open(OUT / "enso-dot-v1.webp") as dot:
        dw, dh = dot.size
    lw = size * w
    lh = lw * dh / dw
    lx, ly = cx + math.sin(t) * lr, cy - math.cos(t) * lr
    art["dot"] = {
        "src": f"{URL}/enso-dot-v1.webp",
        "width": dw,
        "height": dh,
        "left": round((lx - lw / 2) / w, 4),
        "top": round((ly - lh / 2) / h, 4),
        "size": size,
    }
    def around_middle(px, py):
        return math.degrees(math.atan2(px - w / 2, -(py - h / 2))) % 360

    head_x, head_y = cx + math.sin(math.radians(head)) * r0, cy - math.cos(math.radians(head)) * r0
    art["sweepDeg"] = round(around_middle(head_x, head_y) - 3, 1)
    art["startDeg"] = round(around_middle(lx, ly), 1)
    return art


def copied(name):
    """One of D's pictures, as it shipped. It was copied in from D's folder
    (public/images/about-ink), which left the repo when these pages took their own: the copy here
    is now the source, and D's folder is read only if the copy is missing."""
    dst = OUT / f"{name}-v1.webp"
    if not dst.exists():
        OUT.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REPO / "public/images/about-ink" / f"{name}-v1.webp", dst)
    with Image.open(dst) as im:
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
    # In the repo's own format (format:check reads it), so a run that changes nothing leaves the
    # committed file as it is: Prettier from the repo's node_modules.
    prettier = REPO / "node_modules/prettier/bin/prettier.cjs"
    subprocess.run(["node", str(prettier), "--write", str(TS)], cwd=REPO, check=True, capture_output=True)
    print(TS.relative_to(REPO))


if __name__ == "__main__":
    write_ts(
        [
            ("book", gilded("book", 1400)),
            # The oak's gold is a pale glow at the root heart: at 0.3 the mask held its brightest flakes
            # (0.41% of the picture); at 0.22 it holds the glow, with nothing on the grey ink.
            ("oak", gilded("oak", 1200, sat_from=0.22)),
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

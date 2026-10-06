"""Build the About page's paintings ("The name, on a folded letter", Mo's design D, October 6, 2026).

Originals: reference/ink-pages/about/originals/gpt25-<take>.png (GPT Image 2.5 on rice paper; prompts
in prompts/, spend in reference/ink-pages/spend.md). Output: public/images/about-ink/*.webp (lossless
plates in plates/), the brush wipe mask wipe-<V>.png, and src/components/about/letter-art.ts (sizes
and the gold dots' places), which the page imports. The treatments are the homepage's
(reference/home-v2/ink/build_assets.py): the paper divided out so a painting multiplies onto the
page's own paper, gold leaf cut out with its torn edge, and the gold-leaf light mask.

usage: python -X utf8 reference/ink-pages/about/build_about.py
"""

import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "reference/home-v2/ink"))
import build_assets as ba  # noqa: E402

ORIG = HERE / "originals"
OUT = REPO / "public/images/about-ink"
ba.OUT = OUT  # ba.save and ba.gold_mask write here (module globals, read at call time)
ba.PLATES = HERE / "plates"
URL = "/images/about-ink"
TS = REPO / "src/components/about/letter-art.ts"
# Bump when a shipped picture changes: the image optimizer caches by URL.
V = "v1"
# The take of each painting that ships (the original's name after "gpt25-").
TAKES = {
    "word": "word-v1",
    "B": "letter-b-v1",
    "i": "letter-i-v1",
    "G": "letter-g-v1",
    "H": "letter-h-v1",
    "band": "band-v1",
    "pool": "pool-v1",
    "rings": "rings-v2",
    "dots": "dots-v1",
}
# The shared rice-paper tile, aged a little for this page (warmer, never dirty).
TINT = (247, 239, 226)


def load(take):
    return Image.open(ORIG / f"gpt25-{take}.png").convert("RGB")


def divided(img):
    """Paper -> white, ink kept. The paper colour is the median of the picture's outer frame."""
    arr = np.asarray(img).astype(np.float32)
    h, w, _ = arr.shape
    fh, fw = max(h // 20, 1), max(w // 20, 1)
    frame = np.concatenate(
        [arr[:fh].reshape(-1, 3), arr[-fh:].reshape(-1, 3), arr[:, :fw].reshape(-1, 3), arr[:, -fw:].reshape(-1, 3)]
    )
    paper = np.median(frame, axis=0)
    return Image.fromarray(np.clip(arr / paper * 255.0, 0, 255).astype(np.uint8))


def ink_mask(arr, level, sigma=12):
    """Where the ink is on a divided picture: its darkest channel under `level`, measured on a
    blurred copy. The rice paper's own dark fibres and creases (0.5-2% of bare paper falls under
    236) are scattered over the whole sheet; the blur averages them back to paper (bare paper stays
    at 241 or lighter) while strokes and washes stay dark."""
    return cv2.GaussianBlur(arr.min(axis=2), (0, 0), sigma) < level


def ink_box(arr, level=236, pad=0.04):
    """The box around the ink on a divided picture (ink_mask), padded by `pad` of its size;
    stray specks outside the 0.1-99.9 percentiles are ignored."""
    h, w, _ = arr.shape
    ys, xs = np.nonzero(ink_mask(arr, level))
    if not len(xs):
        raise SystemExit("no ink found")
    x0, x1 = np.percentile(xs, [0.1, 99.9])
    y0, y1 = np.percentile(ys, [0.1, 99.9])
    pw, ph = (x1 - x0) * pad, (y1 - y0) * pad
    return int(max(0, x0 - pw)), int(max(0, y0 - ph)), int(min(w, x1 + pw)), int(min(h, y1 + ph))


def gold_pixels(arr):
    """Gold leaf: warm, clearly saturated, bright enough (the test ba.gold_mask uses)."""
    a = arr.astype(np.float32) / 255
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    hi, lo = a.max(axis=2), a.min(axis=2)
    sat = (hi - lo) / np.maximum(hi, 1e-4)
    warm = (r >= g) & (g > b)
    hue = np.where(warm, 60 * (g - b) / np.maximum(hi - lo, 1e-4), 0)
    return warm & (hue > 22) & (hue < 60) & (sat > 0.3) & (hi > 0.3)


def split_dot(img):
    """Lift the gold-leaf dot out of a painting. Returns (painting with paper where the dot was,
    the dot as a gold-leaf cut-out, the cut-out's box in the painting)."""
    arr = np.asarray(img)
    mask = cv2.morphologyEx(gold_pixels(arr).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(mask, 8)
    if n < 2:
        raise SystemExit("no gold dot found")
    i = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    x, y, w, h = (int(v) for v in st[i, :4])
    blob = cv2.dilate((lab == i).astype(np.uint8) * 255, np.ones((15, 15), np.uint8))
    clean = cv2.inpaint(arr, blob, 7, cv2.INPAINT_TELEA)
    m = int(max(w, h) * 0.25)
    box = (max(0, x - m), max(0, y - m), min(arr.shape[1], x + w + m), min(arr.shape[0], y + h + m))
    return Image.fromarray(clean), ba.leaf(img.crop(box)), box


def art_of(img, name, width):
    """Save a picture through ba.save and describe it as it ships (its size after the resize)."""
    ba.save(img, name, width, 86)
    s = min(1.0, width / img.width) if width else 1.0
    return {"src": f"{URL}/{name}.webp", "width": round(img.width * s), "height": round(img.height * s)}


def painting(key, name, width, with_dot=False, pad=0.04):
    """A painting cropped to its ink (and its gold dot, kept in its own picture)."""
    img = load(TAKES[key])
    if with_dot:
        img, dot, dbox = split_dot(img)
    flat = divided(img)
    x0, y0, x1, y1 = ink_box(np.asarray(flat), pad=pad)
    if with_dot:
        x0, y0, x1, y1 = min(x0, dbox[0]), min(y0, dbox[1]), max(x1, dbox[2]), max(y1, dbox[3])
    crop = flat.crop((x0, y0, x1, y1))
    art = art_of(crop, f"{name}-{V}", width)
    if with_dot:
        ba.save(dot, f"{name}-dot-{V}", None, 88)
        art["dot"] = {
            "src": f"{URL}/{name}-dot-{V}.webp",
            "width": dot.width,
            "height": dot.height,
            "left": round((dbox[0] - x0) / crop.width, 4),
            "top": round((dbox[1] - y0) / crop.height, 4),
            "size": round((dbox[2] - dbox[0]) / crop.width, 4),
        }
    return art


def feathered(img, frac=0.03):
    """Fade a picture's outer edge to white over `frac` of its shorter side, so the faint paper
    fibres left after dividing stop softly and no rectangle shows when it multiplies onto the
    page (as build_assets.lift_cranes does for the cranes). Only for crops with a wide paper
    margin (the dots): on the letters it would fade bristle tips that run near the crop's edge."""
    arr = np.asarray(img).astype(np.float32)
    h, w = arr.shape[:2]
    f = max(2.0, min(h, w) * frac)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    keep = np.clip(np.minimum.reduce([xx, yy, w - 1 - xx, h - 1 - yy]) / f, 0, 1)[..., None]
    return Image.fromarray((arr * keep + 255 * (1 - keep)).astype(np.uint8))


def dots_sheet():
    """The four watercolor dots, from one painting: the four largest marks, left to right, each
    with its edge feathered to white (a paper fibre in a corner would otherwise show)."""
    flat = divided(load(TAKES["dots"]))
    arr = np.asarray(flat)
    marks = cv2.morphologyEx(ink_mask(arr, 242).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    n, _, st, _ = cv2.connectedComponentsWithStats(marks, 8)
    big = sorted(range(1, n), key=lambda i: -st[i, cv2.CC_STAT_AREA])[:4]
    if len(big) < 4:
        raise SystemExit(f"found {len(big)} dots, want 4")
    out = []
    for k, i in enumerate(sorted(big, key=lambda i: st[i, 0]), 1):
        x, y, w, h = (int(v) for v in st[i, :4])
        m = int(max(w, h) * 0.18)
        crop = flat.crop((max(0, x - m), max(0, y - m), min(arr.shape[1], x + w + m), min(arr.shape[0], y + h + m)))
        out.append(art_of(feathered(crop), f"dot-{k}-{V}", 360))
    return out


def paper_aged():
    """The shared paper tile multiplied by TINT (a constant, so it still repeats without a seam)."""
    tile = np.asarray(Image.open(REPO / "public/images/home-v2/ink/paper.webp").convert("RGB")).astype(np.float32)
    aged = np.clip(tile * (np.array(TINT, np.float32) / 255), 0, 255).astype(np.uint8)
    ba.save(Image.fromarray(aged), f"paper-aged-{V}", 1600, 80)
    median = np.median(aged.reshape(-1, 3), axis=0).astype(int)
    print("paper-aged median: #%02x%02x%02x  (about-letter.module.css --paper)" % tuple(median))
    return f"{URL}/paper-aged-{V}.webp"


def wipe(width=1536, height=256, seed=11):
    """The brush wipe the letters are written through: opaque on the left 36%, transparent on the
    right 36%, and between them a dry brush's ragged edge (each row ends at its own place, a few
    bristles run ahead). At mask-size 300% 100%, moving it from 100% to 0% writes left to right."""
    rng = np.random.default_rng(seed)
    xs = np.arange(width, dtype=np.float32) / width
    rows = np.arange(height, dtype=np.float32) / height
    wobble = sum(np.sin(rows * np.pi * f + rng.uniform(0, 6.28)) / f for f in (2, 5, 11, 23))
    edge = 0.5 + 0.035 * wobble + rng.random(height).astype(np.float32) ** 6 * 0.06
    alpha = np.clip((edge[:, None] - xs[None, :]) / 0.03 + 0.5, 0, 1)
    alpha[:, : int(width * 0.36)] = 1
    alpha[:, int(width * 0.64) :] = 0
    a = Image.fromarray((alpha * 255).astype(np.uint8), "L")
    OUT.mkdir(parents=True, exist_ok=True)
    Image.merge("RGBA", (a, a, a, a)).save(OUT / f"wipe-{V}.png", optimize=True)
    print(f"public/images/about-ink/wipe-{V}.png")
    return f"{URL}/wipe-{V}.png"


def write_ts(entries):
    head = [
        "// Generated by reference/ink-pages/about/build_about.py. Do not edit by hand: change the",
        "// script (or its TAKES) and run it again. The About page's paintings (Mo's design D, October 6,",
        "// 2026): GPT Image 2.5 on rice paper, the paper divided out so each multiplies onto the page's",
        "// own paper; gold leaf as cut-out pictures (the dots of the i) and as a light mask (the rings).",
        "",
        "export type Art = { src: string; width: number; height: number };",
        "/** A gold-leaf dot: its own picture, placed by fractions of its painting's width and height. */",
        "export type Dot = Art & { left: number; top: number; size: number };",
        "",
    ]
    body = [f"export const {name} = {json.dumps(value, indent=2)} as const;\n" for name, value in entries]
    TS.write_text("\n".join(head) + "\n".join(body), encoding="utf-8", newline="\n")
    print(TS.relative_to(REPO))


if __name__ == "__main__":
    rings = painting("rings", "rings", 1400)
    ba.gold_mask(f"rings-{V}", sat_from=0.3)
    rings["gold"] = f"{URL}/rings-{V}-gold.webp"
    write_ts(
        [
            ("paperAged", paper_aged()),
            ("wipe", wipe()),
            ("word", painting("word", "word", 1800, with_dot=True)),
            (
                "letters",
                {
                    "B": painting("B", "letter-b", 900),
                    "i": painting("i", "letter-i", 700, with_dot=True),
                    "G": painting("G", "letter-g", 900),
                    "H": painting("H", "letter-h", 1100),
                },
            ),
            # The band's pale fringes (paler than ink_mask's level) run ~20% of its height past
            # its body and to near the sheet's ends: a wider pad keeps them, so no edge cuts the wash.
            ("band", painting("band", "band", 2400, pad=0.2)),
            ("pool", painting("pool", "pool", 1200)),
            ("rings", rings),
            ("dots", dots_sheet()),
        ]
    )

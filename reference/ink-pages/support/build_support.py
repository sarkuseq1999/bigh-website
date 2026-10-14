"""Build the Support page's paintings (Mo, October 14, 2026; mockup A, "Pull up a chair").

Originals: reference/ink-pages/support/originals/gpt25-<take>.png (GPT Image 2.5 on rice paper,
the homepage crane as the brushwork reference; prompts in prompts/, spend in
reference/ink-pages/spend-support.md). Output: public/images/support/*.webp and
src/components/support/support-art.ts. The treatments are About's (build_about.py): the paper
divided out and lifted to pure white, so a painting multiplies onto the page's paper with no box.
Each gold steam (the porch's, the cup's) is lifted out into its own picture (the page lets it
rise). The thank-you's cup is its own painting (a-cup-v1, October 14), not a cut of the porch: a
cut at the porch's pixel size was soft on a 2x screen and its table ended in a straight edge.

usage: python -X utf8 reference/ink-pages/support/build_support.py
"""

import json
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
OUT = REPO / "public/images/support"
URL = "/images/support"
TS = REPO / "src/components/support/support-art.ts"
# Bump when a shipped picture changes after it has been pushed (the image optimizer caches by URL).
V = "v1"
TAKES = {"porch": "a-porch-v2", "cup": "a-cup-v1", "mailbox": "a-mailbox", "parcel": "a-parcel", "book": "a-book-v2"}
# The cup is a new painting (its pictures are named v2: the first cup, a crop of the porch, was
# cup-v1, and the image optimizer caches by URL).
CUP_V = "v2"
# The cup is shown at most this wide on the page (support-page.module.css .cup); its plate must be at
# least twice that wide to stay crisp on a 2x screen (check_support.py).
CUP_CSS_WIDTH = 220

bd.ORIG = HERE / "originals"
bd.URL = URL
bd.V = V
bd.TAKES = TAKES
ba.OUT = OUT
ba.PLATES = HERE / "plates"

# Every painting's outer edge fades to white over EDGE of its shorter side (as build_bc.py does).
# ink_box leaves out the outermost 0.1% of the ink, so a stray wash or fibre speck can run into the
# crop's edge and end in a straight line on the page (the first build: mailbox edge down to 126 of
# 255, book 218, parcel 227, against the check's 238).
EDGE = 0.03
_levelled = bd.levelled


def levelled(img):
    """About's levelled, with the outer EDGE feathered to white (bd.painting calls bd.levelled)."""
    return bd.feathered(_levelled(img), EDGE)


bd.levelled = levelled


def split_steam(img):
    """Lift every gold flake of the steam out of the painting. Returns (painting with paper where
    the steam was, the steam as a transparent gold-leaf picture, its box on the original). The
    steam is many small flakes, so all of them are kept (About's split_dot keeps one blob)."""
    arr = np.asarray(img.convert("RGB"))
    # Bright gold only: gold_pixels alone also matches the warm dark ink of the porch's wood
    # (brightness 0.31-0.44, 2000 px, 700 specks over the whole picture), while the steam's leaf is
    # 0.70-0.97 bright (measured on a-porch-v2). A floor of 140 of 255 splits the two cleanly.
    gold = bd.gold_pixels(arr) & (arr.max(axis=2) > 140)
    mask = cv2.morphologyEx(gold.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(mask, 8)
    keep = np.zeros_like(mask, dtype=bool)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] >= 12:
            keep |= lab == i
    if keep.sum() < 200:
        raise SystemExit("no steam found")
    blob = cv2.dilate(keep.astype(np.uint8), np.ones((9, 9), np.uint8)).astype(bool)
    ring = cv2.dilate(blob.astype(np.uint8), np.ones((41, 41), np.uint8)).astype(bool) & ~blob
    ring &= arr.max(axis=2) > 200  # bare paper only, never the cup or the rail
    clean = arr.copy()
    clean[blob] = np.median(arr[ring], axis=0).astype(np.uint8)
    ys, xs = np.where(blob)
    m = 12
    box = (max(0, xs.min() - m), max(0, ys.min() - m), min(arr.shape[1], xs.max() + m), min(arr.shape[0], ys.max() + m))
    steam = np.asarray(ba.leaf(img.convert("RGB").crop(box))).copy()
    soft = cv2.GaussianBlur(blob.astype(np.float32), (0, 0), 2)[box[1] : box[3], box[0] : box[2]]
    steam[..., 3] = np.clip(steam[..., 3] * soft, 0, 255).astype(np.uint8)
    return Image.fromarray(clean), Image.fromarray(steam, "RGBA"), box


def placed(steam_box, crop_box, crop_w, crop_h, steam, src):
    """Where the steam stands on a picture cropped at crop_box (fractions, as the page reads them)."""
    return {
        "src": src,
        "width": steam.width,
        "height": steam.height,
        "left": round((steam_box[0] - crop_box[0]) / crop_w, 4),
        "top": round((steam_box[1] - crop_box[1]) / crop_h, 4),
        "size": round((steam_box[2] - steam_box[0]) / crop_w, 4),
    }


def porch():
    img = bd.load(TAKES["porch"])
    clean, steam, sbox = split_steam(img)
    ba.save(steam, f"porch-steam-{V}", None, 90)
    flat = bd.divided(clean)
    # The porch: cropped to its ink (and its steam), the outer edge feathered to white.
    x0, y0, x1, y1 = bd.ink_box(np.asarray(flat), pad=0.04)
    x0, y0, x1, y1 = min(x0, sbox[0]), min(y0, sbox[1]), max(x1, sbox[2]), max(y1, sbox[3])
    crop = bd.levelled(flat.crop((x0, y0, x1, y1)))  # levelled above also feathers the outer edge
    art = bd.art_of(crop, f"porch-{V}", 1640)
    art["steam"] = placed(sbox, (x0, y0), crop.width, crop.height, steam, f"{URL}/porch-steam-{V}.webp")
    return art


def cup():
    """The thank-you's cup: one painting (cup, saucer and a pale shadow stroke) with its own gold
    steam, cropped to its ink and its steam. Shipped at CUP_CSS_WIDTH x 2.5 or wider."""
    img = bd.load(TAKES["cup"])
    clean, steam, sbox = split_steam(img)
    ba.save(steam, f"cup-steam-{CUP_V}", None, 90)
    flat = bd.divided(clean)
    x0, y0, x1, y1 = bd.ink_box(np.asarray(flat), pad=0.04)
    x0, y0, x1, y1 = min(x0, sbox[0]), min(y0, sbox[1]), max(x1, sbox[2]), max(y1, sbox[3])
    crop = bd.levelled(flat.crop((x0, y0, x1, y1)))
    art = bd.art_of(crop, f"cup-{CUP_V}", round(CUP_CSS_WIDTH * 2.5))
    art["steam"] = placed(sbox, (x0, y0), crop.width, crop.height, steam, f"{URL}/cup-steam-{CUP_V}.webp")
    return art


def write_ts(entries):
    head = [
        "// Generated by reference/ink-pages/support/build_support.py. Do not edit by hand: change the",
        "// script (or its TAKES) and run it again. The Support page's paintings (October 14, 2026): GPT",
        "// Image 2.5 on rice paper, the paper divided out so each multiplies onto the page's own paper;",
        "// the porch's and the cup's gold steam as their own pictures (`steam`), placed by fractions of",
        "// their painting.",
        "",
        "export type Art = { src: string; width: number; height: number };",
        "/** The gold steam, placed by fractions of its painting's width (left, size) and height (top). */",
        "export type Steam = Art & { left: number; top: number; size: number };",
        "",
        "",
    ]
    body = [f"export const {name} = {json.dumps(value, indent=2)} as const;\n" for name, value in entries]
    TS.parent.mkdir(parents=True, exist_ok=True)
    TS.write_text("\n".join(head) + "\n".join(body), encoding="utf-8", newline="\n")
    prettier = REPO / "node_modules/prettier/bin/prettier.cjs"
    subprocess.run(["node", str(prettier), "--write", str(TS)], cwd=REPO, check=True, capture_output=True)
    print(TS.relative_to(REPO))


if __name__ == "__main__":
    write_ts(
        [
            ("porch", porch()),
            ("cup", cup()),
            ("mailbox", bd.painting("mailbox", "mailbox", 1100)),
            ("parcel", bd.painting("parcel", "parcel", 1100)),
            ("book", bd.painting("book", "book", 1100)),
        ]
    )

"""Build the Support page's paintings (Mo, October 14, 2026; mockup A, "Pull up a chair").

Originals: reference/ink-pages/support/originals/gpt25-<take>.png (GPT Image 2.5 on rice paper,
the homepage crane as the brushwork reference; prompts in prompts/, spend in
reference/ink-pages/spend-support.md). Output: public/images/support/*.webp and
src/components/support/support-art.ts. The treatments are About's (build_about.py): the paper
divided out and lifted to pure white, so a painting multiplies onto the page's paper with no box.
The porch's gold steam is lifted out into its own picture (the page lets it rise), and the cup with
its steam is cut from the same painting for the thank-you.

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
TAKES = {"porch": "a-porch-v2", "mailbox": "a-mailbox", "parcel": "a-parcel", "book": "a-book-v2"}
# The cup, its saucer, the table's top and the steam over it, on the porch original (2048x1360).
# The mockup round's box (850, 470, 1110, 840) took in the right chair's arm (from x 1062) and cut
# the table's legs off at a straight edge; this one (measured on a 40 px grid of the original) stops
# short of both: the table top runs x 865-1045, y 790-830, the cup x 925-990, y 735-790, the legs
# end near y 975 and are faded out below the top.
CUP_BOX = (868, 505, 1050, 880)

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


def placed(steam_box, crop_box, crop_w, crop_h, steam):
    """Where the steam stands on a picture cropped at crop_box (fractions, as the page reads them)."""
    return {
        "src": f"{URL}/porch-steam-{V}.webp",
        "width": steam.width,
        "height": steam.height,
        "left": round((steam_box[0] - crop_box[0]) / crop_w, 4),
        "top": round((steam_box[1] - crop_box[1]) / crop_h, 4),
        "size": round((steam_box[2] - steam_box[0]) / crop_w, 4),
    }


def porch_and_cup():
    img = bd.load(TAKES["porch"])
    clean, steam, sbox = split_steam(img)
    ba.save(steam, f"porch-steam-{V}", None, 90)
    flat = bd.divided(clean)
    # The porch: cropped to its ink (and its steam), the outer edge feathered to white.
    x0, y0, x1, y1 = bd.ink_box(np.asarray(flat), pad=0.04)
    x0, y0, x1, y1 = min(x0, sbox[0]), min(y0, sbox[1]), max(x1, sbox[2]), max(y1, sbox[3])
    crop = bd.levelled(flat.crop((x0, y0, x1, y1)))  # levelled above also feathers the outer edge
    porch = bd.art_of(crop, f"porch-{V}", 1640)
    porch["steam"] = placed(sbox, (x0, y0), crop.width, crop.height, steam)
    # The cup: the hills and the rail behind it are pale washes, lifted to white; what is darker
    # (the rail's ends, the chair arms, the table's legs) fades out with an oval around the cup that
    # reaches up to a little above its rim and only a little below the table's top, so only the cup,
    # its saucer and the table's top remain, with no straight cut anywhere.
    cb = (min(CUP_BOX[0], sbox[0]), min(CUP_BOX[1], sbox[1]), max(CUP_BOX[2], sbox[2]), max(CUP_BOX[3], sbox[3]))
    cup_arr = np.asarray(_levelled(flat.crop(cb))).astype(np.float32)
    cup_arr = np.where(cup_arr.mean(axis=2, keepdims=True) > 190, 255, cup_arr)
    h, w = cup_arr.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    cy = 797 - cb[1]  # the table top's level in the crop
    ry = np.where(yy < cy, 95.0, 75.0)
    d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - cy) / ry) ** 2)
    k = np.clip((1.0 - d) / 0.3, 0, 1)[..., None]
    cup_img = Image.fromarray((255 - (255 - cup_arr) * k).astype(np.uint8))
    cup = bd.art_of(cup_img, f"cup-{V}", 600)
    cup["steam"] = placed(sbox, cb, cup_img.width, cup_img.height, steam)
    return porch, cup


def write_ts(entries):
    head = [
        "// Generated by reference/ink-pages/support/build_support.py. Do not edit by hand: change the",
        "// script (or its TAKES) and run it again. The Support page's paintings (October 14, 2026): GPT",
        "// Image 2.5 on rice paper, the paper divided out so each multiplies onto the page's own paper;",
        "// the porch's gold steam as its own picture (`steam`), placed by fractions of its painting.",
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
    porch, cup = porch_and_cup()
    write_ts(
        [
            ("porch", porch),
            ("cup", cup),
            ("mailbox", bd.painting("mailbox", "mailbox", 1100)),
            ("parcel", bd.painting("parcel", "parcel", 1100)),
            ("book", bd.painting("book", "book", 1100)),
        ]
    )

"""Build the moving gold of NuriCell's "What's inside" chapter (Mo picked 1A, October 26, 2026;
mockups reference/ink-pages/mockups/nuricell-inside/).

From the shipped capsule painting (capsule-v1.webp, made by build_nuricell.py, paper divided out so
white is paper) this cuts:
- capsule-ink-v1.webp: the painting with its gold leaf taken out (the two capsule halves, the four
  heaps and their ground), the same size, so it lies exactly where the painting lies;
- capsule-leaf-v1.webp: every flake of the leaf (connected pieces of gold), packed on one sheet in
  three bands, as painted, catching the light (brighter) and turned away (darker), so the page can
  draw each flake on its own and fade between them as it turns;
- capsule-gold-v1.webp: the leaf alone where it is painted (a see-through layer the size of the
  painting), shown where nothing moves (no script, reduced motion).
From the full-size original (originals/gpt25-P7-capsule.png, paper divided by its own colour):
- heap-<ingredient>-v1.webp: the four powder heaps, each on its own, sides and ground faded, for the
  teamwork scenes. They are sized by amount: two at 400 mg, then 200 mg, then 100 mg.
Every cut-out is un-multiplied from white (a colour over paper becomes that colour with an alpha), so
it sits on any paper and can move without a blend group round it.
Writes src/components/product/ink/nuricell-gold.ts.

usage: python -X utf8 reference/ink-pages/nuricell/build_nuricell_gold.py
"""

import json
import subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageFilter

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
OUT = REPO / "public/images/products/nuricell/ink"
URL = "/images/products/nuricell/ink"
TS = REPO / "src/components/product/ink/nuricell-gold.ts"
V = "v1"
# The bands of the leaf sheet: as painted, catching the light, turned away.
LIGHT = (1.0, 1.42, 0.8)
# The heaps in the original, by ingredient (left, top, right, bottom).
HEAPS = {
    "alcar": (528, 1545, 850, 1772),
    "creatine": (832, 1590, 1170, 1768),
    "ala": (1150, 1612, 1398, 1770),
    "choline": (1380, 1650, 1556, 1768),
}
# Each heap's tip in the shipped painting (fractions of its width and height), left to right:
# where the leaf rises from.
TIPS = [[0.335, 0.86], [0.47, 0.865], [0.625, 0.89], [0.717, 0.91]]


def unmultiplied(c, a):
    """A colour over white with this alpha, as the colour itself (so alpha over paper matches)."""
    return np.clip(255 - (255 - c) / np.maximum(a, 0.06)[..., None], 0, 255)


def save(arr, name, lossless=False):
    path = OUT / f"{name}-{V}.webp"
    mode = "RGBA" if arr.shape[2] == 4 else "RGB"
    Image.fromarray(arr.astype(np.uint8), mode).save(path, "WEBP", quality=90, method=6, lossless=lossless)
    print(f"{path.relative_to(REPO)}  {arr.shape[1]}x{arr.shape[0]}  {path.stat().st_size // 1024} KB")
    return f"{URL}/{name}-{V}.webp"


def leaf():
    img = np.asarray(Image.open(OUT / "capsule-v1.webp").convert("RGB")).astype(np.float32)
    H, W = img.shape[:2]
    hsv = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float32)
    hue = hsv[..., 0] * 2
    # Gold: warm with real colour (chroma, not HSV saturation, which jumps on dark ink), and only in
    # the band the leaf rises through (the capsule halves' dark rims are faintly warm too).
    chroma = img.max(axis=2) - img.min(axis=2)
    band = np.zeros((H, W), bool)
    band[:, int(W * 0.24) : int(W * 0.76)] = True
    soft = np.clip((chroma - 22) / 40, 0, 1) * ((hue > 15) & (hue < 62)) * band
    core = cv2.morphologyEx((soft > 0.5).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    filled = core.copy()
    contours, _ = cv2.findContours(core, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(filled, contours, -1, 1, thickness=-1)  # pale highlights inside a flake
    alpha = np.maximum(soft, cv2.erode(filled, np.ones((2, 2), np.uint8)).astype(np.float32))

    # The painting without its leaf: every gold pixel and a 2px ring back to paper.
    ink = img.copy()
    ink[cv2.dilate(((alpha > 0.04) * 255).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0] = 255
    ink_url = save(ink, "capsule-ink")
    gold_url = save(np.dstack([unmultiplied(img, alpha), alpha * 255]), "capsule-gold")

    # The flakes, biggest first.
    n, lab, stats, _ = cv2.connectedComponentsWithStats((alpha > 0.2).astype(np.uint8), 8)
    pad = 3
    pieces = []
    for i in range(1, n):
        x, y, w, h, area = stats[i]
        if area < 5:
            continue
        x0, y0, x1, y1 = max(0, x - pad), max(0, y - pad), min(W, x + w + pad), min(H, y + h + pad)
        own = cv2.dilate((lab[y0:y1, x0:x1] == i).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
        a = alpha[y0:y1, x0:x1] * own
        pieces.append((int(area), (x0, y0, x1, y1), np.dstack([unmultiplied(img[y0:y1, x0:x1], a), a * 255])))
    pieces.sort(key=lambda p: -p[0])

    # Shelf-pack them on a sheet 512px wide, then stack the three bands of light.
    sheet_w, gap, cx, cy, row_h, spots = 512, 2, 0, 0, 0, []
    for _, _, rgba in sorted(pieces, key=lambda p: -p[2].shape[0]):
        h, w = rgba.shape[:2]
        if cx + w > sheet_w:
            cx, cy, row_h = 0, cy + row_h + gap, 0
        spots.append((cx, cy))
        cx, row_h = cx + w + gap, max(row_h, h)
    band_h = cy + row_h
    sheet = np.zeros((band_h * 3 + gap * 2, sheet_w, 4), np.float32)
    flakes = []
    by_height = sorted(range(len(pieces)), key=lambda k: -pieces[k][2].shape[0])
    place = {k: spots[j] for j, k in enumerate(by_height)}
    for k, (_, (x0, y0, x1, y1), rgba) in enumerate(pieces):
        sx, sy = place[k]
        h, w = rgba.shape[:2]
        for b, light in enumerate(LIGHT):
            top = sy + b * (band_h + gap)
            sheet[top : top + h, sx : sx + w, :3] = np.clip(rgba[..., :3] * light, 0, 255)
            sheet[top : top + h, sx : sx + w, 3] = rgba[..., 3]
        # On the sheet: x, y, w, h (px). In the painting: left, top, width, height (fractions).
        flakes.append([sx, sy, w, h, round(x0 / W, 5), round(y0 / H, 5), round(w / W, 5), round(h / H, 5)])
    sheet_url = save(sheet, "capsule-leaf")
    return {
        "ink": {"src": ink_url, "width": W, "height": H},
        "gold": {"src": gold_url, "width": W, "height": H},
        "leaf": {"src": sheet_url, "width": sheet_w, "height": sheet.shape[0], "band": band_h + gap},
        "tips": TIPS,
        "flakes": flakes,
    }


def heaps():
    img = np.asarray(Image.open(HERE / "originals/gpt25-P7-capsule.png").convert("RGB")).astype(np.float32)
    paper = np.median(img[80:420, 80:420].reshape(-1, 3), axis=0)
    ink = np.clip(img / paper, 0, 1) * 255
    ink[ink > 246] = 255  # the paper's own fibre, not ink
    # No gold on the heaps: the flecks near their tips go back to paper (the leaf flies separately).
    chroma = ink.max(axis=2) - ink.min(axis=2)
    gold = np.asarray(Image.fromarray(((chroma > 45) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7))) > 0
    ink[gold] = 255
    out = {}
    for key, (x0, y0, x1, y1) in HEAPS.items():
        c = ink[y0:y1, x0:x1].copy()
        h, w = c.shape[:2]
        # The sides (where the neighbouring heap or the ground runs on) and the bottom fade to paper.
        fx = np.minimum(np.linspace(0, 1, w) / 0.14, np.linspace(1, 0, w) / 0.14).clip(0, 1)
        fy = (np.linspace(1, 0, h) / 0.2).clip(0, 1)
        c = 255 - (255 - c) * (fx[None, :] * fy[:, None])[..., None]
        a = 1 - c.min(axis=2) / 255
        out[key] = {"src": save(np.dstack([unmultiplied(c, a), a * 255]), f"heap-{key}"), "width": w, "height": h}
    return out


def write_ts(art):
    head = [
        "// Generated by reference/ink-pages/nuricell/build_nuricell_gold.py. Do not edit by hand: change",
        "// the script and run it again. The moving gold of NuriCell's What's inside chapter (October 26,",
        "// 2026). capsule.leaf: one sheet of every flake in three bands (as painted, lit, turned away),",
        "// `band` px apart. capsule.flakes, biggest first: [x, y, w, h] on the sheet (px), then [left, top,",
        "// width, height] in the painting (fractions). capsule.tips: the heaps' tips, left to right",
        "// (fractions). heaps: the four powder heaps, cut out for the teamwork scenes.",
        "",
    ]
    TS.write_text("\n".join(head) + f"export const nuricellGold = {json.dumps(art)} as const;\n", encoding="utf-8", newline="\n")
    prettier = REPO / "node_modules/prettier/bin/prettier.cjs"
    subprocess.run(["node", str(prettier), "--write", str(TS)], cwd=REPO, check=True, capture_output=True)
    print(TS.relative_to(REPO))


if __name__ == "__main__":
    write_ts({"capsule": leaf(), "heaps": heaps()})

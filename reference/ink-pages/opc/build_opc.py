"""Build Advanced OPC Formula's ink paintings (Mo, October 16, 2026; picks in
reference/ink-pages/opc/README.md).

Originals: reference/ink-pages/opc/originals/gpt25-<take>.png (GPT Image 2.5 on rice paper; prompts
in prompts/; spend in reference/ink-pages/spend.md). Output: public/images/products/advanced-opc/
ink/*.webp (lossless plates in plates/, not committed) and src/components/product/ink/opc-art.ts.
The treatments are Green Bee Propolis's (build_propolis.py): the paper divided out and lifted to
white so each painting multiplies onto the page's paper with no box, the outer edge feathered, gold
leaf kept as a light mask for the kit's glint.

Why: a bunch of grapes lit from inside by gold (why-grapes-gold) and the same bunch in grey ink, a
GPT edit of it (why-grapes-ink), registered to the gold take; `spread` is where the gold starts
(the middle of the gilded berries). Buy: the vine scene with its bunch at the far left
(buy-vines-left, cut from a fifth down so the real bottle has room over its cap); the real bottle
photo stands in the gap, `front` is the painting's lowest band cut to the bottle's shape. The
opening's card capsules are the two capsules cut from the plate painting.

usage: python -X utf8 reference/ink-pages/opc/build_opc.py
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
OUT = REPO / "public/images/products/advanced-opc/ink"
URL = "/images/products/advanced-opc/ink"
TS = REPO / "src/components/product/ink/opc-art.ts"
BOTTLE = REPO / "public/images/products/advanced-opc.png"
# Bump when a shipped picture changes after it has been pushed (the image optimizer caches by URL).
V = "v1"
TAKES = {
    "grapes-gold": "why-grapes-gold",
    "grapes-ink": "why-grapes-ink",
    "row": "inside-row",
    "lens": "research-lens",
    "mortar": "people-mortar",
    "plate": "daily-plate",
    "sum": "sum",
    "scene": "buy-vines-left",
}
EDGE = 0.03

bd.ORIG = HERE / "originals"
bd.URL = URL
bd.V = V
bd.TAKES = TAKES
ba.OUT = OUT
ba.PLATES = HERE / "plates"


def finish(img, name, width=1100, gold=False):
    """Paper lifted to white, the outer edge feathered to white, saved; its art entry."""
    art = bd.art_of(bd.feathered(bd.levelled(img), EDGE), f"{name}-{V}", width)
    if gold:
        ba.gold_mask(f"{name}-{V}")
        art["gold"] = f"{URL}/{name}-{V}-gold.webp"
    return art


def cropped(key, pad=0.04):
    flat = bd.divided(bd.load(TAKES[key]))
    return flat.crop(bd.ink_box(np.asarray(flat), pad=pad))


def gold_of(arr):
    return cv2.morphologyEx(bd.gold_pixels(arr.astype(np.uint8)).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))


def richer_gold(img, strength=0.75):
    """Dividing by the cream paper bleaches the leaf: the gold pushed back toward deep leaf."""
    a = np.asarray(img).astype(np.float32)
    gold = cv2.dilate(bd.gold_pixels(a.astype(np.uint8)).astype(np.float32), np.ones((3, 3), np.uint8))
    m = (cv2.GaussianBlur(gold, (0, 0), 1.2) * strength)[..., None]
    deep = a * np.array([0.98, 0.80, 0.42], np.float32)
    return Image.fromarray(np.clip(a * (1 - m) + deep * m, 0, 255).astype(np.uint8))


def registered(fixed, moving):
    if moving.size != fixed.size:
        moving = moving.resize(fixed.size, Image.LANCZOS)
    grey = lambda im: cv2.GaussianBlur(np.asarray(im.convert("L")).astype(np.float32) / 255, (0, 0), 3)
    warp = np.eye(2, 3, dtype=np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6)
    _, warp = cv2.findTransformECC(grey(fixed), grey(moving), warp, cv2.MOTION_EUCLIDEAN, criteria, None, 5)
    print(f"grapes: ink take registered by ({warp[0, 2]:.1f}, {warp[1, 2]:.1f}) px")
    w, h = fixed.size
    moved = cv2.warpAffine(np.asarray(moving), warp, (w, h), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE)
    return Image.fromarray(moved)


def grapes():
    """(unlit, lit, spread): the two Why layers in register and where the gold starts."""
    gold_take = bd.divided(bd.load(TAKES["grapes-gold"]))
    ink_take = registered(gold_take, bd.divided(bd.load(TAKES["grapes-ink"])))
    box = bd.ink_box(np.asarray(gold_take), pad=0.04)
    lit_src = richer_gold(gold_take.crop(box))
    lit = finish(lit_src, "grapes-lit", gold=True)
    unlit = finish(ink_take.crop(box), "grapes-unlit")
    ys, xs = np.nonzero(gold_of(np.asarray(lit_src).astype(np.float32)))
    h, w = np.asarray(lit_src).shape[:2]
    spread = {"x": round(float(np.median(xs)) / w, 4), "y": round(float(np.median(ys)) / h, 4)}
    print(f"grapes: gold {len(xs) / (w * h) * 100:.2f}% of the picture, spreads from {spread}")
    return unlit, lit, spread


def brushed_sum():
    """The painted 2 × 60 = 120 cropped to its ink, and the centres of its three numbers as
    fractions of its width (the page sets a caption under each). The model wrote it evenly, so the
    groups come from the gaps in the ink's column profile: a gap under 1.5% of the width is inside a
    number (6 to 0, 1 to 2), the four wider ones part the numbers from the signs."""
    flat = bd.levelled(cropped("sum", pad=0.06))
    a = np.asarray(flat).min(axis=2)
    on = (a < 200).sum(axis=0) > 0
    groups, start = [], None
    for x, v in enumerate(on):
        if v and start is None:
            start = x
        if not v and start is not None:
            if x - start > 4:
                groups.append((start, x))
            start = None
    if start is not None:
        groups.append((start, len(on)))
    merged = []
    for g in groups:
        if merged and g[0] - merged[-1][1] < flat.width * 0.015:
            merged[-1] = (merged[-1][0], g[1])
        else:
            merged.append(g)
    if len(merged) != 5:
        raise SystemExit(f"expected 2, ×, 60, =, 120 as five groups, found {merged}")
    numbers = [merged[0], merged[2], merged[4]]
    art = bd.art_of(bd.feathered(flat, EDGE), f"sum-{V}", 1100)
    art["numbers"] = [2, 60, 120]
    art["centres"] = [round(((g[0] + g[1]) / 2) / flat.width, 4) for g in numbers]
    print("sum: groups", merged, "centres", art["centres"])
    return art


# The Buy scene, in the take's own pixels (1744 x 2336): cut from a fifth down (the vines sit low;
# the real bottle at 90% of the picture's width, as on NuriCell's stroke, needs about 1.04 widths of
# height over its foot), the bottle's glass foot on the ground wash (measured: the lowest row where
# the ink spans 5% of the width, less 2%). The front band is the painting's lowest 12%, fading over
# 5% above, so a leaf and the ground wash cross the bottle's foot.
SCENE_TOP = 0.2
BOTTLE_WIDTH = 0.9
FRONT_BAND, FRONT_FADE = 0.12, 0.05


def scene():
    img = bd.levelled(bd.divided(bd.load(TAKES["scene"])))
    w, h = img.size
    flat = img.crop((0, int(h * SCENE_TOP), w, h))
    art = bd.art_of(bd.feathered(flat, EDGE), f"scene-{V}", 1100)
    cw, ch = flat.size
    a = np.asarray(flat).min(axis=2)
    rows = (a < 235).sum(axis=1)
    ys = np.nonzero(rows > cw * 0.05)[0]
    foot = float(ys.max()) / ch - 0.02
    bottle = Image.open(BOTTLE)
    pic_h = BOTTLE_WIDTH * cw * bottle.height / bottle.width
    # The bottle photo's glass ends 5.2% above its picture's bottom (as Propolis's).
    pic_bottom = foot * ch + 0.052 * pic_h
    art["bottle"] = {"width": BOTTLE_WIDTH, "bottom": round((ch - pic_bottom) / ch, 4)}
    if ch - art["bottle"]["bottom"] * ch - pic_h < 0:
        raise SystemExit("the bottle's cap would run over the scene's top: cut from lower")
    art["front"] = scene_front(art)
    print("scene: foot at", round(foot, 3), "bottle", art["bottle"])
    return art


def scene_front(art):
    """What of the scene is laid again in front of the bottle: the painting's lowest band (fading
    out above it), but only where the bottle photo is, so a leaf crosses its foot and nothing else is
    painted twice (as Propolis's). White elsewhere, so it multiplies to nothing."""
    scene_img = Image.open(OUT / f"scene-{V}.webp").convert("RGB")
    w, h = scene_img.size
    bottle = Image.open(BOTTLE).convert("RGBA")
    bw = round(w * art["bottle"]["width"])
    bh = round(bw * bottle.height / bottle.width)
    alpha = np.zeros((h, w), np.float32)
    left = round(w / 2 - bw / 2)
    top = round(h - h * art["bottle"]["bottom"] - bh)
    a = np.asarray(bottle.resize((bw, bh), Image.LANCZOS))[..., 3].astype(np.float32) / 255
    y0, x0 = max(0, top), max(0, left)
    alpha[y0 : top + bh, x0 : left + bw] = a[y0 - top : min(bh, h - top), x0 - left : min(bw, w - left)]
    yy = np.arange(h, dtype=np.float32)[:, None] / h
    rows = np.clip((yy - (1 - FRONT_BAND - FRONT_FADE)) / FRONT_FADE, 0, 1)
    m = (alpha * rows)[..., None]
    paint = np.asarray(scene_img).astype(np.float32)
    front = Image.fromarray(np.clip(255 - (255 - paint) * m, 0, 255).astype(np.uint8))
    path = OUT / f"scene-front-{V}.webp"
    front.save(path, "WEBP", quality=88, method=6)
    print(f"{path.relative_to(REPO)}  {w}x{h}  {path.stat().st_size // 1024} KB")
    return f"{URL}/scene-front-{V}.webp"


def capsules(box=(0.70, 0.76, 0.97, 0.95)):
    """The opening's "One bottle" card: the two capsules cut from the plate painting (the ink's
    pieces in their region of the take that touch no edge of it, which the plate's rim does), ink
    on a clear ground, as NuriCell's capsule pair."""
    flat = bd.levelled(bd.divided(bd.load(TAKES["plate"])))
    w, h = flat.size
    region = flat.crop((int(w * box[0]), int(h * box[1]), int(w * box[2]), int(h * box[3])))
    a = np.asarray(region)
    ink = (cv2.GaussianBlur(a.min(axis=2), (0, 0), 3) < 225).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(ink, 8)
    rw, rh = region.size

    def inside(i):
        x, y, cw, ch = st[i, cv2.CC_STAT_LEFT], st[i, cv2.CC_STAT_TOP], st[i, cv2.CC_STAT_WIDTH], st[i, cv2.CC_STAT_HEIGHT]
        return x > 2 and y > 2 and x + cw < rw - 2 and y + ch < rh - 2

    keep = [i for i in range(1, n) if inside(i) and st[i, cv2.CC_STAT_AREA] > 200]
    if len(keep) != 2:
        raise SystemExit(f"expected the two capsules, found {len(keep)} pieces")
    mask = np.isin(lab, keep)
    ys, xs = np.nonzero(mask)
    pad = 14
    x0, y0, x1, y1 = max(0, xs.min() - pad), max(0, ys.min() - pad), min(rw, xs.max() + pad), min(rh, ys.max() + pad)
    soft = cv2.GaussianBlur(cv2.dilate(mask.astype(np.float32), np.ones((9, 9), np.uint8)), (0, 0), 3)[y0:y1, x0:x1][..., None]
    cut = a[y0:y1, x0:x1].astype(np.float32) * soft + 255 * (1 - soft)
    img = Image.fromarray(np.clip(cut, 0, 255).astype(np.uint8))
    img = img.resize((150, round(img.height * 150 / img.width)), Image.LANCZOS)
    rgb = np.asarray(img).astype(np.float32)
    # Ink on a clear ground: each pixel as the colour that, multiplied onto paper, gives it.
    alpha = np.clip(255 - rgb.min(axis=2), 0, 255)
    colour = np.where(alpha[..., None] > 0, 255 - (255 - rgb) * 255 / np.maximum(alpha[..., None], 1), 255)
    rgba = np.dstack([np.clip(colour, 0, 255), alpha]).astype(np.uint8)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"capsules-{V}.webp"
    Image.fromarray(rgba, "RGBA").save(path, "WEBP", quality=90, method=6)
    print(f"{path.relative_to(REPO)}  {img.width}x{img.height}")
    return {"src": f"{URL}/capsules-{V}.webp", "width": img.width, "height": img.height}


def write_ts(art):
    head = [
        "// Generated by reference/ink-pages/opc/build_opc.py. Do not edit by hand: change the script",
        "// (or its TAKES) and run it again. Advanced OPC Formula's ink paintings (October 16, 2026):",
        "// GPT Image 2.5 on rice paper, the paper divided out so each multiplies onto the page's own",
        "// paper; gold leaf as a light mask (`gold`). grapesSpread: where the gold starts, as fractions",
        "// of the painting. sum.centres: its three numbers, as fractions of its width. scene.bottle:",
        "// where the real bottle stands, as fractions of the painting (its width, and its picture's",
        "// bottom above the painting's); scene.front: the painting's lowest share where the bottle",
        "// stands, laid again in front of its foot.",
        "",
    ]
    TS.parent.mkdir(parents=True, exist_ok=True)
    TS.write_text("\n".join(head) + f"export const opcArt = {json.dumps(art, indent=2)} as const;\n", encoding="utf-8", newline="\n")
    prettier = REPO / "node_modules/prettier/bin/prettier.cjs"
    subprocess.run(["node", str(prettier), "--write", str(TS)], cwd=REPO, check=True, capture_output=True)
    print(TS.relative_to(REPO))


if __name__ == "__main__":
    unlit, lit, spread = grapes()
    write_ts(
        {
            "grapesUnlit": unlit,
            "grapesLit": lit,
            "grapesSpread": spread,
            "row": finish(cropped("row"), "row"),
            "lens": finish(cropped("lens"), "lens"),
            "mortar": finish(cropped("mortar"), "mortar"),
            "plate": finish(cropped("plate"), "plate"),
            "sum": brushed_sum(),
            "scene": scene(),
            "capsules": capsules(),
        }
    )

"""Build Green Bee Propolis's ink paintings (Mo, October 13-14, 2026; picks in
reference/ink-pages/propolis/README.md).

Originals: reference/ink-pages/propolis/originals/gpt25-<take>.png (GPT Image 2.5 on rice paper;
prompts in prompts/; spend in reference/ink-pages/spend.md). Output: public/images/products/
green-bee-propolis/ink/*.webp (lossless plates in plates/, not committed) and
src/components/product/ink/propolis-art.ts. NuriCell's treatments (build_nuricell.py): the paper
divided out and lifted to white so each painting multiplies onto the page's paper with no box, gold
leaf kept as a light mask for the kit's glint.

Why: the bee tree with its cracks sealed in gold, and the same tree with the cracks open. The open
take is a GPT edit of the gold one; only its cracks are used (laid into the gold take along the
cracks, toned to the bark around them), so nothing but the cracks changes as the gold spreads in.
`spread` is where the gold starts (the middle of the cracks, near the hollow), as fractions.

Buy: the painted scene Mo picked (round 7 A) with its painted bottle taken out by a GPT edit
(buy-painted-empty); the real bottle photo stands in its place (Mo, October 14: the bottle is never
redrawn). `bottle` is where it stands, `front` the painting's lowest share laid again in front of it.

usage: python -X utf8 reference/ink-pages/propolis/build_propolis.py
"""

import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageFilter

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "reference/ink-pages/about"))
import build_about as bd  # noqa: E402

ba = bd.ba
OUT = REPO / "public/images/products/green-bee-propolis/ink"
URL = "/images/products/green-bee-propolis/ink"
TS = REPO / "src/components/product/ink/propolis-art.ts"
# Bump when a shipped picture changes after it has been pushed (the image optimizer caches by URL).
V = "v1"
TAKES = {
    "hive-gold": "why-hive-gold",
    "hive-open": "why-hive-open",
    "resin": "inside-resin-dish",
    "specimen": "research-specimen",
    "mug": "daily-mug-v2",
    "scene": "buy-painted-empty",
}
EDGE = 0.03

bd.ORIG = HERE / "originals"
bd.URL = URL
bd.V = V
bd.TAKES = TAKES
ba.OUT = OUT
ba.PLATES = HERE / "plates"


def finish(img, name, width):
    """Paper lifted to white, the outer edge feathered to white, saved; its art entry."""
    return bd.art_of(bd.feathered(bd.levelled(img), EDGE), f"{name}-{V}", width)


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


def trunk_fade(img, frac=0.12):
    """The trunk runs off the top and bottom of the take: faded out over `frac` of the height (a
    soft brush end, not a cropped photo), and the sides over 3%."""
    arr = np.asarray(img).astype(np.float32)
    h, w = arr.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    v = np.clip(np.minimum(yy, h - 1 - yy) / (h * frac), 0, 1)
    v = v * v * (3 - 2 * v)
    s = np.clip(np.minimum(xx, w - 1 - xx) / (w * 0.03), 0, 1)
    keep = (v * s)[..., None]
    return Image.fromarray((arr * keep + 255 * (1 - keep)).astype(np.uint8))


def registered(fixed, moving):
    if moving.size != fixed.size:
        moving = moving.resize(fixed.size, Image.LANCZOS)
    grey = lambda im: cv2.GaussianBlur(np.asarray(im.convert("L")).astype(np.float32) / 255, (0, 0), 3)
    warp = np.eye(2, 3, dtype=np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6)
    _, warp = cv2.findTransformECC(grey(fixed), grey(moving), warp, cv2.MOTION_EUCLIDEAN, criteria, None, 5)
    print(f"hive: open take registered by ({warp[0, 2]:.1f}, {warp[1, 2]:.1f}) px")
    w, h = fixed.size
    moved = cv2.warpAffine(np.asarray(moving), warp, (w, h), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP,
                           borderMode=cv2.BORDER_REPLICATE)
    return Image.fromarray(moved)


def cracks_open(gold_take, open_take):
    """The gold take everywhere except along its cracks, where the open take's painted crack shows
    (registered, and toned to the gold take's bark in a ring around the cracks)."""
    a = np.asarray(gold_take).astype(np.float32)
    e = np.asarray(registered(gold_take, open_take)).astype(np.float32)
    gold = gold_of(a)
    zone = cv2.dilate(gold, np.ones((19, 19), np.uint8)).astype(bool)
    ring = zone & ~cv2.dilate(gold, np.ones((7, 7), np.uint8)).astype(bool)
    for c in range(3):
        ma, sa = a[..., c][ring].mean(), a[..., c][ring].std()
        me, se = e[..., c][ring].mean(), e[..., c][ring].std()
        e[..., c] = (e[..., c] - me) * (sa / max(se, 1e-3)) + ma
    m = cv2.GaussianBlur(zone.astype(np.float32), (0, 0), 4)[..., None]
    return Image.fromarray(np.clip(a * (1 - m) + e * m, 0, 255).astype(np.uint8))


def hive():
    """(open, gold, spread): the two Why layers in register and where the gold starts."""
    gold_take = bd.divided(bd.load(TAKES["hive-gold"]))
    open_take = bd.divided(bd.load(TAKES["hive-open"]))
    before = cracks_open(gold_take, open_take)
    after = richer_gold(gold_take)
    lit = bd.art_of(trunk_fade(bd.levelled(after)), f"hive-gold-{V}", 1100)
    ba.gold_mask(f"hive-gold-{V}")
    lit["gold"] = f"{URL}/hive-gold-{V}-gold.webp"
    unlit = bd.art_of(trunk_fade(bd.levelled(before)), f"hive-open-{V}", 1100)
    # Where the gold starts: the middle of the gilded cracks (the cracks fan out from the hollow).
    ys, xs = np.nonzero(gold_of(np.asarray(after).astype(np.float32)))
    h, w = np.asarray(after).shape[:2]
    spread = {"x": round(float(np.median(xs)) / w, 4), "y": round(float(np.median(ys)) / h, 4)}
    print(f"hive: gold spreads from {spread}")
    return unlit, lit, spread


# The capsule in the resin painting, on the 1100-wide shipped picture: its centre, length, width and
# tilt (degrees, counter-clockwise), measured on the take. It is painted white; the real capsule is
# yellow (yellow iron oxide on the label), so it is tinted to the mug painting's gold.
CAPSULE = ((945, 545), 230, 89, 27)
YELLOW = np.array([1.0, 0.88, 0.52], np.float32)


def capsule_mask(shape):
    (cx, cy), length, width, angle = CAPSULE
    h, w = shape[:2]
    mask = np.zeros((h, w), np.uint8)
    t = np.deg2rad(angle)
    ux, uy = np.cos(t), -np.sin(t)
    half = (length - width) / 2
    p0 = (int(cx - ux * half), int(cy - uy * half))
    p1 = (int(cx + ux * half), int(cy + uy * half))
    cv2.line(mask, p0, p1, 255, int(width))
    cv2.circle(mask, p0, int(width / 2), 255, -1)
    cv2.circle(mask, p1, int(width / 2), 255, -1)
    return cv2.GaussianBlur(mask.astype(np.float32) / 255, (0, 0), 2.5)


def resin():
    flat = bd.feathered(bd.levelled(cropped("resin")), EDGE)
    flat = flat.resize((1100, round(flat.height * 1100 / flat.width)), Image.LANCZOS)
    a = np.asarray(flat).astype(np.float32)
    m = capsule_mask(a.shape)[..., None]
    a = a * (1 - m) + a * YELLOW * m
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    art = bd.art_of(img, f"resin-{V}", 1100)
    ba.gold_mask(f"resin-{V}")
    art["gold"] = f"{URL}/resin-{V}-gold.webp"
    return art, img, m[..., 0]


def supply(resin_img, mask):
    """The opening's "One bottle" card: the yellow capsule alone, ink on a clear ground (as
    NuriCell's capsule pair: over the paper it draws as a multiplied painting would, with no box
    inside the words' settle animation)."""
    ys, xs = np.nonzero(mask > 0.02)
    pad = 10
    box = (xs.min() - pad, ys.min() - pad, xs.max() + pad, ys.max() + pad)
    a = np.asarray(resin_img.crop(box)).astype(np.float32)
    m = mask[box[1]:box[3], box[0]:box[2]][..., None]
    a = a * m + 255 * (1 - m)
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    img = img.resize((150, round(img.height * 150 / img.width)), Image.LANCZOS)
    rgb = np.asarray(img).astype(np.float32)
    # Ink on a clear ground: each pixel as the colour that, multiplied onto paper, gives it.
    alpha = np.clip(255 - rgb.min(axis=2), 0, 255)
    colour = np.where(alpha[..., None] > 0, 255 - (255 - rgb) * 255 / np.maximum(alpha[..., None], 1), 255)
    rgba = np.dstack([np.clip(colour, 0, 255), alpha]).astype(np.uint8)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"capsule-{V}.webp"
    Image.fromarray(rgba, "RGBA").save(path, "WEBP", quality=90, method=6)
    print(f"{path.relative_to(REPO)}  {img.width}x{img.height}")
    return {"src": f"{URL}/capsule-{V}.webp", "width": img.width, "height": img.height}


def mug():
    """How to take it: a mug of tea and one gold capsule (Mo, October 14: an everyday mug, not a
    teacup)."""
    art = finish(cropped("mug"), "mug", 1100)
    ba.gold_mask(f"mug-{V}")
    art["gold"] = f"{URL}/mug-{V}-gold.webp"
    return art


def scene():
    """The Buy scene: the painting without its bottle, from just above the bee to just under the
    ground wash (the empty paper above the bee and under the ground cut away)."""
    img = bd.load(TAKES["scene"])
    w, h = img.size
    flat = bd.levelled(bd.divided(img)).crop((0, int(h * 0.22), w, int(h * 0.93)))
    art = bd.art_of(bd.feathered(flat, EDGE), f"scene-{V}", 1100)
    # Where the painted bottle stood (round 7 A): 32% of the painting wide, its foot on the ground
    # wash 13.7% above the crop's bottom. The bottle photo's glass is 51.5% of its picture's width
    # and ends 5.2% above its picture's bottom.
    art["bottle"] = {"width": 0.62, "bottom": 0.102}
    art["front"] = scene_front(art, 0.17)
    return art


BOTTLE = REPO / "public/images/products/green-bee-propolis.png"


def scene_front(art, band, fade=0.07):
    """What of the scene is laid again in front of the bottle: the painting's lowest `band` (fading
    out over `fade` above it), but only where the bottle photo is, so a blossom crosses its foot and
    nothing else is painted twice (a full band multiplied onto the painting deepened the blossoms
    beside the bottle; review of October 14). White elsewhere, so it multiplies to nothing. Cut for
    the bottle's place in `art["bottle"]` and the bottle photo as it is: run again if either changes."""
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
    rows = np.clip((yy - (1 - band - fade)) / fade, 0, 1)
    m = (alpha * rows)[..., None]
    paint = np.asarray(scene_img).astype(np.float32)
    front = Image.fromarray(np.clip(255 - (255 - paint) * m, 0, 255).astype(np.uint8))
    path = OUT / f"scene-front-{V}.webp"
    front.save(path, "WEBP", quality=88, method=6)
    print(f"{path.relative_to(REPO)}  {w}x{h}  {path.stat().st_size // 1024} KB")
    return f"{URL}/scene-front-{V}.webp"


def write_ts(art):
    head = [
        "// Generated by reference/ink-pages/propolis/build_propolis.py. Do not edit by hand: change",
        "// the script (or its TAKES) and run it again. Green Bee Propolis's ink paintings (October",
        "// 13-14, 2026): GPT Image 2.5 on rice paper, the paper divided out so each multiplies onto the",
        "// page's own paper; gold leaf as a light mask (`gold`). hiveSpread: where the gold starts, as",
        "// fractions of the painting. scene.bottle: where the real bottle stands, as fractions of the",
        "// painting (its width, and its picture's bottom above the painting's); scene.front: the",
        "// painting's lowest share where the bottle stands, laid again in front of its foot.",
        "",
    ]
    TS.parent.mkdir(parents=True, exist_ok=True)
    TS.write_text("\n".join(head) + f"export const propolisArt = {json.dumps(art, indent=2)} as const;\n",
                  encoding="utf-8", newline="\n")
    prettier = REPO / "node_modules/prettier/bin/prettier.cjs"
    subprocess.run(["node", str(prettier), "--write", str(TS)], cwd=REPO, check=True, capture_output=True)
    print(TS.relative_to(REPO))


if __name__ == "__main__":
    unlit, lit, spread = hive()
    resin_art, resin_img, mask = resin()
    write_ts(
        {
            "hiveOpen": unlit,
            "hiveGold": lit,
            "hiveSpread": spread,
            "resin": resin_art,
            "capsule": supply(resin_img, mask),
            "specimen": finish(cropped("specimen"), "specimen", 1100),
            "mug": mug(),
            "scene": scene(),
        }
    )

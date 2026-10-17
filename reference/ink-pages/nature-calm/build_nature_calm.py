"""Build Nature Calm's ink paintings (Mo, October 16, 2026; picks in
reference/ink-pages/nature-calm/README.md).

Originals: reference/ink-pages/nature-calm/originals/gpt25-<take>.png (GPT Image 2.5 on rice paper;
prompts in prompts/; spend in reference/ink-pages/spend.md). Output: public/images/products/
nature-calm/ink/*.webp (lossless plates in plates/, not committed) and
src/components/product/ink/nature-calm-art.ts. NuriCell's treatments (build_nuricell.py): the paper
divided out and lifted to white so each painting multiplies onto the page's paper with no box, gold
leaf kept as a light mask for the kit's glint.

What is this product's own:
- Why: the lake. The lit painting is the still take (one gold line down the water); the unlit one
  its edit with the water ruffled and the gold scattered, registered onto it, so the cross-fade
  (NuriCell's lantern mode) reads as the water going still and the light gathering. Both keep the
  whole sheet (the wash runs to its edges) and get the same gentle lift and the same deepened wash:
  the take's still water is only 7% darker than its paper and vanished once multiplied onto the page.
- Gold: the kit's detector (hue 24-58) takes the pine cone's browns and any ochre for gold; the leaf
  on these takes sits at hue 38-60 (measured), so a stricter detector (gold_soft) cuts the masks.
- Buy: the lavender rows with the real bottle standing in the gap between them (never redrawn); the
  take is cut from its bottom up to 7% over the bottle's cap, the glass's foot on the ground wash.
- The opening's "One bottle" card: the three capsules from the moon painting (three a day), ink on a
  clear ground as NuriCell's capsule pair.

usage: python -X utf8 reference/ink-pages/nature-calm/build_nature_calm.py
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
OUT = REPO / "public/images/products/nature-calm/ink"
URL = "/images/products/nature-calm/ink"
TS = REPO / "src/components/product/ink/nature-calm-art.ts"
BOTTLE = REPO / "public/images/products/nature-calm.png"
# Bump when a shipped picture changes after it has been pushed (the image optimizer caches by URL).
V = "v1"
TAKES = {
    "water-still": "why-water-still",
    "water-ripple": "why-water-ripple",
    "cone": "inside-cone",
    "stars": "research-stars-v2",
    "moon": "daily-moon",
    "lavender": "buy-lavender",
}
EDGE = 0.03
WIDTH = 1100

bd.ORIG = HERE / "originals"
bd.URL = URL
bd.V = V
bd.TAKES = TAKES
ba.OUT = OUT
ba.PLATES = HERE / "plates"


# --- gold ---------------------------------------------------------------------------------------


def gold_soft(arr):
    """Gold leaf on these takes as a soft 0-1 mask: hue 36-62 (the pine cone's browns top out at
    34, an ochre hill at 39), any clear saturation (dividing out the paper bleaches the leaf to
    about 0.3), bright. Measured on the round-1 takes, October 16, 2026."""
    a = arr.astype(np.float32) / 255
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    hi, lo = a.max(axis=2), a.min(axis=2)
    sat = (hi - lo) / np.maximum(hi, 1e-4)
    warm = (r >= g) & (g > b)
    hue = np.where(warm, 60 * (g - b) / np.maximum(hi - lo, 1e-4), 0)
    in_hue = np.clip((hue - 35) / 4, 0, 1) * np.clip((64 - hue) / 5, 0, 1)
    return in_hue * np.clip((sat - 0.13) / 0.08, 0, 1) * np.clip((hi - 0.55) / 0.1, 0, 1)


def richer_gold(img, strength=0.75):
    """Dividing by the cream paper bleaches the leaf: the gold pushed back toward deep leaf
    (build_propolis.py), through the strict detector."""
    a = np.asarray(img).astype(np.float32)
    m = (cv2.GaussianBlur(gold_soft(a), (0, 0), 1.2) * strength)[..., None]
    deep = a * np.array([0.98, 0.80, 0.42], np.float32)
    return Image.fromarray(np.clip(a * (1 - m) + deep * m, 0, 255).astype(np.uint8))


def gold_mask(name, width=1000):
    """The shipped painting's gold leaf as an alpha mask (<name>-gold.webp, as ba.gold_mask), with
    the strict detector, soft-edged. Returns the share of its pixels that are gold."""
    img = Image.open(ba.PLATES / f"{name}.png").convert("RGB")
    img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    m = cv2.GaussianBlur(gold_soft(np.asarray(img)), (0, 0), 1.0)
    rgba = np.dstack([np.full(m.shape + (3,), 255, np.uint8), (m * 255).astype(np.uint8)])
    path = OUT / f"{name}-gold.webp"
    Image.fromarray(rgba, "RGBA").save(path, "WEBP", quality=90, method=6)
    share = float((m > 0.5).mean())
    print(f"{path.relative_to(REPO)}  gold {share * 100:.2f}%")
    return share


def gilded(art, name):
    gold_mask(name)
    art["gold"] = f"{URL}/{name}-gold.webp"
    return art


# --- paper --------------------------------------------------------------------------------------


def gentle(img, knee=200.0, white=252.0):
    """A divided picture with its paper lifted to white while its pale washes stay: from `white` up
    is white, ink at `knee` or darker unchanged, a straight ramp between (bd.levelled's 220/245
    bleaches a 230-245 wash to nothing)."""
    arr = np.asarray(img).astype(np.float32)
    out = np.where(arr <= knee, arr, knee + (arr - knee) * (255.0 - knee) / (white - knee))
    return Image.fromarray(np.clip(np.rint(out), 0, 255).astype(np.uint8))


def deepen_wash(img, k=2.5, lo=205.0, hi=235.0):
    """A pale wash deepened: the ink in every pale pixel (255 - value) times `k`, eased in from `lo`
    to `hi`, so strokes darker than `lo` keep their depth and bare paper stays white."""
    a = np.asarray(img).astype(np.float32)
    s = np.clip((a - lo) / (hi - lo), 0, 1)
    out = a - (255 - a) * (k - 1) * s
    return Image.fromarray(np.clip(np.rint(out), 0, 255).astype(np.uint8))


def finish(img, name, width=WIDTH, lift=bd.levelled):
    """Paper lifted to white, the outer edge feathered to white, saved; its art entry."""
    return bd.art_of(bd.feathered(lift(img), EDGE), f"{name}-{V}", width)


def cropped(key, pad=0.04):
    flat = bd.divided(bd.load(TAKES[key]))
    return flat.crop(bd.ink_box(np.asarray(flat), pad=pad))


def registered(fixed, moving):
    if moving.size != fixed.size:
        moving = moving.resize(fixed.size, Image.LANCZOS)
    grey = lambda im: cv2.GaussianBlur(np.asarray(im.convert("L")).astype(np.float32) / 255, (0, 0), 3)
    warp = np.eye(2, 3, dtype=np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6)
    _, warp = cv2.findTransformECC(grey(fixed), grey(moving), warp, cv2.MOTION_TRANSLATION, criteria, None, 5)
    print(f"lake: ruffled take registered by ({warp[0, 2]:.1f}, {warp[1, 2]:.1f}) px")
    w, h = fixed.size
    moved = cv2.warpAffine(np.asarray(moving), warp, (w, h), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP,
                           borderMode=cv2.BORDER_REPLICATE)
    return Image.fromarray(moved)


# --- the paintings --------------------------------------------------------------------------------


def lake():
    """(unlit, lit): the ruffled water and the still water, in register, whole sheet, the same lift
    and the same deepened wash."""
    still = bd.divided(bd.load(TAKES["water-still"]))
    ripple = registered(still, bd.divided(bd.load(TAKES["water-ripple"])))
    lift = lambda img: gentle(img, 200, 252)
    lit = finish(deepen_wash(richer_gold(still)), "lake-still", lift=lift)
    unlit = finish(deepen_wash(richer_gold(ripple)), "lake-ruffled", lift=lift)
    return unlit, gilded(lit, f"lake-still-{V}")


def cone():
    return gilded(finish(richer_gold(cropped("cone")), "cone"), f"cone-{V}")


def stars():
    """The stars' sheet is bare paper with a faint cool cast: lifted from 240 so it goes to white."""
    return gilded(finish(richer_gold(cropped("stars")), "stars", lift=lambda img: gentle(img, 200, 240)), f"stars-{V}")


def moon():
    img = richer_gold(cropped("moon"))
    art = gilded(finish(img, "moon"), f"moon-{V}")
    return art, img


def supply(moon_img):
    """The opening's "One bottle" card: the three capsules from the moon painting (three a day), ink
    on a clear ground (NuriCell's capsule pair). The capsules are the small ink marks in the lower
    right of the painting, under the glass: every ink component there shorter than a tenth of the
    painting, their box with a little air."""
    a = np.asarray(bd.levelled(moon_img))
    h, w, _ = a.shape
    ink = (cv2.GaussianBlur(a.min(axis=2).astype(np.float32), (0, 0), 2) < 228).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(ink, 8)
    boxes = []
    for i in range(1, n):
        x, y, bw, bh, area = (int(v) for v in st[i])
        if y > h * 0.6 and x + bw / 2 > w * 0.5 and bh < h * 0.1 and bw < w * 0.2 and area > 400:
            boxes.append((x, y, x + bw, y + bh))
    if not boxes:
        raise SystemExit("supply: no capsules found under the glass")
    x0, y0 = min(b[0] for b in boxes), min(b[1] for b in boxes)
    x1, y1 = max(b[2] for b in boxes), max(b[3] for b in boxes)
    print(f"supply: {len(boxes)} capsule marks in ({x0}, {y0})-({x1}, {y1})")
    m = 18
    crop = Image.fromarray(a).crop((max(0, x0 - m), max(0, y0 - m), min(w, x1 + m), min(h, y1 + m)))
    # Faded to white away from its own ink, so no glass shadow comes with it.
    c = np.asarray(crop).astype(np.float32)
    mark = (c.mean(axis=2) < 235).astype(np.uint8) * 255
    keep = cv2.GaussianBlur(cv2.dilate(mark, np.ones((9, 9), np.uint8)).astype(np.float32), (0, 0), 5) / 255
    c = c * keep[..., None] + 255 * (1 - keep[..., None])
    img = Image.fromarray(np.clip(c, 0, 255).astype(np.uint8))
    img = img.resize((320, round(img.height * 320 / img.width)), Image.LANCZOS)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"capsules-{V}.webp"
    grey = np.asarray(img.convert("L")).astype(np.float32)
    rgba = np.zeros((*grey.shape, 4), np.uint8)
    rgba[..., 3] = np.clip(255 - grey, 0, 255).astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(path, "WEBP", quality=90, method=6)
    print(f"{path.relative_to(REPO)}  {img.width}x{img.height}")
    return {"src": f"{URL}/capsules-{V}.webp", "width": img.width, "height": img.height}


# The Buy scene: the lavender take's ground line, from its bottom, as a share of its height (the
# real bottle's glass foot rests on it); the bottle NuriCell's size (90% of the painting's width);
# the take cut from its bottom up to HEADROOM over the bottle's cap; the front band (the painting's
# lowest share laid again in front of the bottle's foot, so stalks cross it) reaches a little over
# the ground line.
FOOT = 0.075
BOTTLE_WIDTH = 0.9
HEADROOM = 0.07
FRONT_OVER, FRONT_FADE = 0.04, 0.06


def bottle_foot_offset():
    """How far the glass's foot sits above the bottle picture's bottom edge (its clear margin)."""
    a = np.asarray(Image.open(BOTTLE).convert("RGBA"))[..., 3]
    ys = np.nonzero(a > 8)[0]
    return (a.shape[0] - 1 - ys.max()) / a.shape[0]


def scene():
    take = bd.divided(bd.load(TAKES["lavender"]))
    w, h = take.size
    bottle = Image.open(BOTTLE)
    bw = BOTTLE_WIDTH * w
    bh = bw * bottle.height / bottle.width
    bottom_px = FOOT * h - bottle_foot_offset() * bh
    crop_h = min(h, (bottom_px + bh) / (1 - HEADROOM))
    img = take.crop((0, int(h - crop_h), w, h))
    art = finish(img, "lavender")
    art["bottle"] = {"width": BOTTLE_WIDTH, "bottom": round(bottom_px / crop_h, 4)}
    band = FOOT * h / crop_h + FRONT_OVER
    art["front"] = scene_front(art, band, FRONT_FADE)
    print(f"lavender: cut to {crop_h / h:.0%} of the take, bottle bottom {art['bottle']['bottom']:.3f}, front band {band:.3f}")
    return art


def scene_front(art, band, fade):
    """What of the scene is laid again in front of the bottle: the painting's lowest `band` (fading
    out over `fade` above it), but only where the bottle photo is, so stalks cross its foot and
    nothing else is painted twice. White elsewhere, so it multiplies to nothing (build_propolis.py)."""
    scene_img = Image.open(OUT / f"lavender-{V}.webp").convert("RGB")
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
    path = OUT / f"lavender-front-{V}.webp"
    front.save(path, "WEBP", quality=88, method=6)
    print(f"{path.relative_to(REPO)}  {w}x{h}  {path.stat().st_size // 1024} KB")
    return f"{URL}/lavender-front-{V}.webp"


def write_ts(art):
    head = [
        "// Generated by reference/ink-pages/nature-calm/build_nature_calm.py. Do not edit by hand:",
        "// change the script (or its TAKES) and run it again. Nature Calm's ink paintings (October 16,",
        "// 2026): GPT Image 2.5 on rice paper, the paper divided out so each multiplies onto the page's",
        "// own paper; gold leaf as a light mask (`gold`). lakeRuffled and lakeStill are one painting in",
        "// register (the water goes still, the light gathers). lavender.bottle: where the real bottle",
        "// stands, as fractions of the painting (its width, and its picture's bottom above the",
        "// painting's); lavender.front: the painting's lowest share where the bottle stands, laid again",
        "// in front of its foot. capsules: the three capsules for the opening's card, ink on a clear ground.",
        "",
    ]
    TS.parent.mkdir(parents=True, exist_ok=True)
    TS.write_text("\n".join(head) + f"export const natureCalmArt = {json.dumps(art, indent=2)} as const;\n",
                  encoding="utf-8", newline="\n")
    prettier = REPO / "node_modules/prettier/bin/prettier.cjs"
    subprocess.run(["node", str(prettier), "--write", str(TS)], cwd=REPO, check=True, capture_output=True)
    print(TS.relative_to(REPO))


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    unlit, lit = lake()
    moon_art, moon_img = moon()
    write_ts(
        {
            "lakeRuffled": unlit,
            "lakeStill": lit,
            "cone": cone(),
            "stars": stars(),
            "moon": moon_art,
            "capsules": supply(moon_img),
            "lavender": scene(),
        }
    )

"""Build Turmerific's ink paintings (Mo, October 16, 2026; picks in reference/ink-pages/turmerific/README.md).

Originals: reference/ink-pages/turmerific/originals/gpt25-<take>.png (GPT Image 2.5 on rice paper;
prompts in prompts/; spend in reference/ink-pages/spend.md). Output: public/images/products/
turmerific/ink/*.webp (lossless plates in plates/, not committed) and
src/components/product/ink/turmerific-art.ts. The treatments are NuriCell's and Green Bee
Propolis's (build_nuricell.py, build_propolis.py): the paper divided out and lifted to white so
each painting multiplies onto the page's paper with no box, gold leaf kept as a light mask for the
kit's glint.

Why: a turmeric root and one slice cut from it, plain ink (unlit), then the same with the slice and
the root's cut end in gold leaf and the gold soaked out into the paper (lit). The unlit take is a GPT
edit of the lit one, registered onto it. The page reveals the lit painting through `soak`: a sprite
of FRAMES masks, each a wider stretch of the gold, stacked as layers that fade in one after another,
so the gold soaks outward from the slice in the bloom's own ragged shape (not a circle).

Buy: the turmeric plant in flower, as on the label, with an empty space where the real bottle photo
stands (Mo, October 14: the bottle is never redrawn); `bottle` is where it stands, `front` the
painting's lowest band laid again in front of its foot (the gold root slices).

usage: python -X utf8 reference/ink-pages/turmerific/build_turmerific.py
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
OUT = REPO / "public/images/products/turmerific/ink"
URL = "/images/products/turmerific/ink"
TS = REPO / "src/components/product/ink/turmerific-art.ts"
BOTTLE = REPO / "public/images/products/turmerific.png"
# Bump when a shipped picture changes after it has been pushed (the image optimizer caches by URL).
V = "v1"
TAKES = {
    "lit": "why-soak-lit",
    "unlit": "why-soak-unlit",
    "inside": "inside-scoop",
    "research": "research-glasses",
    "daily": "daily-glass",
    "sum": "daily-sum",
    "scene": "buy-plant",
}
EDGE = 0.03

bd.ORIG = HERE / "originals"
bd.URL = URL
bd.V = V
bd.TAKES = TAKES
ba.OUT = OUT
ba.PLATES = HERE / "plates"


def finish(img, name, width=1100):
    """Paper lifted to white, the outer edge feathered to white, saved; its art entry."""
    return bd.art_of(bd.feathered(bd.levelled(img), EDGE), f"{name}-{V}", width)


def cropped(key, pad=0.05):
    flat = bd.divided(bd.load(TAKES[key]))
    return flat.crop(bd.ink_box(np.asarray(flat), pad=pad))


def with_gold(art, name):
    ba.gold_mask(f"{name}-{V}")
    art["gold"] = f"{URL}/{name}-{V}-gold.webp"
    return art


def registered(fixed, moving):
    if moving.size != fixed.size:
        moving = moving.resize(fixed.size, Image.LANCZOS)
    grey = lambda im: cv2.GaussianBlur(np.asarray(im.convert("L")).astype(np.float32) / 255, (0, 0), 3)
    warp = np.eye(2, 3, dtype=np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6)
    _, warp = cv2.findTransformECC(grey(fixed), grey(moving), warp, cv2.MOTION_EUCLIDEAN, criteria, None, 5)
    print(f"why: unlit take registered by ({warp[0, 2]:.1f}, {warp[1, 2]:.1f}) px")
    w, h = fixed.size
    moved = cv2.warpAffine(np.asarray(moving), warp, (w, h), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP,
                           borderMode=cv2.BORDER_REPLICATE)
    return Image.fromarray(moved)


# The soak: where it starts (the middle of the gold slice, as fractions of the cropped painting,
# measured on it), how many masks the sprite holds, and how wide each mask's soft edge is.
SLICE = (0.57, 0.43)
FRAMES = 10
FEATHER = 0.12
SPRITE_WIDTH = 550


def soak_time(lit, unlit, seed=7):
    """When each pixel turns gold: 0 at the slice, 1 at the bloom's edge. Its distance from the slice
    divided by how far the gold reaches in its direction, so the bloom grows in its own shape and
    reaches every edge together; a fine noise roughens the wet edge without islands ahead of it."""
    a = np.asarray(lit).astype(np.float32)
    b = np.asarray(unlit).astype(np.float32)
    h, w = a.shape[:2]
    changed = np.abs(a - b).max(axis=2) > 18
    changed = cv2.morphologyEx(changed.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)) > 0
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dx, dy = xx - SLICE[0] * w, yy - SLICE[1] * h
    d = np.hypot(dx, dy)
    bins = 180
    idx = ((np.arctan2(dy, dx) + np.pi) / (2 * np.pi) * bins).astype(int) % bins
    reach = np.zeros(bins, np.float32)
    np.maximum.at(reach, idx[changed], d[changed])
    reach = np.maximum(reach, np.percentile(reach[reach > 0], 20))
    reach = np.convolve(np.concatenate([reach[-4:], reach, reach[:4]]), np.ones(9) / 9, mode="valid")
    rng = np.random.default_rng(seed)
    noise = np.zeros((h, w), np.float32)
    for scale, amp in ((40, 0.035), (12, 0.015)):
        n = rng.standard_normal((h // scale + 2, w // scale + 2)).astype(np.float32)
        noise += amp * cv2.resize(n, (w, h), interpolation=cv2.INTER_CUBIC)
    return np.clip(d / reach[idx] + noise, 0, 1.3)


def soak_sprite(lit, unlit):
    """FRAMES masks stacked top to bottom (white, the mask in alpha): mask k is the gold that has
    soaked in by step k, with a soft edge; the last is whole. The page fades one layer of the lit
    painting in through each, in order."""
    w = SPRITE_WIDTH
    h = round(lit.height * w / lit.width)
    t = soak_time(lit.resize((w, h), Image.LANCZOS), unlit.resize((w, h), Image.LANCZOS))
    frames = []
    for k in range(FRAMES):
        if k == FRAMES - 1:
            m = np.ones_like(t)
        else:
            edge = (k + 1) / FRAMES
            m = np.clip((edge + FEATHER / 2 - t) / FEATHER, 0, 1)
            m = m * m * (3 - 2 * m)
        frames.append(m)
    alpha = (np.concatenate(frames, axis=0) * 255).astype(np.uint8)
    white = np.full_like(alpha, 255)
    rgba = Image.merge("RGBA", (Image.fromarray(white), Image.fromarray(white), Image.fromarray(white),
                                Image.fromarray(alpha)))
    path = OUT / f"soak-{V}.webp"
    rgba.save(path, "WEBP", quality=82, method=6)
    print(f"{path.relative_to(REPO)}  {w}x{h * FRAMES} ({FRAMES} frames)  {path.stat().st_size // 1024} KB")
    return {"sprite": f"{URL}/soak-{V}.webp", "frames": FRAMES}


# The two cut faces in gold leaf, as ellipses (centre x, centre y, half width, half height, as
# fractions of the cropped painting, measured on it). The glint is for leaf only: the soaked-in
# wash around the slice is watercolour, and a band of light sweeping over it looked like a shine
# on a stain (review of October 16).
FACES = [(0.4636, 0.2993, 0.0564, 0.0818), (0.5927, 0.4572, 0.1018, 0.052)]


def leaf_only(name):
    """Keep the painting's gold mask (ba.gold_mask) only on the leaf faces."""
    path = OUT / f"{name}-gold.webp"
    mask = Image.open(path)
    alpha = np.asarray(mask.split()[3]).astype(np.float32)
    h, w = alpha.shape
    faces = np.zeros((h, w), np.uint8)
    for cx, cy, rx, ry in FACES:
        cv2.ellipse(faces, (round(cx * w), round(cy * h)), (round(rx * w), round(ry * h)), 0, 0, 360, 255, -1)
    keep = cv2.GaussianBlur(faces.astype(np.float32) / 255, (0, 0), 3)
    alpha = Image.fromarray(np.clip(alpha * keep, 0, 255).astype(np.uint8), "L")
    white = Image.new("L", alpha.size, 255)
    Image.merge("RGBA", (white, white, white, alpha)).save(path, "WEBP", quality=80, method=6)
    print(f"{path.relative_to(REPO)}  leaf only: {float((np.asarray(alpha) > 128).mean()):.1%}")


def why():
    """(unlit, lit, soak): the two Why layers in register, cropped by their shared box."""
    lit_take = bd.divided(bd.load(TAKES["lit"]))
    unlit_take = registered(lit_take, bd.divided(bd.load(TAKES["unlit"])))
    a, b = bd.ink_box(np.asarray(lit_take), pad=0.05), bd.ink_box(np.asarray(unlit_take), pad=0.05)
    box = (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))
    lit_img = bd.feathered(bd.levelled(lit_take.crop(box)), EDGE)
    unlit_img = bd.feathered(bd.levelled(unlit_take.crop(box)), EDGE)
    lit = with_gold(bd.art_of(lit_img, f"root-gold-{V}", 1100), "root-gold")
    leaf_only(f"root-gold-{V}")
    unlit = bd.art_of(unlit_img, f"root-plain-{V}", 1100)
    return unlit, lit, soak_sprite(lit_img, unlit_img)


def matte_capsules(img):
    """The model painted the two capsules glossy, like oil softgels; Turmerific's are powder
    capsules. Their white highlight streaks are filled from the capsule colour around them."""
    a = np.asarray(img).copy()
    f = a.astype(np.float32) / 255
    hi, lo = f.max(axis=2), f.min(axis=2)
    sat = (hi - lo) / np.maximum(hi, 1e-4)
    golden = (sat > 0.35) & (hi > 0.45) & (f[..., 0] >= f[..., 1]) & (f[..., 1] > f[..., 2])
    h, w = golden.shape
    # The capsules lie right of the spoon's bowl: golden shapes there, each filled to its hull.
    zone = np.zeros_like(golden)
    zone[:, int(w * 0.6):] = True
    n, lab, st, _ = cv2.connectedComponentsWithStats((golden & zone).astype(np.uint8), 8)
    hull = np.zeros((h, w), np.uint8)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 0.004 * h * w:
            pts = cv2.findNonZero((lab == i).astype(np.uint8))
            cv2.fillConvexPoly(hull, cv2.convexHull(pts), 1)
    hull = cv2.erode(hull, np.ones((9, 9), np.uint8))
    shine = (hull > 0) & (sat < 0.32) & (hi > 0.8)
    shine = cv2.dilate(shine.astype(np.uint8), np.ones((5, 5), np.uint8))
    print(f"inside: {shine.mean():.2%} of the picture was capsule shine, filled")
    return Image.fromarray(cv2.inpaint(a, shine * 255, 9, cv2.INPAINT_TELEA))


def inside():
    img = matte_capsules(cropped("inside"))
    return with_gold(finish(img, "spoon"), "spoon")


def supply():
    """The opening's "One bottle" card: the daily painting's two capsules alone, ink on a clear ground
    (as NuriCell's capsule pair: over the paper it draws as a multiplied painting would)."""
    img = bd.levelled(cropped("daily"))
    a = np.asarray(img).astype(np.float32) / 255
    hi, lo = a.max(axis=2), a.min(axis=2)
    sat = (hi - lo) / np.maximum(hi, 1e-4)
    h, w = sat.shape
    gold = (sat > 0.3) & (hi > 0.35)
    gold[:, : int(w * 0.45)] = False
    gold[: int(h * 0.6)] = False
    ys, xs = np.nonzero(cv2.morphologyEx(gold.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)))
    pad = 24
    box = (xs.min() - pad, ys.min() - pad, xs.max() + pad, ys.max() + pad)
    crop = np.asarray(img.crop(box)).astype(np.float32)
    # Only the capsules and their grey outlines: each capsule's gold filled to its hull and widened
    # to take in the outline (their shadows run into the glass's, so the ink alone can't separate them).
    leaf = gold[box[1] : box[3], box[0] : box[2]].astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(leaf, 8)
    keep = np.zeros(leaf.shape, np.uint8)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 1000:
            cv2.fillConvexPoly(keep, cv2.convexHull(cv2.findNonZero((lab == i).astype(np.uint8))), 1)
    keep = cv2.dilate(keep, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (19, 19)))
    m = cv2.GaussianBlur(keep.astype(np.float32), (0, 0), 2)[..., None]
    crop = crop * m + 255 * (1 - m)
    small = Image.fromarray(np.clip(crop, 0, 255).astype(np.uint8))
    small = small.resize((150, round(small.height * 150 / small.width)), Image.LANCZOS)
    rgb = np.asarray(small).astype(np.float32)
    alpha = np.clip(255 - rgb.min(axis=2), 0, 255)
    colour = np.where(alpha[..., None] > 0, 255 - (255 - rgb) * 255 / np.maximum(alpha[..., None], 1), 255)
    rgba = np.dstack([np.clip(colour, 0, 255), alpha]).astype(np.uint8)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"capsules-{V}.webp"
    Image.fromarray(rgba, "RGBA").save(path, "WEBP", quality=90, method=6)
    print(f"{path.relative_to(REPO)}  {small.width}x{small.height}")
    return {"src": f"{URL}/capsules-{V}.webp", "width": small.width, "height": small.height}


def brushed_sum():
    """The painted 2 × 30 = 60 laid out again with even gaps (as build_nuricell.brushed_sum), and the
    centres of its three numbers as fractions of its width (the page sets a caption under each)."""
    flat = np.asarray(bd.levelled(bd.divided(bd.load(TAKES["sum"]))))
    dark = (flat.min(axis=2) < 150).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(cv2.dilate(dark, np.ones((5, 5), np.uint8)), 8)
    comps = [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] > 200]
    tallest = max(st[i, cv2.CC_STAT_HEIGHT] for i in comps)
    digits = sorted((i for i in comps if st[i, cv2.CC_STAT_HEIGHT] > 0.5 * tallest), key=lambda i: st[i, 0])
    signs = sorted((i for i in comps if i not in digits), key=lambda i: st[i, 0])
    if len(digits) != 5:
        raise SystemExit(f"expected the five digits of 2 30 60, found {len(digits)}")
    groups = [[digits[0]], digits[1:3], digits[3:5]]
    times = [i for i in signs if st[groups[0][-1], 0] < st[i, 0] < st[groups[1][0], 0]]
    equals = [i for i in signs if st[groups[1][-1], 0] < st[i, 0] < st[groups[2][0], 0]]
    pieces = [groups[0], times, groups[1], equals, groups[2]]
    if not times or not equals:
        raise SystemExit("the × or the = sign was not found")
    y0 = max(0, min(st[i, 1] for i in comps) - 40)
    y1 = min(flat.shape[0], max(st[i, 1] + st[i, 3] for i in comps) + 40)
    gap, pad = int(0.32 * tallest), int(0.25 * tallest)
    spans = [(min(st[i, 0] for i in p), max(st[i, 0] + st[i, 2] for i in p)) for p in pieces]
    width = sum(b - a for a, b in spans) + gap * 4 + pad * 2
    canvas = np.full((y1 - y0, width, 3), 255, np.uint8)
    x, centres = pad, []
    for k, (piece, (a, b)) in enumerate(zip(pieces, spans)):
        own = np.isin(lab[y0:y1, a:b], piece)[..., None]
        region = canvas[:, x : x + b - a]
        canvas[:, x : x + b - a] = np.where(own, np.minimum(region, flat[y0:y1, a:b]), region)
        if k % 2 == 0:
            centres.append(round((x + (b - a) / 2) / width, 4))
        x += b - a + gap
    art = bd.art_of(bd.feathered(Image.fromarray(canvas), EDGE), f"sum-{V}", 1400)
    art["numbers"] = [2, 30, 60]
    art["centres"] = centres
    return art


# The Buy scene, in the take's own fractions: the empty space between the leaves is centred on
# GAP_X (the page centres the bottle in the scene, so the crop is centred there too), the ground
# under it at FOOT (the bottle's glass stands there), the crop from TOP to BOTTOM. The bottle photo
# is 90% of the scene's width, as NuriCell's on its stroke and Propolis's in its scene (Mo, October
# 14: both bottles as big as NuriCell's). The front band holds the gold root slices at the foot.
GAP_X, FOOT, TOP, BOTTOM = 0.51, 0.905, 0.03, 0.97
BOTTLE_WIDTH = 0.9
FRONT_BAND, FRONT_FADE = 0.13, 0.04


def glass_gap():
    """How far above its picture's bottom the bottle photo's glass ends, as a share of its height."""
    a = np.asarray(Image.open(BOTTLE).convert("RGBA"))[..., 3]
    rows = np.nonzero((a > 200).sum(axis=1) > 20)[0]
    return (a.shape[0] - 1 - rows.max()) / a.shape[0]


def scene():
    img = bd.levelled(bd.divided(bd.load(TAKES["scene"])))
    w, h = img.size
    half = min(GAP_X, 1 - GAP_X) * w
    left, right = int(GAP_X * w - half), int(GAP_X * w + half)
    top, bottom = int(h * TOP), int(h * BOTTOM)
    art = bd.art_of(bd.feathered(img.crop((left, top, right, bottom)), EDGE), f"plant-{V}", 1100)
    bottle = Image.open(BOTTLE)
    cw, ch = right - left, bottom - top
    pic_h = BOTTLE_WIDTH * cw * bottle.height / bottle.width
    pic_bottom = FOOT * h + glass_gap() * pic_h
    art["bottle"] = {"width": BOTTLE_WIDTH, "bottom": round((bottom - pic_bottom) / ch, 4)}
    art["front"] = scene_front(art)
    return art


def scene_front(art):
    """What of the scene is laid again in front of the bottle: the painting's lowest band (fading out
    above it), but only where the bottle photo is, so a root slice crosses its foot and nothing else
    is painted twice (Green Bee Propolis's review, October 14). White elsewhere, so it multiplies to
    nothing. Cut for the bottle's place and the bottle photo as they are: run again if either changes."""
    scene_img = Image.open(OUT / f"plant-{V}.webp").convert("RGB")
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
    path = OUT / f"plant-front-{V}.webp"
    front.save(path, "WEBP", quality=88, method=6)
    print(f"{path.relative_to(REPO)}  {w}x{h}  {path.stat().st_size // 1024} KB")
    return f"{URL}/plant-front-{V}.webp"


def write_ts(art):
    head = [
        "// Generated by reference/ink-pages/turmerific/build_turmerific.py. Do not edit by hand: change",
        "// the script (or its TAKES) and run it again. Turmerific's ink paintings (October 16, 2026):",
        "// GPT Image 2.5 on rice paper, the paper divided out so each multiplies onto the page's own",
        "// paper; gold leaf as a light mask (`gold`). soak: the sprite of masks the gold soaks in",
        "// through, and how many it holds. scene.bottle: where the real bottle stands, as fractions of",
        "// the painting (its width, and its picture's bottom above the painting's); scene.front: the",
        "// painting's lowest share where the bottle stands, laid again in front of its foot.",
        "",
    ]
    TS.parent.mkdir(parents=True, exist_ok=True)
    TS.write_text("\n".join(head) + f"export const turmerificArt = {json.dumps(art, indent=2)} as const;\n",
                  encoding="utf-8", newline="\n")
    prettier = REPO / "node_modules/prettier/bin/prettier.cjs"
    subprocess.run(["node", str(prettier), "--write", str(TS)], cwd=REPO, check=True, capture_output=True)
    print(TS.relative_to(REPO))


if __name__ == "__main__":
    unlit, lit, soak = why()
    write_ts(
        {
            "rootPlain": unlit,
            "rootGold": lit,
            "soak": soak,
            "spoon": inside(),
            "capsules": supply(),
            "notebook": finish(cropped("research"), "notebook"),
            "glass": with_gold(finish(cropped("daily"), "glass"), "glass"),
            "sum": brushed_sum(),
            "scene": scene(),
        }
    )

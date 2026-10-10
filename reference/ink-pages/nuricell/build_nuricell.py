"""Build NuriCell's ink paintings (Mo, October 9, 2026; spec
docs/superpowers/specs/2026-10-09-nuricell-ink-design.md).

Originals: reference/ink-pages/nuricell/originals/gpt25-<take>.png (GPT Image 2.5 on rice paper;
prompts in prompts/; spend in reference/ink-pages/spend.md). Output: public/images/products/
nuricell/ink/*.webp (lossless plates in plates/, not committed) and
src/components/product/ink/nuricell-art.ts. About's treatments (reference/ink-pages/about/
build_about.py): the paper divided out and lifted to white so each painting multiplies onto the
page's paper with no box, the outer edge feathered, gold leaf kept as a light mask for the kit's
glint. The lantern's unlit take is registered onto its lit take and both share one crop, so the
light comes on in place; the unlit body is dimmed to dusk (dusk), so the light reads as it comes on.
The core-lit takes of Task 9 rounds 1-2 (the light laid on lit-v2 in code) were superseded by the
painted lit-v3; they and the other unshipped lantern files live in spares/. Only shipped pictures
are written to public/. The painted sum is laid out again with even gaps.

usage: python -X utf8 reference/ink-pages/nuricell/build_nuricell.py
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
OUT = REPO / "public/images/products/nuricell/ink"
URL = "/images/products/nuricell/ink"
TS = REPO / "src/components/product/ink/nuricell-art.ts"
# Bump when a shipped picture changes after it has been pushed (the image optimizer caches by URL).
V = "v1"
# The take of each painting that ships (the original's name after "gpt25-"). The lantern's v2 takes
# were chosen in Task 1 (v1 is kept only as a spare original); its lit take since Task 9 round 3 is
# lit-v3, painted as an edit of unlit-v2 (pale paper, a warm core, light under the rims, gold flecks).
TAKES = {
    "lantern-lit": "lantern-lit-v3",
    "lantern-unlit": "lantern-unlit-v2",
    "capsule": "P7-capsule",
    "books": "P7-stepping-books",
    "liu": "P11-liu-face-bold",
    "breakfast": "P7-egg-capsules",
    "sum": "P7-sum",
    "stroke": "P5-stroke",
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


def gilded(key, width, sat_from=0.3, pad=0.04):
    art = finish(cropped(key, pad), key, width)
    ba.gold_mask(f"{key}-{V}", sat_from=sat_from)
    art["gold"] = f"{URL}/{key}-{V}-gold.webp"
    return art


def lantern_body(unlit):
    """The lantern's paper body between its rims, from the unlit layer: a soft mask kept inside the
    body's own sides (the blur must not grey the haze next to it) and the body's box."""
    u = np.asarray(unlit).astype(np.float32)
    h, w = u.shape[:2]
    soft = cv2.GaussianBlur(u.min(axis=2), (0, 0), 6)
    dark = (u.min(axis=2) < 90).sum(axis=1)
    ext = [(y, *np.where(soft[y] < 244)[0][[0, -1]]) for y in range(h) if (soft[y] < 244).any()]
    span = np.median([r - l for _, l, r in ext])
    rims = [y for y in range(h) if dark[y] > 0.25 * span]
    top = max((y for y in rims if y < h // 2), default=0) + 1
    bottom = min((y for y in rims if y > h // 2), default=h) - 1
    rows = [(y, l, r) for y, l, r in ext if top <= y <= bottom]
    mask = np.zeros((h, w), np.float32)
    for y, l, r in rows:
        mask[y, l : r + 1] = 1
    mask = cv2.GaussianBlur(cv2.erode(mask, np.ones((1, 25), np.uint8)), (0, 0), 8)
    left, right = float(np.median([l for _, l, _ in rows])), float(np.median([r for _, _, r in rows]))
    return mask, (left, top, right, bottom)


# The unlit lantern at dusk (Ruling 32, final review): its paper body was near-white, so on the
# page's cream paper the light coming on read too gently. The body's paper is scaled by DUSK (its
# brush texture scaled, not flattened), toward the side tone of Mo's comp (2-why-lantern.jpg: about
# 200-215 on the page), still neutral grey. Strokes darker than STROKES[0] (ribs, cracks) keep their
# value, with a smooth step up to STROKES[1]; the rims, cap, base and cord lie outside the body.
# Variants 0.86 / 0.89 / 0.92 were judged on the page's paper beside lit-v3 and the comp.
DUSK = 0.89
STROKES = (140, 205)
# How far inside the lantern's ink the dimming mask stops before its blur (sigma 8): 3 sigma.
INSET = 24


def dusk_mask(unlit):
    """lantern_body's mask for dimming: the same body between the rims, eroded INSET px in every
    direction from the lantern's own ink before its blur, so the blur never greys the paper beside
    it. The ink's row by row extent, not lantern_body's blurred one: the brush-ragged sides have
    notches of bare paper that the blurred extent fills (round-1 measurement: up to 0.79 of the
    mask on paper 1px past the ink). The erosion runs over the rims too (not from the rim line), so
    the body is dimmed right up to the cap and the base; a 3px soft step at the rim line keeps the
    rims' own light streaks as they are."""
    a = np.asarray(unlit).astype(np.float32)
    h, w = a.shape[:2]
    _, (_, top, _, bottom) = lantern_body(unlit)
    ink = cv2.morphologyEx((a.min(axis=2) < 236).astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    rows = np.zeros((h, w), np.float32)
    for y in range(max(0, top - 2 * INSET), min(h, bottom + 2 * INSET + 1)):
        xs = np.flatnonzero(ink[y])
        if len(xs):
            rows[y, xs[0] : xs[-1] + 1] = 1
    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * INSET + 1, 2 * INSET + 1))
    mask = cv2.GaussianBlur(cv2.erode(rows, disc), (0, 0), 8)
    between = np.zeros((h, 1), np.float32)
    between[top : bottom + 1] = 1
    return mask * cv2.GaussianBlur(between, (0, 0), 3)


def dusk(unlit):
    """The unlit take with its paper body dimmed (DUSK), as it ships."""
    a = np.asarray(unlit).astype(np.float32)
    mask = dusk_mask(unlit)
    value = a @ np.array([0.299, 0.587, 0.114], np.float32)
    w = np.clip((value - STROKES[0]) / (STROKES[1] - STROKES[0]), 0, 1)
    scale = 1 - (1 - DUSK) * w * w * (3 - 2 * w) * mask
    return Image.fromarray(np.clip(np.rint(a * scale[..., None]), 0, 255).astype(np.uint8))


def gold_flecks(a, mask, dx, dy, n=16, sat_from=0.55, min_area=40, max_aspect=None):
    """The lit take's most saturated gold-leaf spots in the body's middle ring, at most n of them,
    70px or more apart: a 0/1 map (the flecks the kit's glint will catch). max_aspect leaves out
    long thin spots (warm light along a rib, not leaf)."""
    hi, lo = a.max(axis=2), a.min(axis=2)
    sat = (hi - lo) / np.maximum(hi, 1)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    hue = np.where((r >= g) & (g > b), 60 * (g - b) / np.maximum(hi - lo, 1), 0)
    gold = (sat > sat_from) & (hue > 22) & (hue < 56) & (hi > 150)
    ring = (np.abs(dy) < 0.55) & (np.abs(dx) < 0.8) & (mask > 0.9)
    found = cv2.morphologyEx((gold & ring).astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    k, lab, st, centres = cv2.connectedComponentsWithStats(found, 8)
    shaped = lambda i: max_aspect is None or max(st[i, 2], st[i, 3]) <= max_aspect * min(st[i, 2], st[i, 3])
    spots = sorted(
        (i for i in range(1, k) if min_area <= st[i, cv2.CC_STAT_AREA] <= 2500 and shaped(i)), key=lambda i: -st[i, cv2.CC_STAT_AREA]
    )
    chosen = []
    for i in spots:
        if all(np.hypot(*(centres[i] - centres[j])) > 70 for j in chosen):
            chosen.append(i)
        if len(chosen) >= n:
            break
    return np.isin(lab, chosen).astype(np.float32)


def fleck_mask(flecks, name, width=1000):
    """The gold mask for the flecks alone (ba.gold_mask would take the whole warm body for leaf)."""
    from PIL import ImageFilter

    h, w = flecks.shape
    alpha = Image.fromarray((np.clip(flecks, 0, 1) * 255).astype(np.uint8), "L")
    alpha = alpha.resize((width, round(h * width / w)), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.2))
    white = Image.new("L", alpha.size, 255)
    path = OUT / f"{name}-gold.webp"
    Image.merge("RGBA", (white, white, white, alpha)).save(path, "WEBP", quality=80, method=6)
    cover = float((np.asarray(alpha) > 128).mean())
    print(f"{path.relative_to(REPO)}  {alpha.width}x{alpha.height}  gold {cover:.2%} (flecks only)")


def lantern():
    """The unlit take (an edit of the lit one) registered onto the lit take, both cut by one box."""
    lit = bd.divided(bd.load(TAKES["lantern-lit"]))
    unlit = bd.divided(bd.load(TAKES["lantern-unlit"]))
    if unlit.size != lit.size:
        unlit = unlit.resize(lit.size, Image.LANCZOS)
    grey = lambda im: cv2.GaussianBlur(np.asarray(im.convert("L")).astype(np.float32) / 255, (0, 0), 3)
    warp = np.eye(2, 3, dtype=np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6)
    _, warp = cv2.findTransformECC(grey(lit), grey(unlit), warp, cv2.MOTION_EUCLIDEAN, criteria, None, 5)
    w, h = lit.size
    moved = cv2.warpAffine(
        np.asarray(unlit), warp, (w, h), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE
    )
    unlit = Image.fromarray(moved)
    print(f"lantern: unlit registered by ({warp[0, 2]:.1f}, {warp[1, 2]:.1f}) px")
    a, b = bd.ink_box(np.asarray(lit), pad=0.06), bd.ink_box(np.asarray(unlit), pad=0.06)
    box = (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))
    unlit = unlit.crop(box)
    # Each picture under a name of its own (a replaced picture needs a new filename: browsers and the
    # image optimizer cache by URL). The painted lit take (lit-v3), as it is. Its gold mask is its
    # leaf flecks alone: its warm glow is light, not leaf, and the kit's glint passes over leaf only.
    name = f"lantern-lit-{TAKES['lantern-lit'].rsplit('-', 1)[-1]}"
    lit_art = bd.art_of(bd.feathered(bd.levelled(lit.crop(box)), EDGE), name, 1100)
    a = np.asarray(bd.levelled(lit.crop(box))).astype(np.float32)
    mask, (l, t, r, b) = lantern_body(bd.levelled(unlit))
    h, w = mask.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dx, dy = (xx - (l + r) / 2) / ((r - l) / 2), (yy - (t + b) / 2) / ((b - t) / 2)
    # lit-v3's flecks are tiny and a little paler than lit-v2's leaf; roundish spots only.
    flecks = gold_flecks(a, mask, dx, dy, n=20, sat_from=0.46, min_area=25, max_aspect=2.5)
    fleck_mask(cv2.dilate(flecks, np.ones((3, 3), np.uint8)), name)
    lit_art["gold"] = f"{URL}/{name}-gold.webp"
    # The unlit take, registered onto this lit take and cropped by their shared box, its body dimmed
    # to dusk (v3 was the same crop, undimmed).
    unlit_art = bd.art_of(bd.feathered(dusk(bd.levelled(unlit)), EDGE), "lantern-unlit-v4", 1100)
    return unlit_art, lit_art


def brushed_sum():
    """The painted 3 × 30 = 90 with even gaps (the model wrote 30 and = touching), and the centres
    of its three numbers as fractions of its width (the page sets a caption under each)."""
    flat = np.asarray(bd.levelled(bd.divided(bd.load(TAKES["sum"]))))
    dark = (flat.min(axis=2) < 150).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(cv2.dilate(dark, np.ones((5, 5), np.uint8)), 8)
    comps = [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] > 200]
    tallest = max(st[i, cv2.CC_STAT_HEIGHT] for i in comps)
    digits = sorted((i for i in comps if st[i, cv2.CC_STAT_HEIGHT] > 0.5 * tallest), key=lambda i: st[i, 0])
    signs = sorted((i for i in comps if i not in digits), key=lambda i: st[i, 0])
    if len(digits) != 5:
        raise SystemExit(f"expected the five digits of 3 30 90, found {len(digits)}")
    groups = [[digits[0]], digits[1:3], digits[3:5]]
    # Each sign belongs between the two groups its centre lies between.
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
    art["numbers"] = [3, 30, 90]
    art["centres"] = centres
    return art


def write_ts(art):
    head = [
        "// Generated by reference/ink-pages/nuricell/build_nuricell.py. Do not edit by hand: change",
        "// the script (or its TAKES) and run it again. NuriCell's ink paintings (October 9, 2026): GPT",
        "// Image 2.5 on rice paper, the paper divided out so each multiplies onto the page's own paper;",
        "// gold leaf as a light mask (`gold`). sum.centres: its three numbers, as fractions of its width.",
        "",
    ]
    TS.parent.mkdir(parents=True, exist_ok=True)
    TS.write_text("\n".join(head) + f"export const nuricellArt = {json.dumps(art, indent=2)} as const;\n", encoding="utf-8", newline="\n")
    prettier = REPO / "node_modules/prettier/bin/prettier.cjs"
    subprocess.run(["node", str(prettier), "--write", str(TS)], cwd=REPO, check=True, capture_output=True)
    print(TS.relative_to(REPO))


if __name__ == "__main__":
    unlit, lit = lantern()
    write_ts(
        {
            "lanternUnlit": unlit,
            "lanternLit": lit,
            "capsule": gilded("capsule", 1200),
            "books": finish(cropped("books"), "books", 1100),
            "liu": finish(cropped("liu"), "liu", 1000),
            "breakfast": gilded("breakfast", 1100),
            "sum": brushed_sum(),
            "stroke": finish(cropped("stroke", pad=0.08), "stroke", 1400),
        }
    )

"""Build NuriCell's ink paintings (Mo, October 9, 2026; spec
docs/superpowers/specs/2026-10-09-nuricell-ink-design.md).

Originals: reference/ink-pages/nuricell/originals/gpt25-<take>.png (GPT Image 2.5 on rice paper;
prompts in prompts/; spend in reference/ink-pages/spend.md). Output: public/images/products/
nuricell/ink/*.webp (lossless plates in plates/, not committed) and
src/components/product/ink/nuricell-art.ts. About's treatments (reference/ink-pages/about/
build_about.py): the paper divided out and lifted to white so each painting multiplies onto the
page's paper with no box, the outer edge feathered, gold leaf kept as a light mask for the kit's
glint. The lantern's unlit take is registered onto its lit take and both share one crop, so the
light comes on in place (lantern). Only shipped pictures are written to public/. The painted sum is
laid out again with even gaps.

usage: python -X utf8 reference/ink-pages/nuricell/build_nuricell.py
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
OUT = REPO / "public/images/products/nuricell/ink"
URL = "/images/products/nuricell/ink"
TS = REPO / "src/components/product/ink/nuricell-art.ts"
# Bump when a shipped picture changes after it has been pushed (the image optimizer caches by URL).
V = "v1"
# The take of each painting that ships (the original's name after "gpt25-"); the lantern's are in
# GOLDRUSH.
TAKES = {
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


# The Why chapter's light since October 26, 2026: a lighthouse on the California coast. Mo first picked
# A of three California lights (a Gold Rush miner's lantern; the paper lantern read as Asian), saw it
# built beside the lighthouse sample, and switched to B the same day. Codex paintings, not GPT Image
# 2.5 (prompts why-lighthouse-*.txt): the lit take (a2, a looser repaint of a1), then the unlit take
# as an edit of it. The paper lantern's originals stay in originals/, the Gold Rush lantern's went
# to codes/bigh-archive/nuricell-why-unused-2026-10-26/ (outside the public repo); neither ships.
LIGHTHOUSE = {"lit": "why-lighthouse-a2", "unlit": "why-lighthouse-unlit-a2b"}
# The lit take's light: warm (red over blue) and light (its darkest channel), so the warm grey ink
# stays out. Its biggest patch is the lamp's light and its beam; its hull, widened by GLOW_PAD (the
# light bleeds a little past the glass) and softened by GLOW_SOFT, is where the unlit take is used.
WARM, LIGHT = 10, 190
GLOW_PAD, GLOW_SOFT = 61, 14
LUMA = np.array([0.299, 0.587, 0.114], np.float32)


def registered(moving, onto):
    """`moving` (an edit of `onto`, the same size) shifted and turned onto it, as their blurred greys
    say."""
    grey = lambda im: cv2.GaussianBlur(np.asarray(im.convert("L")).astype(np.float32) / 255, (0, 0), 3)
    warp = np.eye(2, 3, dtype=np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6)
    _, warp = cv2.findTransformECC(grey(onto), grey(moving), warp, cv2.MOTION_EUCLIDEAN, criteria, None, 5)
    w, h = onto.size
    moved = cv2.warpAffine(
        np.asarray(moving), warp, (w, h), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE
    )
    print(f"lantern: unlit registered by ({warp[0, 2]:.1f}, {warp[1, 2]:.1f}) px")
    return moved


def glow_mask(a):
    """Where the lit take's light is (WARM, LIGHT): its biggest patch's hull, widened and softened."""
    h, w = a.shape[:2]
    light = ((a[..., 0] - a[..., 2] > WARM) & (a.min(axis=2) > LIGHT)).astype(np.float32)
    light = (cv2.GaussianBlur(light, (0, 0), 4) > 0.5).astype(np.uint8)
    _, lab, st, _ = cv2.connectedComponentsWithStats(light, 8)
    glow = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    hull = cv2.convexHull(np.column_stack(np.nonzero(lab == glow)[::-1]).astype(np.int32))
    mask = np.zeros((h, w), np.uint8)
    cv2.fillConvexPoly(mask, hull, 1)
    mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (GLOW_PAD, GLOW_PAD)))
    return cv2.GaussianBlur(mask.astype(np.float32), (0, 0), GLOW_SOFT)[..., None]


def lantern():
    """The lighthouse lit and unlit, cut by one box. Only the unlit take's light is used (the lamp
    room's glass and the sky where the beam was), and in the painting's own ink colour (its values
    kept): everywhere else both pictures are the lit take's own strokes, so nothing but the light
    changes as it comes on."""
    load = lambda name: bd.divided(Image.open(HERE / "originals" / f"{name}.png").convert("RGB"))
    lit, unlit = load(LIGHTHOUSE["lit"]), load(LIGHTHOUSE["unlit"])
    if unlit.size != lit.size:
        unlit = unlit.resize(lit.size, Image.LANCZOS)
    a = np.asarray(lit).astype(np.float32)
    u = registered(unlit, lit).astype(np.float32)
    mask = glow_mask(a)
    ink = (a.min(axis=2) < 120) & (mask[..., 0] < 0.01)
    tint = (255 - a[ink].mean(axis=0)) / (255 - (a[ink] @ LUMA).mean())
    glass = 255 - (255 - u @ LUMA)[..., None] * tint
    plain = Image.fromarray(np.clip(np.rint(a * (1 - mask) + glass * mask), 0, 255).astype(np.uint8))
    # More air above and below than at the sides: the sea and the clouds already run to the
    # painting's sides, and the finial needs sky over it, clear of the feathered edge.
    (x0, _, x1, _), (_, y0, _, y1) = bd.ink_box(a.astype(np.uint8), pad=0.04), bd.ink_box(a.astype(np.uint8), pad=0.07)
    box = (x0, y0, x1, y1)
    # The gold mask is the lamp's leaf alone: the light round it and the beam are light, not leaf.
    lit_art = bd.art_of(bd.feathered(bd.levelled(lit.crop(box)), EDGE), f"lighthouse-lit-{V}", 1100)
    ba.gold_mask(f"lighthouse-lit-{V}")
    lit_art["gold"] = f"{URL}/lighthouse-lit-{V}-gold.webp"
    unlit_art = bd.art_of(bd.feathered(bd.levelled(plain.crop(box)), EDGE), f"lighthouse-unlit-{V}", 1100)
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


def capsule_pair():
    """The capsule's two halves alone, side by side (Mo, October 12: the opening's "One bottle" card,
    after Timeline's and Seed's buy boxes): cut from the shipped capsule painting (the halves lie at
    its bottom left and right), each faded to white away from its own ink so no powder or ground
    comes with it, a small gap between them."""
    capsule = Image.open(OUT / f"capsule-{V}.webp").convert("RGB")

    def half(box):
        a = np.asarray(capsule.crop(box)).astype(np.float32)
        ink = (a.mean(axis=2) < 235).astype(np.uint8) * 255
        keep = Image.fromarray(ink).filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(6))
        k = np.asarray(keep).astype(np.float32)[..., None] / 255
        return Image.fromarray(np.clip(a * k + 255 * (1 - k), 0, 255).astype(np.uint8))

    left, right = half((36, 872, 286, 1066)), half((905, 878, 1174, 1074))
    # White air on every side: the halves' ground touches the crop, and the page needs a white rim.
    gap, h, m = 14, max(left.height, right.height), 24
    pair = Image.new("RGB", (left.width + gap + right.width + 2 * m, h + 2 * m), (255, 255, 255))
    pair.paste(left, (m, m + h - left.height))
    pair.paste(right, (m + left.width + gap, m + h - right.height))
    art = finish(pair, "capsule-pair", 320)
    # Saved again as ink on a clear ground (black, its alpha the ink's darkness): over the paper it
    # draws exactly as a multiplied grey painting would, but needs no blend, so it sits inside the
    # opening's words, which settle in with a filter (a stacking context), without a white box.
    path = OUT / f"capsule-pair-{V}.webp"
    grey = np.asarray(Image.open(path).convert("L")).astype(np.float32)
    rgba = np.zeros((*grey.shape, 4), np.uint8)
    rgba[..., 3] = np.clip(255 - grey, 0, 255).astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(path, "WEBP", quality=90, method=6)
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
            "capsulePair": capsule_pair(),
            "books": finish(cropped("books"), "books", 1100),
            "liu": finish(cropped("liu"), "liu", 1000),
            "breakfast": gilded("breakfast", 1100),
            "sum": brushed_sum(),
            "stroke": finish(cropped("stroke", pad=0.08), "stroke", 1400),
        }
    )

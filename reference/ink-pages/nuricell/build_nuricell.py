"""Build NuriCell's ink paintings (Mo, October 9, 2026; spec
docs/superpowers/specs/2026-10-09-nuricell-ink-design.md).

Originals: reference/ink-pages/nuricell/originals/gpt25-<take>.png (GPT Image 2.5 on rice paper;
prompts in prompts/; spend in reference/ink-pages/spend.md). Output: public/images/products/
nuricell/ink/*.webp (lossless plates in plates/, not committed) and
src/components/product/ink/nuricell-art.ts. About's treatments (reference/ink-pages/about/
build_about.py): the paper divided out and lifted to white so each painting multiplies onto the
page's paper with no box, the outer edge feathered, gold leaf kept as a light mask for the kit's
glint. The lantern's unlit take is registered onto its lit take and both share one crop, so the
light comes on in place. The painted sum is laid out again with even gaps.

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
# were chosen in Task 1 (v1 is kept only as a spare).
TAKES = {
    "lantern-lit": "lantern-lit-v2",
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
    lit_art = finish(lit.crop(box), "lantern-lit", 1100)
    ba.gold_mask(f"lantern-lit-{V}", sat_from=0.25)
    lit_art["gold"] = f"{URL}/lantern-lit-{V}-gold.webp"
    return finish(unlit.crop(box), "lantern-unlit", 1100), lit_art


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

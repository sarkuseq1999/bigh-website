"""Build the ranch scenes of NuriCell's "Why these four work together" (Mo picked B, October 27, 2026;
ideas page reference/ink-pages/mockups/nuricell-pairs/). They replace the powder heaps, which read
as drugs.

From the Codex originals (originals/, prompts in prompts/), paper divided by its own colour, this cuts
for each pair a still painting and the parts that move, all the same size so they lie on each other:
- pair-stove: firewood (acetyl-L-carnitine, fuel in) and the stove (alpha-lipoic acid, energy out),
  flipped so the wood comes first, as the pair is read. pair-stove-gold: its gold fire alone.
- pair-windmill: the windmill (alpha-lipoic acid) filling its tank (creatine, energy kept on hand),
  without its wheel and without its falling water. Round the wheel it is Codex's painting of the same
  scene with the wheel taken away (originals/ranch-windmill-nowheel.png, prompt in prompts/), which
  paints the tower's head the blades hid. pair-windmill-fan: the wheel alone, square round its hub,
  to turn: the painting divided by the wheel-less one, so the two laid on each other are the
  painting again. pair-windmill-gold: the gold water, falling and in the tank.
- pair-rider: the Pony Express rider and his horse (choline and acetyl-L-carnitine, two halves of a
  messenger) carrying a letter. pair-rider-gold: the gold letter alone.
The still paintings multiply onto the page like the site's other paintings (paper divided by the 75th
percentile of the border, as build_questions.py does, edges faded to paper). The moving parts are
un-multiplied from white (a colour over paper becomes that colour with an alpha), as
build_nuricell_gold.py does, so they sit on any paper and move without a blend group round them.
Writes src/components/product/ink/nuricell-pairs.ts.

usage: python -X utf8 reference/ink-pages/nuricell-pairs/build_nuricell_pairs.py
"""

import json
import subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SRC = HERE / "originals"
OUT = REPO / "public/images/products/nuricell/ink"
URL = "/images/products/nuricell/ink"
TS = REPO / "src/components/product/ink/nuricell-pairs.ts"
V = "v1"
WIDTH = 1200  # the originals are 1448 x 1086

# The windmill, in the original's pixels. The wheel's hub and the reach of its blades. Round the
# wheel, and over the tail, the still painting is the wheel-less one. The wheel leaves out what the
# two paint a little differently and the wheel-less one keeps: the hub and the head it turns on, the
# vane, the tail's rod, the pump rod over the hub and the tower's poles. Under the tail's rod and the
# poles the blades are painted back in from round them; behind the pump rod are only spokes.
HUB = (483.5, 240.5)
BLADES = 166
STILL_HUB = 26  # the hub and the head beside it
TAIL = (600, 190, 800, 320)  # the vane and the end of its rod (left, top, right, bottom)
VANE = (633, 230, 300)  # its left edge, and its top and bottom there
TAIL_ROD = ([(498, 240), (544, 250), (600, 258), (640, 270)], 7)  # its line, half its width
PUMP_ROD = (490, 184, 508, 232)
POLES = 0.45  # darker than this in the wheel-less painting: its poles
# The falling water (left, top, right, bottom): from the pipe's mouth to the tank's back rim.
STREAM = (660, 492, 732, 699)
# Where it lands: the light spreads across the tank's gold from there.
FOOT = (706, 706)


def divided(name, flip=False):
    """The original with its paper divided out, so white is paper."""
    img = np.asarray(Image.open(SRC / f"{name}.png").convert("RGB")).astype(np.float32)
    if flip:
        img = img[:, ::-1]
    h, w = img.shape[:2]
    b = max(8, int(min(h, w) * 0.03))
    edge = np.concatenate([img[:b].reshape(-1, 3), img[-b:].reshape(-1, 3),
                           img[:, :b].reshape(-1, 3), img[:, -b:].reshape(-1, 3)])
    return np.clip(img / np.percentile(edge, 75, axis=0) * 255, 0, 255)


def gold_alpha(img):
    """Gold leaf: warm with real colour (chroma, not HSV saturation, which jumps on dark ink)."""
    hsv = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float32)
    hue = hsv[..., 0] * 2
    chroma = img.max(axis=2) - img.min(axis=2)
    soft = np.clip((chroma - 22) / 40, 0, 1) * ((hue > 15) & (hue < 62))
    core = cv2.morphologyEx((soft > 0.5).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(core, 8)
    keep = np.zeros_like(core)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] >= 40:  # leaf, not a warm speck in the ink
            keep[lab == i] = 1
    filled = keep.copy()
    contours, _ = cv2.findContours(keep, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(filled, contours, -1, 1, thickness=-1)  # pale highlights inside the leaf
    near = cv2.dilate(filled, np.ones((5, 5), np.uint8)) > 0
    return np.maximum(soft * near, cv2.erode(filled, np.ones((2, 2), np.uint8)).astype(np.float32))


def unmultiplied(c, a):
    """A colour over white with this alpha, as the colour itself (so alpha over paper matches)."""
    return np.clip(255 - (255 - c) / np.maximum(a, 0.06)[..., None], 0, 255)


def cutout(img, alpha=None):
    """RGBA: the painting's ink as alpha, or the given alpha."""
    a = 1 - img.min(axis=2) / 255 if alpha is None else alpha
    return np.dstack([unmultiplied(img, a), a * 255])


def sized(arr, scale):
    h, w = arr.shape[:2]
    return cv2.resize(arr, (round(w * scale), round(h * scale)), interpolation=cv2.INTER_AREA)


def faded(img):
    """The painting's edges faded to paper, so no hard edge shows on the page."""
    h, w = img.shape[:2]
    fy = np.clip(np.minimum(np.arange(h), np.arange(h)[::-1]) / (h * 0.05), 0, 1)
    fx = np.clip(np.minimum(np.arange(w), np.arange(w)[::-1]) / (w * 0.05), 0, 1)
    f = np.minimum.outer(fy, fx)[..., None]
    return 255 - (255 - img) * (f * f * (3 - 2 * f))


def save(arr, name):
    path = OUT / f"{name}-{V}.webp"
    mode, quality = ("RGBA", 88) if arr.shape[2] == 4 else ("RGB", 82)
    Image.fromarray(np.clip(arr, 0, 255).round().astype(np.uint8), mode).save(path, "WEBP", quality=quality, method=6)
    print(f"{path.relative_to(REPO)}  {arr.shape[1]}x{arr.shape[0]}  {path.stat().st_size // 1024} KB")
    return {"src": f"{URL}/{name}-{V}.webp", "width": arr.shape[1], "height": arr.shape[0]}


def box(rect, w, h):
    """(left, top, right, bottom) in pixels as fractions [left, top, width, height]."""
    l, t, r, b = rect
    return [round(l / w, 4), round(t / h, 4), round((r - l) / w, 4), round((b - t) / h, 4)]


def gold_box(a, pad=6, rows=None):
    """The gold's bounding box (fractions [left, top, width, height]), a little room round it."""
    m = a > 0.05
    if rows is not None:
        m[: rows[0]] = False
        m[rows[1] :] = False
    ys, xs = np.nonzero(m)
    h, w = a.shape
    return box((max(0, xs.min() - pad), max(0, ys.min() - pad), min(w, xs.max() + pad), min(h, ys.max() + pad)), w, h)


def painted(name, flip=False):
    img = divided(name, flip)
    a = gold_alpha(img)
    k = WIDTH / img.shape[1]
    return img, a, k


def stove():
    img, a, k = painted("ranch-stove", flip=True)
    return {
        "still": save(sized(faded(img), k), "pair-stove"),
        "gold": save(sized(cutout(img, a), k), "pair-stove-gold"),
        "glint": gold_box(a),
    }


def rider():
    img, a, k = painted("ranch-rider")
    return {
        "still": save(sized(faded(img), k), "pair-rider"),
        "gold": save(sized(cutout(img, a), k), "pair-rider-gold"),
        "glint": gold_box(a),
    }


def windmill():
    img, a, k = painted("ranch-windmill-v2")
    h, w = img.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.hypot(xx - HUB[0], yy - HUB[1])

    # The same scene with the wheel taken away, laid exactly on the painting.
    bare = divided("ranch-windmill-nowheel")
    grey = lambda im: cv2.cvtColor(im.astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.float32) / 255
    outside = ((r > BLADES + 10) & ~((xx >= TAIL[0]) & (xx <= TAIL[2]) & (yy >= TAIL[1]) & (yy <= TAIL[3])))
    warp = np.eye(2, 3, dtype=np.float32)
    _, warp = cv2.findTransformECC(grey(img), grey(bare), warp, cv2.MOTION_AFFINE,
                                   (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6),
                                   outside.astype(np.uint8), 5)
    bare = cv2.warpAffine(bare, warp, (w, h), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP,
                          borderMode=cv2.BORDER_REPLICATE)

    # Where the still painting is the wheel-less one: round the wheel and over the tail, feathered.
    tail = (xx >= TAIL[0]) & (xx <= TAIL[2]) & (yy >= TAIL[1]) & (yy <= TAIL[3])
    swap = cv2.GaussianBlur(((r < BLADES + 4) | tail).astype(np.float32), (0, 0), 3)[..., None]

    # The wheel: the painting divided by the wheel-less one inside its reach, but not the hub or the
    # vane; under the rods and the poles, the blades painted back in from round them.
    vane = (xx >= VANE[0]) & (yy >= VANE[1]) & (yy <= VANE[2])
    ring = (r > STILL_HUB) & (r < BLADES) & ~vane
    fan = np.where(ring[..., None], np.clip(img * 255 / np.maximum(bare, 1), 0, 255), 255.0)
    under = np.zeros((h, w), np.uint8)
    cv2.polylines(under, [np.array(TAIL_ROD[0], np.int32)], False, 1, TAIL_ROD[1] * 2)
    under = cv2.dilate((under.astype(bool) | (grey(bare) < POLES)).astype(np.uint8), np.ones((3, 3), np.uint8))
    fan = cv2.inpaint(fan.astype(np.uint8), (under.astype(bool) & ring).astype(np.uint8), 5,
                      cv2.INPAINT_TELEA).astype(np.float32)
    fan[~ring] = 255
    fan[PUMP_ROD[1] : PUMP_ROD[3], PUMP_ROD[0] : PUMP_ROD[2]] = 255  # only spokes behind it
    edge = np.clip((BLADES - r) / 3, 0, 1)[..., None]  # soft rim, no hard circle
    fan = 255 - (255 - fan) * edge
    side = 2 * (BLADES + 4)
    x0, y0 = round(HUB[0] - side / 2), round(HUB[1] - side / 2)
    fan_sq = fan[y0 : y0 + side, x0 : x0 + side]

    # The still painting: the wheel-less one round the wheel and the tail, the painting elsewhere; the
    # falling water painted over with what lies behind it (sky and hills); the tank's gold stays.
    still = img * (1 - swap) + bare * swap
    stream = np.zeros((h, w), np.uint8)
    l, t, rr, b = STREAM
    stream[t:b, l:rr] = (a[t:b, l:rr] > 0.03).astype(np.uint8)
    stream = cv2.dilate(stream, np.ones((5, 5), np.uint8))
    still = cv2.inpaint(still.astype(np.uint8), stream, 7, cv2.INPAINT_TELEA).astype(np.float32)

    hub = [round((HUB[0] - x0) / side, 4), round((HUB[1] - y0) / side, 4)]
    pool = gold_box(a, rows=(STREAM[3] - 8, h))
    return {
        "still": save(sized(faded(still), k), "pair-windmill"),
        "fan": {**save(sized(cutout(fan_sq), k), "pair-windmill-fan"),
                "box": box((x0, y0, x0 + side, y0 + side), w, h), "hub": hub},
        "gold": save(sized(cutout(img, a), k), "pair-windmill-gold"),
        "stream": box(STREAM, w, h),
        "glint": pool,
        "foot": [round((FOOT[0] / w - pool[0]) / pool[2], 4), round((FOOT[1] / h - pool[1]) / pool[3], 4)],
    }


def write_ts(art):
    head = [
        "// Generated by reference/ink-pages/nuricell-pairs/build_nuricell_pairs.py. Do not edit by hand:",
        "// change the script and run it again. The ranch scenes of NuriCell's What's inside chapter (Mo",
        "// picked B, October 27, 2026): each pair's still painting and the gold laid over it, the same",
        "// size. Boxes are [left, top, width, height] in the painting, fractions. glint: the box of the gold",
        "// that catches the light (the windmill's: the water in the tank). stores.fan: the wheel, square",
        "// round its hub (hub: its centre in the square). stores.stream: the falling water's box; foot:",
        "// where it lands, in the glint's box.",
        "",
    ]
    TS.write_text("\n".join(head) + f"export const nuricellPairs = {json.dumps(art)} as const;\n",
                  encoding="utf-8", newline="\n")
    prettier = REPO / "node_modules/prettier/bin/prettier.cjs"
    subprocess.run(["node", str(prettier), "--write", str(TS)], cwd=REPO, check=True, capture_output=True)
    print(TS.relative_to(REPO))


if __name__ == "__main__":
    write_ts({"lights": stove(), "stores": windmill(), "joins": rider()})

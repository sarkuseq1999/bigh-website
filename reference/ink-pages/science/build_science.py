"""Build the Science page's paintings.

Round 3 (Mo, November 4, 2026; spec docs/superpowers/specs/2026-11-04-science-california-design.md):
the page opens on the science ("Our science starts in the cell.") and turns from an Asian feel to
California. Every picture is a Codex painting (Mo's ChatGPT plan, no API spend; orders in prompts/,
sent by paint.sh) in the homepage close's way of painting, ink and wash with light colour:

- desk: the opening, a scientist's desk at an open window over golden hills (desk-window-2).
- town: "Why start with the cell?", San Francisco's houses at dusk (town-dusk-1) and the same
  painting with every window lit (town-lit-1, an edit of it, registered onto it here). The lit
  windows are found where the two differ (warm in the lit take, bare paper in the unlit one), laid
  in gold leaf and split into GROUPS layers, so the page can light them a few at a time.
- places: Dr. Liu's path, Berkeley, Salzburg and Today, each a Codex repaint of the October
  handscroll's cut with light washes (wash-<place>-1). Today keeps the handscroll's own gold-leaf
  sun, cut from its old picture and set in the new sky (SUN).
- journals: the research, bound journals on a library table, three laid open (journals-1).
- picnic: Ask BiGH Science, two camp mugs on a redwood picnic table (picnic-1).

Each painting's paper is divided out and lifted to white (reference/ink-pages/about/build_about.py),
so it multiplies onto the page's paper with no box, and its outer edge is feathered. Phones get
tighter cuts. The October pictures (the handscroll's Okayama cut, the scrolls, the health scenes,
the mugs) no longer ship; their originals stay in originals/ (gpt25-*).

usage: python -X utf8 reference/ink-pages/science/build_science.py
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
OUT = REPO / "public/images/science/ink"
URL = "/images/science/ink"
TS = REPO / "src/components/science/ink/science-art.ts"
ORIG = HERE / "originals"
PLATES = HERE / "plates"
# Bump when a shipped picture changes after it has been pushed (the image optimizer caches by URL).
V = "v3"
# The loose takes (November 4): the first takes (desk-window-2, town-dusk-1 and town-lit-1,
# journals-1, picnic-1) read as tidy illustrations; each was painted again far more loosely
# (paint.sh loose-*, town-loose-*), the town's lit take an edit of its loose one (lit-*).
TAKES = {
    "desk": "loose-desk-window-2-1",
    "town": "town-loose-1",
    "town-lit": "lit-town-loose-1",
    "berkeley": "wash-berkeley-1",
    "salzburg": "wash-salzburg-1",
    "today": "wash-today-1",
    "journals": "loose-journals-1-1",
    "picnic": "loose-picnic-1-1",
}
EDGE = 0.03
PHONE_FADE = 0.08
# The town's windows light in this many groups, one after another (science-ink.module.css).
GROUPS = 6
# Phone cuts (left, right) as shares of the wide picture's width; their cut ends fade to paper.
PHONE = {
    "desk": (0.0, 1.0),
    "town": (0.05, 0.72),
    "berkeley": (0.14, 0.86),
    "salzburg": (0.1, 0.94),
    "today": (0.12, 0.92),
    "journals": (0.18, 0.82),
    "picnic": (0.12, 0.88),
}
# Today's sun: the handscroll's gold leaf (old place-today-v1.webp), set at this point of the new
# painting (shares of its width and height), this wide (a share of its width).
SUN = (0.6, 0.2, 0.062)

bd.ORIG = ORIG
bd.URL = URL
bd.V = V
ba.OUT = OUT
ba.PLATES = PLATES


def load(key):
    return Image.open(ORIG / f"{TAKES[key]}.png").convert("RGB")


def faded(arr, left, right):
    """Fade an array's left and right ends to white (smoothstep over `left` / `right` px)."""
    w = arr.shape[1]
    x = np.arange(w, dtype=np.float32)
    k = np.ones(w, np.float32)
    if left:
        k = np.minimum(k, np.clip(x / left, 0, 1))
    if right:
        k = np.minimum(k, np.clip((w - 1 - x) / right, 0, 1))
    k = k * k * (3 - 2 * k)
    return arr * k[None, :, None] + 255.0 * (1 - k[None, :, None])


def faded_top(img, share):
    """Fade a picture's top to white over `share` of its height (smoothstep): the desk's window
    frame runs up to the painting's top edge, which would show as a cut line under the menu bar."""
    arr = np.asarray(img).astype(np.float32)
    h = arr.shape[0]
    k = np.clip(np.arange(h, dtype=np.float32) / max(1, round(h * share)), 0, 1)
    k = (k * k * (3 - 2 * k))[:, None, None]
    return to_img(arr * k + 255.0 * (1 - k))


def to_img(arr):
    return Image.fromarray(np.clip(np.rint(arr), 0, 255).astype(np.uint8))


def flat(img):
    """Paper divided out and lifted to white."""
    return bd.levelled(bd.divided(img))


def inked(img, pad=0.04, level=236):
    """Cropped to its ink (the box found on the picture itself)."""
    return img.crop(bd.ink_box(np.asarray(img), level=level, pad=pad))


def phone_cut(img, key):
    """The phone's cut of a wide picture: its middle (PHONE), trimmed to its ink, ends faded."""
    a, b = PHONE[key]
    crop = img.crop((round(img.width * a), 0, round(img.width * b), img.height))
    _, top, _, bottom = bd.ink_box(np.asarray(crop), pad=0.04)
    crop = crop.crop((0, top, crop.width, bottom))
    side = round(crop.width * PHONE_FADE)
    return to_img(faded(np.asarray(crop).astype(np.float32), side if a > 0 else 0, side if b < 1 else 0))


def art(img, name, width):
    return bd.art_of(bd.feathered(img, EDGE), f"{name}-{V}", width)


def with_phone(img, key, width=2400, phone_width=1100):
    out = art(img, key, width)
    out["phone"] = art(phone_cut(img, key), f"{key}-phone", phone_width)
    return out


def registered(moving, onto):
    """`moving` (an edit of `onto`, the same size) shifted and turned onto it, as their blurred
    greys say (as the NuriCell lighthouse's unlit take)."""
    grey = lambda im: cv2.GaussianBlur(np.asarray(im.convert("L")).astype(np.float32) / 255, (0, 0), 3)
    warp = np.eye(2, 3, dtype=np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6)
    _, warp = cv2.findTransformECC(grey(onto), grey(moving), warp, cv2.MOTION_EUCLIDEAN, criteria, None, 5)
    w, h = onto.size
    moved = cv2.warpAffine(
        np.asarray(moving), warp, (w, h), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE
    )
    print(f"town: lit take registered by ({warp[0, 2]:.1f}, {warp[1, 2]:.1f}) px")
    return Image.fromarray(moved)


def window_mask(unlit, lit):
    """Where the lit take is lamplight and the unlit take bare paper: the windows' panes, each a
    connected patch (tiny specks dropped). Returns the soft mask (0..1) and the label image."""
    u = np.asarray(unlit).astype(np.float32)
    l = np.asarray(lit).astype(np.float32)
    warm = (l[..., 0] - l[..., 2] > 70) & (l[..., 1] - l[..., 2] > 45)
    bare = u.min(axis=2) > 200
    m = (warm & bare).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    keep = np.zeros(n, bool)
    keep[1:] = st[1:, cv2.CC_STAT_AREA] >= 6
    lab = np.where(keep[lab], lab, 0)
    soft = cv2.GaussianBlur((lab > 0).astype(np.float32), (0, 0), 0.6)
    print(f"town: {int(keep.sum())} window panes")
    return np.clip(soft * 1.4, 0, 1), lab


def leaf_texture(h, w, seed=3, tile=96):
    """The lamps' gold: real gold leaf, the homepage sun's own (sun.webp, the leaf of "cells."),
    laid as random tiles from its solid middle, so each pane has the leaf's crinkle and colour."""
    sun = np.asarray(Image.open(REPO / "public/images/home-v2/ink/sun.webp").convert("RGBA")).astype(np.float32)
    ys, xs = np.nonzero(sun[..., 3] > 250)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    cy, cx, r = (y0 + y1) // 2, (x0 + x1) // 2, min(y1 - y0, x1 - x0) // 2
    # The solid square inside the disc.
    s = int(r * 1.3)
    core = sun[cy - s // 2 : cy + s // 2, cx - s // 2 : cx + s // 2, :3]
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w, 3), np.float32)
    for ty in range(0, h, tile):
        for tx in range(0, w, tile):
            oy, ox = rng.integers(0, core.shape[0] - tile), rng.integers(0, core.shape[1] - tile)
            patch = core[oy : oy + tile, ox : ox + tile]
            out[ty : ty + tile, tx : tx + tile] = patch[: h - ty, : w - tx]
    return out


def town():
    unlit = load("town")
    lit = registered(load("town-lit"), unlit)
    mask, lab = window_mask(unlit, lit)
    base = np.asarray(flat(unlit)).astype(np.float32)
    h, w = mask.shape
    gold = leaf_texture(h, w)
    lit_all = base * (1 - mask[..., None]) + gold * mask[..., None]
    # The panes in GROUPS groups: shuffled, so each group is spread over the whole town.
    ids = np.unique(lab)[1:]
    rng = np.random.default_rng(7)
    order = rng.permutation(len(ids))
    group_of = np.zeros(lab.max() + 1, np.int32) - 1
    for rank, i in enumerate(order):
        group_of[ids[i]] = rank * GROUPS // len(ids)
    # One crop for all of them: the unlit painting's ink box.
    box = bd.ink_box(base.astype(np.uint8), pad=0.03)
    x0, y0, x1, y1 = box
    out = {**art(to_img(base).crop(box), "town", 2400)}
    # The page lays the six layers over the town and never shows a lit picture from 960px; the
    # lit town is kept as a lossless plate (feathered as the town is), which the check compares
    # the layers with (check_science_art.py).
    bd.feathered(to_img(lit_all).crop(box), EDGE).save(PLATES / f"town-lit-{V}.png")
    # Each group's layer: the gold panes only, on transparency (RGBA), the same crop and size,
    # fading at the outer edge as the town does (bd.feathered: EDGE of its shorter side), so a
    # lamp by the edge never shines brighter than the paper round it.
    width = out["width"]
    layers = []
    pane = cv2.dilate((lab > 0).astype(np.uint8), np.ones((3, 3), np.uint8))
    near = cv2.dilate(lab.astype(np.float32), np.ones((3, 3), np.uint8)).astype(np.int32)
    ch, cw = y1 - y0, x1 - x0
    f = max(2.0, min(ch, cw) * EDGE)
    yy, xx = np.mgrid[0:ch, 0:cw].astype(np.float32)
    feather = np.clip(np.minimum.reduce([xx, yy, cw - 1 - xx, ch - 1 - yy]) / f, 0, 1)
    for g in range(GROUPS):
        sel = (group_of[np.maximum(near, 0)] == g) & (pane > 0)
        alpha = np.where(sel, mask, 0.0)[y0:y1, x0:x1] * feather
        rgba = np.dstack([gold[y0:y1, x0:x1], alpha * 255])
        img = Image.fromarray(np.clip(np.rint(rgba), 0, 255).astype(np.uint8), "RGBA")
        img = img.resize((width, out["height"]), Image.LANCZOS)
        name = f"town-lamps-{g + 1}-{V}"
        OUT.mkdir(parents=True, exist_ok=True)
        img.save(OUT / f"{name}.webp", "WEBP", quality=88, method=6)
        print(f"{(OUT / f'{name}.webp').relative_to(REPO)}  {(OUT / f'{name}.webp').stat().st_size // 1024} KB")
        layers.append(f"{URL}/{name}.webp")
    out["lamps"] = layers
    # The phone's cut of the town, unlit and lit (no groups: on a phone the lit picture fades in).
    a, b = PHONE["town"]
    for key, src in (("phone", base), ("phoneLit", lit_all)):
        crop = to_img(src).crop(box)
        crop = crop.crop((round(crop.width * a), 0, round(crop.width * b), crop.height))
        side = round(crop.width * PHONE_FADE)
        crop = to_img(faded(np.asarray(crop).astype(np.float32), side, side))
        out[key] = art(crop, "town-phone" if key == "phone" else "town-phone-lit", 1100)
    return out


def sun_leaf():
    """The handscroll's gold-leaf sun as an RGBA cut-out, from its old Today picture."""
    old = Image.open(PLATES / "place-today.png").convert("RGB")
    arr = np.asarray(old)
    m = cv2.morphologyEx(bd.gold_pixels(arr).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    i = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    x, y, w, h = (int(v) for v in st[i, :4])
    pad = int(max(w, h) * 0.3)
    return ba.leaf(old.crop((x - pad, y - pad, x + w + pad, y + h + pad))), w


def today(img):
    """Today's new painting with the handscroll's own gold sun in its sky."""
    leaf, disc = sun_leaf()
    cx, cy, size = SUN
    k = size * img.width / disc
    leaf = leaf.resize((round(leaf.width * k), round(leaf.height * k)), Image.LANCZOS)
    canvas = img.convert("RGBA")
    canvas.alpha_composite(leaf, (round(cx * img.width - leaf.width / 2), round(cy * img.height - leaf.height / 2)))
    return canvas.convert("RGB")


def place(key):
    img = flat(load(key))
    if key == "today":
        img = today(img)
    return inked(img, pad=0.03)


def write_ts(data):
    head = [
        "// Generated by reference/ink-pages/science/build_science.py. Do not edit by hand: change",
        "// the script (or its TAKES) and run it again. The Science page's paintings (round 3,",
        "// November 4, 2026): Codex paintings in ink and wash, the paper divided out so each",
        "// multiplies onto the page's own paper; the town's lamps as gold-leaf layers.",
        "",
    ]
    TS.write_text("\n".join(head) + f"export const scienceArt = {json.dumps(data, indent=2)} as const;\n", encoding="utf-8", newline="\n")
    prettier = REPO / "node_modules/prettier/bin/prettier.cjs"
    subprocess.run(["node", str(prettier), "--write", str(TS)], cwd=REPO, check=True, capture_output=True)
    print(TS.relative_to(REPO))


if __name__ == "__main__":
    desk = faded_top(inked(flat(load("desk")), pad=0.02), 0.07)
    data = {
        "desk": {**art(desk, "desk", 2000), "phone": art(phone_cut(desk, "desk"), "desk-phone", 1100)},
        "town": town(),
        "places": {key: with_phone(place(key), key, 1600, 1100) for key in ("berkeley", "salzburg", "today")},
        "journals": with_phone(inked(flat(load("journals")), pad=0.03), "journals"),
        "picnic": with_phone(inked(flat(load("picnic")), pad=0.03), "picnic"),
    }
    write_ts(data)

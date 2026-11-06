"""Mockups for Mo (November 6, 2026): other pictures for "Why start with the cell?", to compare with
the town at dusk. Mo kept the opening line and asked for a few other picture ideas to compare.
Each idea is built the way the town is (build_science.py town()): a loose Codex painting with its
lightable parts bare, a gilded Codex edit of it (paint.sh gild-*), registered onto it; where the
edit turned warm is laid in the homepage sun's gold leaf and split into GROUPS layers. Unlike the
windows, a butterfly's or a flower's gold falls in several patches (veins, a centre), so the
patches are grouped by what is near them (REACH) and each butterfly or flower lights at once.

Writes reference/ink-pages/mockups/science-why/<idea>/: base.webp, lamps-<k>.webp, phone.webp,
phone-lit.webp (the page's own sizes and cuts), lit.jpg and rest.jpg (whole, for the compare page)
and meta.json. shoot_why_mocks.py lays them into the real page in place of the town.

usage: python -X utf8 reference/ink-pages/mockups/science-why/build_why_mocks.py [idea ...]
"""

import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "reference/ink-pages/science"))
import build_science as bs  # noqa: E402

bd = bs.bd
ORIG = REPO / "reference/ink-pages/science/originals"
# idea: unlit take, gilded take, phone cut (left, right), REACH (px at 1536 wide)
IDEAS = {
    "monarchs": ("loose-monarchs-1-1", "gild-loose-monarchs-1-1", (0.1, 0.8), 9),
    "sunflowers": ("loose-sunflowers-1-1", "gild-loose-sunflowers-1-1", (0.12, 0.82), 7),
    "cheek": ("loose-cheek-cells-1-1", "gild-loose-cheek-cells-1-1", (0.0, 1.0), 5),
}
WIDTH, PHONE_W = 2400, 1100
# The town's own frame from 960px (1536 x 780), width over height.
RATIO = 1536 / 780


def gold_mask(unlit, lit):
    """Where the gilded take turned golden and the unlit one was not (both with their paper divided
    out): soft mask 0..1 and the hard mask."""
    u = np.asarray(bd.divided(unlit)).astype(np.float32)
    g = np.asarray(bd.divided(lit)).astype(np.float32)
    warm_g = g[..., 0] - g[..., 2]
    warm_u = u[..., 0] - u[..., 2]
    m = (warm_g > 60) & (warm_g - warm_u > 40) & (g[..., 1] - g[..., 2] > 30) & (u.mean(axis=2) > 110)
    m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    keep = np.zeros(n, bool)
    keep[1:] = st[1:, cv2.CC_STAT_AREA] >= 12
    hard = keep[lab]
    soft = cv2.GaussianBlur(hard.astype(np.float32), (0, 0), 0.6)
    return np.clip(soft * 1.4, 0, 1), hard


def leaf_smooth(h, w, seed=3, tile=200, step=140):
    """bs.leaf_texture's gold leaf (the homepage sun's), but its tiles overlap and blend (a raised
    cosine each), so a petal or a cell larger than a tile shows no square seams."""
    sun = np.asarray(Image.open(REPO / "public/images/home-v2/ink/sun.webp").convert("RGBA")).astype(np.float32)
    ys, xs = np.nonzero(sun[..., 3] > 250)
    cy, cx = (ys.min() + ys.max()) // 2, (xs.min() + xs.max()) // 2
    s = int(min(ys.max() - ys.min(), xs.max() - xs.min()) // 2 * 1.3)
    core = sun[cy - s // 2 : cy + s // 2, cx - s // 2 : cx + s // 2, :3]
    win = np.hanning(tile + 2)[1:-1]
    win = np.outer(win, win)[..., None].astype(np.float32) + 1e-3
    rng = np.random.default_rng(seed)
    acc = np.zeros((h + 2 * tile, w + 2 * tile, 3), np.float32)
    wsum = np.zeros((h + 2 * tile, w + 2 * tile, 1), np.float32)
    for ty in range(-tile // 2, h, step):
        for tx in range(-tile // 2, w, step):
            oy, ox = rng.integers(0, core.shape[0] - tile), rng.integers(0, core.shape[1] - tile)
            patch = core[oy : oy + tile, ox : ox + tile]
            if rng.random() < 0.5:
                patch = patch[:, ::-1]
            if rng.random() < 0.5:
                patch = patch[::-1]
            y, x = ty + tile // 2, tx + tile // 2
            acc[y : y + tile, x : x + tile] += patch * win
            wsum[y : y + tile, x : x + tile] += win
    out = acc / np.maximum(wsum, 1e-6)
    return out[tile // 2 : tile // 2 + h, tile // 2 : tile // 2 + w]


def from_gilded(lit, idea):
    """When the gilded take moved the drawing (the sunflowers), it is the drawing: its golden parts
    are the mask, and the resting picture is the same take with those parts washed pale."""
    g = np.asarray(bd.divided(lit)).astype(np.float32)
    h = g.shape[0]
    hard = (g[..., 0] - g[..., 2] > 105) & (g[..., 1] - g[..., 2] > 65) & (g[..., 0] > 170)
    hard[: int(h * 0.47)] = False  # the field only: not the far golden band under the oaks
    hard = cv2.morphologyEx(hard.astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8)) > 0
    soft = np.clip(cv2.GaussianBlur(hard.astype(np.float32), (0, 0), 0.8) * 1.3, 0, 1)
    base = np.asarray(bs.flat(lit)).astype(np.float32)
    lum = base.mean(axis=2, keepdims=True)
    pale = (255 - (255 - lum) * 0.3) * np.array([1.0, 0.975, 0.93], np.float32)
    base = base * (1 - soft[..., None]) + pale * soft[..., None]
    return soft, hard, base


def centres(unlit, hard, idea):
    """The flowers' dark centres or the cells' nuclei: dark blobs mostly ringed by gold. Their
    petals or cell bodies overlap into one patch, so each gold pixel lights with its nearest
    centre (a Voronoi split) instead of with its patch."""
    u = np.asarray(bd.divided(unlit)).astype(np.float32)
    lum = u.mean(axis=2)
    if idea == "cheek":
        dark = (u[..., 2] - u[..., 0] > 18) & (lum < 175)
    else:
        dark = lum < 125
    dark = cv2.morphologyEx(dark.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, lab, st, cen = cv2.connectedComponentsWithStats(dark, 8)
    gold = hard.astype(np.uint8)
    seeds = np.zeros(hard.shape, np.uint8)
    found = 0
    for i in range(1, n):
        area = st[i, cv2.CC_STAT_AREA]
        if area < 25:
            continue
        r = max(4, int(np.sqrt(area) * 0.8))
        blob = (lab == i).astype(np.uint8)
        ring = cv2.dilate(blob, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))) - blob
        if (gold[ring > 0]).mean() > 0.45:
            seeds[blob > 0] = 1
            found += 1
    print(f"{idea}: {found} centres")
    if idea == "sunflowers":
        # The far flowers' centres are too small to find: there, small patches of the field
        # (seeds on a loose grid, away from any centre found) light together.
        far = cv2.distanceTransform(1 - seeds, cv2.DIST_L2, 5) > 55
        rng = np.random.default_rng(11)
        h, w = hard.shape
        added = 0
        for y in range(0, h, 34):
            for x in range(0, w, 34):
                jy, jx = y + int(rng.integers(0, 20)), x + int(rng.integers(0, 20))
                if jy < h and jx < w and far[jy, jx] and hard[max(0, jy - 6) : jy + 6, max(0, jx - 6) : jx + 6].any():
                    seeds[jy : jy + 2, jx : jx + 2] = 1
                    added += 1
        print(f"{idea}: {added} patch seeds")
    return seeds


def save(img, path, width=None, quality=86):
    if width and img.width > width:
        img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    img.save(path, "WEBP", quality=quality, method=6)
    return img.size


def build(idea):
    unlit_name, lit_name, (a, b), reach = IDEAS[idea]
    out = HERE / idea
    out.mkdir(parents=True, exist_ok=True)
    unlit = Image.open(ORIG / f"{unlit_name}.png").convert("RGB")
    lit = Image.open(ORIG / f"{lit_name}.png").convert("RGB").resize(unlit.size, Image.LANCZOS)
    if idea == "sunflowers":
        mask, hard, base = from_gilded(lit, idea)
        unlit = lit
    else:
        lit = bs.registered(lit, unlit)
        mask, hard = gold_mask(unlit, lit)
        base = np.asarray(bs.flat(unlit)).astype(np.float32)
    h, w = mask.shape
    gold = leaf_smooth(h, w)
    if idea == "cheek":
        # Whole cells of solid leaf read as slabs: the leaf takes the cell's own wash (its light
        # and dark) and lets a little of it through.
        lum = base.mean(axis=2, keepdims=True)
        ref = np.median(lum[mask > 0.5]) if (mask > 0.5).any() else 200.0
        gold = gold * np.clip(lum / ref, 0.8, 1.12)
        mask = mask * 0.82
    lit_all = base * (1 - mask[..., None]) + gold * mask[..., None]
    # One butterfly or flower = the gold patches within REACH of each other.
    if idea == "monarchs":
        k = max(3, round(reach * w / 1536))
        blobs = cv2.dilate(hard.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
        n, blob = cv2.connectedComponents(blobs, connectivity=8)
    else:
        seeds = centres(unlit, hard, idea)
        n, seed_lab = cv2.connectedComponents(seeds, connectivity=8)
        # Nearest seed for every pixel: distance to the zero pixels (the seeds), labelled by them.
        _, near_lab = cv2.distanceTransformWithLabels(1 - seeds, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_CCOMP)
        # distanceTransformWithLabels numbers the seed components itself; map its labels to ours.
        ys, xs = np.nonzero(seeds)
        remap = np.zeros(near_lab.max() + 1, np.int32)
        remap[near_lab[ys, xs]] = seed_lab[ys, xs]
        blob = np.where(hard | (mask > 0), remap[near_lab], 0).astype(np.int32)
    rng = np.random.default_rng(7)
    order = rng.permutation(n - 1)
    group_of = np.zeros(n, np.int32) - 1
    for rank, i in enumerate(order):
        group_of[i + 1] = rank * bs.GROUPS // (n - 1)
    print(f"{idea}: {int(hard.sum())} gold px, {n - 1} lights")
    box = bd.ink_box(base.astype(np.uint8), pad=0.03)
    # From 960px the town's frame is about 1.97:1 (1536 x 780). A taller painting is cut to that,
    # round its gold's middle; a narrower one (the microscope's circle) gets bare paper either side.
    x0, y0, x1, y1 = box
    pad_x = 0
    if idea == "cheek" and (y1 - y0) * RATIO > (x1 - x0):
        pad_x = round((y1 - y0) * RATIO) - (x1 - x0)
    elif (x1 - x0) / RATIO < (y1 - y0):
        new_h = round((x1 - x0) / RATIO)
        rows = np.nonzero(hard[y0:y1, x0:x1].any(axis=1))[0]
        cy = y0 + int(np.median(rows)) if len(rows) else (y0 + y1) // 2
        y0 = int(np.clip(cy - new_h // 2, y0, y1 - new_h))
        y1 = y0 + new_h
    wide = (x0, y0, x1, y1)

    def widened(img, fill):
        if not pad_x:
            return img
        canvas = Image.new(img.mode, (img.width + pad_x, img.height), fill)
        canvas.paste(img, (pad_x // 2, 0))
        return canvas

    rest = widened(bd.feathered(bs.to_img(base).crop(wide), bs.EDGE), (255, 255, 255))
    size = save(rest, out / "base.webp", WIDTH)
    lit_img = widened(bd.feathered(bs.to_img(lit_all).crop(wide), bs.EDGE), (255, 255, 255))
    rest.convert("RGB").save(out / "rest.jpg", quality=88)
    lit_img.convert("RGB").save(out / "lit.jpg", quality=88)
    ch, cw = y1 - y0, x1 - x0
    f = max(2.0, min(ch, cw) * bs.EDGE)
    yy, xx = np.mgrid[0:ch, 0:cw].astype(np.float32)
    feather = np.clip(np.minimum.reduce([xx, yy, cw - 1 - xx, ch - 1 - yy]) / f, 0, 1)
    near = cv2.dilate(blob.astype(np.float32), np.ones((3, 3), np.uint8)).astype(np.int32)
    for g in range(bs.GROUPS):
        sel = group_of[np.maximum(near, 0)] == g
        alpha = np.where(sel, mask, 0.0)[y0:y1, x0:x1] * feather
        rgba = np.dstack([gold[y0:y1, x0:x1], alpha * 255])
        layer = Image.fromarray(np.clip(np.rint(rgba), 0, 255).astype(np.uint8), "RGBA")
        layer = widened(layer, (0, 0, 0, 0)).resize(size, Image.LANCZOS)
        layer.save(out / f"lamps-{g + 1}.webp", "WEBP", quality=88, method=6)
    phone = {}
    for key, src in (("phone", base), ("phone-lit", lit_all)):
        crop = bs.to_img(src).crop(box)
        crop = crop.crop((round(crop.width * a), 0, round(crop.width * b), crop.height))
        side = round(crop.width * bs.PHONE_FADE)
        crop = bs.to_img(bs.faded(np.asarray(crop).astype(np.float32), side if a > 0 else 0, side if b < 1 else 0))
        phone[key] = save(bd.feathered(crop, bs.EDGE), out / f"{key}.webp", PHONE_W)
    meta = {"width": size[0], "height": size[1], "phone": phone["phone"], "lights": int(n - 1)}
    (out / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"{idea}: {meta}")


if __name__ == "__main__":
    for idea in sys.argv[1:] or IDEAS:
        build(idea)

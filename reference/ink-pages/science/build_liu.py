"""Build Dr. Liu's part of the Science page: "the gold he studies".

Mo found the part plain (a small dark studio photograph on bare paper, November 11, 2026), saw five
ideas mocked on the real page (reference/ink-pages/mockups/science-liu/) and picked C: his painted
portrait in front of one huge cell, its mitochondria slivers of gold that drift slowly, as on the
page's first screen.

- The cell is a Codex painting with no person in it (originals/liu-cell-1.png, order
  prompts/liu-cell-1.txt): its paper divided out, so it multiplies onto the page's paper.
- He is the shipped painted portrait (public/images/products/nuricell/ink/liu-v1.webp): his real
  face, never generated. He hides the cell behind him (figure_cover), and his loose brush edge
  lies over it.
- The gold slivers that stand clear of him and of the plate's edges are painted out of the plate
  (gold(), plate()) and ship as pieces of one picture beside it (piece_of(), build_science.pieces()),
  so each can drift on its own; the rest stay painted where they are.
- Two plates: a wide one (bare paper on its left for the words, the cell running off the window's
  right edge) and a tall one for phones. Each has its own picture of drifting pieces.

Output: public/images/science/ink/liu-cell-<V>.webp, liu-cell-gold-<V>.webp, liu-cell-phone-<V>.webp,
liu-cell-phone-gold-<V>.webp and src/components/science/ink/liu-art.ts. Nothing else of the page is
rebuilt.

usage: python -X utf8 reference/ink-pages/science/build_liu.py
"""

import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_science as bs  # noqa: E402  (its helpers; importing it builds nothing)

bd = bs.bd
REPO, OUT, URL, ORIG = bs.REPO, bs.OUT, bs.URL, bs.ORIG
TS = REPO / "src/components/science/ink/liu-art.ts"
PORTRAIT = REPO / "public/images/products/nuricell/ink/liu-v1.webp"
TAKE = "liu-cell-1"
# Bump when a shipped picture changes after it has been pushed (the image optimizer caches by URL).
V = "v1"

# Each plate: its canvas (w, h); how much larger the painting is drawn and where its corner goes;
# his portrait's width and corner; where the plate dries out into the paper (shares of the canvas:
# left, right, top, foot); how far up from the foot he dries out; the width it ships at.
PLATES = {
    "wide": {
        "name": "liu-cell",
        "canvas": (2200, 1024),
        "scale": 1.25,
        "at": (420, -128),
        "figure": {"width": 640, "x": 1130, "y": 96},
        "fade": (0.0, 0.0, 0.07, 0.12),
        "dry": 0.14,
        "width": 2200,
    },
    "phone": {
        "name": "liu-cell-phone",
        "canvas": (1100, 1180),
        "scale": 1770 / 1536,
        "at": (-470, 0),
        "figure": {"width": 700, "x": 60, "y": 150},
        "fade": (0.05, 0.0, 0.06, 0.12),
        "dry": 0.14,
        "width": 1100,
    },
}
# A sliver drifts only if it keeps this far (canvas px) from him and from the plate's edges: it
# travels a few px and turns a little (people.module.css, --reach).
CLEAR = 22


def smooth_ramp(n, length, reverse=False):
    """0 -> 1 over `length` px (smoothstep), then 1; or the other way round."""
    x = np.clip(np.arange(n, dtype=np.float32) / max(length, 1), 0, 1)
    t = x * x * (3 - 2 * x) if length > 0 else np.ones(n, np.float32)
    return t[::-1] if reverse else t


def wobble(shape, seed, sigma=38):
    """Slow noise in -1..1: a fade's line wanders like a wash drying out, never a ruled gradient."""
    rng = np.random.default_rng(seed)
    field = cv2.GaussianBlur(rng.normal(0, 1, shape).astype(np.float32), (0, 0), sigma)
    return field / (np.abs(field).max() + 1e-6)


def paper_out(img):
    """Paper -> white, ink kept. The paper is the median of the brightest tenth of the picture
    (the cell runs off three of its edges, so the picture's frame is not paper, as build_about's
    divided() takes it to be)."""
    arr = np.asarray(img.convert("RGB")).astype(np.float32)
    lum = arr.mean(axis=2)
    paper = np.median(arr[lum >= np.quantile(lum, 0.9)], axis=0)
    return bs.to_img(np.clip(arr / paper * 255.0 * 1.02, 0, 255))


def placed(layer, canvas, x, y):
    """`layer` (h, w[, c]) on a zero canvas of `canvas` (w, h), its corner at x, y."""
    cw, ch = canvas
    out = np.zeros((ch, cw) + layer.shape[2:], np.float32)
    sx, sy, dx, dy = max(0, -x), max(0, -y), max(0, x), max(0, y)
    w, h = min(layer.shape[1] - sx, cw - dx), min(layer.shape[0] - sy, ch - dy)
    if w > 0 and h > 0:
        out[dy : dy + h, dx : dx + w] = layer[sy : sy + h, sx : sx + w]
    return out


def figure_cover(rgb):
    """How fully his portrait hides what is behind it. Solid through his body (his white shirt, his
    face and his glasses too), so the cell never shows through him; toward his outline it follows
    the paint itself, so the bare paper between his loose brush strokes lets the cell through."""
    dark = 255.0 - rgb.min(axis=2).astype(np.float32)
    solid = (dark > 18).astype(np.uint8)
    solid = cv2.morphologyEx(solid, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41)))
    _, lab, st, _ = cv2.connectedComponentsWithStats(solid, 8)
    body = (lab == 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))).astype(np.uint8)
    holes = body.copy()
    cv2.floodFill(holes, None, (0, 0), 1)
    body = body | (1 - holes)
    core = cv2.erode(body, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (71, 71)))
    core = np.clip(cv2.GaussianBlur(core.astype(np.float32), (0, 0), 12) * 1.6, 0, 1)
    paint = np.clip(cv2.GaussianBlur(dark, (0, 0), 1.2) / 46.0, 0, 1) * cv2.GaussianBlur(body.astype(np.float32), (0, 0), 3)
    return np.maximum(core, paint)


def kept(p):
    """Where the plate keeps its paint (1) and where it dries out into the paper (0)."""
    cw, ch = p["canvas"]
    left, right, top, foot = p["fade"]
    xs = np.arange(cw, dtype=np.float32)[None, :] + 0.035 * cw * wobble((ch, cw), 11)
    ys = np.arange(ch, dtype=np.float32)[:, None] + 0.03 * ch * wobble((ch, cw), 12)
    keep = np.ones((ch, cw), np.float32)
    if left:
        keep *= np.clip(xs / (left * cw), 0, 1)
    if right:
        keep *= np.clip((cw - 1 - xs) / (right * cw), 0, 1)
    if top:
        keep *= np.clip(ys / (top * ch), 0, 1)
    if foot:
        keep *= np.clip((ch - 1 - ys) / (foot * ch), 0, 1)
    return keep * keep * (3 - 2 * keep)


def him_on(p, portrait, cover):
    """His portrait's ink and how fully he covers, on the plate's canvas, drying out at the foot."""
    cw, ch = p["canvas"]
    f = p["figure"]
    fh = round(portrait.height * f["width"] / portrait.width)
    him = 255.0 - np.asarray(portrait.resize((f["width"], fh), Image.LANCZOS)).astype(np.float32)
    where = cv2.resize(cover, (f["width"], fh), interpolation=cv2.INTER_AREA)
    dry = smooth_ramp(ch, int(p["dry"] * ch), True)[:, None]
    return placed(him, (cw, ch), f["x"], f["y"]) * dry[..., None], placed(where, (cw, ch), f["x"], f["y"]) * dry


def disc(n):
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (n, n))


def gold(cell):
    """The painting's gold slivers: a label picture (0 where there is none) and each sliver's
    (label, x, y, w, h, area). The gold is this painting's one strong warm colour (red well over
    blue, and saturated); its sand washes are pale and stay out. build_science.lifted() is tuned
    to the opening's painting: here it took a sand wash for gold and left the slivers pale."""
    rgb = np.asarray(cell).astype(np.float32)
    sat = cv2.cvtColor(np.asarray(cell), cv2.COLOR_RGB2HSV)[..., 1].astype(np.float32) / 255.0
    key = ((rgb[..., 0] - rgb[..., 2] > 55) & (sat > 0.30)).astype(np.uint8)
    # A sliver's dry-brush streaks and pale middle belong to it: it travels as one piece.
    body = cv2.morphologyEx(key, cv2.MORPH_CLOSE, disc(9))
    count, labels, stats, _ = cv2.connectedComponentsWithStats(body, connectivity=8)
    found = [(i, *(int(v) for v in stats[i])) for i in range(1, count) if stats[i, cv2.CC_STAT_AREA] >= 60]
    return labels, found


def box_on(p, sliver, pad=0):
    """A sliver's box on the plate's canvas (x0, y0, x1, y1), as floats."""
    _, x, y, w, h, _ = sliver
    s, (ox, oy) = p["scale"], p["at"]
    return ox + (x - pad) * s, oy + (y - pad) * s, ox + (x + w + pad) * s, oy + (y + h + pad) * s


def adrift(p, sliver, where):
    """Whether a sliver may drift on this plate: whole on the plate, clear of its edges and of him
    (one that he half hides, or that the plate's edge cuts, stays painted where it is)."""
    cw, ch = p["canvas"]
    x0, y0, x1, y1 = box_on(p, sliver)
    x0, y0, x1, y1 = round(x0 - CLEAR), round(y0 - CLEAR), round(x1 + CLEAR), round(y1 + CLEAR)
    if x0 < 0 or y0 < 0 or x1 > cw or y1 > ch:
        return False
    return bool(where[y0:y1, x0:x1].max() <= 0.02)


PAD = 8


def piece_of(p, cell, labels, sliver, keep):
    """A drifting sliver as the kit's (x0, y0, RGBA piece, area), in the painting's own px: the
    painting's pixels under a soft cut of the sliver, thinned where this plate dries out into the
    paper, so it fades with the wash it lies on."""
    i, x, y, w, h, area = sliver
    rgb = np.asarray(cell)
    x0, y0 = max(0, x - PAD), max(0, y - PAD)
    x1, y1 = min(rgb.shape[1], x + w + PAD), min(rgb.shape[0], y + h + PAD)
    own = cv2.dilate((labels[y0:y1, x0:x1] == i).astype(np.uint8), disc(3)).astype(np.float32)
    alpha = np.clip(cv2.GaussianBlur(own, (0, 0), 1.1) * 1.25, 0, 1)
    s, (ox, oy) = p["scale"], p["at"]
    cw, ch = p["canvas"]
    # The plate's keep under this piece (canvas px), brought to the piece's own size.
    cx0, cy0 = int(np.floor(ox + x0 * s)), int(np.floor(oy + y0 * s))
    cx1, cy1 = int(np.ceil(ox + x1 * s)), int(np.ceil(oy + y1 * s))
    under = keep[max(0, cy0) : min(ch, cy1), max(0, cx0) : min(cw, cx1)]
    alpha *= cv2.resize(under, (x1 - x0, y1 - y0), interpolation=cv2.INTER_LINEAR)
    a = np.rint(alpha * 255).astype(np.uint8)
    return x0, y0, Image.fromarray(np.dstack([rgb[y0:y1, x0:x1], a]), "RGBA"), area


def plate(p, cell, labels, free, keep, him, where):
    """One plate: the cell with its drifting slivers painted out (the wash filled in behind them;
    every other sliver untouched), dried out at its edges, him in front."""
    cw, ch = p["canvas"]
    rgb = np.asarray(cell)
    # The hole is cut wide, so it swallows each sliver's pale rim and leaves no ghost behind it.
    hole = cv2.dilate(np.isin(labels, [s[0] for s in free]).astype(np.uint8), disc(23))
    base = cv2.inpaint(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), hole * 255, 9, cv2.INPAINT_TELEA)
    part = 255.0 - cv2.cvtColor(base, cv2.COLOR_BGR2RGB).astype(np.float32)
    s = p["scale"]
    part = cv2.resize(part, (round(part.shape[1] * s), round(part.shape[0] * s)), interpolation=cv2.INTER_LANCZOS4 if s > 1 else cv2.INTER_AREA)
    ink = placed(np.clip(part, 0, 255), (cw, ch), *p["at"]) * keep[..., None]
    out = (255.0 - ink * (1 - where)[..., None]) * (255.0 - him) / 255.0
    return bd.art_of(bs.to_img(out), f"{p['name']}-{V}", p["width"])


def write_ts(data):
    head = [
        "// Generated by reference/ink-pages/science/build_liu.py. Do not edit by hand: change the",
        "// script and run it again. Dr. Liu's part of the Science page (Mo picked C, November 11,",
        '// 2026, "the gold he studies"): his painted portrait in front of one huge cell (a Codex',
        "// painting, the paper divided out), a wide plate and a tall one for phones. Each plate's",
        "// slivers are the gold that stands clear of him and of the plate's edges: pieces of one",
        "// picture (gold), laid where they were painted, so each can drift on its own.",
        "",
    ]
    TS.write_text("\n".join(head) + f"export const liuArt = {json.dumps(data, indent=2)} as const;\n", encoding="utf-8", newline="\n")
    prettier = REPO / "node_modules/prettier/bin/prettier.cjs"
    subprocess.run(["node", str(prettier), "--write", str(TS)], cwd=REPO, check=True, capture_output=True)
    print(TS.relative_to(REPO))


if __name__ == "__main__":
    cell = paper_out(Image.open(ORIG / f"{TAKE}.png"))
    labels, slivers = gold(cell)
    portrait = Image.open(PORTRAIT).convert("RGB")
    cover = figure_cover(np.asarray(portrait))

    data = {}
    for key, p in PLATES.items():
        cw, ch = p["canvas"]
        keep = kept(p)
        him, where = him_on(p, portrait, cover)
        free = [sliver for sliver in slivers if adrift(p, sliver, where)]
        print(key, "slivers adrift:", len(free), "of", len(slivers))
        art = plate(p, cell, labels, free, keep, him, where)
        # This plate's own picture of pieces (each piece fades as this plate does).
        cut = [piece_of(p, cell, labels, sliver, keep) for sliver in free]
        sheet = bs.pieces(cut, cell.size, f"{p['name']}-gold-{V}")
        for item, sliver in zip(sheet["slivers"], free):
            x0, y0, x1, y1 = box_on(p, sliver, PAD)
            item["box"] = [round(x0 / cw, 4), round(y0 / ch, 4), round((x1 - x0) / cw, 4), round((y1 - y0) / ch, 4)]
        art["gold"] = sheet
        data[key] = art
    write_ts(data)

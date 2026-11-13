"""Idea A's gold-leaf kite (November 12, 2026): lifts the painted kite, its tail and its string out of
Codex's painting, lays the kite and the tail's bows in the site's gold leaf, and flies it lower in
the sky (where the painting had it, it sat under the menu bar on a laptop and was cut off).

  python -X utf8 reference/ink-pages/mockups/science-last/gild_kite.py

Writes into science/plates/last/ (git-ignored), paper divided out as the site ships its paintings:
  kite-wide-base.png   last-kite-2 with its kite, tail and string gone, a new string drawn from the
                       child's hand to where the kite now flies
  kite-wide-kite.png   the kite alone, gilded, on transparent, framed like the painting
  kite-wide-tail.png   its tail alone, the same
  kite-tall-*.png      the same kite flown in the tall painting for phones (tall-last-kite-2-<n>),
                       which was painted without one
and prints each pivot (the kite's lower point, where the string and the tail meet) as shares of
its painting, for choices.json. The page sways the kite and its tail about that point, so the
string stays tied on.
"""

import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent.parent
ORIG = HERE.parent.parent / "science" / "originals"
OUT = HERE.parent.parent / "science" / "plates" / "last"
OUT.mkdir(parents=True, exist_ok=True)
LEAF = REPO / "public" / "images" / "home-v2" / "ink" / "gold-leaf-word.webp"

# In last-kite-2 (1536 x 1024), by eye: the kite's four corners, the point where the string and
# the tail leave it, and where the string goes into the child's fist.
KITE = np.array([(1343, 86), (1397, 131), (1313, 209), (1284, 129)], np.float32)
POINT = np.array((1313, 208), np.float32)
FIST = np.array((1158, 592), np.float32)
# Everything of the kite, the tail and the string lies in this box (the fist is below it).
BOX = (1110, 70, 1420, 590)


def paper_of(a: np.ndarray) -> np.ndarray:
    lum = a.mean(axis=2)
    return np.median(a[lum >= np.quantile(lum, 0.9)], axis=0)


def divided(a: np.ndarray, paper: np.ndarray) -> np.ndarray:
    return np.clip(a / paper * 255.0 * 1.04, 0, 255)


def near_segment(shape, p, q, width):
    """Pixels within `width` of the segment p-q."""
    h, w = shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = q - p
    t = np.clip(((xx - p[0]) * d[0] + (yy - p[1]) * d[1]) / float(d @ d), 0, 1)
    return np.hypot(xx - (p[0] + t * d[0]), yy - (p[1] + t * d[1])) < width


def yy_of(h, w):
    return np.mgrid[0:h, 0:w][0].astype(np.float32)


def gold_leaf(shape, shade):
    """The site's gold leaf, tiled, darkened and lightened a little by the paint's own wash so the
    brush still shows through it. A touch less brown than the homepage's gold word (a seventh): at
    a kite's size, in the sky, that read as khaki."""
    leaf = np.asarray(Image.open(LEAF).convert("RGB")).astype(np.float32)
    reps = (-(-shape[0] // leaf.shape[0]), -(-shape[1] // leaf.shape[1]), 1)
    gold = np.tile(leaf, reps)[: shape[0], : shape[1]]
    gold = gold * 0.93 + np.array([110, 78, 20], np.float32) * 0.07
    return np.clip(gold * shade[..., None] * 1.05, 0, 255)


def lift():
    """The wide painting without its kite, and the kite and the tail as layers (paper not divided)."""
    a = np.asarray(Image.open(ORIG / "last-kite-2.png").convert("RGB")).astype(np.float32)
    h, w = a.shape[:2]
    paper = paper_of(a)
    marks = np.linalg.norm(a - paper, axis=2) > 22
    inbox = np.zeros((h, w), bool)
    x0, y0, x1, y1 = BOX
    inbox[y0:y1, x0:x1] = True
    marks &= inbox

    body = np.zeros((h, w), np.uint8)
    cv2.fillPoly(body, [KITE.astype(np.int32)], 1)
    body = cv2.dilate(body, np.ones((7, 7), np.uint8)).astype(bool)
    # The painted string, found row by row (the darkest mark near the line from the kite's point to
    # the fist) and fitted with a straight line: x = slope * y + offset.
    lum = a.mean(axis=2)
    rows, cols = [], []
    for y in range(int(POINT[1]) + 20, int(FIST[1]) - 6):
        guess = POINT[0] + (FIST[0] - POINT[0]) * (y - POINT[1]) / (FIST[1] - POINT[1])
        lo, hi = int(guess) - 10, int(guess) + 11
        x = lo + int(np.argmin(lum[y, lo:hi]))
        if lum[y, x] < 200:
            rows.append(y)
            cols.append(x)
    slope, offset = np.polyfit(rows, cols, 1)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    off_line = np.abs(xx - (slope * yy + offset)) / np.hypot(1, slope)
    along = (yy > POINT[1] + 3) & (yy < FIST[1] - 2)
    string = (off_line < 4.5) & along
    tail = marks & ~body & ~string
    # Keep only the tail itself: big enough to be more than a fleck, and not a leftover of the string.
    count, labels = cv2.connectedComponents(cv2.dilate(tail.astype(np.uint8), np.ones((5, 5), np.uint8)))
    keep = np.zeros_like(tail)
    for i in range(1, count):
        part = labels == i
        if part.sum() > 60 and np.median(off_line[part & tail]) > 9:
            keep |= part
    tail &= keep

    # The painting without them: every mark in the box (and the string down to the fist) filled in
    # from the paper around it.
    gone = (marks | body | string) & inbox
    gone |= (off_line < 4.5) & along & (lum < 228)
    gone = cv2.dilate(gone.astype(np.uint8), np.ones((5, 5), np.uint8))
    base = cv2.inpaint(a.clip(0, 255).astype(np.uint8), gone, 6, cv2.INPAINT_TELEA).astype(np.float32)

    # Gold for the yellow wash (the kite's paper and the tail's bows); the ink lines stay ink.
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    wash = ((r - b) > 45) & (lum > 120)
    ref = np.median(lum[wash & body]) if (wash & body).any() else 180.0
    shade = np.clip(0.65 + 0.35 * lum / ref, 0.9, 1.1)
    gold = gold_leaf((h, w), shade)
    soft = cv2.GaussianBlur(wash.astype(np.float32), (0, 0), 0.8)
    gilded = a * (1 - soft[..., None]) + gold * soft[..., None]

    def layer(mask, grow):
        m = cv2.dilate(mask.astype(np.uint8), np.ones((grow, grow), np.uint8)).astype(np.float32)
        alpha = cv2.GaussianBlur(m, (0, 0), 0.7)
        return np.dstack([gilded, alpha * 255.0])

    return a, paper, base, layer(body, 3), layer(tail, 3)


def fly(base, kite, tail, paper, at, size, fist, name, point=POINT, sag=12.0, mirror=False):
    """Lay the kite (and its tail) with its lower point at `at`, scaled by `size`, on a copy of
    `base`, with a string from `fist`; write the three plates and print the pivot. `mirror` flies
    it the other way round (its tail streaming to the right)."""
    h, w = base.shape[:2]
    sx = -size if mirror else size
    m = np.float32([[sx, 0, at[0] - point[0] * sx], [0, size, at[1] - point[1] * size]])

    def moved(img):
        return cv2.warpAffine(img, m, (w, h), flags=cv2.INTER_LANCZOS4, borderValue=(0, 0, 0, 0))

    k, t = moved(kite), moved(tail)
    # The string: an ink line from the fist up to the kite's lower point, sagging a little below
    # the straight line between them, drawn four times larger and shrunk so its edge is soft.
    up = 4
    canvas = Image.new("L", (w * up, h * up), 0)
    draw = ImageDraw.Draw(canvas)
    p0, p2 = np.float32(fist), np.float32(at)
    chord = p2 - p0
    normal = np.float32([-chord[1], chord[0]]) / np.linalg.norm(chord)
    if normal[1] < 0:
        normal = -normal
    p1 = (p0 + p2) / 2 + normal * sag
    pts = []
    for s in np.linspace(0, 1, 120):
        q = (1 - s) ** 2 * p0 + 2 * (1 - s) * s * p1 + s**2 * p2
        pts.append((float(q[0] * up), float(q[1] * up)))
    draw.line(pts, fill=255, width=round(1.35 * up), joint="curve")
    line = np.asarray(canvas.resize((w, h), Image.LANCZOS)).astype(np.float32) / 255.0
    # As dark as the painted string was (a warm grey-brown ink), a little paler toward the kite.
    fade = np.clip((yy_of(h, w) - at[1]) / max(1.0, fist[1] - at[1]), 0, 1)
    strength = line * (0.72 + 0.16 * fade)
    ink = np.array([78, 66, 56], np.float32)
    out = base * (1 - strength[..., None]) + ink * strength[..., None]

    for key, img in (("base", out), ("kite", k), ("tail", t)):
        if img.shape[2] == 4:
            rgb = divided(img[..., :3], paper)
            img = np.dstack([rgb, img[..., 3]])
            Image.fromarray(img.clip(0, 255).astype(np.uint8), "RGBA").save(OUT / f"{name}-{key}.png")
        else:
            Image.fromarray(divided(img, paper).clip(0, 255).astype(np.uint8)).save(OUT / f"{name}-{key}.png")
    print(f"{name}: pivot [{at[0] / w:.4f}, {at[1] / h:.4f}]")


if __name__ == "__main__":
    a, paper, base, kite, tail = lift()
    # The wide painting: the kite flies lower and a little left, its top about 22% down, so every
    # window from a short laptop to a tall desktop shows it whole under the menu bar.
    fly(base, kite, tail, paper, (1290.0, 348.0), 1.0, FIST, "kite-wide")
    # The tall painting for phones (painted without a kite): the kite beside the grandfather's
    # head, under the words, flown the other way round so its tail streams away from his head (and
    # downwind, as the grass bends). Its fist is found by eye
    # (python gild_kite.py <take> <fist x> <fist y> <kite x> <kite y> <size>).
    if len(sys.argv) >= 7:
        take = sys.argv[1]
        t = np.asarray(Image.open(ORIG / f"{take}.png").convert("RGB")).astype(np.float32)
        fist = (float(sys.argv[2]), float(sys.argv[3]))
        at = (float(sys.argv[4]), float(sys.argv[5]))
        size = float(sys.argv[6])
        # The kite layers are framed like the wide painting: re-frame them on the tall canvas.
        hh, ww = t.shape[:2]
        k = np.zeros((hh, ww, 4), np.float32)
        tl = np.zeros((hh, ww, 4), np.float32)
        x0, y0, x1, y1 = BOX
        cut_k = kite[y0:y1, x0:x1]
        cut_t = tail[y0:y1, x0:x1]
        k[: y1 - y0, : x1 - x0] = cut_k
        tl[: y1 - y0, : x1 - x0] = cut_t
        fly(t, k, tl, paper_of(t), at, size, fist, "kite-tall", point=POINT - np.float32([x0, y0]), mirror=True)

"""Outline the seven books in books-v1.webp as polygons in % of the image.

Each book gets a hand-set search box (nearest first); inside it the largest dark blob is the book,
and its convex hull, simplified, is the outline.

usage: python -X utf8 find_books.py <books.webp> <out-debug.png>
"""

import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from scipy.spatial import ConvexHull

BOXES = [  # x0, y0, x1, y1 in image px, nearest book first
    (30, 600, 520, 875),
    (278, 492, 662, 668),
    (500, 355, 768, 480),
    (642, 248, 870, 348),
    (760, 150, 930, 230),
    (860, 80, 1000, 140),
    (962, 30, 1070, 76),
]

src, out = sys.argv[1], sys.argv[2]
img = Image.open(src).convert("L")
a = np.asarray(img).astype(np.float32)
h, w = a.shape


def rdp(points, tol):
    if len(points) < 3:
        return points
    start, end = points[0], points[-1]
    line = end - start
    norm = np.hypot(*line) or 1.0
    rel = points - start
    dists = np.abs(line[0] * rel[:, 1] - line[1] * rel[:, 0]) / norm
    i = int(np.argmax(dists))
    if dists[i] > tol:
        return np.vstack([rdp(points[: i + 1], tol)[:-1], rdp(points[i:], tol)])
    return np.vstack([start, end])


def simplify(poly, tol):
    poly = poly.astype(np.float64)
    far = int(np.argmax(np.hypot(*(poly - poly.mean(0)).T)))
    ring = np.vstack([poly[far:], poly[:far]])
    opp = int(np.argmax(np.hypot(*(ring - ring[0]).T)))
    first = rdp(ring[: opp + 1], tol)
    second = rdp(np.vstack([ring[opp:], ring[:1]]), tol)
    return np.vstack([first[:-1], second[:-1]])


dbg = Image.open(src).convert("RGB")
d = ImageDraw.Draw(dbg)
for n, (x0, y0, x1, y1) in enumerate(BOXES, 1):
    crop = a[y0:y1, x0:x1] < 95
    crop = ndimage.binary_closing(crop, structure=np.ones((5, 5)))
    crop = ndimage.binary_fill_holes(crop)
    labels, count = ndimage.label(crop)
    sizes = ndimage.sum(crop, labels, range(1, count + 1))
    biggest = int(np.argmax(sizes)) + 1
    ys, xs = np.nonzero(labels == biggest)
    pts = np.column_stack([xs + x0, ys + y0])
    hull = pts[ConvexHull(pts).vertices]
    tol = max(2.0, (x1 - x0) / 80)
    s = simplify(hull, tol)
    d.rectangle((x0, y0, x1, y1), outline=(40, 120, 220))
    d.polygon([tuple(p) for p in s], outline=(220, 30, 30), width=2)
    d.text((x0 + 3, y0 + 2), str(n), fill=(40, 120, 220))
    pct = ", ".join(f"{x / w * 100:.1f}% {y / h * 100:.1f}%" for x, y in s)
    print(f'  "{pct}",  // book {n}: {len(s)} pts')
dbg.save(out)


# Soft masks, one per book: the outline grown a little and feathered, as white with that alpha, at
# half size (the page stretches it over the painting).
if len(sys.argv) > 3:
    from PIL import ImageFilter

    mask_dir = sys.argv[3]
    for n, (x0, y0, x1, y1) in enumerate(BOXES, 1):
        crop = a[y0:y1, x0:x1] < 95
        crop = ndimage.binary_closing(crop, structure=np.ones((5, 5)))
        crop = ndimage.binary_fill_holes(crop)
        labels, count = ndimage.label(crop)
        sizes = ndimage.sum(crop, labels, range(1, count + 1))
        ys, xs = np.nonzero(labels == int(np.argmax(sizes)) + 1)
        pts = np.column_stack([xs + x0, ys + y0])
        hull = pts[ConvexHull(pts).vertices]
        m = Image.new("L", (w, h), 0)
        ImageDraw.Draw(m).polygon([tuple(p) for p in hull], fill=255)
        grow = max(5, int((x1 - x0) / 50)) | 1
        m = m.filter(ImageFilter.MaxFilter(grow)).filter(ImageFilter.GaussianBlur(grow / 2))
        m = m.resize((w // 2, h // 2), Image.LANCZOS)
        rgba = Image.new("RGBA", m.size, (255, 255, 255, 0))
        rgba.putalpha(m)
        rgba.save(f"{mask_dir}/books-mask-v1-{n}.png", optimize=True)
    print("masks ->", mask_dir)

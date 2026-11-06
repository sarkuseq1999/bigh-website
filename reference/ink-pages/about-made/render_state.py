"""Render California (us-atlas states-10m topojson, US Census 1:10m) as a grey silhouette guide.

python -I render_state.py <states-10m.json> <out.png> <width> <height>

An equirectangular projection with the longitude scaled by cos(37 deg), the state centred and
fitted to 84% of the frame's height. Codex paints over it (paint.sh, the "state" orders).
"""
import json
import math
import sys

from PIL import Image, ImageDraw

LAT_MID = 37.0
FILL = 0.84


def decode(topo):
    sx, sy = topo["transform"]["scale"]
    tx, ty = topo["transform"]["translate"]
    arcs = []
    for arc in topo["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in arc:
            x += dx
            y += dy
            pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)
    return arcs


def ring(arcs, idx):
    pts = []
    for i in idx:
        a = arcs[i] if i >= 0 else list(reversed(arcs[~i]))
        pts.extend(a if not pts else a[1:])
    return pts


def main():
    src, out, w, h = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    topo = json.load(open(src, encoding="utf-8"))
    arcs = decode(topo)
    ca = next(g for g in topo["objects"]["states"]["geometries"] if g["properties"]["name"] == "California")
    polys = ca["arcs"] if ca["type"] == "MultiPolygon" else [ca["arcs"]]
    rings = [[ring(arcs, r) for r in poly] for poly in polys]
    k = math.cos(math.radians(LAT_MID))
    pts = [(lon * k, lat) for poly in rings for r in poly for lon, lat in r]
    x0, x1 = min(p[0] for p in pts), max(p[0] for p in pts)
    y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
    s = min(h * FILL / (y1 - y0), w * 0.9 / (x1 - x0))
    ox = (w - (x1 - x0) * s) / 2
    oy = (h - (y1 - y0) * s) / 2

    def px(lon, lat):
        return (ox + (lon * k - x0) * s, h - oy - (lat - y0) * s)

    img = Image.new("L", (w, h), 255)
    d = ImageDraw.Draw(img)
    for poly in rings:
        for n, r in enumerate(poly):
            d.polygon([px(lon, lat) for lon, lat in r], fill=150 if n == 0 else 255)
    img.save(out)
    print(json.dumps({"scale": s, "box": [round(ox), round(oy), round(ox + (x1 - x0) * s), round(oy + (y1 - y0) * s)]}))


main()

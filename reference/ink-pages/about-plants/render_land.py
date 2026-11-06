"""Render Natural Earth land (world-atlas topojson) as a silhouette in a Miller projection.

python render_land.py <land.json> <out.png> <width> <height>
Prints the pixel position of each named place as JSON.
"""
import json
import math
import sys

from PIL import Image, ImageDraw

LON0, LON1 = -150.0, 96.0
LAT0, LAT1 = -45.0, 65.0
PLACES = {
    "california": (-120.0, 36.8),
    "minas": (-44.5, -18.6),
    "turmeric": (77.7, 13.0),
    "grape": (11.0, 43.5),
    "pine": (-1.0, 44.2),
}


def miller(lat):
    return 1.25 * math.log(math.tan(math.pi / 4 + 0.4 * math.radians(lat)))


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
    land = topo["objects"]["land"]
    geoms = land["geometries"] if land["type"] == "GeometryCollection" else [land]
    y0, y1 = miller(LAT0), miller(LAT1)
    # Fit the lon range to the width; centre the lat range vertically.
    kx = w / math.radians(LON1 - LON0)
    ky = kx
    hy = (y1 - y0) * ky
    off = (h - hy) / 2

    def px(lon, lat):
        return ((math.radians(lon - LON0)) * kx, h - off - (miller(max(-80, min(80, lat))) - y0) * ky)

    img = Image.new("L", (w, h), 255)
    d = ImageDraw.Draw(img)
    for g in geoms:
        polys = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
        for poly in polys:
            for k, r in enumerate(poly):
                raw = ring(arcs, r)
                if min(lat for _, lat in raw) < -60:
                    continue
                unwrapped = [raw[0]]
                for lon, lat in raw[1:]:
                    prev = unwrapped[-1][0]
                    while lon - prev > 180:
                        lon -= 360
                    while lon - prev < -180:
                        lon += 360
                    unwrapped.append((lon, lat))
                shift = 0
                while min(lon for lon, _ in unwrapped) + shift < -180:
                    shift += 360
                pts = [px(lon + shift, lat) for lon, lat in unwrapped]
                d.polygon(pts, fill=0 if k == 0 else 255)
    img.save(out)
    print(json.dumps({k: [round(v) for v in px(*p)] for k, p in PLACES.items()}))


main()

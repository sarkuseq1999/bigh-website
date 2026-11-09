"""Render Natural Earth land (world-atlas topojson) on a globe, as a grey guide for Codex.

python render_globe.py <land.json> <out.png> <width> <height> <lon0> <lat0> <radius>

An orthographic view centred on (lon0, lat0): the land drawn first on a 4096 x 2048
equirectangular raster, then each pixel of the disc looked up through the inverse projection.
The disc is light grey, the land darker. Prints the disc's centre and radius and the pixel of
each named place (null when it is on the far side).
"""
import json
import math
import sys

import numpy as np
from PIL import Image, ImageDraw

PLACES = {"california": (-120.0, 36.8)}
EW, EH = 4096, 2048


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


def land_raster(topo):
    arcs = decode(topo)
    land = topo["objects"]["land"]
    geoms = land["geometries"] if land["type"] == "GeometryCollection" else [land]
    img = Image.new("L", (EW, EH), 0)
    d = ImageDraw.Draw(img)
    ex = lambda lon, lat: ((lon + 180) / 360 * EW, (90 - lat) / 180 * EH)
    for g in geoms:
        polys = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
        for poly in polys:
            for k, r in enumerate(poly):
                raw = ring(arcs, r)
                un = [raw[0]]
                for lon, lat in raw[1:]:
                    prev = un[-1][0]
                    while lon - prev > 180:
                        lon -= 360
                    while lon - prev < -180:
                        lon += 360
                    un.append((lon, lat))
                for shift in (-360, 0, 360):
                    d.polygon([ex(lon + shift, lat) for lon, lat in un], fill=255 if k == 0 else 0)
    return np.asarray(img) > 127


def main():
    src, out = sys.argv[1], sys.argv[2]
    w, h = int(sys.argv[3]), int(sys.argv[4])
    lon0, lat0, radius = float(sys.argv[5]), float(sys.argv[6]), float(sys.argv[7])
    topo = json.load(open(src, encoding="utf-8"))
    land = land_raster(topo)
    cx, cy = w / 2, h / 2
    ys, xs = np.mgrid[0:h, 0:w]
    x = (xs + 0.5 - cx) / radius
    y = -(ys + 0.5 - cy) / radius
    rho = np.sqrt(x * x + y * y)
    inside = rho <= 1
    c = np.arcsin(np.clip(rho, 0, 1))
    phi0, lam0 = math.radians(lat0), math.radians(lon0)
    with np.errstate(invalid="ignore", divide="ignore"):
        lat = np.arcsin(np.cos(c) * math.sin(phi0) + np.where(rho > 0, y * np.sin(c) * math.cos(phi0) / rho, 0))
        lon = lam0 + np.arctan2(x * np.sin(c), rho * np.cos(c) * math.cos(phi0) - y * np.sin(c) * math.sin(phi0))
    lon_d = (np.degrees(lon) + 180) % 360 - 180
    lat_d = np.degrees(lat)
    ex = np.clip(((lon_d + 180) / 360 * EW).astype(int), 0, EW - 1)
    ey = np.clip(((90 - lat_d) / 180 * EH).astype(int), 0, EH - 1)
    is_land = inside & land[ey, ex]
    img = np.full((h, w), 255, np.uint8)
    img[inside] = 225
    img[is_land] = 150
    Image.fromarray(img).save(out)

    def px(lon_p, lat_p):
        phi, lam = math.radians(lat_p), math.radians(lon_p)
        cosc = math.sin(phi0) * math.sin(phi) + math.cos(phi0) * math.cos(phi) * math.cos(lam - lam0)
        if cosc < 0:
            return None
        xx = math.cos(phi) * math.sin(lam - lam0)
        yy = math.cos(phi0) * math.sin(phi) - math.sin(phi0) * math.cos(phi) * math.cos(lam - lam0)
        return [round(cx + xx * radius), round(cy - yy * radius)]

    print(json.dumps({"centre": [cx, cy], "radius": radius, "places": {k: px(*v) for k, v in PLACES.items()}}))


main()

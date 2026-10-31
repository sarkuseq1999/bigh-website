"""Tint the homepage's ink paintings with a thin "green spring" watercolour (Mo's pick, October 16,
2026, from three tests and two live versions; ink-color.tsx serves the results).

Each painting is ink on white (the page multiplies it onto its rice paper). Ink is treated as a
pigment: optical density D = -ln(grey). A coloured pigment absorbs each channel in its own ratio,
so the new colour is exp(-D * ratio). Pale washes take the light pigment, the heavy strokes the dark
one (like distance haze in a real watercolour), and the blackest lines stay nearly black. Small
soft "washes" add a spot of colour on chosen objects. Gold leaf is left exactly as it is.

Writes public/images/home-v2/ink/spring/<same name>.webp for each painting the homepage tints.
usage: python -X utf8 reference/home-v2/ink/recolor/recolor.py
"""

from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

SRC = Path(__file__).resolve().parents[4] / "public" / "images" / "home-v2" / "ink"
OUT = SRC


def rgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i : i + 2], 16) for i in (0, 2, 4)], dtype=np.float64) / 255


def pig(h):
    d = -np.log(np.clip(rgb(h), 1e-3, 1))
    return d / d.mean()


def smooth(x, a, b):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def noise(h, w, cells, seed):
    """Soft low-frequency noise 0..1 (a watercolour wash is never even)."""
    rng = np.random.default_rng(seed)
    small = Image.fromarray((rng.random((cells, max(2, int(cells * w / h)))) * 255).astype(np.uint8))
    return np.asarray(small.resize((w, h), Image.BICUBIC), dtype=np.float64) / 255


def blob(h, w, cx, cy, rx, ry, seed=0, rough=0.35):
    y, x = np.mgrid[0:h, 0:w]
    x = x / w
    y = y / h
    d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
    m = np.exp(-d * 2.2)
    if rough:
        m = m * (1 - rough + rough * 2 * noise(h, w, 9, seed))
    return np.clip(m, 0, 1)


def ramp(D, stops):
    """Per-pixel pigment ratio, interpolated along density through (density, hex) stops."""
    ds = [s[0] for s in stops]
    ps = [pig(s[1]) for s in stops]
    out = np.empty(D.shape + (3,))
    for c in range(3):
        out[..., c] = np.interp(D, ds, [p[c] for p in ps])
    return out


def edge_fade(h, w, frac=0.08):
    """1 inside, 0 at the picture's edges, so no wash ever shows the picture's rectangle."""
    y, x = np.mgrid[0:h, 0:w]
    fx = smooth(np.minimum(x, w - 1 - x) / w, 0, frac)
    fy = smooth(np.minimum(y, h - 1 - y) / h, 0, frac)
    return fx * fy


def paint(name, stops, s=1.0, washes=(), keep_black=0.65, gold_keep=True, spots=()):
    im = Image.open(SRC / name)
    alpha = None
    if im.mode == "RGBA":
        alpha = np.asarray(im.split()[3])
    a = np.asarray(im.convert("RGB"), dtype=np.float64) / 255
    h, w = a.shape[:2]
    grey = a.mean(axis=2)
    D = -np.log(np.clip(grey, 1 / 255, 1))
    A = ramp(D, stops)
    A = 1 + s * (A - 1)
    k = (smooth(D, 1.5, 3.2) * keep_black)[..., None]
    A = A * (1 - k) + k
    T = np.exp(-D[..., None] * A)
    fade = edge_fade(h, w)
    for wash in washes:
        m = wash["mask"](h, w) * fade
        T = T * np.exp(-m[..., None] * wash["d"] * pig(wash["hex"]))
    # Spots re-colour the ink itself in a soft region (a petal, a crown) instead of laying a wash.
    for spot in spots:
        m = spot["mask"](h, w) * spot.get("amount", 1.0)
        if spot.get("light_only"):
            m = m * (1 - smooth(D, spot["light_only"][0], spot["light_only"][1]))
        if spot.get("min_d"):
            # Leave the bare paper (its faint fibre) alone: only painted marks take the colour.
            m = m * smooth(D, spot["min_d"][0], spot["min_d"][1])
        m = m[..., None]
        Ds = D[..., None] * (1 + spot.get("s", 1.0) * (pig(spot["hex"]) - 1))
        T = T * (1 - m) + np.exp(-Ds) * m
    if gold_keep:
        sat = a.max(axis=2) - a.min(axis=2)
        g = smooth(sat, 0.06, 0.16)[..., None]
        T = T * (1 - g) + a * g
    out = (np.clip(T, 0, 1) * 255 + 0.5).astype(np.uint8)
    img = Image.fromarray(out, "RGB")
    if alpha is not None:
        img.putalpha(Image.fromarray(alpha))
    return img




# ---------------------------------------------------------------- the palette
# Two other palettes were tried and set aside: "small touches" (grey ink with spots of colour)
# and "coastal fog" (blue-grey). The cell takes its own cooler ink (`mito`) so
# the gold leaf stands out; the still lifes take `still` (a green vase would read as celadon).
DIRS = {
    # Green spring: blue distance, sage-green hills, warm where the sun is.
    "spring": dict(
        stops=[(0.0, "#adc4da"), (0.3, "#a9c0d4"), (0.8, "#8fa77f"), (1.6, "#4a5a42"), (2.6, "#2e302b")],
        s=0.6,
        mito=[(0.0, "#a8c2d8"), (0.6, "#93a8b6"), (1.6, "#34404a"), (2.6, "#26292c")],
        sun="#f3bf92",
        leaf="#8fae7c",
        blossom="#f0a3ad",
        fruit="#dcc95e",
        tea="#c9a35e",
        crown="#d4482f",
        button="#26402f",
        still=[(0.0, "#b3c6d8"), (0.4, "#a7b5bf"), (1.2, "#6f7468"), (2.4, "#2e302b")],
    ),
}


def cover(D, radius):
    """Where the ink is, softened: keeps a wash inside the drawn object, not a round stain."""
    im = Image.fromarray((np.clip(D / 2.5, 0, 1) * 255).astype(np.uint8))
    return np.asarray(im.filter(ImageFilter.GaussianBlur(radius)), dtype=np.float64) / 255


def obj(cx, cy, rx, ry, seed, lo=0.03, hi=0.12, radius=10, src=None):
    """A wash on one object: a soft region times the object's own ink coverage."""

    def f(h, w):
        a = np.asarray(Image.open(SRC / src).convert("L"), dtype=np.float64) / 255
        D = -np.log(np.clip(a, 1 / 255, 1))
        return blob(h, w, cx, cy, rx, ry, seed, 0.25) * smooth(cover(D, radius), lo, hi)

    return f


def build(key):
    P = DIRS[key]
    out = OUT / key
    out.mkdir(parents=True, exist_ok=True)
    st, s = P["stops"], P["s"]
    jobs = {}

    # The opening's hills (the sun's glow is laid by the page above the picture, not in it).
    jobs["landscape.webp"] = paint("landscape.webp", st, s)
    # The close: pine, sea of mist, low gold sun at (0.807, 0.574).
    jobs["purpose-land.webp"] = paint(
        "purpose-land.webp",
        st,
        s,
        washes=[dict(mask=lambda h, w: blob(h, w, 0.807, 0.574, 0.20, 0.34, 2, 0.15), d=0.13, hex=P["sun"])],
    )
    jobs["purpose-cranes.webp"] = paint("purpose-cranes.webp", st, s * 0.5)

    # Still lifes: an overall tint plus a thin wash inside a few objects (hand-tinted, like an
    # old naturalist's print).
    m = "story-morning-v2.webp"
    jobs[m] = paint(
        m,
        P["still"],
        s * 0.7,
        washes=[
            dict(mask=obj(0.42, 0.755, 0.06, 0.03, 5, src=m), d=0.20, hex=P["fruit"]),
            dict(mask=obj(0.60, 0.675, 0.06, 0.03, 6, src=m), d=0.14, hex=P["tea"]),
        ],
        spots=[
            dict(mask=lambda h, w: np.clip(blob(h, w, 0.70, 0.34, 0.26, 0.16, 4, 0) * 3, 0, 1), hex=P["blossom"], s=2.4, amount=1.0, light_only=(0.3, 0.75), min_d=(0.05, 0.12)),
        ],
    )
    r = "story-reading-v2.webp"
    jobs[r] = paint(
        r,
        P["still"],
        s * 0.7,
        washes=[
            dict(mask=obj(0.88, 0.43, 0.12, 0.09, 7, src=r, radius=14), d=0.16, hex=P["leaf"]),
            dict(mask=obj(0.74, 0.545, 0.045, 0.02, 8, src=r), d=0.22, hex=P["tea"]),
        ],
    )
    o = "story-source-v2.webp"
    jobs[o] = paint(
        o,
        P["still"],
        s * 0.7,
        washes=[
            dict(mask=obj(0.38, 0.69, 0.08, 0.07, 10, src=o), d=0.22, hex=P["fruit"]),
            dict(mask=obj(0.79, 0.815, 0.06, 0.025, 11, src=o), d=0.14, hex=P["tea"]),
        ],
        spots=[dict(mask=lambda h, w: blob(h, w, 0.62, 0.50, 0.30, 0.22, 9, 0), hex=P["leaf"], s=1.3, amount=0.9, min_d=(0.05, 0.12))],
    )

    # The cell: its own cooler (or warmer) ink, so the gold leaf stands out more.
    for n in ["mito.webp", "mito-closeup.webp", "mito-aged.webp", "mito-radicals.webp"]:
        jobs[n] = paint(n, P["mito"], s * 0.75)
    jobs["halo.webp"] = paint("halo.webp", st, s * 0.9)
    jobs["pool.webp"] = paint("pool.webp", st, s * 0.5)
    jobs["pool-foot.webp"] = paint("pool-foot.webp", st, s * 0.3)

    # The cranes: only the crown turns red (a real crane's crown is red); the body stays white.
    jobs["crane-painted.webp"] = crane_tint("crane-painted.webp", P, (0.735, 0.483, 0.035, 0.03))
    jobs["crane-rest-v2.webp"] = crane_tint("crane-rest-v2.webp", P, (0.266, 0.089, 0.06, 0.03))

    for n, img in jobs.items():
        img.save(out / n, "WEBP", quality=92, method=4)
    print(key, len(jobs), "pictures ->", out)


def crane_tint(name, P, box):
    im = Image.open(SRC / name)
    alpha = np.asarray(im.split()[3]) if im.mode == "RGBA" else None
    a = np.asarray(im.convert("RGB"), dtype=np.float64) / 255
    h, w = a.shape[:2]
    sat = a.max(axis=2) - a.min(axis=2)
    warm = (a[..., 0] > a[..., 2] + 0.03).astype(np.float64)
    m = (smooth(sat, 0.04, 0.12) * warm * blob(h, w, *box, rough=0))[..., None]
    lum = a.mean(axis=2, keepdims=True)
    c = rgb(P["crown"])
    red = np.clip(c * (lum / c.mean()) ** 0.8, 0, 1)
    out = a * (1 - m) + red * m
    img = Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8), "RGB")
    if alpha is not None:
        img.putalpha(Image.fromarray(alpha))
    return img


if __name__ == "__main__":
    build("spring")

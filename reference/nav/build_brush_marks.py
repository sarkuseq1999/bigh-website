"""Menu bar option A ("Brush", October 5, 2026): the small painted marks, made from the real sumi
strokes in public/images/home-v2/nav/brush-1..7.webp (reference/nav/originals), never drawn
from scratch, so every mark keeps a real brush's texture.

  calm-1..7.webp  each stroke with most of its wave taken out (each column moved toward the
                  stroke's mean line; 22% of the wave stays): the hover underlines.
  ring.webp       Sign up's outline: calm-1 laid once round a pill, loaded where it starts (the
                  upper left), dry where it closes, its tail passing just inside the start, the
                  loop a touch uneven; drawn at 3x, used as a 9-slice border image.
  tick.webp       Products and Science's "opens" mark: calm-7 drawn as one small v, loaded at
                  its left arm, thinning up the right.
  deckle.webp     the scrolled bar's lower edge: the paper's fibre feathering out over a few
                  pixels (an alpha mask, tiling across).

Run from the repo root:  python -X utf8 reference/nav/build_brush_marks.py
"""

from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, map_coordinates

SRC = Path("public/images/home-v2/nav")
OUT = SRC / "brush"
INK = (12, 11, 10)
OUT.mkdir(parents=True, exist_ok=True)


def calm(keep=0.22):
    for n in range(1, 8):
        a = np.asarray(Image.open(SRC / f"brush-{n}.webp").convert("RGBA")).astype(np.float32)
        alpha = a[..., 3] / 255.0
        h, w = alpha.shape
        mass = alpha.sum(0)
        cent = np.where(mass > 0.5, (alpha * np.arange(h)[:, None]).sum(0) / np.maximum(mass, 1e-6), np.nan)
        idx = np.arange(w)
        good = ~np.isnan(cent)
        cent = np.interp(idx, idx[good], cent[good])
        smooth = gaussian_filter(cent, 13.5, mode="nearest")
        target = (smooth * mass).sum() / mass.sum()
        shift = (target - smooth) * (1 - keep)
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        out = np.stack([map_coordinates(a[..., c], [yy - shift[None, :], xx], order=1) for c in range(4)], -1)
        img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGBA")
        box = img.split()[-1].point(lambda v: 255 if v > 6 else 0).getbbox()
        img = img.crop((max(0, box[0] - 2), max(0, box[1] - 2), min(w, box[2] + 2), min(h, box[3] + 2)))
        img.save(OUT / f"calm-{n}.webp", "WEBP", quality=90, method=6)


def stroke_alpha(n):
    a = np.asarray(Image.open(OUT / f"calm-{n}.webp").convert("RGBA")).astype(np.float32)[..., 3] / 255.0
    return a


def lay(src, path, size, thick, u_of_s, offset_of_s=None, thick_of_s=None, ss=4):
    """Lay a stroke (alpha, loaded at the left) along a polyline (target pixels). `thick` is the
    stroke image's full height in target pixels; `u_of_s` maps 0..1 along the path to 0..1 along
    the stroke; `offset_of_s` moves it along the path's normal (target pixels)."""
    W, H = size
    canvas = np.zeros((H * ss, W * ss), np.float32)
    p = np.asarray(path, np.float64) * ss
    seg = np.diff(p, axis=0)
    seglen = np.hypot(seg[:, 0], seg[:, 1])
    cum = np.concatenate([[0], np.cumsum(seglen)])
    L = cum[-1]
    steps = int(L / 0.35) + 1
    s = np.linspace(0, L, steps)
    x = np.interp(s, cum, p[:, 0])
    y = np.interp(s, cum, p[:, 1])
    tx = np.gradient(x)
    ty = np.gradient(y)
    tn = np.hypot(tx, ty) + 1e-9
    tx, ty = tx / tn, ty / tn
    nx, ny = -ty, tx  # the normal to the right of travel
    sn = s / L
    if offset_of_s is not None:
        off = offset_of_s(sn) * ss
        x, y = x + nx * off, y + ny * off
    sh, sw = src.shape
    M = int(thick * ss * 2.2) + 2
    v = np.linspace(0, sh - 1, M)
    U = (u_of_s(sn) * (sw - 1))[:, None] * np.ones((1, M))
    V = np.ones((steps, 1)) * v[None, :]
    val = map_coordinates(src, [V.ravel(), U.ravel()], order=1).reshape(steps, M)
    d = (v - (sh - 1) / 2) / (sh - 1) * thick * ss
    d = d[None, :] * (thick_of_s(sn)[:, None] if thick_of_s is not None else 1)
    X = x[:, None] + nx[:, None] * d
    Y = y[:, None] + ny[:, None] * d
    xi = np.clip(np.rint(X).astype(int), 0, W * ss - 1)
    yi = np.clip(np.rint(Y).astype(int), 0, H * ss - 1)
    np.maximum.at(canvas, (yi.ravel(), xi.ravel()), val.ravel())
    canvas = gaussian_filter(canvas, 0.6)
    return canvas.reshape(H, ss, W, ss).mean((1, 3))


def save_ink(alpha, name):
    h, w = alpha.shape
    rgba = np.zeros((h, w, 4), np.uint8)
    rgba[..., :3] = INK
    rgba[..., 3] = np.clip(alpha * 255, 0, 255).astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(OUT / name, "WEBP", quality=92, method=6, lossless=False)


def piece(points):
    pts = np.asarray(points, np.float64)

    def f(t):
        return np.interp(t, pts[:, 0], pts[:, 1])

    return f


def ring(scale=3, w=136, h=48, pad=4):
    """One loop round a pill w x h (CSS px), drawn at `scale`."""
    W, H = (w + 2 * pad) * scale, (h + 2 * pad) * scale
    inset = 1.6
    x0, x1 = (pad + inset) * scale, (pad + w - inset) * scale
    y0, y1 = (pad + inset) * scale, (pad + h - inset) * scale
    r = (y1 - y0) / 2
    yc = (y0 + y1) / 2
    cl, cr = x0 + r, x1 - r
    pts = []
    # clockwise on screen from the left cap's upper part: up round the left cap, the top edge,
    # the right cap, the bottom edge, the left cap's lower part, and on past the start.
    for a in np.linspace(np.pi * 1.18, np.pi * 1.5, 40):
        pts.append((cl + r * np.cos(a), yc + r * np.sin(a)))
    for xx in np.linspace(cl, cr, 120)[1:]:
        pts.append((xx, y0))
    for a in np.linspace(np.pi * 1.5, np.pi * 2.5, 120)[1:]:
        pts.append((cr + r * np.cos(a), yc + r * np.sin(a)))
    for xx in np.linspace(cr, cl, 120)[1:]:
        pts.append((xx, y1))
    for a in np.linspace(np.pi * 0.5, np.pi * 1.36, 100)[1:]:
        pts.append((cl + r * np.cos(a), yc + r * np.sin(a)))
    # a touch of tilt, so the loop is drawn, not constructed
    c = np.array([W / 2, H / 2])
    th = np.deg2rad(-0.8)
    rot = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    pts = (np.asarray(pts) - c) @ rot.T + c
    src = stroke_alpha(1)
    # the head at its own size, the body drawn out round the pill, the dry tail given room
    u = piece([(0, 0), (0.05, 0.12), (0.7, 0.62), (0.9, 0.84), (1, 0.97)])

    def offset(t):
        # breathing a little in and out (the hand), and the tail closing just inside the start
        wob = 0.3 * np.sin(2 * np.pi * t + 0.6) + 0.16 * np.sin(4 * np.pi * t + 2.1)
        close = 1.25 * np.clip((t - 0.88) / 0.12, 0, 1) ** 1.5
        return (wob + close) * scale

    def swell(t):
        # loaded where it starts, pressing a little on the far cap, thinning as the ink runs out
        return np.interp(t, [0, 0.06, 0.3, 0.52, 0.62, 0.8, 1], [1.08, 1.06, 0.98, 1.02, 0.96, 0.88, 0.8])

    a = lay(src, pts, (W, H), thick=4.0 * scale, u_of_s=u, offset_of_s=offset, thick_of_s=swell)
    save_ink(a, "ring.webp")
    return W, H, (h / 2 + pad) * scale


def tick(scale=4, w=11, h=6.5, pad=2.5):
    W, H = int(round((w + 2 * pad) * scale)), int(round((h + 2 * pad) * scale))
    ax, ay = pad * scale, pad * scale
    bx, by = (pad + w / 2) * scale, (pad + h) * scale
    cx, cy = (pad + w) * scale, (pad + 0.2) * scale
    pts = []
    for t in np.linspace(0, 1, 60):
        pts.append((ax + (bx - ax) * t, ay + (by - ay) * t))
    # a small rounded turn at the bottom
    for t in np.linspace(0, 1, 30)[1:]:
        pts.append((bx + (cx - bx) * t, by + (cy - by) * t))
    pts = np.asarray(pts)
    pts = gaussian_filter(pts, (3, 0), mode="nearest")
    src = stroke_alpha(7)
    u = piece([(0, 0), (0.18, 0.12), (0.72, 0.62), (1, 0.93)])
    a = lay(src, pts, (W, H), thick=2.9 * scale, u_of_s=u)
    save_ink(a, "tick.webp")
    return W, H


def deckle(w=800, h=10, scale=2, seed=7):
    """The bar's lower edge: paper (alpha 1) down to a ragged line that wanders a pixel or two,
    then a few loose fibres, then nothing. Tiles across (all its noise is periodic in x)."""
    rng = np.random.default_rng(seed)
    W, H = w * scale, h * scale
    x = np.arange(W)
    edge = np.full(W, 3.2 * scale)
    for k, amp in ((3, 0.45), (7, 0.35), (19, 0.3), (41, 0.22), (97, 0.16), (211, 0.1)):
        edge += amp * scale * np.sin(2 * np.pi * k * x / W + rng.uniform(0, 2 * np.pi))
    y = np.arange(H)[:, None]
    alpha = np.clip(1 - (y - edge[None, :]) / (1.6 * scale), 0, 1) ** 1.3
    fib = np.zeros((H, W), np.float32)
    for _ in range(int(w * 0.55)):
        cx = rng.uniform(0, W)
        L = rng.uniform(5, 26) * scale
        ang = rng.normal(0, 0.12)
        cy = edge[int(cx) % W] + rng.uniform(0.2, 4.5) * scale
        strength = rng.uniform(0.18, 0.55) * np.exp(-(cy - edge[int(cx) % W]) / (3.2 * scale))
        for t in np.linspace(-0.5, 0.5, int(L)):
            px = int(cx + t * L) % W
            py = int(round(cy + t * L * ang))
            if 0 <= py < H:
                fib[py, px] = max(fib[py, px], strength * (1 - abs(t) * 1.4))
    fib = gaussian_filter(fib, (0.5, 0.8), mode=("nearest", "wrap"))
    a = np.maximum(alpha, fib)
    rgba = np.zeros((H, W, 4), np.uint8)
    rgba[..., 3] = np.clip(a * 255, 0, 255).astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(OUT / "deckle.webp", "WEBP", lossless=True)

    # The paper's own edge as a line: a soft, slightly uneven band along the same ragged edge,
    # darker where the edge turns (the page shows it in ink at low strength, so the bar reads as
    # a sheet of paper lying over the page).
    d = y - edge[None, :]
    strength = 0.8 + 0.2 * np.sin(2 * np.pi * 13 * x / W + 1.3)[None, :]
    line = np.exp(-0.5 * (d / (0.55 * scale)) ** 2) * strength
    rgba = np.zeros((H, W, 4), np.uint8)
    rgba[..., 3] = np.clip(line * 255, 0, 255).astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(OUT / "deckle-line.webp", "WEBP", lossless=True)


if __name__ == "__main__":
    calm()
    print("ring", ring())
    print("tick", tick())
    deckle()
    print("deckle done")

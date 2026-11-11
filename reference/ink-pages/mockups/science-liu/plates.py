"""Plates for the Science page's Dr. Liu mockups (Mo, November 11, 2026; see shoot.py).

  python -X utf8 reference/ink-pages/mockups/science-liu/plates.py [b] [c]

b  "Office hours": a Codex painting of a professor's desk and blackboard with an empty place
   (reference/ink-pages/science/originals/liu-office-3.png: take 2 with its chalk drawing redrawn),
   his shipped portrait set behind the desk, the desk's own front laid back over him so his hands
   rest on its top.
c  "The gold he studies": a Codex painting of one huge cell (originals/liu-cell-1.png), his
   portrait in front of it.

His portrait is public/images/products/nuricell/ink/liu-v1.webp: his real face, never generated.
The paintings were painted with no person in them, so no model ever drew him. Each plate is the
painting with its paper divided out (white multiplies away on the page), saved for a wide window
and for a phone into reference/ink-pages/science/plates/liu/ (git-ignored).
"""

import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SCIENCE = HERE.parent.parent / "science"
ORIG = SCIENCE / "originals"
PLATES = SCIENCE / "plates" / "liu"
PLATES.mkdir(parents=True, exist_ok=True)
PORTRAIT = REPO / "public/images/products/nuricell/ink/liu-v1.webp"

# Each plate: the canvas (w, h); the pieces of the painting laid on it (a box of the painting, how
# much larger or smaller it is drawn, where its corner goes, and how far its own edges dry out, in
# painting px: left, top, right, foot); the figure's width and corner; where the whole plate dries
# out into the paper (shares of the canvas: left, right, top, foot); for b, the desk's front edge
# (canvas px) from which the scene lies over him again; for c, how far up from the foot he dries out.
WHOLE = (0, 0, 1536, 1024)
RECIPES = {
    "b-desk": {
        "take": "liu-office-3",
        "canvas": (1536, 1010),
        "pieces": [{"box": WHOLE, "scale": 1.0, "at": (0, 0)}],
        "figure": {"width": 700, "x": 2, "y": 42},
        "fade": (0.0, 0.07, 0.0, 0.1),
        "front": 877,
    },
    # A phone gets him large: the blackboard hung a little smaller up on the right, so the whole
    # drawing shows beside his head, and the desk with its books and mug under his hands.
    "b-phone": {
        "take": "liu-office-3",
        "canvas": (1100, 1262),
        "pieces": [
            {"box": (560, 40, 1500, 626), "scale": 0.75, "at": (478, 30), "dry": (0, 0, 0, 12)},
            {"box": (0, 642, 1536, 1024), "scale": 1.0, "at": (-352, 890), "dry": (0, 26, 0, 0)},
        ],
        "figure": {"width": 700, "x": 6, "y": 275},
        "fade": (0.0, 0.0, 0.0, 0.085),
        "front": 1125,
    },
    "c-desk": {
        "take": "liu-cell-1",
        "canvas": (2200, 1024),
        "pieces": [{"box": WHOLE, "scale": 1.25, "at": (420, -128)}],
        "figure": {"width": 640, "x": 1130, "y": 96},
        "fade": (0.0, 0.0, 0.07, 0.12),
        "dry": 0.14,
    },
    "c-phone": {
        "take": "liu-cell-1",
        "canvas": (1100, 1180),
        "pieces": [{"box": WHOLE, "scale": 1770 / 1536, "at": (-470, 0)}],
        "figure": {"width": 700, "x": 60, "y": 150},
        "fade": (0.05, 0.0, 0.06, 0.12),
        "dry": 0.14,
    },
}


# Round 2 (Mo, November 11, 2026: two more ideas without the cell; for mockups his picture may be
# redrawn). These are Codex paintings WITH him in them, painted from his photograph, so no figure is
# set in: the painting is only laid on a wider canvas (bare paper on the left, for the words).
RECIPES.update(
    {
        # d "Still looking": he looks up from a brass microscope by a window.
        # Take 2 of two: his face is the closer one to his photograph.
        "d-desk": {
            "take": "liu-scope-2",
            "canvas": (2200, 1024),
            "pieces": [{"box": WHOLE, "scale": 1.0, "at": (664, 0)}],
            "fade": (0.0, 0.0, 0.07, 0.0),
        },
        "d-phone": {
            "take": "liu-scope-2",
            "canvas": (1000, 1024),
            "pieces": [{"box": (536, 0, 1536, 1024), "scale": 1.0, "at": (0, 0), "dry": (120, 0, 0, 0)}],
            "fade": (0.0, 0.0, 0.07, 0.0),
        },
        # e "280 papers": he sends them out as paper planes, three of them gold.
        "e-desk": {
            "take": "liu-planes-2",
            "canvas": (1900, 1024),
            "pieces": [{"box": WHOLE, "scale": 1.0, "at": (364, 0)}],
            "fade": (0.0, 0.0, 0.06, 0.0),
        },
        # A phone keeps more of the flight: the painting from 330px on, a little smaller.
        "e-phone": {
            "take": "liu-planes-2",
            "canvas": (1000, 849),
            "pieces": [{"box": (330, 0, 1536, 1024), "scale": 1000 / 1206, "at": (0, 0)}],
            "fade": (0.0, 0.0, 0.06, 0.0),
        },
    }
)


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


def divided(img):
    """Paper -> white, ink kept: the paper is the median of the brightest tenth of the picture."""
    arr = np.asarray(img.convert("RGB")).astype(np.float32)
    lum = arr.mean(axis=2)
    paper = np.median(arr[lum >= np.quantile(lum, 0.9)], axis=0)
    return np.clip(arr / paper * 255.0 * 1.02, 0, 255)


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
    face and his glasses too), so the scene never shows through him; toward his outline it follows
    the paint itself, so the bare paper between his loose brush strokes lets the scene through (a
    solid outline left white patches on the desk)."""
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


def scene_ink(r):
    """The painting's ink on the canvas, piece by piece (later pieces lie over earlier ones)."""
    cw, ch = r["canvas"]
    flat = divided(Image.open(ORIG / f"{r['take']}.png"))
    ink = np.zeros((ch, cw, 3), np.float32)
    for piece in r["pieces"]:
        x0, y0, x1, y1 = piece["box"]
        part = 255.0 - flat[y0:y1, x0:x1]
        left, top, right, foot = piece.get("dry", (0, 0, 0, 0))
        h, w = part.shape[:2]
        part *= (smooth_ramp(w, left) * smooth_ramp(w, right, True))[None, :, None]
        part *= (smooth_ramp(h, top) * smooth_ramp(h, foot, True))[:, None, None]
        s = piece["scale"]
        if s != 1.0:
            part = cv2.resize(part, (round(w * s), round(h * s)), interpolation=cv2.INTER_LANCZOS4 if s > 1 else cv2.INTER_AREA)
        ink = np.maximum(ink, placed(np.clip(part, 0, 255), (cw, ch), *piece["at"]))
    return ink


def plate(name):
    r = RECIPES[name]
    cw, ch = r["canvas"]
    ink = scene_ink(r)

    # The scene dries out into the paper where it would otherwise stop at a ruled edge.
    left, right, top, foot = r["fade"]
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
    keep = keep * keep * (3 - 2 * keep)
    ink *= keep[..., None]

    out = 255.0 - ink
    if "figure" in r:
        # Round 1 (a, b, c): his shipped portrait set into a painting that has no person in it.
        portrait = Image.open(PORTRAIT).convert("RGB")
        cover_full = figure_cover(np.asarray(portrait))
        f = r["figure"]
        fh = round(portrait.height * f["width"] / portrait.width)
        him = 255.0 - np.asarray(portrait.resize((f["width"], fh), Image.LANCZOS)).astype(np.float32)
        where = cv2.resize(cover_full, (f["width"], fh), interpolation=cv2.INTER_AREA)
        him = placed(him, (cw, ch), f["x"], f["y"])
        where = placed(where, (cw, ch), f["x"], f["y"])
        if r.get("dry"):
            dry = smooth_ramp(ch, int(r["dry"] * ch), True)[:, None]
            him, where = him * dry[..., None], where * dry
        out = (255.0 - ink * (1 - where)[..., None]) * (255.0 - him) / 255.0
    if r.get("front"):
        # The desk's front, from its top's front edge down, lies over him again: a firm edge, a
        # couple of pixels soft.
        over = np.clip((np.arange(ch, dtype=np.float32)[:, None] - r["front"]) / 3.0, 0, 1) * np.ones((1, cw), np.float32)
        out = out * (1 - over[..., None]) + (255.0 - ink) * over[..., None]
    done = Image.fromarray(np.clip(np.rint(out), 0, 255).astype(np.uint8))
    done.save(PLATES / f"{name}.webp", "WEBP", quality=90, method=6)
    done.save(PLATES / f"{name}.png")
    print(name, (cw, ch))


want = sys.argv[1:] or ["b", "c"]
for name in RECIPES:
    if name[0] in want or name in want:
        plate(name)

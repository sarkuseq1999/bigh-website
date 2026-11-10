"""Round 6 (November 10, 2026): get the Codex paintings ready to lie on the page as art/*.png.

usage: python -X utf8 prep6.py sky <take> | stroke <take> | shade <name> | gold | fog
  sky    originals/opening-clearday<take>.png [end fade cut0 cut1] -> art/sky.png (paper divided out,
         rows of sea cut0..cut1 taken out, foot faded to white); <take> is "-bh", "2-ch", ...
  stroke originals/opening-bluestroke-<take>.png -> art/stroke.png (paper divided out, cropped to the stroke)
  shade  originals/opening-<name>.png [out]      -> art/<out or shade>.png (a soft shadow to multiply over the page)
  gold   the site's gold leaf                    -> art/gold-strip.png, art/flake-<n>.png (torn pieces)
  fog    art/sky.png                             -> art/sky-fog.png (the same morning before the fog lifts)
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = Path(__file__).parent
ART = HERE / "art"
ART.mkdir(exist_ok=True)
ORIG = HERE.parents[1] / "nuricell" / "originals"
PUBLIC = HERE.parents[3] / "public" / "images"


def load(name):
    return np.asarray(Image.open(ORIG / f"{name}.png").convert("RGB")).astype(np.float32)


def divide(a, paper_rows):
    """The sheet's own white divided out, so the painting multiplies onto the page's paper."""
    paper = np.median(a[paper_rows].reshape(-1, 3), axis=0)
    d = np.clip(a / paper * 255.0, 0, 255)
    return np.where(d.min(axis=2, keepdims=True) > 249, 255.0, d)


def save(d, name):
    Image.fromarray(np.clip(d, 0, 255).astype(np.uint8)).save(ART / f"{name}.png")
    print(name, d.shape[1], "x", d.shape[0])


def sky(take, end=0.8, fade=0.035, cut0=0, cut1=0):
    """`cut0`..`cut1`: rows of open sea taken out (cross-faded), so the bluff sits closer under the
    horizon: the name rests on the horizon and the bottle still stands on the grass."""
    a = load(f"opening-clearday{take}")
    end, fade, cut0, cut1 = float(end), float(fade), int(cut0), int(cut1)
    h = a.shape[0]
    if cut1 > cut0:
        n = 12
        t = (np.arange(n) / (n - 1))[:, None, None]
        seam = a[cut0 - n : cut0] * (1 - t) + a[cut1 - n : cut1] * t
        a = np.concatenate([a[: cut0 - n], seam, a[cut1:], np.repeat(a[-1:], cut1 - cut0, axis=0)])
    d = divide(a, slice(int(h * 0.93), h))
    # Where things are, for the mock: the horizon (the sharpest step down the middle columns) and
    # the bluff's top in the middle (where the sea's blue ends).
    mid = d[:, int(d.shape[1] * 0.45) : int(d.shape[1] * 0.55)].mean(axis=1)
    step = np.abs(np.diff(mid.mean(axis=1)))
    horizon = int(np.argmax(step[int(h * 0.5) : int(h * 0.7)]) + h * 0.5)
    blue = mid[:, 2] - mid[:, 0]
    below = np.where(blue[horizon + 5 :] < 25)[0]
    print("horizon row", horizon, round(horizon / h, 4), "bluff top", horizon + 5 + int(below[0]), round((horizon + 5 + int(below[0])) / h, 4))
    # Under the bluff the painting is over: the last specks fade into bare paper.
    y = np.arange(h) / h
    k = np.clip((y - (end - fade)) / fade, 0, 1)[:, None, None]
    save(d * (1 - k) + 255 * k, "sky")


def stroke(take):
    a = load(f"opening-bluestroke-{take}")
    h = a.shape[0]
    d = divide(a, slice(0, int(h * 0.2)))
    d = d[int(h * 0.25) : int(h * 0.76)]
    # Stray specks above and below the stroke would read as dirt on the page.
    c = d.shape[0]
    d[: int(c * 0.105)] = 255
    d[int(c * 0.885) :] = 255
    save(d, "stroke")


def shade(name, out="shade", cool=(1.0, 0.965, 0.9), gain=1.0):
    a = load(f"opening-{name}").mean(axis=2)
    paper = np.percentile(a, 97)
    s = np.clip(1 - a / paper, 0, 1) * gain  # 0 = sunlight, 1 = deepest shade
    s = np.where(s < 0.012, 0, s)
    d = np.stack([255 * (1 - s * c) for c in cool], axis=2)
    save(d, out)


def torn(w, h, seed, rough=0.22):
    """A torn piece of leaf: a rectangle whose edges wander, as an alpha mask."""
    rng = np.random.default_rng(seed)
    big = 3
    W, H = w * big, h * big

    def noise(cell, blur):
        n = Image.fromarray((rng.random((H // cell + 2, W // cell + 2)) * 255).astype(np.uint8))
        return np.asarray(n.resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(blur))).astype(np.float32) / 255 - 0.5

    y = (np.arange(H) / H)[:, None]
    x = (np.arange(W) / W)[None, :]
    # Leaf laid along a line: full in the middle of its height, tapering at both ends; its edge
    # wanders slowly, with a few small nicks and a gap or two where the leaf did not take.
    band = 1 - np.abs(y - 0.5) / 0.5
    ends = np.clip(np.minimum(x, 1 - x) / 0.07, 0, 1) ** 0.6
    field = band * (0.55 + 0.45 * ends) + rough * (1.5 * noise(46 * big, 14 * big) + 0.8 * noise(9 * big, 2.5 * big) + 0.35 * noise(3 * big, 0.8 * big))
    a = (field > 0.42).astype(np.uint8) * 255
    return Image.fromarray(a).resize((w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.4))


def gold():
    leaf = Image.open(PUBLIC / "home-v2" / "ink" / "gold-leaf-word.webp").convert("RGB")
    # A long strip: the leaf laid twice side by side (the second sheet turned over, so no seam repeats).
    two = Image.new("RGB", (leaf.width * 2, leaf.height))
    two.paste(leaf, (0, 0))
    two.paste(leaf.transpose(Image.FLIP_LEFT_RIGHT), (leaf.width, 0))
    for name, (w, h), seed, y in [("gold-strip", (620, 44), 3, 40), ("flake-1", (64, 44), 5, 120), ("flake-2", (42, 30), 8, 200), ("flake-3", (30, 22), 11, 260)]:
        piece = two.crop((10, y, 10 + w, y + h)).convert("RGBA")
        piece.putalpha(torn(w, h, seed, 0.5 if name == "gold-strip" else 0.6))
        piece.save(ART / f"{name}.png")
        print(name, piece.size)


def fog():
    """The same morning with the marine layer still in: a soft white bank over the sea and the lower
    sky, thinner higher up. A sketch of the page's first second, not a painting."""
    d = np.asarray(Image.open(ART / "sky.png").convert("RGB")).astype(np.float32)
    h, w = d.shape[:2]
    rng = np.random.default_rng(4)
    # Soft clouds: blurred noise at two sizes.
    def cloud(size, blur):
        n = Image.fromarray((rng.random((h // size + 2, w // size + 2)) * 255).astype(np.uint8))
        return np.asarray(n.resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(blur))).astype(np.float32) / 255
    c = 0.6 * cloud(120, 40) + 0.4 * cloud(40, 14)
    y = (np.arange(h) / h)[:, None]
    # Thickest over the sea (60-70% down), thinning up into the sky and gone under the bluff's top.
    bank = np.clip(1.25 - np.abs(y - 0.6) / 0.42, 0, 1) * np.clip((0.78 - y) / 0.06, 0, 1)
    k = np.clip(bank * (0.55 + 0.9 * c), 0, 0.97)[:, :, None]
    fogged = d * (1 - k) + np.array([250.0, 251.0, 252.0]) * k
    save(fogged, "sky-fog")


if __name__ == "__main__":
    cmd, *rest = sys.argv[1:]
    {"sky": sky, "stroke": stroke, "shade": shade, "gold": gold, "fog": fog}[cmd](*rest)

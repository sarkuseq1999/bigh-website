"""Build the homepage science section's paintings (October 19, 2026) from the Codex originals.

Each painting ships as an ink plate: the paper is divided out (paper -> white, ink kept), so the
page lays it on with mix-blend-mode: multiply and its own rice paper shows through. Paint that runs
off an original's edge dissolves into the paper over the outer 8% (no hard straight cut on the
page). Each is cropped to its painted part with a margin and set in the section's stage box
(1600 x 1195, the stage's 2000:1493). The three Joshua trees share one crop, so they still line up
for the age slider. The hummingbird also gets a gold mask (where its wings are gold leaf), through
which the page passes its band of light.

Output: public/images/home-v2/ink/science/<name>-v1.webp (+ hummingbird-v1-gold.webp).

usage: python -X utf8 reference/ink-pages/home-science/build_home_science.py
"""

from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
ORIG = HERE / "originals"
OUT = REPO / "public/images/home-v2/ink/science"
W, H = 1600, 1195

# shipped name -> original(s); a group shares one crop box
GROUPS = [
    {"hummingbird-v1": "hummingbird-a1"},
    {"apple-lemon-v1": "apple-lemon-a5"},
    {"joshua-young-v1": "joshua-young-a1", "joshua-middle-v1": "joshua-middle-a1", "joshua-old-v1": "joshua-old-a1"},
]
# where the gold leaf is (in the 1600 x 1195 plate): only the wings, so no warm wash elsewhere
# catches the light; this gold is paler than the homepage's other leaf, hence the lower saturation
# paintings that stand on the ground: set at the foot of the box, so the apple and the Joshua tree
# share one ground line (and no wide band of paper is left under the apple)
GROUNDED = {"apple-lemon-v1"}
GOLD = {"hummingbird-v1": ((1040, 110, 1600, 590), 0.2)}


def plate(name):
    """The original with its paper divided out and its edges dissolved, as floats 0..255."""
    im = np.asarray(Image.open(ORIG / f"{name}.png").convert("RGB")).astype(np.float32)
    h, w, _ = im.shape
    b = max(8, min(h, w) // 40)
    border = np.concatenate(
        [im[:b].reshape(-1, 3), im[-b:].reshape(-1, 3), im[:, :b].reshape(-1, 3), im[:, -b:].reshape(-1, 3)]
    )
    flat = np.clip(im / np.median(border, axis=0) * 255.0, 0, 255)
    f = 0.08
    yy = np.linspace(0, 1, h)[:, None]
    xx = np.linspace(0, 1, w)[None, :]
    d = np.minimum(np.minimum(yy, 1 - yy) / f, np.minimum(xx, 1 - xx) / (f * h / w))
    a = np.clip(d, 0, 1)
    a = (a * a * (3 - 2 * a))[..., None]
    return 255 - (255 - flat) * a


def painted_box(flat):
    """The painted part: rows and columns with real ink in them (not the paper's grain)."""
    ink = flat.min(axis=2) < 205
    h, w = ink.shape
    rows = np.where(ink.sum(axis=1) > w * 0.004)[0]
    cols = np.where(ink.sum(axis=0) > h * 0.004)[0]
    return cols[0], rows[0], cols[-1], rows[-1]


def gold_mask(img, region, sat_from, width=1000):
    """Where the painting is gold leaf (warm hue, clearly saturated), as an alpha mask: as
    reference/home-v2/ink/build_assets.py does for the homepage's other gold."""
    k = width / img.width
    img = img.resize((width, round(img.height * k)), Image.LANCZOS)
    arr = np.asarray(img).astype(np.float32) / 255
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    hi, lo = arr.max(axis=2), arr.min(axis=2)
    sat = (hi - lo) / np.maximum(hi, 1e-4)
    warm = (r >= g) & (g > b)
    hue = np.where(warm, 60 * (g - b) / np.maximum(hi - lo, 1e-4), 0)
    in_hue = np.clip((hue - 24) / 8, 0, 1) * np.clip((58 - hue) / 6, 0, 1)
    alpha = np.clip((sat - sat_from) / 0.22, 0, 1) * in_hue * np.clip((hi - 0.3) / 0.2, 0, 1)
    x0, y0, x1, y1 = (round(v * k) for v in region)
    keep = np.zeros_like(alpha)
    keep[y0:y1, x0:x1] = 1
    alpha = alpha * keep
    mask = Image.fromarray((alpha * 255).astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(1.2))
    white = Image.new("L", mask.size, 255)
    return Image.merge("RGBA", (white, white, white, mask)), float((np.asarray(mask) > 128).mean())


OUT.mkdir(parents=True, exist_ok=True)
for group in GROUPS:
    plates = {out: plate(src) for out, src in group.items()}
    boxes = [painted_box(p) for p in plates.values()]
    x0, y0 = min(b[0] for b in boxes), min(b[1] for b in boxes)
    x1, y1 = max(b[2] for b in boxes), max(b[3] for b in boxes)
    for out, flat in plates.items():
        h, w, _ = flat.shape
        m = round(0.05 * max(x1 - x0, y1 - y0))
        box = (max(0, x0 - m), max(0, y0 - m), min(w, x1 + m), min(h, y1 + m))
        img = Image.fromarray(flat.astype(np.uint8)).crop(box)
        scale = min(W / img.width, H / img.height)
        img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
        canvas = Image.new("RGB", (W, H), (255, 255, 255))
        top = H - img.height - round(0.03 * H) if out in GROUNDED else (H - img.height) // 2
        canvas.paste(img, ((W - img.width) // 2, top))
        path = OUT / f"{out}.webp"
        canvas.save(path, "WEBP", quality=86, method=6)
        print(f"{path.relative_to(REPO)}  crop {box}  {path.stat().st_size // 1024} KB")
        if out in GOLD:
            mask, cover = gold_mask(canvas, *GOLD[out])
            gpath = OUT / f"{out}-gold.webp"
            mask.save(gpath, "WEBP", quality=80, method=6)
            print(f"{gpath.relative_to(REPO)}  gold {cover:.1%}  {gpath.stat().st_size // 1024} KB")

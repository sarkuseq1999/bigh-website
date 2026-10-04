"""Build the Ink look's shipping pictures from the GPT Image 2.5 originals (round 4, October 2026).

Every painting was generated on warm rice paper. Three treatments, all local and reproducible:
  ink    the paper is divided out (paper -> white, ink stays), so the page places the painting
         with mix-blend-mode: multiply and the page's own rice paper shows through, as real ink on
         paper does. No seams, no rectangles.
  cut    a true cutout for a figure that must stay opaque over other ink (the crane): BiRefNet
         (rembg, local) alpha, colours kept.
  leaf   gold leaf on paper: alpha from each pixel's distance to the paper colour, colours
         un-premultiplied, so the torn leaf edge survives.
Output: webp in public/images/home-v2/ink/ (<= 2400 px). Run embed-prompt on each afterwards.

usage: python -X utf8 reference/home-v2/ink/build_assets.py [name ...]
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
ORIG = HERE / "originals"
OUT = REPO / "public/images/home-v2/ink"
PLATES = HERE / "plates"


def load(name):
    return Image.open(ORIG / f"gpt25-{name}.png").convert("RGB")


def paper_colour(arr, box):
    x0, y0, x1, y1 = box
    patch = arr[y0:y1, x0:x1].reshape(-1, 3)
    return np.median(patch, axis=0)


def ink(img, box, gain=1.0):
    """Divide the paper out: paper -> white, ink kept (for multiply on the page's paper)."""
    arr = np.asarray(img).astype(np.float32)
    paper = paper_colour(arr, box)
    out = np.clip(arr / paper * 255.0 * gain, 0, 255).astype(np.uint8)
    return Image.fromarray(out)


def leaf(img, lo=15.0, hi=40.0):
    arr = np.asarray(img).astype(np.float32)
    h, w, _ = arr.shape
    paper = paper_colour(arr, (0, 0, w, h // 12))
    dist = np.sqrt(((arr - paper) ** 2).sum(axis=2))
    alpha = np.clip((dist - lo) / (hi - lo), 0, 1)
    a = np.maximum(alpha, 1e-3)[..., None]
    colour = np.clip((arr - (1 - a) * paper) / a, 0, 255)
    rgba = np.dstack([colour, alpha * 255]).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")


def cut(img):
    from rembg import new_session, remove

    return remove(img, session=new_session("birefnet-general"))


def seamless(img):
    """Cross-fade the tile with itself shifted by half, so it repeats without a seam."""
    arr = np.asarray(img).astype(np.float32)
    h, w, _ = arr.shape
    shifted = np.roll(np.roll(arr, h // 2, axis=0), w // 2, axis=1)
    yy = np.abs(np.linspace(-1, 1, h))[:, None]
    xx = np.abs(np.linspace(-1, 1, w))[None, :]
    edge = np.clip(np.maximum(yy, xx) * 1.6 - 0.6, 0, 1)[..., None]  # 1 near the edges
    out = arr * (1 - edge) + shifted * edge
    return Image.fromarray(out.astype(np.uint8))


def tone(img, target=(248, 243, 234)):
    """Shift the paper tile so its median matches the comp's paper."""
    arr = np.asarray(img).astype(np.float32)
    med = np.median(arr.reshape(-1, 3), axis=0)
    return Image.fromarray(np.clip(arr * (np.array(target) / med), 0, 255).astype(np.uint8))


def vignette(img, seed=9):
    """Fade a painting's frame edges into white (paper, once multiplied) with a soft, irregular
    elliptical edge, so no hard rectangle or cut stroke shows."""
    arr = np.asarray(img).astype(np.float32)
    h, w, _ = arr.shape
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    nx, ny = (xx / w - 0.5) * 2, (yy / h - 0.5) * 2
    radius = np.sqrt((nx / 1.02) ** 2 + (ny / 0.98) ** 2)
    angle = np.arctan2(ny, nx)
    wobble = sum(np.sin(angle * (3 + 2 * k) + rng.uniform(0, 6.28)) / (k + 2) for k in range(5))
    keep = np.clip((1.0 + 0.05 * wobble - radius) / 0.34, 0, 1) ** 1.4
    out = arr * keep[..., None] + 255 * (1 - keep[..., None])
    return Image.fromarray(out.astype(np.uint8))


def register(img, box, target):
    """Scale and move a painting so its ink box lands on `target` in a same-size frame."""
    x0, y0, x1, y1 = box
    t0, u0, t1, u1 = target
    sx, sy = (t1 - t0) / (x1 - x0), (u1 - u0) / (y1 - y0)
    scaled = img.resize((round(img.width * sx), round(img.height * sy)), Image.LANCZOS)
    arr = np.asarray(img).astype(np.float32)
    paper = tuple(int(v) for v in paper_colour(arr, (0, 0, 500, 120)))
    frame = Image.new("RGB", img.size, paper)
    frame.paste(scaled, (round(t0 - x0 * sx), round(u0 - y0 * sy)))
    return frame


def bloom_mask(size=512, seed=4):
    """An ink blot's soft, irregular edge, as an alpha mask: paintings bloom through it."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32) / size - 0.5
    radius = np.sqrt(xx**2 + yy**2)
    angle = np.arctan2(yy, xx)
    wobble = np.zeros_like(radius)
    for octave in range(1, 7):
        phase = rng.uniform(0, 2 * np.pi)
        wobble += np.sin(angle * (octave * 3 + rng.integers(0, 3)) + phase) / (octave * 2.2)
    edge = 0.36 + 0.035 * wobble
    alpha = np.clip((edge - radius) / 0.07 + 0.5, 0, 1)
    img = Image.fromarray((alpha * 255).astype(np.uint8), "L")
    rgba = Image.merge("RGBA", (img, img, img, img))
    OUT.mkdir(parents=True, exist_ok=True)
    rgba.save(OUT / "bloom-mask.png", optimize=True)
    print("bloom-mask.png", (OUT / "bloom-mask.png").stat().st_size // 1024, "KB")


def gold_mask(name, width=1000, sat_from=0.38, bright_from=0.3):
    """Where a shipped painting is gold leaf, as an alpha mask (<name>-gold.webp): the page lays
    a moving band of light over the painting through it, so only the leaf catches the light.
    Gold = warm hue, clearly saturated; the soft glow around it stays out."""
    from PIL import ImageFilter

    img = Image.open(PLATES / f"{name}.png").convert("RGB")
    img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    arr = np.asarray(img).astype(np.float32) / 255
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    hi, lo = arr.max(axis=2), arr.min(axis=2)
    sat = (hi - lo) / np.maximum(hi, 1e-4)
    warm = (r >= g) & (g > b)
    hue = np.where(warm, 60 * (g - b) / np.maximum(hi - lo, 1e-4), 0)  # 0..60 degrees
    in_hue = np.clip((hue - 24) / 8, 0, 1) * np.clip((58 - hue) / 6, 0, 1)
    alpha = np.clip((sat - sat_from) / 0.22, 0, 1) * in_hue * np.clip((hi - bright_from) / 0.2, 0, 1)
    mask = Image.fromarray((alpha * 255).astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(1.2))
    white = Image.new("L", mask.size, 255)
    rgba = Image.merge("RGBA", (white, white, white, mask))
    path = OUT / f"{name}-gold.webp"
    rgba.save(path, "WEBP", quality=80, method=6)
    cover = float((np.asarray(mask) > 128).mean())
    print(f"{path.relative_to(REPO)}  {mask.width}x{mask.height}  {path.stat().st_size // 1024} KB  gold {cover:.1%}")


CRANES = (1500, 468, 1826, 640)  # the two cranes, in the 2400-wide purpose painting


def lift_cranes(img):
    """The close's two cranes fly on their own layer: cut them out of the painting (the sky
    behind them is inpainted from the paper around them) and return (painting, cranes)."""
    import cv2

    arr = np.asarray(img).copy()
    x0, y0, x1, y1 = CRANES
    box = arr[y0:y1, x0:x1].copy()
    dark = (box.min(axis=2) < 240).astype(np.uint8) * 255
    dark = cv2.dilate(dark, np.ones((7, 7), np.uint8))
    arr[y0:y1, x0:x1] = cv2.inpaint(box, dark, 5, cv2.INPAINT_TELEA)
    # The cranes on white, the frame feathered so no rectangle multiplies onto the page.
    h, w = y1 - y0, x1 - x0
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    edge = np.minimum.reduce([xx, yy, w - 1 - xx, h - 1 - yy])
    keep = np.clip(edge / 18, 0, 1)[..., None]
    cranes = box.astype(np.float32) * keep + 255 * (1 - keep)
    return Image.fromarray(arr), Image.fromarray(cranes.astype(np.uint8))


def save(img, name, width=None, quality=84):
    OUT.mkdir(parents=True, exist_ok=True)
    if width and img.width > width:
        img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    path = OUT / f"{name}.webp"
    img.save(path, "WEBP", quality=quality, method=6)
    print(f"{path.relative_to(REPO)}  {img.width}x{img.height}  {path.stat().st_size // 1024} KB")
    # The lossless plate (the gate scores PNG); the page ships the webp of the same pixels.
    PLATES.mkdir(parents=True, exist_ok=True)
    img.save(PLATES / f"{name}.png")


def build(name):
    if name == "landscape":
        save(ink(load("landscape-v1"), (60, 520, 900, 1100)), "landscape", 2400, 82)
    elif name == "crane":
        save(cut(load("crane-v1")), "crane", 1600, 86)
    elif name == "sun":
        img = load("sun-v1").crop((106, 45, 1906, 1805))
        save(leaf(img), "sun", 760, 80)
    elif name == "paper":
        tile = tone(seamless(load("paper-v1")))
        save(tile, "paper", 1600, 80)
    elif name == "mito":
        save(ink(load("mito-v1"), (0, 0, 500, 300)), "mito", 2000, 84)
    elif name == "mito-aged":
        # Registered onto the master's ink box so the age slider blends one organelle.
        aged = register(load("mito-aged-v1"), (391, 141, 2162, 1666), (336, 102, 2197, 1700))
        save(ink(aged, (0, 0, 500, 300)), "mito-aged", 1600, 82)
    elif name == "mito-radicals":
        save(ink(load("mito-radicals-v1"), (0, 1300, 300, 1744)), "mito-radicals", 1600, 82)
    elif name == "halo":
        save(ink(load("halo-v1"), (0, 0, 2048, 80)), "halo", 1100, 82)
    elif name == "shadow":
        # v2 (fix round, October 2): the comps' deep grey pools, with a paler wash rising behind.
        img = ink(load("shadow-v2"), (0, 0, 2688, 120))
        # Per-bottle pools: the same painted pool, ink deepened (paper stays white), and a small
        # dense contact shadow from its core.
        arr = np.asarray(img.crop((330, 330, 2330, 1400))).astype(np.float32) / 255
        save(Image.fromarray((255 * arr**1.7).astype(np.uint8)), "pool", 900, 82)
        core = np.asarray(img.crop((700, 640, 1900, 980))).astype(np.float32) / 255
        h, w, _ = core.shape
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        r = np.sqrt(((xx / w - 0.5) / 0.5) ** 2 + ((yy / h - 0.5) / 0.5) ** 2)
        falloff = np.clip(1 - r, 0, 1) ** 1.3  # 1 at the centre, 0 at the ellipse's edge
        ink_amount = (1 - core**2.2) * falloff[..., None]
        save(Image.fromarray((255 * (1 - ink_amount)).astype(np.uint8)), "pool-foot", 600, 82)
    elif name == "purpose":
        full = ink(load("purpose-v1"), (0, 0, 2688, 200))
        full = full.resize((2400, round(full.height * 2400 / full.width)), Image.LANCZOS)
        save(full, "purpose", 2400, 82)  # the whole painting: the plate, and the gold mask's source
        # What the page ships (October 3): the land and sky, and the two cranes on their own layer.
        painting, cranes = lift_cranes(full)
        save(painting, "purpose-land", 2400, 82)
        save(cranes, "purpose-cranes", None, 88)
    elif name.startswith("story-"):
        save(ink(load(f"{name}-v1"), (0, 0, 1744, 200)), name, 1200, 82)
    elif name == "mito-closeup":
        # The gold folds, close: the frame's edges dissolve into the paper like a wet wash.
        save(vignette(ink(load("mito-closeup-v1"), (0, 1600, 120, 1744))), "mito-closeup", 1600, 82)
    elif name == "crane-rest":
        # Round 5 (October 3): the crane at rest, for the page's last line. Ink on paper (its white
        # is the page's own paper), cropped to the bird with its reed and the water at its feet.
        img = ink(load("crane-rest-v1"), (0, 0, 420, 300), gain=1.02)
        save(img.crop((430, 130, 1610, 1950)), "crane-rest", 560, 86)
    elif name == "inkstone":
        # Round 5: a brush on its inkstone, for "Good questions deserve clear answers."
        save(ink(load("inkstone-v1"), (0, 0, 500, 160), gain=1.02), "inkstone", 1200, 84)
    elif name == "bloom":
        bloom_mask()
    elif name == "gold":
        # The light-catching masks for the gold leaf inside the paintings (October 3).
        gold_mask("mito")
        gold_mask("mito-closeup", bright_from=0.5)  # the dark strokes over the leaf stay out
        gold_mask("purpose", sat_from=0.2)  # the low sun's leaf is paler
    else:
        raise SystemExit(f"unknown asset {name}")


if __name__ == "__main__":
    everything = ["landscape", "crane", "sun", "paper", "mito", "mito-aged", "mito-radicals",
                  "halo", "shadow", "purpose", "story-morning", "story-reading", "story-source", "mito-closeup", "bloom", "gold", "crane-rest", "inkstone"]
    for item in sys.argv[1:] or everything:
        build(item)

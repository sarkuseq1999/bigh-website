"""Turmerific's "why" pictures (September 29 and October 2, 2026), from three Gemini renders.

Usage: python -X utf8 scripts/product-pages/why_turmerific.py [scene ...]   (default: every scene)

The renders and their prompts are in reference/product-pages/turmerific/originals/. The chapter tells
its story one picture per line (Mo, October 2: the same picture under every line "doesn't look that
interesting"), like Timeline's How it works (Design Vault #019-#029):
- root:  two fresh turmeric roots, cut open, lit gold ("the compound that gives turmeric its golden
         colour"), plus the same picture unlit, for the light coming on;
- glass: turmeric powder sinking to the bottom of a glass of water ("very little of it reaches your
         bloodstream": curcumin barely dissolves in water);
- drops: tiny golden droplets of oil ("tiny particles of fat").
For each, this script
- flattens the render's ground to the chapter's night (#061625, template-chapters.module.css)
  without touching the subject, and turns everything outside the scene's own keep shape into exactly that
  night (a stray light beam, droplets that would sit under the words);
- shrinks the subject and moves its centre to where the chapter centres its subject (69.3%, 46%:
  template-chapters-why.module.css), so every scene lands in the same place and the words never
  touch it;
- lets the bottom fall into shadow, so on phones, where the words stand just under the picture,
  they never sit on it.
Writes public/images/products/turmerific/why-<scene>-on.webp (and why-root-off.webp).
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
ORIGINALS = ROOT / "reference" / "product-pages" / "turmerific" / "originals"
NIGHT = np.array([6, 22, 37], dtype=np.float32)
LUMA = np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
FOCUS = (0.693, 0.46)

# keep: what of the render stays, as shares of its width and height. ("box", centre x, centre y,
# half width, half height, where the fade starts): a rounded box round the glass, so its rim keeps
# its corners. ("left", x0, x1): everything right of x1, fading out by x0, so the droplets spill to
# the edges as rendered but never reach the words. fade: where the bottom falls into shadow.
# lower: how much lower than the focus the subject's centre sits, as a share of the height.
SCENES = {
    "root": {"source": "why-root-lit.jpeg", "scale": 0.74, "keep": None, "fade": 0.64, "unlit": True},
    "glass": {
        "source": "why-glass.jpeg",
        "scale": 0.72,
        "keep": ("box", 0.691, 0.57, 0.2, 0.47, 0.84),
        "fade": 0.8,
        "lower": 0.045,
        "unlit": False,
    },
    "drops": {
        "source": "why-drops.jpeg",
        "scale": 0.86,
        "keep": ("left", 0.5, 0.62),
        "fade": 0.72,
        "unlit": False,
    },
}


def blur(channel, radius):
    image = Image.fromarray(np.clip(channel, 0, 255).astype(np.uint8))
    return np.asarray(image.filter(ImageFilter.GaussianBlur(radius))).astype(np.float32)


def blur_float(values, radius):
    """Gaussian blur of a float array (the ground estimate needs more than 8 bits)."""
    sigma = radius
    size = int(sigma * 3)
    kernel = np.exp(-0.5 * (np.arange(-size, size + 1) / sigma) ** 2)
    kernel /= kernel.sum()
    padded = np.pad(values, size, mode="edge")
    rows = np.apply_along_axis(lambda r: np.convolve(r, kernel, mode="valid"), 1, padded)
    return np.apply_along_axis(lambda c: np.convolve(c, kernel, mode="valid"), 0, rows)


def kept(width, height, keep):
    """1 where the scene's keep shape holds, fading to 0 at its edge (see SCENES)."""
    xs = np.arange(width, dtype=np.float32) / width
    ys = np.arange(height, dtype=np.float32) / height
    if keep[0] == "left":
        _, x0, x1 = keep
        t = np.broadcast_to(np.clip((xs[None, :] - x0) / (x1 - x0), 0, 1), (height, width))
    else:
        _, cx, cy, rx, ry, inner = keep
        # A superellipse (power 4): a box with softly rounded corners.
        r = (np.abs((xs[None, :] - cx) / rx) ** 4 + np.abs((ys[:, None] - cy) / ry) ** 4) ** 0.25
        t = np.clip((1 - r) / (1 - inner), 0, 1)
    return t * t * (3 - 2 * t)


def process(name: str, scene: dict) -> None:
    lit = np.asarray(Image.open(ORIGINALS / scene["source"]).convert("RGB")).astype(np.float32)
    height, width, _ = lit.shape

    # The ground, estimated away from the subject: a wide blur of the dark pixels only, at a quarter
    # size (the ground changes slowly). Subtracting it and adding the night flattens the ground and
    # moves the subject's colours by at most a few levels.
    luminance = lit @ LUMA
    subject = Image.fromarray((np.clip((luminance - 22) / 20, 0, 1) * 255).astype(np.uint8))
    subject = np.asarray(subject.filter(ImageFilter.MaxFilter(41)).filter(ImageFilter.GaussianBlur(20)))
    weight = 1 - subject.astype(np.float32) / 255
    small = (width // 4, height // 4)
    shrink = lambda a: np.asarray(Image.fromarray(a.astype(np.float32), mode="F").resize(small, Image.BILINEAR))
    grow = lambda a: np.asarray(
        Image.fromarray(a.astype(np.float32), mode="F").resize((width, height), Image.BILINEAR)
    )
    w_small = shrink(weight)
    ground = np.zeros_like(lit)
    for c in range(3):
        numerator = blur_float(shrink(lit[..., c] * weight), 40)
        denominator = blur_float(w_small, 40)
        ground[..., c] = grow(numerator / np.maximum(denominator, 1e-3))
    lit = np.clip(lit - ground + NIGHT, 0, 255)

    # The dark ground carries faint compression blocks. Smooth it (soft by nature) and keep the
    # subject as rendered.
    luminance = lit @ LUMA
    keep = Image.fromarray((np.clip((luminance - 45) / 30, 0, 1) * 255).astype(np.uint8))
    keep = keep.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(6))
    keep = np.asarray(keep).astype(np.float32)[..., None] / 255
    soft = np.stack([blur(lit[..., c], 10) for c in range(3)], axis=-1)
    lit = lit * keep + soft * (1 - keep)
    # Away from the subject the ground becomes exactly the night: its streaks were only a shade or
    # two, but the page's night around the picture is perfectly even.
    luminance = lit @ LUMA
    near = Image.fromarray((np.clip((luminance - 23) / 14, 0, 1) * 255).astype(np.uint8))
    near = near.filter(ImageFilter.MaxFilter(21)).filter(ImageFilter.GaussianBlur(18))
    near = np.asarray(near).astype(np.float32)[..., None] / 255
    lit = NIGHT + (lit - NIGHT) * near
    if scene["keep"]:
        lit = NIGHT + (lit - NIGHT) * kept(width, height, scene["keep"])[..., None]

    # Shrink the subject and move its centre to the chapter's focus point, filling with night.
    scale = scene["scale"]
    luminance = lit @ LUMA
    ys, xs = np.where(luminance > 70)
    small_w, small_h = int(round(width * scale)), int(round(height * scale))
    shrunk = np.stack(
        [
            np.asarray(Image.fromarray(lit[..., c], mode="F").resize((small_w, small_h), Image.LANCZOS))
            for c in range(3)
        ],
        axis=-1,
    )
    # A render whose subject runs off its edges (the droplets) would show the shrunk picture's border
    # as a straight line in the night; fade its outer twelfth into the night first.
    edge_x = np.clip(np.minimum(np.arange(small_w), np.arange(small_w)[::-1]) / (small_w / 12), 0, 1)
    edge_y = np.clip(np.minimum(np.arange(small_h), np.arange(small_h)[::-1]) / (small_h / 12), 0, 1)
    edge = (edge_y[:, None] * edge_x[None, :]).astype(np.float32)
    edge = edge * edge * (3 - 2 * edge)
    shrunk = NIGHT + (shrunk - NIGHT) * edge[..., None]
    dx = int(round(FOCUS[0] * width - xs.mean() * scale))
    # A tall subject (the glass) sits a little lower, clear of the chapter's index on phones.
    dy = int(round((FOCUS[1] + scene.get("lower", 0)) * height - ys.mean() * scale))
    moved = np.empty_like(lit)
    moved[:] = NIGHT
    x0, y0 = max(0, dx), max(0, dy)
    x1, y1 = min(width, dx + small_w), min(height, dy + small_h)
    moved[y0:y1, x0:x1] = shrunk[y0 - dy : y1 - dy, x0 - dx : x1 - dx]
    lit = moved

    # Toward the bottom the picture falls into shadow.
    rows = np.linspace(0, 1, height, dtype=np.float32)
    t = np.clip((rows - scene["fade"]) / (1 - scene["fade"]), 0, 1)
    fade = 1 - 0.8 * (t * t * (3 - 2 * t))
    lit = NIGHT + (lit - NIGHT) * fade[:, None, None]

    outputs = [(f"why-{name}-on", lit)]
    if scene["unlit"]:
        # Unlit: only the subject stays, faint, cool and nearly colourless.
        luminance = lit @ LUMA
        shape = np.clip((luminance - 50) / 60, 0, 1)
        shape = shape * shape * (3 - 2 * shape)
        mask = Image.fromarray((shape * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9))
        mask = np.asarray(mask.filter(ImageFilter.GaussianBlur(5))).astype(np.float32) / 255
        delta = lit - NIGHT
        grey = (delta @ LUMA)[..., None]
        cool = (grey * 0.7 + delta * 0.3) * np.array([0.7, 0.85, 1.1], dtype=np.float32)
        outputs.append((f"why-{name}-off", NIGHT + cool * 0.2 * mask[..., None]))

    out = ROOT / "public" / "images" / "products" / "turmerific"
    out.mkdir(parents=True, exist_ok=True)
    # A whisper of noise before rounding, so the smooth gradients do not band.
    rng = np.random.default_rng(29)
    for file, pixels in outputs:
        pixels = pixels + rng.uniform(-0.5, 0.5, pixels.shape)
        Image.fromarray(np.clip(np.round(pixels), 0, 255).astype(np.uint8)).save(
            out / f"{file}.webp", quality=88, method=6
        )
    print(f"{name}: {width}x{height}, scale {scale}, moved {dx:+d}px, {dy:+d}px")


if __name__ == "__main__":
    for scene_name in sys.argv[1:] or SCENES:
        process(scene_name, SCENES[scene_name])

"""Turmerific's "why" pictures (September 29, 2026), from one Gemini render.

Usage: python -X utf8 scripts/product-pages/why_turmerific.py <render.jpeg>

The render (reference/product-pages/turmerific/originals/, prompt in its sidecar) is the lit
picture: two fresh turmeric roots, cut open, their golden flesh in a warm light. This script
- flattens the render's ground (darker at the top, a lit table at the bottom) to the chapter's
  night (#061625, template-chapters.module.css) without touching the roots, and moves the roots to
  where the chapter centres its subject (69.3%, 46%: template-chapters-why.module.css);
- lets the table's reflection fall into shadow toward the bottom, so on phones, where the words
  stand just under the picture, they never sit on it;
- makes the unlit picture from the same pixels: the roots a faint cool shape, the gold gone. Same
  framing, so the chapter can cross-fade them. (Follows why_propolis.py on the Propolis branch.)
Writes public/images/products/turmerific/why-root-on.webp and why-root-off.webp.
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
NIGHT = np.array([6, 22, 37], dtype=np.float32)
LUMA = np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
FOCUS = (0.693, 0.46)
SCALE = 0.74


def blur(channel, radius):
    image = Image.fromarray(np.clip(channel, 0, 255).astype(np.uint8))
    return np.asarray(image.filter(ImageFilter.GaussianBlur(radius))).astype(np.float32)


def main(source: str) -> None:
    lit = np.asarray(Image.open(source).convert("RGB")).astype(np.float32)
    height, width, _ = lit.shape

    # The ground, estimated away from the roots: a wide blur of the dark pixels only, at a quarter
    # size (the ground changes slowly). Subtracting it and adding the night flattens the ground and
    # moves the roots' colours by at most a few levels.
    luminance = lit @ LUMA
    roots = Image.fromarray((np.clip((luminance - 22) / 20, 0, 1) * 255).astype(np.uint8))
    roots = np.asarray(roots.filter(ImageFilter.MaxFilter(41)).filter(ImageFilter.GaussianBlur(20)))
    weight = 1 - roots.astype(np.float32) / 255
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

    # The dark ground carries faint compression blocks. Smooth it and the reflection (both soft by
    # nature) and keep the roots as rendered.
    luminance = lit @ LUMA
    keep = Image.fromarray((np.clip((luminance - 45) / 30, 0, 1) * 255).astype(np.uint8))
    keep = keep.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(6))
    keep = np.asarray(keep).astype(np.float32)[..., None] / 255
    soft = np.stack([blur(lit[..., c], 10) for c in range(3)], axis=-1)
    lit = lit * keep + soft * (1 - keep)
    # Away from the roots and their reflection the ground becomes exactly the night: its streaks
    # were only a shade or two, but the page's night around the picture is perfectly even.
    luminance = lit @ LUMA
    near = Image.fromarray((np.clip((luminance - 23) / 14, 0, 1) * 255).astype(np.uint8))
    near = near.filter(ImageFilter.MaxFilter(21)).filter(ImageFilter.GaussianBlur(18))
    near = np.asarray(near).astype(np.float32)[..., None] / 255
    lit = NIGHT + (lit - NIGHT) * near

    # Shrink the roots (the chapter shows its picture large: at full size the words touched the
    # roots on desktop and phones cut both ends off, as Nature Calm's microscope did) and move their
    # centre to the chapter's focus point, filling with night.
    luminance = lit @ LUMA
    ys, xs = np.where(luminance > 70)
    small_w, small_h = int(round(width * SCALE)), int(round(height * SCALE))
    shrunk = np.stack(
        [
            np.asarray(Image.fromarray(lit[..., c], mode="F").resize((small_w, small_h), Image.LANCZOS))
            for c in range(3)
        ],
        axis=-1,
    )
    dx = int(round(FOCUS[0] * width - xs.mean() * SCALE))
    dy = int(round(FOCUS[1] * height - ys.mean() * SCALE))
    moved = np.empty_like(lit)
    moved[:] = NIGHT
    x0, y0 = max(0, dx), max(0, dy)
    x1, y1 = min(width, dx + small_w), min(height, dy + small_h)
    moved[y0:y1, x0:x1] = shrunk[y0 - dy : y1 - dy, x0 - dx : x1 - dx]
    lit = moved

    # Toward the bottom the reflection falls into shadow.
    rows = np.linspace(0, 1, height, dtype=np.float32)
    t = np.clip((rows - 0.64) / 0.36, 0, 1)
    fade = 1 - 0.8 * (t * t * (3 - 2 * t))
    lit = NIGHT + (lit - NIGHT) * fade[:, None, None]

    # Unlit: only the roots stay, faint, cool and nearly colourless.
    luminance = lit @ LUMA
    subject = np.clip((luminance - 50) / 60, 0, 1)
    subject = subject * subject * (3 - 2 * subject)
    mask = Image.fromarray((subject * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9))
    mask = np.asarray(mask.filter(ImageFilter.GaussianBlur(5))).astype(np.float32) / 255
    delta = lit - NIGHT
    grey = (delta @ LUMA)[..., None]
    cool = (grey * 0.7 + delta * 0.3) * np.array([0.7, 0.85, 1.1], dtype=np.float32)
    unlit = NIGHT + cool * 0.2 * mask[..., None]

    out = ROOT / "public" / "images" / "products" / "turmerific"
    out.mkdir(parents=True, exist_ok=True)
    # A whisper of noise before rounding, so the smooth gradients do not band.
    rng = np.random.default_rng(29)
    for name, pixels in (("why-root-on", lit), ("why-root-off", unlit)):
        pixels = pixels + rng.uniform(-0.5, 0.5, pixels.shape)
        Image.fromarray(np.clip(np.round(pixels), 0, 255).astype(np.uint8)).save(
            out / f"{name}.webp", quality=88, method=6
        )
    print(f"{width}x{height}, moved {dx:+d}px, {dy:+d}px")


def blur_float(values, radius):
    """Gaussian blur of a float array (the ground estimate needs more than 8 bits)."""
    sigma = radius
    size = int(sigma * 3)
    kernel = np.exp(-0.5 * (np.arange(-size, size + 1) / sigma) ** 2)
    kernel /= kernel.sum()
    padded = np.pad(values, size, mode="edge")
    rows = np.apply_along_axis(lambda r: np.convolve(r, kernel, mode="valid"), 1, padded)
    return np.apply_along_axis(lambda c: np.convolve(c, kernel, mode="valid"), 0, rows)


if __name__ == "__main__":
    main(sys.argv[1])

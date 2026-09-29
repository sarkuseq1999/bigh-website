"""Green Bee Propolis's "why" pictures (September 29, 2026), from one Gemini render.

Usage: python -X utf8 scripts/product-pages/why_propolis.py <render.jpeg>

The render (reference/product-pages/green-bee-propolis/originals/, prompt in its sidecar) is the
lit picture: a honeybee gathering resin at an alecrim shoot tip in the first sunlight. This script
- sets it on the chapter's night (#061625, template-chapters.module.css) and moves it down so the
  shoot tip sits where the chapter centres its subject (69.3%, 46%: template-chapters-why.module.css),
  and lets the shoot's foot fall into shadow;
- makes the unlit picture from the same pixels: before sunrise the shoot and the bee are a faint cool
  shape and the warm halo is gone. Same framing, so the chapter can cross-fade them.
Writes public/images/products/green-bee-propolis/why-bee-on.webp and why-bee-off.webp.
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
NIGHT = np.array([6, 22, 37], dtype=np.float32)
SHIFT = 0.09  # of the height: the shoot tip from about 37% down to 46%


def main(source: str) -> None:
    lit = np.asarray(Image.open(source).convert("RGB")).astype(np.float32)
    height, width, _ = lit.shape

    # The render's ground is a hair darker than the page's night; lift it to match.
    ground = np.median(np.concatenate([lit[:40, :400].reshape(-1, 3), lit[-40:, :400].reshape(-1, 3)]), axis=0)
    lit = np.clip(lit + (NIGHT - ground), 0, 255)

    # Move down, filling the top with night; the shoot's foot leaves at the bottom (feathered there).
    shift = int(round(height * SHIFT))
    moved = np.empty_like(lit)
    moved[:shift] = NIGHT
    moved[shift:] = lit[: height - shift]
    # Blend the seam over a few rows so it cannot show.
    for i in range(24):
        t = i / 24
        moved[shift + i] = NIGHT * (1 - t) + moved[shift + i] * t
    lit = moved

    # The render's dark ground carries faint compression blocks. Smooth the ground and the halo
    # (both soft by nature) and keep the shoot and the bee as rendered.
    luminance = lit @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    keep = Image.fromarray((np.clip((luminance - 45) / 30, 0, 1) * 255).astype(np.uint8))
    keep = keep.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(6))
    keep = np.asarray(keep).astype(np.float32)[..., None] / 255
    soft = np.stack(
        [
            np.asarray(Image.fromarray(np.clip(lit[..., c], 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(10))).astype(np.float32)
            for c in range(3)
        ],
        axis=-1,
    )
    lit = lit * keep + soft * (1 - keep)

    # The shoot's foot falls into shadow toward the bottom, so on phones, where the words stand just
    # under the picture, they never sit on bright leaves.
    rows = np.linspace(0, 1, height, dtype=np.float32)
    t = np.clip((rows - 0.62) / 0.38, 0, 1)
    fade = 1 - 0.72 * (t * t * (3 - 2 * t))
    lit = NIGHT + (lit - NIGHT) * fade[:, None, None]

    # Unlit: only the subject stays, faint, cool and nearly colourless; the halo goes to night.
    luminance = lit @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    subject = np.clip((luminance - 70) / 60, 0, 1)
    subject = subject * subject * (3 - 2 * subject)
    mask = Image.fromarray((subject * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9))
    mask = np.asarray(mask.filter(ImageFilter.GaussianBlur(5))).astype(np.float32) / 255
    delta = lit - NIGHT
    grey = (delta @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32))[..., None]
    cool = (grey * 0.7 + delta * 0.3) * np.array([0.7, 0.85, 1.1], dtype=np.float32)
    unlit = NIGHT + cool * 0.2 * mask[..., None]

    out = ROOT / "public" / "images" / "products" / "green-bee-propolis"
    out.mkdir(parents=True, exist_ok=True)
    # A whisper of noise before rounding, so the smooth gradients do not band.
    rng = np.random.default_rng(29)
    for name, pixels in (("why-bee-on", lit), ("why-bee-off", unlit)):
        pixels = pixels + rng.uniform(-0.5, 0.5, pixels.shape)
        Image.fromarray(np.clip(np.round(pixels), 0, 255).astype(np.uint8)).save(
            out / f"{name}.webp", quality=88, method=6
        )
    print(f"{width}x{height}, ground {ground.round()}, moved down {shift}px")


if __name__ == "__main__":
    main(sys.argv[1])

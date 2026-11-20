"""Build the homepage's lantern paintings ("Make sense of the science.", Mo picked A, November 20, 2026).

Mitochondria: an old barn lantern, its flame in gold leaf (fuel in, light out). Free radicals:
the same lantern up close, soot gathered on the upper glass. Codex paintings on white paper
(originals/redo-lantern-1.png, redo-lantern-soot-1.png; prompts under the same names).

Each is fitted to the science stage's 4:3 frame exactly as Mo saw it in the mockup
(reference/ink-pages/mockups/home-science-redo/prep.py): the paper lifted to pure white (the
stage multiplies onto the page, so white vanishes), the washes given a little more body, the
painting's own edges feathered to white so no cut line shows where paint reaches the frame.

Usage: python -X utf8 reference/ink-pages/home-science/build_lantern.py
"""

from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[2] / "public/images/home-v2/ink/science"
W, H = 1448, 1086
DEEPEN = 1.2  # gamma on the paint: thin washes hold on the page's paper; white stays white
FEATHER = 56  # px of the original over which each edge fades to bare paper
# name: (original, scale inside the frame; 1.0 = the original's whole width)
PAINTINGS = {
    "lantern-fuel-v1": ("redo-lantern-1", 1.12),
    "lantern-soot-v1": ("redo-lantern-soot-1", 1.0),
}


def paper_out(rgb: np.ndarray) -> np.ndarray:
    """Divide the paper out: the border's lightest tone becomes pure white."""
    border = np.concatenate(
        [rgb[:8].reshape(-1, 3), rgb[-8:].reshape(-1, 3), rgb[:, :8].reshape(-1, 3), rgb[:, -8:].reshape(-1, 3)]
    )
    paper = np.percentile(border, 90, axis=0)
    return np.clip(rgb / paper, 0, 1)


def feather(rgb: np.ndarray) -> np.ndarray:
    """Fade each edge to white, so paint that reaches the frame dissolves instead of being cut."""
    h, w, _ = rgb.shape
    ramp_y = np.clip(np.minimum(np.arange(h), np.arange(h)[::-1]) / FEATHER, 0, 1)
    ramp_x = np.clip(np.minimum(np.arange(w), np.arange(w)[::-1]) / FEATHER, 0, 1)
    keep = (ramp_y[:, None] * ramp_x[None, :]) ** 0.5
    keep = (3 * keep**2 - 2 * keep**3)[..., None]  # smoothstep
    return 1 - (1 - rgb) * keep


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (original, scale) in PAINTINGS.items():
        rgb = np.asarray(Image.open(HERE / f"originals/{original}.png").convert("RGB")).astype(np.float64) / 255
        rgb = feather(paper_out(rgb)) ** DEEPEN
        img = Image.fromarray((rgb * 255).round().astype(np.uint8))
        w = round(W * scale)
        img = img.resize((w, round(img.height * w / img.width)), Image.LANCZOS)
        canvas = Image.new("RGB", (W, H), "white")
        canvas.paste(img, ((W - w) // 2, (H - img.height) // 2))
        target = OUT / f"{name}.webp"
        canvas.save(target, format="WEBP", quality=90, method=6)
        print(f"{target.name}: {canvas.width}x{canvas.height}, {target.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()

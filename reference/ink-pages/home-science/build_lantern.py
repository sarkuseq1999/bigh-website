"""Build the homepage's lantern paintings ("Make sense of the science.", Mo picked A, November 20, 2026).

Mitochondria: an old barn lantern, its flame in gold leaf (fuel in, light out). Free radicals:
the same lantern throwing gold sparks, its glass holding most of them in, the few that get out
scorching one of its two poppies (Mo's pick the same day; the first Free radicals picture, soot
on the glass, lantern-soot-v1, was not intuitive enough). Codex paintings on white paper
(originals/redo-lantern-1.png, SPARKS below; prompts under the same names). The sparks picture is
take 3, a Codex edit of the take Mo picked (redo-lantern-poppy-2) that only repaints the burnt
petals softer; the edit left one perfectly round hole in a petal that read as an eye, so MEND
paints it out here (the original stays as Codex made it).

Each is fitted to the science stage's 4:3 frame exactly as Mo saw it in the mockup
(reference/ink-pages/mockups/home-science-redo/prep.py): the paper lifted to pure white (the
stage multiplies onto the page, so white vanishes), the washes given a little more body, the
painting's own edges feathered to white so no cut line shows where paint reaches the frame.

Usage: python -X utf8 reference/ink-pages/home-science/build_lantern.py
"""

from pathlib import Path

import cv2
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[2] / "public/images/home-v2/ink/science"
W, H = 1448, 1086
DEEPEN = 1.2  # gamma on the paint: thin washes hold on the page's paper; white stays white
FEATHER = 56  # px of the original over which each edge fades to bare paper
SPARKS = "redo-lantern-poppy-3"
# original: [(x, y, radius)] spots to paint out from their surroundings before anything else
MEND = {SPARKS: [(1009, 608, 20)]}
# original: (dx, dy) in its own px. The sparks lantern is moved onto the first picture's lantern
# (their blue-grey metal measured: x 453-846 against 546-931, y 205-836 against 205-828), so the
# lantern holds still while the stage blooms from one topic to the other.
SHIFT = {SPARKS: (89, -4)}
# name: (original, scale inside the frame; 1.0 = the original's whole width)
PAINTINGS = {
    "lantern-fuel-v1": ("redo-lantern-1", 1.12),
    "lantern-soot-v1": ("redo-lantern-soot-1", 1.0),  # live for an hour on November 20; kept
    "lantern-sparks-v1": (SPARKS, 1.12),
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
        source = np.asarray(Image.open(HERE / f"originals/{original}.png").convert("RGB"))
        for x, y, radius in MEND.get(original, []):
            spot = np.zeros(source.shape[:2], np.uint8)
            cv2.circle(spot, (x, y), radius, 255, -1)
            source = cv2.inpaint(source, spot, 9, cv2.INPAINT_TELEA)
        rgb = source.astype(np.float64) / 255
        rgb = feather(paper_out(rgb)) ** DEEPEN
        img = Image.fromarray((rgb * 255).round().astype(np.uint8))
        w = round(W * scale)
        img = img.resize((w, round(img.height * w / img.width)), Image.LANCZOS)
        canvas = Image.new("RGB", (W, H), "white")
        dx, dy = (round(d * w / source.shape[1]) for d in SHIFT.get(original, (0, 0)))
        canvas.paste(img, ((W - w) // 2 + dx, (H - img.height) // 2 + dy))
        target = OUT / f"{name}.webp"
        canvas.save(target, format="WEBP", quality=90, method=6)
        print(f"{target.name}: {canvas.width}x{canvas.height}, {target.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()

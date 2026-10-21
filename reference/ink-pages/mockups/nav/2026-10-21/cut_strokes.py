"""Cut the two Codex paintings into ink-only strokes (paper divided out) for the mockups.

Alpha is how much ink covers the paper (1 - lightness, with the paper's own near-white lifted to
zero); the colour is the site's brush ink. Cropped to the stroke with a little air.
"""

from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).parent
OUT = HERE / "assets"
OUT.mkdir(exist_ok=True)
INK = (20, 19, 17)  # brush-ink #141311


def cut(src: Path, dst: Path, white: float, gain: float, width: int) -> None:
    rgb = np.asarray(Image.open(src).convert("RGB")).astype(np.float32) / 255
    light = rgb.mean(axis=2)
    alpha = np.clip((white - light) / white * gain, 0, 1)
    rows = np.where(alpha.max(axis=1) > 0.04)[0]
    cols = np.where(alpha.max(axis=0) > 0.04)[0]
    pad = 6
    top, bottom = max(rows[0] - pad, 0), min(rows[-1] + pad, alpha.shape[0])
    left, right = max(cols[0] - pad, 0), min(cols[-1] + pad, alpha.shape[1])
    alpha = alpha[top:bottom, left:right]
    out = np.zeros((*alpha.shape, 4), dtype=np.uint8)
    out[..., 0], out[..., 1], out[..., 2] = INK
    out[..., 3] = (alpha * 255).round().astype(np.uint8)
    image = Image.fromarray(out, "RGBA")
    if image.width > width:
        image = image.resize((width, round(image.height * width / image.width)), Image.LANCZOS)
    image.save(dst, quality=92)
    print(dst.name, image.size)


cut(HERE / "codex-band" / "band.png", OUT / "band.webp", white=0.97, gain=1.0, width=2172)
cut(HERE / "codex-swash" / "swash.png", OUT / "swash.webp", white=0.95, gain=1.15, width=900)

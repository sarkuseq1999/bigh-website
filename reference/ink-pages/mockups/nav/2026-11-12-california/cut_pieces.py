"""Cut the Codex paintings for ideas C (poppy) and D (sky strip) into transparent pieces.

    python -X utf8 cut_pieces.py

Paper is divided out (alpha = distance of the darkest channel from the page's white; colour
unmultiplied), so each piece lays its paint on the site's rice paper the way the paintings do.
Writes mock/poppy-swatch.png, mock/poppy-dash.png and mock/sky.png.
"""

from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).parent
MOCK = HERE / "mock"
MOCK.mkdir(exist_ok=True)


def unpaper(path):
    a = np.asarray(Image.open(path).convert("RGB"), dtype=np.float64) / 255
    white = np.percentile(a.reshape(-1, 3), 92, axis=0)
    a = np.clip(a / white, 0, 1)
    alpha = np.clip((1 - a.min(axis=2) - 0.02) / 0.98, 0, 1)
    rgb = np.clip(1 - (1 - a) / np.maximum(alpha[..., None], 1e-3), 0, 1)
    return rgb, alpha


def calm(rgb, chroma):
    lum = (rgb * [0.2126, 0.7152, 0.0722]).sum(axis=2, keepdims=True)
    return lum + (rgb - lum) * chroma


def save(rgb, alpha, name):
    Image.fromarray(np.dstack([rgb * 255, alpha[..., None] * 255]).astype(np.uint8), "RGBA").save(MOCK / name)


def bbox(alpha, t=0.05, pad=6):
    ys, xs = np.where(alpha > t)
    return max(ys.min() - pad, 0), ys.max() + pad, max(xs.min() - pad, 0), xs.max() + pad


# C: the poppy swatch behind Sign up, a touch calmer than the painting.
rgb, al = unpaper(HERE / "job5" / "poppy-swatch-1.png")
y0, y1, x0, x1 = bbox(al)
save(calm(rgb, 0.8)[y0:y1, x0:x1], al[y0:y1, x0:x1], "poppy-swatch.png")
print("swatch", x1 - x0, y1 - y0)

# C: one poppy dash (the top one) for the page you're on.
rgb, al = unpaper(HERE / "job6" / "poppy-dash-1.png")
top = al[: al.shape[0] // 4]
y0, y1, x0, x1 = bbox(top)
save(calm(rgb, 0.9)[y0:y1, x0:x1], al[y0:y1, x0:x1], "poppy-dash.png")
print("dash", x1 - x0, y1 - y0)

# D: the sky strip. The painting's sky is a soft wash, so it can be drawn much shorter than painted;
# the hills keep their own shape and fade into the paper soon under the ridge.
rgb, al = unpaper(HERE / "job8" / "sky-strip-2.png")
h, w = al.shape
ridge_top = 560  # just above the highest oak in this painting
sky_rows = 122  # the painted sky (0..ridge_top) drawn this tall
hill_rows = 92  # rows of hills kept under ridge_top before they have faded
sky = Image.fromarray(np.dstack([rgb[:ridge_top] * 255, al[:ridge_top, :, None] * 255]).astype(np.uint8), "RGBA")
sky = sky.resize((w, sky_rows), Image.LANCZOS)
hills_rgb = rgb[ridge_top : ridge_top + hill_rows]
hills_al = al[ridge_top : ridge_top + hill_rows].copy()
t = np.linspace(0, 1, hill_rows)[:, None]
fade = np.clip(1 - (t - 0.45) / 0.55, 0, 1)
hills_al *= fade * fade * (3 - 2 * fade)
hills = Image.fromarray(np.dstack([hills_rgb * 255, hills_al[..., None] * 255]).astype(np.uint8), "RGBA")
strip = Image.new("RGBA", (w, sky_rows + hill_rows))
strip.paste(sky, (0, 0))
strip.paste(hills, (0, sky_rows))
strip.save(MOCK / "sky.png")
print("sky", strip.size, "ridge at about", round((sky_rows + 30) / strip.size[1], 3))

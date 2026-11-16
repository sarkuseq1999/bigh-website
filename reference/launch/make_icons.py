"""The site's icons from the logo's two green leaves (November 16, 2026, for launch: icon.svg was
an empty 32x32 SVG, so every tab showed a blank icon). Writes src/app/icon.png (transparent, for
tabs), src/app/apple-icon.png (on the site's paper, for phone home screens) and
src/app/favicon.ico (16, 32, 48 for older browsers).
Run from the repo root: python reference/launch/make_icons.py"""
import numpy as np
from PIL import Image

logo = Image.open("public/images/brand/bigh-logo-black-green.png").convert("RGBA")
a = np.asarray(logo).astype(int)
green = (a[..., 3] > 20) & (a[..., 1] > a[..., 0] + 25) & (a[..., 1] > a[..., 2] + 25)
ys, xs = np.nonzero(green)
box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
leaves = logo.crop(box)
# Keep only the leaves (the crop can catch the top of the black letters): clear non-green pixels.
la = np.asarray(leaves).copy()
g = (la[..., 1].astype(int) > la[..., 0].astype(int) + 10)
la[..., 3] = np.where(g, la[..., 3], 0)
leaves = Image.fromarray(la)


def square(size, pad, background=None):
    canvas = Image.new("RGBA", (size, size), background or (0, 0, 0, 0))
    inner = size - 2 * pad
    w, h = leaves.size
    scale = inner / max(w, h)
    art = leaves.resize((max(1, round(w * scale)), max(1, round(h * scale))), Image.LANCZOS)
    canvas.alpha_composite(art, ((size - art.width) // 2, (size - art.height) // 2))
    return canvas


square(512, 24).save("src/app/icon.png")
square(180, 26, (248, 243, 234, 255)).convert("RGB").save("src/app/apple-icon.png")
square(256, 8).save("src/app/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
print("leaves box", box)

"""Cut the footer's trail sign (GPT Image 2.5, originals/gpt25-sign-v1.png) into the site's two
pictures: public/images/home-v2/ink/fda-sign.webp (the sign, its grass and the oak on the hill) and
fda-sign-phone.webp (the same without the hill and the oak, its right end fading out).

The paper becomes transparent so the sign stands on the paper footers and on the Science page's dark
one alike. The wood is solid (its own painted colours, opaque); the loose washes around it (grass,
hill, oak) are un-multiplied from the paper: over white paper they look exactly as painted, and over
a dark footer they keep their colour instead of vanishing.

Prints the 9-slice numbers for fda-statement.module.css (in the webp's pixels).

usage: python -X utf8 reference/ink-pages/fda-sign/build_sign.py
"""

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).parent
REPO = HERE.parents[2]
SRC = HERE / "originals" / "gpt25-sign-v1.png"
OUT = REPO / "public" / "images" / "home-v2" / "ink"
SCALE = 0.42  # 2x screens show the sign at 0.2 CSS px per painting px, so 0.4 is enough

# Source pixels (2688 x 1520), measured on the painting.
CROP = (240, 300, 2660, 1325)  # the sign, its grass and the hill, with a little paper around
PHONE_RIGHT = 1990  # the phone picture ends here: past the plank's right end, before the oak
SLICE_X = (900, 1490)  # between the posts: only these columns stretch sideways
SLICE_Y = (520, 790)  # inside the panel: only these rows stretch downwards
PANEL_X = (640, 1760)  # where words may go, inside the panel's routed border
# The wood: the plank, the post tops above it and the legs below it. Only inside these boxes can
# the painting be solid (the grass around the legs stays a wash).
WOOD = [(478, 412, 1892, 888), (662, 318, 888, 434), (1502, 318, 1728, 434), (668, 868, 879, 1226), (1510, 868, 1718, 1226)]


def cutout(rgb):
    a = rgb.astype(float)
    paper = np.median(a[:60].reshape(-1, 3), axis=0)
    # Un-multiply from the paper: alpha is how much darker than the paper a pixel is, at most.
    c = np.clip(a / paper * 255.0, 0, 255)
    alpha_w = 1.0 - c.min(axis=2) / 255.0
    safe = np.maximum(alpha_w, 1e-3)[..., None]
    wash = np.clip((c - 255.0 * (1.0 - alpha_w[..., None])) / safe, 0, 255)
    # The wood: dark enough to be the sign, closed and filled, so the plank and the posts are solid.
    dark = Image.fromarray(((a.mean(axis=2) < paper.mean() - 70) * 255).astype("uint8"))
    dark = dark.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.MinFilter(9))
    box = Image.new("L", dark.size, 0)
    for b in WOOD:
        ImageDraw.Draw(box).rectangle(b, fill=255)
    # copy(): an image made from an array is read-only, and floodfill would silently do nothing.
    dark = Image.fromarray(np.minimum(np.asarray(dark), np.asarray(box))).copy()
    ImageDraw.floodfill(dark, (1200, 650), 200)  # the sign: the dark piece the panel belongs to
    sign = Image.fromarray(((np.asarray(dark) == 200) * 255).astype("uint8"))
    filled = sign.copy()
    ImageDraw.floodfill(filled, (0, 0), 128)  # the paper outside it; whatever else is left is a hole in the wood
    solid = (np.asarray(filled) != 128).astype(float)
    solid = np.asarray(Image.fromarray((solid * 255).astype("uint8")).filter(ImageFilter.MinFilter(5))
                       .filter(ImageFilter.GaussianBlur(1.5))).astype(float) / 255.0
    alpha = solid + (1.0 - solid) * alpha_w
    colour = (solid[..., None] * a + ((1.0 - solid) * alpha_w)[..., None] * wash) / np.maximum(alpha, 1e-3)[..., None]
    out = np.dstack([np.clip(colour, 0, 255), np.clip(alpha * 255.0, 0, 255)]).astype("uint8")
    return Image.fromarray(out, "RGBA"), solid


def save(img, name):
    w, h = round(img.width * SCALE), round(img.height * SCALE)
    img = img.resize((w, h), Image.LANCZOS)
    path = OUT / name
    img.save(path, "WEBP", quality=78, alpha_quality=80, method=6)
    print(f"{name}: {w} x {h}, {path.stat().st_size // 1024} KB")
    return img


def main():
    full, solid = cutout(np.asarray(Image.open(SRC).convert("RGB")))
    sign = full.crop(CROP)
    save(sign, "fda-sign.webp")
    phone = full.crop((CROP[0], CROP[1], PHONE_RIGHT, CROP[3]))
    fade = 170
    px = np.asarray(phone).copy()
    wood = solid[CROP[1]:CROP[3], CROP[0]:PHONE_RIGHT]
    ramp = np.linspace(1.0, 0.0, fade)[None, :]
    keep = np.maximum(ramp, wood[:, -fade:])  # the grass fades out; the wood never does
    px[:, -fade:, 3] = (px[:, -fade:, 3] * keep).astype("uint8")
    save(Image.fromarray(px, "RGBA"), "fda-sign-phone.webp")

    k = SCALE
    x0, y0 = CROP[0], CROP[1]
    print("slice (top right bottom left), webp px:")
    print("  full: ", round((SLICE_Y[0] - y0) * k), round((CROP[2] - SLICE_X[1]) * k),
          round((CROP[3] - SLICE_Y[1]) * k), round((SLICE_X[0] - x0) * k))
    print("  phone:", round((SLICE_Y[0] - y0) * k), round((PHONE_RIGHT - SLICE_X[1]) * k),
          round((CROP[3] - SLICE_Y[1]) * k), round((SLICE_X[0] - x0) * k))
    print("panel reach (left, right), webp px:", round((SLICE_X[0] - PANEL_X[0]) * k), round((PANEL_X[1] - SLICE_X[1]) * k))


if __name__ == "__main__":
    main()

"""Build the sunshine in NuriCell's opening (Mo picked A, "light from the corner", November 11,
2026; mockups reference/ink-pages/mockups/nuricell-opening/round7/). Mo asked for "some kind of
reflection of the sun" in the opening's upper right corner: "California sunshine".

The sun is just out of the picture: its warm light pours into the sky from beyond the window's top
right corner (`light`), and its sparkle lies on the sea under that corner (`glint`). Both are laid
over the opening's painting, inside its blend group (nuricell-opening.tsx, nuricell.module.css).

Codex painted the light as skies of its own, with the opening's painting attached so the blue and
the hand match (paint_sun.sh; prompts/opening-suncorner-1.txt and opening-sundisc-1.txt): LIGHT
(light pouring in from beyond the top right corner) and GLINT (a small sun over the sea, of which
only the sparkle on the water is used). Their blue is Codex's, not the opening's, so only the light
is taken from them: where a take is less blue than its own plain sky at that height, the blue was
lifted and warm paint laid in. That share (`lift`) becomes the layer's alpha and the warm paint its
colour, so on the page the opening's own sky shows wherever the take is plain blue, and the light
keeps the take's brush edges, blooms and backruns.

    python -X utf8 reference/ink-pages/nuricell/build_nuricell_sun.py

Writes public/images/products/nuricell/ink/opening-sun{,-glint}-v<N>.webp and
src/components/product/ink/nuricell-sun-art.ts.
"""

import json
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, gaussian_filter1d

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
OUT = REPO / "public/images/products/nuricell/ink"
URL = "/images/products/nuricell/ink"
TS = REPO / "src/components/product/ink/nuricell-sun-art.ts"
LIGHT = "opening-suncorner-a"
GLINT = "opening-sundisc-b"
# Bump when a shipped picture changes after it has been pushed (the image optimizer caches by URL).
V = "v1"
QUALITY = 86
# The light: the take's columns from LIGHT_X of its width (the plain sky left of them is not
# taken), its rows down to LIGHT_ROWS of its height; its left and bottom ease out over EASE of
# the take's width and height.
LIGHT_X = 0.36
LIGHT_ROWS = 0.7
EASE = 0.12
# The light's top edge is its brightest, so if it ended inside the window (a tablet, where the
# painting's top is near the window's top) it would end in a hard line. Its first PAD rows are laid
# again above it, mirrored, and the page sets the layer's top at or above the painting's own top:
# the light can only end where the painting ends.
PAD = 300
# The glint: the sea's rows under the take's horizon (SEA of its height), the columns within
# REACH of the take's width either side of its sun, laid STRONGER than painted (the flecks are
# thin and are shown at about a third of the take's size), squeezed to SQUEEZE of its height (a
# flatter band, so it stays on the open sea under the horizon, clear of the bluff's grass).
SEA = 0.13
REACH = 0.2
STRONGER = 1.5
SQUEEZE = 0.78


def blueness(a):
    return a[..., 2] - a[..., 0]


def plain_sky(a, rows, x0, x1, smooth):
    """The take's plain sky (or sea) at each row: the median blueness and colour of columns x0..x1,
    far from the light, smoothed down the rows."""
    part = a[rows[0] : rows[1], x0:x1]
    b = gaussian_filter1d(np.median(blueness(part), axis=1), smooth)
    rgb = gaussian_filter1d(np.median(part, axis=1), smooth, axis=0)
    return b, rgb


def lifted(a, rows, ref):
    """How much of the plain blue was lifted at each pixel of the rows (0..1)."""
    part = a[rows[0] : rows[1]]
    lift = np.clip(1 - blueness(part) / np.maximum(ref[:, None], 1), 0, 1)
    # A soft floor: the plain wash's own unevenness (a few percent) is not light.
    lift = np.clip((lift - 0.1) / 0.9, 0, 1)
    return part, gaussian_filter(lift, 0.8)


def paint_of(part, lift, sky_rgb):
    """The warm paint laid where the blue was lifted: take = sky * (1 - lift) + paint * lift."""
    l = lift[..., None]
    paint = np.clip((part - sky_rgb[:, None, :] * (1 - l)) / np.maximum(l, 0.15), 0, 255)
    # Where the lift is small the estimate is noise: lean on a warm white.
    warm = np.array([255.0, 250.0, 226.0])
    w = np.clip((l - 0.15) / 0.35, 0, 1)
    paint = paint * w + warm * (1 - w)
    # Paper is white: keep the paint from going grey or blue, and its warmth a yellow, never pink
    # (green at least as strong as red, blue no stronger than green).
    paint = np.maximum(paint, paint.max(axis=2, keepdims=True) * 0.86)
    paint[..., 1] = np.maximum(paint[..., 1], paint[..., 0] * 0.985)
    paint[..., 0] = np.minimum(paint[..., 0], paint[..., 1] / 0.985)
    paint[..., 2] = np.minimum(paint[..., 2], paint[..., 1])
    return paint


def eased(alpha, left=0, right=0, bottom=0):
    """The alpha eased to nothing over the given number of pixels at each edge."""
    h, w = alpha.shape
    xs, ys = np.arange(w), np.arange(h)
    f = np.ones((h, w))
    for n, d in ((left, xs[None, :]), (right, (w - 1 - xs)[None, :]), (bottom, (h - 1 - ys)[:, None])):
        if n:
            t = np.clip(d / n, 0, 1)
            f = f * (t * t * (3 - 2 * t))
    return alpha * f


def rgba(paint, alpha):
    return Image.fromarray(np.clip(np.rint(np.dstack([paint, alpha * 255])), 0, 255).astype(np.uint8), "RGBA")


def take(name):
    return np.asarray(Image.open(HERE / "originals" / f"{name}.png").convert("RGB")).astype(np.float32)


def light():
    a = take(LIGHT)
    h, w, _ = a.shape
    rows = (0, int(h * LIGHT_ROWS))
    ref, sky_rgb = plain_sky(a, rows, int(w * 0.03), int(w * 0.3), 12)
    part, lift = lifted(a, rows, ref)
    paint = paint_of(part, lift, sky_rgb)
    x0 = int(w * LIGHT_X)
    alpha = eased(lift[:, x0:], left=int(w * EASE), bottom=int(h * EASE))
    paint = paint[:, x0:]
    paint = np.concatenate([paint[PAD:0:-1], paint])
    alpha = np.concatenate([alpha[PAD:0:-1], alpha])
    return rgba(paint, alpha)


def glint():
    a = take(GLINT)
    h, w, _ = a.shape
    # The horizon: the sharpest step down the left columns, low in the picture.
    step = np.abs(np.diff(a[:, int(w * 0.05) : int(w * 0.4)].mean(axis=(1, 2))))
    horizon = int(np.argmax(step[int(h * 0.6) : int(h * 0.95)]) + h * 0.6)
    # The sun: the middle of the bare paper (all three channels high) in the sky.
    sky = a[: horizon - 6]
    ys, xs = np.nonzero((sky[..., 0] > 238) & (sky[..., 2] > 238))
    sun = int(round(xs.mean()))
    rows = (horizon + 2, min(h, horizon + int(h * SEA)))
    ref, sea_rgb = plain_sky(a, rows, int(w * 0.03), int(w * 0.25), 3)
    part, lift = lifted(a, rows, ref)
    paint = paint_of(part, lift, sea_rgb)
    x0, x1 = int(sun - w * REACH), int(min(w, sun + w * REACH))
    lift = np.clip(lift * STRONGER, 0, 1)
    alpha = eased(lift[:, x0:x1], left=int(w * 0.06), right=int(w * 0.06), bottom=int((rows[1] - rows[0]) * 0.35))
    img = rgba(paint[:, x0:x1], alpha)
    img = img.resize((img.width, round(img.height * SQUEEZE)), Image.LANCZOS)
    return img, sun - x0


def shipped(img, name):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"opening-sun{name}-{V}.webp"
    img.save(path, "WEBP", quality=QUALITY, method=6)
    print(f"{path.relative_to(REPO)}  {img.width}x{img.height}  {path.stat().st_size // 1024} KB")
    return {"src": f"{URL}/{path.name}", "width": img.width, "height": img.height}


def main():
    lit = light()
    sparkle, under = glint()
    art = {
        "light": {**shipped(lit, ""), "pad": PAD},
        "glint": {**shipped(sparkle, "-glint"), "sun": under},
    }
    head = [
        "// Generated by reference/ink-pages/nuricell/build_nuricell_sun.py. Do not edit by hand: change",
        "// the script and run it again. The sunshine in NuriCell's opening (Mo picked A, November 11,",
        "// 2026): `light`, the sun's warm light pouring in from beyond the window's top right corner",
        "// (its first `pad` rows are its own top, mirrored); `glint`, its sparkle on the sea under that",
        "// corner (`sun`, the column under the sun). Both are laid in the opening painting's blend group.",
        "",
    ]
    TS.write_text("\n".join(head) + f"export const nuricellSun = {json.dumps(art, indent=2)} as const;\n", encoding="utf-8", newline="\n")
    prettier = REPO / "node_modules/prettier/bin/prettier.cjs"
    subprocess.run(["node", str(prettier), "--write", str(TS)], cwd=REPO, check=True, capture_output=True)
    print(TS.relative_to(REPO), f"glint's sun at column {under} of {sparkle.width}")


if __name__ == "__main__":
    main()

"""Cut the California opening mockup pictures (October 28, 2026).

A scene (originals/<take>.png, 1536 x 1024, painted as the whole first screen) becomes the opening's
landscape layer: its paper divided out to white (the page multiplies it onto its own rice paper),
cut to the live landscape's shape (2400 x 1029) from the picture's foot, since the live landscape
box starts 30% down the opening. A crane take (an edit of the live crane's original) is lined up
on the live crane (ECC, so the brush line still leaves from under its trailing legs), its paper
turned to transparency, at the live cut-out's size (1600 x 1062).

    python -X utf8 reference/ink-pages/home-california/cut_california.py big-sur-1 sandhill-crane-1 ...

Output: plates/img/<take>.png (git-ignored).
"""

import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
OUT = HERE / "plates" / "img"
LIVE_CRANE = HERE.parents[2] / "reference" / "home-v2" / "ink" / "originals" / "gpt25-crane-paint-a.png"
LAND = (2400, 1029)
CRANE = (1600, 1062)


def divided(img, top=False):
    """Paper -> white, ink kept. The paper colour is the median of the picture's top tenth (a
    landscape) or of its outer frame (a bird on bare paper)."""
    arr = np.asarray(img.convert("RGB")).astype(np.float32)
    h, w, _ = arr.shape
    m = max(4, min(h, w) // 40)
    frame = arr[: h // 10].reshape(-1, 3) if top else np.concatenate(
        [arr[:m].reshape(-1, 3), arr[-m:].reshape(-1, 3), arr[:, :m].reshape(-1, 3), arr[:, -m:].reshape(-1, 3)]
    )
    paper = np.median(frame, axis=0)
    out = np.clip(arr / paper * 255.0, 0, 255)
    knee, white = 228.0, 246.0
    lum = out.min(axis=2, keepdims=True)
    lift = np.clip((lum - knee) / (white - knee), 0, 1)
    return out + (255.0 - out) * lift


def to_alpha(arr):
    """White to transparency: alpha from the darkest channel, colour un-mixed from white."""
    a = 1.0 - arr.min(axis=2, keepdims=True) / 255.0
    safe = np.where(a > 1e-3, a, 1.0)
    rgb = np.clip((arr - 255.0 * (1.0 - a)) / safe, 0, 255)
    return Image.fromarray(np.concatenate([rgb, a * 255.0], axis=2).astype(np.uint8), "RGBA")


# How each scene is framed in the live landscape's box: (top, x). The painting is cut from `top`
# (a fraction of its height) to its foot and scaled to the box's height; it starts `x` px into the
# 2400 px box ("right": its right edge on the box's), anything past the right edge is cut off.
# Chosen so the live sun (about 69% across at 1440, 74% at 1920) sits in open sky:
# - big-sur-1: its path of light on the water (57% across the painting) under the sun at 69%,
#   the bridge's far end still inside (97%); the horizon a little under the sun.
# - golden-hills-1: the far hills just under the sun, as the live ridges are.
# - yosemite-1: Half Dome under the sun (75%), El Capitan's top corner clear of it (86%).
FRAME = {
    "big-sur-1": (0.15, 621),
    "big-sur-2": (0.15, 621),
    "golden-hills-1": (0.25, "right"),
    "golden-hills-2": (0.25, "right"),
    "yosemite-1": (0.12, "right"),
    "yosemite-2": (0.05, "right"),
}
FEATHER = 0.28  # of the painting's width: its left edge fades into the paper
TOP_FADE = 90  # rows: the box's top edge dissolves, so no window shows it as a cut


def full(take):
    """D, the sequoias, is painted as the whole first screen: paper divided out, kept whole."""
    img = Image.open(HERE / "originals" / f"{take}.png")
    out = Image.fromarray(divided(img, top=True).astype(np.uint8), "RGB").resize((2400, 1600), Image.LANCZOS)
    out.save(OUT / f"{take}.png", optimize=True)
    print(take, "full screen", out.size)


def scene(take):
    if take.startswith("sequoia"):
        return full(take)
    img = Image.open(HERE / "originals" / f"{take}.png")
    arr = divided(img, top=True)
    w, h = img.size
    top, x = FRAME.get(take, (1 - w * LAND[1] / LAND[0] / h, 0))
    src = arr[round(top * h) :]
    width = round(src.shape[1] * LAND[1] / src.shape[0])
    src = np.asarray(Image.fromarray(src.astype(np.uint8), "RGB").resize((width, LAND[1]), Image.LANCZOS)).astype(np.float32)
    x = LAND[0] - width if x == "right" else x
    if x > 0:
        ramp = np.clip(np.arange(width) / (FEATHER * width), 0, 1)[None, :, None]
        src = 255.0 - (255.0 - src) * (ramp * ramp * (3 - 2 * ramp))
    canvas = np.full((LAND[1], LAND[0], 3), 255.0, np.float32)
    x0, s0 = max(0, x), max(0, -x)
    span = min(LAND[0] - x0, width - s0)
    canvas[:, x0 : x0 + span] = src[:, s0 : s0 + span]
    fade = np.clip(np.arange(LAND[1]) / TOP_FADE, 0, 1)[:, None, None]
    canvas = 255.0 - (255.0 - canvas) * fade
    out = Image.fromarray(canvas.astype(np.uint8), "RGB")
    out.save(OUT / f"{take}.png", optimize=True)
    print(take, "landscape", out.size, "top", top, "x", x, "width", width)


def gray(arr, size):
    g = cv2.cvtColor(cv2.resize(arr.astype(np.uint8), size, interpolation=cv2.INTER_AREA), cv2.COLOR_RGB2GRAY)
    return (255 - g).astype(np.float32) / 255.0


def crane(take):
    new = divided(Image.open(HERE / "originals" / f"{take}.png"))
    old = divided(Image.open(LIVE_CRANE))
    new = cv2.resize(new, CRANE, interpolation=cv2.INTER_AREA)
    old = cv2.resize(old, CRANE, interpolation=cv2.INTER_AREA)
    # Line the new bird up on the old one (affine ECC on ink density, at a quarter size).
    small = (CRANE[0] // 4, CRANE[1] // 4)
    warp = np.eye(2, 3, dtype=np.float32)
    try:
        _, warp = cv2.findTransformECC(
            gray(old, small), gray(new, small), warp, cv2.MOTION_AFFINE,
            (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6), None, 5,
        )
        warp[:, 2] *= 4
        new = cv2.warpAffine(new, warp, CRANE, flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP,
                             borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
    except cv2.error as err:
        print(take, "ECC failed, unaligned:", err)
    to_alpha(new.astype(np.float32)).save(OUT / f"{take}.png", optimize=True)
    print(take, "crane", CRANE, "warp", np.round(warp, 3).tolist())


def bird(take):
    """Another bird painted over the live crane's original, in its frame: no lining up (it is a
    different shape), just its paper turned to transparency at the live cut-out's size."""
    new = divided(Image.open(HERE / "originals" / f"{take}.png"))
    new = cv2.resize(new, CRANE, interpolation=cv2.INTER_AREA)
    to_alpha(new.astype(np.float32)).save(OUT / f"{take}.png", optimize=True)
    print(take, "bird", CRANE)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name in sys.argv[1:]:
        if name.startswith("sandhill"):
            crane(name)
        elif name.startswith(("hummingbird", "golden-eagle")):
            bird(name)
        else:
            scene(name)

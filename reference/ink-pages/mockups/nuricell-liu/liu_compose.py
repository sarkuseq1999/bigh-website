"""Stand Dr. Liu's real portrait painting (liu-v1.webp) in a Codex landscape (mockups only).

The landscape's paper is divided out, its edges fade into bare paper, the figure's solid mask
paints paper over the landscape where he stands, then the portrait multiplies on top. Output is a
plate on white paper, placed on the page with mix-blend-mode: multiply like every ink painting.

Usage: python liu_compose.py <spec.json>
spec: {"landscape", "portrait", "mask", "out", "canvas": [w, h],
       "land": {"width", "x", "y", "fade": {"left", "right", "top", "bottom"}, "sat"},
       "figure": {"width", "x", "y"}}
Fades are fractions of the canvas size. x/y are the top-left corners on the canvas.
"""

import json
import sys

import numpy as np
from PIL import Image


def divide_paper(rgb: np.ndarray) -> np.ndarray:
    """Divide out the landscape's paper colour (taken from its brightest, emptiest pixels)."""
    flat = rgb.reshape(-1, 3).astype(np.float32)
    lum = flat.mean(axis=1)
    paper = flat[lum >= np.percentile(lum, 90)].mean(axis=0)
    return np.clip(rgb.astype(np.float32) / paper * 255.0, 0, 255)


def saturate(rgb: np.ndarray, amount: float) -> np.ndarray:
    grey = rgb.mean(axis=2, keepdims=True)
    return np.clip(grey + (rgb - grey) * amount, 0, 255)


def ramp(n: int, length: int, reverse: bool = False) -> np.ndarray:
    """0 -> 1 over `length` px (smoothstep), then 1."""
    t = np.ones(n, np.float32)
    if length > 0:
        x = np.clip(np.arange(n, dtype=np.float32) / length, 0, 1)
        t = x * x * (3 - 2 * x)
    return t[::-1] if reverse else t


def main() -> None:
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    cw, ch = spec["canvas"]
    canvas = np.full((ch, cw, 3), 255.0, np.float32)

    land = spec["land"]
    img = Image.open(spec["landscape"]).convert("RGB")
    lw = int(land["width"])
    lh = round(img.height * lw / img.width)
    lrgb = divide_paper(np.asarray(img.resize((lw, lh), Image.LANCZOS)))
    lrgb = saturate(lrgb, land.get("sat", 1.0))
    link = 255.0 - lrgb
    link[link.max(axis=2) < 8] = 0  # the sky's faint paper grain is paper
    # The painting's own top edge always dissolves (its sky is never quite the paper's colour).
    link *= ramp(lh, int(land.get("own_top", 0.3) * lh))[:, None, None]
    # Paste the landscape (as ink amount, so it can be faded) onto the canvas.
    ink = np.zeros((ch, cw, 3), np.float32)
    x0, y0 = int(land["x"]), int(land["y"])
    sx0, sy0 = max(0, -x0), max(0, -y0)
    dx0, dy0 = max(0, x0), max(0, y0)
    w = min(lw - sx0, cw - dx0)
    h = min(lh - sy0, ch - dy0)
    ink[dy0 : dy0 + h, dx0 : dx0 + w] = link[sy0 : sy0 + h, sx0 : sx0 + w]
    fade = land.get("fade", {})
    fx = ramp(cw, int(fade.get("left", 0) * cw)) * ramp(cw, int(fade.get("right", 0) * cw), True)
    fy = ramp(ch, int(fade.get("top", 0) * ch)) * ramp(ch, int(fade.get("bottom", 0) * ch), True)
    ink *= (fy[:, None] * fx[None, :])[..., None]

    fig = spec["figure"]
    p = Image.open(spec["portrait"]).convert("RGB")
    m = Image.open(spec["mask"]).convert("L")
    pw = int(fig["width"])
    ph = round(p.height * pw / p.width)
    prgb = np.asarray(p.resize((pw, ph), Image.LANCZOS)).astype(np.float32)
    pm = np.asarray(m.resize((pw, ph), Image.LANCZOS)).astype(np.float32) / 255.0
    full_p = np.full((ch, cw, 3), 255.0, np.float32)
    full_m = np.zeros((ch, cw), np.float32)
    fx0, fy0 = int(fig["x"]), int(fig["y"])
    sx0, sy0 = max(0, -fx0), max(0, -fy0)
    dx0, dy0 = max(0, fx0), max(0, fy0)
    w = min(pw - sx0, cw - dx0)
    h = min(ph - sy0, ch - dy0)
    full_p[dy0 : dy0 + h, dx0 : dx0 + w] = prgb[sy0 : sy0 + h, sx0 : sx0 + w]
    full_m[dy0 : dy0 + h, dx0 : dx0 + w] = pm[sy0 : sy0 + h, sx0 : sx0 + w]
    # Optional: his painting dries out toward the canvas's foot (when it runs past the bottom edge).
    fb = int(fig.get("fade_bottom", 0) * ch)
    if fb:
        fy_fig = ramp(ch, fb, True)
        full_p = 255.0 - (255.0 - full_p) * fy_fig[:, None, None]
        full_m = full_m * fy_fig[:, None]

    # Where he stands the landscape gives way to paper; then his painting multiplies over it.
    ink *= (1.0 - full_m)[..., None]
    canvas = (255.0 - ink) * full_p / 255.0

    # Optional front layer (grass in front of his base), multiplied over everything.
    front = spec.get("front")
    if front:
        fimg = Image.open(front["path"]).convert("RGB")
        fw = int(front["width"])
        fh = round(fimg.height * fw / fimg.width)
        frgb = saturate(divide_paper(np.asarray(fimg.resize((fw, fh), Image.LANCZOS))), front.get("sat", 1.0))
        fink = 255.0 - frgb
        fink[fink.max(axis=2) < 8] = 0
        fink *= front.get("strength", 1.0)
        layer = np.zeros((ch, cw, 3), np.float32)
        x0, y0 = int(front["x"]), int(front["y"])
        sx0, sy0 = max(0, -x0), max(0, -y0)
        dx0, dy0 = max(0, x0), max(0, y0)
        w = min(fw - sx0, cw - dx0)
        h = min(fh - sy0, ch - dy0)
        layer[dy0 : dy0 + h, dx0 : dx0 + w] = fink[sy0 : sy0 + h, sx0 : sx0 + w]
        ff = front.get("fade", {})
        gx = ramp(cw, int(ff.get("left", 0) * cw)) * ramp(cw, int(ff.get("right", 0) * cw), True)
        gy = ramp(ch, int(ff.get("top", 0) * ch)) * ramp(ch, int(ff.get("bottom", 0) * ch), True)
        # A horizontal window: full strength between from/to (canvas fractions), fading over `soft`.
        if "from" in ff:
            xs = np.arange(cw, dtype=np.float32) / cw
            soft = ff.get("soft", 0.1)
            win = np.clip((xs - (ff["from"] - soft)) / soft, 0, 1) * np.clip(((ff.get("to", 1.0) + soft) - xs) / soft, 0, 1)
            gx = gx * win
        # Holes: [x0, x1] canvas fractions kept clear (his hands), softened by `soft`.
        for h0, h1 in ff.get("holes", []):
            xs = np.arange(cw, dtype=np.float32) / cw
            soft = ff.get("soft", 0.1)
            inside = np.clip((xs - (h0 - soft)) / soft, 0, 1) * np.clip(((h1 + soft) - xs) / soft, 0, 1)
            gx = gx * (1.0 - inside)
        layer *= (gy[:, None] * gx[None, :])[..., None]
        canvas = canvas * (255.0 - layer) / 255.0
    out = Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8))
    out.save(spec["out"], quality=92) if spec["out"].endswith(".webp") else out.save(spec["out"])
    print(spec["out"], out.size)


if __name__ == "__main__":
    main()

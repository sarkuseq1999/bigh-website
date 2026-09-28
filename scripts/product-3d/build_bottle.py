"""Rebuild a product bottle in 3D from its approved front photo.

Usage: python -X utf8 scripts/product-3d/build_bottle.py <slug>

Reads public/images/products/<slug>.png (transparent, front view) and writes:
  - public/images/products/3d/<slug>-label.webp: the printed label unwrapped off the curved
    bottle into a flat strip (front 140° from the photo, the unseen back continued from the
    label's own edge colours), with the photo's left-to-right shading evened out so the 3D
    lights can light it again;
  - src/components/product/bottles/<slug>.json: the bottle's outline (radius by height), where
    the cap, neck and label sit, all as fractions of the bottle's height.
The photo stays the only source of the label artwork; nothing is redrawn.
"""

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
ARC = np.radians(70)  # front half-angle taken from the photo
TEXTURE_W, TEXTURE_H = 2048, 640


def smooth1d(values, sigma):
    radius = int(sigma * 3)
    kernel = np.exp(-0.5 * (np.arange(-radius, radius + 1) / sigma) ** 2)
    kernel /= kernel.sum()
    padded = np.pad(values, radius, mode="edge")
    return np.convolve(padded, kernel, mode="valid")


def main(slug):
    source = ROOT / "public" / "images" / "products" / f"{slug}.png"
    rgba = np.asarray(Image.open(source).convert("RGBA")).astype(np.float32)
    alpha = rgba[..., 3]
    height, width = alpha.shape
    rows = np.where(alpha.max(axis=1) > 128)[0]
    top, bottom = int(rows[0]), int(rows[-1])

    # Outline: half-width and centre per row.
    half = np.zeros(height)
    centre = np.zeros(height)
    for y in range(top, bottom + 1):
        xs = np.where(alpha[y] > 128)[0]
        if len(xs):
            half[y] = (xs[-1] - xs[0] + 1) / 2
            centre[y] = (xs[0] + xs[-1]) / 2
    axis = float(np.median(centre[top : bottom + 1]))

    # Regions. The cap is the wide top block; the neck is the narrow band under it.
    body_radius = float(np.median(half[top + (bottom - top) // 2 : bottom - (bottom - top) // 6]))
    # Walk down from the top: the cap ends where the outline first narrows to the neck, and
    # the neck ends where it widens again into the shoulder.
    cap_radius = float(np.median(half[top + 20 : top + 150]))
    cap_bottom = next(y for y in range(top + 20, bottom) if half[y] < cap_radius * 0.9) - 1
    neck_top = next(y for y in range(cap_bottom + 1, bottom) if half[y] < cap_radius * 0.82)
    neck_radius = float(np.median(half[neck_top : neck_top + 12]))
    neck_bottom = next(y for y in range(neck_top, bottom) if half[y] > neck_radius * 1.04) - 1

    # The label: rows whose middle is strongly coloured (printed), between shoulder and base.
    rgb = rgba[..., :3]
    mx = rgb.max(axis=2)
    mn = rgb.min(axis=2)
    saturation = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
    band = saturation[:, int(axis) - 60 : int(axis) + 60].mean(axis=1)
    label_rows = [y for y in range(neck_bottom, bottom) if band[y] > 0.08]
    label_top, label_bottom = min(label_rows), max(label_rows)

    # Unwrap: texture column u ↔ angle θ around the axis (front at the middle).
    label_h = label_bottom - label_top + 1
    front_w = int(round(TEXTURE_W * (2 * ARC) / (2 * np.pi)))
    thetas = np.linspace(-ARC, ARC, front_w)
    front = np.zeros((label_h, front_w, 3), dtype=np.float32)
    for i, y in enumerate(range(label_top, label_bottom + 1)):
        r = half[y] - 1.5
        xs = np.clip(axis + r * np.sin(thetas), 0, width - 1)
        x0 = np.floor(xs).astype(int)
        x1 = np.minimum(x0 + 1, width - 1)
        t = (xs - x0)[:, None]
        front[i] = rgb[y, x0] * (1 - t) + rgb[y, x1] * t

    # Even out the photo's left-to-right shading (brighter middle, darker sides). Level to the
    # label's typical brightness, not its brightest column: the brightest is the studio glare in
    # the middle, and levelling up to it made the whole print paler than the photo (Mo, Sept 25).
    luminance = front @ np.array([0.2126, 0.7152, 0.0722])
    column = smooth1d(np.median(luminance, axis=0), sigma=front_w * 0.08)
    gain = (np.median(column) / np.maximum(column, 1)) ** 0.85
    front = np.clip(front * gain[None, :, None], 0, 255)

    # Full wrap: the front in the middle, the back continued from the front's edge colours.
    wrap = np.zeros((label_h, TEXTURE_W, 3), dtype=np.float32)
    start = (TEXTURE_W - front_w) // 2
    wrap[:, start : start + front_w] = front
    # Edge colours averaged over a wide strip and smoothed down the rows, so the continuation
    # reads as the label's plain background rather than streaks of its pattern.
    left_edge = front[:, :90].mean(axis=1)
    right_edge = front[:, -90:].mean(axis=1)
    for edge in (left_edge, right_edge):
        for channel in range(3):
            edge[:, channel] = smooth1d(edge[:, channel], sigma=10)
    back_w = TEXTURE_W - front_w
    for j in range(back_w):
        # Walk round the back from the right edge to the left edge.
        t = j / max(1, back_w - 1)
        column_colour = right_edge * (1 - t) + left_edge * t
        x = (start + front_w + j) % TEXTURE_W
        wrap[:, x] = column_colour
    image = Image.fromarray(wrap.astype(np.uint8)).resize((TEXTURE_W, TEXTURE_H), Image.LANCZOS)
    # Soften only the seam regions so the continuation has no hard edge.
    blurred = image.filter(ImageFilter.GaussianBlur(6))
    mask = np.zeros((TEXTURE_H, TEXTURE_W), dtype=np.float32)
    for edge in (start, start + front_w):
        for dx in range(-18, 19):
            x = (edge + dx) % TEXTURE_W
            mask[:, x] = np.maximum(mask[:, x], 1 - abs(dx) / 18)
    blend = np.asarray(image).astype(np.float32) * (1 - mask[..., None]) + np.asarray(blurred).astype(
        np.float32
    ) * mask[..., None]
    out_dir = ROOT / "public" / "images" / "products" / "3d"
    out_dir.mkdir(parents=True, exist_ok=True)
    Image.fromarray(blend.astype(np.uint8)).save(out_dir / f"{slug}-label.webp", quality=90, method=6)

    # Outline for the lathe, from the neck down to the base, as (height fraction, radius fraction).
    total = bottom - top
    fraction = lambda y: round((bottom - y) / total, 5)
    samples = list(range(neck_top, bottom + 1, 6)) + [bottom]
    profile = [[fraction(y), round(half[y] / total, 5)] for y in samples if half[y] > 0]
    data = {
        "slug": slug,
        "source": f"/images/products/{slug}.png",
        "label": f"/images/products/3d/{slug}-label.webp",
        "heightPx": total,
        "profile": profile,
        "cap": {
            "top": fraction(top),
            "bottom": fraction(cap_bottom),
            "radius": round(cap_radius / total, 5),
        },
        "neck": {"radius": round(neck_radius / total, 5), "top": fraction(neck_top)},
        "labelBand": {
            "top": fraction(label_top),
            "bottom": fraction(label_bottom),
            "radius": round(float(np.median(half[label_top:label_bottom])) / total, 5),
            "arc": round(float(np.degrees(ARC)), 1),
        },
    }
    json_dir = ROOT / "src" / "components" / "product" / "bottles"
    json_dir.mkdir(parents=True, exist_ok=True)
    (json_dir / f"{slug}.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(
        f"{slug}: bottle rows {top}-{bottom}, cap to {cap_bottom} (r {cap_radius:.0f}), "
        f"neck {neck_top}-{neck_bottom} (r {neck_radius:.0f}), label {label_top}-{label_bottom}, "
        f"body r {body_radius:.0f}, axis {axis:.1f}"
    )


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "nuricell")

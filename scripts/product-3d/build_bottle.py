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
ARC_GLASS = np.radians(62)  # narrower on glass bottles: see the unwrap
# A pale label (typical brightness above PALE) takes a little less of the studio's light, so its
# golds stay rich instead of washing toward white. 0.88 was picked against the Propolis photo
# (September 29, 2026; 1.0 read pale, 0.72 dull).
PALE, PALE_LABEL_LIGHT = 200, 0.88
TEXTURE_W, TEXTURE_H = 2048, 640


def smooth1d(values, sigma):
    radius = int(sigma * 3)
    kernel = np.exp(-0.5 * (np.arange(-radius, radius + 1) / sigma) ** 2)
    kernel /= kernel.sum()
    padded = np.pad(values, radius, mode="edge")
    return np.convolve(padded, kernel, mode="valid")


# Labels whose artwork runs off the photo's edge (a leaf, side lettering). See clean_edges.
STRAY_EDGE_ART = {"advanced-opc"}


def clean_edges(front, left_edge, right_edge):
    """Replace edge colours that are artwork, not the label's plain ground, in place.

    The ground is the edge pixels near the two strips' usual hue and colour strength. Where a row
    has enough of them and an edge strays from their colour, that edge takes the ground's colour,
    so a leaf or a word cut by the edge is not smeared round the whole back of the bottle."""
    strips = np.concatenate([front[:, :90], front[:, -90:]], axis=1) / 255
    top_c, low_c = strips.max(axis=2), strips.min(axis=2)
    chroma = top_c - low_c
    r, g, b = strips[..., 0], strips[..., 1], strips[..., 2]
    safe = np.maximum(chroma, 1e-6)
    sector = np.where(
        top_c == r, ((g - b) / safe) % 6, np.where(top_c == g, (b - r) / safe + 2, (r - g) / safe + 4)
    )
    hue = sector * (np.pi / 3)
    strength = chroma / np.maximum(top_c, 1e-6)
    usual = np.angle(np.sum(strength * np.exp(1j * hue)))
    plain = (np.abs(np.angle(np.exp(1j * (hue - usual)))) < np.radians(22)) & (
        strength > 0.5 * np.median(strength)
    )
    count = plain.sum(axis=1)
    ground = (strips * plain[..., None]).sum(axis=1) / np.maximum(count, 1)[:, None] * 255
    for edge in (left_edge, right_edge):
        stray = (count >= 40) & (np.abs(edge - ground).max(axis=1) > 24)
        edge[stray] = ground[stray]


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

    # The body: white plastic, or tinted glass (Green Bee Propolis is amber, September 29, 2026).
    # Glass is dark and strongly coloured where plastic is near white; its colour is the median of
    # the glass under the label, where the photo has no print and few reflections.
    rgb = rgba[..., :3]
    mx = rgb.max(axis=2)
    mn = rgb.min(axis=2)
    saturation = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
    luminance_map = rgb @ np.array([0.2126, 0.7152, 0.0722])
    base_rows = slice(bottom - (bottom - top) // 12, bottom - 4)
    base_mask = alpha[base_rows] > 250
    glass = (
        float(np.median(luminance_map[base_rows][base_mask])) < 110
        and float(np.median(saturation[base_rows][base_mask])) > 0.5
    )

    # The label: between shoulder and base, the rows whose middle is printed. On plastic that is
    # where the middle is strongly coloured; on coloured glass the glass is coloured too, so there
    # it is where the middle is bright.
    centre_band = slice(int(axis) - 60, int(axis) + 60)
    if glass:
        band = luminance_map[:, centre_band].mean(axis=1)
        label_rows = [y for y in range(neck_bottom, bottom) if band[y] > 120]
    else:
        band = saturation[:, centre_band].mean(axis=1)
        label_rows = [y for y in range(neck_bottom, bottom) if band[y] > 0.08]
    label_top, label_bottom = min(label_rows), max(label_rows)

    # Unwrap: texture column u ↔ angle θ around the axis (front at the middle). Propolis's label
    # has narrow side panels (badges, the facts box) squeezed into the photo's last few degrees;
    # on glass the front stops short of them, and the plain back continues from there.
    arc = ARC_GLASS if glass else ARC
    label_h = label_bottom - label_top + 1
    front_w = int(round(TEXTURE_W * (2 * arc) / (2 * np.pi)))
    thetas = np.linspace(-arc, arc, front_w)
    front = np.zeros((label_h, front_w, 3), dtype=np.float32)
    for i, y in enumerate(range(label_top, label_bottom + 1)):
        r = half[y] - 1.5
        xs = np.clip(axis + r * np.sin(thetas), 0, width - 1)
        x0 = np.floor(xs).astype(int)
        x1 = np.minimum(x0 + 1, width - 1)
        t = (xs - x0)[:, None]
        front[i] = rgb[y, x0] * (1 - t) + rgb[y, x1] * t

    if glass:
        # The photo looks down on the bottle a little, so the label's bottom edge curves up toward
        # the sides and the glass shows below it there. Against dark glass the edge is easy to
        # find: stretch each column so the label reaches the bottom of the strip, keeping the top.
        rows = np.arange(label_h, dtype=np.float32)
        front_luminance = front @ np.array([0.2126, 0.7152, 0.0722])
        lowest = label_h - label_h // 8
        for j in range(front_w):
            printed = np.where(front_luminance[lowest:, j] > 120)[0]
            edge = lowest + (printed[-1] if len(printed) else label_h - 1 - lowest)
            source_rows = rows * (edge / max(1, label_h - 1))
            for channel in range(3):
                front[:, j, channel] = np.interp(source_rows, rows, front[:, j, channel])

    # Even out the photo's left-to-right shading (brighter middle, darker sides). Level to the
    # label's typical brightness, not its brightest column: the brightest is the studio glare in
    # the middle, and levelling up to it made the whole print paler than the photo (Mo, Sept 25).
    luminance = front @ np.array([0.2126, 0.7152, 0.0722])
    pale = float(np.median(luminance)) > PALE
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
    # Artwork cut by an edge (Advanced OPC's grape leaf) would smear round the whole back. Only
    # for the labels listed, so the approved NuriCell label rebuilds exactly as before.
    if slug in STRAY_EDGE_ART:
        clean_edges(front, left_edge, right_edge)
    for edge in (left_edge, right_edge):
        for channel in range(3):
            edge[:, channel] = smooth1d(edge[:, channel], sigma=10)
    back_w = TEXTURE_W - front_w
    if glass:
        # Continue with the label's ground colour row by row (its cream between the gold borders),
        # easing in from the front's edges, so the unseen back reads as plain label. The ground is
        # the light end of each row (print and pattern are darker), so the lettering leaves no
        # stripes behind.
        typical = np.percentile(front, 80, axis=1)
        for channel in range(3):
            typical[:, channel] = smooth1d(typical[:, channel], sigma=3)
    for j in range(back_w):
        # Walk round the back from the right edge to the left edge.
        t = j / max(1, back_w - 1)
        column_colour = right_edge * (1 - t) + left_edge * t
        if glass:
            ease = np.exp(-min(j, back_w - 1 - j) / 60)
            column_colour = column_colour * ease + typical * (1 - ease)
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
            "arc": round(float(np.degrees(arc)), 1),
        },
    }
    if pale:
        data["labelLight"] = PALE_LABEL_LIGHT
    if glass:
        # Only glass bottles say so; plastic ones (NuriCell's file) stay as they were.
        glass_rgb = np.median(rgb[base_rows][base_mask], axis=0)
        data["glass"] = {"color": "#" + "".join(f"{int(round(v)):02x}" for v in glass_rgb)}
    json_dir = ROOT / "src" / "components" / "product" / "bottles"
    json_dir.mkdir(parents=True, exist_ok=True)
    (json_dir / f"{slug}.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(
        f"{slug}: bottle rows {top}-{bottom}, cap to {cap_bottom} (r {cap_radius:.0f}), "
        f"neck {neck_top}-{neck_bottom} (r {neck_radius:.0f}), label {label_top}-{label_bottom}, "
        f"body r {body_radius:.0f}, axis {axis:.1f}, {'glass' if glass else 'plastic'}, label median {np.median(luminance):.0f}"
    )


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "nuricell")

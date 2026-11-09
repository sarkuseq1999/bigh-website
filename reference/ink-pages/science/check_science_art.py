"""Checks the Science page's built pictures (round 3, November 4, 2026; spec
docs/superpowers/specs/2026-11-04-science-california-design.md).

- every picture named in science-art.ts exists at its stated size;
- each painting's outer 3px strip is white (254.5 or whiter), so nothing shows a box when it
  multiplies onto the page;
- the town: its six lamp layers are the town's own size, each clear (alpha 0) at its border and
  holding some gold, never one window in two layers, and all six over the town make its lit
  plate (plates/town-lit-<V>.png, lossless, not shipped); its phone pictures, unlit and lit, the
  same size as each other;
- Dr. Liu's path: three places, each with a phone cut, each wider than tall (a place beside its
  words, not a band) and at least 1000px wide for the page's 60% column.
Writes plates/contact.jpg (every picture, the town half lit) to look at.

usage: python -X utf8 reference/ink-pages/science/check_science_art.py
"""

import json
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
TS = REPO / "src/components/science/ink/science-art.ts"
results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f"  ({detail})" if detail else ""))


def art():
    text = TS.read_text(encoding="utf-8")
    body = text[text.index("= {") + 2 : text.rindex("} as const")] + "}"
    body = re.sub(r"(\w+):", r'"\1":', body)
    body = re.sub(r",(\s*[}\]])", r"\1", body)
    return json.loads(body)


def file_of(src):
    return REPO / "public" / src.lstrip("/")


def opened(entry, name):
    path = file_of(entry["src"])
    if not path.exists():
        check(f"{name}: exists", False, str(path))
        return None
    img = Image.open(path)
    check(f"{name}: {img.width}x{img.height} as stated", img.size == (entry["width"], entry["height"]), f"{img.size} vs {entry['width']}x{entry['height']}")
    return img


def edge_white(img, name):
    a = np.asarray(img.convert("RGB")).astype(np.float32)
    strip = np.concatenate([a[:3].reshape(-1, 3), a[-3:].reshape(-1, 3), a[:, :3].reshape(-1, 3), a[:, -3:].reshape(-1, 3)])
    check(f"{name}: outer 3px white", strip.mean() >= 254.5, f"{strip.mean():.2f}")


def painting(entry, name):
    img = opened(entry, name)
    if img is not None:
        edge_white(img, name)
    return img


def main():
    data = art()
    shown = []
    for key in ("desk", "journals", "picnic"):
        shown.append(painting(data[key], key))
        shown.append(painting(data[key]["phone"], f"{key} phone"))
    town = data["town"]
    base = painting(town, "town")
    # The lit town is a lossless plate the page never shows (build_science.py town()).
    lit_path = HERE / "plates" / f"town-lit-{town['src'].rsplit('-', 1)[1].split('.')[0]}.png"
    lit = Image.open(lit_path) if lit_path.exists() else None
    check("town: its lit plate", lit is not None and base is not None and lit.size == base.size, str(lit_path.name))
    phone = painting(town["phone"], "town phone")
    phone_lit = painting(town["phoneLit"], "town phone lit")
    if phone is not None and phone_lit is not None:
        check("town phone: unlit and lit the same size", phone.size == phone_lit.size, f"{phone.size} {phone_lit.size}")
    lamps = town["lamps"]
    check("town: six lamp layers", len(lamps) == 6, str(len(lamps)))
    alphas = []
    for i, src in enumerate(lamps):
        layer = Image.open(file_of(src)).convert("RGBA")
        check(f"town lamps {i + 1}: the town's size", base is not None and layer.size == base.size, f"{layer.size}")
        a = np.asarray(layer)[..., 3].astype(np.float32) / 255
        border = np.concatenate([a[:3].ravel(), a[-3:].ravel(), a[:, :3].ravel(), a[:, -3:].ravel()])
        check(f"town lamps {i + 1}: clear at its border", border.max() < 0.02, f"{border.max():.3f}")
        check(f"town lamps {i + 1}: holds some gold", (a > 0.5).mean() > 0.0015, f"{(a > 0.5).mean() * 100:.2f}%")
        alphas.append(a)
    if alphas and base is not None and lit is not None:
        stack = np.stack(alphas)
        check("town lamps: no window in two layers", ((stack > 0.5).sum(axis=0) > 1).mean() < 0.0005, f"{((stack > 0.5).sum(axis=0) > 1).mean() * 100:.3f}%")
        # All six layers laid over the town (as the page lays them) give the lit picture: the
        # town's own lossless plate, so the shipped webp's compression is not counted.
        plate = HERE / "plates" / Path(town["src"]).with_suffix(".png").name
        whole = (Image.open(plate) if plate.exists() else base).convert("RGBA")
        for src in lamps:
            whole.alpha_composite(Image.open(file_of(src)).convert("RGBA"))
        diff = np.abs(np.asarray(whole.convert("RGB")).astype(np.float32) - np.asarray(lit.convert("RGB")).astype(np.float32)).max(axis=2)
        check("town lamps: together they make the lit town", diff.mean() < 1.5 and np.percentile(diff, 99.9) < 40, f"mean {diff.mean():.2f}, 99.9% {np.percentile(diff, 99.9):.0f}")
    places = data["places"]
    check("path: three places", list(places) == ["berkeley", "salzburg", "today"], str(list(places)))
    for key, entry in places.items():
        img = painting(entry, f"place {key}")
        painting(entry["phone"], f"place {key} phone")
        if img is not None:
            check(f"place {key}: wider than tall", img.width > img.height, f"{img.size}")
            check(f"place {key}: at least 1000px wide", img.width >= 1000, f"{img.width}")
        shown.append(img)
    # The contact sheet: every painting, and the town half lit.
    if base is not None:
        half = base.convert("RGBA")
        for src in lamps[:3]:
            half.alpha_composite(Image.open(file_of(src)).convert("RGBA"))
        shown.insert(0, half.convert("RGB"))
    row_h, gap = 260, 16
    tiles = [im.convert("RGB").resize((round(im.width * row_h / im.height), row_h)) for im in shown if im is not None]
    width = max(1, sum(t.width for t in tiles[:4]) + gap * 3)
    rows = [tiles[i : i + 4] for i in range(0, len(tiles), 4)]
    sheet = Image.new("RGB", (max(sum(t.width for t in r) + gap * (len(r) - 1) for r in rows), len(rows) * (row_h + gap)), "white")
    for y, r in enumerate(rows):
        x = 0
        for t in r:
            sheet.paste(t, (x, y * (row_h + gap)))
            x += t.width + gap
    (HERE / "plates").mkdir(exist_ok=True)
    sheet.save(HERE / "plates/contact.jpg", quality=88)
    print(f"plates/contact.jpg  {sheet.width}x{sheet.height}  (width {width})")
    print(f"\n{sum(results)}/{len(results)} passed")
    return all(results)


if __name__ == "__main__":
    sys.exit(0 if main() else 1)

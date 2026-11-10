"""Checks the Science page's built pictures (round 3, November 4, 2026; spec
docs/superpowers/specs/2026-11-04-science-california-design.md).

- every picture named in science-art.ts exists at its stated size;
- each painting's outer 3px strip is white (254.5 or whiter), so nothing shows a box when it
  multiplies onto the page;
- the zoom opening (November 9, 2026): the hills and the hand are 3:2 and at least 1500px wide
  (they fill the window, so they keep their whole frame and need no white edge); the cell has a
  white edge like every other painting, is wider than tall, and holds gold (its mitochondria);
- Dr. Liu's path: three places, each with a phone cut, each wider than tall (a place beside its
  words, not a band) and at least 1000px wide for the page's 60% column.
Writes plates/contact.jpg (every picture) to look at.

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
    for key in ("journals", "picnic"):
        shown.append(painting(data[key], key))
        shown.append(painting(data[key]["phone"], f"{key} phone"))
    zoom = data["zoom"]
    check("zoom: four views, in the page's order", list(zoom) == ["inside", "cell", "hand", "hills"], str(list(zoom)))
    for key in ("hills", "hand", "inside"):
        img = opened(zoom[key], f"zoom {key}")
        if img is not None:
            check(f"zoom {key}: 3:2", abs(img.width / img.height - 1.5) < 0.01, f"{img.size}")
            check(f"zoom {key}: at least 1500px wide", img.width >= 1500, f"{img.width}")
        shown.insert(0, img)
    # The inside view ships without its gold, which rides above it in pieces (one picture).
    inside, sheet = shown[0], zoom["inside"]["gold"]
    if inside is not None:
        a = np.asarray(inside.convert("RGB")).astype(np.int32)
        gold = (a[..., 0] - a[..., 2] > 70) & (a[..., 1] - a[..., 2] > 40) & (a[..., 0] > 170)
        check("zoom inside: its gold is lifted off it", gold.mean() < 0.002, f"{gold.mean() * 100:.3f}%")
    pieces = Image.open(REPO / "public" / sheet["src"].lstrip("/"))
    check("zoom inside gold: the picture is as described", pieces.size == (sheet["width"], sheet["height"]) and pieces.mode == "RGBA", f"{pieces.size} {pieces.mode}")
    slivers = sheet["slivers"]
    check("zoom inside gold: thirty slivers or more", len(slivers) >= 30, str(len(slivers)))
    inside_frame = all(0 <= v <= 1 for s_ in slivers for v in s_["box"]) and all(s_["box"][0] + s_["box"][2] <= 1.001 and s_["box"][1] + s_["box"][3] <= 1.001 for s_ in slivers)
    check("zoom inside gold: every sliver inside the painting", inside_frame)
    in_sheet = all(s_["at"][0] + s_["at"][2] <= 1.001 and s_["at"][1] + s_["at"][3] <= 1.001 for s_ in slivers)
    check("zoom inside gold: every sliver inside its picture", in_sheet)
    b = np.asarray(pieces).astype(np.int32)
    solid = b[..., 3] > 128
    warm = (b[..., 0] - b[..., 2] > 60) & (b[..., 0] > 170)
    check("zoom inside gold: the pieces are gold", solid.mean() > 0.03 and (warm & solid).sum() / max(1, solid.sum()) > 0.6, f"{solid.mean() * 100:.1f}% solid, {(warm & solid).sum() / max(1, solid.sum()) * 100:.0f}% of it warm")
    cell = painting(zoom["cell"], "zoom cell")
    if cell is not None:
        check("zoom cell: wider than tall", cell.width > cell.height, f"{cell.size}")
        a = np.asarray(cell.convert("RGB")).astype(np.int32)
        gold = (a[..., 0] - a[..., 2] > 70) & (a[..., 1] - a[..., 2] > 40) & (a[..., 0] > 170)
        check("zoom cell: holds gold", gold.mean() > 0.01, f"{gold.mean() * 100:.2f}%")
    shown.insert(0, cell)
    places = data["places"]
    check("path: three places", list(places) == ["berkeley", "salzburg", "today"], str(list(places)))
    for key, entry in places.items():
        img = painting(entry, f"place {key}")
        painting(entry["phone"], f"place {key} phone")
        if img is not None:
            check(f"place {key}: wider than tall", img.width > img.height, f"{img.size}")
            check(f"place {key}: at least 1000px wide", img.width >= 1000, f"{img.width}")
        shown.append(img)
    # The contact sheet: every painting.
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

"""Checks the Science page's built pictures (spec docs/superpowers/specs/2026-10-14-science-ink-design.md).

- every picture named in science-art.ts exists at its stated size;
- each picture's outer 3px strip is white (254.5 or whiter), so nothing shows a box when it
  multiplies onto the page;
- (October 26) Dr. Liu's path: four places, each with a phone cut, each wider than tall (a place
  beside its words, not a band) and at least 1000px wide for the page's 60% column;
- the health scenes are three, each narrower than the strip;
- (Task 6) the mugs' steam is kept: ink above the mugs' rims, on the wide strip and the phone crop
  (the ink box once cut it off).
Writes plates/contact.jpg (the band with the places' cuts marked, the places, the strips, the
scenes) to look at.

usage: python -X utf8 reference/ink-pages/science/check_science_art.py
"""

import json
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

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


def picture(entry):
    path = REPO / "public" / entry["src"].lstrip("/")
    img = Image.open(path).convert("RGB")
    check(f"{entry['src']} size", img.size == (entry["width"], entry["height"]), f"{img.size}")
    a = np.asarray(img).astype(np.float32)
    edge = np.concatenate([a[:3].reshape(-1, 3), a[-3:].reshape(-1, 3), a[:, :3].reshape(-1, 3), a[:, -3:].reshape(-1, 3)])
    check(f"{entry['src']} white edge", edge.mean() >= 254.5, f"{edge.mean():.1f}")
    return img


data = art()
check("four places, in order", list(data["places"]) == ["okayama", "berkeley", "salzburg", "today"], str(list(data["places"])))
places = []
for key, entry in data["places"].items():
    wide = picture(entry)
    phone = picture(entry["phone"])
    check(f"place {key}: wider than tall", wide.width > 1.5 * wide.height and phone.width > 1.2 * phone.height,
          f"{wide.size} {phone.size}")
    check(f"place {key}: 1000px or wider", wide.width >= 1000, f"{wide.width}")
    places.append(wide)
for key in ("scrolls", "mugs"):
    picture(data[key])
    picture(data[key]["phone"])
for name, entry in (("wide", data["mugs"]), ("phone", data["mugs"]["phone"])):
    gray = np.asarray(Image.open(REPO / "public" / entry["src"].lstrip("/")).convert("L")).astype(np.float32)
    # The rows above the mugs: the first row where a column-run of dark ink (a mug's body) starts.
    body = int(np.argmax((gray < 120).mean(axis=1) > 0.02))
    steam = gray[: max(1, body - 10)]
    check(f"mugs {name}: the steam above the mugs is kept", body > gray.shape[0] * 0.2 and (steam < 225).sum() > 200,
          f"mugs start at row {body} of {gray.shape[0]}, {(steam < 225).sum()} ink pixels above them")
health = picture(data["health"])
scenes = [picture(s) for s in data["health"]["scenes"]]
check("three health scenes", len(scenes) == 3)
check("each scene narrower than the strip", all(s.width < health.width * 0.6 for s in scenes))

sheet_w = 2400
rows = []
band_plate = HERE / "plates/band.png"
if band_plate.exists():
    # The band with each place's wide cut (red) and phone cut (blue), from build_science.PLACES.
    sys.path.insert(0, str(HERE))
    from build_science import PLACES  # noqa: E402

    band = Image.open(band_plate).convert("RGB")
    k = sheet_w / band.width
    rows.append(band.resize((sheet_w, round(band.height * k))))
    draw = ImageDraw.Draw(rows[0])
    for wide, phone in PLACES.values():
        for (a, b, *_), colour, inset in ((wide, (200, 0, 0), 2), (phone, (0, 60, 200), 10)):
            draw.rectangle([round(a * k), inset, round(b * k) - 1, rows[0].height - 1 - inset], outline=colour, width=3)
row = Image.new("RGB", (sheet_w, max(round(p.height * (sheet_w / 4 - 20) / p.width) for p in places)), "white")
x = 0
for p in places:
    small = p.resize((sheet_w // 4 - 20, round(p.height * (sheet_w / 4 - 20) / p.width)))
    row.paste(small, (x, 0))
    x += sheet_w // 4
rows.append(row)
for img in (Image.open(REPO / "public" / data[k]["src"].lstrip("/")) for k in ("scrolls", "health", "mugs")):
    rows.append(img.convert("RGB").resize((sheet_w // 2, round(img.height * (sheet_w // 2) / img.width))))
rows.append(Image.new("RGB", (sheet_w, max(s.height for s in scenes) // 2), "white"))
x = 0
for s in scenes:
    small = s.resize((s.width // 2, s.height // 2))
    rows[-1].paste(small, (x, 0))
    x += small.width + 40
sheet = Image.new("RGB", (sheet_w, sum(r.height + 30 for r in rows)), "white")
y = 0
for r in rows:
    sheet.paste(r, (0, y))
    y += r.height + 30
(HERE / "plates").mkdir(exist_ok=True)
sheet.save(HERE / "plates/contact.jpg", quality=85)
print("contact sheet: reference/ink-pages/science/plates/contact.jpg")
print("ALL PASS" if all(results) else f"{results.count(False)} FAILED")
sys.exit(0 if all(results) else 1)

"""Check the B and C paintings (build_bc.py): every picture about-art.ts names exists at its
stated size; ink pictures are pure white to their edges (no box on the page); gold masks cover a
small, real share; the enso's dot is a cut-out and its start angle is a real angle; the desk has
no gold; four dots, deep to pale.

usage: python -X utf8 reference/ink-pages/about-bc/check_bc.py   (exit 0 when all pass)
"""

import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[3]
TS = (REPO / "src/components/about/about-art.ts").read_text(encoding="utf-8")
sys.path.insert(0, str(REPO / "reference/ink-pages/about"))
from build_about import gold_pixels  # noqa: E402

results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"{'PASS' if ok else 'FAIL'} {name}{(' — ' + str(detail)) if detail and not ok else ''}")


def file_of(src):
    return REPO / "public" / src.lstrip("/")


# Prettier unquotes the generated object's keys, so a key may or may not be in quotes.
srcs = set(re.findall(r'"(/images/about-bc/[^"]+)"', TS))
check("about-art.ts names pictures", len(srcs) >= 20, len(srcs))
missing = sorted(s for s in srcs if not file_of(s).exists())
check("every picture about-art.ts names exists", not missing, missing)
for src, w, h in re.findall(r'"?src"?:\s*"([^"]+)",\s*"?width"?:\s*(\d+),\s*"?height"?:\s*(\d+)', TS):
    if file_of(src).exists():
        size = Image.open(file_of(src)).size
        check(f"{src} is {w}x{h}", size == (int(w), int(h)), size)

for name in ["book", "seedling", "desk", "sequoia", "palms", "bee", "moon", "letter", "lamp", "enso", "hills", "glasses"]:
    p = REPO / f"public/images/about-bc/{name}-v1.webp"
    if p.exists():
        a = np.asarray(Image.open(p).convert("L")).astype(int)
        strip = np.concatenate([a[:3].ravel(), a[-3:].ravel(), a[:, :3].ravel(), a[:, -3:].ravel()])
        check(f"{name}: white to its edge (outer 3px mean ≥ 254.5, < 1% under 235)", strip.mean() >= 254.5 and (strip < 235).mean() < 0.01, [round(strip.mean(), 2), round((strip < 235).mean(), 4)])

for name in ["book", "seedling", "sequoia", "lamp"]:
    p = REPO / f"public/images/about-bc/{name}-v1-gold.webp"
    if p.exists():
        cover = (np.asarray(Image.open(p).convert("RGBA"))[..., 3] > 128).mean()
        check(f"{name}: a gold light mask (0.05%-15% of the picture)", 0.0005 <= cover <= 0.15, round(cover, 4))
    else:
        check(f"{name}: gold mask exists", False, p.name)

desk = REPO / "public/images/about-bc/desk-v1.webp"
if desk.exists():
    check("desk: no gold leaf", gold_pixels(np.asarray(Image.open(desk).convert("RGB"))).mean() < 0.0005)

dot = REPO / "public/images/about-bc/enso-dot-v1.webp"
if dot.exists():
    alpha = np.asarray(Image.open(dot).convert("RGBA"))[..., 3]
    check("enso dot: a gold cut-out with transparency", (alpha < 20).mean() > 0.2 and (alpha > 200).mean() > 0.05)
m = re.search(r'"?startDeg"?:\s*([\d.]+)', TS)
check("enso: a start angle in [0, 360)", bool(m) and 0 <= float(m.group(1)) < 360, m.group(1) if m else None)

tones = []
for k in range(1, 5):
    p = REPO / f"public/images/about-bc/dot-{k}-v1.webp"
    if p.exists():
        tones.append(np.percentile(np.asarray(Image.open(p).convert("L")).astype(int), 5))
check("four dots, deep to pale", len(tones) == 4 and all(x < y for x, y in zip(tones, tones[1:])), tones)

print(f"\n{sum(results)}/{len(results)} passed")
sys.exit(0 if all(results) else 1)

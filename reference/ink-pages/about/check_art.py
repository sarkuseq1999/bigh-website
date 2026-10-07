"""Check the About page's built paintings (build_about.py): every picture letter-art.ts names
exists at its stated size; ink pictures have white paper at their corners (they multiply);
the gold dots are cut-outs with real transparency; the word and the i keep no gold in their ink
picture (the dot is its own picture); the rings' gold mask covers a thin ring; four dots, deep
to pale; the letters are sharp enough for their largest size on a 2x screen.

usage: python -X utf8 reference/ink-pages/about/check_art.py   (exit 0 when all pass)
"""

import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[3]
TS = (REPO / "src/components/about/letter-art.ts").read_text(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_about import gold_pixels  # noqa: E402

results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"{'PASS' if ok else 'FAIL'} {name}{(' — ' + str(detail)) if detail and not ok else ''}")


def file_of(src):
    return REPO / "public" / src.lstrip("/")


# Prettier unquotes the generated object's keys, so a key may or may not be in quotes.
srcs = re.findall(r'"?src"?:\s*"([^"]+)"', TS) + re.findall(r'"(/images/about-ink/[^"]+)"', TS)
missing = sorted({s for s in srcs if not file_of(s).exists()})
check("every picture letter-art.ts names exists", not missing, missing)

for src, w, h in re.findall(r'"?src"?:\s*"([^"]+)",\s*"?width"?:\s*(\d+),\s*"?height"?:\s*(\d+)', TS):
    if file_of(src).exists():
        size = Image.open(file_of(src)).size
        check(f"{src} is {w}x{h}", size == (int(w), int(h)), size)

for name in ["word", "letter-b", "letter-i", "letter-g", "letter-h", "band", "pool", "rings", "dot-1", "dot-4"]:
    p = REPO / f"public/images/about-ink/{name}-v1.webp"
    if p.exists():
        a = np.asarray(Image.open(p).convert("RGB")).astype(int)
        corners = [a[:8, :8], a[:8, -8:], a[-8:, :8], a[-8:, -8:]]
        check(f"{name}: paper divided out (corners white)", min(c.mean() for c in corners) >= 248, [round(c.mean()) for c in corners])

# No box on the page: a picture's paper must be white right up to its edge, or the box multiplies
# onto the page a shade darker than the paper around it (Task 3 review: the outer strips averaged
# about 252). Every ink picture, not the gold cut-outs.
INK = ["word", "letter-b", "letter-i", "letter-g", "letter-h", "band", "pool", "rings", "dot-1", "dot-2", "dot-3", "dot-4"]
for name in INK:
    p = REPO / f"public/images/about-ink/{name}-v1.webp"
    if p.exists():
        a = np.asarray(Image.open(p).convert("L")).astype(float)
        strip = np.concatenate([a[:3].ravel(), a[-3:].ravel(), a[:, :3].ravel(), a[:, -3:].ravel()])
        mean, dark = strip.mean(), (strip < 235).mean()
        check(f"{name}: white to its edge (outer 3px mean 254.5+, under 1% below 235)", mean >= 254.5 and dark < 0.01, [round(float(mean), 2), f"{dark:.2%}"])

for name in ["word-dot", "letter-i-dot"]:
    p = REPO / f"public/images/about-ink/{name}-v1.webp"
    if p.exists():
        alpha = np.asarray(Image.open(p).convert("RGBA"))[..., 3]
        check(f"{name}: a gold cut-out with transparency", (alpha < 20).mean() > 0.2 and (alpha > 200).mean() > 0.05, [round((alpha < 20).mean(), 2), round((alpha > 200).mean(), 2)])

for name in ["word", "letter-i"]:
    p = REPO / f"public/images/about-ink/{name}-v1.webp"
    if p.exists():
        left = gold_pixels(np.asarray(Image.open(p).convert("RGB"))).mean()
        check(f"{name}: no gold left in the ink picture", left < 0.0002, left)

gold = REPO / "public/images/about-ink/rings-v1-gold.webp"
if gold.exists():
    cover = (np.asarray(Image.open(gold).convert("RGBA"))[..., 3] > 128).mean()
    check("rings: the gold mask is a thin ring (0.3%-12% of the picture)", 0.003 <= cover <= 0.12, round(cover, 4))

tones = []
for k in range(1, 5):
    p = REPO / f"public/images/about-ink/dot-{k}-v1.webp"
    if p.exists():
        a = np.asarray(Image.open(p).convert("L")).astype(int)
        tones.append(np.percentile(a, 5))
check("four dots, deep to pale", len(tones) == 4 and all(x < y for x, y in zip(tones, tones[1:])), tones)

for name, least in [("letter-b", 520), ("letter-i", 520), ("letter-g", 520), ("letter-h", 640)]:
    p = REPO / f"public/images/about-ink/{name}-v1.webp"
    if p.exists():
        check(f"{name}: at least {least}px tall (sharp on a 2x screen)", Image.open(p).height >= least, Image.open(p).size)

print(f"\n{sum(results)}/{len(results)} passed")
sys.exit(0 if all(results) else 1)

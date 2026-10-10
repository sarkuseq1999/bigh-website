"""Checks on NuriCell's built paintings (run after build_nuricell.py).

usage: python -X utf8 reference/ink-pages/nuricell/check_nuricell_art.py
"""
import json
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[3]
TS = REPO / "src/components/product/ink/nuricell-art.ts"
fails = []


def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f"  ({detail})" if detail else ""))
    if not ok:
        fails.append(name)


def pixels(src):
    return np.asarray(Image.open(REPO / "public" / src.lstrip("/")).convert("RGB")).astype(np.float32)


if not TS.exists():
    sys.exit("FAIL nuricell-art.ts missing: run build_nuricell.py")
text = TS.read_text(encoding="utf-8")
# The file is Prettier's TypeScript: unquoted keys and trailing commas. Make it JSON again.
body = re.search(r"nuricellArt = (\{.*\}) as const", text, re.S).group(1)
body = re.sub(r"(?m)^(\s*)([A-Za-z_]\w*):", r'\1"\2":', body)
body = re.sub(r",(\s*[}\]])", r"\1", body)
art = json.loads(body)

for key, entry in art.items():
    arr = pixels(entry["src"])
    h, w = arr.shape[:2]
    check(f"{key}: size as listed", (w, h) == (entry["width"], entry["height"]), f"{w}x{h}")
    rim = np.concatenate([arr[:3].reshape(-1, 3), arr[-3:].reshape(-1, 3), arr[:, :3].reshape(-1, 3), arr[:, -3:].reshape(-1, 3)])
    check(f"{key}: white rim (no box on the page)", rim.mean() >= 254.0, f"{rim.mean():.1f}")
    if "gold" in entry:
        mask = np.asarray(Image.open(REPO / "public" / entry["gold"].lstrip("/")).split()[-1])
        share = float((mask > 128).mean())
        check(f"{key}: gold mask covers its leaf", 0.001 <= share <= 0.35, f"{share:.2%}")

check("lantern: lit and unlit the same size", (art["lanternLit"]["width"], art["lanternLit"]["height"]) == (art["lanternUnlit"]["width"], art["lanternUnlit"]["height"]))
lit, unlit = pixels(art["lanternLit"]["src"]), pixels(art["lanternUnlit"]["src"])
# Registered: the dark outlines (rims, cord) sit in the same place; compare edge maps.
def edges(a):
    g = a.mean(axis=2)
    return (np.abs(np.diff(g, axis=0))[:, :-1] + np.abs(np.diff(g, axis=1))[:-1]) > 40
e1, e2 = edges(lit), edges(unlit)
overlap = (e1 & e2).sum() / max(1, min(e1.sum(), e2.sum()))
check("lantern: lit and unlit in register", overlap > 0.35, f"edge overlap {overlap:.2f}")
warm = lambda a: float(((a[..., 0] - a[..., 2]) > 40).mean())
check("lantern: the unlit one has no gold", warm(unlit) < 0.002, f"{warm(unlit):.3%}")
check("lantern: the lit one glows", warm(lit) > 0.03, f"{warm(lit):.2%}")
# Lit from within: across the middle of the body, the centre is clearly lighter than the body's
# sides. Either by a lot (70+ levels: core-v1 95, core-v2 80), or by 30+ with the sides still pale,
# unsaturated paper, as in Mo's comp (2-why-lantern.jpg: centre about 237, sides about 200-205,
# +35; the painted lit-v3: +41, sides 209). The plain lit-v2 take (gold rim to rim: +49, its sides
# saturated gold, (R-B)/R 0.52) fails both.
H = lit.shape[0]
band_lit, band_unlit = lit[int(H * 0.4) : int(H * 0.6)], unlit[int(H * 0.4) : int(H * 0.6)]
cols = np.where((band_unlit.min(axis=2) < 236).mean(axis=0) > 0.5)[0]
x0, x1 = cols.min(), cols.max()
span = x1 - x0
lum = lambda a: (a @ np.array([0.299, 0.587, 0.114], np.float32)).mean()
centre = lum(band_lit[:, x0 + int(span * 0.4) : x0 + int(span * 0.6)])
sides = (lum(band_lit[:, x0 + int(span * 0.04) : x0 + int(span * 0.16)]) + lum(band_lit[:, x1 - int(span * 0.16) : x1 - int(span * 0.04)])) / 2
side_rgb = np.concatenate(
    [band_lit[:, x0 + int(span * 0.04) : x0 + int(span * 0.16)].reshape(-1, 3), band_lit[:, x1 - int(span * 0.16) : x1 - int(span * 0.04)].reshape(-1, 3)]
).mean(axis=0)
pale_sides = sides >= 190 and (side_rgb[0] - side_rgb[2]) / side_rgb[0] <= 0.35
check(
    "lantern: lit from within (centre lighter than the sides)",
    centre > sides + 70 or (centre > sides + 30 and pale_sides),
    f"centre {centre:.0f}, sides {sides:.0f}, pale sides {pale_sides}",
)

# Sides not olive (rounds 2-3): the body's side bands, across its middle, average either a warm
# amber (G/R at most 0.86, B/R at most 0.68, R - B at least 45: core-v2 197/155/98) or pale paper
# (luminance 190+, (R - B)/R at most 0.35: the painted lit-v3 230/206/169, and Mo's comp's sides,
# about 233/202/151). Olive is a dull, darker yellow: round 1's core-v1 (173, 151, 107: luminance
# 154, G/R 0.87) fails both. (The comp's own sides are G/R 0.86-0.87, so hue ratios alone cannot
# tell olive from the comp.)
def side_colour(a):
    band = a[int(H * 0.4) : int(H * 0.6)]
    sides = np.concatenate(
        [band[:, x0 + int(span * 0.04) : x0 + int(span * 0.16)].reshape(-1, 3), band[:, x1 - int(span * 0.16) : x1 - int(span * 0.04)].reshape(-1, 3)]
    )
    return sides.mean(axis=0)


r_, g_, b_ = side_colour(lit)
amber = g_ / r_ <= 0.86 and b_ / r_ <= 0.68 and r_ - b_ >= 45
pale = 0.299 * r_ + 0.587 * g_ + 0.114 * b_ >= 190 and (r_ - b_) / r_ <= 0.35
check(
    "lantern: its sides warm amber or pale paper, not olive",
    amber or pale,
    f"({r_:.0f}, {g_:.0f}, {b_:.0f}): G/R {g_ / r_:.2f}, B/R {b_ / r_:.2f}, R-B {r_ - b_:.0f}, amber {amber}, pale {pale}",
)
# The lit lantern's gold mask covers a few flecks, not the whole warm body.
flecks = np.asarray(Image.open(REPO / "public" / art["lanternLit"]["gold"].lstrip("/")).split()[-1])
fleck_share = float((flecks > 128).mean())
check("lantern: its gold mask is a few flecks, not the body", 0.0005 <= fleck_share <= 0.02, f"{fleck_share:.2%}")

liu = pixels(art["liu"]["src"])
hi, lo = liu.max(axis=2), liu.min(axis=2)
sat = (hi - lo) / np.maximum(hi, 1)
skin = (sat > 0.12) & (hi > 120)
check("liu: in colour, never black-and-white", skin.mean() > 0.03, f"coloured pixels {skin.mean():.1%}")
books = pixels(art["books"]["src"])
check("books: no gold", warm(books) < 0.001, f"{warm(books):.3%}")
stroke = pixels(art["stroke"]["src"])
check("stroke: no gold", warm(stroke) < 0.001, f"{warm(stroke):.3%}")

c = art["sum"]["centres"]
check("sum: numbers 3, 30, 90", art["sum"]["numbers"] == [3, 30, 90])
check("sum: three centres left to right, apart", len(c) == 3 and c[0] < c[1] < c[2] and min(c[1] - c[0], c[2] - c[1]) > 0.15, str(c))

print("ALL PASS" if not fails else f"{len(fails)} FAIL")
sys.exit(1 if fails else 0)

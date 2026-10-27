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
    """The picture as it draws on white: a clear-ground picture (the capsule pair) laid on white
    first, so its rim test reads what the page would show."""
    img = Image.open(REPO / "public" / src.lstrip("/"))
    if img.mode in ("RGBA", "LA"):
        img = Image.alpha_composite(Image.new("RGBA", img.size, (255, 255, 255, 255)), img.convert("RGBA"))
    return np.asarray(img.convert("RGB")).astype(np.float32)


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
    # The lighthouse's lamp is a small light far off: its own check is below.
    if "gold" in entry and key != "lanternLit":
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
# The lighthouse (October 26, 2026; the Gold Rush lantern's own checks went with it): its light is
# the lamp room's glow and the beam's wash over the sky. The light: the lit picture's light pixels
# (darkest channel 190+) that are warm (red over blue by 10+), the test build_nuricell.py's
# glow_mask starts from. Lit, the light is warm; unlit, the same pixels are grey sky and glass.
light = ((lit[..., 0] - lit[..., 2]) > 10) & (lit.min(axis=2) > 190)
check("lantern: the lit one has a light", 0.03 <= light.mean() <= 0.3, f"{light.mean():.2%} of the picture")
glow = lambda a: float((a[..., 0] - a[..., 2])[light].mean())
check("lantern: its light warm lit, grey unlit", glow(lit) >= glow(unlit) + 12, f"{glow(unlit):.1f} -> {glow(lit):.1f}")
# The lamp room itself (around the gold mask's leaf) lit warmer than unlit: the light is not only
# a wash over the sky.
flecks = np.asarray(Image.open(REPO / "public" / art["lanternLit"]["gold"].lstrip("/")).split()[-1])
fy, fx = np.nonzero(flecks > 128)
k = lit.shape[1] / flecks.shape[1]
room = (slice(int(fy.min() * k), int(fy.max() * k) + 1), slice(int(fx.min() * k), int(fx.max() * k) + 1))
lamp = lambda a: float((a[room][..., 0] - a[room][..., 2]).mean())
check("lantern: its lamp room warm lit, grey unlit", lamp(lit) >= lamp(unlit) + 20, f"{lamp(unlit):.1f} -> {lamp(lit):.1f}")
# The sky over the unlit lighthouse is white paper where the beam was (no grey ghost of the beam).
H, W = lit.shape[:2]
sky = unlit[: int(fy.min() * k), : int(fx.min() * k)]
check("lantern: the sky where the beam was stays pale unlit", sky.mean() >= 240.0, f"{sky.mean():.1f}")
# The lit lighthouse's gold mask covers its lamp's leaf, not the beam or the glow round it.
fleck_share = float((flecks > 128).mean())
check("lantern: its gold mask is the lamp, not the glow", 0.0005 <= fleck_share <= 0.02, f"{fleck_share:.2%}")

liu = pixels(art["liu"]["src"])
hi, lo = liu.max(axis=2), liu.min(axis=2)
sat = (hi - lo) / np.maximum(hi, 1)
skin = (sat > 0.12) & (hi > 120)
check("liu: in colour, never black-and-white", skin.mean() > 0.03, f"coloured pixels {skin.mean():.1%}")
books = pixels(art["books"]["src"])
check("books: no gold", warm(books) < 0.001, f"{warm(books):.3%}")
stroke = pixels(art["stroke"]["src"])
check("stroke: no gold", warm(stroke) < 0.001, f"{warm(stroke):.3%}")

# Only shipped pictures under public/ (the build writes nothing else; spares live in
# reference/ink-pages/nuricell/spares/).
listed = {Path(v).name for entry in art.values() for k, v in entry.items() if k in ("src", "gold")}
# What's inside's moving gold and heaps (build_nuricell_gold.py, October 26, 2026) ship here too.
gold_ts = (REPO / "src/components/product/ink/nuricell-gold.ts").read_text(encoding="utf-8")
listed |= set(re.findall(r"/images/products/nuricell/ink/([\w.-]+\.webp)", gold_ts))
folder = REPO / "public" / art["books"]["src"].lstrip("/").rsplit("/", 1)[0]
extra = sorted(f.name for f in folder.iterdir() if f.is_file() and f.name not in listed)
check("public: only the shipped pictures", not extra, ", ".join(extra) or f"{len(listed)} files")

c = art["sum"]["centres"]
check("sum: numbers 3, 30, 90", art["sum"]["numbers"] == [3, 30, 90])
check("sum: three centres left to right, apart", len(c) == 3 and c[0] < c[1] < c[2] and min(c[1] - c[0], c[2] - c[1]) > 0.15, str(c))

print("ALL PASS" if not fails else f"{len(fails)} FAIL")
sys.exit(1 if fails else 0)

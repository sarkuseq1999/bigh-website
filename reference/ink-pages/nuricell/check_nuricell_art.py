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
# The Gold Rush lantern (October 26, 2026; the paper lantern's own checks went with it): its glass
# is where the light is. The glass: the lit picture's light pixels (darkest channel 190+) that are
# warm (red over blue by 10+), the test build_nuricell.py's glow_mask starts from. Lit, it glows
# (measured 0.12 of the picture, warmth 26 lit, 8 unlit, the unlit glass in the tin's warm grey).
glass = ((lit[..., 0] - lit[..., 2]) > 10) & (lit.min(axis=2) > 190)
check("lantern: the lit one has a glowing glass", 0.05 <= glass.mean() <= 0.3, f"{glass.mean():.2%} of the picture")
glow = lambda a: float((a[..., 0] - a[..., 2])[glass].mean())
check("lantern: its glass warm lit, grey unlit", glow(lit) >= glow(unlit) + 12, f"{glow(unlit):.1f} -> {glow(lit):.1f}")
# The paper round the unlit lantern is white across its middle (no grey halo, no box on the page).
H = lit.shape[0]
beside = []
for row in unlit[int(H * 0.3) : int(H * 0.7) : 4]:
    ink = np.where(row.min(axis=1) < 236)[0]
    beside.append(np.concatenate([row[max(0, ink.min() - 40) : max(0, ink.min() - 8)], row[ink.max() + 8 : ink.max() + 40]]))
beside = np.concatenate(beside)
check("lantern: the paper beside the unlit one stays white", beside.mean() >= 254.0, f"{beside.mean():.1f}")
# The lit lantern's gold mask covers its flame's leaf, not the glow round it.
flecks = np.asarray(Image.open(REPO / "public" / art["lanternLit"]["gold"].lstrip("/")).split()[-1])
fleck_share = float((flecks > 128).mean())
check("lantern: its gold mask is the flame, not the glow", 0.0005 <= fleck_share <= 0.02, f"{fleck_share:.2%}")

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

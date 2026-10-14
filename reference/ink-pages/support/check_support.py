"""Check the Support page's built paintings (run after build_support.py).

usage: python -X utf8 reference/ink-pages/support/check_support.py
"""

import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "reference/ink-pages/about"))
import build_about as bd  # noqa: E402

OUT = REPO / "public/images/support"
TS = REPO / "src/components/support/support-art.ts"
fails = []


def leaf_gold(arr):
    """Gold LEAF: bd.gold_pixels, and bright and rich. bd.gold_pixels alone also matches the warm
    browns of the parcel's kraft paper and its oak leaf (1316 px, brightness p50 0.43, colour about
    161,134,110), which are ink on this page, not gold. The steam's leaf is 0.71-0.97 bright and
    saturation 0.43 at the median (the porch original, measured); the parcel's tan has none that is
    both over 0.55 bright and over 0.40 saturated, and 76% of the steam's leaf pixels are."""
    a = arr.astype(np.float32) / 255
    hi, lo = a.max(axis=2), a.min(axis=2)
    return bd.gold_pixels(arr) & (hi > 0.55) & ((hi - lo) / np.maximum(hi, 1e-4) > 0.40)


def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'} {name}{(' - ' + str(detail)) if detail and not ok else ''}")
    if not ok:
        fails.append(name)


names = ["porch", "porch-steam", "cup", "mailbox", "parcel", "book"]
for n in names:
    check(f"{n}-v1.webp exists", (OUT / f"{n}-v1.webp").exists())
if not fails:
    for n in ["porch", "cup", "mailbox", "parcel", "book"]:
        arr = np.asarray(Image.open(OUT / f"{n}-v1.webp").convert("RGB"))
        edge = np.concatenate([arr[0], arr[-1], arr[:, 0], arr[:, -1]])
        check(f"{n}: its edge is white paper (multiplies with no box)", edge.min() >= 238, int(edge.min()))
        gold = int(leaf_gold(arr).sum())
        check(f"{n}: no gold left in the ink plate", gold < 40, gold)
    for n in ["porch-steam"]:
        img = Image.open(OUT / f"{n}-v1.webp")
        check(f"{n}: has transparency", img.mode == "RGBA")
        rgba = np.asarray(img.convert("RGBA"))
        shown = rgba[..., 3] > 128
        check(f"{n}: holds gold leaf", shown.sum() > 400 and bd.gold_pixels(rgba[..., :3])[shown].mean() > 0.3,
              int(shown.sum()))
    ts = TS.read_text(encoding="utf-8")
    for n in ["porch", "cup", "mailbox", "parcel", "book"]:
        check(f"support-art.ts exports {n}", re.search(rf"export const {n} = ", ts) is not None)
    # Prettier unquotes the keys (quoteProps "as-needed"), so look for `steam: {`.
    check("support-art.ts places the steam on the porch and the cup", len(re.findall(r"\bsteam: \{", ts)) == 2)
print(f"\n{'ALL PASS' if not fails else f'{len(fails)} FAILED'}")
sys.exit(1 if fails else 0)

"""Side-by-side comparison shots: original bighnow.com vs the local clone.
Produces compare-<slug>.png files (original left, clone right, same scale)."""

import pathlib
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

if sys.stdout:
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = sys.argv[1:] or [
    "nuricell", "deer-horn-reishi", "turmerific", "nano-detoxifier", "heart-q10",
    "advanced-opc-formula", "green-bee-propolis", "nature-calm", "super-green", "uber-calcium",
]

def shoot(pg, url, path):
    pg.goto(url, wait_until="domcontentloaded", timeout=60000)
    pg.wait_for_timeout(2500)
    pg.evaluate(
        "async () => { for (let y = 0; y <= document.body.scrollHeight; y += 500) {"
        " window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } window.scrollTo(0,0); }"
    )
    pg.wait_for_timeout(1500)
    pg.screenshot(path=path, full_page=True)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    for slug in PAGES:
        try:
            shoot(pg, f"https://bighnow.com/{slug}", ROOT / f"_cmp_orig_{slug}.png")
            shoot(pg, f"http://localhost:3456/{slug}", ROOT / f"_cmp_mine_{slug}.png")
            a = Image.open(ROOT / f"_cmp_orig_{slug}.png")
            c = Image.open(ROOT / f"_cmp_mine_{slug}.png")
            # scale both to 700px wide, stack side by side
            def scaled(im):
                w = 700
                h = int(im.height * w / im.width)
                return im.resize((w, h))
            a2, c2 = scaled(a), scaled(c)
            H = max(a2.height, c2.height)
            canvas = Image.new("RGB", (1410, H), "white")
            canvas.paste(a2, (0, 0))
            canvas.paste(c2, (710, 0))
            canvas.save(ROOT / f"compare-{slug}.png")
            (ROOT / f"_cmp_orig_{slug}.png").unlink()
            (ROOT / f"_cmp_mine_{slug}.png").unlink()
            print(slug, f"ok (orig {a.height}px vs clone {c.height}px)")
        except Exception as e:
            print(slug, "FAIL", str(e)[:120])
    b.close()
print("done")

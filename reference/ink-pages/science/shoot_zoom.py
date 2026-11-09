"""Screenshots of the Science page's zoom opening at several scroll depths.

  python -X utf8 reference/ink-pages/science/shoot_zoom.py <base-url> [out-dir]

Desktop, laptop, tablet and phone, plus reduced motion; pictures land in plates/zoom-shots/
(git-ignored) unless an out-dir is given.
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://localhost:3104"
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parent / "plates" / "zoom-shots"
OUT.mkdir(parents=True, exist_ok=True)
STOPS = (0.0, 0.2, 0.37, 0.5, 0.68, 0.78, 0.9, 1.0)
SIZES = (("desk", 1440, 900), ("laptop", 1280, 720), ("wide", 1920, 1080), ("tablet", 768, 1024), ("phone", 390, 844), ("small", 360, 740))
TO = """s => { const t = document.querySelector('[data-zoom]');
  scrollTo({ top: t.offsetTop + (t.offsetHeight - innerHeight) * s, behavior: 'instant' }); }"""

with sync_playwright() as p:
    b = p.chromium.launch()
    for name, w, h in SIZES:
        ctx = b.new_context(viewport={"width": w, "height": h})
        pg = ctx.new_page()
        pg.goto(BASE + "/en/science", wait_until="networkidle")
        pg.wait_for_timeout(4200)
        for s in STOPS:
            pg.evaluate(TO, s)
            pg.wait_for_timeout(1600)
            pg.screenshot(path=str(OUT / f"{name}-{int(s * 100):03d}.png"))
        pg.mouse.wheel(0, h * 0.8)
        pg.wait_for_timeout(1800)
        pg.screenshot(path=str(OUT / f"{name}-after.png"))
        ctx.close()
    for name, w, h in (("desk", 1440, 900), ("phone", 390, 844)):
        ctx = b.new_context(viewport={"width": w, "height": h}, reduced_motion="reduce")
        pg = ctx.new_page()
        pg.goto(BASE + "/en/science", wait_until="networkidle")
        pg.wait_for_timeout(1500)
        for i in range(3):
            pg.screenshot(path=str(OUT / f"{name}-still-{i}.png"))
            pg.mouse.wheel(0, h * 0.95)
            pg.wait_for_timeout(700)
        ctx.close()
    b.close()
print("shots in", OUT)

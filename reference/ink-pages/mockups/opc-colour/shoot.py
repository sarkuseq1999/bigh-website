"""Before and after for Advanced OPC Formula's four repainted chapter paintings (November 17, 2026:
Mo picked "same pictures, in color"): the research lens, Dr. Wang's mortar, the plate and the vine
scene by the bottle. Shoots each chapter on a page (the live demo for before, the built site for
after), its picture just under the menu bar, at 1440 and 390 px, reduced motion (no bloom wait).

usage: python -X utf8 shoot.py <label> <base-url>
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
label, base = sys.argv[1], sys.argv[2]
OUT = HERE / "shots"
OUT.mkdir(exist_ok=True)
CHAPTERS = ["research", "people", "daily", "buy"]
with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-angle=d3d11"])
    for size, w, h, dpr in [("desk", 1440, 900, 1), ("phone", 390, 844, 2)]:
        mobile = w < 768
        ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=dpr, is_mobile=mobile, has_touch=mobile, reduced_motion="reduce")
        pg = ctx.new_page()
        pg.goto(base + "/en/products/advanced-opc", wait_until="networkidle")
        pg.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
        for ch in CHAPTERS:
            pg.evaluate(
                "([s, t]) => { const e = document.querySelector(s); window.scrollBy(0, e.getBoundingClientRect().top - t); }",
                [f'[data-chapter="{ch}"] figure', 105 if not mobile else 60],
            )
            pg.wait_for_timeout(1200)
            pg.screenshot(path=str(OUT / f"{label}-{ch}-{size}.png"))
        ctx.close()
    b.close()
print("done", label)

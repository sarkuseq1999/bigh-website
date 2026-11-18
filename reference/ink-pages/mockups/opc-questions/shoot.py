"""Before and after for Advanced OPC Formula's six question paintings in colour (November 17,
2026: Mo picked A, the same pictures in color, the capsule one without its powder). Opens each
question in turn at 1440 px and shoots the questions part; at 390 px shoots the capsule question.

usage: python -X utf8 shoot.py <label> <base-url>
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
label, base = sys.argv[1], sys.argv[2]
OUT = HERE / "shots"
OUT.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-angle=d3d11"])
    for size, w, h, dpr in [("desk", 1440, 900, 1), ("phone", 390, 844, 2)]:
        mobile = w < 768
        ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=dpr, is_mobile=mobile, has_touch=mobile, reduced_motion="reduce")
        pg = ctx.new_page()
        pg.goto(base + "/en/products/advanced-opc", wait_until="networkidle")
        pg.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
        buttons = pg.locator("#questions ol > li > h3 button")
        n = buttons.count()
        for i in range(n):
            if mobile and i != 3:
                continue
            btn = buttons.nth(i)
            if btn.get_attribute("aria-expanded") != "true":
                btn.click()
            pg.wait_for_timeout(900)
            target = "#questions" if not mobile else f"#questions ol > li:nth-child({i + 1})"
            pg.evaluate("([s, t]) => { const e = document.querySelector(s); window.scrollBy(0, e.getBoundingClientRect().top - t); }", [target, 90])
            pg.wait_for_timeout(900)
            pg.screenshot(path=str(OUT / f"{label}-{size}-{i + 1}.png"))
        ctx.close()
    b.close()
print("done", label)

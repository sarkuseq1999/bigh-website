"""Before and after for Turmerific's paintings in colour (November 17, 2026: the same pictures in
color, page by page): the Why root before and after its moment, the research notebook, and the
five questions, each opened. 1440 px; the Why also at 390 px.

usage: python -X utf8 shoot.py <label> <base-url>
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
label, base = sys.argv[1], sys.argv[2]
OUT = HERE / "shots"
OUT.mkdir(exist_ok=True)
URL = base + "/en/products/turmerific"
BRING = "([s, t]) => { const e = document.querySelector(s); window.scrollBy(0, e.getBoundingClientRect().top - t); }"
with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-angle=d3d11"])
    for size, w, h, dpr in [("desk", 1440, 900, 1), ("phone", 390, 844, 2)]:
        mobile = w < 768
        ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=dpr, is_mobile=mobile, has_touch=mobile)
        pg = ctx.new_page()
        pg.goto(URL, wait_until="networkidle")
        pg.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
        pg.evaluate(BRING, ['[data-chapter="why"] figure', 105 if not mobile else 60])
        pg.wait_for_timeout(1300)
        pg.screenshot(path=str(OUT / f"{label}-why-{size}-1before.png"))
        pg.wait_for_timeout(8500)
        pg.screenshot(path=str(OUT / f"{label}-why-{size}-2after.png"))
        if not mobile:
            pg.evaluate(BRING, ['[data-chapter="research"] figure', 105])
            pg.wait_for_timeout(2500)
            pg.screenshot(path=str(OUT / f"{label}-research-{size}.png"))
            buttons = pg.locator("#questions ol > li > h3 button")
            for i in range(buttons.count()):
                btn = buttons.nth(i)
                if btn.get_attribute("aria-expanded") != "true":
                    btn.click()
                pg.wait_for_timeout(700)
                pg.evaluate(BRING, ["#questions", 90])
                pg.wait_for_timeout(900)
                pg.screenshot(path=str(OUT / f"{label}-q{i + 1}-{size}.png"))
        ctx.close()
    b.close()
print("done", label)

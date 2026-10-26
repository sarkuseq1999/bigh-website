"""Screenshot NuriCell's "What's inside" chapter as a visitor scrolls to it (desktop and phone),
plus the labels of the chapters round it, to judge the chapter as it is now.

usage: python -X utf8 shoot_now.py <outdir> [base-url]
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

out = Path(sys.argv[1])
base = sys.argv[2] if len(sys.argv) > 2 else "https://bigh-website-demo.vercel.app"
out.mkdir(parents=True, exist_ok=True)

SIZES = [("desk1440", 1440, 900, 1), ("phone", 390, 844, 2)]

with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-angle=d3d11"])
    for label, w, h, dpr in SIZES:
        mobile = w < 768
        ctx = b.new_context(
            viewport={"width": w, "height": h},
            device_scale_factor=dpr,
            is_mobile=mobile,
            has_touch=mobile,
        )
        pg = ctx.new_page()
        pg.goto(base + "/products/nuricell", wait_until="networkidle")
        pg.wait_for_timeout(2000)
        top = pg.evaluate(
            "Math.round(document.querySelector('[data-chapter=inside]').getBoundingClientRect().top + scrollY)"
        )
        for y in range(0, top, 400):
            pg.evaluate(f"window.scrollTo(0,{y})")
            pg.wait_for_timeout(100)
        height = pg.evaluate(
            "Math.round(document.querySelector('[data-chapter=inside]').getBoundingClientRect().height)"
        )
        i, y = 0, top - 60
        while True:
            pg.evaluate(f"window.scrollTo(0,{y})")
            pg.wait_for_timeout(2500)
            pg.screenshot(path=str(out / f"now-{label}-{i}.png"))
            i += 1
            y += h - 160
            if y >= top + height - 60 or i >= 8:
                break
        # The chapter labels and headings across the page, to compare their look.
        info = pg.evaluate(
            """() => [...document.querySelectorAll('[data-chapter]')].map(s => {
                const l = s.querySelector('[data-words] > p:first-child');
                const h = s.querySelector('h2');
                const cs = l ? getComputedStyle(l) : null;
                const hs = h ? getComputedStyle(h) : null;
                return [s.dataset.chapter, l && l.textContent, cs && cs.fontSize, cs && cs.color,
                        cs && cs.fontFamily.slice(0, 30), cs && cs.textTransform,
                        h && h.textContent.slice(0, 50), hs && hs.fontSize, hs && hs.fontFamily.slice(0, 30), hs && hs.fontWeight];
            })"""
        )
        for row in info:
            print(label, row)
        ctx.close()
    b.close()
print("done")

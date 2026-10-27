"""Screenshot NuriCell's Questions section as it is now, with what sits above and below it.

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
        pg.wait_for_timeout(1500)
        top = pg.evaluate(
            "() => document.querySelector('#questions').getBoundingClientRect().top + scrollY"
        )
        # Three screens: the one before the questions, the questions, the one after.
        for i, off in enumerate((-h, 0, h)):
            pg.evaluate(f"window.scrollTo(0, {top + off - 40})")
            pg.wait_for_timeout(900)
            pg.screenshot(path=str(out / f"{label}-{i}.png"))
        ctx.close()
    b.close()
print("done", out)

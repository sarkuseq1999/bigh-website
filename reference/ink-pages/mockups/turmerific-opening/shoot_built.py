"""Shoot Turmerific's opening as built, at the sizes the review uses.

usage: python -X utf8 shoot_built.py <base-url> <outdir> [label,...]
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

base, out = sys.argv[1].rstrip("/"), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
only = sys.argv[3].split(",") if len(sys.argv) > 3 else None
SIZES = [
    ("desk1440", 1440, 900, 1),
    ("desk1920", 1920, 1080, 1),
    ("desk1280", 1280, 720, 1),
    ("desk1600", 1600, 1000, 1),
    ("desk2560", 2560, 1300, 1),
    ("desk1024", 1024, 768, 1),
    ("tablet768", 768, 1024, 1),
    ("phone", 390, 844, 2),
    ("phone360", 360, 780, 2),
    ("short1440", 1440, 700, 1),
]

with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-angle=d3d11"])
    for label, w, h, dpr in SIZES:
        if only and label not in only:
            continue
        mobile = w < 768
        ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=dpr, is_mobile=mobile, has_touch=mobile)
        pg = ctx.new_page()
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto(base + "/en/products/turmerific", wait_until="networkidle")
        pg.wait_for_timeout(2600)
        sideways = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        pg.screenshot(path=str(out / f"built-{label}.png"))
        print(label, "sideways scroll", sideways, "errors", errors, flush=True)
        ctx.close()
    b.close()

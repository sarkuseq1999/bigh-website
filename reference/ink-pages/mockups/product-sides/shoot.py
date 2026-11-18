"""The painted product pages' chapters with alternating sides (November 18, 2026): each chapter
from "Why it matters" to Buy, its painting near the window's top, at 1440 and 1024 px, reduced
motion. Before: the live demo; after: the built site.

usage: python -X utf8 shoot.py <label> <base-url>
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
label, base = sys.argv[1], sys.argv[2]
OUT = HERE / "shots"
OUT.mkdir(exist_ok=True)
PAGES = {"advanced-opc": ["why", "inside", "research", "people", "daily", "buy"], "turmerific": ["why", "inside", "research", "daily", "buy"], "nature-calm": ["why", "inside", "research", "people", "daily", "buy"]}
BRING = "([s, t]) => { const e = document.querySelector(s); window.scrollBy(0, e.getBoundingClientRect().top - t); }"
with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-angle=d3d11"])
    for w, h in [(1440, 900), (1024, 768)]:
        ctx = b.new_context(viewport={"width": w, "height": h}, reduced_motion="reduce")
        pg = ctx.new_page()
        for slug, chapters in PAGES.items():
            pg.goto(f"{base}/en/products/{slug}", wait_until="networkidle")
            pg.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
            for ch in chapters:
                pg.evaluate(BRING, [f'[data-chapter="{ch}"] figure', 110])
                pg.wait_for_timeout(900)
                pg.screenshot(path=str(OUT / f"{label}-{slug}-{ch}-{w}.png"))
        ctx.close()
    b.close()
print("done", label)

"""Before and after for the small grey labels over the product chapters' headings (November 16,
2026). Mo found them strange three times on NuriCell ("Why cellular health matters", "What's
inside", "The research") and they were taken off there; OPC, Turmerific and Nature Calm still show
them on every chapter but the opening and the buy chapter (whose line is the product's eyebrow).
Green Bee Propolis numbers its labels as its own chapter system and is left out.

The after is the live page with the labels hidden by script; nothing else changes.

usage: python -X utf8 shoot.py [base-url]
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
OUT = HERE / "shots"
OUT.mkdir(exist_ok=True)
BASE = sys.argv[1] if len(sys.argv) > 1 else "https://bigh-website-demo.vercel.app"
PAGES = {"advanced-opc": ["why", "inside"], "turmerific": ["why", "research"], "nature-calm": ["why", "people"]}
HIDE = """() => { const s = document.createElement('style');
  s.textContent = '[data-chapter]:not([data-chapter="overview"]):not([data-chapter="buy"]) [data-words] > p[class*="label"] { display: none !important; }';
  document.head.append(s); }"""

with sync_playwright() as p:
    b = p.chromium.launch()
    for slug, chapters in PAGES.items():
        for label, w, h, dpr in [("desk", 1440, 900, 1), ("phone", 390, 844, 2)]:
            for state in ["before", "after"]:
                ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=dpr, reduced_motion="reduce")
                pg = ctx.new_page()
                pg.goto(f"{BASE}/en/products/{slug}", wait_until="networkidle")
                pg.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
                if state == "after":
                    pg.evaluate(HIDE)
                for ch in chapters:
                    # The heading near the window's top on a computer; on a phone the chapter's words.
                    sel = f'[data-chapter="{ch}"] h2' if label == "desk" else f'[data-chapter="{ch}"] [data-words]'
                    pg.evaluate("([s, t]) => { const e = document.querySelector(s); window.scrollBy(0, e.getBoundingClientRect().top - t); }", [sel, 260 if label == "desk" else 120])
                    pg.wait_for_timeout(900)
                    pg.screenshot(path=str(OUT / f"{slug}-{ch}-{label}-{state}.png"))
                ctx.close()
        print("done", slug, flush=True)
    b.close()

"""Viewport shots of NuriCell's built daily chapter (the redwood round), scrolled like a visitor.

usage: python -X utf8 shoot_built.py <base-url> <out-dir> [locale]
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE, OUT = sys.argv[1], Path(sys.argv[2])
LOCALE = sys.argv[3] if len(sys.argv) > 3 else "en"
OUT.mkdir(parents=True, exist_ok=True)
SIZES = {"1440": (1440, 900, 1), "1024": (1024, 768, 1), "390": (390, 844, 2), "360": (360, 780, 2)}

with sync_playwright() as p:
    browser = p.chromium.launch()
    for tag, (w, h, scale) in SIZES.items():
        ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=scale,
                                  is_mobile=w < 600, has_touch=w < 600)
        page = ctx.new_page()
        page.goto(f"{BASE}/{LOCALE}/products/nuricell", wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        top, bottom = page.evaluate("""() => { const c = document.querySelector('[data-chapter="daily"]');
          const r = c.getBoundingClientRect(); return [r.top + scrollY, r.bottom + scrollY]; }""")
        # Walk in from the end of Dr. Liu's chapter, as a visitor scrolls, so the painting blooms.
        y, k = top - h * 0.6, 0
        while y < bottom + h * 0.3 and k < 5:
            page.evaluate(f"window.scrollTo(0, {y})")
            page.wait_for_timeout(2600)
            page.screenshot(path=str(OUT / f"{LOCALE}-{tag}-{k}.png"))
            k += 1
            y += h * 0.55
        info = page.evaluate("""() => { const c = document.querySelector('[data-chapter="daily"]');
          const f = c.querySelector('figure').getBoundingClientRect(), t = c.querySelector('[data-words]').getBoundingClientRect();
          const img = c.querySelector('figure img');
          return { fig: [Math.round(f.left), Math.round(f.top), Math.round(f.width), Math.round(f.height)],
                   words: [Math.round(t.left), Math.round(t.top), Math.round(t.width), Math.round(t.height)],
                   src: img.currentSrc.slice(-60), loaded: img.complete && img.naturalWidth > 0,
                   bloom: img.dataset.bloom, sum: !!c.querySelector('[data-sum]') }; }""")
        print(LOCALE, tag, k, "shots", info, flush=True)
        ctx.close()
    browser.close()

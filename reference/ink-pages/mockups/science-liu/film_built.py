"""Film the BUILT Dr. Liu part's drifting gold (still pictures cannot show it), for the review page.

  python -X utf8 reference/ink-pages/mockups/science-liu/film_built.py <base-url>

Opens <base-url>/science at a desktop and a phone size, brings Dr. Liu's painting into the window,
waits for it to bloom, then takes a frame about every 100ms for 7 seconds (the painting's own box)
and saves them as one moving picture each, review/built-drift-desk.webp and -phone.webp, at the pace
they were taken. Also prints how far the busiest sliver travelled, in css px.
"""

import sys
import time
from io import BytesIO
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
REVIEW = HERE / "review"
REVIEW.mkdir(exist_ok=True)
BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://localhost:3006"
SIZES = (("desk", 1440, 900, 1, 960), ("phone", 390, 844, 2, 520))
SECONDS = 7.0

TRAVEL = """() => { window.__at = window.__at || [];
  const s = [...document.querySelectorAll('#liu [data-liu-plate] span')].filter(e => e.offsetParent !== null);
  window.__at.push(s.map(e => { const r = e.getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; })); }"""
FARTHEST = """() => { const a = window.__at; let far = 0;
  for (let i = 0; i < a[0].length; i++) { const xs = a.map(f => f[i][0]), ys = a.map(f => f[i][1]);
    far = Math.max(far, Math.hypot(Math.max(...xs) - Math.min(...xs), Math.max(...ys) - Math.min(...ys))); }
  return far; }"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    for name, w, h, dense, out_width in SIZES:
        ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=dense)
        page = ctx.new_page()
        page.goto(BASE + "/science", wait_until="networkidle")
        page.wait_for_timeout(1200)
        page.evaluate(
            "bar => { const r = document.querySelector('#liu [data-liu-plate]').getBoundingClientRect();"
            " scrollBy({ top: r.top - bar - Math.max(0, (innerHeight - bar - r.height) / 2), behavior: 'instant' }); }",
            96,
        )
        page.wait_for_function("document.querySelector('#liu [data-liu-plate]').dataset.bloom === 'done'", timeout=9000)
        page.wait_for_timeout(400)
        box = page.locator("#liu [data-liu-plate]").bounding_box()
        clip = {"x": box["x"], "y": max(0, box["y"]), "width": box["width"], "height": min(box["height"], h - max(0, box["y"]))}
        frames, stamps = [], []
        start = time.perf_counter()
        while time.perf_counter() - start < SECONDS:
            stamps.append(time.perf_counter())
            page.evaluate(TRAVEL)
            frames.append(page.screenshot(clip=clip, type="jpeg", quality=88))
        far = page.evaluate(FARTHEST)
        ctx.close()
        images = [Image.open(BytesIO(f)).convert("RGB") for f in frames]
        images = [im.resize((out_width, round(im.height * out_width / im.width)), Image.LANCZOS) for im in images]
        gaps = [round((b - a) * 1000) for a, b in zip(stamps, stamps[1:])] + [100]
        path = REVIEW / f"built-drift-{name}.webp"
        images[0].save(path, "WEBP", save_all=True, append_images=images[1:], duration=gaps, loop=0, quality=72, method=4)
        print(name, len(images), "frames,", f"{sum(gaps) / 1000:.1f}s,", f"{path.stat().st_size // 1024} KB,", f"farthest sliver travelled {far:.1f} css px")
    browser.close()

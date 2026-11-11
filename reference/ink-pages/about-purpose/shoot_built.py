"""Shoot the built About page's purpose part like a visitor: with motion, scrolled to, settled.

Usage: python -X utf8 shoot_built.py <base-url> <out-dir> [path]
Shots: desk (1440x900), wide (1920x1000), tablet (768x1024), phone (390x844, 2x): the part centred,
then arriving from the meadow; plus the gold's light band mid-pass on the desk.
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

base = sys.argv[1].rstrip("/")
out = Path(sys.argv[2])
path = sys.argv[3] if len(sys.argv) > 3 else "/about"
out.mkdir(parents=True, exist_ok=True)

SIZES = [("desk", 1440, 900, 1), ("wide", 1920, 1000, 1), ("tablet", 768, 1024, 1), ("phone", 390, 844, 2)]

CENTRE = """() => {
  const r = document.querySelector('[data-part="purpose"]').getBoundingClientRect();
  const y = r.top + scrollY;
  scrollTo(0, Math.max(0, r.height < innerHeight ? y - (innerHeight - r.height) / 2 : y));
}"""
ARRIVE = """() => {
  const r = document.querySelector('[data-part="purpose"]').getBoundingClientRect();
  scrollTo(0, Math.max(0, r.top + scrollY - innerHeight * 0.42));
}"""
STATE = """() => {
  const fig = document.querySelector('[data-part="purpose"] [data-picture]');
  const img = fig.querySelector('img');
  const gold = fig.querySelector('span > span');
  return { bloom: img.dataset.bloom, src: img.currentSrc.replace(/^.*url=/, '').slice(0, 60), natural: img.naturalWidth,
           blend: getComputedStyle(img).mixBlendMode, gold: gold ? getComputedStyle(gold).opacity : null,
           goldMask: gold ? getComputedStyle(gold).getPropertyValue('--gold') : null, alt: img.alt.slice(0, 50) };
}"""

with sync_playwright() as p:
    browser = p.chromium.launch(args=["--use-angle=d3d11"])
    for name, w, h, dpr in SIZES:
        ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=dpr,
                                  is_mobile=name == "phone", has_touch=name == "phone")
        page = ctx.new_page()
        errors = []
        page.on("console", lambda m: errors.append(m.text) if m.type in ("error", "warning") else None)
        page.goto(f"{base}{path}", wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(1200)
        # Scroll down in steps, like a visitor, so the painting blooms as it arrives.
        target = page.evaluate("""() => document.querySelector('[data-part="purpose"]').getBoundingClientRect().top + scrollY""")
        y = 0
        while y < target - h * 0.42:
            y = min(y + 260, target - h * 0.42)
            page.evaluate(f"scrollTo(0, {y})")
            page.wait_for_timeout(120)
        page.wait_for_timeout(2600)
        page.screenshot(path=str(out / f"{name}-arrive.png"))
        # The light on the gold leaf, mid-pass: the painting 38% of the way through the window.
        page.evaluate("""() => {
          const r = document.querySelector('[data-part="purpose"] [data-picture] img').getBoundingClientRect();
          const top = innerHeight - 0.38 * (innerHeight + r.height);
          scrollTo(0, r.top + scrollY - top);
        }""")
        page.wait_for_timeout(700)
        page.screenshot(path=str(out / f"{name}-glint.png"))
        page.evaluate(CENTRE)
        page.wait_for_timeout(2600)
        page.screenshot(path=str(out / f"{name}.png"))
        print(name, page.evaluate(STATE), "console:", errors[:3])
        ctx.close()
    browser.close()

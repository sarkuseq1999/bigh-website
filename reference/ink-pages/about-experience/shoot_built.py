"""Shoot the built About page's experience part like a visitor: with motion, scrolled to, settled.

Usage: python -X utf8 shoot_built.py <base-url> <out-dir> [path]
Shots: desk (1440x900), wide (1920x1000), tablet (768x1024), phone (390x844, 2x): the part centred
(its top under the menu bar when it is taller than the window), then arriving from the valley
above; plus, on each, the gold leaf's colour as the painting comes up the window (the kit's band of
light should cross it on the way and have left it at rest), and a shot of the leaf at its most lit.
"""

import io
import sys
from pathlib import Path

from PIL import Image, ImageStat
from playwright.sync_api import sync_playwright

base = sys.argv[1].rstrip("/")
out = Path(sys.argv[2])
path = sys.argv[3] if len(sys.argv) > 3 else "/about"
out.mkdir(parents=True, exist_ok=True)

SIZES = [("desk", 1440, 900, 1), ("wide", 1920, 1000, 1), ("tablet", 768, 1024, 1), ("phone", 390, 844, 2)]
IMG = '[data-part="experience"] [data-picture] img'
# The leaf's heart, in fractions of the painting (build_about_experience.py).
LEAF = (0.449, 0.427, 0.465, 0.443)

CENTRE = """() => {
  const r = document.querySelector('[data-part="experience"]').getBoundingClientRect();
  const y = r.top + scrollY;
  const bar = document.querySelector('header')?.getBoundingClientRect().bottom ?? 0;
  scrollTo(0, Math.max(0, r.height < innerHeight - bar ? y - (innerHeight - r.height) / 2 : y - bar));
}"""
STATE = f"""() => {{
  const img = document.querySelector('{IMG}');
  const gold = img.nextElementSibling;
  return {{ bloom: img.dataset.bloom, src: decodeURIComponent(img.currentSrc).replace(/^.*url=/, '').slice(0, 60),
           natural: img.naturalWidth, blend: getComputedStyle(img).mixBlendMode,
           gold: gold ? getComputedStyle(gold).opacity : null, alt: img.alt.slice(0, 60) }};
}}"""
# Put the painting `t` of the way through the window (0: its top at the window's foot; 1: its foot
# at the window's top), the kit's "cover" range.
AT = f"""(t) => {{
  const r = document.querySelector('{IMG}').getBoundingClientRect();
  const top = innerHeight - t * (innerHeight + r.height);
  scrollTo(0, r.top + scrollY - top);
}}"""


def leaf(page):
    box = page.evaluate(f"(() => {{ const r = document.querySelector('{IMG}').getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; }})()")
    shot = Image.open(io.BytesIO(page.screenshot())).convert("RGB")
    s = shot.width / page.viewport_size["width"]
    x0, y0, x1, y1 = LEAF
    heart = shot.crop((round((box[0] + x0 * box[2]) * s), round((box[1] + y0 * box[3]) * s),
                       round((box[0] + x1 * box[2]) * s), round((box[1] + y1 * box[3]) * s)))
    r, g, b = (round(v) for v in ImageStat.Stat(heart).mean)
    return [r, g, b], shot


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
        target = page.evaluate("""() => document.querySelector('[data-part="experience"]').getBoundingClientRect().top + scrollY""")
        y = 0
        while y < target - h * 0.45:
            y = min(y + 300, target - h * 0.45)
            page.evaluate(f"scrollTo(0, {y})")
            page.wait_for_timeout(100)
        page.wait_for_timeout(2600)
        page.screenshot(path=str(out / f"{name}-arrive.png"))
        # The leaf as the painting comes up the window.
        scan, brightest = [], None
        for t in [0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55]:
            page.evaluate(AT, t)
            page.wait_for_timeout(250)
            rgb, shot = leaf(page)
            scan.append((t, rgb[0] - rgb[2]))
            if brightest is None or rgb[2] > brightest[0]:
                brightest = (rgb[2], shot)
        brightest[1].save(out / f"{name}-glint.png")
        page.evaluate(CENTRE)
        page.wait_for_timeout(2600)
        rest, shot = leaf(page)
        shot.save(out / f"{name}.png")
        print(name, page.evaluate(STATE), "| leaf at rest", rest, "| red over blue on the way up", scan, "| console:", errors[:3])
        ctx.close()
    browser.close()

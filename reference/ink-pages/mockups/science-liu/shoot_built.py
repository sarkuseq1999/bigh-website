"""Shots of the BUILT Dr. Liu part (Mo picked C, November 11, 2026), for the look-before-you-show.

  python -X utf8 reference/ink-pages/mockups/science-liu/shoot_built.py <base-url> [lang]

Opens <base-url>[/<lang>]/science at seven window sizes, brings Dr. Liu's part into the window as a
visitor meets it (centred when it fits, else its top under the menu bar), waits for its painting to
bloom, and saves each window into built/ beside this script (smaller copies into review/ as
built-*.jpg). Prints the part's box, the painting's box and how many gold slivers are shown.
"""

import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
OUT = HERE / "built"
REVIEW = HERE / "review"
OUT.mkdir(exist_ok=True)
REVIEW.mkdir(exist_ok=True)

BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://localhost:3007"
LANG = sys.argv[2] if len(sys.argv) > 2 else ""
SIZES = (
    ("wide", 1920, 1080, 1),
    ("desk", 1440, 900, 1),
    ("laptop", 1280, 720, 1),
    ("small", 1024, 768, 1),
    ("tablet", 768, 1024, 1),
    ("phone", 390, 844, 2),
    ("phone-s", 360, 740, 2),
)

MEASURE = """() => {
  const box = e => { const r = e.getBoundingClientRect(); return { left: Math.round(r.left), top: Math.round(r.top + scrollY), width: Math.round(r.width), height: Math.round(r.height) }; };
  const liu = document.querySelector('#liu');
  const plate = liu.querySelector('[data-liu-plate]');
  const shown = [...liu.querySelectorAll('[data-liu-plate] span')].filter(s => s.offsetParent !== null).length;
  const column = liu.querySelector('h2').parentElement;
  return { liu: box(liu), plate: box(plate), words: box(column), slivers: shown, bloom: plate.dataset.bloom, adrift: plate.dataset.adrift,
    scrollWidth: document.documentElement.scrollWidth, clientWidth: document.documentElement.clientWidth };
}"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    for name, w, h, dense in SIZES:
        ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=dense)
        page = ctx.new_page()
        errors = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.goto(f"{BASE}{'/' + LANG if LANG else ''}/science", wait_until="networkidle")
        page.wait_for_timeout(1500)
        m = page.evaluate(MEASURE)
        bar = 96
        fits = m["liu"]["height"] < h - bar
        top = m["liu"]["top"] - (max(bar, (h - m["liu"]["height"]) / 2) if fits else bar)
        page.evaluate("y => scrollTo({ top: y, behavior: 'instant' })", top)
        page.wait_for_timeout(4200)
        tag = f"{LANG + '-' if LANG else ''}{name}"
        page.screenshot(path=str(OUT / f"{tag}.png"))
        if not fits:
            page.evaluate("y => scrollTo({ top: y, behavior: 'instant' })", top + h - bar - 40)
            page.wait_for_timeout(1200)
            page.screenshot(path=str(OUT / f"{tag}-2.png"))
        m = page.evaluate(MEASURE)
        print(tag, m, "| errors:", errors[:2])
        ctx.close()
    browser.close()

for shot in sorted(OUT.glob("*.png")):
    im = Image.open(shot).convert("RGB")
    width = 780 if "phone" in shot.stem else 1280
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(REVIEW / f"built-{shot.stem}.jpg", "JPEG", quality=86, optimize=True, progressive=True)
print("pictures in", OUT, "and", REVIEW)

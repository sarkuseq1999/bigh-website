"""Shoot the NuriCell opening with an optional CSS/JS mock injected.

usage: python -X utf8 shoot.py <name> <base-url> [css-file|-] [sizes] [js-file]
Writes shots/<name>-<size>.png and prints measurements (letters' foot, horizon row on screen,
grass end vs. words).
"""

import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
name, base = sys.argv[1], sys.argv[2]
css = Path(sys.argv[3]).read_text(encoding="utf-8") if len(sys.argv) > 3 and sys.argv[3] != "-" else ""
only = sys.argv[4].split(",") if len(sys.argv) > 4 and sys.argv[4] else None
js = Path(sys.argv[5]).read_text(encoding="utf-8") if len(sys.argv) > 5 else ""
OUT = HERE / "shots"
OUT.mkdir(exist_ok=True)

SIZES = [
    ("mo", 1844, 1000, 1),
    ("d1440", 1440, 900, 1),
    ("d1280", 1280, 720, 1),
    ("d1920", 1920, 1080, 1),
    ("tab", 820, 1180, 2),
    ("phone", 390, 844, 2),
    ("d2560", 2560, 1300, 1),
    ("d1700", 1700, 760, 1),
    ("p320", 320, 568, 2),
]

MEASURE = """
() => {
  const sec = document.querySelector('[data-chapter="overview"]');
  const h1 = sec.querySelector('h1');
  const spans = [...h1.children].filter(e => e.getAttribute('aria-hidden') === 'true');
  const r = (e) => { const b = e.getBoundingClientRect(); return {top: Math.round(b.top), bottom: Math.round(b.bottom), left: Math.round(b.left), right: Math.round(b.right)}; };
  const sky = sec.querySelector('[data-sky]');
  const words = h1.nextElementSibling;
  const out = {name: getComputedStyle(h1).fontSize, spans: spans.map(r), sky: sky ? r(sky) : null, words: r(words)};
  const kids = words ? [...words.querySelectorAll('h2, p, ul, [class*="tags"], [class*="highlights"]')].slice(0, 4).map(e => ({tag: e.tagName, cls: e.className.slice(0, 40), ...r(e)})) : [];
  out.kids = kids;
  return out;
}
"""

with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-angle=d3d11"])
    for label, w, h, dpr in SIZES:
        if only and label not in only:
            continue
        mobile = w < 768
        ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=dpr, is_mobile=mobile, has_touch=mobile)
        pg = ctx.new_page()
        pg.goto(base + "/products/nuricell", wait_until="networkidle")
        pg.wait_for_timeout(4500)
        if css:
            pg.add_style_tag(content=css)
        if js:
            pg.evaluate(js)
        pg.wait_for_timeout(1200)
        pg.screenshot(path=str(OUT / f"{name}-{label}.png"))
        print(label, json.dumps(pg.evaluate(MEASURE)))
        ctx.close()
    b.close()

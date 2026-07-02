"""Measure the original bighnow.com layout so the clone can match it exactly.

Captures, per page: every visible image's src + bounding box (as % of page
width), section backgrounds, and for product pages the main image vs thumbnail
order plus price/buy-button geometry. Writes content/harvest/_layout.json.
"""

import json
import pathlib
import sys

from playwright.sync_api import sync_playwright

if sys.stdout:
    sys.stdout.reconfigure(encoding="utf-8")

OUT = pathlib.Path(__file__).resolve().parent.parent / "content" / "harvest" / "_layout.json"

PRODUCTS = [
    "advanced-opc-formula", "deer-horn-reishi", "green-bee-propolis", "heart-q10",
    "nature-calm", "nano-detoxifier", "nuricell", "super-green", "turmerific", "uber-calcium",
]

JS_COLLECT = """
() => {
  const out = { images: [], sections: [] };
  document.querySelectorAll('img').forEach(img => {
    const r = img.getBoundingClientRect();
    if (r.width < 20 || r.height < 20) return;
    out.images.push({
      src: img.currentSrc || img.src,
      x: Math.round(r.x + window.scrollX), y: Math.round(r.y + window.scrollY),
      w: Math.round(r.width), h: Math.round(r.height),
    });
  });
  document.querySelectorAll('section.elementor-section, .elementor-top-section, div[data-elementor-type] > .e-con, .e-con.e-parent').forEach(sec => {
    const r = sec.getBoundingClientRect();
    if (r.height < 40) return;
    const cs = getComputedStyle(sec);
    out.sections.push({
      y: Math.round(r.y + window.scrollY), h: Math.round(r.height),
      bg: cs.backgroundColor, bgImage: cs.backgroundImage.slice(0, 160),
    });
  });
  const btns = [];
  document.querySelectorAll('a').forEach(a => {
    const r = a.getBoundingClientRect();
    if (r.width < 30 || r.height < 14) return;
    const cs = getComputedStyle(a);
    const txt = (a.textContent || '').trim().slice(0, 40);
    if (txt) btns.push({ text: txt, x: Math.round(r.x), y: Math.round(r.y + window.scrollY),
      w: Math.round(r.width), h: Math.round(r.height), bg: cs.backgroundColor, href: (a.href||'').slice(0,120) });
  });
  out.buttons = btns.slice(0, 40);
  out.pageH = document.body.scrollHeight;
  return out;
}
"""

def scroll_all(pg):
    pg.evaluate(
        "async () => { for (let y = 0; y <= document.body.scrollHeight; y += 500) {"
        " window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } window.scrollTo(0,0); }"
    )
    pg.wait_for_timeout(1200)

result = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})

    for name, url in [("home", "https://bighnow.com/en")] + [
        (slug, f"https://bighnow.com/{slug}") for slug in PRODUCTS
    ]:
        try:
            pg.goto(url, wait_until="domcontentloaded", timeout=60000)
            pg.wait_for_timeout(2500)
            scroll_all(pg)
            result[name] = pg.evaluate(JS_COLLECT)
            print(name, "ok —", len(result[name]["images"]), "imgs,", len(result[name]["sections"]), "sections")
        except Exception as e:
            print(name, "FAIL", str(e)[:120])
    b.close()

OUT.write_text(json.dumps(result, indent=1), encoding="utf-8")
print("wrote", OUT)

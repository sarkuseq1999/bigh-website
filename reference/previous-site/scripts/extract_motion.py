"""Extract Elementor motion-fx settings + floating decoration geometry from
the original product pages, producing src/data/product-decor.json."""

import json
import pathlib
import re
import sys

from playwright.sync_api import sync_playwright

if sys.stdout:
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "src" / "data" / "product-decor.json"

PRODUCTS = [
    "advanced-opc-formula", "deer-horn-reishi", "green-bee-propolis", "heart-q10",
    "nature-calm", "nano-detoxifier", "nuricell", "super-green", "turmerific", "uber-calcium",
]

JS = """
() => {
  const out = [];
  document.querySelectorAll('[data-settings]').forEach(el => {
    const s = el.getAttribute('data-settings') || '';
    if (!s.includes('motion_fx') && !s.includes('_animation')) return;
    const img = el.querySelector('img');
    const r = el.getBoundingClientRect();
    out.push({
      img: img ? (img.currentSrc || img.src) : null,
      x: Math.round(r.x), y: Math.round(r.y + scrollY), w: Math.round(r.width), h: Math.round(r.height),
      settings: s.slice(0, 500),
    });
  });
  return out;
}
"""

def local(url):
    m = re.search(r"wp-content/(.+)$", url or "")
    return "/original/" + m.group(1) if m else None

result = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    for slug in PRODUCTS:
        try:
            pg.goto(f"https://bighnow.com/{slug}", wait_until="domcontentloaded", timeout=60000)
            pg.wait_for_timeout(2200)
            pg.evaluate(
                "async () => { for (let y = 0; y <= document.body.scrollHeight; y += 600) {"
                " window.scrollTo(0, y); await new Promise(r => setTimeout(r, 100)); } window.scrollTo(0,0); }"
            )
            pg.wait_for_timeout(800)
            rows = pg.evaluate(JS)
            cleaned = []
            for r in rows:
                st = r["settings"]
                speed = None
                m = re.search(r'"motion_fx_translateY_speed":\{"unit":"px","size":([\d.]+)', st)
                if m:
                    speed = float(m.group(1))
                direction = "negative" if '"motion_fx_translateY_direction":"negative"' in st else "positive"
                cleaned.append({
                    "img": local(r["img"]),
                    "x": r["x"], "y": r["y"], "w": r["w"], "h": r["h"],
                    "speed": speed, "direction": direction,
                    "hasMotion": "motion_fx_motion_fx_scrolling" in st and '"motion_fx_translateY_effect":"yes"' in st,
                })
            result[slug] = cleaned
            n_motion = sum(1 for c in cleaned if c["hasMotion"])
            print(slug, "-", len(cleaned), "fx elements,", n_motion, "with scroll motion")
        except Exception as e:
            print(slug, "FAIL", str(e)[:100])
    b.close()

OUT.write_text(json.dumps(result, indent=1), encoding="utf-8")
print("wrote", OUT)

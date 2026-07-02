"""Round-2 measurements: about/science page backgrounds, support form fields,
Key Ingredients card geometry + icons, particle-effect detection, hero offsets."""

import json
import pathlib
import sys

from playwright.sync_api import sync_playwright

if sys.stdout:
    sys.stdout.reconfigure(encoding="utf-8")

OUT = pathlib.Path(__file__).resolve().parent.parent / "content" / "harvest" / "_details.json"

JS = """
() => {
  const out = { bgs: [], imgs: [], form: [], particles: [], cards: [], headings: [] };
  // any element with a background-image
  document.querySelectorAll('*').forEach(el => {
    const cs = getComputedStyle(el);
    if (cs.backgroundImage && cs.backgroundImage.includes('url(')) {
      const r = el.getBoundingClientRect();
      if (r.width > 100 && r.height > 60)
        out.bgs.push({ y: Math.round(r.y + scrollY), h: Math.round(r.height), w: Math.round(r.width),
                       x: Math.round(r.x), img: cs.backgroundImage.slice(0, 180), size: cs.backgroundSize, pos: cs.backgroundPosition });
    }
  });
  document.querySelectorAll('img').forEach(img => {
    const r = img.getBoundingClientRect();
    if (r.width < 20) return;
    out.imgs.push({ src: (img.currentSrc || img.src).split('/').pop().slice(0, 60),
                    x: Math.round(r.x), y: Math.round(r.y + scrollY), w: Math.round(r.width), h: Math.round(r.height) });
  });
  document.querySelectorAll('input, textarea, select, button[type=submit], label').forEach(el => {
    const r = el.getBoundingClientRect();
    out.form.push({ tag: el.tagName, type: el.type || '', name: el.name || '', label: (el.textContent || el.placeholder || '').trim().slice(0, 50),
                    x: Math.round(r.x), y: Math.round(r.y + scrollY), w: Math.round(r.width), h: Math.round(r.height),
                    required: !!el.required });
  });
  document.querySelectorAll('canvas, [data-particle_enable], [class*=particle], [id*=particle]').forEach(el => {
    const r = el.getBoundingClientRect();
    out.particles.push({ tag: el.tagName, cls: (el.className.baseVal || el.className || '').toString().slice(0, 80),
                         attrs: el.getAttributeNames().filter(a => a.includes('part') || a.includes('settings')).map(a => a + '=' + (el.getAttribute(a)||'').slice(0,120)),
                         y: Math.round(r.y + scrollY), w: Math.round(r.width), h: Math.round(r.height) });
  });
  // ingredient-style cards: h3 headings and their parent column boxes
  document.querySelectorAll('h3').forEach(h => {
    const col = h.closest('.elementor-column, .elementor-widget') || h.parentElement;
    const r = col.getBoundingClientRect();
    const icon = col.querySelector('img');
    const cs = getComputedStyle(col.querySelector('.elementor-widget-container') || col);
    out.cards.push({ title: h.textContent.trim().slice(0, 40), x: Math.round(r.x), y: Math.round(r.y + scrollY),
                     w: Math.round(r.width), h: Math.round(r.height),
                     icon: icon ? icon.src.split('/').pop().slice(0, 50) : null, bg: cs.backgroundColor, radius: cs.borderRadius });
  });
  document.querySelectorAll('h1, h2').forEach(h => {
    const r = h.getBoundingClientRect();
    const cs = getComputedStyle(h);
    out.headings.push({ text: h.textContent.trim().slice(0, 40), x: Math.round(r.x), y: Math.round(r.y + scrollY),
                        size: cs.fontSize, color: cs.color, align: cs.textAlign });
  });
  const hdr = document.querySelector('header, .elementor-location-header, #masthead');
  if (hdr) {
    const r = hdr.getBoundingClientRect();
    const cs = getComputedStyle(hdr);
    out.header = { h: Math.round(r.height), bg: cs.backgroundColor, position: cs.position,
                   inner: Array.from(hdr.querySelectorAll('div,nav')).slice(0,6).map(d => {
                     const c = getComputedStyle(d); return c.backgroundColor;
                   }) };
  }
  return out;
}
"""

PAGES = {
    "about": "https://bighnow.com/about",
    "science": "https://bighnow.com/science",
    "support": "https://bighnow.com/support",
    "nuricell": "https://bighnow.com/nuricell",
    "nano-detoxifier": "https://bighnow.com/nano-detoxifier",
    "heart-q10": "https://bighnow.com/heart-q10",
    "turmerific": "https://bighnow.com/turmerific",
    "home": "https://bighnow.com/en",
}

result = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    for name, url in PAGES.items():
        try:
            pg.goto(url, wait_until="domcontentloaded", timeout=60000)
            pg.wait_for_timeout(2500)
            pg.evaluate(
                "async () => { for (let y = 0; y <= document.body.scrollHeight; y += 600) {"
                " window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } window.scrollTo(0,0); }"
            )
            pg.wait_for_timeout(1000)
            result[name] = pg.evaluate(JS)
            print(name, "ok:", {k: len(v) for k, v in result[name].items()})
        except Exception as e:
            print(name, "FAIL", str(e)[:100])
    b.close()

OUT.write_text(json.dumps(result, indent=1), encoding="utf-8")
print("wrote", OUT)

"""Where the name's baselines and the bottle's foot fall on the live OPC opening, per window."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE = Path(__file__).parent
js = (HERE / "m6.js").read_text(encoding="utf-8") + """
;(() => { const m = window.__m6; const g = m.glass();
 const base = (el) => { const p = document.createElement('span'); Object.assign(p.style,{display:'inline-block',width:'0',height:'0',verticalAlign:'baseline'}); el.append(p); const y = p.getBoundingClientRect().top; p.remove(); return y; };
 const opc = m.first.lastChild; const r = document.createRange(); r.selectNodeContents(m.first); const rects=[...r.getClientRects()];
 return {W: m.W, formula: base(m.second), firstBottom: m.first.getBoundingClientRect().bottom, foot: g.foot, cx: g.cx, glassTop: g.top}; })()
"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for w, h in [(1440, 900), (1920, 1080), (1280, 720), (1600, 1000)]:
        ctx = b.new_context(viewport={"width": w, "height": h})
        pg = ctx.new_page()
        pg.goto("https://bigh-website-demo.vercel.app/en/products/advanced-opc", wait_until="networkidle")
        pg.wait_for_timeout(1500)
        print(w, h, pg.evaluate(js))
        ctx.close()
    b.close()

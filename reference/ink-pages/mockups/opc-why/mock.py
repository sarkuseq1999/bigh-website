"""Mock up Advanced OPC Formula's "Why antioxidants matter" picture on the live page and shoot its
moment (November 17, 2026). The live grapes are swapped for prep.py's pictures by a route on the
image optimizer; the chapter's own code runs the moment (the lit painting spreads from one point
over the unlit one). The gold-leaf light layer (litGold) is hidden: it belongs to the live take.

usage: python -X utf8 mock.py <concept> <outdir> [base-url]
concept: now | ripe-ah | ripe-bh | seeds-ah | seeds-bh
"""

import sys
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
concept, out = sys.argv[1], Path(sys.argv[2])
base = sys.argv[3] if len(sys.argv) > 3 else "https://bigh-website-demo.vercel.app"
out.mkdir(parents=True, exist_ok=True)
ART = HERE / "art"
# Where the lit painting starts to spread, as fractions of the picture: A from the top of the bunch
# (it ripens from the stem down), B from the seeds (prep.py writes where they are).
SPREAD = {"ripe-ah": (0.5, 0.3), "ripe-bh": (0.5, 0.3)}
for take in ["seeds-ah", "seeds-bh"]:
    f = ART / f"why-{take}-spread.txt"
    if f.exists():
        x, y = f.read_text(encoding="utf-8").split()
        SPREAD[take] = (float(x), float(y))

SIZES = [("desk", 1440, 900, 1), ("phone", 390, 844, 2)]
# Shots after the chapter is brought into view: before the light, in the middle of it, after it.
TIMES = [("1before", 1300), ("2during", 3300), ("3after", 9500)]


def serve(route):
    q = parse_qs(urlparse(route.request.url).query)
    src = unquote(q.get("url", [""])[0])
    for state in ["unlit", "lit"]:
        if src.endswith(f"/grapes-{state}-v1.webp"):
            f = ART / f"why-{concept}-{state}.png"
            return route.fulfill(status=200, body=f.read_bytes(), headers={"content-type": "image/png", "cache-control": "no-store"})
    return route.continue_()


with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-angle=d3d11"])
    for label, w, h, dpr in SIZES:
        mobile = w < 768
        ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=dpr, is_mobile=mobile, has_touch=mobile)
        if concept != "now":
            ctx.route("**/_next/image**", serve)
        pg = ctx.new_page()
        pg.goto(base + "/en/products/advanced-opc", wait_until="networkidle")
        pg.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
        # The small labels over the headings are going (Mo said yes, November 16): hidden here too.
        pg.evaluate("""() => { const s = document.createElement('style');
          s.textContent = '[data-chapter]:not([data-chapter="overview"]):not([data-chapter="buy"]) [data-words] > p[class*="label"] { display: none !important; }';
          document.head.append(s); }""")
        if concept != "now":
            x, y = SPREAD[concept]
            pg.evaluate(
                """([x, y]) => {
                  const s = document.createElement('style');
                  s.textContent = '[data-chapter="why"] [class*="litGold"] { display: none !important; }';
                  document.head.append(s);
                  const lit = document.querySelector('[data-chapter="why"] img[data-lit]');
                  lit.style.setProperty('--spread-x', (x * 100).toFixed(2) + '%');
                  lit.style.setProperty('--spread-y', (y * 100).toFixed(2) + '%');
                }""",
                [x, y],
            )
        # Bring the chapter's picture in, just under the menu bar.
        sel = '[data-chapter="why"] figure'
        pg.evaluate(
            "([s, t]) => { const e = document.querySelector(s); window.scrollBy(0, e.getBoundingClientRect().top - t); }",
            [sel, 105 if not mobile else 60],
        )
        t0 = 0
        for name, at in TIMES:
            pg.wait_for_timeout(at - t0)
            t0 = at
            pg.screenshot(path=str(out / f"{concept}-{label}-{name}.png"))
        if mobile:
            pg.evaluate("() => { const e = document.querySelector('[data-chapter=\"why\"] h2'); window.scrollBy(0, e.getBoundingClientRect().top - 90); }")
            pg.wait_for_timeout(700)
            pg.screenshot(path=str(out / f"{concept}-{label}-4words.png"))
        ctx.close()
    b.close()
print("done", concept)

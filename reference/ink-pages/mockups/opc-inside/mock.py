"""Mock up Advanced OPC Formula's "What's inside" painting on the live page and shoot it (November
17, 2026). The live row is swapped for prep.py's pictures by a route on the image optimizer.

usage: python -X utf8 mock.py <concept> <outdir> [base-url]
concept: now | color-ah | color-bh | nine-ah | nine-bh
"""

import sys
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
concept, out = sys.argv[1], Path(sys.argv[2])
base = sys.argv[3] if len(sys.argv) > 3 else "https://bigh-website-demo.vercel.app"
out.mkdir(parents=True, exist_ok=True)
SIZES = [("desk", 1440, 900, 1), ("phone", 390, 844, 2)]


def serve(route):
    q = parse_qs(urlparse(route.request.url).query)
    if unquote(q.get("url", [""])[0]).endswith("/row-v1.webp"):
        f = HERE / "art" / f"inside-{concept}.png"
        return route.fulfill(status=200, body=f.read_bytes(), headers={"content-type": "image/png", "cache-control": "no-store"})
    return route.continue_()


with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-angle=d3d11"])
    for label, w, h, dpr in SIZES:
        mobile = w < 768
        ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=dpr, is_mobile=mobile, has_touch=mobile, reduced_motion="reduce")
        if concept != "now":
            ctx.route("**/_next/image**", serve)
        pg = ctx.new_page()
        pg.goto(base + "/en/products/advanced-opc", wait_until="networkidle")
        pg.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
        # The chapter's picture just under the menu bar; on a phone also its words.
        pg.evaluate(
            "([s, t]) => { const e = document.querySelector(s); window.scrollBy(0, e.getBoundingClientRect().top - t); }",
            ['[data-chapter="inside"] figure', 105 if not mobile else 60],
        )
        pg.wait_for_timeout(1500)
        pg.screenshot(path=str(out / f"{concept}-{label}.png"))
        ctx.close()
    b.close()
print("done", concept)

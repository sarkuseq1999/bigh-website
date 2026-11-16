"""Link-preview pictures (Open Graph, 1200x630) for the site's pages (November 16, 2026, for launch):
each page's own first screen, shot on the built site at 1200x630 once its opening has settled, so a
shared link shows the page as it opens. Writes public/og/<name>-v1.jpg (src/lib/seo.ts and the
product route name them). Re-shoot after a page's opening changes, under a new version.

usage: python -X utf8 reference/launch/shoot_og.py http://localhost:3006
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://localhost:3006"
OUT = Path(__file__).resolve().parents[2] / "public/og"
OUT.mkdir(parents=True, exist_ok=True)
V = "v1"

PAGES = {
    "home": "/",
    "about": "/about",
    "science": "/science",
    "support": "/support",
    "nuricell": "/products/nuricell",
    "green-bee-propolis": "/products/green-bee-propolis",
    "advanced-opc": "/products/advanced-opc",
    "turmerific": "/products/turmerific",
    "nature-calm": "/products/nature-calm",
}

with sync_playwright() as p:
    browser = p.chromium.launch(args=["--use-angle=d3d11"])
    context = browser.new_context(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
    page = context.new_page()
    for name, path in PAGES.items():
        page.goto(BASE + path, wait_until="networkidle")
        page.wait_for_timeout(6000)  # the opening's fog, bloom and bird settle
        page.screenshot(path=str(OUT / f"{name}-{V}.jpg"), type="jpeg", quality=86)
        print(name)
    browser.close()

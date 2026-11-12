"""Print the nav's hashed CSS-module class names on the public demo."""

import sys

from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "https://bigh-website-demo.vercel.app"

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1536, "height": 864})
    pg.goto(BASE + "/about", wait_until="networkidle")
    names = pg.evaluate(
        """() => {
        const out = new Set();
        document.querySelectorAll('header *, header').forEach(el => {
          for (const c of el.classList) if (/nav-inscription|inscription/i.test(c)) out.add(c);
        });
        return [...out].sort();
      }"""
    )
    print("\n".join(names))
    sheets = pg.evaluate(
        """() => [...document.styleSheets].map(s => s.href).filter(Boolean)"""
    )
    print("\n".join(sheets))
    b.close()

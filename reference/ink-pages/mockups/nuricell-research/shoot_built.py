"""Screenshot the built NuriCell research chapter (Mo picked A): English and two other languages,
desktop and phone, at rest and after a book is tapped.

usage: python -X utf8 shoot_built.py <outdir> [base-url]
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

out = Path(sys.argv[1])
base = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:3091"
out.mkdir(parents=True, exist_ok=True)

CHAPTER = '[data-chapter="research"]'
BOOK_AT = """(n) => {
  const b = document.querySelector('[data-chapter="research"] [data-book="' + n + '"]');
  const r = b.getBoundingClientRect();
  const pts = [...b.style.clipPath.matchAll(/([\\d.]+)% ([\\d.]+)%/g)].map((m) => [+m[1], +m[2]]);
  const cx = pts.reduce((s, p) => s + p[0], 0) / pts.length;
  const cy = pts.reduce((s, p) => s + p[1], 0) / pts.length;
  return [r.left + (r.width * cx) / 100, r.top + (r.height * cy) / 100];
}"""


def to(pg, selector, gap):
    top = pg.evaluate(
        f"() => document.querySelector('{CHAPTER} {selector}').getBoundingClientRect().top + scrollY"
    )
    pg.evaluate(f"window.scrollTo(0, {top - gap})")
    pg.wait_for_timeout(1600)


with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-angle=d3d11"])
    for locale in ("en", "kr", "jp"):
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        pg = ctx.new_page()
        pg.goto(f"{base}/{locale}/products/nuricell", wait_until="networkidle")
        to(pg, "h2", 110)
        pg.mouse.move(1430, 890)
        pg.screenshot(path=str(out / f"desk-{locale}-1-rest.png"))
        x, y = pg.evaluate(BOOK_AT, 3)
        pg.mouse.click(x, y)
        pg.mouse.move(1430, 890)
        pg.wait_for_timeout(1800)
        pg.screenshot(path=str(out / f"desk-{locale}-2-book3.png"))
        ctx.close()

        ctx = b.new_context(
            viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True
        )
        pg = ctx.new_page()
        pg.goto(f"{base}/{locale}/products/nuricell", wait_until="networkidle")
        to(pg, "figure", 90)
        pg.screenshot(path=str(out / f"phone-{locale}-1-painting.png"))
        to(pg, "h2", 100)
        pg.screenshot(path=str(out / f"phone-{locale}-2-questions.png"))
        to(pg, "figure", 90)
        x, y = pg.evaluate(BOOK_AT, 3)
        pg.touchscreen.tap(x, y)
        pg.wait_for_timeout(2200)
        pg.screenshot(path=str(out / f"phone-{locale}-3-book3.png"))
        ctx.close()
    b.close()
print("done", out)

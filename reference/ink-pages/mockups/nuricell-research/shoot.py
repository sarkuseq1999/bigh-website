"""Screenshot the NuriCell research mockup (books as buttons, studies as plain questions).

usage: python -X utf8 shoot.py <outdir> [base-url]
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

out = Path(sys.argv[1])
base = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:3090"
out.mkdir(parents=True, exist_ok=True)

CHAPTER = '[data-chapter="research"]'

# The middle of a book's tap area, in window px.
BOOK_AT = """(n) => {
  const b = document.querySelector('[data-chapter="research"] [data-book="' + n + '"]');
  const r = b.getBoundingClientRect();
  const pts = [...b.style.clipPath.matchAll(/([\\d.]+)% ([\\d.]+)%/g)].map((m) => [+m[1], +m[2]]);
  const cx = pts.reduce((s, p) => s + p[0], 0) / pts.length;
  const cy = pts.reduce((s, p) => s + p[1], 0) / pts.length;
  return [r.left + (r.width * cx) / 100, r.top + (r.height * cy) / 100];
}"""


def settle(pg, ms=1300):
    pg.wait_for_timeout(ms)


def to_heading(pg, gap):
    """Scroll so the chapter's heading sits `gap` px under the window's top."""
    top = pg.evaluate(
        f"() => document.querySelector('{CHAPTER} h2').getBoundingClientRect().top + scrollY"
    )
    pg.evaluate(f"window.scrollTo(0, {top - gap})")
    settle(pg, 1600)


def to_figure(pg, gap):
    top = pg.evaluate(
        f"() => document.querySelector('{CHAPTER} figure').getBoundingClientRect().top + scrollY"
    )
    pg.evaluate(f"window.scrollTo(0, {top - gap})")
    settle(pg, 1600)


with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-angle=d3d11"])

    for label, w, h in (("desk", 1440, 900), ("wide", 1920, 1080)):
        ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1)
        pg = ctx.new_page()
        pg.goto(base + "/products/nuricell", wait_until="networkidle")
        settle(pg, 1500)
        to_heading(pg, 110)
        pg.mouse.move(w - 20, h - 20)
        pg.screenshot(path=str(out / f"{label}-1-rest.png"))
        if label == "wide":
            ctx.close()
            continue
        x, y = pg.evaluate(BOOK_AT, 5)
        pg.mouse.move(x, y)
        settle(pg, 900)
        pg.screenshot(path=str(out / f"{label}-2-hover-book5.png"))
        x, y = pg.evaluate(BOOK_AT, 3)
        pg.mouse.click(x, y)
        pg.mouse.move(w - 20, h - 20)
        settle(pg, 1600)
        pg.screenshot(path=str(out / f"{label}-3-click-book3.png"))
        x, y = pg.evaluate(BOOK_AT, 7)
        pg.mouse.click(x, y)
        pg.mouse.move(w - 20, h - 20)
        settle(pg, 1600)
        pg.screenshot(path=str(out / f"{label}-4-click-book7.png"))
        ctx.close()

    # Phone
    ctx = b.new_context(
        viewport={"width": 390, "height": 844},
        device_scale_factor=2,
        is_mobile=True,
        has_touch=True,
    )
    pg = ctx.new_page()
    pg.goto(base + "/products/nuricell", wait_until="networkidle")
    settle(pg, 1500)
    to_figure(pg, 90)
    pg.screenshot(path=str(out / "phone-1-painting.png"))
    to_heading(pg, 100)
    pg.screenshot(path=str(out / "phone-2-questions.png"))
    to_figure(pg, 90)
    x, y = pg.evaluate(BOOK_AT, 4)
    pg.touchscreen.tap(x, y)
    settle(pg, 2000)
    pg.screenshot(path=str(out / "phone-3-tapped-book4.png"))
    to_figure(pg, 90)
    x, y = pg.evaluate(BOOK_AT, 6)
    pg.touchscreen.tap(x, y)
    settle(pg, 2000)
    pg.screenshot(path=str(out / "phone-4-tapped-book6.png"))
    ctx.close()
    b.close()
print("done", out)

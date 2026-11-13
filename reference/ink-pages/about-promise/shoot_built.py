"""Shoot the built About page's "Our promise" with the coloured dots (Mo picked A, November 12, 2026).

Like shoot_mockups.py, but nothing is swapped in: the page's own pictures and sizes. Reduced motion
for the stills (everything at rest); the part in the middle of the window, then scrolled as a
visitor arrives at it. Also prints each dot's box and loaded picture.

    python -X utf8 reference/ink-pages/about-promise/shoot_built.py [base-url]

Out: plates/shots/built-<size>.png and built-<size>-arrive.png (git-ignored).
"""

import sys

from playwright.sync_api import sync_playwright

from shoot_mockups import ARRIVE, CENTRE, SHOTS

SIZES = [
    ("1440", 1440, 900, 1),
    ("1280", 1280, 800, 1),
    ("1024", 1024, 768, 1),
    ("768", 768, 1024, 1),
    ("390", 390, 844, 2),
    ("360", 360, 740, 2),
]

DOTS = """() => [...document.querySelectorAll('[data-part="promise"] [data-promise] > img')].map((i) => {
  const r = i.getBoundingClientRect();
  return [Math.round(r.width), i.currentSrc.split('url=')[1]?.split('&')[0] ?? i.currentSrc, i.naturalWidth];
})"""


def main():
    base = next((a for a in sys.argv[1:] if "://" in a), "http://localhost:3105").rstrip("/")
    SHOTS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for size, vw, vh, dpr in SIZES:
            ctx = browser.new_context(
                viewport={"width": vw, "height": vh},
                device_scale_factor=dpr,
                reduced_motion="reduce",
                is_mobile=dpr == 2,
                has_touch=dpr == 2,
            )
            page = ctx.new_page()
            page.goto(f"{base}/about", wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            page.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
            page.evaluate(CENTRE)
            page.wait_for_timeout(1500)
            print(size, page.evaluate(DOTS))
            page.screenshot(path=str(SHOTS / f"built-{size}.png"))
            page.evaluate(ARRIVE)
            page.wait_for_timeout(900)
            page.screenshot(path=str(SHOTS / f"built-{size}-arrive.png"))
            ctx.close()
        browser.close()


if __name__ == "__main__":
    main()

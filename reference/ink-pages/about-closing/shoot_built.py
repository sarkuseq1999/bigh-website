"""Shoot the built About page's closing with the tide pool (Mo picked B, November 13, 2026).

Like shoot_mockups.py, but nothing is swapped in: the page's own picture and sizes. Reduced motion
for the stills (everything at rest); the part in the middle of the window, then scrolled as a
visitor arrives at it. Also measures the painting's drawn width at many window widths, against the
width TIDEPOOL in about-ink.tsx asks the server for.

    python -X utf8 reference/ink-pages/about-closing/shoot_built.py [base-url]

Out: plates/shots/built-<size>.png and built-<size>-arrive.png (git-ignored).
"""

import re
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

WIDTHS = [360, 390, 430, 505, 532, 600, 768, 959, 960, 1024, 1142, 1200, 1279, 1280, 1395, 1440, 1920, 2560]

# about-ink.tsx TIDEPOOL, as (max-width, css px or vw share)
SIZES_ATTR = "(max-width: 532px) 85vw, (max-width: 959px) 450px, (max-width: 1142px) 40vw, (max-width: 1279px) 450px, (max-width: 1395px) 36vw, 495px"


def asked(width):
    for part in SIZES_ATTR.split(", "):
        m = re.match(r"\(max-width: (\d+)px\) (\d+)(px|vw)", part)
        if m and width <= int(m[1]):
            return int(m[2]) if m[3] == "px" else width * int(m[2]) / 100
        if not m:
            return int(part.rstrip("px"))
    return None


def main():
    base = next((a for a in sys.argv[1:] if "://" in a), "http://localhost:3105").rstrip("/")
    SHOTS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(f"{base}/about", wait_until="networkidle")
        for w in WIDTHS:
            page.set_viewport_size({"width": w, "height": 900})
            page.wait_for_timeout(250)
            drawn = page.evaluate("document.querySelector('[data-part=\"closing\"] [data-picture] img').getBoundingClientRect().width")
            want = asked(w)
            flag = "" if abs(drawn - want) <= max(4, 0.03 * drawn) else "  <-- off"
            print(f"width {w}: drawn {drawn:.0f}px, asked {want:.0f}px{flag}")
        page.close()
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
            info = page.evaluate("(() => { const i = document.querySelector('[data-part=\"closing\"] [data-picture] img'); const r = i.getBoundingClientRect(); return [Math.round(r.width), Math.round(r.height), decodeURIComponent(i.currentSrc).split('/').pop().split('&')[0], i.alt.slice(0, 40)]; })()")
            print(size, info)
            page.screenshot(path=str(SHOTS / f"built-{size}.png"))
            page.evaluate(ARRIVE)
            page.wait_for_timeout(900)
            page.screenshot(path=str(SHOTS / f"built-{size}-arrive.png"))
            ctx.close()
        browser.close()


if __name__ == "__main__":
    main()

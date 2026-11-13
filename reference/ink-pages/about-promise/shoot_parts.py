"""Shoot only the "Our promise" part for ideas B and C, to set side by side (November 12, 2026).

Mo asked to compare B (four wildflowers) and C (one poppy counting to four). Same swap as
shoot_mockups.py, reduced motion (everything at rest), but each shot is the part alone: its label,
heading, the four pictures and their words.

    python -X utf8 reference/ink-pages/about-promise/shoot_parts.py [base-url]

Out: plates/shots/part-<key>-<size>.png (git-ignored).
"""

import sys

from playwright.sync_api import sync_playwright

from shoot_mockups import SHOTS, SWAP, serve

TAKES = {"b": ("wildflowers-2", 112, 80), "c": ("poppy-count-1", 170, 92)}
SIZES = [("desk", 1440, 900, 1), ("phone", 390, 844, 2)]


def main():
    base = next((a for a in sys.argv[1:] if "://" in a), "https://bigh-website-demo.vercel.app").rstrip("/")
    SHOTS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for key, (take, px, phone) in TAKES.items():
            for size, vw, vh, dpr in SIZES:
                ctx = browser.new_context(
                    viewport={"width": vw, "height": vh},
                    device_scale_factor=dpr,
                    reduced_motion="reduce",
                    is_mobile=dpr == 2,
                    has_touch=dpr == 2,
                )
                page = ctx.new_page()
                page.route("**/__mock/**", serve)
                page.goto(f"{base}/about", wait_until="networkidle")
                page.evaluate("document.fonts.ready")
                if not page.evaluate(SWAP, [take, px, phone]):
                    print("FAIL pictures did not load", key, size)
                part = page.locator('[data-part="promise"] > div').first
                part.scroll_into_view_if_needed()
                page.wait_for_timeout(1200)
                out = SHOTS / f"part-{key}-{size}.png"
                part.screenshot(path=str(out))
                print(key, size, out.name)
                ctx.close()
        browser.close()


if __name__ == "__main__":
    main()

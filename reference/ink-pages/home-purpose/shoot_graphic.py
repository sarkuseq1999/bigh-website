"""Part 10 of the homepage's California pass (November 9, 2026): "Small beginnings. Bigger
possibilities." under the Big Sur close is a <p>, so it never got the title face (home-titles.module.css
gives Ysabeau to h1-h3 only) and shows in heavy Switzer with a grey second line, unlike every other
title on the page. Each look is CSS laid over the live homepage (nothing in src/ changes); shots at
laptop and phone, the words as a visitor scrolls to them.

    python -X utf8 reference/ink-pages/home-purpose/shoot_graphic.py [base-url]

Shots go to plates/graphic/ (git-ignored).
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
OUT = HERE / "plates" / "graphic"
SIZES = [("1440", 1440, 900, False), ("390", 390, 844, True)]
SEL = "#purpose p:has(> span + span)"
LOOKS = {
    "today": "",
    # A: the title face, the second line still grey.
    "a": f"{SEL} {{ font-family: var(--display-font) !important; }}",
    # B: the title face, both lines in ink.
    "b": f"{SEL} {{ font-family: var(--display-font) !important; }} {SEL} > span:last-child {{ color: inherit !important; }}",
}


def main():
    base = (sys.argv[1] if len(sys.argv) > 1 else "https://bigh-website-demo.vercel.app").rstrip("/")
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--use-angle=d3d11"])
        for size, w, h, mobile in SIZES:
            ctx = browser.new_context(
                viewport={"width": w, "height": h}, is_mobile=mobile, has_touch=mobile, device_scale_factor=2
            )
            page = ctx.new_page()
            page.goto(base + "/", wait_until="networkidle")
            page.wait_for_timeout(1500)
            # Wheel down until the words sit a third of the way down the window (the page eases
            # the wheel, so keep turning until it stops moving).
            place = f"document.querySelector('{SEL}').getBoundingClientRect().top + scrollY - innerHeight * 0.3"
            for _ in range(600):
                left = round(page.evaluate(place) - page.evaluate("scrollY"))
                if abs(left) < 24:
                    break
                page.mouse.wheel(0, max(-240, min(240, left)))
                page.wait_for_timeout(50 if abs(left) > 600 else 250)
            page.wait_for_timeout(3000)
            font = page.evaluate(f"getComputedStyle(document.querySelector('{SEL}')).fontFamily")
            print(size, "today's font:", font)
            for name, css in LOOKS.items():
                page.evaluate(
                    """(css) => { let s = document.getElementById('mock'); if (!s) { s = document.createElement('style');
                       s.id = 'mock'; document.head.append(s); } s.textContent = css; }""",
                    css,
                )
                page.wait_for_timeout(400)
                page.screenshot(path=str(OUT / f"{name}-{size}.png"))
            ctx.close()
        browser.close()


if __name__ == "__main__":
    main()

"""QA captures for the three new customer-story designs on the local dev server."""
import os
import sys
from playwright.sync_api import sync_playwright

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "qa_stories")
os.makedirs(OUT, exist_ok=True)
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3007"
LOCALE = sys.argv[2] if len(sys.argv) > 2 else ""  # e.g. "kr"
SIZES = {"desktop": (1440, 900), "phone": (390, 844)}
tag = f"-{LOCALE}" if LOCALE else ""


def jump(page, y):
    page.evaluate(f"window.scrollTo({{top: {y}, behavior: 'instant'}})")
    page.wait_for_timeout(700)


with sync_playwright() as p:
    browser = p.chromium.launch()
    for label, (w, h) in SIZES.items():
        for n in (1, 2, 3):
            page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
            errors = []
            page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
            page.on("console", lambda m: errors.append(f"console: {m.text}") if m.type == "error" else None)
            path = f"/{LOCALE}" if LOCALE else "/"
            page.goto(f"{BASE}{path}?stories={n}", wait_until="networkidle")
            page.wait_for_timeout(800)
            top = page.evaluate("document.getElementById('stories').getBoundingClientRect().top + scrollY")
            jump(page, top)
            page.wait_for_timeout(1400)
            overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            section_h = page.evaluate("Math.round(document.getElementById('stories').getBoundingClientRect().height)")
            if n in (1, 2):
                page.locator("#stories").screenshot(path=os.path.join(OUT, f"d{n}-{label}{tag}.png"))
            else:
                page.screenshot(path=os.path.join(OUT, f"d3-{label}{tag}-head.png"))
                chapters = page.evaluate(
                    "[...document.querySelectorAll('#stories article')].map(a => {const r=a.getBoundingClientRect(); return [Math.round(r.top+scrollY), Math.round(r.height)]})"
                )
                for ci, (ctop, ch) in enumerate(chapters[:2]):
                    travel = max(ch - h, 0)
                    points = [0.0, 0.35, 0.75] if travel else [-0.55, -0.25, 0.1]
                    for pi, frac in enumerate(points):
                        y = ctop + (travel * frac if travel else h * frac)
                        jump(page, y)
                        page.wait_for_timeout(300)
                        page.screenshot(path=os.path.join(OUT, f"d3-{label}{tag}-c{ci + 1}-{pi + 1}.png"))
            print(f"{label} design {n}: section {section_h}px, sideways overflow {overflow}px, errors {len(errors)}")
            for e in errors[:5]:
                print("   ", e[:220])
            page.close()
    browser.close()

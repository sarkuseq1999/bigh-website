"""Capture the three closing looks at desktop and phone width, with the pointer over the picture."""
import os, sys
from playwright.sync_api import sync_playwright
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3007"
LOC = sys.argv[2] if len(sys.argv) > 2 else ""
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "shoot_closing")
os.makedirs(OUT, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    for w, h, tag in ((1440, 900, "desk"), (390, 844, "phone")):
        for n in ("1", "2", "3"):
            page = b.new_page(viewport={"width": w, "height": h})
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.on("console", lambda m: errors.append("console " + m.text[:140]) if m.type == "error" else None)
            page.goto(f"{BASE}/{LOC}?closing={n}", wait_until="networkidle")
            page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
            page.evaluate("document.getElementById('start').scrollIntoView({block: 'start'})")
            page.wait_for_timeout(500)
            box = page.locator("#start").bounding_box()
            # A pointer over the picture, so the tilt, parallax or field light shows.
            page.mouse.move(w * 0.62, min(h - 40, box["height"] * 0.55))
            page.wait_for_timeout(2600)
            page.locator("#start").screenshot(path=os.path.join(OUT, f"{LOC or 'en'}-{tag}-{n}.png"))
            design = page.evaluate("document.getElementById('start').dataset.design")
            # The join with the footer.
            page.evaluate("window.scrollBy(0, document.getElementById('start').getBoundingClientRect().bottom - innerHeight * 0.55)")
            page.wait_for_timeout(600)
            page.screenshot(path=os.path.join(OUT, f"{LOC or 'en'}-{tag}-{n}-join.png"))
            print(tag, n, design, {k: round(v) for k, v in box.items()}, errors[:2] or "no errors")
            page.close()
    b.close()

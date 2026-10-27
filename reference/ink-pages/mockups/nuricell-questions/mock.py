"""Mock up a new Questions section on the NuriCell page by changing the live page in the browser
(mock.js), then screenshot it as a visitor scrolls to it.

usage: python -X utf8 mock.py <idea a|b|c> <outdir> [base-url] [sizes] [pick]
Pictures come from art/div/ through a route on /mock-art/. For C, the numbered marks and the
bottle's spot are set here (shares of the painting's width and height).
"""

import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
idea, out = sys.argv[1], Path(sys.argv[2])
base = (len(sys.argv) > 3 and sys.argv[3]) or "https://bigh-website-demo.vercel.app"
only = sys.argv[4].split(",") if len(sys.argv) > 4 and sys.argv[4] else None
pick = int(sys.argv[5]) if len(sys.argv) > 5 else 0
out.mkdir(parents=True, exist_ok=True)

# C: where each question's number sits on the painting, and where the bottle stands.
MARKS = [(0.1, 0.585), (0.235, 0.105), (0.375, 0.74), (0.535, 0.595), (0.43, 0.56), (0.8, 0.57)]
BOTTLE = {"x": 0.86, "y": 0.745, "h": 0.25}

setup = f"window.__idea = {json.dumps(idea)}; window.__pick = {pick}; "
setup += f"window.__marks = {json.dumps(MARKS)}; window.__bottle = {json.dumps(BOTTLE)};"
js = setup + (HERE / "mock.js").read_text(encoding="utf-8")

SIZES = [
    ("desk1440", 1440, 900, 1),
    ("desk1920", 1920, 1080, 1),
    ("desk1280", 1280, 720, 1),
    ("phone", 390, 844, 2),
]


def serve(route):
    name = route.request.url.split("/mock-art/")[1].split("?")[0]
    f = HERE / "art" / "div" / name
    if not f.exists():
        return route.fulfill(status=404, body="missing " + name)
    route.fulfill(status=200, body=f.read_bytes(), headers={"content-type": "image/png"})


with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-angle=d3d11"])
    for label, w, h, dpr in SIZES:
        if only and label not in only:
            continue
        mobile = w < 768
        ctx = b.new_context(
            viewport={"width": w, "height": h},
            device_scale_factor=dpr,
            is_mobile=mobile,
            has_touch=mobile,
        )
        ctx.route("**/mock-art/**", serve)
        pg = ctx.new_page()
        pg.goto(base + "/products/nuricell", wait_until="networkidle")
        pg.wait_for_timeout(1500)
        pg.evaluate(js)
        pg.wait_for_timeout(1500)
        top = pg.evaluate(
            "() => document.querySelector('#questions').getBoundingClientRect().top + scrollY"
        )
        bottom = pg.evaluate(
            "() => document.querySelector('#questions').getBoundingClientRect().bottom + scrollY"
        )
        nav = 96 if not mobile else 70
        y = top + 30 - nav
        i = 0
        # Screens down the section, as a visitor scrolls (no full-page shots: they break svh).
        while True:
            # Instant, twice: the page scrolls smoothly, and pictures loading on the way move it.
            for _ in range(2):
                pg.evaluate(f"window.scrollTo({{top: {y}, behavior: 'instant'}})")
                pg.wait_for_timeout(900)
            pg.screenshot(path=str(out / f"{idea}{pick if idea == 'a' else ''}-{label}-{i}.png"))
            i += 1
            y += h - nav - 60
            if y + nav > bottom - 80 or i > 4:
                break
        ctx.close()
    b.close()
print("done", out)

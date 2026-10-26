"""Film the mockup page (index.html) as a visitor would: each part scrolled into view, frames over
time so the gold's motion can be judged, and the taps in C. Desktop and phone. The page is wrapped
the way the Artifact host wraps it (doctype and a phone viewport) in _preview.html first.

usage: python -X utf8 shoot_mock.py <outdir> [only-sizes]
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
out = Path(sys.argv[1])
only = sys.argv[2].split(",") if len(sys.argv) > 2 else None
out.mkdir(parents=True, exist_ok=True)
wrap = HERE / "_preview.html"
wrap.write_text(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
    "</head><body>" + (HERE / "index.html").read_text(encoding="utf-8") + "</body></html>",
    encoding="utf-8",
    newline="\n",
)
url = wrap.resolve().as_uri()

SIZES = [("desk", 1440, 900, 1), ("phone", 390, 844, 2)]

with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-angle=d3d11"])
    for label, w, h, dpr in SIZES:
        if only and label not in only:
            continue
        mobile = w < 768
        ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=dpr, is_mobile=mobile, has_touch=mobile)
        pg = ctx.new_page()
        errs = []
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(url, wait_until="networkidle")
        pg.wait_for_timeout(800)
        pg.screenshot(path=str(out / f"{label}-00-top.png"))

        def to(sel, dy=0, i=0):
            pg.evaluate(f"window.scrollTo(0, document.querySelectorAll('{sel}')[{i}].getBoundingClientRect().top + scrollY + {dy})")

        def shots(name, times):
            last = 0
            for t in times:
                pg.wait_for_timeout(t - last)
                last = t
                pg.screenshot(path=str(out / f"{label}-{name}-{t:05d}.png"))

        # Part 1: the plate, frames through the rise and into the float.
        to(".plate", -20 if not mobile else -10)
        shots("1-rise", (300, 900, 1600, 2400, 3400, 5000, 9000))
        if mobile:
            to(".ing", -40)
            pg.wait_for_timeout(600)
            pg.screenshot(path=str(out / f"{label}-1-list.png"))
        to(".choices")
        pg.click("#m2")
        to(".plate", -20 if not mobile else -10)
        shots("1-updraft", (1500, 4000, 7000))
        to(".label-card", -300)
        pg.wait_for_timeout(500)
        pg.screenshot(path=str(out / f"{label}-1-bottom.png"))

        # A: the three scenes (one at a time on phones).
        if mobile:
            for i in range(3):
                to(".scene", -60, i)
                shots(f"A-{i}", (1200, 2600, 4800))
        else:
            to(".proto-a", -30)
            shots("A", (1500, 3200, 5200, 7600))

        # B: each step in the middle of the window.
        for i in range(3):
            pg.evaluate(
                f"(() => {{ const s = document.querySelectorAll('#stepsB .step')[{i}]; const r = s.getBoundingClientRect(); window.scrollTo(0, r.top + scrollY + r.height/2 - innerHeight/2); }})()"
            )
            shots(f"B-{i}", (1400, 4200))

        # C: at rest, after picking Creatine, after picking its partner.
        to("#protoC", -30)
        pg.wait_for_timeout(3600)
        pg.screenshot(path=str(out / f"{label}-C-0-rest.png"))
        pg.click("#gridC [data-k=creatine]")
        pg.wait_for_timeout(500)
        pg.screenshot(path=str(out / f"{label}-C-1-picked.png"))
        pg.click("#gridC [data-k=ala]")
        pg.wait_for_timeout(4600)
        pg.screenshot(path=str(out / f"{label}-C-2-done.png"))

        to(".reply", -300)
        pg.wait_for_timeout(400)
        pg.screenshot(path=str(out / f"{label}-9-end.png"))
        overflow = pg.evaluate("document.documentElement.scrollWidth - innerWidth")
        print(label, "errors:", errs or "none", "| sideways overflow px:", overflow)
        ctx.close()
    b.close()

"""Mock up a new bottom-left for the NuriCell opening (the headline and the purpose under "Nuri") by
changing the live page in the browser, then screenshot it.

usage: python -X utf8 mock.py <idea> <outdir> [base-url] [sizes|all] [product-slug]
idea: now | a | b | c ...  (each has mock_<idea>.js next to this file; "now" changes nothing)
Pictures the mock needs are served from this folder's art/ through a route on /mock-art/.
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
idea, out = sys.argv[1], Path(sys.argv[2])
base = sys.argv[3] if len(sys.argv) > 3 else "https://bigh-website-demo.vercel.app"
only = sys.argv[4].split(",") if len(sys.argv) > 4 and sys.argv[4] != "all" else None
# The product page to change (the opening is shared by all five): nuricell unless named.
product = sys.argv[5] if len(sys.argv) > 5 else "nuricell"
tag = idea if product == "nuricell" else f"{idea}-{product}"
out.mkdir(parents=True, exist_ok=True)
def expand(text):
    """ "//@include <file>" lines pull in another script (an idea that reuses a shared builder),
    which may include another in turn."""
    return "\n".join(
        expand((HERE / line.split(" ", 1)[1].strip()).read_text(encoding="utf-8"))
        if line.startswith("//@include ")
        else line
        for line in text.splitlines()
    )


js = expand((HERE / f"mock_{idea}.js").read_text(encoding="utf-8")) if idea != "now" else ""

# label, width, height, screens, device pixel ratio
SIZES = [
    ("desk1440", 1440, 900, 1, 1),
    ("desk1920", 1920, 1080, 1, 1),
    ("desk1280", 1280, 720, 1, 1),
    ("desk1440x2", 1440, 900, 1, 2),
    ("phone", 390, 844, 2, 2),
]


def serve(route):
    name = route.request.url.split("/mock-art/")[1].split("?")[0]
    f = HERE / "art" / name
    if not f.exists():
        return route.fulfill(status=404, body="missing " + name)
    ctype = "image/png" if name.endswith(".png") else "image/webp"
    route.fulfill(status=200, body=f.read_bytes(), headers={"content-type": ctype})


with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-angle=d3d11"])
    for label, w, h, screens, dpr in SIZES:
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
        pg.goto(base + "/products/" + product, wait_until="networkidle")
        pg.wait_for_timeout(2500)
        if js:
            pg.evaluate(js)
            pg.wait_for_timeout(1800)
        for i in range(screens):
            # A phone's second screen starts where the words start, as a visitor scrolls to them.
            y = 0
            if i:
                y = pg.evaluate(
                    "Math.round(document.querySelector('[data-chapter=overview] h1').getBoundingClientRect().bottom + scrollY - 150)"
                )
            pg.evaluate(f"window.scrollTo(0,{y})")
            pg.wait_for_timeout(900)
            pg.screenshot(path=str(out / f"{tag}-{label}-{i}.png"))
        ctx.close()
    b.close()
print("done", idea)

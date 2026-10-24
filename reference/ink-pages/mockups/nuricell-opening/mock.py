"""Mock up a new NuriCell opening by changing the live page in the browser, then screenshot it.

usage: python -X utf8 mock.py <concept> <outdir> [base-url]
concept: now | a | b | c   (each has mock_<concept>.js next to this file; "now" changes nothing)
Pictures the mock needs are served from this folder's art/ through a route on /mock-art/.
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
concept, out = sys.argv[1], Path(sys.argv[2])
base = sys.argv[3] if len(sys.argv) > 3 else "https://bigh-website-demo.vercel.app"
out.mkdir(parents=True, exist_ok=True)
if (HERE / f"scene_{concept}.json").exists():
    # A painting-beside-the-words idea: its settings, then the shared builder.
    js = (
        "window.__scene = "
        + (HERE / f"scene_{concept}.json").read_text(encoding="utf-8")
        + ";\n"
        + (HERE / "mock_scene.js").read_text(encoding="utf-8")
    )
else:
    js = (HERE / f"mock_{concept}.js").read_text(encoding="utf-8") if concept != "now" else ""
# "//@include <file>" lines pull in another script (an idea that reuses another's builder with its
# own settings).
js = "\n".join(
    (HERE / line.split(" ", 1)[1].strip()).read_text(encoding="utf-8") if line.startswith("//@include ") else line
    for line in js.splitlines()
)

SIZES = [
    ("desk1440", 1440, 900, 1, 1),
    ("desk1920", 1920, 1080, 1, 1),
    ("desk1280", 1280, 720, 1, 1),
    ("desk1600", 1600, 1000, 1, 1),
    ("phone", 390, 844, 3, 2),
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
    only = sys.argv[4].split(",") if len(sys.argv) > 4 else None
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
        pg.goto(base + "/products/nuricell", wait_until="networkidle")
        pg.wait_for_timeout(2500)
        if js:
            pg.evaluate(js)
            pg.wait_for_timeout(1500)
        for i in range(screens):
            pg.evaluate(f"window.scrollTo(0,{i * h})")
            pg.wait_for_timeout(900)
            pg.screenshot(path=str(out / f"{concept}-{label}-{i}.png"))
        ctx.close()
    b.close()
print("done", concept)

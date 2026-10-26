"""Mock up a new "Why cellular health matters" chapter on the NuriCell page by changing the live
page in the browser, then screenshot the chapter as a visitor scrolls to it.

usage: python -X utf8 mock.py <idea> <outdir> [base-url] [sizes]
idea: now (changes nothing) | words (the tidied words, the lantern kept) | <art name> (the tidied
words and the lantern swapped for art/<art name>.png)
Pictures the mock needs are served from this folder's art/ through a route on /mock-art/. Once Mo
picked A (October 26, 2026), the samples' art/ and their shots/ moved to
codes/bigh-archive/nuricell-why-unused-2026-10-26/mockup-pngs/ (outside the public repo); the
compare page's pictures stay in page/. `now` against the built site shoots what was built (built/,
also moved there once its page pictures were made).
"""

import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
idea, out = sys.argv[1], Path(sys.argv[2])
base = sys.argv[3] if len(sys.argv) > 3 else "https://bigh-website-demo.vercel.app"
only = sys.argv[4].split(",") if len(sys.argv) > 4 else None
out.mkdir(parents=True, exist_ok=True)
js = ""
if idea != "now":
    js = (HERE / "words.js").read_text(encoding="utf-8")
if idea not in ("now", "words"):
    w, h = Image.open(HERE / "art" / f"{idea}.png").size
    # Both the unlit and the lit picture become the new painting (shown lit); the lantern's gold
    # mask goes; the width and height attributes take the new shape.
    js += f"""
(() => {{
  const fig = document.querySelector("[data-chapter=why] figure");
  fig.style.setProperty("--aspect", {w / h:.4f});
  fig.querySelectorAll("img").forEach((img) => {{
    img.removeAttribute("srcset");
    img.src = "/mock-art/{idea}.png";
    img.width = {w};
    img.height = {h};
  }});
  fig.querySelectorAll("span[style*='--gold']").forEach((s) => s.remove());
}})();
"""

# label, width, height, device pixel ratio
SIZES = [
    ("desk1440", 1440, 900, 1),
    ("desk1920", 1920, 1080, 1),
    ("desk1280", 1280, 720, 1),
    ("phone", 390, 844, 2),
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
        pg.wait_for_timeout(2000)
        if js:
            pg.evaluate(js)
            pg.wait_for_timeout(800)
        # Scroll the chapter in slowly so its bloom, count-up and light all run as for a visitor.
        # The chapter's first screen: its words and painting just under the menu bar.
        top = pg.evaluate(
            """Math.round(Math.min(...[...document.querySelectorAll('[data-chapter=why] figure, [data-chapter=why] [data-words]')]
                .map((e) => e.getBoundingClientRect().top)) + scrollY - 110)"""
        )
        for y in range(0, top, 400):
            pg.evaluate(f"window.scrollTo(0,{y})")
            pg.wait_for_timeout(120)
        pg.evaluate(f"window.scrollTo(0,{top})")
        pg.wait_for_timeout(6000)
        # Screens down the chapter: as many as it takes to reach its end.
        height = pg.evaluate(
            "Math.round(document.querySelector('[data-chapter=why]').getBoundingClientRect().height)"
        )
        i, y = 0, top
        while True:
            pg.evaluate(f"window.scrollTo(0,{y})")
            pg.wait_for_timeout(1500)
            pg.screenshot(path=str(out / f"{idea}-{label}-{i}.png"))
            i += 1
            y += h - 120
            if y >= top + height - 200 or i >= 4:
                break
        ctx.close()
    b.close()
print("done", idea)

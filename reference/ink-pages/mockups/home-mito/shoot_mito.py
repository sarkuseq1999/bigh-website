"""Shoot the built homepage with the "Tiny power plants." mitochondrion swapped for each new
colouring (November 4, 2026), by answering the page's own image request with the new picture.

    python -X utf8 shoot_mito.py [base-url]   (default http://localhost:3006)

Writes <look>-desk-flow.jpg (the opening, then the next screen, stitched as a visitor scrolls),
<look>-desk.jpg (the section) and <look>-phone.jpg for look in now, a, b.
"""

import io
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
ROOT = HERE.parents[3]
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3006"
LOOKS = {
    "now": None,
    "a": ROOT / "reference" / "ink-pages" / "home-mito" / "mito-a-v1.webp",
    "b": ROOT / "reference" / "ink-pages" / "home-mito" / "mito-b-v1.webp",
}


def swap(page, src):
    if src is None:
        return
    body = src.read_bytes()
    page.route(
        "**/_next/image?url=%2Fimages%2Fhome-v2%2Fink%2Fspring%2Fmito.webp*",
        lambda route: route.fulfill(status=200, content_type="image/webp", body=body),
    )


def settle(page, y, ms=4200):
    page.evaluate(f"window.scrollTo(0, {y})")
    page.wait_for_timeout(ms)


def main():
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=["--use-angle=d3d11"])
        for look, src in LOOKS.items():
            ctx = b.new_context(viewport={"width": 1440, "height": 900})
            p = ctx.new_page()
            swap(p, src)
            p.goto(BASE + "/", wait_until="networkidle", timeout=120000)
            p.wait_for_timeout(5000)
            top = p.screenshot()
            settle(p, 900)
            nxt = p.screenshot()
            flow = Image.new("RGB", (1440, 1800))
            flow.paste(Image.open(io.BytesIO(top)), (0, 0))
            flow.paste(Image.open(io.BytesIO(nxt)), (0, 900))
            flow.save(HERE / f"{look}-desk-flow.jpg", quality=86)
            y = p.evaluate("document.getElementById('cellular').getBoundingClientRect().top + scrollY")
            settle(p, y - 135)
            p.screenshot(path=str(HERE / f"{look}-desk.jpg"), type="jpeg", quality=88)
            ctx.close()

            ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2)
            p = ctx.new_page()
            swap(p, src)
            p.goto(BASE + "/", wait_until="networkidle", timeout=120000)
            p.wait_for_timeout(1500)
            fig = p.evaluate("document.querySelector('#cellular figure').getBoundingClientRect().top + scrollY")
            settle(p, fig - 120)
            p.screenshot(path=str(HERE / f"{look}-phone.jpg"), type="jpeg", quality=86)
            ctx.close()
            print("shot", look)
        b.close()


if __name__ == "__main__":
    main()

"""Shoot the homepage hummingbird's six wing frames on a real page, plus its first screen.

    python -X utf8 shoot_wings.py <base-url> <name>

For a laptop (1440 x 900) and a phone (390 x 844), both 2x: pauses every animation once the bird
has bloomed in, sets both wings to each of their six frames in turn, and shoots the bird with a
margin (<name>-<size>-f<k>.png), then the whole first screen at the beat's lowest frame
(<name>-<size>-screen.png). Prints where the wings' box ends in the bird's frame.
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
OUT = HERE / "shots"
SIZES = {"laptop": (1440, 900), "phone": (390, 844)}

FREEZE = """
*, *::before, *::after { animation-play-state: paused !important; transition: none !important; }
#top [data-wing] { animation: none !important; }
"""


def main():
    base, name = sys.argv[1].rstrip("/"), sys.argv[2]
    OUT.mkdir(exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=["--use-angle=d3d11"])
        for size, (w, h) in SIZES.items():
            ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=2)
            page = ctx.new_page()
            page.goto(base + "/", wait_until="networkidle")
            page.wait_for_timeout(6000)  # the bloom and the beat are over
            page.add_style_tag(content=FREEZE)
            bird = page.locator("#top [data-brush=crane] img").first
            b = bird.bounding_box()
            low = page.evaluate(
                """() => { const b = document.querySelector('#top [data-brush=crane] img').getBoundingClientRect();
                return [...document.querySelectorAll('#top [data-brush=crane] [data-wing]')].map(w =>
                  w.dataset.wing + ' ' + ((w.getBoundingClientRect().bottom - b.top) / b.height).toFixed(3) + ' ' +
                  getComputedStyle(w).backgroundImage.split('/').pop()); }"""
            )
            print(name, size, "bird", [round(v) for v in (b["x"], b["y"], b["width"], b["height"])], low)
            pad = 0.08 * b["width"]
            clip = {
                "x": max(0, b["x"] - pad),
                "y": max(0, b["y"] - pad),
                "width": b["width"] + 2 * pad,
                "height": b["height"] + 2 * pad,
            }
            for k in range(6):
                page.evaluate(
                    f"() => document.querySelectorAll('#top [data-wing]').forEach(w => w.style.backgroundPosition = '{k * 20}% 0')"
                )
                page.wait_for_timeout(80)
                page.screenshot(path=str(OUT / f"{name}-{size}-f{k}.png"), clip=clip)
            page.evaluate(
                "() => document.querySelectorAll('#top [data-wing]').forEach(w => w.style.backgroundPosition = '60% 0')"
            )
            page.wait_for_timeout(80)
            page.screenshot(path=str(OUT / f"{name}-{size}-screen.png"))
            ctx.close()
        browser.close()


if __name__ == "__main__":
    main()

"""Mock a painted end for About A's meadow on the public demo (October 28, 2026): swap in the
joined painting's two layers (route interception) and lay the painting past the fold by injected
CSS, then shoot the first screen and the steps a visitor scrolls through into Purpose.

    python -X utf8 reference/ink-pages/about-opening/shoot_join.py <take> [base-url]

Reads plates/join/<take>-base.webp and -gold.webp (join_foot.py join <take>); their height says
where the painting's original foot (row 1024 of 1536 wide) falls. ONLY=phone shoots one size.
Writes plates/join-shots/<take>/.
"""

import os
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
NAME = sys.argv[1]
BASE = sys.argv[2] if len(sys.argv) > 2 else "https://bigh-website-demo.vercel.app"
PLATES = HERE / "plates" / "join"
OUT = HERE / "plates" / "join-shots" / NAME
OUT.mkdir(parents=True, exist_ok=True)

BASE_IMG = (PLATES / f"{NAME}-base.webp").read_bytes()
GOLD_IMG = (PLATES / f"{NAME}-gold.webp").read_bytes()
W, H = Image.open(PLATES / f"{NAME}-base.webp").size
FOOT = 1024 / H  # the original's foot, as a share of the joined painting's height
_a = np.asarray(Image.open(PLATES / f"{NAME}-base.webp"))[..., 3] > 30
INK = (np.nonzero(_a.mean(axis=1) > 0.005)[0].max() + 1) / W  # last painted row, as a share of the width
print("ink ends at", round(INK * W), "rows; share of width", round(INK, 3))

# The painting is as wide as it must be for its original 3:2 part to cover the first screen; its
# sky is cut 30% of any excess (as the live page's object-position), so its original foot runs
# 70% of the excess below the fold, then the painted continuation runs on. Purpose moves down by
# what is painted below the fold, less 20px, so the last strokes end above the oak. The gold's
# bloom still starts from the original foot.
CSS = f"""
section[data-part="opening"][data-scene] {{ overflow: visible !important; overflow-x: clip !important; }}
section[data-part="opening"][data-scene] > div:first-child {{ inset: 0 0 auto 0 !important; height: 100% !important; overflow: visible !important; }}
section[data-part="opening"][data-scene] > div:first-child img {{
  inset: auto !important; left: 50% !important;
  top: calc((100svh - max(100vw, 150svh) / 1.5) * 0.3) !important;
  width: max(100vw, 150svh) !important; height: auto !important; max-width: none !important;
  object-fit: fill !important; transform: translateX(-50%);
}}
section[data-part="opening"][data-scene] > div:first-child img:nth-child(2) {{
  -webkit-mask-image: radial-gradient(ellipse 70% {60 * FOOT:.2f}% at 50% {100 * FOOT:.2f}%, #000 calc(var(--reach) - 30%), transparent var(--reach)) !important;
  mask-image: radial-gradient(ellipse 70% {60 * FOOT:.2f}% at 50% {100 * FOOT:.2f}%, #000 calc(var(--reach) - 30%), transparent var(--reach)) !important;
}}
[data-part="purpose"] {{ position: relative; margin-top: max(0px, calc(max(100vw, 150svh) * ({INK:.4f} - 0.2) - 70svh - 20px)); }}
"""

SIZES = {"desk": (1440, 900), "wide": (1920, 1000), "laptop": (1280, 720), "phone": (390, 844)}


def serve(route):
    url = route.request.url
    body = GOLD_IMG if "superbloom-gold-v1" in url else BASE_IMG
    route.fulfill(status=200, body=body, headers={"content-type": "image/webp", "cache-control": "no-store"})


if os.environ.get("ONLY"):
    SIZES = {k: v for k, v in SIZES.items() if k == os.environ["ONLY"]}

with sync_playwright() as p:
    browser = p.chromium.launch()
    for size, (w, h) in SIZES.items():
        ctx = browser.new_context(
            viewport={"width": w, "height": h}, device_scale_factor=2 if size == "phone" else 1,
            is_mobile=size == "phone", has_touch=size == "phone",
        )
        page = ctx.new_page()
        page.route("**/*superbloom*", serve)
        page.goto(BASE + "/about-a", wait_until="networkidle")
        page.add_style_tag(content=CSS)
        page.wait_for_timeout(5000)
        info = page.evaluate(
            """() => {
              const o = document.querySelector('section[data-part="opening"]').getBoundingClientRect();
              const img = document.querySelector('section[data-part="opening"] img').getBoundingClientRect();
              const oak = document.querySelector('[data-part="purpose"] img').getBoundingClientRect();
              return {fold: o.bottom + scrollY, imgTop: img.top + scrollY, imgBottom: img.bottom + scrollY,
                      oakTop: oak.top + scrollY};
            }"""
        )
        print(size, info)
        page.screenshot(path=str(OUT / f"{size}-0top.png"))
        for i, frac in enumerate((0.45, 0.75, 1.05, 1.35)):
            page.evaluate(f"window.scrollTo(0, {info['fold'] - h * (1 - frac)})")
            page.wait_for_timeout(900)
            page.screenshot(path=str(OUT / f"{size}-{i + 1}.png"))
        ctx.close()
    browser.close()

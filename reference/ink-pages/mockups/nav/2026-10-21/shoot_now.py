"""Screenshots of today's menu bar on the public demo: desktop top, settled, other pages, phone."""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "https://bigh-website-demo.vercel.app"
OUT = Path(__file__).parent / "now"
OUT.mkdir(exist_ok=True)

SHOTS = [
    ("home-top", "/", 0),
    ("home-settled", "/", 1400),
    ("about-top", "/about", 0),
    ("nuricell-top", "/products/nuricell", 0),
    ("science-top", "/science", 0),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    desk = browser.new_page(viewport={"width": 1536, "height": 900})
    for name, path, y in SHOTS:
        desk.goto(BASE + path, wait_until="networkidle", timeout=90000)
        desk.wait_for_timeout(3500)
        if y:
            desk.mouse.wheel(0, y)
            desk.wait_for_timeout(2500)
        desk.screenshot(path=str(OUT / f"{name}.png"))
        desk.screenshot(path=str(OUT / f"{name}-bar.png"), clip={"x": 0, "y": 0, "width": 1536, "height": 160})
    phone = browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    phone.goto(BASE + "/", wait_until="networkidle", timeout=90000)
    phone.wait_for_timeout(3500)
    phone.screenshot(path=str(OUT / "phone-home-top.png"))
    browser.close()
print("done", OUT)

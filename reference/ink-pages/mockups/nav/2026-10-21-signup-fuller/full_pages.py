"""Whole screens with each Sign up stroke swapped in, as a visitor sees them: the homepage and the
About page on a laptop, the homepage on a phone, and the phone menu open.

usage: python -X utf8 full_pages.py <base-url> <variant> [...]
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.argv, ARGS = sys.argv[:1], sys.argv[1:]
sys.path.insert(0, str(Path(__file__).parent))
import try_strokes as t  # noqa: E402  (its variants and stylesheet; it runs nothing without arguments)

BASE = ARGS[0].rstrip("/")
OUT = Path(__file__).parent / "pages"
OUT.mkdir(exist_ok=True)


def route(ctx):
    ctx.route("**/__mock/**", lambda r: r.fulfill(path=str(t.CUT / r.request.url.split("/__mock/")[1])))


with sync_playwright() as p:
    browser = p.chromium.launch()
    for variant in ARGS[1:]:
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        route(ctx)
        page = ctx.new_page()
        for name, path in (("home", "/"), ("about", "/about")):
            page.goto(BASE + path, wait_until="networkidle", timeout=120000)
            page.wait_for_timeout(3500)
            t.dress(page, variant)
            page.screenshot(path=str(OUT / f"{variant}-{name}.png"))
        ctx.close()
        ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
        route(ctx)
        page = ctx.new_page()
        page.goto(BASE + "/", wait_until="networkidle", timeout=120000)
        page.wait_for_timeout(3500)
        t.dress(page, variant)
        page.screenshot(path=str(OUT / f"{variant}-phone.png"))
        page.locator(t.MENU).tap()
        page.wait_for_timeout(1600)
        page.screenshot(path=str(OUT / f"{variant}-phone-menu.png"))
        ctx.close()
        print(variant, "done", flush=True)
    browser.close()

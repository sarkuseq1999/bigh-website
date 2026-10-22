"""Try Sign up strokes on the real menu bar: each variant's mask (and its own padding) is swapped in
over the site's own stroke, then the bar is photographed on a desktop, on a phone (Menu) and in the
phone menu's foot (Log in, Sign up).

usage: python -X utf8 try_strokes.py <base-url> <variant> [<variant> ...]
       a variant is "today" (the site as it is) or a name in VARIANTS
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip("/")
HERE = Path(__file__).parent
CUT = HERE / "cut"
OUT = HERE / "shots"
OUT.mkdir(exist_ok=True)

# name: (mask file, Sign up padding, Menu padding, the stroke's inset round its button)
VARIANTS = {
    "pill1": ("pill1.webp", "0 24px 2px", "0 21px 2px", "-2px -3px"),
    "pill2": ("pill2.webp", "0 24px 2px", "0 21px 2px", "-2px -3px"),
    "clean1": ("clean1.webp", "0 26px 2px", "0 22px 2px", "0 -4px"),
    "clean2": ("clean2.webp", "0 26px 2px", "0 22px 2px", "0 -4px"),
    "dry1": ("dry1.webp", "0 28px 2px", "0 24px 2px", "-4px -6px"),
    "dry2": ("dry2.webp", "0 28px 2px", "0 24px 2px", "-4px -6px"),
}

SIGNUP = '#site-navigation [class*="__account"] button, [data-nav-sheet] [class*="__sheetFoot"] button'
MENU = "[data-nav-menu-button]"


def css(variant):
    mask, pad, menu_pad, inset = VARIANTS[variant]
    return f"""
:is({SIGNUP})::before, {MENU}::before {{
  mask-image: url("/__mock/{mask}") !important; inset: {inset} !important; }}
:is({SIGNUP}) {{ padding: {pad} !important; }}
{MENU} {{ padding: {menu_pad} !important; }}
"""


def dress(page, variant):
    if variant != "today":
        page.add_style_tag(content=css(variant))
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(900)


with sync_playwright() as p:
    browser = p.chromium.launch()
    for variant in sys.argv[2:]:
        ctx = browser.new_context(viewport={"width": 1536, "height": 900}, device_scale_factor=2)
        ctx.route("**/__mock/**", lambda route: route.fulfill(path=str(CUT / route.request.url.split("/__mock/")[1])))
        page = ctx.new_page()
        page.goto(BASE + "/", wait_until="networkidle", timeout=120000)
        page.wait_for_timeout(3000)
        dress(page, variant)
        page.screenshot(path=str(OUT / f"{variant}-desk.png"), clip={"x": 0, "y": 0, "width": 1536, "height": 130})
        page.screenshot(path=str(OUT / f"{variant}-desk-zoom.png"), clip={"x": 1160, "y": 20, "width": 290, "height": 84})
        page.goto(BASE + "/products/nuricell", wait_until="networkidle", timeout=120000)
        page.wait_for_timeout(2500)
        dress(page, variant)
        page.screenshot(path=str(OUT / f"{variant}-nuricell.png"), clip={"x": 0, "y": 0, "width": 1536, "height": 900})
        ctx.close()

        ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
        ctx.route("**/__mock/**", lambda route: route.fulfill(path=str(CUT / route.request.url.split("/__mock/")[1])))
        page = ctx.new_page()
        page.goto(BASE + "/", wait_until="networkidle", timeout=120000)
        page.wait_for_timeout(3000)
        dress(page, variant)
        page.screenshot(path=str(OUT / f"{variant}-phone.png"), clip={"x": 0, "y": 0, "width": 390, "height": 90})
        page.locator(MENU).tap()
        page.wait_for_timeout(1500)
        page.evaluate("document.querySelector('[data-nav-sheet]').scrollTop = 99999")
        page.wait_for_timeout(800)
        foot = page.locator('[data-nav-sheet] [class*="__sheetFoot"]').bounding_box()
        page.screenshot(path=str(OUT / f"{variant}-phone-foot.png"), clip={"x": 0, "y": foot["y"] - 10, "width": 390, "height": foot["height"] + 20})
        ctx.close()
        print(variant, "done", flush=True)
    browser.close()

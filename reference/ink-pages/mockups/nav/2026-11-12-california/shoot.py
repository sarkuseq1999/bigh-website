"""Shoot the menu bar today and with mock-up CSS (A warm ink, B warm ink + golden ridge) on the
public demo. Nothing on the site changes: the CSS is laid over the built page in the browser.

    python -X utf8 shoot.py <variant> [variant ...]     (today, a, b)
"""

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "https://bigh-website-demo.vercel.app"
HERE = Path(__file__).parent
OUT = HERE / "shots"
OUT.mkdir(exist_ok=True)
X = "nav-inscription-module__KMPmia__"

WARM = "#5e4535"  # warm umber: cream letters on it 8:1
RIDGE = HERE / "ridge-strip.png"
RIDGE_W, RIDGE_H, RIDGE_V = 2172, 51, 0.361  # set from cut_ridge.py's output

WARM_CSS = f"""
.{X}root {{ --warm: {WARM}; }}
.{X}rule::before, .{X}ink::before, .{X}dab {{ background: var(--warm) !important; }}
/* Sign up and Menu: a loaded brush of umber, darkest where it lands, warmer as it thins out. */
.{X}account button::before, .{X}sheetFoot button::before,
.{X}root .{X}menuButton::before {{
  background: linear-gradient(90deg, #4a3226 0%, #5e4232 45%, #7a5640 100%) !important;
}}
.{X}word::after, .{X}account a::after, .{X}sheetFoot a::after {{ background: var(--warm) !important; }}
"""


def ridge_css():
    v = RIDGE_V * 100
    return f"""
.{X}rule {{
  aspect-ratio: {RIDGE_W} / {RIDGE_H} !important;
  min-height: 0 !important;
  translate: -50% -{v:.1f}% !important;
}}
.{X}root[data-settle][data-size="tall"] .{X}rule {{
  translate: -50% calc(-{v:.1f}% - var(--insc-dh) * var(--insc-g)) !important;
}}
.{X}root .{X}rule {{ opacity: 0.78; }}
/* The bar's paper runs on under the whole of the land's wash before it fades. */
.{X}root[data-ground="solid"] .{X}ground,
.{X}root[data-ground="settling"] .{X}ground {{ height: calc(var(--h) + 34px) !important; }}
.{X}rule::before {{
  background: url("/__mock/ridge.png") 0 0 / 100% 100% no-repeat !important;
  mask: none !important;
}}
"""


VARIANTS = {
    "today": "",
    "a": WARM_CSS,
    "b": WARM_CSS + ridge_css(),
}


def page_for(browser, css, w, h, dpr, mobile=False):
    ctx = browser.new_context(
        viewport={"width": w, "height": h},
        device_scale_factor=dpr,
        is_mobile=mobile,
        has_touch=mobile,
    )
    pg = ctx.new_page()
    if css:
        pg.add_init_script(
            "document.addEventListener('DOMContentLoaded',()=>{const s=document.createElement('style');"
            f"s.textContent={css!r};document.head.appendChild(s);}});"
        )
        pg.route(
            "**/__mock/ridge.png",
            lambda r: r.fulfill(path=str(RIDGE), content_type="image/png"),
        )
    return ctx, pg


def shoot(variant):
    css = VARIANTS[variant]
    with sync_playwright() as p:
        b = p.chromium.launch()

        ctx, pg = page_for(b, css, 1536, 864, 2)
        pg.goto(BASE + "/", wait_until="networkidle")
        time.sleep(5)
        pg.screenshot(path=OUT / f"{variant}-home.png")
        pg.evaluate("window.scrollTo(0, 1100)")
        time.sleep(2)
        pg.screenshot(path=OUT / f"{variant}-home-settled.png")
        pg.goto(BASE + "/about", wait_until="networkidle")
        time.sleep(4)
        pg.screenshot(path=OUT / f"{variant}-about.png")
        pg.screenshot(path=OUT / f"{variant}-about-bar.png", clip={"x": 0, "y": 0, "width": 1536, "height": 150})
        ctx.close()

        ctx, pg = page_for(b, css, 390, 844, 3, mobile=True)
        pg.goto(BASE + "/", wait_until="networkidle")
        time.sleep(5)
        pg.screenshot(path=OUT / f"{variant}-phone-home.png")
        pg.locator(f".{X}menuButton").first.click()
        time.sleep(2)
        pg.screenshot(path=OUT / f"{variant}-phone-menu.png")
        ctx.close()
        b.close()
    print("shot", variant)


if __name__ == "__main__":
    for v in sys.argv[1:]:
        shoot(v)

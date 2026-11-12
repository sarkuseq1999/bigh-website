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


# E, open air: the mark at the left, every word to its right, no brushwork in the bar at all.
OPEN_CSS = f"""
.{X}root .{X}bar {{ display: flex !important; align-items: center; }}
.{X}left, .{X}right {{ display: contents !important; }}
.{X}root .{X}bar a.{X}mark[href] {{ order: 0; }}
.{X}left > .{X}links, .{X}right > .{X}links, .{X}left > .{X}language, .{X}right > .{X}account {{
  margin-top: calc(var(--mark) * (0.175 - 2 * var(--lift)));
}}
.{X}left > .{X}links {{ order: 1; margin-left: auto; }}
.{X}right > .{X}links {{ order: 2; }}
.{X}left > .{X}language {{ order: 3; margin-left: var(--gap); }}
.{X}right > .{X}account {{ order: 4; }}
.{X}left > .{X}menuButton {{ order: 5; margin-left: 14px; }}
@media (max-width: 1100px) {{
  .{X}right > .{X}account {{ margin-left: auto; }}
}}
/* One fine sepia hairline instead of the painted rule. */
.{X}rule {{ aspect-ratio: auto !important; height: 1px !important; min-height: 1px !important; }}
.{X}root .{X}rule {{ opacity: 1; }}
.{X}rule::before {{ mask: none !important; background: #d3c6b3 !important; }}
/* You are here: a plain 2px ink line. */
.{X}ink::before {{ mask: none !important; inset: auto 0 0 0 !important; height: 2px !important; background: currentColor !important; }}
.{X}dab {{ mask: none !important; height: 1px !important; width: 56px !important; background: #cdbfac !important; opacity: 1 !important; }}
/* Sign up and Menu: the page's own ink pill, like "Discover NuriCell". */
.{X}account button::before, .{X}sheetFoot button::before, .{X}root .{X}menuButton::before {{
  mask: none !important; inset: 0 !important; border-radius: 999px !important; background: var(--ink) !important;
}}
.{X}root :is(.{X}account, .{X}sheetFoot) button {{ padding: 0 24px 1px !important; }}
.{X}root .{X}menuButton {{ padding: 0 20px 1px !important; min-height: 44px; }}
"""

# C, poppy: Sign up and Menu on a watercolour swatch of California-poppy orange (ink letters), the
# page you're on marked by a soft poppy dash; the rest of the bar in A's warm ink.
POPPY_CSS = WARM_CSS + f"""
.{X}account button::before, .{X}sheetFoot button::before {{
  mask: none !important;
  background: url("/__mock/poppy-swatch.png") center / 100% 100% no-repeat !important;
}}
.{X}root :is(.{X}account, .{X}sheetFoot) button {{ color: var(--ink) !important; }}
.{X}ink::before {{
  mask: none !important;
  background: url("/__mock/poppy-dash.png") 0 50% / 100% 100% no-repeat !important;
}}
"""

# D, sky strip: the bar is a slim painting of a California morning, its hills at the bar's foot and
# the words in its sky; the marks in A's warm ink.
SKY_H = "calc((var(--h) - 12px) / 0.58)"
SKY_CSS = WARM_CSS + f"""
.{X}rule {{
  left: 0 !important; top: 0 !important; width: 100% !important; height: {SKY_H} !important;
  min-height: 0 !important; aspect-ratio: auto !important; translate: none !important; mask: none !important;
}}
.{X}root[data-settle][data-size="tall"] .{X}rule {{
  translate: 0 round(calc(-1 * var(--insc-dh) * var(--insc-g)), 1px) !important;
}}
.{X}root .{X}rule {{ opacity: 1; }}
.{X}rule::before {{ mask: none !important; background: url("/__mock/sky.png") 50% 0 / cover no-repeat !important; }}
@media (max-width: 1100px) {{
  .{X}rule::before {{ background-position: 6% 0 !important; }}
}}
.{X}root[data-ground="solid"] .{X}ground,
.{X}root[data-ground="settling"] .{X}ground {{ height: {SKY_H} !important; }}
"""

VARIANTS = {
    "today": "",
    "a": WARM_CSS,
    "b": WARM_CSS + ridge_css(),
    "c": POPPY_CSS,
    "d": SKY_CSS,
    "e": OPEN_CSS,
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
            "**/__mock/*",
            lambda r: r.fulfill(
                path=str(HERE / "mock" / r.request.url.rsplit("/", 1)[1]),
                content_type="image/png",
            ),
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

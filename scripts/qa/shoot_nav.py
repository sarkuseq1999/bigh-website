"""Screenshots of one menu bar option (October 5, 2026 review), the same set for every option.

usage: python -X utf8 scripts/qa/shoot_nav.py <a|b|c|today> [--base http://localhost:3027]
       [--out scripts/qa/out/nav] [--only desk|phone|tablet] [--locale en|vn|jp|kr|cns]

Contract the options keep, so this script can drive them:
  [data-nav-trigger="products"|"science"]  the desktop drop-down buttons
  [data-nav-panel="products"|"science"]    their panels
  [data-nav-menu-button]                   the narrow window's menu button
  [data-nav-sheet]                         the open menu sheet
  [data-nav-sheet-toggle="products"]       (optional) the sheet's Products disclosure
Writes PNGs to <out>/<option>/ and prints any console errors.
"""

import argparse
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument("option")
ap.add_argument("--base", default="http://localhost:3027")
ap.add_argument("--out", default="scripts/qa/out/nav")
ap.add_argument("--only", default="")
ap.add_argument("--locale", default="en")
args = ap.parse_args()

opt = args.option
prefix = "" if args.locale == "en" else f"/{args.locale}"
query = "?rec=1" if opt == "today" else f"?nav={opt}&rec=1"
url = f"{args.base}{prefix}/{query}"
out = Path(args.out) / (opt if args.locale == "en" else f"{opt}-{args.locale}")
out.mkdir(parents=True, exist_ok=True)
errors: list[str] = []


def watch(page):
    page.on("console", lambda m: m.type == "error" and errors.append(m.text[:300]))
    page.on("pageerror", lambda e: errors.append(str(e)[:300]))


def settle(page, ms=1200):
    page.wait_for_timeout(ms)


def scroll_to(page, y):
    page.evaluate(f"window.scrollTo(0, {y})")
    page.mouse.wheel(0, 1)
    settle(page, 1600)


with sync_playwright() as p:
    browser = p.chromium.launch(args=["--use-angle=d3d11"])

    if args.only in ("", "desk"):
        for width, height, tag in ((1536, 900, ""), (1280, 800, "-1280"), (1920, 1080, "-1920")):
            page = browser.new_page(viewport={"width": width, "height": height})
            watch(page)
            page.goto(url, wait_until="networkidle")
            settle(page, 3500)
            page.screenshot(path=str(out / f"desk{tag}-top.png"))
            if tag:
                page.close()
                continue
            for panel in ("products", "science"):
                trigger = page.locator(f'[data-nav-trigger="{panel}"]').first
                if trigger.count():
                    trigger.hover()
                    settle(page, 1500)
                    page.screenshot(path=str(out / f"desk-top-{panel}.png"))
            page.mouse.move(760, 880)
            settle(page, 900)
            scroll_to(page, 1500)
            page.screenshot(path=str(out / "desk-scrolled.png"))
            trigger = page.locator('[data-nav-trigger="products"]').first
            if trigger.count():
                trigger.hover()
                settle(page, 1500)
                page.screenshot(path=str(out / "desk-scrolled-products.png"))
                page.mouse.move(760, 880)
                settle(page, 900)
            scroll_to(page, 1200)  # scrolling back up a little
            page.screenshot(path=str(out / "desk-scrolled-up.png"))
            page.close()

    if args.only in ("", "phone"):
        page = browser.new_page(
            viewport={"width": 390, "height": 844},
            device_scale_factor=2,
            is_mobile=True,
            has_touch=True,
        )
        watch(page)
        page.goto(url, wait_until="networkidle")
        settle(page, 3000)
        page.screenshot(path=str(out / "phone-top.png"))
        scroll_to(page, 1400)
        page.screenshot(path=str(out / "phone-scrolled.png"))
        scroll_to(page, 0)
        button = page.locator("[data-nav-menu-button]").first
        if button.count():
            button.click()
            settle(page, 1500)
            page.screenshot(path=str(out / "phone-menu.png"))
            toggle = page.locator('[data-nav-sheet-toggle="products"]').first
            if toggle.count():
                toggle.click()
                settle(page, 1200)
                page.screenshot(path=str(out / "phone-menu-products.png"))
        page.close()

    if args.only in ("", "tablet"):
        page = browser.new_page(viewport={"width": 834, "height": 1112}, device_scale_factor=1)
        watch(page)
        page.goto(url, wait_until="networkidle")
        settle(page, 3000)
        page.screenshot(path=str(out / "tablet-top.png"))
        button = page.locator("[data-nav-menu-button]").first
        if button.count():
            button.click()
            settle(page, 1500)
            page.screenshot(path=str(out / "tablet-menu.png"))
        page.close()

    browser.close()

print(f"wrote {out}")
if errors:
    print("CONSOLE ERRORS:")
    for e in errors:
        print(" -", e)
    sys.exit(1)

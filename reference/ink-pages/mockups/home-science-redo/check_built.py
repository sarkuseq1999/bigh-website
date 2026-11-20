"""Capture the built lantern paintings on the real page (no browser overrides), with the moving states.

Usage: python -X utf8 check_built.py <base-url>
Writes built/<width>-<state>.jpg for 1440x1000 and 390x844 and asserts both lantern pictures
are the ones shown, fully decoded, with their new lines, no sideways overflow and no page errors.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
OUT = HERE / (sys.argv[2] if len(sys.argv) > 2 else "built")
OUT.mkdir(exist_ok=True)
BASE = sys.argv[1]
TOPICS = ["Mitochondria", "Free radicals"]
ART = ["lantern-fuel-v1.webp", "lantern-soot-v1.webp"]
LINES = ["fuel goes in, and the flame turns it into light", "Every flame leaves a little soot"]

with sync_playwright() as p:
    browser = p.chromium.launch(
        args=["--use-gl=angle", "--use-angle=d3d11", "--enable-gpu", "--ignore-gpu-blocklist"]
    )
    for width, height in [(1440, 1000), (390, 844)]:
        context = browser.new_context(
            viewport={"width": width, "height": height},
            is_mobile=width < 900,
            has_touch=width < 900,
            device_scale_factor=2 if width < 900 else 1,
        )
        page = context.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(BASE, wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        assert page.locator('#science img[src*="workshop"]').count() == 0, "an old workshop picture is still on the page"
        page.locator("#science-title").evaluate(
            "(e) => scrollTo(0, scrollY + e.getBoundingClientRect().top - 110)"
        )
        page.wait_for_timeout(600)
        page.screenshot(path=str(OUT / f"{width}-arriving.jpg"), type="jpeg", quality=90)
        page.wait_for_timeout(3000)
        for i in [0, 1, 0]:
            page.locator("#science button").filter(has_text=TOPICS[i]).first.click()
            for ms in (350, 900):
                page.wait_for_timeout(ms if ms == 350 else 550)
                page.screenshot(path=str(OUT / f"{width}-to-{i}-{ms}ms.jpg"), type="jpeg", quality=88)
            page.wait_for_timeout(3000)
            if width < 900:
                page.locator("#science [role=tablist]").evaluate(
                    "(e) => scrollTo(0, scrollY + e.getBoundingClientRect().top - 100)"
                )
                page.wait_for_timeout(400)
                figure = page.locator(f"#ink-topic-panel-{i} figure")
            else:
                figure = page.locator("#science figure").first
            art = figure.locator(f'img[src$="{ART[i]}"]')
            assert art.evaluate("(i) => i.complete && i.naturalWidth === 1448"), f"{ART[i]} not decoded"
            assert art.evaluate("(i) => +getComputedStyle(i).opacity") == 1, f"{ART[i]} not shown"
            assert LINES[i] in figure.inner_text() or LINES[i] in page.locator("#science").inner_text(), LINES[i]
            assert not page.evaluate("document.documentElement.scrollWidth > innerWidth"), "sideways overflow"
            page.screenshot(path=str(OUT / f"{width}-topic-{i}.jpg"), type="jpeg", quality=90)
        assert not errors, errors
        print(f"{width}px: both lantern pictures decoded and shown, lines present, no overflow, no page errors", flush=True)
        context.close()
    browser.close()

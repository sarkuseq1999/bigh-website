"""Desktop and phone review plates for the Propolis design, including its gold transition."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3007"
ROUND = sys.argv[2] if len(sys.argv) > 2 else "before"
OUT = Path(__file__).resolve().parent / "out" / "propolis-design" / ROUND
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    for width, height in [(1440, 1000), (390, 844)]:
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(BASE + "/en/products/green-bee-propolis", wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(3200)
        page.screenshot(path=str(OUT / f"{width}-opening.png"))
        for chapter in ["why", "inside", "research", "daily", "buy"]:
            page.locator(f'[data-chapter="{chapter}"]').evaluate("e => window.scrollTo({top: e.offsetTop - 110, behavior: 'instant'})")
            page.wait_for_timeout(600)
            if chapter == "why":
                page.screenshot(path=str(OUT / f"{width}-why-arriving.png"))
                page.wait_for_timeout(3200)
                page.screenshot(path=str(OUT / f"{width}-why-filling.png"))
                page.wait_for_timeout(5200)
            else:
                page.wait_for_timeout(4800)
            page.screenshot(path=str(OUT / f"{width}-{chapter}.png"))
            if width < 500:
                page.locator(f'[data-chapter="{chapter}"] [data-words]').evaluate("e => window.scrollBy({top: e.getBoundingClientRect().top - 120, behavior: 'instant'})")
                page.wait_for_timeout(2000)
                page.screenshot(path=str(OUT / f"{width}-{chapter}-words.png"))
        for section in ["questions", "more"]:
            page.locator(f'#{section}').evaluate("e => window.scrollTo({top: e.offsetTop - 110, behavior: 'instant'})")
            page.wait_for_timeout(800)
            page.screenshot(path=str(OUT / f"{width}-{section}.png"))
        page.evaluate("window.scrollTo({top: document.body.scrollHeight, behavior: 'instant'})")
        page.wait_for_timeout(3200)
        page.screenshot(path=str(OUT / f"{width}-footer.png"))
        page.screenshot(path=str(OUT / f"{width}-full.png"), full_page=True)
        print({"width": width, "errors": errors, "output": str(OUT)}, flush=True)
        page.close()
    browser.close()

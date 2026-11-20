"""Mock new science paintings on the real homepage (browser-only swap; no site file changes).

Usage: python -X utf8 shoot.py <base-url> <key> [fuel.png sparks.png ["caption 0" "caption 1"]]
  key "now" with no pictures captures the page as it is.
Writes shots/<key>-<width>-<topic>.jpg for 1440x1000 and 390x844, topics 0 and 1.
"""
import base64
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
OUT = HERE / "shots"
OUT.mkdir(exist_ok=True)
BASE = sys.argv[1]
KEY = sys.argv[2]
ART = [Path(a) for a in sys.argv[3:5]]
LINES = sys.argv[5:7]
TOPICS = ["Mitochondria", "Free radicals"]
MATCH = ["workshop-fuel", "workshop-sparks"]

SWAP = """([urls, lines]) => {
  const match = ['workshop-fuel', 'workshop-sparks'];
  match.forEach((m, i) => {
    document.querySelectorAll(`#science img[src*="${m}"], #science img[data-mock="${i}"]`).forEach((img) => {
      img.dataset.mock = String(i);
      img.loading = 'eager';
      img.removeAttribute('srcset');
      img.src = urls[i];
    });
  });
  window.__mockLines = lines;
}"""

# The caption under the painting changes with the topic; rewrite it after each topic change.
CAPTION = """([i, lines]) => {
  if (!lines || !lines[i]) return;
  const old = ['food is the fuel', 'Most sparks are caught'][i];
  document.querySelectorAll('#science p, #science figcaption, #science span').forEach((el) => {
    if (el.children.length === 0 && el.textContent.includes(old)) el.textContent = lines[i];
  });
}"""


def data_url(path: Path) -> str:
    kind = {".png": "png", ".jpg": "jpeg", ".webp": "webp"}[path.suffix]
    return f"data:image/{kind};base64," + base64.b64encode(path.read_bytes()).decode()


with sync_playwright() as p:
    browser = p.chromium.launch(
        args=["--use-gl=angle", "--use-angle=d3d11", "--enable-gpu", "--ignore-gpu-blocklist"]
    )
    urls = [data_url(a) for a in ART]
    for width, height in [(1440, 1000), (390, 844)]:
        context = browser.new_context(
            viewport={"width": width, "height": height},
            is_mobile=width < 900,
            has_touch=width < 900,
            device_scale_factor=2 if width < 900 else 1,
        )
        page = context.new_page()
        page.goto(BASE, wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        if urls:
            page.evaluate(SWAP, [urls, LINES])
            page.wait_for_function(
                """() => [...document.querySelectorAll('#science img[data-mock]')]
                     .every((i) => i.complete && i.naturalWidth > 0)""",
                timeout=20000,
            )
        page.locator("#science-title").evaluate(
            "(e) => scrollTo(0, scrollY + e.getBoundingClientRect().top - 110)"
        )
        page.wait_for_timeout(3400)
        for i, topic in enumerate(TOPICS):
            page.locator("#science button").filter(has_text=topic).first.click()
            page.wait_for_timeout(3600)
            if width < 900:
                page.locator("#science [role=tablist]").evaluate(
                    "(e) => scrollTo(0, scrollY + e.getBoundingClientRect().top - 100)"
                )
                page.wait_for_timeout(400)
            if urls:
                page.evaluate(SWAP, [urls, LINES])
                page.evaluate(CAPTION, [i, LINES])
                page.wait_for_timeout(300)
            over = page.evaluate("document.documentElement.scrollWidth > innerWidth")
            page.screenshot(path=str(OUT / f"{KEY}-{width}-{i}.jpg"), type="jpeg", quality=90)
            print(f"{KEY} {width} topic {i}: captured; overflow={over}", flush=True)
        context.close()
    browser.close()

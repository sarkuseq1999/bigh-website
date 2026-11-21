"""Capture the actual built section and export an interactive, English-only art review."""
import base64
import sys
from html import escape
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "package.json").is_file())
ART = ROOT / "reference/ink-pages/nuricell/originals/research-berkeley-shelf-v1.png"
OUT = HERE / "preview"
OUT.mkdir(exist_ok=True)
Image.open(ART).save(OUT / "shelf.webp", quality=88, method=6)
URI = "data:image/webp;base64," + base64.b64encode((OUT / "shelf.webp").read_bytes()).decode()
SECTION = '[data-chapter="research"]'
STYLE = (HERE / "painting.css").read_text()
URL = sys.argv[1].rstrip("/") + "/products/nuricell"


def on_page(pg, y):
    pg.locator(SECTION).locator("h2").evaluate("(el,gap) => window.scrollBy(0, el.getBoundingClientRect().top-gap)", y)
    pg.wait_for_timeout(1200)


def book_point(pg, i):
    return pg.locator(SECTION).locator("img").evaluate("""(el,i) => {
      const r=el.getBoundingClientRect();
      const xs=[198,368,535,705,868,1029,1225];
      const x=r.left+r.width*xs[i]/1402, y=r.top+r.height*.66;
      if (document.elementFromPoint(x,y)?.dataset.book !== String(i+1)) throw Error('Wrong target for book '+(i+1));
      return [x,y]
    }""", i)


def portable(pg):
    # Retain the real section and its ancestor classes so all responsive rules apply.
    html = pg.locator(SECTION).evaluate("""section => {
      const node = section.cloneNode(true);
      node.querySelector('img').src='shelf.webp';
      node.querySelector('img').removeAttribute('data-bloom');
      let tree=node;
      for(let el=section.parentElement; el && el!==document.body; el=el.parentElement) {
        const shell=el.cloneNode(false); shell.append(tree); tree=shell;
      }
      return tree.outerHTML;
    }""")
    css = pg.evaluate("""() => Array.from(document.styleSheets, sheet => Array.from(sheet.cssRules, r => r.cssText).join('\\n')).join('\\n')""")
    body_class = escape(pg.locator("body").get_attribute("class") or "", quote=True)
    html_class = escape(pg.locator("html").get_attribute("class") or "", quote=True)
    css += """ [data-look="ink"] [data-chapter="research"] {padding-block:clamp(28px,5vw,72px)}
      [data-look="ink"] [data-chapter="research"] figure {top:24px} html {scroll-padding-top:16px}
      [data-look="ink"] {min-height:100svh} """
    js = (HERE / "studies.js").read_text()
    (OUT / "index.html").write_text(f'''<!doctype html><html lang="en" class="{html_class}"><head>
      <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
      <title>NuriCell research · Berkeley bookshelf preview</title>
      <style>{css}</style></head><body class="{body_class}">{html}<script>{js}</script></body></html>''', encoding="utf-8")


with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for name, width, height in [("desktop", 1440, 1000), ("phone", 390, 844)]:
        mobile = name == "phone"
        pg = browser.new_page(viewport={"width": width, "height": height}, has_touch=mobile, is_mobile=mobile)
        pg.goto(URL, wait_until="domcontentloaded", timeout=90000)
        pg.locator(SECTION).wait_for(state="attached")
        pg.evaluate("document.fonts.ready")
        pg.add_style_tag(content=STYLE)
        pg.evaluate((HERE / "painting.js").read_text() + "\n(source => placePainting(source))", URI)
        pg.locator(SECTION).locator("img").evaluate("img => img.decode()")
        on_page(pg, 112)
        pg.locator(SECTION + ' img[data-bloom="done"]').wait_for(state="visible")
        pg.wait_for_timeout(400)
        pg.screenshot(path=OUT / f"{name}.jpg", quality=91)
        if not mobile:
            portable(pg)
        for i, row in enumerate([0, 1, 2, 2, 3, 4, 5]):
            on_page(pg, 112)
            x,y = book_point(pg, i)
            if mobile:
                pg.touchscreen.tap(x,y)
            else:
                pg.mouse.click(x,y)
                pg.mouse.move(width-4, height-4)
            if i == 2:
                pg.wait_for_timeout(220)
                pg.screenshot(path=OUT / f"{name}-switching.jpg", quality=89)
            pg.wait_for_timeout(1250)
            selected = pg.locator(SECTION + " [data-study][data-open]")
            assert selected.count() == 1 and selected.locator("button").get_attribute("aria-controls") == f"research-answer-{row}"
            if i == 2:
                pg.screenshot(path=OUT / f"{name}-reviews.jpg", quality=91)
        print(f"{name}: seven painted books opened the correct rows", flush=True)
        pg.close()
    browser.close()

"""QA for the closing block: the three looks render, the buttons work, nothing overflows, no errors."""
import sys
from playwright.sync_api import sync_playwright
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3007"
LOCALES = sys.argv[2].split(",") if len(sys.argv) > 2 else ["", "kr"]
results = []
def check(name, ok, detail=""):
    results.append(ok)
    print(("PASS " if ok else "FAIL ") + name + ("  [" + detail + "]" if detail else ""))
with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    for loc in LOCALES:
        for w, h, tag in ((1440, 900, "desk"), (390, 844, "phone")):
            for n, expect in (("1", "space"), ("2", "light"), ("3", "field")):
                page = b.new_page(viewport={"width": w, "height": h})
                problems = []
                page.on("pageerror", lambda e: problems.append("pageerror " + str(e)[:120]))
                page.on("console", lambda m: problems.append("console " + m.text[:120]) if m.type == "error" else None)
                page.on("response", lambda r: problems.append(f"{r.status} {r.url[-60:]}") if r.status >= 400 else None)
                page.goto(f"{BASE}/{loc}?closing={n}", wait_until="networkidle")
                page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
                page.evaluate("document.getElementById('start').scrollIntoView({block: 'start'})")
                page.wait_for_timeout(2400)
                state = page.evaluate("""(() => { const s = document.getElementById('start'); const words = [...s.querySelectorAll('[data-words] > *')];
                  return {design: s.dataset.design, title: s.querySelector('h2').textContent, visible: words.every(e => +getComputedStyle(e).opacity > 0.95),
                    products: !!document.getElementById('products'), overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
                    footerTop: !!document.querySelector('footer h2'), canvas: !!s.querySelector('canvas'), img: !!s.querySelector('img')}; })()""")
                page.locator("#start button").first.click()
                page.wait_for_timeout(600)
                dialog = page.locator("dialog[open] h2").inner_text() if page.locator("dialog[open]").count() else None
                page.keyboard.press("Escape")
                page.wait_for_timeout(300)
                ok = (state["design"] == expect and state["visible"] and state["products"] and state["overflow"] == 0
                      and not state["footerTop"] and bool(dialog) and not problems and len(state["title"]) > 5)
                check(f"{loc or 'en'}-{tag}-{n}: {expect} renders, words shown, Discover NuriCell opens the product, #products exists, no overflow/errors, footer headline gone",
                      ok, f"{state} dialog={dialog!r} {problems[:2]}")
                page.close()
    b.close()
print(f"\n{sum(results)} passed, {len(results) - sum(results)} failed")

"""QA for the menu bar, "Inscription" (Mo's pick, October 5, 2026), on the homepage.

usage: python -X utf8 scripts/qa/qa_nav.py [base] [--only=desk|phone|tablet|lang]
       base defaults to http://localhost:3014

On the real GPU (ANGLE/D3D11):
  - desktop 1536x900: the bar's links (Products, Science, About, Support; no "Home": the mark goes
    home), the mark centred in the window and at least 120 px wide over the opening, words at
    least 18 px and every control at least 48 px tall; Products opens on hover, the pointer can
    cross into it, Science swaps in without rolling the scroll up again, leaving closes it and it
    rolls back up, its pictures loaded (they wait until the pointer reaches the bar); a click toggles; a click on the wash closes it (and doesn't scroll the page);
    Enter opens, Tab steps into the panel, Escape closes and hands focus back; the Tab order
    follows the line; a visible ring on the keyboard's focus; Support opens its sheet; scrolled,
    the bar settles small with its painted rule; a product link goes to its page.
  - reduced motion: the scroll is down at once.
  - phone 390x844: the menu opens and locks the page, the button says Close, Escape closes it and
    hands focus back, the Close button closes it, Products and Science fold open one at a time,
    Support opens its sheet, a product link goes to its page.
  - tablet 834x1112: the menu opens with Products unfolded.
  - Vietnamese and Japanese at 1101 and 1280 px: the bar's three groups stay apart and inside the
    window.
  - no page errors or console errors anywhere.
Pictures land in scripts/qa/out/nav/.
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = (ARGS[0] if ARGS else "http://localhost:3014").rstrip("/")
ONLY = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--only=")), None)
OUT = Path(__file__).parent / "out" / "nav"
OUT.mkdir(parents=True, exist_ok=True)
URL = f"{BASE}/"
results: list[tuple[str, bool]] = []
errors: list[str] = []


def check(name, ok, detail=""):
    results.append((name, bool(ok)))
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail != "" else ""))


def watch(page):
    page.on("pageerror", lambda e: errors.append(f"{page.url} {e}"[:300]))
    page.on("console", lambda m: m.type == "error" and errors.append(f"{page.url} {m.text}"[:300]))


def r_value(page):
    return page.evaluate(
        "getComputedStyle(document.querySelector('header')).getPropertyValue('--insc-r').trim()"
    )


def is_open(page, panel):
    return page.evaluate(
        f"document.querySelector('[data-nav-panel=\"{panel}\"]').hasAttribute('data-open')"
    )


def focused(page):
    return page.evaluate(
        """() => { const e = document.activeElement; if (!e) return 'none';
        return (e.getAttribute('aria-label') || e.textContent || e.tagName).trim().slice(0, 40); }"""
    )


def menu_open(page):
    return page.evaluate("document.querySelector('header').hasAttribute('data-menu')")


def desktop(browser):
    page = browser.new_page(viewport={"width": 1536, "height": 900})
    watch(page)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(2500)
    page.screenshot(path=str(OUT / "desk-top.png"))

    bar = page.evaluate(
        """() => {
      const nav = document.querySelector('#site-navigation');
      const shown = el => { const r = el.getBoundingClientRect(); const s = getComputedStyle(el);
        return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
      const words = [...nav.querySelectorAll('[data-nav-trigger], a, button')]
        .filter(el => shown(el) && !el.closest('[data-nav-panel], [data-nav-sheet]'))
        .map(el => ({ text: (el.innerText || el.getAttribute('aria-label') || '').trim(),
          size: parseFloat(getComputedStyle(el).fontSize), h: el.getBoundingClientRect().height }));
      const select = [...nav.querySelectorAll('select')].filter(shown)
        .map(el => el.closest('label') || el)
        .map(el => ({ text: 'language', size: parseFloat(getComputedStyle(el).fontSize),
          h: el.getBoundingClientRect().height }));
      const mark = nav.querySelector('[data-nav-logo]').getBoundingClientRect();
      return { words: words.concat(select), mark: { x: mark.x + mark.width / 2, w: mark.width },
        width: innerWidth };
    }"""
    )
    texts = [w["text"] for w in bar["words"]]
    check(
        "desk: the bar's links (no Home; the mark goes home)",
        all(t in texts for t in ("Products", "Science", "About", "Support", "Log in", "Sign up"))
        and "Home" not in texts,
        texts,
    )
    check(
        "desk: the mark centred and clearly visible",
        abs(bar["mark"]["x"] - bar["width"] / 2) < 4 and bar["mark"]["w"] >= 120,
        bar["mark"],
    )
    small = [w for w in bar["words"] if w["text"] and w["text"] != "BiGH home" and w["size"] < 18]
    check("desk: words at least 18 px", not small, small)
    short = [w for w in bar["words"] if w["h"] < 47.5]
    check("desk: every control at least 48 px tall", not short, short)

    waiting = page.evaluate(
        "[...document.querySelectorAll('[data-nav-panel] img')].filter(i => i.complete && i.naturalWidth > 0).length"
    )
    check("desk: the drop-downs' pictures wait until the visitor reaches for the bar", waiting == 0, waiting)

    trig = page.locator('[data-nav-trigger="products"]')
    trig.hover()
    page.wait_for_timeout(400)
    check("desk: hover opens Products", is_open(page, "products"))
    check("desk: its button says it is open", trig.get_attribute("aria-expanded") == "true")
    page.wait_for_timeout(900)
    check("desk: the scroll is unrolled", r_value(page) == "1", r_value(page))
    unloaded = page.evaluate(
        "[...document.querySelectorAll('[data-nav-panel=products] img')].filter(i => !i.complete || i.naturalWidth === 0).map(i => i.currentSrc || i.src)"
    )
    check("desk: every picture on the unrolled Products has loaded", not unloaded, unloaded[:3])
    page.screenshot(path=str(OUT / "desk-products.png"))
    box = page.locator('[data-nav-panel="products"] a').first.bounding_box()
    page.mouse.move(box["x"] + box["width"] / 2, box["y"] + 40, steps=8)
    page.wait_for_timeout(700)
    check("desk: the pointer can cross into the panel", is_open(page, "products"))
    page.locator('[data-nav-trigger="science"]').hover()
    samples = []
    for _ in range(6):
        page.wait_for_timeout(60)
        samples.append(float(r_value(page) or 0))
    check(
        "desk: Science swaps in", is_open(page, "science") and not is_open(page, "products")
    )
    check("desk: the swap keeps the scroll down", min(samples) > 0.99, samples)
    page.wait_for_timeout(900)
    page.screenshot(path=str(OUT / "desk-science.png"))
    page.mouse.move(760, 860, steps=6)
    page.wait_for_timeout(800)
    check("desk: leaving closes it", not is_open(page, "science"))
    page.wait_for_timeout(500)
    check("desk: the scroll rolls back up", float(r_value(page) or 1) < 0.01, r_value(page))

    page.locator('[data-nav-trigger="science"]').click()
    page.wait_for_timeout(300)
    check("desk: a click opens Science", is_open(page, "science"))
    page.locator('[data-nav-trigger="science"]').click()
    page.wait_for_timeout(300)
    check("desk: a second click closes it", not is_open(page, "science"))

    page.locator('[data-nav-trigger="products"]').click()
    page.wait_for_timeout(900)
    page.mouse.move(760, 860)
    page.mouse.click(760, 860)
    page.wait_for_timeout(400)
    check("desk: a click on the wash closes it", not is_open(page, "products"))
    check("desk: ...without scrolling the page", page.evaluate("scrollY") < 5, page.evaluate("scrollY"))

    page.mouse.move(760, 600)
    page.locator('[data-nav-trigger="products"]').focus()
    page.keyboard.press("Enter")
    page.wait_for_timeout(300)
    check("desk: Enter opens Products", is_open(page, "products"))
    page.keyboard.press("Tab")
    f = focused(page)
    check("desk: Tab steps into the panel", "NuriCell" in f, f)
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    f = focused(page)
    check(
        "desk: Escape closes it and hands focus back",
        not is_open(page, "products") and "Products" in f,
        f,
    )

    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(2000)
    order = []
    ring = ""
    for _ in range(10):
        page.keyboard.press("Tab")
        order.append(focused(page))
        if "Products" in order[-1]:
            ring = page.evaluate(
                "(() => { const s = getComputedStyle(document.activeElement); "
                "return s.outlineStyle + ' ' + s.outlineWidth; })()"
            )
    check(
        "desk: the Tab order follows the line",
        order[1].startswith("Choose language")
        and "Products" in order[2]
        and "Science" in order[3]
        and "BiGH home" in order[4]
        and "About" in order[5]
        and "Support" in order[6]
        and "Log in" in order[7],
        " | ".join(order),
    )
    check(
        "desk: a visible ring on the keyboard's focus",
        ring.startswith(("solid", "auto")) and not ring.endswith(" 0px"),
        ring,
    )

    page.locator("#site-navigation").get_by_role("button", name="Support").click()
    page.wait_for_timeout(1200)
    check("desk: Support opens its sheet", page.evaluate("!!document.querySelector('dialog[open]')"))
    page.keyboard.press("Escape")
    page.wait_for_timeout(600)

    page.evaluate("window.scrollTo(0, 1400)")
    page.mouse.wheel(0, 1)
    page.wait_for_timeout(1800)
    page.screenshot(path=str(OUT / "desk-scrolled.png"))
    info = page.evaluate(
        """() => { const h = document.querySelector('header');
        const bar = h.querySelector('nav'); const rule = h.querySelector('[class*=rule]');
        return { size: h.dataset.size, bar: Math.round(bar.getBoundingClientRect().height),
          rule: getComputedStyle(rule).opacity } }"""
    )
    check(
        "desk: scrolled, the bar settles small with its painted rule",
        info["size"] == "small" and float(info["rule"]) > 0.5 and 70 <= info["bar"] <= 78,
        info,
    )

    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(600)
    page.locator('[data-nav-trigger="products"]').click()
    page.wait_for_timeout(900)
    page.locator('[data-nav-panel="products"] a', has_text="Turmerific").click()
    page.wait_for_url("**/products/turmerific**", timeout=30000)
    check("desk: a product link goes to its page", "/products/turmerific" in page.url, page.url)
    page.close()

    page = browser.new_page(viewport={"width": 1536, "height": 900}, reduced_motion="reduce")
    watch(page)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(1500)
    page.locator('[data-nav-trigger="products"]').click()
    page.wait_for_timeout(50)
    check("reduced motion: the scroll is down at once", r_value(page) == "1", r_value(page))
    page.close()


def phone(browser):
    page = browser.new_page(
        viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2
    )
    watch(page)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(2000)
    page.screenshot(path=str(OUT / "phone-top.png"))
    btn = page.locator("[data-nav-menu-button]")
    btn.click()
    page.wait_for_timeout(1200)
    page.screenshot(path=str(OUT / "phone-menu.png"))
    check("phone: the menu opens", menu_open(page))
    check("phone: the page is locked", page.evaluate("document.body.style.overflow") == "hidden")
    check("phone: its button says Close", "Close" in btn.inner_text(), btn.inner_text())
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    check("phone: Escape closes it", not menu_open(page))
    check(
        "phone: focus back on its button",
        page.evaluate("document.activeElement?.hasAttribute('data-nav-menu-button')"),
    )
    check("phone: the page is unlocked", page.evaluate("document.body.style.overflow") != "hidden")
    btn.click()
    page.wait_for_timeout(900)
    btn.click()
    page.wait_for_timeout(500)
    check("phone: the Close button closes it", not menu_open(page))
    btn.click()
    page.wait_for_timeout(900)
    page.locator('[data-nav-sheet-toggle="products"]').click()
    page.wait_for_timeout(900)
    page.screenshot(path=str(OUT / "phone-menu-products.png"))
    check(
        "phone: Products folds open",
        page.locator("[data-nav-sheet] a", has_text="NuriCell").is_visible(),
    )
    page.locator('[data-nav-sheet-toggle="science"]').click()
    page.wait_for_timeout(800)
    check(
        "phone: Science folds open, Products folds away",
        page.locator("[data-nav-sheet] a", has_text="Research library").is_visible()
        and page.locator('[data-nav-sheet-toggle="products"]').get_attribute("aria-expanded")
        == "false",
    )
    page.locator("[data-nav-sheet] button", has_text="Support").click()
    page.wait_for_timeout(1200)
    check("phone: Support opens its sheet", page.evaluate("!!document.querySelector('dialog[open]')"))
    page.keyboard.press("Escape")
    page.wait_for_timeout(700)
    btn.click()
    page.wait_for_timeout(900)
    page.locator('[data-nav-sheet-toggle="products"]').click()
    page.wait_for_timeout(800)
    page.locator("[data-nav-sheet] a", has_text="NuriCell").click()
    page.wait_for_url("**/products/nuricell**", timeout=30000)
    check("phone: a product link goes to its page", "/products/nuricell" in page.url, page.url)
    page.close()


def tablet(browser):
    page = browser.new_page(viewport={"width": 834, "height": 1112})
    watch(page)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(2000)
    page.locator("[data-nav-menu-button]").click()
    page.wait_for_timeout(1200)
    page.screenshot(path=str(OUT / "tablet-menu.png"))
    check(
        "tablet: the menu opens with Products unfolded",
        page.locator('[data-nav-sheet-toggle="products"]').get_attribute("aria-expanded") == "true"
        and page.locator("[data-nav-sheet] a", has_text="Nature Calm").is_visible(),
    )
    page.close()


def languages(browser):
    for locale in ("vn", "jp"):
        for width in (1101, 1280):
            page = browser.new_page(viewport={"width": width, "height": 800})
            watch(page)
            page.goto(f"{BASE}/{locale}", wait_until="networkidle")
            page.wait_for_timeout(2200)
            page.screenshot(path=str(OUT / f"{locale}-{width}.png"), clip={"x": 0, "y": 0, "width": width, "height": 120})
            fit = page.evaluate(
                """() => {
              const nav = document.querySelector('#site-navigation');
              const box = el => el.getBoundingClientRect();
              const left = box(nav.firstElementChild), mark = box(nav.querySelector('[data-nav-logo]'));
              const right = box(nav.lastElementChild);
              const shown = [...nav.querySelectorAll('a, button, select')].filter(el => {
                const r = box(el); return r.width > 0 && !el.closest('[data-nav-panel], [data-nav-sheet]');
              });
              const out = shown.filter(el => { const r = box(el); return r.left < 0 || r.right > innerWidth; })
                .map(el => el.innerText.trim());
              return { gapLeft: Math.round(mark.left - left.right), gapRight: Math.round(right.left - mark.right), out };
            }"""
            )
            check(
                f"{locale} {width}: the bar's three groups stay apart and inside the window",
                fit["gapLeft"] >= 16 and fit["gapRight"] >= 16 and not fit["out"],
                fit,
            )
            page.close()


with sync_playwright() as p:
    browser = p.chromium.launch(args=["--use-angle=d3d11"])
    if ONLY in (None, "desk"):
        desktop(browser)
    if ONLY in (None, "phone"):
        phone(browser)
    if ONLY in (None, "tablet"):
        tablet(browser)
    if ONLY in (None, "lang"):
        languages(browser)
    browser.close()

check("no page errors or console errors", not errors, errors[:5])
fails = [name for name, ok in results if not ok]
print(f"\n{len(results) - len(fails)}/{len(results)} checks passed. Pictures: {OUT}")
sys.exit(1 if fails else 0)

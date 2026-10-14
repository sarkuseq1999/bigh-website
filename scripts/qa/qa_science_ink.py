"""QA for the Science page in Ink & Gold, the handscroll (spec
docs/superpowers/specs/2026-10-14-science-ink-design.md; plan
docs/superpowers/plans/2026-10-14-science-ink.md).

Sections (all, or --only=a,b):
  shell       200 in the ink look, the menu bar marks Science, one h1, the parts' ids in order,
              no canvas, no console errors (1440x900, 390x844)
  people      Dr. Liu's real photo on its mount, his name, numbers and sources, "Read his story"
              opens his sheet; the five bottles with their credits, each linking to its page
  journey     (Task 3) the scroll pins, travels from Okayama to Today and lets go
  still       (Task 3) reduced motion and no script: nothing pins, every stop readable
  multiply    (Task 3, 4) every painting's blend group sits on the page with no stacking context
  strips      (Task 4) research, health and ask: painting, words, the full list, the explainers
  languages   (Task 5) kr, jp, cns, vn: 200, no errors, the new strings translated
  layout      (Task 6) sizes 1920 to 360: no sideways scroll, text 15px+, targets 44px+
  deep_links  (Task 6) #scientists, #research, #health, #ask land under the menu bar
Pictures: scripts/qa/out/science-ink/.

usage: python -X utf8 scripts/qa/qa_science_ink.py [base-url] [--only=shell,people,...]
"""

import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = ARGS[0] if ARGS else "http://localhost:3050"
ONLY = next((a.split("=", 1)[1].split(",") for a in sys.argv[1:] if a.startswith("--only=")), None)
REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "scripts/qa/out/science-ink"
OUT.mkdir(parents=True, exist_ok=True)
PATH = "/en/science"
PARTS = ["scientists", "liu", "formulas", "research", "health", "ask"]
PREFETCH_CSS = re.compile(r"was preloaded using link preload but not used")
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f"  ({detail})" if detail else ""), flush=True)


def opened(browser, w, h, path=PATH, reduced=False, js=True):
    ctx = browser.new_context(
        viewport={"width": w, "height": h},
        reduced_motion="reduce" if reduced else "no-preference",
        java_script_enabled=js,
    )
    page = ctx.new_page()
    errors = []
    page.on("console", lambda m: m.type == "error" and not PREFETCH_CSS.search(m.text) and errors.append(m.text))
    page.on("pageerror", lambda e: errors.append(str(e)))
    response = page.goto(BASE + path, wait_until="networkidle")
    if js:
        page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
    return ctx, page, response, errors


def bring(page, selector, top=140):
    page.evaluate(
        "([s, t]) => { const e = document.querySelector(s); window.scrollBy(0, e.getBoundingClientRect().top - t); }",
        [selector, top],
    )


def shell(browser):
    for w, h in [(1440, 900), (390, 844)]:
        ctx, page, response, errors = opened(browser, w, h)
        check(f"shell {w}: 200", response is not None and response.status == 200)
        check(f"shell {w}: ink look", page.locator('[data-look="ink"][data-page="science"]').count() == 1)
        check(f"shell {w}: Science carries the menu's stroke", page.locator('[data-nav-trigger="science"][data-ink="here"]').count() == 1)
        h1 = page.locator("h1")
        check(f"shell {w}: one h1, the title", h1.count() == 1 and "Meet the scientists" in h1.inner_text(), h1.first.inner_text() if h1.count() else "")
        ids = page.evaluate("() => [...document.querySelectorAll('main > section[id]')].map(s => s.id)")
        check(f"shell {w}: parts in order", ids == PARTS, str(ids))
        check(f"shell {w}: no canvas", page.locator("main canvas").count() == 0)
        font = page.evaluate("getComputedStyle(document.querySelector('h1')).fontFamily")
        check(f"shell {w}: title in Ysabeau", "ysabeau" in font.lower(), font)
        page.wait_for_timeout(1500)
        check(f"shell {w}: no console errors", not errors, "; ".join(errors[:3]))
        ctx.close()


def people(browser):
    ctx, page, _, errors = opened(browser, 1440, 900)
    bring(page, "#liu")
    page.wait_for_timeout(600)
    photo = page.locator('#liu img[src*="jiankang-liu"]')
    check("people: Dr. Liu's real photo", photo.count() == 1)
    check("people: the photo on its mount", photo.evaluate("i => getComputedStyle(i.closest('figure')).boxShadow") != "none")
    text = page.locator("#liu").inner_text()
    for word in ["Dr. Jiankang Liu", "280+", "1994", "2025", "Chief Scientific Advisor, BiGH"]:
        check(f"people: {word}", word in text)
    check("people: three sources", page.locator("#liu dl a[href^='https://']").count() == 3)
    page.get_by_role("button", name="Read his story").click()
    page.wait_for_timeout(800)
    check("people: his sheet opens", page.locator("dialog[open]").count() == 1)
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    check("people: his sheet closes", page.locator("dialog[open]").count() == 0)
    bottles = page.locator("#formulas li")
    check("people: five bottles", bottles.count() == 5, str(bottles.count()))
    for name, slug in [("NuriCell", "nuricell"), ("Nature Calm", "nature-calm"), ("Advanced OPC Formula", "advanced-opc"),
                       ("Green Bee Propolis", "green-bee-propolis"), ("Turmerific", "turmerific")]:
        link = page.locator(f'#formulas a[href$="/products/{slug}"]')
        check(f"people: {name} links to its page", link.count() == 1)
    words = page.locator("#formulas").inner_text()
    check("people: Dr. Iris Wang in words", "Dr. Iris Wang developed Nature Calm" in words)
    check("people: no photo of Dr. Iris Wang", page.locator('img[alt*="Iris"]').count() == 0)
    check("people: no console errors", not errors, "; ".join(errors[:3]))
    ctx.close()


STACKING = """el => {
  // Each element from the blend group's parent up to the page root that makes a stacking context
  // (a white box where the paper should show: the footer crane's trap).
  const found = [];
  for (let e = el.parentElement; e && !e.matches('[data-look="ink"]'); e = e.parentElement) {
    const s = getComputedStyle(e);
    const why = [];
    if (s.transform !== 'none') why.push('transform');
    if (Number(s.opacity) < 1) why.push('opacity');
    if (s.filter !== 'none') why.push('filter');
    if (s.maskImage && s.maskImage !== 'none') why.push('mask');
    if (s.isolation === 'isolate') why.push('isolation');
    if (s.mixBlendMode !== 'normal') why.push('blend');
    if (s.position !== 'static' && s.zIndex !== 'auto') why.push('z-index');
    if (['fixed', 'sticky'].includes(s.position)) why.push(s.position);
    if (s.willChange && s.willChange !== 'auto') why.push('will-change');
    if (/paint|layout|strict|content/.test(s.contain)) why.push('contain');
    if (why.length) found.push((e.tagName + '.' + e.className).slice(0, 60) + ': ' + why.join(','));
  }
  return found;
}"""

STATE = """() => {
  const s = document.querySelector('#scientists');
  const band = s.querySelector('[data-band]').getBoundingClientRect();
  const img = s.querySelector('[data-painting]').getBoundingClientRect();
  const pin = s.querySelector('[data-pin]').getBoundingClientRect();
  return { now: Number(s.dataset.now), pinTop: pin.top, pinBottom: pin.bottom,
           imgLeft: img.left, imgRight: img.right, bandLeft: band.left, bandRight: band.right,
           innerHeight, scrollY, sectionBottom: s.getBoundingClientRect().bottom };
}"""


def journey(browser):
    for w, h, lang in [(1440, 900, "en"), (1280, 720, "en"), (1280, 720, "vn"), (390, 844, "en")]:
        ctx, page, _, errors = opened(browser, w, h, path=f"/{lang}/science")
        page.wait_for_timeout(1200)
        start = page.evaluate(STATE)
        check(f"journey {w}x{h} {lang}: starts at Okayama", start["now"] == 0, str(start["now"]))
        check(f"journey {w}x{h} {lang}: pin fits the window", start["pinBottom"] <= h + 1, f"{start['pinBottom']:.0f} > {h}")
        travel = page.evaluate("() => { const s = document.querySelector('#scientists'); return s.offsetHeight - s.querySelector('[data-pin]').offsetHeight; }")
        check(f"journey {w}x{h} {lang}: room to travel", travel > w, f"{travel}px")
        seen = []
        for step in range(0, 11):
            page.evaluate(f"window.scrollTo(0, {travel * step / 10})")
            page.wait_for_timeout(250)
            st = page.evaluate(STATE)
            seen.append(st["now"])
            if 0 < step < 10:
                check(f"journey {w}x{h} {lang} {step}/10: pinned", abs(st["pinTop"] - start["pinTop"]) < 2, f"{st['pinTop']:.0f}")
                check(f"journey {w}x{h} {lang} {step}/10: painting covers the band", st["imgLeft"] <= st["bandLeft"] + 1 and st["imgRight"] >= st["bandRight"] - 1)
        check(f"journey {w}x{h} {lang}: stops in order, Okayama to Today", seen == sorted(seen) and seen[0] == 0 and seen[-1] == 4, str(seen))
        end = page.evaluate(STATE)
        check(f"journey {w}x{h} {lang}: the painting's end in view at the end", abs(end["imgRight"] - end["bandRight"]) < 3, f"{end['imgRight']:.0f} vs {end['bandRight']:.0f}")
        page.evaluate(f"window.scrollTo(0, {travel + 400})")
        page.wait_for_timeout(300)
        after = page.evaluate(STATE)
        check(f"journey {w}x{h} {lang}: lets go after Today", after["pinTop"] < start["pinTop"] - 100, f"{after['pinTop']:.0f}")
        page.evaluate(f"window.scrollTo(0, {travel * 0.5})")
        page.wait_for_timeout(300)
        page.screenshot(path=str(OUT / f"journey-{w}x{h}-{lang}-half.png"))
        if w == 1440:
            page.set_viewport_size({"width": 1024, "height": 768})
            page.wait_for_timeout(600)
            st = page.evaluate(STATE)
            check("journey resize 1440→1024 half way: painting still covers the band", st["imgLeft"] <= st["bandLeft"] + 1 and st["imgRight"] >= st["bandRight"] - 1)
        check(f"journey {w}x{h} {lang}: no console errors", not errors, "; ".join(errors[:3]))
        ctx.close()


def still(browser):
    for label, kwargs in [("reduced motion", {"reduced": True}), ("no script", {"js": False})]:
        for w, h in [(1440, 900), (390, 844)]:
            ctx, page, _, _ = opened(browser, w, h, **kwargs)
            page.wait_for_timeout(800)
            pin = page.evaluate("getComputedStyle(document.querySelector('[data-pin]')).position")
            check(f"still {label} {w}: nothing pins", pin == "static", pin)
            room = page.evaluate("document.querySelector('#scientists [data-room]').offsetHeight")
            check(f"still {label} {w}: no travel room", room == 0, str(room))
            visible = page.evaluate("[...document.querySelectorAll('#scientists li[data-stop] p')].map(p => getComputedStyle(p).visibility === 'visible' && getComputedStyle(p).display !== 'none' && p.getBoundingClientRect().height > 0)")
            check(f"still {label} {w}: all five stops readable", visible == [True] * 5, str(visible))
            band = page.evaluate("getComputedStyle(document.querySelector('[data-band]')).overflowX")
            check(f"still {label} {w}: the band scrolls sideways", band == "auto", band)
            shown = page.evaluate("getComputedStyle(document.querySelector('[data-painting]')).filter")
            check(f"still {label} {w}: the painting crisp", shown in ("none",), shown)
            page.screenshot(path=str(OUT / f"still-{label.replace(' ', '-')}-{w}.png"))
            ctx.close()


def multiply(browser):
    for w, h in [(1440, 900), (390, 844)]:
        ctx, page, _, _ = opened(browser, w, h, reduced=True)
        pin = page.locator("[data-pin]")
        check(f"multiply {w}: the pin is the scroll's blend group", pin.evaluate("e => getComputedStyle(e).mixBlendMode") == "multiply")
        found = pin.evaluate(STACKING)
        check(f"multiply {w}: nothing between the pin and the paper", not found, "; ".join(found))
        for img in page.locator("main figure[data-picture] img, main [data-scene] img").all():
            found = img.evaluate(STACKING)
            check(f"multiply {w}: {img.get_attribute('src')[:50]} sits on the paper", not found, "; ".join(found))
        ctx.close()


SECTIONS = {"shell": shell, "people": people, "journey": journey, "still": still, "multiply": multiply}

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name, run in SECTIONS.items():
            if ONLY is None or name in ONLY:
                run(browser)
        browser.close()
    failed = [r for r in results if not r[1]]
    print(f"\n{len(results) - len(failed)}/{len(results)} passed")
    sys.exit(1 if failed else 0)

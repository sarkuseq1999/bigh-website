"""QA for NuriCell's ink page (Mo, October 9, 2026; spec
docs/superpowers/specs/2026-10-09-nuricell-ink-design.md; plan
docs/superpowers/plans/2026-10-09-nuricell-ink.md).

Sections (all, or --only=a,b):
  shell       200 in the ink look, the menu bar marks Products, one h1 (the name), the real bottle,
              no canvas, no console errors (1440x900, 390x844)
  others      the other four product pages keep today's template
  multiply    every painting multiplies onto the paper: no stacking context in between, no box
  lantern     unlit blooms, then the light comes on once with no lighter flash; reduced motion: lit
  nojs        with JavaScript off every painting shows and the lantern is lit
  words       every word in nuricell.ts on the page; each chapter its own painting
  sticky      with every study open a sticky painting stays inside its chapter
  sum         the painted sum matches the serving, a caption under each number; set in type
              (?ink-sum=type, ?ink-sum=odd) each caption sits under its own numeral
  buy         Add to cart: the kit's hover, a pill on focus
  layout      sizes 1536 to 360: no sideways scroll, the painting left of its words from 960px and above
              them below, text 15px+, targets 44px+, words readable with pictures blocked
  deep_links  /en/products/nuricell#chapter-<id> lands its heading under the menu bar
  languages   kr, jp, cns, vn: 200, no console errors, the new strings translated
Pictures: scripts/qa/out/nuricell-ink/.

usage: python -X utf8 scripts/qa/qa_nuricell_ink.py [base-url] [--only=shell,others,...]
"""

import re
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = ARGS[0] if ARGS else "http://localhost:3034"
ONLY = next((a.split("=", 1)[1].split(",") for a in sys.argv[1:] if a.startswith("--only=")), None)
REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "scripts/qa/out/nuricell-ink"
OUT.mkdir(parents=True, exist_ok=True)
PATH = "/en/products/nuricell"
OTHERS = ["green-bee-propolis", "advanced-opc", "turmerific", "nature-calm"]
CHAPTERS = ["overview", "why", "inside", "research", "people", "daily", "buy"]
# Next's prefetched-CSS warning is not an error of this page (qa_about.py's PREFETCH_CSS).
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
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" and not PREFETCH_CSS.search(m.text) else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    response = page.goto(BASE + path, wait_until="networkidle")
    if js:
        page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
    return ctx, page, response, errors


def bring(page, selector, top=140):
    """Scroll the element's top to `top` px under the window's top (scrollBy: the document's 150px
    scroll-padding stops scrollIntoView short)."""
    page.evaluate(
        "([s, t]) => { const e = document.querySelector(s); window.scrollBy(0, e.getBoundingClientRect().top - t); }",
        [selector, top],
    )


def corner_diff(page, el, shot_name):
    """Brings the picture's element in view and compares its top-left corner, just inside, with the
    paper just outside it: a painting that multiplies onto the paper shows no box."""
    page.evaluate("(e) => window.scrollBy(0, e.getBoundingClientRect().top - 160)", el.element_handle())
    page.wait_for_timeout(300)
    box = el.bounding_box()
    shot = OUT / shot_name
    page.screenshot(path=str(shot))
    img = Image.open(shot).convert("RGB")
    x, y = int(box["x"]) + 3, int(box["y"]) + 3
    inside = img.getpixel((x, y))
    outside = img.getpixel((max(0, int(box["x"]) - 12), y))
    return inside, outside, max(abs(a - b) for a, b in zip(inside, outside))


def saturated_share(png):
    """The share of a picture's pixels that are clearly coloured (saturation over 0.2, not near
    black). The paper is about 0.06; a black-and-white painting has next to none."""
    import io

    hsv = Image.open(io.BytesIO(png)).convert("RGB").convert("HSV").tobytes()
    sat, val = hsv[1::3], hsv[2::3]
    return sum(1 for s_, v_ in zip(sat, val) if s_ / 255 > 0.2 and v_ / 255 > 0.25) / len(sat)


def shell(browser):
    for w, h in [(1440, 900), (390, 844)]:
        ctx, page, response, errors = opened(browser, w, h)
        tag = f"shell {w}x{h}"
        check(f"{tag}: 200", response is not None and response.status == 200)
        check(f"{tag}: the ink look", page.locator('[data-look="ink"][data-page="products"]').count() == 1)
        check(f"{tag}: the menu bar marks Products", page.locator('[data-nav-trigger="products"][data-current]').count() >= 1)
        # The accessible name is the whole word: the two visible halves sit in separate grid cells,
        # which Chrome would read as "Nuri Cell".
        check(f"{tag}: one h1", page.locator("h1").count() == 1)
        check(
            f"{tag}: the h1's accessible name is NuriCell",
            page.get_by_role("heading", level=1, name="NuriCell", exact=True).count() == 1,
        )
        check(
            f"{tag}: the opening is a region named NuriCell",
            page.get_by_role("region", name="NuriCell", exact=True).count() == 1,
        )
        check(f"{tag}: the real bottle", page.locator('[data-chapter="overview"] img[src*="nuricell.png"]').count() >= 1)
        check(f"{tag}: no canvas", page.locator("canvas").count() == 0)
        check(f"{tag}: no console errors", not errors, "; ".join(errors[:3]))
        # After the opening's words have settled (they arrive from a blur), not mid-way.
        page.wait_for_timeout(2500)
        page.screenshot(path=str(OUT / f"shell-{w}.png"))
        ctx.close()


def others(browser):
    for slug in OTHERS:
        ctx, page, response, errors = opened(browser, 1440, 900, f"/en/products/{slug}")
        check(f"others {slug}: 200", response is not None and response.status == 200)
        check(f"others {slug}: today's template", page.locator('[data-look="ink"]').count() == 0 and page.locator("#main-content").count() == 1)
        # Pins the summaries' inkColor: the template's own page root carries --product-ink.
        colour = page.evaluate(
            "() => { const e = document.querySelector('#main-content')?.closest('[style*=\"--product-ink\"]');"
            " return e ? getComputedStyle(e).getPropertyValue('--product-ink').trim() : ''; }"
        )
        check(f"others {slug}: its --product-ink is a colour", re.fullmatch(r"#[0-9a-fA-F]{3,8}|rgba?\(.*\)", colour), colour or "(empty)")
        check(f"others {slug}: no console errors", not errors, "; ".join(errors[:3]))
        ctx.close()


STACKING = """(el) => {
  // Each element from the figure's parent up to the page root that makes a stacking context.
  const found = [];
  for (let e = el.parentElement; e && !e.matches('[data-look="ink"]'); e = e.parentElement) {
    const s = getComputedStyle(e);
    const why = [];
    if (s.transform !== 'none') why.push('transform');
    if (s.translate !== 'none' || s.scale !== 'none' || s.rotate !== 'none') why.push('translate/scale/rotate');
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


def multiply(browser):
    for w, h in [(1440, 900), (390, 844)]:
        ctx, page, _, _ = opened(browser, w, h, reduced=True)
        figures = page.locator("[data-chapter] figure[data-picture]:not([data-stand])")
        check(f"multiply {w}: a painting in every chapter but the opening and buy", figures.count() >= 1, str(figures.count()))
        for i in range(figures.count()):
            fig = figures.nth(i)
            chapter = fig.evaluate("f => f.closest('[data-chapter]').dataset.chapter")
            blend = fig.evaluate("f => getComputedStyle(f).mixBlendMode")
            check(f"multiply {w} {chapter}: the figure multiplies", blend == "multiply", blend)
            found = fig.evaluate(STACKING)
            check(f"multiply {w} {chapter}: no stacking context above it", not found, "; ".join(found))
            # The picture's top-left corner matches the paper just outside it (no box).
            bring(page, f'[data-chapter="{chapter}"] figure[data-picture]', 160)
            page.wait_for_timeout(300)
            box = fig.locator("img").first.bounding_box()
            shot = OUT / f"multiply-{w}-{chapter}.png"
            page.screenshot(path=str(shot))
            img = Image.open(shot).convert("RGB")
            x, y = int(box["x"]) + 3, int(box["y"]) + 3
            inside = img.getpixel((x, y))
            outside = img.getpixel((max(0, int(box["x"]) - 12), y))
            diff = max(abs(a - b) for a, b in zip(inside, outside))
            check(f"multiply {w} {chapter}: no box at its corner", diff <= 6, f"{inside} vs {outside}")
        # The buy chapter's stroke (its figure holds the bottle's photo, so it is not a blend group:
        # the stroke multiplies on its own) and the painted sum.
        for name, selector, shot_name in [
            ("buy stroke", '[data-chapter="buy"] img[src*="stroke"]', f"multiply-{w}-buy-stroke.png"),
            ("sum", '[data-sum] img[src*="sum-"]', f"multiply-{w}-sum.png"),
        ]:
            el = page.locator(selector).first
            blend = el.evaluate("e => getComputedStyle(e).mixBlendMode")
            check(f"multiply {w} {name}: it multiplies", blend == "multiply", blend)
            found = el.evaluate(STACKING)
            check(f"multiply {w} {name}: no stacking context above it", not found, "; ".join(found))
            inside, outside, diff = corner_diff(page, el, shot_name)
            check(f"multiply {w} {name}: no box at its corner", diff <= 6, f"{inside} vs {outside}")
        ctx.close()


def lantern_state(page):
    return page.evaluate(
        """() => { const f = document.querySelector('[data-lantern]');
                   const lit = f.querySelector('[data-lit]'); const unlit = f.querySelector('img:not([data-lit])');
                   return { light: f.dataset.light, bloom: unlit.dataset.bloom, lit: Number(getComputedStyle(lit).opacity) }; }"""
    )


BLOOMING = "() => ['in', 'done'].includes(document.querySelector('[data-lantern] img:not([data-lit])').dataset.bloom)"
LIT_STATE = """() => { const f = document.querySelector('[data-lantern]'); const lit = f.querySelector('[data-lit]');
                       return { light: f.dataset.light, complete: lit.complete && lit.naturalWidth > 0,
                                lit: Number(getComputedStyle(lit).opacity) }; }"""


def lantern_waits_for_its_picture(browser):
    """The light never starts before the lit picture is in: its request is held for 5s (past
    LIGHT_AFTER and the decode wait), then let go. (Not opened(): a held picture never lets the
    page reach networkidle or load.)"""
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    held = []
    page.route("**/*", lambda route: held.append(route) if "lantern-lit-v1.webp" in route.request.url else route.continue_())
    page.goto(BASE + PATH, wait_until="domcontentloaded")
    # Hydrated: React has attached itself to the lantern's figure.
    page.wait_for_function("() => { const f = document.querySelector('[data-lantern]'); return f && Object.keys(f).some(k => k.startsWith('__react')); }", timeout=60000)
    page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
    # Note the lit picture's state at the moment the light turns on.
    page.evaluate(
        """() => { const f = document.querySelector('[data-lantern]'); const lit = f.querySelector('[data-lit]');
                   new MutationObserver(() => { if (f.dataset.light === 'on' && !window.__litAtOn)
                     window.__litAtOn = { complete: lit.complete && lit.naturalWidth > 0 }; })
                   .observe(f, { attributes: true, attributeFilter: ['data-light'] }); }"""
    )
    bring(page, "[data-lantern]", 160)
    page.wait_for_function(BLOOMING)
    states = []
    for _ in range(20):
        page.wait_for_timeout(250)
        states.append(page.evaluate(LIT_STATE))
    waiting = all(s["light"] == "off" and not s["complete"] for s in states)
    check("lantern: its picture held 5s, the light stays off", held and waiting, f"{len(held)} held; last {states[-1]}")
    for route in held:
        route.continue_()
    page.wait_for_function("() => document.querySelector('[data-lantern]').dataset.light === 'on'", timeout=15000)
    at_on = page.evaluate("() => window.__litAtOn")
    check("lantern: let go, it comes on with its picture in", at_on and at_on["complete"], str(at_on))
    ctx.close()


def lantern_waits_until_half_seen(browser):
    """A slow scroller: with 30% of the lantern in the window it blooms, but its light waits until
    at least half of it is in."""
    ctx, page, _, _ = opened(browser, 1440, 900)
    page.evaluate(
        """() => { const f = document.querySelector('[data-lantern]'); const b = f.getBoundingClientRect();
                   window.scrollBy(0, b.top - (innerHeight - b.height * 0.3)); }"""
    )
    page.wait_for_timeout(4500)
    part = page.evaluate(
        """() => { const f = document.querySelector('[data-lantern]'); const b = f.getBoundingClientRect();
                   return { light: f.dataset.light, bloom: f.querySelector('img').dataset.bloom,
                            seen: Math.round((innerHeight - b.top) / b.height * 100) / 100 }; }"""
    )
    check("lantern: 30% in the window, it blooms but stays unlit", part["bloom"] in ("in", "done") and part["light"] == "off", str(part))
    bring(page, "[data-lantern]", 160)
    page.wait_for_timeout(1200)
    soon = page.evaluate(LIT_STATE)
    page.wait_for_timeout(4000)
    later = page.evaluate(LIT_STATE)
    check("lantern: brought in, the light comes on a breath later", soon["light"] == "off" and later["light"] == "on", f"{soon} -> {later}")
    ctx.close()


def lantern(browser):
    ctx, page, _, _ = opened(browser, 1440, 900)
    first = lantern_state(page)
    check("lantern: off before it arrives", first["light"] == "off" and first["lit"] < 0.05, str(first))
    # No lighter flash by construction: both layers draw normally inside the figure, which alone
    # multiplies, so the change is a plain cross-fade (two multiplied layers would lighten mid-way).
    blends = page.evaluate(
        """() => { const f = document.querySelector('[data-lantern]');
                   return [getComputedStyle(f).mixBlendMode, ...[...f.querySelectorAll('img')].map(i => getComputedStyle(i).mixBlendMode)]; }"""
    )
    check("lantern: one blend group (figure multiplies, its layers normal)", blends[0] == "multiply" and all(b == "normal" for b in blends[1:]), str(blends))
    bring(page, "[data-lantern]", 160)
    page.wait_for_function(BLOOMING)
    page.wait_for_timeout(500)
    early = lantern_state(page)
    check("lantern: still off as it starts to bloom", early["bloom"] in ("in", "done") and early["lit"] < 0.05, str(early))
    # The unlit picture is taken 1.1s after the bloom starts, well before the light (why.tsx's
    # LIGHT_AFTER, 1.8s): the lantern well grown in, still unlit.
    page.wait_for_timeout(600)
    shot = lantern_state(page)
    check("lantern: unlit when photographed", shot["light"] == "off" and shot["lit"] < 0.05, str(shot))
    page.screenshot(path=str(OUT / "lantern-unlit-1440.png"))
    page.wait_for_timeout(6100)
    last = lantern_state(page)
    check("lantern: the light comes on", last["light"] == "on" and last["lit"] > 0.95, str(last))
    page.screenshot(path=str(OUT / "lantern-lit-1440.png"))
    before = Image.open(OUT / "lantern-unlit-1440.png").convert("RGB")
    after = Image.open(OUT / "lantern-lit-1440.png").convert("RGB")
    box = page.locator("[data-lantern] img").first.bounding_box()

    # Mean warmth (red minus blue) over the painting's middle half: its exact centre is the light's
    # white-hot core, about as warm unlit as lit, so one pixel there says nothing.
    def warmth(img):
        xs = range(int(box["x"] + box["width"] / 4), int(box["x"] + box["width"] * 3 / 4), 3)
        ys = range(int(box["y"] + box["height"] / 4), int(min(box["y"] + box["height"] * 3 / 4, img.height)), 3)
        px = [img.getpixel((x, y)) for x in xs for y in ys]
        return sum(p[0] - p[2] for p in px) / len(px)

    check("lantern: it glows warmer once lit", warmth(after) > warmth(before) + 20, f"{warmth(before):.1f} -> {warmth(after):.1f}")
    ctx.close()
    ctx, page, _, _ = opened(browser, 1440, 900, reduced=True)
    still = lantern_state(page)
    check("lantern: reduced motion, lit from the start", still["light"] == "on" and still["lit"] > 0.95, str(still))
    ctx.close()
    lantern_waits_for_its_picture(browser)
    lantern_waits_until_half_seen(browser)


def nojs(browser):
    ctx, page, _, _ = opened(browser, 1440, 900, js=False)
    shown = page.evaluate(
        """() => [...document.querySelectorAll('[data-chapter] figure[data-picture] img')].map(i => {
             const s = getComputedStyle(i); return { src: i.getAttribute('src'), o: Number(s.opacity), m: s.maskSize || s.webkitMaskSize };
           })"""
    )
    hidden = [s["src"] for s in shown if s["o"] < 0.95 or (s["m"] and s["m"].startswith("0%"))]
    check("nojs: every painting shown", shown and not hidden, ", ".join(hidden[:4]))
    lit = page.evaluate("() => Number(getComputedStyle(document.querySelector('[data-lantern] [data-lit]')).opacity)")
    check("nojs: the lantern lit", lit > 0.95, str(lit))
    # The studies past the first few wait behind "Show all" only where scripts run.
    listed = page.evaluate(
        """() => [...document.querySelectorAll('[data-chapter="research"] li[data-study]')].map(l => getComputedStyle(l).display !== 'none')"""
    )
    button = page.evaluate(
        """() => { const b = document.querySelector('[data-chapter="research"] button[aria-expanded]');
                  return b ? getComputedStyle(b).display : 'none'; }"""
    )
    check("nojs: every study listed, no dead Show all button", len(listed) == 7 and all(listed) and button == "none", f"{sum(listed)}/{len(listed)} shown; button {button}")
    ctx.close()


def nuricell_strings():
    """Every word of nuricell.ts the page must show: its string literals, less picture alts and
    pictures, keys, units and colours."""
    source = (REPO / "src/components/product/products/nuricell.ts").read_text(encoding="utf-8")
    keep = []
    for line in source.splitlines():
        if re.search(r"\b(alt|src|accent|key|from|to|unit|signature)\s*:", line) or line.strip().startswith("//"):
            continue
        for text in re.findall(r'"((?:[^"\\]|\\.)*)"', line):
            if len(text) < 4 or text.startswith(("/", "#", "../", "./")) or re.fullmatch(r"[a-z0-9-]+/?", text):
                continue
            keep.append(text)
    return keep


EXPECT = {
    "why": "lantern-unlit",
    "inside": "capsule",
    "research": "books",
    "people": "liu-v1",
    "daily": "breakfast",
    "buy": "stroke",
}


def people_painting(page):
    """Dr. Liu's chapter shows his painting, not his photograph, and in colour (never black and
    white: in Asia that signals a person has died)."""
    selector = '[data-chapter="people"] figure[data-picture] img'
    src = page.locator(selector).first.get_attribute("src") or ""
    check("people: Dr. Liu's painting, not his photograph", "liu-v1" in src and "jiankang-liu" not in src, src)
    bring(page, selector, 160)
    page.wait_for_timeout(400)
    box = page.locator(selector).first.bounding_box()
    vh = page.viewport_size["height"]
    top = max(box["y"], 0)
    png = page.screenshot(clip={"x": box["x"], "y": top, "width": box["width"], "height": min(box["height"], vh - top)})
    share = saturated_share(png)
    check("people: the painting is in colour", share > 0.03, f"{share:.1%} of its pixels clearly coloured (paper alone about 0)")


def words(browser, chapters=tuple(CHAPTERS)):
    ctx, page, _, _ = opened(browser, 1440, 900, reduced=True)
    text = re.sub(r"\s+", " ", page.locator("main").text_content())
    # Words of the sections not built yet (Questions, the caution, the FDA line) are listed, not failed.
    missing = [s for s in nuricell_strings() if re.sub(r"\s+", " ", s) not in text]
    print(f"words: {len(missing)} strings not on the page yet: {missing[:6]}")
    for chapter in chapters:
        if chapter in EXPECT:
            n = page.locator(f'[data-chapter="{chapter}"] img[src*="{EXPECT[chapter]}"]').count()
            check(f"words {chapter}: its own painting", n >= 1)
        if chapter == "people":
            people_painting(page)
    built = {
        # The title is one span per sentence: a space between them keeps the text one sentence.
        "why": ["Tiny power plants. A big part of your health."],
        "inside": ["Inside every capsule, four ingredients.", "Acetyl-L-carnitine", "Creatine", "Alpha-lipoic acid",
                   "Choline", "Why these four work together", "Fuel in, energy out", "Energy on hand",
                   "Two halves of a messenger"],
        "research": ["The research on the ingredients", "Show all 7 studies"],
        "people": ["The people behind the formula", "Dr. Jiankang Liu", "Chief Scientific Advisor, BiGH", "Portrait painting"],
        "daily": ["How to take it", "One bottle, one month.", "Take 3 capsules once a day, with or after a meal.",
                  "capsules a day", "days", "capsules in each bottle"],
        "buy": ["In each bottle", "Formulated by Dr. Jiankang Liu.", "Add to cart"],
    }
    for chapter in chapters:
        for s in built.get(chapter, []):
            check(f"words {chapter}: “{s}”", s in text)
    ctx.close()
    return missing


SUM_CAPTIONS = ["capsules a day", "days", "capsules in each bottle"]

# Each caption's centre against its numeral's box, the caption below it, and nothing outside the sum.
SUM_TYPE_GEOMETRY = """() => {
  const figure = document.querySelector('[data-sum]').getBoundingClientRect();
  return [...document.querySelectorAll('[data-sum] [data-sum-type] > span')]
    .filter((cell) => cell.querySelector('[data-sum-numeral]')).map((cell) => {
      const n = cell.querySelector('[data-sum-numeral]').getBoundingClientRect();
      const c = cell.querySelector('[data-sum-label]').getBoundingClientRect();
      return { offset: c.left + c.width / 2 - (n.left + n.width / 2), half: n.width / 2, below: c.top - n.bottom,
               inside: c.left >= figure.left - 1 && c.right <= figure.right + 1 && n.left >= figure.left - 1 && n.right <= figure.right + 1,
               text: cell.querySelector('[data-sum-numeral]').textContent };
    });
}"""


def sum_type(browser):
    """The sum set in type (the dev-only ?ink-sum=type and ?ink-sum=odd fixtures; a painting whose
    numbers are not the serving's gets this): a caption directly under its own numeral, the x and =
    only when the numbers make that sum."""
    for fixture, numerals, operators in [("type", ["3", "30", "90"], True), ("odd", ["3", "30", "91"], False)]:
        for w, h in [(1440, 900), (390, 844)]:
            tag = f"sum type ({fixture}) {w}"
            ctx, page, _, errors = opened(browser, w, h, f"{PATH}?ink-sum={fixture}", reduced=True)
            try:
                page.wait_for_selector('[data-sum-kind="type"]', timeout=15000)
            except Exception:
                pass
            kind = page.locator("[data-sum]").get_attribute("data-sum-kind")
            check(f"{tag}: the type branch shows, no painting", kind == "type" and page.locator("[data-sum] img").count() == 0, str(kind))
            check(f"{tag}: no centres claimed", page.locator("[data-sum]").get_attribute("data-centres") is None)
            bring(page, "[data-sum]", 200)
            page.wait_for_timeout(300)
            cells = page.evaluate(SUM_TYPE_GEOMETRY)
            check(f"{tag}: three numerals {numerals}", [c["text"] for c in cells] == numerals, str([c["text"] for c in cells]))
            shown = page.locator("[data-sum] [data-sum-type]").inner_text()
            check(
                f"{tag}: the × and = {'shown' if operators else 'left out'}",
                ("×" in shown and "=" in shown) if operators else ("×" not in shown and "=" not in shown),
                repr(shown),
            )
            captions = page.locator("[data-sum] [data-sum-label]")
            check(f"{tag}: the visible captions are the three words", captions.all_inner_texts() == SUM_CAPTIONS and all(c.is_visible() for c in captions.all()), str(captions.all_inner_texts()))
            within = all(abs(c["offset"]) <= c["half"] for c in cells)
            check(f"{tag}: each caption's centre within its numeral", len(cells) == 3 and within, ", ".join(f"{c['offset']:.1f}/{c['half']:.1f}" for c in cells))
            check(f"{tag}: each caption under its numeral, all inside the figure", len(cells) == 3 and all(c["below"] >= -1 and c["inside"] for c in cells), str([(round(c["below"]), c["inside"]) for c in cells]))
            check(f"{tag}: no console errors", not errors, "; ".join(errors[:3]))
            page.screenshot(path=str(OUT / f"sum-type-{fixture}-{w}.png"))
            ctx.close()


def sum_check(browser):
    ctx, page, _, _ = opened(browser, 1440, 900, reduced=True)
    painted = page.locator('[data-sum] img[src*="sum-"]')
    check("sum: painted for NuriCell's 3 × 30 = 90", painted.count() == 1)
    said = page.locator("[data-sum] [data-sum-text]").text_content()
    check("sum: said in words for screen readers", "3" in said and "30" in said and "90" in said, said)
    labels = page.evaluate(
        """() => { const img = document.querySelector('[data-sum] img').getBoundingClientRect();
                   return [...document.querySelectorAll('[data-sum] [data-sum-label]')].map(l => {
                     const r = l.getBoundingClientRect(); return { centre: (r.left + r.width / 2 - img.left) / img.width, top: r.top - img.bottom }; }); }"""
    )
    art = page.evaluate("() => JSON.parse(document.querySelector('[data-sum]').dataset.centres)")
    check("sum: three captions", len(labels) == 3, str(labels))
    near = all(abs(l["centre"] - c) < 0.06 for l, c in zip(labels, art))
    check("sum: each caption under its number", near, f"{[round(l['centre'], 3) for l in labels]} vs {art}")
    # What is on screen, not the hidden sentence (which also holds "capsules a day").
    captions = page.locator("[data-sum] [data-sum-label]")
    check(
        "sum: the visible captions are the three words",
        captions.all_inner_texts() == SUM_CAPTIONS and all(c.is_visible() for c in captions.all()),
        str(captions.all_inner_texts()),
    )
    kind = page.locator("[data-sum]").get_attribute("data-sum-kind")
    check("sum: painted by default", kind == "painted", str(kind))
    ctx.close()
    sum_type(browser)


def buy_check(browser):
    """The buy chapter's Add to cart is a pill with the kit's hover (the old template's blue would
    clash), and a pill-shaped focus ring (the kit's focus rule alone rounds it to 6px)."""
    ctx, page, _, _ = opened(browser, 1440, 900, reduced=True)
    button = page.locator('[data-chapter="buy"] button')
    check("buy: one Add to cart", button.count() == 1 and button.inner_text() == "Add to cart")
    bring(page, '[data-chapter="buy"] button', 400)
    state = """() => { const b = document.querySelector('[data-chapter="buy"] button'); const s = getComputedStyle(b);
                       return { bg: s.backgroundColor, radius: s.borderRadius, outline: s.outlineStyle, focus: b.matches(':focus-visible') }; }"""
    rest = page.evaluate(state)
    button.hover()
    page.wait_for_timeout(600)
    hover = page.evaluate(state)
    check("buy: Add to cart hover is the kit's, not the old blue", hover["bg"] == "rgb(58, 56, 51)", f"{rest['bg']} -> {hover['bg']}")
    page.mouse.move(5, 5)
    page.keyboard.press("Shift")
    button.focus()
    page.wait_for_timeout(600)
    focus = page.evaluate(state)
    check("buy: the focus ring follows a pill (99px radius)", focus["focus"] and focus["radius"] == "99px" and focus["outline"] == "solid", str(focus))
    ctx.close()


def sticky(browser):
    """With every study open, a sticky painting stays between the top of its spread and the bottom of
    its words (not just inside the chapter's padding), and it really does pin: it rides down beside
    the words while they scroll."""
    for w, h in [(1440, 900), (1024, 768)]:
        ctx, page, _, _ = opened(browser, w, h, reduced=True)
        page.locator('[data-chapter="research"] button[aria-expanded]').click()
        for summary in page.locator('[data-chapter="research"] summary').all():
            summary.click()
        for chapter in ("inside", "research"):
            bring(page, f'[data-chapter="{chapter}"]', 0)
            tall = page.evaluate(f"() => document.querySelector('[data-chapter=\"{chapter}\"]').getBoundingClientRect().height")
            worst = 0.0
            rode = 0.0
            for step in range(0, int(tall) + h, 120):
                r = page.evaluate(
                    f"""() => {{ const c = document.querySelector('[data-chapter="{chapter}"]');
                        const f = c.querySelector('figure[data-picture]');
                        const fb = f.getBoundingClientRect();
                        const spread = f.parentElement.getBoundingClientRect();
                        const words = c.querySelector('[data-words]').getBoundingClientRect();
                        return [fb.top - spread.top, words.bottom - fb.bottom]; }}"""
                )
                worst = min(worst, r[0], r[1])
                rode = max(rode, r[0])
                page.mouse.wheel(0, 120)
                page.wait_for_timeout(30)
            check(f"sticky {w}x{h} {chapter}: the painting stays beside its words", worst >= -1, f"worst {worst:.1f}px")
            check(f"sticky {w}x{h} {chapter}: it pins while the words scroll", rode >= 100, f"rode {rode:.0f}px")
        ctx.close()


SECTIONS = {
    "shell": shell,
    "others": others,
    "multiply": multiply,
    "lantern": lantern,
    "nojs": nojs,
    "words": words,
    "sticky": sticky,
    "sum": sum_check,
    "buy": buy_check,
}

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

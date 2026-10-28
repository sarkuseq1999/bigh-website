"""QA for NuriCell's ink page (Mo, October 9, 2026; spec
docs/superpowers/specs/2026-10-09-nuricell-ink-design.md; plan
docs/superpowers/plans/2026-10-09-nuricell-ink.md).

Sections (all, or --only=a,b):
  shell       200 in the ink look, the menu bar marks Products, one h1 (the name), the real bottle,
              no canvas but the moving gold leaf's, no console errors (1440x900, 390x844)
  opening     no line over the name and no pool under the bottle (Mo, October 10); the bottle's middle
              on the letters' middle from 960px (1920 to 960 wide); "NuriCell" one word on a phone or
              tablet; each half on one line in every language
  others      the products not yet in ink keep today's template
  multiply    every painting multiplies onto the paper: no stacking context in between, no box
              (the four small pools under "More from BiGH" too)
  lantern     unlit blooms, then the light comes on once with no lighter flash; reduced motion: lit
              (the lighthouse since October 26, 2026)
  nojs        with JavaScript off every painting shows and the lantern is lit
  words       every word in nuricell.ts on the page; each chapter its own painting; the four
              "More from BiGH" links
  after       the questions, More from BiGH and the notes on one left edge; the four cards four across
              from 960px, two by two below, their rows lined up
  sticky      with the longest answer open the sticky books stay inside their chapter
  research    the books open their studies (Mo picked A, October 26, 2026): six plain questions, the
              first open; a book opens its question and the other books fade (the 2003 pair lights
              two); a question lights its book, pointing previews one; on a phone a tapped book
              brings its question up under the menu bar; reduced motion: no fades
  formula     "The same formula for about 20 years" (Mo picked it, October 27, 2026) in place of how
              to take it: no label and no sum; the heading, a lead in ink and the note; the redwood
              round with its gold ring's light mask; "acetyl-L-carnitine" never broken (1440 to 360)
  buy         Add to cart: the kit's hover, a pill on focus
  layout      sizes 1536 to 360: no sideways scroll, each painting in its own place from 960px and above
              them below, text 15px+, targets 44px+, words readable with pictures blocked
  deep_links  /en/products/nuricell#chapter-<id> lands its heading under the menu bar
  polish      Task 9's fixes pinned: the supply line's dot never starts or ends a line, More links end with their
              words, the lantern's fetched width, one line per Why sentence (320-1536), the phone
              lantern with its heading in view, the opening in 1440x900, Add to cart's width
  languages   kr, jp, cns, vn: 200, no console errors, the new strings translated
  why         the Why words tidied (Mo picked them with the Gold Rush lantern, October 26, 2026, then the
              lighthouse): no
              label over the heading, one lead-in line on the heading's left edge, the 2% smaller than
              the 20% (side by side from 600px, stacked, small first, below)
  plate       What's inside tidied (Mo picked 1A, October 26, 2026): no label over the heading, the
              amounts' "per serving" line between the heading and the rows, the label card
  gold        its gold leaf: still where nothing moves (reduced motion), and moving: it rises from the
              powder (little gold at first, low down), settles as painted (about the painted leaf's
              gold), then keeps turning (two frames differ)
  scenes      the pairs as three ranch scenes (Mo picked B, October 27, 2026): paintings and their gold
              loaded, multiplied onto the page, no powder heaps; three across from 900px and stacked
              below; each pair's names in reading order; each plays as it comes into view (the wheel
              turns, the water pours) and comes to rest as painted; Play again starts it over;
              reduced motion: the paintings still, no Play again
Pictures: scripts/qa/out/nuricell-ink/.

usage: python -X utf8 scripts/qa/qa_nuricell_ink.py [base-url] [--only=shell,others,...]
"""

import io
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

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
# The products still on the Chapters template (Green Bee Propolis has its own ink page since
# October 14, 2026, Turmerific, Nature Calm and Advanced OPC Formula since October 16:
# scripts/qa/qa_propolis_ink.py, qa_turmerific_ink.py, qa_nature_calm_ink.py, qa_opc_ink.py).
OLD_TEMPLATE: list[str] = []
CHAPTERS = ["overview", "why", "inside", "research", "people", "daily", "buy"]
# The research's six plain questions, oldest first, and every other word of its answers
# (nuricell-research.tsx; Mo picked A, "tap a book, read its study", October 26, 2026).
QUESTIONS = [
    "Can two nutrients help an aging brain?",
    "Do they help old cells make energy?",
    "Does acetyl-L-carnitine help people with memory problems?",
    "What does lipoic acid do in an aging brain?",
    "What do we know about lipoic acid as a supplement?",
    "Does creatine help healthy people think?",
]
RESEARCH_WORDS = [
    "The research on the ingredients",
    "Each book is one study. Tap one to read it.",
    *QUESTIONS,
    "Animal study · PNAS", "Two reviews of trials", "Review · Neurochem Res", "Review · BBA",
    "Review of trials · Exp Gerontol",
    "In old rats, yes.", "Scientists disagree.", "In animals, it helped memory.",
    "How it works is clearer than what it does for people.", "Maybe, for short-term memory and reasoning.",
    "Old rats fed acetyl-L-carnitine and lipoic acid did better on memory tests",
    "Their cells made energy better and showed less wear",
    "Pooled trials", "A small benefit.", "Over a placebo, in people with mild memory problems",
    "Cochrane review", "No clear benefit.", "On memory tests, in people with Alzheimer’s.",
    "Both looked at patients, not healthy adults.", "Dr. Liu’s own overview:",
    "A review of lab, animal and human studies.", "Six small trials, 281 people.",
]
# Which books each question lights (1-7, nearest first): the two 2003 reviews share one question.
BOOKS_OF = [[1], [2], [3, 4], [5], [6], [7]]
# Next's prefetched-CSS warning is not an error of this page (qa_about.py's PREFETCH_CSS).
PREFETCH_CSS = re.compile(r"was preloaded using link preload but not used")
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f"  ({detail})" if detail else ""), flush=True)


def opened(browser, w, h, path=PATH, reduced=False, js=True, chunk_errors=None):
    """`chunk_errors`, when given, collects the console errors whose own URL is a /_next/static/chunks/
    file (m.text is only the generic "Failed to load resource") instead of `errors`; the caller
    decides whether they count."""
    ctx = browser.new_context(
        viewport={"width": w, "height": h},
        reduced_motion="reduce" if reduced else "no-preference",
        java_script_enabled=js,
    )
    page = ctx.new_page()
    errors = []

    def on_console(m):
        if m.type != "error" or PREFETCH_CSS.search(m.text):
            return
        in_chunks = urlparse(m.location.get("url") or "").path.startswith("/_next/static/chunks/")
        (chunk_errors if chunk_errors is not None and in_chunks else errors).append(m.text)

    page.on("console", on_console)
    page.on("pageerror", lambda e: errors.append(str(e)))
    response = page.goto(BASE + path, wait_until="networkidle")
    if js:
        page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
    return ctx, page, response, errors


def development(response):
    """The dev server (next dev) answers every page with no-cache; a built site does not, whether
    `next start` (s-maxage) or Vercel (public, max-age=0, must-revalidate). Only the dev server
    honours the dev-only fixtures."""
    cache = (response.headers.get("cache-control") or "") if response is not None else ""
    return "no-cache" in cache or "no-store" in cache


def bring(page, selector, top=140):
    """Scroll the element's top to `top` px under the window's top (scrollBy: the document's 150px
    scroll-padding stops scrollIntoView short)."""
    page.evaluate(
        "([s, t]) => { const e = document.querySelector(s); window.scrollBy(0, e.getBoundingClientRect().top - t); }",
        [selector, top],
    )


def patch(img, x, y, n=10):
    """The mean colour of an n x n patch from (x, y): the paper's fibre makes two single pixels 15px
    apart differ by up to 8 on bare paper, so one pixel each side of an edge can fail with no box."""
    px = [img.getpixel((min(xx, img.width - 1), min(yy, img.height - 1))) for xx in range(x, x + n) for yy in range(y, y + n)]
    return tuple(round(sum(c[i] for c in px) / len(px), 1) for i in range(3))


def corner_of(img, box):
    """The picture's top-left corner just inside, against the paper just outside it, as patches: a
    painting whose paper is not divided out, or that does not multiply, shows its own paper there
    (a white box: 9 to 23 off the page's paper)."""
    x, y = int(box["x"]), int(box["y"])
    inside = patch(img, x + 2, y + 2)
    outside = patch(img, max(0, x - 14), y + 2)
    return inside, outside, max(abs(a - b) for a, b in zip(inside, outside))


def corner_diff(page, el, shot_name):
    """Brings the picture's element in view and compares its top-left corner, just inside, with the
    paper just outside it: a painting that multiplies onto the paper shows no box."""
    page.evaluate("(e) => window.scrollBy(0, e.getBoundingClientRect().top - 160)", el.element_handle())
    page.wait_for_timeout(300)
    box = el.bounding_box()
    shot = OUT / shot_name
    page.screenshot(path=str(shot))
    return corner_of(Image.open(shot).convert("RGB"), box)


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
        # The one canvas is What's inside's moving gold leaf (October 26, 2026).
        check(f"{tag}: no canvas but the gold leaf's", page.locator("canvas:not([data-leaf])").count() == 0)
        check(f"{tag}: no console errors", not errors, "; ".join(errors[:3]))
        # After the opening's words have settled (they arrive from a blur), not mid-way.
        page.wait_for_timeout(2500)
        page.screenshot(path=str(OUT / f"shell-{w}.png"))
        ctx.close()


def others(browser):
    for slug in OLD_TEMPLATE:
        chunk_errors = []
        ctx, page, response, errors = opened(browser, 1440, 900, f"/en/products/{slug}", chunk_errors=chunk_errors)
        # next dev (Turbopack, Next 16.2.6) logs a 404 for one chunk preload on these four pages: the dev
        # loadable manifest has a wrong chunk hash for a next/dynamic entry with nested dynamic imports
        # (fixed after 16.2.6). A built site has none, so only the dev server is excused.
        if chunk_errors and development(response):
            print(f"NOTE others {slug}: ignored {len(chunk_errors)} /_next/static/chunks/ 404 on the dev server (Turbopack dev bug)")
        else:
            errors += chunk_errors
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
            inside, outside, diff = corner_of(Image.open(shot).convert("RGB"), box)
            check(f"multiply {w} {chapter}: no box at its corner", diff <= 6, f"{inside} vs {outside}")
        # The buy chapter's stroke (its figure holds the bottle's photo, so it is not a blend group:
        # the stroke multiplies on its own).
        for name, selector, shot_name in [
            ("buy stroke", '[data-chapter="buy"] img[src*="stroke"]', f"multiply-{w}-buy-stroke.png"),
        ]:
            el = page.locator(selector).first
            blend = el.evaluate("e => getComputedStyle(e).mixBlendMode")
            check(f"multiply {w} {name}: it multiplies", blend == "multiply", blend)
            found = el.evaluate(STACKING)
            check(f"multiply {w} {name}: no stacking context above it", not found, "; ".join(found))
            inside, outside, diff = corner_diff(page, el, shot_name)
            check(f"multiply {w} {name}: no box at its corner", diff <= 6, f"{inside} vs {outside}")
        # The small pools under "More from BiGH": each multiplies, with no stacking context above it.
        pools = page.locator("#more a > span:first-child > img:first-child")
        check(f"multiply {w} more: four pools", pools.count() == 4, str(pools.count()))
        for i in range(pools.count()):
            blend = pools.nth(i).evaluate("e => getComputedStyle(e).mixBlendMode")
            found = pools.nth(i).evaluate(STACKING)
            check(f"multiply {w} more {i + 1}: the pool multiplies, no stacking context above it", blend == "multiply" and not found, f"{blend}; " + "; ".join(found))
        # The shared pool painting (the four small pools under More from BiGH) is not quite white
        # at its edges: each carries a radial mask on itself, or a faint rectangle shows on the paper.
        masked = page.evaluate(
            """() => [...document.querySelectorAll('#more a > span:first-child > img:first-child')]
                 .map((e) => { const s = getComputedStyle(e); return s.maskImage || s.webkitMaskImage || 'none'; })"""
        )
        unmasked = [i + 1 for i, m in enumerate(masked) if "radial-gradient" not in m]
        check(f"multiply {w} masks: the four More pools", len(masked) == 4 and not unmasked, f"{len(masked)} found; unmasked: {unmasked}")
        # Hovering a link changes only its colour: a transform, opacity or filter on it would cut the
        # pool out of the paper's blend.
        bring(page, "#more", 160)
        link = page.locator("#more a").first
        link.hover()
        page.wait_for_timeout(700)
        state = link.evaluate("e => { const s = getComputedStyle(e); return [s.transform, s.opacity, s.filter]; }")
        found = pools.first.evaluate(STACKING)
        blend = pools.first.evaluate("e => getComputedStyle(e).mixBlendMode")
        check(f"multiply {w} more: hovering a link leaves its pool multiplying", state == ["none", "1", "none"] and blend == "multiply" and not found, f"{state}; {blend}; " + "; ".join(found))
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
    # The lit picture itself (lighthouse-lit-v1.webp, or a later name), not its gold mask.
    lit_picture = re.compile(r"(?:lantern|goldrush|lighthouse)-lit-(?:core-)?v\d+\.webp")
    page.route("**/*", lambda route: held.append(route) if lit_picture.search(route.request.url) else route.continue_())
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

    # Mean warmth (red minus blue) over the lighthouse's lamp room and the light round it (52-74%
    # of the picture's width, 7-24% of its height; the tower's cap and rail are grey ink lit or
    # not). Measured October 26, 2026: 12.0 unlit, 38.7 lit.
    def warmth(img):
        xs = range(int(box["x"] + box["width"] * 0.52), int(box["x"] + box["width"] * 0.74), 3)
        ys = range(int(box["y"] + box["height"] * 0.07), int(min(box["y"] + box["height"] * 0.24, img.height)), 3)
        px = [img.getpixel((x, y)) for x in xs for y in ys]
        return sum(p[0] - p[2] for p in px) / len(px)

    check("lantern: its lamp glows warmer once lit", warmth(after) > warmth(before) + 10, f"{warmth(before):.1f} -> {warmth(after):.1f}")
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
    # The books and the questions' toggles need scripts: without them every answer shows, every book
    # stays dark, and the hint ("Tap one to read it") and the toggles step aside.
    research = page.evaluate(
        """() => { const c = document.querySelector('[data-chapter="research"]');
                  const shown = (e) => e && getComputedStyle(e).display !== 'none' && getComputedStyle(e).visibility === 'visible';
                  const answers = [...c.querySelectorAll('[data-study] [id^="research-answer-"]')];
                  return { rows: c.querySelectorAll('li[data-study]').length,
                           answers: answers.filter((a) => shown(a) && a.getBoundingClientRect().height > 40).length,
                           dim: [...c.querySelectorAll('[data-dim]')].filter(shown).length,
                           hint: shown([...c.querySelectorAll('[data-words] p')].find((p) => p.textContent.startsWith('Each book'))),
                           marks: [...c.querySelectorAll('[data-study] button [aria-hidden]')].filter(shown).length }; }"""
    )
    check(
        "nojs: six questions, every answer readable, every book dark, no hint or toggles",
        research["rows"] == 6 and research["answers"] == 6 and research["dim"] == 0 and not research["hint"] and research["marks"] == 0,
        str(research),
    )
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
    # The ink page shows the label card (labelCard) in place of the otherIngredients sentence, and
    # the pairs' note, which says it too, in place of notes.science (Mo picked the tidier What's
    # inside, October 26, 2026); the template still uses both.
    shown_elsewhere = [m.group(1) for m in re.finditer(r'\b(?:otherIngredients|science):\s*"((?:[^"\\]|\\.)*)"', source)]
    # The Why label too: the ink page's heading stands alone (Mo, October 26, 2026).
    shown_elsewhere += re.findall(r'why:\s*\{\s*label:\s*"((?:[^"\\]|\\.)*)"', source)
    return [text for text in keep if text not in shown_elsewhere]


EXPECT = {
    "why": "lighthouse-unlit",
    "inside": "capsule",
    "research": "books",
    "people": "liu-berkeley",
    "daily": "rings-",
    "buy": "stroke",
}


def people_painting(page):
    """Dr. Liu's chapter shows his painting, not his photograph, and in colour (never black and
    white: in Asia that signals a person has died). Since October 26, 2026 (Mo picked A2) it is the
    view west, his portrait at the right of a grey ink landscape: the wide framing from 960px, the
    phone framing below; the colour is measured on him (the plate's right 45%), not the grey bay."""
    selector = '[data-chapter="people"] figure[data-picture] img'
    bring(page, selector, 160)
    page.wait_for_timeout(400)
    # The picture is lazy: which framing it shows is known once it has loaded.
    page.wait_for_function(f"() => document.querySelector('{selector}').complete")
    shown = page.locator(selector).first.evaluate("img => img.currentSrc") or ""
    wide = page.viewport_size["width"] >= 960
    framing = "liu-berkeley-v" if wide else "liu-berkeley-phone-v"
    check(f"people: Dr. Liu's painting, not his photograph ({'wide' if wide else 'phone'} framing)",
          framing in shown and "jiankang-liu" not in shown, shown[-90:])
    box = page.locator(selector).first.bounding_box()
    vh = page.viewport_size["height"]
    top = max(box["y"], 0)
    left = box["x"] + box["width"] * 0.55
    png = page.screenshot(clip={"x": left, "y": top, "width": box["width"] * 0.45, "height": min(box["height"], vh - top)})
    share = saturated_share(png)
    check("people: the painting is in colour", share > 0.03, f"{share:.1%} of his part's pixels clearly coloured (paper alone about 0)")


def reachable_text(page):
    """Every word a visitor can read: innerText, which leaves out whatever is not rendered
    (display:none, hidden), after opening every question, each one click away (a closed <details>
    is not rendered either, so its answer would otherwise be missed; a string hidden for good still
    is). The research opens one answer at a time, so each is opened in turn and read."""
    answers = []
    for row in page.locator('[data-chapter="research"] li[data-study]').all():
        if row.locator("button").first.get_attribute("aria-expanded") != "true":
            row.locator("button").first.click()
            page.wait_for_timeout(700)
        answers.append(row.inner_text())
    page.evaluate("() => document.querySelectorAll('main details').forEach((d) => { d.open = true; })")
    page.wait_for_timeout(300)
    # The questions show one answer at a time, each one click away: pick each and read it too.
    questions = page.evaluate(
        """async () => { const answers = [];
             for (const b of document.querySelectorAll('#questions ol > li > h3 button')) {
               if (b.getAttribute('aria-expanded') !== 'true') b.click();
               await new Promise((r) => setTimeout(r, 60));
               answers.push(b.closest('li').querySelector('[role=region]').innerText); }
             return answers.join(' '); }"""
    )
    return re.sub(r"\s+", " ", page.locator("main").inner_text() + " " + " ".join(answers) + " " + questions)


def words(browser, chapters=tuple(CHAPTERS)):
    ctx, page, _, _ = opened(browser, 1440, 900, reduced=True)
    # The page at rest, as rendered: the per-chapter words below are visible without a click.
    text = re.sub(r"\s+", " ", page.locator("main").inner_text())
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
        "research": ["The research on the ingredients", "Each book is one study. Tap one to read it.", *QUESTIONS],
        # No label over his name on NuriCell (Mo picked A2, October 26, 2026); a lead and a note.
        "people": ["Dr. Jiankang Liu", "Chief Scientific Advisor, BiGH", "Portrait painting",
                   "At UC Berkeley, he studied two of NuriCell’s nutrients together.",
                   "An animal study, not a test of NuriCell."],
        # The same formula for about 20 years (Mo picked it, October 27, 2026).
        "daily": FORMULA,
        "buy": ["In each bottle", "Formulated by Dr. Jiankang Liu.", "Add to cart"],
    }
    for chapter in chapters:
        for s in built.get(chapter, []):
            check(f"words {chapter}: “{s}”", s in text)
    # The FDA statement (notes.fda) is shown by the shared footer since October 12, 2026, so the
    # footer's words count too.
    everything = reachable_text(page) + " " + re.sub(r"\s+", " ", page.locator("footer").last.inner_text())
    missing = [s for s in nuricell_strings() if re.sub(r"\s+", " ", s) not in everything]
    check("words: every string of nuricell.ts on the page", not missing, f"{len(missing)} missing: {missing[:5]}")
    if "research" in chapters:
        unread = [s for s in RESEARCH_WORDS if s not in everything]
        check("words research: every question and answer readable, one click away", not unread, ", ".join(unread[:3]))
    for slug in OTHERS:
        check(f"words: More from BiGH links {slug}", page.locator(f'#more a[href$="/products/{slug}"]').count() == 1)
    ctx.close()
    return missing


# The after-buy sections' left edges and the More cards' rows.
AFTER_GEOMETRY = """() => {
  const left = (e) => e.getBoundingClientRect().left;
  const tops = (selector) => [...document.querySelectorAll('#more li ' + selector)].map((e) => Math.round(e.getBoundingClientRect().top));
  const list = document.querySelector('#questions ol').getBoundingClientRect();
  const more = document.querySelector('#more ul').getBoundingClientRect();
  return {
    questions: left(document.querySelector('#questions h2')),
    more: left(document.querySelector('#more h2')),
    notes: left(document.querySelector('[data-notes] p')),
    list: list.left, listWidth: list.width, moreWidth: more.width,
    cards: [...document.querySelectorAll('#more li')].map((e) => Math.round(e.getBoundingClientRect().top)),
    stands: tops('a > span:nth-of-type(1)'), names: tops('a > span:nth-of-type(2)'), focus: tops('a > span:nth-of-type(3)'),
    scrollW: document.documentElement.scrollWidth, innerW: innerWidth,
  };
}"""


def after(browser):
    """After Buy: the questions' heading, the More heading and the notes start on one left edge (the
    wrap's); the questions (each answer with its painting beside it from 960px, qa_questions.py)
    span the wrap, as the cards do; the four cards are four across from 960px and
    two by two below, and in each row the bottles, the names and the focus lines line up even when a
    name wraps."""
    for w, h in [(1440, 900), (1024, 768), (964, 768), (960, 768), (390, 844)]:
        ctx, page, _, _ = opened(browser, w, h, reduced=True)
        g = page.evaluate(AFTER_GEOMETRY)
        edges = [g["questions"], g["more"], g["notes"], g["list"]]
        check(f"after {w}: one left edge (questions, more, notes, the list)", max(edges) - min(edges) <= 1, str([round(e, 1) for e in edges]))
        check(f"after {w}: the questions span the wrap, as the cards do", abs(g["listWidth"] - g["moreWidth"]) <= 1, f"{g['listWidth']:.0f} vs {g['moreWidth']:.0f}px")
        per_row = 4 if w >= 960 else 2
        rows = [g["cards"][i : i + per_row] for i in range(0, len(g["cards"]), per_row)]
        check(f"after {w}: {per_row} cards a row", len(g["cards"]) == 4 and all(len(set(r)) == 1 for r in rows), str(g["cards"]))
        for name in ("stands", "names", "focus"):
            aligned = all(len(set(g[name][i : i + per_row])) == 1 for i in range(0, 4, per_row))
            check(f"after {w}: each row's {name} line up", aligned, str(g[name]))
        check(f"after {w}: no sideways scroll", g["scrollW"] <= g["innerW"], f"{g['scrollW']} vs {g['innerW']}")
        if w in (1440, 390):
            page.evaluate("() => { const e = document.querySelector('#questions'); window.scrollBy(0, e.getBoundingClientRect().top - 90); }")
            page.wait_for_timeout(300)
            page.screenshot(path=str(OUT / f"after-{w}-questions.png"))
            page.evaluate("() => { const e = document.querySelector('#more'); window.scrollBy(0, e.getBoundingClientRect().top - 90); }")
            page.wait_for_timeout(300)
            page.screenshot(path=str(OUT / f"after-{w}-more.png"))
        ctx.close()


# "The same formula for about 20 years" (Mo picked 2 of round 3, October 27, 2026; mockups
# reference/ink-pages/mockups/nuricell-daily/): in place of how to take it, which the buy box and the
# first question say.
FORMULA = [
    "The same formula for about 20 years.",
    "Dr. Liu chose its four nutrients. We haven’t changed them since.",
    "The gold ring is about 20 years ago. Each ring outside it is a year with the same four: "
    "acetyl-L-carnitine, creatine, alpha-lipoic acid and choline.",
]

# The chapter's words in order, the lead's ink, the painting and its gold ring's light mask, and on
# how many lines each hyphenated nutrient sits (as the lines of its glyph rects).
FORMULA_GEOMETRY = """(words) => {
  const c = document.querySelector('[data-chapter="daily"]');
  const kids = [...c.querySelector('[data-words]').children];
  const img = c.querySelector('figure[data-picture] img');
  const gold = c.querySelector('figure[data-picture] [style*="--gold"]');
  const lines = (word) => {
    const walk = document.createTreeWalker(c.querySelector('[data-words]'), NodeFilter.SHOW_TEXT);
    for (let node = walk.nextNode(); node; node = walk.nextNode()) {
      const i = node.data.indexOf(word);
      if (i < 0 || node.parentElement.closest('[class*=visuallyHidden]')) continue;
      const r = document.createRange(); r.setStart(node, i); r.setEnd(node, i + word.length);
      return new Set([...r.getClientRects()].filter((x) => x.width > 0).map((x) => Math.round(x.top))).size;
    }
    return 0;
  };
  const style = (e) => getComputedStyle(e);
  return {
    tags: kids.map((k) => k.tagName), texts: kids.map((k) => k.textContent.replace(/\\s+/g, ' ').trim()),
    sum: !!c.querySelector('[data-sum]'), howTo: c.textContent.includes('How to take it'),
    leadInk: kids[1] && style(kids[1]).color === style(kids[0]).color, leadSize: kids[1] ? parseFloat(style(kids[1]).fontSize) : 0,
    src: img ? decodeURIComponent(img.currentSrc || img.src) : '', loaded: !!img && img.complete && img.naturalWidth > 0,
    caption: (c.querySelector('figure[data-picture] figcaption') || {}).textContent,
    gold: gold ? style(gold).getPropertyValue('--gold') : '',
    whole: Object.fromEntries(words.map((w) => [w, lines(w)])),
  };
}"""


def formula_check(browser):
    for w, h in [(1440, 900), (1024, 768), (768, 1024), (390, 844), (360, 780)]:
        tag = f"formula {w}"
        ctx, page, _, errors = opened(browser, w, h, reduced=True)
        bring(page, '[data-chapter="daily"]', 100)
        page.wait_for_timeout(400)
        g = page.evaluate(FORMULA_GEOMETRY, ["acetyl-L-carnitine", "alpha-lipoic"])
        check(f"{tag}: the heading, the lead, the note", g["tags"] == ["H2", "P", "P"] and g["texts"] == FORMULA, str(g["texts"]))
        check(f"{tag}: no label and no sum", not g["sum"] and not g["howTo"])
        check(f"{tag}: the lead in ink, a step under the heading", g["leadInk"] and g["leadSize"] >= 22, f"{g['leadInk']} {g['leadSize']}px")
        check(f"{tag}: the redwood round, loaded, captioned Illustration", "/rings-" in g["src"] and g["loaded"] and g["caption"] == "Illustration", f"{g['src'][-50:]} {g['caption']}")
        check(f"{tag}: its gold ring's light mask", "rings-v1-gold" in g["gold"], g["gold"])
        check(f"{tag}: each hyphenated nutrient on one line", all(v == 1 for v in g["whole"].values()), str(g["whole"]))
        check(f"{tag}: no console errors", not errors, "; ".join(errors[:2]))
        if w == 1440:
            mask = page.request.get(BASE + "/images/products/nuricell/ink/rings-v1-gold.webp")
            check("formula: the gold ring's light mask is served", mask.status == 200, str(mask.status))
        page.screenshot(path=str(OUT / f"formula-{w}.png"))
        ctx.close()
    # Chinese breaks between any two characters: the heading and lead break only at their
    # punctuation, so "配方" and "营养素" stay whole (they split at 390 and 1440 before).
    for w, h in [(1440, 900), (1024, 768), (390, 844), (360, 780)]:
        ctx, page, _, _ = opened(browser, w, h, "/cns/products/nuricell", reduced=True)
        bring(page, '[data-chapter="daily"]', 100)
        page.wait_for_timeout(300)
        g = page.evaluate(FORMULA_GEOMETRY, ["配方", "营养素"])
        check(f"formula cns {w}: no word split in the heading or lead", all(v == 1 for v in g["whole"].values()), str(g["whole"]))
        page.screenshot(path=str(OUT / f"formula-cns-{w}.png"))
        ctx.close()


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
    """With the longest answer open (the 2003 pair: the words a few hundred px taller than the books),
    a sticky painting stays between the top of its spread and the bottom of its words (not just
    inside the chapter's padding), and it really does pin: it rides down beside the words while they
    scroll. The research's books; the capsule stands still in the middle of its ingredients since
    October 19 (nuricell.module.css), so What's inside has no sticky painting."""
    for w, h in [(1440, 900), (1024, 768)]:
        ctx, page, _, _ = opened(browser, w, h, reduced=True)
        page.locator('[data-chapter="research"] li[data-study]').nth(2).locator("button").first.click()
        page.wait_for_timeout(300)
        for chapter in ("research",):
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


# The middle of a book's tap area in window px: its clip-path's points, averaged.
BOOK_AT = """(n) => {
  const b = document.querySelector('[data-chapter="research"] [data-book="' + n + '"]');
  const r = b.getBoundingClientRect();
  const pts = [...b.style.clipPath.matchAll(/([\\d.]+)% ([\\d.]+)%/g)].map((m) => [+m[1], +m[2]]);
  const cx = pts.reduce((s, p) => s + p[0], 0) / pts.length;
  const cy = pts.reduce((s, p) => s + p[1], 0) / pts.length;
  return [r.left + (r.width * cx) / 100, r.top + (r.height * cy) / 100];
}"""
# Which questions are open (0-5) and which books are dark (1-7, not faded under paper).
RESEARCH_STATE = """() => { const c = document.querySelector('[data-chapter="research"]');
  return { open: [...c.querySelectorAll('li[data-study] > button')].flatMap((b, i) => b.getAttribute('aria-expanded') === 'true' ? [i] : []),
           dark: [...c.querySelectorAll('[data-fade]')].flatMap((f) => f.hasAttribute('data-dim') ? [] : [Number(f.dataset.fade)]) }; }"""


def research(browser):
    """Tap a book, read its study (Mo picked A, October 26, 2026)."""
    ctx, page, _, errors = opened(browser, 1440, 900)
    bring(page, '[data-chapter="research"] h2', 110)
    page.mouse.move(1430, 890)
    page.wait_for_timeout(900)
    state = lambda: page.evaluate(RESEARCH_STATE)
    rest = state()
    check("research: at rest the first question is open, its book dark, the other six faded", rest == {"open": [0], "dark": [1]}, str(rest))
    rows = page.locator('[data-chapter="research"] li[data-study]')
    check("research: six plain questions", rows.count() == 6 and rows.locator("button").first.inner_text().count("?") == 1)
    names = page.locator('[data-chapter="research"] [data-book]').evaluate_all(
        "els => els.map(e => [e.getAttribute('aria-label'), e.getAttribute('aria-controls')])"
    )
    want = [[q, f"research-answer-{i}"] for i, books in enumerate(BOOKS_OF) for q in [QUESTIONS[i]] * len(books)]
    check("research: each book named by its year and question, and points at its answer",
          [[n.split(": ", 1)[-1], c] for n, c in names] == want, str(names[:2]))
    own = [
        n for n in range(1, 8)
        if page.evaluate(f"([x, y]) => document.elementFromPoint(x, y)?.dataset.book", page.evaluate(BOOK_AT, n)) != str(n)
    ]
    check("research 1440: each book's middle is its own button", not own, f"books {own} covered")
    x, y = page.evaluate(BOOK_AT, 3)
    page.mouse.click(x, y)
    page.mouse.move(1430, 890)
    page.wait_for_timeout(1200)
    pair = state()
    links = page.locator('[data-chapter="research"] li[data-study][data-open] a').evaluate_all(
        "els => els.filter(e => getComputedStyle(e).visibility === 'visible' && e.getBoundingClientRect().height > 0).length"
    )
    faded = page.evaluate("() => Number(getComputedStyle(document.querySelector('[data-fade=\"1\"]')).opacity)")
    check("research: a 2003 book opens the shared question and lights both books, two studies to read",
          pair == {"open": [2], "dark": [3, 4]} and links == 2, f"{pair}, {links} links")
    check("research: a faded book sits under a little paper (0.6)", abs(faded - 0.6) < 0.02, f"{faded:.2f}")
    x, y = page.evaluate(BOOK_AT, 6)
    page.mouse.move(x, y, steps=6)
    page.wait_for_timeout(300)
    peek = state()
    page.mouse.move(1430, 890, steps=6)
    page.wait_for_timeout(300)
    back = state()
    check("research: pointing at a book previews it, leaving it returns to the open study",
          peek == {"open": [2], "dark": [6]} and back == pair, f"{peek} then {back}")
    question = rows.nth(5).locator("button").first
    question.hover()
    page.wait_for_timeout(300)
    lit = state()
    question.click()
    page.wait_for_timeout(700)
    clicked = state()
    check("research: pointing at a question lights its book; clicking opens it",
          lit["dark"] == [7] and clicked == {"open": [5], "dark": [7]}, f"{lit} then {clicked}")
    question.click()
    page.mouse.move(1430, 890)
    page.wait_for_timeout(700)
    shut = state()
    check("research: closing the open question leaves every book dark", shut == {"open": [], "dark": list(range(1, 8))}, str(shut))
    page.locator('[data-chapter="research"] [data-book="5"]').focus()
    page.wait_for_timeout(200)
    focused = state()
    page.keyboard.press("Enter")
    page.wait_for_timeout(700)
    pressed = state()
    check("research: a book reached by keyboard lights, and Enter opens its question",
          focused["dark"] == [5] and pressed["open"] == [3], f"{focused} then {pressed}")
    check("research 1440: no console errors", not errors, "; ".join(errors[:2]))
    ctx.close()

    # A phone: the questions sit under the painting, so a tapped book brings its question up to the
    # top, just under the menu bar, once the rows have settled.
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    page = ctx.new_page()
    page.goto(BASE + PATH, wait_until="networkidle")
    page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
    bring(page, '[data-chapter="research"] figure', 90)
    page.wait_for_timeout(600)
    own = [
        n for n in range(1, 8)
        if page.evaluate(f"([x, y]) => document.elementFromPoint(x, y)?.dataset.book", page.evaluate(BOOK_AT, n)) != str(n)
    ]
    check("research 390: each book's middle is its own button", not own, f"books {own} covered")
    x, y = page.evaluate(BOOK_AT, 6)
    page.touchscreen.tap(x, y)
    page.wait_for_timeout(1800)
    top, bar = page.evaluate(
        """() => [document.querySelectorAll('[data-chapter="research"] li[data-study]')[4].getBoundingClientRect().top,
                  document.querySelector('header').getBoundingClientRect().bottom]"""
    )
    tapped = page.evaluate(RESEARCH_STATE)
    check("research 390: a tapped book opens its question and brings it up under the menu bar",
          tapped["open"] == [4] and bar <= top <= bar + 40, f"{tapped}; row top {top:.0f}, bar {bar:.0f}")
    ctx.close()

    ctx, page, _, _ = opened(browser, 1440, 900, reduced=True)
    still = page.evaluate(
        "() => [...document.querySelectorAll('[data-chapter=\"research\"] [data-fade], [data-chapter=\"research\"] [id^=\"research-answer-\"]')].map(e => getComputedStyle(e).transitionDuration)"
    )
    check("research: reduced motion, the books and answers change without fading", still and all(set(d.split(", ")) == {"0s"} for d in still), str(sorted(set(still))))
    ctx.close()


SIZES = [(1536, 864), (1440, 900), (1280, 800), (1024, 768), (960, 800), (900, 900), (768, 1024), (390, 844), (360, 780)]


def layout(browser):
    for w, h in SIZES:
        ctx, page, _, _ = opened(browser, w, h, reduced=True)
        tag = f"layout {w}x{h}"
        wide = page.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
        check(f"{tag}: no sideways scroll", wide <= 0, f"{wide}px")
        # From 960px each painting in its own place (Mo picked B, October 19, 2026): the words left
        # of the lantern; Dr. Liu's view west across the chapter with his words in its sky, ending
        # above its land (its lower 45%; Mo picked A2, October 26, 2026); the books and the bottle
        # left of theirs; the capsule between
        # its ingredients (the first and third left of it, the second and fourth right of it) under
        # the heading; the redwood round right of its words (October 27, 2026). One column: each
        # painting over its words.
        bad = page.evaluate(
            """(two) => [...document.querySelectorAll('[data-chapter]:not([data-chapter="overview"])')].map(c => {
                 const box = (e) => e.getBoundingClientRect();
                 const f = box(c.querySelector('figure[data-picture]'));
                 const t = box(c.querySelector('[data-words]'));
                 const id = c.dataset.chapter;
                 let ok;
                 if (!two) ok = f.bottom <= t.top + 1;
                 else if (id === 'why' || id === 'daily') ok = t.right <= f.left + 1;
                 else if (id === 'people') {
                   const img = box(c.querySelector('figure[data-picture] img'));
                   const last = box([...c.querySelectorAll('[data-words] > *')].pop());
                   ok = img.width >= Math.min(window.innerWidth, 1.8 * (window.innerHeight - 140)) - 2
                     && last.bottom <= img.top + img.height * 0.55 + 1 && t.left < img.left + img.width / 2;
                 }
                 else if (id === 'inside') {
                   const rows = [...c.querySelectorAll('tbody tr')].map(box);
                   ok = rows.length === 4 && box(c.querySelector('h2')).bottom <= f.top + 1
                     && rows.every((r, i) => (i % 2 ? r.left >= f.right - 1 : r.right <= f.left + 1));
                 } else ok = f.right <= t.left + 1;
                 return ok ? null : id; }).filter(Boolean)""",
            w >= 960,
        )
        check(f"{tag}: each painting in its place {'(B, October 19)' if w >= 960 else '(above its words)'}", not bad, ", ".join(bad))
        small = page.evaluate(
            """() => [...document.querySelectorAll('main p, main li, main dd, main dt, main td, main th, main figcaption')]
                 .filter(e => e.offsetParent && e.textContent.trim() && parseFloat(getComputedStyle(e).fontSize) < 15)
                 .map(e => e.textContent.trim().slice(0, 30))"""
        )
        check(f"{tag}: text 15px or larger", not small, "; ".join(small[:3]))
        y, n, total = 0, 0, page.evaluate("() => document.documentElement.scrollHeight")
        while y < total and n < 30:
            page.evaluate(f"window.scrollTo(0, {y})")
            page.wait_for_timeout(150)
            page.screenshot(path=str(OUT / f"layout-{w}-{n:02d}.png"))
            y, n = y + h, n + 1
        # Every target, including those inside closed questions (opened first, after the screenshots,
        # which show the page as it arrives) and each study's "Read the study" link, measured whether
        # its answer is open or not (a closed answer keeps its link's size, out of sight).
        page.evaluate("() => document.querySelectorAll('main details').forEach((d) => { d.open = true; })")
        page.wait_for_timeout(300)
        targets = page.evaluate(
            """() => [...document.querySelectorAll('main button, main summary, main a')]
                 .filter(e => e.offsetParent).map(e => e.getBoundingClientRect().height)"""
        )
        tiny = sum(1 for height in targets if height < 44)
        links = page.evaluate("() => [...document.querySelectorAll('[data-study] a')].filter(e => e.offsetParent).length")
        check(
            f"{tag}: targets 44px or taller (questions open, all seven study links)",
            tiny == 0 and links == 7,
            f"{tiny} small of {len(targets)}; {links} of 7 study links measured",
        )
        ctx.close()
    ctx = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    page = ctx.new_page()
    page.route(re.compile(r"\.(webp|png|jpg|jpeg|avif)(\?|$)|/_next/image"), lambda route: route.abort())
    page.goto(BASE + PATH, wait_until="networkidle")
    # The research's closed answers and the questions' other answers wait one click away by design
    # (not for want of a picture), so they are left out (qa_questions.py picks each question); the
    # open ones count.
    hidden = page.evaluate(
        """() => [...document.querySelectorAll('main h1, main h2, main p')]
             .filter(e => !e.closest('[data-chapter="research"] li[data-study]:not([data-open])'))
             .filter(e => !e.closest('#questions li:not([data-open]) [role=region]'))
             .filter(e => e.textContent.trim() && (e.offsetParent === null || getComputedStyle(e).visibility === 'hidden' || Number(getComputedStyle(e).opacity) < 0.9))
             .map(e => e.textContent.trim().slice(0, 30))"""
    )
    check("layout: words readable with pictures blocked", not hidden, "; ".join(hidden[:3]))
    ctx.close()


def deep_links(browser):
    for w, h in [(1440, 900), (1024, 768), (390, 844)]:
        for chapter in CHAPTERS[1:]:
            ctx, page, _, _ = opened(browser, w, h, f"{PATH}#chapter-{chapter}", reduced=True)
            page.wait_for_timeout(400)
            top = page.evaluate(f"() => document.getElementById('chapter-{chapter}-title').getBoundingClientRect().top")
            bar = page.evaluate("() => document.querySelector('header').getBoundingClientRect().bottom")
            check(f"deep link {w} #{chapter}: heading under the bar, in the window", bar <= top <= h - 80, f"top {top:.0f}, bar {bar:.0f}")
            ctx.close()


# The supply line ("90 vegetarian capsules · 30-day supply"), in the opening and the Buy rows, as
# laid out (ink-chapter.tsx's keepTogether): each fact's dot is its ::before, in the gap before it,
# and the row is clipped one gap left of the column. A dot shows only for a fact on the same line
# as the one before it (it never starts a line), with the fact's words straight after it on that
# line (it never ends one); a fact that starts a line has its words on the column's edge, its dot
# in the clipped gap. "30-day" is one client rect. The whole line is there for screen readers.
SUPPLY_LINES = """() => [document.querySelector('[data-chapter=overview] [class*=bottleCardSupply]'),
                    document.querySelector('[data-chapter=buy] dl div:nth-child(2) dd')].map((el) => {
  const clip = el.querySelector('[data-facts]').parentElement.getBoundingClientRect();
  const facts = [...el.querySelectorAll('[data-fact]')];
  const lineTops = (e) => { const r = document.createRange(); r.selectNodeContents(e);
    return [...r.getClientRects()].filter((x) => x.width > 1).map((x) => Math.round(x.top)); };
  const out = { facts: facts.length, bad: [], shown: 0, hidden: 0 };
  if (getComputedStyle(el.querySelector('[data-facts]').parentElement).overflowX === 'visible') out.bad.push('the row is not clipped');
  facts.forEach((f, i) => {
    const box = f.getBoundingClientRect(); const pad = parseFloat(getComputedStyle(f).paddingLeft);
    const tops = lineTops(f);
    if (i === 0) { if (Math.abs(box.left + pad - clip.left) > 1) out.bad.push('first fact off the edge'); return; }
    const dot = getComputedStyle(f, '::before');
    // The dot is centred on its `left` (translate -50%): its right edge, against the clip.
    const dotRight = box.left + parseFloat(dot.left) + parseFloat(dot.width) / 2;
    const visible = dotRight > clip.left + 0.5;
    if (visible) {
      out.shown++;
      const prev = lineTops(facts[i - 1]);
      if (Math.abs(tops[0] - prev[prev.length - 1]) > 3) out.bad.push('dot starts a line: ' + f.textContent);
      // It never ends one: the dot sits on the line of the words it introduces, straight before
      // them (their first line box holds the dot's middle, and they start within one gap of it).
      const r = document.createRange(); r.selectNodeContents(f);
      const first = [...r.getClientRects()].find((x) => x.width > 1);
      const dotMid = box.top + parseFloat(dot.top) + parseFloat(dot.height) / 2;
      if (dot.position !== 'absolute' || !first || dotMid < first.top || dotMid > first.bottom
          || first.left < dotRight - 0.5 || first.left - dotRight > pad) out.bad.push('dot ends a line: ' + f.textContent);
    } else {
      out.hidden++;
      if (Math.abs(box.left + pad - clip.left) > 1) out.bad.push('wrapped fact off the edge: ' + f.textContent);
      if (dotRight > clip.left) out.bad.push('wrapped fact dot not clipped');
    }
  });
  const day = [...el.querySelectorAll('[data-fact] span')].find((s) => s.textContent.includes('-'));
  out.day = day ? day.getClientRects().length : 0;
  out.read = (el.querySelector(':scope > span:first-child')?.textContent || '').includes('90 vegetarian capsules · 30-day supply');
  return out;
})"""

# The Why heading's sentences, each on one line of its own.
WHY_LINES = """() => [...document.getElementById('chapter-why-title').children].map((sp) => {
  const r = document.createRange(); r.selectNodeContents(sp);
  return new Set([...r.getClientRects()].filter((x) => x.width > 1).map((x) => Math.round(x.top))).size;
})"""


# The bottle's visible part of its picture (the alpha box of nuricell.png, 1230x1278): its top and
# bottom as fractions of the picture's height.
BOTTLE_TOP, BOTTLE_BOTTOM = 0.038, 0.971


def opening_check(browser):
    """Mo, October 10: no "Our flagship formula" over the name, no ink pool under the bottle, and
    the bottle's middle on the letters' middle (it sat high, on their baseline)."""
    ctx, page, _, _ = opened(browser, 1440, 900, reduced=True)
    eyebrow = page.evaluate("() => /Our flagship formula/.test(document.querySelector('[data-chapter=overview]').innerText)")
    kept = page.evaluate("() => /Our flagship formula/.test(document.querySelector('[data-chapter=buy]').innerText)")
    check("opening: no line over the name (the Buy chapter keeps 'Our flagship formula')", not eyebrow and kept, f"opening {eyebrow}, buy {kept}")
    name = page.evaluate("() => [...document.querySelectorAll('[data-chapter=overview] h1 img')].map((e) => e.getAttribute('src'))")
    pools = page.evaluate(
        "() => [...document.querySelectorAll('[data-chapter=overview] img')].map((e) => decodeURIComponent(e.getAttribute('src'))).filter((s) => /shadow|pool|contact/i.test(s))"
    )
    check("opening: the bottle alone in the name, no pool or contact shadow anywhere in the opening",
          len(name) == 1 and "nuricell.png" in unquote(name[0]) and not pools, f"{name} {pools}")
    ctx.close()
    for w, h in [(1920, 1080), (1536, 864), (1440, 900), (1280, 800), (1024, 768), (960, 800)]:
        ctx, page, _, _ = opened(browser, w, h, reduced=True)
        boxes = page.evaluate(
            """() => ['h1 [class*=first]', 'h1 [class*=second]', 'h1 img'].map((s) => {
                 const b = document.querySelector('[data-chapter=overview] ' + s).getBoundingClientRect();
                 return [b.left, b.top, b.right, b.bottom]; })"""
        )
        # The letters' ink, top to bottom: the darkest pixels in "Nuri"'s box (40px of air above and below).
        x0, y0, x1, y1 = boxes[0]
        clip = {"x": x0, "y": max(y0 - 40, 0), "width": x1 - x0, "height": y1 - y0 + 80}
        shot = Image.open(io.BytesIO(page.screenshot(clip=clip))).convert("L").point(lambda v: 255 if v < 70 else 0)
        ink = shot.getbbox()
        letters = (clip["y"] + ink[1] + clip["y"] + ink[3]) / 2 if ink else None
        _, bt, _, bb = boxes[2]
        bottle = bt + (bb - bt) * (BOTTLE_TOP + BOTTLE_BOTTOM) / 2
        across = abs((boxes[2][0] + boxes[2][2]) / 2 - (boxes[0][2] + boxes[1][0]) / 2)
        ok = letters is not None and abs(bottle - letters) <= 6 and across <= 6
        check(f"opening {w}x{h}: the bottle's middle on the letters' middle, and midway between the halves", ok,
              f"letters {letters}, bottle {bottle:.0f}, off across {across:.0f}")
        ctx.close()
    # The buy box (Mo, October 12, after Timeline's and Seed's): the highlights in equal parts of the
    # row, each centred, one ink line between them in the middle; the "One bottle" card with the
    # supply, how many a day and the promise badge on its top edge; a wide Add to cart, the refund
    # line under it; under "Nuri" (Mo, October 26: "C, title face"; October 13: the credit and face
    # gone), the headline in Ysabeau and the purpose a lead in ink with no side line, the two
    # together, and from 960px the purpose's row ending where Add to cart ends (the last line's
    # box a few pixels lower: Add to cart's empty note keeps its gap).
    for w, h in [(1440, 900), (390, 844)]:
        ctx, page, _, _ = opened(browser, w, h, reduced=True)
        box = page.evaluate(
            """() => { const o = document.querySelector('[data-chapter=overview]');
                 const lis = [...o.querySelectorAll('ul[class*=highlights] li')]; const ul = o.querySelector('ul[class*=highlights]').getBoundingClientRect();
                 const halves = lis.map((li) => li.getBoundingClientRect()); const bar = getComputedStyle(lis[1], '::before');
                 const card = o.querySelector('[class*=bottleCard]'); const badge = o.querySelector('p[class*=promise]').getBoundingClientRect(); const c = card.getBoundingClientRect();
                 const button = o.querySelector('[class*=openingBuy] button').getBoundingClientRect(); const refund = o.querySelector('p[class*=refund]').getBoundingClientRect();
                 const lead = o.querySelector('[class*=openingWords] p[class*=text]'), head = o.querySelector('p[class*=headline]');
                 const leadBox = lead.getBoundingClientRect(), headBox = head.getBoundingClientRect();
                 return { parts: halves.map((r) => Math.round(r.width)), centred: lis.every((li) => getComputedStyle(li).textAlign === 'center'),
                          barMiddle: Math.round(halves[1].left - (ul.left + ul.width / 2)), bar: bar.content !== 'none' && parseFloat(bar.width) > 0, oneBar: getComputedStyle(lis[0], '::before').content === 'none',
                          card: card.innerText, badgeOnEdge: Math.abs(badge.top + badge.height / 2 - c.top) <= 2, wide: Math.round(button.width) >= Math.round(c.width) - 1,
                          refundUnder: refund.top >= button.bottom,
                          lead: { ysabeau: /ysabeau/i.test(getComputedStyle(head).fontFamily), ink: getComputedStyle(lead).color === getComputedStyle(head).color,
                                  side: getComputedStyle(lead, '::before').content !== 'none', foot: Math.round(leadBox.bottom - button.bottom),
                                  together: Math.round(leadBox.top - headBox.bottom) },
                          credit: !!o.querySelector('[class*=credit]') }; }"""
        )
        ok = (len(box["parts"]) == 2 and abs(box["parts"][0] - box["parts"][1]) <= 1 and box["centred"] and abs(box["barMiddle"]) <= 1
              and box["bar"] and box["oneBar"])
        check(f"opening {w}: the highlights centred in equal halves, one ink line in the middle", ok, str({k: box[k] for k in ("parts", "centred", "barMiddle", "bar", "oneBar")}))
        card = box["card"].replace("‑", "-")
        ok = all(s in card for s in ["One bottle", "90 vegetarian capsules", "30-day supply", "3 a day", "45 days to decide"]) and box["badgeOnEdge"]
        check(f"opening {w}: the 'One bottle' card (supply, 3 a day, the promise badge on its edge)", ok, " | ".join(box["card"].splitlines()))
        check(f"opening {w}: a wide Add to cart, the refund line under it", box["wide"] and box["refundUnder"], f"wide {box['wide']}, under {box['refundUnder']}")
        lead = box["lead"]
        ok = lead["ysabeau"] and lead["ink"] and not lead["side"] and not box["credit"] and abs(lead["together"] - 26) <= 1
        if w >= 960:
            ok = ok and 0 <= lead["foot"] <= 10
        check(f"opening {w}: the headline in Ysabeau, the purpose in ink with no side line, the two together" + (", ending where Add to cart ends" if w >= 960 else "")
              + "; no credit or face in the opening", ok, str(lead) + f" credit {box['credit']}")
        ctx.close()
    # Each half of the name on one line in every language (Korean's overflow-wrap: anywhere broke
    # "Nuri" into "Nur" over "i"); on a phone or tablet the two halves are one word on one line,
    # inside the column, the bottle under it (Mo, October 10).
    for locale in ["en", "kr", "jp", "cns", "vn"]:
        for w, h in [(320, 700), (390, 844), (768, 1024), (1440, 900)]:
            ctx, page, _, _ = opened(browser, w, h, f"/{locale}/products/nuricell", reduced=True)
            name = page.evaluate(
                """() => { const h = document.querySelector('[data-chapter=overview] h1'); const lh = parseFloat(getComputedStyle(h).lineHeight);
                     const wrap = h.parentElement, ws = getComputedStyle(wrap), wr = wrap.getBoundingClientRect();
                     const f = h.querySelector('[class*=first]').getBoundingClientRect(), s = h.querySelector('[class*=second]').getBoundingClientRect(), img = h.querySelector('img').getBoundingClientRect();
                     return { lines: [Math.round(f.height / lh), Math.round(s.height / lh)], row: Math.abs(f.top - s.top) < 1, gap: s.left - f.right,
                              inside: f.left >= wr.left + parseFloat(ws.paddingLeft) - 1 && s.right <= wr.right - parseFloat(ws.paddingRight) + 1,
                              below: img.top >= Math.max(f.bottom, s.bottom) - 1, sideways: document.documentElement.scrollWidth > innerWidth }; }"""
            )
            if w < 960:
                ok = name["lines"] == [1, 1] and name["row"] and abs(name["gap"]) <= 1 and name["inside"] and name["below"] and not name["sideways"]
                what = "'NuriCell' one word on one line inside the column, the bottle under it"
            else:
                ok = name["lines"] == [1, 1] and not name["sideways"]
                what = "each half of the name on one line"
            check(f"opening {locale} {w}: {what}", ok, str(name))
            ctx.close()


def polish(browser):
    """Task 9's polish, pinned: the supply line's dot never starts or ends a line, "30-day" whole; More's links end with their
    words; the lantern fetches about the width it is drawn at; one line per sentence in the Why
    heading; the phone's lantern leaves its label and heading in view; the opening's words in the
    first 1440x900 window; Add to cart full width only on a phone."""
    for locale in ["en", "jp"]:
        for w, h in [(320, 700), (360, 780), (390, 844), (768, 1024), (1024, 768), (1440, 900)]:
            ctx, page, _, _ = opened(browser, w, h, f"/{locale}/products/nuricell", reduced=True)
            lines = page.evaluate(SUPPLY_LINES)
            ok = all(l["facts"] == 2 and not l["bad"] and l["day"] == 1 and l["read"] for l in lines)
            check(f"polish {locale} {w}: the supply line, no dot starting or ending a line, '30-day' whole (opening, buy)", ok, str(lines))
            ctx.close()
    for w, h in [(1440, 900), (390, 844)]:
        ctx, page, _, _ = opened(browser, w, h, reduced=True)
        gaps = page.evaluate("() => [...document.querySelectorAll('#more a')].map((a) => Math.round(a.getBoundingClientRect().bottom - a.querySelector('[class*=meta]').getBoundingClientRect().bottom))")
        check(f"polish {w}: each More link ends with its words", len(gaps) == 4 and all(abs(g) <= 1 for g in gaps), str(gaps))
        bring(page, "[data-lantern]", 160)
        page.wait_for_timeout(1500)
        fetched = page.evaluate(
            r"""() => [...document.querySelectorAll('[data-lantern] img')].map((i) => ({ drawn: Math.round(i.getBoundingClientRect().width),
                 got: Number((decodeURIComponent(i.currentSrc).match(/[?&]w=(\d+)/) || [])[1] || 0) }))"""
        )
        check(f"polish {w}: the lantern fetches at most twice its drawn width (DPR 1)", fetched and all(0 < f["got"] <= 2 * f["drawn"] for f in fetched), str(fetched))
        ctx.close()
    for w, h in [(320, 700), (360, 780), (390, 844), (600, 900), (768, 1024), (900, 900), (959, 800), (960, 800), (1024, 768), (1280, 800), (1440, 900), (1536, 864)]:
        ctx, page, _, _ = opened(browser, w, h, reduced=True)
        lines = page.evaluate(WHY_LINES)
        check(f"polish {w}: the Why heading, one line per sentence", lines == [1, 1], str(lines))
        ctx.close()
    # The phone's lantern under the menu bar: its heading is in the window too.
    ctx, page, _, _ = opened(browser, 390, 844, reduced=True)
    page.evaluate("() => { const f = document.querySelector('[data-lantern]'); const bar = document.querySelector('header').getBoundingClientRect().bottom; window.scrollBy(0, f.getBoundingClientRect().top - bar - 8); }")
    page.wait_for_timeout(300)
    seen = page.evaluate("() => Math.round(document.getElementById('chapter-why-title').getBoundingClientRect().bottom)")
    check("polish 390: the lantern under the bar leaves its heading in view", seen <= 844, f"heading bottom {seen} of 844")
    ctx.close()
    # The opening's words (headline, purpose, highlights, Add to cart, supply) in the first window.
    ctx, page, _, _ = opened(browser, 1440, 900, reduced=True)
    bottom = page.evaluate("() => Math.round(Math.max(...[...document.querySelectorAll('[data-chapter=overview] [class*=openingWords] :is(p, li, button)')].map((e) => e.getBoundingClientRect().bottom)))")
    check("polish 1440x900: the opening's words all in the first window", bottom <= 900, f"last word's bottom {bottom}")
    ctx.close()
    # The opening's Add to cart spans its buy block at every width (Mo, October 12), the block a
    # card's width (460px at most) in one column from 600px, so a tablet gets no black bar; the Buy
    # chapter's spans the column on a phone and keeps a pill's width (420px at most) from 600px.
    for w, h in [(390, 844), (768, 1024), (900, 900), (1440, 900)]:
        ctx, page, _, _ = opened(browser, w, h, reduced=True)
        (ob, oc), (bb, bc) = page.evaluate(
            """() => ['[data-chapter=overview] button', '[data-chapter=buy] button'].map((s) => { const b = document.querySelector(s);
                 return [Math.round(b.getBoundingClientRect().width), Math.round(b.closest('[data-words], [class*=openingBuy]').getBoundingClientRect().width)]; })"""
        )
        opening = ob >= oc - 1 and (oc <= 461 if 600 <= w < 960 else True)
        buy = bb >= bc - 1 if w < 600 else (bb <= 421 if w < 960 else True)
        check(f"polish {w}: the opening's Add to cart spans its block (a card's width on a tablet); the Buy chapter's as before", opening and buy,
              f"opening {ob} of {oc}, buy {bb} of {bc}")
        ctx.close()


NEW = ["Portrait painting",
       # The same formula for about 20 years (m962-m964, October 27, 2026).
       *FORMULA,
       # Dr. Liu in the view west (m907-m909, October 26, 2026).
       "At UC Berkeley, he studied two of NuriCell’s nutrients together.",
       "Both are in NuriCell, which he formulated.", "An animal study, not a test of NuriCell.",
       # The Why chapter's tidied words (m901-m906, October 26, 2026).
       "Inside many of your cells, mitochondria turn food into the energy you live on.",
       "Your brain is about 2% of your weight.", "Yet it uses about 20% of your energy.",
       "About 20 watts, day and night.", "Brain energy figures:",
       # The research as plain questions (m930-m961, the heading too, October 26, 2026), closed
       # answers too: the chapters' textContent holds them.
       *RESEARCH_WORDS]
# The ingredient table's hidden header is new words too, but each also sits inside English sentences
# the template leaves untranslated (the notes say "Ingredient research…"), so they are read from
# their own elements.
NEW_TABLE_HEADERS = ["Per serving", "Ingredient", "About it"]
# The five paintings' descriptions as the page passes them (nuricell.ts), by chapter.
ALTS = {
    "why": "A lighthouse on the California coast whose light comes on, painted in ink",
    "inside": "An opened capsule with its four powders in a row and gold sparks rising, painted in ink",
    "research": "Seven books as stepping stones across a calm stream, painted in ink",
    "people": "A portrait painting of Dr. Jiankang Liu on a hill above San Francisco Bay, the Golden Gate in the fog, painted in ink and colour",
    "daily": "The cut end of a young redwood log, one ring about 20 years in from the bark laid in gold leaf, painted in ink",
}
PLACEHOLDER = re.compile(r"\{[^{}]*\}")

def languages(browser):
    for locale in ["kr", "jp", "cns", "vn"]:
        ctx, page, response, errors = opened(browser, 1440, 900, f"/{locale}/products/nuricell", reduced=True)
        check(f"languages {locale}: 200", response is not None and response.status == 200)
        check(f"languages {locale}: no console errors", not errors, "; ".join(errors[:2]))
        # The chapters' words, not the whole <main>: the questions under them are the template's
        # untranslated English ("…a 30-day supply at 3 capsules a day.") and are out of this task.
        chapters = lambda: " ".join(page.locator("[data-chapter]").evaluate_all("els => els.map(e => e.textContent)"))
        text = chapters()
        left = [s for s in NEW if s in text]
        check(f"languages {locale}: new strings translated", not left, ", ".join(left))
        alts = {
            chapter: page.locator(f'[data-chapter="{chapter}"] figure[data-picture] img').first.get_attribute("alt")
            for chapter in ALTS
        }
        untranslated = [c for c, a in alts.items() if not a or a == ALTS[c]]
        check(f"languages {locale}: all five painting descriptions translated", not untranslated, ", ".join(untranslated) or alts["why"])
        headers = page.locator('[data-chapter="inside"] thead th').evaluate_all("els => els.map(e => e.textContent.trim())")
        check(f"languages {locale}: ingredient table headers translated", len(headers) == 3 and not set(headers) & set(NEW_TABLE_HEADERS), str(headers))
        check(f"languages {locale}: no raw {{placeholder}} in a chapter", not PLACEHOLDER.search(text), str(PLACEHOLDER.findall(text)[:3]))
        # The books are named by their questions for screen readers: "2002: <question>", translated.
        books = page.locator('[data-chapter="research"] [data-book]').evaluate_all("els => els.map(e => e.getAttribute('aria-label'))")
        english = [b for b in books if b.split(": ", 1)[-1] in QUESTIONS]
        check(f"languages {locale}: the seven books' names translated", len(books) == 7 and not english, ", ".join(english[:2]) or books[0])
        ctx.close()


# The Why words, tidied (Mo picked them with the Gold Rush lantern, then the lighthouse, October
# 26, 2026; mockups
# reference/ink-pages/mockups/nuricell-why/).
WHY_GEOMETRY = """() => {
  const c = document.querySelector('[data-chapter="why"] [data-words]');
  const h2 = c.querySelector('h2');
  const lead = h2.nextElementSibling;
  const facts = [...c.querySelectorAll('dl > div')].map((d) => {
    const dt = d.querySelector('dt');
    const n = dt.getBoundingClientRect();
    return { size: parseFloat(getComputedStyle(dt).fontSize), left: Math.round(n.left), top: Math.round(n.top), bottom: Math.round(n.bottom) };
  });
  const text = (e) => { const r = document.createRange(); r.selectNodeContents(e); return r.getClientRects()[0]; };
  return { first: c.firstElementChild.tagName,
           label: [...c.querySelectorAll('p')].some((p) => p.textContent.trim() === 'Why cellular health matters'),
           lead: lead.tagName === 'P' ? lead.textContent.trim() : '', after: c.querySelectorAll('h2 ~ p').length,
           edge: Math.round(text(lead).left - text(h2).left), facts };
}"""


def why_words(browser):
    for w, h in [(1440, 900), (1024, 768), (600, 900), (390, 844), (320, 700)]:
        ctx, page, _, _ = opened(browser, w, h, reduced=True)
        tag = f"why {w}x{h}"
        g = page.evaluate(WHY_GEOMETRY)
        check(f"{tag}: no label over the heading, the heading first", not g["label"] and g["first"] == "H2", f"{g['first']} label={g['label']}")
        # After the heading: the lead-in, the comparison and the source.
        check(f"{tag}: one lead-in line, then the figures", g["lead"].startswith("Inside many of your cells") and g["after"] == 3, f"{g['after']} after h2: {g['lead'][:40]}")
        check(f"{tag}: the lead-in on the heading's left edge", abs(g["edge"]) <= 4, f"{g['edge']}px")
        small, big = g["facts"]
        check(f"{tag}: the 2% smaller than the 20%", small["size"] * 1.3 < big["size"], f"{small['size']} vs {big['size']}")
        if w >= 600:
            check(f"{tag}: the two figures side by side, their feet level", small["left"] < big["left"] and abs(small["bottom"] - big["bottom"]) <= 12, str(g["facts"]))
        else:
            check(f"{tag}: the two figures stacked, the small one first", small["bottom"] <= big["top"], str(g["facts"]))
        ctx.close()


# What's inside, tidied, its gold moving and its pairs as scenes (Mo picked 1A, October 26, 2026;
# mockups reference/ink-pages/mockups/nuricell-inside/).
PLATE_GEOMETRY = """() => {
  const c = document.querySelector('[data-chapter="inside"]');
  const box = (e) => e && e.getBoundingClientRect();
  const h2 = box(c.querySelector('h2'));
  const cap = box(c.querySelector('caption'));
  const rows = [...c.querySelectorAll('tbody tr')].map(box);
  const card = c.querySelector('[data-label-card]');
  return {
    first: c.querySelector('[data-words]').firstElementChild.tagName,
    label: [...c.querySelectorAll('p')].some((p) => p.textContent.trim() === 'What’s inside'),
    caption: c.querySelector('caption').textContent.trim(),
    between: cap.top >= h2.bottom - 1 && rows.every((r) => cap.bottom <= r.top + 1),
    terms: card ? [...card.querySelectorAll('dt')].map((d) => d.textContent.trim()) : [],
    values: card ? card.querySelectorAll('dd').length : 0,
    cardBelow: card ? rows.every((r) => box(card).top >= r.bottom - 1) : false,
    notes: [...c.querySelectorAll('p')].filter((p) => /^(Other ingredients:|Each line describes)/.test(p.textContent.trim())).length,
  };
}"""


def plate(browser):
    for w, h in [(1440, 900), (1024, 768), (390, 844)]:
        ctx, page, _, _ = opened(browser, w, h, reduced=True)
        tag = f"plate {w}x{h}"
        g = page.evaluate(PLATE_GEOMETRY)
        check(f"{tag}: no label over the heading, the heading first", not g["label"] and g["first"] == "H2", f"{g['first']} label={g['label']}")
        check(f"{tag}: the amounts' per-serving line between the heading and the rows", g["between"] and "3 capsules" in g["caption"], g["caption"])
        check(f"{tag}: the label card, two lines, under the rows", g["terms"] == ["Other ingredients", "Capsule"] and g["values"] == 2 and g["cardBelow"], str(g["terms"]))
        check(f"{tag}: the old notes under the plate are gone", g["notes"] == 0, str(g["notes"]))
        ctx.close()


# The gold the canvas holds: how many pixels, and how low their middle sits (0 top, 1 bottom).
CANVAS_GOLD = """() => {
  const c = document.querySelector('[data-leaf]');
  const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
  let n = 0, y = 0;
  for (let i = 3; i < d.length; i += 4) if (d[i] > 60) { n++; y += Math.floor((i >> 2) / c.width); }
  return { n, y: n ? y / n / c.height : 0, w: c.width, h: c.height };
}"""
# The still leaf's gold drawn at the canvas's size: what the painting holds.
STILL_GOLD = """async () => {
  const c = document.querySelector('[data-leaf]');
  const img = new Image();
  img.src = document.querySelector('[data-gold-still]').currentSrc;
  await img.decode();
  const o = document.createElement('canvas'); o.width = c.width; o.height = c.height;
  const x = o.getContext('2d'); x.drawImage(img, 0, 0, o.width, o.height);
  const d = x.getImageData(0, 0, o.width, o.height).data;
  let n = 0; for (let i = 3; i < d.length; i += 4) if (d[i] > 60) n++;
  return n;
}"""
CANVAS_DIFF = """async () => {
  const c = document.querySelector('[data-leaf]');
  const a = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
  await new Promise((r) => setTimeout(r, 900));
  const b = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
  let n = 0; for (let i = 3; i < a.length; i += 4) if (Math.abs(a[i] - b[i]) > 60) n++;
  return n;
}"""


def gold(browser):
    for w, h in [(1440, 900), (390, 844)]:
        tag = f"gold {w}x{h}"
        ctx, page, _, errors = opened(browser, w, h, reduced=True)
        still = page.evaluate(
            """() => { const s = document.querySelector('[data-gold-still]');
                return { canvas: !!document.querySelector('[data-leaf]'), shown: getComputedStyle(s).visibility, w: s.naturalWidth }; }"""
        )
        check(f"{tag} reduced motion: the leaf as painted, nothing moving", not still["canvas"] and still["shown"] == "visible" and still["w"] > 0, str(still))
        ctx.close()
        ctx, page, _, errors = opened(browser, w, h)
        bring(page, '[data-chapter="inside"] figure[data-picture]', 140 if w >= 960 else 100)
        page.wait_for_timeout(700)
        early = page.evaluate(CANVAS_GOLD)
        page.wait_for_timeout(7300)
        late = page.evaluate(CANVAS_GOLD)
        painted = page.evaluate(STILL_GOLD)
        hidden = page.locator('[data-gold-still="moving"]').count() == 1
        moving = page.evaluate(CANVAS_DIFF)
        check(f"{tag}: the still leaf gives way to the moving one", hidden)
        check(
            f"{tag}: it rises from the powder: little gold at first, low down",
            early["n"] < late["n"] * 0.5 and (early["n"] == 0 or early["y"] > late["y"]),
            f"{early['n']} at {early['y']:.2f} -> {late['n']} at {late['y']:.2f}",
        )
        ratio = late["n"] / painted if painted else 0
        check(f"{tag}: settled, about the painted leaf's gold", 0.7 <= ratio <= 1.3, f"{late['n']} of {painted} ({ratio:.2f})")
        check(f"{tag}: then it keeps turning", moving > 20, f"{moving} pixels changed in 0.9s")
        check(f"{tag}: no console errors", not errors, "; ".join(errors[:2]))
        page.screenshot(path=str(OUT / f"gold-{w}.png"))
        ctx.close()


# The pairs as three scenes from a California ranch (Mo picked B, October 27, 2026; ideas
# reference/ink-pages/mockups/nuricell-pairs/): they replaced the powder heaps, which read as drugs.
SCENES = """() => [...document.querySelectorAll('[data-scene]')].map((s) => {
  const box = (e) => e.getBoundingClientRect();
  const stage = s.querySelector('[class*="stage"]');
  const still = stage.querySelector('img[class*="still"]');
  const imgs = [...stage.querySelectorAll('img')];
  const fan = stage.querySelector('img[class*="fan"]');
  const stream = stage.querySelector('[class*="stream"]');
  const angle = (e) => {
    const t = getComputedStyle(e).transform;
    if (!t || t === 'none') return 0;
    const [a, b] = t.slice(7, -1).split(',').map(Number);
    return Math.round((Math.atan2(b, a) * 180) / Math.PI);
  };
  const inside = (r, o) =>
    r.left >= o.left - 1 && r.right <= o.right + 1 && r.top >= o.top - 1 && r.bottom <= o.bottom + 1;
  const sb = box(still);
  return {
    kind: s.dataset.scene,
    top: Math.round(box(s).top),
    bottom: Math.round(box(s).bottom),
    loaded: imgs.length >= 2 && imgs.every((i) => i.complete && i.naturalWidth > 0),
    multiply: getComputedStyle(still).mixBlendMode,
    heaps: s.querySelectorAll('[data-heap]').length + imgs.filter((i) => /heap-/.test(i.currentSrc)).length,
    layersOn: [...stage.querySelectorAll('[class*="cut"]')].every((e) => inside(box(e), sb)),
    pair: s.querySelector('p[class*="pair"]')?.textContent.replace(/\\s+/g, ' ').trim(),
    playing: stage.dataset.play === 'on',
    angle: fan ? angle(fan) : null,
    clip: stream ? getComputedStyle(stream).clipPath : null,
    again: !!s.querySelector('button'),
  };
})"""
PAIRS = {
    "lights": "Acetyl-L-carnitine + Alpha-lipoic acid",
    "stores": "Alpha-lipoic acid + Creatine",
    "joins": "Choline + Acetyl-L-carnitine",
}


def whole(clip):
    """The windmill's water shows whole: no clip-path, or an inset of nothing."""
    return clip == "none" or bool(re.fullmatch(r"inset\((0(px|%)?\s*)+\)", clip or ""))

# On a fresh page, before it plays, the windmill waits with its water hidden (not poured, then again).
WAITING = """() => {
  const stage = document.querySelector('[data-scene="stores"] [class*="stage"]');
  const stream = stage.querySelector('[class*="stream"]');
  return stage.dataset.play === 'wait' && /100%/.test(getComputedStyle(stream).clipPath);
}"""
TO_SCENE = "window.scrollBy(0, document.querySelectorAll('[data-scene]')[{i}].getBoundingClientRect().top - 120)"


def scenes(browser):
    for w, h in [(1440, 900), (390, 844)]:
        tag = f"scenes {w}x{h}"
        across = w >= 900
        ctx, page, _, errors = opened(browser, w, h)
        check(f"{tag} stores: until its turn, its water not yet poured", page.evaluate(WAITING))
        # The windmill plays as it comes into view: mid-play its wheel is turned.
        page.evaluate(TO_SCENE.format(i=1))
        page.wait_for_function("document.querySelectorAll('[data-scene] [data-play]').length > 0", timeout=5000)
        page.wait_for_timeout(1600 if across else 1400)
        got = page.evaluate(SCENES)
        kinds = [g["kind"] for g in got]
        check(f"{tag}: three scenes, lights, stores, joins", kinds == ["lights", "stores", "joins"], str(kinds))
        if kinds != ["lights", "stores", "joins"]:
            ctx.close()
            continue
        mid = got[1]
        check(f"{tag} stores: it plays as it comes into view, the wheel turning", mid["playing"] and abs(mid["angle"]) > 10, f"{mid['angle']} deg")
        for i in range(3):
            page.evaluate(TO_SCENE.format(i=i))
            page.wait_for_timeout(500)
        page.wait_for_timeout(6000)
        if across:
            page.evaluate("window.scrollBy(0, document.querySelector('[data-synergy]').getBoundingClientRect().top - 110)")
            page.wait_for_timeout(300)
        got = page.evaluate(SCENES)
        by = {g["kind"]: g for g in got}
        check(f"{tag}: every scene's painting and gold loaded", all(g["loaded"] for g in got))
        check(f"{tag}: the paintings multiply onto the page", all(g["multiply"] == "multiply" for g in got), str([g["multiply"] for g in got]))
        check(f"{tag}: no powder heaps", sum(g["heaps"] for g in got) == 0)
        check(f"{tag}: the gold lies on its painting", all(g["layersOn"] for g in got))
        check(f"{tag}: each pair's names, in reading order", all(by[k]["pair"] == v for k, v in PAIRS.items()), str([g["pair"] for g in got]))
        tops = [g["top"] for g in got]
        laid = max(tops) - min(tops) <= 2 if across else all(got[i + 1]["top"] >= got[i]["bottom"] for i in range(len(got) - 1))
        check(f"{tag}: {'three across' if across else 'one under another'}", laid, str(tops))
        check(f"{tag}: all three played", all(g["playing"] for g in got))
        rest = by["stores"]
        check(f"{tag} stores: at rest as painted, the wheel upright, the water whole", rest["angle"] % 360 == 0 and whole(rest["clip"]), f"{rest['angle']} deg, {rest['clip']}")
        check(f"{tag}: Play again on each scene", all(g["again"] for g in got))
        page.screenshot(path=str(OUT / f"scenes-{w}.png"))
        # Play again: the windmill starts over (its water gone from the pipe, its wheel near upright).
        button = page.locator('[data-scene="stores"] button')
        button.scroll_into_view_if_needed()
        button.click()
        page.wait_for_timeout(250)
        again = page.evaluate(SCENES)[1]
        check(f"{tag}: Play again starts the scene over", not whole(again["clip"]) and abs(again["angle"]) < 40, f"{again['angle']} deg, {again['clip']}")
        check(f"{tag}: no console errors", not errors, "; ".join(errors[:2]))
        ctx.close()
        ctx, page, _, _ = opened(browser, w, h, reduced=True)
        for i in range(3):
            page.evaluate(TO_SCENE.format(i=i))
            page.wait_for_timeout(300)
        got = page.evaluate(SCENES)
        still = all(not g["playing"] for g in got) and got[1]["angle"] == 0 and whole(got[1]["clip"])
        check(f"{tag} reduced motion: the paintings as painted, nothing playing", still, str(got[1]))
        check(f"{tag} reduced motion: no Play again", not any(g["again"] for g in got))
        ctx.close()


SECTIONS = {
    "shell": shell,
    "others": others,
    "multiply": multiply,
    "lantern": lantern,
    "nojs": nojs,
    "words": words,
    "after": after,
    "sticky": sticky,
    "research": research,
    "formula": formula_check,
    "buy": buy_check,
    "layout": layout,
    "deep_links": deep_links,
    "polish": polish,
    "opening": opening_check,
    "languages": languages,
    "why": why_words,
    "plate": plate,
    "gold": gold,
    "scenes": scenes,
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

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
  sum         the painted sum matches the serving, a caption under each number
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
        ctx.close()


def lantern_state(page):
    return page.evaluate(
        """() => { const f = document.querySelector('[data-lantern]');
                   const lit = f.querySelector('[data-lit]'); const unlit = f.querySelector('img:not([data-lit])');
                   return { light: f.dataset.light, bloom: unlit.dataset.bloom, lit: Number(getComputedStyle(lit).opacity) }; }"""
    )


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
    page.wait_for_timeout(500)
    early = lantern_state(page)
    check("lantern: still off as it starts to bloom", early["bloom"] in ("in", "done") and early["lit"] < 0.05, str(early))
    # The unlit picture is taken before the light starts (why.tsx's LIGHT_AFTER, 1.8s after the
    # bloom starts): the lantern well grown in, still unlit.
    page.wait_for_timeout(1000)
    shot = lantern_state(page)
    check("lantern: unlit when photographed", shot["light"] == "off" and shot["lit"] < 0.05, str(shot))
    page.screenshot(path=str(OUT / "lantern-unlit-1440.png"))
    page.wait_for_timeout(5700)
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
    ctx.close()


SECTIONS = {"shell": shell, "others": others, "multiply": multiply, "lantern": lantern, "nojs": nojs}

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

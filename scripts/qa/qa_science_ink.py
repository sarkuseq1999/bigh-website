"""QA for the Science page in Ink & Gold (spec docs/superpowers/specs/2026-10-14-science-ink-design.md;
plan docs/superpowers/plans/2026-10-14-science-ink.md). Since Mo's pick B (October 26, 2026) the page
opens on the title and Dr. Liu, then his path one place per screen going down (the handscroll's
sideways travel and its checks are gone), then research, health explained, the formulas and Ask.

Sections (all, or --only=a,b):
  shell       200 in the ink look, the menu bar marks Science, one h1, the parts' ids in order,
              no canvas, no console errors (1440x900, 390x844); (final review) the shared footer
              promise and the menu's drop-down title in the same face as on About
  people      Dr. Liu's real photo on its mount, on the first screen, his name and role, no numbers
              row (his path tells them), "Read his story" opens his sheet; the five bottles with
              their credits, each linking to its page; DESIGN.md's mount shadow, the intro's margin,
              the bottles, names and credits each on one line per row
  path        (October 26) his four places in order, each painting loaded and bloomed in, the phone
              cut under 960px; from 960px the paintings take turns (left, right, left), each running
              to the page's edge, Today wide with its words in its sky over paper; under 960px one
              column, each painting over its words; each place fits one screen; its caption in the
              painting's box and the window; its links out to their sources
  settled     the parts below the path stand still once every painting has arrived (the menu's and
              the footer's #research, #health and #ask links land by them)
  still       reduced motion and no script: the path's and the strips' paintings whole and crisp
              (no bloom left waiting); print: the path's paintings whole
  multiply    every painting's blend group sits on the page with no stacking context
  strips      research, health and ask: the painting in use (phone crop under 960px) and bloomed in,
              year · kind · journal, the full list, each explainer's own sheet; from 960px the
              columns' titles, words and links each start on one line
  languages   kr, jp, cns, vn: 200, no errors, the research links translated, Dr. Liu named as the
              site names him
  layout      sizes 1920 to 360: no sideways scroll, text 15px+, targets 44px+
  deep_links  #scientists, #research, #health, #formulas, #ask land under the menu bar
Pictures: scripts/qa/out/science-ink/ (webkit/ for --browser=webkit).

usage: python -X utf8 scripts/qa/qa_science_ink.py [base-url] [--only=shell,people,...]
       [--browser=chromium|webkit|firefox]  (default chromium)
"""

import os
import re
import sys
import threading
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeout, sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = ARGS[0] if ARGS else "http://localhost:3050"
ONLY = next((a.split("=", 1)[1].split(",") for a in sys.argv[1:] if a.startswith("--only=")), None)
BROWSER = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--browser=")), "chromium")
REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "scripts/qa/out/science-ink" / ("" if BROWSER == "chromium" else BROWSER)
OUT.mkdir(parents=True, exist_ok=True)
PATH = "/en/science"
PARTS = ["scientists", "research", "health", "formulas", "ask"]
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


# The shared pieces' title face: the footer's promise ("Stay sharp. Live fully.") and the menu
# bar's drop-down title (Products'; Science's drop-down is put away, Mo, October 26, 2026; in the
# page at every width, shown or not).
SHARED_FACES = """() => ['[data-brush="footer-promise"] p', '[data-nav-panel="products"] h2']
  .map(s => { const e = document.querySelector(s); return e ? getComputedStyle(e).fontFamily : null; })"""


def shell(browser):
    for w, h in [(1440, 900), (390, 844)]:
        # (Final review, Ruling 20) The page's Ysabeau is for its own titles only: the menu bar and
        # the footer are shared and read as on About (and NuriCell), in Switzer.
        ctx, page, _, _ = opened(browser, w, h, path="/en/about")
        about = page.evaluate(SHARED_FACES)
        ctx.close()
        ctx, page, response, errors = opened(browser, w, h)
        faces = page.evaluate(SHARED_FACES)
        for name, here, there in zip(["the footer's promise", "the menu's drop-down title"], faces, about):
            check(f"shell {w}: {name} in the same face as on About", here is not None and here == there and "ysabeau" not in here.lower(), f"{here} | About: {there}")
        check(f"shell {w}: 200", response is not None and response.status == 200)
        check(f"shell {w}: ink look", page.locator('[data-look="ink"][data-page="science"]').count() == 1)
        check(f"shell {w}: Science carries the menu's stroke", page.locator('#site-navigation a[href$="/science"][data-ink="here"]').count() == 1)
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


MOUNT_SHADOW = "rgba(12, 11, 10, 0.42) 0px 22px 44px -22px, rgba(12, 11, 10, 0.1) 0px 3px 8px 0px"
# Per row of bottles (bottles whose boxes share some height): their pictures' feet, their names'
# and credits' tops.
BOTTLE_ROWS = """() => {
  const rows = [];
  const at = e => Math.round(e.getBoundingClientRect()[e.tagName === 'IMG' ? 'bottom' : 'top']);
  for (const li of document.querySelectorAll('#formulas li')) {
    const box = li.getBoundingClientRect();
    let r = rows.find(r => box.top < r.bottom && box.bottom > r.top);
    if (!r) { r = { top: box.top, bottom: box.bottom, bottles: [], names: [], credits: [] }; rows.push(r); }
    r.top = Math.min(r.top, box.top); r.bottom = Math.max(r.bottom, box.bottom);
    r.bottles.push(at(li.querySelector('img'))); r.names.push(at(li.querySelector('a span')));
    r.credits.push(at(li.querySelector(':scope > p')));
  }
  return rows.filter(r => r.bottles.length > 1).map(({ bottles, names, credits }) => ({ bottles, names, credits }));
}"""


def people(browser):
    ctx, page, _, errors = opened(browser, 1440, 900)
    bring(page, "#liu")
    page.wait_for_timeout(600)
    photo = page.locator('#liu img[src*="jiankang-liu"]')
    check("people: Dr. Liu's real photo", photo.count() == 1)
    check("people: the photo on its mount", photo.evaluate("i => getComputedStyle(i.closest('figure')).boxShadow") != "none")
    text = page.locator("#liu").inner_text()
    for word in ["Dr. Jiankang Liu", "Chief Scientific Advisor, BiGH"]:
        check(f"people: {word}", word in text)
    # (October 26) His dated record (280+, 1994, 2025) is told by his path, with its sources.
    check("people: no numbers row (his path tells them)", page.locator("#liu dl").count() == 0)
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
    # (Task 6) The same real photo sits the same way on every page: DESIGN.md's one mount shadow.
    shadow = photo.evaluate("i => getComputedStyle(i.closest('figure')).boxShadow")
    check("people: the mount's shadow is DESIGN.md's photo mount", shadow == MOUNT_SHADOW, shadow)
    margin = page.evaluate("getComputedStyle(document.querySelector('#liu h2 ~ p ~ p')).marginTop")
    check("people: the intro keeps its 10px under the headline", margin == "10px", margin)
    check("people: no console errors", not errors, "; ".join(errors[:3]))
    ctx.close()
    # (Task 6) Rows that read as rows: the bottles on one ground line, the names and the credits
    # each starting on one line (per row of bottles). (October 26) He opens the page: his photo
    # starts on the first screen, under the title.
    for w, h in [(1440, 900), (390, 844)]:
        ctx, page, _, _ = opened(browser, w, h)
        rows = page.evaluate(BOTTLE_ROWS)
        for i, row in enumerate(rows):
            for part, edges in row.items():
                check(f"people {w}: bottle row {i + 1}'s {part} on one line", max(edges) - min(edges) <= 1, str(edges))
        top, title = page.evaluate("[document.querySelector('#liu figure').getBoundingClientRect().top, document.querySelector('h1').getBoundingClientRect().bottom]")
        check(f"people {w}: his photo on the first screen, under the title", title < top < h * 0.6, f"title ends {title:.0f}, photo at {top:.0f}")
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

# (October 26) His path: the four places in order, their links' counts.
PATH_NAMES = ["Okayama", "Berkeley", "Salzburg", "Today"]
PATH_LINKS = [1, 2, 1, 0]
PATH_PICTURES = "#scientists [data-place] img"
# The path stops growing at 1600px (path.module.css .places).
PATH_MAX = 1600
PATH_SIZES = [(1920, 1080), (1440, 900), (1366, 657), (1280, 720), (1024, 768), (960, 800), (959, 800), (768, 1024), (390, 844), (360, 740)]
# A place must fit one screen under the menu bar at these sizes (a small phone may need a little more).
ONE_SCREEN = {(1920, 1080), (1440, 900), (1366, 657), (1280, 720), (1024, 768), (960, 800), (768, 1024), (390, 844)}
PLACES = """() => [...document.querySelectorAll('[data-place]')].map(li => {
  const box = e => { const r = e.getBoundingClientRect(); return { l: r.left, t: r.top + scrollY, r: r.right, b: r.bottom + scrollY, w: r.width, h: r.height }; };
  const img = li.querySelector('img'), h3 = li.querySelector('h3'), cap = li.querySelector('figcaption');
  return { key: li.dataset.place, side: li.dataset.side, name: h3.textContent.trim(), li: box(li), img: box(img),
           words: box(h3.parentElement), cap: box(cap), capText: cap.textContent.trim(),
           links: [...li.querySelectorAll('a')].map(a => [a.href, a.target, a.rel]) };
})"""
# The share of the painting's pixels under a part of its words (page px) that are ink (darkest
# channel under 200), read from the picture in use at its own size.
INK_UNDER = """([key, sel]) => new Promise(done => {
  const li = document.querySelector(`[data-place="${key}"]`); const img = li.querySelector('img');
  const r = img.getBoundingClientRect(); const b = li.querySelector(sel).getBoundingClientRect();
  const pic = new Image();
  pic.onload = () => {
    const k = pic.naturalWidth / r.width; const c = document.createElement('canvas');
    c.width = pic.naturalWidth; c.height = pic.naturalHeight; const g = c.getContext('2d'); g.drawImage(pic, 0, 0);
    const x = Math.max(0, Math.round((b.left - r.left) * k)), y = Math.max(0, Math.round((b.top - r.top) * k));
    const w = Math.min(c.width - x, Math.round(b.width * k)), h = Math.min(c.height - y, Math.round(b.height * k));
    const d = g.getImageData(x, y, w, h).data; let ink = 0;
    for (let i = 0; i < d.length; i += 4) if (Math.min(d[i], d[i + 1], d[i + 2]) < 200) ink++;
    done(ink / (d.length / 4));
  };
  pic.src = img.currentSrc;
})"""
CENTRE = """([key, bar]) => { const r = document.querySelector(`[data-place="${key}"]`).getBoundingClientRect();
  window.scrollBy(0, r.top - bar - Math.max(0, (innerHeight - bar - r.height) / 2)); }"""
PAINTING_STATE = """key => { const i = document.querySelector(`[data-place="${key}"] img`); const s = getComputedStyle(i);
  return [i.complete && i.naturalWidth > 0, i.dataset.bloom, s.opacity, s.filter, decodeURIComponent(i.currentSrc)]; }"""


def path(browser):
    for w, h in PATH_SIZES:
        tag = f"path {w}x{h}"
        ctx, page, _, errors = opened(browser, w, h)
        places = page.evaluate(PLACES)
        check(f"{tag}: four places in order", [p["name"] for p in places] == PATH_NAMES, str([p["name"] for p in places]))
        check(f"{tag}: one under another", all(a["li"]["b"] <= b["li"]["t"] + 1 for a, b in zip(places, places[1:])))
        bar = page.evaluate("document.querySelector('header').getBoundingClientRect().bottom")
        for place, links_wanted in zip(places, PATH_LINKS):
            key = place["key"]
            # Brought to the middle of the window, as a visitor scrolls to it; then it blooms in.
            page.evaluate(CENTRE, [key, bar])
            try:
                page.wait_for_function(f"document.querySelector('[data-place=\"{key}\"] img').dataset.bloom === 'done'", timeout=7000)
            except PlaywrightTimeout:
                pass
            state = page.evaluate(PAINTING_STATE, key)
            check(f"{tag} {key}: painting loaded and bloomed in", state[:4] == [True, "done", "1", "none"], str(state[:4]))
            check(f"{tag} {key}: the {'phone' if w < 960 else 'wide'} cut in use", ("-phone-" in state[4]) == (w < 960), state[4][-48:])
            if w in (1440, 390):
                page.screenshot(path=str(OUT / f"path-{w}-{key}.png"))
            img, words, cap, li = place["img"], place["words"], place["cap"], place["li"]
            if (w, h) in ONE_SCREEN:
                check(f"{tag} {key}: fits one screen under the menu bar", li["h"] <= h - bar, f"{li['h']:.0f} of {h - bar:.0f}")
            check(f"{tag} {key}: its caption in the painting's box and the window",
                  place["capText"] == "Illustration" and cap["t"] >= img["t"] - 1 and cap["b"] <= img["b"] + 2 and cap["l"] >= 0 and cap["r"] <= w, str(cap))
            links = place["links"]
            check(f"{tag} {key}: its {links_wanted} link(s) open their sources in a new tab",
                  len(links) == links_wanted and all(href.startswith("https://") and target == "_blank" and "noreferrer" in rel for href, target, rel in links), str(links))
            if w >= 960:
                side = place["side"]
                edge_l, edge_r = max(0, (w - PATH_MAX) / 2), min(w, (w + PATH_MAX) / 2)
                if side == "left":
                    check(f"{tag} {key}: painting left of its words, to the page's edge", img["r"] <= words["l"] + 1 and img["l"] <= edge_l + 1,
                          f"img {img['l']:.0f}-{img['r']:.0f}, words from {words['l']:.0f}")
                elif side == "right":
                    check(f"{tag} {key}: painting right of its words, to the page's edge", img["l"] >= words["r"] - 1 and img["r"] >= edge_r - 1,
                          f"img {img['l']:.0f}-{img['r']:.0f}, words to {words['r']:.0f}")
                else:
                    inside = words["l"] >= img["l"] and words["r"] <= img["r"] and words["t"] >= img["t"] and words["b"] <= img["t"] + img["h"] * 0.5
                    check(f"{tag} {key}: its words in the painting's sky (top half)", inside, f"words {words}, img {img}")
                    sentence = page.evaluate(INK_UNDER, [key, "h3 + p"])
                    name = page.evaluate(INK_UNDER, [key, "h3"])
                    check(f"{tag} {key}: its words over paper, not ink", sentence < 0.01 and name < 0.01, f"ink under the sentence {sentence:.3f}, the name {name:.3f}")
            else:
                check(f"{tag} {key}: one column, the painting over its words", img["b"] <= words["t"] + 1, f"img ends {img['b']:.0f}, words from {words['t']:.0f}")
                check(f"{tag} {key}: the painting the window's width", img["w"] >= w - 1, f"{img['w']:.0f}")
        if w >= 960:
            sides = [p["side"] for p in places]
            check(f"{tag}: the paintings take turns (left, right, left, wide)", sides == ["left", "right", "left", "wide"], str(sides))
        check(f"{tag}: no console errors", not errors, "; ".join(errors[:3]))
        ctx.close()


def still(browser):
    for label, kwargs in [("reduced motion", {"reduced": True}), ("no script", {"js": False})]:
        for w, h in [(1440, 900), (390, 844)]:
            ctx, page, _, _ = opened(browser, w, h, **kwargs)
            page.wait_for_timeout(800)
            # The path's paintings and the strips' (the server marks them "waiting"): shown whole
            # and crisp, a strip's wide one with only its own soft ends (no bloom blot), the path's
            # and a phone scene with no mask at all.
            places = page.locator(PATH_PICTURES).all()
            check(f"still {label} {w}: the path's four paintings show", len(places) == 4 and all(p.is_visible() for p in places), str(len(places)))
            for img in places:
                name = (img.get_attribute("alt") or "")[:36]
                filt, mask, opacity = img.evaluate("i => { const s = getComputedStyle(i); return [s.filter, s.maskImage, s.opacity]; }")
                check(f"still {label} {w}: {name} whole and crisp", filt == "none" and mask == "none" and opacity == "1", f"{filt} | {mask[:40]} | {opacity}")
            pictures = [p for p in page.locator(STRIP_PICTURES).all() if p.is_visible()]
            check(f"still {label} {w}: the strips' paintings show", len(pictures) == (3 if w == 1440 else 5), str(len(pictures)))
            for img in pictures:
                name = (img.get_attribute("alt") or "")[:36]
                filt, mask, opacity, scene = img.evaluate("i => { const s = getComputedStyle(i); return [s.filter, s.maskImage, s.opacity, !!i.closest('[data-scene]')]; }")
                soft_ends = "none" if scene else "linear-gradient(90deg"
                ok = filt == "none" and opacity == "1" and (mask == "none" if scene else (mask.startswith(soft_ends) and "url(" not in mask))
                check(f"still {label} {w}: {name} whole and crisp, only its own soft ends", ok, f"{filt} | {mask[:40]} | {opacity}")
            page.screenshot(path=str(OUT / f"still-{label.replace(' ', '-')}-{w}.png"))
            ctx.close()
    # Printed before the visitor scrolled down: the path's paintings whole (not left waiting).
    for w, h in [(1440, 900), (390, 844)]:
        ctx, page, _, _ = opened(browser, w, h)
        page.wait_for_timeout(800)
        page.emulate_media(media="print")
        page.wait_for_timeout(600)
        shown = page.evaluate("sel => [...document.querySelectorAll(sel)].map(i => { const s = getComputedStyle(i); return s.maskImage === 'none' && s.filter === 'none'; })", PATH_PICTURES)
        check(f"still print {w}: the path's paintings whole", shown == [True] * 4, str(shown))
        ctx.close()


PART_TOPS = "['research', 'health', 'formulas', 'ask'].map(id => Math.round(document.getElementById(id).getBoundingClientRect().top + scrollY))"
SETTLED_SIZES = [(1440, 900, "en"), (1280, 720, "en"), (1024, 768, "en"), (960, 800, "en"), (390, 844, "en"), (360, 740, "en"), (1440, 900, "vn"), (390, 844, "kr")]


def settled(browser):
    # The paintings are lazy and each phone cut has another ratio than its wide one: the stylesheet
    # reserves each one's box (path.module.css, strip.module.css), so once every painting has
    # arrived the parts below stand where they stood before (the menu's links land by them).
    pictures = f"{PATH_PICTURES}, {STRIP_PICTURES}"
    for w, h, lang in SETTLED_SIZES:
        ctx = browser.new_context(viewport={"width": w, "height": h})
        page = ctx.new_page()
        # A first visit warms the cache, so the fonts are there when the page is read.
        page.goto(BASE + f"/{lang}/science", wait_until="networkidle")
        page.goto(BASE + f"/{lang}/science", wait_until="domcontentloaded")
        first = page.evaluate(PART_TOPS)
        page.evaluate("sel => document.querySelectorAll(sel).forEach(i => { i.loading = 'eager'; })", pictures)
        page.wait_for_function(
            "sel => [...document.querySelectorAll(sel)].filter(i => i.offsetParent).every(i => i.complete && i.naturalWidth > 0)",
            arg=pictures,
            timeout=15000,
        )
        page.wait_for_timeout(300)
        arrived = page.evaluate(PART_TOPS)
        for name, before, after in zip(["#research", "#health", "#formulas", "#ask"], first, arrived):
            check(f"settled {w}x{h} {lang}: {name} stays put once the paintings have arrived", abs(after - before) <= 2, f"{before} -> {after}")
        ctx.close()


def multiply(browser):
    for w, h in [(1440, 900), (390, 844)]:
        ctx, page, _, _ = opened(browser, w, h, reduced=True)
        for img in page.locator(f"{PATH_PICTURES}, main figure[data-picture] img, main [data-scene] img").all():
            src = img.get_attribute("src")[:50]
            check(f"multiply {w}: {src} multiplies", img.evaluate("i => getComputedStyle(i).mixBlendMode") == "multiply")
            found = img.evaluate(STACKING)
            check(f"multiply {w}: {src} sits on the paper", not found, "; ".join(found))
        ctx.close()


KEY_META = ["2002 · Animal study · PNAS", "2008 · Review · Neurochem Res", "2023 · Review · Cell"]
EXPLAINER_SHEETS = ["Energy starts small.", "Balance matters.", "Aging is a bigger story."]
# A painting the visitor was meant to see: the strips' wide paintings and the health scenes.
STRIP_PICTURES = "#research figure[data-picture] img, #health figure[data-picture] img, #ask figure[data-picture] img, #health [data-scene] img"


# The tops of each column's title, words and link (the research's link row, or health's button).
COLUMN_ROWS = """sel => {
  const top = e => Math.round(e.getBoundingClientRect().top);
  const cols = [...document.querySelectorAll(sel)];
  return { titles: cols.map(c => top(c.querySelector('h3'))),
           words: cols.map(c => top(c.querySelector('h3 + p'))),
           links: cols.map(c => top(c.querySelector('a, button'))) };
}"""


def tidy(text):
    """Words as read: the word joiner (U+2060, which keeps a dash off a line's start) is no letter."""
    return re.sub(r"\s+", " ", text.replace(chr(0x2060), "")).strip()


def strips(browser):
    for w, h in [(1440, 900), (390, 844)]:
        ctx, page, _, errors = opened(browser, w, h)
        for part in ["research", "health", "ask"]:
            bring(page, f"#{part}")
            page.wait_for_timeout(500)
            check(f"strips {w} {part}: its title", page.locator(f"#{part} h2").count() == 1)
            pics = page.locator(f"#{part} img")
            shown = [p for p in pics.all() if p.is_visible()]
            check(f"strips {w} {part}: a painting shows", len(shown) >= 1, str(len(shown)))
            for img in shown:
                ok = img.evaluate("i => i.complete && i.naturalWidth > 0")
                check(f"strips {w} {part}: {img.get_attribute('alt')[:40]} loaded", ok)
            # is_visible() also counts a painting still waiting to bloom (blurred, or masked to
            # nothing): bring each into the window and wait until it has bloomed in.
            for img in shown:
                img.scroll_into_view_if_needed()
                page.wait_for_timeout(200)
            try:
                page.wait_for_function(
                    "sel => [...document.querySelectorAll(sel)].filter(i => i.offsetParent).every(i => i.dataset.bloom === 'done')",
                    arg=f"#{part} img",
                    timeout=7000,
                )
            except PlaywrightTimeout:
                # The checks below fail for each painting that has not bloomed; say why here.
                waiting = page.evaluate(
                    "sel => [...document.querySelectorAll(sel)].filter(i => i.offsetParent && i.dataset.bloom !== 'done').map(i => `${(i.alt || i.src).slice(0, 30)}: ${i.dataset.bloom}`)",
                    f"#{part} img",
                )
                print(f"NOTE strips {w} {part}: the bloom wait timed out after 7s; still waiting: {'; '.join(waiting)}", flush=True)
            for img in shown:
                state = img.evaluate("i => [i.dataset.bloom, getComputedStyle(i).opacity, getComputedStyle(i).filter]")
                check(f"strips {w} {part}: {img.get_attribute('alt')[:40]} has bloomed in", state == ["done", "1", "none"], str(state))
            if part in ("research", "ask"):
                # Art direction: the phone crop under 960px, the wide painting above.
                src = shown[0].evaluate("i => decodeURIComponent(i.currentSrc)")
                check(f"strips {w} {part}: the {'phone crop' if w == 390 else 'wide painting'} is the picture in use", ("-phone-" in src) == (w == 390), src[-60:])
        scenes = page.locator("#health [data-scene] img")
        wide = page.locator("#health figure[data-picture]")
        if w == 390:
            check("strips 390 health: one scene over each article", scenes.count() == 3 and all(s.is_visible() for s in scenes.all()))
            check("strips 390 health: the wide painting is hidden", wide.count() == 1 and not wide.is_visible())
        else:
            check("strips 1440 health: the wide painting stands over the columns", wide.count() == 1 and wide.is_visible())
            check("strips 1440 health: the phone scenes are hidden", scenes.count() == 3 and not any(s.is_visible() for s in scenes.all()))
        text = page.locator("#research").inner_text()
        for title in ["Mitochondrial nutrients and the aging cell", "Dr. Liu on lipoic acid and the aging brain", "Healthy aging has many moving parts"]:
            check(f"strips {w} research: {title}", title in text)
        metas = [re.sub(r"\s+", " ", m).strip() for m in page.locator("#research ul > li > p:first-child").all_inner_texts()]
        check(f"strips {w} research: each study's line is year · kind · journal", metas == KEY_META, str(metas))
        check(f"strips {w} research: the honesty line", "do not establish the effects of a finished BiGH product" in text)
        rows_before = page.locator("#research details").count()
        page.get_by_role("button", name=re.compile(r"See all 36 sources")).click()
        page.wait_for_timeout(500)
        rows_after = page.locator("#research details").count()
        check(f"strips {w} research: the full list opens (36)", rows_before == 0 and rows_after == 36, f"{rows_before} → {rows_after}")
        page.get_by_role("button", name=re.compile(r"Show fewer sources")).click()
        page.wait_for_timeout(300)
        check(f"strips {w} research: and closes", page.locator("#research details").count() == 0)
        buttons = page.locator("#health button")
        check(f"strips {w} health: three explainers", buttons.count() == 3)
        headings = [tidy(t) for t in page.locator("#health li h3").all_inner_texts()]
        for i in range(3):
            button = buttons.nth(i)
            described = button.evaluate("b => { const e = document.getElementById(b.getAttribute('aria-describedby') || ''); return e ? e.textContent : null; }")
            described = tidy(described or "")
            check(f"strips {w} health: explainer {i + 1} is described by its article title", described == headings[i] and described != "", described)
            button.scroll_into_view_if_needed()
            button.click()
            page.wait_for_timeout(700)
            open_sheets = page.locator("dialog[open]")
            title = open_sheets.locator("h2").first.inner_text() if open_sheets.count() == 1 else ""
            check(f"strips {w} health: explainer {i + 1} opens its own sheet", open_sheets.count() == 1 and title == EXPLAINER_SHEETS[i], title)
            page.keyboard.press("Escape")
            page.wait_for_timeout(400)
            check(f"strips {w} health: explainer {i + 1} closes on Escape", page.locator("dialog[open]").count() == 0)
            check(f"strips {w} health: focus returns to explainer {i + 1}'s button", button.evaluate("b => b === document.activeElement"))
        ask = page.locator("#ask").inner_text()
        for word in ["Ask BiGH Science", "In development", "not accepting submissions"]:
            check(f"strips {w} ask: {word}", word in ask)
        check(f"strips {w} ask: three numbered steps", page.locator("#ask ol > li").count() == 3)
        # (Final review) list-style none drops the list's role in Safari/VoiceOver: role="list".
        steps_role = page.evaluate("document.querySelector('#ask ol').getAttribute('role')")
        steps_tree = page.locator("#ask ol").aria_snapshot()
        check(f"strips {w} ask: the steps are a list to screen readers (role=list)", steps_role == "list" and steps_tree.lstrip().startswith("- list"), f"{steps_role} {steps_tree.strip()[:30]!r}")
        check(f"strips {w}: no console errors", not errors, "; ".join(errors[:3]))
        ctx.close()
    # (Task 6) From 960px the research and health columns share their rows: the titles, the words
    # and the links each start on one line (at 1024px the first study's words ran two lines longer
    # than the second's, and the three "Read the study" links stood at three heights).
    for w, h in [(1440, 900), (1024, 768)]:
        ctx, page, _, _ = opened(browser, w, h)
        for part in ["research", "health"]:
            rows = page.evaluate(COLUMN_ROWS, f"#{part} ul > li")
            for name, tops in rows.items():
                check(f"strips {w} {part}: the {name} start on one line", max(tops) - min(tops) <= 1, str(tops))
        ctx.close()


# The key studies' links, as the catalogs translate "Read the study".
READ_STUDY = {"kr": "연구 보기", "jp": "研究を読む", "cns": "阅读研究", "vn": "Đọc nghiên cứu"}
# How the catalogs already name him (cns.json 刘健康; m198 in jp, kr, vn).
LIU_NAME = {"kr": "Dr. Jiankang Liu", "jp": "Dr. Jiankang Liu", "cns": "刘健康博士", "vn": "Dr. Jiankang Liu"}


def languages(browser):
    for lang, read in READ_STUDY.items():
        ctx, page, response, errors = opened(browser, 1440, 900, path=f"/{lang}/science")
        check(f"languages {lang}: 200", response is not None and response.status == 200)
        # The page already had longer lines holding "Read the study" in some languages ("Read the
        # 2002 study"): the key studies' own links say it, word for word.
        go = [tidy(t) for t in page.locator("#research ul > li a").all_inner_texts()]
        check(f"languages {lang}: each key study's link reads {read}", go == [read] * 3, str(go))
        # The key study's kind is the first " · " part of its translated category (Ruling 9).
        metas = [tidy(m).split(" · ") for m in page.locator("#research ul > li > p:first-child").all_inner_texts()]
        check(f"languages {lang}: each key study's line is year · kind · journal", len(metas) == 3 and all(len(m) == 3 and all(m) for m in metas), str(metas))
        alt = page.locator("#liu img").get_attribute("alt") or ""
        check(f"languages {lang}: his photo's alt names Dr. Liu as the site does", LIU_NAME[lang] in alt, alt[:40])
        overflow = page.evaluate("document.documentElement.scrollWidth - innerWidth")
        check(f"languages {lang}: no sideways scroll", overflow <= 0, str(overflow))
        check(f"languages {lang}: no console errors", not errors, "; ".join(errors[:3]))
        ctx.close()




SIZES = [(1920, 1080), (1536, 864), (1440, 900), (1280, 720), (1024, 768), (900, 1000), (768, 1024), (390, 844), (360, 740)]

SMALL_TEXT = """() => [...document.querySelectorAll('main *')].filter(e => {
  if (!e.childNodes.length || ![...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) return false;
  const s = getComputedStyle(e); const r = e.getBoundingClientRect();
  return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && parseFloat(s.fontSize) < 15;
}).map(e => e.tagName + ' ' + e.textContent.trim().slice(0, 30))"""

SMALL_TARGETS = """() => [...document.querySelectorAll('main a, main button, main summary')].filter(e => {
  const r = e.getBoundingClientRect(); const s = getComputedStyle(e);
  return r.width > 0 && s.visibility !== 'hidden' && (r.height < 44 && !e.closest('p, dd'));
}).map(e => e.tagName + ' ' + e.textContent.trim().slice(0, 30) + ' ' + Math.round(e.getBoundingClientRect().height))"""


def layout(browser):
    for w, h in SIZES:
        ctx, page, _, errors = opened(browser, w, h)
        height = page.evaluate("document.documentElement.scrollHeight")
        for y in range(0, height, h):
            page.evaluate(f"window.scrollTo(0, {y})")
            page.wait_for_timeout(120)
        page.wait_for_timeout(800)
        overflow = page.evaluate("document.documentElement.scrollWidth - innerWidth")
        check(f"layout {w}x{h}: no sideways scroll", overflow <= 0, str(overflow))
        small = page.evaluate(SMALL_TEXT)
        check(f"layout {w}x{h}: text 15px or larger", not small, "; ".join(small[:4]))
        targets = page.evaluate(SMALL_TARGETS)
        check(f"layout {w}x{h}: targets 44px or larger", not targets, "; ".join(targets[:4]))
        check(f"layout {w}x{h}: no console errors", not errors, "; ".join(errors[:3]))
        ctx.close()


# True once scrollY has stayed the same for 300ms (polled; the state lives on window).
SCROLL_SETTLED = """() => {
  const now = performance.now(), y = Math.round(scrollY), s = window.__still || (window.__still = { y, t: now });
  if (s.y !== y) { s.y = y; s.t = now; }
  return now - s.t >= 300;
}"""


def deep_links(browser):
    # globals.css sets scroll-padding-top: 150px, so a correct landing puts the part's top at about
    # 150px, under the menu bar (controller's ruling, October 14); its heading must clear the bar.
    for w, h in [(1440, 900), (390, 844)]:
        for part in ["scientists", "research", "health", "formulas", "ask"]:
            ctx, page, _, _ = opened(browser, w, h, path=f"{PATH}#{part}")
            # The landing as read once the native smooth scroll has finished: scrollY the same for
            # 300ms (a fixed wait once read one phone landing mid-scroll, at top -2).
            page.wait_for_function(SCROLL_SETTLED, polling=100, timeout=8000)
            top = page.evaluate(f"document.getElementById('{part}').getBoundingClientRect().top")
            heading = page.evaluate(f"document.querySelector('#{part} h1, #{part} h2').getBoundingClientRect().top")
            bar = page.evaluate("document.querySelector('header').getBoundingClientRect().bottom")
            check(f"deep_links {w} #{part}: lands at its part", -5 <= top <= 220 or part == "scientists", f"top {top:.0f}")
            check(f"deep_links {w} #{part}: heading clear of the menu bar", heading >= bar - 1, f"{heading:.0f} vs {bar:.0f}")
            ctx.close()


SECTIONS = {"shell": shell, "people": people, "path": path, "settled": settled, "still": still, "multiply": multiply, "strips": strips, "languages": languages, "layout": layout, "deep_links": deep_links}

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = getattr(p, BROWSER).launch()
        print(f"browser: {BROWSER} {browser.version}", flush=True)
        for name, run in SECTIONS.items():
            if ONLY is None or name in ONLY:
                run(browser)
        failed = [r for r in results if not r[1]]
        print(f"\n{len(results) - len(failed)}/{len(results)} passed", flush=True)
        # The count is in before the browser closes: one WebKit run (Windows, October 14) never
        # returned from closing after its last check, so a stuck close ends the run after 60s.
        watchdog = threading.Timer(60, lambda: os._exit(1 if failed else 0))
        watchdog.daemon = True
        watchdog.start()
        browser.close()
    sys.exit(1 if failed else 0)

"""QA for the Science page in Ink & Gold, the handscroll (spec
docs/superpowers/specs/2026-10-14-science-ink-design.md; plan
docs/superpowers/plans/2026-10-14-science-ink.md).

Sections (all, or --only=a,b):
  shell       200 in the ink look, the menu bar marks Science, one h1, the parts' ids in order,
              no canvas, no console errors (1440x900, 390x844); (final review) the shared footer
              promise and the menu's drop-down title in the same face as on About
  people      Dr. Liu's real photo on its mount, his name, numbers and sources, "Read his story"
              opens his sheet; the five bottles with their credits, each linking to its page;
              (Task 6) DESIGN.md's mount shadow, the intro's margin, the bottles, names and credits
              each on one line per row, the sources on one line, the numbers stacked on phones
  journey     (Task 3) the scroll pins, travels from Okayama to Today and lets go, the stop in
              view's words and link in the window, Tab only on shown links; real short windows
              (the title goes on under the bar) and a phone held sideways (the still scroll);
              (Task 6) from 960px the stop in view's inked dot in the window with the line inked to
              it and no other stop's words cut by the misty ends; a lifted box in the middle of the
              window under the bar, its title faded; (final review) the painting loaded, the phone
              picture under 960px, bloomed in from the castle; a travel floor (the painting's
              overflow at least 0.6 of the band's width at 1366x657, 1440x900, 1920x1080); the
              other stops' sentences in the accessibility tree; very wide and short-wide windows
              (3000px wide and more, or 3:1 and wider) get the still scroll
  settled    (Task 3) #liu has the same offsetTop at DOMContentLoaded and after the script ran;
              (Task 4) #research, #health and #ask stand still once their paintings have arrived;
              (Task 6) a cold first visit: the last resort waits while the fonts arrive
  still       (Task 3) reduced motion and no script: nothing pins, every stop readable;
              (Task 4) the strips' paintings whole and crisp (no bloom left waiting);
              (final review) print: the still scroll, no travel room
  multiply    (Task 3, 4) every painting's blend group sits on the page with no stacking context
  strips      (Task 4) research, health and ask: the painting in use (phone crop under 960px) and
              bloomed in, year · kind · journal, the full list, each explainer's own sheet;
              (Task 6) from 960px the columns' titles, words and links each start on one line
  languages   (Task 5) kr, jp, cns, vn: 200, no errors, the new strings translated
  rooms       (Task 5) all five languages, 280 to 1536px wide: the stylesheet's --words-room and
              --stops-room cover what the pinned box needs besides the painting, with 20px to spare
  layout      (Task 6) sizes 1920 to 360: no sideways scroll, text 15px+, targets 44px+
  deep_links  (Task 6) #scientists, #research, #health, #ask land under the menu bar
Pictures: scripts/qa/out/science-ink/ (webkit/ for --browser=webkit).

usage: python -X utf8 scripts/qa/qa_science_ink.py [base-url] [--only=shell,people,...]
       [--browser=chromium|webkit|firefox]  (default chromium; journey and settled are the sections
       meant to run in WebKit too: --browser=webkit --only=journey,settled)
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


# The shared pieces' title face: the footer's promise ("Stay sharp. Live fully.") and the menu
# bar's Science drop-down title (in the page at every width, shown or not).
SHARED_FACES = """() => ['[data-brush="footer-promise"] p', '[data-nav-panel="science"] h2']
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
    # (Task 6) The same real photo sits the same way on every page: DESIGN.md's one mount shadow.
    shadow = photo.evaluate("i => getComputedStyle(i.closest('figure')).boxShadow")
    check("people: the mount's shadow is DESIGN.md's photo mount", shadow == MOUNT_SHADOW, shadow)
    margin = page.evaluate("getComputedStyle(document.querySelector('#liu h2 ~ p ~ p')).marginTop")
    check("people: the intro keeps its 10px under the headline", margin == "10px", margin)
    check("people: no console errors", not errors, "; ".join(errors[:3]))
    ctx.close()
    # (Task 6) Rows that read as rows: the bottles on one ground line, the names and the credits
    # each starting on one line (per row of bottles), Dr. Liu's three "Source" links on one line,
    # and on phones his three numbers one under another (three 89px columns wrapped 5-6 lines).
    for w, h in [(1440, 900), (390, 844)]:
        ctx, page, _, _ = opened(browser, w, h)
        rows = page.evaluate(BOTTLE_ROWS)
        for i, row in enumerate(rows):
            for part, edges in row.items():
                check(f"people {w}: bottle row {i + 1}'s {part} on one line", max(edges) - min(edges) <= 1, str(edges))
        sources = page.evaluate("[...document.querySelectorAll('#liu dl a')].map(a => Math.round(a.getBoundingClientRect().top))")
        if w == 1440:
            check(f"people {w}: the three sources on one line", max(sources) - min(sources) <= 1, str(sources))
        else:
            lefts = page.evaluate("[...document.querySelectorAll('#liu dl > div')].map(d => Math.round(d.getBoundingClientRect().left))")
            check(f"people {w}: the three numbers one under another", len(set(lefts)) == 1 and sources == sorted(sources), f"{lefts} {sources}")
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
  const pinEl = s.querySelector('[data-pin]');
  const band = s.querySelector('[data-band]').getBoundingClientRect();
  const imgEl = s.querySelector('[data-painting]');
  const img = imgEl.getBoundingClientRect();
  const pin = pinEl.getBoundingClientRect();
  const box = e => { if (!e) return null; const r = e.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom]; };
  const cur = s.querySelector(`li[data-stop="${s.dataset.now}"]`);
  const shown = e => { for (; e && e !== s; e = e.parentElement) if (Number(getComputedStyle(e).opacity) < 1) return false; return true; };
  // Links Tab can reach: each must be shown and inside the window.
  const reachable = [...s.querySelectorAll('li[data-stop] a')].filter(a => a.tabIndex >= 0)
    .map(a => { const r = a.getBoundingClientRect(); return shown(a) && r.left >= -1 && r.right <= innerWidth + 1 && r.top >= -1 && r.bottom <= innerHeight + 1; });
  const still = s.hasAttribute('data-still') || getComputedStyle(pinEl).position === 'static';
  // (Task 6) The stop in view's dot (over its words) and the inked line's end; the other stops
  // whose words stand in the track's misty ends without being faded (data-out).
  const dot = cur && cur.querySelector('i'); const d = dot && dot.getBoundingClientRect();
  const ink = s.querySelector('div[aria-hidden="true"] > span'); const k = ink && ink.getBoundingClientRect();
  const words = li => [...li.querySelectorAll('span')].map(e => { const r = document.createRange(); r.selectNodeContents(e); return r.getBoundingClientRect(); });
  const misty = [...s.querySelectorAll('li[data-stop]')].filter(li => li !== cur && !li.hasAttribute('data-out'))
    .filter(li => words(li).some(b => b.left < band.left + band.width * 0.06 - 1 || b.right > band.right - band.width * 0.06 + 1))
    .map(li => li.dataset.stop);
  const hidden = [...s.querySelectorAll('li[data-stop][data-out]')]
    .filter(li => words(li).every(b => b.left > band.left + band.width * 0.06 + 1 && b.right < band.right - band.width * 0.06 - 1))
    .map(li => li.dataset.stop);
  const cs = getComputedStyle(s);
  return { now: Number(s.dataset.now), still, pinTop: pin.top, pinBottom: pin.bottom, bandTop: band.top,
           mode: cs.getPropertyValue('--mode').trim(), barFoot: document.querySelector('header').getBoundingClientRect().bottom,
           wordsOpacity: Number(getComputedStyle(pinEl.firstElementChild).opacity),
           dotX: d ? (d.left + d.right) / 2 : null, inkEnd: k ? k.right : null, misty, hidden,
           stick: parseFloat(getComputedStyle(pinEl).top), padTop: parseFloat(getComputedStyle(s).paddingTop),
           room: s.querySelector('[data-room]').offsetHeight, overflow: img.width - band.width,
           imgLeft: img.left, imgRight: img.right, bandLeft: band.left, bandRight: band.right,
           text: box(cur && cur.querySelector('p')), textShown: shown(cur && cur.querySelector('p')),
           link: box(cur && cur.querySelector('a')), reachable,
           innerHeight, innerWidth, scrollY, sectionBottom: s.getBoundingClientRect().bottom };
}"""
# A few words of each stop's sentence (science-content.ts pathStops, English).
STOP_SENTENCES = ["Okayama University in Japan", "Bruce Ames’s laboratory", "Published in PNAS", "European Academy of Sciences and Arts", "guides the science behind our formulas"]


# The stops whose dot shows inside the band while their words do not (opacity as rendered).
LONE_DOTS = """() => {
  const s = document.querySelector('#scientists'); const band = s.querySelector('[data-band]').getBoundingClientRect();
  const shown = e => { for (; e && e !== s; e = e.parentElement) if (Number(getComputedStyle(e).opacity) < 0.5) return false; return true; };
  return [...s.querySelectorAll('li[data-stop]')].filter(li => {
    const d = li.querySelector('i').getBoundingClientRect(); const x = (d.left + d.right) / 2;
    return x > band.left && x < band.right && shown(li.querySelector('i')) && !shown(li.querySelector('span'));
  }).map(li => li.dataset.stop);
}"""
# The last stop's link (it always has one): its underline, its arrow, its size.
STOP_LINK = """(() => { const a = document.querySelector('#scientists li[data-stop] a'); const s = getComputedStyle(a);
  return [s.textDecorationLine, !!a.querySelector('svg'), s.fontSize]; })()"""


def inside(rect, w, h):
    return rect is None or (rect[0] >= -1 and rect[2] <= w + 1 and rect[1] >= -1 and rect[3] <= h + 1)


JOURNEY_SIZES = [
    (1440, 900, "en"), (1280, 720, "en"), (1280, 720, "vn"), (390, 844, "en"),
    # Real windows (October 14 review): a laptop with its browser bars, iPhone Safari with its
    # toolbars, a small phone, and a phone held sideways (the still scroll).
    (1366, 657, "en"), (390, 664, "en"), (375, 667, "en"), (844, 390, "en"),
    # (Task 5) a small old phone: under 360px wide the lifted box needs up to 586px (Vietnamese).
    (320, 568, "en"),
    # (Final review, Ruling 21) Common large screens still travel; very wide windows (the painting,
    # 3802px at its largest, barely wider than the band or narrower: 362px of travel at 3440, none
    # at 3840) and short-wide ones (the painting narrower than the band at 1920x580-613,
    # 2560x580-686 and, with the title kept, 2560x821-841) get the still scroll.
    (1920, 1080, "en"), (2560, 1440, "en"),
    (3840, 2160, "en"), (3440, 1440, "en"), (3000, 1300, "en"), (1920, 580, "en"), (1920, 613, "en"),
    (2560, 580, "en"), (2560, 686, "en"), (2560, 830, "en"),
]
STILL_SIZES = {(844, 390), (320, 568), (3840, 2160), (3440, 1440), (3000, 1300), (1920, 580), (1920, 613), (2560, 580), (2560, 686), (2560, 830)}
# (Final review, Ruling 19) The travel is accepted at its length (about 1.9 window heights at
# 1440x900); this floor keeps a future crop or room change from making it barely move.
TRAVEL_FLOOR = {(1366, 657), (1440, 900), (1920, 1080)}
TRAVEL_SHARE = 0.6
# (Final review) The scroll painting itself, and the stops' words in the accessibility tree.
PAINTING_SIZES = {(1440, 900), (390, 844)}
PAINTING = """() => { const i = document.querySelector('#scientists [data-painting]');
  // The bloom's mask position as the cascade sets it while a painting waits (read with the mark
  // set for a moment: once bloomed the painting has no mask), the painting's width, the castle's
  // place on it (the first stop's --at).
  const was = i.dataset.bloom; i.dataset.bloom = 'waiting';
  const s = getComputedStyle(i); const mask = s.maskPosition || s.webkitMaskPosition; i.dataset.bloom = was;
  return { natural: i.naturalWidth, src: decodeURIComponent(i.currentSrc), bloom: i.dataset.bloom, mask,
           width: i.getBoundingClientRect().width,
           castle: parseFloat(document.querySelector('#scientists li[data-stop="0"]').style.getPropertyValue('--at')) }; }"""


def blot_middles(mask, width, sizes=(0.5, 1.0, 2.0)):
    """Where the bloom's blot has its middle (px from the painting's left) at a few of its sizes
    (a share of the painting's width): the first layer's x position, `p% + q px`, places the blot's
    left edge at p% of (width - blot) + q."""
    x = mask.split(",")[0].strip()
    x = x[5:x.index(")")] if x.startswith("calc(") else x.split(" ")[0]
    pct = px = 0.0
    for sign, value, unit in re.findall(r"([+-]?)\s*(\d+(?:\.\d+)?)(%|px)", x):
        v = -float(value) if sign == "-" else float(value)
        if unit == "%":
            pct += v
        else:
            px += v
    return [pct / 100 * (width - s * width) + px + s * width / 2 for s in sizes]
# Each stop not in view: its sentence and every box around it up to the section neither
# display: none nor visibility other than visible (Ruling 3: only transparent).
OTHERS_IN_TREE = """() => { const s = document.querySelector('#scientists');
  return [...s.querySelectorAll('li[data-stop]')].filter(li => li.dataset.stop !== s.dataset.now).map(li => {
    const bad = []; for (let e = li.querySelector('p'); e && e !== s; e = e.parentElement) {
      const c = getComputedStyle(e); if (c.display === 'none' || c.visibility !== 'visible') bad.push(e.tagName + ' ' + c.display + ' ' + c.visibility); }
    return li.dataset.stop + (bad.length ? ': ' + bad.join(', ') : ''); }); }"""


def journey(browser):
    for w, h, lang in JOURNEY_SIZES:
        tag = f"journey {w}x{h} {lang}"
        ctx, page, _, errors = opened(browser, w, h, path=f"/{lang}/science")
        page.wait_for_timeout(1200)
        start = page.evaluate(STATE)
        check(f"{tag}: starts at Okayama", start["now"] == 0, str(start["now"]))
        if (w, h) in STILL_SIZES:
            # Too short for the pinned box even with the title gone and the painting at its least.
            check(f"{tag}: the still scroll", start["still"])
            pin = page.evaluate("getComputedStyle(document.querySelector('[data-pin]')).position")
            check(f"{tag}: nothing pins", pin == "static", pin)
            check(f"{tag}: no travel room", start["room"] == 0, str(start["room"]))
            visible = page.evaluate("[...document.querySelectorAll('#scientists li[data-stop] p')].map(p => getComputedStyle(p).opacity === '1' && p.getBoundingClientRect().height > 0)")
            check(f"{tag}: all five stops readable", visible == [True] * 5, str(visible))
            band = page.evaluate("(() => { const b = document.querySelector('[data-band]'); return [getComputedStyle(b).overflowX, b.getAttribute('role'), b.tabIndex]; })()")
            check(f"{tag}: the band scrolls sideways, a region the keyboard reaches", band == ["auto", "region", 0], str(band))
            check(f"{tag}: every link reachable", page.evaluate("[...document.querySelectorAll('#scientists li a')].every(a => a.tabIndex >= 0)"))
            page.screenshot(path=str(OUT / f"journey-{w}x{h}-{lang}-still.png"))
            check(f"{tag}: no console errors", not errors, "; ".join(errors[:3]))
            ctx.close()
            continue
        check(f"{tag}: travels (not the still scroll)", not start["still"])
        check(f"{tag}: room to travel", start["overflow"] > 0 and start["room"] >= start["overflow"] - 1, f"overflow {start['overflow']:.0f}, room {start['room']}")
        band_w = start["bandRight"] - start["bandLeft"]
        if (w, h) in TRAVEL_FLOOR and lang == "en":
            check(f"{tag}: travel floor, the painting's overflow at least {TRAVEL_SHARE} of the band's width", start["overflow"] >= TRAVEL_SHARE * band_w, f"overflow {start['overflow']:.0f} = {start['overflow'] / band_w:.2f} x band {band_w:.0f}")
        if (w, h) in PAINTING_SIZES and lang == "en":
            # The painting arrived, the phone picture under 960px (the wide one from 960px), and it
            # blooms in from the castle (about 9% across), not from its middle off-screen.
            try:
                page.wait_for_function("() => document.querySelector('#scientists [data-painting]').dataset.bloom === 'done'", timeout=9000)
            except PlaywrightTimeout:
                pass
            art = page.evaluate(PAINTING)
            check(f"{tag}: the scroll painting loaded", art["natural"] > 0, str(art["natural"]))
            check(f"{tag}: the {'phone' if w < 960 else 'wide'} scroll picture in use", ("scroll-phone" in art["src"]) == (w < 960), art["src"][-48:])
            check(f"{tag}: the scroll painting has bloomed in", art["bloom"] == "done", str(art["bloom"]))
            # The blot's middle stays on the castle as it grows (within 2% of the painting's width).
            middles = blot_middles(art["mask"], art["width"])
            castle = art["castle"] * art["width"]
            check(f"{tag}: the scroll painting blooms from the castle", all(abs(m - castle) <= 0.02 * art["width"] for m in middles), f"blot middle {[round(m) for m in middles]} vs castle {castle:.0f} ({art['mask']})")
        # The box sticks once it has risen to its sticky top (higher than the menu bar's foot when
        # the title goes on under the bar); the travel runs over the room from there.
        begin = max(0, start["padTop"] - start["stick"])
        room = start["room"]
        seen = []
        for step in range(0, 11):
            page.evaluate(f"window.scrollTo(0, {begin + room * step / 10})")
            page.wait_for_timeout(250)
            st = page.evaluate(STATE)
            seen.append(st["now"])
            if 0 < step < 10:
                check(f"{tag} {step}/10: pinned", abs(st["pinTop"] - st["stick"]) < 2, f"{st['pinTop']:.0f} vs {st['stick']:.0f}")
                check(f"{tag} {step}/10: the pinned box fits the window", st["pinBottom"] <= h + 1, f"{st['pinBottom']:.0f} > {h}")
                check(f"{tag} {step}/10: painting covers the band", st["imgLeft"] <= st["bandLeft"] + 1 and st["imgRight"] >= st["bandRight"] - 1)
                check(f"{tag} {step}/10: the stop's sentence and link shown, in the window", st["textShown"] and inside(st["text"], w, h) and inside(st["link"], w, h), f"{st['text']} {st['link']}")
                check(f"{tag} {step}/10: Tab reaches only shown links", all(st["reachable"]) and len(st["reachable"]) <= 1, str(st["reachable"]))
                if step == 5 and (w, h) in PAINTING_SIZES and lang == "en":
                    # (Final review) Ruling 3's guarantee, checked: the stops not in view are only
                    # transparent, so the accessibility tree keeps all five sentences, in a list
                    # (role="list": list-style none drops the list in Safari/VoiceOver).
                    others = page.evaluate(OTHERS_IN_TREE)
                    check(f"{tag} {step}/10: the other stops' sentences visible to the accessibility tree", len(others) == 4 and all(":" not in o for o in others), str(others))
                    tree = page.locator("#scientists ol").aria_snapshot()
                    missing = [t for t in STOP_SENTENCES if t not in tree]
                    check(f"{tag} {step}/10: the accessibility tree has the stops' list and all five sentences", tree.lstrip().startswith("- list") and not missing, f"{tree.strip()[:40]!r}, missing {missing}")
                    role = page.evaluate("document.querySelector('#scientists ol').getAttribute('role')")
                    check(f"{tag} {step}/10: the stops' list says role=list", role == "list", str(role))
                if step == 5 and st["mode"] == "lift":
                    # (Task 6) A lifted box stands in the middle of what the menu bar leaves (a
                    # tall phone left about 220px of blank paper under the words), and its title,
                    # stopped short of the bar, has faded.
                    above, below = st["bandTop"] - st["barFoot"], h - st["pinBottom"]
                    check(f"{tag} {step}/10: the lifted box in the middle of the window", below - above <= 60, f"paper above the painting {above:.0f}, under the words {below:.0f}")
                    check(f"{tag} {step}/10: the lifted title has faded", st["wordsOpacity"] == 0, str(st["wordsOpacity"]))
                if w >= 960:
                    # (Task 6) The stop in view always shows its inked dot, the line inked up to
                    # it; no other stop's words are cut by the misty ends.
                    dot_ok = st["dotX"] is not None and st["bandLeft"] <= st["dotX"] <= st["bandRight"]
                    check(f"{tag} {step}/10: the stop in view's dot in the window, the line inked to it", dot_ok and abs(st["inkEnd"] - st["dotX"]) < 3, f"dot {st['dotX']}, ink {st['inkEnd']}")
                    check(f"{tag} {step}/10: no other stop's words in the misty ends", not st["misty"], str(st["misty"]))
                    check(f"{tag} {step}/10: every stop's words in the clear shown", not st["hidden"], str(st["hidden"]))
        check(f"{tag}: stops in order, Okayama to Today", seen == sorted(seen) and seen[0] == 0 and seen[-1] == 4, str(seen))
        end = page.evaluate(STATE)
        check(f"{tag}: the painting's end in view at the end", abs(end["imgRight"] - end["bandRight"]) < 3, f"{end['imgRight']:.0f} vs {end['bandRight']:.0f}")
        if w >= 960:
            check(f"{tag}: at the end, no other stop's words in the misty ends", not end["misty"], str(end["misty"]))
            # (Task 6 fix round 1, Ruling 15) No lone dot: a dot shown in the window always has its
            # words (a stop fading in the misty ends fades its dot with them), once the fade has run.
            for f in (0.25, 0.5, 1.0):
                page.evaluate(f"window.scrollTo(0, {begin + room * f})")
                page.wait_for_timeout(900)
                lone = page.evaluate(LONE_DOTS)
                check(f"{tag} at {f:.2f}: no dot shown without its words", not lone, str(lone))
            if (w, lang) == (1440, "en"):
                look = page.evaluate(STOP_LINK)
                check(f"{tag}: the stop's link has the page's link style (underline, arrow, 15px)", look == ["underline", True, "15px"], str(look))
        page.evaluate(f"window.scrollTo(0, {begin + room + 400})")
        page.wait_for_timeout(300)
        after = page.evaluate(STATE)
        check(f"{tag}: lets go after Today", after["pinTop"] < after["stick"] - 100, f"{after['pinTop']:.0f}")
        page.evaluate(f"window.scrollTo(0, {begin + room * 0.5})")
        page.wait_for_timeout(300)
        page.screenshot(path=str(OUT / f"journey-{w}x{h}-{lang}-half.png"))
        if w == 1440:
            page.set_viewport_size({"width": 1024, "height": 768})
            page.wait_for_timeout(600)
            st = page.evaluate(STATE)
            check("journey resize 1440→1024 half way: painting still covers the band", st["imgLeft"] <= st["bandLeft"] + 1 and st["imgRight"] >= st["bandRight"] - 1)
        check(f"{tag}: no console errors", not errors, "; ".join(errors[:3]))
        ctx.close()


# Where the travel starts and how long its room is (as shoot_science_ink.py).
TRAVEL = """() => {
  const s = document.querySelector('#scientists'); const pin = s.querySelector('[data-pin]');
  const pad = parseFloat(getComputedStyle(s).paddingTop); const stick = parseFloat(getComputedStyle(pin).top);
  return [Math.max(0, pad - stick), s.querySelector('[data-room]').offsetHeight];
}"""
# The handscroll as printed: each part's opacity is its own times its boxes' up to the page.
PRINTED = """() => { const s = document.querySelector('#scientists'); const pin = s.querySelector('[data-pin]');
  const op = e => { let o = 1; for (; e && e !== document.body; e = e.parentElement) o *= Number(getComputedStyle(e).opacity); return o; };
  return { room: s.querySelector('[data-room]').offsetHeight, pin: getComputedStyle(pin).position,
           transform: getComputedStyle(s.querySelector('[data-painting]')).transform, title: op(pin.firstElementChild),
           stops: [...s.querySelectorAll('li[data-stop] p')].map(p => op(p) === 1 && p.getBoundingClientRect().height > 0) }; }"""


def still(browser):
    for label, kwargs in [("reduced motion", {"reduced": True}), ("no script", {"js": False})]:
        for w, h in [(1440, 900), (390, 844)]:
            ctx, page, _, _ = opened(browser, w, h, **kwargs)
            page.wait_for_timeout(800)
            pin = page.evaluate("getComputedStyle(document.querySelector('[data-pin]')).position")
            check(f"still {label} {w}: nothing pins", pin == "static", pin)
            room = page.evaluate("document.querySelector('#scientists [data-room]').offsetHeight")
            check(f"still {label} {w}: no travel room", room == 0, str(room))
            visible = page.evaluate("[...document.querySelectorAll('#scientists li[data-stop] p')].map(p => getComputedStyle(p).visibility === 'visible' && getComputedStyle(p).display !== 'none' && getComputedStyle(p).opacity === '1' && getComputedStyle(p.closest('li')).opacity === '1' && p.getBoundingClientRect().height > 0)")
            check(f"still {label} {w}: all five stops readable", visible == [True] * 5, str(visible))
            check(f"still {label} {w}: every link reachable", page.evaluate("[...document.querySelectorAll('#scientists li a')].every(a => a.tabIndex >= 0)"))
            band = page.evaluate("getComputedStyle(document.querySelector('[data-band]')).overflowX")
            check(f"still {label} {w}: the band scrolls sideways", band == "auto", band)
            if label == "reduced motion":
                role = page.evaluate("document.querySelector('[data-band]').getAttribute('role')")
                check(f"still {label} {w}: the band is a named region", role == "region", str(role))
            shown = page.evaluate("(() => { const s = getComputedStyle(document.querySelector('[data-painting]')); return [s.filter, s.maskImage]; })()")
            check(f"still {label} {w}: the painting crisp and whole", shown == ["none", "none"], str(shown))
            # The strips' paintings (the server marks them "waiting"): shown whole and crisp, a wide
            # one with only its own soft ends (no bloom blot), a phone scene with no mask at all.
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
    # (Final review) Printed: the still scroll once, not the travel's room (about two pages of
    # blank paper), even when the visitor prints from the middle of the travel (the painting moved,
    # a lifted title faded).
    for w, h in [(1440, 900), (390, 844)]:
        ctx, page, _, _ = opened(browser, w, h)
        page.wait_for_timeout(800)
        begin, room = page.evaluate(TRAVEL)
        page.evaluate(f"window.scrollTo(0, {begin + room * 0.5})")
        page.wait_for_timeout(400)
        page.emulate_media(media="print")
        page.wait_for_timeout(1000)
        d = page.evaluate(PRINTED)
        check(f"still print {w}: no travel room", d["room"] == 0, str(d["room"]))
        check(f"still print {w}: nothing pins", d["pin"] == "static", d["pin"])
        check(f"still print {w}: the painting from its start (not moved)", d["transform"] == "none", d["transform"])
        check(f"still print {w}: the title shown", d["title"] == 1, str(d["title"]))
        check(f"still print {w}: all five stops readable", d["stops"] == [True] * 5, str(d["stops"]))
        page.screenshot(path=str(OUT / f"still-print-{w}.png"))
        ctx.close()


# useJourney's LAST_RESORT (use-journey.ts): the first words of the warning its last resort logs.
LAST_RESORT = "[science-journey:last-resort]"
PART_TOPS = "['research', 'health', 'ask'].map(id => Math.round(document.getElementById(id).getBoundingClientRect().top + scrollY))"
SETTLED_SIZES = [
    (1440, 900, "en"), (1440, 900, "vn"), (1366, 657, "en"), (1280, 720, "en"), (1280, 720, "vn"),
    (390, 664, "en"), (375, 667, "en"), (390, 844, "en"), (390, 844, "vn"),
    # (Task 5) the translated pages, a large phone, and the narrow-phone rooms (under 360px the hint
    # takes two lines in Vietnamese; at 360px the Japanese hint is near its wrap).
    (1440, 900, "kr"), (1440, 900, "jp"), (1440, 900, "cns"),
    (390, 664, "kr"), (390, 664, "jp"), (390, 664, "cns"),
    (430, 932, "en"), (360, 640, "jp"), (320, 640, "vn"),
]


# A style that makes the pinned box's title 100px taller (from the parsed page on), and a record of
# the fonts' status each time the last resort warns.
FORCED_SHORTFALL = """
window.__lastResort = [];
const warn = console.warn;
console.warn = function (...a) {
  if (String(a[0]).startsWith('[science-journey:last-resort]')) window.__lastResort.push(document.fonts.status);
  return warn.apply(this, a);
};
const style = document.createElement('style');
style.textContent = '#scientists [data-pin] > :first-child { padding-bottom: 100px !important; }';
// In the head once it is parsed (a style put straight on <html> is gone after hydration).
document.addEventListener('DOMContentLoaded', () => document.head.appendChild(style));
"""
COLD_SIZES = [(1440, 900, "kr"), (1440, 900, "vn"), (1280, 720, "kr"), (1536, 864, "jp"), (390, 664, "kr"), (390, 844, "vn")]


def settled(browser):
    # The stylesheet alone sets the painting's height (and the page's): nothing below the journey
    # moves once the script has run (review, October 14: the menu's #research, #health and #ask
    # links must land under the menu bar).
    for w, h, lang in SETTLED_SIZES:
        ctx = browser.new_context(viewport={"width": w, "height": h})
        page = ctx.new_page()
        warnings = []
        page.on("console", lambda m: m.type == "warning" and LAST_RESORT in m.text and warnings.append(m.text))
        # A first visit warms the cache, so the fonts are there when the page is read before its
        # script runs (on a cold first visit the lead can re-wrap when Switzer arrives: the fonts'
        # doing, not the script's).
        page.goto(BASE + f"/{lang}/science", wait_until="networkidle")
        read = "[document.querySelector('#liu').offsetTop, document.querySelector('#scientists [data-room]').offsetHeight, document.querySelector('#scientists').style.getPropertyValue('--band-h'), document.querySelector('#scientists').hasAttribute('data-still')]"
        page.goto(BASE + f"/{lang}/science", wait_until="domcontentloaded")
        first = page.evaluate(read)
        first_parts = page.evaluate(PART_TOPS)
        page.wait_for_timeout(1500)
        later = page.evaluate(read)
        check(f"settled {w}x{h} {lang}: #liu stays put after load", abs(later[0] - first[0]) <= 2, f"{first[0]} -> {later[0]}")
        check(f"settled {w}x{h} {lang}: the travel room stays put", later[1] == first[1], f"{first[1]} -> {later[1]}")
        check(f"settled {w}x{h} {lang}: the script sets no painting height", later[2] == "", repr(later[2]))
        check(f"settled {w}x{h} {lang}: the script does not fall back to the still scroll", not later[3])
        check(f"settled {w}x{h} {lang}: the last resort stays quiet (no console warning)", not warnings, "; ".join(warnings[:1]))
        # The strips' paintings are lazy and the phone's has another ratio than the wide one: the
        # stylesheet reserves each one's box (strip.module.css), so once every painting has arrived
        # the three parts stand where they stood before (the menu's links land by them).
        page.evaluate(f"document.querySelectorAll('{STRIP_PICTURES}').forEach(i => {{ i.loading = 'eager'; }})")
        page.wait_for_function(
            "sel => [...document.querySelectorAll(sel)].filter(i => i.offsetParent).every(i => i.complete && i.naturalWidth > 0)",
            arg=STRIP_PICTURES,
            timeout=15000,
        )
        page.wait_for_timeout(300)
        arrived = page.evaluate(PART_TOPS)
        for name, before, after in zip(["#research", "#health", "#ask"], first_parts, arrived):
            check(f"settled {w}x{h} {lang}: {name} stays put once its paintings have arrived", abs(after - before) <= 2, f"{before} -> {after}")
        ctx.close()
    # (Task 6) A cold first visit, the fonts not yet in: the last resort waits for them (on the
    # built site the Korean lead took two lines in the fallback face until Switzer arrived, and the
    # last resort shrank the painting by 3.6px at 1440x900 on every cold visit, moving the anchors).
    for w, h, lang in COLD_SIZES:
        ctx = browser.new_context(viewport={"width": w, "height": h})
        page = ctx.new_page()
        warnings = []
        page.on("console", lambda m: m.type == "warning" and LAST_RESORT in m.text and warnings.append(m.text))
        page.goto(BASE + f"/{lang}/science", wait_until="domcontentloaded")
        page.wait_for_timeout(2500)
        check(f"settled cold {w}x{h} {lang}: the last resort stays quiet while the fonts arrive", not warnings, "; ".join(warnings[:1])[:160])
        ctx.close()
    # (Task 6 fix round 1) The wait must not become "never judges": a genuine shortfall (the title
    # made 100px taller by an injected style) still shrinks the painting
    # once the fonts are in, and says so then, never while they load. The cold case bites only on
    # the built site (next start): dev serves the fonts so that they are in before the first measure.
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.add_init_script(FORCED_SHORTFALL)
    page.goto(BASE + "/kr/science", wait_until="domcontentloaded")
    page.wait_for_timeout(3000)
    told, band_h = page.evaluate("[window.__lastResort, document.querySelector('#scientists').style.getPropertyValue('--band-h')]")
    check("settled forced shortfall 1440x900 kr: the last resort still acts once the fonts are in", told and all(t == "loaded" for t in told) and band_h.endswith("px"), f"warned with fonts {told}, --band-h {band_h!r}")
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


NEW_STRINGS = {
    "kr": ["계속 스크롤하세요", "연구 보기"],
    "jp": ["スクロールを続けると", "研究を読む"],
    "cns": ["继续向下滚动", "阅读研究"],
    "vn": ["Tiếp tục cuộn", "Đọc nghiên cứu"],
}
# How the catalogs already name him (cns.json 刘健康; m198 in jp, kr, vn).
LIU_NAME = {"kr": "Dr. Jiankang Liu", "jp": "Dr. Jiankang Liu", "cns": "刘健康博士", "vn": "Dr. Jiankang Liu"}


def languages(browser):
    for lang, words in NEW_STRINGS.items():
        ctx, page, response, errors = opened(browser, 1440, 900, path=f"/{lang}/science")
        check(f"languages {lang}: 200", response is not None and response.status == 200)
        text = page.locator("main").inner_text()
        for word in words:
            check(f"languages {lang}: {word}", word in text)
        # The page already had longer lines holding "Read the study" in some languages ("Read the
        # 2002 study"): the key studies' own links say it, word for word.
        go = [tidy(t) for t in page.locator("#research ul > li a").all_inner_texts()]
        check(f"languages {lang}: each key study's link reads {words[1]}", go == [words[1]] * 3, str(go))
        # The key study's kind is the first " · " part of its translated category (Ruling 9).
        metas = [tidy(m).split(" · ") for m in page.locator("#research ul > li > p:first-child").all_inner_texts()]
        check(f"languages {lang}: each key study's line is year · kind · journal", len(metas) == 3 and all(len(m) == 3 and all(m) for m in metas), str(metas))
        alt = page.locator("[data-painting]").get_attribute("alt") or ""
        check(f"languages {lang}: the scroll's alt names Dr. Liu as the site does", LIU_NAME[lang] in alt, alt[:40])
        overflow = page.evaluate("document.documentElement.scrollWidth - innerWidth")
        check(f"languages {lang}: no sideways scroll", overflow <= 0, str(overflow))
        check(f"languages {lang}: no console errors", not errors, "; ".join(errors[:3]))
        ctx.close()


# What the pinned box needs besides the painting (useJourney's last resort fires past it): the
# title, the foot, the stops, the grid's gaps and useJourney's own 12px. Pin mode keeps the title in
# the box (--words-room, from 960px); lift mode sends it under the menu bar (--stops-room).
ROOM_NEEDS = """async () => {
  await document.fonts.ready;
  const s = document.querySelector('#scientists'); const pin = s.querySelector('[data-pin]');
  const [words, , foot, track] = [...pin.children].map(c => c.getBoundingClientRect().height);
  const gap = parseFloat(getComputedStyle(pin).rowGap); const cs = getComputedStyle(s);
  return { pin: words + foot + track + 3 * gap + 12, lift: foot + track + 2 * gap + 12,
           wordsRoom: parseFloat(cs.getPropertyValue('--words-room')), stopsRoom: parseFloat(cs.getPropertyValue('--stops-room')) };
}"""
ROOM_WIDTHS = [280, 320, 360, 390, 768, 960, 1280, 1536]
ROOM_SPARE = 20


def rooms(browser):
    # The rooms are measured with about one line to spare (journey.module.css); a string that grows
    # eats into it, and this fails before the last resort ever moves the anchors.
    for lang in ["en", "vn", "kr", "jp", "cns"]:
        for w in ROOM_WIDTHS:
            ctx, page, _, _ = opened(browser, w, 1400, path=f"/{lang}/science")
            d = page.evaluate(ROOM_NEEDS)
            check(f"rooms {lang} {w}: --stops-room {d['stopsRoom']:.0f} covers the lifted box", d["stopsRoom"] - d["lift"] >= ROOM_SPARE, f"needs {d['lift']:.1f}, spare {d['stopsRoom'] - d['lift']:.1f}")
            if w >= 960:
                check(f"rooms {lang} {w}: --words-room {d['wordsRoom']:.0f} covers the pinned box", d["wordsRoom"] - d["pin"] >= ROOM_SPARE, f"needs {d['pin']:.1f}, spare {d['wordsRoom'] - d['pin']:.1f}")
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
        for part in ["scientists", "research", "health", "ask"]:
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


SECTIONS = {"shell": shell, "people": people, "strips": strips, "journey": journey, "settled": settled, "still": still, "multiply": multiply, "languages": languages, "rooms": rooms, "layout": layout, "deep_links": deep_links}

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

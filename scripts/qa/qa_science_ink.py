"""QA for the Science page in Ink & Gold, the handscroll (spec
docs/superpowers/specs/2026-10-14-science-ink-design.md; plan
docs/superpowers/plans/2026-10-14-science-ink.md).

Sections (all, or --only=a,b):
  shell       200 in the ink look, the menu bar marks Science, one h1, the parts' ids in order,
              no canvas, no console errors (1440x900, 390x844)
  people      Dr. Liu's real photo on its mount, his name, numbers and sources, "Read his story"
              opens his sheet; the five bottles with their credits, each linking to its page
  journey     (Task 3) the scroll pins, travels from Okayama to Today and lets go, the stop in
              view's words and link in the window, Tab only on shown links; real short windows
              (the title goes on under the bar) and a phone held sideways (the still scroll)
  settled     (Task 3) #liu has the same offsetTop at DOMContentLoaded and after the script ran;
              (Task 4) #research, #health and #ask stand still once their paintings have arrived
  still       (Task 3) reduced motion and no script: nothing pins, every stop readable;
              (Task 4) the strips' paintings whole and crisp (no bloom left waiting)
  multiply    (Task 3, 4) every painting's blend group sits on the page with no stacking context
  strips      (Task 4) research, health and ask: the painting in use (phone crop under 960px) and
              bloomed in, year · kind · journal, the full list, each explainer's own sheet
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
  return { now: Number(s.dataset.now), still, pinTop: pin.top, pinBottom: pin.bottom,
           stick: parseFloat(getComputedStyle(pinEl).top), padTop: parseFloat(getComputedStyle(s).paddingTop),
           room: s.querySelector('[data-room]').offsetHeight, overflow: img.width - band.width,
           imgLeft: img.left, imgRight: img.right, bandLeft: band.left, bandRight: band.right,
           text: box(cur && cur.querySelector('p')), textShown: shown(cur && cur.querySelector('p')),
           link: box(cur && cur.querySelector('a')), reachable,
           innerHeight, innerWidth, scrollY, sectionBottom: s.getBoundingClientRect().bottom };
}"""


def inside(rect, w, h):
    return rect is None or (rect[0] >= -1 and rect[2] <= w + 1 and rect[1] >= -1 and rect[3] <= h + 1)


JOURNEY_SIZES = [
    (1440, 900, "en"), (1280, 720, "en"), (1280, 720, "vn"), (390, 844, "en"),
    # Real windows (October 14 review): a laptop with its browser bars, iPhone Safari with its
    # toolbars, a small phone, and a phone held sideways (the still scroll).
    (1366, 657, "en"), (390, 664, "en"), (375, 667, "en"), (844, 390, "en"),
]


def journey(browser):
    for w, h, lang in JOURNEY_SIZES:
        tag = f"journey {w}x{h} {lang}"
        ctx, page, _, errors = opened(browser, w, h, path=f"/{lang}/science")
        page.wait_for_timeout(1200)
        start = page.evaluate(STATE)
        check(f"{tag}: starts at Okayama", start["now"] == 0, str(start["now"]))
        if (w, h) == (844, 390):
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
        check(f"{tag}: stops in order, Okayama to Today", seen == sorted(seen) and seen[0] == 0 and seen[-1] == 4, str(seen))
        end = page.evaluate(STATE)
        check(f"{tag}: the painting's end in view at the end", abs(end["imgRight"] - end["bandRight"]) < 3, f"{end['imgRight']:.0f} vs {end['bandRight']:.0f}")
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


PART_TOPS = "['research', 'health', 'ask'].map(id => Math.round(document.getElementById(id).getBoundingClientRect().top + scrollY))"
SETTLED_SIZES = [
    (1440, 900, "en"), (1440, 900, "vn"), (1366, 657, "en"), (1280, 720, "en"), (1280, 720, "vn"),
    (390, 664, "en"), (375, 667, "en"), (390, 844, "en"), (390, 844, "vn"),
]


def settled(browser):
    # The stylesheet alone sets the painting's height (and the page's): nothing below the journey
    # moves once the script has run (review, October 14: the menu's #research, #health and #ask
    # links must land under the menu bar).
    for w, h, lang in SETTLED_SIZES:
        ctx = browser.new_context(viewport={"width": w, "height": h})
        page = ctx.new_page()
        # A first visit warms the cache, so the fonts are there when the page is read before its
        # script runs (on a cold first visit the lead can re-wrap when Switzer arrives: the fonts'
        # doing, not the script's).
        page.goto(BASE + f"/{lang}/science", wait_until="networkidle")
        read = "[document.querySelector('#liu').offsetTop, document.querySelector('#scientists [data-room]').offsetHeight, document.querySelector('#scientists').style.getPropertyValue('--band-h')]"
        page.goto(BASE + f"/{lang}/science", wait_until="domcontentloaded")
        first = page.evaluate(read)
        first_parts = page.evaluate(PART_TOPS)
        page.wait_for_timeout(1500)
        later = page.evaluate(read)
        check(f"settled {w}x{h} {lang}: #liu stays put after load", abs(later[0] - first[0]) <= 2, f"{first[0]} -> {later[0]}")
        check(f"settled {w}x{h} {lang}: the travel room stays put", later[1] == first[1], f"{first[1]} -> {later[1]}")
        check(f"settled {w}x{h} {lang}: the script sets no painting height", later[2] == "", repr(later[2]))
        if w in (1440, 390):
            # The strips' paintings are lazy and the phone's has another ratio than the wide one:
            # the stylesheet reserves each one's box (strip.module.css), so once every painting has
            # arrived the three parts stand where they stood before (the menu's links land by them).
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
            except Exception:
                pass
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
        check(f"strips {w}: no console errors", not errors, "; ".join(errors[:3]))
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


SECTIONS = {"shell": shell, "people": people, "strips": strips, "journey": journey, "settled": settled, "still": still, "multiply": multiply, "languages": languages}

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

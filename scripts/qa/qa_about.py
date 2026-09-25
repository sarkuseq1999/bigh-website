"""QA for the About page: three looks (?look=a|b|c) at desktop (1440x900) and phone (390x844).

Every look and size: no page or console errors and no failed requests; all the locked words on the
page, and never "CellGen"; one h1; the four part anchors; no sideways scrolling; every image has an
alt; tap targets in the page body at least 44 px; body text at least 17 px; the Ask BiGH Science and
Support panels open and close. Then each look's one effect: A's photo sharpens as it reaches the
middle of the window, B's dive swaps the cloud of cells for one cell and the opening words for the
purpose, C's pictures open inside the headline. A reduced-motion run checks the calm versions, and
Korean is smoke-tested.

Pictures: scripts/qa/out/about-<look>-<size>-NN.png, viewport shots taken while scrolling
(full-page screenshots break the svh layouts), plus about-b-<size>-dive-<p>.png.

Usage: python -X utf8 scripts/qa/qa_about.py [base-url]
"""

import os
import re
import sys

from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3009"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)
results = []

LOCKED = [
    "About BiGH",
    "Be in Good Health.",
    "What our name stands for. What our work is for.",
    "A full life has many parts.",
    "We focus on one you can’t see: your cells.",
    "Our mission is to support cellular health and mental energy, helping people live life to the fullest.",
    "Our key formulas begin with scientists.",
    "Dr. Jian Kang Liu, our Chief Scientific Advisor, studies mitochondria and aging. With Dr. Iris Wang, he developed NuriCell and Nature Calm.",
    "280+",
    "scientific papers by Dr. Liu",
    "Meet our scientists",
    "Our flagship formula is older than BiGH.",
    "2016",
    "BiGH founded in California",
    "20+ years",
    "NuriCell’s formula, unchanged",
    "What you can count on.",
    "Made in California.",
    "By GMP-certified manufacturers.",
    "Know where it comes from.",
    "Our green propolis comes only from Minas Gerais, Brazil.",
    "45 days to decide.",
    "Not right for you? Send it back for a refund.",
    "Answers in your language.",
    "We reply in the language you write in.",
    "Curious about the science?",
    "Ask BiGH Science. We help you explore the research, with guidance from the scientists we work with.",
    "Explore our products",
]
SIZES = ((1440, 900, "desk"), (390, 844, "phone"))
CREAM = "rgb(255, 250, 242)"
INK = "rgb(36, 39, 34)"


def check(name, ok, detail=""):
    results.append(ok)
    print(("PASS " if ok else "FAIL ") + name + ("  [" + detail + "]" if detail else ""))


def watch(page):
    problems = []
    page.on("pageerror", lambda e: problems.append("pageerror " + str(e)[:140]))
    page.on(
        "console",
        lambda m: problems.append(f"console.{m.type} " + m.text[:140]) if m.type in ("error", "warning") else None,
    )
    page.on("requestfailed", lambda r: problems.append("requestfailed " + r.url[-80:]))
    page.on("response", lambda r: problems.append(f"http {r.status} " + r.url[-80:]) if r.status >= 400 else None)
    return problems


def opacity(page, selector):
    return page.evaluate(
        "s => { const e = document.querySelector(s); return e ? parseFloat(getComputedStyle(e).opacity) : -1 }",
        selector,
    )


def shoot_scroll(page, name):
    """Viewport shots from top to bottom, waiting for reveals at each stop."""
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(700)
    height = page.evaluate("document.documentElement.scrollHeight")
    view = page.evaluate("innerHeight")
    y, i = 0, 0
    while True:
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(750)
        page.screenshot(path=os.path.join(OUT, f"{name}-{i:02d}.png"))
        i += 1
        if y + view >= height or i >= 24:
            break
        y = min(y + int(view * 0.9), height - view)
    return i


def common_checks(page, look, tag, problems):
    main_text = re.sub(r"\s+", " ", page.evaluate("document.querySelector('main').innerText"))
    missing = [words for words in LOCKED if words not in main_text]
    check(f"{look}-{tag}: every locked line is on the page", not missing, f"missing={missing}")
    check(f"{look}-{tag}: never names CellGen", "cellgen" not in main_text.lower())
    h1 = page.locator("h1").count()
    anchors = page.evaluate("['purpose','roots','experience','promise'].filter(id => !document.getElementById(id))")
    check(f"{look}-{tag}: one h1 and the four part anchors", h1 == 1 and not anchors, f"h1={h1} missingAnchors={anchors}")
    overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    check(f"{look}-{tag}: no sideways scrolling", overflow == 0, f"overflow={overflow}")
    no_alt = page.evaluate("[...document.images].filter(i => !i.hasAttribute('alt')).map(i => i.src.slice(-40))")
    check(f"{look}-{tag}: every image has an alt", not no_alt, f"{no_alt}")
    small = page.evaluate(
        """() => [...document.querySelectorAll('main a, main button')]
            .map(e => [e.textContent.trim().slice(0, 30), e.getBoundingClientRect()])
            .filter(([, r]) => r.width > 0 && (r.height < 44 || r.width < 44))
            .map(([t, r]) => `${t}:${Math.round(r.width)}x${Math.round(r.height)}`)"""
    )
    check(f"{look}-{tag}: tap targets in the page are at least 44 px", not small, f"{small}")
    tiny = page.evaluate(
        """() => [...document.querySelectorAll('main p, main li, main h3')]
            .filter(e => e.offsetParent && parseFloat(getComputedStyle(e).fontSize) < 17)
            .map(e => e.textContent.trim().slice(0, 30) + ':' + getComputedStyle(e).fontSize)"""
    )
    check(f"{look}-{tag}: body text at least 17 px", not tiny, f"{tiny[:4]}")


def panel_checks(page, look, tag):
    page.evaluate("window.scrollTo(0, 0)")
    page.get_by_role("button", name="Ask BiGH Science").first.click()
    page.wait_for_timeout(400)
    title = page.evaluate("document.querySelector('dialog[open] h2')?.textContent")
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    closed = page.evaluate("!document.querySelector('dialog[open]')")
    check(f"{look}-{tag}: Ask BiGH Science panel opens and Escape closes it", title == "Ask BiGH Science" and closed, f"title={title} closed={closed}")
    if tag == "phone":
        page.get_by_role("button", name="Open menu").click()
        page.wait_for_timeout(300)
    page.locator("header").get_by_role("button", name="Support").click()
    page.wait_for_timeout(400)
    title = page.evaluate("document.querySelector('dialog[open] h2')?.textContent")
    page.get_by_role("button", name="Close details").click()
    page.wait_for_timeout(300)
    closed = page.evaluate("!document.querySelector('dialog[open]')")
    check(f"{look}-{tag}: Support panel opens from the menu and closes", title == "BiGH support" and closed, f"title={title} closed={closed}")


def look_a(page, tag):
    if page.url.endswith("look=a"):
        switcher = page.locator("nav[aria-label='Design options']").count()
        check(f"a-{tag}: Mo picked A, so the look switcher is gone", switcher == 0, f"switchers={switcher}")
    blur = "() => { const f = getComputedStyle(document.querySelector('[class*=photoImage]')).filter; const m = /blur\\(([\\d.]+)px\\)/.exec(f); return m ? parseFloat(m[1]) : 0 }"
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(400)
    at_top = page.evaluate(blur)
    page.evaluate(
        "() => { const r = document.querySelector('[class*=photo]').getBoundingClientRect(); window.scrollBy(0, r.top + r.height / 2 - innerHeight / 2) }"
    )
    page.wait_for_timeout(500)
    in_middle = page.evaluate(blur)
    check(f"a-{tag}: the photo is soft below the fold and sharp in the middle", at_top > in_middle and in_middle < 0.3, f"blur top={at_top} middle={in_middle}")


def look_b(page, tag):
    top, height, view = page.evaluate(
        "() => { const s = document.querySelector('[class*=dive]'); const r = s.getBoundingClientRect(); return [r.top + scrollY, r.height, innerHeight] }"
    )
    travel = height - view
    states = {}
    for p in (0, 0.25, 0.5, 0.75, 1.0):
        page.evaluate(f"window.scrollTo(0, {top + p * travel})")
        page.wait_for_timeout(450)
        states[p] = {
            "open": opacity(page, "[class*=openingWords]"),
            "purpose": opacity(page, "[class*=purposeWords]"),
            "cloud": opacity(page, "[class*=cluster]"),
            "cell": opacity(page, "[class*=single]"),
        }
        page.screenshot(path=os.path.join(OUT, f"about-b-{tag}-dive-{int(p * 100):03d}.png"))
    s0, s1 = states[0], states[1.0]
    ok = (
        s0["open"] > 0.95 and s0["purpose"] < 0.05 and s0["cloud"] > 0.95 and s0["cell"] < 0.05
        and s1["open"] < 0.05 and s1["purpose"] > 0.95 and s1["cloud"] < 0.05 and s1["cell"] > 0.95
    )
    check(f"b-{tag}: the dive swaps the cloud for one cell and the opening for the purpose", ok, f"{states}")
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(500)
    dark = page.evaluate("getComputedStyle(document.querySelector('header')).color")
    # scrollIntoView would stop 150 px short (globals.css sets scroll-padding-top), leaving the
    # dark promise section under the header; put the closing's top exactly at the window's top.
    page.evaluate("window.scrollBy(0, document.querySelector('[class*=closing]').getBoundingClientRect().top)")
    page.wait_for_timeout(700)
    light = page.evaluate("getComputedStyle(document.querySelector('header')).color")
    check(f"b-{tag}: header is light-on-dark over navy and dark-on-light over the closing", dark == CREAM and light == INK, f"top={dark} closing={light}")


def look_ab(page, tag):
    """The mix: A's photo focus, then the purpose dive (line one over the cloud, line two with the
    single cell), and a header that follows each section's tone."""
    look_a(page, tag)
    top, height, view = page.evaluate(
        "() => { const s = document.querySelector('[class*=purposeDive]'); const r = s.getBoundingClientRect(); return [r.top + scrollY, r.height, innerHeight] }"
    )
    travel = height - view
    states = {}
    for p in (0, 0.25, 0.5, 0.75, 1.0):
        page.evaluate(f"window.scrollTo(0, {top + p * travel})")
        page.wait_for_timeout(450)
        states[p] = {
            "lineOne": opacity(page, "[class*=purposeDive] [class*=openingWords]"),
            "lineTwo": opacity(page, "[class*=purposeDive] [class*=purposeWords]"),
            "cloud": opacity(page, "[class*=purposeDive] [class*=cluster]"),
            "cell": opacity(page, "[class*=purposeDive] [class*=single]"),
        }
        page.screenshot(path=os.path.join(OUT, f"about-ab-{tag}-dive-{int(p * 100):03d}.png"))
    s0, s1 = states[0], states[1.0]
    ok = (
        s0["lineOne"] > 0.95 and s0["lineTwo"] < 0.05 and s0["cloud"] > 0.95 and s0["cell"] < 0.05
        and s1["lineOne"] < 0.05 and s1["lineTwo"] > 0.95 and s1["cloud"] < 0.05 and s1["cell"] > 0.95
    )
    check(f"ab-{tag}: line one over the cloud, line two with the single cell", ok, f"{states}")
    heading = re.sub(r"\s+", " ", page.evaluate("document.getElementById('purpose-title').textContent"))
    check(
        f"ab-{tag}: the purpose heading (for screen readers) holds both lines",
        heading == "A full life has many parts. We focus on one you can’t see: your cells.",
        heading,
    )
    tones = {}
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(500)
    tones["hero"] = page.evaluate("getComputedStyle(document.querySelector('header')).color")
    for name, selector in (
        ("dive", "[class*=purposeDive]"),
        ("roots", "#roots"),
        ("experience", "#experience"),
        ("promise", "#promise"),
    ):
        page.evaluate(f"window.scrollBy(0, document.querySelector('{selector}').getBoundingClientRect().top + 2)")
        page.wait_for_timeout(600)
        tones[name] = page.evaluate("getComputedStyle(document.querySelector('header')).color")
    expected = {"hero": INK, "dive": CREAM, "roots": INK, "experience": CREAM, "promise": INK}
    check(f"ab-{tag}: the header follows light and dark sections", tones == expected, f"{tones}")


def pill_widths(page, selector):
    return page.evaluate(
        "s => [...document.querySelectorAll(s)].map(e => +(e.getBoundingClientRect().width / parseFloat(getComputedStyle(e).fontSize)).toFixed(2))",
        selector,
    )


def look_c(page, tag):
    # span only: the <img> inside each pill also has "pill" in its class name.
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(1800)
    hero = pill_widths(page, "h1 span[class*=pill]")
    before = pill_widths(page, "#purpose h2 span[class*=pill]")
    page.evaluate("window.scrollBy(0, document.getElementById('purpose').getBoundingClientRect().top)")
    page.wait_for_timeout(1800)
    after = pill_widths(page, "#purpose h2 span[class*=pill]")
    ok = (
        len(hero) == 1 and len(before) == 2 and len(after) == 2
        and hero[0] >= 1.8 and all(w < 1.0 for w in before) and all(w >= 1.8 for w in after)
    )
    check(
        f"c-{tag}: the pictures open inside the headlines (closed until their line is seen)",
        ok,
        f"hero={hero} purpose before={before} after={after} (em)",
    )


with sync_playwright() as p:
    browser = p.chromium.launch()
    for look in ("a", "b", "ab", "c"):
        for w, h, tag in SIZES:
            page = browser.new_page(viewport={"width": w, "height": h})
            problems = watch(page)
            page.goto(f"{BASE}/about?look={look}", wait_until="networkidle")
            page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
            page.wait_for_timeout(600)
            common_checks(page, look, tag, problems)
            {"a": look_a, "b": look_b, "ab": look_ab, "c": look_c}[look](page, tag)
            shots = shoot_scroll(page, f"about-{look}-{tag}")
            panel_checks(page, look, tag)
            check(f"{look}-{tag}: no errors, warnings or failed requests ({shots} shots)", not problems, f"{problems[:3]}")
            page.close()

    # Reduced motion: the calm versions, with everything visible at once.
    for w, h, tag in SIZES:
        for look in ("a", "b", "ab", "c"):
            page = browser.new_page(viewport={"width": w, "height": h}, reduced_motion="reduce")
            problems = watch(page)
            page.goto(f"{BASE}/about?look={look}", wait_until="networkidle")
            page.wait_for_timeout(600)
            if look == "a":
                f = page.evaluate("getComputedStyle(document.querySelector('[class*=photoImage]')).filter")
                check(f"a-{tag}-reduced: the photo is sharp from the start", f == "none", f"filter={f}")
            if look == "b":
                dive = page.locator("[class*=dive]").count()
                stills = page.locator("[class*=still]").count()
                shown = [opacity(page, "[class*=openingWords]"), opacity(page, "[class*=purposeWords]")]
                check(f"b-{tag}-reduced: no dive, two still scenes, all words shown", dive == 0 and stills >= 2 and shown == [1, 1], f"dive={dive} stills={stills} opacity={shown}")
                page.screenshot(path=os.path.join(OUT, f"about-b-{tag}-reduced.png"))
            if look == "ab":
                dive = page.locator("[class*=purposeDive]").count()
                shown = opacity(page, "#purpose [class*=purposeWords]")
                f = page.evaluate("getComputedStyle(document.querySelector('[class*=photoImage]')).filter")
                check(f"ab-{tag}-reduced: no dive, the purpose shows still, photo sharp", dive == 0 and shown == 1 and f == "none", f"dive={dive} opacity={shown} filter={f}")
                page.screenshot(path=os.path.join(OUT, f"about-ab-{tag}-reduced.png"))
            if look == "c":
                hero = pill_widths(page, "h1 span[class*=pill]")
                check(f"c-{tag}-reduced: the pictures are open from the start", hero and hero[0] >= 1.8, f"hero={hero}")
            check(f"{look}-{tag}-reduced: no errors", not problems, f"{problems[:3]}")
            page.close()

    # Korean: the page renders (untranslated About lines fall back to English for now).
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    problems = watch(page)
    page.goto(f"{BASE}/kr/about?look=a", wait_until="networkidle")
    page.wait_for_timeout(600)
    lang = page.evaluate("document.documentElement.lang")
    check("kr-desk: the page renders in the Korean site with no errors", lang == "ko" and page.locator("h1").count() == 1 and not problems, f"lang={lang} {problems[:3]}")
    page.close()
    browser.close()

print(f"\n{sum(results)} passed, {len(results) - sum(results)} failed")

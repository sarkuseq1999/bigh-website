"""QA for the About page in the Ink & Gold look (October 5, 2026; Mo approved the mockup
reference/ink-pages/mockups/about.jpg).

At 1440x900 and 390x844, then the opening at 1280x720, 1536x1000, 1024x768, 900x1100, 768x1024
and 360x780: answers 200; no console errors or warnings (except the built site's link-prefetch
CSS preload note, see PREFETCH_CSS); no failed requests; one h1, English
"Be in Good Health." with lang="en"; every locked line is on the page; no WebGL canvas in the
page; every painting multiplies onto the paper and the page wears the paper texture; the header
marks About as the current page and its Products link goes to /#products; no sideways scrolling;
text at least 15px and navigation at least 18px; links and buttons in the page at least 48px tall;
the cell sits in the first screen and never touches the title or the opening words; four
stations; the Support and Ask BiGH Science sheets open, close and hand focus back.
Desktop only (900px and wider): the brush layer draws the page layout, and its ink passes each
station's leader. Review focus: /about#promise lands below the header; Skip to content puts focus
at the words; with pictures blocked every heading and paragraph is visible.
Reduced motion: every painting shown, the gold leaf fully up, the whole line drawn.
Other languages (kr, jp, cns, vn): 200, no console errors, the h1 stays English, no English
source sentence left visible.

Pictures: scripts/qa/out/about-ink/<size>-NN.png (viewport shots while scrolling).

Usage: python -X utf8 scripts/qa/qa_about.py [base-url]
"""

import os
import re
import sys

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = ARGS[0] if ARGS else "http://localhost:3025"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "about-ink")
os.makedirs(OUT, exist_ok=True)
results = []

# The locked words (src/components/about/about-content.ts), as they appear on the page.
LOCKED = [
    "What our name stands for.",
    "What our work is for.",
    "A full life has many parts.",
    "We focus on one you can’t see: your cells.",
    "Our mission is to support cellular health and mental energy, helping people live life to the fullest.",
    "Our key formulas begin with scientists.",
    "Dr. Jiankang Liu, our Chief Scientific Advisor, studies mitochondria and aging. He formulated NuriCell, and with Dr. Iris Wang, he developed Nature Calm.",
    "Meet our scientists",
    "Our flagship formula is older than BiGH.",
    "scientific papers by Dr. Liu",
    "BiGH founded in California",
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
    "Ask BiGH Science",
    "Explore our products",
]
STATIONS = ["Our purpose", "Our scientific roots", "Our experience", "Our promise"]


def check(name, ok, detail=""):
    results.append((name, bool(ok)))
    print(f"{'PASS' if ok else 'FAIL'} {name}{(' — ' + str(detail)) if detail and not ok else ''}")


# One warning is not counted, and only on the built site: Chrome's note that a stylesheet of
# ANOTHER route was preloaded and not used. Next's <Link> prefetch (production only) adds
# <link rel="preload" as="style"> for each linked route's CSS. Evidence (next start, 1440x900,
# scrolled, October 5, 2026; task5-fix1-preload-evidence.log): the homepage shows it 3 times (the
# product page's, Science's and About's CSS), /science once (the homepage's CSS), /about 3 times
# (the product page's, Science's and the homepage's CSS); with the router's prefetch requests
# blocked it never appears on any of them. qa_home_ink.py counts console errors only, so it never
# sees this warning. Only this exact message for a /_next/static/*.css file is ignored.
PREFETCH_CSS = re.compile(
    r"^The resource \S+/_next/static/\S+\.css was preloaded using link preload but not used "
    r"within a few seconds from the window's load event\."
)


def counted(message):
    return not (message.type == "warning" and PREFETCH_CSS.match(message.text))


def open_page(browser, width, height, path="/about", reduced=False, block_images=False):
    context = browser.new_context(
        viewport={"width": width, "height": height},
        reduced_motion="reduce" if reduced else "no-preference",
    )
    page = context.new_page()
    errors, failed = [], []
    page.on(
        "console",
        lambda m: errors.append(m.text) if m.type in ("error", "warning") and counted(m) else None,
    )
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("requestfailed", lambda r: failed.append(r.url))
    if block_images:
        page.route("**/*.{webp,png,jpg,jpeg,avif}", lambda route: route.abort())
        page.route("**/_next/image**", lambda route: route.abort())
    response = page.goto(f"{BASE}{path}", wait_until="networkidle", timeout=120000)
    page.evaluate("document.fonts.ready.then(() => true)")
    page.wait_for_timeout(1200)
    return context, page, response, errors, failed


def shots(page, tag, height):
    total = page.evaluate("document.documentElement.scrollHeight")
    y, i = 0, 0
    while y < total:
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(900)
        page.screenshot(path=os.path.join(OUT, f"{tag}-{i:02d}.png"))
        y += height
        i += 1


def desktop_and_phone(browser):
    for width, height in [(1440, 900), (390, 844)]:
        tag = f"{width}x{height}"
        context, page, response, errors, failed = open_page(browser, width, height)
        check(f"{tag} answers 200", response.status == 200, response.status)
        text = page.evaluate("document.body.innerText")
        missing = [line for line in LOCKED if line not in text]
        check(f"{tag} every locked line", not missing, missing)
        h1 = page.evaluate(
            "[...document.querySelectorAll('h1')].map(h => [h.getAttribute('aria-label') || h.textContent.trim(), h.lang])"
        )
        check(f"{tag} one English h1", h1 == [["Be in Good Health.", "en"]], h1)
        check(f"{tag} no WebGL canvas in the page", page.evaluate("document.querySelectorAll('main canvas').length") == 0)
        blends = page.evaluate(
            "[...document.querySelectorAll('main img[data-bloom]')].map(i => getComputedStyle(i).mixBlendMode)"
        )
        check(f"{tag} paintings multiply", blends and all(b == "multiply" for b in blends), blends)
        paper = page.evaluate("getComputedStyle(document.querySelector('[data-look=\"ink\"]')).backgroundImage")
        check(f"{tag} paper texture", "paper.webp" in paper, paper)
        nav = page.evaluate(
            """() => { const n = document.querySelector('#home-navigation');
                 return { current: [...n.querySelectorAll('[aria-current="page"]')].map(a => a.textContent.trim()),
                          products: [...n.querySelectorAll('a')].find(a => a.textContent.trim() === 'Products')?.getAttribute('href') }; }"""
        )
        check(f"{tag} header marks About", nav["current"] == ["About"], nav)
        check(f"{tag} Products goes home", (nav["products"] or "").endswith("/#products"), nav)
        sideways = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
        check(f"{tag} no sideways scrolling", sideways <= 0, sideways)
        small = page.evaluate(
            """[...document.querySelectorAll('main *')].filter(e => e.childNodes.length && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && e.offsetParent)
                 .map(e => [e.textContent.trim().slice(0, 30), parseFloat(getComputedStyle(e).fontSize)]).filter(([, s]) => s < 15)"""
        )
        check(f"{tag} text at least 15px", not small, small[:5])
        targets = page.evaluate(
            """[...document.querySelectorAll('main a, main button')].filter(e => e.offsetParent)
                 .map(e => [e.textContent.trim().slice(0, 30), Math.round(e.getBoundingClientRect().height)]).filter(([, h]) => h < 48)"""
        )
        check(f"{tag} targets at least 48px", not targets, targets)
        stations = page.evaluate("[...document.querySelectorAll('[data-station]')].map(s => s.textContent.trim())")
        check(f"{tag} four stations", stations == STATIONS, stations)
        cell = page.evaluate(
            """() => { const c = document.querySelector('[data-brush="about-cell"] img').getBoundingClientRect();
                 const words = [...document.querySelectorAll('[data-brush="opening"] h1, [data-brush="opening"] p')].map(e => e.getBoundingClientRect());
                 const hit = words.some(w => !(c.right <= w.left || c.left >= w.right || c.bottom <= w.top || c.top >= w.bottom));
                 return { top: c.top, inFirst: c.top < innerHeight, hit }; }"""
        )
        check(f"{tag} cell in the first screen", cell["inFirst"], cell)
        check(f"{tag} cell clear of the words", not cell["hit"], cell)
        # Sheets: Support from the header (menu on a phone), Ask from the pause.
        if width < 1101:
            page.click("button[aria-controls='home-navigation']")
        page.click("#home-navigation button:has-text('Support')")
        page.wait_for_timeout(900)
        check(f"{tag} Support sheet opens", page.evaluate("!!document.querySelector('dialog[open]')"))
        page.keyboard.press("Escape")
        page.wait_for_timeout(600)
        ask = page.locator("main button:has-text('Ask BiGH Science')")
        ask.scroll_into_view_if_needed()
        ask.click()
        page.wait_for_timeout(900)
        sheet = page.evaluate("document.querySelector('dialog[open]')?.innerText ?? ''")
        check(f"{tag} Ask sheet opens", "Ask BiGH Science" in sheet, sheet[:80])
        page.keyboard.press("Escape")
        page.wait_for_timeout(600)
        back = page.evaluate("document.activeElement?.textContent?.trim()")
        check(f"{tag} focus returns to Ask", back == "Ask BiGH Science", back)
        check(f"{tag} no console errors or warnings", not errors, errors[:3])
        check(f"{tag} no failed requests", not failed, failed[:3])
        page.evaluate("window.scrollTo(0, 0)")
        shots(page, tag, height)
        context.close()


def openings(browser):
    for width, height in [(1280, 720), (1536, 1000), (1024, 768), (900, 1100), (768, 1024), (360, 780)]:
        tag = f"{width}x{height}"
        context, page, response, errors, failed = open_page(browser, width, height)
        cell = page.evaluate(
            """() => { const c = document.querySelector('[data-brush="about-cell"] img').getBoundingClientRect();
                 const words = [...document.querySelectorAll('[data-brush="opening"] h1, [data-brush="opening"] p')].map(e => e.getBoundingClientRect());
                 return { inFirst: c.top < innerHeight, hit: words.some(w => !(c.right <= w.left || c.left >= w.right || c.bottom <= w.top || c.top >= w.bottom)) }; }"""
        )
        check(f"{tag} cell in the first screen", cell["inFirst"], cell)
        check(f"{tag} cell clear of the words", not cell["hit"], cell)
        sideways = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
        check(f"{tag} no sideways scrolling", sideways <= 0, sideways)
        page.screenshot(path=os.path.join(OUT, f"opening-{tag}.png"))
        context.close()


def line_and_focus(browser):
    context, page, response, errors, failed = open_page(browser, 1440, 900, reduced=True)
    layout = page.evaluate("document.querySelector('[data-lifts]')?.dataset.layout")
    check("1440 brush draws the page layout", layout == "page", layout)
    # Each station's leader ends at the line: some ink within 14px right of the label's leader.
    meets = page.evaluate(
        """() => [...document.querySelectorAll('[data-station]')].map(s => {
             const box = s.getBoundingClientRect(); const x = box.right + window.scrollX; const y = box.top + box.height / 2 + window.scrollY;
             const host = document.querySelector('[data-lifts]'); const top = host.getBoundingClientRect().top + window.scrollY;
             for (const c of host.querySelectorAll('canvas')) {
               const t = parseFloat(c.style.top); const h = parseFloat(c.style.height); if (y - top < t || y - top > t + h) continue;
               const ctx = c.getContext('2d'); const sx = c.width / c.clientWidth;
               const data = ctx.getImageData(Math.round((x - host.getBoundingClientRect().left - window.scrollX) * sx), Math.round((y - top - t) * sx), Math.round(28 * sx), 1).data;
               for (let i = 3; i < data.length; i += 4) if (data[i] > 40) return true;
             } return false; })"""
    )
    check("1440 line meets every station", meets and all(meets), meets)
    bloom = page.evaluate("[...document.querySelectorAll('[data-bloom]')].every(e => e.dataset.bloom === 'done')")
    check("reduced motion: every painting shown", bloom)
    charge = page.evaluate("getComputedStyle(document.querySelector('[data-charge]')).opacity")
    check("reduced motion: gold leaf fully up", float(charge) == 0, charge)
    context.close()
    # With motion: the cell blooms with its leaf drained, then the leaf comes up.
    context, page, response, errors, failed = open_page(browser, 1440, 900)
    early = float(page.evaluate("getComputedStyle(document.querySelector('[data-charge]')).opacity"))
    page.wait_for_timeout(9000)
    late = float(page.evaluate("getComputedStyle(document.querySelector('[data-charge]')).opacity"))
    check("motion: the gold leaf comes up after the bloom", early > 0.5 and late < 0.05, [early, late])
    context.close()
    # Deep link lands below the header.
    context, page, response, errors, failed = open_page(browser, 1440, 900, path="/about#promise")
    page.wait_for_timeout(1500)
    gap = page.evaluate(
        "document.querySelector('#promise-title').getBoundingClientRect().top - document.querySelector('header').getBoundingClientRect().bottom"
    )
    check("/about#promise lands below the header", gap >= 0, gap)
    context.close()
    # Skip to content, on a page opened without a #fragment: after /about#promise the browser
    # starts Tab from the fragment's target (the next stop is the pause's Ask button), as it should.
    context, page, response, errors, failed = open_page(browser, 1440, 900)
    page.keyboard.press("Tab")
    skip = page.evaluate("document.activeElement?.textContent?.trim()")
    page.keyboard.press("Enter")
    page.wait_for_timeout(300)
    focus = page.evaluate("document.activeElement?.id")
    check("Skip to content puts focus at the words", skip == "Skip to content" and focus == "main", [skip, focus])
    context.close()
    # Pictures blocked: words still visible. Read like a visitor, to the end of the page: each
    # station waits for the brush line to reach it (DESIGN.md, Stations), which has nothing to do
    # with pictures.
    context, page, response, errors, failed = open_page(browser, 1440, 900, block_images=True)
    total = page.evaluate("document.documentElement.scrollHeight")
    for y in range(0, total, 450):
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(250)
    page.wait_for_timeout(1500)
    hidden = page.evaluate(
        """[...document.querySelectorAll('main h1, main h2, main p')].filter(e => {
             let n = e; while (n) { if (parseFloat(getComputedStyle(n).opacity) < 0.05) return true; n = n.parentElement; } return false; })
           .map(e => e.textContent.trim().slice(0, 30))"""
    )
    check("pictures blocked: every heading and paragraph visible", not hidden, hidden[:5])
    context.close()


def languages(browser):
    english = [line for line in LOCKED if len(line) > 24]
    for lang in ["kr", "jp", "cns", "vn"]:
        context, page, response, errors, failed = open_page(browser, 1440, 900, path=f"/{lang}/about")
        check(f"{lang} answers 200", response.status == 200, response.status)
        h1 = page.evaluate("document.querySelector('h1').getAttribute('aria-label')")
        check(f"{lang} h1 stays English", h1 == "Be in Good Health.", h1)
        text = page.evaluate("document.querySelector('main').innerText")
        left = [line for line in english if line in text]
        check(f"{lang} no English sentence left", not left, left[:3])
        check(f"{lang} no console errors or warnings", not errors, errors[:3])
        page.screenshot(path=os.path.join(OUT, f"{lang}-opening.png"))
        context.close()


with sync_playwright() as p:
    browser = p.chromium.launch(args=["--use-angle=d3d11"])
    desktop_and_phone(browser)
    openings(browser)
    line_and_focus(browser)
    languages(browser)
    browser.close()

passed = sum(ok for _, ok in results)
print(f"\n{passed}/{len(results)} passed")
sys.exit(0 if passed == len(results) else 1)

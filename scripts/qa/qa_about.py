"""QA for the About page, "The name, on a folded letter" (Mo approved design D on October 6, 2026;
mockup reference/ink-pages/mockups/about-d.png; spec docs/superpowers/specs/2026-10-05-ink-pages-design.md).

desktop_and_phone (1440x900, 390x844): answers 200; no console errors or warnings (except the built
site's link-prefetch CSS note, PREFETCH_CSS); no failed requests; one h1, English "Be in Good
Health." with lang="en"; every locked line on the page; no canvas and no brush layer; every painting
multiplies onto the paper; the page wears the aged paper; the menu bar marks About (bar and narrow
menu), has no Home link, and its Products drop-down holds the five products and "Explore our
products."; no sideways scrolling; text 15px+, navigation 18px+, targets 48px+; the four chapter
words B, i, G, H, hidden from screen readers, in English, their paintings loaded; the written name
loads eagerly and is preloaded; the Support and Ask sheets open, close and hand focus back.
letter_layout (1440x900, 1280x800, 1024x768, 768x1024, 390x844): the middle fold from 900px up
(centred within 2px), none below; four folds across; on two columns Be's letter left and words
right, in's words left and letter and portrait right, Good's letter and rings left and words right,
each 24px or more clear of the middle fold; the promise heading centred; four promises in one row
from 1200px, two by two below that, one column on one column; the closing centred; the closing H
24px or more above its heading; no words over a painting; Dr. Liu's photo in the middle of its pool;
the rings carry "Illustration". On one column each part's chapter word stands over its label, over
its heading.
focus: Skip to content puts focus at the words; with pictures blocked every heading and paragraph
is visible.
boundary (899x900, 900x900): no sideways scrolling; the middle fold shows at 900 only; at 900 no
words cross it.
first_screen (1280x720, 1440x900, 1536x864, 390x844): the written name and the title in the first
screen; from 900px the band starts in it too.

Pictures: scripts/qa/out/about-letter/<size>-NN.png (viewport shots while scrolling).

Usage: python -X utf8 scripts/qa/qa_about.py [base-url] [--only=desktop_and_phone,letter_layout,focus,boundary,first_screen]
"""

import os
import re
import sys

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = ARGS[0] if ARGS else "http://localhost:3025"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "about-letter")
os.makedirs(OUT, exist_ok=True)
results = []

# The locked words (src/components/about/about-content.ts), as they appear on the page.
LOCKED = [
    "What our name stands for.",
    "What our work is for.",
    "Our purpose",
    "A full life has many parts.",
    "We focus on one you can’t see: your cells.",
    "Our mission is to support cellular health and mental energy, helping people live life to the fullest.",
    "Our scientific roots",
    "Our key formulas begin with scientists.",
    "Dr. Jiankang Liu, our Chief Scientific Advisor, studies mitochondria and aging. He formulated NuriCell, and with Dr. Iris Wang, he developed Nature Calm.",
    "Meet our scientists",
    "Our experience",
    "Our flagship formula is older than BiGH.",
    "scientific papers by Dr. Liu",
    "BiGH founded in California",
    "NuriCell’s formula, unchanged",
    "Our promise",
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


def check(name, ok, detail=""):
    results.append((name, bool(ok)))
    print(f"{'PASS' if ok else 'FAIL'} {name}{(' — ' + str(detail)) if detail and not ok else ''}")


# One warning is not counted, and only on the built site: Chrome's note that a stylesheet of
# ANOTHER route was preloaded and not used (Next's <Link> prefetch adds <link rel="preload"
# as="style"> for each linked route's CSS; with the router's prefetch blocked it never appears).
# Only this exact message for a /_next/static/*.css file is ignored.
PREFETCH_CSS = re.compile(
    r"^The resource \S+/_next/static/\S+\.css was preloaded using link preload but not used "
    r"within a few seconds from the window's load event\."
)


def counted(message):
    return message.type != "warning" or not PREFETCH_CSS.match(message.text)


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


def scroll_through(page, step=450, pause=250):
    """Read to the end like a visitor (lazy pictures load, arrivals fire), then back to the top."""
    total = page.evaluate("document.documentElement.scrollHeight")
    for y in range(0, total, step):
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(pause)
    page.wait_for_timeout(800)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(400)


# The folds: the middle one is the sheet's ::before (from 900px), each part's fold across is its
# own ::before. The page's middle is the document's (scrollbar excluded).
FOLDS_JS = """() => {
  const sheet = document.querySelector('[data-sheet]');
  const v = getComputedStyle(sheet, '::before');
  const sb = sheet.getBoundingClientRect();
  const shown = v.content !== 'none' && v.display !== 'none';
  return { middle: shown, centre: shown ? sb.left + parseFloat(v.left) + parseFloat(v.width) / 2 : null,
           mid: document.documentElement.clientWidth / 2,
           across: [...document.querySelectorAll('[data-part]')].filter(p => getComputedStyle(p, '::before').content !== 'none').length };
}"""

# Each side's horizontal extent: the union of the matched boxes.
SIDES_JS = """() => {
  const side = (sel) => { const b = [...document.querySelectorAll(sel)].filter(e => e.offsetParent).map(e => e.getBoundingClientRect());
    return b.length ? { left: Math.min(...b.map(x => x.left)), right: Math.max(...b.map(x => x.right)) } : null; };
  return { mid: document.documentElement.clientWidth / 2,
    purposeLetter: side('#purpose [data-chapter]'), purposeWords: side('#purpose [data-label], #purpose h2, #purpose p'),
    rootsWords: side('#roots [data-label], #roots h2, #roots p, #roots a'), rootsLetter: side('#roots [data-chapter]'), rootsPrint: side('#roots [data-mount]'),
    goodLetter: side('#experience [data-chapter]'), goodRings: side('#experience [data-rings] img'), goodWords: side('#experience [data-label], #experience h2, #experience dl') };
}"""

# Words over paintings: glyph rectangles of the page's words (not the chapter words' own letters)
# against the boxes of the paintings that are not meant to sit under words (the pool is: Dr. Liu's
# print rests on it).
OVERLAP_JS = """() => {
  const words = [...document.querySelectorAll('main h1, main h2, main h3, main p, main dt, main dd, main a, main button, main figcaption')]
    .filter(e => e.offsetParent && !e.closest('[data-chapter], [data-word]'));
  const art = [...document.querySelectorAll('[data-chapter] img, [data-word] img, [data-rings] img, [data-band], [data-promise] img')].filter(e => e.offsetParent);
  const hits = [];
  for (const w of words) {
    const range = document.createRange(); range.selectNodeContents(w);
    const rects = [...range.getClientRects()].filter(r => r.width > 1);
    for (const a of art) {
      const b = a.getBoundingClientRect();
      if (rects.some(r => r.left < b.right - 2 && r.right > b.left + 2 && r.top < b.bottom - 2 && r.bottom > b.top + 2))
        hits.push([w.textContent.trim().slice(0, 24), (a.getAttribute('src') || a.tagName).slice(-32)]);
    }
  }
  return hits;
}"""

# Words crossing the middle fold, in the two-sided parts (from 900px): glyph rectangles that come
# within 24px of the page's middle.
CREASE_JS = """() => {
  const mid = document.documentElement.clientWidth / 2;
  const out = [];
  for (const el of document.querySelectorAll('#purpose [data-label], #purpose h2, #purpose p, #roots [data-label], #roots h2, #roots p, #roots a, #experience [data-label], #experience h2, #experience dt, #experience dd')) {
    if (!el.offsetParent) continue;
    const range = document.createRange(); range.selectNodeContents(el);
    for (const r of range.getClientRects()) {
      if (r.width > 1 && r.left < mid + 24 && r.right > mid - 24) { out.push([el.textContent.trim().slice(0, 20), Math.round(r.left), Math.round(r.right), Math.round(mid)]); break; }
    }
  }
  return out;
}"""


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
        check(f"{tag} no canvas in the page", page.evaluate("document.querySelectorAll('main canvas').length") == 0)
        check(f"{tag} no brush layer", page.evaluate("!document.querySelector('[data-lifts]')"))
        blends = page.evaluate(
            "[...document.querySelectorAll('main img')].filter(i => !i.closest('[data-mount]') && !i.matches('[data-dot]')).map(i => getComputedStyle(i).mixBlendMode)"
        )
        check(f"{tag} paintings multiply", blends and all(b == "multiply" for b in blends), blends)
        paper = page.evaluate("getComputedStyle(document.querySelector('[data-look=\"ink\"]')).backgroundImage")
        check(f"{tag} the aged paper", "paper-aged" in paper, paper)
        chapters = page.evaluate(
            "[...document.querySelectorAll('[data-chapter]')].map(c => [c.dataset.chapter, c.getAttribute('aria-hidden'), c.lang])"
        )
        check(
            f"{tag} four chapter words, hidden from screen readers, in English",
            chapters == [["B", "true", "en"], ["i", "true", "en"], ["G", "true", "en"], ["H", "true", "en"]],
            chapters,
        )
        eager = page.evaluate(
            """(() => { const i = document.querySelector('[data-word] img');
                 const preload = [...document.querySelectorAll('link[rel=preload][as=image]')]
                   .some(l => ((l.getAttribute('imagesrcset') || '') + (l.getAttribute('href') || '')).includes('word-v'));
                 return { loading: i.getAttribute('loading'), preload }; })()"""
        )
        check(f"{tag} the written name loads eagerly and is preloaded", eager["loading"] != "lazy" and eager["preload"], eager)
        nav = page.evaluate(
            """() => { const n = document.querySelector('#site-navigation');
                 const sheet = document.querySelector('[data-nav-sheet]');
                 const panel = document.querySelector('[data-nav-panel="products"]');
                 const trigger = document.querySelector('[data-nav-trigger="products"]');
                 return { current: [...n.querySelectorAll('[aria-current="page"]')].map(a => a.textContent.trim()),
                          menuCurrent: [...sheet.querySelectorAll('[aria-current="page"]')].map(a => a.textContent.trim()),
                          home: [...document.querySelectorAll('header a')].filter(a => a.textContent.trim() === 'Home').length,
                          mark: n.querySelector('[data-nav-logo]')?.getAttribute('href') ?? null,
                          productsControls: trigger?.getAttribute('aria-controls') === panel?.id,
                          productPages: [...panel.querySelectorAll('a[href*="/products/"]')].length,
                          productsAll: [...panel.querySelectorAll('a')].map(a => a.getAttribute('href')).filter(h => h.endsWith('/#products')) }; }"""
        )
        check(f"{tag} header marks About", nav["current"] == ["About"] and nav["menuCurrent"] == ["About"], nav)
        check(f"{tag} no Home link; the mark goes home", nav["home"] == 0 and nav["mark"] == "/", nav)
        check(
            f"{tag} Products opens the five products and Explore goes home",
            nav["productsControls"] and nav["productPages"] == 5 and len(nav["productsAll"]) == 1,
            nav,
        )
        if width >= 1101:
            words = page.evaluate(
                "[...document.querySelectorAll('#site-navigation [data-nav-trigger], #site-navigation a[href$=\"/about\"], #site-navigation button')].filter(e => e.offsetParent && ['Products', 'Science', 'About', 'Support'].includes(e.textContent.trim())).map(e => [e.textContent.trim(), parseFloat(getComputedStyle(e).fontSize)])"
            )
            check(f"{tag} navigation at least 18px", len(words) == 4 and all(s >= 18 for _, s in words), words)
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
        if width < 1101:
            page.click("[data-nav-menu-button]")
            page.wait_for_timeout(900)
            page.click("[data-nav-sheet] button:has-text('Support')")
        else:
            page.click("#site-navigation button:has-text('Support')")
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
        page.evaluate("window.scrollTo(0, 0)")
        shots(page, tag, height)
        loaded = page.evaluate(
            "[...document.querySelectorAll('[data-chapter] img, [data-word] img')].map(i => i.complete && i.naturalWidth > 0)"
        )
        check(f"{tag} every letter's painting loaded", loaded and all(loaded), loaded)
        check(f"{tag} no console errors or warnings", not errors, errors[:3])
        check(f"{tag} no failed requests", not failed, failed[:3])
        context.close()


def letter_layout(browser):
    for width, height in [(1440, 900), (1280, 800), (1024, 768), (768, 1024), (390, 844)]:
        tag = f"{width}x{height}"
        two = width >= 900
        context, page, response, errors, failed = open_page(browser, width, height, reduced=True)
        folds = page.evaluate(FOLDS_JS)
        if two:
            check(f"{tag} the middle fold, centred", folds["middle"] and abs(folds["centre"] - folds["mid"]) <= 2, folds)
        else:
            check(f"{tag} no middle fold on one column", not folds["middle"], folds)
        check(f"{tag} four folds across", folds["across"] == 4, folds)
        if two:
            s = page.evaluate(SIDES_JS)
            m = s["mid"]
            left_ok = lambda b: b is not None and b["right"] <= m - 24
            right_ok = lambda b: b is not None and b["left"] >= m + 24
            check(f"{tag} Be: letter left, words right", left_ok(s["purposeLetter"]) and right_ok(s["purposeWords"]), s)
            check(f"{tag} in: words left, letter and portrait right", left_ok(s["rootsWords"]) and right_ok(s["rootsLetter"]) and right_ok(s["rootsPrint"]), s)
            check(f"{tag} Good: letter and rings left, words right", left_ok(s["goodLetter"]) and left_ok(s["goodRings"]) and right_ok(s["goodWords"]), s)
        centred = page.evaluate(
            """() => { const mid = document.documentElement.clientWidth / 2;
                 const c = (sel) => { const b = document.querySelector(sel).getBoundingClientRect(); return Math.round(b.left + b.width / 2 - mid); };
                 return { promise: c('#promise-title'), closing: c('#closing-title'), closingWord: c('#closing [data-chapter]') }; }"""
        )
        check(
            f"{tag} the promise heading and the closing are centred",
            abs(centred["promise"]) <= 4 and abs(centred["closing"]) <= 4 and abs(centred["closingWord"]) <= 32,
            centred,
        )
        rows = page.evaluate("new Set([...document.querySelectorAll('[data-promise]')].map(li => Math.round(li.getBoundingClientRect().top / 4))).size")
        want = 1 if width >= 1200 else 2 if two else 4
        check(f"{tag} the promises in {want} row(s)", rows == want, rows)
        gap = page.evaluate(
            "document.querySelector('#closing-title').getBoundingClientRect().top - document.querySelector('#closing [data-chapter] img').getBoundingClientRect().bottom"
        )
        check(f"{tag} clear paper under the closing H (24px or more)", gap >= 24, round(gap))
        hits = page.evaluate(OVERLAP_JS)
        check(f"{tag} no words over a painting", not hits, hits[:4])
        liu = page.evaluate(
            """() => { const p = document.querySelector('[data-pool]').getBoundingClientRect();
                 const f = document.querySelector('[data-mount] img').getBoundingClientRect();
                 return { dx: (f.left + f.width / 2 - p.left - p.width / 2) / p.width, dy: (f.top + f.height / 2 - p.top - p.height / 2) / p.height }; }"""
        )
        check(f"{tag} Dr. Liu's photo in the middle of its pool", abs(liu["dx"]) <= 0.15 and abs(liu["dy"]) <= 0.15, liu)
        caption = page.evaluate("document.querySelector('[data-rings] figcaption')?.textContent.trim()")
        check(f"{tag} the rings carry Illustration", caption == "Illustration", caption)
        if not two:
            order = page.evaluate(
                """() => ['purpose', 'roots', 'experience'].map(id => { const s = document.getElementById(id);
                     const t = (sel) => s.querySelector(sel).getBoundingClientRect().top;
                     return [id, t('[data-chapter]') < t('[data-label]') && t('[data-label]') < t('h2')]; })"""
            )
            check(f"{tag} one column: chapter word, then label, then heading", all(ok for _, ok in order), order)
        page.screenshot(path=os.path.join(OUT, f"layout-{tag}.png"), full_page=False)
        context.close()


def focus(browser):
    context, page, response, errors, failed = open_page(browser, 1440, 900)
    page.keyboard.press("Tab")
    skip = page.evaluate("document.activeElement?.textContent?.trim()")
    page.keyboard.press("Enter")
    page.wait_for_timeout(300)
    where = page.evaluate("document.activeElement?.id")
    check("Skip to content puts focus at the words", skip == "Skip to content" and where == "main", [skip, where])
    context.close()
    context, page, response, errors, failed = open_page(browser, 1440, 900, block_images=True)
    scroll_through(page)
    hidden = page.evaluate(
        """[...document.querySelectorAll('main h1, main h2, main h3, main p')].filter(e => {
             let n = e; while (n) { if (parseFloat(getComputedStyle(n).opacity) < 0.05) return true; n = n.parentElement; } return false; })
           .map(e => e.textContent.trim().slice(0, 30))"""
    )
    check("pictures blocked: every heading and paragraph visible", not hidden, hidden[:5])
    context.close()


def boundary(browser):
    for width in (899, 900):
        context, page, response, errors, failed = open_page(browser, width, 900, reduced=True)
        sideways = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
        check(f"{width} no sideways scrolling", sideways <= 0, sideways)
        folds = page.evaluate(FOLDS_JS)
        check(f"{width} the middle fold {'shows' if width == 900 else 'is gone'}", folds["middle"] == (width == 900), folds)
        if width == 900:
            crossing = page.evaluate(CREASE_JS)
            check("900 no words cross the middle fold", not crossing, crossing[:3])
        context.close()


def first_screen(browser):
    for width, height in [(1280, 720), (1440, 900), (1536, 864), (390, 844)]:
        tag = f"{width}x{height}"
        context, page, response, errors, failed = open_page(browser, width, height, reduced=True)
        geo = page.evaluate(
            """() => ({ word: document.querySelector('[data-word] img').getBoundingClientRect().bottom,
                        title: document.querySelector('h1').getBoundingClientRect().bottom,
                        band: document.querySelector('[data-band]').getBoundingClientRect().top, win: innerHeight })"""
        )
        check(f"{tag} the written name and the title in the first screen", geo["word"] <= geo["win"] and geo["title"] <= geo["win"], geo)
        if width >= 900:
            check(f"{tag} the band starts in the first screen", geo["band"] < geo["win"], geo)
        context.close()


# --only=letter_layout,boundary runs just those groups (while working on one thing); the full run is the gate.
GROUPS = [desktop_and_phone, letter_layout, focus, boundary, first_screen]
ONLY = next((a.split("=", 1)[1].split(",") for a in sys.argv[1:] if a.startswith("--only=")), None)

with sync_playwright() as p:
    browser = p.chromium.launch(args=["--use-angle=d3d11"])
    for group in GROUPS:
        if ONLY is None or group.__name__ in ONLY:
            group(browser)
    browser.close()

passed = sum(ok for _, ok in results)
print(f"\n{passed}/{len(results)} passed")
sys.exit(0 if passed == len(results) else 1)

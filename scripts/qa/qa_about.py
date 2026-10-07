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
letter_layout (1440x900, 1280x800, 1200x800, 1024x768, 768x1024, 390x844): the middle fold from
900px up (centred within 2px), none below; four folds across; on two columns Be's letter left and
words right, in's words left and letter and portrait right, Good's letter and rings left and words
right, each 24px or more clear of the middle fold; the promise heading centred; four promises in one
row from 1200px, two by two below that, one column on one column; promise headings side by side stand
level; the closing centred; the closing H
24px or more above its heading; no words over a painting; Dr. Liu's photo in the middle of its pool;
the rings carry "Illustration"; hello in five languages centred under its promise (8px). On two
columns Dr. Liu's pool 16px or more clear of the middle fold, and the roots' words start level with
the "in" (24px); the closing H's ink and its "ealth" stay outside the middle fold's 16px on both
sides. As in the mockup, on two columns Dr. Liu's print stands beside the "in", its bottom level
with "Meet our scientists" (48px), and the part is no taller than its words need (the words fill
70% or more of its height); from 1200px the rings stand beside the G, and the three figures stand
in one row, each on one line. At 1440x900, no seam where the settled bar meets the page's darker sides (a step
of 4 levels or less). On one column each part's chapter word stands over its label, over its
heading.
fold_header (1024x768, 1440x900, 1536x864, at the top of the page): the middle fold starts under the
header's box and draws nothing inside it (with the header hidden, the paper down the page's middle
inside the header's box matches the paper beside it, 2 levels or less).
motion: reduced motion is complete and still (no waiting letters, every bloom done, the dots up, no
running animation, nothing logged, the wipe never fetched), and before the page's scripts run the
server-marked band is already crisp and shown; with motion the name is written (its animation, one
breath) and its gold dot is delayed until the name is visibly done (1.7s or more) and comes up
after it; the band waits invisible, nothing of it shows before its bloom (no pop, then vanish), and
then it blooms; a chapter letter waits out of view, is written as it comes in and ends unmasked;
the wipe front over the H's stem is a soft ink front (no regular banding down the stem); the wipe
mask is preloaded for motion visitors only (and fetched once). With JavaScript off the written name is
visible and the band is crisp and shown.
focus: Skip to content puts focus at the words; with pictures blocked every heading and paragraph
is visible.
deep_links (1440x900, 1024x768, 768x1024, 390x844, 360x780): /about#purpose, #roots, #experience,
#promise land the part's first content 0-64px under the header, nothing of it under the bar, its
heading fully in the window. languages (kr, jp, cns, vn): 200, no console errors, the h1 and the
chapter words stay English, no English source sentence left visible. languages_layout (every language
at 1440x900, 1024x768, 768x1024, 390x844, 360x780; Japanese and Chinese also at 900x900): no word
crosses the side margins; in Korean, Japanese, Chinese and Vietnamese no bad line break; from 900px
no words cross the middle fold; in Japanese and Chinese, at 390, 360 and 900px, no heading phrase
(up to 12 characters) is split across lines; Vietnamese at 390: the closing pills balance their two
lines. nav_locales: from /vn/about and
/kr/about the bar and the narrow menu stay in the language.
boundary (899x900, 900x900): no sideways scrolling; the middle fold shows at 900 only; at 900 no
words cross it and Dr. Liu's pool stays 16px or more clear of it.
first_screen (1280x720, 1440x900, 1536x864, 390x844): the written name and the title in the first
screen; from 900px the band starts in it too.

Pictures: scripts/qa/out/about-letter/<size>-NN.png (viewport shots while scrolling).

Usage: python -X utf8 scripts/qa/qa_about.py [base-url] [--only=desktop_and_phone,letter_layout,fold_header,motion,focus,deep_links,languages,languages_layout,nav_locales,boundary,first_screen]
"""

import io
import os
import re
import sys

from PIL import Image, ImageChops
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
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


# Hello in five languages (the fourth promise): the visible words' box, centred on its promise.
GREETINGS_JS = """() => { const li = document.querySelectorAll('[data-promise]')[3];
  const words = [...li.querySelectorAll('[aria-hidden="true"] > [lang]')].map(w => w.getBoundingClientRect()).filter(r => r.width > 0);
  const l = Math.min(...words.map(r => r.left)), r = Math.max(...words.map(r => r.right)), b = li.getBoundingClientRect();
  return { off: Math.round((l + r) / 2 - (b.left + b.width / 2)), lines: new Set(words.map(r => Math.round(r.top))).size }; }"""

# Dr. Liu's pool against the middle fold's right edge (the sheet's ::before).
POOL_FOLD_JS = """() => { const sheet = document.querySelector('[data-sheet]'); const v = getComputedStyle(sheet, '::before');
  const edge = sheet.getBoundingClientRect().left + parseFloat(v.left) + parseFloat(v.width);
  const pool = document.querySelector('[data-pool]').getBoundingClientRect();
  return { clear: Math.round(pool.left - edge), pool: Math.round(pool.left), fold: Math.round(edge) }; }"""


def bar_edge_step(page):
    """The settled bar's paper against the page's just under it, at both edges of the window:
    luminance 4px above and 4px below the header box's bottom. Read with the bar's bottom 120px
    inside the purpose part, where both edges of the window are bare paper (600px down, the band's
    wash runs under the bar's edge at 1440 and reads as a 5-level step that is the painting, not the
    paper). Each reading averages a 5x3 patch, so the paper's own fibre (single pixels vary by about
    3 levels) is not read as a step."""
    page.evaluate(
        """window.scrollTo(0, Math.round(document.getElementById('purpose').getBoundingClientRect().top + scrollY + 120
             - document.querySelector('header').getBoundingClientRect().bottom))"""
    )
    page.wait_for_timeout(1200)
    bottom = round(page.evaluate("document.querySelector('header').getBoundingClientRect().bottom"))
    width = page.evaluate("innerWidth")
    img = Image.open(io.BytesIO(page.screenshot())).convert("RGB")
    px = img.load()

    def lum(x, y):
        cells = [px[x + dx, y + dy] for dx in range(-2, 3) for dy in range(-1, 2)]
        return sum(0.2126 * r + 0.7152 * g + 0.0722 * b for r, g, b in cells) / len(cells)

    steps = [round(abs(lum(x, bottom - 4) - lum(x, bottom + 4)), 1) for x in (5, width - 6)]
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(300)
    return {"step": max(steps), "left_right": steps, "bar_bottom": bottom}


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


# The closing word against the middle fold: where the H's ink ends (column 1053 of the painting's
# 1069, letter-art.ts) and where "ealth" begins, each side's distance from the fold's centre line.
CLOSING_FOLD_JS = """() => { const mid = document.documentElement.clientWidth / 2;
  const chapter = document.querySelector('#closing [data-chapter]');
  const h = chapter.querySelector('img').getBoundingClientRect(); const ink = h.left + h.width * 1053 / 1069;
  const rest = chapter.lastElementChild; const range = document.createRange(); range.selectNodeContents(rest);
  const e = [...range.getClientRects()].filter(r => r.width > 1)[0];
  return { left: +(mid - ink).toFixed(1), right: +(e.left - mid).toFixed(1), ink: Math.round(ink), e: Math.round(e.left), mid }; }"""

# The mockup's arrangement of in (two columns) and Good (from 1200px): the print beside the "in"
# and level with the button at the foot of the words; the rings beside the G; the figures in one
# row, each on one line (its numeral and unit inside its own column).
SPREAD_JS = """() => { const r = (sel) => document.querySelector(sel).getBoundingClientRect();
  const roots = r('#roots'), words = r('#roots [data-label]').top, button = r('#roots a[href]'), inWord = r('#roots [data-chapter]'), mount = r('[data-mount]');
  const g = r('#experience [data-chapter]'), rings = r('#experience [data-rings] img');
  const figs = [...document.querySelectorAll('#experience dl > div')].map(d => { const b = d.getBoundingClientRect();
    const range = document.createRange(); range.selectNodeContents(d.querySelector('dd')); const t = range.getBoundingClientRect();
    return { top: Math.round(b.top), fits: t.right <= b.right + 0.5 && t.left >= b.left - 0.5 }; });
  const pad = parseFloat(getComputedStyle(document.getElementById('roots')).paddingTop) + parseFloat(getComputedStyle(document.getElementById('roots')).paddingBottom);
  return { beside: Math.round(mount.left - inWord.right), level: Math.round(mount.bottom - button.bottom),
           fill: +((button.bottom - words) / (roots.height - pad)).toFixed(2),
           ringsBeside: Math.round(rings.left - g.right), ringsOverlap: rings.top < g.bottom && rings.bottom > g.top,
           rows: new Set(figs.map(f => f.top)).size, fit: figs.every(f => f.fits) }; }"""


def letter_layout(browser):
    for width, height in [(1440, 900), (1280, 800), (1200, 800), (1024, 768), (768, 1024), (390, 844)]:
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
        # Promises side by side: their headings stand level (the dots' pictures are not all the
        # same shape; at their own heights two headings in the row sat 1.7px lower).
        level_rows = page.evaluate(
            """() => { const rows = {};
                 for (const li of document.querySelectorAll('[data-promise]')) {
                   const top = Math.round(li.getBoundingClientRect().top);
                   (rows[top] = rows[top] || []).push(li.querySelector('h3').getBoundingClientRect().top); }
                 return Object.values(rows).map(t => +(Math.max(...t) - Math.min(...t)).toFixed(1)); }"""
        )
        check(f"{tag} the promise headings side by side stand level (0.5px)", max(level_rows) <= 0.5, level_rows)
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
        greet = page.evaluate(GREETINGS_JS)
        check(f"{tag} hello in five languages centred under its promise (8px)", abs(greet["off"]) <= 8, greet)
        if two:
            reach = page.evaluate(POOL_FOLD_JS)
            check(f"{tag} Dr. Liu's pool 16px or more clear of the middle fold", reach["clear"] >= 16, reach)
            level = page.evaluate(
                "Math.round(document.querySelector('#roots [data-label]').getBoundingClientRect().top - document.querySelector('#roots [data-chapter]').getBoundingClientRect().top)"
            )
            check(f"{tag} roots: the words start level with the in (24px)", abs(level) <= 24, level)
            closing = page.evaluate(CLOSING_FOLD_JS)
            check(
                f"{tag} the closing H's ink and its ealth stay outside the middle fold (8px from its centre)",
                closing["left"] >= 8 and closing["right"] >= 8,
                closing,
            )
        if two:
            spread = page.evaluate(SPREAD_JS)
            check(
                f"{tag} in: Dr. Liu's print beside the in, level with the button (48px)",
                spread["beside"] >= 8 and abs(spread["level"]) <= 48,
                spread,
            )
            check(f"{tag} in: the words fill the part (70% or more of its height)", spread["fill"] >= 0.7, spread)
        if width >= 1200:
            check(
                f"{tag} Good: the rings beside the G, the three figures in one row, each on one line",
                spread["ringsBeside"] >= 8 and spread["ringsOverlap"] and spread["rows"] == 1 and spread["fit"],
                spread,
            )
        if width == 1440:
            step = bar_edge_step(page)
            check(f"{tag} no seam where the settled bar meets the page's sides (step 4 or less)", step["step"] <= 4, step)
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
            reach = page.evaluate(POOL_FOLD_JS)
            check("900 Dr. Liu's pool 16px or more clear of the middle fold", reach["clear"] >= 16, reach)
        context.close()


def fold_header(browser):
    """At the top of the page the header is clear over the opening, so a fold that started at the
    sheet's top ran behind it, through the logo. Read the fold's own top against the header's box,
    then hide the header and compare the paper down the page's middle (the fold's 16px) inside the
    header's box with the paper 40-60px to each side (column averages, so the paper's fibre is not
    read as a fold)."""
    for width, height in [(1024, 768), (1440, 900), (1536, 864)]:
        tag = f"{width}x{height}"
        context, page, response, errors, failed = open_page(browser, width, height, reduced=True)
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(300)
        geo = page.evaluate(
            """() => { const sheet = document.querySelector('[data-sheet]'); const v = getComputedStyle(sheet, '::before');
                 return { top: Math.round(sheet.getBoundingClientRect().top + parseFloat(v.top)),
                          header: Math.round(document.querySelector('header').getBoundingClientRect().bottom),
                          mid: Math.round(document.documentElement.clientWidth / 2) }; }"""
        )
        check(f"{tag} the middle fold starts under the header's box", geo["top"] >= geo["header"], geo)
        page.add_style_tag(content="header { visibility: hidden !important; }")
        page.wait_for_timeout(300)
        img = Image.open(io.BytesIO(page.screenshot())).convert("L")
        px = img.load()
        bottom, mid = geo["header"], geo["mid"]

        def column(x):
            return sum(px[x, y] for y in range(0, bottom)) / bottom

        beside = [column(x) for x in list(range(mid - 60, mid - 40)) + list(range(mid + 40, mid + 60))]
        paper = sum(beside) / len(beside)
        worst = max(abs(column(x) - paper) for x in range(mid - 8, mid + 8))
        check(
            f"{tag} nothing of the middle fold inside the header's box (2 levels or less)",
            worst <= 2,
            {"worst": round(worst, 1), "header_bottom": bottom},
        )
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


def wait_until(page, expression, timeout=10000):
    """True once the page's expression holds; False when it never does (the checks then report it)."""
    try:
        page.wait_for_function(expression, timeout=timeout)
        return True
    except PlaywrightTimeoutError:
        return False


BAND_BOX_JS = """() => { const r = document.querySelector('[data-band]').getBoundingClientRect();
  const top = Math.max(r.top, 0), bottom = Math.min(r.bottom, innerHeight);
  return { x: 0, y: top, width: innerWidth, height: bottom - top }; }"""


def band_ink(page):
    """How many pixels of the band's box differ when the band is hidden: 0 when nothing of it shows."""
    box = page.evaluate(BAND_BOX_JS)
    shown = Image.open(io.BytesIO(page.screenshot(clip=box))).convert("L")
    page.evaluate("document.querySelector('[data-band]').style.visibility = 'hidden'")
    hidden = Image.open(io.BytesIO(page.screenshot(clip=box))).convert("L")
    return sum(ImageChops.difference(shown, hidden).histogram()[9:])


WRITE_TIMES = (900, 1000, 1100, 1200, 1300, 1400)


def front_banding(page):
    """Seek the written name through the middle of its stroke and read the front over the H's right
    stem. For each pixel, alpha = how much of the ink has come through = (paper - frame) / (paper -
    ink): a multiplied painting is linear in it, so the painting's own texture drops out. At each
    moment the stem column whose front is half through is read from the top of the stem to its
    foot, and the times its alpha swings between under 0.35 and over 0.65 are counted. A soft front
    changes slowly down a stem (0 to 2 swings); venetian blinds change every few pixels (a dozen)."""
    box = page.evaluate(
        """() => { const r = document.querySelector('[data-word] img').getBoundingClientRect();
             return { x: Math.round(r.left), y: Math.round(r.top), width: Math.round(r.width), height: Math.round(r.height) }; }"""
    )
    page.evaluate(
        """() => { const a = document.getAnimations().find(x => (x.animationName || '').includes('write'));
             a.pause(); window.__write = a; }"""
    )

    def grab(ms):
        page.evaluate(f"window.__write.currentTime = {ms}")
        page.wait_for_timeout(150)
        return Image.open(io.BytesIO(page.screenshot(clip=box))).convert("L")

    paper, ink = grab(0), grab(3000)
    w, h = paper.size
    p_px, i_px = paper.load(), ink.load()
    # The H's right stem: of the right-hand columns, the ones with the most ink.
    counts = {x: sum(1 for y in range(h) if p_px[x, y] - i_px[x, y] > 60) for x in range(int(w * 0.84), w)}
    top = max(counts.values())
    stem = [x for x, c in counts.items() if c >= 0.6 * top]
    readings = []
    for ms in WRITE_TIMES:
        frame = grab(ms).load()
        best = None
        for x in stem:
            rows = [y for y in range(h) if p_px[x, y] - i_px[x, y] > 60]
            alphas = [min(max((p_px[x, y] - frame[x, y]) / (p_px[x, y] - i_px[x, y]), 0), 1) for y in rows]
            mean = sum(alphas) / len(alphas)
            if best is None or abs(mean - 0.5) < abs(best[1] - 0.5):
                best = (x, mean, alphas)
        x, mean, alphas = best
        if abs(mean - 0.5) > 0.12:
            continue
        state, swings = None, 0
        for a in alphas:
            now = "low" if a < 0.35 else "high" if a > 0.65 else state
            if state is not None and now != state:
                swings += 1
            state = now
        readings.append({"ms": ms, "column": x, "mean_alpha": round(mean, 2), "swings": swings})
    return readings


def motion(browser):
    # Reduced motion: complete and still, from the first paint to the last.
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    page = context.new_page()
    errors, wipe_requests = [], []
    page.on("console", lambda m: errors.append(m.text) if m.type in ("error", "warning") and counted(m) else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("request", lambda r: wipe_requests.append(r.url) if "wipe-v1" in r.url else None)
    page.goto(f"{BASE}/about", wait_until="networkidle", timeout=120000)
    page.evaluate("document.fonts.ready.then(() => true)")
    page.wait_for_timeout(1200)
    scroll_through(page)
    still = page.evaluate(
        """() => ({ waiting: document.querySelectorAll('[data-arrive]').length,
             blooms: [...document.querySelectorAll('[data-bloom]')].filter(e => e.dataset.bloom !== 'done').length,
             dots: [...document.querySelectorAll('[data-dot]')].map(d => getComputedStyle(d).opacity),
             word: getComputedStyle(document.querySelector('[data-word] img')).animationName,
             masks: [...document.querySelectorAll('[data-chapter] img, [data-word] img')].map(i => getComputedStyle(i).maskImage).filter(m => m !== 'none'),
             running: document.getAnimations().filter(a => { const t = a.effect && a.effect.target;
               return t && t.closest && t.closest('main') && !t.closest('[class*=greetings]'); }).length })"""
    )
    check("reduced motion: no letter waits", still["waiting"] == 0, still)
    check("reduced motion: every bloom done", still["blooms"] == 0, still)
    check("reduced motion: the gold dots are up", still["dots"] and all(float(o) == 1 for o in still["dots"]), still)
    check("reduced motion: the name is still and nothing is masked", still["word"] == "none" and not still["masks"], still)
    check("reduced motion: nothing moves", still["running"] == 0, still)
    check("reduced motion: nothing logged (no preload left unused)", not errors, errors[:3])
    check("reduced motion: the wipe mask is never fetched", not wipe_requests, wipe_requests[:2])
    context.close()

    # Reduced motion is complete from the first paint: before any script runs (the scripts are
    # blocked here, so the server-marked band stays "waiting"), the band is crisp and shown, not
    # the kit's blur(5px). The band is the one painting the server marks.
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    page = context.new_page()
    page.route("**/*.js", lambda route: route.abort())
    page.goto(f"{BASE}/about", wait_until="load", timeout=120000)
    first_paint = page.evaluate(
        """() => { const b = document.querySelector('[data-band]'), s = getComputedStyle(b);
             return { bloom: b.dataset.bloom, filter: s.filter, opacity: s.opacity }; }"""
    )
    check(
        "reduced motion: before any script the band is crisp and shown",
        first_paint["bloom"] == "waiting" and first_paint["filter"] == "none" and first_paint["opacity"] == "1",
        first_paint,
    )
    context.close()

    # The wipe mask is found only from the stylesheet, so the page preloads it, for motion
    # visitors only (a reduced-motion visit never uses it and would log an unused preload).
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="no-preference")
    html = context.request.get(f"{BASE}/about").text()
    context.close()
    link = re.search(r"<link\b[^>]*wipe-v1\.png[^>]*>", html)
    tag = link.group(0) if link else ""
    check(
        "motion: the wipe mask is preloaded, for motion visitors only",
        'rel="preload"' in tag
        and 'as="image"' in tag
        and 'crossorigin="anonymous"' in tag
        and 'media="(prefers-reduced-motion: no-preference)"' in tag,
        tag or "no <link> for wipe-v1.png in the page",
    )
    check("motion: the preload sits in the head", bool(tag) and tag in html.split("</head>")[0], tag or "none")

    # The bloom hold: the band waits invisible, and nothing of it shows before its bloom starts.
    # (Chrome drops a mask layer of no size, so the kit alone leaves a waiting painting whole and
    # blurred; the band then hung there, vanished in one frame and spread out again.)
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="no-preference")
    page = context.new_page()
    page.goto(f"{BASE}/about", wait_until="domcontentloaded", timeout=120000)
    waiting = page.evaluate(
        """() => { const b = document.querySelector('[data-band]'); return [b.dataset.bloom, getComputedStyle(b).opacity]; }"""
    )
    check("motion: the band waits invisible", waiting[1] == "0", waiting)
    reached = wait_until(page, "document.querySelector('[data-band]').dataset.bloom === 'in'")
    held = page.evaluate("getComputedStyle(document.querySelector('[data-band]')).opacity")
    changed = band_ink(page)
    still_holding = page.evaluate(
        "document.getAnimations().some(a => (a.animationName || '').includes('bloom-hold'))"
    )
    check("motion: the band is invisible through its hold", reached and held == "0", [reached, held])
    check(
        "motion: nothing of the band shows before its bloom (no pop, then vanish)",
        still_holding and changed <= 20,
        {"changed_pixels": changed, "hold_still_running": still_holding},
    )
    context.close()

    # The wipe front over a stem is a soft ink front, not venetian blinds: seek the name to the
    # middle of its stroke and read the front down the H's stem.
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="no-preference")
    page = context.new_page()
    page.goto(f"{BASE}/about", wait_until="networkidle", timeout=120000)
    page.evaluate("document.fonts.ready.then(() => true)")
    readings = front_banding(page)
    check("motion: the wipe front crosses the H's stem", bool(readings), readings)
    check(
        "motion: no regular banding on the front over the H stem (3 light/dark swings or fewer)",
        bool(readings) and max(r["swings"] for r in readings) <= 3,
        readings,
    )
    context.close()

    # With motion: the name is written in one breath, then its gold dot comes up.
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="no-preference")
    page = context.new_page()
    mask_requests = []
    page.on("request", lambda r: mask_requests.append(r.url) if "wipe-v1" in r.url else None)
    page.goto(f"{BASE}/about", wait_until="domcontentloaded", timeout=120000)
    # The page's stylesheet first (the dot's delay is 1.8s, so this still reads it waiting). If the
    # name has no animation the wait runs out and the checks below report it, instead of a traceback.
    wait_until(page, "getComputedStyle(document.querySelector('[data-word] img')).animationName !== 'none'", 5000)
    early = page.evaluate(
        """() => { const i = getComputedStyle(document.querySelector('[data-word] img'));
             const d = getComputedStyle(document.querySelector('[data-word] [data-dot]'));
             return { name: i.animationName, duration: i.animationDuration,
                      dot: d.opacity, dotDelay: parseFloat(d.animationDelay) }; }"""
    )
    check("motion: the name is written (its animation, one breath)", "write" in early["name"] and early["duration"] == "2.4s", early)
    check("motion: the gold dot waits for the name", float(early["dot"]) < 0.5 and early["dotDelay"] >= 1.7, early)
    # The page's own clock decides when it is done (the band 3.4s plus its delay after it starts,
    # the dot at its delay plus 1.2s), not a fixed wait.
    wait_until(page, "document.querySelector('[data-band]').dataset.bloom === 'done'")
    wait_until(
        page, "parseFloat(getComputedStyle(document.querySelector('[data-word] [data-dot]')).opacity) === 1"
    )
    late = page.evaluate(
        """() => ({ mask: getComputedStyle(document.querySelector('[data-word] img')).maskPosition,
             dot: getComputedStyle(document.querySelector('[data-word] [data-dot]')).opacity,
             band: document.querySelector('[data-band]').dataset.bloom })"""
    )
    check("motion: the name ends whole", late["mask"].startswith("0%"), late)
    check("motion: then its gold dot is up", float(late["dot"]) == 1, late)
    check("motion: the band has bloomed", late["band"] == "done", late)
    check(
        "motion: the wipe mask is fetched once (the preload is the one the stylesheet uses)",
        len(mask_requests) == 1,
        mask_requests,
    )

    # A chapter letter out of the window waits, is written as it comes in, and ends unmasked.
    state = lambda: page.evaluate(
        """() => { const c = document.querySelector('[data-chapter="G"]');
             return [c.dataset.arrive ?? null, getComputedStyle(c.querySelector('img')).maskImage]; }"""
    )
    first = state()
    check("motion: the G waits out of the window", first[0] == "waiting", first)
    page.evaluate(
        """() => { const c = document.querySelector('[data-chapter="G"]');
             window.scrollTo(0, c.getBoundingClientRect().top + window.scrollY - innerHeight / 2); }"""
    )
    page.wait_for_timeout(700)
    second = state()
    check("motion: the G is being written as it comes in", second[0] == "in" and second[1] != "none", second)
    page.wait_for_timeout(3200)
    third = state()
    check("motion: the G ends written and unmasked", third[0] == "done" and third[1] == "none", third)
    context.close()

    # JavaScript off: the written name still appears (its animation is CSS only). Read from pixels:
    # the word's band of the first screen holds ink.
    context = browser.new_context(viewport={"width": 1440, "height": 900}, java_script_enabled=False)
    page = context.new_page()
    page.goto(f"{BASE}/about", wait_until="load", timeout=120000)
    page.wait_for_timeout(4500)
    shot = Image.open(io.BytesIO(page.screenshot(clip={"x": 360, "y": 110, "width": 720, "height": 330}))).convert("L")
    dark = sum(shot.histogram()[:90]) / (shot.width * shot.height)
    check("JavaScript off: the written name is visible", dark >= 0.02, round(dark, 4))
    band = page.evaluate(
        """() => { const b = document.querySelector('[data-band]'), s = getComputedStyle(b);
             return { bloom: b.dataset.bloom, filter: s.filter, opacity: s.opacity }; }"""
    )
    check(
        "JavaScript off: the band is crisp and shown",
        band["bloom"] == "waiting" and band["filter"] == "none" and band["opacity"] == "1",
        band,
    )
    context.close()


def settle(page, still=300, limit=5000):
    """Wait for a smooth scroll to end: scrollY unchanged for `still` ms (at most `limit` ms)."""
    last, held, waited = None, 0, 0
    while held < still and waited < limit:
        page.wait_for_timeout(50)
        waited += 50
        y = page.evaluate("window.scrollY")
        held = held + 50 if y == last else 0
        last = y
    return last


# Where a deep link lands: the part's first content (its chapter word or its label, whichever is
# higher) 0-64px under the header's bottom (measured at run time), and its heading fully in the
# window below the bar.
LANDING_JS = """(id) => {
  const s = document.getElementById(id);
  const tops = [...s.querySelectorAll('[data-chapter], [data-label]')].filter(e => e.offsetParent).map(e => e.getBoundingClientRect().top);
  const head = document.getElementById(id + '-title').getBoundingClientRect();
  const bar = document.querySelector('header').getBoundingClientRect();
  return { scrollY: Math.round(window.scrollY), bar: Math.round(bar.bottom), first: Math.round(Math.min(...tops)),
           headTop: Math.round(head.top), headBottom: Math.round(head.bottom), win: window.innerHeight };
}"""


def deep_links(browser):
    # Each size is one browser context: a first visit warms the fonts into the cache (a cold dev
    # font can reflow the page after the browser has aimed its scroll), then every deep link is a
    # fresh load.
    for width, height in [(1440, 900), (1024, 768), (768, 1024), (390, 844), (360, 780)]:
        context = browser.new_context(viewport={"width": width, "height": height}, reduced_motion="no-preference")
        warm = context.new_page()
        warm.goto(f"{BASE}/about", wait_until="networkidle", timeout=120000)
        warm.evaluate("document.fonts.ready.then(() => true)")
        warm.close()
        for anchor in ["purpose", "roots", "experience", "promise"]:
            page = context.new_page()
            page.goto(f"{BASE}/about#{anchor}", wait_until="networkidle", timeout=120000)
            page.evaluate("document.fonts.ready.then(() => true)")
            settle(page)
            at = page.evaluate(LANDING_JS, anchor)
            gap = at["first"] - at["bar"]
            check(
                f"{width}x{height} /about#{anchor}: lands 0-64px under the header ({gap}px), heading in the window",
                at["scrollY"] > 0 and 0 <= gap <= 64 and at["headTop"] >= at["bar"] and at["headBottom"] <= at["win"],
                at,
            )
            page.close()
        context.close()


def languages(browser):
    english = [line for line in LOCKED if len(line) > 24]
    for lang in ["kr", "jp", "cns", "vn"]:
        context, page, response, errors, failed = open_page(browser, 1440, 900, path=f"/{lang}/about", reduced=True)
        check(f"{lang} answers 200", response.status == 200, response.status)
        h1 = page.evaluate("document.querySelector('h1').getAttribute('aria-label')")
        check(f"{lang} h1 stays English", h1 == "Be in Good Health.", h1)
        chapters = page.evaluate("[...document.querySelectorAll('[data-chapter]')].map(c => [c.dataset.chapter, c.lang, c.textContent.trim()])")
        check(
            f"{lang} the chapter words stay English",
            chapters == [["B", "en", "e"], ["i", "en", "n"], ["G", "en", "ood"], ["H", "en", "ealth"]],
            chapters,
        )
        text = page.evaluate("document.querySelector('main').innerText")
        left = [line for line in english if line in text]
        check(f"{lang} no English sentence left", not left, left[:3])
        alt = page.evaluate("document.querySelector('[data-rings] img').alt")
        check(f"{lang} the rings' description is translated", alt and not alt.startswith("Tree rings"), alt)
        check(f"{lang} no console errors or warnings", not errors, errors[:3])
        page.screenshot(path=os.path.join(OUT, f"{lang}-opening.png"))
        context.close()


# Line breaks and margins, read from the page itself (every line of every text block, by the
# position of each character). A line with one letter, or a line that starts with closing
# punctuation (and, in Japanese, a small kana or "ー"), is a bad break.
BREAKS_JS = r"""(lang) => {
  const closing = new Set([...'。、，．，,.;:!?！？：；）)」』】〕》〉”’…%']);
  const small = new Set([...'ぁぃぅぇぉっゃゅょゎゕゖァィゥェォッャュョヮヵヶー々']);
  const letter = /[\p{L}\p{N}]/u;
  const out = [];
  const els = [...document.querySelectorAll('main h2, main h3, main p, main dt')]
    .filter(e => e.offsetParent && !e.closest('[class*=greetings]'));
  for (const el of els) {
    const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    const chars = [];
    let n;
    while ((n = walker.nextNode())) {
      const t = n.textContent;
      for (let i = 0; i < t.length; i++) {
        if (/\s/.test(t[i])) continue;
        const r = document.createRange(); r.setStart(n, i); r.setEnd(n, i + 1);
        const rects = r.getClientRects(); if (!rects.length) continue;
        chars.push({ c: t[i], mid: (rects[0].top + rects[0].bottom) / 2 });
      }
    }
    if (!chars.length) continue;
    const lines = []; let cur = [chars[0]];
    for (let i = 1; i < chars.length; i++) {
      if (Math.abs(chars[i].mid - cur[cur.length - 1].mid) > 9) { lines.push(cur); cur = [chars[i]]; } else cur.push(chars[i]);
    }
    lines.push(cur);
    if (lines.length < 2) continue;
    const text = el.textContent.trim().slice(0, 24);
    lines.forEach((line, k) => {
      const s = line.map(x => x.c).join('');
      if (k > 0 && (closing.has(line[0].c) || (lang === 'jp' && small.has(line[0].c)))) out.push(['line starts with ' + line[0].c, text, s.slice(0, 16)]);
      if (line.filter(x => letter.test(x.c)).length <= 1) out.push(['one character on a line', text, s.slice(0, 16)]);
    });
  }
  return out;
}"""

# Every word of the page stays inside its column: none crosses the page's side margins (a phrase
# too wide for its column once did, in Japanese on a phone).
MARGINS_JS = r"""() => {
  const out = [];
  for (const el of document.querySelectorAll('main h1, main h2, main h3, main p, main dt, main dd, main a, main button')) {
    if (!el.offsetParent || el.closest('figure')) continue;
    const wrap = el.closest('[class*=wrap]'); if (!wrap) continue;
    const wb = wrap.getBoundingClientRect(); const cs = getComputedStyle(wrap);
    const left = wb.left + parseFloat(cs.paddingLeft), right = wb.right - parseFloat(cs.paddingRight);
    const range = document.createRange(); range.selectNodeContents(el);
    for (const r of range.getClientRects()) {
      if (r.width && (r.right > right + 1 || r.left < left - 1)) { out.push([el.textContent.trim().slice(0, 18), Math.round(r.left), Math.round(r.right), Math.round(left), Math.round(right)]); break; }
    }
  }
  return out;
}"""


# No heading phrase is broken across lines (Japanese and Chinese, on a phone and at 900px, where the
# words column is narrowest). What a heading keeps whole is a phrase: in Chinese the words between
# two punctuation marks (word-break: keep-all; the translations put a comma where a line may end),
# in Japanese the browser's own phrases (word-break: auto-phrase), which it breaks inside only when
# a phrase is wider than the line. The page's rules size the headings so that a phrase of up to
# about 12 characters fits its column; without them a heading breaks inside one ("主力フォーミュラ /
# は、", "核心配 / 方，", "那一部 / 分").
#   Chinese: the real lines are read against the phrases of a 1px-wide copy of the heading (each
#   line of it is one phrase); no phrase of 12 characters or fewer may stand on two lines.
#   Japanese: punctuation is no phrase boundary ("目に見えないひとつ。" is rightly broken after
#   "目に"), and a 1px copy breaks inside every phrase, so the copy is set as wide as its longest
#   phrase (width: min-content) and that width must fit the words column (when it is 12em or less).
PHRASES_JS = r"""(lang) => {
  const readChars = (root) => {
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    const out = []; let n;
    while ((n = walker.nextNode())) {
      const t = n.textContent;
      for (let i = 0; i < t.length; i++) {
        if (/\s/.test(t[i])) continue;
        const r = document.createRange(); r.setStart(n, i); r.setEnd(n, i + 1);
        const rects = r.getClientRects(); if (!rects.length) continue;
        out.push({ c: t[i], mid: (rects[0].top + rects[0].bottom) / 2 });
      }
    }
    return out;
  };
  const split = []; let examined = 0;
  for (const h of document.querySelectorAll('main h2[id$="-title"]')) {
    if (!h.offsetParent) continue;
    const name = h.textContent.trim().slice(0, 12);
    const probe = h.cloneNode(true);
    probe.removeAttribute('id');
    probe.style.cssText = 'position:absolute;left:0;top:0;max-width:none;margin:0;visibility:hidden;overflow-wrap:normal;line-break:strict;text-wrap:wrap;word-break:'
      + (lang === 'jp' ? 'auto-phrase;width:min-content' : 'keep-all;width:1px');
    h.after(probe);
    if (lang === 'jp') {
      const longest = probe.getBoundingClientRect().width;
      probe.remove();
      const box = h.parentElement, cs = getComputedStyle(box);
      const column = box.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
      if (longest / parseFloat(getComputedStyle(h).fontSize) > 12) continue;
      examined++;
      if (longest > column + 0.5) split.push([name, 'longest phrase ' + Math.round(longest) + 'px, column ' + Math.round(column) + 'px']);
      continue;
    }
    const real = readChars(h), cut = readChars(probe);
    probe.remove();
    if (cut.length !== real.length) { split.push([name, 'phrases not read']); continue; }
    let start = 0;
    for (let i = 1; i <= cut.length; i++) {
      if (i < cut.length && Math.abs(cut[i].mid - cut[i - 1].mid) <= 9) continue;
      const phrase = real.slice(start, i); start = i;
      if (phrase.length > 12) continue;
      examined++;
      const mids = phrase.map(x => x.mid);
      if (Math.max(...mids) - Math.min(...mids) > 9) split.push([phrase.map(x => x.c).join(''), 'split over lines', name]);
    }
  }
  return { split, examined };
}"""


def languages_layout(browser):
    """Each language at desktop, tablet and phone sizes: no word crosses the side margins, and
    in Korean, Japanese, Chinese and Vietnamese no bad line break. Japanese and Chinese also at
    900x900, and on a phone and at 900px no heading phrase is split across lines."""
    for lang in ["en", "kr", "jp", "cns", "vn"]:
        sizes = [(1440, 900), (1024, 768), (768, 1024), (390, 844), (360, 780)]
        if lang in ("jp", "cns"):
            sizes.append((900, 900))
        for width, height in sizes:
            tag = f"{lang} {width}x{height}"
            path = "/about" if lang == "en" else f"/{lang}/about"
            context, page, response, errors, failed = open_page(browser, width, height, path=path, reduced=True)
            over = page.evaluate(MARGINS_JS)
            check(f"{tag} words inside the margins", not over, over[:3])
            if width >= 900:
                crossing = page.evaluate(CREASE_JS)
                check(f"{tag} no words cross the middle fold", not crossing, crossing[:3])
            if lang != "en":
                bad = page.evaluate(BREAKS_JS, lang)
                check(f"{tag} no bad line break", not bad, bad[:3])
            if lang in ("jp", "cns") and width in (390, 360, 900):
                phrases = page.evaluate(PHRASES_JS, lang)
                check(
                    f"{tag} no heading phrase is broken across lines ({phrases['examined']} read)",
                    phrases["examined"] > 0 and not phrases["split"],
                    phrases,
                )
            if lang == "vn" and width == 390:
                # "Khám phá sản phẩm của chúng tôi" takes two lines on a phone; they must be even
                # (an earlier selector matched nothing and left 239px over 91px).
                pills = page.evaluate(
                    """[...document.querySelectorAll('main [class*=actions] a, main [class*=actions] button')].map(e => {
                         const r = document.createRange(); r.selectNodeContents(e);
                         const widths = {}; for (const x of r.getClientRects()) if (x.width > 4) widths[Math.round(x.top)] = (widths[Math.round(x.top)] || 0) + x.width;
                         return { wrap: getComputedStyle(e).textWrap, widths: Object.values(widths).map(Math.round) }; })"""
                )
                check(f"{tag} closing pills balance their lines (computed text-wrap)", len(pills) == 2 and all(p["wrap"] == "balance" for p in pills), pills)
                two = [p["widths"] for p in pills if len(p["widths"]) == 2]
                check(f"{tag} the pill's two lines are even", bool(two) and all(min(w) / max(w) >= 0.6 for w in two), pills)
            context.close()


# The menu bar keeps the visitor's language off the homepage: from /<locale>/about every link of
# the bar and of the narrow window's menu stays in that locale, and following them (a click, as a
# visitor would) lands on the localized page.
NAV_LINKS_JS = """() => {
  const n = document.querySelector('#site-navigation');
  const sheet = document.querySelector('[data-nav-sheet]');
  const own = (root) => [...root.querySelectorAll('a')].map(a => a.getAttribute('href')).filter(h => h.startsWith('/'));
  return { bar: own(n), menu: own(sheet), mark: n.querySelector('[data-nav-logo]').getAttribute('href'),
           current: [...n.querySelectorAll('[aria-current=page]')].map(a => a.getAttribute('href')),
           menuCurrent: [...sheet.querySelectorAll('[aria-current=page]')].map(a => a.getAttribute('href')) };
}"""


def nav_locales(browser):
    for locale in ["vn", "kr"]:
        tag = f"{locale} nav"
        context, page, response, errors, failed = open_page(browser, 1440, 900, path=f"/{locale}/about")
        links = page.evaluate(NAV_LINKS_JS)
        own = [h for h in links["bar"] + links["menu"] if h != links["mark"]]
        stray = [h for h in own if not h.startswith(f"/{locale}/") and not h.startswith(f"/{locale}#")]
        check(f"{tag}: every bar and menu link stays in the language", own and not stray and links["mark"] == f"/{locale}", [links["mark"], stray])
        check(
            f"{tag}: About is the current page",
            links["current"] == [f"/{locale}/about"] and links["menuCurrent"] == [f"/{locale}/about"],
            links,
        )
        # Clicks: the first product, "Explore our products.", a Science part, and the mark.
        for trigger, pick, want in [
            ("products", "first", f"/{locale}/products/nuricell"),
            ("products", "last", f"/{locale}#products"),
            ("science", "nth1", f"/{locale}/science#health"),
        ]:
            page.goto(f"{BASE}/{locale}/about", wait_until="networkidle", timeout=120000)
            page.click(f'[data-nav-trigger="{trigger}"]')
            page.wait_for_timeout(1200)
            items = page.locator(f'[data-nav-panel="{trigger}"] a')
            item = items.first if pick == "first" else items.last if pick == "last" else items.nth(1)
            item.click()
            page.wait_for_url(f"**{want}", timeout=30000)
            if want.endswith("#products"):
                # The language's homepage, scrolled to its products section.
                settle(page)
                home = page.evaluate(
                    """() => { const r = document.getElementById('products')?.getBoundingClientRect();
                               return { url: location.pathname + location.hash, lang: document.documentElement.lang,
                                        inView: !!r && r.top < innerHeight && r.bottom > 0, top: r ? Math.round(r.top) : null }; }"""
                )
                check(
                    f"{tag}: Explore our products. goes to the {locale} homepage's products section",
                    home["url"].replace("/#", "#") == want and home["inView"] and home["lang"] != "en",
                    home,
                )
            else:
                check(f"{tag}: {trigger} link lands on {want}", page.url.endswith(want), page.url)
        page.goto(f"{BASE}/{locale}/about", wait_until="networkidle", timeout=120000)
        page.click("[data-nav-logo]")
        page.wait_for_url(f"**/{locale}", timeout=30000)
        check(f"{tag}: the mark goes to the language's homepage", page.url.rstrip("/").endswith(f"/{locale}"), page.url)
        check(f"{tag}: no console errors or warnings", not errors, errors[:3])
        context.close()
    # The phone menu, once: a product from the menu's Products part.
    context, page, response, errors, failed = open_page(browser, 390, 844, path="/vn/about")
    page.click("[data-nav-menu-button]")
    page.wait_for_timeout(1000)
    page.click('[data-nav-sheet-toggle="products"]')
    page.wait_for_timeout(1000)
    page.locator("[data-nav-sheet] a[href*='/products/']").first.click()
    page.wait_for_url("**/vn/products/nuricell", timeout=30000)
    check("vn nav: the phone menu's product link lands on /vn/products/nuricell", page.url.endswith("/vn/products/nuricell"), page.url)
    context.close()


# --only=letter_layout,boundary runs just those groups (while working on one thing); the full run is the gate.
GROUPS = [desktop_and_phone, letter_layout, fold_header, motion, focus, deep_links, languages, languages_layout, nav_locales, boundary, first_screen]
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

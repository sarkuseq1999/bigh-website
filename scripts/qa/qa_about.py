"""QA for the About page in the Ink & Gold look (October 5, 2026; Mo approved the mockup
reference/ink-pages/mockups/about.jpg).

At 1440x900 and 390x844, then the opening at 1280x720, 1536x1000, 1024x768, 900x1100, 768x1024
and 360x780: answers 200; no console errors or warnings (except the built site's link-prefetch
CSS preload note, see PREFETCH_CSS); no failed requests; one h1, English
"Be in Good Health." with lang="en"; every locked line is on the page; no WebGL canvas in the
page; every painting multiplies onto the paper and the page wears the paper texture; the menu bar
("Inscription", #site-navigation) marks About as the current page, in the bar and in the narrow
window's menu; it has no Home link (the mark goes home) and its Products drop-down holds the five
product pages and "Explore our products." (/#products); no sideways scrolling;
text at least 15px and navigation at least 18px; links and buttons in the page at least 48px tall;
the cell sits in the first screen and never touches the title or the opening words; four
stations; the Support and Ask BiGH Science sheets open, close and hand focus back.
Desktop only (900px and wider): the brush layer draws the page layout, and its ink passes each
station's leader. Review focus: each part's deep link (/about#purpose, #roots, #experience, #promise) lands its heading
(its station, where a print stands over the words) 0-48px under the header at 1440, 1024, 768 and 390;
Skip to content puts focus
at the words; with pictures blocked every heading and paragraph is visible.
Reduced motion: every painting shown, the gold leaf fully up, the whole line drawn.
Other languages (kr, jp, cns, vn): 200, no console errors, the h1 stays English, no English
source sentence left visible; in Vietnamese the brush line still meets every station after the
late font arrives. Every language (and English) at 1440x900, 1024x768, 768x1024, 390x844 and
360x780: no word crosses the page's side margins; in Korean, Japanese, Chinese and Vietnamese no
line holds one character and none starts with closing punctuation (or, in Japanese, a small kana).
Vietnamese at 390: the closing pills' text-wrap is balance and the wrapped pill's two lines are even.
Resizing from 1440 to 820 wide redraws the brush line for one column.

Pictures: scripts/qa/out/about-ink/<size>-NN.png (viewport shots while scrolling).

Finish pass (October 5, 2026): the title on two lines at every opening size; a tablet held upright
(721-899 px) keeps the cell beside a large title (and wider than its line), the next block's heading
in the first window, and the pause's inkstone small; every station on one line at 1440 and
1536; each promise rule lands at least 5px thick; Japanese strict line breaks stay in the page's
words, not the header and footer.

Finish review round (October 5, 2026): the sweep out of the cell is a curve (not a chord) and loaded;
the margin's stroke is loaded and thickens and thins; the light band crosses the cell's leaf rather
than resting on it; the cell at the comp's scale, near the title, low, in the first screen, no letter
over it; the name's other letters an ink-wash grey (3:1 on paper, 3.5:1 against the initials); the
tablet cell 55-62% wide, off the right edge, both gold folds in view.

Second review round (October 5, 2026): the brush holds 3px or more of real ink (alpha over 140)
on the sweep's run and down the margin between reloads; on a phone no brush ink within 12px of the
painting; on a tablet the stroke out of the cell ends at the tip of the first station's leader and
touches no words; the promise heading beside the list, level with its first rule, the list's right
edge on the figures'.

Third review round (October 5, 2026): the line starts clear of the painting (no brush ink within
12px of its ink, outer wash included) with a loaded landing (3px of real ink over its first 30px) at
every two-column and tablet size; just above the stacking breakpoint the promises keep a reading
measure (columns 250px or more, titles on one line, text in three lines or fewer).

Fourth review round (October 5, 2026): the line sets down beside the cell's foot already travelling
left (level or drifting down, never climbing) with the painting above its end, not ahead of it (the
stroke's aim 45 degrees or more off the painting's nearest ink); on a tablet no tick under the cell
(the first 60px level and left); the head is a round, pressed tip, wider than the run, thinning
into it.

Menu bar (October 5, 2026, the Inscription bar merged from main): from /vn/about and /kr/about
every link of the bar and of the narrow window's menu stays in that language, About is the current
page, and clicks on a product, "Explore our products.", a Science part, the mark and the phone
menu's first product land on the localized pages ("Explore our products." on that language's
homepage, its products section in view).

Usage: python -X utf8 scripts/qa/qa_about.py [base-url] [--only=openings,finish,round2,round3,round4,round5,line_and_focus,deep_links,languages,nav_locales]
"""

import math
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


# A second warning is not counted, and only on the dev server: Next's dev-only LCP note for the
# cell's painting. On /about that one file is both the opening's cell (priority: eager and
# preloaded) and the menu bar's Science painting (lazy until the visitor reaches for the bar). Next's
# dev check (next/dist/shared/lib/get-img-props.js) keys images by their src URL, and both render the
# same one (/_next/image?url=...mito.webp&w=3840&q=75), so whichever re-rendered last speaks for
# both and the cell's LCP is reported as lazy (October 5, 2026, merging the Inscription bar; seen
# intermittently on /about, /vn/about, /kr/about). The built site never logs it. Only this exact
# message for mito.webp is ignored, and desktop_and_phone checks that the cell really is eager and
# preloaded.
DEV_LCP_MITO = re.compile(
    r'^Image with src "/images/home-v2/ink/mito\.webp" was detected as the Largest Contentful Paint \(LCP\)\.'
)


def counted(message):
    if message.type != "warning":
        return True
    return not (PREFETCH_CSS.match(message.text) or DEV_LCP_MITO.match(message.text))


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


# The opening section (its words: the kicker, the title and the lead) and whether the cell sits in
# the first screen and clear of every one of them (boxes, not ink: no word ever over the painting).
OPENING = 'section[aria-labelledby="about-title"]'
CELL_JS = """() => { const c = document.querySelector('[data-brush="about-cell"] img').getBoundingClientRect();
  const words = [...document.querySelectorAll('OPENING h1, OPENING p')].map(e => e.getBoundingClientRect());
  const hit = words.some(w => !(c.right <= w.left || c.left >= w.right || c.bottom <= w.top || c.top >= w.bottom));
  return { top: Math.round(c.top), inFirst: c.top < innerHeight, hit }; }""".replace("OPENING", OPENING)


def stations_met(page):
    """Whether the brush line's ink passes each station's leader (some ink within 28px right of the
    label). The brush layer keeps only the tiles near the window drawn (and a tall page, such as the
    Vietnamese one, has stations several windows down), so each station is brought into the window
    before its row is read. Needs the whole line drawn (reduced motion)."""
    count = page.evaluate("document.querySelectorAll('[data-station]').length")
    met = []
    for i in range(count):
        page.evaluate(
            f"""() => {{ const s = document.querySelectorAll('[data-station]')[{i}];
                 window.scrollTo(0, s.getBoundingClientRect().top + window.scrollY - innerHeight / 2); }}"""
        )
        page.wait_for_timeout(500)
        met.append(
            page.evaluate(
                f"""() => {{ const s = document.querySelectorAll('[data-station]')[{i}];
                     const box = s.getBoundingClientRect(); const host = document.querySelector('[data-lifts]');
                     const hb = host.getBoundingClientRect(); const y = box.top + box.height / 2 - hb.top;
                     for (const c of host.querySelectorAll('canvas')) {{
                       const t = parseFloat(c.style.top), h = parseFloat(c.style.height);
                       if (y < t || y > t + h || c.width < 400) continue;
                       const sx = c.width / c.clientWidth;
                       const d = c.getContext('2d').getImageData(Math.round((box.right - hb.left) * sx), Math.round((y - t) * sx), Math.round(28 * sx), 1).data;
                       for (let i = 3; i < d.length; i += 4) if (d[i] > 40) return true; }}
                     return false; }}"""
            )
        )
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(400)
    return met


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
        # The menu bar ("Inscription", nav-inscription.tsx): About is the current page in the bar
        # and in the narrow window's menu; there is no Home link (the mark goes home); Products is
        # a drop-down holding the five product pages and "Explore our products." (/#products).
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
        stations = page.evaluate("[...document.querySelectorAll('[data-station]')].map(s => s.textContent.trim())")
        check(f"{tag} four stations", stations == STATIONS, stations)
        cell = page.evaluate(CELL_JS)
        check(f"{tag} cell in the first screen", cell["inFirst"], cell)
        check(f"{tag} cell clear of the words", not cell["hit"], cell)
        # The cell is the first screen's painting: it is not lazy and the page preloads it (Next's
        # priority image: a <link rel="preload" as="image"> in the head; see DEV_LCP_MITO).
        eager = page.evaluate(
            """(() => { const i = document.querySelector('[data-brush="about-cell"] img');
                 const preload = [...document.querySelectorAll('link[rel=preload][as=image]')]
                   .some(l => ((l.getAttribute('imagesrcset') || '') + (l.getAttribute('href') || '')).includes('mito.webp'));
                 return { loading: i.getAttribute('loading'), preload }; })()"""
        )
        check(f"{tag} the cell loads eagerly and is preloaded", eager["loading"] != "lazy" and eager["preload"], eager)
        # Sheets: Support from the header (menu on a phone), Ask from the pause.
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
        check(f"{tag} no console errors or warnings", not errors, errors[:3])
        check(f"{tag} no failed requests", not failed, failed[:3])
        page.evaluate("window.scrollTo(0, 0)")
        shots(page, tag, height)
        if width == 1440:
            page.set_viewport_size({"width": 820, "height": 900})
            page.wait_for_timeout(1200)
            layout = page.evaluate("document.querySelector('[data-lifts]')?.dataset.layout")
            check("resize to 820: the line redraws for one column", layout == "column", layout)
        context.close()


# The title's lines: "Be in Good" over "Health." at every size (a word of the first line that has no
# room wraps alone, which reads as a broken title). Read from the word boxes once it has opened.
TITLE_LINES_JS = """() => {
  const tops = new Set([...document.querySelectorAll('h1 > span > span')].map(w => Math.round(w.getBoundingClientRect().top)));
  return tops.size;
}"""


def openings(browser):
    for width, height in [(1280, 720), (1536, 1000), (1024, 768), (900, 1100), (768, 1024), (834, 1112), (721, 1000), (360, 780)]:
        tag = f"{width}x{height}"
        context, page, response, errors, failed = open_page(browser, width, height)
        cell = page.evaluate(CELL_JS)
        check(f"{tag} cell in the first screen", cell["inFirst"], cell)
        check(f"{tag} cell clear of the words", not cell["hit"], cell)
        sideways = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
        check(f"{tag} no sideways scrolling", sideways <= 0, sideways)
        page.wait_for_timeout(1600)
        lines = page.evaluate(TITLE_LINES_JS)
        check(f"{tag} title on two lines", lines == 2, lines)
        if 721 <= width <= 899:
            # A tablet held upright (721-899 px): the opening keeps the desktop's composition, words
            # beside the cell, the title large and the cell larger, and stays compact, so the next
            # block starts in the same window (DESIGN.md, Layout: the opening is never much taller
            # than the comp at its width). Before October 5 it stacked a full-width cell over a
            # small title with the right half of the window empty.
            tablet = page.evaluate(
                f"""() => {{ const c = document.querySelector('[data-brush="about-cell"] img').getBoundingClientRect();
                     const h = document.querySelector('{OPENING} h1'); const t = h.getBoundingClientRect();
                     const s = document.querySelector('#purpose-title').getBoundingClientRect();
                     const walk = document.createTreeWalker(h, NodeFilter.SHOW_TEXT); const rights = []; let n;
                     while ((n = walk.nextNode())) {{ if (!n.textContent.trim()) continue; const r = document.createRange(); r.selectNodeContents(n);
                       for (const x of r.getClientRects()) if (x.width > 0) rights.push(x.right); }}
                     const line = Math.max(...rights) - t.left;
                     return {{ font: parseFloat(getComputedStyle(h).fontSize), beside: c.top < t.bottom && c.bottom > t.top && c.left >= t.right - 1,
                              cell: Math.round(c.width), line: Math.round(line), next: Math.round(s.top), vh: innerHeight }}; }}"""
            )
            check(f"{tag} tablet: title at least 60px", tablet["font"] >= 60, tablet)
            check(f"{tag} tablet: the cell beside the words", tablet["beside"], tablet)
            check(f"{tag} tablet: the painting leads (the cell wider than the title's line)", tablet["cell"] >= tablet["line"] * 1.1, tablet)
            check(f"{tag} tablet: the next block's heading in the first window", tablet["next"] < tablet["vh"] * 0.8, tablet)
        page.screenshot(path=os.path.join(OUT, f"opening-{tag}.png"))
        context.close()


# The longest vertical run of the brush layer's ink (alpha over 90) in one page column between two
# page rows, in CSS pixels; the tile holding those rows must be in the window.
INK_RUN_JS = r"""([x, y0, y1]) => {
  const host = document.querySelector('[data-lifts]'); const hb = host.getBoundingClientRect();
  let best = 0;
  for (const c of host.querySelectorAll('canvas')) {
    if (c.width < 400) continue;
    const t = parseFloat(c.style.top), h = parseFloat(c.style.height), sx = c.width / c.clientWidth;
    const ya = Math.max(y0 - (hb.top + scrollY), t), yb = Math.min(y1 - (hb.top + scrollY), t + h);
    if (yb <= ya) continue;
    const d = c.getContext('2d').getImageData(Math.round((x - hb.left) * sx), Math.round((ya - t) * sx), 1, Math.round((yb - ya) * sx)).data;
    let run = 0;
    for (let i = 3; i < d.length; i += 4) { if (d[i] > 90) { run++; best = Math.max(best, run / sx); } else run = 0; }
  }
  return best;
}"""


def finish(browser):
    """The finish pass (October 5, 2026, Task 9): what the review at full size asked for."""
    # Each station label keeps one line where the page has room (1200 px and wider): "Our
    # scientific roots" broke after "scientific" at 1440.
    for width, height in [(1440, 900), (1536, 1000)]:
        context, page, response, errors, failed = open_page(browser, width, height, reduced=True)
        tall = page.evaluate(
            """[...document.querySelectorAll('[data-station]')].map(s => [s.textContent.trim(), Math.round(s.getBoundingClientRect().height)])
                 .filter(([, h]) => h > 17 * 1.3 * 1.5)"""
        )
        check(f"{width}x{height} every station on one line", not tall, tall)
        context.close()
    # The promises' rules are brush strokes a reader sees as strokes (the mockup's short loaded
    # rules), not hairlines: each lands at least 5px thick at 1440. Read from the brush layer.
    context, page, response, errors, failed = open_page(browser, 1440, 900, reduced=True)
    weights = []
    for i in range(4):
        page.evaluate(f"document.querySelector('[data-brush=\"promise-{i}\"]').scrollIntoView({{block: 'center'}})")
        page.wait_for_timeout(500)
        box = page.evaluate(
            f"(() => {{ const b = document.querySelector('[data-brush=\"promise-{i}\"]').getBoundingClientRect(); return [b.left, b.top + scrollY, b.width]; }})()"
        )
        runs = [page.evaluate(INK_RUN_JS, [box[0] + box[2] * f, box[1] - 14, box[1] + 14]) for f in (0.04, 0.08, 0.12, 0.16, 0.2, 0.3)]
        weights.append(round(max(runs), 1))
    check("1440 each promise rule lands at least 5px thick", all(w >= 5 for w in weights), weights)
    context.close()
    # Japanese line breaking (strict, and anywhere for a phrase too wide) belongs to the page's
    # words, not to the shared header and footer.
    context, page, response, errors, failed = open_page(browser, 1440, 900, path="/jp/about", reduced=True)
    breaks = page.evaluate(
        """() => ({ main: getComputedStyle(document.querySelector('main')).lineBreak,
                    header: getComputedStyle(document.querySelector('header')).lineBreak,
                    footer: getComputedStyle(document.querySelector('footer')).lineBreak })"""
    )
    check("jp strict line breaks in the page's words only", breaks == {"main": "strict", "header": "auto", "footer": "auto"}, breaks)
    context.close()
    # The pause's inkstone is the small painting of the Three Sizes on a tablet too (at most 400px,
    # under half the window), not 70vw as on a phone.
    for width, height in [(768, 1024), (834, 1112)]:
        context, page, response, errors, failed = open_page(browser, width, height, reduced=True)
        stone = page.evaluate("Math.round(document.querySelector('#closing figure').getBoundingClientRect().width)")
        check(f"{width}x{height} the pause's inkstone stays small", stone <= min(400, width / 2), stone)
        context.close()


# The finish review's round (October 5, 2026, Task 9 fix round 1).

# The brush layer's ink over a page rectangle (CSS pixels, one sample per pixel): rows of 0/1
# (alpha over `level`: 90 by default, 40 to count the paler ink of a dry-brush passage). The tiles
# holding the rectangle must be in the window.
INK_GRID_JS = r"""([x0, y0, x1, y1, level]) => {
  const host = document.querySelector('[data-lifts]'); const hb = host.getBoundingClientRect();
  const W = Math.max(1, Math.round(x1 - x0)), H = Math.max(1, Math.round(y1 - y0));
  const grid = Array.from({ length: H }, () => new Array(W).fill(0));
  const top = hb.top + scrollY;
  for (const c of host.querySelectorAll('canvas')) {
    if (c.width < 2) continue;  // a tile far from the window holds no pixels
    const t = parseFloat(c.style.top), h = parseFloat(c.style.height), sx = c.width / c.clientWidth;
    const ya = Math.max(y0 - top, t), yb = Math.min(y1 - top, t + h);
    if (yb <= ya) continue;
    const d = c.getContext('2d').getImageData(Math.round((x0 - hb.left) * sx), Math.round((ya - t) * sx), Math.max(1, Math.round(W * sx)), Math.max(1, Math.round((yb - ya) * sx)));
    for (let r = 0; r < Math.round(yb - ya); r++) {
      const gy = Math.round(ya + top - y0) + r; if (gy < 0 || gy >= H) continue;
      const sy = Math.min(d.height - 1, Math.round(r * sx));
      for (let q = 0; q < W; q++) { const i = (sy * d.width + Math.min(d.width - 1, Math.round(q * sx))) * 4 + 3; if (d.data[i] > level) grid[gy][q] = 1; }
    }
  }
  return grid.map(row => row.join('')).join('\n');
}"""


def ink_grid(page, x0, y0, x1, y1, level=90):
    return [[ch == "1" for ch in row] for row in page.evaluate(INK_GRID_JS, [x0, y0, x1, y1, level]).split("\n")]


def box(page, sel):
    return page.evaluate(
        """(sel) => { const e = document.querySelector(sel); if (!e) return null; const b = e.getBoundingClientRect();
             return {left: b.left, right: b.right, top: b.top + scrollY, bottom: b.bottom + scrollY, width: b.width, height: b.height}; }""",
        sel,
    )


def luminance(rgb):
    def ch(v):
        v = v / 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4

    r, g, b = rgb
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a, b):
    la, lb = sorted([luminance(a), luminance(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def rgb_of(css):
    return tuple(float(v) for v in re.findall(r"[\d.]+", css)[:3])


# Glyph rectangles (page coordinates) of every text node under the matched elements.
GLYPHS_JS = """(sel) => { const out = [];
  for (const el of document.querySelectorAll(sel)) {
    const walk = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); let n;
    while ((n = walk.nextNode())) { if (!n.textContent.trim()) continue; const r = document.createRange(); r.selectNodeContents(n);
      for (const x of r.getClientRects()) if (x.width > 0) out.push([x.left, x.top + scrollY, x.right, x.bottom + scrollY]); } }
  return out; }"""


def longest_run(values):
    best = run = 0
    for v in values:
        run = run + 1 if v else 0
        best = max(best, run)
    return best


def round2(browser):
    """The finish review's items (Task 9 fix round 1)."""
    # 1. The brush is a brush, not a wire (1440, whole line drawn). The sweep from where it leaves
    # the painting to the first station's bend is a curve, not a straight chord: along its run its
    # direction turns 20 degrees or more (it was one straight diagonal, then a knee). It is loaded
    # (4.2px or more at its fullest). The stroke down the margin is loaded (4.2px or more at its
    # fullest, about 4.5 at the 1536 comp) and thickens and thins: it narrows to a point (2px or less)
    # at the roots leader, where the brush rises and lands again, and swells to 5px or more between
    # the stations. (Round 3 keeps the run itself at 3px of real ink or more, round3 item 1, so the
    # thinning now lives at the leaders, not in long dry stretches.)
    context, page, response, errors, failed = open_page(browser, 1440, 900, reduced=True)
    cell = box(page, '[data-brush="about-cell"] img')
    st = box(page, '[data-brush="st-purpose"]')
    st2 = box(page, '[data-brush="st-roots"]')
    page.evaluate(f"window.scrollTo(0, {max(0, cell['bottom'] - 450)})")
    page.wait_for_timeout(500)
    x0, x1 = st["right"] + 110, cell["left"] + cell["width"] * 0.14
    y0, y1 = cell["top"] + cell["height"] * 0.6, st["top"] + st["height"] / 2
    grid = ink_grid(page, x0, y0, x1, y1, 40)
    cols = []
    for q in range(0, len(grid[0]), 6):
        column = [grid[r][q] for r in range(len(grid))]
        rows = [r for r, v in enumerate(column) if v]
        if rows:
            # The stroke's width in this column: its envelope, dry-brush streaks inside it included.
            cols.append((x0 + q, y0 + (rows[0] + rows[-1]) / 2, rows[-1] - rows[0] + 1))
    angles = [math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])) for a, b in zip(cols, cols[4:])]
    turn = round(max(angles) - min(angles), 1) if angles else None
    thick = [c[2] for c in cols]
    check("1440 the sweep is a curve (its direction turns 20 degrees or more)", turn is not None and turn >= 20, [turn, len(cols)])
    check("1440 the sweep is loaded (4.2px or more at its fullest)", bool(thick) and max(thick) >= 4.2, thick)
    page.evaluate(f"window.scrollTo(0, {st['top'] - 300})")
    page.wait_for_timeout(500)
    widths = []
    for k in range(1, 10):
        y = st["top"] + st["height"] / 2 + (st2["top"] - st["top"]) * k / 10
        widths.append(longest_run(ink_grid(page, st["right"] - 10, y, st["right"] + 120, y + 1)[0]))
    check("1440 the margin's stroke is loaded (4.2px or more at its fullest)", bool(widths) and max(widths) >= 4.2, widths)
    cy = st2["top"] + st2["height"] / 2
    pinch = min(longest_run(ink_grid(page, st2["right"] - 10, cy + d, st2["right"] + 120, cy + d + 1)[0]) for d in range(-3, 4))
    check("1440 the margin's stroke thickens and thins (2px or less at the leader, 5px or more between)", bool(widths) and pinch <= 2 and max(widths) >= 5, [pinch, widths])
    context.close()

    # 2. The light on the cell's leaf crosses it and leaves it (as on the opening's sun), not parked
    # on it: the cell rests in the first screen, where a scroll-driven pass held the pale band over
    # the leaf (gold saturation 114 against 148 without it, October 5). Sampled for 10 s.
    context, page, response, errors, failed = open_page(browser, 1440, 900)
    page.wait_for_timeout(8000)
    on, samples = 0, 25
    for _ in range(samples):
        pos = page.evaluate(
            "parseFloat(getComputedStyle(document.querySelector('[data-brush=\"about-cell\"] [data-charge]').previousElementSibling).backgroundPositionX)"
        )
        on += 1 if 20 < pos < 80 else 0
        page.wait_for_timeout(400)
    check("1440 the light band is on the leaf at most 40% of the time", on / samples <= 0.4, f"{on}/{samples}")
    context.close()

    # 3. The cell at the comp's scale, low and near the title (1536, 1440, 1280): 46% of the window
    # wide or more, its box within 4.5% of the window from the title's last letter, all of it in the
    # first screen, reaching under the opening's words (6% of the window or more), no letter over it.
    for width, height in [(1536, 1000), (1440, 900), (1280, 720)]:
        context, page, response, errors, failed = open_page(browser, width, height, reduced=True)
        cell = box(page, '[data-brush="about-cell"] img')
        glyphs = page.evaluate(GLYPHS_JS, f"{OPENING} h1, {OPENING} p")
        title_right = max(g[2] for g in page.evaluate(GLYPHS_JS, f"{OPENING} h1"))
        lead_bottom = max(g[3] for g in glyphs)
        hit = [g for g in glyphs if not (cell["right"] <= g[0] or cell["left"] >= g[2] or cell["bottom"] <= g[1] or cell["top"] >= g[3])]
        tag = f"{width}x{height}"
        info = {"w": round(cell["width"]), "left": round(cell["left"]), "title_right": round(title_right), "bottom": round(cell["bottom"]), "lead_bottom": round(lead_bottom)}
        check(f"{tag} the cell is 46% of the window or more", cell["width"] >= 0.46 * width, info)
        check(f"{tag} the cell stands near the title", cell["left"] - title_right <= 0.045 * width, info)
        check(f"{tag} the whole cell in the first screen", cell["bottom"] <= height, info)
        check(f"{tag} the cell reaches under the words", cell["bottom"] - lead_bottom >= 0.06 * width, info)
        check(f"{tag} no letter of the opening over the cell", not hit, hit[:2])
        context.close()

    # 4. The name: the letters after B, i, G and H in an ink-wash grey that still reads (3:1 or more
    # on the paper, large text) and stands clearly apart from the initials (3.5:1 or more).
    context, page, response, errors, failed = open_page(browser, 1440, 900, reduced=True)
    colors = page.evaluate(
        """() => { const word = document.querySelector('h1 > span > span');
             return { initial: getComputedStyle(word.firstElementChild).color, rest: getComputedStyle(word.lastElementChild).color }; }"""
    )
    on_paper = round(contrast(rgb_of(colors["rest"]), (0xF8, 0xF3, 0xEA)), 2)
    apart = round(contrast(rgb_of(colors["rest"]), rgb_of(colors["initial"])), 2)
    check("the name's other letters read on the paper (3:1 or more)", on_paper >= 3.0, [colors, on_paper])
    check("the name's other letters stand apart from the initials (3.5:1 or more)", apart >= 3.5, [colors, apart])
    context.close()

    # 5. (Superseded in round 3: the stroke below 900px, see round3 item 2.)

    # 6. A tablet held upright: the cell runs 55-62% of the window wide and off its right edge, both
    # gold folds in view (the leaf spans 44-65% of the picture's width).
    for width, height in [(768, 1024), (834, 1112), (721, 1000)]:
        context, page, response, errors, failed = open_page(browser, width, height, reduced=True)
        cell = box(page, '[data-brush="about-cell"] img')
        gold_right = cell["left"] + cell["width"] * 0.648
        info = {"w": round(cell["width"]), "left": round(cell["left"]), "right": round(cell["right"]), "gold_right": round(gold_right)}
        check(f"{width}x{height} tablet: the cell runs 55-62% of the window", 0.55 * width <= cell["width"] <= 0.62 * width, info)
        check(f"{width}x{height} tablet: the cell runs off the right edge", cell["right"] > width, info)
        check(f"{width}x{height} tablet: both gold folds in view", gold_right <= width - 8, info)
        context.close()

    # 7. (Superseded in round 3: the comp's side-by-side promise layout, see round3 item 3.)


def core_weights(browser, width, height):
    """The brush's real ink (alpha over 140, dry-brush paper inside it not counted), measured across
    the stroke: on the sweep out of the cell (columns over its long run, corrected for the run's
    slope) and down the margin between each pair of stations (rows), leaving out 40px either side of
    each reload, where the brush lands and presses in."""
    context, page, response, errors, failed = open_page(browser, width, height, reduced=True)
    cell = box(page, '[data-brush="about-cell"] img')
    sts = [box(page, f'[data-brush="st-{i}"]') for i in ("purpose", "roots", "experience", "promise")]
    st = sts[0]
    page.evaluate(f"window.scrollTo(0, {max(0, cell['bottom'] - 450)})")
    page.wait_for_timeout(500)
    x0, x1 = st["right"] + 110, cell["left"] + cell["width"] * 0.14
    y0, y1 = cell["top"] + cell["height"] * 0.6, st["top"] + st["height"] / 2
    grid = ink_grid(page, x0, y0, x1, y1, 140)
    cols = []
    for q in range(0, len(grid[0]), 3):
        rows = [r for r in range(len(grid)) if grid[r][q]]
        cols.append((x0 + q, y0 + (rows[0] + rows[-1]) / 2 if rows else None, len(rows)))
    sweep = []
    for k, (x, y, n) in enumerate(cols):
        a, b = cols[max(0, k - 3)], cols[min(len(cols) - 1, k + 3)]
        if y is None or a[1] is None or b[1] is None:
            sweep.append(n)
            continue
        slope = math.atan2(b[1] - a[1], b[0] - a[0])
        sweep.append(round(n * abs(math.cos(slope)), 1))
    margin = []
    for a, b in zip(sts, sts[1:]):
        top, bottom = a["top"] + a["height"] / 2 + 40, b["top"] + b["height"] / 2 - 40
        page.evaluate(f"window.scrollTo(0, {top - 200})")
        page.wait_for_timeout(500)
        rows = ink_grid(page, st["right"] - 10, top, st["right"] + 140, min(bottom, top + 680), 140)
        margin += [sum(r) for r in rows[::3]]
        if bottom > top + 680:
            page.evaluate(f"window.scrollTo(0, {top + 480})")
            page.wait_for_timeout(500)
            rows = ink_grid(page, st["right"] - 10, top + 680, st["right"] + 140, bottom, 140)
            margin += [sum(r) for r in rows[::3]]
    context.close()
    return sweep, margin


def round3(browser):
    """The finish review's second round (Task 9 fix round 2)."""
    # 1. The brush holds real ink: 3px or more of it across the stroke everywhere on the sweep's run
    # and down the margin (except 40px either side of a reload), within the homepage's brush (its
    # loads stay at or under the closing stroke's). On 0290159 long stretches were a 1-2px pen line.
    for width, height in [(1536, 1000), (1440, 900)]:
        sweep, margin = core_weights(browser, width, height)
        thin_s = sum(1 for v in sweep if v < 3)
        thin_m = sum(1 for v in margin if v < 3)
        check(f"{width}x{height} the sweep holds 3px of real ink along its run", bool(sweep) and thin_s == 0, f"{thin_s}/{len(sweep)} under 3px, min {min(sweep) if sweep else None}")
        check(f"{width}x{height} the margin's stroke holds 3px of real ink between reloads", bool(margin) and thin_m == 0, f"{thin_m}/{len(margin)} under 3px, min {min(margin) if margin else None}")

    # 2. Nothing grows out of the cell. On a phone no brush ink lies within 12px of the painting's own
    # ink (a stroke out of its corner read as a tail). On a tablet held upright the stroke out of the
    # cell runs on to the first station and ends at the tip of its leader (within 16px), as the page's
    # line arriving at its first station, never stopping in open paper.
    for width, height in [(390, 844), (360, 780)]:
        context, page, response, errors, failed = open_page(browser, width, height, reduced=True)
        cell = box(page, '[data-brush="about-cell"] img')
        painting = page.evaluate(
            """() => { const img = document.querySelector('[data-brush="about-cell"] img'); const b = img.getBoundingClientRect();
                 const c = document.createElement('canvas'); c.width = Math.round(b.width); c.height = Math.round(b.height);
                 const x = c.getContext('2d'); x.fillStyle = '#fff'; x.fillRect(0, 0, c.width, c.height); x.drawImage(img, 0, 0, c.width, c.height);
                 const d = x.getImageData(0, 0, c.width, c.height).data; let s = '';
                 for (let i = 0; i < d.length; i += 4) s += (0.2126 * d[i] + 0.7152 * d[i + 1] + 0.0722 * d[i + 2]) < 225 ? '1' : '0';
                 return { w: c.width, h: c.height, s }; }"""
        )
        pw, ph = painting["w"], painting["h"]
        ink_pts = [(i % pw, i // pw) for i, ch in enumerate(painting["s"]) if ch == "1"]
        gx0, gy0 = max(0, cell["left"] - 12), cell["top"] - 12
        gx1, gy1 = min(width, cell["right"] + 12), cell["bottom"] + 12
        brush = ink_grid(page, gx0, gy0, gx1, gy1, 40)
        near = set()
        for (px, py) in ink_pts[::2]:
            near.add((int((cell["left"] + px - gx0) // 12), int((cell["top"] + py - gy0) // 12)))
        close = 0
        for r, row in enumerate(brush):
            for c, v in enumerate(row):
                if v and any((c // 12 + dx, r // 12 + dy) in near for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                    close += 1
        check(f"{width}x{height} no brush ink within 12px of the painting", bool(ink_pts) and close == 0, close)
        context.close()
    for width, height in [(768, 1024), (834, 1112), (721, 1000)]:
        context, page, response, errors, failed = open_page(browser, width, height, reduced=True)
        cell, st = box(page, '[data-brush="about-cell"] img'), box(page, '[data-brush="st-purpose"]')
        y0, y1 = cell["top"] + cell["height"] * 0.75, st["bottom"] + 12
        grid = ink_grid(page, 0, y0, width, y1, 40)
        pts = [(c, r) for r, row in enumerate(grid) for c, v in enumerate(row) if v]
        tip = (st["left"], st["top"] + st["height"] / 2 - y0)
        end = min(pts, key=lambda p: p[0]) if pts else None
        gap = round(math.hypot(end[0] - tip[0], end[1] - tip[1]), 1) if end else None
        check(f"{width}x{height} the stroke out of the cell ends at the first station's leader (16px)", gap is not None and gap <= 16 and len(pts) >= 300, [gap, end, tip, len(pts)])
        glyphs = page.evaluate(GLYPHS_JS, f'{OPENING} h1, {OPENING} p, [data-brush="st-purpose"], #purpose-title')
        touched = 0
        for g in glyphs:
            for r in range(max(0, int(g[1] - y0)), min(len(grid), int(g[3] - y0) + 1)):
                touched += sum(grid[r][max(0, int(g[0])):min(width, int(g[2]) + 1)])
        check(f"{width}x{height} the stroke touches no words", touched == 0, touched)
        context.close()

    # 3. The comp's promise layout: "What you can count on." beside the two-by-two list (the page's one
    # heading-beside-list moment), its top level with the first rule (12px), the list's right edge on
    # the figures' right edge above it (8px).
    for width, height in [(1536, 1000), (1440, 900), (1280, 720)]:
        context, page, response, errors, failed = open_page(browser, width, height, reduced=True)
        lay = page.evaluate(
            """() => { const r = document.createRange(); r.selectNodeContents(document.querySelector('#promise-title'));
                 const lines = [...r.getClientRects()].filter(x => x.width > 0);
                 const list = document.querySelector('[data-brush="promise-0"]').parentElement.getBoundingClientRect();
                 const first = document.querySelector('[data-brush="promise-0"]').getBoundingClientRect();
                 const figures = document.querySelector('[data-brush="figures"]').getBoundingClientRect();
                 return { headRight: Math.round(Math.max(...lines.map(x => x.right))), headTop: Math.round(Math.min(...lines.map(x => x.top))),
                          listLeft: Math.round(list.left), listRight: Math.round(list.right), ruleTop: Math.round(first.top),
                          figuresRight: Math.round(figures.right) }; }"""
        )
        tag = f"{width}x{height}"
        check(f"{tag} the promise heading stands beside the list", lay["headRight"] <= lay["listLeft"], lay)
        check(f"{tag} the heading's top level with the first rule (12px)", abs(lay["headTop"] - lay["ruleTop"]) <= 12, lay)
        check(f"{tag} the list's right edge on the figures' right edge (8px)", abs(lay["listRight"] - lay["figuresRight"]) <= 8, lay)
        context.close()


# The painting's own ink (its paper is divided out: anything darker than 236 of 255 is ink or wash)
# at its drawn size, as a string of rows of 0/1 over the picture's box.
PAINTING_JS = """() => { const img = document.querySelector('[data-brush="about-cell"] img'); const b = img.getBoundingClientRect();
  const c = document.createElement('canvas'); c.width = Math.round(b.width); c.height = Math.round(b.height);
  const x = c.getContext('2d'); x.fillStyle = '#fff'; x.fillRect(0, 0, c.width, c.height); x.drawImage(img, 0, 0, c.width, c.height);
  const d = x.getImageData(0, 0, c.width, c.height).data; const rows = [];
  for (let y = 0; y < c.height; y++) { let s = ''; for (let i = y * c.width * 4; i < (y + 1) * c.width * 4; i += 4)
    s += (0.2126 * d[i] + 0.7152 * d[i + 1] + 0.0722 * d[i + 2]) < 236 ? '1' : '0'; rows.push(s); }
  return { left: b.left, top: b.top + scrollY, rows }; }"""


def cell_foot(page, width, pad=140):
    """The painting's ink and the brush layer's ink around the cell, on one page-pixel grid: a dict
    with the painting's boundary points, the brush's ink (alpha over 40) and core ink (over 140)."""
    import numpy as np

    paint = page.evaluate(PAINTING_JS)
    rows = paint["rows"]
    ph, pw = len(rows), len(rows[0])
    x0, y0 = max(0, int(paint["left"]) - pad), int(paint["top"]) - pad
    x1, y1 = min(width, int(paint["left"]) + pw + pad), int(paint["top"]) + ph + pad
    mask = np.zeros((y1 - y0, x1 - x0), dtype=bool)
    pm = np.array([[ch == "1" for ch in r] for r in rows], dtype=bool)
    ox, oy = int(paint["left"]) - x0, int(paint["top"]) - y0
    sx0, sx1 = max(0, -ox), min(pw, mask.shape[1] - ox)
    mask[oy:oy + ph, ox + sx0:ox + sx1] = pm[:, sx0:sx1]
    inner = mask.copy()
    inner[1:-1, 1:-1] = mask[1:-1, 1:-1] & mask[:-2, 1:-1] & mask[2:, 1:-1] & mask[1:-1, :-2] & mask[1:-1, 2:]
    edge = np.argwhere(mask & ~inner)
    ink = np.array(ink_grid(page, x0, y0, x1, y1, 40), dtype=bool)
    core = np.array(ink_grid(page, x0, y0, x1, y1, 140), dtype=bool)
    return {"origin": (x0, y0), "mask": mask, "edge": edge, "ink": ink, "core": core}


def distances(points, edge):
    """Each point's distance to the nearest painting boundary point (chunked, numpy only)."""
    import numpy as np

    out = np.full(len(points), np.inf)
    for i in range(0, len(points), 2000):
        p = points[i:i + 2000][:, None, :].astype(float)
        out[i:i + 2000] = np.sqrt(((p - edge[None, :, :]) ** 2).sum(-1)).min(1)
    return out


def round4(browser):
    """The finish review's third round (Task 9 fix round 3)."""
    import numpy as np

    # 1. The line starts as a brush set down on the paper under the cell, never as something growing
    # out of it: no brush ink inside the painting or within 12px of its ink (its outer wash included),
    # and the stroke's first 30px hold 3px or more of real ink (alpha over 140) across it: a loaded,
    # blunt landing, no needle lead-in and no neck. On 2a18847 it began as a hairline inside the
    # membrane, ran as a filament and pinched before it swelled.
    for width, height in [(1536, 1000), (1440, 900), (1280, 720), (1024, 768), (768, 1024), (834, 1112), (721, 1000)]:
        context, page, response, errors, failed = open_page(browser, width, height, reduced=True)
        g = cell_foot(page, width)
        tag = f"{width}x{height}"
        pts = np.argwhere(g["ink"])
        if not len(pts) or not len(g["edge"]):
            check(f"{tag} the line starts clear of the painting (12px)", False, "no ink found")
            check(f"{tag} the line's first 30px are loaded (3px of real ink)", False, "no ink found")
            context.close()
            continue
        inside = int((g["ink"] & g["mask"]).sum())
        dist = distances(pts, g["edge"])
        dist[g["mask"][pts[:, 0], pts[:, 1]]] = 0
        near = int((dist < 12).sum())
        check(f"{tag} the line starts clear of the painting (12px)", near == 0, {"within_12px": near, "inside": inside, "nearest": round(float(dist.min()), 1)})
        start = pts[int(np.argmin(dist))]
        cores = np.argwhere(g["core"])
        rad = np.sqrt(((cores - start) ** 2).sum(1)) if len(cores) else np.array([])
        across = [int(((rad >= d - 0.5) & (rad < d + 0.5)).sum()) for d in range(3, 31, 3)]
        check(f"{tag} the line's first 30px are loaded (3px of real ink)", bool(across) and min(across) >= 3, {"start": (int(start[1]) + g["origin"][0], int(start[0]) + g["origin"][1]), "across": across})
        context.close()

    # 2. Round the stacking breakpoint the promises keep a reading measure: each of the two list
    # columns 250px wide or more, every title on one line and no description over three lines. At
    # 1200-1279px the heading stands over the list (beside it the columns were 219-238px and two
    # titles wrapped); from 1280px it stands beside it.
    for width, height in [(1200, 800), (1240, 800), (1280, 800)]:
        context, page, response, errors, failed = open_page(browser, width, height, reduced=True)
        cols = page.evaluate(
            """() => [...document.querySelectorAll('[data-brush^="promise-"]')].map(li => {
                 const lines = (e) => { const r = document.createRange(); r.selectNodeContents(e);
                   return new Set([...r.getClientRects()].filter(x => x.width > 0).map(x => Math.round(x.top))).size; };
                 return { w: Math.round(li.getBoundingClientRect().width), title: lines(li.querySelector('h3')), text: lines(li.querySelector('p')) }; })"""
        )
        tag = f"{width}x{height}"
        check(f"{tag} the promises keep a reading measure (250px or more)", cols and min(c["w"] for c in cols) >= 250, cols)
        check(f"{tag} every promise title on one line, no text over three", cols and all(c["title"] == 1 and c["text"] <= 3 for c in cols), cols)
        context.close()


def stroke_head(page, width):
    """The brush's head beside the cell's foot, read off the pixels (the whole line drawn): the tip
    (the end of the core ink nearest the painting), the heading of the first 40px from it, the
    angle between the stroke's aim (its axis, backwards out of the tip) and the painting's nearest
    ink, the course of the first 60px in 10px steps, and the core-ink width (alpha over 140, in px
    across the stroke) along the first 40px. Angles: `lean` is measured from straight left, down
    positive (a climbing stroke leans negative)."""
    import numpy as np

    g = cell_foot(page, width)
    ink, core, edge = np.argwhere(g["ink"]), np.argwhere(g["core"]), g["edge"]
    if not len(ink) or not len(core) or not len(edge):
        return None
    dist = distances(ink, edge)
    dist[g["mask"][ink[:, 0], ink[:, 1]]] = 0
    near = ink[int(np.argmin(dist))].astype(float)

    def heading(origin, reach=40):
        sel = core[np.sqrt(((core - origin) ** 2).sum(1)) < reach]
        d = sel.mean(0) - origin
        return d / (np.linalg.norm(d) or 1)

    # A first axis from the ink nearest the painting; the end of the stroke is the core pixel
    # farthest back along it. Then the real axis of the first 40px, from the centres of two slabs
    # of the stroke (2-14px and 26-40px in), so a corner pixel of the end does not tilt it.
    d0 = heading(near)
    about = core[np.sqrt(((core - near) ** 2).sum(1)) < 60]
    tip = about[int(np.argmax(((about - near) * -d0).sum(1)))].astype(float)
    along0 = ((core - tip) * d0).sum(1)
    first, later = core[(along0 >= 2) & (along0 < 14)], core[(along0 >= 26) & (along0 < 40)]
    if len(first) < 4 or len(later) < 4:
        return None
    d = later.mean(0) - first.mean(0)
    d = d / (np.linalg.norm(d) or 1)  # (dy, dx)
    lean = math.degrees(math.atan2(d[0], -d[1]))
    along = (core * d).sum(1)
    along -= along.min()
    end = core[along < 3].mean(0)  # the centre of the end, 3px deep
    v = edge[int(np.argmin(((edge - end) ** 2).sum(1)))] - end
    v = v / (np.linalg.norm(v) or 1)
    aim = math.degrees(math.acos(max(-1.0, min(1.0, float((-d * v).sum())))))
    centres = [end]
    for a in range(10, 61, 10):
        sel = core[np.abs(along - a) < 5]
        centres.append(sel.mean(0) if len(sel) else centres[-1])
    steps = []
    for p, q in zip(centres, centres[1:]):
        dy, dx = q - p
        steps.append({"lean": round(math.degrees(math.atan2(dy, -dx)) if (dx or dy) else 0.0), "dy": round(float(dy), 1)})
    widths = [round(float(((along >= a - 1) & (along < a + 1)).sum()) / 2, 1) for a in range(1, 41)]
    # How square the end is: the core ink over the stroke's first half-width (from the end), as a
    # share of the rectangle a square cut at the head's width would fill (1.0; a half-round end
    # fills about 0.78). On a 4px head (the tablet's brush scale) the pixel grid cannot show an end
    # rounder than about 0.88.
    head = max(widths[5:14])
    fill = float((along < head / 2).sum()) / max(1.0, (head / 2) * head)
    ox, oy = g["origin"]
    return {
        "tip": (int(end[1]) + ox, int(end[0]) + oy),
        "lean": round(lean),
        "aim": round(aim),
        "steps": steps,
        "widths": widths,
        "fill": round(fill, 2),
        "gap": round(float(dist.min()), 1),
    }


def round5(browser):
    """The finish review's fourth round (Task 9 fix round 4): the line's start no longer reads as
    something hanging from the cell."""
    sizes = [(1536, 1000), (1440, 900), (1280, 720), (1024, 768), (768, 1024), (834, 1112), (721, 1000)]
    for width, height in sizes:
        context, page, response, errors, failed = open_page(browser, width, height, reduced=True)
        tag = f"{width}x{height}"
        h = stroke_head(page, width)
        if h is None:
            check(f"{tag} the stroke sets down beside the cell, not aimed at it", False, "no ink found")
            check(f"{tag} a round, pressed head thinning into the run", False, "no ink found")
            context.close()
            continue
        # 1. The brush sets down already travelling left (level or drifting down-left, never
        # climbing, its first 40px within 25 degrees of level), and the painting lies above or beside
        # the stroke's end, not ahead of it: the angle between the stroke's aim (its axis, backwards
        # out of the tip) and the painting's nearest ink is 45 degrees or more. On 1e463c0 the first
        # segment ran along the painting's normal, so its axis pointed straight back into the lobe
        # (aim about 0 degrees, lean about 50).
        check(
            f"{tag} the stroke sets down beside the cell, not aimed at it",
            h["aim"] >= 45 and -5 <= h["lean"] <= 25,
            {"aim": h["aim"], "lean": h["lean"], "tip": h["tip"], "gap": h["gap"]},
        )
        # 2. On a tablet held upright no tick under the cell: the first 60px of the stroke run left,
        # level or gently down (each 10px step within 35 degrees of level, never climbing, turning no
        # more than 25 degrees from the step before). On 1e463c0 a steep tick fell from the foot and
        # kinked into the run.
        if width < 900:
            turns = [abs(a["lean"] - b["lean"]) for a, b in zip(h["steps"], h["steps"][1:])]
            check(
                f"{tag} no tick under the cell: the first 60px run level and left",
                all(-8 <= s["lean"] <= 35 and s["dy"] >= -2 for s in h["steps"]) and all(t <= 25 for t in turns),
                {"steps": h["steps"], "turns": turns},
            )
        # 3. A round, pressed head that thins into the run: the end is round, not a square cut (the
        # core ink over the first half-width fills at most 85% of a square cut's rectangle; read
        # where the head is 5px or more, since a 4px head, the tablet's brush scale, narrows 2-3-4
        # over its last pixels and the grid cannot show rounder), the head (6-14px in) is wider
        # than the run (30-40px in) by a tenth or more, and from 6px in the stroke holds 3px of
        # core ink everywhere over its first 40px. On 1e463c0 the end was a square cut (fill about
        # 0.9-1.0) at the run's full width.
        w = h["widths"]
        head, run = max(w[5:14]), sum(w[29:40]) / len(w[29:40])
        check(
            f"{tag} a round, pressed head thinning into the run",
            (head < 5 or h["fill"] <= 0.85) and head >= 1.1 * run and min(w[5:40]) >= 3,
            {"fill": h["fill"], "head": head, "run": round(run, 1), "min6to40": min(w[5:40]), "widths": w[:16]},
        )
        context.close()


def line_and_focus(browser):
    context, page, response, errors, failed = open_page(browser, 1440, 900, reduced=True)
    layout = page.evaluate("document.querySelector('[data-lifts]')?.dataset.layout")
    check("1440 brush draws the page layout", layout == "page", layout)
    # Each station's leader ends at the line: some ink within 28px right of the label's leader.
    meets = stations_met(page)
    check("1440 line meets every station", len(meets) == 4 and all(meets), meets)
    bloom = page.evaluate("[...document.querySelectorAll('[data-bloom]')].every(e => e.dataset.bloom === 'done')")
    check("reduced motion: every painting shown", bloom)
    charge = page.evaluate("getComputedStyle(document.querySelector('[data-charge]')).opacity")
    check("reduced motion: gold leaf fully up", float(charge) == 0, charge)
    # The brush layer's effect runs twice under reduced motion (the preference starts true, then
    # flips); the first run's late font relayout must not add a second set of canvases (TILE in
    # src/components/ink/brush.tsx is 1200px).
    page.wait_for_timeout(1000)
    tiles = page.evaluate(
        """() => { const host = document.querySelector('[data-lifts]');
                   return { canvases: host.querySelectorAll('canvas').length,
                            need: Math.ceil(host.offsetHeight / 1200), height: host.offsetHeight }; }"""
    )
    check("reduced motion 1440: the brush holds one set of canvas tiles", tiles["canvases"] == tiles["need"] and tiles["need"] > 0, tiles)
    context.close()
    # With motion: the cell blooms with its leaf drained, then the leaf comes up.
    context, page, response, errors, failed = open_page(browser, 1440, 900)
    early = float(page.evaluate("getComputedStyle(document.querySelector('[data-charge]')).opacity"))
    page.wait_for_timeout(9000)
    late = float(page.evaluate("getComputedStyle(document.querySelector('[data-charge]')).opacity"))
    check("motion: the gold leaf comes up after the bloom", early > 0.5 and late < 0.05, [early, late])
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


# Where a deep link lands: the section's heading (the part's first words) sits 0-48px under the
# header's bottom, measured at run time (the header's height is not assumed). The part's scroll
# margin works against the page's own scroll-padding-top (150px, globals.css) and the part's top
# padding. Exception: under 1200px Dr. Liu's print stands over the roots' words, so that section's
# first content is its station label (the heading is 480-600px lower); landing on the heading
# would scroll the portrait away.
DEEP_LINK_JS = """([id, lead]) => {
  const target = document.querySelector(lead === 'heading' ? `#${id}-title` : `#${id} [data-station]`);
  const header = document.querySelector('header').getBoundingClientRect().bottom;
  return { scrollY: Math.round(window.scrollY), header: Math.round(header),
           gap: Math.round(target.getBoundingClientRect().top - header) };
}"""


def deep_links(browser):
    # Each size is one browser context: a first visit to /about warms the fonts into the cache, then
    # every deep link is a fresh load of the page. On a cold load the dev server's web fonts can
    # arrive after the page has started scrolling; the roots part then reflows (39px shorter at 390)
    # and the smooth scroll, already aimed, ends that far too low (the heading under the header; 4 of
    # 10 cold dev loads at 390 for #promise, 0 of 10 on the built site and 0 of 6 on the built site
    # behind a slow network and CPU). The check is about the landing the CSS sets, so fonts are in.
    for width, height in [(1440, 900), (1024, 768), (768, 1024), (390, 844)]:
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
            lead = "station" if anchor == "roots" and width < 1200 else "heading"
            at = page.evaluate(DEEP_LINK_JS, [anchor, lead])
            check(
                f"{width}x{height} /about#{anchor}: the {lead} lands 0-48px under the header ({at['gap']}px)",
                at["scrollY"] > 0 and 0 <= at["gap"] <= 48,
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
        text = page.evaluate("document.querySelector('main').innerText")
        left = [line for line in english if line in text]
        check(f"{lang} no English sentence left", not left, left[:3])
        check(f"{lang} no console errors or warnings", not errors, errors[:3])
        if lang == "vn":
            # The longest labels, after the late Vietnamese font: the line must still meet every leader.
            page.evaluate("document.fonts.ready.then(() => true)")
            page.wait_for_timeout(1500)
            meets = stations_met(page)
            check("vn line meets every station after the font arrives", len(meets) == 4 and all(meets), meets)
        page.screenshot(path=os.path.join(OUT, f"{lang}-opening.png"))
        context.close()


def languages_layout(browser):
    """Each language at desktop, tablet and phone sizes: no word crosses the side margins, and
    in Korean, Japanese, Chinese and Vietnamese no bad line break."""
    for lang in ["en", "kr", "jp", "cns", "vn"]:
        for width, height in [(1440, 900), (1024, 768), (768, 1024), (390, 844), (360, 780)]:
            tag = f"{lang} {width}x{height}"
            path = "/about" if lang == "en" else f"/{lang}/about"
            context, page, response, errors, failed = open_page(browser, width, height, path=path, reduced=True)
            over = page.evaluate(MARGINS_JS)
            check(f"{tag} words inside the margins", not over, over[:3])
            if lang != "en":
                bad = page.evaluate(BREAKS_JS, lang)
                check(f"{tag} no bad line break", not bad, bad[:3])
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


# --only=openings,finish runs just those groups (while working on one thing); the full run is the gate.
GROUPS = [desktop_and_phone, openings, finish, round2, round3, round4, round5, line_and_focus, deep_links, languages, languages_layout, nav_locales]
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

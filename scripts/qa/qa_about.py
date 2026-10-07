"""QA for About B, "The album" (Mo, October 7, 2026; mockup reference/ink-pages/mockups/about-b.png;
spec docs/superpowers/specs/2026-10-05-ink-pages-design.md, "About (stage 1), October 7").

desktop_and_phone (1440x900, 390x844): 200; no console errors or warnings (but PREFETCH_CSS); no
failed requests; one h1, English "Be in Good Health." with lang="en"; every locked line; no canvas,
no brush layer, no folds, no aged paper; every painting multiplies and nothing between a painting
and the page root makes a stacking context; the menu bar marks About; no sideways scrolling; text
15px+, navigation 18px+, targets 48px+; the opening's painting loads eagerly; the Support and Ask
sheets open, close and hand focus back.
rhythm (1440x900, 1280x800, 1080x800, 1024x768, 960x800, 768x1024, 390x844): every spread part has
one picture and its words; on two columns (from 960px) the pictures stand opening right, purpose
left, roots right, experience left, closing right, and are about the same size, and nothing in a
words column reaches past its right edge; on one column each picture comes first; the name once
(nothing in the page but the h1 at 56px or larger, no painted name); "Illustration" under each
picture, "Illustrations" under the promise row; no words over a painting; four promises in one row
from 1200px, two by two from 600px, one column below; Dr. Liu's photo in his words, beside his
paragraph on a tablet's column and from 1080px, above it elsewhere.
motion: reduced motion complete and still; with motion every painting is server-marked waiting (none
paints whole, then vanishes), the opening's painting blooms on arrival and a lower painting waits
out of view, then blooms; a waiting painting is hidden; with JavaScript off every painting shows.
focus: Skip to content puts focus at the words; with pictures blocked every heading and paragraph
is visible.
boundary (959x900, 960x900): no sideways scrolling; one column at 959 (picture first), two at 960.
first_screen (1280x720, 1440x900, 1536x864, 390x844): the title and the top of the opening's picture
in the first screen.

Pictures: scripts/qa/out/about-album/<size>-NN.png.

Usage: python -X utf8 scripts/qa/qa_about.py [base-url] [--only=desktop_and_phone,rhythm,motion,focus,boundary,first_screen]
"""

import io
import os
import re
import sys

from PIL import Image
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = ARGS[0] if ARGS else "http://localhost:3025"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "about-album")
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


# Hello in five languages (the fourth promise): the visible words' box, centred on its promise.
GREETINGS_JS = """() => { const li = document.querySelectorAll('[data-promise]')[3];
  const words = [...li.querySelectorAll('[aria-hidden="true"] > [lang]')].map(w => w.getBoundingClientRect()).filter(r => r.width > 0);
  const l = Math.min(...words.map(r => r.left)), r = Math.max(...words.map(r => r.right)), b = li.getBoundingClientRect();
  return { off: Math.round((l + r) / 2 - (b.left + b.width / 2)), lines: new Set(words.map(r => Math.round(r.top))).size }; }"""


# Multiply: a painting blends with the page root's paper only if no element between it and the root
# makes a stacking context. For each painting (the dots and Dr. Liu's mount multiply nothing) walk
# its ancestors up to, but not including, the root and report what each one makes: a z-index on a
# positioned (or flex/grid item) element, a fixed or sticky position, opacity under 1, a transform
# (including translate, rotate and scale), a filter, a backdrop-filter, a perspective, a clip-path,
# a mask, isolation, a blend mode other than normal, contain: paint (or layout, strict, content),
# content-visibility, a container type, or a will-change that names one of them.
STACKING_JS = """() => {
  const root = document.querySelector('[data-look="ink"]');
  const none = (v) => !v || v === 'none' || v === 'auto' || v === 'normal';
  const makes = (el) => {
    const s = getComputedStyle(el), parent = el.parentElement, why = [];
    const item = parent && /flex|grid/.test(getComputedStyle(parent).display);
    if (s.zIndex !== 'auto' && (s.position !== 'static' || item)) why.push('z-index ' + s.zIndex);
    if (s.position === 'fixed' || s.position === 'sticky') why.push('position ' + s.position);
    if (parseFloat(s.opacity) < 1) why.push('opacity ' + s.opacity);
    for (const [name, value] of [['transform', s.transform], ['translate', s.translate], ['rotate', s.rotate],
        ['scale', s.scale], ['filter', s.filter], ['backdrop-filter', s.backdropFilter], ['perspective', s.perspective],
        ['clip-path', s.clipPath], ['mask', s.maskImage]])
      if (!none(value)) why.push(name + ' ' + value);
    if (s.isolation === 'isolate') why.push('isolation');
    if (s.mixBlendMode !== 'normal') why.push('mix-blend-mode ' + s.mixBlendMode);
    if (/paint|layout|strict|content/.test(s.contain)) why.push('contain ' + s.contain);
    if (s.contentVisibility !== 'visible') why.push('content-visibility ' + s.contentVisibility);
    if (s.containerType !== 'normal') why.push('container-type ' + s.containerType);
    if (/opacity|transform|translate|rotate|scale|filter|perspective|clip-path|mask|mix-blend|isolation|backdrop/.test(s.willChange))
      why.push('will-change ' + s.willChange);
    return why;
  };
  const found = [];
  const paintings = [...document.querySelectorAll('main img')].filter(i => !i.closest('[data-mount]') && !i.matches('[data-dot]'));
  for (const img of paintings) {
    for (let el = img.parentElement; el && el !== root; el = el.parentElement) {
      const why = makes(el);
      if (why.length) found.push([(img.getAttribute('src') || '').slice(-26), el.tagName.toLowerCase() + '.' + String(el.className).split(' ')[0], why.join(', ')]);
    }
    if (!root.contains(img)) found.push([(img.getAttribute('src') || '').slice(-26), 'outside the page root', '']);
  }
  return { paintings: paintings.length, found };
}"""


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


def wait_until(page, expression, timeout=10000):
    """True once the page's expression holds; False when it never does (the checks then report it)."""
    try:
        page.wait_for_function(expression, timeout=timeout)
        return True
    except PlaywrightTimeoutError:
        return False


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


DESIGN = "album"
# Each spread part and the side its picture stands on from 960px (the promise is the centred row).
SIDES = {"opening": "right", "purpose": "left", "roots": "right", "experience": "left", "closing": "right"}
TWO_COLUMNS = 960


def roots_beside(width):
    """Where Dr. Liu's photo stands beside his paragraph (album.module.css): on a tablet's 640px
    column (600 to 959px) and from 1080px. Elsewhere it stands above it."""
    return 600 <= width < TWO_COLUMNS or width >= 1080


# Nothing in a words column reaches past its right edge: each element's box, and the glyphs of the
# text it holds (a pill that cannot wrap ran 18px past the column from 960 to about 1010px when Dr.
# Liu's photo stood beside the paragraph there).
WORDS_FIT_JS = """() => {
  const out = [];
  for (const w of document.querySelectorAll('[data-words]')) {
    const edge = w.getBoundingClientRect().right;
    for (const e of w.querySelectorAll('*')) {
      const b = e.getBoundingClientRect();
      if (!b.width) continue;
      let right = b.right;
      if ([...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) {
        const r = document.createRange(); r.selectNodeContents(e);
        for (const x of r.getClientRects()) if (x.width > 0) right = Math.max(right, x.right);
      }
      if (right > edge + 1) out.push([e.tagName.toLowerCase() + ' ' + (e.textContent || '').trim().slice(0, 20), Math.round(right - edge)]);
    }
  }
  return out;
}"""

RHYTHM_JS = """(sides) => {
  const out = {};
  for (const part of Object.keys(sides)) {
    const p = document.querySelector(`[data-part="${part}"]`);
    if (!p) { out[part] = null; continue; }
    const pics = [...p.querySelectorAll('[data-picture]')], words = [...p.querySelectorAll('[data-words]')];
    const pb = pics[0]?.querySelector('img')?.getBoundingClientRect(), wb = words[0]?.getBoundingClientRect();
    out[part] = { pictures: pics.length, words: words.length,
      side: pb && wb ? ((pb.left + pb.width / 2) < (wb.left + wb.width / 2) ? 'left' : 'right') : null,
      first: pb && wb ? (pb.top < wb.top ? 'picture' : 'words') : null,
      height: pb ? Math.round(pb.height) : 0, captions: [...p.querySelectorAll('[data-picture] figcaption')].map(c => c.textContent.trim()) };
  }
  return out;
}"""

# Words over paintings: glyph rectangles of the page's words against the boxes of its paintings
# (Dr. Liu's photo is not a painting; the promise pictures are).
OVERLAP_JS = """() => {
  const words = [...document.querySelectorAll('main h1, main h2, main h3, main p, main dt, main dd, main a, main button, main figcaption')]
    .filter(e => e.offsetParent && !e.closest('[data-picture]'));
  const art = [...document.querySelectorAll('[data-picture] img, [data-promise] img, [data-picture-band]')].filter(e => e.offsetParent && !e.closest('[data-mount]'));
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

# The name once: nothing in the page but the h1 is set at 56px or larger, and no picture is a
# painted name.
NAME_ONCE_JS = """() => ({
  big: [...document.querySelectorAll('main *')].filter(e => e.offsetParent && e.tagName !== 'H1' && !e.closest('h1')
      && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && parseFloat(getComputedStyle(e).fontSize) >= 56)
    .map(e => [e.textContent.trim().slice(0, 20), getComputedStyle(e).fontSize]),
  painted: [...document.querySelectorAll('main img')].map(i => i.getAttribute('src') || '').filter(s => /word-v[0-9]|letter-[bigh]-v[0-9]/.test(s)) })"""


def desktop_and_phone(browser):
    for width, height in [(1440, 900), (390, 844)]:
        tag = f"{width}x{height}"
        context, page, response, errors, failed = open_page(browser, width, height)
        check(f"{tag} answers 200", response.status == 200, response.status)
        check(f"{tag} the {DESIGN} page", page.evaluate(f"!!document.querySelector('[data-about=\"{DESIGN}\"]')"))
        text = page.evaluate("document.body.innerText")
        missing = [line for line in LOCKED if line not in text]
        check(f"{tag} every locked line", not missing, missing)
        h1 = page.evaluate("[...document.querySelectorAll('h1')].map(h => [h.textContent.trim(), h.lang])")
        check(f"{tag} one English h1", h1 == [["Be in Good Health.", "en"]], h1)
        check(f"{tag} no canvas and no brush layer", page.evaluate("!document.querySelector('main canvas') && !document.querySelector('[data-lifts]')"))
        folds = page.evaluate(
            "[...document.querySelectorAll('[data-part]')].filter(p => getComputedStyle(p, '::before').content !== 'none').length + document.querySelectorAll('[data-sheet]').length"
        )
        check(f"{tag} no folds", folds == 0, folds)
        paper = page.evaluate("getComputedStyle(document.querySelector('[data-look=\"ink\"]')).backgroundImage")
        check(f"{tag} the kit's plain rice paper", "paper.webp" in paper and "aged" not in paper, paper)
        blends = page.evaluate(
            "[...document.querySelectorAll('main img')].filter(i => !i.closest('[data-mount]') && !i.matches('[data-dot]')).map(i => getComputedStyle(i).mixBlendMode)"
        )
        check(f"{tag} paintings multiply", blends and all(b == "multiply" for b in blends), blends)
        stacking = page.evaluate(STACKING_JS)
        check(f"{tag} nothing between a painting and the page root makes a stacking context", stacking["paintings"] > 0 and not stacking["found"], stacking["found"][:4])
        nav = page.evaluate(
            """() => { const n = document.querySelector('#site-navigation'); const sheet = document.querySelector('[data-nav-sheet]');
                 return { current: [...n.querySelectorAll('[aria-current="page"]')].map(a => a.textContent.trim()),
                          menuCurrent: [...sheet.querySelectorAll('[aria-current="page"]')].map(a => a.textContent.trim()) }; }"""
        )
        check(f"{tag} the menu bar marks About", nav["current"] == ["About"] and nav["menuCurrent"] == ["About"], nav)
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
        eager = page.evaluate("(() => { const i = document.querySelector('[data-part=\"opening\"] img'); return i ? i.getAttribute('loading') : 'missing'; })()")
        check(f"{tag} the opening's painting loads eagerly", eager != "lazy" and eager != "missing", eager)
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
        check(f"{tag} Ask sheet opens", "Ask BiGH Science" in page.evaluate("document.querySelector('dialog[open]')?.innerText ?? ''"))
        page.keyboard.press("Escape")
        page.wait_for_timeout(600)
        check(f"{tag} focus returns to Ask", page.evaluate("document.activeElement?.textContent?.trim()") == "Ask BiGH Science")
        page.evaluate("window.scrollTo(0, 0)")
        shots(page, tag, height)
        loaded = page.evaluate("[...document.querySelectorAll('main img')].map(i => i.complete && i.naturalWidth > 0)")
        check(f"{tag} every picture loaded", loaded and all(loaded), loaded)
        check(f"{tag} no console errors or warnings", not errors, errors[:3])
        check(f"{tag} no failed requests", not failed, failed[:3])
        context.close()


def rhythm(browser):
    for width, height in [(1440, 900), (1280, 800), (1080, 800), (1024, 768), (960, 800), (768, 1024), (390, 844)]:
        tag = f"{width}x{height}"
        context, page, response, errors, failed = open_page(browser, width, height, reduced=True)
        r = page.evaluate(RHYTHM_JS, SIDES)
        pairs = {p: v and (v["pictures"], v["words"]) for p, v in r.items()}
        check(f"{tag} every spread part: one picture and its words", all(v == (1, 1) for v in pairs.values()), pairs)
        if width >= TWO_COLUMNS:
            sides = {p: v and v["side"] for p, v in r.items()}
            check(f"{tag} pictures on alternating sides", sides == SIDES, sides)
            heights = sorted(v["height"] for v in r.values() if v)
            median = heights[len(heights) // 2]
            check(f"{tag} the pictures about the same size (0.55-1.6 of the median)", all(0.55 <= h / median <= 1.6 for h in heights), heights)
            over = page.evaluate(WORDS_FIT_JS)
            check(f"{tag} nothing in a words column past its right edge", not over, over[:4])
        else:
            firsts = {p: v and v["first"] for p, v in r.items()}
            check(f"{tag} one column: each picture first", all(f == "picture" for f in firsts.values()), firsts)
        once = page.evaluate(NAME_ONCE_JS)
        check(f"{tag} the name once", not once["big"] and not once["painted"], once)
        captions = {p: v and v["captions"] for p, v in r.items()}
        check(f"{tag} Illustration under each picture", all(c == ["Illustration"] for c in captions.values()), captions)
        row_caption = page.evaluate("document.querySelector('[data-part=\"promise\"] [data-row-caption]')?.textContent.trim() ?? null")
        check(f"{tag} Illustrations under the promise row", row_caption == "Illustrations", row_caption)
        hits = page.evaluate(OVERLAP_JS)
        check(f"{tag} no words over a painting", not hits, hits[:4])
        rows = page.evaluate("new Set([...document.querySelectorAll('[data-promise]')].map(li => Math.round(li.getBoundingClientRect().top / 4))).size")
        want = 1 if width >= 1200 else 2 if width >= 600 else 4
        check(f"{tag} the promises in {want} row(s)", rows == want, rows)
        mount = page.evaluate(
            """() => { const m = document.querySelector('#roots [data-mount]'), w = document.querySelector('#roots [data-words]');
                 const t = document.querySelector('#roots [data-words] p:not([data-label])');
                 if (!m || !w || !t) return null; const a = m.getBoundingClientRect(), b = w.getBoundingClientRect(), c = t.getBoundingClientRect();
                 return { inside: a.left >= b.left - 1 && a.right <= b.right + 1 && a.top >= b.top - 1 && a.bottom <= b.bottom + 1,
                          beside: a.right <= c.left + 1, above: a.bottom <= c.top + 1 }; }"""
        )
        beside = roots_beside(width)
        check(f"{tag} Dr. Liu's photo in his words", bool(mount) and mount["inside"], mount)
        check(
            f"{tag} Dr. Liu's photo {'beside' if beside else 'above'} his paragraph",
            bool(mount) and (mount["beside"] if beside else mount["above"]),
            mount,
        )
        page.screenshot(path=os.path.join(OUT, f"rhythm-{tag}.png"))
        context.close()


def motion(browser):
    # Reduced motion: complete and still.
    context, page, response, errors, failed = open_page(browser, 1440, 900, reduced=True)
    scroll_through(page)
    still = page.evaluate(
        """() => ({ blooms: [...document.querySelectorAll('[data-bloom]')].filter(e => e.dataset.bloom !== 'done').length,
             hidden: [...document.querySelectorAll('main img')].filter(i => parseFloat(getComputedStyle(i).opacity) < 1).length,
             running: document.getAnimations().filter(a => { const t = a.effect && a.effect.target;
               return t && t.closest && t.closest('main') && !t.closest('[class*=greetings]'); }).length })"""
    )
    check("reduced motion: every painting shown, still", still["blooms"] == 0 and still["hidden"] == 0 and still["running"] == 0, still)
    context.close()

    # With motion: the opening's painting blooms on arrival; a lower painting waits, then blooms.
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="no-preference")
    page = context.new_page()
    page.goto(f"{BASE}/about", wait_until="domcontentloaded", timeout=120000)
    marks = page.evaluate("[...document.querySelectorAll('[data-picture] img, [data-promise] img')].map(i => i.dataset.bloom ?? null)")
    check("motion: every painting server-marked waiting (none paints whole, then vanishes)", len(marks) == 9 and all(m == "waiting" for m in marks), marks)
    first = page.evaluate("document.querySelector('[data-part=\"opening\"] img').dataset.bloom ?? null")
    check("motion: the opening's painting starts waiting (server-marked)", first == "waiting", first)
    check("motion: the opening's painting blooms", wait_until(page, "document.querySelector('[data-part=\"opening\"] img').dataset.bloom === 'done'"))
    low = "document.querySelector('[data-part=\"experience\"] [data-picture] img')"
    state = page.evaluate(f"[{low}.dataset.bloom ?? null, getComputedStyle({low}).opacity]")
    check("motion: a lower painting waits out of view, hidden", state[0] == "waiting" and float(state[1]) == 0, state)
    page.evaluate(f"(() => {{ const i = {low}; window.scrollTo(0, i.getBoundingClientRect().top + window.scrollY - innerHeight / 2); }})()")
    check("motion: then it blooms", wait_until(page, f"{low}.dataset.bloom === 'done'"))
    context.close()

    # JavaScript off: every painting shows (nothing waits for a bloom that will not come).
    context = browser.new_context(viewport={"width": 1440, "height": 900}, java_script_enabled=False)
    page = context.new_page()
    page.goto(f"{BASE}/about", wait_until="load", timeout=120000)
    page.wait_for_timeout(1500)
    box = page.locator('[data-part="opening"] img').bounding_box()
    shot = Image.open(io.BytesIO(page.screenshot(clip=box))).convert("L")
    ink = sum(shot.histogram()[:180]) / (shot.width * shot.height)
    check("JavaScript off: the opening's painting is visible", ink >= 0.02, round(ink, 4))
    context.close()


def boundary(browser):
    for width in (959, 960):
        context, page, response, errors, failed = open_page(browser, width, 900, reduced=True)
        sideways = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
        check(f"{width} no sideways scrolling", sideways <= 0, sideways)
        r = page.evaluate(RHYTHM_JS, SIDES)
        if width == 959:
            firsts = {p: v and v["first"] for p, v in r.items()}
            check("959 one column: each picture first", all(f == "picture" for f in firsts.values()), firsts)
        else:
            sides = {p: v and v["side"] for p, v in r.items()}
            check("960 two columns: pictures on alternating sides", sides == SIDES, sides)
        context.close()


def first_screen(browser):
    for width, height in [(1280, 720), (1440, 900), (1536, 864), (390, 844)]:
        tag = f"{width}x{height}"
        context, page, response, errors, failed = open_page(browser, width, height, reduced=True)
        geo = page.evaluate(
            """() => ({ title: document.querySelector('h1').getBoundingClientRect().bottom,
                        picture: document.querySelector('[data-part="opening"] img').getBoundingClientRect().top, win: innerHeight })"""
        )
        check(f"{tag} the title and the top of the opening's picture in the first screen", geo["title"] <= geo["win"] and geo["picture"] < geo["win"], geo)
        context.close()


# --only=rhythm,boundary runs just those groups (while working on one thing); the full run is the gate.
GROUPS = [desktop_and_phone, rhythm, motion, focus, boundary, first_screen]
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

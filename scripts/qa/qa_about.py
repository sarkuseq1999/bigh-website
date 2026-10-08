"""QA for About C, "The circle" (Mo, October 7, 2026; mockup reference/ink-pages/mockups/about-c.png;
spec docs/superpowers/specs/2026-10-05-ink-pages-design.md, "About (stage 1), October 7").

desktop_and_phone (1440x900, 390x844): 200; no console errors or warnings (but PREFETCH_CSS); no
failed requests; one h1, English "Be in Good Health." with lang="en"; every locked line in the
page's main (the footer's "About BiGH" does not stand in for the opening's label); no canvas,
no brush layer, no folds, no aged paper; every painting multiplies and nothing between a painting
and the page root makes a stacking context; the menu bar marks About; no sideways scrolling; text
15px+, navigation 18px+, targets 48px+; the opening's circle loads eagerly; the Support and Ask
sheets open, close and hand focus back.
rhythm (1440x900, 1280x800, 1080x800, 1024x768, 960x800, 768x1024, 390x844): every spread part has
one picture and its words; on two columns (from 960px) the pictures stand purpose left, roots
right, experience left, closing right (the opening is centred), and are about the same size, and
nothing in a words column reaches past its right edge; on one column each picture comes first; the
name once (nothing in the page but the h1 at 56px or larger, no painted name); "Illustration" under
the purpose, experience and closing paintings, none under Dr. Liu's photo or the promise dots; no
words over a painting; four promises in one row from 1200px, two by two from 600px, one column
below; Dr. Liu's photo in the middle of its pool; the circle appears once. In Vietnamese at 360,
600, 960, 1080 and 1200px (the longest pill label, "Gặp các nhà khoa học", once ran past its
column) nothing in a words column reaches past its right edge.
motion: reduced motion complete and still (the circle whole, its gold up, every painting shown);
every painting is server-marked waiting (none paints whole, then vanishes); with motion the circle
paints itself around in one breath from where the brush began (stopped in the frame its clock
reaches 1.1s it is part drawn: the first two quarters whole, the one reached last under half of
its ink; then it ends whole), then its gold comes up, and the hills bloom; a lower painting waits,
then blooms; with JavaScript off the circle shows whole, and every other painting (the hills, the
seedling, the pool, the sequoia, the four promise dots and the glasses) as inked as it does still.
focus: Skip to content puts focus at the words; with pictures blocked every heading and paragraph
is visible.
deep_links (1440x900, 1024x768, 768x1024, 390x844, 360x780): /about#purpose, #roots, #experience,
#promise, #closing land the part's first content 0-64px under the header, its heading in the window.
languages (kr, jp, cns, vn): 200, no console errors, the h1 English, no English source sentence
left, the paintings' descriptions translated.
languages_layout (every language at 1440x900, 1024x768, 768x1024, 600x900, 390x844, 360x780; jp and
cns also 960x900): no word crosses the side margins; no words over a painting; in kr, jp, cns, vn no
bad line break; jp and cns heading phrases whole on a phone and at 960 (the narrowest two-column
words column, 377px); Vietnamese at 390: the closing pills balance their lines.
nav_locales: from /vn/about and /kr/about the bar and menu stay in the language.
greetings (1440x900, 390x844, and /kr/about at 390x844): with motion the five greetings play one
word at a time, never two visible in the same frame, each wholly in once, ending on the visitor's
own language, in under five seconds.
boundary (959x900, 960x900): no sideways scrolling; one column at 959 (picture first), two at 960.
first_screen (1280x720, 1440x900, 1536x864, 390x844): the title and the top of the opening's circle
in the first screen.

Pictures: scripts/qa/out/about-circle/<size>-NN.png.

Usage: python -X utf8 scripts/qa/qa_about.py [base-url] [--only=desktop_and_phone,rhythm,motion,focus,deep_links,languages,languages_layout,nav_locales,greetings,boundary,first_screen]
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
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "about-circle")
os.makedirs(OUT, exist_ok=True)
results = []

# The locked words (src/components/about/about-content.ts), as they appear on the page. They are
# read from the page's main: the footer also says "About BiGH".
LOCKED = [
    "About BiGH",
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


# Hello in five languages (the fourth promise), read still (reduced motion: all five shown): the
# words' box against its promise (off: its centre's offset from the promise's centre; start: its
# left edge's offset from the promise's title), its lines, and whether it stands under the
# promise's words.
GREETINGS_JS = """() => { const li = document.querySelectorAll('[data-promise]')[3];
  const words = [...li.querySelectorAll('[aria-hidden="true"] > [lang]')].map(w => w.getBoundingClientRect()).filter(r => r.width > 0);
  const l = Math.min(...words.map(r => r.left)), r = Math.max(...words.map(r => r.right)), b = li.getBoundingClientRect();
  const h = li.querySelector('h3').getBoundingClientRect(), p = li.querySelector('p').getBoundingClientRect();
  return { off: Math.round((l + r) / 2 - (b.left + b.width / 2)), start: Math.round(l - h.left),
           lines: new Set(words.map(r => Math.round(r.top))).size, under: Math.min(...words.map(r => r.top)) >= p.bottom - 1 }; }"""

# The greetings play (motion): every animation frame for 7s from scrolling the fourth promise into
# view, the opacity of each of the five words. most: the most words visible (over 0.02) in any one
# frame, and that frame; full: the words that were wholly in (0.99) at some frame; final: the words
# in at the end; began and settled: the first and last frames in which anything changed.
GREETINGS_PLAY_JS = """() => new Promise((resolve) => {
  const li = document.querySelectorAll('[data-promise]')[3];
  const words = [...li.querySelectorAll('[aria-hidden="true"] > [lang]')];
  const t0 = performance.now(), full = new Set();
  let most = 0, at = null, prev = null, began = null, settled = null, ops = [];
  const tick = () => {
    const t = Math.round(performance.now() - t0);
    ops = words.map(w => parseFloat(getComputedStyle(w).opacity));
    const shown = ops.filter(o => o > 0.02).length;
    if (shown > most) { most = shown; at = { t, ops: ops.map(o => +o.toFixed(2)) }; }
    ops.forEach((o, i) => { if (o >= 0.99) full.add(words[i].lang); });
    const key = ops.map(o => o.toFixed(3)).join(',');
    if (prev !== null && key !== prev) { if (began === null) began = t; settled = t; }
    prev = key;
    if (t < 7000) requestAnimationFrame(tick);
    else resolve({ most, at, full: [...full], final: words.filter((w, i) => ops[i] >= 0.99).map(w => w.lang), began, settled });
  };
  window.scrollTo(0, li.getBoundingClientRect().top + scrollY - innerHeight / 2);
  requestAnimationFrame(tick);
})"""

# On a phone each promise is a row: its picture at the left, its title and words beside it,
# left-aligned. For each promise: the picture's width, its right edge against the title's left
# edge, its top against the title's top, the title's and the words' left edges and alignment; the
# gaps between rows; and the part's heading's left edge against the list's.
PROMISE_ROWS_JS = """() => {
  const items = [...document.querySelectorAll('[data-promise]')];
  const rows = items.map(li => { const i = li.querySelector('img').getBoundingClientRect(), h = li.querySelector('h3'), p = li.querySelector('p');
    const hb = h.getBoundingClientRect(), pb = p.getBoundingClientRect();
    return { pic: Math.round(i.width), beside: i.right <= hb.left + 1, top: Math.round(i.top - hb.top),
             aligned: Math.abs(hb.left - pb.left) <= 1, align: getComputedStyle(h).textAlign + '/' + getComputedStyle(p).textAlign }; });
  const gaps = items.slice(1).map((li, k) => Math.round(li.getBoundingClientRect().top - items[k].getBoundingClientRect().bottom));
  const head = document.getElementById('promise-title').getBoundingClientRect();
  return { rows, gaps, head: Math.round(head.left - items[0].getBoundingClientRect().left) };
}"""


def greetings(browser):
    """The greetings under the fourth promise play once with motion, one word at a time: in no frame
    are two words visible at once (the crossfade set "Xin chào" over "안녕하세요"), every word is
    wholly in at some point, the play ends on the visitor's own language and lasts under five
    seconds (so it needs no pause button). At a desktop and a phone size, in English and Korean."""
    for width, height, path, own in [(1440, 900, "/about", "en"), (390, 844, "/about", "en"), (390, 844, "/kr/about", "ko")]:
        tag = f"{path} {width}x{height}"
        context = browser.new_context(viewport={"width": width, "height": height}, reduced_motion="no-preference")
        page = context.new_page()
        page.goto(f"{BASE}{path}", wait_until="networkidle", timeout=120000)
        page.evaluate("document.fonts.ready.then(() => true)")
        page.wait_for_timeout(600)
        play = page.evaluate(GREETINGS_PLAY_JS)
        check(f"{tag} greetings: never two words visible at once", play["most"] == 1, play)
        check(f"{tag} greetings: all five words shown, each wholly in", len(play["full"]) == 5, play["full"])
        check(f"{tag} greetings: it ends on the visitor's own language", play["final"] == [own], play["final"])
        span = None if play["began"] is None else play["settled"] - play["began"]
        check(f"{tag} greetings: the play lasts under five seconds ({span}ms)", span is not None and 3000 <= span < 5000, play)
        context.close()


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


# No heading phrase is broken across lines (Japanese and Chinese, on a phone and at 960px, where the
# words column is narrowest: two columns start there, 377px of words; at 900px one column is 640px). What a heading keeps whole is a phrase: in Chinese the words between
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


DESIGN = "circle"
# Each spread part and the side its picture stands on from 960px (the opening's circle and the
# promise row are centred).
SIDES = {"purpose": "left", "roots": "right", "experience": "left", "closing": "right"}
TWO_COLUMNS = 960


# Nothing in a words column reaches past its right edge: each element's box, and the glyphs of the
# text it holds (in the album a pill that cannot wrap ran 17px past the column from 960 to about
# 1010px, where Dr. Liu's photo stood beside the paragraph).
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
        text = page.evaluate("document.querySelector('main').innerText")
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
        eager = page.evaluate("(() => { const i = document.querySelector('[data-enso] img'); return i ? i.getAttribute('loading') : 'missing'; })()")
        check(f"{tag} the opening's circle loads eagerly", eager != "lazy" and eager != "missing", eager)
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
        want_captions = {"purpose": ["Illustration"], "roots": [], "experience": ["Illustration"], "closing": ["Illustration"]}
        check(f"{tag} Illustration under each painting that pictures something", captions == want_captions, captions)
        row_caption = page.evaluate("document.querySelector('[data-part=\"promise\"] [data-row-caption]')?.textContent.trim() ?? null")
        check(f"{tag} no caption under the promise dots", row_caption is None, row_caption)
        hits = page.evaluate(OVERLAP_JS)
        check(f"{tag} no words over a painting", not hits, hits[:4])
        rows = page.evaluate("new Set([...document.querySelectorAll('[data-promise]')].map(li => Math.round(li.getBoundingClientRect().top / 4))).size")
        want = 1 if width >= 1200 else 2 if width >= 600 else 4
        check(f"{tag} the promises in {want} row(s)", rows == want, rows)
        hello = page.evaluate(GREETINGS_JS)
        if width >= 600:
            check(f"{tag} Hello in five languages centred under the fourth promise", abs(hello["off"]) <= 2 and hello["under"] and hello["lines"] <= 2, hello)
        else:
            # A phone's promises are a list of rows (they were centred posters, two and a half
            # screens of them): this replaces nothing; the rows themselves are new.
            check(f"{tag} Hello in five languages under the fourth promise's words, at their left edge", abs(hello["start"]) <= 1 and hello["under"] and hello["lines"] <= 2, hello)
            lst = page.evaluate(PROMISE_ROWS_JS)
            check(
                f"{tag} each promise a row: its picture (56-72px) at the left, beside its title, at the row's top",
                all(56 <= r["pic"] <= 72 and r["beside"] and abs(r["top"]) <= 4 for r in lst["rows"]),
                lst["rows"],
            )
            check(
                f"{tag} the promises' titles and words left-aligned, one edge",
                all(r["aligned"] and r["align"] in ("left/left", "start/start") for r in lst["rows"]),
                lst["rows"],
            )
            check(f"{tag} the promise rows evenly spaced", len(lst["gaps"]) == 3 and max(lst["gaps"]) - min(lst["gaps"]) <= 1, lst["gaps"])
            check(f"{tag} the promise heading at the list's left edge", abs(lst["head"]) <= 1, lst["head"])
        liu = page.evaluate(
            """() => { const p = document.querySelector('[data-pool]'), f = document.querySelector('[data-mount] img');
                 if (!p || !f) return null; const a = p.getBoundingClientRect(), b = f.getBoundingClientRect();
                 return { dx: (b.left + b.width / 2 - a.left - a.width / 2) / a.width, dy: (b.top + b.height / 2 - a.top - a.height / 2) / a.height }; }"""
        )
        check(f"{tag} Dr. Liu's photo in the middle of its pool", liu is not None and abs(liu["dx"]) <= 0.15 and abs(liu["dy"]) <= 0.15, liu)
        # The pool is a light, wide, low wash the photo rests on (it was a dark round blob about as
        # tall as the photo): at least 1.8 times as wide as it is tall and 2.4 times the photo's
        # width, at least as tall as the photo, at 0.6 to 0.75 of its ink.
        wash = page.evaluate(
            """() => { const p = document.querySelector('[data-pool]'), m = document.querySelector('[data-mount]');
                 const a = p.getBoundingClientRect(), b = m.getBoundingClientRect();
                 return { shape: +(a.width / a.height).toFixed(2), wide: +(a.width / b.width).toFixed(2), tall: +(a.height / b.height).toFixed(2),
                          opacity: parseFloat(getComputedStyle(p).opacity) }; }"""
        )
        check(f"{tag} Dr. Liu's pool light, wide and low", wash["shape"] >= 1.8 and wash["wide"] >= 2.4 and wash["tall"] >= 1 and 0.6 <= wash["opacity"] <= 0.75, wash)
        # The stroke only: "enso" alone also matches its gold start, enso-dot-v1.webp.
        once_circle = page.evaluate("document.querySelectorAll('main img[src*=\"enso-v\"]').length")
        check(f"{tag} the circle appears once", once_circle == 1, once_circle)
        page.screenshot(path=os.path.join(OUT, f"rhythm-{tag}.png"))
        context.close()
    # The pill labels differ by language: the Vietnamese "Gặp các nhà khoa học" is the longest (in
    # the album, beside Dr. Liu's photo, it ran 22px past the words column at 1080px). Here the
    # words column holds no photo; the pill must fit it on a phone, on a tablet's column, at the
    # narrowest two columns (960px) and wider.
    for width in (360, 600, 960, 1080, 1200):
        context, page, response, errors, failed = open_page(browser, width, 800, path="/vn/about", reduced=True)
        over = page.evaluate(WORDS_FIT_JS)
        check(f"vn {width}x800 nothing in a words column past its right edge", not over, over[:4])
        context.close()


# The page's paintings but the circle: the hills, the seedling, the pool under Dr. Liu's photo (not
# the photo), the sequoia, the four promise dots and the glasses.
PAINTINGS = "[data-picture-band], [data-picture] img:not([data-mount] img), [data-promise] img"


def inks(page):
    """Each painting's ink, in page order: the share of its pixels darker than 215. Dr. Liu's
    photo, which lies on the pool, is left out (with 16px round it for its shadow): it would count
    as the pool's ink even with the pool hidden."""
    out = []
    pictures = page.locator(PAINTINGS)
    for i in range(pictures.count()):
        picture = pictures.nth(i)
        picture.scroll_into_view_if_needed()
        page.wait_for_timeout(400)
        shot = Image.open(io.BytesIO(picture.screenshot())).convert("L")
        box, keep = picture.bounding_box(), None
        mount = page.locator("[data-mount]").bounding_box()
        if mount and box:
            sx, sy = shot.width / box["width"], shot.height / box["height"]
            x0, y0 = int((mount["x"] - 16 - box["x"]) * sx), int((mount["y"] - 16 - box["y"]) * sy)
            x1, y1 = int((mount["x"] + mount["width"] + 16 - box["x"]) * sx), int((mount["y"] + mount["height"] + 16 - box["y"]) * sy)
            if x1 > 0 and y1 > 0 and x0 < shot.width and y0 < shot.height:
                keep = Image.new("L", shot.size, 255)
                keep.paste(0, (max(0, x0), max(0, y0), min(shot.width, x1), min(shot.height, y1)))
        counts = shot.histogram(mask=keep)
        name = (picture.get_attribute("src") or "").split("%2F")[-1].split(".webp")[0]
        out.append((name, round(sum(counts[:215]) / max(1, sum(counts)), 4)))
    return out


def motion(browser):
    # Reduced motion: complete and still. Every picture at its full strength: opacity 1, but the
    # pool under Dr. Liu's photo, which lies at 0.7 by design (a light wash; circle.module.css), so
    # it must be at least that.
    context, page, response, errors, failed = open_page(browser, 1440, 900, reduced=True)
    scroll_through(page)
    still = page.evaluate(
        """() => { const e = document.querySelector('[data-enso] img'), d = document.querySelector('[data-enso] [data-dot]');
             return { blooms: [...document.querySelectorAll('[data-bloom]')].filter(x => x.dataset.bloom !== 'done').length,
                      hidden: [...document.querySelectorAll('main img')].filter(i => parseFloat(getComputedStyle(i).opacity) < (i.matches('[data-pool]') ? 0.7 : 1)).length,
                      pool: getComputedStyle(document.querySelector('[data-pool]')).opacity,
                      draw: getComputedStyle(e).animationName, mask: getComputedStyle(e).maskImage, dot: getComputedStyle(d).opacity,
                      running: document.getAnimations().filter(a => { const t = a.effect && a.effect.target;
                        return t && t.closest && t.closest('main') && !t.closest('[class*=greetings]'); }).length }; }"""
    )
    check("reduced motion: the circle whole, its gold up, every painting shown, still",
          still["blooms"] == 0 and still["hidden"] == 0 and still["draw"] == "none" and still["mask"] == "none"
          and float(still["dot"]) == 1 and still["running"] == 0, still)
    context.close()

    # With motion: the circle paints itself in one breath, then its gold; the hills bloom.
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="no-preference")
    # Every painting server-marked waiting (none paints whole, then vanishes), read from the HTML
    # the server sends, before any script could mark one: in the page's main, the hills, the
    # seedling, the pool, the sequoia, the four promise dots and the glasses (the circle draws
    # itself instead; the shared closing crane after main is the kit's own).
    html = context.request.get(f"{BASE}/about").text()
    main = html[html.index("<main"):html.index("</main>")]
    marks = re.findall(r'<img[^>]*?\sdata-bloom="([^"]*)"', main)
    check("motion: every painting server-marked waiting (none paints whole, then vanishes)", len(marks) == 9 and all(m == "waiting" for m in marks), marks)
    page = context.new_page()
    page.goto(f"{BASE}/about", wait_until="domcontentloaded", timeout=120000)
    wait_until(page, "getComputedStyle(document.querySelector('[data-enso] img')).animationName !== 'none'", 5000)
    early = page.evaluate(
        """() => { const e = getComputedStyle(document.querySelector('[data-enso] img'));
             return { name: e.animationName, duration: e.animationDuration, start: e.getPropertyValue('--start').trim(),
                      dot: getComputedStyle(document.querySelector('[data-enso] [data-dot]')).opacity,
                      delay: parseFloat(getComputedStyle(document.querySelector('[data-enso] [data-dot]')).animationDelay) }; }"""
    )
    check("motion: the circle paints itself (its animation, one breath, from where the brush began)",
          "draw" in early["name"] and early["duration"] == "2.4s" and early["start"].endswith("deg"), early)
    check("motion: its gold waits for the stroke", float(early["dot"]) < 0.5 and early["delay"] >= 2.4, early)
    check("motion: then the gold is up", wait_until(page, "getComputedStyle(document.querySelector('[data-enso] [data-dot]')).opacity === '1'"))
    check("motion: the hills bloom", wait_until(page, "document.querySelector('[data-picture-band]').dataset.bloom === 'done'"))
    low = "document.querySelector('[data-part=\"experience\"] [data-picture] img')"
    state = page.evaluate(f"[{low}.dataset.bloom ?? null, getComputedStyle({low}).opacity]")
    check("motion: a lower painting waits out of view, hidden", state[0] == "waiting" and float(state[1]) == 0, state)
    page.evaluate(f"(() => {{ const i = {low}; window.scrollTo(0, i.getBoundingClientRect().top + window.scrollY - innerHeight / 2); }})()")
    check("motion: then it blooms", wait_until(page, f"{low}.dataset.bloom === 'done'"))
    context.close()

    # The circle's ink, by quarter in the order the stroke draws them (clockwise from the top
    # right: top right, bottom right, bottom left, top left): the share of each quarter's pixels
    # that is dark. The still circle (reduced motion: no mask at all, its gold up) is the whole one.
    def circle_shot(reduced):
        context = browser.new_context(viewport={"width": 1440, "height": 900}, java_script_enabled=False,
                                      reduced_motion="reduce" if reduced else "no-preference")
        page = context.new_page()
        page.goto(f"{BASE}/about", wait_until="load", timeout=120000)
        page.wait_for_timeout(1500 if reduced else 4000)
        box = page.locator("[data-enso] img:not([data-dot])").bounding_box()
        shot = Image.open(io.BytesIO(page.screenshot(clip=box))).convert("L")
        context.close()
        return shot

    def quarters(shot):
        w, h = shot.size
        boxes = [(w // 2, 0, w, h // 2), (w // 2, h // 2, w, h), (0, h // 2, w // 2, h), (0, 0, w // 2, h // 2)]
        return [round(sum(shot.crop(b).histogram()[:200]) / ((b[2] - b[0]) * (b[3] - b[1])), 4) for b in boxes]

    still_circle = quarters(circle_shot(True))

    # The stroke really progresses (a mask that never sweeps would pass "its animation runs" with
    # the circle whole from the first frame, or blank to the end). The animation runs in real time;
    # the page stops it (and the gold's) in the frame its clock first reaches 1.1s, which counts
    # its 0.3s delay (1.1s in, about 255 degrees are drawn), so the shot is the same on a slow
    # machine. Then the circle must be partly drawn in order: the first two quarters whole, the
    # one the stroke reaches last (top left) under half. Then it runs on and ends whole.
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="no-preference")
    page = context.new_page()
    page.goto(f"{BASE}/about", wait_until="domcontentloaded", timeout=120000)
    wait_until(page, "getComputedStyle(document.querySelector('[data-enso] img')).animationName !== 'none'", 5000)
    stopped = page.evaluate(
        """() => new Promise((resolve) => {
             const wrap = document.querySelector('[data-enso]');
             const draw = wrap.querySelector('img:not([data-dot])').getAnimations()[0];
             if (!draw) return resolve(null);
             const began = performance.now();
             const tick = () => {
               if (Number(draw.currentTime) >= 1100) {
                 wrap.getAnimations({ subtree: true }).forEach((a) => a.pause());
                 return resolve(Math.round(Number(draw.currentTime)));
               }
               if (performance.now() - began > 8000) return resolve(null);
               requestAnimationFrame(tick);
             };
             tick();
           })"""
    )
    box = page.locator("[data-enso] img:not([data-dot])").bounding_box()
    midway = quarters(Image.open(io.BytesIO(page.screenshot(clip=box))).convert("L"))
    check("motion: the stroke is part drawn 1.1s in (first quarters whole, the last under half)",
          stopped is not None and midway[0] >= 0.9 * still_circle[0] and midway[1] >= 0.9 * still_circle[1]
          and midway[3] <= 0.5 * still_circle[3],
          {"clock_ms": stopped, "midway": midway, "still": still_circle})
    page.evaluate("document.querySelector('[data-enso]').getAnimations({ subtree: true }).forEach((a) => a.play())")
    wait_until(page, "getComputedStyle(document.querySelector('[data-enso] [data-dot]')).opacity === '1'")
    page.wait_for_timeout(400)
    end = quarters(Image.open(io.BytesIO(page.screenshot(clip=box))).convert("L"))
    check("motion: then the stroke ends whole (each quarter as inked as the still circle)",
          all(e >= 0.97 * s for e, s in zip(end, still_circle)), {"end": end, "still": still_circle})
    context.close()

    # JavaScript off: the circle shows whole (its stroke is pure CSS). Visible is not whole: half
    # drawn, the circle's ink already passes the visible floor (0.097 at 600ms). So each quarter of
    # it must also hold as much ink as the still circle's. The sweep ends in the top half: the
    # top-left quarter held 0.38 of its ink at 1.5s, the top-right 0.94 at 2.2s (the few degrees
    # before the wet head come last); whole, both match exactly.
    shot = circle_shot(False)
    ink = sum(shot.histogram()[:120]) / (shot.width * shot.height)
    check("JavaScript off: the circle is visible", ink >= 0.04, round(ink, 4))
    drawn = quarters(shot)
    check("JavaScript off: the circle shows whole (each quarter as inked as the still circle)",
          all(d >= 0.97 * s for d, s in zip(drawn, still_circle)), {"drawn": drawn, "still": still_circle})

    # JavaScript off: every other painting shows too (nothing waits for a bloom that will not come).
    # Each one's ink (the share of its pixels darker than 215: the hills and the palest dot are
    # light wash) is read on the page with script off and on the still page (reduced motion, read
    # to the end, every bloom done); with script off each holds at least 0.9 of its still ink. A
    # painting left hidden holds none, one stuck in its blot only part of it.
    context, page, response, errors, failed = open_page(browser, 1440, 900, reduced=True)
    scroll_through(page)
    still = inks(page)
    context.close()
    context = browser.new_context(viewport={"width": 1440, "height": 900}, java_script_enabled=False)
    page = context.new_page()
    page.goto(f"{BASE}/about", wait_until="load", timeout=120000)
    page.wait_for_timeout(1500)
    off = inks(page)
    context.close()
    faint = [(name, ink, s) for (name, ink), (_, s) in zip(off, still) if ink < 0.9 * s]
    check(
        "JavaScript off: every painting shows (each as inked as it is still)",
        len(off) == 9 and len(still) == 9 and all(s >= 0.01 for _, s in still) and not faint,
        {"faint": faint, "off": off, "still": still},
    )


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
                        picture: document.querySelector('[data-enso] img').getBoundingClientRect().top, win: innerHeight })"""
        )
        check(f"{tag} the title and the top of the opening's circle in the first screen", geo["title"] <= geo["win"] and geo["picture"] < geo["win"], geo)
        context.close()


LANDING_JS = """(id) => {
  const s = document.getElementById(id);
  const tops = [...s.querySelectorAll('[data-picture], [data-label], h2')].filter(e => e.offsetParent).map(e => e.getBoundingClientRect().top);
  const head = document.getElementById(id + '-title').getBoundingClientRect();
  const bar = document.querySelector('header').getBoundingClientRect();
  return { scrollY: Math.round(window.scrollY), bar: Math.round(bar.bottom), first: Math.round(Math.min(...tops)),
           headTop: Math.round(head.top), headBottom: Math.round(head.bottom), win: window.innerHeight };
}"""


def deep_links(browser):
    # One browser context per size: a first visit warms the fonts into the cache, then every deep
    # link is a fresh load.
    for width, height in [(1440, 900), (1024, 768), (768, 1024), (390, 844), (360, 780)]:
        context = browser.new_context(viewport={"width": width, "height": height}, reduced_motion="no-preference")
        warm = context.new_page()
        warm.goto(f"{BASE}/about", wait_until="networkidle", timeout=120000)
        warm.evaluate("document.fonts.ready.then(() => true)")
        warm.close()
        for anchor in ["purpose", "roots", "experience", "promise", "closing"]:
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
        h1 = page.evaluate("[document.querySelector('h1').textContent.trim(), document.querySelector('h1').lang]")
        check(f"{lang} the h1 stays English", h1 == ["Be in Good Health.", "en"], h1)
        text = page.evaluate("document.querySelector('main').innerText")
        left = [line for line in english if line in text]
        check(f"{lang} no English sentence left", not left, left[:3])
        alts = page.evaluate("[...document.querySelectorAll('[data-picture] img')].map(i => i.alt).filter(a => a)")
        check(f"{lang} the paintings' descriptions translated", alts and not any(" painted in ink" in a or a.startswith("An ") or a.startswith("A ") for a in alts), alts)
        check(f"{lang} no console errors or warnings", not errors, errors[:3])
        page.screenshot(path=os.path.join(OUT, f"{lang}-opening.png"))
        context.close()


def languages_layout(browser):
    """Each language at desktop, tablet and phone sizes: no word crosses the side margins, no
    words over a painting, and in Korean, Japanese, Chinese and Vietnamese no bad line break.
    Japanese and Chinese also at 960x900 (two columns start at 960px, the narrowest words column),
    and on a phone and at 960px no heading phrase is split."""
    for lang in ["en", "kr", "jp", "cns", "vn"]:
        sizes = [(1440, 900), (1024, 768), (768, 1024), (600, 900), (390, 844), (360, 780)]
        if lang in ("jp", "cns"):
            sizes.append((960, 900))
        for width, height in sizes:
            tag = f"{lang} {width}x{height}"
            path = "/about" if lang == "en" else f"/{lang}/about"
            context, page, response, errors, failed = open_page(browser, width, height, path=path, reduced=True)
            over = page.evaluate(MARGINS_JS)
            check(f"{tag} words inside the margins", not over, over[:3])
            hits = page.evaluate(OVERLAP_JS)
            check(f"{tag} no words over a painting", not hits, hits[:3])
            if lang != "en":
                bad = page.evaluate(BREAKS_JS, lang)
                check(f"{tag} no bad line break", not bad, bad[:3])
            if lang in ("jp", "cns") and width in (390, 360, 960):
                phrases = page.evaluate(PHRASES_JS, lang)
                check(
                    f"{tag} no heading phrase is broken across lines ({phrases['examined']} read)",
                    phrases["examined"] > 0 and not phrases["split"],
                    phrases,
                )
            if lang == "vn" and width == 390:
                pills = page.evaluate(
                    """[...document.querySelectorAll('main [class*=actions] a, main [class*=actions] button')].map(e => {
                         const r = document.createRange(); r.selectNodeContents(e);
                         const widths = {}; for (const x of r.getClientRects()) if (x.width > 4) widths[Math.round(x.top)] = (widths[Math.round(x.top)] || 0) + x.width;
                         return { wrap: getComputedStyle(e).textWrap, widths: Object.values(widths).map(Math.round) }; })"""
                )
                check(f"{tag} closing pills balance their lines (computed text-wrap)", len(pills) == 2 and all(p["wrap"] == "balance" for p in pills), pills)
                two = [p["widths"] for p in pills if len(p["widths"]) == 2]
                check(f"{tag} the pill's two lines are even", not two or all(min(w) / max(w) >= 0.6 for w in two), pills)
            context.close()


# --only=rhythm,boundary runs just those groups (while working on one thing); the full run is the gate.
GROUPS = [desktop_and_phone, rhythm, motion, focus, deep_links, languages, languages_layout, nav_locales, greetings, boundary, first_screen]
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

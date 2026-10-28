"""QA for About C (Mo, October 7, 2026; mockup reference/ink-pages/mockups/about-c.png; spec
docs/superpowers/specs/2026-10-05-ink-pages-design.md, "About (stage 1), October 7"), opened by the
poppy meadow since October 28, 2026 (it replaced the ink circle; Mo picked A "Superbloom", then A
"the meadow thins out": reference/ink-pages/about-opening/README.md).

desktop_and_phone (1440x900, 390x844): 200; no console errors or warnings (but PREFETCH_CSS); no
failed requests; one h1, English "Be in Good Health." with lang="en"; every locked line in the
page's main (the footer's "About BiGH" does not stand in for the opening's label); no canvas,
no brush layer, no folds, no aged paper; every painting multiplies (but the meadow, whose paper is
cut to transparency) and nothing between a painting and the page root makes a stacking context;
the menu bar marks About; no sideways scrolling; text 15px+, navigation 18px+, targets 48px+; the
mission 21px+ and in ink; the meadow loads at once, the painting with high priority; Support is a
link to its page; the Ask sheet opens, closes and hands focus back.
rhythm (1440x900, 1280x800, 1080x800, 1024x768, 960x800, 768x1024, 390x844): every spread part has
one picture and its words; on two columns (from 960px) the pictures stand purpose left, roots
right, experience left, closing right (the opening is centred), and are about the same size but
the purpose's oak, which stands larger (1.0-1.8 of the others' average), and
nothing in a words column reaches past its right edge; on one column each picture comes first; the
name once (nothing in the page but the h1 at 56px or larger, no painted name); "Illustration" under
the purpose, experience and closing paintings, none under Dr. Liu's photo or the promise dots; no
words over a painting; four promises in one row from 1200px, two by two from 600px, one column
below; Dr. Liu's photo in the middle of its pool; the meadow appears once. In Vietnamese at 360,
600, 960, 1080 and 1200px (the longest pill label, "Gặp các nhà khoa học", once ran past its
column) nothing in a words column reaches past its right edge.
motion: reduced motion complete and still (the meadow and its gold whole, no mask, every painting
shown); every painting below the opening is server-marked waiting (none paints whole, then
vanishes); with motion the meadow's gold arrives (3.4s after 0.4s), spreading from the foot of the
first screen: stopped 1.4s in, it holds under half of its gold, most of it in the screen's lower
half; stopped 1.7s in, more, not yet all; then all of it; a lower painting waits, then blooms; on a
slow link (the gold's picture held 3s) the meadow shows at once and its gold waits: 2.5s in none,
the gold starts only once its picture is in and arrives whole; with no gold picture, 9s in it
still holds; with JavaScript off the meadow shows with all its gold, and every other painting (the
oak, the pool, the sequoia, the four promise dots and the glasses) as inked as it does still.
meadow_layout (Mo, October 28, 2026: the meadow thins out into the paper before Our purpose). At
1920x1000, 1440x900, 1280x720, 1024x768, 768x1024, 600x900, 390x844 and 360x780: the painting
spans the window; the words centred, no ink within 8px of them; the meadow fills the first
screen's foot (no bare band, no edge); below it the painting ends in bare paper (its last 12px
hold no ink) and its last strokes stand above Our purpose's first content; no sideways
scrolling.
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
greetings (1440x900, 390x844, and /kr/about at 390x844): the five greetings on one line, the own
language last; with motion they wait out of view, then arrive one by one (100-300ms apart), done
within 2.5s, then still, all five in, none overlapping; reduced motion and no script: all five at
once, the own language last and darkest.
closing_pills (1440x900, 1024x768, 768x1024, 390x844): 4px above each closing pill's bottom edge the
element is the pill; the footer starts at or under the closing part's end.
boundary (959x900, 960x900): no sideways scrolling; one column at 959 (picture first), two at 960.
first_screen (1280x720, 1440x900, 1536x864, 390x844): the title and the meadow's far hills in the
first screen.

Pictures: scripts/qa/out/about/<size>-NN.png.

Usage: python -X utf8 scripts/qa/qa_about.py [base-url] [--only=desktop_and_phone,rhythm,motion,focus,deep_links,languages,languages_layout,nav_locales,greetings,closing_pills,boundary,first_screen,meadow_layout]
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
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "about")
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
# Vercel adds its deployment to each asset's address (".css?dpl=dpl_..."), so the query is optional.
PREFETCH_CSS = re.compile(
    r"^The resource \S+/_next/static/\S+\.css(\?\S*)? was preloaded using link preload "
    r"but not used within a few seconds from the window's load event\."
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


# Hello in five languages (the fourth promise), read still (reduced motion): the words' box
# against its promise (off: its centre's offset from the promise's centre; start: its left edge's
# offset from the promise's title), its lines (words more than 8px apart in height; fonts set a
# word's box a pixel higher or lower), whether it stands under the promise's words, whether the
# visitor's own language is the last word and the darkest, and whether all five are visible.
GREETINGS_JS = """() => { const li = document.querySelectorAll('[data-promise]')[3];
  const els = [...li.querySelectorAll('[aria-hidden="true"] > [lang]')];
  const words = els.map(w => w.getBoundingClientRect()).filter(r => r.width > 0);
  const l = Math.min(...words.map(r => r.left)), r = Math.max(...words.map(r => r.right)), b = li.getBoundingClientRect();
  const h = li.querySelector('h3').getBoundingClientRect(), p = li.querySelector('p').getBoundingClientRect();
  const ts = words.map(r => r.top).sort((x, y) => x - y);
  const lum = (c) => { const [R, G, B] = c.match(/[0-9.]+/g).map(Number); return 0.2126 * R + 0.7152 * G + 0.0722 * B; };
  const own = els.findIndex(w => w.hasAttribute('data-own'));
  const lums = els.map(w => lum(getComputedStyle(w).color));
  return { off: Math.round((l + r) / 2 - (b.left + b.width / 2)), start: Math.round(l - h.left),
           lines: 1 + ts.slice(1).filter((t, i) => t - ts[i] > 8).length, under: Math.min(...words.map(r => r.top)) >= p.bottom - 1,
           ownLast: own === els.length - 1, ownDarkest: lums.every((v, i) => i === own || v > lums[own] + 20),
           shown: els.length === 5 && els.every(w => parseFloat(getComputedStyle(w).opacity) === 1) }; }"""

# The greetings' arrival (motion): every animation frame for 6s from scrolling the fourth promise
# into view, each word's opacity and rise (the transform's y). hidden: all five hidden before the
# scroll (the line waits out of view); starts: when each word began to show (opacity over 0.02),
# in page order; done: when the last word was wholly in and at rest (opacity 0.99, rise under
# 0.5px); settled: the last frame in which anything changed; overlaps: pairs of words whose boxes
# meet at the end; final: the words wholly in at the end; ownLast: the visitor's own language if it
# is the last word.
GREETINGS_PLAY_JS = """() => new Promise((resolve) => {
  const li = document.querySelectorAll('[data-promise]')[3];
  const words = [...li.querySelectorAll('[aria-hidden="true"] > [lang]')];
  const ty = (w) => { const m = getComputedStyle(w).transform; return m === 'none' ? 0 : parseFloat(m.split(',')[5]); };
  const read = () => words.map(w => [parseFloat(getComputedStyle(w).opacity), ty(w)]);
  const hidden = read().every(([o]) => o < 0.02);
  const t0 = performance.now(), starts = words.map(() => null);
  let prev = null, settled = null, done = null, now = [];
  const tick = () => {
    const t = Math.round(performance.now() - t0);
    now = read();
    now.forEach(([o], i) => { if (o > 0.02 && starts[i] === null) starts[i] = t; });
    if (done === null && now.every(([o, y]) => o >= 0.99 && Math.abs(y) < 0.5)) done = t;
    const key = now.map(([o, y]) => o.toFixed(3) + '/' + y.toFixed(2)).join(',');
    if (prev !== null && key !== prev) settled = t;
    prev = key;
    if (t < 6000) requestAnimationFrame(tick);
    else {
      const rs = words.map(w => w.getBoundingClientRect()), overlaps = [];
      rs.forEach((a, i) => rs.forEach((b, j) => { if (j > i && a.left < b.right - 1 && b.left < a.right - 1 && a.top < b.bottom - 1 && b.top < a.bottom - 1) overlaps.push([words[i].lang, words[j].lang]); }));
      resolve({ hidden, starts, done, settled, overlaps, final: words.filter((w, i) => now[i][0] >= 0.99).map(w => w.lang),
                ownLast: words[words.length - 1].hasAttribute('data-own') ? words[words.length - 1].lang : null, end: t });
    }
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
    """The greetings under the fourth promise: all five on one calm line (two where narrow), the
    visitor's own language last. With motion, when the line first comes into view, the words arrive
    one by one (each starting 100-300ms after the one before), the whole arrival done within 2.5s,
    and then nothing moves; at the end all five are wholly in and no two overlap. With reduced
    motion and with no script all five are there at once, still, the own language last and darkest.
    (The line replaced a word cycle that ran nine seconds, too long without a pause control.) At a
    desktop and a phone size, in English and Korean."""
    for width, height, path, own in [(1440, 900, "/about", "en"), (390, 844, "/about", "en"), (390, 844, "/kr/about", "ko")]:
        tag = f"{path} {width}x{height}"
        context = browser.new_context(viewport={"width": width, "height": height}, reduced_motion="no-preference")
        page = context.new_page()
        page.goto(f"{BASE}{path}", wait_until="networkidle", timeout=120000)
        page.evaluate("document.fonts.ready.then(() => true)")
        page.wait_for_timeout(600)
        play = page.evaluate(GREETINGS_PLAY_JS)
        starts = play["starts"]
        steps = [b - a for a, b in zip(starts, starts[1:])] if None not in starts else None
        check(
            f"{tag} greetings: hidden while out of view, then arrive one by one",
            play["hidden"] and steps is not None and all(100 <= d <= 300 for d in steps),
            play,
        )
        # The arrival lasts from the first word showing to the last change of any word (its rise
        # eases out a little after it is wholly in); after that, nothing changes to the end.
        span = None if None in (play["done"], play["settled"], starts[0]) else play["settled"] - starts[0]
        check(
            f"{tag} greetings: the arrival done within 2.5s ({span}ms), then nothing moves",
            span is not None and span <= 2500,
            play,
        )
        check(
            f"{tag} greetings: at the end all five wholly in, none overlapping, the own language last",
            len(play["final"]) == 5 and not play["overlaps"] and play["ownLast"] == own,
            play,
        )
        context.close()
    for label, options in [("reduced motion", {"reduced_motion": "reduce"}), ("JavaScript off", {"java_script_enabled": False})]:
        context = browser.new_context(viewport={"width": 1440, "height": 900}, **options)
        page = context.new_page()
        page.goto(f"{BASE}/about", wait_until="load", timeout=120000)
        page.evaluate("window.scrollTo(0, document.querySelectorAll('[data-promise]')[3].getBoundingClientRect().top + scrollY - innerHeight / 2)")
        page.wait_for_timeout(150)
        hello = page.evaluate(GREETINGS_JS)
        check(f"{label}: all five greetings there at once, the own language last and darkest", hello["shown"] and hello["ownLast"] and hello["ownDarkest"], hello)
        context.close()


# The closing's pills are wholly the page's: at a point 4px above each pill's bottom edge, in the
# middle, the element there is the pill (or inside it), not the footer's band (a negative margin
# once pulled the footer's empty padding over their lower 16-25px). The footer starts at or under
# the closing part's end.
PILLS_JS = """() => {
  const part = document.querySelector('[data-part="closing"]');
  const pills = [...part.querySelectorAll('[data-words] a, [data-words] button')];
  const out = pills.map(p => { p.scrollIntoView({ block: 'center', behavior: 'instant' }); const r = p.getBoundingClientRect();
    const hit = document.elementFromPoint(r.left + r.width / 2, r.bottom - 4);
    return { pill: p.textContent.trim().slice(0, 24), hit: hit ? hit.tagName.toLowerCase() + (hit.closest('footer') ? ' in footer' : '') : null, own: !!hit && p.contains(hit) }; });
  const footer = document.querySelector('footer').getBoundingClientRect().top, end = part.getBoundingClientRect().bottom;
  return { pills: out, under: Math.round(footer - end) };
}"""


def closing_pills(browser):
    for width, height in [(1440, 900), (1024, 768), (768, 1024), (390, 844)]:
        tag = f"{width}x{height}"
        context, page, response, errors, failed = open_page(browser, width, height, reduced=True)
        r = page.evaluate(PILLS_JS)
        check(f"{tag} closing pills: the point 4px above each pill's bottom is the pill", len(r["pills"]) == 2 and all(p["own"] for p in r["pills"]), r)
        check(f"{tag} the footer starts at or under the closing part's end (nothing overlaps)", r["under"] >= 0, r)
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
  const paintings = [...document.querySelectorAll('main img')].filter(i => !i.closest('[data-mount]'));
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
        # Clicks: the first product, "Explore our products.", Science (a plain link while its
        # drop-down is put away, Mo, October 26, 2026), and the mark.
        for trigger, pick, want in [
            ("products", "first", f"/{locale}/products/nuricell"),
            ("products", "last", f"/{locale}#products"),
            ("science", None, f"/{locale}/science"),
        ]:
            page.goto(f"{BASE}/{locale}/about", wait_until="networkidle", timeout=120000)
            if pick is None:
                page.click(f'#site-navigation [class*="__links"] > a[href="/{locale}/{trigger}"]')
            else:
                page.click(f'[data-nav-trigger="{trigger}"]')
                page.wait_for_timeout(1200)
                items = page.locator(f'[data-nav-panel="{trigger}"] a')
                item = items.first if pick == "first" else items.last
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


DESIGN = "meadow"
# Each spread part and the side its picture stands on from 960px (the opening and the promise row
# are centred).
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
  const art = [...document.querySelectorAll('[data-picture] img, [data-promise] img')].filter(e => e.offsetParent && !e.closest('[data-mount]'));
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
        # The mission, a step under the heading and in ink (Mo, October 19, 2026: at the body's 19px
        # grey it was too small to read): 21px or larger, larger than the other parts' body text,
        # and the ink's #2a2824, not the muted grey.
        mission = page.evaluate(
            """(() => { const m = document.querySelector('[data-mission]'), b = document.querySelector('[data-part="roots"] [data-words] p:not([data-label])');
                 return m && { size: parseFloat(getComputedStyle(m).fontSize), body: parseFloat(getComputedStyle(b).fontSize), color: getComputedStyle(m).color }; })()"""
        )
        check(f"{tag} the mission stands a step under the heading, in ink",
              bool(mission) and mission["size"] >= 21 and mission["size"] > mission["body"] and mission["color"] == "rgb(42, 40, 36)", mission)
        check(f"{tag} no canvas and no brush layer", page.evaluate("!document.querySelector('main canvas') && !document.querySelector('[data-lifts]')"))
        folds = page.evaluate(
            "[...document.querySelectorAll('[data-part]')].filter(p => getComputedStyle(p, '::before').content !== 'none').length + document.querySelectorAll('[data-sheet]').length"
        )
        check(f"{tag} no folds", folds == 0, folds)
        paper = page.evaluate("getComputedStyle(document.querySelector('[data-look=\"ink\"]')).backgroundImage")
        check(f"{tag} the kit's plain rice paper", "paper.webp" in paper and "aged" not in paper, paper)
        # The meadow's paper is cut to transparency (build_about_opening.py), so it lies on the page
        # with no blend; every other painting multiplies.
        blends = page.evaluate(
            "[...document.querySelectorAll('main img')].filter(i => !i.closest('[data-mount], [data-meadow]')).map(i => getComputedStyle(i).mixBlendMode)"
        )
        check(f"{tag} paintings multiply (but the meadow)", blends and all(b == "multiply" for b in blends), blends)
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
        eager = page.evaluate("[...document.querySelectorAll('[data-meadow] img')].map(i => [i.getAttribute('loading'), i.getAttribute('fetchpriority')])")
        check(f"{tag} the meadow loads at once, the painting with high priority",
              len(eager) == 2 and all(l != "lazy" for l, _ in eager) and eager[0][1] == "high", eager)
        check(
            f"{tag} Support links to its page",
            page.evaluate("[...document.querySelectorAll('a')].some(a => a.textContent.trim() === 'Support' && a.getAttribute('href').endsWith('/support'))"),
        )
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
            # The purpose's oak stands larger than the rest by design (Mo, October 19, 2026); the
            # other three read about the same size, measured against their average (the middle of
            # three jumps with whichever painting is middle), and the oak is larger than that
            # average, not huge.
            heights = sorted(v["height"] for p, v in r.items() if v and p != "purpose")
            average = sum(heights) / len(heights)
            check(f"{tag} the pictures about the same size (0.55-1.6 of their average)", all(0.55 <= h / average <= 1.6 for h in heights), heights)
            oak = r["purpose"] and r["purpose"]["height"]
            check(f"{tag} the purpose's oak stands larger (1.0-1.8 of the others' average)",
                  bool(oak) and 1.0 <= oak / average <= 1.8, {"oak": oak, "others": heights})
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
            check(f"{tag} Hello in five languages centred under the fourth promise, the own language last and darkest", abs(hello["off"]) <= 2 and hello["under"] and hello["lines"] <= 2 and hello["ownLast"] and hello["ownDarkest"], hello)
        else:
            # A phone's promises are a list of rows (they were centred posters, two and a half
            # screens of them): this replaces nothing; the rows themselves are new.
            check(f"{tag} Hello in five languages under the fourth promise's words, at their left edge, in two lines at most, the own language last and darkest", abs(hello["start"]) <= 1 and hello["under"] and hello["lines"] <= 2 and hello["ownLast"] and hello["ownDarkest"], hello)
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
                          opacity: parseFloat(getComputedStyle(p).opacity), mat: Math.round(b.width) }; }"""
        )
        check(f"{tag} Dr. Liu's pool light, wide and low", wash["shape"] >= 1.8 and wash["wide"] >= 2.4 and wash["tall"] >= 1 and 0.6 <= wash["opacity"] <= 0.75, wash)
        if width >= 1200:
            # On a desktop the photo stands about 200px wide on its wash, as in the mockup (its mat
            # was 240px and stood large).
            check(f"{tag} Dr. Liu's photo about 200px wide on its wash (190-210)", 190 <= wash["mat"] <= 210, wash)
        once = page.evaluate(
            """['superbloom-v', 'superbloom-gold-v', 'enso', 'hills-v'].map(n => document.querySelectorAll(`main img[src*="${n}"]`).length)"""
        )
        check(f"{tag} the meadow appears once (its painting and its gold; no circle, no hills)", once == [1, 1, 0, 0], once)
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


# The meadow's two pictures: the painting (its gold a pale ghost) and the gold alone over it.
INK = "[data-meadow] img:first-child"
GOLD = "[data-meadow] img + img"

# The meadow's gold, every animation frame for 14s from navigation: [ms since navigation, its
# reach (the mask's edge, in %: 0 before it begins, 150 once whole), the gold's picture in, the
# painting's picture in]. Installed before the page's own scripts; it only reads.
GOLD_LOG = """(() => {
  const log = (window.__gold = []);
  const tick = () => {
    const ink = document.querySelector('[data-meadow] img:first-child'), gold = document.querySelector('[data-meadow] img + img');
    if (ink && gold)
      log.push([Math.round(performance.now()), parseFloat(getComputedStyle(gold).getPropertyValue('--reach')),
                gold.complete && gold.naturalWidth > 0, ink.complete && ink.naturalWidth > 0]);
    if (performance.now() < 14000) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
})();"""

# The opening's words hidden, so a shot of the first screen is the meadow alone (they stand in
# its sky).
HIDE_WORDS = '[data-part="opening"] :is(h1, p) { visibility: hidden !important; }'

# The page's paintings below the opening: the oak, the pool under Dr. Liu's photo (not the
# photo), the sequoia, the four promise dots and the glasses.
PAINTINGS = "[data-picture] img:not([data-mount] img), [data-promise] img"


def gold_shares(shot):
    """The share of a shot's pixels that are gold (warm: red over blue by 70 or more, red 140 or
    more; the paper, the ink and the gold's pale grey ghost are none of them), in all of it and in
    its upper and lower halves."""
    r, g, b = shot.convert("RGB").split()
    warm = ImageChops.subtract(r, b).point(lambda v: 255 if v >= 70 else 0)
    gold = ImageChops.multiply(warm, r.point(lambda v: 255 if v >= 140 else 0))
    w, h = gold.size
    upper = gold.crop((0, 0, w, h // 2)).histogram()[255]
    lower = gold.crop((0, h // 2, w, h)).histogram()[255]
    return {"all": round((upper + lower) / (w * h), 4), "upper": round(upper / (w * (h // 2)), 4), "lower": round(lower / (w * (h - h // 2)), 4)}


def first_screen_shot(page):
    """The first screen with the opening's words hidden, as a picture."""
    page.evaluate("window.scrollTo(0, 0)")
    page.add_style_tag(content=HIDE_WORDS)
    page.wait_for_timeout(150)
    return Image.open(io.BytesIO(page.screenshot())).convert("RGB")


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
    # it must be at least that. The meadow's gold is whole at once: no mask, no animation.
    context, page, response, errors, failed = open_page(browser, 1440, 900, reduced=True)
    scroll_through(page)
    still = page.evaluate(
        f"""() => {{ const g = document.querySelector('{GOLD}');
             return {{ blooms: [...document.querySelectorAll('[data-bloom]')].filter(x => x.dataset.bloom !== 'done').length,
                      hidden: [...document.querySelectorAll('main img')].filter(i => parseFloat(getComputedStyle(i).opacity) < (i.matches('[data-pool]') ? 0.7 : 1)).length,
                      arrive: getComputedStyle(g).animationName, mask: getComputedStyle(g).maskImage,
                      running: document.getAnimations().filter(a => {{ const t = a.effect && a.effect.target;
                        return t && t.closest && t.closest('main') && !t.closest('[class*=greetings]'); }}).length }}; }}"""
    )
    check("reduced motion: the meadow and its gold whole (no mask), every painting shown, still",
          still["blooms"] == 0 and still["hidden"] == 0 and still["arrive"] == "none" and still["mask"] == "none"
          and still["running"] == 0, still)
    whole = gold_shares(first_screen_shot(page))
    check("reduced motion: the first screen's meadow holds its gold", whole["all"] >= 0.08, whole)
    context.close()

    # With motion. Every painting below the opening server-marked waiting (none paints whole, then
    # vanishes), read from the HTML the server sends, before any script could mark one: in the
    # page's main, the oak, the pool, the sequoia, the four promise dots and the glasses (the
    # meadow's gold arrives instead; the shared closing crane after main is the kit's own).
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="no-preference")
    html = context.request.get(f"{BASE}/about").text()
    main = html[html.index("<main"):html.index("</main>")]
    marks = re.findall(r'<img[^>]*?\sdata-bloom="([^"]*)"', main)
    check("motion: every painting below the opening server-marked waiting (none paints whole, then vanishes)", len(marks) == 8 and all(m == "waiting" for m in marks), marks)
    page = context.new_page()
    page.goto(f"{BASE}/about", wait_until="domcontentloaded", timeout=120000)
    wait_until(page, f"getComputedStyle(document.querySelector('{GOLD}')).animationName !== 'none'", 5000)
    early = page.evaluate(
        f"""() => {{ const e = getComputedStyle(document.querySelector('{GOLD}'));
             return {{ name: e.animationName, duration: e.animationDuration, wait: parseFloat(e.animationDelay) }}; }}"""
    )
    check("motion: the meadow's gold arrives (its animation, 3.4s after 0.4s)",
          "arrive" in early["name"] and early["duration"] == "3.4s" and early["wait"] == 0.4, early)
    low = "document.querySelector('[data-part=\"experience\"] [data-picture] img')"
    state = page.evaluate(f"[{low}.dataset.bloom ?? null, getComputedStyle({low}).opacity]")
    check("motion: a lower painting waits out of view, hidden", state[0] == "waiting" and float(state[1]) == 0, state)
    page.evaluate(f"(() => {{ const i = {low}; window.scrollTo(0, i.getBoundingClientRect().top + window.scrollY - innerHeight / 2); }})()")
    check("motion: then it blooms", wait_until(page, f"{low}.dataset.bloom === 'done'"))
    context.close()

    # The gold really spreads, from the foot of the first screen (a mask that never moves would
    # pass "its animation runs" with the gold whole from the first frame, or none to the end). The
    # page stops the gold in the frame its clock first reaches a set time (which counts its 0.4s
    # delay), shoots the first screen, then lets it run on. At 1440x900 the first screen's gold
    # comes in from about 1s to 2s (the bloom's far reach, past the screen, takes to 3.8s): 1.4s in
    # it holds under half of the still meadow's gold (about a third), more of it in the screen's
    # lower half than in its upper; 1.7s in, more (about 0.8), not yet all; then all of it. A clock
    # past the animation's end (3.8s) is never reached.
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="no-preference")
    page = context.new_page()
    page.goto(f"{BASE}/about", wait_until="domcontentloaded", timeout=120000)
    wait_until(page, f"getComputedStyle(document.querySelector('{GOLD}')).animationName !== 'none'", 5000)
    page.add_style_tag(content=HIDE_WORDS)

    def stop_at(ms):
        """Stop the gold's animation in the frame its clock first reaches `ms`, and shoot the first
        screen: [the clock where it stopped, its gold]."""
        stopped = page.evaluate(
            f"""(ms) => new Promise((resolve) => {{
                 const arrive = document.querySelector('{GOLD}').getAnimations()[0];
                 if (!arrive) return resolve(null);
                 const began = performance.now();
                 const tick = () => {{
                   if (Number(arrive.currentTime) >= ms) {{ arrive.pause(); return resolve(Math.round(Number(arrive.currentTime))); }}
                   if (performance.now() - began > 12000) return resolve(null);
                   requestAnimationFrame(tick);
                 }};
                 tick();
               }})""",
            ms,
        )
        shot = gold_shares(Image.open(io.BytesIO(page.screenshot())).convert("RGB"))
        page.evaluate(f"document.querySelector('{GOLD}').getAnimations().forEach((a) => a.play())")
        return stopped, shot

    clock, begun = stop_at(1400)
    check("motion: the gold starts at the foot (1.4s in: under half of it, more in the lower half than the upper)",
          clock is not None and 0 < begun["all"] <= 0.5 * whole["all"] and begun["lower"] > begun["upper"],
          {"clock_ms": clock, "begun": begun, "still": whole})
    clock, midway = stop_at(1700)
    check("motion: 1.7s in, more of it, not yet all",
          clock is not None and begun["all"] < midway["all"] < 0.97 * whole["all"],
          {"clock_ms": clock, "midway": midway, "begun": begun, "still": whole})
    page.wait_for_timeout(2500)
    end = gold_shares(Image.open(io.BytesIO(page.screenshot())).convert("RGB"))
    check("motion: then all of it arrives (as much gold as the still meadow)", end["all"] >= 0.97 * whole["all"], {"end": end, "still": whole})
    context.close()

    # A slow link: the gold's picture arrives late (its requests held until 3s after navigation).
    # The meadow shows at once and its gold waits for its picture: 2.5s in, the painting is in and
    # no gold has come; the gold starts only once its picture is in, and arrives whole at least its
    # delay and duration after the picture (0.4s and 3.4s, read from the page; less 150ms, as its
    # ease nears 150% a little before its end). Every frame is logged from navigation, to 14s.
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="no-preference")
    context.add_init_script(GOLD_LOG)
    page = context.new_page()
    held = []
    page.route(re.compile(r"superbloom-gold-v\d"), lambda route: held.append(route))
    page.goto(f"{BASE}/about", wait_until="domcontentloaded", timeout=120000)
    wait_until(page, "performance.now() >= 3000", 15000)
    for route in held:
        route.continue_()
    wait_until(page, "performance.now() >= 13500", 20000)
    log = page.evaluate("window.__gold || []")
    gold_ms = page.evaluate(
        f"""(() => {{ const e = getComputedStyle(document.querySelector('{GOLD}'));
             return Math.round((parseFloat(e.animationDelay) + parseFloat(e.animationDuration)) * 1000); }})()"""
    )
    context.close()
    at = [f for f in log if f[0] <= 2500]
    early = at[-1] if at else None
    check("slow gold: 2.5s in, the meadow shows and no gold has come",
          early is not None and not early[2] and early[3] and early[1] <= 0, {"held": len(held), "frame": early})
    arrived = next((f[0] for f in log if f[2]), None)
    began = next((f[0] for f in log if 0 < f[1] < 149.9), None)
    spreading = [f for f in log if arrived is not None and f[0] >= arrived and 5 < f[1] < 140]
    check("slow gold: the gold starts only once its picture is in, then spreads",
          arrived is not None and began is not None and began >= arrived and len(spreading) >= 10,
          {"arrived_ms": arrived, "began_ms": began, "frames_spreading": len(spreading)})
    done = next((f[0] for f in log if f[1] >= 149.9 and f[0] >= (began or 0)), None)
    check("slow gold: then it arrives whole (its delay and duration after the picture), and stays",
          arrived is not None and done is not None and gold_ms >= 3800
          and done >= arrived + gold_ms - 150 and bool(log) and log[-1][1] >= 149.9,
          {"arrived_ms": arrived, "gold_ms": gold_ms, "done_ms": done, "last": log[-1] if log else None})

    # A failed gold picture: nothing lets the gold go (no timer; Next's onLoad fires for a broken
    # img that is complete when it hydrates, so the opening checks naturalWidth). 9s in (unheld,
    # it would have arrived 0.4s + 3.4s after the page is styled), it still holds, and the meadow
    # shows.
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="no-preference")
    page = context.new_page()
    page.route(re.compile(r"superbloom-gold-v\d"), lambda route: route.abort())
    page.goto(f"{BASE}/about", wait_until="domcontentloaded", timeout=120000)
    wait_until(page, "performance.now() >= 9000", 20000)
    failed = page.evaluate(
        f"""() => {{ const g = document.querySelector('{GOLD}'), i = document.querySelector('{INK}');
             return {{ picture: g.naturalWidth, play: getComputedStyle(g).animationPlayState, meadow: i.naturalWidth }}; }}"""
    )
    context.close()
    check("failed gold picture: 9s in, the gold still holds and the meadow shows",
          failed["picture"] == 0 and failed["play"] == "paused" and failed["meadow"] > 0, failed)

    # JavaScript off: nothing holds the gold (its arrival is pure CSS); once it has arrived (0.4s
    # and 3.4s from when the page is styled; shot 5s after load) the first screen holds as much
    # gold as the still meadow.
    context = browser.new_context(viewport={"width": 1440, "height": 900}, java_script_enabled=False, reduced_motion="no-preference")
    page = context.new_page()
    page.goto(f"{BASE}/about", wait_until="load", timeout=120000)
    page.wait_for_timeout(5000)
    # A plain shot: with script off Playwright cannot add a style or scroll, and the words are
    # ink, never gold.
    off = gold_shares(Image.open(io.BytesIO(page.screenshot())).convert("RGB"))
    context.close()
    check("JavaScript off: the meadow shows with all its gold", off["all"] >= 0.97 * whole["all"], {"off": off, "still": whole})

    # JavaScript off: every other painting shows too (nothing waits for a bloom that will not come).
    # Each one's ink (the share of its pixels darker than 215: the palest dot is light wash) is
    # read on the page with script off and on the still page (reduced motion, read to the end,
    # every bloom done); with script off each holds at least 0.9 of its still ink. A painting left
    # hidden holds none, one stuck in its blot only part of it.
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
        len(off) == 8 and len(still) == 8 and all(s >= 0.01 for _, s in still) and not faint,
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


def ink_rows(shot, level=200, least=2):
    """For each row of a picture, whether it holds ink: at least `least` pixels darker than `level`
    (the paper's fibres are lighter)."""
    grey = shot.convert("L").point(lambda v: 255 if v < level else 0)
    w, h = grey.size
    return [grey.crop((0, y, w, y + 1)).histogram()[255] >= least for y in range(h)]


def first_screen(browser):
    for width, height in [(1280, 720), (1440, 900), (1536, 864), (390, 844)]:
        tag = f"{width}x{height}"
        context, page, response, errors, failed = open_page(browser, width, height, reduced=True)
        title = page.evaluate("document.querySelector('h1').getBoundingClientRect().bottom")
        rows = ink_rows(first_screen_shot(page).crop((0, 110, width, height)), least=max(2, width // 100))
        hills = next((110 + y for y, inked in enumerate(rows) if inked), None)
        check(f"{tag} the title and the meadow's far hills in the first screen", title <= height and hills is not None and hills < height,
              {"title": title, "hills": hills, "win": height})
        context.close()


# The opening: the meadow's painting (its box, in page coordinates), the words (each line's box),
# the window, where the opening ends and where Our purpose's first content (its painting, label or
# heading) begins. The kicker is the opening's first p, the lead the p after the h1.
MEADOW_JS = """() => {
  const o = document.querySelector('[data-part="opening"]');
  const pic = o.querySelector('img').getBoundingClientRect();
  const lines = (e) => { const r = document.createRange(); r.selectNodeContents(e);
    return [...r.getClientRects()].filter(x => x.width > 1).map(x => [x.left, x.top, x.right, x.bottom]); };
  const kicker = o.querySelector('p'), title = o.querySelector('h1'), lead = o.querySelector('h1 + p');
  const t = lines(title);
  const purpose = [...document.querySelectorAll('[data-part="purpose"] :is([data-picture] img, [data-label], h2)')].filter(e => e.offsetParent);
  return { pic: [pic.left, pic.top + scrollY, pic.right, pic.bottom + scrollY], win: [document.documentElement.clientWidth, innerHeight],
           title: [Math.min(...t.map(x => x[0])), Math.max(...t.map(x => x[2]))],
           lines: [kicker, title, lead].flatMap(lines), end: o.getBoundingClientRect().bottom + scrollY,
           purpose: Math.min(...purpose.map(e => e.getBoundingClientRect().top)) + scrollY,
           sideways: document.documentElement.scrollWidth - innerWidth };
}"""


def ink_near_words(shot, lines, pad=8):
    """The painting's dark pixels (under 200) within `pad` px of any word, on a shot of the first
    screen with the words hidden."""
    grey = shot.convert("L")
    dark = 0
    for l, t, r, b in lines:
        crop = (max(0, int(l - pad)), max(0, int(t - pad)), min(grey.width, int(r + pad)), min(grey.height, int(b + pad)))
        if crop[2] > crop[0] and crop[3] > crop[1]:
            dark += sum(grey.crop(crop).histogram()[:200])
    return dark


def meadow_layout(browser):
    sizes = [(1920, 1000), (1440, 900), (1280, 720), (1024, 768), (768, 1024), (600, 900), (390, 844), (360, 780)]
    for width, height in sizes:
        tag = f"meadow {width}x{height}"
        context, page, response, errors, failed = open_page(browser, width, height, reduced=True)
        g = page.evaluate(MEADOW_JS)
        (pl, pt, pr, pb), (ww, wh) = g["pic"], g["win"]
        check(f"{tag} the painting spans the window", pl <= 0 and pr >= ww, g["pic"])
        check(f"{tag} the title centred", abs((g["title"][0] + g["title"][1]) / 2 - ww / 2) <= 2, g["title"])
        shot = first_screen_shot(page)
        near = ink_near_words(shot, g["lines"])
        check(f"{tag} no ink within 8px of the words", near == 0, near)
        # The first screen's foot: the meadow runs on past it, its last 40px full of poppies and
        # grass (no bare band and no edge there).
        foot = shot.convert("L").crop((0, wh - 40, ww, wh))
        full = sum(foot.histogram()[:215]) / (ww * 40)
        check(f"{tag} the meadow fills the first screen's foot", pb > wh and full >= 0.2, {"inked": round(full, 3), "bottom": pb})
        # Below the first screen the meadow ends in the paper: its painting's last 12px hold no ink,
        # its last strokes stand under the first screen and above Our purpose's first content.
        page.evaluate(f"window.scrollTo(0, {max(0, pb - wh * 0.7)})")
        page.wait_for_timeout(300)
        y0 = page.evaluate("scrollY")
        view = Image.open(io.BytesIO(page.screenshot())).convert("RGB")
        top, bottom = int(max(0, pt - y0)), int(min(wh, pb - y0))
        rows = ink_rows(view.crop((0, top, ww, bottom)))
        last = next((top + y0 + y for y in range(len(rows) - 1, -1, -1) if rows[y]), None)
        bare = not any(rows[-12:])
        check(f"{tag} the meadow ends in bare paper (its last 12px no ink)", bare, {"last_ink": last, "bottom": pb})
        check(f"{tag} its last strokes under the first screen, 24px or more above Our purpose",
              last is not None and last > wh and last + 24 <= g["purpose"], {"last_ink": last, "first_screen": wh, "purpose": g["purpose"], "end": g["end"]})
        check(f"{tag} no sideways scrolling", g["sideways"] <= 0, g["sideways"])
        view.save(os.path.join(OUT, f"meadow-end-{width}x{height}.png"))
        shot.save(os.path.join(OUT, f"meadow-{width}x{height}.png"))
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
GROUPS = [desktop_and_phone, rhythm, motion, focus, deep_links, languages, languages_layout, nav_locales, greetings, closing_pills, boundary, first_screen, meadow_layout]
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

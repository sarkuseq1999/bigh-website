"""QA for the menu bar, "Inscription" (Mo's pick, October 5, 2026), on the homepage.

usage: python -X utf8 scripts/qa/qa_nav.py [base] [--only=desk|settle|rows|phone|tablet|lang|r10]
       base defaults to http://localhost:3014

On the real GPU (ANGLE/D3D11):
  - desktop 1536x900: the bar's links (Products, Science, About, Support; no "Home": the mark goes
    home), the mark centred in the window and at least 120 px wide over the opening, words at
    least 18 px and every control at least 48 px tall; Products opens on hover, the pointer can
    cross into it, Science swaps in without rolling the scroll up again, leaving closes it and it
    rolls back up, its pictures loaded (they wait until the pointer reaches the bar); a click toggles; a click on the wash closes it (and doesn't scroll the page);
    Enter opens, Tab steps into the panel, Escape closes and hands focus back; the Tab order
    follows the line; a visible ring on the keyboard's focus; Support opens its sheet; scrolled,
    the bar settles small with its painted rule; a product link goes to its page.
  - the rule (round 3): the painted stroke (rule-whole.webp), drawn whole once the page has moved
    on, across the page's column and centred on the mark (2px), its ink over at least 92% of it,
    its body 2-4.5px at 1536 (measured in the pixels) and 16px or more under the mark; laid by the
    scroll from its loaded end (part way at 160px and not moving on its own a second later, whole
    by 320px); with reduced motion, there whole.
  - scrolled (desktop, phone, tablet 768): the bar is solid paper. A headline, a paragraph and a
    text link of the page are each put behind the bar's words and on its brush rule, and the band
    from the bar's top to just under the rule's ink must not change by more than 6 levels (round 1:
    at 93% paper the page ghosted behind the words and the rule struck through lines under it).
  - the two rows (round 11, Mo's pick: everything at once). At 1536x900, 1280x800, 1920x1080@2x,
    1101x800 and 1366x657: Products shows all five at once in one row, side by side (each picture,
    name and line seen), inside the window and above the scroll's torn foot, every name and line in
    its own column; the names on one line and every line starting on one line (1px), each name
    centred under its picture (2px), names 21px+, lines 17px+; each bottle on its own pale pool
    (multiplied, 45-65%) and all on one painted ground line (the bar's stroke: 1-8px of ink in
    every gap between bottles, under half the old 16px rod), each bottle crisp (its picture at least its size on screen)
    and 170px+ tall; the scroll's foot above the window's foot. Science the same with its four
    parts, on one page with Products (1px: the title, the pictures' row's top and height, the
    names' line, the captions on the focus lines' line, the link under the row); Dr. Liu's print
    75%+ of its room and every picture crisp; one weight (1536, 1101, 1920@2x, in the pixels): the
    three paintings' ink within 25% of their mean, the print as tall as any painting and 75%+ of a
    bottle. Every part one link to its own page (48px+), the link under the row centred and going
    to the products or the science. Keyboard: Enter opens each, Tab steps through its parts in
    order (each ringed, its name lined, its bottle lifted 6px with the others standing, or its
    picture forward with the others eased back to 60-85%), then the link under the row. Pointer:
    resting on a part does the same and lines only its name; a click opens its page; on a touch
    laptop the first tap opens its page. Filmed at real speed along each row: one name lined on
    every frame, a bottle lifting at most its 6px and never fading, no Science picture past 60% and
    no painting's paper as a light box; swapping back in from Products, no light box. Vietnamese,
    Japanese and Korean at 1101 and 1536: both rows whole, inside the window, long names wrapping in
    their own column (two lines at most), names on one line and lines starting on one line.
  - reduced motion: the scroll is down at once.
  - the painted stroke (round 6) at 1536x900: the homepage marks no page (no aria-current, no
    data-current, no stroke "here" in the bar). The stroke follows the reader: none over the
    opening, the scientists, the stories or the purpose; under Products while #products is read;
    under Science in #cellular, #science and #research; laid whole (its ink 50%+) a moment after the
    part arrives, gone (ink 0) a moment after it leaves; in the pixels its ink runs under the word
    from its first letter over 75%+ of it, 3-8px thick, centred where the fine line runs and clear of
    the chevron. Exactly one painted stroke at a time on every frame the page draws while the whole
    page is read down at a few hundred px a second. Pointing at About or opening a drop-down lifts
    it (ink 0) and it comes back after; with reduced motion it is there whole at once. On a phone
    the bar shows no stroke. Escape from a drop-down, scrolled, hands focus back without moving
    the page (the page's 150px scroll padding made a plain focus() jump it about 480px up).
  - phone 390x844: the menu opens and locks the page, the button says Close, Escape closes it and
    hands focus back, the Close button closes it, Products and Science fold open one at a time,
    Support opens its sheet, a product link goes to its page.
  - tablet 834x1112: the menu opens with Products unfolded.
  - the menu's rows and finale (round 7). Phones 390x844, 360x780, 430x932 and 360x640, and
    Vietnamese and Japanese at 390x844 (and Vietnamese at 360x780): Products unfolds as five rows
    and Science as four, every name written out and unclipped, every row (name, line, picture)
    inside the window's width, nothing cut off at a side and nothing scrolling sideways; in
    English at the three phones all of them in view at once without scrolling; rows 56px+ tall,
    names 20px+, lines 16px+; the link under the rows keeps its arrow on its last word's line.
    With the four words alone (780px tall and more) the crane stands whole at the foot with Log
    in and Sign up under it, no scrolling; with Science unfolded, scrolled to the end, the same,
    the menu scrolling on its own while the page under it stays put. Filmed frame by frame at
    390x844: as Products unfolds the crane is carried down (never up), and folding it away brings
    it back, never hidden, faded or jumping (no frame over 64px). Tablets: 834x1112 and 768x1024
    open with Products unfolded (the five in a row, all in view, focus lines on one line, no
    hollow over 120px between Support and the crane, the crane whole at the foot); 1024x768 opens
    with the four words and the crane; Science shows its four in a row, captions on one line.
    On the upright tablet the crane eases (never pops) as Science replaces Products and folds
    away. Filmed at real speed on a phone: Science unfolding and the menu opening show no light
    box round the paintings or the crane.
  - the bar's three groups in every language (round 8): English, Simplified Chinese, Korean,
    Vietnamese and Japanese at 1101, 1160, 1220, 1280, 1366, 1440, 1536 and 1920px, over the opening
    and scrolled: the gap before the account group (and after the language) at least 1.5 times the
    spacing between the links; the inscription symmetric about the centred mark (one spacing, its
    sides within 1.35 times; the rest is the words' own length); 12px+ between neighbours, 16px+
    from the window's edge; no word wrapping, none under 18px. Then every 20px from 1101 to 1920 in
    both states, and with the window's own scrollbar showing. The stroke under a short word (产品,
    제품, 製品; 소개 as the current page): about three characters long, centred, past both ends,
    its ink never past the chevron's middle.
  - filmed at real speed (round 2; every frame the compositor draws, plus the bar's state on every
    frame the page draws): Science opening (its three paintings; Dr. Liu's print is never
    multiplied) and Products opening (its five pools), from the tall bar and from the scrolled
    bar, show no light box behind a painting or a pool (only pictures drawn at the end are
    measured; a painting against the paper under it, the same place with the paintings lifted, so
    the paper's own grain never reads as light; a pool against the paper in the gaps between the
    bottles): no sample of a multiplied picture is more than 4 levels lighter than that paper, on
    any frame (two frames
    running) once the scroll has reached it (a bottle's pool, whose edge is masked, is read with
    the bottles and the ground line hidden at the points where its own painting is paper, averaged,
    against the paper in the gaps between the bottles, and must not be more than 1 level over it:
    multiplied it reads -2 to -7 levels, an isolated blend about +3). Moving from one drop-down to the other (both ways):
    the scroll's ink never drops below 60% of the lighter drop-down's, one drop-down is always drawn
    whole, only one word is ever underlined and no chevron is ever turned sideways; pointing on to
    About keeps one line. The tablet menu opens, and the phone menu's Products unfolds, with no
    light box round the pools and the chevron turning over, never sideways.
  - the title settles with the scroll (round 9), at 1536x900, every 6px from 0 to 300 down and
    back up: the mark only shrinks and the paper and the rule only grow going down, between its two
    sizes at a dozen depths or more inside 48-240px (a gesture, not a step); tall and clear to
    48px; from 240px small, solid paper, the rule laid; nothing moves where the bar takes its small
    layout (239 -> 240px); scrolling back up gives the same bar at every depth. Filmed through a
    wheel scroll to 400px and back (the page's smooth scrolling): the mark follows the scroll both
    ways on every frame, no frame over 25ms (a couple allowed). Reloaded 150px and 600px down: the
    bar right on every look while the page loads and after. Behind every word of the bar, every
    8px of the settle, at 1536, 1280, 1920 and on a 390 phone (the words hidden, the ground under
    their letters read): contrast with the words' ink 7:1 or more, the ground's levels spread 40
    or less. Reduced motion: two states, never between. Firefox (no scroll-driven animation, so
    the script's fallback): the same sweep and checks.
  - nothing dead, nothing small (round 10). At 1536x900 and 1101x800 (over the opening, scrolled,
    Products and Science open), on phones 390x844 and 360x640 and the tablet 834x1112 (the bar, the
    menu, each fold, its foot), and in Chinese, Korean, Vietnamese and Japanese (1101 over the
    opening, scrolled and both drop-downs; the phone menu's folds and foot): every visible text 15px
    or larger and 7:1 or more on the paper, every control's target 48px or more both ways (a short
    word's and the mark's reach past their box). Sign up, with no link yet, promises nothing: not a
    Tab stop, the default cursor, the same pixels when pointed at and pressed (bar and menu). The
    wash under an open scroll is 26-32% (round 9). Focus rings, stepping through every control
    from the keyboard (the bar over the opening and scrolled, both drop-downs, the phone, short
    phone and tablet menu with both folds): 2px of ink, whole on all four sides in the pixels,
    inside the window (the menu keeps the focused line above its foot), 4px or more clear of the
    mark's leaf and letters, round the language picker's globe, never across the brush marks
    between the menu's lines, and in the settled bar clear of its rule. On a short phone the word
    pressed in the menu stays in the window while the folds move. The language picker is as wide
    as the language it shows, its arrow beside the word, in Chrome and in Firefox.
  - no page errors or console errors anywhere.
Pictures land in scripts/qa/out/nav/.
"""

import base64
import math
import sys
from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = (ARGS[0] if ARGS else "http://localhost:3014").rstrip("/")
ONLY = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--only=")), None)
OUT = Path(__file__).parent / "out" / "nav"
OUT.mkdir(parents=True, exist_ok=True)
URL = f"{BASE}/"
results: list[tuple[str, bool]] = []
errors: list[str] = []


def check(name, ok, detail=""):
    results.append((name, bool(ok)))
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail != "" else ""))


def watch(page):
    page.on("pageerror", lambda e: errors.append(f"{page.url} {e}"[:300]))
    page.on("console", lambda m: m.type == "error" and errors.append(f"{page.url} {m.text}"[:300]))


def r_value(page):
    return page.evaluate(
        "getComputedStyle(document.querySelector('header')).getPropertyValue('--insc-r').trim()"
    )


def is_open(page, panel):
    return page.evaluate(
        f"document.querySelector('[data-nav-panel=\"{panel}\"]').hasAttribute('data-open')"
    )


def focused(page):
    return page.evaluate(
        """() => { const e = document.activeElement; if (!e) return 'none';
        return (e.getAttribute('aria-label') || e.textContent || e.tagName).trim().slice(0, 40); }"""
    )


def menu_open(page):
    return page.evaluate("document.querySelector('header').hasAttribute('data-menu')")


# Lines of the page to put under the scrolled bar: a headline, a paragraph and a text link past the
# opening, each by the middle of its first line (document y), visible (not waiting to be revealed).
LINES = """() => {
  const first = el => { const r = document.createRange(); r.selectNodeContents(el);
    const box = [...r.getClientRects()].find(b => b.width > 40 && b.height > 8); return box; };
  const pick = sel => [...document.querySelectorAll(sel)].find(el => {
    if (el.closest('header, footer, dialog')) return false;
    const b = first(el); return b && b.top + scrollY > 1200 && el.textContent.trim().length > 12 &&
      el.checkVisibility({ opacityProperty: true, visibilityProperty: true });
  });
  return ['main h2', 'main p', 'main a'].map(pick).filter(Boolean).map(el => { const b = first(el);
    return { text: el.textContent.trim().slice(0, 28), y: b.top + scrollY + b.height / 2 }; });
}"""


def scroll_to(page, y):
    page.evaluate(f"window.scrollTo(0, {y})")
    page.mouse.wheel(0, 1)
    page.wait_for_timeout(1400)


# Round 3: the rule is one real painted stroke (a mask cut from a painting), laid by the scroll.
RULE = """() => { const h = document.querySelector('header'); const rule = h.querySelector('[class*="__rule"]');
  const s = getComputedStyle(rule); const r = rule.getBoundingClientRect();
  const m = h.querySelector('[data-nav-logo]').getBoundingClientRect();
  const nav = h.querySelector('#site-navigation'); const col = nav.getBoundingClientRect();
  const pad = parseFloat(getComputedStyle(nav).paddingLeft);
  return { draw: parseFloat(s.getPropertyValue('--insc-draw')), opacity: +s.opacity, mask: getComputedStyle(rule, '::before').maskImage,
    left: r.left, right: r.right, top: r.top, bottom: r.bottom, mid: (r.left + r.right) / 2,
    markMid: (m.left + m.right) / 2, markBottom: m.bottom, colLeft: col.left + pad, colRight: col.right - pad,
    barBottom: col.bottom }; }"""


def rule_ink(page, info):
    """Where the rule's ink is, from the pixels: each column's darkest level against the paper just
    above the rule, and the stroke's body (rows at least half as dark, in its loaded first half).
    Only 7px each side of the rule's middle is read: above that are the bar's words (the Sign up
    pill's foot), and from 8px under the bar the page fades in."""
    middle = (info["top"] + info["bottom"]) / 2
    top = round(middle) - 7
    bottom = min(round(middle) + 8, round(info["barBottom"]) + 8)
    band = {"x": 0, "y": top, "width": page.viewport_size["width"], "height": bottom - top}
    a = np.asarray(Image.open(BytesIO(page.screenshot(clip=band))).convert("L"), dtype=np.float32)
    paper = float(np.median(a[:3]))
    depth = paper - a.min(axis=0)
    inked = np.where(depth > 40)[0]
    x0, x1 = round(info["left"]), round(info["right"])
    body = a[:, x0 + round((x1 - x0) * 0.08) : x0 + round((x1 - x0) * 0.5)]
    half = paper - (paper - body.min(axis=0)) / 2
    return {
        "from": int(inked.min()) if len(inked) else -1,
        "to": int(inked.max()) if len(inked) else -1,
        "thick": float(np.median((body < half[None, :]).sum(axis=0))),
    }


def rule_checks(browser):
    """Round 3: the scrolled bar's edge is a real brush stroke (not the drawn bar of before), light,
    across the page's column and centred on the mark, laid by the reader's scroll (not on a timer);
    with reduced motion it is there whole."""
    page = browser.new_page(viewport={"width": 1536, "height": 900})
    watch(page)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(2000)
    page.mouse.move(768, 896)
    scroll_to(page, 1400)
    info = page.evaluate(RULE)
    ink = rule_ink(page, info)
    page.screenshot(
        path=str(OUT / "desk-rule.png"),
        clip={"x": 0, "y": 0, "width": 1536, "height": round(info["bottom"]) + 16},
    )
    check(
        "desk: the rule is the painted stroke, drawn whole once the page has moved on",
        "rule-whole.webp" in info["mask"] and info["draw"] == 1 and info["opacity"] >= 0.6,
        f"draw {info['draw']}, opacity {info['opacity']}",
    )
    span = info["right"] - info["left"]
    check(
        "desk: the rule runs across the page's column, centred on the mark (2px), its ink over 92% of it",
        abs(info["left"] - info["colLeft"]) <= 2
        and abs(info["right"] - info["colRight"]) <= 2
        and abs(info["mid"] - info["markMid"]) <= 2
        and ink["from"] - info["left"] <= 12
        and ink["to"] - ink["from"] >= 0.92 * span,
        f"rule {info['left']:.0f}-{info['right']:.0f}, column {info['colLeft']:.0f}-{info['colRight']:.0f}, "
        f"mark centre {info['markMid']:.1f}, ink {ink['from']}-{ink['to']}",
    )
    middle = (info["top"] + info["bottom"]) / 2
    check(
        "desk: the rule is light (body 2-4.5px at 1536) and 16px or more under the mark",
        2 <= ink["thick"] <= 4.5 and middle - info["markBottom"] >= 16,
        f"body {ink['thick']:.1f} px; rule middle {middle:.1f}, mark foot {info['markBottom']:.1f}",
    )
    # Laid by the scroll: part way at 160px and the same a second later (no timer), its ink
    # reaching only part of the column from the left; whole by 320px.
    scroll_to(page, 160)
    first = page.evaluate(RULE)
    page.wait_for_timeout(1000)
    later = page.evaluate(RULE)
    part = rule_ink(page, later)
    page.screenshot(path=str(OUT / "desk-rule-160.png"), clip={"x": 0, "y": 0, "width": 1536, "height": 110})
    scroll_to(page, 320)
    whole = page.evaluate(RULE)
    check(
        "desk: the scroll lays the rule from its loaded end (part way at 160px and still a second later, whole by 320px)",
        0.2 <= first["draw"] <= 0.7
        and abs(later["draw"] - first["draw"]) < 0.01
        and whole["draw"] == 1
        and part["from"] - later["left"] <= 12
        and part["to"] < later["left"] + 0.75 * (later["right"] - later["left"]),
        f"at 160px: {first['draw']:.2f}, a second later {later['draw']:.2f}, ink {part['from']}-{part['to']}; "
        f"at 320px: {whole['draw']}",
    )
    page.close()

    page = browser.new_page(viewport={"width": 1536, "height": 900}, reduced_motion="reduce")
    watch(page)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(1500)
    scroll_to(page, 160)
    info = page.evaluate(RULE)
    check(
        "reduced motion: the rule is there whole",
        info["draw"] == 1 and info["opacity"] >= 0.6,
        f"draw {info['draw']}, opacity {info['opacity']}",
    )
    page.close()


def solid_bar(page, tag):
    """Round 1: once the page moves on, the bar is a solid sheet of paper. Lines of the page are put
    behind its words and on its brush rule; from the bar's top to just under the rule's ink, the bar
    must look the same whatever is under it (nothing ghosts through it, nothing is crossed by the
    rule)."""
    size = page.viewport_size
    page.mouse.move(size["width"] / 2, size["height"] - 4)
    # The reading stroke (round 6) comes and goes with the part of the page being read, on purpose;
    # it is held out here, where only the paper and its rule are compared.
    held = page.add_style_tag(content="[data-nav-ink] { visibility: hidden !important; }")
    scroll_to(page, 1400)
    bar = page.evaluate("document.querySelector('#site-navigation').getBoundingClientRect().bottom")
    band = {"x": 0, "y": 0, "width": size["width"], "height": round(bar) + 6}
    shots, placed = [], []
    for line in page.evaluate(LINES):
        for at in (bar / 2, bar):
            scroll_to(page, round(line["y"] - at))
            y = line["y"] - page.evaluate("scrollY")
            placed.append(f"{line['text']!r} at {y:.0f}")
            shots.append(Image.open(BytesIO(page.screenshot(clip=band))).convert("RGB"))
    page.screenshot(path=str(OUT / f"{tag}-solid-bar.png"), clip=band)
    held.evaluate("el => el.remove()")
    worst = max(
        (max(hi for _, hi in ImageChops.difference(shots[0], shot).getextrema()) for shot in shots[1:]),
        default=255,
    )
    check(
        f"{tag}: scrolled, the bar is solid paper (no page line shows through it or meets its rule)",
        len(shots) >= 4 and worst <= 6,
        f"bar {bar:.0f} px, band to {band['height']} px; most any pixel changed: {worst} levels; "
        + "; ".join(placed),
    )


# ---------------------------------------------------------------- round 2: filmed at real speed

# The bar's state on every frame the page draws: how far the scroll and the menu are let down, the
# open drop-down, each drop-down's opacity and visibility, each word's underline, each chevron's
# turn, and where the menu's folds end.
LOGGER = """() => {
  const h = document.querySelector('header');
  const words = [...document.querySelectorAll('#site-navigation [class*="word"]')];
  const chevrons = [...document.querySelectorAll('[data-nav-trigger] svg, [data-nav-sheet-toggle] svg')];
  const panels = [...document.querySelectorAll('[data-nav-panel]')];
  window.__log = []; window.__logging = true;
  const tick = () => {
    const hs = getComputedStyle(h);
    window.__log.push({
      t: performance.timeOrigin + performance.now(),
      r: parseFloat(hs.getPropertyValue('--insc-r')) || 0,
      s: parseFloat(hs.getPropertyValue('--insc-s')) || 0,
      open: (h.querySelector('[data-nav-panel][data-open]') || {}).dataset?.navPanel || null,
      panels: panels.map(p => { const s = getComputedStyle(p);
        return { id: p.dataset.navPanel, o: +s.opacity, vis: s.visibility }; }),
      lines: words.filter(w => (parseFloat(getComputedStyle(w, '::after').scale) || 0) > 0.04)
        .map(w => w.textContent.trim()),
      chev: chevrons.filter(c => c.getBoundingClientRect().width > 0).map(c => getComputedStyle(c).rotate),
      folds: [...document.querySelectorAll('[data-nav-sheet] [id^="nav-sheet-"]')].map(f => {
        const r = f.getBoundingClientRect(); return { id: f.id, bottom: r.bottom }; }),
    });
    if (window.__logging) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}"""

# The multiplied pictures in a drop-down or a fold (paintings and pools; the contact shadows sit
# under the bottles' feet, so they are left out), where each is drawn.
PICTURES = """(sel) => {
  const drawn = img => {
    const r = img.getBoundingClientRect(); const s = getComputedStyle(img);
    const nw = img.naturalWidth || r.width, nh = img.naturalHeight || r.height;
    if (s.objectFit !== 'contain') return { x: r.x, y: r.y, w: r.width, h: r.height };
    const k = Math.min(r.width / nw, r.height / nh);
    return { x: r.x + (r.width - nw * k) / 2, y: r.y + (r.height - nh * k) / 2, w: nw * k, h: nh * k };
  };
  return [...document.querySelectorAll(sel + ' img')].filter(img => {
    const s = getComputedStyle(img);
    return s.mixBlendMode === 'multiply' && s.display !== 'none' && +s.opacity > 0.05 &&
      img.getBoundingClientRect().width > 4;
  }).map((img, i) => {
    const kind = /pool/i.test(img.className) ? 'pool' : /contact/i.test(img.className) ? 'contact' : 'painting';
    const masked = getComputedStyle(img).maskImage !== 'none';
    const file = new URL(img.currentSrc || img.src, location.href).searchParams.get('url') || '';
    return { name: (img.dataset.painting || kind) + (masked ? '(mean)' : '') + '#' + i, kind, masked, file, ...drawn(img) };
  }).filter(p => p.kind !== 'contact');
}"""

# Paper beside the pictures: the middle of each gap between neighbouring items on one row.
GAPS = """(sel) => { const items = [...document.querySelectorAll(sel)].map(li => li.getBoundingClientRect())
  .filter(r => r.width > 0); const out = [];
  for (let i = 1; i < items.length; i++)
    if (Math.abs(items[i].top - items[i - 1].top) < 4) out.push((items[i - 1].right + items[i].left) / 2);
  return out; }"""


class Film:
    """Every frame the compositor draws (CDP screencast, with wall-clock times) while `act` runs,
    and the bar's state on every frame the page draws."""

    def __init__(self, page):
        self.page = page
        self.cdp = page.context.new_cdp_session(page)
        self.raw = []
        self.cdp.on("Page.screencastFrame", self._frame)

    def _frame(self, ev):
        self.raw.append((ev["metadata"]["timestamp"] * 1000.0, ev["data"]))
        try:
            self.cdp.send("Page.screencastFrameAck", {"sessionId": ev["sessionId"]})
        except Exception:
            pass

    def shoot(self, act, ms):
        self.raw = []
        self.page.evaluate(LOGGER)
        self.page.evaluate(
            """() => { window.__t0 = 0; const mark = () => { window.__t0 ||= performance.timeOrigin + performance.now(); };
            for (const type of ['pointerdown', 'touchstart']) document.addEventListener(type, mark, { capture: true, once: true }); }"""
        )
        self.cdp.send("Page.startScreencast", {"format": "png", "everyNthFrame": 1})
        self.page.wait_for_timeout(150)
        act()
        self.page.wait_for_timeout(ms)
        self.cdp.send("Page.stopScreencast")
        self.page.evaluate("window.__logging = false")
        self.page.wait_for_timeout(80)
        self.log = self.page.evaluate("window.__log")
        self.t0 = self.page.evaluate("window.__t0") or self.log[0]["t"] + 150
        return self

    def frames(self, t0=None):
        """(ms since t0, wall time, picture) for every frame filmed."""
        t0 = self.t0 if t0 is None else t0
        return [
            (tw - t0, tw, Image.open(BytesIO(base64.b64decode(data))).convert("RGB"))
            for tw, data in self.raw
        ]

    def state(self, tw):
        """The bar's state on the page's last frame at or before wall time tw."""
        best = self.log[0]
        for entry in self.log:
            if entry["t"] > tw:
                break
            best = entry
        return best


def luma(img):
    return np.asarray(img.convert("L"), dtype=np.float32)


def box_mean(a, box, k):
    x0, y0, x1, y1 = (int(round(v * k)) for v in box)
    return float(a[y0:y1, x0:x1].mean())


def samples(pic):
    """Boxes inside a picture. A painting: a grid over it. A pool: its picture's upper corners beside
    the bottle's foot, white in the picture (so exactly the paper under multiply)."""
    x, y, w, h = pic["x"], pic["y"], pic["w"], pic["h"]
    if pic["kind"] == "pool" and pic.get("masked"):
        # A bottle's pool fades out through an elliptical mask from 72% of its radius, so its
        # corners show nothing. It is read instead at the points inside the ellipse where its own
        # painting is paper (the bottle is hidden while it is filmed), and light_boxes averages
        # them: multiplied, they sit a little under the page's paper (the painting's paper is 2%
        # off white, about -7 levels); an isolated blend shows them over it (about +3).
        pool = np.asarray(
            Image.open(Path(__file__).parents[2] / "public" / pic["file"].lstrip("/"))
            .convert("L")
            .resize((max(1, round(w)), max(1, round(h)))),
            dtype=np.float32,
        )
        yy, xx = np.mgrid[0 : pool.shape[0], 0 : pool.shape[1]]
        inside = ((xx / pool.shape[1] - 0.5) / 0.5) ** 2 + ((yy / pool.shape[0] - 0.5) / 0.5) ** 2 <= 0.66**2
        points = np.argwhere(inside & (pool >= 249))
        return [(x + px - 1, y + py - 1, x + px + 2, y + py + 2) for py, px in points[:: max(1, len(points) // 60)]]
    if pic["kind"] == "pool":
        return [
            (bx, y + h * fy, bx + 4, y + h * fy + 4)
            for fy in (0.04, 0.22)
            for bx in (x + 1, x + w - 5)
        ]
    return [
        (x + 10 + (w - 28) * i / 5, y + 10 + (h - 28) * j / 3, x + 18 + (w - 28) * i / 5, y + 18 + (h - 28) * j / 3)
        for i in range(6)
        for j in range(4)
    ]


def light_boxes(film, pics, gaps, reveal, width, lo, hi, under=None):
    """Under multiply nothing in a picture can be lighter than the paper it lies on; an isolated blend
    shows the picture's white paper as a light box. For each picture, frame by frame from lo to hi ms:
    its lightest sample minus the paper beside it at the same height, counting only what the scroll
    (or fold) has already let down, with a margin. A value counts when two frames running show it.
    With `under` (a picture of the same view with the pictures lifted off the paper), each sample is
    read against the paper under it instead, the same fibre in the same place: the paper's own grain
    (a few levels between one place and another) then never reads as light, and a light box (about
    +12 levels for these paintings, measured) stands out from nothing.
    Returns {picture: (worst levels, frames measured)}."""
    series = {p["name"]: [] for p in pics}
    boxes = {p["name"]: samples(p) for p in pics}
    base = None if under is None else (luma(under), under.width / width)
    for t, tw, img in film.frames():
        if not lo - 40 <= t <= hi:
            continue
        a, k = luma(img), img.width / width
        edge = reveal(film.state(tw - 60))
        for pic in pics:
            found = []
            for box in boxes[pic["name"]]:
                if box[3] > edge - 10 or box[0] < 0 or box[2] > width:
                    continue
                if base is not None:
                    found.append(box_mean(a, box, k) - box_mean(base[0], box, base[1]))
                    continue
                cy = (box[1] + box[3]) / 2
                refs = [(g - 3, cy - 4, g + 3, cy + 4) for g in gaps if 0 < g < width]
                if refs:
                    found.append(box_mean(a, box, k) - sum(box_mean(a, r, k) for r in refs) / len(refs))
            best = None
            if found:
                best = sum(found) / len(found) if pic.get("masked") else max(found)
            series[pic["name"]].append((t, best))
    out = {}
    for name, s in series.items():
        held = [min(u, v) for (tu, u), (_, v) in zip(s, s[1:]) if u is not None and v is not None and tu >= lo]
        out[name] = (round(max(held), 1) if held else None, sum(1 for t, v in s if v is not None and t >= lo))
    return out


def paper_under(page, sel):
    """The view as it is, with a drop-down's paintings lifted off the paper (hidden): the paper under
    each of them, for light_boxes(under=...)."""
    tag = page.add_style_tag(content=f"{sel} img[data-plate] {{ visibility: hidden !important; }}")
    page.wait_for_timeout(120)
    shot = Image.open(BytesIO(page.screenshot())).convert("RGB")
    tag.evaluate("el => el.remove()")
    page.wait_for_timeout(120)
    return shot


def no_light_box(name, found, frames=6):
    # A masked pool is averaged: multiplied it reads -2 to -7 levels, an isolated blend about +3.
    limit = {k: 1 if "(mean)" in k else 4 for k in found}
    check(
        name,
        found and all(v is not None and v <= limit[k] and n >= frames for k, (v, n) in found.items()),
        {k: f"{v:+} levels over {n} frames" if v is not None else "not measured" for k, (v, n) in found.items()},
    )


def sideways(rotate):
    """A chevron turned more than 20 degrees off pointing up or down."""
    deg = 0.0 if rotate in ("", "none") else float(rotate.split()[-1].replace("deg", ""))
    return abs(math.sin(math.radians(deg))) > math.sin(math.radians(20))


def warm(page):
    """Point at the bar so the drop-downs' pictures load, wait for them, then leave."""
    page.mouse.move(1100, 40)
    page.wait_for_timeout(300)
    page.wait_for_function(
        "[...document.querySelectorAll('[data-nav-panel] img')].every(i => i.complete && i.naturalWidth > 0)",
        timeout=30000,
    )
    page.mouse.move(760, 880)
    page.wait_for_timeout(900)


def drop_down_motion(browser):
    """Round 2: opening a drop-down shows no light box; moving between them shows no empty scroll,
    no second underline and no sideways chevron. Filmed from the tall bar and from the scrolled bar."""
    for scrolled in (False, True):
        tag = "desk scrolled" if scrolled else "desk"
        page = browser.new_page(viewport={"width": 1536, "height": 900})
        watch(page)
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(2500)
        page.mouse.move(760, 880)
        if scrolled:
            scroll_to(page, 1400)
        warm(page)
        film = Film(page)
        deckle = page.evaluate("parseFloat(getComputedStyle(document.querySelector('header')).getPropertyValue('--deckle'))")
        for panel in ("science", "products"):
            box = page.locator(f'[data-nav-trigger="{panel}"]').bounding_box()
            hide = None
            if panel == "products":
                # The pools are measured where the bottles stand over them, and the ground line runs
                # through them: both are hidden while they are filmed.
                hide = page.add_style_tag(
                    content='[data-nav-panel="products"] :is([class*="__bottle"], [class*="__shelfGround"]) { visibility: hidden !important; }'
                )
            film.shoot(lambda box=box: page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2), 1500)
            sel = f'[data-nav-panel="{panel}"]'
            top, height = page.evaluate(
                f"(() => {{ const r = document.querySelector('{sel}').getBoundingClientRect(); return [r.top, r.height]; }})()"
            )
            pics = page.evaluate(PICTURES, sel)
            found = light_boxes(
                film,
                pics,
                page.evaluate(GAPS, f"{sel} li"),
                lambda e: top + e["r"] * height - deckle,
                1536,
                250,
                1500,
                under=paper_under(page, sel) if panel == "science" else None,
            )
            files = sorted(pic["file"].rsplit("/", 1)[-1] for pic in pics)
            if panel == "science":
                name = f"{tag}: Science opens with no light box behind its three paintings (filmed at real speed)"
                want = sorted(["mito.webp", "reading-still-life.webp", "inkstone-v2.webp"])
            else:
                name = f"{tag}: Products opens with no light box round the five bottles' pools (filmed at real speed)"
                want = ["pool.webp"] * 5
            if files == want:
                no_light_box(name, found)
            else:
                check(name, False, f"pictures measured: {files}")
            if hide:
                hide.evaluate("el => el.remove()")
                page.wait_for_timeout(100)
            page.screenshot(path=str(OUT / f"{tag.replace(' ', '-')}-{panel}-filmed.png"))
            if panel == "science":
                page.keyboard.press("Escape")
                page.mouse.move(760, 880)
                page.wait_for_timeout(900)
        if not scrolled:
            switches(page, film)
        page.close()


def switches(page, film):
    """Products is down. Point across to Science and back, then on to About, filming each move."""
    band = page.evaluate(
        """() => { const top = document.querySelector('[data-nav-panel]').getBoundingClientRect().top + 12;
        const foot = Math.max(...[...document.querySelectorAll('[data-nav-panel] a[class*=more]')]
          .map(a => a.getBoundingClientRect().bottom));
        return [120, Math.round(top - 6), 1416, Math.round(foot + 6)]; }"""
    )

    def ink(img):
        a = luma(img)[band[1] : band[3], band[0] : band[2]]
        return float(np.clip(np.median(a) - a - 6, 0, None).mean())

    for leave, arrive in (("products", "science"), ("science", "products")):
        before = ink(Image.open(BytesIO(page.screenshot())))
        box = page.locator(f'[data-nav-trigger="{arrive}"]').bounding_box()
        film.shoot(lambda: page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=4), 1100)
        page.wait_for_timeout(900)
        after = ink(Image.open(BytesIO(page.screenshot())))
        flip = next((e["t"] for e in film.log if e["open"] == arrive), None)
        if flip is None:
            check(f"desk: {leave} -> {arrive}: the move happened", False, "it never opened")
            continue
        lighter = min(before, after)
        shares = [round(ink(img) / lighter, 2) for t, _, img in film.frames(flip) if -20 <= t <= 800]
        check(
            f"desk: {leave.capitalize()} -> {arrive.capitalize()}: the scroll is never empty (filmed: its ink never below 60% of the lighter drop-down's)",
            len(shares) >= 10 and min(shares) >= 0.6,
            f"least {min(shares, default=0)} over {len(shares)} frames; at rest {before:.1f} -> {after:.1f}",
        )
        during = [e for e in film.log if flip - 40 <= e["t"] <= flip + 900]
        thin = [round(e["t"] - flip) for e in during if not any(p["vis"] == "visible" and p["o"] >= 0.6 for p in e["panels"])]
        check(
            f"desk: {leave.capitalize()} -> {arrive.capitalize()}: one drop-down always drawn whole (at least 60%), every frame",
            len(during) >= 30 and not thin,
            f"{len(during)} frames; thin at {thin[:5]} ms",
        )
        two = [(round(e["t"] - flip), e["lines"]) for e in during if len(e["lines"]) > 1]
        turned = [(round(e["t"] - flip), e["chev"]) for e in during if any(sideways(r) for r in e["chev"])]
        check(
            f"desk: {leave.capitalize()} -> {arrive.capitalize()}: only one word underlined and no chevron sideways, every frame",
            len(during) >= 30 and not two and not turned,
            f"{len(during)} frames; two lines {two[:3]}; sideways {turned[:3]}",
        )
    box = page.locator("#site-navigation a[href$='/about']").bounding_box()
    film.shoot(lambda: page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=6), 1300)
    two = [(round(e["t"] - film.t0), e["lines"]) for e in film.log if len(e["lines"]) > 1]
    check(
        "desk: pointing from the open Products on to About, one line at a time (filmed)",
        not two and not is_open(page, "products") and film.log[-1]["lines"] == ["About"],
        f"{len(film.log)} frames; two lines {two[:3]}; last {film.log[-1]['lines']}",
    )


# ---------------------------------------------------------------- round 11: the two rows

SLUGS = ["nuricell", "green-bee-propolis", "advanced-opc", "turmerific", "nature-calm"]
NAMES = ["NuriCell", "Green Bee Propolis", "Advanced OPC Formula", "Turmerific", "Nature Calm"]
PARTS = ["Our scientists", "Cellular health", "Research library", "Ask BiGH Science"]
PART_HREFS = ["/science#scientists", "/science#health", "/science#research", "/science#ask"]
PLATES = ["print", "cell", "reading", "inkstone"]
PAINTED = {"mito": "cell", "reading": "reading", "inkstone": "inkstone"}
ROW_SIZES = ((1536, 900, 1), (1280, 800, 1), (1920, 1080, 2), (1101, 800, 1), (1366, 657, 1))

# A drop-down's row as drawn: its title, each part (its link, picture room, picture, name and line:
# their boxes, the lines their words are set on, their sizes, whether the name is lined, how far a
# bottle is lifted, a Science picture's opacity and scale, how sharp its picture is), the pools,
# the ground line, the link under the row and the scroll's foot.
ROW = r"""(id) => {
  const p = document.querySelector(`[data-nav-panel="${id}"]`);
  const box = el => { const r = el.getBoundingClientRect();
    return { l: r.left, r: r.right, t: r.top, b: r.bottom, w: r.width, h: r.height }; };
  const lines = el => { const g = document.createRange(); g.selectNodeContents(el);
    const rects = [...g.getClientRects()].filter(x => x.width > 1 && x.height > 1);
    return { first: rects.length ? rects[0].top : null, last: rects.length ? Math.max(...rects.map(x => x.top)) : null,
      count: new Set(rects.map(x => Math.round(x.top))).size,
      l: Math.min(...rects.map(x => x.left)), r: Math.max(...rects.map(x => x.right)), b: Math.max(...rects.map(x => x.bottom)) }; };
  const seen = el => el.checkVisibility({ opacityProperty: true, visibilityProperty: true });
  const items = [...p.querySelectorAll('[data-nav-item]')].map(a => {
    const n = a.querySelector('[data-nav-item-name]'), f = a.querySelector('[data-nav-item-line]');
    const room = a.querySelector('[class*="__stand"], [class*="__room"]');
    const img = a.querySelector('img[class*="__bottle"], img[data-plate], [data-plate] img');
    const plate = a.querySelector('[data-plate]');
    const bottle = a.querySelector('img[class*="__bottle"]');
    const w = /[?&]w=(\d+)/.exec(img.currentSrc);
    const t = bottle ? getComputedStyle(bottle).translate : 'none';
    return { href: a.getAttribute('href'), name: n.textContent.trim(), line: f.textContent.trim(),
      size: parseFloat(getComputedStyle(n).fontSize), fsize: parseFloat(getComputedStyle(f).fontSize),
      a: box(a), n: box(n), f: box(f), room: box(room), nl: lines(n), fl: lines(f),
      img: { w: w ? +w[1] : 0, css: img.getBoundingClientRect().width, h: img.getBoundingClientRect().height,
        loaded: img.complete && img.naturalWidth > 0, o: bottle ? +getComputedStyle(bottle).opacity : 1 },
      plate: plate ? { kind: plate.dataset.plate, ...box(plate), o: +getComputedStyle(plate).opacity,
        scale: getComputedStyle(plate).scale } : null,
      lift: t === 'none' ? 0 : parseFloat(t.split(' ')[1] || '0'),
      lined: parseFloat(getComputedStyle(n.firstElementChild).backgroundSize) || 0,
      visible: seen(n) && seen(f) && seen(img) };
  });
  const ground = p.querySelector('[class*="__shelfGround"]');
  const paper = document.querySelector('header [class*="__paper"]').getBoundingClientRect();
  return { items, title: box(p.querySelector('h2')),
    pools: [...p.querySelectorAll('img[class*="__pool"]')].map(i => ({ o: +getComputedStyle(i).opacity,
      mask: getComputedStyle(i).maskImage, blend: getComputedStyle(i).mixBlendMode })),
    contacts: p.querySelectorAll('img[class*="__contact"]').length,
    ground: ground ? { mask: getComputedStyle(ground).maskImage, ...box(ground) } : null,
    links: [...p.querySelectorAll('a[class*="more"]')].map(a => ({ text: a.textContent.trim(), href: a.getAttribute('href'), ...box(a) })),
    paperBottom: paper.bottom, deckle: parseFloat(getComputedStyle(document.querySelector('header')).getPropertyValue('--deckle')),
    vh: innerHeight, vw: innerWidth, dpr: devicePixelRatio };
}"""


def open_panel(page, panel):
    """Reach for the bar (the pictures load), then open a drop-down with a click and rest the
    pointer on empty paper inside the scroll."""
    w = page.viewport_size["width"]
    page.mouse.move(w * 0.7, 40)
    page.wait_for_timeout(300)
    page.wait_for_function(
        "[...document.querySelectorAll('[data-nav-panel] img')].every(i => i.complete && i.naturalWidth > 0)",
        timeout=30000,
    )
    page.mouse.move(w / 2, page.viewport_size["height"] - 6)
    page.wait_for_timeout(600)
    page.locator(f'[data-nav-trigger="{panel}"]').click()
    page.wait_for_timeout(200)
    bar = page.evaluate("document.querySelector('#site-navigation').getBoundingClientRect().bottom")
    page.mouse.move(12, bar + 30, steps=4)
    page.wait_for_timeout(1500)


def rest_on(page, panel, i, ms=1000):
    """Rest the pointer on a part of a row, on its picture."""
    b = page.locator(f'[data-nav-panel="{panel}"] [data-nav-item]').nth(i).bounding_box()
    page.mouse.move(b["x"] + b["width"] / 2, b["y"] + b["height"] * 0.35, steps=4)
    page.wait_for_timeout(ms)
    return b


def one_row(tag, what, info, want, english=True):
    """All of a row's parts at once, side by side in one row, inside the window and above the
    scroll's torn foot; the names on one line and every line starting on one line, each centred under
    its picture; names 21px+, lines 17px+; every name and line inside its own column."""
    items = info["items"]
    tops = [i["room"]["t"] for i in items]
    order = all(a["a"]["r"] <= b["a"]["l"] + 0.5 for a, b in zip(items, items[1:]))
    foot = info["paperBottom"] - info["deckle"]
    inside = all(
        i["a"]["l"] >= 0 and i["a"]["r"] <= info["vw"] and i["room"]["t"] >= 0 and i["fl"]["b"] <= min(foot, info["vh"])
        for i in items
    )
    own = all(
        i["nl"]["l"] >= i["a"]["l"] - 0.5 and i["nl"]["r"] <= i["a"]["r"] + 0.5
        and i["fl"]["l"] >= i["a"]["l"] - 0.5 and i["fl"]["r"] <= i["a"]["r"] + 0.5
        for i in items
    )
    check(
        f"{tag}: {what}: all {len(want)} at once in one row (picture, name and line each seen), side by side, "
        "inside the window and above the scroll's torn foot, every name and line inside its own column",
        [i["name"] for i in items] == want and all(i["visible"] for i in items) and max(tops) - min(tops) <= 1
        and order and inside and own,
        f"rooms' tops {sorted(set(round(t) for t in tops))}; columns {[(round(i['a']['l']), round(i['a']['r'])) for i in items]}; "
        f"lowest line {max(i['fl']['b'] for i in items):.0f}, torn foot {foot:.0f}, window {info['vh']}",
    )
    # A name stands at the foot of the names' row: the names share their last line (one line in
    # English), and every line starts on one line.
    firsts = [i["nl"]["last"] for i in items]
    starts = [i["fl"]["first"] for i in items]
    centred = [abs((i["nl"]["l"] + i["nl"]["r"]) / 2 - (i["room"]["l"] + i["room"]["r"]) / 2) for i in items]
    check(
        f"{tag}: {what}: shared baselines (the names on one line, every line starting on one line, 1px), each name "
        f"centred under its picture (2px) and its line right under it (8px or less); names 21px+, lines 17px+"
        + ("" if english else ", names in two lines or fewer"),
        max(firsts) - min(firsts) <= 1
        and max(starts) - min(starts) <= 1
        and max(centred) <= 2
        and all(i["n"]["t"] >= i["room"]["b"] - 1 and 0 <= i["f"]["t"] - i["n"]["b"] <= 8 for i in items)
        and all(i["size"] >= 21 and i["fsize"] >= 17 for i in items)
        and all(i["nl"]["count"] <= (1 if english else 2) for i in items),
        f"names at {sorted(set(round(x, 1) for x in firsts))}, lines at {sorted(set(round(x, 1) for x in starts))}; "
        f"off centre {max(centred):.1f}px; name lines {[i['nl']['count'] for i in items]}; sizes {[(i['size'], i['fsize']) for i in items][:1]}",
    )


def ground_ink(page, info):
    """The ground line's ink across its thickness, in the pixels, in each gap between two bottles:
    the rows at least 25 levels darker than the paper above and below it (a painted line: a few
    pixels; the old squashed stroke was a 16px grey rod)."""
    img = luma(Image.open(BytesIO(page.screenshot())))
    k = img.shape[1] / info["vw"]
    g = info["ground"]
    mid = (g["t"] + g["b"]) / 2
    out = []
    for a, b in zip(info["items"], info["items"][1:]):
        x = (a["room"]["r"] + b["room"]["l"]) / 2
        cols = img[round((mid - 16) * k) : round((mid + 16) * k), round((x - 4) * k) : round((x + 4) * k)]
        paper = float(np.median(np.concatenate([cols[: round(5 * k)], cols[-round(5 * k) :]])))
        out.append(round(float(np.median((cols < paper - 25).sum(axis=0))) / k, 1))
    return out


def weigh(img, stand):
    """The ink of the picture standing in `stand` (a screenshot): its height (rows 30+ levels darker
    than the paper beside the stand) and its mass (darkness summed over the stand, widened 15% each
    side for the paintings that run past it; the name under it is left out)."""
    a = luma(img)
    k = img.width / stand["vw"]
    x0, x1 = (stand["l"] - 0.15 * stand["w"]) * k, (stand["r"] + 0.15 * stand["w"]) * k
    y0, y1 = (stand["t"] - 0.04 * stand["h"]) * k, stand["b"] * k
    # The paper: the band just above the picture's room, across it (in a row, beside a picture is
    # its neighbour, or the window's edge).
    paper = float(np.median(a[round(y0 - 10 * k) : round(y0 - 2 * k), round(x0) : round(x1)]))
    dark = np.clip(paper - a[round(y0) : round(y1), round(x0) : round(x1)], 0, None)
    rows = np.where((dark > 30).sum(axis=1) > 2)[0]
    return {"h": round(float(rows.max() - rows.min()) / k) if len(rows) else 0, "mass": float(dark.sum()) / (k * k * 1e3)}


def row_layout(browser):
    """Round 11: each drop-down is one row, everything at once. At each desktop size: Products shows
    the five side by side, each bottle on its own pale pool, all on one painted ground line, crisp;
    Science its four parts the same way, the pictures at one weight; the two share one page (the
    title, the pictures' row, the names' line and the link under them); every part one link; the
    scroll ends above the window's foot."""
    for w, h, dsf in ROW_SIZES:
        tag = f"rows {w}x{h}" + (f"@{dsf}x" if dsf > 1 else "")
        page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=dsf)
        watch(page)
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(2000)
        open_panel(page, "products")
        page.screenshot(path=str(OUT / f"rows-products-{w}x{h}.png"))
        pro = page.evaluate(ROW, "products")
        one_row(tag, "Products", pro, NAMES)
        thick = ground_ink(page, pro)
        items = pro["items"]
        check(
            f"{tag}: Products: each bottle on its own pale pool (multiplied, 45-65%), all on one painted ground line "
            "(the bar's stroke: 1-8px of ink in every gap, under half the old 16px rod), each crisp (its picture at least "
            "its size on screen) and 170px+ tall",
            len(pro["pools"]) == 5
            and all(0.45 <= x["o"] <= 0.65 and x["blend"] == "multiply" and "radial-gradient" in x["mask"] for x in pro["pools"])
            and pro["contacts"] == 5
            and pro["ground"] and "rule-whole.webp" in pro["ground"]["mask"]
            and all(1 <= t <= 8 for t in thick)
            and all(i["img"]["w"] >= i["img"]["css"] * pro["dpr"] * 0.98 and i["img"]["h"] >= 170 for i in items),
            f"pools {[round(x['o'], 2) for x in pro['pools']]}; ground ink {thick}px; "
            f"bottles {[(i['img']['w'], round(i['img']['css'] * pro['dpr'])) for i in items]}, {items[0]['img']['h']:.0f}px tall",
        )
        check(
            f"{tag}: the scroll ends above the window's foot",
            pro["paperBottom"] <= pro["vh"],
            f"scroll foot {pro['paperBottom']:.0f}, window {pro['vh']}",
        )
        if (w, h) == (1536, 900):
            more = pro["links"][0]
            check(
                "rows: every product is one link to its own page; Explore our products under the row, centred, to the products",
                [i["href"] for i in items] == [f"/products/{s}" for s in SLUGS]
                and all(i["a"]["h"] >= 48 and i["a"]["w"] >= 48 for i in items)
                and len(pro["links"]) == 1
                and more["text"].startswith("Explore our products") and more["href"].endswith("/#products")
                and more["t"] >= max(i["a"]["b"] for i in items)
                and abs((more["l"] + more["r"]) / 2 - w / 2) <= 2,
                f"{[i['href'] for i in items]}; {[(x['text'], x['href']) for x in pro['links']]}",
            )
        bottle = None
        if (w, h) in ((1536, 900), (1101, 800), (1920, 1080)):
            shot = Image.open(BytesIO(page.screenshot())).convert("RGB")
            bottle = max(weigh(shot, dict(i["room"], vw=w))["h"] for i in items)
        page.keyboard.press("Escape")
        page.mouse.move(w / 2, h - 6)
        page.wait_for_timeout(900)

        open_panel(page, "science")
        page.screenshot(path=str(OUT / f"rows-science-{w}x{h}.png"))
        sci = page.evaluate(ROW, "science")
        pro = page.evaluate(ROW, "products")
        one_row(tag, "Science", sci, PARTS)
        same = lambda u, v: abs(u - v) <= 1  # noqa: E731
        s, p = sci["items"], pro["items"]
        check(
            f"{tag}: one page with Products (1px): the title, the pictures' row (top and height), the names' line, "
            "the captions on the focus lines' line, the link under the row on its line",
            same(sci["title"]["t"], pro["title"]["t"])
            and all(same(a["room"]["t"], p[0]["room"]["t"]) and same(a["room"]["h"], p[0]["room"]["h"]) for a in s)
            and same(s[0]["nl"]["last"], p[0]["nl"]["last"])
            and same(s[0]["fl"]["first"], p[0]["fl"]["first"])
            and same(sci["links"][0]["b"], pro["links"][0]["b"]),
            f"titles {sci['title']['t']:.0f}/{pro['title']['t']:.0f}; rooms {s[0]['room']['t']:.0f}+{s[0]['room']['h']:.0f} vs "
            f"{p[0]['room']['t']:.0f}+{p[0]['room']['h']:.0f}; names {s[0]['nl']['last']:.0f}/{p[0]['nl']['last']:.0f}; "
            f"lines {s[0]['fl']['first']:.0f}/{p[0]['fl']['first']:.0f}; links {sci['links'][0]['b']:.0f}/{pro['links'][0]['b']:.0f}",
        )
        crisp = [(i["plate"]["kind"], i["img"]["w"], round(i["img"]["css"] * sci["dpr"])) for i in s]
        check(
            f"{tag}: Science: Dr. Liu's print 75%+ of its room's height, every picture crisp (its picture at least its size on screen)",
            [i["plate"]["kind"] for i in s] == PLATES
            and s[0]["plate"]["h"] >= 0.75 * s[0]["room"]["h"]
            and all(have >= need * 0.98 for _, have, need in crisp),
            f"print {s[0]['plate']['h']:.0f}px in a {s[0]['room']['h']:.0f}px room; {crisp}",
        )
        if bottle is not None:
            shot = Image.open(BytesIO(page.screenshot())).convert("RGB")
            weights = [weigh(shot, dict(i["room"], vw=w)) for i in s]
            paintings = [x["mass"] for x in weights[1:]]
            mean = sum(paintings) / 3
            check(
                f"{tag}: the four Science pictures of one weight (paintings' ink within 25% of their mean; the print as tall as any painting and 75%+ of a bottle)",
                all(abs(m / mean - 1) <= 0.25 for m in paintings)
                and all(weights[0]["h"] >= x["h"] for x in weights[1:])
                and weights[0]["h"] >= 0.75 * bottle,
                f"ink {[round(m / mean, 2) for m in paintings]} of the paintings' mean; heights "
                f"{dict(zip(PLATES, [x['h'] for x in weights]))}, bottle {bottle}",
            )
        if (w, h) == (1536, 900):
            more = sci["links"][0]
            check(
                "rows: every Science part is one link to its own part of the Science page; Explore the science under the row, centred",
                [i["href"] for i in s] == PART_HREFS
                and all(i["a"]["h"] >= 48 and i["a"]["w"] >= 48 for i in s)
                and len(sci["links"]) == 1
                and more["text"].startswith("Explore the science") and more["href"] == "/science"
                and more["t"] >= max(i["a"]["b"] for i in s)
                and abs((more["l"] + more["r"]) / 2 - w / 2) <= 2,
                f"{[i['href'] for i in s]}; {[(x['text'], x['href']) for x in sci['links']]}",
            )
        page.close()


def row_reach(browser):
    """Round 11: every part is reachable directly. By keyboard: Enter opens a drop-down, Tab steps
    through its parts in order (each ringed, its name lined; a bottle lifted, a Science picture
    brought forward while the others ease back a little), then the link under the row. By pointer:
    resting on a part does the same, and a click opens its page. On a touch laptop: the first tap on
    a part opens its page."""
    for panel, want, more in (("products", NAMES, "Explore our products"), ("science", PARTS, "Explore the science")):
        page = browser.new_page(viewport={"width": 1536, "height": 900})
        watch(page)
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(2000)
        warm(page)
        page.mouse.move(768, 896)
        page.locator(f'[data-nav-trigger="{panel}"]').focus()
        page.keyboard.press("Enter")
        page.wait_for_timeout(1300)
        bad = []
        for i, name in enumerate(want):
            page.keyboard.press("Tab")
            page.wait_for_timeout(900)
            info = page.evaluate(ROW, panel)
            ring = page.evaluate(FOCUS_RING)
            lined = [x["name"] for x in info["items"] if x["lined"] > 50]
            why = []
            if not focused(page).startswith(name):
                why.append(f"focus on {focused(page)[:20]!r}")
            if not ring or ring["style"] == "none":
                why.append("no ring")
            if lined != [name]:
                why.append(f"lined {lined}")
            if panel == "products":
                lifts = [round(x["lift"], 1) for x in info["items"]]
                if not (-6.5 <= lifts[i] <= -5.5 and all(abs(v) < 0.5 for j, v in enumerate(lifts) if j != i)):
                    why.append(f"lifts {lifts}")
            else:
                plates = [(round(x["plate"]["o"], 2), x["plate"]["scale"]) for x in info["items"]]
                if not (plates[i][0] == 1 and plates[i][1] == "1.04"
                        and all(0.6 <= o <= 0.85 and sc in ("none", "1") for j, (o, sc) in enumerate(plates) if j != i)):
                    why.append(f"pictures {plates}")
            if why:
                bad.append(f"{name}: {', '.join(why)}")
            if i == len(want) - 1:
                page.screenshot(path=str(OUT / f"rows-keyboard-{panel}.png"))
        page.keyboard.press("Tab")
        after = focused(page)
        check(
            f"rows: {panel.capitalize()}: Enter opens it and Tab steps through its {len(want)} parts in order, each ringed and its name lined"
            + (" and its bottle lifted 6px (the others down)" if panel == "products" else ", its picture forward and the others eased back a little (60-85%)")
            + f", then {more}",
            not bad and more in after,
            ("; ".join(bad) or "all") + f"; then {after!r}",
        )
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

        open_panel(page, panel)
        at = 3 if panel == "products" else 2
        rest_on(page, panel, at)
        info = page.evaluate(ROW, panel)
        lined = [x["name"] for x in info["items"] if x["lined"] > 50]
        if panel == "products":
            lifts = [round(x["lift"], 1) for x in info["items"]]
            ok = -6.5 <= lifts[at] <= -5.5 and all(abs(v) < 0.5 for j, v in enumerate(lifts) if j != at)
            detail = f"lifts {lifts}"
            what = "lifts its bottle a little (6px), the others standing"
        else:
            plates = [(round(x["plate"]["o"], 2), x["plate"]["scale"]) for x in info["items"]]
            ok = plates[at] == (1, "1.04") and all(0.6 <= o <= 0.85 for j, (o, _) in enumerate(plates) if j != at)
            detail = f"pictures {plates}"
            what = "brings its picture gently forward, the others easing back a little (60-85%)"
        page.screenshot(path=str(OUT / f"rows-point-{panel}.png"))
        check(
            f"rows: {panel.capitalize()}: resting the pointer on {want[at]} {what} and lines only its name",
            ok and lined == [want[at]],
            f"{detail}; lined {lined}",
        )
        target = info["items"][at]["href"]
        b = info["items"][at]["a"]
        page.mouse.click(b["l"] + b["w"] / 2, b["t"] + b["h"] * 0.35)
        page.wait_for_url(f"**{target}", timeout=30000)
        check(f"rows: {panel.capitalize()}: a click on {want[at]} opens its page", page.url.endswith(target), page.url)
        page.close()

        ctx = browser.new_context(viewport={"width": 1536, "height": 900}, has_touch=True)
        page = ctx.new_page()
        watch(page)
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(2000)
        page.locator(f'[data-nav-trigger="{panel}"]').tap()
        page.wait_for_timeout(1200)
        target = "/products/green-bee-propolis" if panel == "products" else "/science#ask"
        page.locator(f'[data-nav-panel="{panel}"] [data-nav-item]', has_text=want[1 if panel == "products" else 3]).tap()
        try:
            page.wait_for_url(f"**{target}", timeout=30000)
        except Exception:
            pass
        check(f"rows: {panel.capitalize()}: on a touch laptop the first tap on a part opens its page", page.url.endswith(target), page.url)
        ctx.close()


# Every frame: which names of a row are lined (their line over 4% drawn), how far each bottle is
# lifted and how see-through it is, and each Science picture's opacity.
ROW_LOG = """(id) => { const p = document.querySelector(`[data-nav-panel="${id}"]`);
  const items = [...p.querySelectorAll('[data-nav-item]')];
  window.__log = []; window.__logging = true;
  const tick = () => { window.__log.push({ t: performance.timeOrigin + performance.now(),
      lines: items.filter(a => (parseFloat(getComputedStyle(a.querySelector('[data-nav-item-name] > span')).backgroundSize) || 0) > 4)
        .map(a => a.querySelector('[data-nav-item-name]').textContent.trim()),
      lifts: items.map(a => { const b = a.querySelector('img[class*="__bottle"]'); if (!b) return 0;
        const t = getComputedStyle(b).translate; return t === 'none' ? 0 : parseFloat(t.split(' ')[1] || '0'); }),
      bottles: items.map(a => { const b = a.querySelector('img[class*="__bottle"]'); return b ? +getComputedStyle(b).opacity : 1; }),
      o: Object.fromEntries([...p.querySelectorAll('[data-plate]')].map(x => [x.dataset.plate, +getComputedStyle(x).opacity])) });
    if (window.__logging) requestAnimationFrame(tick); };
  requestAnimationFrame(tick); }"""


def row_motion(browser):
    """Round 11, filmed at real speed: the pointer moves along each row, resting on each part. One
    name lined on every frame; a bottle lifts at most its 6px and never fades; a Science picture
    never eases back past 60% and no painting shows its paper as a light box. Then over to Products
    and back: Science swaps in with no light box behind its paintings."""
    page = browser.new_page(viewport={"width": 1536, "height": 900})
    watch(page)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(2500)
    film = Film(page)
    for panel, want in (("products", NAMES), ("science", PARTS)):
        open_panel(page, panel)
        sel = f'[data-nav-panel="{panel}"]'
        rest_on(page, panel, 0)
        # The paintings where they are drawn at rest (Dr. Liu's print pointed, the three eased back
        # at their own size): pointed, a painting grows from its middle, over these samples.
        pics = {pic["file"]: pic for pic in page.evaluate(PICTURES, sel)} if panel == "science" else {}
        gaps = page.evaluate(GAPS, f"{sel} li")
        page.evaluate(ROW_LOG, panel)
        film.raw = []
        film.cdp.send("Page.startScreencast", {"format": "png", "everyNthFrame": 1})
        page.wait_for_timeout(150)
        for i in range(1, len(want)):
            rest_on(page, panel, i, 450)
        page.wait_for_timeout(700)
        film.cdp.send("Page.stopScreencast")
        page.evaluate("window.__logging = false")
        film.log = page.evaluate("window.__log")
        film.t0 = film.log[0]["t"]
        two = [e["lines"] for e in film.log if len(e["lines"]) > 1]
        if panel == "products":
            high = min(min(e["lifts"]) for e in film.log)
            faded = min(min(e["bottles"]) for e in film.log)
            check(
                "rows: pointing along the five products (filmed): one name lined on every frame, ending on Nature Calm; "
                "a bottle lifts at most its 6px and none ever fades",
                len(film.log) >= 60 and not two and film.log[-1]["lines"] == ["Nature Calm"] and high >= -6.5 and faded == 1,
                f"{len(film.log)} frames; two at once {two[:3]}; last {film.log[-1]['lines']}; highest lift {high:.1f}px; least bottle {faded}",
            )
        else:
            least = min(min(e["o"].values()) for e in film.log)
            check(
                "rows: pointing along the four Science parts (filmed): one name lined on every frame, ending on Ask BiGH Science; "
                "no picture ever eases back past 60% (never a ghost)",
                len(film.log) >= 60 and not two and film.log[-1]["lines"] == ["Ask BiGH Science"] and least >= 0.6,
                f"{len(film.log)} frames; two at once {two[:3]}; last {film.log[-1]['lines']}; least picture {least:.2f}",
            )
            found = light_boxes(film, list(pics.values()), gaps, lambda e: 10000, 1536, 0, 5000, under=paper_under(page, sel))
            names = sorted(p["file"].rsplit("/", 1)[-1] for p in pics.values())
            name = "rows: no Science painting shows its paper as a light box while the row is pointed along (filmed: never 4+ levels over the paper)"
            if names == sorted(["mito.webp", "reading-still-life.webp", "inkstone-v2.webp"]):
                no_light_box(name, found)
            else:
                check(name, False, f"pictures {names}")
        page.keyboard.press("Escape")
        page.mouse.move(768, 896)
        page.wait_for_timeout(900)

    # Over to Products and back: Science swaps in over Products. Products' pictures (bottles, pools,
    # the ground) stand elsewhere on the page, so during the dissolve they show through the new panel
    # for a few frames: that is Products leaving, not a light box; they are hidden while the paintings
    # are measured.
    open_panel(page, "science")
    sel = '[data-nav-panel="science"]'
    gaps = page.evaluate(GAPS, f"{sel} li")
    box = page.locator('[data-nav-trigger="products"]').bounding_box()
    page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=4)
    page.wait_for_timeout(1300)
    hide = page.add_style_tag(
        content='[data-nav-panel="products"] :is(img, [class*="__shelfGround"]) { visibility: hidden !important; }'
    )
    box = page.locator('[data-nav-trigger="science"]').bounding_box()
    film.shoot(lambda: page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=4), 1300)
    hide.evaluate("el => el.remove()")
    page.screenshot(path=str(OUT / "rows-science-swapped-back.png"))
    shown = page.evaluate(PICTURES, sel)
    flip = next((e["t"] for e in film.log if e["open"] == "science"), None)
    name = "rows: swapping back in from Products, no light box behind Science's paintings (filmed)"
    names = sorted(p["file"].rsplit("/", 1)[-1] for p in shown)
    if flip is None or names != sorted(["mito.webp", "reading-still-life.webp", "inkstone-v2.webp"]):
        check(name, False, f"flip {flip}; shown {names}")
    else:
        found = light_boxes(
            film, shown, gaps, lambda e: 10000, 1536, round(flip - film.t0), round(flip - film.t0) + 900,
            under=paper_under(page, sel),
        )
        no_light_box(name, found)
    page.close()


def row_languages(browser):
    """Round 11: in Vietnamese, Japanese and Korean, at the narrowest desktop and at 1536: both rows
    whole, side by side and inside the window, long names wrapping cleanly in their own column (two
    lines at most, nothing running into a neighbour), the names on one line and the lines starting
    on one line, all above the scroll's foot."""
    for loc in ("vn", "jp", "kr"):
        for w, h in ((1101, 800), (1536, 900)):
            page = browser.new_page(viewport={"width": w, "height": h})
            watch(page)
            page.goto(f"{BASE}/{loc}", wait_until="networkidle")
            page.wait_for_timeout(2000)
            for panel, count in (("products", 5), ("science", 4)):
                open_panel(page, panel)
                page.screenshot(path=str(OUT / f"rows-{loc}{w}-{panel}.png"))
                info = page.evaluate(ROW, panel)
                one_row(f"rows {loc} {w}x{h}", panel.capitalize(), info, [i["name"] for i in info["items"]][:count] if len(info["items"]) == count else [], english=False)
                page.keyboard.press("Escape")
                page.mouse.move(w / 2, h - 6)
                page.wait_for_timeout(900)
            page.close()


def desktop(browser):
    page = browser.new_page(viewport={"width": 1536, "height": 900})
    watch(page)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(2500)
    page.screenshot(path=str(OUT / "desk-top.png"))

    bar = page.evaluate(
        """() => {
      const nav = document.querySelector('#site-navigation');
      const shown = el => { const r = el.getBoundingClientRect(); const s = getComputedStyle(el);
        return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
      const words = [...nav.querySelectorAll('[data-nav-trigger], a, button')]
        .filter(el => shown(el) && !el.closest('[data-nav-panel], [data-nav-sheet]'))
        .map(el => ({ text: (el.innerText || el.getAttribute('aria-label') || '').trim(),
          size: parseFloat(getComputedStyle(el).fontSize), h: el.getBoundingClientRect().height }));
      const select = [...nav.querySelectorAll('select')].filter(shown)
        .map(el => el.closest('label') || el)
        .map(el => ({ text: 'language', size: parseFloat(getComputedStyle(el).fontSize),
          h: el.getBoundingClientRect().height }));
      const mark = nav.querySelector('[data-nav-logo]').getBoundingClientRect();
      return { words: words.concat(select), mark: { x: mark.x + mark.width / 2, w: mark.width },
        width: innerWidth };
    }"""
    )
    texts = [w["text"] for w in bar["words"]]
    check(
        "desk: the bar's links (no Home; the mark goes home)",
        all(t in texts for t in ("Products", "Science", "About", "Support", "Log in", "Sign up"))
        and "Home" not in texts,
        texts,
    )
    check(
        "desk: the mark centred and clearly visible",
        abs(bar["mark"]["x"] - bar["width"] / 2) < 4 and bar["mark"]["w"] >= 120,
        bar["mark"],
    )
    small = [w for w in bar["words"] if w["text"] and w["text"] != "BiGH home" and w["size"] < 18]
    check("desk: words at least 18 px", not small, small)
    short = [w for w in bar["words"] if w["h"] < 47.5]
    check("desk: every control at least 48 px tall", not short, short)

    waiting = page.evaluate(
        "[...document.querySelectorAll('[data-nav-panel] img')].filter(i => i.complete && i.naturalWidth > 0).length"
    )
    check("desk: the drop-downs' pictures wait until the visitor reaches for the bar", waiting == 0, waiting)

    trig = page.locator('[data-nav-trigger="products"]')
    trig.hover()
    page.wait_for_timeout(400)
    check("desk: hover opens Products", is_open(page, "products"))
    check("desk: its button says it is open", trig.get_attribute("aria-expanded") == "true")
    page.wait_for_timeout(900)
    check("desk: the scroll is unrolled", r_value(page) == "1", r_value(page))
    unloaded = page.evaluate(
        "[...document.querySelectorAll('[data-nav-panel=products] img')].filter(i => !i.complete || i.naturalWidth === 0).map(i => i.currentSrc || i.src)"
    )
    check("desk: every picture on the unrolled Products has loaded", not unloaded, unloaded[:3])
    page.screenshot(path=str(OUT / "desk-products.png"))
    box = page.locator('[data-nav-panel="products"] a').first.bounding_box()
    page.mouse.move(box["x"] + box["width"] / 2, box["y"] + 40, steps=8)
    page.wait_for_timeout(700)
    check("desk: the pointer can cross into the panel", is_open(page, "products"))
    page.locator('[data-nav-trigger="science"]').hover()
    samples = []
    for _ in range(6):
        page.wait_for_timeout(60)
        samples.append(float(r_value(page) or 0))
    check(
        "desk: Science swaps in", is_open(page, "science") and not is_open(page, "products")
    )
    check("desk: the swap keeps the scroll down", min(samples) > 0.99, samples)
    page.wait_for_timeout(900)
    page.screenshot(path=str(OUT / "desk-science.png"))
    page.mouse.move(760, 860, steps=6)
    page.wait_for_timeout(800)
    check("desk: leaving closes it", not is_open(page, "science"))
    page.wait_for_timeout(500)
    check("desk: the scroll rolls back up", float(r_value(page) or 1) < 0.01, r_value(page))

    page.locator('[data-nav-trigger="science"]').click()
    page.wait_for_timeout(300)
    check("desk: a click opens Science", is_open(page, "science"))
    page.locator('[data-nav-trigger="science"]').click()
    page.wait_for_timeout(300)
    check("desk: a second click closes it", not is_open(page, "science"))

    page.locator('[data-nav-trigger="products"]').click()
    page.wait_for_timeout(900)
    page.mouse.move(760, 860)
    page.mouse.click(760, 860)
    page.wait_for_timeout(400)
    check("desk: a click on the wash closes it", not is_open(page, "products"))
    check("desk: ...without scrolling the page", page.evaluate("scrollY") < 5, page.evaluate("scrollY"))

    page.mouse.move(760, 600)
    page.locator('[data-nav-trigger="products"]').focus()
    page.keyboard.press("Enter")
    page.wait_for_timeout(300)
    check("desk: Enter opens Products", is_open(page, "products"))
    page.keyboard.press("Tab")
    f = focused(page)
    check("desk: Tab steps into the panel", "NuriCell" in f, f)
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    f = focused(page)
    check(
        "desk: Escape closes it and hands focus back",
        not is_open(page, "products") and "Products" in f,
        f,
    )

    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(2000)
    order = []
    ring = ""
    for _ in range(10):
        page.keyboard.press("Tab")
        order.append(focused(page))
        if "Products" in order[-1]:
            # (Drawn on the control or on a box laid round it: see FOCUS_RING, round 10.)
            r = page.evaluate(FOCUS_RING)
            ring = f"{r['style']} {r.get('width', 0)}px"
    check(
        "desk: the Tab order follows the line",
        order[1].startswith("Choose language")
        and "Products" in order[2]
        and "Science" in order[3]
        and "BiGH home" in order[4]
        and "About" in order[5]
        and "Support" in order[6]
        and "Log in" in order[7],
        " | ".join(order),
    )
    check(
        "desk: a visible ring on the keyboard's focus",
        ring.startswith(("solid", "auto")) and not ring.endswith(" 0px"),
        ring,
    )

    page.locator("#site-navigation").get_by_role("button", name="Support").click()
    page.wait_for_timeout(1200)
    check("desk: Support opens its sheet", page.evaluate("!!document.querySelector('dialog[open]')"))
    page.keyboard.press("Escape")
    page.wait_for_timeout(600)

    page.evaluate("window.scrollTo(0, 1400)")
    page.mouse.wheel(0, 1)
    page.wait_for_timeout(1800)
    page.screenshot(path=str(OUT / "desk-scrolled.png"))
    info = page.evaluate(
        """() => { const h = document.querySelector('header');
        const bar = h.querySelector('nav'); const rule = h.querySelector('[class*="__rule"]');
        return { size: h.dataset.size, bar: Math.round(bar.getBoundingClientRect().height),
          rule: getComputedStyle(rule).opacity } }"""
    )
    check(
        "desk: scrolled, the bar settles small with its painted rule",
        info["size"] == "small" and float(info["rule"]) > 0.5 and 74 <= info["bar"] <= 82,
        info,
    )
    solid_bar(page, "desk")

    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(600)
    page.locator('[data-nav-trigger="products"]').click()
    page.wait_for_timeout(900)
    page.locator('[data-nav-panel="products"] a', has_text="Turmerific").click()
    page.wait_for_url("**/products/turmerific**", timeout=30000)
    check("desk: a product link goes to its page", "/products/turmerific" in page.url, page.url)
    page.close()

    page = browser.new_page(viewport={"width": 1536, "height": 900}, reduced_motion="reduce")
    watch(page)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(1500)
    page.locator('[data-nav-trigger="products"]').click()
    page.wait_for_timeout(50)
    check("reduced motion: the scroll is down at once", r_value(page) == "1", r_value(page))
    page.close()


# ---------------------------------------------------------------- round 7: the menu's rows and finale

# Paper beside the pictures of a menu's rows (one column on a phone): left of the pictures' room
# and in the gap between it and the words, past any painting's overhang.
ROWGAPS = """(sel) => { const t = [...document.querySelectorAll(sel + ' [class*="sheetThumb"]')]
  .map(e => e.getBoundingClientRect()).filter(r => r.width > 0);
  if (!t.length) return []; return [t[0].left - 14, t[0].right + 16]; }"""

# The open menu as a visitor sees it: the visible part of the sheet (from the bar to the window's
# foot), each unfolded row (its link, picture, name and line), the four words, the link under the
# rows (and where its arrow stands against its last word), the crane and Log in / Sign up.
MENU = """() => {
  const box = el => { const r = el.getBoundingClientRect(); return { left: r.left, right: r.right, top: r.top, bottom: r.bottom, w: r.width, h: r.height }; };
  const sheet = document.querySelector('[data-nav-sheet]');
  const bar = document.querySelector('#site-navigation').getBoundingClientRect();
  const fold = sheet.querySelector('[class*="sheetPart"][data-open]');
  const rows = fold ? [...fold.querySelectorAll('[class*="sheetRow"][href]')].map(a => {
    const name = a.querySelector('[class*="sheetRowName"]'), line = a.querySelector('[class*="sheetRowLine"]');
    const thumb = a.querySelector('[class*="sheetThumb"]');
    return { name: name.textContent.trim(), link: box(a), nameBox: box(name), lineBox: box(line), thumb: box(thumb),
      nameSize: parseFloat(getComputedStyle(name).fontSize), lineSize: parseFloat(getComputedStyle(line).fontSize),
      clipped: [name, line].some(e => e.scrollWidth > e.clientWidth + 1) };
  }) : [];
  const more = fold && fold.querySelector('a[class*="more"]');
  let arrow = null;
  if (more) {
    const tail = more.querySelector('[class*="tail"]'); const svg = tail.querySelector('svg');
    const range = document.createRange(); range.selectNodeContents(tail.firstChild);
    const lines = [...range.getClientRects()]; const last = lines[lines.length - 1]; const s = svg.getBoundingClientRect();
    arrow = { sameLine: s.top < last.bottom && s.bottom > last.top, gap: Math.round(s.left - last.right) };
  }
  const crane = sheet.querySelector('[class*="sheetCrane"]');
  const words = [...sheet.querySelectorAll(':scope [class*="sheetInner"] > a, :scope [class*="sheetInner"] > button, [data-nav-sheet-toggle]')]
    .map(e => ({ text: e.textContent.trim(), ...box(e) }));
  const foot = [...sheet.querySelectorAll('[class*="sheetFoot"] a, [class*="sheetFoot"] button')]
    .filter(e => e.getBoundingClientRect().width > 0).map(e => ({ text: e.textContent.trim(), ...box(e) }));
  return { W: innerWidth, H: innerHeight, top: bar.bottom, scrollTop: sheet.scrollTop,
    scrollable: sheet.scrollHeight - sheet.clientHeight,
    hscroll: sheet.scrollWidth > sheet.clientWidth + 1 || document.documentElement.scrollWidth > innerWidth + 1,
    rows, arrow, crane: box(crane), craneOpacity: +getComputedStyle(crane).opacity, words, foot,
    pageY: scrollY, locked: document.body.style.overflow === 'hidden' };
}"""


def inside(b, m, pad=0):
    """A box wholly inside the visible menu: the window's width, from the bar down to its foot."""
    return b["left"] >= -pad and b["right"] <= m["W"] + pad and b["top"] >= m["top"] - pad and b["bottom"] <= m["H"] + pad


def sheet_end(page):
    page.evaluate("(() => { const s = document.querySelector('[data-nav-sheet]'); s.scrollTop = s.scrollHeight; })()")
    page.wait_for_timeout(500)


def sheet_top(page):
    page.evaluate("document.querySelector('[data-nav-sheet]').scrollTop = 0")
    page.wait_for_timeout(300)


def unfold(page, part):
    toggle = page.locator(f'[data-nav-sheet-toggle="{part}"]')
    if toggle.get_attribute("aria-expanded") != "true":
        toggle.click()
    page.wait_for_timeout(1300)
    sheet_top(page)


def rows_checks(tag, m, count, full=True):
    """Every row of an unfolded part whole on the screen: its name and line written out, unclipped,
    inside the window's width (and, `full`, all of them in view at once without scrolling), each
    row a 56px+ target, names 20px+ and lines 16px+; the link under them keeps its arrow with its
    last word; nothing scrolls sideways."""
    rows = m["rows"]
    check(f"{tag}: {count} rows, every name written out", len(rows) == count and all(r["name"] for r in rows),
          [r["name"] for r in rows])
    out = [r["name"] for r in rows if not (r["nameBox"]["left"] >= 0 and r["nameBox"]["right"] <= m["W"]
           and r["lineBox"]["left"] >= 0 and r["lineBox"]["right"] <= m["W"] and r["thumb"]["left"] >= 0
           and r["thumb"]["right"] <= m["W"])]
    check(f"{tag}: every row inside the window's width, nothing cut off at a side", not out, out)
    if full:
        hidden = [r["name"] for r in rows if not (inside(r["nameBox"], m) and inside(r["lineBox"], m) and inside(r["thumb"], m, 2))]
        check(f"{tag}: all {count} in view at once, no scrolling (name, line and picture)", not hidden,
              {"hidden": hidden, "H": m["H"], "last": round(rows[-1]["link"]["bottom"]) if rows else None})
    small = [(r["name"], round(r["link"]["h"]), r["nameSize"], r["lineSize"]) for r in rows
             if r["link"]["h"] < 56 or r["link"]["w"] < 48 or r["nameSize"] < 20 or r["lineSize"] < 16]
    check(f"{tag}: rows 56px+ tall, names 20px+, lines 16px+", not small,
          small or f"{min(round(r['link']['h']) for r in rows)}px rows, {rows[0]['nameSize']}px names" if rows else "none")
    check(f"{tag}: no word clipped", not any(r["clipped"] for r in rows))
    check(f"{tag}: the link's arrow stays with its last word", m["arrow"] and m["arrow"]["sameLine"] and 0 <= m["arrow"]["gap"] <= 16, m["arrow"])
    check(f"{tag}: nothing scrolls sideways", not m["hscroll"])


def finale_checks(tag, m, at_once):
    """The crane at the foot, whole on the screen, with Log in and Sign up under it."""
    c = m["crane"]
    foot = {f["text"]: f for f in m["foot"]}
    ok = inside(c, m) and c["h"] >= 120 and m["craneOpacity"] > 0.99 and foot and all(inside(f, m) for f in foot.values()) \
        and all(f["top"] >= c["bottom"] - 4 for f in foot.values())
    check(f"{tag}: the crane stands whole at the foot, Log in and Sign up under it" + (" (no scrolling)" if at_once else " (scrolled to the end)"),
          ok and (not at_once or m["scrollTop"] == 0),
          {"crane": [round(c["top"]), round(c["bottom"]), round(c["h"])], "H": m["H"], "foot": [round(f["top"]) for f in foot.values()],
           "scrollTop": m["scrollTop"], "opacity": round(m["craneOpacity"], 3)})


# The crane on every frame the page draws while a part folds open or shut: where its top is, its
# height, and whether it is drawn (never hidden, never faded).
CRANE_LOG = """() => { const c = document.querySelector('[data-nav-sheet] [class*="sheetCrane"]');
  window.__crane = []; window.__craneOn = true;
  const tick = () => { const r = c.getBoundingClientRect(); const s = getComputedStyle(c);
    window.__crane.push({ t: performance.now(), top: r.top, h: r.height, o: +s.opacity, d: s.display, v: s.visibility });
    if (window.__craneOn) requestAnimationFrame(tick); };
  requestAnimationFrame(tick); }"""


def crane_motion(page, tag, act, ms=1200):
    """Filmed frame by frame: the crane never disappears or jumps while a part folds (it eases with
    the fold: no frame moves it more than 64px, or changes its size by more than 12px)."""
    page.evaluate(CRANE_LOG)
    page.wait_for_timeout(100)
    act()
    page.wait_for_timeout(ms)
    page.evaluate("window.__craneOn = false")
    log = page.evaluate("window.__crane")
    gone = [round(e["t"] - log[0]["t"]) for e in log if e["h"] < 100 or e["o"] < 0.99 or e["d"] == "none" or e["v"] == "hidden"]
    jumps = [round(abs(b["top"] - a["top"])) for a, b in zip(log, log[1:])]
    sizes = [round(abs(b["h"] - a["h"]), 1) for a, b in zip(log, log[1:])]
    moved = round(log[-1]["top"] - log[0]["top"])
    check(
        f"{tag}: the crane eases with the fold, never pops (every frame drawn whole, no jump)",
        len(log) >= 30 and not gone and max(jumps) <= 64 and max(sizes) <= 12,
        f"{len(log)} frames, moved {moved}px, largest step {max(jumps)}px, size step {max(sizes)}px, hidden at {gone[:4]}",
    )
    return log


def phone_rows(browser):
    """Round 7: the phone menu's rows and finale at three phones (and a short one), in English,
    Vietnamese and Japanese."""
    for loc, w, h, full in (
        ("en", 390, 844, True), ("en", 360, 780, True), ("en", 430, 932, True), ("en", 360, 640, False),
        ("vn", 390, 844, False), ("jp", 390, 844, False), ("vn", 360, 780, False),
    ):
        tag = f"phone {loc} {w}x{h}"
        page = browser.new_page(viewport={"width": w, "height": h}, is_mobile=True, has_touch=True, device_scale_factor=2)
        watch(page)
        page.goto(BASE + ("/" if loc == "en" else f"/{loc}"), wait_until="networkidle")
        page.wait_for_timeout(1500)
        page.locator("[data-nav-menu-button]").click()
        # The crane settles last (from 0.64s, for 0.9s): measured once it has.
        page.wait_for_timeout(1900)
        m = page.evaluate(MENU)
        if h >= 780:
            finale_checks(f"{tag} menu", m, at_once=True)
        unfold(page, "products")
        page.screenshot(path=str(OUT / f"phone-{loc}-{w}-products.png"))
        m = page.evaluate(MENU)
        rows_checks(f"{tag} Products", m, 5, full)
        unfold(page, "science")
        page.screenshot(path=str(OUT / f"phone-{loc}-{w}-science.png"))
        m = page.evaluate(MENU)
        rows_checks(f"{tag} Science", m, 4, full)
        y = m["pageY"]
        sheet_end(page)
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(500)
        m = page.evaluate(MENU)
        page.screenshot(path=str(OUT / f"phone-{loc}-{w}-foot.png"))
        finale_checks(f"{tag} Science unfolded", m, at_once=False)
        check(f"{tag}: the menu scrolls on its own, the page under it stays put", m["locked"] and m["pageY"] == y and m["scrollTop"] > 0,
              {"locked": m["locked"], "pageY": [y, m["pageY"]], "scrollTop": m["scrollTop"]})
        page.close()

    # The crane, filmed: Products folding open and shut at 390x844.
    page = browser.new_page(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2)
    watch(page)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(1500)
    page.locator("[data-nav-menu-button]").click()
    page.wait_for_timeout(1500)
    toggle = page.locator('[data-nav-sheet-toggle="products"]')
    box = toggle.bounding_box()
    tap = lambda: page.touchscreen.tap(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)  # noqa: E731
    log = crane_motion(page, "phone 390x844, Products unfolds", tap)
    check("phone 390x844: the crane is carried down, never up, as Products unfolds",
          all(b["top"] >= a["top"] - 0.5 for a, b in zip(log, log[1:])) and log[-1]["top"] > log[0]["top"] + 200,
          f"{round(log[0]['top'])} -> {round(log[-1]['top'])}")
    crane_motion(page, "phone 390x844, Products folds away", tap)
    page.close()


def tablet_rows(browser):
    """Round 7: the tablet menu. Held upright it opens with Products unfolded, the five in a row,
    the four words and the crane at the foot all on the screen (no hollow over 120px between
    Support and the crane); the names' lines start on one line; Science shows its four the same
    way. Held sideways (1024x768) it opens with the four words and the crane."""
    for w, h in ((834, 1112), (768, 1024), (1024, 768)):
        tag = f"tablet {w}x{h}"
        page = browser.new_page(viewport={"width": w, "height": h})
        watch(page)
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(1500)
        page.locator("[data-nav-menu-button]").click()
        page.wait_for_timeout(1500)
        m = page.evaluate(MENU)
        page.screenshot(path=str(OUT / f"tablet-{w}x{h}-menu.png"))
        upright = h >= 900
        check(f"{tag}: the menu opens " + ("with Products unfolded" if upright else "with the four words"),
              (len(m["rows"]) == 5) == upright, len(m["rows"]))
        finale_checks(f"{tag} menu", m, at_once=True)
        support = next(wd for wd in m["words"] if wd["text"] in ("Support",))
        ink_top = m["crane"]["top"] + m["crane"]["h"] * 0.08
        check(f"{tag}: no hollow over 120px between Support and the crane", ink_top - support["bottom"] <= 120 or not upright,
              f"{round(ink_top - support['bottom'])}px")
        if upright:
            rows_checks(f"{tag} Products", m, 5)
            lines = [round(r["lineBox"]["top"]) for r in m["rows"]]
            check(f"{tag}: the five focus lines start on one line", max(lines) - min(lines) <= 1, lines)
        unfold(page, "science")
        m = page.evaluate(MENU)
        page.screenshot(path=str(OUT / f"tablet-{w}x{h}-science.png"))
        rows_checks(f"{tag} Science", m, 4, full=upright)
        lines = [round(r["lineBox"]["top"]) for r in m["rows"]]
        check(f"{tag}: the four captions start on one line", max(lines) - min(lines) <= 1, lines)
        sheet_end(page)
        finale_checks(f"{tag} Science unfolded", page.evaluate(MENU), at_once=False)
        page.close()

    # Upright, moving from Products to Science: the crane eases with the fold, never pops.
    page = browser.new_page(viewport={"width": 834, "height": 1112})
    watch(page)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(1500)
    page.locator("[data-nav-menu-button]").click()
    page.wait_for_timeout(1500)
    crane_motion(page, "tablet 834x1112, Science unfolds as Products folds", lambda: page.locator('[data-nav-sheet-toggle="science"]').click())
    crane_motion(page, "tablet 834x1112, Science folds away", lambda: page.locator('[data-nav-sheet-toggle="science"]').click())
    page.close()


def menu_light_boxes(browser):
    """Round 7, filmed at real speed on a phone: Science unfolding (Dr. Liu's print and the three
    paintings settle onto the paper) and the menu opening with its crane: no painting's paper, and
    not the crane's, ever shows as a light box."""
    page = browser.new_page(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2)
    watch(page)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(2000)
    btn = page.locator("[data-nav-menu-button]")
    btn.click()
    page.wait_for_timeout(600)
    toggle = page.locator('[data-nav-sheet-toggle="science"]')
    toggle.click()
    page.wait_for_function(
        "[...document.querySelectorAll('[data-nav-sheet] img')].every(i => i.complete && i.naturalWidth > 0)", timeout=30000
    )
    page.wait_for_timeout(900)
    toggle.click()
    page.wait_for_timeout(1000)
    box = toggle.bounding_box()
    film = Film(page).shoot(lambda: page.touchscreen.tap(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2), 1300)
    pics = [p for p in page.evaluate(PICTURES, "#nav-sheet-science") if p["y"] + p["h"] < 844]
    found = light_boxes(
        film, pics, page.evaluate(ROWGAPS, "#nav-sheet-science"),
        lambda e: next(f["bottom"] for f in e["folds"] if f["id"] == "nav-sheet-science"), 390, 0, 1200,
    )
    no_light_box("phone: Science unfolds with no light box round its paintings (filmed at real speed)", found, frames=4)
    btn.click()
    page.wait_for_timeout(1200)
    film = Film(page).shoot(lambda: btn.tap(), 1500)
    deckle = page.evaluate("parseFloat(getComputedStyle(document.querySelector('header')).getPropertyValue('--deckle'))")
    top, height = page.evaluate(
        "(() => { const r = document.querySelector('[data-nav-sheet]').getBoundingClientRect(); return [r.top, r.height]; })()"
    )
    crane = page.evaluate(PICTURES, '[data-nav-sheet] [class*="sheetFinale"]')
    found = light_boxes(film, crane, [16, 374], lambda e: top + e["s"] * height - deckle, 390, 300, 1400)
    no_light_box("phone: the menu opens with the crane multiplied on its paper, no light box (filmed at real speed)", found, frames=4)
    page.close()


def phone(browser):
    page = browser.new_page(
        viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2
    )
    watch(page)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(2000)
    page.screenshot(path=str(OUT / "phone-top.png"))
    solid_bar(page, "phone")
    scroll_to(page, 0)
    btn = page.locator("[data-nav-menu-button]")
    btn.click()
    page.wait_for_timeout(1200)
    page.screenshot(path=str(OUT / "phone-menu.png"))
    check("phone: the menu opens", menu_open(page))
    check("phone: the page is locked", page.evaluate("document.body.style.overflow") == "hidden")
    check("phone: its button says Close", "Close" in btn.inner_text(), btn.inner_text())
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    check("phone: Escape closes it", not menu_open(page))
    check(
        "phone: focus back on its button",
        page.evaluate("document.activeElement?.hasAttribute('data-nav-menu-button')"),
    )
    check("phone: the page is unlocked", page.evaluate("document.body.style.overflow") != "hidden")
    btn.click()
    page.wait_for_timeout(900)
    btn.click()
    page.wait_for_timeout(500)
    check("phone: the Close button closes it", not menu_open(page))
    btn.click()
    page.wait_for_timeout(900)
    page.locator('[data-nav-sheet-toggle="products"]').click()
    page.wait_for_timeout(900)
    page.screenshot(path=str(OUT / "phone-menu-products.png"))
    check(
        "phone: Products folds open",
        page.locator("[data-nav-sheet] a", has_text="NuriCell").is_visible(),
    )
    page.locator('[data-nav-sheet-toggle="science"]').click()
    page.wait_for_timeout(800)
    check(
        "phone: Science folds open, Products folds away",
        page.locator("[data-nav-sheet] a", has_text="Research library").is_visible()
        and page.locator('[data-nav-sheet-toggle="products"]').get_attribute("aria-expanded")
        == "false",
    )
    page.locator("[data-nav-sheet] button", has_text="Support").click()
    page.wait_for_timeout(1200)
    check("phone: Support opens its sheet", page.evaluate("!!document.querySelector('dialog[open]')"))
    page.keyboard.press("Escape")
    page.wait_for_timeout(700)
    btn.click()
    page.wait_for_timeout(900)
    page.locator('[data-nav-sheet-toggle="products"]').click()
    page.wait_for_timeout(800)
    page.locator("[data-nav-sheet] a", has_text="NuriCell").click()
    page.wait_for_url("**/products/nuricell**", timeout=30000)
    check("phone: a product link goes to its page", "/products/nuricell" in page.url, page.url)
    page.close()

    # Round 2: Products unfolds, filmed at real speed.
    page = browser.new_page(
        viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2
    )
    watch(page)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(2500)
    page.locator("[data-nav-menu-button]").click()
    page.wait_for_timeout(1500)
    toggle = page.locator('[data-nav-sheet-toggle="products"]')
    toggle.click()
    page.wait_for_function(
        "[...document.querySelectorAll('#nav-sheet-products img')].every(i => i.complete && i.naturalWidth > 0)",
        timeout=30000,
    )
    page.wait_for_timeout(900)
    toggle.click()
    page.wait_for_timeout(1000)
    box = toggle.bounding_box()
    film = Film(page).shoot(lambda: page.touchscreen.tap(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2), 1100)
    # Five rows in one column (round 7): every pool on the screen is measured, against the paper
    # beside the pictures' column.
    found = light_boxes(
        film,
        [p for p in page.evaluate(PICTURES, "#nav-sheet-products") if p["y"] + p["h"] < 844],
        page.evaluate(ROWGAPS, "#nav-sheet-products"),
        lambda e: next(f["bottom"] for f in e["folds"] if f["id"] == "nav-sheet-products"),
        390,
        0,
        1000,
    )
    no_light_box("phone: Products unfolds with no light box around the pools (filmed at real speed)", found, frames=4)
    turned = [round(e["t"] - film.t0) for e in film.log if any(sideways(r) for r in e["chev"])]
    check(
        "phone: its chevron never turns sideways, every frame",
        len(film.log) >= 30 and not turned,
        f"{len(film.log)} frames; sideways at {turned[:5]} ms",
    )
    page.close()


def tablet(browser):
    page = browser.new_page(viewport={"width": 834, "height": 1112})
    watch(page)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(2000)
    page.locator("[data-nav-menu-button]").click()
    page.wait_for_timeout(1200)
    page.screenshot(path=str(OUT / "tablet-menu.png"))
    check(
        "tablet: the menu opens with Products unfolded",
        page.locator('[data-nav-sheet-toggle="products"]').get_attribute("aria-expanded") == "true"
        and page.locator("[data-nav-sheet] a", has_text="Nature Calm").is_visible(),
    )
    page.close()

    page = browser.new_page(viewport={"width": 768, "height": 1024})
    watch(page)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(2000)
    solid_bar(page, "tablet 768")
    page.close()

    # Round 2: the menu opens with Products unfolded; its pools stay multiplied while it settles.
    page = browser.new_page(viewport={"width": 834, "height": 1112})
    watch(page)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(2500)
    btn = page.locator("[data-nav-menu-button]")
    btn.click()
    page.wait_for_function(
        "[...document.querySelectorAll('[data-nav-sheet] img')].every(i => i.complete && i.naturalWidth > 0)",
        timeout=30000,
    )
    page.wait_for_timeout(800)
    btn.click()
    page.wait_for_timeout(1200)
    box = btn.bounding_box()
    film = Film(page).shoot(lambda: page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2), 1600)
    deckle = page.evaluate("parseFloat(getComputedStyle(document.querySelector('header')).getPropertyValue('--deckle'))")
    top, height = page.evaluate(
        "(() => { const r = document.querySelector('[data-nav-sheet]').getBoundingClientRect(); return [r.top, r.height]; })()"
    )
    found = light_boxes(
        film,
        page.evaluate(PICTURES, "#nav-sheet-products"),
        page.evaluate(GAPS, "#nav-sheet-products li"),
        lambda e: top + e["s"] * height - deckle,
        834,
        200,
        1500,
    )
    no_light_box("tablet: the menu opens with no light box around the bottles' pools (filmed at real speed)", found)
    page.close()


# Round 8: the bar's three groups (the language | the inscription: two links, the mark, two links |
# the account) in every language. Every bar item's box, each word's font size and the lines it is
# set on.
GROUPS = """() => {
  const nav = document.querySelector('#site-navigation');
  const R = el => { const r = el.getBoundingClientRect(); return { l: r.left, r: r.right, w: r.width }; };
  const lang = nav.firstElementChild.firstElementChild.querySelector('label');
  const right = nav.lastElementChild; const [about, support] = [...right.firstElementChild.children];
  const acct = right.lastElementChild;
  const items = { lang, prod: nav.querySelector('[data-nav-trigger="products"]'),
    sci: nav.querySelector('[data-nav-trigger="science"]'), mark: nav.querySelector('[data-nav-logo]'),
    about, support, login: acct.querySelector('a'), signup: acct.querySelector('button') };
  const text = { lang: lang.querySelector('select'), prod: items.prod.firstElementChild,
    sci: items.sci.firstElementChild, about: about.firstElementChild, support: support.firstElementChild,
    login: items.login, signup: items.signup };
  const lines = el => { if (el.tagName === 'SELECT') return el.getBoundingClientRect().height < 60 ? 1 : 2;
    const walk = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); const tops = new Set(); let n;
    while ((n = walk.nextNode())) { if (!n.textContent.trim()) continue; const rg = document.createRange();
      rg.selectNodeContents(n);
      [...rg.getClientRects()].filter(r => r.width > 1).forEach(r => tops.add(Math.round(r.top / 6))); }
    return tops.size; };
  const map = f => Object.fromEntries(Object.entries(text).map(([k, e]) => [k, f(e)]));
  return { cw: document.documentElement.clientWidth,
    box: Object.fromEntries(Object.entries(items).map(([k, e]) => [k, R(e)])),
    lines: map(lines), size: map(e => parseFloat(getComputedStyle(e).fontSize)),
    pill: parseFloat(getComputedStyle(items.signup).borderTopWidth) > 0 };
}"""

ORDER = ["lang", "prod", "sci", "mark", "about", "support", "login", "signup"]


def groups(g):
    """The bar's spacing from GROUPS: the gaps between neighbours, the two group gaps against the
    spacing between the links, the inscription's symmetry about the mark, and what is wrong."""
    b, cw = g["box"], g["cw"]
    gap = {f"{a}>{c}": b[c]["l"] - b[a]["r"] for a, c in zip(ORDER, ORDER[1:])}
    link = max(gap["prod>sci"], gap["about>support"])
    mid = (b["mark"]["l"] + b["mark"]["r"]) / 2
    reach = (mid - b["prod"]["l"], b["support"]["r"] - mid)
    return {
        "ratio": min(gap["support>login"], gap["lang>prod"]) / link,
        "account": round(gap["support>login"]),
        "language": round(gap["lang>prod"]),
        "link": round(link, 1),
        # One spacing for the inscription and the mark at the window's centre: its two sides differ
        # only by their own words' lengths.
        "symmetric": abs(mid - cw / 2) <= 1
        and abs(gap["sci>mark"] - gap["mark>about"]) <= 1
        and abs(gap["prod>sci"] - gap["about>support"]) <= 1
        and abs(gap["sci>mark"] - gap["prod>sci"]) <= 1,
        "reach": round(max(reach) / min(reach), 2),
        "tightest": round(min(gap.values())),
        "inside": b["lang"]["l"] >= 16 and b["signup"]["r"] <= cw - 16,
        "edges": (round(b["lang"]["l"]), round(cw - b["signup"]["r"])),
        "wrapped": [k for k, v in g["lines"].items() if v != 1],
        "small": [k for k, v in g["size"].items() if v < 18],
    }


LANG_WIDTHS = (1101, 1160, 1220, 1280, 1366, 1440, 1536, 1920)


def languages(browser, playwright):
    """Round 8: in every language, at 1101-1920px, over the opening (tall) and scrolled (small), the
    bar reads as three groups: the gap before the account group (and, mirrored, after the language)
    at least 1.5 times the spacing between the links; the inscription symmetric about the centred
    mark (one spacing; its two sides differ only by their words, never more than 1.35 times);
    nothing overlapping (12px+ between neighbours) or within 16px of the window's edge; no word
    wrapping; no word under 18px. Then every 20px from 1101 to 1920 in both states, and with the
    window's own scrollbar showing (as on Windows), the same group gaps and fit."""
    for locale in ("en", "cns", "kr", "vn", "jp"):
        url = f"{BASE}/" if locale == "en" else f"{BASE}/{locale}"
        found = {}
        for width in LANG_WIDTHS:
            page = browser.new_page(viewport={"width": width, "height": 800})
            watch(page)
            page.goto(url, wait_until="networkidle")
            page.wait_for_timeout(1500)
            page.mouse.move(width / 2, 796)
            for state in ("tall", "small"):
                if state == "small":
                    page.evaluate("window.scrollTo(0, 700)")
                    page.mouse.wheel(0, 1)
                    page.wait_for_timeout(1300)
                found[(width, state)] = groups(page.evaluate(GROUPS))
                page.screenshot(
                    path=str(OUT / f"lang-{locale}-{width}-{state}.png"),
                    clip={"x": 0, "y": 0, "width": width, "height": 130 if state == "tall" else 110},
                )
            page.close()

        def worst(key, low=True):
            pick = (min if low else max)(found.items(), key=lambda kv: kv[1][key])
            return f"{pick[0][0]} {pick[0][1]}: {round(pick[1][key], 2)}"

        every = list(found.values())
        check(
            f"{locale}: the gap before the account group and after the language at least 1.5x the "
            "spacing between the links (1101-1920, tall and small)",
            all(f["ratio"] >= 1.5 for f in every),
            "lowest ratio "
            + worst("ratio")
            + "; tall account/language/link: "
            + ", ".join(
                f"{w} {f['account']}/{f['language']}/{f['link']}" for (w, s), f in found.items() if s == "tall"
            ),
        )
        check(
            f"{locale}: the inscription is symmetric about the centred mark, its sides within 1.35x",
            all(f["symmetric"] and f["reach"] <= 1.35 for f in every),
            "widest reach "
            + worst("reach", low=False)
            + "; not symmetric: "
            + str([k for k, f in found.items() if not f["symmetric"]]),
        )
        check(
            f"{locale}: nothing overlaps (12px+ between neighbours) or comes within 16px of the edge",
            all(f["tightest"] >= 12 and f["inside"] for f in every),
            "tightest gap "
            + worst("tightest")
            + "; outside: "
            + str([(k, f["edges"]) for k, f in found.items() if not f["inside"]]),
        )
        check(
            f"{locale}: no word in the bar wraps, none under 18px",
            all(not f["wrapped"] and not f["small"] for f in every),
            [(k, f["wrapped"], f["small"]) for k, f in found.items() if f["wrapped"] or f["small"]],
        )

        # Every 20px, both states; then with the window's scrollbar showing (tall).
        def sweep(page, label, states):
            bad, low = [], (9.0, None)
            for state in states:
                if state == "small":
                    page.evaluate("window.scrollTo(0, 700)")
                    page.mouse.wheel(0, 1)
                    page.wait_for_timeout(1300)
                for width in range(1101, 1921, 20):
                    page.set_viewport_size({"width": width, "height": 800})
                    page.wait_for_timeout(90)
                    f = groups(page.evaluate(GROUPS))
                    low = min(low, (round(f["ratio"], 2), f"{width} {state}"))
                    if (
                        f["ratio"] < 1.5
                        or f["tightest"] < 12
                        or not f["inside"]
                        or f["wrapped"]
                        or not f["symmetric"]
                    ):
                        bad.append((width, state, round(f["ratio"], 2), f["tightest"], f["edges"], f["wrapped"]))
            check(
                f"{locale}: every 20px from 1101 to 1920 ({label}): three groups, symmetric, inside, unwrapped",
                not bad,
                f"lowest ratio {low}; {bad[:4]}",
            )

        page = browser.new_page(viewport={"width": 1101, "height": 800})
        watch(page)
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(1500)
        page.mouse.move(500, 796)
        sweep(page, "tall and small", ("tall", "small"))
        page.close()
        bars = playwright.chromium.launch(args=["--use-angle=d3d11"], ignore_default_args=["--hide-scrollbars"])
        page = bars.new_page(viewport={"width": 1101, "height": 800})
        watch(page)
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(1500)
        page.mouse.move(500, 796)
        sweep(page, "the window's scrollbar showing", ("tall",))
        bars.close()

    STROKE_BOX = """w => { const link = [...document.querySelectorAll('#site-navigation [data-nav-ink]')]
      .map(i => i.closest('a, button')).find(l => l.innerText.trim() === w);
      return Math.round(link.querySelector('[data-nav-ink]').getBoundingClientRect().width); }"""

    # The painted stroke under a short word (round 8): two Chinese, Japanese or Korean characters
    # (产品, 제품, 製品, 소개) carry a stroke about three characters long, centred under the word,
    # a little past both its ends, its ink never past the chevron's middle: a stroke, not a dab.
    for locale, word, about in (("cns", "产品", "关于我们"), ("kr", "제품", "소개"), ("jp", "製品", "私たちについて")):
        page = browser.new_page(viewport={"width": 1536, "height": 900})
        watch(page)
        page.goto(f"{BASE}/{locale}", wait_until="networkidle")
        page.wait_for_timeout(1500)
        page.mouse.move(768, 896)
        put(page, "products")
        px = stroke_pixels(page, word)
        size = page.evaluate(
            "parseFloat(getComputedStyle(document.querySelector('#site-navigation')).fontSize)"
        )
        page.screenshot(
            path=str(OUT / f"stroke-{locale}-products.png"),
            clip={"x": round(px["left"]) - 40, "y": 0, "width": round(px["right"] - px["left"]) + 110, "height": 110},
        )
        box = page.evaluate(STROKE_BOX, word)
        check(
            f"stroke ({locale}): under {word} about three characters long (2.6em+), its dark ink (2.2em+) "
            "centred under the word (3px), starting before it, ending before the chevron's middle",
            px["ink"]
            and box >= 2.6 * size
            and px["to"] - px["from"] >= 2.2 * size
            and abs((px["from"] + px["to"]) / 2 - (px["left"] + px["right"]) / 2) <= 3
            and px["from"] < px["left"]
            and px["to"] <= px["chevron"] + 7,
            {k: (round(v, 1) if isinstance(v, float) else v) for k, v in px.items()} | {"em": size, "box": box},
        )
        if locale == "kr":
            put(page, "top", 0, 900)
            page.evaluate("document.querySelector('#site-navigation a[href$=\"/about\"]').dataset.ink = 'here'")
            page.wait_for_timeout(1700)
            px = stroke_pixels(page, about)
            box = page.evaluate(STROKE_BOX, about)
            check(
                f"stroke ({locale}): under {about} (as the current page) about three characters long, "
                "its dark ink centred under the word (3px)",
                px["ink"]
                and box >= 2.6 * size
                and px["to"] - px["from"] >= 2.2 * size
                and abs((px["from"] + px["to"]) / 2 - (px["left"] + px["right"]) / 2) <= 3,
                {k: (round(v, 1) if isinstance(v, float) else v) for k, v in px.items()} | {"box": box},
            )
        page.close()

# Round 6: the painted stroke under a word. Each ink of the bar's three words (Products, Science,
# About): which state its link gives it, and how much ink it shows.
INKS = """() => [...document.querySelectorAll('#site-navigation [data-nav-ink]')].map(i => {
  const link = i.closest('a, button'); const s = getComputedStyle(i); const r = i.getBoundingClientRect();
  return { word: link.innerText.trim(), state: link.dataset.ink || '', opacity: +s.opacity,
    draw: parseFloat(s.getPropertyValue('--insc-ink')), shown: r.width > 0 && r.height > 0 }; })"""

# Where a part of the homepage is put under the reading band (40-42% down the window): a third of
# the way into it, or for a part that marks nothing, its middle.
PUT = """([id, share]) => { const r = document.getElementById(id).getBoundingClientRect();
  return r.top + scrollY + r.height * share - innerHeight * 0.41; }"""


def put(page, part, share=1 / 3, wait=1500):
    y = page.evaluate(PUT, [part, share])
    page.evaluate(f"window.scrollTo(0, {y})")
    page.mouse.wheel(0, 1)
    page.wait_for_timeout(wait)
    return page.evaluate(INKS)


def inked(inks):
    return [i["word"] for i in inks if i["opacity"] > 0.02]


def stroke_pixels(page, word):
    """The stroke under `word` in the pixels: where its ink runs (columns at least 40 levels darker
    than the paper), its thickness, and the word's, the fine line's and the chevron's places."""
    box = page.evaluate(
        """w => { const link = [...document.querySelectorAll('#site-navigation [data-nav-ink]')]
        .map(i => i.closest('a, button')).find(l => l.innerText.trim() === w);
      const word = link.querySelector('[data-nav-ink]').parentElement;
      const r = word.getBoundingClientRect(); const after = getComputedStyle(word, '::after');
      const chev = link.querySelector('svg'); const c = chev && chev.getBoundingClientRect();
      return { left: r.left, right: r.right, bottom: r.bottom, chevron: c ? c.left : null,
        line: r.bottom - parseFloat(after.bottom) - parseFloat(after.height) / 2 }; }""",
        word,
    )
    top = round(box["bottom"]) + 1
    clip = {"x": round(box["left"]) - 12, "y": top, "width": round(box["right"] - box["left"]) + 40, "height": 13}
    a = np.asarray(Image.open(BytesIO(page.screenshot(clip=clip))).convert("L"), dtype=np.float32)
    paper = float(np.median(a[:, -6:]))
    dark = (paper - a) > 40
    cols = np.where(dark.any(axis=0))[0]
    rows = np.where(dark.any(axis=1))[0]
    if not len(cols):
        return {"ink": False, **box}
    body = dark[:, cols.min() : cols.min() + max(4, (cols.max() - cols.min()) // 2)]
    return {
        "ink": True,
        "from": clip["x"] + int(cols.min()),
        "to": clip["x"] + int(cols.max()),
        "thick": float(np.median(body.sum(axis=0))),
        "mid": top + (rows.min() + rows.max() + 1) / 2,
        **box,
    }


def reading_stroke(browser):
    """Round 6: the painted stroke. The homepage marks no page; its stroke follows the reader."""
    page = browser.new_page(viewport={"width": 1536, "height": 900})
    watch(page)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(2000)
    page.mouse.move(768, 896)

    marks = page.evaluate(
        """() => ({ aria: [...document.querySelectorAll('header [aria-current]')].map(e => e.innerText.trim()),
        current: [...document.querySelectorAll('header [data-current]')].map(e => e.innerText.trim()),
        here: [...document.querySelectorAll('header [data-ink="here"]')].map(e => e.innerText.trim()) })"""
    )
    check(
        "stroke: the homepage marks no page (no aria-current, no data-current, no stroke 'here')",
        not marks["aria"] and not marks["current"] and not marks["here"],
        marks,
    )
    inks = page.evaluate(INKS)
    check(
        "stroke: one ink under each of Products, Science and About; none shown over the opening",
        [i["word"] for i in inks] == ["Products", "Science", "About"] and not inked(inks),
        inks,
    )

    expect = [
        ("cellular", 1 / 3, "Science"),
        ("scientists", 0.5, None),
        ("products", 1 / 3, "Products"),
        ("stories", 0.5, None),
        ("science", 1 / 3, "Science"),
        ("research", 1 / 3, "Science"),
        ("purpose", 0.5, None),
    ]
    for part, share, word in expect:
        inks = put(page, part, share)
        states = [i["word"] for i in inks if i["state"]]
        whole = [i for i in inks if i["word"] == word and i["opacity"] >= 0.5 and i["draw"] == 1]
        if word:
            ok = states == [word] and inked(inks) == [word] and whole
        else:
            ok = not states and not inked(inks)
        check(
            f"stroke: reading #{part}, {'under ' + word if word else 'no stroke'}",
            ok,
            [(i["word"], i["state"], round(i["opacity"], 2), round(i["draw"], 2)) for i in inks],
        )
        if part != "products":
            continue
        page.screenshot(path=str(OUT / "stroke-products.png"), clip={"x": 300, "y": 0, "width": 940, "height": 110})
        px = stroke_pixels(page, "Products")
        span = px["right"] - px["left"]
        check(
            "stroke: in the pixels, under the word from its first letter over 75%+ of it, 3-8px thick, "
            "where the fine line runs (3px), clear of the chevron",
            px["ink"]
            and abs(px["from"] - px["left"]) <= 3
            and px["to"] - px["from"] >= 0.75 * span
            and 3 <= px["thick"] <= 8
            and abs(px["mid"] - px["line"]) <= 3
            and (px["chevron"] is None or px["to"] <= px["chevron"] - 2),
            {k: (round(v, 1) if isinstance(v, float) else v) for k, v in px.items()},
        )
        # Pointing at About lifts it; it comes back once the pointer leaves the bar. (The pointer is
        # moved by hand: a locator's hover scrolls the page to the sticky bar's place in the flow.)
        def point(selector):
            r = page.evaluate(f"(() => {{ const r = document.querySelector('{selector}').getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; }})()")
            page.mouse.move(r[0], r[1], steps=4)

        point('#site-navigation a[href$="/about"]')
        page.wait_for_timeout(700)
        pointed = page.evaluate(INKS)
        page.mouse.move(768, 896)
        page.wait_for_timeout(1300)
        back = page.evaluate(INKS)
        check(
            "stroke: pointing at About lifts it, and it is laid again after",
            not inked(pointed) and inked(back) == ["Products"] and back[0]["draw"] == 1,
            f"pointing: {inked(pointed)}; after: {[(i['word'], round(i['opacity'], 2)) for i in back if i['opacity'] > 0.02]}",
        )
        # An open drop-down takes over; once it has rolled back up the stroke comes back.
        point('[data-nav-trigger="science"]')
        page.wait_for_timeout(700)
        opened = page.evaluate(INKS)
        was_open = is_open(page, "science")
        y0 = page.evaluate("scrollY")
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        y1 = page.evaluate("scrollY")
        check(
            "desk: Escape hands focus back to the button without moving the page (scrolled)",
            abs(y1 - y0) <= 1 and page.evaluate("document.activeElement?.dataset.navTrigger") == "science",
            f"scrollY {y0} -> {y1}",
        )
        page.mouse.move(768, 896)
        page.wait_for_timeout(1300)
        closed = page.evaluate(INKS)
        check(
            "stroke: an open drop-down lifts it, and it is laid again once the scroll is up",
            was_open and not inked(opened) and inked(closed) == ["Products"],
            f"open: {was_open} {inked(opened)}; closed: {inked(closed)}",
        )

    # Every frame the page draws while the page is read down at a few hundred px a second: never
    # more than one stroke with ink.
    put(page, "top", 0, 800)
    page.evaluate(
        """() => { window.__inks = { max: 0, frames: 0, seen: new Set() }; const loop = () => {
      const on = [...document.querySelectorAll('#site-navigation [data-nav-ink]')]
        .filter(i => +getComputedStyle(i).opacity > 0.02);
      window.__inks.max = Math.max(window.__inks.max, on.length); window.__inks.frames++;
      on.forEach(i => window.__inks.seen.add(i.closest('a, button').innerText.trim()));
      if (!window.__inks.stop) requestAnimationFrame(loop); }; requestAnimationFrame(loop); }"""
    )
    end = page.evaluate("document.getElementById('purpose').getBoundingClientRect().top + scrollY")
    while page.evaluate("scrollY") < end:
        page.mouse.wheel(0, 120)
        page.wait_for_timeout(150)
    page.wait_for_timeout(800)
    film = page.evaluate(
        "(() => { window.__inks.stop = true; return { max: window.__inks.max, frames: window.__inks.frames, seen: [...window.__inks.seen] }; })()"
    )
    check(
        "stroke: exactly one painted stroke at a time, every frame, reading the whole page down",
        film["max"] == 1 and film["frames"] > 100 and sorted(film["seen"]) == ["Products", "Science"],
        film,
    )
    page.close()

    page = browser.new_page(viewport={"width": 1536, "height": 900}, reduced_motion="reduce")
    watch(page)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(1500)
    page.mouse.move(768, 896)
    inks = put(page, "products", wait=250)
    check(
        "reduced motion: the stroke is simply there",
        inked(inks) == ["Products"] and inks[0]["draw"] == 1 and inks[0]["opacity"] >= 0.5,
        inks,
    )
    page.close()

    page = browser.new_page(
        viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2
    )
    watch(page)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(1500)
    inks = put(page, "products")
    check("phone: the bar shows no stroke", not any(i["shown"] for i in inks), inks)
    page.close()


# ---------------------------------------------------------------- round 9: the title settles with the scroll

# The bar's state: the settle's values on the header, the mark's and two links' boxes as drawn (with
# their transforms), the paper's opacity and the rule's draw.
SETTLE = """() => { const h = document.querySelector('header'); const s = getComputedStyle(h);
  const box = el => { const r = el.getBoundingClientRect(); return [r.left, r.top, r.width]; };
  const ground = h.querySelector('[class*="__ground"]'); const rule = h.querySelector('[class*="__rule"]');
  return { y: scrollY, size: h.dataset.size, g: +s.getPropertyValue('--insc-g') || 0,
    mark: box(h.querySelector('[data-nav-logo]')), products: box(h.querySelector('[data-nav-trigger="products"]') || h.querySelector('[data-nav-menu-button]')),
    about: box(h.querySelector('#site-navigation a[href$="/about"]') || h.querySelector('[class*="account"] label') || h.querySelector('[data-nav-logo]')),
    paper: +getComputedStyle(ground).opacity, draw: parseFloat(getComputedStyle(rule).getPropertyValue('--insc-draw')),
    ruleOpacity: +getComputedStyle(rule).opacity }; }"""

# The bar's words, each as the box round its letters, and their ink.
BAR_WORDS = r"""() => {
  const nav = document.querySelector('#site-navigation');
  const els = [...nav.querySelectorAll('[class*="__word"], [data-nav-menu-button] span, [class*="account"] a, [class*="account"] button, [class*="language"] select, [class*="account"] select')];
  const out = [];
  for (const el of els) {
    const s = getComputedStyle(el); if (s.display === 'none' || s.visibility === 'hidden' || !el.checkVisibility()) continue;
    const r = document.createRange(); r.selectNodeContents(el);
    const rects = [...r.getClientRects()].filter(x => x.width > 4 && x.height > 4);
    const b = rects.length ? rects.reduce((a, c) => ({ left: Math.min(a.left, c.left), top: Math.min(a.top, c.top),
      right: Math.max(a.right, c.right), bottom: Math.max(a.bottom, c.bottom) })) : el.getBoundingClientRect();
    if (b.right - b.left < 4 || b.right <= 0 || b.left >= innerWidth) continue;
    out.push({ text: (el.innerText || '').trim().split('\n')[0].slice(0, 12), left: b.left, top: b.top, right: b.right, bottom: b.bottom, color: s.color });
  }
  return out; }"""
HIDE_WORDS = """#site-navigation :is([class*="__link"], [class*="account"], [class*="language"], [data-nav-menu-button], [data-nav-logo]) { visibility: hidden !important; }"""


def relative_luminance(rgb):
    c = np.asarray(rgb, dtype=np.float64) / 255.0
    c = np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def word_grounds(page, width):
    """What stands behind each of the bar's words (the words hidden): the contrast of the words' ink
    with the darker tenth of the ground under the letters, and how busy that ground is (the spread
    of its levels, p90 - p10, in 0-255)."""
    words = page.evaluate(BAR_WORDS)
    tag = page.add_style_tag(content=HIDE_WORDS)
    page.wait_for_timeout(60)
    shot = np.asarray(Image.open(BytesIO(page.screenshot(clip={"x": 0, "y": 0, "width": width, "height": 130}))).convert("RGB"))
    tag.evaluate("el => el.remove()")
    k = shot.shape[1] / width
    out = []
    for w in words:
        x0, y0, x1, y1 = (int(round(v * k)) for v in (w["left"], w["top"], w["right"], w["bottom"]))
        ground = shot[max(0, y0) : y1, max(0, x0) : x1].reshape(-1, 3)
        if not len(ground):
            continue
        lum = relative_luminance(ground)
        ink = relative_luminance([float(v) for v in w["color"][w["color"].index("(") + 1 : -1].replace(",", " ").split()[:3]])
        levels = np.asarray(Image.fromarray(ground.reshape(1, -1, 3).astype(np.uint8)).convert("L"), dtype=np.float32)
        out.append({
            "text": w["text"],
            "ratio": float((np.percentile(lum, 10) + 0.05) / (ink + 0.05)),
            "spread": float(np.percentile(levels, 90) - np.percentile(levels, 10)),
        })
    return out


def sweep(page, depths, wait=160):
    states = []
    for y in depths:
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(wait)
        states.append(page.evaluate(SETTLE))
    return states


def settle_follows(tag, down, up, small_w, tall_w):
    """Checks shared by every engine: the settle follows the scroll one way down and is undone the
    same way up, is a gesture (not a snap), is complete by 240px and changes layout unseen."""
    ws = [s["mark"][2] for s in down]
    papers = [s["paper"] for s in down]
    draws = [s["draw"] for s in down]
    mono = (
        all(b <= a + 0.3 for a, b in zip(ws, ws[1:]))
        and all(b >= a - 0.005 for a, b in zip(papers, papers[1:]))
        and all(b >= a - 0.005 for a, b in zip(draws, draws[1:]))
    )
    between = [s["y"] for s in down if small_w + 2 < s["mark"][2] < tall_w - 2]
    check(
        f"{tag}: the title settles with the scroll, one way (mark only shrinks, paper and rule only grow going down), over the scroll not at a step",
        mono and len(between) >= 12 and min(between) >= 48 and max(between) <= 240,
        f"mark {[round(w, 1) for w in ws[::4]]}; paper {[round(q, 2) for q in papers[::4]]}; between sizes at {len(between)} depths ({min(between, default=None)}-{max(between, default=None)}px)",
    )
    top = [s for s in down if s["y"] <= 48]
    done = [s for s in down if s["y"] >= 240]
    check(
        f"{tag}: over the opening the title stands tall and clear; from 240px the bar is settled (small, solid paper, rule laid)",
        all(abs(s["mark"][2] - tall_w) < 0.6 and s["paper"] < 0.01 for s in top)
        and all(s["size"] == "small" and abs(s["mark"][2] - small_w) < 0.6 and s["paper"] > 0.999 and s["draw"] == 1 and s["ruleOpacity"] > 0.6 for s in done),
        f"at 0: {top[0]['mark'][2]:.1f}px, paper {top[0]['paper']}; at {done[0]['y']}: {done[0]['size']}, {done[0]['mark'][2]:.1f}px, paper {done[0]['paper']}, rule {done[0]['draw']}",
    )
    by = {s["y"]: s for s in down}
    a, b = by.get(239), by.get(240)
    seam = a and b and all(abs(x - y) < 0.6 for k in ("mark", "products", "about") for x, y in zip(a[k], b[k]))
    check(
        f"{tag}: where the bar takes its small layout (239 -> 240px) nothing moves",
        bool(seam),
        f"239: {a and [round(v, 1) for v in a['mark']]} ({a and a['size']}); 240: {b and [round(v, 1) for v in b['mark']]} ({b and b['size']})",
    )
    ups = {s["y"]: s for s in up}
    worst = max(
        max(abs(x - y) for k in ("mark", "products", "about") for x, y in zip(s[k], ups[s["y"]][k])) + 40 * abs(s["paper"] - ups[s["y"]]["paper"])
        for s in down if s["y"] in ups
    )
    check(f"{tag}: scrolling back up undoes it exactly (the same bar at every depth)", worst < 0.6, f"largest difference {worst:.2f}")


def settle_checks(browser, playwright):
    """Round 9: the title settles with the scroll. Over the first 48-240px the mark shrinks, the bar
    and its words settle, the paper comes in under the words and the rule is laid, with the
    reader's hand; scrolling back up undoes it; it is right as the page loads part way down; the
    words stay legible over the painting all the way; with reduced motion there are two states;
    in Firefox (no scroll-driven animation) the script does the same."""
    depths = list(range(0, 301, 6)) + [239, 240, 241]
    depths = sorted(set(depths))
    page = browser.new_page(viewport={"width": 1536, "height": 900})
    watch(page)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(2500)
    page.mouse.move(768, 896)
    tall_w, small_w = page.evaluate(
        """() => { const s = getComputedStyle(document.querySelector('header'));
        return [parseFloat(s.getPropertyValue('--insc-mark-tall')), parseFloat(s.getPropertyValue('--insc-mark-small'))]; }"""
    )
    down = sweep(page, depths)
    page.evaluate("window.scrollTo(0, 420)")
    page.wait_for_timeout(300)
    up = sweep(page, depths[::-1])
    settle_follows("settle (Chrome)", down, up, small_w, tall_w)

    # Every frame the page draws while it is scrolled from 0 to 400px and back by the wheel, through
    # the page's own smooth scrolling: the mark only shrinks going down and only grows coming back
    # up, and no frame runs long (a 60 fps page draws one every 16.7ms).
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(800)
    page.evaluate(
        """() => { window.__f = []; window.__on = true; const m = document.querySelector('[data-nav-logo]');
        const tick = t => { window.__f.push([t, scrollY, m.getBoundingClientRect().width]); if (window.__on) requestAnimationFrame(tick); };
        requestAnimationFrame(tick); }"""
    )
    for direction in (1, -1):
        for _ in range(10):
            page.mouse.wheel(0, 40 * direction)
            page.wait_for_timeout(90)
        page.wait_for_timeout(900)
    log = page.evaluate("(() => { window.__on = false; return window.__f; })()")
    turn = max(range(len(log)), key=lambda i: log[i][1])
    shrink = all(b[2] <= a[2] + 0.3 for a, b in zip(log[:turn], log[1 : turn + 1]))
    grow = all(b[2] >= a[2] - 0.3 for a, b in zip(log[turn:], log[turn + 1 :]))
    gaps = [b[0] - a[0] for a, b in zip(log, log[1:])]
    long = [round(g) for g in gaps if g > 25]
    check(
        "settle: filmed frame by frame through a wheel scroll down and back, it follows the scroll both ways, and no frame runs long",
        shrink and grow and log[turn][1] >= 380 and len(log) > 100 and len(long) <= max(2, len(log) // 50),
        f"{len(log)} frames, deepest {log[turn][1]:.0f}px, median {sorted(gaps)[len(gaps) // 2]:.1f}ms, over 25ms: {long[:6]}",
    )

    # Reloaded part way through the settle, and past it: every frame drawn while the page reloads
    # shows the bar as it was (the band of the mark and the words, above the words' painted stroke,
    # which comes and goes with the part being read), and once loaded it is the same bar. (The
    # smooth scrolling's own glide ends first.)
    page.wait_for_timeout(1500)
    for at in (150, 600):
        page.evaluate(f"window.scrollTo(0, {at})")
        page.wait_for_timeout(900)
        before = page.evaluate(SETTLE)
        if before["y"] != at:
            check(f"settle: reloaded {at}px down, the bar is right on every frame as the page loads", False, f"could not scroll to {at}: {before['y']}")
            continue
        band = round(page.evaluate("document.querySelector('[data-nav-trigger=\"products\"] [class*=\"__word\"]').getBoundingClientRect().bottom")) + 2
        clip = {"x": 0, "y": 0, "width": 1536, "height": band}
        reference = luma(Image.open(BytesIO(page.screenshot(clip=clip))))
        cdp = page.context.new_cdp_session(page)
        raw = []

        def frame(ev, raw=raw, cdp=cdp):
            raw.append(ev["data"])
            try:
                cdp.send("Page.screencastFrameAck", {"sessionId": ev["sessionId"]})
            except Exception:
                pass

        cdp.on("Page.screencastFrame", frame)
        cdp.send("Page.startScreencast", {"format": "png", "everyNthFrame": 1})
        page.wait_for_timeout(150)
        page.reload(wait_until="load")
        page.wait_for_timeout(1600)
        try:
            cdp.send("Page.stopScreencast")
        except Exception:
            pass
        shots = [Image.open(BytesIO(base64.b64decode(data))).convert("RGB") for data in raw]
        diffs = [float(np.abs(luma(im.crop((0, 0, 1536, band))) - reference).mean()) for im in shots]
        after = page.evaluate(SETTLE)
        same = abs(after["mark"][2] - before["mark"][2]) < 0.6 and abs(after["paper"] - before["paper"]) < 0.02 and after["y"] == at
        check(
            f"settle: reloaded {at}px down, the bar is right on every frame as the page loads",
            len(diffs) >= 10 and max(diffs) <= 2.5 and same,
            f"{len(diffs)} frames, most any frame differs: {max(diffs, default=-1):.2f} levels (mean); after: {after['mark'][2]:.1f}px, paper {after['paper']} at {after['y']}px",
        )
    page.close()

    # The words stay legible: behind every word, at every 8px of the settle, at three desktop sizes
    # and on a phone, the ground under the letters keeps a contrast of 7:1 or more with the words'
    # ink (WCAG's highest level) and is never busy (its levels spread 40 or less in 255: the
    # painting never shows through as shapes behind the letters).
    sizes = [
        ("1536", dict(viewport={"width": 1536, "height": 900})),
        ("1280", dict(viewport={"width": 1280, "height": 800})),
        ("1920", dict(viewport={"width": 1920, "height": 1080})),
        ("phone", dict(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2)),
    ]
    for tag, opts in sizes:
        page = browser.new_page(**opts)
        watch(page)
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(3000)
        if not opts.get("has_touch"):
            page.mouse.move(opts["viewport"]["width"] / 2, opts["viewport"]["height"] - 4)
        worst = []
        for y in range(0, 265, 8):
            page.evaluate(f"window.scrollTo(0, {y})")
            page.wait_for_timeout(200)
            worst += [dict(w, y=y) for w in word_grounds(page, opts["viewport"]["width"])]
        low = min(worst, key=lambda w: w["ratio"])
        busy = max(worst, key=lambda w: w["spread"])
        check(
            f"settle ({tag}): the bar's words stay legible over the painting all the way (7:1 or more, a quiet ground)",
            low["ratio"] >= 7 and busy["spread"] <= 40 and len(worst) >= 2 * 34,
            f"lowest {low['ratio']:.1f}:1 ({low['text']!r} at {low['y']}px); busiest ground {busy['spread']:.0f} ({busy['text']!r} at {busy['y']}px)",
        )
        page.close()

    # Reduced motion: two states, never between.
    page = browser.new_page(viewport={"width": 1536, "height": 900}, reduced_motion="reduce")
    watch(page)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(1500)
    states = sweep(page, list(range(0, 301, 6)), wait=120)
    tall = [s["y"] for s in states if abs(s["mark"][2] - tall_w) < 0.6 and s["paper"] < 0.01]
    small = [s["y"] for s in states if abs(s["mark"][2] - small_w) < 0.6 and s["paper"] > 0.999 and s["size"] == "small"]
    check(
        "reduced motion: the bar has two states (the title over the opening, the bar on paper past 48px), never between",
        len(tall) + len(small) == len(states) and tall and small and max(tall) < min(small) and max(tall) <= 48,
        f"tall to {max(tall, default=None)}px, small from {min(small, default=None)}px, {len(states) - len(tall) - len(small)} between",
    )
    page.close()

    # Firefox has no scroll-driven animation: the script writes the same settle.
    try:
        firefox = playwright.firefox.launch()
    except Exception as error:  # noqa: BLE001
        check("settle (Firefox): the script's fallback", False, f"Firefox would not start: {error}"[:200])
        return
    page = firefox.new_page(viewport={"width": 1536, "height": 900})
    page.on("pageerror", lambda e: errors.append(f"firefox {e}"[:300]))
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(3000)
    page.mouse.move(768, 896)
    native = page.evaluate("CSS.supports('animation-timeline: scroll()')")
    down = sweep(page, depths, wait=200)
    page.evaluate("window.scrollTo(0, 420)")
    page.wait_for_timeout(300)
    up = sweep(page, depths[::-1], wait=200)
    settle_follows(f"settle (Firefox, {'native' if native else 'the script'})", down, up, small_w, tall_w)
    firefox.close()


# ---------------------------------------------------------------- round 10: nothing dead, nothing small

# Everything the bar shows a visitor in its present state: visible text (each run of words, its
# size and its contrast with the paper: its colour and its opacity through every ancestor, over the
# paper), and every control a pointer or the keyboard can reach (its hit box).
SHOWN = """() => {
  const header = document.querySelector('header');
  const paper = [248, 243, 234];
  const lin = c => { c /= 255; return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; };
  const lum = ([r, g, b]) => 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
  const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((m, n) => n - m); return (x + 0.05) / (y + 0.05); };
  const seen = el => el.checkVisibility({ opacityProperty: true, visibilityProperty: true }) && !el.closest('[inert]');
  const onScreen = b => b.width > 1 && b.height > 1 && b.bottom > 0 && b.top < innerHeight && b.right > 0 && b.left < innerWidth;
  const alpha = el => { let a = 1; for (let n = el; n && n !== document.documentElement; n = n.parentElement) a *= +getComputedStyle(n).opacity; return a; };
  const texts = [];
  const walker = document.createTreeWalker(header, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const t = walker.currentNode; const words = t.textContent.trim(); const el = t.parentElement;
    if (!words || !seen(el) || el.closest('option, [role=status]')) continue;
    const r = document.createRange(); r.selectNodeContents(t);
    if (!onScreen(r.getBoundingClientRect())) continue;
    const s = getComputedStyle(el); const m = s.color.match(/[\\d.]+/g).map(Number);
    const k = (m.length > 3 ? m[3] : 1) * alpha(el);
    const shown = m.slice(0, 3).map((v, i) => v * k + paper[i] * (1 - k));
    texts.push({ text: words.slice(0, 24), size: parseFloat(s.fontSize), ratio: +ratio(shown, paper).toFixed(1) });
  }
  // A control's hit box: its own, and what its ::before reaches over where that is laid round it
  // (the mark's, a little round its picture; a short word's, out to 48px).
  const hit = el => { const b = el.getBoundingClientRect(); const box = { l: b.left, t: b.top, r: b.right, b: b.bottom };
    const p = getComputedStyle(el, '::before');
    if (p.content !== 'none' && p.position === 'absolute') {
      box.l = Math.min(box.l, b.left + parseFloat(p.left)); box.t = Math.min(box.t, b.top + parseFloat(p.top));
      box.r = Math.max(box.r, b.right - parseFloat(p.right)); box.b = Math.max(box.b, b.bottom - parseFloat(p.bottom)); }
    return { w: +(box.r - box.l).toFixed(1), h: +(box.b - box.t).toFixed(1) }; };
  const controls = [...header.querySelectorAll('a[href], button, select')]
    .filter(el => seen(el) && el.tabIndex >= 0 && onScreen(el.getBoundingClientRect()))
    .map(el => ({ text: (el.getAttribute('aria-label') || el.innerText || '').trim().slice(0, 24), ...hit(el) }));
  return { texts, controls };
}"""


def nothing_small(page, tag):
    """Every visible text in the bar, its drop-downs and its menu 15px or larger and 7:1 or more
    against the paper; every control 48px or more both ways."""
    m = page.evaluate(SHOWN)
    small = [(t["text"], t["size"]) for t in m["texts"] if t["size"] < 15]
    faint = [(t["text"], t["ratio"]) for t in m["texts"] if t["ratio"] < 7]
    short = [(c["text"], c["w"], c["h"]) for c in m["controls"] if c["w"] < 47.5 or c["h"] < 47.5]
    check(
        f"{tag}: nothing small or faint (text 15px+, 7:1+ on the paper; every control 48px+ both ways)",
        m["texts"] and m["controls"] and not small and not faint and not short,
        f"{len(m['texts'])} texts from {min(t['size'] for t in m['texts']):.0f}px, lowest "
        f"{min(t['ratio'] for t in m['texts'])}:1; {len(m['controls'])} controls"
        + (f"; small {small[:3]}" if small else "") + (f"; faint {faint[:3]}" if faint else "")
        + (f"; short {short[:4]}" if short else ""),
    )


# The ring the keyboard's focus draws: on the control itself, on a box laid round it (its ::before
# or ::after: the mark's, the bar's words', a row's parts'), or round a language picker's
# whole label (its globe, the language and the arrow).
FOCUS_RING = """() => {
  const el = document.activeElement; if (!el || el === document.body) return null;
  const box = (n, pseudo) => { const b = n.getBoundingClientRect(); const r = { l: b.left, t: b.top, r: b.right, b: b.bottom };
    if (pseudo) { const p = getComputedStyle(n, pseudo); r.l += parseFloat(p.left); r.t += parseFloat(p.top);
      r.r -= parseFloat(p.right); r.b -= parseFloat(p.bottom); } return r; };
  const ringOf = (n, pseudo) => { const s = getComputedStyle(n, pseudo);
    return s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) > 0 ? s : null; };
  let host = null, s = null, pseudo = null;
  const label = el.closest('label');
  for (const [n, p] of [[el, null], [el, '::before'], [el, '::after'], [label, null], [label, '::after']]) {
    if (n && (s = ringOf(n, p))) { host = n; pseudo = p; break; } }
  const name = (el.getAttribute('aria-label') || el.innerText || el.tagName).trim().replace(/\\s+/g, ' ').slice(0, 28);
  if (!host) return { name, style: 'none' };
  const b = box(host, pseudo); const off = parseFloat(s.outlineOffset) || 0, w = parseFloat(s.outlineWidth);
  const ring = { l: b.l - off - w, t: b.t - off - w, r: b.r + off + w, b: b.b + off + w };
  const out = { name, style: s.outlineStyle, width: w, color: s.outlineColor, radius: parseFloat(s.borderTopLeftRadius) || 0, ...ring };
  const logo = el.matches('[data-nav-logo]') && el.querySelector('span');
  if (logo) { const p = logo.getBoundingClientRect(); out.clear = Math.min(p.left - ring.l, p.top - ring.t, ring.r - p.right, ring.b - p.bottom) - w; }
  // Clear of the brush marks between the menu's lines, and of the settled bar's painted rule.
  const meets = r => r.width > 0 && r.right > ring.l && r.left < ring.r && r.bottom > ring.t && r.top < ring.b;
  out.dab = [...document.querySelectorAll('[class*="__dab"]')].some(d => meets(d.getBoundingClientRect()));
  const header = document.querySelector('header'); const rule = header.querySelector('[class*="__rule"]');
  if (header.dataset.size === 'small' && +getComputedStyle(rule).opacity > 0.5 && el.closest('#site-navigation')) {
    const r = rule.getBoundingClientRect(); out.rule = (r.top + r.bottom) / 2 - 2 - ring.b; }
  const globe = host.tagName === 'LABEL' && host.querySelector('svg');
  if (globe && globe.getBoundingClientRect().width > 0 && getComputedStyle(globe).display !== 'none') {
    const g = globe.getBoundingClientRect(); out.globe = g.left >= ring.l + w && g.right <= ring.r - w; }
  return out;
}"""


def ring_sides(page, ring):
    """Each side of the ring, from the pixels: the share of points along its middle (corners left
    out) where the darkest pixel across the band is ink (luma 110 or less)."""
    img = luma(Image.open(BytesIO(page.screenshot())))
    k = img.shape[1] / page.viewport_size["width"]
    w, pad = ring["width"], ring["radius"] + ring["width"] + 3

    def darkest(x, y, dx, dy):
        vals = []
        for d in (-1.5, -0.5, 0.5, 1.5):
            xi, yi = int(round((x + dx * d) * k)), int(round((y + dy * d) * k))
            if 0 <= xi < img.shape[1] and 0 <= yi < img.shape[0]:
                vals.append(img[yi, xi])
        return min(vals) if vals else 255

    sides = {}
    for side in ("top", "bottom", "left", "right"):
        if side in ("top", "bottom"):
            y = ring["t"] + w / 2 if side == "top" else ring["b"] - w / 2
            vals = [darkest(x, y, 0, 1) for x in np.linspace(ring["l"] + pad, ring["r"] - pad, 24)]
        else:
            x = ring["l"] + w / 2 if side == "left" else ring["r"] - w / 2
            vals = [darkest(x, y, 1, 0) for y in np.linspace(ring["t"] + pad, ring["b"] - pad, 12)]
        sides[side] = round(sum(v <= 110 for v in vals) / len(vals), 2)
    return sides


def ring_ok(page, tag, rings):
    """The ring on the focused control: 2px of ink, whole on all four sides in the pixels (never
    clipped by the bar, a fold or a mask), inside the window; round the mark with air between it and
    the leaf and the letters; round a picker with its globe inside it; never across the brush marks
    between the menu's lines, and in the settled bar clear of its painted rule."""
    ring = page.evaluate(FOCUS_RING)
    if not ring:
        return None
    bad = ""
    if ring["style"] == "none":
        bad = "no ring"
    else:
        sides = ring_sides(page, ring)
        W, H = page.viewport_size["width"], page.viewport_size["height"]
        if abs(ring["width"] - 2) > 0.01 or ring["color"] != "rgb(12, 11, 10)":
            bad = f"{ring['width']}px {ring['color']}"
        elif not (ring["l"] >= 0 and ring["t"] >= 0 and ring["r"] <= W and ring["b"] <= H):
            bad = f"outside the window ({ring['l']:.0f},{ring['t']:.0f})-({ring['r']:.0f},{ring['b']:.0f})"
        elif min(sides.values()) < 0.9:
            bad = f"not whole {sides}"
        elif ring.get("clear") is not None and ring["clear"] < 4:
            bad = f"{ring['clear']:.1f}px from the mark"
        elif ring.get("globe") is False:
            bad = "the globe outside it"
        elif ring.get("dab"):
            bad = "across a brush mark between the lines"
        elif ring.get("rule") is not None and ring["rule"] < 2:
            bad = f"on the rule ({ring['rule']:.1f}px)"
    rings.append((f"{tag} {ring['name']}", bad))
    return ring


def tab_rings(page, tag, rings, stops, until=None):
    """Tab on through the header, checking each stop's ring; stop on leaving the header or at
    `until` (a name)."""
    names = []
    for _ in range(stops):
        page.keyboard.press("Tab")
        page.wait_for_timeout(420)
        if not page.evaluate("!!document.activeElement?.closest('header')"):
            if names:
                break
            continue
        name = page.evaluate("(document.activeElement.getAttribute('aria-label') || document.activeElement.innerText || '').trim()")
        if name.startswith(("Products", "Science")) and page.evaluate(
            "document.activeElement.hasAttribute('data-nav-sheet-toggle') && document.activeElement.getAttribute('aria-expanded') === 'false'"
        ):
            page.keyboard.press("Enter")
            page.wait_for_timeout(1000)
        ring = ring_ok(page, tag, rings)
        names.append(ring["name"] if ring else "?")
        if until and until in name:
            break
    return names


def sign_up(page, tag, scope):
    """Sign up has no link yet (Mo has not given it): until it has, it is a placeholder that promises
    nothing. Not a Tab stop, the default cursor, and pointing at it or pressing on it changes nothing
    on the screen. Once it leads somewhere (a link, or an enabled button), this holds it to nothing
    more than being one."""
    loc = page.locator(f"{scope} button", has_text="Sign up").first
    info = loc.evaluate("b => ({ disabled: b.disabled, tab: b.tabIndex, cursor: getComputedStyle(b).cursor })")
    if not info["disabled"]:
        check(f"{tag}: Sign up leads somewhere", True, "enabled")
        return
    box = loc.bounding_box()
    clip = {"x": box["x"] - 6, "y": box["y"] - 6, "width": box["width"] + 12, "height": box["height"] + 12}
    page.mouse.move(page.viewport_size["width"] / 2, page.viewport_size["height"] - 4)
    page.wait_for_timeout(600)
    rest = Image.open(BytesIO(page.screenshot(clip=clip))).convert("RGB")
    page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    page.wait_for_timeout(700)
    pointed = Image.open(BytesIO(page.screenshot(clip=clip))).convert("RGB")
    page.mouse.down()
    page.wait_for_timeout(250)
    pressed = Image.open(BytesIO(page.screenshot(clip=clip))).convert("RGB")
    page.mouse.up()
    page.mouse.move(page.viewport_size["width"] / 2, page.viewport_size["height"] - 4)
    changed = max(max(hi for _, hi in ImageChops.difference(rest, im).getextrema()) for im in (pointed, pressed))
    check(
        f"{tag}: Sign up (no link yet) promises nothing: not a Tab stop, the default cursor, unchanged when pointed at or pressed",
        info["cursor"] == "default" and changed <= 8,
        f"disabled, cursor {info['cursor']}, most any pixel changed {changed} levels",
    )


# The language picker's room against its words: how much wider the select is than the language it
# shows (with its own padding, which holds the arrow).
PICKER = """() => [...document.querySelectorAll('header select')].filter(s => s.checkVisibility()).map(s => {
  const st = getComputedStyle(s); const probe = document.createElement('span');
  probe.textContent = s.selectedOptions[0].textContent;
  probe.style.cssText = `position:absolute;visibility:hidden;white-space:pre;font:${st.font}`;
  document.body.append(probe); const words = probe.getBoundingClientRect().width; probe.remove();
  const room = parseFloat(st.paddingLeft) + parseFloat(st.paddingRight) + parseFloat(st.borderLeftWidth) + parseFloat(st.borderRightWidth);
  return { text: s.selectedOptions[0].textContent, spare: +(s.getBoundingClientRect().width - words - room).toFixed(1) }; })"""


def round10(browser, playwright):
    """Round 10: every control says what it does, nothing is small, every focus ring is whole."""
    rings: list[tuple[str, str]] = []

    # The language picker is as wide as the language it shows, so its arrow stands beside the word:
    # in Chrome by the stylesheet (field-sizing), in Firefox (no field-sizing: the picker was as wide
    # as "Tiếng Việt", "English" a long gap from its arrow) by the script.
    spare = []
    for name, engine in (("Chrome", None), ("Firefox", playwright.firefox)):
        b = browser if engine is None else engine.launch()
        for loc, w, h in (("", 1536, 900), ("vn", 1101, 800), ("cns", 1280, 800), ("", 390, 844)):
            page = b.new_page(viewport={"width": w, "height": h})
            page.goto(f"{BASE}/{loc}", wait_until="networkidle")
            page.wait_for_timeout(1500)
            spare += [(name, loc or "en", w, x["text"], x["spare"]) for x in page.evaluate(PICKER)]
            page.close()
        if engine is not None:
            b.close()
    check(
        "the language picker is as wide as the language it shows, its arrow beside the word (Chrome and Firefox)",
        len(spare) >= 8 and all(-1 <= x[-1] <= 6 for x in spare),
        "; ".join(f"{n} {loc} {w}: {t} {sp:+}px" for n, loc, w, t, sp in spare),
    )

    for w, h in ((1536, 900), (1101, 800)):
        tag = f"r10 {w}x{h}"
        page = browser.new_page(viewport={"width": w, "height": h})
        watch(page)
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(2500)
        warm(page)
        nothing_small(page, f"{tag} over the opening")
        sign_up(page, tag, "#site-navigation [class*=\"__account\"]")
        tab_rings(page, f"{tag} top:", rings, 10)
        page.evaluate("document.activeElement?.blur()")
        scroll_to(page, 1400)
        nothing_small(page, f"{tag} scrolled")
        page.evaluate("document.querySelector('[class*=skip]')?.focus()")
        tab_rings(page, f"{tag} scrolled:", rings, 10)
        scroll_to(page, 0)
        page.mouse.move(w / 2, h - 4)
        for panel, last in (("products", "Science"), ("science", "BiGH home")):
            page.locator(f'[data-nav-trigger="{panel}"]').focus()
            page.keyboard.press("Enter")
            page.wait_for_timeout(1300)
            nothing_small(page, f"{tag} {panel.capitalize()}")
            if panel == "products":
                wash = page.evaluate(
                    """() => { const w = document.querySelector('[class*="__wash"]'); const s = getComputedStyle(w);
                    return { a: +(s.backgroundColor.match(/[\\d.]+/g)[3] ?? 1), o: +s.opacity }; }"""
                )
                check(
                    f"{tag}: the wash under the open scroll is 26-32% (a headline under its torn edge recedes; round 9)",
                    0.26 <= wash["a"] * wash["o"] <= 0.32,
                    wash,
                )
            tab_rings(page, f"{tag} {panel}:", rings, 10, until=last)
            page.keyboard.press("Escape")
            page.wait_for_timeout(600)
        page.close()

    for w, h, mobile in ((390, 844, True), (360, 640, True), (834, 1112, False)):
        tag = f"r10 {w}x{h} menu"
        page = browser.new_page(viewport={"width": w, "height": h}, is_mobile=mobile, has_touch=mobile, device_scale_factor=2)
        watch(page)
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(2000)
        nothing_small(page, f"r10 {w}x{h} bar")
        tab_rings(page, f"r10 {w}x{h} bar:", rings, 4)
        page.locator("[data-nav-menu-button]").focus()
        page.keyboard.press("Enter")
        page.wait_for_timeout(1400)
        nothing_small(page, f"{tag} open")
        for part in ("products", "science"):
            unfold(page, part)
            nothing_small(page, f"{tag} {part.capitalize()}")
        sheet_end(page)
        sign_up(page, tag, "[data-nav-sheet] [class*=\"__sheetFoot\"]")
        page.locator("[data-nav-menu-button]").focus()
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)
        page.locator("[data-nav-menu-button]").focus()
        page.keyboard.press("Enter")
        page.wait_for_timeout(1400)
        # Every stop of the menu, from the keyboard, unfolding each part on the way: whole, and in
        # the window (the menu runs on under the window's foot; it keeps the focus above it).
        tab_rings(page, f"{tag}:", rings, 40, until="Log in")
        page.close()

    # A short phone, scrolled down through Products to Science at the window's foot: pressing it
    # folds Products away above it. The menu's own scroll used to carry Science up and out of the
    # window (focus left on a word above it, the visitor in the middle of its rows); the word pressed
    # stays in the window, under the bar, on every frame and at the end.
    page = browser.new_page(viewport={"width": 360, "height": 640}, is_mobile=True, has_touch=True, device_scale_factor=2)
    watch(page)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(2000)
    page.locator("[data-nav-menu-button]").click()
    page.wait_for_timeout(1300)
    unfold(page, "products")
    results_at = []
    for foot in (24, 120):
        page.evaluate(
            """(foot) => { const s = document.querySelector('[data-nav-sheet]');
            const sci = document.querySelector('[data-nav-sheet-toggle="science"]');
            s.scrollTop += sci.getBoundingClientRect().bottom - (innerHeight - foot); }""",
            foot,
        )
        page.wait_for_timeout(400)
        page.evaluate(
            """() => { window.__w = []; window.__go = true;
            const sci = document.querySelector('[data-nav-sheet-toggle="science"]');
            const bar = document.querySelector('#site-navigation');
            const tick = () => { const r = sci.getBoundingClientRect();
              window.__w.push({ top: r.top, bottom: r.bottom, bar: bar.getBoundingClientRect().bottom });
              if (window.__go) requestAnimationFrame(tick); }; requestAnimationFrame(tick); }"""
        )
        page.locator('[data-nav-sheet-toggle="science"]').click()
        page.wait_for_timeout(1100)
        page.evaluate("window.__go = false")
        log = page.evaluate("window.__w")
        out = [round(e["top"]) for e in log if e["top"] < e["bar"] - 1 or e["bottom"] > 640]
        results_at.append((foot, len(log), round(log[-1]["top"]), out[:4]))
        # Fold Products open again for the next look.
        unfold(page, "products")
    page.close()
    check(
        "short phone 360x640: the word pressed in the menu stays in the window while the folds move (Science pressed at the foot)",
        all(n >= 30 and not out for _, n, _, out in results_at),
        "; ".join(f"Science {foot}px over the foot: {n} frames, ends at {end}px" + (f", out at {out}" if out else "") for foot, n, end, out in results_at),
    )

    # Every language: the bar over the opening and scrolled, both drop-downs at the narrowest
    # desktop, and the menu (its folds and its foot) on a phone. Two-character words (帮助, 登录,
    # 소개) are about 40px wide; their targets reach out to 48px.
    for loc in ("cns", "kr", "vn", "jp"):
        page = browser.new_page(viewport={"width": 1101, "height": 800})
        watch(page)
        page.goto(f"{BASE}/{loc}", wait_until="networkidle")
        page.wait_for_timeout(2500)
        warm(page)
        nothing_small(page, f"r10 {loc} 1101x800 over the opening")
        for panel in ("products", "science"):
            page.locator(f'[data-nav-trigger="{panel}"]').click()
            page.wait_for_timeout(1300)
            nothing_small(page, f"r10 {loc} 1101x800 {panel.capitalize()}")
        page.keyboard.press("Escape")
        scroll_to(page, 1400)
        nothing_small(page, f"r10 {loc} 1101x800 scrolled")
        page.close()
        page = browser.new_page(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2)
        watch(page)
        page.goto(f"{BASE}/{loc}", wait_until="networkidle")
        page.wait_for_timeout(2000)
        page.locator("[data-nav-menu-button]").click()
        page.wait_for_timeout(1400)
        for part in ("products", "science"):
            unfold(page, part)
            nothing_small(page, f"r10 {loc} 390x844 menu {part.capitalize()}")
        sheet_end(page)
        nothing_small(page, f"r10 {loc} 390x844 menu foot")
        page.close()

    bad = [f"{name}: {why}" for name, why in rings if why]
    check(
        "focus rings: every control of the bar, both drop-downs and the menu (phone, short phone, tablet) "
        "shows a whole 2px ink ring, inside the window, clear of the mark, the rule and the brush marks, round the picker's globe",
        len(rings) >= 80 and not bad,
        f"{len(rings)} stops; " + ("; ".join(bad[:6]) if bad else "all whole"),
    )


with sync_playwright() as p:
    browser = p.chromium.launch(args=["--use-angle=d3d11"])
    if ONLY in (None, "desk"):
        desktop(browser)
        rule_checks(browser)
        reading_stroke(browser)
        drop_down_motion(browser)
    if ONLY in (None, "desk", "settle"):
        settle_checks(browser, p)
    if ONLY in (None, "desk", "rows"):
        row_layout(browser)
        row_reach(browser)
        row_motion(browser)
        row_languages(browser)
    if ONLY in (None, "phone"):
        phone(browser)
        phone_rows(browser)
        menu_light_boxes(browser)
    if ONLY in (None, "tablet"):
        tablet(browser)
        tablet_rows(browser)
    if ONLY in (None, "lang"):
        languages(browser, p)
    if ONLY in (None, "r10"):
        round10(browser, p)
    browser.close()

check("no page errors or console errors", not errors, errors[:5])
fails = [name for name, ok in results if not ok]
print(f"\n{len(results) - len(fails)}/{len(results)} checks passed. Pictures: {OUT}")
sys.exit(1 if fails else 0)

"""QA for the menu bar, "Inscription" (Mo's pick, October 5, 2026), on the homepage.

usage: python -X utf8 scripts/qa/qa_nav.py [base] [--only=desk|showroom|science|phone|tablet|lang]
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
  - the Products showroom (round 4) at 1536x900, 1280x800, 1920x1080@2x, 1101x800 and 1366x657:
    the five names (28px+) visible, inside the window, on one left edge and evenly spaced (2px),
    every one a 48px+ link to its own page, its focus line (17px+) under it on the same edge; the
    bottle beside them 280px+ tall, its picture at least its size on screen (crisp), 40px+ clear of
    the names; the scroll's foot above the window's foot. NuriCell shown first (its name
    underlined); Discover goes to the shown product, Explore to the products. Tab steps through
    the five names in order, each showing its own bottle and Discover link, with a visible ring;
    resting the pointer on a name shows its bottle, passing over another on the way to Discover
    keeps it, and Discover goes to its page; on a touch laptop the first tap on a name opens its
    page. Filmed at real speed down the names: the bottle's place never empty, one line at a time.
  - the Science showroom (round 5), the second page of the same book, at 1536x900, 1280x800,
    1920x1080@2x, 1101x800 and 1366x657: the four names (28px+) visible, inside the window, on one
    left edge and evenly spaced, each a 48px+ link with its caption (17px+) under it; the names on
    Products' left edge and lines, the picture in the bottle's stand, the two links on Products'
    line (1px); Dr. Liu's print 75%+ of the stand's height and crisp; the scroll's foot above the
    window's foot. One weight (1536, 1101, 1920@2x, measured in the pixels): the three paintings'
    ink within 25% of their mean, the print as tall as any painting and 75%+ of the bottle, every
    picture crisp. Our scientists shown first; every name goes to its part, Explore to the science.
    Enter opens it and Tab steps through the four in order, each showing its own picture and link,
    with a visible ring; resting the pointer shows a part's picture, passing over another on the
    way to its link keeps it, and the link goes to its part; on a touch laptop the first tap opens
    its part. Filmed at real speed down the names: the picture's place never empty, one line at a
    time, no painting's paper as a light box; swapping back in from Products on a painting, no
    light box behind it.
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
    frame the page draws): Science opening on a painting (the cell: rested on, closed and opened
    again at once; it opens on Dr. Liu's print, which is never multiplied), from the tall bar and
    from the scrolled bar, and Products opening show no light box behind a painting or a pool
    (only pictures drawn at the end are measured): no sample of a multiplied
    picture is more than 4 levels lighter than the paper beside it, on any frame (two frames
    running) once the scroll has reached it (the showroom's pool, whose edge is masked, is read
    with the bottles hidden at the points where its own painting is paper, averaged, against the
    paper either side of the bottle, and must not be more than 1 level over it: multiplied it
    reads -2 to -7 levels, an isolated blend about +3). Moving from one drop-down to the other (both ways):
    the scroll's ink never drops below 60% of the lighter drop-down's, one drop-down is always drawn
    whole, only one word is ever underlined and no chevron is ever turned sideways; pointing on to
    About keeps one line. The tablet menu opens, and the phone menu's Products unfolds, with no
    light box round the pools and the chevron turning over, never sideways.
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

# Round 4: the paper beside a showroom's stand, left and right of it, `off` px out (28 beside a
# bottle; 90 beside a Science picture, whose paintings run a little past the stand on their paper).
BESIDE = """([sel, off]) => { const s = document.querySelector(sel + ' [class*="stageStand"]').getBoundingClientRect();
  return [s.left - off, s.right + off]; }"""

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
        # The showroom's pool fades out through an elliptical mask from 72% of its radius, so its
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


def light_boxes(film, pics, gaps, reveal, width, lo, hi):
    """Under multiply nothing in a picture can be lighter than the paper it lies on; an isolated blend
    shows the picture's white paper as a light box. For each picture, frame by frame from lo to hi ms:
    its lightest sample minus the paper beside it at the same height, counting only what the scroll
    (or fold) has already let down, with a margin. A value counts when two frames running show it.
    Returns {picture: (worst levels, frames measured)}."""
    series = {p["name"]: [] for p in pics}
    boxes = {p["name"]: samples(p) for p in pics}
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
            if panel == "science":
                # Science opens on Dr. Liu's print (a real photograph, never multiplied). To film a
                # painting settling in with the scroll: rest on Cellular health, close, and open
                # again at once (it keeps the cell for 0.42s after closing). A pointer click at the
                # button: a locator click would scroll the page, and scrolling closes the scroll.
                page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                page.wait_for_timeout(1200)
                cell = page.locator('[data-nav-panel="science"] [class*="nameText"]', has_text="Cellular health").bounding_box()
                page.mouse.move(cell["x"] + 30, cell["y"] + cell["height"] / 2, steps=4)
                page.wait_for_timeout(900)
            if panel == "products":
                # The pool is measured where the bottle would cover it: the bottles are hidden.
                hide = page.add_style_tag(
                    content='[data-nav-panel="products"] [class*="__big"] { visibility: hidden !important; }'
                )
            def act(panel=panel, box=box):
                if panel == "science":
                    # Closed and opened again at once (inside the film, so never later than the
                    # 0.42s the cell is kept); the film's clock starts at the click.
                    page.keyboard.press("Escape")
                    page.wait_for_timeout(60)
                page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)

            film.shoot(act, 1500)
            sel = f'[data-nav-panel="{panel}"]'
            top, height = page.evaluate(
                f"(() => {{ const r = document.querySelector('{sel}').getBoundingClientRect(); return [r.top, r.height]; }})()"
            )
            pics = page.evaluate(PICTURES, sel)
            found = light_boxes(
                film,
                pics,
                page.evaluate(BESIDE, [sel, 90 if panel == "science" else 28]),
                lambda e: top + e["r"] * height - deckle,
                1536,
                250,
                1500,
            )
            if panel == "science":
                name = f"{tag}: Science opens on a painting (the cell) with no light box behind it (filmed at real speed)"
                shown = [pic["file"].rsplit("/", 1)[-1] for pic in pics]
                if shown == ["mito.webp"]:
                    no_light_box(name, found)
                else:
                    check(name, False, f"the cell was not the picture shown: {shown}")
            else:
                no_light_box(f"{tag}: Products opens with no light box round the showroom bottle's pool (filmed at real speed)", found)
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


# ---------------------------------------------------------------- round 4: the Products showroom

SLUGS = ["nuricell", "green-bee-propolis", "advanced-opc", "turmerific", "nature-calm"]
NAMES = ["NuriCell", "Green Bee Propolis", "Advanced OPC Formula", "Turmerific", "Nature Calm"]

SHOWROOM = r"""() => {
  const p = document.querySelector('[data-nav-panel="products"]');
  const box = el => { const r = el.getBoundingClientRect();
    return { l: r.left, r: r.right, t: r.top, b: r.bottom, w: r.width, h: r.height }; };
  const names = [...p.querySelectorAll('a[class*="nameLink"]')].map(a => {
    const n = a.querySelector('[class*="nameText"]'), f = a.querySelector('[class*="nameFocus"]');
    return { href: a.getAttribute('href'), name: n.textContent.trim(), focus: f.textContent.trim(),
      size: parseFloat(getComputedStyle(n).fontSize), fsize: parseFloat(getComputedStyle(f).fontSize),
      n: box(n), f: box(f), a: box(a), shown: a.hasAttribute('data-shown'),
      visible: n.checkVisibility({ opacityProperty: true, visibilityProperty: true }) };
  });
  const big = p.querySelector('[class*="__big"][data-shown]');
  const w = /[?&]w=(\d+)/.exec(big.currentSrc);
  const paper = document.querySelector('header [class*="__paper"]').getBoundingClientRect();
  return { names, stand: box(p.querySelector('[class*="stageStand"]')),
    big: { src: decodeURIComponent(big.currentSrc), w: w ? +w[1] : 0, css: big.getBoundingClientRect().width },
    links: [...p.querySelectorAll('a[class*="more"]')].map(a => ({ text: a.textContent.trim(), href: a.getAttribute('href') })),
    paperBottom: paper.bottom, vh: innerHeight, vw: innerWidth, dpr: devicePixelRatio };
}"""


def open_products(page):
    """Reach for the bar (the pictures load), then open Products with a click and rest the pointer
    on empty paper inside the scroll."""
    w = page.viewport_size["width"]
    page.mouse.move(w * 0.7, 40)
    page.wait_for_timeout(300)
    page.wait_for_function(
        "[...document.querySelectorAll('[data-nav-panel] img')].every(i => i.complete && i.naturalWidth > 0)",
        timeout=30000,
    )
    page.mouse.move(w / 2, page.viewport_size["height"] - 6)
    page.wait_for_timeout(600)
    page.locator('[data-nav-trigger="products"]').click()
    page.wait_for_timeout(200)
    bar = page.evaluate("document.querySelector('#site-navigation').getBoundingClientRect().bottom")
    page.mouse.move(12, bar + 30, steps=4)
    page.wait_for_timeout(1500)


def shown_product(page):
    info = page.evaluate(SHOWROOM)
    return info, next((s for s in SLUGS if f"/products/{s}." in info["big"]["src"]), None)


def showroom_layout(browser):
    """Round 4: at each desktop size the five names stand large on one left edge, evenly spaced,
    each with its focus line under it, every one a link to its own page; the bottle stands large
    and crisp beside them, clear of the names; the scroll ends above the window's foot."""
    for w, h, dsf in ((1536, 900, 1), (1280, 800, 1), (1920, 1080, 2), (1101, 800, 1), (1366, 657, 1)):
        tag = f"showroom {w}x{h}" + (f"@{dsf}x" if dsf > 1 else "")
        page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=dsf)
        watch(page)
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(2000)
        open_products(page)
        page.screenshot(path=str(OUT / f"showroom-{w}x{h}.png"))
        info, slug = shown_product(page)
        names = info["names"]
        lefts = [n["n"]["l"] for n in names]
        steps = [round(b["n"]["t"] - a["n"]["t"], 1) for a, b in zip(names, names[1:])]
        check(
            f"{tag}: the five names, large (28px+), visible, inside the window, on one left edge, evenly spaced",
            [n["name"] for n in names] == NAMES
            and all(n["size"] >= 28 and n["visible"] and n["n"]["l"] >= 0 and n["n"]["r"] <= info["vw"] for n in names)
            and max(lefts) - min(lefts) <= 1
            and max(steps) - min(steps) <= 2
            and all(n["a"]["h"] >= 48 for n in names),
            f"sizes {[n['size'] for n in names]}; lefts {sorted(set(round(x) for x in lefts))}; steps {steps}",
        )
        check(
            f"{tag}: each focus line (17px+) under its own name, on its left edge",
            all(
                n["fsize"] >= 17 and abs(n["f"]["l"] - n["n"]["l"]) <= 1 and 0 <= n["f"]["t"] - n["n"]["b"] <= 14
                for n in names
            ),
            [(n["focus"][:18], n["fsize"], round(n["f"]["t"] - n["n"]["b"])) for n in names],
        )
        need = info["big"]["css"] * info["dpr"]
        gap = info["stand"]["l"] - max(n["n"]["r"] for n in names)
        check(
            f"{tag}: the bottle stands large (280px+) and crisp (its picture at least its size on screen), clear of the names",
            info["stand"]["h"] >= 279.5 and info["big"]["w"] >= need * 0.98 and gap >= 40,
            f"stand {info['stand']['h']:.0f}px; picture {info['big']['w']}w for {need:.0f}px; gap {gap:.0f}px",
        )
        check(
            f"{tag}: the scroll ends above the window's foot",
            info["paperBottom"] <= info["vh"],
            f"scroll foot {info['paperBottom']:.0f}, window {info['vh']}",
        )
        if (w, h) == (1536, 900):
            hrefs = [n["href"] for n in names]
            check(
                "showroom: every name is a link to its own product page",
                all(href.endswith(f"/products/{s}") for href, s in zip(hrefs, SLUGS)),
                hrefs,
            )
            check(
                "showroom: NuriCell shown first, its name underlined, Discover goes to it, Explore to the products",
                slug == "nuricell"
                and [n["shown"] for n in names] == [True, False, False, False, False]
                and any(
                    link["text"].startswith("Discover NuriCell") and link["href"].endswith("/products/nuricell")
                    for link in info["links"]
                )
                and any(
                    link["text"].startswith("Explore our products") and link["href"].endswith("/#products")
                    for link in info["links"]
                ),
                info["links"],
            )
        page.close()


def showroom_reach(browser):
    """Round 4: every product is reachable directly. By keyboard: Tab from the open Products steps
    through the five names in order, each showing its own bottle and Discover link. By pointer:
    resting on a name shows its bottle; passing over another name on the way to Discover does not
    change it; Discover goes to the shown product. On a touch laptop: the first tap on a name opens
    its page (no preview-only tap)."""
    page = browser.new_page(viewport={"width": 1536, "height": 900})
    watch(page)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(2000)
    open_products(page)
    page.locator('[data-nav-trigger="products"]').focus()
    seen = []
    for _ in range(5):
        page.keyboard.press("Tab")
        page.wait_for_timeout(120)
        info, slug = shown_product(page)
        discover = next((link["text"] for link in info["links"] if link["text"].startswith("Discover")), "")
        seen.append((focused(page)[:24], slug, discover))
    page.screenshot(path=str(OUT / "showroom-keyboard-naturecalm.png"))
    page.keyboard.press("Tab")
    after = focused(page)
    check(
        "showroom: Tab reaches every product's name in order, each showing its own bottle and Discover link",
        all(
            f.startswith(n) and slug == s and d.startswith(f"Discover {n}")
            for (f, slug, d), n, s in zip(seen, NAMES, SLUGS)
        )
        and "Explore our products" in after,
        f"{seen}; then {after!r}",
    )
    page.keyboard.press("Shift+Tab")
    ring = page.evaluate(
        "(() => { const s = getComputedStyle(document.activeElement); return s.outlineStyle + ' ' + s.outlineWidth; })()"
    )
    check(
        "showroom: a visible ring on a name under the keyboard's focus",
        "Nature Calm" in focused(page) and not ring.endswith(" 0px") and "none" not in ring,
        f"{focused(page)!r}: {ring}",
    )
    page.keyboard.press("Escape")
    page.wait_for_timeout(400)

    open_products(page)
    links = page.locator('[data-nav-panel="products"] a[class*="nameLink"]')
    t = links.nth(3).locator('[class*="nameText"]').bounding_box()
    page.mouse.move(t["x"] + 20, t["y"] + t["height"] / 2, steps=6)
    page.wait_for_timeout(800)
    info, slug = shown_product(page)
    check("showroom: resting on a name shows its bottle", slug == "turmerific", slug)
    nc = links.nth(4).locator('[class*="nameText"]').bounding_box()
    disc = page.locator('[data-nav-panel="products"] a[class*="more"]', has_text="Discover").bounding_box()
    page.mouse.move(nc["x"] + 20, nc["y"] + nc["height"] / 2, steps=2)
    page.mouse.move(disc["x"] + 30, disc["y"] + disc["height"] / 2, steps=3)
    page.wait_for_timeout(700)
    info, slug = shown_product(page)
    check("showroom: passing over another name on the way to Discover keeps the bottle", slug == "turmerific", slug)
    page.mouse.click(disc["x"] + 30, disc["y"] + disc["height"] / 2)
    page.wait_for_url("**/products/turmerific**", timeout=30000)
    check("showroom: Discover goes to the shown product's page", "/products/turmerific" in page.url, page.url)
    page.close()

    ctx = browser.new_context(viewport={"width": 1536, "height": 900}, has_touch=True)
    page = ctx.new_page()
    watch(page)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(2000)
    page.locator('[data-nav-trigger="products"]').tap()
    page.wait_for_timeout(1200)
    page.locator('[data-nav-panel="products"] a[class*="nameLink"]', has_text="Green Bee Propolis").tap()
    try:
        page.wait_for_url("**/products/green-bee-propolis**", timeout=30000)
    except Exception:
        pass
    check(
        "showroom: on a touch laptop the first tap on a name opens its page",
        "/products/green-bee-propolis" in page.url,
        page.url,
    )
    ctx.close()


# Every frame: which names carry their line (scale over 4%).
NAME_LINES = """() => { const names = [...document.querySelectorAll('[data-nav-panel="products"] [class*="nameText"]')];
  window.__log = []; window.__logging = true;
  const tick = () => { window.__log.push({ t: performance.timeOrigin + performance.now(),
      lines: names.filter(n => (parseFloat(getComputedStyle(n, '::after').scale) || 0) > 0.04).map(n => n.textContent.trim()) });
    if (window.__logging) requestAnimationFrame(tick); };
  requestAnimationFrame(tick); }"""


def showroom_motion(browser):
    """Round 4, filmed at real speed: moving down the names from NuriCell to Nature Calm (resting on
    each), the bottle's place is never empty (its ink never under 60% of the lightest bottle's at
    rest) and only one name carries its line on every frame."""
    page = browser.new_page(viewport={"width": 1536, "height": 900})
    watch(page)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(2500)
    open_products(page)
    stand = page.locator('[data-nav-panel="products"] [class*="stageStand"]').bounding_box()
    crop = (round(stand["x"]), round(stand["y"]), round(stand["x"] + stand["width"]), round(stand["y"] + stand["height"]))
    beside = (crop[0] - 60, crop[1], crop[0] - 20, crop[3])
    links = page.locator('[data-nav-panel="products"] a[class*="nameLink"]')
    spots = []
    for i in range(5):
        b = links.nth(i).locator('[class*="nameText"]').bounding_box()
        spots.append((b["x"] + 20, b["y"] + b["height"] / 2))

    def ink(img):
        a = luma(img.crop(crop))
        paper = float(np.median(luma(img.crop(beside))))
        return float(np.clip(paper - a - 6, 0, None).mean())

    rest = []
    for x, y in spots:
        page.mouse.move(x, y, steps=4)
        page.wait_for_timeout(1000)
        rest.append(ink(Image.open(BytesIO(page.screenshot()))))
    page.mouse.move(*spots[0], steps=4)
    page.wait_for_timeout(1000)
    film = Film(page)
    page.evaluate(NAME_LINES)
    film.raw = []
    film.cdp.send("Page.startScreencast", {"format": "png", "everyNthFrame": 1})
    page.wait_for_timeout(150)
    for x, y in spots[1:]:
        page.mouse.move(x, y, steps=8)
        page.wait_for_timeout(450)
    page.wait_for_timeout(700)
    film.cdp.send("Page.stopScreencast")
    page.evaluate("window.__logging = false")
    log = page.evaluate("window.__log")
    shares = [round(ink(img) / min(rest), 2) for _, _, img in film.frames(0)]
    two = [e["lines"] for e in log if len(e["lines"]) > 1]
    check(
        "showroom: moving down the names, the bottle's place is never empty (filmed: its ink never under 60% of the lightest bottle's)",
        len(shares) >= 20 and min(shares) >= 0.6,
        f"least {min(shares, default=0)} over {len(shares)} frames; at rest {[round(r, 1) for r in rest]}",
    )
    check(
        "showroom: only one name underlined on every frame (filmed)",
        len(log) >= 60 and not two and log[-1]["lines"] == ["Nature Calm"],
        f"{len(log)} frames; two at once {two[:3]}; last {log[-1]['lines'] if log else None}",
    )
    page.close()


# ---------------------------------------------------------------- round 5: the Science showroom

PARTS = ["Our scientists", "Cellular health", "Research library", "Ask BiGH Science"]
PART_HREFS = ["/science#scientists", "/science#health", "/science#research", "/science#ask"]
PART_LINKS = ["Meet our scientists", "Explore cellular health", "Explore the research", "Discover Ask BiGH Science"]
PLATES = ["print", "cell", "reading", "inkstone"]
PAINTED = {"mito": "cell", "reading": "reading", "inkstone": "inkstone"}

SCIENCE = r"""() => {
  const box = el => { const r = el.getBoundingClientRect();
    return { l: r.left, r: r.right, t: r.top, b: r.bottom, w: r.width, h: r.height }; };
  const room = id => {
    const p = document.querySelector(`[data-nav-panel="${id}"]`);
    const names = [...p.querySelectorAll('a[class*="nameLink"]')].map(a => {
      const n = a.querySelector('[class*="nameText"]'), f = a.querySelector('[class*="nameFocus"]');
      return { href: a.getAttribute('href'), name: n.textContent.trim(), line: f.textContent.trim(),
        size: parseFloat(getComputedStyle(n).fontSize), fsize: parseFloat(getComputedStyle(f).fontSize),
        n: box(n), f: box(f), a: box(a), shown: a.hasAttribute('data-shown'),
        visible: n.checkVisibility({ opacityProperty: true, visibilityProperty: true }) };
    });
    const links = [...p.querySelectorAll('a[class*="more"]')].map(a => ({ text: a.textContent.trim(),
      href: a.getAttribute('href'), ...box(a) }));
    return { names, links, stand: box(p.querySelector('[class*="stageStand"]')) };
  };
  const p = document.querySelector('[data-nav-panel="science"]');
  const plate = p.querySelector('[data-plate][data-shown]');
  const img = plate.tagName === 'IMG' ? plate : plate.querySelector('img');
  const w = /[?&]w=(\d+)/.exec(img.currentSrc);
  const paper = document.querySelector('header [class*="__paper"]').getBoundingClientRect();
  return { science: room('science'), products: room('products'),
    plate: { kind: plate.dataset.plate, ...box(plate), w: w ? +w[1] : 0, css: img.getBoundingClientRect().width },
    paperBottom: paper.bottom, vh: innerHeight, vw: innerWidth, dpr: devicePixelRatio };
}"""


def open_science(page):
    """Reach for the bar (the pictures load), then open Science with a click and rest the pointer
    on empty paper inside the scroll."""
    w = page.viewport_size["width"]
    page.mouse.move(w * 0.7, 40)
    page.wait_for_timeout(300)
    page.wait_for_function(
        "[...document.querySelectorAll('[data-nav-panel] img')].every(i => i.complete && i.naturalWidth > 0)",
        timeout=30000,
    )
    page.mouse.move(w / 2, page.viewport_size["height"] - 6)
    page.wait_for_timeout(600)
    page.locator('[data-nav-trigger="science"]').click()
    page.wait_for_timeout(200)
    bar = page.evaluate("document.querySelector('#site-navigation').getBoundingClientRect().bottom")
    page.mouse.move(12, bar + 30, steps=4)
    page.wait_for_timeout(1500)


def rest_on(page, panel, i, ms=1000):
    b = page.locator(f'[data-nav-panel="{panel}"] a[class*="nameLink"]').nth(i).locator('[class*="nameText"]').bounding_box()
    page.mouse.move(b["x"] + 30, b["y"] + b["height"] / 2, steps=4)
    page.wait_for_timeout(ms)
    return b


def weigh(img, stand):
    """The ink of the picture standing in `stand` (a screenshot): its height (rows 30+ levels darker
    than the paper beside the stand) and its mass (darkness summed over the stand, widened 15% each
    side for the paintings that run past it; the link under it is left out)."""
    a = luma(img)
    k = img.width / stand["vw"]
    x0, x1 = (stand["l"] - 0.15 * stand["w"]) * k, (stand["r"] + 0.15 * stand["w"]) * k
    y0, y1 = (stand["t"] - 0.04 * stand["h"]) * k, stand["b"] * k
    paper = float(np.median(a[round(y0) : round(y1), round(x0 - 60 * k) : round(x0 - 20 * k)]))
    dark = np.clip(paper - a[round(y0) : round(y1), round(x0) : round(x1)], 0, None)
    rows = np.where((dark > 30).sum(axis=1) > 2)[0]
    return {"h": round(float(rows.max() - rows.min()) / k) if len(rows) else 0, "mass": float(dark.sum()) / (k * k * 1e3)}


def science_layout(browser):
    """Round 5: Science is the second page of the same book as Products. At each desktop size the
    four names stand large on one left edge, evenly spaced, each with its caption under it, every
    one a link to its part; they start on the products' left edge and lines; the picture stands in
    the bottle's stand, large and crisp; the link under the names and the link under the picture
    are on Products' line; the scroll ends above the window's foot. The four pictures are of one
    weight: the three paintings' ink within 25% of their mean, Dr. Liu's print at least as tall as
    every painting (no longer the smallest) and at least three quarters of the bottle's height."""
    for w, h, dsf in ((1536, 900, 1), (1280, 800, 1), (1920, 1080, 2), (1101, 800, 1), (1366, 657, 1)):
        tag = f"science {w}x{h}" + (f"@{dsf}x" if dsf > 1 else "")
        page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=dsf)
        watch(page)
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(2000)
        open_science(page)
        page.screenshot(path=str(OUT / f"science-{w}x{h}.png"))
        info = page.evaluate(SCIENCE)
        sci, pro = info["science"], info["products"]
        names = sci["names"]
        lefts = [n["n"]["l"] for n in names]
        steps = [round(b["n"]["t"] - a["n"]["t"], 1) for a, b in zip(names, names[1:])]
        check(
            f"{tag}: the four names, large (28px+), visible, inside the window, on one left edge, evenly spaced",
            [n["name"] for n in names] == PARTS
            and all(n["size"] >= 28 and n["visible"] and n["n"]["l"] >= 0 and n["n"]["r"] <= info["vw"] for n in names)
            and max(lefts) - min(lefts) <= 1
            and max(steps) - min(steps) <= 2
            and all(n["a"]["h"] >= 48 for n in names),
            f"sizes {[n['size'] for n in names]}; lefts {sorted(set(round(x) for x in lefts))}; steps {steps}",
        )
        check(
            f"{tag}: each caption (17px+) under its own name, on its left edge",
            all(
                n["fsize"] >= 17 and abs(n["f"]["l"] - n["n"]["l"]) <= 1 and 0 <= n["f"]["t"] - n["n"]["b"] <= 14
                for n in names
            ),
            [(n["line"][:18], n["fsize"], round(n["f"]["t"] - n["n"]["b"])) for n in names],
        )
        same = lambda u, v: abs(u - v) <= 1  # noqa: E731
        sline = max(link["b"] for link in sci["links"]) - min(link["b"] for link in sci["links"])
        check(
            f"{tag}: one page with Products: the names on its edge and lines, the picture in the bottle's stand, the links on its line (1px)",
            all(same(a["n"]["l"], b["n"]["l"]) and same(a["n"]["t"], b["n"]["t"]) for a, b in zip(names, pro["names"]))
            and all(same(sci["stand"][k], pro["stand"][k]) for k in ("l", "t", "w", "h"))
            and sline <= 1
            and all(same(a["b"], pro["links"][0]["b"]) for a in sci["links"]),
            f"names {[(round(n['n']['l']), round(n['n']['t'])) for n in names]} vs "
            f"{[(round(n['n']['l']), round(n['n']['t'])) for n in pro['names'][:4]]}; stand "
            f"{[round(sci['stand'][k]) for k in ('l', 't', 'w', 'h')]} vs {[round(pro['stand'][k]) for k in ('l', 't', 'w', 'h')]}; "
            f"links {[round(x['b']) for x in sci['links']]} vs {[round(x['b']) for x in pro['links']]}",
        )
        need = info["plate"]["css"] * info["dpr"]
        check(
            f"{tag}: the picture stands large (the print 75%+ of the stand's height) and crisp (its picture at least its size on screen)",
            info["plate"]["kind"] == "print"
            and info["plate"]["h"] >= 0.75 * sci["stand"]["h"]
            and info["plate"]["w"] >= need * 0.98,
            f"{info['plate']['kind']} {info['plate']['h']:.0f}px in a {sci['stand']['h']:.0f}px stand; picture {info['plate']['w']}w for {need:.0f}px",
        )
        check(
            f"{tag}: the scroll ends above the window's foot",
            info["paperBottom"] <= info["vh"],
            f"scroll foot {info['paperBottom']:.0f}, window {info['vh']}",
        )
        if (w, h) in ((1536, 900), (1101, 800), (1920, 1080)):
            stand = dict(sci["stand"], vw=info["vw"])
            weights, crisp = [], []
            for i in range(4):
                rest_on(page, "science", i)
                weights.append(weigh(Image.open(BytesIO(page.screenshot())).convert("RGB"), stand))
                plate = page.evaluate(SCIENCE)["plate"]
                crisp.append((plate["kind"], plate["w"], round(plate["css"] * info["dpr"])))
            page.screenshot(path=str(OUT / f"science-{w}x{h}-inkstone.png"))
            paintings = [x["mass"] for x in weights[1:]]
            mean = sum(paintings) / 3
            open_products(page)
            bottle = weigh(Image.open(BytesIO(page.screenshot())).convert("RGB"), stand)
            check(
                f"{tag}: the four pictures of one weight (paintings' ink within 25% of their mean; the print as tall as any painting and 75%+ of the bottle)",
                all(abs(m / mean - 1) <= 0.25 for m in paintings)
                and all(weights[0]["h"] >= x["h"] for x in weights[1:])
                and weights[0]["h"] >= 0.75 * bottle["h"],
                f"ink {[round(m / mean, 2) for m in paintings]} of the paintings' mean; heights "
                f"{dict(zip(PLATES, [x['h'] for x in weights]))}, bottle {bottle['h']}",
            )
            check(
                f"{tag}: every Science picture crisp (its picture at least its size on screen)",
                all(have >= need * 0.98 for _, have, need in crisp),
                crisp,
            )
        if (w, h) == (1536, 900):
            check(
                "science: every name is a link to its own part of the Science page",
                [n["href"] for n in names] == PART_HREFS,
                [n["href"] for n in names],
            )
            check(
                "science: Our scientists shown first (its name underlined); its link meets the scientists; Explore goes to the science",
                [n["shown"] for n in names] == [True, False, False, False]
                and any(
                    link["text"].startswith("Meet our scientists") and link["href"] == "/science#scientists"
                    for link in sci["links"]
                )
                and any(link["text"].startswith("Explore the science") and link["href"] == "/science" for link in sci["links"]),
                [(x["text"], x["href"]) for x in sci["links"]],
            )
        page.close()


def shown_part(page):
    info = page.evaluate(SCIENCE)
    link = next((x["text"] for x in info["science"]["links"] if not x["text"].startswith("Explore the science")), "")
    return info["plate"]["kind"], link


def science_reach(browser):
    """Round 5: every part is reachable directly. By keyboard: Enter opens Science, Tab steps
    through the four names in order, each showing its own picture and link, then Explore; a
    visible ring. By pointer: resting on a name shows its picture; passing over another name on
    the way to the picture's link keeps it; that link goes to its part. On a touch laptop: the
    first tap on a name opens its part."""
    page = browser.new_page(viewport={"width": 1536, "height": 900})
    watch(page)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(2000)
    page.mouse.move(760, 600)
    page.locator('[data-nav-trigger="science"]').focus()
    page.keyboard.press("Enter")
    page.wait_for_timeout(900)
    seen = []
    for _ in range(4):
        page.keyboard.press("Tab")
        page.wait_for_timeout(150)
        kind, link = shown_part(page)
        seen.append((focused(page)[:24], kind, link))
    page.keyboard.press("Tab")
    after = focused(page)
    check(
        "science: Enter opens it and Tab reaches every part's name in order, each showing its own picture and link",
        all(f.startswith(n) and k == pl and lk.startswith(t) for (f, k, lk), n, pl, t in zip(seen, PARTS, PLATES, PART_LINKS))
        and "Explore the science" in after,
        f"{seen}; then {after!r}",
    )
    page.keyboard.press("Shift+Tab")
    ring = page.evaluate(
        "(() => { const s = getComputedStyle(document.activeElement); return s.outlineStyle + ' ' + s.outlineWidth; })()"
    )
    check(
        "science: a visible ring on a name under the keyboard's focus",
        "Ask BiGH Science" in focused(page) and not ring.endswith(" 0px") and "none" not in ring,
        f"{focused(page)!r}: {ring}",
    )
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    open_science(page)
    rest_on(page, "science", 2, 800)
    kind, _ = shown_part(page)
    check("science: resting on a name shows its picture", kind == "reading", kind)
    nxt = page.locator('[data-nav-panel="science"] a[class*="nameLink"]').nth(3).locator('[class*="nameText"]').bounding_box()
    link = page.locator('[data-nav-panel="science"] a[class*="more"]', has_text="Explore the research").bounding_box()
    page.mouse.move(nxt["x"] + 30, nxt["y"] + nxt["height"] / 2, steps=2)
    page.mouse.move(link["x"] + 30, link["y"] + link["height"] / 2, steps=3)
    page.wait_for_timeout(700)
    kind, text = shown_part(page)
    check(
        "science: passing over another name on the way to the picture's link keeps the picture",
        kind == "reading" and text.startswith("Explore the research"),
        (kind, text),
    )
    page.mouse.click(link["x"] + 30, link["y"] + link["height"] / 2)
    page.wait_for_url("**/science#research", timeout=30000)
    check("science: the picture's link goes to its part", page.url.endswith("/science#research"), page.url)
    page.close()

    ctx = browser.new_context(viewport={"width": 1536, "height": 900}, has_touch=True)
    page = ctx.new_page()
    watch(page)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(2000)
    page.locator('[data-nav-trigger="science"]').tap()
    page.wait_for_timeout(1200)
    page.locator('[data-nav-panel="science"] a[class*="nameLink"]', has_text="Ask BiGH Science").tap()
    try:
        page.wait_for_url("**/science#ask", timeout=30000)
    except Exception:
        pass
    check("science: on a touch laptop the first tap on a name opens its part", page.url.endswith("/science#ask"), page.url)
    ctx.close()


# Every frame: which Science names carry their line, and each picture's opacity.
SCIENCE_LOG = """() => { const p = document.querySelector('[data-nav-panel="science"]');
  const names = [...p.querySelectorAll('[class*="nameText"]')], plates = [...p.querySelectorAll('[data-plate]')];
  window.__log = []; window.__logging = true;
  const tick = () => { window.__log.push({ t: performance.timeOrigin + performance.now(),
      lines: names.filter(n => (parseFloat(getComputedStyle(n, '::after').scale) || 0) > 0.04).map(n => n.textContent.trim()),
      o: Object.fromEntries(plates.map(x => [x.dataset.plate, +getComputedStyle(x).opacity])) });
    if (window.__logging) requestAnimationFrame(tick); };
  requestAnimationFrame(tick); }"""


def science_motion(browser):
    """Round 5, filmed at real speed. Moving down the four names (resting on each): the picture's
    place is never empty (its ink never under 60% of the lightest picture's at rest), only one name
    carries its line on every frame, and no painting shows its paper as a light box on any frame
    (frames while the print is drawn are left out: its mat is meant to be lighter than the paper).
    Then over to Products and back: Science swaps in on its painting with no light box behind it."""
    page = browser.new_page(viewport={"width": 1536, "height": 900})
    watch(page)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(2500)
    open_science(page)
    sel = '[data-nav-panel="science"]'
    stand = page.locator(f"{sel} [class*='stageStand']").bounding_box()
    crop = (round(stand["x"] - 50), round(stand["y"]), round(stand["x"] + stand["width"] + 50), round(stand["y"] + stand["height"]))
    beside = (crop[0] - 50, crop[1], crop[0] - 20, crop[3])

    def ink(img):
        a = luma(img.crop(crop))
        paper = float(np.median(luma(img.crop(beside))))
        return float(np.clip(paper - a - 6, 0, None).mean())

    rest = []
    for i in range(4):
        rest_on(page, "science", i)
        rest.append(ink(Image.open(BytesIO(page.screenshot()))))
    rest_on(page, "science", 0)
    pics = {}
    for i in range(1, 4):
        rest_on(page, "science", i, 700)
        for pic in page.evaluate(PICTURES, sel):
            pics[pic["name"].split("#")[0] + pic["file"]] = pic
    rest_on(page, "science", 0)
    gaps = page.evaluate(BESIDE, [sel, 90])
    film = Film(page)
    page.evaluate(SCIENCE_LOG)
    film.raw = []
    film.cdp.send("Page.startScreencast", {"format": "png", "everyNthFrame": 1})
    page.wait_for_timeout(150)
    for i in range(1, 4):
        rest_on(page, "science", i, 450)
    page.wait_for_timeout(700)
    film.cdp.send("Page.stopScreencast")
    page.evaluate("window.__logging = false")
    film.log = page.evaluate("window.__log")
    film.t0 = film.log[0]["t"]
    shares = [round(ink(img) / min(rest), 2) for _, _, img in film.frames()]
    check(
        "science: moving down the names, the picture's place is never empty (filmed: its ink never under 60% of the lightest picture's)",
        len(shares) >= 20 and min(shares) >= 0.6,
        f"least {min(shares, default=0)} over {len(shares)} frames; at rest {[round(r, 1) for r in rest]}",
    )
    two = [e["lines"] for e in film.log if len(e["lines"]) > 1]
    check(
        "science: only one name underlined on every frame (filmed)",
        len(film.log) >= 60 and not two and film.log[-1]["lines"] == ["Ask BiGH Science"],
        f"{len(film.log)} frames; two at once {two[:3]}; last {film.log[-1]['lines'] if film.log else None}",
    )
    # The light-box test frame by frame, only on frames where the print is not drawn.
    worst, counted = {}, {}
    for t, tw, img in film.frames():
        state = film.state(tw - 20)
        if state["o"].get("print", 0) > 0.02:
            continue
        a, k = luma(img), img.width / 1536
        for pic in pics.values():
            kind = next((v for k, v in PAINTED.items() if k in pic["file"]), None)
            if not kind or state["o"].get(kind, 0) < 0.05:
                continue
            vals = []
            for box in samples(pic):
                cy = (box[1] + box[3]) / 2
                refs = [(g - 3, cy - 4, g + 3, cy + 4) for g in gaps]
                vals.append(box_mean(a, box, k) - sum(box_mean(a, r, k) for r in refs) / len(refs))
            worst[kind] = max(worst.get(kind, -99), max(vals))
            counted[kind] = counted.get(kind, 0) + 1
    check(
        "science: no painting shows its paper as a light box while the pictures change (filmed: never 4+ levels over the paper)",
        set(worst) == {"cell", "reading", "inkstone"} and all(v <= 4 for v in worst.values()) and min(counted.values()) >= 6,
        {k: f"{v:+.1f} levels over {counted[k]} frames" for k, v in worst.items()},
    )

    # Over to Products and back: Science swaps in on the inkstone. The bottle stands where the
    # inkstone stands (one page layout), so during the dissolve its white label shows through the
    # new panel for a few frames, lighter than the paper: that is the bottle leaving, not a light
    # box. The bottles are hidden while the painting is measured (as for the showroom's pool).
    for arrive in ("products", "science"):
        box = page.locator(f'[data-nav-trigger="{arrive}"]').bounding_box()
        if arrive == "products":
            page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=4)
            page.wait_for_timeout(1200)
            continue
        hide = page.add_style_tag(content='[data-nav-panel="products"] [class*="__big"] { visibility: hidden !important; }')
        film.shoot(lambda: page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=4), 1300)
        hide.evaluate("el => el.remove()")
    page.screenshot(path=str(OUT / "science-swapped-back.png"))
    shown = [pic for pic in page.evaluate(PICTURES, sel)]
    flip = next((e["t"] for e in film.log if e["open"] == "science"), None)
    name = "science: swapping back in from Products on its painting (the inkstone), no light box behind it (filmed)"
    if flip is None or [p["file"].rsplit("/", 1)[-1] for p in shown] != ["inkstone-v2.webp"]:
        check(name, False, f"flip {flip}; shown {[p['file'] for p in shown]}")
    else:
        found = light_boxes(film, shown, gaps, lambda e: 10000, 1536, round(flip - film.t0), round(flip - film.t0) + 900)
        no_light_box(name, found)
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
            ring = page.evaluate(
                "(() => { const s = getComputedStyle(document.activeElement); "
                "return s.outlineStyle + ' ' + s.outlineWidth; })()"
            )
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
           "scrollTop": m["scrollTop"]})


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
        page.wait_for_timeout(1400)
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


with sync_playwright() as p:
    browser = p.chromium.launch(args=["--use-angle=d3d11"])
    if ONLY in (None, "desk"):
        desktop(browser)
        rule_checks(browser)
        reading_stroke(browser)
        drop_down_motion(browser)
    if ONLY in (None, "desk", "showroom"):
        showroom_layout(browser)
        showroom_reach(browser)
        showroom_motion(browser)
    if ONLY in (None, "desk", "science"):
        science_layout(browser)
        science_reach(browser)
        science_motion(browser)
    if ONLY in (None, "phone"):
        phone(browser)
        phone_rows(browser)
        menu_light_boxes(browser)
    if ONLY in (None, "tablet"):
        tablet(browser)
        tablet_rows(browser)
    if ONLY in (None, "lang"):
        languages(browser, p)
    browser.close()

check("no page errors or console errors", not errors, errors[:5])
fails = [name for name, ok in results if not ok]
print(f"\n{len(results) - len(fails)}/{len(results)} checks passed. Pictures: {OUT}")
sys.exit(1 if fails else 0)

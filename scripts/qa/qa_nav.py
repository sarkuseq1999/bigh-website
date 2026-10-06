"""QA for the menu bar, "Inscription" (Mo's pick, October 5, 2026), on the homepage.

usage: python -X utf8 scripts/qa/qa_nav.py [base] [--only=desk|phone|tablet|lang]
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
  - reduced motion: the scroll is down at once.
  - phone 390x844: the menu opens and locks the page, the button says Close, Escape closes it and
    hands focus back, the Close button closes it, Products and Science fold open one at a time,
    Support opens its sheet, a product link goes to its page.
  - tablet 834x1112: the menu opens with Products unfolded.
  - Vietnamese and Japanese at 1101 and 1280 px: the bar's three groups stay apart and inside the
    window.
  - filmed at real speed (round 2; every frame the compositor draws, plus the bar's state on every
    frame the page draws): Science opening (from the tall bar and from the scrolled bar) and
    Products opening show no light box behind a painting or a pool: no sample of a multiplied
    picture is more than 4 levels lighter than the paper beside it, on any frame (two frames
    running) once the scroll has reached it. Moving from one drop-down to the other (both ways):
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
    return s.mixBlendMode === 'multiply' && s.display !== 'none' && img.getBoundingClientRect().width > 4;
  }).map((img, i) => {
    const kind = /pool/.test(img.className) ? 'pool' : /contact/.test(img.className) ? 'contact' : 'painting';
    return { name: (img.dataset.painting || kind) + '#' + i, kind, ...drawn(img) };
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
    for t, tw, img in film.frames():
        if not lo - 40 <= t <= hi:
            continue
        a, k = luma(img), img.width / width
        edge = reveal(film.state(tw - 60))
        for pic in pics:
            best = None
            for box in samples(pic):
                if box[3] > edge - 10 or box[0] < 0 or box[2] > width:
                    continue
                cy = (box[1] + box[3]) / 2
                refs = [(g - 3, cy - 4, g + 3, cy + 4) for g in gaps if 0 < g < width]
                if refs:
                    d = box_mean(a, box, k) - sum(box_mean(a, r, k) for r in refs) / len(refs)
                    best = d if best is None else max(best, d)
            series[pic["name"]].append((t, best))
    out = {}
    for name, s in series.items():
        held = [min(u, v) for (tu, u), (_, v) in zip(s, s[1:]) if u is not None and v is not None and tu >= lo]
        out[name] = (round(max(held), 1) if held else None, sum(1 for t, v in s if v is not None and t >= lo))
    return out


def no_light_box(name, found, frames=6):
    check(
        name,
        found and all(v is not None and v <= 4 and n >= frames for v, n in found.values()),
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
            film.shoot(lambda: page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2), 1500)
            sel = f'[data-nav-panel="{panel}"]'
            top, height = page.evaluate(
                f"(() => {{ const r = document.querySelector('{sel}').getBoundingClientRect(); return [r.top, r.height]; }})()"
            )
            found = light_boxes(
                film,
                page.evaluate(PICTURES, sel),
                page.evaluate(GAPS, f"{sel} li"),
                lambda e: top + e["r"] * height - deckle,
                1536,
                250,
                1500,
            )
            what = "behind its paintings" if panel == "science" else "around the bottles' pools"
            no_light_box(f"{tag}: {panel.capitalize()} opens with no light box {what} (filmed at real speed)", found)
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
        """() => { const top = document.querySelector('[data-nav-panel] h2').getBoundingClientRect().top;
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
    # The row runs off the right edge (a swipe away): the pools in the window are measured.
    found = light_boxes(
        film,
        [p for p in page.evaluate(PICTURES, "#nav-sheet-products") if p["x"] + 6 < 390],
        page.evaluate(GAPS, "#nav-sheet-products li"),
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


def languages(browser):
    for locale in ("vn", "jp"):
        for width in (1101, 1280):
            page = browser.new_page(viewport={"width": width, "height": 800})
            watch(page)
            page.goto(f"{BASE}/{locale}", wait_until="networkidle")
            page.wait_for_timeout(2200)
            page.screenshot(path=str(OUT / f"{locale}-{width}.png"), clip={"x": 0, "y": 0, "width": width, "height": 120})
            fit = page.evaluate(
                """() => {
              const nav = document.querySelector('#site-navigation');
              const box = el => el.getBoundingClientRect();
              const left = box(nav.firstElementChild), mark = box(nav.querySelector('[data-nav-logo]'));
              const right = box(nav.lastElementChild);
              const shown = [...nav.querySelectorAll('a, button, select')].filter(el => {
                const r = box(el); return r.width > 0 && !el.closest('[data-nav-panel], [data-nav-sheet]');
              });
              const out = shown.filter(el => { const r = box(el); return r.left < 0 || r.right > innerWidth; })
                .map(el => el.innerText.trim());
              return { gapLeft: Math.round(mark.left - left.right), gapRight: Math.round(right.left - mark.right), out };
            }"""
            )
            check(
                f"{locale} {width}: the bar's three groups stay apart and inside the window",
                fit["gapLeft"] >= 16 and fit["gapRight"] >= 16 and not fit["out"],
                fit,
            )
            page.close()


with sync_playwright() as p:
    browser = p.chromium.launch(args=["--use-angle=d3d11"])
    if ONLY in (None, "desk"):
        desktop(browser)
        rule_checks(browser)
        drop_down_motion(browser)
    if ONLY in (None, "phone"):
        phone(browser)
    if ONLY in (None, "tablet"):
        tablet(browser)
    if ONLY in (None, "lang"):
        languages(browser)
    browser.close()

check("no page errors or console errors", not errors, errors[:5])
fails = [name for name, ok in results if not ok]
print(f"\n{len(results) - len(fails)}/{len(results)} checks passed. Pictures: {OUT}")
sys.exit(1 if fails else 0)

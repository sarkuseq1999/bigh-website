"""QA for the About page (/about: "Glass", opening 3, Switzer; Mo's picks, Sept 28, 2026), at desktop
(1440x900) and phone (390x844), plus the opening at six sizes.

At each size: no page or console errors or warnings and no failed requests; every locked line on the page (the
title is the h1's aria-label), never "CellGen"; one h1; the four part anchors; no review controls left; no
sideways scrolling; every image has an alt; tap targets in the page at least 44 px; body text at least 17 px,
small labels and captions at least 17 px; the Ask BiGH Science and Support panels open and close.

The system, measured: Switzer is loaded (document.fonts.check) and is the first family of the h1, the headings,
labels, numbers and body copy; no lime or cobalt anywhere; every text color passes WCAG AA on the paper, also on
the warm paper at the close; on desktop every chapter's left edge meets the header logo's, the right column
starts at the same grid line in every chapter, and the spec list sits in the grid's last three columns.

The opening, at 1280x720, 1440x900, 1575x940, 1920x1080, 768x1024 and 390x844: the glass is placed, never touches
a letter of the title or the other opening words, sits in the first screen, and its caption is 16-17 px.

The signature moment, measured: the glass battery is drawn by WebGL (canvas shown, still hidden); it rises from
the opening into its dock, large there; its charge (the shader's fill uniform, mirrored in data-charge) climbs
chapter by chapter to full; the render's own pixels turn more golden as it charges; each chapter's number joins
the spec list as the chapter slides away (desktop); the promise bars fill with honey; each chapter heading rises
into place line by line; chapters take turns (sampled every 40 px, never two chapters' words at once); the paper
warms and the glow grows with the charge; the loop rests when the visitor stops and sleeps offscreen; the pinned
battery stops above the footer. A reduced-motion run shows the still render, every bar full and the list
complete; a no-WebGL run keeps the still render.

Other languages (kr, jp, cns, vn). The catalogs, read from the files: every string the About page shows or reads
out has a key, the five catalogs have the same keys, and their {placeholders} match. Then per language: /xx/about
answers 200 with no console errors or warnings; the h1 is the English "Be in Good Health." with its unfold and
lang="en"; the tab title is translated; none of the page's English source sentences is left in the visible text,
the dialogs, the aria-labels or the alt texts (allowed: the English h1 and names kept in Latin letters); and no
heading, label or paragraph line is a lone character or starts with closing punctuation (1575x940 and 390x844).
In Japanese and Vietnamese, the glass after "Health." never touches a letter. In Vietnamese, Chrome's DevTools
font report shows every Vietnamese text drawn in Be Vietnam Pro only and the English h1 in Switzer only. Review shots of every chapter, the footer and the
Ask panel: scripts/qa/out/about-i18n/<lang>-<desk|phone>-N-<part>.png.

Pictures: scripts/qa/out/about-<size>-NN.png, viewport shots while scrolling (never full-page: svh layouts).
Chromium runs on the real GPU (ANGLE/D3D11); pass --swiftshader to use the software renderer instead.

Usage: python -X utf8 scripts/qa/qa_about.py [base-url] [--swiftshader]
"""

import io
import json
import os
import re
import sys

import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = ARGS[0] if ARGS else "http://localhost:3009"
URL = f"{BASE}/about"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
OUT_I18N = os.path.join(OUT, "about-i18n")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.makedirs(OUT_I18N, exist_ok=True)
results = []

LOCKED = [
    "About BiGH",
    "Be in Good Health.",
    "What our name stands for. What our work is for.",
    "Our purpose",
    "A full life has many parts.",
    "We focus on one you can’t see: your cells.",
    "Our mission is to support cellular health and mental energy, helping people live life to the fullest.",
    "Our scientific roots",
    "Our key formulas begin with scientists.",
    "Dr. Jiankang Liu, our Chief Scientific Advisor, studies mitochondria and aging. He formulated NuriCell, and with Dr. Iris Wang, he developed Nature Calm.",
    "280+",
    "scientific papers by Dr. Liu",
    "Meet our scientists",
    "Our experience",
    "Our flagship formula is older than BiGH.",
    "2016",
    "BiGH founded in California",
    "20+ years",
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
    "Illustration",
]
SIZES = ((1440, 900, "desk"), (390, 844, "phone"))
REVEAL = """() => { const h = document.querySelector('#experience h2'); const l = h.querySelector('div > div');
    return [h.dataset.split ?? null, h.dataset.revealed ?? null, l ? getComputedStyle(l).transform : null]; }"""
LAUNCH = (
    ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"]
    if "--swiftshader" in sys.argv
    else ["--use-gl=angle", "--use-angle=d3d11", "--enable-gpu", "--ignore-gpu-blocklist"]
)
ROOT = "document.querySelector('[data-motion]')"
LIME, COBALT = "rgb(226, 237, 148)", "rgb(33, 73, 163)"
CONTRAST = """() => {
            const ctx = document.createElement('canvas').getContext('2d', { willReadFrequently: true });
            const rgb = c => { ctx.clearRect(0, 0, 1, 1); ctx.fillStyle = '#000'; ctx.fillStyle = c; ctx.fillRect(0, 0, 1, 1); return [...ctx.getImageData(0, 0, 1, 1).data].slice(0, 3); };
            const lum = c => { const [r, g, b] = rgb(c).map(v => v / 255)
                .map(v => v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
            const paper = lum(getComputedStyle(document.querySelector('[data-motion]')).backgroundColor);
            const worst = {};
            for (const e of document.querySelector('[data-motion]').querySelectorAll('p, span, h1, h2, h3, a, li, button')) {
              if (!e.offsetParent || e.closest('nav') || e.closest('button, [class*=primary]')) continue;
              if (![...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) continue;
              const c = getComputedStyle(e).color; const a = (c.match(/[\\d.]+/g)[3] ?? 1) * 1;
              if (a < 1) continue;
              const l = lum(c); const r = (Math.max(l, paper) + 0.05) / (Math.min(l, paper) + 0.05);
              const size = parseFloat(getComputedStyle(e).fontSize);
              const need = size >= 24 ? 3 : 4.5;
              if (r < need) worst[e.textContent.trim().slice(0, 24)] = r.toFixed(2);
            }
            return worst; }"""

# The look's paper as sRGB bytes (its computed color may be oklab, from color-mix).
PAPER = """() => { const ctx = document.createElement('canvas').getContext('2d');
  ctx.fillStyle = getComputedStyle(document.querySelector('[data-motion]')).backgroundColor; ctx.fillRect(0, 0, 1, 1);
  return [...ctx.getImageData(0, 0, 1, 1).data].slice(0, 3); }"""

# Which chapters have words in the window right now (after the choreography has drawn this scroll position).
VISIBLE = """async (y) => {
  window.scrollTo(0, y);
  await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
  await new Promise(r => requestAnimationFrame(r));
  const root = document.querySelector('[data-motion]');
  const mark = root.querySelector('[data-band]');
  const cap = root.querySelector('[class*=cap]');
  const header = document.querySelector('header').getBoundingClientRect().bottom;
  const capOn = cap && mark.offsetParent && parseFloat(getComputedStyle(cap).opacity) > 0.9;
  const visTop = capOn ? mark.getBoundingClientRect().top : header;
  const out = [];
  for (const c of root.querySelectorAll('[data-chapter]')) {
    const f = c.querySelector('[data-frame]') || c.querySelector('[data-fade]') || c;
    const op = parseFloat(getComputedStyle(f).opacity);
    if (op <= 0.02) continue;
    const texts = [...c.querySelectorAll('p, h1, h2, h3, span, a, button, li')]
      .filter(e => [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()));
    if (texts.some(e => { const r = e.getBoundingClientRect(); return r.height > 0 && r.bottom > visTop + 2 && r.top < innerHeight - 2; }))
      out.push(c.dataset.chapter + ':' + op.toFixed(2));
  }
  return out;
}"""



def check(name, ok, detail=""):
    results.append(ok)
    print(("PASS " if ok else "FAIL ") + name + ("  [" + detail + "]" if detail else ""))


def watch(page):
    problems = []
    page.on("pageerror", lambda e: problems.append("pageerror " + str(e)[:160]))
    page.on(
        "console",
        lambda m: problems.append(f"console.{m.type} " + m.text[:160]) if m.type in ("error", "warning") else None,
    )
    page.on("requestfailed", lambda r: problems.append("requestfailed " + r.url[-80:]))
    page.on("response", lambda r: problems.append(f"http {r.status} " + r.url[-80:]) if r.status >= 400 else None)
    return problems


def open_page(browser, w, h, reduced=False, url=URL):
    page = browser.new_page(viewport={"width": w, "height": h}, reduced_motion="reduce" if reduced else "no-preference")
    problems = watch(page)
    page.goto(url, wait_until="networkidle")
    page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
    page.wait_for_timeout(1800)
    return page, problems


# Where a chapter is read: desktop, the middle of its hold under the battery; phone, its frame's top at the band.
READING = """(sel) => {
  const root = document.querySelector('[data-motion]');
  const band = root.querySelector('[data-band]').offsetTop;
  const s = document.querySelector(sel);
  const f = s.querySelector('[data-frame]');
  const top = s.getBoundingClientRect().top + scrollY;
  const hold = getComputedStyle(f).position === 'sticky' ? s.offsetHeight - f.offsetHeight : 0;
  return top - band + hold / 2;
}"""


def scroll_to_chapter(page, selector, settle=2600):
    """Walk to the chapter's reading position (in steps, as a reader would), then let the scene settle."""
    target = page.evaluate(READING, selector)
    here = page.evaluate("scrollY")
    for i in range(1, 7):
        page.evaluate(f"window.scrollTo(0, {here + (target - here) * i / 6})")
        page.wait_for_timeout(90)
    page.wait_for_timeout(settle)


def shoot_scroll(page, name):
    """Viewport shots from top to bottom of the look (the footer is not ours)."""
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(900)
    end = page.evaluate(f"{ROOT}.getBoundingClientRect().bottom + scrollY")
    view = page.evaluate("innerHeight")
    last = int(end - view)
    for old in os.listdir(OUT):
        if re.fullmatch(re.escape(name) + r"-\d\d\.png", old):
            os.remove(os.path.join(OUT, old))
    y, i = 0, 0
    while True:
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(1500)
        page.screenshot(path=os.path.join(OUT, f"{name}-{i:02d}.png"))
        i += 1
        if y >= last or i >= 30:
            break
        y = min(y + int(view * 0.5), last)
    return i


def page_checks(page, tag):
    main_text = re.sub(r"\s+", " ", page.evaluate("document.querySelector('main').innerText"))
    main_text += " " + (page.evaluate("document.querySelector('main h1')?.getAttribute('aria-label')") or "")
    missing = [words for words in LOCKED if words not in main_text]
    check(f"{tag}: every locked line is on the page", not missing, f"missing={missing}")
    check(f"{tag}: never names CellGen", "cellgen" not in main_text.lower())
    h1 = page.locator("h1").count()
    anchors = page.evaluate("['purpose','roots','experience','promise'].filter(id => !document.getElementById(id))")
    check(f"{tag}: one h1 and the four part anchors", h1 == 1 and not anchors, f"h1={h1} missingAnchors={anchors}")
    review = page.evaluate(
        """() => [...document.querySelectorAll('nav')].map(n => n.getAttribute('aria-label') || '')
            .filter(l => /design options|type|opening/i.test(l))"""
    )
    check(f"{tag}: no review controls left (look, type or opening pickers)", not review, f"{review}")
    overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    check(f"{tag}: no sideways scrolling", overflow == 0, f"overflow={overflow}")
    no_alt = page.evaluate("[...document.images].filter(i => !i.hasAttribute('alt')).map(i => i.src.slice(-40))")
    check(f"{tag}: every image has an alt", not no_alt, f"{no_alt}")
    small = page.evaluate(
        """() => [...document.querySelectorAll('main a, main button')]
            .map(e => [e.textContent.trim().slice(0, 30), e.getBoundingClientRect()])
            .filter(([, r]) => r.width > 0 && (r.height < 44 || r.width < 44))
            .map(([t, r]) => `${t}:${Math.round(r.width)}x${Math.round(r.height)}`)"""
    )
    check(f"{tag}: tap targets in the page are at least 44 px", not small, f"{small}")
    tiny = page.evaluate(
        """() => [...document.querySelectorAll('main p, main li, main h3, main span')]
            .filter(e => e.offsetParent && e.textContent.trim() && getComputedStyle(e).visibility !== 'hidden'
                && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())
                && parseFloat(getComputedStyle(e).fontSize) < 16)
            .map(e => e.textContent.trim().slice(0, 30) + ':' + getComputedStyle(e).fontSize)"""
    )
    check(f"{tag}: no text under 16 px (labels) ", not tiny, f"{tiny[:4]}")
    body_small = page.evaluate(
        """() => [...document.querySelectorAll('main p, main li, main h3')]
            .filter(e => e.offsetParent && !e.closest('[aria-hidden=true]') && parseFloat(getComputedStyle(e).fontSize) < 17)
            .map(e => e.textContent.trim().slice(0, 30) + ':' + getComputedStyle(e).fontSize)"""
    )
    check(f"{tag}: body text at least 17 px", not body_small, f"{body_small[:4]}")


def system_checks(page, tag):
    """The type, color and grid system, read from the rendered page."""
    fams = page.evaluate(
        f"""async () => {{ await document.fonts.ready; const root = {ROOT}; const f = s => getComputedStyle(root.querySelector(s)).fontFamily;
            return {{ h1: f('h1'), h2: f('#roots h2'), label: f('#roots p'), number: f('#experience [data-source] span'),
                     body: f('#roots [class*=body]'), item: f('[data-pill] p'), lead: f('[class*=lead]'),
                     header: getComputedStyle(document.querySelector('header nav a')).fontFamily,
                     footer: getComputedStyle(document.querySelector('footer p')).fontFamily,
                     check: document.fonts.check('16px Switzer') }}; }}"""
    )
    first = {k: v.split(",")[0].strip().strip('"') for k, v in fams.items() if k != "check"}
    everywhere = all(v == "Switzer" for v in first.values())
    check(
        f"{tag}: Switzer is loaded and is the first family of the h1, headings, labels, numbers, body copy, header and footer",
        everywhere and fams["check"] is True,
        f"first={first} fonts.check={fams['check']}",
    )

    colors = page.evaluate(
        f"""() => {{ const out = new Set();
            for (const e of {ROOT}.querySelectorAll('*')) {{ const s = getComputedStyle(e);
              [s.color, s.backgroundColor, s.borderTopColor, s.outlineColor].forEach(c => out.add(c)); }}
            return [...out]; }}"""
    )
    bad = [c for c in colors if c in (LIME, COBALT)]
    check(f"{tag}: no lime or cobalt in the look (one accent: honey)", not bad, f"{bad}")

    contrast = page.evaluate(CONTRAST)
    check(f"{tag}: every text color passes WCAG AA on the paper", not contrast, f"{contrast}")

    if tag.startswith("desk"):
        grid = page.evaluate(
            f"""() => {{ const x = e => Math.round(e.getBoundingClientRect().left);
                const logo = x(document.querySelector('header a'));
                const heads = ['#purpose','#roots','#experience','#promise','[data-chapter=closing]']
                    .map(s => x(document.querySelector(s + ' h2')));
                const rights = ['#roots [class*=side]','#experience [class*=numbers]','#promise [class*=promises]','[data-chapter=closing] [class*=side]']
                    .map(s => x(document.querySelector(s)));
                const facts = x({ROOT}.querySelector('[class*=stage] ol'));
                const grid = {ROOT}.querySelector('#roots [class*=grid]'); const cs = getComputedStyle(grid);
                const inner = grid.getBoundingClientRect().left + parseFloat(cs.paddingLeft);
                const col = (grid.clientWidth - parseFloat(cs.paddingLeft) * 2 - 11 * parseFloat(cs.columnGap)) / 12;
                const line = n => Math.round(inner + (n - 1) * (col + parseFloat(cs.columnGap)));
                return {{ logo, heads, rights, facts, col7: line(7), col10: line(10) }}; }}"""
        )
        aligned = all(abs(h - grid["logo"]) <= 1 for h in grid["heads"]) and all(abs(r - grid["col7"]) <= 1 for r in grid["rights"])
        check(f"{tag}: chapters sit on the 12-column grid (left edges meet the logo; right column on line 7)", aligned, f"{grid}")
        check(f"{tag}: the spec list sits in the grid's last three columns", abs(grid["facts"] - grid["col10"]) <= 1, f"list x={grid['facts']} col10={grid['col10']}")


def handoff_check(page, tag):
    """Every 40 px of scroll through the whole look: never two chapters' words in the window at once
    (the opening counts as a chapter). Words under the battery's paper do not count as seen."""
    end = int(page.evaluate(f"{ROOT}.getBoundingClientRect().bottom + scrollY - innerHeight"))
    worst, bad, samples = 0, [], 0
    for y in range(0, end + 1, 40):
        seen = page.evaluate(VISIBLE, y)
        samples += 1
        worst = max(worst, len(seen))
        if len(seen) > 1:
            bad.append((y, seen))
    check(
        f"{tag}: chapters take turns (never two chapters' words at once; {samples} samples every 40 px)",
        worst <= 1,
        f"max at once={worst} first clashes={bad[:3]}",
    )


def light_checks(page, tag):
    """The page fills with light: at the close the paper has warmed toward honey and the glow
    behind the glass is on, while every text color still passes AA on the warmer paper."""
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(1500)
    cold = page.evaluate(PAPER)
    scroll_to_chapter(page, "[data-chapter=closing]")
    warm = page.evaluate(PAPER)
    glow = float(page.evaluate(f"getComputedStyle({ROOT}.querySelector('[class*=glow]')).opacity"))

    a, b = cold, warm
    warmer = (b[0] - b[2]) > (a[0] - a[2]) + 8
    check(f"{tag}: the paper warms and the glow grows with the charge", warmer and glow > 0.8, f"paper {cold} -> {warm}; glow={glow:.2f}")
    worst = page.evaluate(CONTRAST)
    check(f"{tag}: every text color still passes WCAG AA on the warm paper at the close", not worst, f"{worst}")


# The glass's visible box and the ink box of every word in the opening (the letters themselves:
# baseline minus the text's ascent to baseline plus its descent, not the line box).
OPENING = """() => {
  const root = document.querySelector('[data-motion]');
  const b = root.querySelector('[class*=battery]').getBoundingClientRect();
  const glass = { l: b.left + b.width * 0.194, r: b.left + b.width * 0.807, t: b.top + b.height * 0.228, b: b.top + b.height * 0.73 };
  const ctx = document.createElement('canvas').getContext('2d');
  const h1 = root.querySelector('h1');
  const boxes = [];
  const walker = document.createTreeWalker(root.querySelector('[class*=hero]'), NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const n = walker.currentNode; const text = n.textContent.trim(); if (!text) continue;
    const st = getComputedStyle(n.parentElement); ctx.font = `${st.fontWeight} ${st.fontSize} ${st.fontFamily}`;
    const m = ctx.measureText(text); const range = document.createRange(); range.selectNodeContents(n);
    for (const r of range.getClientRects()) if (r.width > 1 && r.height > 1) {
      const base = r.top + m.fontBoundingBoxAscent;
      boxes.push({ text: text.slice(0, 16), title: h1.contains(n), l: r.left, r: r.right, t: base - m.actualBoundingBoxAscent, b: base + m.actualBoundingBoxDescent });
    }
  }
  const hit = x => x.l < glass.r && x.r > glass.l && x.t < glass.b && x.b > glass.t;
  const cap = root.querySelector('[class*=illustration]').getBoundingClientRect();
  return { placed: root.dataset.placed, titleHits: boxes.filter(x => x.title && hit(x)).map(x => x.text),
           otherHits: boxes.filter(x => !x.title && hit(x)).map(x => x.text), words: boxes.length,
           inView: glass.l >= -2 && glass.r <= innerWidth + 2 && glass.t >= 70 && glass.b <= innerHeight,
           caption: Math.round(cap.height / 1.3 * 10) / 10,
           glass: [Math.round(glass.l), Math.round(glass.t), Math.round(glass.r - glass.l)] };
}"""
HERO_SIZES = ((1280, 720), (1440, 900), (1575, 940), (1920, 1080), (768, 1024), (390, 844))


def opening_checks(browser):
    """The opening at the six review sizes: placed, the glass never over a letter of the title nor any
    other opening words, inside the first screen, and its caption 16-17 px whatever the battery's scale."""
    bad, seen = [], []
    for w, h in HERO_SIZES:
        page, problems = open_page(browser, w, h)
        page.wait_for_timeout(1400)
        geo = page.evaluate(OPENING)
        seen.append(f"{w}x{h}: glass {geo['glass']}")
        ok = (
            geo["placed"] == "true"
            and not geo["titleHits"]
            and not geo["otherHits"]
            and geo["inView"]
            and 16 <= geo["caption"] <= 17.5
            and geo["words"] >= 5
            and not problems
        )
        if not ok:
            bad.append((f"{w}x{h}", geo, problems[:2]))
        page.close()
    check(
        "opening: at all six sizes the glass never touches a letter of the title or the other opening words, sits in the first screen, caption 16-17 px",
        not bad,
        f"{bad[:2] if bad else seen}",
    )


def readability_checks(page, tag):
    """Older readers: the spec list's labels, the captions, the kicker and every small label are at
    least 17 px; the list's values are large."""
    sizes = page.evaluate(
        f"""() => {{ const root = {ROOT}; const px = s => [...root.querySelectorAll(s)].map(e => parseFloat(getComputedStyle(e).fontSize));
            return {{ factLabel: px('[class*=factLabel]'), factValue: px('[class*=factValue]'), caption: px('[class*=illustration]'),
                     kicker: px('[class*=kicker]'), label: px('[class*=__label]'), statLabel: px('[class*=statLabel], [class*=numberLabel]') }}; }}"""
    )
    small = {k: min(v) for k, v in sizes.items() if v and k != "factValue" and min(v) < 17}
    big = min(sizes["factValue"]) >= (30 if tag.startswith("phone") else 34)
    check(f"{tag}: small text is at least 17 px and the list's values are large", not small and big, f"{ {k: min(v) for k, v in sizes.items() if v} }")


def glass_color(page):
    """Mean warmth (R - B) of the glass body in a viewport screenshot."""
    box = page.evaluate(
        """() => { const r = document.querySelector('[class*=battery]').getBoundingClientRect();
            return {x: r.left + r.width * 0.25, y: r.top + r.height * 0.3, w: r.width * 0.5, h: r.height * 0.36}; }"""
    )
    shot = Image.open(io.BytesIO(page.screenshot())).convert("RGB")
    ratio = shot.width / page.evaluate("innerWidth")
    crop = shot.crop(
        (
            max(0, int(box["x"] * ratio)),
            max(0, int(box["y"] * ratio)),
            min(shot.width, int((box["x"] + box["w"]) * ratio)),
            min(shot.height, int((box["y"] + box["h"]) * ratio)),
        )
    )
    pixels = np.asarray(crop).astype(float)
    return round(float((pixels[..., 0] - pixels[..., 2]).mean()), 1)


def gold_center(page):
    """Horizontal center (px) of the glass's gold pixels in a viewport screenshot."""
    box = page.evaluate("(() => { const r = document.querySelector('[class*=battery]').getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; })()")
    shot = np.asarray(Image.open(io.BytesIO(page.screenshot())).convert("RGB")).astype(float)
    x, y, w, h = (int(v) for v in box)
    area = shot[max(0, y) : y + h, max(0, x) : x + w]
    warm = (area[..., 0] - area[..., 2]) > 70
    cols = np.nonzero(warm)[1]
    return float(cols.mean()) if cols.size else 0.0


def signature_checks(page, tag, before):
    info = page.evaluate(
        f"""() => {{ const root = {ROOT}; const canvas = root.querySelector('canvas');
            const still = root.querySelector('[class*=still]');
            return {{ ready: root.dataset.ready, renderer: root.dataset.renderer,
                     canvas: canvas ? getComputedStyle(canvas).opacity : null,
                     still: still ? getComputedStyle(still).opacity : null }}; }}"""
    )
    check(
        f"{tag}: the glass battery is drawn live by WebGL (canvas shown, still hidden)",
        info["ready"] == "true" and info["canvas"] == "1" and info["still"] == "0",
        f"{info}",
    )

    # It opens where the opening puts it and rises into its dock, large there.
    width = "(() => { const r = document.querySelector('[class*=battery]').getBoundingClientRect(); return [r.top, r.width]; })()"
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(1800)
    low, open_w = page.evaluate(width)
    scroll_to_chapter(page, "#purpose")
    rest, dock_w = page.evaluate(width)
    view_w = page.evaluate("innerWidth")
    glass_open, glass_dock = open_w * 0.61 / view_w, dock_w * 0.61 / view_w
    big = glass_dock >= (0.4 if tag == "desk" else 0.8)
    check(
        f"{tag}: the battery rises from the opening into its dock, large there",
        low - rest > 80 and big,
        f"top {low:.0f} -> {rest:.0f}; glass width {glass_open:.0%} -> {glass_dock:.0%} of the window",
    )

    # It charges chapter by chapter; the glass's own pixels turn more golden.
    charges, warmth = [], []
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(2600)
    charges.append(float(page.evaluate(f"{ROOT}.dataset.charge") or 0))
    warmth.append(glass_color(page))
    for selector in ("#purpose", "#roots", "#experience", "#promise", "[data-chapter=closing]"):
        scroll_to_chapter(page, selector)
        charges.append(float(page.evaluate(f"{ROOT}.dataset.charge") or 0))
        warmth.append(glass_color(page))
    rising = all(b > a + 0.08 for a, b in zip(charges, charges[1:]))
    check(f"{tag}: the charge climbs chapter by chapter to full", rising and charges[-1] > 0.97, f"charge={charges}")
    check(
        f"{tag}: the render's own pixels turn more golden as it charges",
        warmth[-1] > warmth[1] + 8 and warmth[-1] > warmth[0] + 12,
        f"warmth (R-B) by chapter={warmth}",
    )

    after = page.evaluate(REVEAL)[1:]
    hidden = before[0] == "true" and before[1] is None and before[2] not in (None, "none", "matrix(1, 0, 0, 1, 0, 0)")
    shown = after[0] == "true" and after[1] in ("none", "matrix(1, 0, 0, 1, 0, 0)")
    hidden_parts = page.evaluate("document.querySelectorAll('main h2 [aria-hidden], main h2 [aria-label]').length")
    check(f"{tag}: split headings still read as plain text (nothing hidden or relabelled inside an h2)", hidden_parts == 0, f"{hidden_parts}")
    check(f"{tag}: headings rise into place line by line (masked on load, in place after)", hidden and shown, f"before={before} after={after}")

    if tag == "desk":
        # The pointer tilts the glass: its nearer parts shift over the depth map.
        scroll_to_chapter(page, "#experience")
        page.mouse.move(20, 450)
        page.wait_for_timeout(2200)
        left = gold_center(page)
        page.mouse.move(1420, 450)
        page.wait_for_timeout(2200)
        right = gold_center(page)
        check(f"{tag}: the pointer tilts the glass (gold shifts over the depth map)", abs(left - right) > 3, f"gold center x: pointer left={left:.1f} right={right:.1f}")

        docked = []
        for selector in ("#roots", "#experience", "#promise", "[data-chapter=closing]"):
            scroll_to_chapter(page, selector)
            docked.append(page.evaluate(f"{ROOT}.querySelectorAll('[class*=stage] [data-fact][data-docked=true]').length"))
        shown_fact = page.evaluate(f"getComputedStyle({ROOT}.querySelector('[class*=stage] [data-fact] span')).opacity")
        check(
            f"{tag}: each chapter's number joins the spec list as it slides away (0, 1, 3, 4)",
            docked == [0, 1, 3, 4] and shown_fact == "1",
            f"docked={docked} opacity={shown_fact}",
        )

    # The promise bars fill with honey as the promise holds (desktop) or as each arrives (phone).
    page.evaluate("document.querySelector('[data-pill]').scrollIntoView({block: 'end'})")
    page.evaluate("window.scrollBy(0, innerHeight * 0.02)")
    page.wait_for_timeout(700)
    before = page.evaluate("[...document.querySelectorAll('[data-pill]')].map(p => p.style.getPropertyValue('--fill'))")
    scroll_to_chapter(page, "[data-chapter=closing]")
    after = page.evaluate("[...document.querySelectorAll('[data-pill]')].map(p => [p.style.getPropertyValue('--fill'), p.dataset.done])")
    honey = page.evaluate("getComputedStyle(document.querySelector('[data-pill] [class*=bar]'), '::after').backgroundColor")
    check(
        f"{tag}: the promise bars fill with the battery's honey",
        float(before[-1] or 0) < 0.5 and all(f == "1.000" and d == "true" for f, d in after) and honey == "rgb(184, 128, 31)",
        f"before={before} after={after} color={honey}",
    )

    if tag == "phone":
        recap = page.evaluate(
            f"""() => [...{ROOT}.querySelectorAll('[class*=recap] [data-fact]')]
                .map(f => f.dataset.docked === 'true' && getComputedStyle(f.querySelector('span')).opacity === '1')"""
        )
        clear = page.evaluate(
            f"""() => {{ const band = {ROOT}.querySelector('[data-band]').offsetTop;
                const r = {ROOT}.querySelector('[class*=recap]').getBoundingClientRect();
                return Math.round(r.top - band); }}"""
        )
        check(f"{tag}: the spec list is complete under the full battery at the close, clear of it", recap == [True] * 4 and clear >= 0, f"{recap} recapTop-band={clear}")

    # Nothing moves by itself for more than 5 s: the loop comes to rest, and sleeps offscreen.
    page.mouse.move(5, 5)
    page.wait_for_timeout(6000)
    idle = page.evaluate(f"{ROOT}.dataset.awake")
    size = page.viewport_size
    page.set_viewport_size({"width": size["width"], "height": 300})
    page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
    page.wait_for_timeout(900)
    page.evaluate("window.scrollBy(0, -2); window.scrollBy(0, 2)")
    page.wait_for_timeout(400)
    below = page.evaluate(f"{ROOT}.getBoundingClientRect().bottom")
    off = page.evaluate(f"{ROOT}.dataset.awake")
    page.set_viewport_size(size)
    page.wait_for_timeout(600)
    check(
        f"{tag}: the scene rests when the visitor stops and sleeps offscreen",
        idle == "false" and off == "false" and below <= 0,
        f"idle={idle} offscreen={off} lookBottom={below:.0f}",
    )


def footer_check(page, tag):
    """At the very bottom the pinned battery must end with the look, never over the footer
    (a negative-margin sticky stage once hung 100svh past the look's end)."""
    page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
    page.wait_for_timeout(600)
    gap = page.evaluate(
        """() => {
          const stage = document.querySelector('[class*=look-glass-module__][class*=stage]');
          const footer = document.querySelector('footer');
          return footer.getBoundingClientRect().top - stage.getBoundingClientRect().bottom;
        }"""
    )
    check(f"{tag}: the pinned battery stops above the footer", gap >= -1, f"footerTop - stageBottom = {gap:.0f}px")


def panel_checks(page, tag):
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(300)
    page.locator("main").get_by_role("button", name="Ask BiGH Science").click()
    page.wait_for_timeout(500)
    title = page.evaluate("document.querySelector('dialog[open] h2')?.textContent")
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    closed = page.evaluate("!document.querySelector('dialog[open]')")
    check(f"{tag}: Ask BiGH Science opens the panel and Escape closes it", title == "Ask BiGH Science" and closed, f"title={title} closed={closed}")
    page.evaluate("window.scrollTo(0, 0)")
    if tag == "phone":
        page.get_by_role("button", name="Open menu").click()
        page.wait_for_timeout(300)
    page.locator("header").get_by_role("button", name="Support").click()
    page.wait_for_timeout(400)
    title = page.evaluate("document.querySelector('dialog[open] h2')?.textContent")
    page.get_by_role("button", name="Close details").click()
    page.wait_for_timeout(300)
    closed = page.evaluate("!document.querySelector('dialog[open]')")
    check(f"{tag}: Support panel opens from the menu and closes", title == "BiGH support" and closed, f"title={title} closed={closed}")


# ---- Other languages -------------------------------------------------------------------------

LOCALES = ("kr", "jp", "cns", "vn")
CATALOGS = ("en", "kr", "jp", "cns", "vn")
# The About page's own files, and the shared header controls it shows.
ABOUT_FILES = [
    "src/components/about/about-page.tsx",
    "src/components/about/site-chrome.tsx",
    "src/components/about/look-glass.tsx",
    "src/components/about/acronym.tsx",
    "src/components/about/greetings.tsx",
    "src/components/home/header-utilities.tsx",
]
# May stay in English on a translated page: the h1 (what the name stands for, kept English on purpose) and
# names the catalogs keep in Latin letters.
KEEP_ENGLISH = {"Be in Good Health.", "BiGH", "Dr. Jiankang Liu"}


def read(path):
    with open(os.path.join(REPO, path), encoding="utf-8") as f:
        return f.read()


def copy_literals(text):
    """The string literals passed to copy(...), e.g. copy(open ? "Close menu" : "Open menu")."""
    found = []
    for m in re.finditer(r"\bcopy\(", text):
        i = j = m.end()
        depth = 1
        while depth and j < len(text):
            if text[j] == '"':
                j += 1
                while text[j] != '"':
                    j += 2 if text[j] == "\\" else 1
            elif text[j] == "(":
                depth += 1
            elif text[j] == ")":
                depth -= 1
            j += 1
        inner = re.sub(r'[!=]==\s*"[^"]*"', "", text[i : j - 1])
        found += re.findall(r'"((?:[^"\\]|\\.)*)"', inner)
    return found


def content_strings(text):
    """The words in about-content.ts's `about` and `drafts` (not paths, numbers, or the greetings, which are
    each written in their own language)."""
    found = []
    for name in ("about", "drafts"):
        block = re.search(rf"export const {name} = \{{(.*?)\n\}} as const;", text, re.S).group(1)
        block = re.sub(r"greetings: \[.*?\],", "", block, flags=re.S)
        block = re.sub(r"^\s*//.*$", "", block, flags=re.M)
        for key, value in re.findall(r'(?:(\w+):\s*)?"((?:[^"\\]|\\.)*)"', block):
            if key in ("src", "value", "lang") or not value or value.startswith("/"):
                continue
            found.append(value)
    return found


def about_sources():
    sources = content_strings(read("src/components/about/about-content.ts"))
    for path in ABOUT_FILES:
        sources += copy_literals(read(path))
    return list(dict.fromkeys(s.replace('\\"', '"') for s in sources))


def catalog_checks():
    keys = json.loads(read("src/i18n/copy-keys.json"))
    sources = about_sources()
    missing = [s for s in sources if s not in keys]
    check(f"i18n: every About string has a catalog key ({len(sources)} strings)", not missing and len(sources) > 60, f"missing={missing}")
    page = read("src/app/[locale]/about/page.tsx")
    check("i18n: the tab title's word comes from the catalogs", 'copyKeys["About"]' in page and "About" in keys)

    copies = {loc: json.loads(read(f"messages/{loc}.json")).get("Copy", {}) for loc in CATALOGS}
    ids = set(keys.values())
    uneven = {loc: (len(ids - set(c)), len(set(c) - ids)) for loc, c in copies.items() if set(c) != ids}
    check(f"i18n: the five catalogs have the same {len(ids)} keys as the source map", not uneven, f"(missing, extra)={uneven}")
    # About strings only: two homepage eyebrows ("04 / FOLLOW THE EVIDENCE", "05 / BE IN GOOD HEALTH") differ
    # from their English catalog text ("07 / …", "08 / …") on main; that is the homepage's to settle.
    wrong_en = [s for s in sources if s in keys and copies["en"].get(keys[s]) != s]
    check("i18n: the English catalog equals the About source text", not wrong_en, f"{wrong_en[:3]}")
    holes = lambda t: sorted(re.findall(r"\{(\w+)\}", t or ""))
    bad = [(loc, k) for loc in CATALOGS for s, k in keys.items() if holes(copies[loc].get(k)) != holes(s)]
    check("i18n: every translation keeps the source's {placeholders}", not bad, f"{bad[:4]}")
    hken = json.loads(read("messages/hken.json"))
    check("i18n: hken.json stays empty (it falls back to English; /hken redirects to /cns)", hken == {}, f"{list(hken)[:3]}")
    return sources


# Every line of every leaf text block (heading, label, paragraph, link, button) in the page and footer. A new
# line is where the next letter starts left of the last one, so it also reads the masked, shifted heading lines.
LINES = r"""() => {
  const out = [];
  for (const el of document.querySelectorAll('main h2, main h3, main p, main [class*=abel], main a, main button, footer p, footer a, footer button, footer h2')) {
    if (!el.getClientRects().length || el.closest('[aria-hidden=true]') || el.querySelector('p, h2, h3, [class*=abel]')) continue;
    const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    const r = document.createRange(); const lines = []; let cur = '', left = null, top = null;
    while (walker.nextNode()) {
      const t = walker.currentNode;
      for (let i = 0; i < t.length; i++) {
        r.setStart(t, i); r.setEnd(t, i + 1); const b = r.getClientRects()[0]; const ch = t.data[i];
        if (!b || b.width === 0 || /\s/.test(ch)) { cur += ch; continue; }
        if (left !== null && (b.left < left - 1 || b.top > top + b.height * 1.2)) { lines.push(cur); cur = ''; }
        left = b.left; top = b.top; cur += ch;
      }
    }
    lines.push(cur);
    out.push(lines.map(l => l.trim()).filter(Boolean));
  }
  return out;
}"""
CJK = r"[぀-ヿ㐀-鿿가-힯]"
CLOSING_PUNCT = "。、，．：；！？）」』・ー"


def line_checks(page, tag):
    bad = []
    for lines in page.evaluate(LINES):
        for i, line in enumerate(lines if len(lines) > 1 else []):
            core = re.sub(r"[。、，．：；！？」』,.:;!?]", "", line)
            if (i and line[0] in CLOSING_PUNCT) or re.fullmatch(CJK, core):
                bad.append(" / ".join(lines))
                break
    check(f"{tag}: no line is a lone character or starts with closing punctuation", not bad, f"{bad[:3]}")


def left_in_english(page, sources):
    """English source strings still showing, or read out (aria-label, alt), anywhere on the page."""
    text = page.evaluate(
        """() => [document.body.innerText, ...[...document.querySelectorAll('[aria-label]')].map(e => e.getAttribute('aria-label')),
                  ...[...document.images].map(i => i.alt)].join('\\n')"""
    )
    left = []
    for source in sources:
        if source in KEEP_ENGLISH:
            continue
        pattern = r"(?<![A-Za-z])" + re.escape(source) + r"(?![A-Za-z])"
        if re.search(pattern, text):
            left.append(source)
    return left


def shoot_chapters(page, loc, tag):
    """Viewport shots of each chapter where it is read, the footer and the Ask panel."""
    shot = lambda part: page.screenshot(path=os.path.join(OUT_I18N, f"{loc}-{tag}-{part}.png"))
    # A dialog closed with Escape hands focus back to its button; its focus ring is not part of the page.
    page.evaluate("document.activeElement?.blur()")
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(1200)
    shot("1-opening")
    parts = (("purpose", "#purpose"), ("roots", "#roots"), ("experience", "#experience"), ("promise", "#promise"), ("closing", "[data-chapter=closing]"))
    for i, (part, selector) in enumerate(parts, start=2):
        scroll_to_chapter(page, selector, settle=2400)
        shot(f"{i}-{part}")
    page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
    page.wait_for_timeout(900)
    shot("7-footer")
    page.locator("[data-chapter=closing] button").first.click()
    page.wait_for_timeout(700)
    shot("8-ask")
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)


def vietnamese_type_check(page):
    """Chrome's own answer (DevTools Protocol) to which faces drew the text: every Vietnamese heading, label, paragraph,
    link and button in Be Vietnam Pro only (Switzer lacks most Vietnamese letters, so Chrome used to fill them from
    Arial), and the English h1 in Switzer only."""
    cdp = page.context.new_cdp_session(page)
    cdp.send("DOM.enable")
    cdp.send("CSS.enable")
    count = page.evaluate(
        """() => { let n = 0;
            for (const e of document.querySelectorAll('header a, header button, main h1 span, main h2, main h3, main p, main li, main a, main button, footer p, footer a')) {
              if (!e.getClientRects().length || ![...e.childNodes].some(c => c.nodeType === 3 && c.textContent.trim())) continue;
              e.dataset.typeProbe = String(n++); }
            return n; }"""
    )
    root = cdp.send("DOM.getDocument", {"depth": -1})["root"]["nodeId"]
    vietnamese, english, wrong = {}, {}, []
    for i in range(count):
        node = cdp.send("DOM.querySelector", {"nodeId": root, "selector": f'[data-type-probe="{i}"]'})["nodeId"]
        lang = page.evaluate(f"document.querySelector('[data-type-probe=\"{i}\"]').closest('[lang]').lang")
        fonts = {f["familyName"]: f["glyphCount"] for f in cdp.send("CSS.getPlatformFontsForNode", {"nodeId": node})["fonts"]}
        if lang not in ("vi", "en"):
            continue  # the other languages' greetings
        into = english if lang == "en" else vietnamese
        for family, glyphs in fonts.items():
            into[family] = into.get(family, 0) + glyphs
        face = "Switzer" if lang == "en" else "Be Vietnam Pro"
        if any(not family.startswith(face) for family in fonts):
            wrong.append(f"{lang}:{i} {fonts}")
    cdp.detach()
    check(
        "vn: Vietnamese text is drawn in Be Vietnam Pro only, and the English h1 in Switzer (DevTools fonts, header to footer)",
        count > 20 and not wrong and any(f.startswith("Be Vietnam Pro") for f in vietnamese) and list(english) and all(f.startswith("Switzer") for f in english),
        f"elements={count} vietnamese={vietnamese} english={english} wrong={wrong[:3]}",
    )


def i18n_checks(browser, sources):
    for loc in LOCALES:
        # Desktop: the page, the words, the title, the dialogs, the breaks, the pictures.
        page = browser.new_page(viewport={"width": 1575, "height": 940})
        problems = watch(page)
        response = page.goto(f"{BASE}/{loc}/about", wait_until="networkidle")
        page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
        page.wait_for_timeout(2200)
        head = page.evaluate(
            """() => { const h = document.querySelector('h1');
                return { lang: h.lang, label: h.getAttribute('aria-label'), words: h.querySelectorAll(':scope > span > span').length,
                         open: h.dataset.open ?? null, title: document.title, html: document.documentElement.lang }; }"""
        )
        check(
            f"{loc}: /{loc}/about answers 200 and keeps the English h1 with its unfold (lang=en)",
            response.status == 200 and head["lang"] == "en" and head["label"] == "Be in Good Health." and head["words"] == 4 and head["open"] == "true",
            f"status={response.status} {head}",
        )
        check(f"{loc}: the tab title is translated", head["title"].startswith("BiGH — ") and head["title"] != "BiGH — About", head["title"])
        if loc == "vn":
            vietnamese_type_check(page)
        left = left_in_english(page, sources)
        # The dialogs: Ask BiGH Science from the closing, support from the header.
        page.locator("[data-chapter=closing] button").first.click()
        page.wait_for_timeout(500)
        left += left_in_english(page, sources)
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        page.locator("header nav button").first.click()
        page.wait_for_timeout(500)
        support = page.evaluate("!!document.querySelector('dialog[open]')")
        left += left_in_english(page, sources)
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        left = sorted(set(left))
        check(f"{loc}: no English source sentence left on the page, in the dialogs, labels or alt texts", not left and support, f"left={left} supportOpened={support}")
        line_checks(page, f"{loc}-desk")
        shoot_chapters(page, loc, "desk")
        check(f"{loc}-desk: no console errors or warnings", not problems, f"{problems[:3]}")
        page.close()

        # Phone: the breaks and the pictures.
        page = browser.new_page(viewport={"width": 390, "height": 844})
        problems = watch(page)
        page.goto(f"{BASE}/{loc}/about", wait_until="networkidle")
        page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
        page.wait_for_timeout(2200)
        line_checks(page, f"{loc}-phone")
        overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        shoot_chapters(page, loc, "phone")
        check(f"{loc}-phone: no sideways scrolling, no console errors or warnings", overflow == 0 and not problems, f"overflow={overflow} {problems[:3]}")
        page.close()

    # /hken is not a language of its own: it goes to the Chinese page, as the homepage and product pages do.
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    problems = watch(page)
    page.goto(f"{BASE}/hken/about", wait_until="networkidle")
    page.wait_for_timeout(800)
    lang = page.evaluate("document.documentElement.lang")
    check("hken: /hken/about goes to /cns/about, no errors", page.url.endswith("/cns/about") and lang == "zh-Hans" and not problems, f"url={page.url} lang={lang} {problems[:2]}")
    page.close()

    # The English h1 in a translated page: the glass after "Health." never touches a letter. Japanese, and
    # Vietnamese, whose other words are set in Be Vietnam Pro around the Switzer title.
    for loc in ("jp", "vn"):
        bad = []
        for w, h in ((1575, 940), (1280, 720), (390, 844)):
            page, problems = open_page(browser, w, h, url=f"{BASE}/{loc}/about")
            page.wait_for_timeout(1400)
            geo = page.evaluate(OPENING)
            if geo["placed"] != "true" or geo["titleHits"] or geo["otherHits"] or not geo["inView"] or problems:
                bad.append((f"{w}x{h}", geo, problems[:2]))
            page.close()
        check(f"{loc}: the glass after the English title never touches a letter and sits in the first screen (1575x940, 1280x720, 390x844)", not bad, f"{bad[:2]}")


SOURCES = catalog_checks()

with sync_playwright() as p:
    browser = p.chromium.launch(args=LAUNCH)
    for w, h, tag in SIZES:
        page, problems = open_page(browser, w, h)
        # On load, a heading below the fold waits behind its mask (read before anything scrolls).
        page.wait_for_function("document.querySelector('#experience h2').dataset.split === 'true'", timeout=8000)
        before = page.evaluate(REVEAL)
        shots = shoot_scroll(page, f"about-{tag}")
        page_checks(page, tag)
        system_checks(page, tag)
        signature_checks(page, tag, before)
        handoff_check(page, tag)
        light_checks(page, tag)
        readability_checks(page, tag)
        footer_check(page, tag)
        panel_checks(page, tag)
        check(f"{tag}: no errors, warnings or failed requests ({shots} shots)", not problems, f"{problems[:3]}")
        page.close()

        # Reduced motion: the still render, every bar full, the list complete, no WebGL, no errors.
        page, problems = open_page(browser, w, h, reduced=True)
        state = page.evaluate(
            f"""() => {{ const root = {ROOT}; const still = root.querySelector('[class*=still]');
                return {{ canvas: !!root.querySelector('canvas'), still: getComputedStyle(still).opacity,
                         bars: [...root.querySelectorAll('[data-pill] [class*=bar]')].map(b => getComputedStyle(b, '::after').transform),
                         recap: [...root.querySelectorAll('[class*=recap] [data-fact] span')].map(s => getComputedStyle(s).opacity) }}; }}"""
        )
        text = re.sub(r"\s+", " ", page.evaluate("document.querySelector('main').innerText"))
        missing = [words for words in LOCKED if words not in text and words != "Be in Good Health."]
        full = all(t in ("none", "matrix(1, 0, 0, 1, 0, 0)") for t in state["bars"]) and len(state["bars"]) == 4
        listed = state["recap"] == ["1"] * 8
        check(
            f"{tag}-reduced: the still render, every word, full bars, the list complete, no WebGL, no errors",
            not state["canvas"] and state["still"] == "1" and full and listed and not missing and not problems,
            f"{state} missing={missing} {problems[:3]}",
        )
        shoot_scroll(page, f"about-{tag}-reduced")
        page.close()

    opening_checks(browser)

    # No WebGL at all: the still render stays, its gold still follows the charge, and nothing is logged.
    nogl = p.chromium.launch(args=["--disable-3d-apis"])
    page = nogl.new_page(viewport={"width": 1440, "height": 900})
    problems = watch(page)
    page.goto(URL, wait_until="networkidle")
    page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
    page.wait_for_timeout(2600)
    saturate = "() => parseFloat(/saturate\\(([\\d.]+)\\)/.exec(getComputedStyle(document.querySelector('[class*=still]')).filter)?.[1] ?? '0')"
    at_top = page.evaluate(saturate)
    scroll_to_chapter(page, "[data-chapter=closing]")
    at_end = page.evaluate(saturate)
    state = page.evaluate(f"({{ canvas: !!{ROOT}.querySelector('canvas'), still: getComputedStyle({ROOT}.querySelector('[class*=still]')).opacity }})")
    page.screenshot(path=os.path.join(OUT, "about-nowebgl-closing.png"))
    check(
        "desk-no-webgl: the still render stays and its gold follows the charge, no errors",
        not state["canvas"] and state["still"] == "1" and at_end > at_top + 0.5 and not problems,
        f"{state} saturate top={at_top} end={at_end} {problems[:3]}",
    )
    page.close()
    nogl.close()

    # Korean, Japanese, Chinese and Vietnamese.
    i18n_checks(browser, SOURCES)
    browser.close()

print(f"\n{sum(results)} passed, {len(results) - sum(results)} failed")

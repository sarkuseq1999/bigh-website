"""QA for chapter 2, "Why it matters", at night (Template 2, "Chapters"): the light bulb story, or any
product's night story with --product=<slug> (the words each product must carry are in PRODUCTS).

With motion, at 1440x900 and 390x844, it scrolls the pinned track in small settled steps and checks:
- the moments arrive one at a time and in order: 2%, 20%, the comparison, the three approved lines,
  the title; never two readable at once (no illegible overlap)
- the light is off for the first figure and on from the second; the figure counts up to 20
- at every beat: no text over the bulb, and every line of text at least 4.5:1 against the pixels
  actually behind it (a screenshot with the words hidden)
- the photo has no edge: the page's night matches the photo's own ground where they meet
- the chapter index reads light on the night (rail on wide screens, pill on phones)
- jumping straight to the end and straight back settles on the right moment (fast scrolling)
Reduced motion (both sizes): no track, nothing sticky or split, the lit photo and every figure and
line shown, still no text over the bulb and the same contrast. Also: a phone held sideways (844x390)
gets the still layout; 1920x1080 keeps the photo edge invisible; a product without a night photo
(?chapters-fixture=full, development only) keeps the quiet paper list. No console errors anywhere.

Pictures (viewport shots; full-page shots break svh layouts): scripts/qa/out/why-<run>-<nn>-<beat>.png
and why-<run>-sheet.png.

    python -X utf8 scripts/qa/qa_why_chapter.py http://localhost:3007
    python -X utf8 scripts/qa/qa_why_chapter.py http://localhost:3010 --product=green-bee-propolis
"""
import io
import os
import sys

import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

POSITIONAL = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = (POSITIONAL[0] if POSITIONAL else "http://localhost:3007").rstrip("/")
SLUG = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--product=")), "nuricell")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)
NIGHT = (6, 22, 37)  # --night, sampled from the photos
# Per product: the moments in order (fact-<figure>, comparison, line-n, title), their words, the start
# of the source line, and the figures (the count each fact shows once it has counted up).
PRODUCTS = {
    "nuricell": {
        "beats": ["fact-2", "fact-20", "comparison", "line-1", "line-2", "line-3", "title"],
        "lines": [
            "Your brain is about 2% of your body’s weight.",
            "Yet it uses about 20% of your body’s energy.",
            "About 20 watts, day and night. Like a light that never goes out.",
            "Inside many of your body’s cells are mitochondria—tiny power plants that turn energy from food into a form your cells can use.",
            "That energy helps your brain think, your heart beat, and your muscles move.",
            "It’s one reason good health starts with your cells.",
            "Tiny power plants. A big part of your health.",
        ],
        "source": "Brain energy figures:",
        "figures": ["2", "20"],
    },
    "green-bee-propolis": {
        "beats": ["fact-7", "line-1", "line-2", "line-3", "title"],
        "lines": [
            "Minutes, on average, for one bee to gather a load of resin.",
            "Bees make propolis from the resin they gather from plants. They line their hive with it and seal its cracks.",
            "In Minas Gerais, they snip it from the shoot tips of one shrub, alecrim, and carry it home on their legs.",
            "That resin carries artepillin C, the compound green propolis is known for.",
            "Gathered by bees, from one Brazilian shrub.",
        ],
        "source": "Sources: Teixeira",
        "figures": ["7"],
    },
    "turmerific": {
        "beats": ["line-1", "line-2", "line-3", "title"],
        "lines": [
            "Curcumin is the compound that gives turmeric its golden colour.",
            "On its own, very little of it reaches your bloodstream.",
            "Longvida® carries curcumin in tiny particles of fat, designed to help your body absorb it.",
            "A golden compound. A hard one to absorb.",
        ],
        "source": "Sources: NIH (NCCIH)",
        "figures": [],
    },
}
BEATS = PRODUCTS[SLUG]["beats"]
LINES = PRODUCTS[SLUG]["lines"]
SOURCE = PRODUCTS[SLUG]["source"]
FIGURES = PRODUCTS[SLUG]["figures"]
passed = failed = 0
dev_notes = set()
url = None


def check(name, ok, detail=""):
    global passed, failed
    passed += bool(ok)
    failed += not ok
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))


def open_page(browser, w, h, reduced=False, extra=""):
    ctx = browser.new_context(
        viewport={"width": w, "height": h}, reduced_motion="reduce" if reduced else "no-preference"
    )
    page = ctx.new_page()
    problems = []

    def on_console(message):
        if message.type == "error" and "Failed to load resource" not in message.text:
            problems.append(f"console {message.text[:220]}")

    def on_response(response):
        if response.status < 400:
            return
        if response.status == 404 and "/_next/static/chunks/" in response.url:
            dev_notes.add(response.url.split("/_next/")[-1])
        else:
            problems.append(f"{response.status} {response.url[-90:]}")

    page.on("console", on_console)
    page.on("pageerror", lambda error: problems.append(f"pageerror {error}"))
    page.on("response", on_response)
    response = page.goto(url + extra, wait_until="networkidle")
    if not response or response.status >= 500:
        raise RuntimeError(f"page answered {response.status if response else 'nothing'}")
    page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
    page.wait_for_selector("[data-chapter='why']")
    page.wait_for_timeout(2500)
    return ctx, page, problems


TRACK = "document.querySelector('[data-chapter=\"why\"] [style*=\"--beats\"]')"
WHERE = f"""(() => {{ const t = {TRACK}; const r = t.getBoundingClientRect();
  return {{ top: Math.round(r.top + scrollY), height: t.offsetHeight }}; }})()"""
STATE = f"""(() => {{
  const track = {TRACK};
  const op = el => el ? +getComputedStyle(el).opacity : 0;
  const moments = [...track.querySelectorAll('[data-why-moment]')];
  const vis = moments.map(m => {{
    let v = op(m);
    const line = m.querySelector('[data-why-fact-line]');
    const figure = m.querySelector('[data-why-figure]');
    if (line) v = Math.min(v, op(line), op(figure));
    if (m.matches('[data-why-title]')) {{
      const first = m.querySelector('.tc-line');
      if (first) v = Math.min(v, Math.abs(new DOMMatrix(getComputedStyle(first).transform).m42) < 2 ? 1 : 0);
    }}
    return Math.round(v * 50) / 50;
  }});
  return {{
    vis, copy: op(track.querySelector('[data-why-copy]')),
    lit: Math.round(op(track.querySelector('[data-why-lit]')) * 50) / 50,
    counts: [...track.querySelectorAll('[data-why-count]')].map(c => c.textContent),
    texts: moments.map(m => (m.querySelector('[data-why-fact-line]') || m).textContent.trim()),
    tone: document.querySelector('[data-motion][data-active]').dataset.tone,
  }};
}})()"""
# Every visible line of text in the chapter, as the boxes its glyphs really occupy (one per line;
# a text node's own client rects, so a wide block never counts as text), with the text's colour
# and size after its own and its ancestors' opacity. Also the bulb's box, the picture's clip, and
# the fixed overlay (the chapter index).
TEXTS = f"""(() => {{
  const track = {TRACK};
  const W = innerWidth, H = innerHeight;
  const out = [];
  const walker = document.createTreeWalker(track, NodeFilter.SHOW_TEXT);
  let node;
  while ((node = walker.nextNode())) {{
    if (!node.nodeValue.trim()) continue;
    const el = node.parentElement;
    let alpha = 1;
    for (let a = el; a && a !== track.parentElement; a = a.parentElement) alpha *= +getComputedStyle(a).opacity;
    if (alpha < 0.9 || getComputedStyle(el).visibility !== 'visible') continue;
    const s = getComputedStyle(el);
    const range = document.createRange();
    range.selectNodeContents(node);
    for (const r of range.getClientRects()) {{
      if (r.width < 2 || r.height < 2 || r.bottom <= 0 || r.top >= H) continue;
      out.push({{ text: (el.closest('p, h2') || el).textContent.trim().slice(0, 40),
        x0: Math.max(0, r.left), y0: Math.max(0, r.top), x1: Math.min(W, r.right), y1: Math.min(H, r.bottom),
        color: s.color, size: parseFloat(s.fontSize) }});
    }}
  }}
  const frame = track.querySelector('[data-why-frame]');
  const clip = track.querySelector('[data-why-picture]').getBoundingClientRect();
  const f = frame.getBoundingClientRect();
  const bulb = {{ x0: Math.max(clip.left, f.left + 0.52 * f.width), x1: Math.min(clip.right, f.left + 0.87 * f.width),
    y0: Math.max(clip.top, f.top), y1: Math.min(clip.bottom, f.top + 0.83 * f.height) }};
  const box = e => {{ if (!e) return null; const r = e.getBoundingClientRect(); const st = getComputedStyle(e);
    if (!r.width || st.display === 'none' || st.visibility !== 'visible' || +st.opacity < 0.1) return null;
    return {{ x0: r.left, y0: r.top, x1: r.right, y1: r.bottom }}; }};
  const nav = document.querySelector('nav[aria-label="Chapters"]');
  const overlays = [nav && nav.dataset.shown === 'true' ? box(nav.querySelector('button[aria-controls]')) : null,
    nav && nav.dataset.shown === 'true' ? box(nav.querySelector('ol')) : null].filter(Boolean);
  return {{ texts: out, bulb, overlays, frame: {{ x0: f.left, y0: f.top, x1: f.right, y1: f.bottom }},
    picture: {{ x0: clip.left, y0: clip.top, x1: clip.right, y1: clip.bottom }} }};
}})()"""
OVERLAYS = "nav[aria-label='Chapters']"
HIDE = f"""{TRACK}.querySelectorAll('[data-why-copy], p').forEach(e => e.style.visibility = 'hidden');
  document.querySelectorAll("{OVERLAYS}").forEach(e => e.style.visibility = 'hidden')"""
SHOW = f"""{TRACK}.querySelectorAll('[data-why-copy], p').forEach(e => e.style.visibility = '');
  document.querySelectorAll("{OVERLAYS}").forEach(e => e.style.visibility = '')"""


def rgba(css):
    inside = css[css.index("(") + 1: css.index(")")].replace("/", ",").replace(" ", ",")
    parts = [float(p) for p in inside.split(",") if p]
    return parts[:3], (parts[3] if len(parts) > 3 else 1.0)


def luminance(rgb):
    c = np.asarray(rgb, dtype=np.float64) / 255
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return c[..., 0] * 0.2126 + c[..., 1] * 0.7152 + c[..., 2] * 0.0722


def shot_array(page):
    return np.asarray(Image.open(io.BytesIO(page.screenshot())).convert("RGB"), dtype=np.float64)


def intersects(a, b, margin=6):
    return a["x0"] < b["x1"] - margin and a["x1"] > b["x0"] + margin and a["y0"] < b["y1"] - margin and a["y1"] > b["y0"] + margin


def legibility(page, pinned=True):
    """Words never over the bulb (nor, on the pinned stage, under the fixed index), and
    every line at least 4.5:1 against the brightest pixels actually behind it (the words and the
    overlays hidden for that picture). Still layouts scroll under the fixed overlays by nature."""
    info = page.evaluate(TEXTS)
    page.evaluate(HIDE)
    page.wait_for_timeout(120)
    bg = shot_array(page)
    page.evaluate(SHOW)
    worst, over = {}, []
    for t in info["texts"]:
        if intersects(t, info["bulb"]):
            over.append(t["text"])
        if pinned and any(intersects(t, o, 0) for o in info["overlays"]):
            over.append("under an overlay: " + t["text"])
        region = bg[int(t["y0"]): int(t["y1"]), int(t["x0"]): int(t["x1"])]
        if region.size == 0:
            continue
        lum = luminance(region.reshape(-1, 3))
        bright = float(np.percentile(lum, 99))
        base = region.reshape(-1, 3)[int(np.argmin(np.abs(lum - bright)))]
        rgb, alpha = rgba(t["color"])
        text = np.asarray(rgb) * alpha + base * (1 - alpha)
        lt = float(luminance(text))
        ratio = round((max(lt, bright) + 0.05) / (min(lt, bright) + 0.05), 1)
        key = t["text"]
        if key not in worst or ratio < worst[key][0]:
            worst[key] = (ratio, key, t["size"])
    return info, sorted(set(over)), sorted(worst.values())


def settle(page, limit=3200):
    last, waited = None, 0
    page.wait_for_timeout(450)
    while waited < limit:
        state = page.evaluate(STATE)
        key = (tuple(state["vis"]), state["lit"], tuple(state["counts"]), round(state["copy"], 2))
        if key == last:
            return state
        last = key
        page.wait_for_timeout(180)
        waited += 180
    return page.evaluate(STATE)


def glide(page, y, steps=10):
    current = page.evaluate("scrollY")
    for s in range(1, steps + 1):
        page.evaluate(f"window.scrollTo({{top: {current + (y - current) * s / steps}, behavior: 'instant'}})")
        page.wait_for_timeout(30)


def jump(page, y):
    page.evaluate(f"window.scrollTo({{top: {y}, behavior: 'instant'}})")


class Shots:
    def __init__(self, run):
        self.run, self.paths = run, []

    def take(self, page, name):
        path = os.path.join(OUT, f"why-{self.run}-{len(self.paths):02d}-{name}.png")
        page.screenshot(path=path)
        self.paths.append(path)
        return path

    def sheet(self, scale, columns):
        images = [Image.open(p).convert("RGB") for p in self.paths]
        images = [im.resize((int(im.width * scale), int(im.height * scale))) for im in images]
        w, h = images[0].size
        rows = (len(images) + columns - 1) // columns
        sheet = Image.new("RGB", (columns * (w + 10), rows * (h + 10)), (40, 44, 52))
        for i, im in enumerate(images):
            sheet.paste(im, ((i % columns) * (w + 10), (i // columns) * (h + 10)))
        path = os.path.join(OUT, f"why-{self.run}-sheet.png")
        sheet.save(path)
        return path


def seam(page, label, lit_state):
    """Where the page's night meets the photo, the two must match (no visible edge)."""
    info = page.evaluate(TEXTS)
    img = shot_array(page)
    H, W = img.shape[:2]
    f, pic = info["frame"], info["picture"]
    diffs = []
    # Plain night far from the bulb, inside the photo.
    x0 = int(max(f["x0"] + 0.15 * (f["x1"] - f["x0"]), pic["x0"], 0))
    patch = img[8:60, x0: x0 + 60].reshape(-1, 3).mean(axis=0)
    diffs.append(("photo ground vs night", float(np.abs(patch - NIGHT).max())))
    # The photo's left edge, when it is on screen.
    if f["x0"] > 24:
        xe = int(f["x0"])
        outside = img[8:60, max(0, xe - 20): xe - 4].reshape(-1, 3).mean(axis=0)
        inside = img[8:60, xe + 4: xe + 40].reshape(-1, 3).mean(axis=0)
        diffs.append(("left edge", float(np.abs(outside - inside).max())))
    # The picture's lower edge, when it is on screen, away from the bulb.
    if pic["y1"] < H - 20:
        yb = int(pic["y1"])
        above = img[yb - 14: yb - 4, 4:40].reshape(-1, 3).mean(axis=0)
        below = img[yb + 4: yb + 14, 4:40].reshape(-1, 3).mean(axis=0)
        diffs.append(("picture's lower edge", float(np.abs(above - below).max())))
    bad = [d for d in diffs if d[1] > 4]
    check(f"{label}: no photo edge ({lit_state}): the night matches the photo's ground", not bad,
          ", ".join(f"{n} Δ{v:.1f}" for n, v in diffs))


def index_on_night(page, label, phone):
    js = """(() => { const nav = document.querySelector('nav[aria-label="Chapters"]');
      const link = nav.querySelector('a:not([aria-current])'); const cur = nav.querySelector('a[aria-current] span');
      const toggle = nav.querySelector('button[aria-controls]');
      const s = e => getComputedStyle(e);
      return { tone: document.querySelector('[data-motion][data-active]').dataset.tone,
        link: s(link).color, current: s(cur).backgroundColor, currentText: s(cur).color,
        toggleBg: s(toggle).backgroundColor, toggleText: s(toggle).color, shown: nav.dataset.shown }; })()"""
    st = page.evaluate(js)

    def ratio(fg, bg):
        (f, fa), (b, ba) = rgba(fg), rgba(bg)
        b = np.asarray(b) * ba + np.asarray(NIGHT) * (1 - ba)
        f = np.asarray(f) * fa + b * (1 - fa)
        lf, lb = float(luminance(f)), float(luminance(b))
        return (max(lf, lb) + 0.05) / (min(lf, lb) + 0.05)

    if phone:
        r = ratio(st["toggleText"], st["toggleBg"])
        check(f"{label}: over the night the page is 'night' and the phone pill reads light on dark (>= 4.5:1)",
              st["tone"] == "night" and r >= 4.5 and luminance(rgba(st["toggleBg"])[0]) < 0.1,
              f"tone={st['tone']} pill={st['toggleBg']} text={st['toggleText']} ratio={r:.1f}")
    else:
        r_link = ratio(st["link"], "rgb(6, 22, 37)")
        r_cur = ratio(st["currentText"], st["current"])
        check(f"{label}: over the night the page is 'night', the rail reads light (>= 4.5:1) and marks the chapter in gold",
              st["tone"] == "night" and r_link >= 4.5 and r_cur >= 4.5 and st["current"] == "rgb(234, 164, 58)",
              f"tone={st['tone']} link={st['link']} {r_link:.1f}:1 current={st['current']} {r_cur:.1f}:1")


def run_motion(browser, label, w, h):
    ctx, page, problems = open_page(browser, w, h)
    shots = Shots(label)
    phone = w < 900
    where = page.evaluate(WHERE)
    texts = page.evaluate(STATE)["texts"]
    check(f"{label}: the chapter carries the approved words, in order", texts == LINES,
          str([t[:30] for t in texts]) if texts != LINES else f"{len(LINES)} moments")
    pinned = where["height"] - h
    # About half a window of scrolling per moment (NuriCell's seven: over three windows).
    check(f"{label}: a tall pinned track (motion on)", pinned > h * 0.45 * len(BEATS),
          f"track={where['height']} window={h}")

    # The stage rising into view.
    glide(page, where["top"] - int(h * 0.45), steps=12)
    settle(page)
    shots.take(page, "arriving")

    # Scan the pinned track in small settled steps.
    steps = 36
    scan = []
    for i in range(steps):
        y = where["top"] + int(pinned * (i + 0.5) / steps)
        glide(page, y, steps=6)
        state = settle(page)
        scan.append((y, state))
    full = [[k for k, v in enumerate(s["vis"]) if v >= 0.95] for _, s in scan]
    doubles = [(i, s["vis"]) for i, (_, s) in enumerate(scan) if sum(v >= 0.35 for v in s["vis"]) > 1]
    order = []
    for f in full:
        for k in f:
            if not order or order[-1] != k:
                order.append(k)
    check(f"{label}: the moments arrive one at a time, in order ({', '.join(BEATS)})",
          order == list(range(len(BEATS))) and all(len(f) <= 1 for f in full), f"order={order}")
    check(f"{label}: never two moments readable at once (no overlapping words)", not doubles, str(doubles[:2]))
    first = [s for f, (_, s) in zip(full, scan) if f == [0]]
    second = [s for f, (_, s) in zip(full, scan) if f == [1]]
    check(f"{label}: the light is off for the first moment and on from the second"
          + (f", which counts up to {FIGURES[1]}" if len(FIGURES) > 1 else ""),
          first and second and all(s["lit"] <= 0.02 for s in first) and all(s["lit"] >= 0.98 for s in second)
          and all(s["counts"][1] == FIGURES[1] for s in second if len(FIGURES) > 1),
          f"off={[s['lit'] for s in first]} on={[s['lit'] for s in second]} counts={[s['counts'] for s in second]}")
    later = [s["lit"] for f, (_, s) in zip(full, scan) if f and f[0] >= 1]
    check(f"{label}: once on, the light stays on to the end", later and min(later) >= 0.98, str(later))
    # A product without figures (Turmerific) has no count to read while the light comes on.
    counting = [s["counts"][-1] for f, (_, s) in zip(full, scan) if not f and 0 < s["lit"] < 1 and s["counts"]]
    print(f"      (between the figures the count read {counting}, the light {[s['lit'] for f, (_, s) in zip(full, scan) if not f and 0 < s['lit'] < 1]})")

    # A picture at each beat, with the words checked against what is really behind them.
    runs = {}
    for i, f in enumerate(full):
        if len(f) == 1:
            runs.setdefault(f[0], []).append(i)
    switch = [i for i, (_, s) in enumerate(scan) if 0.15 < s["lit"] < 0.85]
    plan = []
    for k, name in enumerate(BEATS):
        if k in runs:
            plan.append((name, scan[runs[k][len(runs[k]) // 2]][0], k))
        if k == 0 and switch:
            plan.append(("switching-on", scan[switch[len(switch) // 2]][0], None))
    legible_bad, over_bad, notes = [], [], []
    for name, y, k in plan:
        glide(page, y, steps=8)
        state = settle(page)
        page.wait_for_timeout(250)
        shots.take(page, name)
        if k is None:
            continue
        info, over, worst = legibility(page)
        notes.append(f"{name} {worst[0][0]}:1" if worst else f"{name} -")
        if over:
            over_bad.append((name, over))
        low = [x for x in worst if x[0] < 4.5]
        if low:
            legible_bad.append((name, low[:2]))
        if k == 0:
            seam(page, label, "light off")
            index_on_night(page, label, phone)
        if k == len(BEATS) - 1:
            seam(page, label, "light on")
            source = [t for t in info["texts"] if t["text"].startswith(SOURCE)]
            check(f"{label}: the source line is on screen, at least 15px",
                  source and min(t["size"] for t in source) >= 15,
                  f"{source[0]['size'] if source else None}px {source[0] if source else ''}")
    check(f"{label}: no words over the bulb at any beat", not over_bad, str(over_bad[:2]))
    check(f"{label}: every visible line of text >= 4.5:1 against the pixels behind it, at every beat",
          not legible_bad, str(legible_bad[:2]) if legible_bad else "lowest per beat: " + ", ".join(notes))

    # Fast scrolling: straight to the title, then straight back to the first figure.
    title_y = next(y for n, y, _ in plan if n == "title")
    first_y = next(y for n, y, _ in plan if n == BEATS[0])
    jump(page, title_y)
    end = settle(page, 5000)
    jump(page, first_y)
    back = settle(page, 5000)
    check(f"{label}: a fast jump to the end settles on the title (light on), and straight back on the first moment (light off)",
          [k for k, v in enumerate(end["vis"]) if v >= 0.95] == [len(BEATS) - 1] and end["lit"] >= 0.98
          and [k for k, v in enumerate(back["vis"]) if v >= 0.95] == [0] and back["lit"] <= 0.02
          and back["counts"] == ([FIGURES[0]] * len(FIGURES) if FIGURES else []),
          f"end={end['vis']} lit={end['lit']} back={back['vis']} lit={back['lit']} counts={back['counts']}")
    shots.take(page, "back-to-start")

    # Leaving: the next chapter's own zone decides the page's tone again (it may be night too).
    glide(page, where["top"] + where["height"] + int(h * 0.1), steps=10)
    page.wait_for_timeout(700)
    hand = page.evaluate("""(() => { const root = document.querySelector('[data-motion][data-active]');
      const line = innerHeight * 0.45; let last = null;
      root.querySelectorAll('[data-tone]').forEach(z => { if (z.getBoundingClientRect().top <= line) last = z; });
      return { tone: root.dataset.tone, active: root.dataset.active, mine: !!last.closest('[data-chapter="why"]'),
        zone: last.dataset.tone }; })()""")
    shots.take(page, "leaving")
    check(f"{label}: after the chapter the index follows the next chapter's own tone", not hand["mine"]
          and hand["active"] != "why" and hand["tone"] == hand["zone"], str(hand))

    check(f"{label}: no console errors, page errors or failed requests", not problems, str(problems[:3]))
    ctx.close()
    return shots


def run_still(browser, label, w, h, reduced=True):
    ctx, page, problems = open_page(browser, w, h, reduced=reduced)
    shots = Shots(label)
    where = page.evaluate(WHERE)
    still = page.evaluate(f"""(() => {{ const t = {TRACK}; const stage = t.firstElementChild;
      const op = e => +getComputedStyle(e).opacity;
      const bits = [...t.querySelectorAll('[data-why-moment], [data-why-figure], [data-why-fact-line]')];
      return {{ extra: t.offsetHeight - stage.offsetHeight, position: getComputedStyle(stage).position,
        sticky: [...t.querySelectorAll('*')].filter(e => getComputedStyle(e).position === 'sticky').length,
        masks: t.querySelectorAll('.tc-line-mask').length, lit: op(t.querySelector('[data-why-lit]')),
        glow: op(t.querySelector('[data-why-glow]')), hidden: bits.filter(e => op(e) < 0.99).length, count: bits.length,
        counts: [...t.querySelectorAll('[data-why-count]')].map(c => c.textContent) }}; }})()""")
    check(f"{label}: still layout: no track, nothing sticky or split",
          still["extra"] == 0 and still["position"] != "sticky" and still["sticky"] == 0 and still["masks"] == 0, str(still))
    check(f"{label}: the lit photo and every figure and line are shown ({', '.join(FIGURES)})",
          still["lit"] == 1 and still["glow"] == 1 and still["hidden"] == 0 and still["counts"] == FIGURES, str(still))
    y = where["top"]
    over_bad, legible_bad, notes = [], [], []
    n = 0
    while y < where["top"] + where["height"] and n < 8:
        jump(page, y)
        page.wait_for_timeout(500)
        shots.take(page, f"still-{n}")
        info, over, worst = legibility(page, pinned=False)
        if n == 0:
            seam(page, label, "light on")
        notes.append(f"{worst[0][0]}:1" if worst else "-")
        if over:
            over_bad.append((n, over))
        low = [x for x in worst if x[0] < 4.5]
        if low:
            legible_bad.append((n, low[:2]))
        y += int(h * 0.85)
        n += 1
    check(f"{label}: no words over the bulb", not over_bad, str(over_bad[:2]))
    check(f"{label}: every line of text >= 4.5:1 against the pixels behind it", not legible_bad,
          str(legible_bad[:2]) if legible_bad else "lowest per screen: " + ", ".join(notes))
    check(f"{label}: no console errors, page errors or failed requests", not problems, str(problems[:3]))
    ctx.close()
    return shots


def run_wide(browser):
    ctx, page, problems = open_page(browser, 1920, 1080)
    shots = Shots("wide")
    where = page.evaluate(WHERE)
    glide(page, where["top"] + 40, steps=10)
    settle(page)
    shots.take(page, BEATS[0])
    seam(page, "wide 1920x1080", "light off")
    info, over, worst = legibility(page)
    check("wide 1920x1080: no words over the bulb, contrast >= 4.5:1", not over and (not worst or worst[0][0] >= 4.5),
          f"over={over} lowest={worst[:1]}")
    glide(page, where["top"] + where["height"] - 1080 - 20, steps=14)
    settle(page)
    shots.take(page, "title")
    seam(page, "wide 1920x1080", "light on")
    check("wide 1920x1080: no console errors", not problems, str(problems[:3]))
    ctx.close()
    return shots


def run_fixture(browser):
    ctx, page, problems = open_page(browser, 1440, 900, extra="?chapters-fixture=full")
    st = page.evaluate("""(() => { const s = document.querySelector('[data-chapter="why"]');
      return { night: s.querySelectorAll('[data-why-picture]').length, tone: s.dataset.tone,
        lines: s.querySelectorAll('[data-why-line]').length, title: !!s.querySelector('h2') }; })()""")
    if st["night"] and st["lines"] == 3:
        print("NOTE fixture skipped: this server ignores ?chapters-fixture (a production build)")
    else:
        check("fixture 'full' (no night photo): the quiet list on paper, four lines and the title, no errors",
              st["night"] == 0 and st["tone"] == "paper" and st["lines"] == 4 and st["title"] and not problems,
              f"{st} {problems[:2]}")
    ctx.close()


def attempt(fn, *args, **kwargs):
    """Other agents save files while this runs; a crash from a mid-run reload gets one retry."""
    try:
        return fn(*args, **kwargs)
    except Exception as error:  # noqa: BLE001
        print(f"RETRY after: {str(error)[:160]}")
        return fn(*args, **kwargs)


with sync_playwright() as p:
    browser = p.chromium.launch(args=["--use-gl=angle", "--use-angle=d3d11", "--enable-gpu", "--ignore-gpu-blocklist"])
    for url in [f"{BASE}/products/{SLUG}"]:
        probe = browser.new_page()
        probe.goto(url, wait_until="domcontentloaded")
        found = probe.locator("[data-chapter='why'] [data-why-picture]").count()
        probe.close()
        if found:
            break
    print(f"Page: {url}")
    sheets = []
    for label, w, h in (("desk", 1440, 900), ("phone", 390, 844)):
        sheets.append(attempt(run_motion, browser, label, w, h).sheet(0.5 if w > 1000 else 0.6, 4))
    for label, w, h in (("still-desk", 1440, 900), ("still-phone", 390, 844)):
        sheets.append(attempt(run_still, browser, label, w, h).sheet(0.5 if w > 1000 else 0.6, 4))
    sheets.append(attempt(run_still, browser, "landscape", 844, 390, reduced=False).sheet(0.6, 3))
    sheets.append(attempt(run_wide, browser).sheet(0.4, 2))
    attempt(run_fixture, browser)
    browser.close()

print("\nSheets:", *sheets, sep="\n  ")
if dev_notes:
    print("\nNOTE (not counted): the dev server preloads a missing chunk:", *sorted(dev_notes), sep="\n  ")
print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)

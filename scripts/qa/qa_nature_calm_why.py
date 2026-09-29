"""QA for Nature Calm's "Why it matters" at night: the microscope whose lamp comes on.

Derived from qa_why_chapter.py (NuriCell's light bulb), September 28, 2026. With motion, at
1440x900 and 390x844, it scrolls the pinned track in small settled steps and checks:
- the moments arrive one at a time and in order: the four lines, then the title; never two
  readable at once (no illegible overlap)
- the lamp is off for the first line and on from the second, and stays on
- at every beat: no text over the microscope, and every line of text at least 4.5:1 against the
  pixels actually behind it (a screenshot with the words hidden)
- the photo has no edge: the page's night matches the photo's own ground where they meet
- the chapter index reads light on the night (rail on wide screens, pill on phones)
- jumping straight to the end and straight back settles on the right moment (fast scrolling)
Reduced motion (both sizes): no track, nothing sticky or split, the lit photo and every line shown,
still no text over the microscope and the same contrast. Also: a phone held sideways (844x390)
gets the still layout; 1920x1080 keeps the photo edge invisible. No console errors anywhere.

Pictures (viewport shots; full-page shots break svh layouts): scripts/qa/out/ncwhy-<run>-<nn>-<beat>.png
and ncwhy-<run>-sheet.png.

    python -X utf8 scripts/qa/qa_nature_calm_why.py http://localhost:3013
"""
import io
import os
import sys

import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3013").rstrip("/")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)
NIGHT = (6, 22, 37)  # --night, sampled from the photos
BEATS = ["line-1", "line-2", "line-3", "line-4", "title"]
LINES = [
    "Under stress, your body releases hormones that get it ready to respond.",
    "Scientists study what stress does inside your cells, including their mitochondria.",
    "In animal studies, Dr. Liu and Dr. Wang found that stress raised oxidative damage in the brain.",
    "Nature Calm brings their research into a formula for life’s demanding days.",
    "Stress, seen from inside the cell.",
]
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
    texts: moments.map(m => (m.querySelector('[data-why-fact-line]') || m).textContent.replace(/\u00a0/g, ' ').trim()),
    tone: document.querySelector('[data-motion][data-active]').dataset.tone,
  }};
}})()"""
# Every visible line of text in the chapter, as the boxes its glyphs really occupy (one per line;
# a text node's own client rects, so a wide block never counts as text), with the text's colour
# and size after its own and its ancestors' opacity. Also the scope's box, the picture's clip, and
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
  const scope = {{ x0: Math.max(clip.left, f.left + 0.53 * f.width), x1: Math.min(clip.right, f.left + 0.89 * f.width),
    y0: Math.max(clip.top, f.top), y1: Math.min(clip.bottom, f.top + 0.8 * f.height) }};
  const box = e => {{ if (!e) return null; const r = e.getBoundingClientRect(); const st = getComputedStyle(e);
    if (!r.width || st.display === 'none' || st.visibility !== 'visible' || +st.opacity < 0.1) return null;
    return {{ x0: r.left, y0: r.top, x1: r.right, y1: r.bottom }}; }};
  const nav = document.querySelector('nav[aria-label="Chapters"]');
  const overlays = [nav && nav.dataset.shown === 'true' ? box(nav.querySelector('button[aria-controls]')) : null,
    nav && nav.dataset.shown === 'true' ? box(nav.querySelector('ol')) : null].filter(Boolean);
  return {{ texts: out, scope, overlays, frame: {{ x0: f.left, y0: f.top, x1: f.right, y1: f.bottom }},
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
    """Words never over the microscope (nor, on the pinned stage, under the fixed index), and
    every line at least 4.5:1 against the brightest pixels actually behind it (the words and the
    overlays hidden for that picture). Still layouts scroll under the fixed overlays by nature."""
    info = page.evaluate(TEXTS)
    page.evaluate(HIDE)
    page.wait_for_timeout(120)
    bg = shot_array(page)
    page.evaluate(SHOW)
    worst, over = {}, []
    for t in info["texts"]:
        if intersects(t, info["scope"]):
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
        path = os.path.join(OUT, f"ncwhy-{self.run}-{len(self.paths):02d}-{name}.png")
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
        path = os.path.join(OUT, f"ncwhy-{self.run}-sheet.png")
        sheet.save(path)
        return path


def seam(page, label, lit_state):
    """Where the page's night meets the photo, the two must match (no visible edge)."""
    info = page.evaluate(TEXTS)
    img = shot_array(page)
    H, W = img.shape[:2]
    f, pic = info["frame"], info["picture"]
    diffs = []
    # Plain night far from the scope, inside the photo.
    x0 = int(max(f["x0"] + 0.15 * (f["x1"] - f["x0"]), pic["x0"], 0))
    patch = img[8:60, x0: x0 + 60].reshape(-1, 3).mean(axis=0)
    diffs.append(("photo ground vs night", float(np.abs(patch - NIGHT).max())))
    # The photo's left edge, when it is on screen.
    if f["x0"] > 24:
        xe = int(f["x0"])
        outside = img[8:60, max(0, xe - 20): xe - 4].reshape(-1, 3).mean(axis=0)
        inside = img[8:60, xe + 4: xe + 40].reshape(-1, 3).mean(axis=0)
        diffs.append(("left edge", float(np.abs(outside - inside).max())))
    # The picture's lower edge, when it is on screen, away from the scope.
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
          str([t[:30] for t in texts]) if texts != LINES else "7 moments")
    pinned = where["height"] - h
    # Five moments here against NuriCell's seven, so the track is shorter than NuriCell's 3 screens.
    check(f"{label}: a tall pinned track (motion on)", pinned > h * 2, f"track={where['height']} window={h}")

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
    check(f"{label}: the moments arrive one at a time, in order (four lines, then the title)",
          order == list(range(len(BEATS))) and all(len(f) <= 1 for f in full), f"order={order}")
    check(f"{label}: never two moments readable at once (no overlapping words)", not doubles, str(doubles[:2]))
    first = [s for f, (_, s) in zip(full, scan) if f == [0]]
    second = [s for f, (_, s) in zip(full, scan) if f == [1]]
    check(f"{label}: the lamp is off for the first line and on from the second",
          first and second and all(s["lit"] <= 0.02 for s in first) and all(s["lit"] >= 0.98 for s in second),
          f"off={[s['lit'] for s in first]} on={[s['lit'] for s in second]}")
    later = [s["lit"] for f, (_, s) in zip(full, scan) if f and f[0] >= 1]
    check(f"{label}: once on, the light stays on to the end", later and min(later) >= 0.98, str(later))

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
    check(f"{label}: no words over the microscope at any beat", not over_bad, str(over_bad[:2]))
    check(f"{label}: every visible line of text >= 4.5:1 against the pixels behind it, at every beat",
          not legible_bad, str(legible_bad[:2]) if legible_bad else "lowest per beat: " + ", ".join(notes))

    # Fast scrolling: straight to the title, then straight back to the first figure.
    title_y = next(y for n, y, _ in plan if n == "title")
    first_y = next(y for n, y, _ in plan if n == "line-1")
    jump(page, title_y)
    end = settle(page, 5000)
    jump(page, first_y)
    back = settle(page, 5000)
    check(f"{label}: a fast jump to the end settles on the title (lamp on), and straight back on the first line (lamp off)",
          [k for k, v in enumerate(end["vis"]) if v >= 0.95] == [len(BEATS) - 1] and end["lit"] >= 0.98
          and [k for k, v in enumerate(back["vis"]) if v >= 0.95] == [0] and back["lit"] <= 0.02,
          f"end={end['vis']} lit={end['lit']} back={back['vis']} lit={back['lit']}")
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
    check(f"{label}: the lit photo and every line are shown",
          still["lit"] == 1 and still["glow"] == 1 and still["hidden"] == 0 and still["count"] == len(BEATS), str(still))
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
    check(f"{label}: no words over the microscope", not over_bad, str(over_bad[:2]))
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
    shots.take(page, "line-1")
    seam(page, "wide 1920x1080", "light off")
    info, over, worst = legibility(page)
    check("wide 1920x1080: no words over the microscope, contrast >= 4.5:1", not over and (not worst or worst[0][0] >= 4.5),
          f"over={over} lowest={worst[:1]}")
    glide(page, where["top"] + where["height"] - 1080 - 20, steps=14)
    settle(page)
    shots.take(page, "title")
    seam(page, "wide 1920x1080", "light on")
    check("wide 1920x1080: no console errors", not problems, str(problems[:3]))
    ctx.close()
    return shots


def attempt(fn, *args, **kwargs):
    """Other agents save files while this runs; a crash from a mid-run reload gets one retry."""
    try:
        return fn(*args, **kwargs)
    except Exception as error:  # noqa: BLE001
        print(f"RETRY after: {str(error)[:160]}")
        return fn(*args, **kwargs)


with sync_playwright() as p:
    browser = p.chromium.launch(args=["--use-gl=angle", "--use-angle=d3d11", "--enable-gpu", "--ignore-gpu-blocklist"])
    for url in [f"{BASE}/products/nature-calm"]:
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
    browser.close()

print("\nSheets:", *sheets, sep="\n  ")
if dev_notes:
    print("\nNOTE (not counted): the dev server preloads a missing chunk:", *sorted(dev_notes), sep="\n  ")
print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)

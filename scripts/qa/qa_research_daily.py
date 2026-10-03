"""QA for two chapters of Template 2, "Chapters": the research timeline and "One bottle, one month."

Checks at 1440x900 and 390x844 with motion, then both again with reduced motion:
- research: the heading and the honesty line (product.notes.research) stay on screen, uncovered,
  at every step through the chapter; every study card is fully in view at some point (inside the
  timeline's window, not faded); each study's link is reached with Tab and brings its card into view;
  links open a new tab with rel="noopener"; studies run oldest first; wide screens with motion pin
  the stage (sticky) and the gold line fills and lights the years; phones and reduced motion get a
  sideways list with scroll-snap and the next card peeking
- daily: the month has 30 days; with motion it fills day by day as you scroll (never going back while
  scrolling down), un-fills when you scroll back up, lands right after a fast jump either way, and
  ends at 30 days, 90 capsules and "Then a new bottle."; reduced motion shows it all filled and still
- both: no horizontal page scroll (document scrollWidth <= innerWidth) at any step, no text under
  15px except the capsule counts, no link or button under 44x44, no console errors or page errors
- development only: the lean (1 a day, 60 days, no studies) and full (6 a day, 14 studies) fixtures

Pictures: scripts/qa/out/rd-<run>-<nn>-<name>.png (viewport shots; full-page shots break svh
layouts), and rd-<run>-sheet.png, the shots of a run side by side.

    python -X utf8 scripts/qa/qa_research_daily.py http://localhost:3007
    python -X utf8 scripts/qa/qa_research_daily.py http://localhost:3010 --product=green-bee-propolis

The numbers above are NuriCell's; --product=<slug> checks another product against its own (PRODUCTS).
"""
import os
import sys
import time

from PIL import Image
from playwright.sync_api import sync_playwright

POSITIONAL = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = (POSITIONAL[0] if POSITIONAL else "http://localhost:3007").rstrip("/")
SLUG = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--product=")), "nuricell")
URL = f"{BASE}/products/{SLUG}"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)
# Per product: the research note, how many studies, and the month (days, capsules a day, title).
PRODUCTS = {
    "nuricell": {"honesty": "These studies are about NuriCell’s ingredients, not the finished product.",
                 "studies": 7, "days": 30, "pills": 3, "title": "One bottle, one month."},
    "green-bee-propolis": {"honesty": "These studies are about propolis, not the finished product.",
                           "studies": 7, "days": 60, "pills": 1, "title": "One bottle, two months."},
}
HONESTY = PRODUCTS[SLUG]["honesty"]
STUDIES = PRODUCTS[SLUG]["studies"]
DAYS = PRODUCTS[SLUG]["days"]
PILLS = PRODUCTS[SLUG]["pills"]
TITLE = PRODUCTS[SLUG]["title"]
COUNT = f"{DAYS * PILLS} capsules · {DAYS} days"
passed = failed = 0
dev_notes = set()


def check(name, ok, detail=""):
    global passed, failed
    passed += bool(ok)
    failed += not ok
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))


def open_page(browser, w, h, reduced=False, fixture=None):
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
    url = URL + (f"?chapters-fixture={fixture}" if fixture else "")
    response = page.goto(url, wait_until="networkidle")
    if not response or response.status >= 500:
        raise RuntimeError(f"page answered {response.status if response else 'nothing'}")
    page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
    page.wait_for_selector("[data-chapter='research'], [data-chapter='daily']")
    page.wait_for_timeout(2800)
    return ctx, page, problems


def glide(page, y, steps=10):
    """Scroll like a person, a little at a time, so scrubbed scenes follow."""
    current = page.evaluate("scrollY")
    for s in range(1, steps + 1):
        page.evaluate(f"window.scrollTo({{top: {current + (y - current) * s / steps}, behavior: 'instant'}})")
        page.wait_for_timeout(35)


def jump(page, y):
    page.evaluate(f"window.scrollTo({{top: {y}, behavior: 'instant'}})")


class Shots:
    def __init__(self, run):
        self.run, self.paths = run, []

    def take(self, page, name):
        path = os.path.join(OUT, f"rd-{self.run}-{len(self.paths):02d}-{name}.png")
        page.screenshot(path=path)
        self.paths.append(path)
        return path

    def sheet(self, scale):
        if not self.paths:
            return None
        images = [Image.open(p).convert("RGB") for p in self.paths]
        images = [im.resize((int(im.width * scale), int(im.height * scale))) for im in images]
        per_row = 4
        rows = [images[i:i + per_row] for i in range(0, len(images), per_row)]
        width = max(sum(im.width + 12 for im in row) for row in rows)
        height = sum(max(im.height for im in row) + 12 for row in rows)
        sheet = Image.new("RGB", (width, height), (40, 44, 52))
        y = 0
        for row in rows:
            x = 0
            for im in row:
                sheet.paste(im, (x, y))
                x += im.width + 12
            y += max(im.height for im in row) + 12
        path = os.path.join(OUT, f"rd-{self.run}-sheet.png")
        sheet.save(path)
        return path


def box(page, chapter):
    return page.evaluate(f"""(() => {{ const s = document.querySelector('[data-chapter="{chapter}"]');
      return s ? {{ top: Math.round(s.getBoundingClientRect().top + scrollY), height: s.offsetHeight }} : null; }})()""")


NO_SIDEWAYS = "document.documentElement.scrollWidth <= innerWidth"

# The research chapter as it stands on screen: whether it is pinned, whether the heading and the
# honesty line are on screen and uncovered, and which study cards are fully in view.
RESEARCH = """(() => {
  const s = document.querySelector('[data-chapter="research"]');
  const stage = s.firstElementChild;
  const win = s.querySelector('[data-window]');
  const wide = innerWidth > 900;
  const wr = win.getBoundingClientRect();
  // The window's soft edges: 16px at the left and 48px at the right on wide screens. Two pixels'
  // grace: the pinned stage's sub-pixel scroll can leave the first card 1.4px into the fade.
  const left = Math.max(0, wr.left + (wide ? 16 : 0)) - 2;
  const right = Math.min(innerWidth, wr.right - (wide ? 48 : 0)) + 2;
  const opacity = el => { let o = 1; for (let a = el; a && a !== document.body; a = a.parentElement) o *= +getComputedStyle(a).opacity; return o; };
  const shown = el => {
    const r = el.getBoundingClientRect();
    if (r.top < 0 || r.bottom > innerHeight || r.left < 0 || r.right > innerWidth || !r.width) return false;
    const hit = document.elementFromPoint(r.left + Math.min(20, r.width / 2), r.top + r.height / 2);
    return !!hit && (hit === el || el.contains(hit)) && opacity(el) > 0.99;
  };
  const heading = s.querySelector('h2');
  const honesty = s.querySelector('[data-head] p');
  const cards = [...s.querySelectorAll('[data-study]')].map(li => {
    const r = li.getBoundingClientRect();
    // 0.98: a jump can land at the tail of the chapter's scrubbed fade (0.987-0.992), invisible.
    return r.left >= left && r.right <= right && r.top >= 0 && r.bottom <= innerHeight && opacity(li) > 0.98;
  });
  const sr = s.getBoundingClientRect();
  return {
    pinned: getComputedStyle(stage).position === 'sticky',
    inPin: sr.top <= 0.5 && sr.bottom >= innerHeight - 0.5,
    stageTop: Math.round(stage.getBoundingClientRect().top),
    heading: shown(heading), honesty: shown(honesty), honestyText: honesty.textContent,
    cards, lit: s.querySelectorAll('[data-study][data-lit="true"]').length,
    current: [...s.querySelectorAll('[data-study]')].findIndex(li => li.dataset.current === 'true'),
    years: [...s.querySelectorAll('[data-study] p:first-child')].map(p => p.textContent.trim()),
    scrollLeft: Math.round(win.scrollLeft), scrollMax: win.scrollWidth - win.clientWidth,
    snap: getComputedStyle(win).scrollSnapType, overflowX: getComputedStyle(win).overflowX,
    sideways: document.documentElement.scrollWidth <= innerWidth,
  };
})()"""

DAILY = """(() => {
  const s = document.querySelector('[data-chapter="daily"]');
  const stage = s.firstElementChild;
  const count = s.querySelector('[class*="count"] span[aria-hidden]');
  const then = s.querySelector('[class*="then"]');
  const sr = s.getBoundingClientRect();
  const grid = s.querySelector('ol');
  const gr = grid ? grid.getBoundingClientRect() : null;
  return {
    days: s.querySelectorAll('ol > li').length,
    filled: s.querySelectorAll('ol > li[data-filled="true"]').length,
    pills: s.querySelector('ol > li') ? s.querySelector('ol > li').querySelectorAll('[class*="pill"]:not([class*="pills"])').length : 0,
    today: [...s.querySelectorAll('ol > li')].findIndex(li => li.dataset.today === 'true'),
    count: count ? count.textContent : null,
    thenOpacity: then ? +getComputedStyle(then).opacity : null,
    title: s.querySelector('h2').textContent,
    pinned: getComputedStyle(stage).position === 'sticky',
    inPin: sr.top <= 0.5 && sr.bottom >= innerHeight - 0.5,
    gridInView: gr ? gr.top >= 0 && gr.bottom <= innerHeight : false,
    sideways: document.documentElement.scrollWidth <= innerWidth,
  };
})()"""

SMALL = """((ids) => {
  const bad = [], tiny = [];
  for (const id of ids) {
    const s = document.querySelector(`[data-chapter="${id}"]`);
    if (!s) continue;
    const walker = document.createTreeWalker(s, NodeFilter.SHOW_TEXT);
    let node;
    while ((node = walker.nextNode())) {
      const text = node.nodeValue.trim(), el = node.parentElement;
      if (!text || !el || el.closest('[class*="srOnly"]')) continue;
      const r = el.getBoundingClientRect();
      if (r.width <= 1 || r.height <= 1) continue;
      const size = parseFloat(getComputedStyle(el).fontSize);
      if (size < 15) bad.push(size + 'px "' + text.slice(0, 30) + '"');
    }
    for (const el of s.querySelectorAll('a, button')) {
      const r = el.getBoundingClientRect();
      if (!r.width || getComputedStyle(el).display === 'none') continue;
      if (r.width < 44 || r.height < 44) tiny.push(Math.round(r.width) + 'x' + Math.round(r.height) + ' ' + el.textContent.trim().slice(0, 20));
    }
  }
  return { bad, tiny };
})"""


def research_view(page, label, w, h, reduced, shots):
    where = box(page, "research")
    phone = w <= 900
    expect_pin = not reduced and not phone
    state = page.evaluate(RESEARCH)
    count = len(state["cards"])
    years = [int(y) for y in state["years"]]
    check(f"{label} research: {count} studies, oldest first", count == STUDIES and years == sorted(years), str(state["years"]))
    check(f"{label} research: honesty line is the product's research note", HONESTY in state["honestyText"], state["honestyText"][:60])
    links = page.evaluate("""[...document.querySelectorAll('[data-chapter="research"] [data-study] a')].map(a => [a.target, a.rel, a.href.startsWith('https://')])""")
    check(f"{label} research: every study links out, new tab, rel=noopener", len(links) == STUDIES and all(t == "_blank" and "noopener" in r and ok for t, r, ok in links), str(links[:1]))

    seen = [False] * count
    heading_ok, sideways_ok, lit_trace, stops = [], [], [], []
    if expect_pin:
        # Step through the pinned stage from its top to its bottom, and a little past.
        n = 22
        for i in range(n + 1):
            y = where["top"] + (where["height"] - h) * i / n
            glide(page, y, steps=4)
            page.wait_for_timeout(700)
            s = page.evaluate(RESEARCH)
            stops.append(s)
            seen = [a or b for a, b in zip(seen, s["cards"])]
            if s["inPin"]:
                heading_ok.append((i, s["heading"] and s["honesty"]))
            sideways_ok.append(s["sideways"])
            lit_trace.append(s["lit"])
            if i in (0, 5, 11, 17, n):
                shots.take(page, f"research-{i:02d}")
        pinned = [s for s in stops if s["inPin"]]
        check(f"{label} research: the stage is pinned (sticky, top 0) all through the chapter",
              pinned and all(s["pinned"] and abs(s["stageTop"]) <= 1 for s in pinned), str([(s["pinned"], s["stageTop"]) for s in pinned[:3]]))
        check(f"{label} research: the gold line lights the years one by one (1 at the start, all {STUDIES} at the end, never fewer on the way down)",
              lit_trace[0] == 1 and lit_trace[-1] == count and all(b >= a for a, b in zip(lit_trace, lit_trace[1:])), str(lit_trace))
        # Scroll fast back to the start: the timeline and the lights settle back.
        jump(page, where["top"] + 2)
        page.wait_for_timeout(1400)
        back = page.evaluate(RESEARCH)
        check(f"{label} research: a fast jump back to the start settles (first card in view, 1 year lit)",
              back["cards"][0] and back["lit"] == 1, f"cards={back['cards']} lit={back['lit']}")
    else:
        # The list: scroll it sideways, study by study.
        jump(page, where["top"] + int(where["height"] * 0.5) - h // 2)
        page.wait_for_timeout(1500)
        s = page.evaluate(RESEARCH)
        check(f"{label} research: nothing pinned; a sideways list with scroll-snap",
              not s["pinned"] and s["overflowX"] == "auto" and "x" in s["snap"] and "mandatory" in s["snap"], f"pinned={s['pinned']} overflow={s['overflowX']} snap={s['snap']}")
        heading_top = page.evaluate("document.querySelector('[data-chapter=\"research\"] h2').getBoundingClientRect().top + scrollY")
        list_top = page.evaluate("document.querySelector('[data-chapter=\"research\"] [data-window]').getBoundingClientRect().top + scrollY")
        # A view with the heading, the honesty line and the first study, if the screen holds them.
        jump(page, int(heading_top) - 24)
        page.wait_for_timeout(900)
        top_state = page.evaluate(RESEARCH)
        heading_ok.append((0, top_state["heading"] and top_state["honesty"]))
        shots.take(page, "research-top")
        jump(page, int(list_top) - 110)
        page.wait_for_timeout(900)
        # The first study not wholly in view shows a part of itself at the right edge.
        peek = page.evaluate("""(() => { const win = document.querySelector('[data-chapter="research"] [data-window]');
          const r = win.getBoundingClientRect(); const edge = Math.min(innerWidth, r.right);
          const next = [...win.querySelectorAll('[data-study]')].map(li => li.getBoundingClientRect()).find(b => b.right > edge + 1);
          return next ? { index: 0, peek: Math.round(edge - next.left), width: Math.round(next.width) } : null; })()""")
        check(f"{label} research: the next study peeks in at the right", peek and 12 <= peek["peek"] < peek["width"] * 0.7, str(peek))
        steps_needed = count + 1
        for i in range(steps_needed):
            s = page.evaluate(RESEARCH)
            seen = [a or b for a, b in zip(seen, s["cards"])]
            sideways_ok.append(s["sideways"])
            lit_trace.append(s["lit"])
            if i in (0, 3, count):
                shots.take(page, f"research-list-{i}")
            page.evaluate("""(() => { const win = document.querySelector('[data-chapter="research"] [data-window]');
              const item = win.querySelector('[data-study]'); const gap = parseFloat(getComputedStyle(item.parentElement).columnGap) || 0;
              win.scrollBy({ left: item.offsetWidth + gap, behavior: 'instant' }); })()""")
            page.wait_for_timeout(700)
        if not reduced:
            check(f"{label} research: swiping fills the gold line and lights the years in turn",
                  lit_trace[0] == 1 and lit_trace[-1] == count, str(lit_trace))
        else:
            check(f"{label} research: reduced motion: every year lit, the gold line full",
                  all(v == count for v in lit_trace), str(lit_trace))
        if not phone:
            # The mouse buttons step the list.
            page.evaluate("document.querySelector('[data-chapter=\"research\"] [data-window]').scrollLeft = 0")
            page.wait_for_timeout(300)
            later = page.locator("[data-chapter='research'] button", has_text="Later studies")
            later.click()
            page.wait_for_timeout(900)
            moved = page.evaluate("document.querySelector('[data-chapter=\"research\"] [data-window]').scrollLeft")
            check(f"{label} research: the 'Later studies' button steps the list", moved > 100, f"scrollLeft={moved}")
    check(f"{label} research: every study card is fully in view at some point", all(seen), str(seen))
    check(f"{label} research: heading and honesty line on screen and uncovered at every step",
          heading_ok and all(ok for _, ok in heading_ok), str([i for i, ok in heading_ok if not ok][:6]) or str(len(heading_ok)))
    check(f"{label} research: no horizontal page scroll at any step", all(sideways_ok), str(sideways_ok.count(False)))

    # The keyboard: Tab through every study's link; each brings its card fully into view.
    jump(page, where["top"] - h)
    page.wait_for_timeout(600)
    page.evaluate("document.querySelector('[data-chapter=\"research\"]').focus({ preventScroll: true })")
    results = []
    for i in range(count):
        page.keyboard.press("Tab")
        page.wait_for_timeout(1100)
        active = page.evaluate("""(() => { const a = document.activeElement; const li = a && a.closest('[data-study]');
          return li && a.tagName === 'A' ? +li.dataset.study : -1; })()""")
        s = page.evaluate(RESEARCH)
        results.append((i, active, s["cards"][i] if 0 <= active < count else False, s["heading"] and s["honesty"], s["sideways"]))
        if i in (0, count - 1):
            shots.take(page, f"research-tab-{i}")
    bad = [r for r in results if r[1] != r[0] or not r[2] or not r[4]]
    check(f"{label} research: Tab reaches each study's link in turn and brings its card fully into view",
          not bad, str(bad[:3]))
    if expect_pin:
        check(f"{label} research: heading and honesty line still on screen while tabbing",
              all(r[3] for r in results), str([r[0] for r in results if not r[3]]))


def daily_view(page, label, w, h, reduced, shots):
    where = box(page, "daily")
    expect_pin = not reduced and h >= 600
    first = page.evaluate(DAILY)
    check(f"{label} daily: the title and {DAYS} days, {PILLS} capsules each", first["title"] == TITLE and first["days"] == DAYS and first["pills"] == PILLS,
          f"title={first['title']!r} days={first['days']} pills={first['pills']}")
    trace, sideways, inview = [], [], []
    if expect_pin:
        jump(page, where["top"] - h)
        page.wait_for_timeout(700)
        n = 14
        for i in range(n + 1):
            y = where["top"] - h * 0.3 + (where["height"] - h * 0.7) * i / n
            glide(page, y, steps=4)
            page.wait_for_timeout(600)
            s = page.evaluate(DAILY)
            trace.append(s["filled"])
            sideways.append(s["sideways"])
            if s["inPin"]:
                inview.append(s["gridInView"] and s["pinned"])
            if i in (3, 7, 10, n):
                shots.take(page, f"daily-{i:02d}")
        end = page.evaluate(DAILY)
        check(f"{label} daily: the month fills day by day as you scroll down (never goes back)",
              trace[0] < 10 and all(b >= a for a, b in zip(trace, trace[1:])) and len(set(trace)) >= 6, str(trace))
        check(f"{label} daily: it ends full: {DAYS} days, '{COUNT}', 'Then a new bottle.' shown, day {DAYS} ringed",
              end["filled"] == DAYS and end["count"] == COUNT and end["thenOpacity"] > 0.99 and end["today"] == DAYS - 1,
              f"filled={end['filled']} count={end['count']!r} then={end['thenOpacity']} today={end['today']}")
        check(f"{label} daily: pinned, and the whole month on screen while pinned", inview and all(inview), f"{inview.count(False)} of {len(inview)} off")
        # Back up a little: fewer days. Then fast jumps both ways land right.
        glide(page, where["top"] + (where["height"] - h) * 0.35, steps=6)
        page.wait_for_timeout(700)
        middle = page.evaluate(DAILY)
        jump(page, where["top"] + where["height"] - h)
        page.wait_for_timeout(700)
        bottom = page.evaluate(DAILY)
        jump(page, where["top"] - h)
        page.wait_for_timeout(700)
        top = page.evaluate(DAILY)
        check(f"{label} daily: scrolling back un-fills, fast jumps settle both ways",
              0 < middle["filled"] < DAYS and bottom["filled"] == DAYS and top["filled"] == 0,
              f"middle={middle['filled']} bottom={bottom['filled']} top={top['filled']} ({top['count']!r})")
    else:
        jump(page, where["top"])
        page.wait_for_timeout(800)
        shots.take(page, "daily-top")
        grid_bottom = page.evaluate("document.querySelector('[data-chapter=\"daily\"] ol').getBoundingClientRect().bottom + scrollY")
        jump(page, max(where["top"], int(grid_bottom) - h + 160))
        page.wait_for_timeout(800)
        shots.take(page, "daily-end")
        s = page.evaluate(DAILY)
        sideways.append(s["sideways"])
        check(f"{label} daily: still: the whole month filled, the full count and the last line shown",
              not s["pinned"] and s["filled"] == DAYS and s["count"] == COUNT and s["thenOpacity"] > 0.99,
              f"pinned={s['pinned']} filled={s['filled']} count={s['count']!r} then={s['thenOpacity']}")
    check(f"{label} daily: no horizontal page scroll at any step", all(sideways), str(sideways.count(False)))


def run_view(browser, label, w, h, reduced=False):
    ctx, page, problems = open_page(browser, w, h, reduced)
    shots = Shots(label)
    research_view(page, label, w, h, reduced, shots)
    daily_view(page, label, w, h, reduced, shots)
    small = page.evaluate(SMALL, ["research", "daily"])
    check(f"{label}: no text under 15px and no link or button under 44x44 in these chapters", not small["bad"] and not small["tiny"], f"{small['bad'][:3]} {small['tiny'][:3]}")
    check(f"{label}: no console errors, page errors or failed requests", not problems, str(problems[:3]))
    ctx.close()
    return shots


def run_fixtures(browser):
    """Development only: other products' shapes. lean: 1 capsule a day for 60 days, no studies.
    full: 6 capsules a day, 14 studies."""
    ctx, page, problems = open_page(browser, 1440, 900, fixture="lean")
    if page.locator("[data-chapter='research']").count():
        print("NOTE fixtures skipped: this server ignores ?chapters-fixture (a production build)")
        ctx.close()
        return None
    shots = Shots("fixtures")
    where = box(page, "daily")
    glide(page, where["top"] + where["height"] - 900, steps=12)
    page.wait_for_timeout(1200)
    shots.take(page, "lean-daily-end")
    s = page.evaluate(DAILY)
    check("lean fixture: 'One bottle, two months.', 60 days, 1 capsule each, fills to '60 capsules · 60 days'",
          s["title"] == "One bottle, two months." and s["days"] == 60 and s["pills"] == 1 and s["filled"] == 60 and s["count"] == "60 capsules · 60 days",
          f"{s['title']!r} days={s['days']} pills={s['pills']} filled={s['filled']} {s['count']!r}")
    shape = page.evaluate("""(() => { const p = document.querySelector('[data-chapter="daily"] ol > li [class*="pill"]:not([class*="pills"])');
      const r = p.getBoundingClientRect(); return r.height / r.width; })()""")
    check("lean fixture: a lone capsule keeps a capsule's shape (about 2.5 times as tall as wide)", 2.3 <= shape <= 2.7, f"{shape:.2f}")
    check("lean fixture: no research chapter, no errors", page.locator("[data-chapter='research']").count() == 0 and not problems, str(problems[:2]))
    ctx.close()

    for w, h, run in ((1440, 900, "full-desk"), (390, 844, "full-phone")):
        ctx, page, problems = open_page(browser, w, h, fixture="full")
        where = box(page, "research")
        seen = [False] * (2 * STUDIES)
        if w > 900:
            for i in range(31):
                glide(page, where["top"] + (where["height"] - h) * i / 30, steps=3)
                page.wait_for_timeout(450)
                seen = [a or b for a, b in zip(seen, page.evaluate(RESEARCH)["cards"])]
                if i in (15,):
                    shots.take(page, f"{run}-research")
        else:
            list_top = page.evaluate("document.querySelector('[data-chapter=\"research\"] [data-window]').getBoundingClientRect().top + scrollY")
            jump(page, int(list_top) - 110)
            page.wait_for_timeout(900)
            for i in range(15):
                seen = [a or b for a, b in zip(seen, page.evaluate(RESEARCH)["cards"])]
                page.evaluate("""(() => { const win = document.querySelector('[data-chapter="research"] [data-window]');
                  const item = win.querySelector('[data-study]'); win.scrollBy({ left: item.offsetWidth + 28, behavior: 'instant' }); })()""")
                page.wait_for_timeout(500)
            shots.take(page, f"{run}-research")
        d = box(page, "daily")
        glide(page, d["top"] + d["height"] - h, steps=10)
        page.wait_for_timeout(1200)
        shots.take(page, f"{run}-daily")
        s = page.evaluate(DAILY)
        sideways = page.evaluate(NO_SIDEWAYS)
        check(f"{run} fixture: all {2 * STUDIES} studies come fully into view; 6 capsules a day; no sideways scroll; no errors",
              all(seen) and s["pills"] == 6 and s["filled"] == DAYS and sideways and not problems,
              f"seen={seen.count(True)}/{2 * STUDIES} pills={s['pills']} filled={s['filled']} sideways={sideways} {problems[:2]}")
        ctx.close()
    return shots


def attempt(fn, *args):
    """Other agents save files while this runs; a crash from a mid-run reload gets one retry."""
    try:
        return fn(*args)
    except Exception as error:  # noqa: BLE001
        print(f"RETRY after: {str(error)[:200]}")
        time.sleep(4)
        return fn(*args)


with sync_playwright() as p:
    browser = p.chromium.launch(args=["--use-gl=angle", "--use-angle=d3d11", "--enable-gpu", "--ignore-gpu-blocklist"])
    sheets = []
    for label, (w, h), reduced in (
        ("desk", (1440, 900), False),
        ("phone", (390, 844), False),
        ("still-desk", (1440, 900), True),
        ("still-phone", (390, 844), True),
    ):
        shots = attempt(run_view, browser, label, w, h, reduced)
        sheets.append(shots.sheet(0.5 if w > 1000 else 0.7))
    fixture_shots = attempt(run_fixtures, browser)
    if fixture_shots:
        sheets.append(fixture_shots.sheet(0.5))
    browser.close()

print("\nSheets:", *[s for s in sheets if s], sep="\n  ")
if dev_notes:
    print("\nNOTE (not counted): the dev server preloads a missing chunk on the product route:", *sorted(dev_notes), sep="\n  ")
print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)

"""QA for the Science page (/science?look=a|b|c): the three openings, the shared sections, phones,
reduced motion. Viewport pictures land in scripts/qa/out/science/ (full-page shots break the svh
layouts, so the script steps through the page one screen at a time).

python -X utf8 scripts/qa/qa_science.py http://localhost:3008 d,e,f   (round 2; a,b,c = round 1)
Each round-2 look also has its own script (qa_science_d.py, _e, _f) for its scenes.
"""
import os
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3008"
LOOKS = sys.argv[2].split(",") if len(sys.argv) > 2 else ["d", "e", "f"]
LOCALE = sys.argv[3] if len(sys.argv) > 3 else ""
SHOTS = os.path.join(os.path.dirname(__file__), "out", "science")
os.makedirs(SHOTS, exist_ok=True)
passed = failed = 0


def check(name, ok, detail=""):
    global passed, failed
    passed += bool(ok)
    failed += not ok
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))


def open_page(browser, w, h, url, reduced=False):
    ctx = browser.new_context(
        viewport={"width": w, "height": h},
        reduced_motion="reduce" if reduced else "no-preference",
        device_scale_factor=1,
    )
    page = ctx.new_page()
    problems = []
    page.on("pageerror", lambda e: problems.append(f"pageerror {e}"))
    page.on("console", lambda m: problems.append(f"console {m.text[:160]}") if m.type == "error" else None)
    page.on("response", lambda r: problems.append(f"{r.status} {r.url[-60:]}") if r.status >= 400 and "favicon" not in r.url else None)
    page.goto(url, wait_until="networkidle")
    page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
    return ctx, page, problems


def walk(page, y, steps=10):
    current = page.evaluate("scrollY")
    for s in range(1, steps + 1):
        page.evaluate(f"window.scrollTo(0, {current + (y - current) * s / steps})")
        page.wait_for_timeout(40)


def top_of(page, selector):
    return page.evaluate(f"(() => {{ const e = document.querySelector('{selector}'); return e ? e.getBoundingClientRect().top + scrollY : -1; }})()")


CLIPPED = """(() => {
  // Words cut off at the side of the screen (the page itself may not scroll sideways, but a
  // too-wide box inside it can still hide text). The sideways path in look B is exempt.
  const out = [];
  for (const el of document.querySelectorAll('main h1, main h2, main h3, main p, main button, main a')) {
    if (el.closest('[data-track]') || el.closest('[aria-hidden="true"]')) continue;
    const r = el.getBoundingClientRect();
    if (!r.width || r.bottom < 0 || r.top > innerHeight) continue;
    const style = getComputedStyle(el);
    if (style.visibility === 'hidden' || +style.opacity === 0) continue;
    if (r.left < -1 || r.right > innerWidth + 1) out.push(el.textContent.trim().slice(0, 40));
  }
  return out;
})()"""
clipped_seen = []


def shoot(page, name):
    page.screenshot(path=os.path.join(SHOTS, name + ".png"))
    clipped_seen.extend(f"{name}: {text}" for text in page.evaluate(CLIPPED))


def overflow(page):
    return page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")


COMMON = """(() => {
  const img = document.querySelector('#scientists img');
  return {
    h1: document.querySelector('h1')?.textContent.trim(),
    photo: img ? img.naturalWidth : 0,
    sections: ['#research', '#health', '#ask'].map(s => !!document.querySelector(s)),
    rows: document.querySelectorAll('#research details').length,
    cards: document.querySelectorAll('#research a[class*=card]').length,
    doors: document.querySelectorAll('#health article').length,
  };
})()"""
ROUND_TWO = {"d", "e", "f"}

with sync_playwright() as p:
    browser = p.chromium.launch()
    prefix = f"/{LOCALE}" if LOCALE else ""
    for look in LOOKS:
        for label, (w, h) in {"desk": (1440, 900), "phone": (390, 844)}.items():
            tag = f"{look}-{label}{'-' + LOCALE if LOCALE else ''}"
            ctx, page, problems = open_page(browser, w, h, f"{BASE}{prefix}/science?look={look}")
            page.wait_for_timeout(2800)
            info = page.evaluate(COMMON)
            research_ok = info["cards"] == 3 and info["rows"] == 0 if look in ROUND_TWO else info["rows"] >= 15
            check(f"{tag}: opening, photo, shared sections render",
                  bool(info["h1"]) and info["photo"] > 0 and all(info["sections"]) and research_ok and info["doors"] == 3,
                  str(info))
            if look in ROUND_TWO:
                # Three key studies first; "See all" opens the full list of 36 and closes again.
                page.evaluate("document.querySelector('#research').scrollIntoView()")
                more = page.locator("#research button[aria-expanded]").first
                more.click()
                page.wait_for_timeout(400)
                opened = page.evaluate("document.querySelectorAll('#research details').length")
                more.click()
                page.wait_for_timeout(300)
                shut = page.evaluate("document.querySelectorAll('#research details').length")
                check(f"{tag}: three key studies; 'See all' opens all 36 and closes", opened == 36 and shut == 0, f"open={opened} closed={shut}")
                page.evaluate("window.scrollTo(0, 0)")
                page.wait_for_timeout(600)
            shoot(page, f"{tag}-00")

            # "Read his story" opens the story panel; its close button shuts it.
            page.get_by_role("button", name="Read his story").first.click()
            page.wait_for_timeout(500)
            opened = page.evaluate("(() => { const d = document.querySelector('dialog'); return d.open && d.textContent.includes('Okayama'); })()")
            if label == "desk":
                shoot(page, f"{tag}-story")
            page.get_by_role("button", name="Close details").click()
            page.wait_for_timeout(300)
            closed = page.evaluate("!document.querySelector('dialog').open")
            check(f"{tag}: 'Read his story' opens the story and closes again", opened and closed, f"opened={opened} closed={closed}")
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(400)

            # Step through the opening one screen at a time.
            research = top_of(page, "#research")
            y, n = 0, 1
            while y + h * 0.85 < research and n < 30:
                y += h * 0.85
                walk(page, y)
                page.wait_for_timeout(1100)
                shoot(page, f"{tag}-{n:02d}")
                n += 1

            if look == "a":
                blur = page.evaluate("getComputedStyle(document.querySelector('[data-photo]')).filter")
                count = page.evaluate("document.querySelector('[data-count]')?.textContent")
                check(f"{tag}: photo in focus after scrolling; 280 counted up", ("blur(0px)" in blur or blur == "none") and count == "280", f"filter={blur} count={count}")
            if look == "b":
                if label == "desk":
                    # Measure where the path starts from the pin's spacer (the pinned element itself
                    # reports top 0 while fixed), then walk along it from before the start.
                    journey = page.evaluate("(() => { const j = document.querySelector('[data-journey]'); const s = j.parentElement.classList.contains('pin-spacer') ? j.parentElement : j; return s.getBoundingClientRect().top + scrollY; })()")
                    span = page.evaluate("document.querySelector('[data-track]').scrollWidth - innerWidth")
                    walk(page, journey - h)
                    page.wait_for_timeout(900)
                    xs, lit = [], []
                    for step in (0.02, 0.3, 0.6, 0.99):
                        walk(page, journey + step * span)
                        page.wait_for_timeout(1300)
                        xs.append(round(page.evaluate("new DOMMatrix(getComputedStyle(document.querySelector('[data-track]')).transform).m41")))
                        lit.append(page.evaluate("document.querySelectorAll('[data-lit]').length"))
                    slides = all(a > b for a, b in zip(xs, xs[1:]))
                    lights = lit == sorted(lit) and lit[0] < lit[-1] and lit[-1] >= 5
                    check(f"{tag}: the path pins and slides sideways; stops light in order", slides and xs[-1] < -500 and lights, f"x={xs} lit={lit}")
                else:
                    x = page.evaluate("new DOMMatrix(getComputedStyle(document.querySelector('[data-track]')).transform).m41")
                    check(f"{tag}: phones get the path top to bottom (no sideways slide)", x == 0, f"x={x}")
            if look == "c":
                track = top_of(page, "[data-cell-track]")
                track_h = page.evaluate("document.querySelector('[data-cell-track]').offsetHeight")
                chapters, tones = [], []
                for at in (0.12, 0.5, 0.9):
                    walk(page, track + (track_h - h) * at)
                    page.wait_for_timeout(1300)
                    chapters.append(page.evaluate("[...document.querySelectorAll('[aria-pressed]')].findIndex(b => b.getAttribute('aria-pressed') === 'true')"))
                    shoot(page, f"{tag}-cell-{int(at * 100)}")
                header_dark = page.evaluate("getComputedStyle(document.querySelector('header')).backgroundColor")
                walk(page, top_of(page, "#research") + 40)
                page.wait_for_timeout(900)
                header_light = page.evaluate("getComputedStyle(document.querySelector('header')).backgroundColor")
                check(f"{tag}: the cell steps through energy, balance, aging; header turns light over the research",
                      chapters == [0, 1, 2] and header_dark != header_light, f"chapters={chapters} header {header_dark} -> {header_light}")

            # The shared sections, one screen each.
            for part in ("research", "health", "ask"):
                walk(page, top_of(page, f"#{part}"))
                page.wait_for_timeout(1000)
                shoot(page, f"{tag}-z-{part}")
            walk(page, page.evaluate("document.documentElement.scrollHeight"))
            page.wait_for_timeout(600)
            shoot(page, f"{tag}-z-footer")
            ov = overflow(page)
            check(f"{tag}: no sideways scroll, no errors", ov == 0 and not problems, f"overflow={ov} {problems[:3]}")
            mine = [c for c in clipped_seen if c.startswith(tag + "-")]
            check(f"{tag}: no words cut off at the screen edge", not mine, "; ".join(mine[:4]))
            ctx.close()

        # Reduced motion: everything readable without animation.
        ctx, page, problems = open_page(browser, 1440, 900, f"{BASE}{prefix}/science?look={look}", reduced=True)
        page.wait_for_timeout(800)
        state = page.evaluate("""(() => ({
          chapters: [...document.querySelectorAll('[class*=chapter]')].filter(e => +getComputedStyle(e).opacity > 0.9).length,
          lit: getComputedStyle(document.querySelector('[data-stop] [class*=below]') || document.body).opacity,
          blur: document.querySelector('[data-photo]') ? getComputedStyle(document.querySelector('[data-photo]')).filter : 'none',
          // Every heading and paragraph in the opening is visible (nothing left at opacity 0).
          hidden: [...document.querySelectorAll('#scientists h1, #scientists h2, #scientists h3, #scientists p')]
            .filter(e => { let n = e; while (n && n !== document.body) { if (+getComputedStyle(n).opacity < 0.5) return true; n = n.parentElement; } return false; })
            .map(e => e.textContent.trim().slice(0, 30)),
        }))()""")
        ok = {"a": state["blur"] == "none", "b": state["lit"] == "1", "c": state["chapters"] >= 3}.get(look, not state["hidden"])
        check(f"{look}-reduced: calm version shows everything", ok and not problems, f"{state} {problems[:2]}")
        walk(page, top_of(page, "#scientists") + 900)
        page.wait_for_timeout(300)
        shoot(page, f"{look}-reduced-01")
        ctx.close()
    browser.close()

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)

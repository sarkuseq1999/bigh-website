"""Page-wide QA for the Science page (/science, look D "Golden hour", Mo's pick of September 25):
the opening renders, three key studies and "See all", the story panel, the shared sections, no
sideways scroll, no errors, no words cut off, and a calm reduced-motion version. Look D's own scenes
(film strip, focus, counters) are checked by qa_science_d.py.

python -X utf8 scripts/qa/qa_science.py http://localhost:3008 [locale]
The earlier multi-look version is reference/science-page/looks/qa/qa_science_rounds.py.
"""
import os
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3008"
LOCALE = sys.argv[2] if len(sys.argv) > 2 else ""
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

with sync_playwright() as p:
    browser = p.chromium.launch()
    url = f"{BASE}{'/' + LOCALE if LOCALE else ''}/science"
    for label, (w, h) in {"desk": (1440, 900), "laptop": (1280, 720), "phone": (390, 844)}.items():
        tag = f"{label}{'-' + LOCALE if LOCALE else ''}"
        ctx, page, problems = open_page(browser, w, h, url)
        page.wait_for_timeout(2800)
        info = page.evaluate(COMMON)
        check(f"{tag}: opening, photo, three key studies, shared sections render",
              bool(info["h1"]) and info["photo"] > 0 and all(info["sections"]) and info["cards"] == 3
              and info["rows"] == 0 and info["doors"] == 3, str(info))
        shoot(page, f"{tag}-00")

        # Three key studies first; "See all" opens the full list of 36 and closes again.
        page.evaluate("document.querySelector('#research').scrollIntoView()")
        more = page.locator("#research button[aria-expanded]").first
        more.click()
        page.wait_for_timeout(400)
        opened = page.evaluate("document.querySelectorAll('#research details').length")
        more.click()
        page.wait_for_timeout(300)
        shut = page.evaluate("document.querySelectorAll('#research details').length")
        check(f"{tag}: 'See all' opens all 36 sources and closes", opened == 36 and shut == 0, f"open={opened} closed={shut}")

        # "Read his story" opens the story panel; its close button shuts it.
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(500)
        page.get_by_role("button", name="Read his story").first.click()
        page.wait_for_timeout(500)
        # Open, with his photo and at least three paragraphs of his story (in any language).
        story = page.evaluate("(() => { const d = document.querySelector('dialog'); return d.open && !!d.querySelector('img') && d.querySelectorAll('p').length >= 4; })()")
        if label == "desk":
            shoot(page, f"{tag}-story")
        # The close button's label is translated, so find it by place, not by its English name.
        page.locator("dialog button").first.click()
        page.wait_for_timeout(300)
        closed = page.evaluate("!document.querySelector('dialog').open")
        check(f"{tag}: 'Read his story' opens and closes", story and closed, f"opened={story} closed={closed}")

        # Step through the whole page one screen at a time (pictures + cut-off words).
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(500)
        end = page.evaluate("document.documentElement.scrollHeight") - h
        y, n = 0, 1
        while y < end and n < 60:
            y = min(end, y + h * 0.85)
            walk(page, y)
            page.wait_for_timeout(900)
            shoot(page, f"{tag}-{n:02d}")
            n += 1
        ov = overflow(page)
        check(f"{tag}: no sideways scroll, no errors", ov == 0 and not problems, f"overflow={ov} {problems[:3]}")
        mine = [c for c in clipped_seen if c.startswith(tag + "-")]
        check(f"{tag}: no words cut off at the screen edge", not mine, "; ".join(mine[:4]))
        ctx.close()

    # Reduced motion: everything readable without animation.
    ctx, page, problems = open_page(browser, 1440, 900, url, reduced=True)
    page.wait_for_timeout(800)
    hidden = page.evaluate("""[...document.querySelectorAll('#scientists h1, #scientists h2, #scientists h3, #scientists p')]
      .filter(e => { let n = e; while (n && n !== document.body) { if (+getComputedStyle(n).opacity < 0.5) return true; n = n.parentElement; } return false; })
      .map(e => e.textContent.trim().slice(0, 30))""")
    check("reduced motion: every heading and line in the opening is visible", not hidden and not problems, f"{hidden[:4]} {problems[:2]}")
    ctx.close()
    browser.close()

print()
print(f"{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)

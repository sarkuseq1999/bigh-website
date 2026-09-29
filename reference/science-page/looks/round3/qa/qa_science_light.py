"""QA for look A, "Liquid light" (/science?look=light): the liquid light (WebGL) in the hero, the
numerals, the river and Ask BiGH Science; the headline reveal; Dr. Liu's focus pull; the pinned
sideways path whose years fill with light; the formulas; three key studies and "See all" (36); the
health rows that open their renders; the story panel; no sideways scroll, no errors, no words cut
off, nothing stuck invisible; and a calm reduced-motion version.

Real GPU (ANGLE on D3D11). Viewport pictures land in scripts/qa/out/science-light/ (full-page
shots break the svh layouts, so the script steps through the page one screen at a time, and through
the pinned path at several points). Mid-animation frames of the hero are named desk-hero-t*.png.

python -X utf8 scripts/qa/qa_science_light.py http://localhost:3008
"""
import os
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3008"
URL = f"{BASE}/science?look=light"
SHOTS = os.path.join(os.path.dirname(__file__), "out", "science-light")
os.makedirs(SHOTS, exist_ok=True)
GPU = ["--use-gl=angle", "--use-angle=d3d11", "--enable-gpu", "--ignore-gpu-blocklist"]
TITLE = "Meet the scientists behind BiGH’s key formulas."
passed = failed = 0


def check(name, ok, detail=""):
    global passed, failed
    passed += bool(ok)
    failed += not ok
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))


def open_page(browser, w, h, reduced=False):
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
    # Other looks are edited on the same dev server; if the page is mid-rebuild, wait and retry.
    for _ in range(20):
        page.goto(URL, wait_until="networkidle")
        if page.evaluate("!!document.querySelector('[data-hero-light]') && !!document.querySelector('#ask')"):
            break
        page.wait_for_timeout(6000)
    problems.clear()
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
  // Words cut off at the side of the screen. The sideways path is exempt (it slides by design).
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

# Anything still invisible after the whole page has been walked (a reveal that never ran).
STUCK = """(() => [...document.querySelectorAll('main h1, main h2, main h3, main p, main li, main figure, main img')]
  .filter(e => {
    if (e.closest('[aria-hidden="true"]') || e.closest('dialog')) return false;
    if (e.closest('[data-doors]') && e.closest('[class*=doorMedia]')) return false;
    let n = e;
    while (n && n !== document.body) { if (+getComputedStyle(n).opacity < 0.2 || getComputedStyle(n).visibility === 'hidden') return true; n = n.parentElement; }
    return false;
  })
  .map(e => (e.textContent || e.getAttribute('alt') || e.tagName).trim().slice(0, 30)))()"""

COMMON = """(() => {
  const img = document.querySelector('#scientists img');
  const canvases = [...document.querySelectorAll('main canvas')];
  return {
    h1: document.querySelector('h1')?.textContent.trim(),
    photo: img ? img.naturalWidth : 0,
    sections: ['#scientists', '#research', '#health', '#ask'].map(s => !!document.querySelector(s)),
    studies: document.querySelectorAll('#research ol > li').length,
    rows: document.querySelectorAll('#research details').length,
    doors: document.querySelectorAll('#health article').length,
    bottles: document.querySelectorAll('[data-studio] img:not([alt=""]), [class*=shelf] img:not([alt=""])').length,
    numerals: document.querySelectorAll('[data-fill]').length,
    stops: document.querySelectorAll('[data-stop]').length,
    canvases: canvases.length,
  };
})()"""

LIGHTS = "[...document.querySelectorAll('main canvas')].map(c => ({ kind: c.dataset.light || '?', frames: +(c.dataset.frames || 0), renderer: (c.dataset.renderer || '').slice(0, 40) }))"

PATH = """(() => {
  const track = document.querySelector('[data-track]');
  const m = getComputedStyle(track).transform;
  const x = m === 'none' ? 0 : new DOMMatrix(m).m41;
  return {
    sideways: !!document.querySelector('main [data-sideways]'),
    x: Math.round(x),
    reach: track.style.getPropertyValue('--reach'),
    dim: document.querySelectorAll('[data-stop][data-dim]').length,
  };
})()"""


def pin_y(page, fraction):
    return page.evaluate(f"""(() => {{
      const pin = document.querySelector('[data-pin]');
      const spacer = pin.parentElement;
      const top = spacer.getBoundingClientRect().top + scrollY;
      return top + (spacer.offsetHeight - innerHeight) * {fraction};
    }})()""")


def shoot(page, name, clipped):
    page.screenshot(path=os.path.join(SHOTS, name + ".png"))
    clipped.extend(f"{name}: {text}" for text in page.evaluate(CLIPPED))


with sync_playwright() as p:
    browser = p.chromium.launch(args=GPU)

    # The star moment: the headline rising over the light, frame by frame (desktop). A screencast
    # keeps real time (single screenshots are too slow to catch the reveal mid-way).
    ctx, page, problems = open_page(browser, 1440, 900)
    cdp = ctx.new_cdp_session(page)
    frames = []

    def on_frame(event):
        frames.append((event["metadata"]["timestamp"], event["data"]))
        cdp.send("Page.screencastFrameAck", {"sessionId": event["sessionId"]})

    cdp.on("Page.screencastFrame", on_frame)
    cdp.send("Page.startScreencast", {"format": "jpeg", "quality": 85, "everyNthFrame": 1})
    page.reload(wait_until="commit")
    page.wait_for_timeout(5000)
    cdp.send("Page.stopScreencast")
    if frames:
        import base64
        import io
        from PIL import Image
        start = frames[0][0]
        for target in (0.6, 1.0, 1.4, 1.8, 2.4, 3.2, 4.4):
            stamp, data = min(frames, key=lambda f: abs(f[0] - start - target))
            Image.open(io.BytesIO(base64.b64decode(data))).save(
                os.path.join(SHOTS, f"desk-hero-t{int(target * 1000):04d}.png"))
    check("desk: the hero reveal was filmed", len(frames) > 30, f"{len(frames)} frames")
    split = page.evaluate("document.querySelector('[data-hero-title]').dataset.split")
    words = page.evaluate("[...document.querySelectorAll('[data-hero-title] div div, [data-hero-title] div > div')].length")
    check("desk: headline split into masked lines and words, then revealed", split == "done" and words > 3, f"split={split} parts={words}")
    # The pointer stirs the light: frames keep coming while it moves.
    before = page.evaluate("+document.querySelector('[data-hero-light]').dataset.frames")
    for i in range(24):
        page.mouse.move(700 + i * 22, 300 + (i % 6) * 30)
        page.wait_for_timeout(30)
    page.wait_for_timeout(400)
    page.screenshot(path=os.path.join(SHOTS, "desk-hero-stirred.png"))
    after = page.evaluate("+document.querySelector('[data-hero-light]').dataset.frames")
    check("desk: the hero light animates (and keeps drawing while stirred)", after - before > 20, f"frames {before} -> {after}")
    # Scrolling away deepens it.
    walk(page, 450)
    page.wait_for_timeout(700)
    page.screenshot(path=os.path.join(SHOTS, "desk-hero-deepened.png"))
    ctx.close()

    for label, (w, h) in {"desk": (1440, 900), "laptop": (1280, 720), "phone": (390, 844)}.items():
        clipped = []
        ctx, page, problems = open_page(browser, w, h)
        page.wait_for_timeout(3200)
        info = page.evaluate(COMMON)
        check(f"{label}: headline, photo, all sections, 3 studies, 3 doors, 5 bottles, 3 numerals, 5 stops",
              info["h1"] == TITLE and info["photo"] > 0 and all(info["sections"]) and info["studies"] == 3
              and info["rows"] == 0 and info["doors"] == 3 and info["bottles"] == 5 and info["numerals"] == 3
              and info["stops"] == 5, str(info))
        lights = page.evaluate(LIGHTS)
        hero = lights[0] if lights else {}
        check(f"{label}: the liquid light runs on the GPU", hero.get("kind") == "webgl" and hero.get("frames", 0) > 30,
              f"{hero} renderer={hero.get('renderer')}")
        shoot(page, f"{label}-00-hero", clipped)

        # Dr. Liu, his record (280 counts up to 280 and stays).
        walk(page, top_of(page, "#dr-liu") - (84 if w > 1100 else 72))
        page.wait_for_timeout(1900)
        shoot(page, f"{label}-01-liu", clipped)
        if w > 900:
            fit = page.evaluate("""(() => {
              const b = document.querySelector('#dr-liu button').getBoundingClientRect();
              const p = document.querySelector('[data-portrait]').getBoundingClientRect();
              return { button: Math.round(b.bottom), photo: Math.round(p.bottom), h: innerHeight };
            })()""")
            check(f"{label}: Dr. Liu's name, photograph, words and button fit one screen",
                  fit["button"] <= fit["h"] and fit["photo"] <= fit["h"] + 2, str(fit))
            strip = page.evaluate("document.querySelector('[data-strip-light]').dataset.light")
            check(f"{label}: the band of light beside his photograph draws", strip == "webgl", f"strip={strip}")
        walk(page, top_of(page, "[data-fill]") - h * 0.3)
        page.wait_for_timeout(2600)
        shoot(page, f"{label}-02-record", clipped)
        counted = page.evaluate("document.querySelector('[data-count]').textContent")
        fills = page.evaluate("[...document.querySelectorAll('[data-fill]')].map(c => c.dataset.light || '?')")
        check(f"{label}: 280+ counts up and ends on 280; numerals filled with light", counted == "280" and all(k == "webgl" for k in fills),
              f"count={counted} fills={fills}")

        # His path: pinned and sideways on wide screens, top to bottom on phones.
        state = page.evaluate(PATH)
        if w > 900:
            frames = []
            for i, fraction in enumerate((0.0, 0.25, 0.5, 0.75, 1.0)):
                walk(page, pin_y(page, fraction), steps=14)
                page.wait_for_timeout(1300)
                frames.append(page.evaluate(PATH))
                shoot(page, f"{label}-03-path-{i}", clipped)
            xs = [f["x"] for f in frames]
            dims = [f["dim"] for f in frames]
            check(f"{label}: path pins and slides sideways; the light runs to Today",
                  frames[0]["sideways"] and xs[0] > -30 and xs[-1] < xs[2] < xs[0] and dims[0] >= 3 and dims[-1] == 0,
                  f"x={xs} dim={dims} reach={frames[-1]['reach']}")
            river = page.evaluate("document.querySelector('[data-river-light]').dataset.light")
            check(f"{label}: the river and the years show the light", river == "webgl", f"river={river}")
        else:
            lit = page.evaluate("document.querySelector('[data-path]').hasAttribute('data-still')")
            check(f"{label}: path stacks top to bottom (no pin); the years hold a still frame of the light",
                  not state["sideways"] and lit, f"{state} still={lit}")
            walk(page, top_of(page, "[data-pin]"))
            page.wait_for_timeout(900)
            shoot(page, f"{label}-03-path", clipped)

        # The formulas.
        walk(page, top_of(page, "[data-studio]") - (130 if w > 900 else 110))
        page.wait_for_timeout(1300)
        shoot(page, f"{label}-04-formulas", clipped)
        walk(page, top_of(page, "[class*=shelf]") - (h * 0.3 if w > 900 else 90))
        page.wait_for_timeout(1000)
        shoot(page, f"{label}-04-formulas-row", clipped)

        # Three key studies first; "See all" opens the full list of 36 and closes again.
        walk(page, top_of(page, "#research") - 40)
        page.wait_for_timeout(1100)
        shoot(page, f"{label}-05-research", clipped)
        more = page.locator("#research button[aria-expanded]").first
        more.scroll_into_view_if_needed()
        more.click()
        page.wait_for_timeout(500)
        opened = page.evaluate("document.querySelectorAll('#research details').length")
        if label == "desk":
            shoot(page, f"{label}-05-research-all", clipped)
        more.click()
        page.wait_for_timeout(400)
        shut = page.evaluate("document.querySelectorAll('#research details').length")
        check(f"{label}: 'See all' opens all 36 sources and closes", opened == 36 and shut == 0, f"open={opened} closed={shut}")

        # Health explained: the row reached (or hovered) opens its render.
        walk(page, top_of(page, "#health article:nth-of-type(2)") - h * 0.3)
        page.wait_for_timeout(1100)
        active = page.evaluate("[...document.querySelectorAll('#health article')].map(a => a.hasAttribute('data-active'))")
        shoot(page, f"{label}-06-health", clipped)
        if w > 900:
            page.hover("#health article:nth-of-type(3)")
            page.wait_for_timeout(800)
            hovered = page.evaluate("[...document.querySelectorAll('#health article')].map(a => a.hasAttribute('data-active'))")
            shoot(page, f"{label}-06-health-hover", clipped)
        else:
            hovered = [False, False, True]
        check(f"{label}: health rows open their renders (reached, then hovered)",
              active.count(True) == 1 and hovered == [False, False, True], f"reached={active} hovered={hovered}")

        # Ask BiGH Science over the calm light.
        walk(page, top_of(page, "#ask"))
        page.wait_for_timeout(1600)
        shoot(page, f"{label}-07-ask", clipped)
        ask = page.evaluate("document.querySelector('[data-ask-light]').dataset.light")
        check(f"{label}: Ask BiGH Science draws its light", ask == "webgl", f"ask={ask}")

        # "Read his story" opens the story panel; its close button shuts it.
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(400)
        page.get_by_role("button", name="Read his story").first.click()
        page.wait_for_timeout(600)
        story = page.evaluate("(() => { const d = document.querySelector('dialog'); return d.open && !!d.querySelector('img') && d.querySelectorAll('p').length >= 4; })()")
        if label == "desk":
            shoot(page, f"{label}-story", clipped)
        page.locator("dialog button").first.click()
        page.wait_for_timeout(300)
        closed = page.evaluate("!document.querySelector('dialog').open")
        check(f"{label}: 'Read his story' opens and closes", story and closed, f"opened={story} closed={closed}")

        # Step through the whole page one screen at a time.
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(500)
        end = page.evaluate("document.documentElement.scrollHeight") - h
        y, n = 0, 1
        while y < end and n < 60:
            y = min(end, y + h * 0.85)
            walk(page, y)
            page.wait_for_timeout(700)
            shoot(page, f"{label}-walk-{n:02d}", clipped)
            n += 1
        stuck = page.evaluate(STUCK)
        check(f"{label}: nothing left invisible after scrolling through", not stuck, str(stuck[:5]))
        ov = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        check(f"{label}: no sideways scroll, no errors", ov == 0 and not problems, f"overflow={ov} {problems[:3]}")
        check(f"{label}: no words cut off at the screen edge", not clipped, "; ".join(clipped[:4]))
        ctx.close()

    # Reduced motion: no pin, no reveals, one still frame of light, everything readable.
    clipped = []
    ctx, page, problems = open_page(browser, 1440, 900, reduced=True)
    page.wait_for_timeout(1500)
    shoot(page, "reduced-00-hero", clipped)
    hidden = page.evaluate(STUCK)
    state = page.evaluate(PATH)
    kinds = sorted(set(c["kind"] for c in page.evaluate(LIGHTS)))
    check("reduced motion: everything visible at once, no pin, the light is one still frame",
          not hidden and not state["sideways"] and "webgl" not in kinds and not problems,
          f"hidden={hidden[:4]} sideways={state['sideways']} lights={kinds} {problems[:2]}")
    for name, selector in (("01-liu", "#dr-liu"), ("02-record", "[data-fill]"), ("03-path", "[data-pin]"), ("04-formulas", "[data-studio]"), ("07-ask", "#ask")):
        page.evaluate(f"window.scrollTo(0, {top_of(page, selector) - 120})")
        page.wait_for_timeout(500)
        shoot(page, f"reduced-{name}", clipped)
    check("reduced motion: no words cut off", not clipped, "; ".join(clipped[:4]))
    ctx.close()
    browser.close()

print()
print(f"{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)

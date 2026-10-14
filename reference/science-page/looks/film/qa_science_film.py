"""QA for the Science page (/science): look B "Scroll film", Mo's pick of September 28, 2026.

The film: WebGL on a real GPU, the stage held while the playhead runs, captions on their marks,
the curtain into Dr. Liu. Then the path strip (pinned sideways on wide screens), the story panel,
"See all" (36 sources) and back, no sideways scroll, no errors, no words cut off, nothing under
15px, phones without pinning, reduced motion with everything visible, and the stills fallback
without WebGL. Screenshots (named key screens plus one screen at a time) go to
scripts/qa/out/science-film/.

python -X utf8 scripts/qa/qa_science_film.py [http://localhost:3008]
"""
import os
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3008"
URL = f"{BASE}/science"
SHOTS = os.path.join(os.path.dirname(__file__), "out", "science-film")
os.makedirs(SHOTS, exist_ok=True)
GPU = ["--use-gl=angle", "--use-angle=d3d11", "--enable-gpu", "--ignore-gpu-blocklist"]
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
    page.goto(URL, wait_until="networkidle")
    page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
    return ctx, page, problems


def glide(page, y, steps=14, pause=35):
    current = page.evaluate("scrollY")
    for s in range(1, steps + 1):
        page.evaluate(f"window.scrollTo(0, {current + (y - current) * s / steps})")
        page.wait_for_timeout(pause)


def top_of(page, selector):
    return page.evaluate("(s) => { const e = document.querySelector(s); return e ? e.getBoundingClientRect().top + scrollY : -1; }", selector)


CLIPPED = """(() => {
  // Words cut off at the side of the screen. The sideways path strip is exempt.
  const out = [];
  for (const el of document.querySelectorAll('main h1, main h2, main h3, main p, main button, main a, main li, main dt, main dd')) {
    if (el.closest('[data-track]') || el.closest('[aria-hidden="true"]')) continue;
    const r = el.getBoundingClientRect();
    if (!r.width || r.bottom < 0 || r.top > innerHeight) continue;
    const style = getComputedStyle(el);
    if (style.visibility === 'hidden' || +style.opacity === 0) continue;
    if (r.left < -1 || r.right > innerWidth + 1) out.push(el.textContent.trim().slice(0, 40));
  }
  return out;
})()"""

SMALL = """(() => {
  // Visible text under 15px in this look (the shared source list has its own styles).
  const out = [];
  const walker = document.createTreeWalker(document.querySelector('main'), NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const node = walker.currentNode;
    if (!node.textContent.trim()) continue;
    const el = node.parentElement;
    if (!el || el.closest('[class*="research-library"]')) continue;
    const r = el.getBoundingClientRect();
    if (!r.width) continue;
    const size = parseFloat(getComputedStyle(el).fontSize);
    if (size < 15) out.push(`${size}px ${node.textContent.trim().slice(0, 30)}`);
  }
  return [...new Set(out)];
})()"""

clipped_seen = []


def shoot(page, name):
    page.screenshot(path=os.path.join(SHOTS, name + ".png"))
    clipped_seen.extend(f"{name}: {text}" for text in page.evaluate(CLIPPED))


def overflow(page):
    return page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")


def reel_length(page):
    return page.evaluate("(() => { const r = document.querySelector('[data-reel]'); return { top: r.offsetTop, len: r.offsetHeight - 2 * innerHeight, h: r.offsetHeight }; })()")


def shared_checks(page, tag, h):
    # "See all" opens the full list of 36 and closes again.
    glide(page, top_of(page, "#research") - 40, steps=20)
    page.wait_for_timeout(600)
    button = page.locator("#research button[aria-expanded]").first
    button.click()
    page.wait_for_timeout(500)
    opened = page.evaluate("document.querySelectorAll('#research details').length")
    shoot(page, f"{tag}-research-open")
    button.click()
    page.wait_for_timeout(400)
    shut = page.evaluate("document.querySelectorAll('#research details').length")
    keys = page.evaluate("document.querySelectorAll('#research [data-key-study]').length")
    check(f"{tag}: three key studies; 'See all' opens 36 sources and closes", keys == 3 and opened == 36 and shut == 0, f"key={keys} open={opened} closed={shut}")

    # "Read his story" opens the story panel; its close button shuts it.
    glide(page, top_of(page, "[data-portrait]") - 140, steps=20)
    page.wait_for_timeout(900)
    page.get_by_role("button", name="Read his story").first.click()
    page.wait_for_timeout(500)
    story = page.evaluate("(() => { const d = document.querySelector('dialog'); return d.open && !!d.querySelector('img') && d.querySelectorAll('p').length >= 4; })()")
    if tag.startswith("desk"):
        shoot(page, f"{tag}-story")
    page.locator("dialog button").first.click()
    page.wait_for_timeout(300)
    closed = page.evaluate("!document.querySelector('dialog').open")
    check(f"{tag}: 'Read his story' opens and closes", story and closed, f"opened={story} closed={closed}")


def walk(page, tag, h, start=0):
    page.evaluate(f"window.scrollTo(0, {start})")
    page.wait_for_timeout(600)
    end = page.evaluate("document.documentElement.scrollHeight") - h
    y, n = start, 1
    while y < end and n < 80:
        y = min(end, y + h * 0.85)
        glide(page, y, steps=10)
        page.wait_for_timeout(900)
        shoot(page, f"{tag}-walk-{n:02d}")
        n += 1


with sync_playwright() as p:
    browser = p.chromium.launch(args=GPU)

    # ---- Wide screens: the film. ------------------------------------------------------------
    for label, (w, h) in {"desk": (1440, 900), "laptop": (1280, 720)}.items():
        ctx, page, problems = open_page(browser, w, h)
        page.wait_for_timeout(3200)
        info = page.evaluate("""(() => {
          const reel = document.querySelector('[data-reel]');
          const canvas = document.querySelector('[data-canvas] canvas');
          return { film: reel.dataset.film || null, fallback: !!reel.dataset.fallback,
                   renderer: canvas ? canvas.dataset.renderer : null, h1: document.querySelector('h1')?.textContent.trim(),
                   words: document.querySelectorAll('h1 [style*="--w"]').length };
        })()""")
        check(f"{label}: the film runs in WebGL on the GPU", info["film"] == "webgl" and not info["fallback"], str(info))
        check(f"{label}: the title is the opening's words", info["h1"] and "scientists" in info["h1"] and info["words"] >= 6, info["h1"] or "")
        fonts = page.evaluate("""(() => ({ h1: getComputedStyle(document.querySelector('h1')).fontFamily,
          body: getComputedStyle(document.querySelector('#dr-liu [class*=intro]')).fontFamily,
          header: getComputedStyle(document.querySelector('header nav a')).fontFamily,
          loaded: [...new Set([...document.fonts].filter(f => f.status === 'loaded').map(f => f.family))].join('|') }))()""")
        check(f"{label}: Switzer for display, text and header (as on the NuriCell page)",
              fonts["h1"].startswith("Switzer") and fonts["body"].startswith("Switzer")
              and fonts["header"].startswith("Switzer") and "Switzer" in fonts["loaded"], str({k: v[:40] if k != "loaded" else v for k, v in fonts.items()}))
        tone = page.evaluate("document.querySelector('[data-stage]').dataset.tone")
        check(f"{label}: the header over the film is see-through (film tone)", tone == "film", str(tone))
        shoot(page, f"{label}-film-00-open")

        reel = reel_length(page)
        check(f"{label}: the film is about 4-5 screens of scroll", 3.2 * h <= reel["len"] <= 5.2 * h, f"{reel['len'] / h:.2f} screens")
        # The star moment, frame by frame. Each mark: (playhead, name).
        marks = [(0.14, "push"), (0.23, "through-the-lens"), (0.3, "cells"), (0.35, "bright-cell"), (0.37, "rim"),
                 (0.52, "cell-words"), (0.6, "cell"), (0.74, "double-exposure"), (0.84, "field-words"), (1.0, "field")]
        held, playheads = [], []
        for mark, name in marks:
            glide(page, reel["top"] + reel["len"] * mark, steps=12)
            page.wait_for_timeout(1900)
            held.append(page.evaluate("Math.round(document.querySelector('[data-stage]').getBoundingClientRect().top)"))
            playheads.append(float(page.evaluate("document.querySelector('[data-stage]').dataset.filmP || '-1'")))
            shoot(page, f"{label}-film-{int(mark * 100):03d}-{name}")
        check(f"{label}: the stage stays on screen while the film plays", all(abs(t) <= 1 for t in held), str(held))
        near = all(abs(a - m) < 0.03 for a, (m, _) in zip(playheads, marks))
        check(f"{label}: the playhead follows the scroll", near, str([round(v, 3) for v in playheads]))
        caption = page.evaluate("""(() => { const c = document.querySelector('[data-caption="field"]'); const s = getComputedStyle(c);
          return { vis: s.visibility, op: +s.opacity, words: c.querySelectorAll('.line-mask, [class*="line"]').length }; })()""")
        check(f"{label}: the last caption is on screen at the end of the film", caption["vis"] == "visible" and caption["op"] > 0.9, str(caption))
        title = page.evaluate("+getComputedStyle(document.querySelector('[data-title]')).opacity")
        check(f"{label}: the opening title has left by the end", title < 0.05, f"opacity={title}")

        # The curtain: Dr. Liu's section rises over the last frame.
        glide(page, reel["top"] + reel["len"] + h * 0.55, steps=12)
        page.wait_for_timeout(1500)
        shoot(page, f"{label}-curtain")

        # Dr. Liu, framed.
        glide(page, top_of(page, "[data-portrait]") - (110 if h > 800 else 96), steps=16)
        page.wait_for_timeout(2600)
        shoot(page, f"{label}-liu")
        photo = page.evaluate("getComputedStyle(document.querySelector('[data-photo]')).filter")
        check(f"{label}: his photograph comes fully into focus", photo in ("none", "blur(0px) brightness(1)"), photo)
        glide(page, top_of(page, "[data-record]") - 160, steps=12)
        page.wait_for_timeout(2400)
        shoot(page, f"{label}-record")
        count = page.evaluate("document.querySelector('[data-count]').textContent")
        check(f"{label}: 280 counts up to 280", count == "280", count)

        # The path: pinned, sliding sideways.
        path_top = top_of(page, "[data-path]")
        glide(page, path_top, steps=12)
        page.wait_for_timeout(900)
        x0 = page.evaluate("new DOMMatrix(getComputedStyle(document.querySelector('[data-track]')).transform).m41")
        shoot(page, f"{label}-path-00")
        distance = page.evaluate("(() => { const t = document.querySelector('[data-track]'); const p = document.querySelector('[data-path]'); return t.scrollWidth - p.clientWidth; })()")
        for i, f in enumerate([0.22, 0.45, 0.7, 1.0]):
            glide(page, path_top + distance * f, steps=12)
            page.wait_for_timeout(1500)
            shoot(page, f"{label}-path-{i + 1:02d}")
        x1 = page.evaluate("new DOMMatrix(getComputedStyle(document.querySelector('[data-track]')).transform).m41")
        pinned = page.evaluate("Math.round(document.querySelector('[data-path]').getBoundingClientRect().top)")
        check(f"{label}: the path is pinned and slides sideways", abs(pinned) <= 1 and x1 < x0 - distance * 0.9, f"top={pinned} x {x0:.0f} -> {x1:.0f} of {distance}")

        # The formulas: one shared credit line under the two bottles it names (Propolis, Turmerific);
        # NuriCell, Nature Calm and Advanced OPC (Dr. Iris Wang alone, Mo, September 29) keep their own.
        credit = page.evaluate("""(() => { const shared = document.querySelectorAll('[data-lineup] p[aria-hidden]');
          const own = [...document.querySelectorAll('[data-lineup] figcaption span')].filter(e => e.getBoundingClientRect().width > 2).length;
          return { shared: shared.length, own, text: shared[0]?.textContent.trim().slice(-60) }; })()""")
        check(f"{label}: the formulas share one credit line; NuriCell, Nature Calm and Advanced OPC keep their own",
              credit["shared"] == 1 and credit["own"] == 3, str(credit))

        # The formulas, research, health and ask, framed.
        for sel, name, offset in [("#film-formulas", "formulas", 130 if h > 800 else 100),
                                  ("[data-lineup]", "formulas-stage", 110), ("#research", "research", -30),
                                  ("[data-key-study]", "research-credits", 130), ("#health", "health", -130 if h > 800 else -60),
                                  ("[data-screen]", "ask", 90), ("#ask ol", "ask-steps", 300 if h > 800 else 200)]:
            glide(page, top_of(page, sel) - offset, steps=18)
            page.wait_for_timeout(2600)
            shoot(page, f"{label}-{name}")

        shared_checks(page, label, h)
        walk(page, label, h, start=reel["top"] + reel["len"])
        ov = overflow(page)
        check(f"{label}: no sideways scroll, no errors", ov == 0 and not problems, f"overflow={ov} {problems[:3]}")
        mine = [c for c in clipped_seen if c.startswith(label + "-")]
        check(f"{label}: no words cut off at the screen edge", not mine, "; ".join(mine[:4]))
        small = page.evaluate(SMALL)
        check(f"{label}: nothing under 15px", not small, "; ".join(small[:5]))
        ctx.close()

    # ---- Phone: stacked stills, no pinning. ------------------------------------------------------
    ctx, page, problems = open_page(browser, 390, 844)
    page.wait_for_timeout(2600)
    info = page.evaluate("""(() => {
      const reel = document.querySelector('[data-reel]');
      const stage = document.querySelector('[data-stage]');
      return { reel: reel.offsetHeight, sticky: getComputedStyle(stage).position, canvas: !!document.querySelector('[data-canvas] canvas'),
               pinned: !!document.querySelector('.pin-spacer'), stills: [...document.querySelectorAll('[data-shot-media]')].filter(e => e.getBoundingClientRect().height > 100).length };
    })()""")
    check("phone: no film pinning; three stills with their captions", info["sticky"] != "sticky" and not info["canvas"] and not info["pinned"] and info["stills"] == 3, str(info))
    shoot(page, "phone-00-open")
    for sel, name in [("[data-shot='2']", "cell"), ("[data-shot='3']", "field"), ("[data-portrait]", "liu"), ("[data-path]", "path"),
                      ("[data-lineup]", "formulas"), ("#research", "research"), ("#health", "health"), ("[data-screen]", "ask")]:
        glide(page, top_of(page, sel) - 90, steps=14)
        page.wait_for_timeout(1800)
        shoot(page, f"phone-{name}")
    shared_checks(page, "phone", 844)
    walk(page, "phone", 844)
    ov = overflow(page)
    check("phone: no sideways scroll, no errors", ov == 0 and not problems, f"overflow={ov} {problems[:3]}")
    mine = [c for c in clipped_seen if c.startswith("phone-")]
    check("phone: no words cut off at the screen edge", not mine, "; ".join(mine[:4]))
    small = page.evaluate(SMALL)
    check("phone: nothing under 15px", not small, "; ".join(small[:5]))
    ctx.close()

    # ---- Reduced motion: no scenes, everything visible at once. ----------------------------------
    ctx, page, problems = open_page(browser, 1440, 900, reduced=True)
    page.wait_for_timeout(1200)
    info = page.evaluate("""(() => ({ reel: document.querySelector('[data-reel]').offsetHeight, pinned: !!document.querySelector('.pin-spacer'),
       canvas: !!document.querySelector('[data-canvas] canvas') }))()""")
    check("reduced motion: no film, no pinning", info["reel"] < 4000 and not info["pinned"] and not info["canvas"], str(info))
    shoot(page, "reduced-00-open")
    page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
    page.wait_for_timeout(600)
    hidden = page.evaluate("""[...document.querySelectorAll('main h1, main h2, main h3, main p, main li, main button, main dd')]
      .filter(e => { let n = e; while (n && n !== document.body) { const s = getComputedStyle(n); if (+s.opacity < 0.5 || s.visibility === 'hidden') return true; n = n.parentElement; } return false; })
      .map(e => e.textContent.trim().slice(0, 30))""")
    check("reduced motion: every heading and line is visible", not hidden and not problems, f"{hidden[:4]} {problems[:2]}")
    walk(page, "reduced", 900)
    ctx.close()

    # ---- Without WebGL: the stills play the film. -------------------------------------------------
    nogl = p.chromium.launch(args=["--disable-webgl", "--disable-3d-apis"])
    ctx, page, problems = open_page(nogl, 1440, 900)
    page.wait_for_timeout(2500)
    reel = reel_length(page)
    glide(page, reel["top"] + reel["len"] * 0.6, steps=14)
    page.wait_for_timeout(1800)
    state = page.evaluate("""(() => { const reel = document.querySelector('[data-reel]'); const m = [...document.querySelectorAll('[data-shot-media]')];
      return { fallback: !!reel.dataset.fallback, cell: m[2] ? +getComputedStyle(m[2]).opacity : -1, desk: m[0] ? +getComputedStyle(m[0]).opacity : -1 }; })()""")
    shoot(page, "nogl-film-060")
    real = [x for x in problems if "WebGL" not in x and "webgl" not in x]
    check("no WebGL: the stills play the film instead", state["fallback"] and state["cell"] > 0.9 and state["desk"] < 0.1 and not real, f"{state} {real[:2]}")
    ctx.close()
    nogl.close()
    browser.close()

print()
print(f"{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)

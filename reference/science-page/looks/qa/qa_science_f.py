"""QA for look F, "Glass" (/science?look=f): the live three.js glass cell, the portrait clearing through
frosted glass, the pinned sideways path on glass cards, phones, reduced motion, and the fallbacks
(software rendering, no WebGL). Screens land in scripts/qa/out/science-f/ (one viewport at a time:
full-page shots break the svh layouts).

python -X utf8 scripts/qa/qa_science_f.py [http://localhost:3008]
Uses the real GPU (ANGLE on D3D11) for the WebGL checks, as the brief asks.
"""
import os
import sys
from io import BytesIO

from PIL import Image, ImageChops, ImageStat
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3008"
URL = f"{BASE}/science?look=f"
SHOTS = os.path.join(os.path.dirname(__file__), "out", "science-f")
os.makedirs(SHOTS, exist_ok=True)
GPU = ["--use-gl=angle", "--use-angle=d3d11", "--enable-gpu", "--ignore-gpu-blocklist"]
passed = failed = 0


def check(name, ok, detail=""):
    global passed, failed
    passed += bool(ok)
    failed += not ok
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))


def open_page(browser, w, h, reduced=False, scale=1, allow=()):
    ctx = browser.new_context(
        viewport={"width": w, "height": h},
        reduced_motion="reduce" if reduced else "no-preference",
        device_scale_factor=scale,
    )
    page = ctx.new_page()
    problems = []

    def on_console(m):
        if m.type == "error" and not any(a in m.text for a in allow):
            problems.append(f"console {m.text[:160]}")

    page.on("pageerror", lambda e: problems.append(f"pageerror {e}"))
    page.on("console", on_console)
    page.on("response", lambda r: problems.append(f"{r.status} {r.url[-60:]}") if r.status >= 400 and "favicon" not in r.url else None)
    page.goto(URL, wait_until="networkidle")
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
  // Words cut off at the side of the screen. The sideways path (data-track) is exempt: its stops
  // wait off screen by design.
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


STATS = "(() => { const c = document.querySelector('[data-glass-canvas]'); return c && c.glassStats ? { ...c.glassStats } : null; })()"


def canvas_png(page):
    box = page.evaluate("(() => { const r = document.querySelector('[data-glass-canvas]').getBoundingClientRect(); return { x: Math.max(0, r.left), y: Math.max(0, r.top), width: Math.min(innerWidth, r.right) - Math.max(0, r.left), height: Math.min(innerHeight, r.bottom) - Math.max(0, r.top) }; })()")
    return Image.open(BytesIO(page.screenshot(clip=box))).convert("RGB")


def difference(a, b):
    return sum(ImageStat.Stat(ImageChops.difference(a, b)).mean) / 3


def fps(page, ms=2000):
    start = page.evaluate(STATS)["frames"]
    page.wait_for_timeout(ms)
    return (page.evaluate(STATS)["frames"] - start) * 1000 / ms


FROST = """(() => { const p = document.querySelector('[data-pane]'); const cs = getComputedStyle(p);
  return { frost: parseFloat(cs.getPropertyValue('--frost')) || 0, filter: cs.backdropFilter }; })()"""

with sync_playwright() as p:
    gpu = p.chromium.launch(args=GPU)

    for label, (w, h) in {"desk": (1440, 900), "laptop": (1280, 720), "phone": (390, 844)}.items():
        tag = f"f-{label}"
        ctx, page, problems = open_page(gpu, w, h)
        page.wait_for_timeout(3000)

        # 1. The live glass cell: real GPU, drawn, turning on its own, and smooth.
        stats = page.evaluate(STATS)
        live = page.evaluate("!!document.querySelector('#scientists[data-live]')")
        still_hidden = page.evaluate("getComputedStyle(document.querySelector('[data-hero] img')).visibility === 'hidden'")
        check(f"{tag}: the live glass cell replaces the still (real GPU)",
              live and still_hidden and stats and not stats["slow"] and "NVIDIA" in stats["renderer"],
              f"live={live} still hidden={still_hidden} renderer={stats and stats['renderer'][:40]}")
        a = canvas_png(page)
        page.wait_for_timeout(1200)
        b = canvas_png(page)
        moved = difference(a, b)
        rate = fps(page)
        check(f"{tag}: the cell turns by itself at a smooth rate", moved > 0.3 and rate >= 50, f"pixel change={moved:.2f} fps={rate:.0f}")
        # Its colors: a warm gold inside a pale glass rim (not lemon, not grey).
        center = b.crop((b.width * 0.4, b.height * 0.4, b.width * 0.6, b.height * 0.6))
        r, g, bl = ImageStat.Stat(center).mean
        check(f"{tag}: the inside reads warm gold", r > 200 and 120 < g < 215 and bl < 150 and r - bl > 90, f"rgb=({r:.0f},{g:.0f},{bl:.0f})")
        page.mouse.move(w * 0.9, h * 0.2)
        page.wait_for_timeout(1500)
        shoot(page, f"{tag}-00-hero")

        # 2. Read his story opens and closes.
        page.get_by_role("button", name="Read his story").first.click()
        page.wait_for_timeout(500)
        opened = page.evaluate("(() => { const d = document.querySelector('dialog'); return d.open && d.textContent.includes('Okayama'); })()")
        page.get_by_role("button", name="Close details").click()
        page.wait_for_timeout(300)
        closed = page.evaluate("!document.querySelector('dialog').open")
        check(f"{tag}: 'Read his story' opens the story and closes again", opened and closed, f"opened={opened} closed={closed}")
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(500)

        # 3. The portrait clears through the glass: frosted while low on the screen, clear (and
        # untinted: no saturation left on his photo) once it settles.
        portrait = top_of(page, "[data-portrait]")
        walk(page, portrait - h * 0.92)
        page.wait_for_timeout(1200)
        frosted = page.evaluate(FROST)
        shoot(page, f"{tag}-01-frosted")
        walk(page, portrait - h * 0.18)
        page.wait_for_timeout(1400)
        clear = page.evaluate(FROST)
        shoot(page, f"{tag}-02-portrait")
        check(f"{tag}: the portrait comes into focus through frosted glass",
              frosted["frost"] >= 12 and clear["frost"] == 0 and "saturate(1)" in clear["filter"],
              f"frosted={frosted} clear={clear}")

        # 4. Step through the rest of the opening one screen at a time.
        research = top_of(page, "#research")
        y = portrait - h * 0.18
        n = 3
        while y + h * 0.85 < research and n < 40:
            y += h * 0.85
            walk(page, y)
            page.wait_for_timeout(1100)
            shoot(page, f"{tag}-{n:02d}")
            n += 1

        if label != "phone":
            # The path pins and slides; stops light in order; the gold line fills; it ends with the
            # formulas and Dr. Iris Wang fully on screen.
            journey = page.evaluate("(() => { const j = document.querySelector('[data-journey]'); const s = j.parentElement.classList.contains('pin-spacer') ? j.parentElement : j; return s.getBoundingClientRect().top + scrollY; })()")
            span = page.evaluate("document.querySelector('[data-track]').scrollWidth - innerWidth")
            walk(page, journey - h)
            page.wait_for_timeout(900)
            xs, lit, fills = [], [], []
            for i, step in enumerate((0.02, 0.35, 0.7, 1.0)):
                walk(page, journey + step * span)
                page.wait_for_timeout(1400)
                xs.append(round(page.evaluate("new DOMMatrix(getComputedStyle(document.querySelector('[data-track]')).transform).m41")))
                lit.append(page.evaluate("document.querySelectorAll('[data-lit]').length"))
                fills.append(round(page.evaluate("new DOMMatrix(getComputedStyle(document.querySelector('[data-fill]')).transform).a"), 2))
                shoot(page, f"{tag}-path-{i}")
            slides = all(a > b for a, b in zip(xs, xs[1:]))
            lights = lit == sorted(lit) and lit[0] < lit[-1] and lit[-1] == 5
            filling = fills == sorted(fills) and fills[-1] > 0.9
            ends = page.evaluate("""(() => { const f = document.querySelector('[class*=finale]'); const r = f.getBoundingClientRect();
              return r.left >= -1 && r.right <= innerWidth + 1; })()""")
            check(f"{tag}: the path pins and slides; stops light in order; the line fills; it ends on the formulas",
                  slides and xs[-1] < -500 and lights and filling and ends, f"x={xs} lit={lit} fill={fills} end on screen={ends}")
        else:
            x = page.evaluate("new DOMMatrix(getComputedStyle(document.querySelector('[data-track]')).transform).m41")
            lit = page.evaluate("document.querySelectorAll('[data-lit]').length")
            fill = round(page.evaluate("new DOMMatrix(getComputedStyle(document.querySelector('[data-fill]')).transform).d"), 2)
            check(f"{tag}: phones get the path top to bottom; stops light and the line fills as you read",
                  x == 0 and lit == 5 and fill > 0.9, f"x={x} lit={lit} fill={fill}")

        # 5. The cell stops drawing when it is off screen.
        walk(page, top_of(page, "#research"))
        page.wait_for_timeout(600)
        idle = fps(page, 1200)
        check(f"{tag}: the cell stops drawing off screen", idle == 0, f"fps off screen={idle:.0f}")

        for part in ("research", "health", "ask"):
            walk(page, top_of(page, f"#{part}"))
            page.wait_for_timeout(900)
            shoot(page, f"{tag}-z-{part}")
        ov = overflow(page)
        check(f"{tag}: no sideways scroll, no errors", ov == 0 and not problems, f"overflow={ov} {problems[:3]}")
        mine = [c for c in clipped_seen if c.startswith(tag + "-")]
        check(f"{tag}: no words cut off at the screen edge", not mine, "; ".join(mine[:4]))
        ctx.close()

    # A sharp (retina) screen: the pixel ratio stays at 2 and it still runs smoothly.
    ctx, page, problems = open_page(gpu, 1440, 900, scale=2)
    page.wait_for_timeout(3500)
    rate = fps(page)
    stats = page.evaluate(STATS)
    check("f-retina: the cell runs at 2x pixels and stays smooth", stats["pixelRatio"] == 2 and rate >= 50, f"pixel ratio={stats['pixelRatio']} fps={rate:.0f}")
    page.screenshot(path=os.path.join(SHOTS, "f-retina-hero.png"))
    ctx.close()

    # Reduced motion: the still render (no WebGL, no pin, no scroll scenes), everything visible.
    for label, (w, h) in {"desk": (1440, 900), "phone": (390, 844)}.items():
        ctx, page, problems = open_page(gpu, w, h, reduced=True)
        page.wait_for_timeout(1200)
        state = page.evaluate("""(() => ({
          live: !!document.querySelector('#scientists[data-live]'),
          still: getComputedStyle(document.querySelector('[data-hero] img')).opacity,
          blend: getComputedStyle(document.querySelector('[data-hero] img')).mixBlendMode,
          pinned: !!document.querySelector('.pin-spacer'),
          frost: getComputedStyle(document.querySelector('[data-pane]')).backdropFilter,
          hidden: [...document.querySelectorAll('#scientists h1, #scientists h2, #scientists h3, #scientists p, #scientists img')]
            .filter(e => { let n = e; while (n && n !== document.body) { if (+getComputedStyle(n).opacity < 0.5) return true; n = n.parentElement; } return false; })
            .filter(e => !e.closest('[aria-hidden="true"]'))
            .map(e => (e.textContent || e.alt || e.src).trim().slice(0, 30)),
        }))()""")
        ok = (not state["live"] and state["still"] == "1" and state["blend"] == "multiply" and not state["pinned"]
              and "blur(0px)" in state["frost"] and not state["hidden"])
        check(f"f-reduced-{label}: the still render, no pin, everything visible at once", ok and not problems, f"{state} {problems[:2]}")
        page.screenshot(path=os.path.join(SHOTS, f"f-reduced-{label}-00.png"))
        for i, sel in enumerate(("[data-portrait]", "[data-track]", "[class*=finale]")):
            walk(page, top_of(page, sel) - 90)
            page.wait_for_timeout(300)
            shoot(page, f"f-reduced-{label}-{i + 1:02d}")
        check(f"f-reduced-{label}: no sideways scroll", overflow(page) == 0, f"overflow={overflow(page)}")
        ctx.close()
    gpu.close()

    # Software rendering (SwiftShader, no GPU): one pixel per CSS pixel, drawn only when something
    # changes, so it never burns the processor.
    soft = p.chromium.launch()
    ctx, page, problems = open_page(soft, 1440, 900)
    page.wait_for_timeout(5000)
    stats = page.evaluate(STATS)
    idle = fps(page, 1500)
    walk(page, 300)
    page.wait_for_timeout(600)
    after = page.evaluate(STATS)
    check("f-software: SwiftShader draws only on change, at 1x",
          stats and stats["slow"] and stats["pixelRatio"] == 1 and idle == 0 and after["frames"] > stats["frames"] and not problems,
          f"renderer={stats and stats['renderer'][:40]} idle fps={idle:.0f} frames {stats and stats['frames']}->{after['frames']} {problems[:2]}")
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(600)
    page.screenshot(path=os.path.join(SHOTS, "f-software-hero.png"))
    ctx.close()
    soft.close()

    # No WebGL at all: the still render stays, multiplied into the pearl page, with no page errors.
    bare = p.chromium.launch(args=["--disable-webgl", "--disable-3d-apis"])
    ctx, page, problems = open_page(bare, 1440, 900)
    page.wait_for_timeout(2500)
    state = page.evaluate("""(() => ({ live: !!document.querySelector('#scientists[data-live]'),
      still: getComputedStyle(document.querySelector('[data-hero] img')).opacity }))()""")
    check("f-no-webgl: the still render stays and nothing breaks", not state["live"] and state["still"] == "1" and not problems, f"{state} {problems[:2]}")
    page.screenshot(path=os.path.join(SHOTS, "f-no-webgl-hero.png"))
    ctx.close()
    bare.close()

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)

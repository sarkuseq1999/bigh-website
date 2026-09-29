"""QA for look E, "Night sky" (/science?look=e): the WebGL sky, the hero, Dr. Liu's portrait, the
constellation timeline (pinned sideways on wide screens, top to bottom on phones and with reduced
motion), the formulas with Dr. Iris Wang, and the seam into the shared sections.

Viewport pictures land in scripts/qa/out/science-e/ (full-page shots break the svh layouts, so the
script steps through the page one screen at a time). WebGL runs on the real GPU (ANGLE D3D11); one
extra pass runs without it (SwiftShader) to prove the software path.

python -X utf8 scripts/qa/qa_science_e.py http://localhost:3008
"""
import io
import os
import sys
from PIL import Image, ImageChops, ImageStat
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3008"
URL = f"{BASE}/science?look=e"
SHOTS = os.path.join(os.path.dirname(__file__), "out", "science-e")
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


def walk(page, y, steps=10):
    current = page.evaluate("scrollY")
    for s in range(1, steps + 1):
        page.evaluate(f"window.scrollTo(0, {current + (y - current) * s / steps})")
        page.wait_for_timeout(40)


def top_of(page, selector):
    return page.evaluate(f"(() => {{ const e = document.querySelector('{selector}'); return e ? e.getBoundingClientRect().top + scrollY : -1; }})()")


def grab(page, clip=None):
    return Image.open(io.BytesIO(page.screenshot(clip=clip))).convert("RGB")


def diff(a, b):
    return sum(ImageStat.Stat(ImageChops.difference(a, b)).mean) / 3


def bright_stars(img, threshold=110):
    """Count points of light (local maxima above a brightness) in a picture of empty sky."""
    g = img.convert("L")
    w, h = g.size
    px = g.load()
    count = 0
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            v = px[x, y]
            if v < threshold:
                continue
            if all(v >= px[x + dx, y + dy] for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy) and v > px[x - 1, y]:
                count += 1
    return count


CLIPPED = """(() => {
  // Words cut off at the side of the screen. The sideways path is exempt (it slides on purpose).
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

# In the pinned stage: words of a stop that is on screen must not run under the header or off the
# bottom of the screen (short laptop screens).
VCLIPPED = """(() => {
  const out = [];
  for (const el of document.querySelectorAll('[data-track] h2, [data-track] h3, [data-track] p, [data-track] a, [data-track] figcaption')) {
    const r = el.getBoundingClientRect();
    if (!r.width || r.right < 0 || r.left > innerWidth) continue;
    if (r.top < 84 - 1 || r.bottom > innerHeight + 1) out.push(el.textContent.trim().slice(0, 30) + ` (${Math.round(r.top)}-${Math.round(r.bottom)})`);
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
  const s = document.querySelector('#scientists');
  const img = document.querySelector('#scientists [data-photo]');
  return {
    h1: document.querySelector('h1')?.textContent.trim(),
    tone: s?.dataset.tone,
    sky: s?.dataset.sky,
    canvas: !!s?.querySelector('canvas'),
    photo: img ? img.naturalWidth : 0,
    sections: ['#research', '#health', '#ask'].map(q => !!document.querySelector(q)),
    stops: document.querySelectorAll('[data-stop]').length,
    bottles: [...document.querySelectorAll('[data-together] img')].filter(i => i.naturalWidth > 0).length,
  };
})()"""

STATE = """(() => ({
  x: Math.round(new DOMMatrix(getComputedStyle(document.querySelector('[data-track]')).transform).m41),
  lit: document.querySelectorAll('[data-stop][data-lit]').length,
  together: !!document.querySelector('[data-together][data-lit]'),
  papers: +(document.querySelector('#scientists').dataset.papers || 0),
  clip: parseFloat((document.querySelector('[data-lit-line]').style.clipPath.match(/inset\\(0px (\\S+)px/) || [0, 1e9])[1]),
  value: getComputedStyle(document.querySelector('[data-papers-label] span')).color,
  valueOpacity: +getComputedStyle(document.querySelector('[data-papers-label]').parentElement).opacity,
}))()"""


def desktop(browser, w, h):
    tag = f"e-desk-{w}x{h}"
    ctx, page, problems = open_page(browser, w, h)
    page.wait_for_timeout(3600)
    info = page.evaluate(COMMON)
    check(f"{tag}: opening, photo, sky, formulas and shared sections render",
          info["h1"] and info["tone"] == "dark" and info["sky"] == "webgl" and info["canvas"] and info["photo"] > 0
          and all(info["sections"]) and info["stops"] == 5, str(info))
    shoot(page, f"{tag}-00")

    # The sky is alive: over a second the stars drift and twinkle (the words stay put).
    sky_box = {"x": 0, "y": 100, "width": w, "height": 160}
    a = grab(page, sky_box)
    page.wait_for_timeout(1200)
    b = grab(page, sky_box)
    alive = diff(a, b)
    check(f"{tag}: the sky moves on its own (drift, twinkle)", alive > 0.05, f"mean change {alive:.3f}")

    # "Read his story" opens the story panel; its close button shuts it.
    walk(page, top_of(page, "[data-intro]") - 200)
    page.wait_for_timeout(600)
    page.get_by_role("button", name="Read his story").first.click()
    page.wait_for_timeout(500)
    opened = page.evaluate("(() => { const d = document.querySelector('dialog'); return d.open && d.textContent.includes('Okayama'); })()")
    shoot(page, f"{tag}-story")
    page.get_by_role("button", name="Close details").click()
    page.wait_for_timeout(300)
    closed = page.evaluate("!document.querySelector('dialog').open")
    check(f"{tag}: 'Read his story' opens the story and closes again", opened and closed, f"opened={opened} closed={closed}")

    # Dr. Liu comes into focus as the portrait rises (blurred on the way in, sharp in place).
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(500)
    frame = top_of(page, "[data-frame]")
    walk(page, frame - h * 0.92)
    page.wait_for_timeout(900)
    early = page.evaluate("getComputedStyle(document.querySelector('[data-photo]')).filter")
    walk(page, frame - h * 0.3)
    page.wait_for_timeout(1400)
    late = page.evaluate("getComputedStyle(document.querySelector('[data-photo]')).filter")
    shoot(page, f"{tag}-portrait")
    check(f"{tag}: the portrait comes into focus out of the dark", "blur(0px)" not in early and "blur(0px)" in late and "brightness(1)" in late, f"{early} -> {late}")

    # Step through the opening one screen at a time.
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(400)
    research = top_of(page, "#research")
    y, n = 0, 1
    while y + h * 0.85 < research and n < 30:
        y += h * 0.85
        walk(page, y)
        page.wait_for_timeout(1100)
        shoot(page, f"{tag}-{n:02d}")
        n += 1

    # The constellation: pinned, it slides; the line draws; stars light in order; the paper stars
    # arrive; 280+ lights only at 2025; the formulas and Dr. Iris Wang light at the end.
    journey = page.evaluate("(() => { const j = document.querySelector('[data-journey]'); const s = j.parentElement.classList.contains('pin-spacer') ? j.parentElement : j; return s.getBoundingClientRect().top + scrollY; })()")
    span = page.evaluate("document.querySelector('[data-track]').scrollWidth - innerWidth")
    walk(page, journey - h)
    page.wait_for_timeout(900)
    states, stars, vclip = [], [], []
    for step in (0.0, 0.25, 0.5, 0.75, 1.0):
        walk(page, journey + step * span)
        page.wait_for_timeout(1700)
        states.append(page.evaluate(STATE))
        stars.append(bright_stars(grab(page, {"x": 0, "y": 92, "width": w, "height": 88})))
        vclip.extend(page.evaluate(VCLIPPED))
        shoot(page, f"{tag}-path-{int(step * 100):03d}")
    bottles = page.evaluate("[...document.querySelectorAll('[data-together] img')].filter(i => i.complete && i.naturalWidth > 0).length")
    check(f"{tag}: both bottles are on the night at the end of the path", bottles == 2, f"bottles={bottles}")
    xs = [s["x"] for s in states]
    lit = [s["lit"] for s in states]
    papers = [s["papers"] for s in states]
    clips = [s["clip"] for s in states]
    slides = all(a > b for a, b in zip(xs, xs[1:])) and xs[-1] < -1000
    check(f"{tag}: the path pins and slides sideways; the line draws itself",
          slides and all(a > b for a, b in zip(clips, clips[1:])), f"x={xs} clip-right={[round(c) for c in clips]}")
    check(f"{tag}: stars light in order, the formulas last",
          lit == sorted(lit) and lit[0] == 0 and lit[-1] == 5 and states[-1]["together"] and not states[0]["together"], f"lit={lit} together={[s['together'] for s in states]}")
    at2025 = next((s for s in states if s["lit"] >= 4), None)
    before2025 = [s for s in states if s["lit"] < 4]
    check(f"{tag}: 280+ lights gold only once 2025 is reached",
          at2025 is not None and at2025["valueOpacity"] == 1 and "243, 197, 106" in at2025["value"]
          and all(s["valueOpacity"] < 1 for s in before2025), f"{[(s['lit'], s['valueOpacity'], s['value']) for s in states]}")
    check(f"{tag}: the paper stars arrive along the path (progress 0 -> 1 at 2025; more stars in the sky)",
          papers[0] == 0 and papers == sorted(papers) and papers[-1] == 1 and stars[3] > stars[0] * 1.2, f"papers={papers} bright stars in the top band={stars[:4]}")
    check(f"{tag}: no words of the path under the header or off the bottom", not vclip, "; ".join(vclip[:4]))

    # The seam: the sky fades into the research section's own night, with no visible edge.
    seam = top_of(page, "#research")
    walk(page, seam - h / 2)
    page.wait_for_timeout(1200)
    shot = grab(page)
    shoot(page, f"{tag}-seam")
    gaps = []
    for x in (w // 2, w // 5, w - w // 5):
        above = shot.getpixel((x, h // 2 - 4))
        below = shot.getpixel((x, h // 2 + 4))
        gaps.append(max(abs(p - q) for p, q in zip(above, below)))
    check(f"{tag}: the sky ends without an edge into the research section", max(gaps) <= 6, f"max channel gap={gaps}")

    for part in ("research", "health", "ask"):
        walk(page, top_of(page, f"#{part}"))
        page.wait_for_timeout(900)
        shoot(page, f"{tag}-z-{part}")
    ov = overflow(page)
    check(f"{tag}: no sideways scroll, no errors", ov == 0 and not problems, f"overflow={ov} {problems[:3]}")
    mine = [c for c in clipped_seen if c.startswith(tag + "-")]
    check(f"{tag}: no words cut off at the screen edge", not mine, "; ".join(mine[:4]))
    ctx.close()


def phone(browser):
    w, h = 390, 844
    tag = "e-phone"
    ctx, page, problems = open_page(browser, w, h)
    page.wait_for_timeout(3000)
    info = page.evaluate(COMMON)
    check(f"{tag}: opening, photo, still sky, formulas and shared sections render",
          info["h1"] and info["sky"] == "still" and info["photo"] > 0 and all(info["sections"]) and info["bottles"] == 2, str(info))
    shoot(page, f"{tag}-00")
    a = grab(page, {"x": 0, "y": 80, "width": w, "height": 150})
    page.wait_for_timeout(1200)
    b = grab(page, {"x": 0, "y": 80, "width": w, "height": 150})
    check(f"{tag}: the sky is still (no animation on phones)", diff(a, b) < 0.01, f"mean change {diff(a, b):.4f}")
    # The planet shines beside the hero words, then leaves the still sky once they have scrolled away.
    spot = page.evaluate("(() => { const r = document.querySelector('[data-planet]').getBoundingClientRect(); return {x: Math.max(0, r.x - 14), y: Math.max(0, r.y - 14), width: 30, height: 30}; })()")
    lit_before = grab(page, spot).convert("L").getextrema()[1]
    walk(page, 900)
    page.wait_for_timeout(500)
    lit_after = grab(page, spot).convert("L").getextrema()[1]
    walk(page, 0)
    page.wait_for_timeout(300)
    check(f"{tag}: the planet shines by the hero, then leaves the still sky", lit_before > 200 and lit_after < lit_before - 60, f"brightest {lit_before} -> {lit_after}")

    page.get_by_role("button", name="Read his story").first.click()
    page.wait_for_timeout(500)
    opened = page.evaluate("document.querySelector('dialog').open")
    page.get_by_role("button", name="Close details").click()
    page.wait_for_timeout(300)
    check(f"{tag}: 'Read his story' opens and closes", opened and page.evaluate("!document.querySelector('dialog').open"))

    research = top_of(page, "#research")
    y, n = 0, 1
    while y + h * 0.85 < research and n < 40:
        y += h * 0.85
        walk(page, y)
        page.wait_for_timeout(700)
        shoot(page, f"{tag}-{n:02d}")
        n += 1
    path = page.evaluate("""(() => {
      const stops = [...document.querySelectorAll('[data-stop]')];
      return {
        x: new DOMMatrix(getComputedStyle(document.querySelector('[data-track]')).transform).m41,
        pinned: !!document.querySelector('.pin-spacer'),
        dim: stops.filter(s => +getComputedStyle(s.querySelector('[class*=below]')).opacity < 1).length,
        ordered: stops.every((s, i) => i === 0 || s.getBoundingClientRect().top > stops[i - 1].getBoundingClientRect().top),
        aligned: stops.every(s => Math.abs(s.querySelector('p').getBoundingClientRect().left - s.querySelector('h3').getBoundingClientRect().left) < 2),
        value: getComputedStyle(document.querySelector('[data-papers-label] span')).color,
      };
    })()""")
    check(f"{tag}: the path runs top to bottom, every stop lit and readable",
          path["x"] == 0 and not path["pinned"] and path["dim"] == 0 and path["ordered"] and path["aligned"] and "243, 197, 106" in path["value"], str(path))
    for part in ("research", "ask"):
        walk(page, top_of(page, f"#{part}"))
        page.wait_for_timeout(700)
        shoot(page, f"{tag}-z-{part}")
    ov = overflow(page)
    check(f"{tag}: no sideways scroll, no errors", ov == 0 and not problems, f"overflow={ov} {problems[:3]}")
    mine = [c for c in clipped_seen if c.startswith(tag + "-")]
    check(f"{tag}: no words cut off at the screen edge", not mine, "; ".join(mine[:4]))
    ctx.close()


def reduced(browser):
    tag = "e-reduced"
    ctx, page, problems = open_page(browser, 1440, 900, reduced=True)
    page.wait_for_timeout(2500)
    state = page.evaluate("""(() => ({
      sky: document.querySelector('#scientists').dataset.sky,
      pinned: !!document.querySelector('.pin-spacer'),
      hidden: [...document.querySelectorAll('#scientists h1 span, #scientists [data-stop] *, [data-together] *')].filter(e => +getComputedStyle(e).opacity < 1).length,
      photo: getComputedStyle(document.querySelector('[data-photo]')).filter,
    }))()""")
    ok = state["sky"] == "still" and not state["pinned"] and state["hidden"] == 0 and state["photo"] == "none"
    check(f"{tag}: calm version shows everything at once (still sky, no pin)", ok and not problems, f"{state} {problems[:2]}")
    shoot(page, f"{tag}-00")
    for i, part in enumerate(("[data-journey]", "[data-together]")):
        walk(page, top_of(page, part) - 100)
        page.wait_for_timeout(400)
        shoot(page, f"{tag}-{i + 1:02d}")
    mine = [c for c in clipped_seen if c.startswith(tag + "-")]
    check(f"{tag}: no words cut off, no sideways scroll", not mine and overflow(page) == 0, "; ".join(mine[:4]))
    ctx.close()


with sync_playwright() as p:
    browser = p.chromium.launch(args=GPU)
    desktop(browser, 1440, 900)
    desktop(browser, 1280, 720)
    phone(browser)
    reduced(browser)
    browser.close()

    # Without a GPU (SwiftShader): the software path draws the sky only when something moves.
    browser = p.chromium.launch()
    ctx, page, problems = open_page(browser, 1440, 900)
    page.wait_for_timeout(3000)
    sky = page.evaluate("document.querySelector('#scientists').dataset.sky")
    renderer = page.evaluate("document.querySelector('#scientists canvas')?.dataset.renderer || ''")
    shoot(page, "e-software-00")
    check("e-software: SwiftShader gets the slow path and still draws the sky", sky == "slow" and not problems, f"sky={sky} renderer={renderer[:60]} {problems[:2]}")
    ctx.close()
    browser.close()

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)

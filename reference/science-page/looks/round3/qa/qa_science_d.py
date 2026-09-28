"""QA for look D, "Golden hour" (/science?look=d): hero, Dr. Liu, his record, the film strip, the
formulas and Dr. Iris Wang, at 1440 x 900, 1280 x 720 and 390 x 844, plus reduced motion. Viewport
pictures land in scripts/qa/out/science-d/ (full-page shots break the svh layouts, so the script
steps through the page one screen at a time, and through the pinned strip at several points).

python -X utf8 scripts/qa/qa_science_d.py http://localhost:3008
"""
import os
import re
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3008"
SHOTS = os.path.join(os.path.dirname(__file__), "out", "science-d")
os.makedirs(SHOTS, exist_ok=True)
URL = f"{BASE}/science?look=d"
passed = failed = 0
GPU = ["--use-gl=angle", "--use-angle=d3d11", "--enable-gpu", "--ignore-gpu-blocklist"]


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
    for _ in range(8):
        page.goto(URL, wait_until="networkidle")
        if page.evaluate("!!document.querySelector('#scientists [data-film]') && !!document.querySelector('#research')"):
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


def blur_of(css):
    found = re.search(r"blur\(([\d.]+)px\)", css or "")
    return float(found.group(1)) if found else 0.0


# Words cut off at the side of the screen. On wide screens the sideways strip is exempt (its cards
# slide past the edges on purpose); on phones it is checked like everything else.
CLIPPED = """((exemptTrack) => {
  const out = [];
  for (const el of document.querySelectorAll('main h1, main h2, main h3, main p, main button, main a')) {
    if ((exemptTrack && el.closest('[data-track]')) || el.closest('[aria-hidden="true"]')) continue;
    const r = el.getBoundingClientRect();
    if (!r.width || r.bottom < 0 || r.top > innerHeight) continue;
    const style = getComputedStyle(el);
    if (style.visibility === 'hidden' || +style.opacity === 0) continue;
    if (r.left < -1 || r.right > innerWidth + 1) out.push(el.textContent.trim().slice(0, 40));
  }
  return out;
})"""
# Words cut off inside their own card (a card hides what overflows it).
INSIDE = """(() => {
  const out = [];
  for (const box of document.querySelectorAll('#scientists [data-stop] > div:first-child, #scientists [class*=irisCard]')) {
    const b = box.getBoundingClientRect();
    for (const el of box.querySelectorAll('p, h3')) {
      const r = el.getBoundingClientRect();
      const wide = el.scrollWidth > el.clientWidth + 1;
      if (wide || r.left < b.left - 1 || r.right > b.right + 1 || r.bottom > b.bottom + 1) out.push(el.textContent.trim().slice(0, 30));
    }
  }
  // The words in the "Today" panel must not sit under a bottle.
  const hit = (a, b) => a.left < b.right && b.left < a.right && a.top < b.bottom && b.top < a.bottom;
  for (const el of document.querySelectorAll('[data-today] p, [data-today] h3')) {
    for (const bottle of document.querySelectorAll('[data-bottle]')) {
      if (hit(el.getBoundingClientRect(), bottle.getBoundingClientRect())) out.push('under a bottle: ' + el.textContent.trim().slice(0, 24));
    }
  }
  return out;
})()"""
clipped_seen = []


def shoot(page, name, exempt_track=True):
    page.screenshot(path=os.path.join(SHOTS, name + ".png"))
    clipped_seen.extend(f"{name}: {text}" for text in page.evaluate(f"{CLIPPED}({'true' if exempt_track else 'false'})"))


def overflow(page):
    return page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")


COMMON = """(() => {
  const hero = document.querySelector('[data-hero-image]');
  const photo = document.querySelector('[data-photo]');
  const labels = [...document.querySelectorAll('#scientists span')].filter(s => s.textContent.trim() === 'Illustration');
  const credits = [...document.querySelectorAll('#scientists figcaption')].map(f => f.textContent.trim());
  const iris = document.querySelector('#scientists [class*=irisCard]');
  return {
    h1: document.querySelector('h1')?.textContent.trim(),
    hero: hero ? hero.naturalWidth : 0,
    photo: photo ? photo.naturalWidth : 0,
    cards: document.querySelectorAll('[data-card-media] img').length,
    labels: labels.length,
    credits,
    irisWords: iris ? iris.textContent.includes('Dr. Iris Wang') : false,
    irisPictures: iris ? iris.querySelectorAll('img, svg, picture').length : -1,
    sections: ['#research', '#health', '#ask'].map(s => !!document.querySelector(s)),
  };
})()"""

with sync_playwright() as p:
    browser = p.chromium.launch(args=GPU)
    for label, (w, h) in {"desk": (1440, 900), "laptop": (1280, 720), "phone": (390, 844)}.items():
        tag = f"d-{label}"
        wide = w > 900
        ctx, page, problems = open_page(browser, w, h)
        before = page.evaluate("getComputedStyle(document.querySelector('[data-photo]')).filter")
        page.wait_for_timeout(3600)
        info = page.evaluate(COMMON)
        credits_ok = any("Formulated by Dr. Jiankang Liu." in c for c in info["credits"]) and any(
            "Developed by Dr. Jiankang Liu and Dr. Iris Wang." in c for c in info["credits"])
        check(f"{tag}: hero, photo, 4 pictures, 5 'Illustration' labels, credits, Iris in words only, shared sections",
              info["h1"] and info["hero"] > 0 and info["photo"] > 0 and info["cards"] == 4 and info["labels"] == 5
              and credits_ok and info["irisWords"] and info["irisPictures"] == 0 and all(info["sections"]),
              str(info))
        shoot(page, f"{tag}-00")

        # The hero: the sun has come up (load-in done), the picture drifts, the light breathes.
        hero_state = page.evaluate("""(() => ({
          image: getComputedStyle(document.querySelector('[data-hero-image]')).filter,
          words: [...document.querySelectorAll('[data-hero-rise]')].map(e => +getComputedStyle(e).opacity),
        }))()""")
        drift_a = page.evaluate("getComputedStyle(document.querySelector('[data-hero-media] > div')).transform")
        page.wait_for_timeout(1500)
        drift_b = page.evaluate("getComputedStyle(document.querySelector('[data-hero-media] > div')).transform")
        check(f"{tag}: hero words visible, picture at full light, slow drift moving",
              min(hero_state["words"]) == 1 and "brightness(1)" in hero_state["image"] and drift_a != drift_b,
              f"{hero_state} drift {drift_a[:40]} -> {drift_b[:40]}")

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
        page.wait_for_timeout(500)

        # Scrolling away from the hero softens it.
        hero_h = page.evaluate("document.querySelector('[data-hero]').offsetHeight")
        walk(page, hero_h * 0.6)
        page.wait_for_timeout(700)
        soft = blur_of(page.evaluate("getComputedStyle(document.querySelector('[data-hero-media]')).filter"))
        sun_a = page.evaluate("getComputedStyle(document.querySelector('[data-sun]')).transform")
        shoot(page, f"{tag}-01-leaving")
        check(f"{tag}: the hero softens as you scroll away", soft > 2, f"blur={soft}px")

        # Step through the opening one screen at a time, up to the strip.
        film_top = page.evaluate("(() => { const f = document.querySelector('[data-film]'); const s = f.parentElement.classList.contains('pin-spacer') ? f.parentElement : f; return s.getBoundingClientRect().top + scrollY; })()")
        y, n = hero_h * 0.6, 2
        while y + h * 0.85 < film_top and n < 30:
            y += h * 0.85
            walk(page, y)
            page.wait_for_timeout(1100)
            shoot(page, f"{tag}-{n:02d}", exempt_track=wide)
            n += 1
        sun_b = page.evaluate("getComputedStyle(document.querySelector('[data-sun]')).transform")
        after = page.evaluate("getComputedStyle(document.querySelector('[data-photo]')).filter")
        count = page.evaluate("[...document.querySelectorAll('[data-numbers] p:first-child')].map(p => p.textContent.trim())")
        check(f"{tag}: his photo comes into focus (blurred before, sharp after); window light moves; 280 counts up",
              blur_of(before) > 10 and blur_of(after) == 0 and sun_a != sun_b and count == ["280+", "1994", "2025"],
              f"before={before} after={after} light {sun_a[:30]} -> {sun_b[:30]} numbers={count}")

        if wide:
            # The strip: pinned, sliding, the line filling, stops lighting in order, and the
            # sharpest picture always the one nearest the middle of the screen.
            span = page.evaluate("document.querySelector('[data-track]').scrollWidth - innerWidth")
            walk(page, film_top - h * 0.5)
            page.wait_for_timeout(700)
            xs, fills, lit, ticks, focus = [], [], [], [], []
            for step in (0.02, 0.25, 0.5, 0.75, 0.99):
                walk(page, film_top + step * span)
                page.wait_for_timeout(1500)
                state = page.evaluate("""(() => {
                  const cards = [...document.querySelectorAll('[data-card-media]')].map(m => {
                    const r = m.parentElement.getBoundingClientRect();
                    const blur = +((getComputedStyle(m).filter.match(/blur\\(([\\d.]+)px\\)/) || [0, 0])[1]);
                    return { mid: Math.abs(r.left + r.width / 2 - innerWidth / 2), blur, seen: r.right > 0 && r.left < innerWidth };
                  }).filter(c => c.seen);
                  const nearest = cards.slice().sort((a, b) => a.mid - b.mid)[0];
                  const sharpest = cards.slice().sort((a, b) => a.blur - b.blur)[0];
                  return {
                    x: new DOMMatrix(getComputedStyle(document.querySelector('[data-track]')).transform).m41,
                    fill: new DOMMatrix(getComputedStyle(document.querySelector('[data-fill]')).transform).a,
                    lit: document.querySelectorAll('[data-stop][data-lit]').length,
                    ticks: document.querySelectorAll('[data-tick][data-on]').length,
                    focus: cards.length ? { ok: nearest === sharpest || nearest.blur < 0.6, nearest: nearest.blur, blurs: cards.map(c => c.blur.toFixed(1)) } : null,
                  };
                })()""")
                xs.append(round(state["x"]))
                fills.append(round(state["fill"], 2))
                lit.append(state["lit"])
                ticks.append(state["ticks"])
                focus.append(state["focus"])
                shoot(page, f"{tag}-strip-{int(step * 100):02d}")
            slides = all(a > b for a, b in zip(xs, xs[1:])) and xs[-1] < -800
            fills_ok = all(a < b for a, b in zip(fills, fills[1:])) and fills[-1] > 0.95
            lights = lit == sorted(lit) and lit[0] < lit[-1] and lit[-1] >= 6 and ticks == sorted(ticks) and ticks[-1] == 5
            in_focus = [f["ok"] for f in focus if f]
            soft_edges = any(f and max(float(b) for b in f["blurs"]) > 2 for f in focus)
            check(f"{tag}: the strip pins and slides; the gold line fills; stops light in order",
                  slides and fills_ok and lights, f"x={xs} fill={fills} lit={lit} ticks={ticks}")
            check(f"{tag}: pictures are sharp in the middle and soft at the sides",
                  all(in_focus) and soft_edges, f"{focus}")
        else:
            x = page.evaluate("new DOMMatrix(getComputedStyle(document.querySelector('[data-track]')).transform).m41")
            rail = page.evaluate("getComputedStyle(document.querySelector('[data-fill]').parentElement.parentElement).display")
            check(f"{tag}: phones get the path top to bottom (no sideways slide, no line)", x == 0 and rail == "none", f"x={x} rail={rail}")

        # Walk the rest of the opening (the strip on phones, what follows the pin on wide screens).
        research = top_of(page, "#research")
        y = page.evaluate("scrollY")
        while y + h * 0.85 < research and n < 60:
            y += h * 0.85
            walk(page, y)
            page.wait_for_timeout(1100)
            shoot(page, f"{tag}-{n:02d}", exempt_track=wide)
            n += 1
        if not wide:
            blurs = page.evaluate("[...document.querySelectorAll('[data-card-media]')].map(m => getComputedStyle(m).filter)")
            check(f"{tag}: every picture on the phone strip came into focus", all(blur_of(b) == 0 for b in blurs), str(blurs))
        loaded = page.evaluate("[...document.querySelectorAll('#scientists img')].map(i => i.naturalWidth)")
        check(f"{tag}: every picture in the opening loaded", len(loaded) == 8 and all(v > 0 for v in loaded), str(loaded))
        inside = page.evaluate(INSIDE)
        check(f"{tag}: no words cut off inside the cards", not inside, "; ".join(inside[:4]))

        # The shared sections, one screen each.
        for part in ("research", "health", "ask"):
            walk(page, top_of(page, f"#{part}"))
            page.wait_for_timeout(900)
            shoot(page, f"{tag}-z-{part}")
        walk(page, page.evaluate("document.documentElement.scrollHeight"))
        page.wait_for_timeout(600)
        shoot(page, f"{tag}-z-footer")
        ov = overflow(page)
        check(f"{tag}: no sideways scroll, no errors", ov == 0 and not problems, f"overflow={ov} {problems[:3]}")
        mine = [c for c in clipped_seen if c.startswith(tag + "-")]
        check(f"{tag}: no words cut off at the screen edge", not mine, "; ".join(mine[:4]))
        ctx.close()

    # Reduced motion: no pin, no scroll scenes, everything readable and visible at once.
    for label, (w, h) in {"desk": (1440, 900), "phone": (390, 844)}.items():
        tag = f"d-reduced-{label}"
        ctx, page, problems = open_page(browser, w, h, reduced=True)
        page.wait_for_timeout(900)
        state = page.evaluate("""(() => ({
          pinned: !!document.querySelector('.pin-spacer'),
          x: new DOMMatrix(getComputedStyle(document.querySelector('[data-track]')).transform).m41,
          photo: getComputedStyle(document.querySelector('[data-photo]')).filter,
          drift: getComputedStyle(document.querySelector('[data-hero-media] > div')).animationName,
          faded: [...document.querySelectorAll('#scientists p, #scientists h1, #scientists h2, #scientists h3, #scientists a')]
            .filter(e => { let n = e; while (n && n !== document.body) { if (+getComputedStyle(n).opacity < 0.99) return true; n = n.parentElement; } return false; })
            .map(e => e.textContent.trim().slice(0, 24)),
        }))()""")
        check(f"{tag}: calm version, nothing pinned, drifting or faded",
              not state["pinned"] and state["x"] == 0 and state["photo"] == "none" and state["drift"] == "none" and not state["faded"] and not problems,
              f"{state} {problems[:2]}")
        y, n = 0, 0
        research = top_of(page, "#research")
        while y < research and n < 40:
            shoot(page, f"{tag}-{n:02d}", exempt_track=False)
            y += h * 0.85
            walk(page, y, steps=2)
            page.wait_for_timeout(250)
            n += 1
        ov = overflow(page)
        mine = [c for c in clipped_seen if c.startswith(tag + "-")] + page.evaluate(INSIDE)
        check(f"{tag}: no sideways scroll, no words cut off or covered", ov == 0 and not mine, f"overflow={ov} {mine[:3]}")
        ctx.close()
    browser.close()

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)

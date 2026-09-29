"""Browser checks for Green Bee Propolis's page (September 29, 2026): its own facts and pictures.

The template's chapters have their own checks; run them with --product=green-bee-propolis:
    python -X utf8 scripts/qa/qa_why_chapter.py http://localhost:3010 --product=green-bee-propolis
    python -X utf8 scripts/qa/qa_research_daily.py http://localhost:3010 --product=green-bee-propolis
This script checks what only this page has, at 1440x900 and 390x844 (and once with reduced motion):
- the opening: the headline, the eyebrow on one line and clear of the giant name, the name's two
  halves with a word space on phones and parted round the bottle on wide screens, the 3D bottle
  arriving in amber glass (not white plastic), no sideways scroll;
- what's inside: one ingredient shown large (200 mg), and the full label (2019 label, awaiting Mo's
  confirmation): the extract, its amount, the other ingredients;
- buy: the 3D bottle, the directions and the supply, six questions that open, the four other
  products, and the footer's caution (bee products) and FDA line;
- the homepage links here; no console errors, page errors or failed requests.

    python -X utf8 scripts/qa/qa_green_bee_propolis.py http://localhost:3010
Pictures: scripts/qa/out/propolis-<size>-<name>.png (viewport shots).
"""

import io
import os
import sys

import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

BASE = next((a for a in sys.argv[1:] if a.startswith("http")), "http://localhost:3007").rstrip("/")
URL = f"{BASE}/products/green-bee-propolis"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)
ARGS = ["--use-gl=angle", "--use-angle=d3d11", "--enable-gpu", "--ignore-gpu-blocklist"]
passed = failed = 0


def check(name, ok, detail=""):
    global passed, failed
    passed += bool(ok)
    failed += not ok
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))


def open_page(browser, url, w, h, reduced=False):
    ctx = browser.new_context(viewport={"width": w, "height": h}, reduced_motion="reduce" if reduced else "no-preference")
    page = ctx.new_page()
    problems = []
    page.on("console", lambda m: problems.append(f"console {m.text[:200]}") if m.type == "error" and "Failed to load resource" not in m.text else None)
    page.on("pageerror", lambda e: problems.append(f"pageerror {e}"))
    page.on("response", lambda r: problems.append(f"{r.status} {r.url[-80:]}") if r.status >= 400 and "/_next/static/chunks/" not in r.url else None)
    page.goto(url, wait_until="networkidle")
    page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
    return ctx, page, problems


def shot(page, name):
    path = os.path.join(OUT, f"propolis-{name}.png")
    page.screenshot(path=path)
    return path


def amber_pixels(page, selector):
    """How many of the stage's pixels are dark amber glass (warm, dark, strongly coloured). White
    plastic has none; the bottle's glass has thousands however large the stage around it."""
    box = page.locator(selector).bounding_box()
    img = np.asarray(Image.open(io.BytesIO(page.screenshot(clip=box))).convert("RGB")).astype(float)
    r, g, b = img[..., 0], img[..., 1], img[..., 2]
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    amber = (r > g + 12) & (g > b) & (r - b > 35) & (lum < 110)
    return int(amber.sum())


def scroll_to(page, chapter, offset=0.0):
    page.evaluate(f"""(() => {{ const s = document.querySelector('[data-chapter="{chapter}"]');
      window.scrollTo(0, s.getBoundingClientRect().top + scrollY + {offset} * innerHeight); }})()""")
    page.wait_for_timeout(1200)


OPENING = """(() => {
  const hero = document.querySelector('[data-chapter="overview"]');
  const box = e => { const r = e.getBoundingClientRect(); return { top: r.top, bottom: r.bottom, left: r.left, right: r.right, height: r.height }; };
  const eyebrow = hero.querySelector('[data-intro="eyebrow"]');
  const halves = [...hero.querySelectorAll('[data-giant-half]')];
  const giant = halves[0].parentElement;
  return {
    h1: hero.querySelector('h1').textContent.replace(/\\s+/g, ' ').trim(),
    eyebrow: eyebrow.textContent.replace(/\\s+/g, ' ').trim(), eyebrowBox: box(eyebrow),
    eyebrowLine: parseFloat(getComputedStyle(eyebrow).lineHeight),
    halves: halves.map(e => e.textContent), halfBoxes: halves.map(box),
    nameSize: parseFloat(getComputedStyle(giant).fontSize), spaced: giant.dataset.spaced === 'true',
    stage: box(hero.querySelector('[data-status]')), status: hero.querySelector('[data-status]').dataset.status,
    sideways: document.documentElement.scrollWidth <= innerWidth,
  };
})()"""


def run(browser, label, w, h):
    ctx, page, problems = open_page(browser, URL, w, h)
    phone = w < 900
    try:
        page.wait_for_selector("[data-chapter='overview'] [data-status='ready']", timeout=20000)
    except Exception:  # noqa: BLE001
        pass
    page.wait_for_timeout(3500)
    o = page.evaluate(OPENING)
    shot(page, f"{label}-opening")
    # The h1 also carries the name for screen readers and the split words' own copy.
    check(f"{label} opening: the headline", "Distinctive green propolis." in o["h1"], o["h1"])
    check(f"{label} opening: the eyebrow, on one line",
          o["eyebrow"] == "Green Bee Propolis · Made by bees" and o["eyebrowBox"]["height"] < o["eyebrowLine"] * 1.5,
          f"{o['eyebrow']!r} {o['eyebrowBox']['height']:.0f}px")
    a, b = o["halfBoxes"]
    check(f"{label} opening: the giant name parts as 'Green Bee' | 'Propolis', clear of the eyebrow",
          o["halves"] == ["Green Bee", "Propolis"] and o["spaced"] and a["top"] >= o["eyebrowBox"]["bottom"] - 2,
          f"{o['halves']} eyebrow bottom {o['eyebrowBox']['bottom']:.0f}, name top {a['top']:.0f}")
    gap = b["left"] - a["right"]
    if phone:
        check(f"{label} opening: on a phone the two halves keep a word space", 0.15 * o["nameSize"] <= gap <= 0.5 * o["nameSize"],
              f"gap {gap:.0f}px at {o['nameSize']:.0f}px")
    else:
        middle = (o["stage"]["left"] + o["stage"]["right"]) / 2
        check(f"{label} opening: on a wide screen the halves part round the bottle", a["right"] < middle - 60 and b["left"] > middle + 60,
              f"{a['right']:.0f} | {middle:.0f} | {b['left']:.0f}")
    amber = amber_pixels(page, "[data-chapter='overview'] [data-status]")
    check(f"{label} opening: the 3D bottle arrives in amber glass", o["status"] == "ready" and amber > 3000,
          f"status={o['status']} amber pixels={amber}")
    check(f"{label} opening: no sideways scroll", o["sideways"])

    # What's inside: one ingredient, large; the full label.
    scroll_to(page, "inside", 0.1)
    inside = page.evaluate("""(() => { const s = document.querySelector('[data-chapter="inside"]');
      const ol = s.querySelector('ol'); const li = ol.querySelector('li');
      return { single: /single/.test(ol.className), rows: ol.children.length,
        amount: li.querySelector('p').textContent.replace(/\\s+/g, ' ').trim(),
        size: parseFloat(getComputedStyle(li.querySelector('p')).fontSize),
        name: li.querySelector('h3').textContent }; })()""")
    shot(page, f"{label}-inside")
    check(f"{label} inside: one ingredient, its amount large", inside["single"] and inside["rows"] == 1
          and inside["amount"].startswith("200") and inside["amount"].endswith("mg") and inside["size"] >= 72
          and inside["name"] == "Green propolis extract", str(inside))
    page.get_by_role("button", name="See the full label").click()
    page.wait_for_timeout(500)
    panel = page.evaluate("""(() => { const t = document.querySelector('[data-chapter="inside"] table');
      const panel = t.closest('div'); return { hidden: panel.hidden, text: panel.textContent }; })()""")
    shot(page, f"{label}-label")
    check(f"{label} inside: the full label opens with the extract, 200 mg and the other ingredients",
          not panel["hidden"] and "Green Bee Propolis Extract" in panel["text"] and "200 mg" in panel["text"]
          and "rice flour, silicon dioxide and magnesium stearate" in panel["text"]
          and "hypromellose, titanium dioxide and yellow iron oxide" in panel["text"], panel["text"][:120])

    # Buy.
    scroll_to(page, "buy", 0.0)
    try:
        page.wait_for_selector("[data-chapter='buy'] [data-status='ready']", timeout=20000)
    except Exception:  # noqa: BLE001
        pass
    page.wait_for_timeout(3000)
    shot(page, f"{label}-buy")
    buy = page.evaluate("""(() => { const s = document.querySelector('[data-chapter="buy"]');
      return { status: s.querySelector('[data-status]').dataset.status, text: s.textContent,
        questions: [...s.querySelectorAll('button[aria-expanded]')].map(b => b.textContent.trim()),
        cards: [...s.querySelectorAll('ul a[href]')].map(a => [a.textContent.trim().slice(0, 24), a.getAttribute('href')]) }; })()""")
    amber = amber_pixels(page, "[data-chapter='buy'] [data-status]")
    check(f"{label} buy: the 3D bottle in amber glass", buy["status"] == "ready" and amber > 3000,
          f"status={buy['status']} amber pixels={amber}")
    check(f"{label} buy: directions and supply", "Take 1 capsule a day." in buy["text"] and "60 vegetarian capsules · 60-day supply" in buy["text"])
    check(f"{label} buy: six questions", len(buy["questions"]) == 6, str(buy["questions"]))
    first = page.locator("[data-chapter='buy'] button[aria-expanded]").first
    first.scroll_into_view_if_needed()
    first.click()
    page.wait_for_timeout(400)
    opened = page.evaluate("""(() => { const b = document.querySelector('[data-chapter="buy"] button[aria-expanded]');
      const a = document.getElementById(b.getAttribute('aria-controls')); return [b.getAttribute('aria-expanded'), a.hidden, a.textContent]; })()""")
    shot(page, f"{label}-questions")
    check(f"{label} buy: a question opens its answer", opened[0] == "true" and not opened[1] and "1 capsule a day" in opened[2], str(opened))
    names = [c[0] for c in buy["cards"]]
    check(f"{label} buy: the four other products, NuriCell linking to its page",
          len(buy["cards"]) == 4 and names[0].startswith("NuriCell") and buy["cards"][0][1].endswith("/products/nuricell"),
          str(buy["cards"]))
    footer = page.evaluate("document.querySelector('footer').textContent")
    check(f"{label} footer: the caution (bee products) and the FDA line",
          "allergic to bee products" in footer and "Food and Drug Administration" in footer)
    check(f"{label}: no console errors, page errors or failed requests", not problems, str(problems[:3]))
    ctx.close()


def run_reduced(browser):
    ctx, page, problems = open_page(browser, URL, 1440, 900, reduced=True)
    page.wait_for_timeout(2500)
    st = page.evaluate("""(() => ({ chapters: [...document.querySelectorAll('[data-chapter]')].map(s => s.dataset.chapter),
      h1: getComputedStyle(document.querySelector('h1')).opacity }))()""")
    check("reduced motion: six chapters, the headline shown, no errors",
          st["chapters"] == ["overview", "why", "inside", "research", "daily", "buy"] and float(st["h1"]) == 1 and not problems,
          f"{st} {problems[:2]}")
    ctx.close()


def run_home(browser):
    ctx, page, problems = open_page(browser, f"{BASE}/", 1440, 900)
    links = page.evaluate("[...document.querySelectorAll('a[href]')].filter(a => a.getAttribute('href').endsWith('/products/green-bee-propolis')).length")
    check("homepage: links to the Green Bee Propolis page", links >= 1, f"{links} links")
    ctx.close()


with sync_playwright() as p:
    browser = p.chromium.launch(args=ARGS)
    run(browser, "desktop", 1440, 900)
    run(browser, "phone", 390, 844)
    run_reduced(browser)
    run_home(browser)
    browser.close()

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)

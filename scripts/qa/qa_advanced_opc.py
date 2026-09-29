"""QA for the Advanced OPC Formula product page (Template 2, "Chapters"), September 28, 2026.

At 1440x900 and 390x844 with motion, then both again with reduced motion:
- the page answers in English and Korean; the chapter index has seven chapters, "The people" with
  Dr. Iris Wang, text only (she asked for no photograph)
- overview: the name, the approved headline and purpose, the 3D bottle drawn (not the flat photo)
- the photo moment: the still life loads and its line reads "Nine plant extracts. One formula."
- why, at night (motion): the three lines and the title arrive one at a time, in order; the grapes
  are dark for the first line and lit from the second; no words over the grapes; every line at
  least 4.5:1 against the pixels behind it; no edge where the photo meets the page's night
- inside: 13 ingredients; six rows, then "Show all 13 ingredients" opens the rest; the nine plant
  rows lead with a round photo, the four others keep an empty slot; the full label table has the 13
  amounts exactly as printed on the label, per serving of 2 capsules
- research: five studies, oldest first, every link a PubMed page opening in a new tab with noopener
- how to take it: "One bottle, two months." ending at 120 capsules and 60 days
- buy: the credit line (Dr. Iris Wang); the supply line; the four other products, NuriCell first, linking their pages
- questions: six, the first one opens
- homepage: Advanced OPC Formula's Discover link opens /products/advanced-opc
- buy's 3D bottle draws after a fast jump straight to it, three fresh pages in a row
- everywhere: no horizontal page scroll, no console errors or failed requests

Pictures: scripts/qa/out/opc-<run>-<nn>-<name>.png (viewport shots; full-page shots break svh).

    python -X utf8 scripts/qa/qa_advanced_opc.py http://localhost:3011 [--gpu]
"""
import io
import json
import os
import sys

import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

BASE = (sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "http://localhost:3011").rstrip("/")
URL = f"{BASE}/products/advanced-opc"
GPU = "--gpu" in sys.argv
ARGS = (
    ["--use-gl=angle", "--use-angle=d3d11", "--enable-gpu", "--ignore-gpu-blocklist"]
    if GPU
    else ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"]
)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)
NIGHT = (6, 22, 37)
CHAPTERS = ["Overview", "Why it matters", "What’s inside", "The research", "The people", "How to take it", "Buy"]
CREDIT = "Formulated under the guidance of Dr. Iris Wang."
# The nine plant rows carry a round photo; the vitamins and selenium do not.
PICTURED = ["grape-seed", "pine-bark", "red-wine", "bilberry", "tea", "citrus", "noni", "lutein", "melilotus"]
WHY = [
    "Making energy also makes a few free radicals—unstable molecules that can damage cells.",
    "Antioxidants keep them in balance. Your body makes its own, and plants are full of them.",
    "Grape seeds and pine bark are rich in OPCs, plant compounds that act as antioxidants.",
    "A balance worth keeping.",
]
# The 2019 label (old-storage/.../uploads/2019/04/sup_opc.png), per serving of 2 capsules.
LABEL = {
    "Grape seed extract (Vitis vinifera, 95% polyphenols)": "25 mg",
    "Pine bark (Pinus pinaster, 95% polyphenol)": "25 mg",
    "Red wine 10:1": "25 mg",
    "Bilberry (fruit) extract (Vaccinium myrtillus, 25% anthocyanosides)": "25 mg",
    "Tea (leaf) extract blend from white tea 30%, green tea 45 and black tea 20% polyphenols, Camellia sinensis": "40 mg",
    "Citrus bioflavonoids (fruit) 25%": "100 mg",
    "Noni concentrate (fruit) (Morinda citrifolia 5:1)": "25 mg",
    "Lutein (marigold petal extract 5% from flower)": "3 mg",
    "LymphaSelect (flower) (Melilotus officinalis extract)": "20 mg",
    "Vitamin C (from ascorbic acid)": "300 mg",
    "Vitamin E (as d-alpha-tocopherol succinate, natural E)": "20 IU",
    "Gamma-tocopherol": "5 mg",
    "Selenium (as selenomethionine)": "10 mcg",
}
YEARS = ["2008", "2010", "2011", "2020", "2024"]
passed = failed = 0


def check(name, ok, detail=""):
    global passed, failed
    passed += bool(ok)
    failed += not ok
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))


def open_page(browser, w, h, reduced=False, url=URL):
    ctx = browser.new_context(
        viewport={"width": w, "height": h}, reduced_motion="reduce" if reduced else "no-preference"
    )
    page = ctx.new_page()
    problems = []
    page.on(
        "console",
        lambda m: problems.append(f"console {m.text[:200]}")
        if m.type == "error" and "Failed to load resource" not in m.text
        else None,
    )
    page.on("pageerror", lambda e: problems.append(f"pageerror {e}"))
    page.on(
        "response",
        lambda r: problems.append(f"{r.status} {r.url[-90:]}")
        if r.status >= 400 and "/_next/static/chunks/" not in r.url
        else None,
    )
    response = page.goto(url, wait_until="networkidle")
    status = response.status if response else 0
    page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
    page.wait_for_timeout(3000)
    return ctx, page, problems, status


def glide(page, y, steps=10):
    current = page.evaluate("scrollY")
    for s in range(1, steps + 1):
        page.evaluate(f"window.scrollTo({{top: {current + (y - current) * s / steps}, behavior: 'instant'}})")
        page.wait_for_timeout(30)


def box(page, selector):
    return page.evaluate(f"""(() => {{ const s = document.querySelector({json.dumps(selector)});
      if (!s) return null; const r = s.getBoundingClientRect();
      return {{ top: Math.round(r.top + scrollY), height: s.offsetHeight }}; }})()""")


def shot(page, run, n, name):
    path = os.path.join(OUT, f"opc-{run}-{n:02d}-{name}.png")
    page.screenshot(path=path)
    return path


NO_SIDEWAYS = "document.documentElement.scrollWidth <= innerWidth"

TRACK = "document.querySelector('[data-chapter=\"why\"] [style*=\"--beats\"]')"
STATE = f"""(() => {{
  const track = {TRACK};
  const op = el => el ? +getComputedStyle(el).opacity : 0;
  const moments = [...track.querySelectorAll('[data-why-moment]')];
  const vis = moments.map(m => {{
    let v = op(m);
    if (m.matches('[data-why-title]')) {{
      const first = m.querySelector('.tc-line');
      if (first) v = Math.min(v, Math.abs(new DOMMatrix(getComputedStyle(first).transform).m42) < 2 ? 1 : 0);
    }}
    return Math.round(v * 50) / 50;
  }});
  return {{ vis, lit: Math.round(op(track.querySelector('[data-why-lit]')) * 50) / 50,
    texts: moments.map(m => m.textContent.trim()) }};
}})()"""
# Visible text boxes in the chapter, the grapes' box and the fixed chapter index.
TEXTS = f"""(() => {{
  const track = {TRACK};
  const W = innerWidth, H = innerHeight, out = [];
  const walker = document.createTreeWalker(track, NodeFilter.SHOW_TEXT);
  let node;
  while ((node = walker.nextNode())) {{
    if (!node.nodeValue.trim()) continue;
    const el = node.parentElement;
    let alpha = 1;
    for (let a = el; a && a !== track.parentElement; a = a.parentElement) alpha *= +getComputedStyle(a).opacity;
    if (alpha < 0.9 || getComputedStyle(el).visibility !== 'visible') continue;
    const range = document.createRange();
    range.selectNodeContents(node);
    for (const r of range.getClientRects()) {{
      if (r.width < 2 || r.height < 2 || r.bottom <= 0 || r.top >= H) continue;
      out.push({{ text: (el.closest('p, h2') || el).textContent.trim().slice(0, 40),
        x0: Math.max(0, r.left), y0: Math.max(0, r.top), x1: Math.min(W, r.right), y1: Math.min(H, r.bottom),
        color: getComputedStyle(el).color }});
    }}
  }}
  const clip = track.querySelector('[data-why-picture]').getBoundingClientRect();
  const f = track.querySelector('[data-why-frame]').getBoundingClientRect();
  // The grapes and their stem in the photo: 51-84% across, the top to 92% down.
  const grapes = {{ x0: Math.max(clip.left, f.left + 0.51 * f.width), x1: Math.min(clip.right, f.left + 0.84 * f.width),
    y0: Math.max(clip.top, f.top), y1: Math.min(clip.bottom, f.top + 0.92 * f.height) }};
  return {{ texts: out, grapes, frame: {{ x0: f.left, x1: f.right }}, picture: {{ x0: clip.left, y1: clip.bottom }} }};
}})()"""
HIDE = f"""{TRACK}.querySelectorAll('[data-why-copy], p').forEach(e => e.style.visibility = 'hidden');
  document.querySelectorAll("nav[aria-label='Chapters']").forEach(e => e.style.visibility = 'hidden')"""
SHOW = f"""{TRACK}.querySelectorAll('[data-why-copy], p').forEach(e => e.style.visibility = '');
  document.querySelectorAll("nav[aria-label='Chapters']").forEach(e => e.style.visibility = '')"""


def luminance(rgb):
    c = np.asarray(rgb, dtype=np.float64) / 255
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return c[..., 0] * 0.2126 + c[..., 1] * 0.7152 + c[..., 2] * 0.0722


def rgba(css):
    inside = css[css.index("(") + 1: css.index(")")].replace("/", ",").replace(" ", ",")
    parts = [float(p) for p in inside.split(",") if p]
    return parts[:3], (parts[3] if len(parts) > 3 else 1.0)


def intersects(a, b, margin=6):
    return a["x0"] < b["x1"] - margin and a["x1"] > b["x0"] + margin and a["y0"] < b["y1"] - margin and a["y1"] > b["y0"] + margin


def legibility(page):
    info = page.evaluate(TEXTS)
    page.evaluate(HIDE)
    page.wait_for_timeout(120)
    bg = np.asarray(Image.open(io.BytesIO(page.screenshot())).convert("RGB"), dtype=np.float64)
    page.evaluate(SHOW)
    over, worst = [], 99.0
    for t in info["texts"]:
        if intersects(t, info["grapes"]):
            over.append(t["text"])
        region = bg[int(t["y0"]): int(t["y1"]), int(t["x0"]): int(t["x1"])]
        if region.size == 0:
            continue
        lum = luminance(region.reshape(-1, 3))
        bright = float(np.percentile(lum, 99))
        base = region.reshape(-1, 3)[int(np.argmin(np.abs(lum - bright)))]
        rgb, alpha = rgba(t["color"])
        lt = float(luminance(np.asarray(rgb) * alpha + base * (1 - alpha)))
        worst = min(worst, (max(lt, bright) + 0.05) / (min(lt, bright) + 0.05))
    return info, sorted(set(over)), round(worst, 1), bg


def settle(page, limit=3000):
    last, waited = None, 0
    page.wait_for_timeout(400)
    while waited < limit:
        state = page.evaluate(STATE)
        key = (tuple(state["vis"]), state["lit"])
        if key == last:
            return state
        last = key
        page.wait_for_timeout(160)
        waited += 160
    return page.evaluate(STATE)


def page_checks(page, label, status, reduced):
    check(f"{label}: the page answers", status == 200, str(status))
    names = page.evaluate("""[...document.querySelectorAll("nav[aria-label='Chapters'] ol a")]
      .map(a => a.textContent.replace(/^\\s*\\d+\\s*/, '').trim())""")
    check(f"{label}: seven chapters, with 'The people'", names == CHAPTERS, str(names))
    hero = page.evaluate("""(() => ({ h1: document.querySelector('h1').textContent,
      stage: document.querySelector('[data-status]')?.dataset.status }))()""")
    check(f"{label}: overview names the product with the approved headline",
          "Advanced OPC Formula" in hero["h1"] and "Nature’s antioxidant power. Focused on your cells." in hero["h1"], hero["h1"][:90])
    check(f"{label}: the 3D bottle is drawn", hero["stage"] == "ready", str(hero["stage"]))
    name = page.evaluate("""(() => { const g = document.querySelector('[data-giant-half="a"]').parentElement;
      const e = document.querySelector('[data-intro="eyebrow"]').getBoundingClientRect();
      const a = g.querySelector('[data-giant-half="a"]').getBoundingClientRect();
      const b = g.querySelector('[data-giant-half="b"]').getBoundingClientRect();
      return { spaced: g.hasAttribute('data-spaced'), gap: Math.round(b.left - a.right), size: parseFloat(getComputedStyle(g).fontSize), stacked: Math.abs(a.top - b.top) > 4,
        eyebrowBottom: Math.round(e.bottom), nameTop: Math.round(Math.min(a.top, b.top) + 0.12 * a.height) }; })()""")
    check(f"{label}: the giant name keeps its word space", name["spaced"] and (name["stacked"] or name["gap"] >= 0.15 * name["size"]), str(name))
    check(f"{label}: the eyebrow stands clear of the giant name", name["eyebrowBottom"] <= name["nameTop"], str(name))
    photo = page.evaluate("""(() => { const img = document.querySelector('[data-photo]');
      const line = document.querySelector('[data-photo-line]');
      return { loaded: !!img && img.complete && img.naturalWidth > 0, line: line && line.textContent.trim() }; })()""")
    check(f"{label}: the still life loads with its line", photo["loaded"] and photo["line"] == "Nine plant extracts. One formula.", str(photo))

    # Inside: six rows first, then all 13, and the full label.
    inside = box(page, "[data-chapter='inside']")
    glide(page, inside["top"], steps=8)
    page.wait_for_timeout(500)
    rows = page.evaluate("""[...document.querySelectorAll("[data-chapter='inside'] ol")]
      .map(o => o.hidden ? 0 : o.children.length)""")
    check(f"{label}: six ingredient rows shown first", rows == [6, 0], str(rows))
    page.get_by_role("button", name="Show all 13 ingredients").click()
    page.get_by_role("button", name="See the full label").click()
    page.wait_for_timeout(400)
    rows = page.evaluate("""[...document.querySelectorAll("[data-chapter='inside'] ol")]
      .map(o => o.hidden ? 0 : o.children.length)""")
    table = page.evaluate("""Object.fromEntries([...document.querySelectorAll("[data-chapter='inside'] table tbody tr")]
      .map(r => [r.querySelector('th').textContent.trim(), r.querySelector('td').textContent.replace(/\\s+/g, ' ').trim()]))""")
    caption = page.evaluate("document.querySelector(\"[data-chapter='inside'] table caption\").textContent")
    check(f"{label}: all 13 ingredients open", rows == [6, 7], str(rows))
    pics = page.evaluate("""[...document.querySelectorAll("[data-chapter='inside'] li")].map(li => {
      const slot = li.querySelector(':scope > span[aria-hidden]'); const img = slot && slot.querySelector('img');
      const r = slot && slot.getBoundingClientRect();
      return { slot: !!slot, src: img ? decodeURIComponent(img.currentSrc || img.src) : null, ok: !!img && img.complete && img.naturalWidth > 0,
        alt: img ? img.alt : null, round: slot ? getComputedStyle(slot).borderRadius : null, w: r ? Math.round(r.width) : 0 }; })""")
    shown = [next((k for k in PICTURED if p["src"] and f"/{k}.webp" in p["src"]), None) for p in pics]
    check(f"{label}: the nine plant rows show their round photo, the other four keep an empty slot",
          shown == PICTURED + [None] * 4 and all(p["slot"] for p in pics) and all(p["ok"] for p in pics[:9])
          and all(p["alt"] == "" for p in pics[:9]) and all(p["round"] == "50%" for p in pics),
          str([(s, p["ok"], p["w"]) for s, p in zip(shown, pics)]))
    check(f"{label}: the full label matches the printed label, amount for amount", table == LABEL,
          str({k: v for k, v in table.items() if LABEL.get(k) != v}))
    check(f"{label}: the label is per serving of 2 capsules", "2 capsules" in caption, caption)
    check(f"{label}: no sideways scroll with the lists open", page.evaluate(NO_SIDEWAYS))

    # Research: five studies, oldest first, safe PubMed links.
    studies = page.evaluate("""[...document.querySelectorAll("[data-chapter='research'] [data-study]")].map(s => ({
      text: s.textContent, href: s.querySelector('a')?.href, target: s.querySelector('a')?.target,
      rel: s.querySelector('a')?.rel }))""")
    years = [next((y for y in YEARS if y in s["text"]), "?") for s in studies]
    check(f"{label}: five studies, oldest first", years == YEARS, str(years))
    check(f"{label}: every study links to PubMed in a new tab with noopener",
          all(s["href"] and s["href"].startswith("https://pubmed.ncbi.nlm.nih.gov/") and s["target"] == "_blank"
              and "noopener" in s["rel"] for s in studies), str([s["href"] for s in studies]))

    people = page.evaluate("""(() => { const s = document.querySelector("[data-chapter='people']");
      return s ? { text: s.textContent, imgs: s.querySelectorAll('img').length } : null; })()""")
    check(f"{label}: the people chapter names Dr. Iris Wang, text only (no photograph)",
          people and "Dr. Iris Wang" in people["text"] and people["imgs"] == 0, str(people and people["imgs"]))

    # How to take it: the month fills to two months.
    daily = box(page, "[data-chapter='daily']")
    glide(page, daily["top"] + daily["height"] - page.viewport_size["height"], steps=16)
    page.wait_for_timeout(900)
    count = page.evaluate("document.querySelector(\"[data-chapter='daily'] h2\").textContent + ' | ' + "
                          "[...document.querySelectorAll(\"[data-chapter='daily'] p\")].map(p => p.textContent).join(' | ')")
    check(f"{label}: 'One bottle, two months.' ending at 120 capsules and 60 days",
          count.startswith("One bottle, two months.") and "120 capsules · 60 days" in count, count[:160])

    # Buy: no credit, the supply, the four others with NuriCell first.
    buy = page.evaluate("""(() => { const s = document.querySelector("[data-chapter='buy']");
      return { text: s.textContent, cards: [...s.querySelectorAll('ul a')].map(a => [a.textContent, a.getAttribute('href')]),
        questions: s.querySelectorAll('button[aria-expanded]').length }; })()""")
    check(f"{label}: the credit line", CREDIT in buy["text"], CREDIT)
    check(f"{label}: the supply line", "120 vegetarian capsules · 60 servings" in buy["text"])
    check(f"{label}: four other products, NuriCell first, linking its page",
          len(buy["cards"]) == 4 and buy["cards"][0][0].startswith("NuriCell") and buy["cards"][0][1].endswith("/products/nuricell"),
          str(buy["cards"]))
    first_q = page.locator("[data-chapter='buy'] button[aria-expanded]").first
    first_q.scroll_into_view_if_needed()
    first_q.click()
    page.wait_for_timeout(300)
    check(f"{label}: six questions; the first opens",
          buy["questions"] == 6 and first_q.get_attribute("aria-expanded") == "true", str(buy["questions"]))
    check(f"{label}: no sideways scroll at the end", page.evaluate(NO_SIDEWAYS))


def why_motion(page, label, run, w, h):
    where = box(page, "[data-chapter='why'] [style*='--beats']")
    texts = page.evaluate(STATE)["texts"]
    check(f"{label}: why carries its words, in order", texts == WHY, str([t[:30] for t in texts]))
    pinned = where["height"] - h
    steps, scan = 24, []
    glide(page, where["top"] - h, steps=10)
    for i in range(steps):
        y = where["top"] + int(pinned * (i + 0.5) / steps)
        glide(page, y, steps=6)
        state = settle(page)
        scan.append(state)
        if i % 4 == 1:
            shot(page, run, i, f"why-{i}")
    full = [[k for k, v in enumerate(s["vis"]) if v >= 0.95] for s in scan]
    order = []
    for f in full:
        for k in f:
            if not order or order[-1] != k:
                order.append(k)
    check(f"{label}: the lines and the title arrive one at a time, in order",
          order == list(range(len(WHY))) and all(len(f) <= 1 for f in full), f"order={order}")
    first = [s["lit"] for f, s in zip(full, scan) if f == [0]]
    later = [s["lit"] for f, s in zip(full, scan) if f and f[0] >= 1]
    check(f"{label}: the grapes are dark for the first line and lit from the second",
          first and later and max(first) <= 0.02 and min(later) >= 0.98, f"first={first} later={later}")
    # Legibility at each resting moment.
    bad, worst_all = [], 99.0
    for k in range(len(WHY)):
        idx = next((i for i, f in enumerate(full) if f == [k]), None)
        if idx is None:
            continue
        y = where["top"] + int(pinned * (idx + 0.5) / steps)
        glide(page, y, steps=4)
        settle(page)
        info, over, worst, bg = legibility(page)
        bad += over
        worst_all = min(worst_all, worst)
        if k == 1:
            # No edge where the picture meets the night: the plain ground at the picture's left edge
            # (wide screens), or across the picture's lower edge (phones, picture above the words).
            H = bg.shape[0]
            pic = info["picture"]
            if pic["y1"] < H - 20:
                yb = int(pic["y1"])
                above = bg[yb - 14: yb - 4, 4:40].reshape(-1, 3).mean(axis=0)
                below = bg[yb + 4: yb + 14, 4:40].reshape(-1, 3).mean(axis=0)
                delta, spot = float(np.abs(above - below).max()), f"lower edge at y{yb}"
            else:
                x0, y0 = int(max(pic["x0"], 0)) + 4, int(H * 0.45)
                patch = bg[y0: y0 + 40, x0: x0 + 20].reshape(-1, 3).mean(axis=0)
                delta, spot = float(np.abs(patch - NIGHT).max()), f"ground at x{x0} y{y0}"
            check(f"{label}: no edge where the photo meets the page's night", delta <= 4, f"Δ{delta:.1f} ({spot})")
    check(f"{label}: no words over the grapes", not bad, str(bad[:3]))
    check(f"{label}: every line at least 4.5:1 against the pixels behind it", worst_all >= 4.5, f"worst {worst_all}:1")


def fast_jumps(browser, label, w, h):
    """The buy chapter's bottle draws even after a fast jump straight to it (three fresh pages)."""
    statuses = []
    for _ in range(3):
        ctx, page, problems, status = open_page(browser, w, h)
        page.evaluate("window.scrollTo({top: document.querySelector('[data-chapter=\"buy\"]').offsetTop, behavior: 'instant'})")
        page.wait_for_timeout(3500)
        statuses.append(page.evaluate("document.querySelector('[data-chapter=\"buy\"] [data-status]')?.dataset.status"))
        ctx.close()
    check(f"{label}: after a fast jump to Buy the 3D bottle draws (3 of 3)", statuses == ["ready"] * 3, str(statuses))


def run(browser, w, h, reduced):
    label = f"{w}x{h}{' reduced' if reduced else ''}"
    tag = f"{w}{'r' if reduced else ''}"
    ctx, page, problems, status = open_page(browser, w, h, reduced)
    shot(page, tag, 0, "overview")
    if reduced:
        why = page.evaluate(f"""(() => {{ const t = {TRACK}; const op = e => +getComputedStyle(e).opacity;
          return {{ lit: op(t.querySelector('[data-why-lit]')), all: [...t.querySelectorAll('[data-why-moment]')].every(m => op(m) > 0.95) }}; }})()""")
        check(f"{label}: reduced motion shows the lit grapes and every line", why["lit"] > 0.95 and why["all"], str(why))
    else:
        why_motion(page, label, tag, w, h)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(400)
    page_checks(page, label, status, reduced)
    shot(page, tag, 99, "end")
    check(f"{label}: no console errors or failed requests", not problems, str(problems[:3]))
    ctx.close()


with sync_playwright() as p:
    browser = p.chromium.launch(args=ARGS)
    for w, h in [(1440, 900), (390, 844)]:
        for reduced in (False, True):
            run(browser, w, h, reduced)
        fast_jumps(browser, f"{w}x{h}", w, h)
    # The page exists in the other languages too, and the homepage links to it.
    ctx, page, problems, status = open_page(browser, 1440, 900, url=f"{BASE}/kr/products/advanced-opc")
    check("kr: the page answers in Korean", status == 200, str(status))
    ctx.close()
    ctx, page, problems, status = open_page(browser, 1440, 900, url=f"{BASE}/")
    hrefs = page.evaluate("[...document.querySelectorAll('a')].map(a => a.getAttribute('href')).filter(h => h && h.includes('advanced-opc'))")
    check("homepage: links open /products/advanced-opc", any(h.endswith("/products/advanced-opc") for h in hrefs), str(sorted(set(hrefs))))
    ctx.close()
    browser.close()

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)

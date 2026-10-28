"""QA for Advanced OPC Formula's ink page (Mo, October 16, 2026; picks and paintings in
reference/ink-pages/opc/README.md). The template is NuriCell's (qa_nuricell_ink.py); this checks
what Advanced OPC brings: "Advanced" small over "OPC" round the bottle with "Formula", the gold
spreading through the grapes, thirteen ingredients, a painting of Dr. Wang's work (no face), the
painted sum 2 × 60 = 120, the real bottle inside the vine scene.

Sections (all, or --only=a,b):
  shell       200 in the ink look, one h1 (Advanced OPC Formula), the real bottle, no canvas, no console
              errors (1440x900, 390x844)
  name        1920 to 360: "Advanced" small over "OPC" and as wide as it, both halves inside the wrap and
              clear of the bottle, on one row from 960px, side by side over the bottle below; vi too
  chapters    overview, why, inside, research, people, daily, buy; each its own painting; "thirteen
              ingredients"; 300 mg; Dr. Wang's words with a work painting captioned Illustration; the
              painted sum; every study; the questions
  spread      the gold waits, then fills the grapes from their middle; reduced motion and no script:
              filled from the first paint; its glint mask follows
  multiply    every painting multiplies onto the paper with no box
  buy         the real bottle (advanced-opc.png) stands inside the scene, centred; the front layer
              multiplies over its foot and changes nothing beside it; captioned; Add to cart
  size        both bottles exactly NuriCell's size (1440, 1024, 390)
  layout      sizes 1536 to 360: no sideways scroll, painting left of its words from 960px and above
              them below, text 15px+
  deep_links  #chapter-<id> lands its heading under the menu bar
  languages   kr, jp, cns, vn: 200, no console errors, the new strings translated
  sum         the shared sum (from qa_nuricell_ink.py, October 27, 2026): set in type (?ink-sum=type,
              ?ink-sum=odd, dev server only) each caption sits under its own numeral; in jp and cns
              no caption breaks inside its capsule word
Pictures: scripts/qa/out/opc-ink/.

usage: python -X utf8 scripts/qa/qa_opc_ink.py [base-url] [--only=shell,name,...]
"""

import io
import re
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = ARGS[0] if ARGS else "http://localhost:3052"
ONLY = next((a.split("=", 1)[1].split(",") for a in sys.argv[1:] if a.startswith("--only=")), None)
REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "scripts/qa/out/opc-ink"
OUT.mkdir(parents=True, exist_ok=True)
SLUG = "advanced-opc"
PATH = f"/en/products/{SLUG}"
CHAPTERS = ["overview", "why", "inside", "research", "people", "daily", "buy"]
PAINTED = ["why", "inside", "research", "people", "daily"]
PREFETCH_CSS = re.compile(r"was preloaded using link preload but not used")
# next dev (Turbopack, Next 16.2.6) logs a 404 for one chunk preload on old-template pages; this page
# has none, but the dev server is excused the same way qa_nuricell_ink.py excuses it.
CHUNK_404 = re.compile(r"/_next/static/chunks/.*404")
SIZES = [(1920, 1080), (1536, 864), (1440, 900), (1280, 800), (1024, 768), (960, 800), (900, 900), (768, 1024), (390, 844), (360, 780)]
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f"  ({detail})" if detail else ""), flush=True)


def opened(browser, w, h, path=PATH, reduced=False, js=True):
    ctx = browser.new_context(
        viewport={"width": w, "height": h},
        reduced_motion="reduce" if reduced else "no-preference",
        java_script_enabled=js,
    )
    page = ctx.new_page()
    errors = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" and not PREFETCH_CSS.search(m.text) and not CHUNK_404.search(m.text) else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    response = page.goto(BASE + path, wait_until="networkidle")
    if js:
        page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
    return ctx, page, response, errors


def development(response):
    """The dev server (next dev) answers every page with no-cache; a built site does not, whether
    `next start` (s-maxage) or Vercel (public, max-age=0, must-revalidate). Only the dev server
    honours the dev-only fixtures."""
    cache = (response.headers.get("cache-control") or "") if response is not None else ""
    return "no-cache" in cache or "no-store" in cache


def bring(page, selector, top=140):
    page.evaluate(
        "([s, t]) => { const e = document.querySelector(s); window.scrollBy(0, e.getBoundingClientRect().top - t); }",
        [selector, top],
    )


def patch(img, x, y, n=10):
    px = [img.getpixel((min(xx, img.width - 1), min(yy, img.height - 1))) for xx in range(x, x + n) for yy in range(y, y + n)]
    return tuple(round(sum(c[i] for c in px) / len(px), 1) for i in range(3))


def shell(browser):
    for w, h in [(1440, 900), (390, 844)]:
        ctx, page, response, errors = opened(browser, w, h)
        tag = f"shell {w}x{h}"
        check(f"{tag}: 200", response is not None and response.status == 200)
        check(f"{tag}: the ink look", page.locator('[data-look="ink"][data-page="products"]').count() == 1)
        check(f"{tag}: the ink page for Advanced OPC", page.locator(f'[data-product-ink="{SLUG}"]').count() == 1)
        check(f"{tag}: one h1", page.locator("h1").count() == 1)
        check(
            f"{tag}: the h1's accessible name is Advanced OPC Formula",
            page.get_by_role("heading", level=1, name="Advanced OPC Formula", exact=True).count() == 1,
        )
        check(f"{tag}: the real bottle in the opening", page.locator(f'[data-chapter="overview"] img[src*="{SLUG}.png"]').count() >= 1)
        check(f"{tag}: no canvas", page.locator("canvas").count() == 0)
        check(f"{tag}: no console errors", not errors, "; ".join(errors[:3]))
        page.wait_for_timeout(2500)
        page.screenshot(path=str(OUT / f"shell-{w}.png"))
        ctx.close()


NAME_BOXES = """() => {
  const h = document.querySelector('h1#product-name');
  const wrap = h.parentElement.getBoundingClientRect();
  const style = getComputedStyle(h.parentElement);
  const inner = [wrap.left + parseFloat(style.paddingLeft), wrap.right - parseFloat(style.paddingRight)];
  const box = (el) => { const r = el.getBoundingClientRect(); return { l: r.left, r: r.right, t: r.top, b: r.bottom }; };
  const first = h.querySelector('[class*=first]'), second = h.querySelector('[class*=second]');
  const lead = h.querySelector('[class*=lead]');
  const bottle = h.querySelector('[class*=stand] img');
  // The bottle's glass: the photo has a wide transparent margin (its visible part is 51.5% of its
  // width, centred).
  const b = box(bottle), mid = (b.l + b.r) / 2, half = (b.r - b.l) * 0.515 / 2;
  // The first half's own word ("OPC"): the first cell's box less the lead's.
  const range = document.createRange();
  const word = [...first.childNodes].find(n => n.nodeType === 3 && n.textContent.trim());
  let opc = null;
  if (word) { range.selectNodeContents(word); const r = range.getBoundingClientRect(); opc = { l: r.left, r: r.right, t: r.top, b: r.bottom }; }
  return { inner, first: box(first), second: box(second), opc,
           lead: lead ? { ...box(lead), size: parseFloat(getComputedStyle(lead).fontSize), text: lead.textContent.trim() } : null,
           size: parseFloat(getComputedStyle(h).fontSize),
           glass: { l: mid - half, r: mid + half, t: b.t, b: b.b } };
}"""


def name(browser):
    for locale in ["en", "vn"]:
        for w, h in SIZES:
            if locale == "vn" and w not in (1440, 1024, 390):
                continue
            ctx, page, _, _ = opened(browser, w, h, f"/{locale}/products/{SLUG}", reduced=True)
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(300)
            m = page.evaluate(NAME_BOXES)
            tag = f"name {locale} {w}x{h}"
            lo, hi = m["inner"]
            inside = m["first"]["l"] >= lo - 1 and m["second"]["r"] <= hi + 1 and m["first"]["r"] <= hi + 1 and m["second"]["l"] >= lo - 1
            check(f"{tag}: both halves inside the wrap", inside, f"wrap {lo:.0f}-{hi:.0f}, first {m['first']['l']:.0f}-{m['first']['r']:.0f}, second {m['second']['l']:.0f}-{m['second']['r']:.0f}")
            lead, opc = m["lead"], m["opc"]
            # The lead's box is its line box (line-height 0.86) and OPC's its glyph box, which reaches
            # above the line: the lead is over OPC when its box ends within a third of a size of OPC's top.
            over = lead is not None and opc is not None and lead["b"] <= opc["t"] + 0.34 * m["size"] and (lead["t"] + lead["b"]) < (opc["t"] + opc["b"])
            check(f"{tag}: Advanced over OPC, small", lead is not None and lead["text"] == "Advanced" and lead["size"] < 0.6 * m["size"] and over,
                  f"lead {lead['size']:.0f}px of {m['size']:.0f}px, lead bottom {lead['b']:.0f} vs OPC top {opc['t'] if opc else -1:.0f}" if lead else "no lead")
            if lead and opc:
                lw, ow = lead["r"] - lead["l"], opc["r"] - opc["l"]
                check(f"{tag}: Advanced as wide as OPC", abs(lw - ow) <= max(4, 0.06 * ow) and abs(lead["l"] - opc["l"]) <= 2, f"{lw:.0f} vs {ow:.0f}, left {lead['l']:.0f} vs {opc['l']:.0f}")
            if w >= 960:
                row = abs((m["first"]["t"] + m["first"]["b"]) / 2 - (m["second"]["t"] + m["second"]["b"]) / 2) < 0.35 * m["size"]
                clear = m["first"]["r"] <= m["glass"]["l"] + 1 and m["second"]["l"] >= m["glass"]["r"] - 1
                check(f"{tag}: one row, clear of the bottle's glass", row and clear,
                      f"first ends {m['first']['r']:.0f}, glass {m['glass']['l']:.0f}-{m['glass']['r']:.0f}, second starts {m['second']['l']:.0f}")
            else:
                beside = m["second"]["l"] >= m["first"]["r"] + 2 and m["glass"]["t"] >= max(m["first"]["b"], m["second"]["b"]) - 30
                check(f"{tag}: Advanced-OPC beside Formula over the bottle", beside,
                      f"first {m['first']['l']:.0f}-{m['first']['r']:.0f}, second {m['second']['l']:.0f}-{m['second']['r']:.0f}, bottle top {m['glass']['t']:.0f}")
            if locale == "en" and w in (1440, 1024, 390):
                page.screenshot(path=str(OUT / f"name-{w}.png"))
            ctx.close()


EXPECT = [
    "Why antioxidants matter",
    "A balance worth keeping.",
    "Making energy also makes a few free radicals",
    "Inside every capsule, thirteen ingredients.",
    "Grape seed extract",
    "Selenium",
    "Amounts per serving of 2 capsules, as printed on the Advanced OPC Formula label.",
    "Other ingredients: rice flour, magnesium stearate and silica.",
    "These studies are about antioxidants and this formula",
    "Dr. Iris Wang",
    "Formulation guidance",
    "In animal studies with Dr. Liu, she has researched oxidative damage",
    "One bottle, two months.",
    "Take 1 to 2 capsules once a day, with or after a meal.",
    "Formulated under the guidance of Dr. Iris Wang.",
    "What does OPC mean?",
    "These statements have not been evaluated by the Food and Drug Administration.",
]


def chapters(browser):
    ctx, page, _, _ = opened(browser, 1440, 900, reduced=True)
    found = page.evaluate("() => [...document.querySelectorAll('[data-chapter]')].map(c => c.dataset.chapter)")
    check("chapters: in order, with people", found == CHAPTERS, ", ".join(found))
    srcs = page.evaluate(
        """(ids) => ids.map(id => { const i = document.querySelector(`[data-chapter="${id}"] figure[data-picture] img`);
             return i ? decodeURIComponent(i.currentSrc || i.src) : null; })""",
        PAINTED + ["buy"],
    )
    check("chapters: each its own painting", all(srcs) and len(set(srcs)) == len(srcs), "; ".join(s or "none" for s in srcs))
    check("chapters: Advanced OPC's own paintings", all(f"{SLUG}/ink/" in s for s in srcs if s), "")
    rows = page.locator('[data-chapter="inside"] tbody tr').count()
    check("chapters: thirteen ingredient rows", rows == 13, f"{rows}")
    check("chapters: 300 mg", page.locator('[data-chapter="inside"]').get_by_text("300").count() >= 1)
    people = page.locator('[data-chapter="people"]')
    check("chapters: Dr. Wang's painting is of her work, captioned Illustration",
          people.locator("figure[data-picture] figcaption").inner_text().strip() == "Illustration"
          and "mortar" in people.locator("figure[data-picture] img").get_attribute("alt"),
          people.locator("figure[data-picture] figcaption").inner_text().strip())
    check("chapters: no photograph of Dr. Wang", people.locator("img[src*='.jpg'], img[src*='.jpeg'], img[src*='photo']").count() == 0)
    s = page.locator("[data-sum]")
    check("chapters: the painted sum", s.count() == 1 and s.get_attribute("data-sum-kind") == "painted", s.get_attribute("data-sum-kind") if s.count() else "none")
    labels = page.evaluate("() => [...document.querySelectorAll('[data-sum-label]')].map(e => e.textContent.trim())")
    check("chapters: a caption under each number", labels == ["capsules a day", "days", "capsules in each bottle"], ", ".join(labels))
    check("chapters: the sum reads 2 for 60 days, 120", "2 capsules a day for 60 days: 120 capsules" in page.locator("[data-sum-text]").inner_text())
    page.evaluate("""() => { document.querySelector('[data-chapter="research"] button[aria-expanded="false"]')?.click();
                         document.querySelectorAll('main details').forEach(d => { d.open = true; }); }""")
    page.wait_for_timeout(300)
    # The questions show one answer at a time: each is one click away, so pick each and read it.
    text = page.evaluate(
        """async () => { const answers = [];
             for (const b of document.querySelectorAll('#questions ol > li > h3 button')) {
               if (b.getAttribute('aria-expanded') !== 'true') b.click();
               await new Promise((r) => setTimeout(r, 60));
               answers.push(b.closest('li').querySelector('[role=region]').innerText); }
             return (document.body.innerText + ' ' + answers.join(' ')).replace(/\\s+/g, ' '); }"""
    )
    missing = [e for e in EXPECT if e not in text]
    check("chapters: the page's words", not missing, "; ".join(missing))
    studies = page.locator("[data-study]").count()
    check("chapters: all five studies", studies == 5, f"{studies}")
    alts = page.evaluate("() => [...document.querySelectorAll('main figure img[alt]')].map(i => i.alt).filter(Boolean)")
    check("chapters: every painting described", len(alts) >= 6, "; ".join(a[:30] for a in alts))
    capsules = page.locator('[data-chapter="overview"] img[src*="capsules-"]').count()
    check("chapters: the two capsules on the One bottle card", capsules == 1, f"{capsules}")
    ctx.close()


SPREAD = """() => { const f = document.querySelector('[data-chapter="why"] figure[data-spread]');
  const lit = f && f.querySelector('img[data-lit]'); const gold = f && f.querySelector('[class*=litGold]');
  return f ? { light: f.dataset.light, spread: getComputedStyle(lit).getPropertyValue('--spread').trim(),
               bloom: f.querySelector('img:not([data-lit])').dataset.bloom,
               mask: getComputedStyle(lit).maskImage || getComputedStyle(lit).webkitMaskImage,
               glint: gold ? Number(getComputedStyle(gold).opacity) : null } : null; }"""


def spread(browser):
    ctx, page, _, _ = opened(browser, 1440, 900)
    first = page.evaluate(SPREAD)
    check("spread: the Why figure spreads its gold (not the lantern)", first is not None and page.locator("[data-lantern]").count() == 0)
    if first is None:
        ctx.close()
        return
    check("spread: off before the chapter is seen", first["light"] == "off" and first["spread"] == "-14%", str(first))
    check("spread: radial from the grapes' middle", "radial-gradient" in (first["mask"] or ""), (first["mask"] or "")[:80])
    bring(page, '[data-chapter="why"] figure', 120)
    seen = []
    for _ in range(14):
        page.wait_for_timeout(500)
        seen.append(page.evaluate(SPREAD))
    mids = [s["spread"] for s in seen if s["light"] == "on"]
    partial = [m for m in mids if m not in ("-14%", "115%")]
    check("spread: comes on once seen", seen[-1]["light"] == "on", str(seen[-1]))
    check("spread: passes through partly filled", len(partial) >= 2, ", ".join(mids[:8]))
    check("spread: ends filled", seen[-1]["spread"] == "115%", seen[-1]["spread"])
    page.wait_for_timeout(3000)
    glint = page.evaluate(SPREAD)["glint"]
    check("spread: the gold's glint after the fill", glint == 1, str(glint))
    page.screenshot(path=str(OUT / "spread-1440.png"))
    ctx.close()
    for label, kwargs in [("reduced motion", {"reduced": True}), ("no script", {"js": False})]:
        ctx, page, _, _ = opened(browser, 1440, 900, **kwargs)
        page.locator('[data-chapter="why"] figure').scroll_into_view_if_needed()
        page.wait_for_timeout(300)
        state = page.evaluate(SPREAD) if kwargs.get("js", True) else None
        if state is not None:
            check(f"spread {label}: filled from the first paint", state["spread"] == "115%", str(state))
        else:
            shot = OUT / "spread-nojs.png"
            page.locator('[data-chapter="why"] figure').screenshot(path=str(shot))
            img = Image.open(shot).convert("RGB").convert("HSV")
            sat = img.tobytes()[1::3]
            gold = sum(1 for s in sat if s > 90) / len(sat)
            check(f"spread {label}: the gold shows", gold > 0.002, f"{gold:.4f} of pixels gold")
        ctx.close()


def multiply(browser):
    ctx, page, _, _ = opened(browser, 1440, 900, reduced=True)
    for chapter in PAINTED + ["buy"]:
        sel = f'[data-chapter="{chapter}"] figure[data-picture]'
        bring(page, sel, 160)
        page.wait_for_timeout(300)
        box = page.locator(sel).bounding_box()
        shot = OUT / f"multiply-{chapter}.png"
        page.screenshot(path=str(shot))
        img = Image.open(shot).convert("RGB")
        x, y = int(box["x"]), int(box["y"])
        inside, outside = patch(img, x + 2, y + 2), patch(img, max(0, x - 14), y + 2)
        diff = max(abs(a - b) for a, b in zip(inside, outside))
        check(f"multiply {chapter}: no box at its corner", diff <= 6, f"{inside} vs {outside}")
    ctx.close()


BUY = """() => { const f = document.querySelector('[data-chapter="buy"] figure[data-scene]');
  if (!f) return null;
  const stage = f.querySelector('[class*=sceneStage]'), fr = stage.getBoundingClientRect();
  const bottle = f.querySelector('img[class*=buyBottle]'), b = bottle.getBoundingClientRect();
  const front = f.querySelector('[data-scene-front]');
  return { src: decodeURIComponent(bottle.currentSrc || bottle.src), alt: bottle.alt,
           figure: [fr.left, fr.right, fr.top, fr.bottom], bottle: [b.left, b.right, b.top, b.bottom],
           front: front ? { blend: getComputedStyle(front).mixBlendMode, after: !!(bottle.compareDocumentPosition(front) & Node.DOCUMENT_POSITION_FOLLOWING),
                            hidden: front.getAttribute('aria-hidden') === 'true' && front.alt === '' } : null,
           caption: f.querySelector('figcaption')?.textContent.trim(),
           button: !!document.querySelector('[data-chapter="buy"] button') }; }"""


def front_only_on_bottle(page, m, tag):
    """The front layer changes the picture only over the bottle (it is cut to the bottle's shape):
    the stage drawn with and without it, every changed pixel inside the bottle's box."""
    fl, fr, ft, fb = m["figure"]
    clip = {"x": fl, "y": ft, "width": fr - fl, "height": fb - ft}
    with_front = Image.open(io.BytesIO(page.screenshot(clip=clip))).convert("RGB")
    page.evaluate("() => { document.querySelector('[data-scene-front]').style.visibility = 'hidden'; }")
    page.wait_for_timeout(200)
    without = Image.open(io.BytesIO(page.screenshot(clip=clip))).convert("RGB")
    page.evaluate("() => { document.querySelector('[data-scene-front]').style.visibility = ''; }")
    bl, br, bt, bb = m["bottle"]
    a, b = with_front.load(), without.load()
    outside = inside = 0
    for y in range(with_front.height):
        for x in range(with_front.width):
            if max(abs(c1 - c2) for c1, c2 in zip(a[x, y], b[x, y])) > 10:
                px, py = fl + x, ft + y
                if bl - 3 <= px <= br + 3 and bt - 3 <= py <= bb + 3:
                    inside += 1
                else:
                    outside += 1
    check(f"{tag}: the front layer touches only the bottle", outside == 0 and inside > 0, f"{inside} px on the bottle, {outside} beside it")


def buy(browser):
    for w, h in [(1440, 900), (1024, 768), (390, 844)]:
        ctx, page, _, _ = opened(browser, w, h, reduced=True)
        bring(page, '[data-chapter="buy"]', 100)
        page.wait_for_timeout(300)
        m = page.evaluate(BUY)
        tag = f"buy {w}x{h}"
        check(f"{tag}: a painted scene", m is not None)
        if m is None:
            ctx.close()
            continue
        check(f"{tag}: the real bottle photo", f"{SLUG}.png" in m["src"], m["src"][:90])
        check(f"{tag}: the bottle named", "Advanced OPC Formula" in m["alt"], m["alt"])
        fl, fr, ft, fb = m["figure"]
        bl, br, bt, bb = m["bottle"]
        centre = ((bl + br) / 2 - (fl + fr) / 2) / (fr - fl)
        check(f"{tag}: the bottle centred in the scene", abs(centre) < 0.02, f"{centre:+.3f}")
        check(f"{tag}: the bottle inside the scene", bt >= ft - 1 and bb <= fb + 1, f"bottle {bt:.0f}-{bb:.0f}, figure {ft:.0f}-{fb:.0f}")
        front = m["front"]
        check(f"{tag}: the front layer multiplies, over the bottle, unannounced", front is not None and front["blend"] == "multiply" and front["after"] and front["hidden"],
              str(front))
        front_only_on_bottle(page, m, tag)
        check(f"{tag}: captioned Illustration", m["caption"] == "Illustration", str(m["caption"]))
        check(f"{tag}: Add to cart", m["button"])
        page.locator('[data-chapter="buy"]').screenshot(path=str(OUT / f"buy-{w}.png"))
        ctx.close()


SIZE = """() => { const w = (s) => Math.round(document.querySelector(s)?.getBoundingClientRect().width ?? -1);
  return [w('[data-chapter=overview] img[class*=bottle]'), w('[data-chapter=buy] img[class*=buyBottle]')]; }"""


def bottle_size(browser):
    """Both bottles exactly NuriCell's size (Mo: as big as NuriCell's), at a laptop, a tablet and a phone."""
    for w, h in [(1440, 900), (1024, 768), (390, 844)]:
        sizes = {}
        for slug in ["nuricell", SLUG]:
            ctx, page, _, _ = opened(browser, w, h, f"/en/products/{slug}", reduced=True)
            sizes[slug] = page.evaluate(SIZE)
            ctx.close()
        a, b = sizes["nuricell"], sizes[SLUG]
        check(f"size {w}x{h}: the opening bottle as big as NuriCell's", abs(a[0] - b[0]) <= 2, f"{b[0]} vs {a[0]}")
        check(f"size {w}x{h}: the Buy bottle as big as NuriCell's", abs(a[1] - b[1]) <= 2, f"{b[1]} vs {a[1]}")


def layout(browser):
    for w, h in SIZES[1:]:
        ctx, page, _, _ = opened(browser, w, h, reduced=True)
        tag = f"layout {w}x{h}"
        wide = page.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
        check(f"{tag}: no sideways scroll", wide <= 0, f"{wide}px")
        bad = page.evaluate(
            """(two) => [...document.querySelectorAll('[data-chapter]:not([data-chapter="overview"])')].map(c => {
                 const f = c.querySelector('figure[data-picture]').getBoundingClientRect();
                 const t = c.querySelector('[data-words]').getBoundingClientRect();
                 const ok = two ? f.right <= t.left + 1 : f.bottom <= t.top + 1;
                 return ok ? null : c.dataset.chapter; }).filter(Boolean)""",
            w >= 960,
        )
        check(f"{tag}: each painting {'left of' if w >= 960 else 'above'} its words", not bad, ", ".join(bad))
        small = page.evaluate(
            """() => [...document.querySelectorAll('main p, main li, main dd, main dt, main td, main th, main figcaption')]
                 .filter(e => e.offsetParent && e.textContent.trim() && parseFloat(getComputedStyle(e).fontSize) < 15)
                 .map(e => e.textContent.trim().slice(0, 30))"""
        )
        check(f"{tag}: text 15px or larger", not small, "; ".join(small[:3]))
        ctx.close()


def deep_links(browser):
    for w, h in [(1440, 900), (390, 844)]:
        for chapter in CHAPTERS[1:]:
            ctx, page, _, _ = opened(browser, w, h, f"{PATH}#chapter-{chapter}", reduced=True)
            page.wait_for_timeout(400)
            top = page.evaluate(f"() => document.getElementById('chapter-{chapter}-title').getBoundingClientRect().top")
            bar = page.evaluate("() => document.querySelector('header').getBoundingClientRect().bottom")
            check(f"deep link {w} #{chapter}: heading under the bar, in the window", bar <= top <= h - 80, f"top {top:.0f}, bar {bar:.0f}")
            ctx.close()


# The Inside heading is English in every language today, as NuriCell's "four" is (the product data
# strings are not yet translated site-wide); the six painting descriptions are
# (reference/ink-pages/opc/translations-opc.cjs, drafts m700-m705).
HEADING = "Inside every capsule, thirteen ingredients."


def languages(browser):
    for locale in ["kr", "jp", "cns", "vn"]:
        ctx, page, response, errors = opened(browser, 1440, 900, f"/{locale}/products/{SLUG}", reduced=True)
        tag = f"languages {locale}"
        check(f"{tag}: 200", response is not None and response.status == 200)
        check(f"{tag}: no console errors", not errors, "; ".join(errors[:2]))
        heading = page.locator("#chapter-inside-title").inner_text().strip()
        check(f"{tag}: the thirteen-ingredient heading as NuriCell's (English for now)", heading == HEADING, heading)
        english = page.evaluate("() => [...document.querySelectorAll('main figure img[alt]')].map(i => i.alt).filter(a => /painted in/.test(a))")
        check(f"{tag}: the paintings described in {locale}", not english, "; ".join(english[:2]))
        ctx.close()


SUM_CAPTIONS = ["capsules a day", "days", "capsules in each bottle"]

# The shared sum (daily.tsx) moved here from qa_nuricell_ink.py on October 27, 2026, when
# NuriCell's chapter became the redwood round: Advanced OPC still shows a painted sum.
# Each caption's centre against its numeral's box, the caption below it, and nothing outside the sum.
SUM_TYPE_GEOMETRY = """() => {
  const figure = document.querySelector('[data-sum]').getBoundingClientRect();
  return [...document.querySelectorAll('[data-sum] [data-sum-type] > span')]
    .filter((cell) => cell.querySelector('[data-sum-numeral]')).map((cell) => {
      const n = cell.querySelector('[data-sum-numeral]').getBoundingClientRect();
      const c = cell.querySelector('[data-sum-label]').getBoundingClientRect();
      return { offset: c.left + c.width / 2 - (n.left + n.width / 2), half: n.width / 2, below: c.top - n.bottom,
               inside: c.left >= figure.left - 1 && c.right <= figure.right + 1 && n.left >= figure.left - 1 && n.right <= figure.right + 1,
               text: cell.querySelector('[data-sum-numeral]').textContent };
    });
}"""


def sum_type(browser):
    """The sum set in type (the dev-only ?ink-sum=type and ?ink-sum=odd fixtures; a painting whose
    numbers are not the serving's gets this): a caption directly under its own numeral, the x and =
    only when the numbers make that sum."""
    for fixture, numerals, operators in [("type", ["2", "60", "120"], True), ("odd", ["2", "60", "121"], False)]:
        for w, h in [(1440, 900), (390, 844)]:
            tag = f"sum type ({fixture}) {w}"
            ctx, page, response, errors = opened(browser, w, h, f"{PATH}?ink-sum={fixture}", reduced=True)
            if not development(response):
                # The fixtures are development only (daily.tsx): a built site (next start or the
                # demo) shows the product as given, the painted sum, for each of them.
                kind = page.locator("[data-sum]").get_attribute("data-sum-kind")
                check(f"sum type ({fixture}): a built site ignores ?ink-sum={fixture} (the painted sum)", kind == "painted", str(kind))
                print(f"NOTE sum type ({fixture}) skipped: a built site ignores ?ink-sum (run it against the dev server)")
                ctx.close()
                break
            try:
                page.wait_for_selector('[data-sum-kind="type"]', timeout=15000)
            except Exception:
                pass
            kind = page.locator("[data-sum]").get_attribute("data-sum-kind")
            check(f"{tag}: the type branch shows, no painting", kind == "type" and page.locator("[data-sum] img").count() == 0, str(kind))
            check(f"{tag}: no centres claimed", page.locator("[data-sum]").get_attribute("data-centres") is None)
            bring(page, "[data-sum]", 200)
            page.wait_for_timeout(300)
            cells = page.evaluate(SUM_TYPE_GEOMETRY)
            check(f"{tag}: three numerals {numerals}", [c["text"] for c in cells] == numerals, str([c["text"] for c in cells]))
            shown = page.locator("[data-sum] [data-sum-type]").inner_text()
            check(
                f"{tag}: the × and = {'shown' if operators else 'left out'}",
                ("×" in shown and "=" in shown) if operators else ("×" not in shown and "=" not in shown),
                repr(shown),
            )
            captions = page.locator("[data-sum] [data-sum-label]")
            check(f"{tag}: the visible captions are the three words", captions.all_inner_texts() == SUM_CAPTIONS and all(c.is_visible() for c in captions.all()), str(captions.all_inner_texts()))
            within = all(abs(c["offset"]) <= c["half"] for c in cells)
            check(f"{tag}: each caption's centre within its numeral", len(cells) == 3 and within, ", ".join(f"{c['offset']:.1f}/{c['half']:.1f}" for c in cells))
            check(f"{tag}: each caption under its numeral, all inside the figure", len(cells) == 3 and all(c["below"] >= -1 and c["inside"] for c in cells), str([(round(c["below"]), c["inside"]) for c in cells]))
            check(f"{tag}: no console errors", not errors, "; ".join(errors[:3]))
            page.screenshot(path=str(OUT / f"sum-type-{fixture}-{w}.png"))
            ctx.close()


# Each sum caption's lines: whole, and the word capsule (カプセル / 胶囊) alone, as the lines of its
# glyph rects (a word split across two lines has rects at two heights); inside the sum's figure.
SUM_CAPTION_LINES = """() => {
  const figure = document.querySelector('[data-sum]').getBoundingClientRect();
  const lines = (node, a, b) => {
    const r = document.createRange(); r.setStart(node, a); r.setEnd(node, b);
    const tops = [...r.getClientRects()].filter((x) => x.width > 0).map((x) => x.top).sort((p, q) => p - q);
    return tops.reduce((n, t, i) => (i === 0 || t - tops[i - 1] > 4 ? n + 1 : n), 0);
  };
  return [...document.querySelectorAll('[data-sum] [data-sum-label]')].map((el) => {
    const node = el.firstChild;
    const text = node.data;
    const word = ['カプセル', '胶囊'].find((w) => text.includes(w)) ?? null;
    const box = el.getBoundingClientRect();
    return { text, word, lines: lines(node, 0, text.length),
             wordLines: word ? lines(node, text.indexOf(word), text.indexOf(word) + word.length) : 0,
             inside: box.left >= figure.left - 1 && box.right <= figure.right + 1,
             wide: document.documentElement.scrollWidth > window.innerWidth };
  });
}"""


def sum_captions_whole(browser, locale, w, h):
    """jp and cns break anywhere between characters, which split カプセル and 胶囊 across two lines
    (1日のカ / プセル数): the captions keep their words whole and stay inside the figure."""
    ctx, page, _, _ = opened(browser, w, h, f"/{locale}/products/{SLUG}", reduced=True)
    bring(page, "[data-sum]", 200)
    page.wait_for_timeout(300)
    caps = page.evaluate(SUM_CAPTION_LINES)
    tag = f"languages {locale} {w}"
    having = [c for c in caps if c["word"]]
    check(f"{tag}: three sum captions", len(caps) == 3, str([c["text"] for c in caps]))
    check(
        f"{tag}: no caption breaks inside its capsule word",
        len(having) == 2 and all(c["wordLines"] == 1 for c in having),
        str([(c["text"], c["wordLines"]) for c in caps]),
    )
    check(f"{tag}: the captions stay inside the sum, no sideways scroll", all(c["inside"] and not c["wide"] for c in caps), str([(c["text"], c["inside"], c["wide"]) for c in caps]))
    ctx.close()


def sum_section(browser):
    sum_type(browser)
    for locale in ["jp", "cns"]:
        for w, h in [(1440, 900), (390, 844)]:
            sum_captions_whole(browser, locale, w, h)


SECTIONS = {
    "shell": shell,
    "name": name,
    "chapters": chapters,
    "spread": spread,
    "multiply": multiply,
    "buy": buy,
    "size": bottle_size,
    "layout": layout,
    "deep_links": deep_links,
    "languages": languages,
    "sum": sum_section,
}

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for section, run in SECTIONS.items():
            if ONLY is None or section in ONLY:
                run(browser)
        browser.close()
    failed = [r for r in results if not r[1]]
    print(f"\n{len(results) - len(failed)}/{len(results)} passed")
    sys.exit(1 if failed else 0)

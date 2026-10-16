"""QA for Turmerific's ink page (Mo, October 16, 2026; picks and paintings in
reference/ink-pages/turmerific/README.md). The template is NuriCell's (qa_nuricell_ink.py) with Green
Bee Propolis's additions (qa_propolis_ink.py); this checks what Turmerific brings: its one-word name
split round the bottle, the gold soaking into the paper, one ingredient, the painted 2 × 30 = 60,
the real bottle inside the painted turmeric plant.

Sections (all, or --only=a,b):
  shell       200 in the ink look, one h1 (Turmerific), the real bottle, no canvas, no console
              errors (1440x900, 390x844)
  name        1920 to 360: both halves inside the wrap; from 960px on one row clear of the bottle's
              glass, below it one word over the bottle; vi too
  chapters    overview, why, inside, research, daily, buy (no people); each its own painting;
              "Inside every capsule, one ingredient."; 1,000 mg; the painted sum; all six studies; the
              questions, with no liver answer yet (Mo's research)
  soak        the gold waits, then soaks in layer by layer from the slice, the gold area growing;
              ends whole with its glint; reduced motion and no script: whole from the first paint
  multiply    every painting multiplies onto the paper with no box
  buy         the real bottle (turmerific.png) stands inside the scene, centred; the front layer
              multiplies over its foot and changes nothing beside it; captioned; Add to cart
  size        both bottles exactly NuriCell's size (1440, 1024, 390)
  layout      sizes 1536 to 360: no sideways scroll, painting left of its words from 960px and above
              them below, text 15px+
  deep_links  #chapter-<id> lands its heading under the menu bar
  languages   kr, jp, cns, vn: 200, no console errors, the new strings translated
Pictures: scripts/qa/out/turmerific-ink/.

usage: python -X utf8 scripts/qa/qa_turmerific_ink.py [base-url] [--only=shell,name,...]
"""

import io
import re
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = ARGS[0] if ARGS else "http://localhost:3054"
ONLY = next((a.split("=", 1)[1].split(",") for a in sys.argv[1:] if a.startswith("--only=")), None)
REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "scripts/qa/out/turmerific-ink"
OUT.mkdir(parents=True, exist_ok=True)
PATH = "/en/products/turmerific"
CHAPTERS = ["overview", "why", "inside", "research", "daily", "buy"]
PAINTED = ["why", "inside", "research", "daily"]
PREFETCH_CSS = re.compile(r"was preloaded using link preload but not used")
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
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" and not PREFETCH_CSS.search(m.text) else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    response = page.goto(BASE + path, wait_until="networkidle")
    if js:
        page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
    return ctx, page, response, errors


def bring(page, selector, top=140):
    page.evaluate(
        "([s, t]) => { const e = document.querySelector(s); window.scrollBy(0, e.getBoundingClientRect().top - t); }",
        [selector, top],
    )


def patch(img, x, y, n=10):
    px = [img.getpixel((min(xx, img.width - 1), min(yy, img.height - 1))) for xx in range(x, x + n) for yy in range(y, y + n)]
    return tuple(round(sum(c[i] for c in px) / len(px), 1) for i in range(3))


def gold_share(img):
    """The share of a picture's pixels that are clearly golden (saturated and warm)."""
    hsv = img.convert("RGB").convert("HSV")
    h, s, v = hsv.split()
    hb, sb, vb = h.tobytes(), s.tobytes(), v.tobytes()
    n = sum(1 for i in range(len(sb)) if sb[i] > 70 and vb[i] > 120 and 15 <= hb[i] <= 45)
    return n / len(sb)


def shell(browser):
    for w, h in [(1440, 900), (390, 844)]:
        ctx, page, response, errors = opened(browser, w, h)
        tag = f"shell {w}x{h}"
        check(f"{tag}: 200", response is not None and response.status == 200)
        check(f"{tag}: the ink look", page.locator('[data-look="ink"][data-page="products"]').count() == 1)
        check(f"{tag}: the ink page for Turmerific", page.locator('[data-product-ink="turmerific"]').count() == 1)
        check(f"{tag}: one h1", page.locator("h1").count() == 1)
        check(
            f"{tag}: the h1's accessible name is Turmerific",
            page.get_by_role("heading", level=1, name="Turmerific", exact=True).count() == 1,
        )
        check(f"{tag}: the real bottle in the opening", page.locator('[data-chapter="overview"] img[src*="turmerific.png"]').count() >= 1)
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
  const bottle = h.querySelector('[class*=stand] img');
  // The bottle's glass: the photo has a wide transparent margin (its visible part is about 52% of
  // its width, centred).
  const b = box(bottle), mid = (b.l + b.r) / 2, half = (b.r - b.l) * 0.52 / 2;
  return { inner, first: box(first), second: box(second), glass: { l: mid - half, r: mid + half, t: b.t, b: b.b } };
}"""


def name(browser):
    for locale in ["en", "vn"]:
        for w, h in SIZES:
            if locale == "vn" and w not in (1440, 1024, 390):
                continue
            ctx, page, _, _ = opened(browser, w, h, f"/{locale}/products/turmerific", reduced=True)
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(300)
            m = page.evaluate(NAME_BOXES)
            tag = f"name {locale} {w}x{h}"
            lo, hi = m["inner"]
            inside = m["first"]["l"] >= lo - 1 and m["second"]["r"] <= hi + 1 and m["first"]["r"] <= hi + 1 and m["second"]["l"] >= lo - 1
            check(f"{tag}: both halves inside the wrap", inside, f"wrap {lo:.0f}-{hi:.0f}, first {m['first']['l']:.0f}-{m['first']['r']:.0f}, second {m['second']['l']:.0f}-{m['second']['r']:.0f}")
            row = abs(m["first"]["t"] - m["second"]["t"]) < 2
            if w >= 960:
                clear = m["first"]["r"] <= m["glass"]["l"] + 1 and m["second"]["l"] >= m["glass"]["r"] - 1
                check(f"{tag}: one row, clear of the bottle's glass", row and clear,
                      f"first ends {m['first']['r']:.0f}, glass {m['glass']['l']:.0f}-{m['glass']['r']:.0f}, second starts {m['second']['l']:.0f}")
            else:
                # One word: "Turm" and "erific" touch on one row, over the bottle.
                joined = abs(m["second"]["l"] - m["first"]["r"]) < 3
                over = m["glass"]["t"] >= m["first"]["b"] - 30
                check(f"{tag}: one word over the bottle", row and joined and over,
                      f"first {m['first']['l']:.0f}-{m['first']['r']:.0f} top {m['first']['t']:.0f}, second {m['second']['l']:.0f} top {m['second']['t']:.0f}, bottle top {m['glass']['t']:.0f}")
            if locale == "en" and w in (1440, 1024, 390):
                page.screenshot(path=str(OUT / f"name-{w}.png"))
            ctx.close()


EXPECT = [
    "Why the form matters",
    "A golden compound.",
    "A hard one to absorb.",
    "Curcumin is the compound that gives turmeric its golden colour.",
    "Longvida® carries curcumin in tiny particles of fat, designed to help your body absorb it.",
    "Inside every capsule, one ingredient.",
    "Longvida® curcumin",
    "Amount per serving of 2 capsules, as printed on the Turmerific label.",
    "Other ingredients: rice flour, vegetable oil powder",
    "These studies are about Longvida®, the curcumin in Turmerific, not the finished product.",
    "One bottle, one month.",
    "Take 1 to 2 capsules a day, or as your healthcare professional advises.",
    "Developed under the direction and guidance of Dr.",
    "Is the 1,000 mg all curcumin?",
    "These statements have not been evaluated by the Food and Drug Administration.",
]


def chapters(browser):
    ctx, page, _, _ = opened(browser, 1440, 900, reduced=True)
    found = page.evaluate("() => [...document.querySelectorAll('[data-chapter]')].map(c => c.dataset.chapter)")
    check("chapters: in order, no people", found == CHAPTERS, ", ".join(found))
    srcs = page.evaluate(
        """(ids) => ids.map(id => { const i = document.querySelector(`[data-chapter="${id}"] figure[data-picture] img`);
             return i ? decodeURIComponent(i.currentSrc || i.src) : null; })""",
        PAINTED + ["buy"],
    )
    check("chapters: each its own painting", all(srcs) and len(set(srcs)) == len(srcs), "; ".join(s or "none" for s in srcs))
    check("chapters: Turmerific's own paintings", all("turmerific/ink/" in s for s in srcs if s), "")
    check("chapters: 1,000 mg", page.locator('[data-chapter="inside"]').get_by_text("1,000").count() >= 1)
    sum_kind = page.evaluate("() => document.querySelector('[data-sum]')?.dataset.sumKind ?? null")
    sum_src = page.evaluate("() => decodeURIComponent(document.querySelector('[data-sum] img')?.currentSrc ?? '')")
    check("chapters: the painted 2 × 30 = 60", sum_kind == "painted" and "turmerific/ink/sum" in sum_src, f"{sum_kind} {sum_src[:80]}")
    sum_text = page.evaluate("() => document.querySelector('[data-sum-text]')?.textContent.trim()")
    check("chapters: the sum read aloud", sum_text == "2 capsules a day for 30 days: 60 capsules in each bottle.", str(sum_text))
    page.evaluate("""() => { document.querySelector('[data-chapter="research"] button[aria-expanded="false"]')?.click();
                         document.querySelectorAll('main details').forEach(d => { d.open = true; }); }""")
    page.wait_for_timeout(300)
    text = page.evaluate("() => document.body.innerText.replace(/\\s+/g, ' ')")
    missing = [e for e in EXPECT if e not in text]
    check("chapters: the page's words", not missing, "; ".join(missing))
    main_text = page.evaluate("() => document.querySelector('main').innerText")
    # A whole word: "delivery" (the purpose's "delivery system") holds the letters too.
    check("chapters: no liver answer yet (Mo's research first)", not re.search(r"\bliver\b", main_text, re.I))
    studies = page.locator("[data-study]").count()
    check("chapters: all six studies", studies == 6, f"{studies}")
    alts = page.evaluate("() => [...document.querySelectorAll('main figure img[alt]')].map(i => i.alt).filter(Boolean)")
    check("chapters: every painting described", len(alts) >= 5, "; ".join(a[:30] for a in alts))
    ctx.close()


SOAK = """() => { const f = document.querySelector('[data-chapter="why"] figure[data-soak]');
  if (!f) return null;
  const lit = f.querySelector('img[data-lit]'), gold = f.querySelector('[class*=litGold]');
  const layers = [...f.querySelectorAll('img[data-soak-layer]')];
  const cs = (e) => getComputedStyle(e);
  return { light: f.dataset.light, bloom: f.querySelector('img:not([data-lit]):not([data-soak-layer])').dataset.bloom,
           lit: Number(cs(lit).opacity), layers: layers.map(l => Number(cs(l).opacity)),
           masks: layers.map(l => (cs(l).maskImage || cs(l).webkitMaskImage || '')),
           positions: layers.map(l => (cs(l).maskPosition || cs(l).webkitMaskPosition || '')),
           glint: gold ? Number(cs(gold).opacity) : null }; }"""


def soak(browser):
    ctx, page, _, _ = opened(browser, 1440, 900)
    first = page.evaluate(SOAK)
    check("soak: the Why figure soaks its gold in (not the lantern, not the spread)",
          first is not None and page.locator("[data-lantern], [data-spread]").count() == 0)
    if first is None:
        ctx.close()
        return
    check("soak: nine layers, each through the soak sprite", len(first["layers"]) == 9 and all("turmerific/ink/soak" in m for m in first["masks"]),
          f"{len(first['layers'])} layers; {first['masks'][:1]}")
    check("soak: each layer its own mask of the sprite", len(set(first["positions"])) == 9, "; ".join(first["positions"][:3]))
    check("soak: off before the chapter is seen", first["light"] == "off" and first["lit"] == 0 and max(first["layers"]) == 0, str(first["layers"]))
    bring(page, '[data-chapter="why"] figure', 120)
    fig = page.locator('[data-chapter="why"] figure [class*=body]').first
    seen, golds = [], []
    for _ in range(18):
        page.wait_for_timeout(400)
        state = page.evaluate(SOAK)
        seen.append(state)
        if state["light"] == "on":
            golds.append(gold_share(Image.open(io.BytesIO(fig.screenshot()))))
    check("soak: comes on once seen", seen[-1]["light"] == "on", str(seen[-1]["light"]))
    partial = [s for s in seen if s["light"] == "on" and 0 < sum(1 for o in s["layers"] if o > 0.99) < 9]
    check("soak: passes through partly soaked (some layers in, some still to come)", len(partial) >= 2, f"{len(partial)} samples")
    rising = len(golds) >= 4 and golds[-1] > golds[0] * 2 and all(b >= a - 0.004 for a, b in zip(golds, golds[1:]))
    check("soak: the gold area grows as it soaks in", rising, ", ".join(f"{g:.3f}" for g in golds[:10]))
    end = seen[-1]
    check("soak: ends whole", end["lit"] == 1 and min(end["layers"]) == 1, f"lit {end['lit']}, layers {end['layers']}")
    page.wait_for_timeout(2500)
    glint = page.evaluate(SOAK)["glint"]
    check("soak: the gold's glint after the soak", glint == 1, str(glint))
    page.screenshot(path=str(OUT / "soak-1440.png"))
    ctx.close()
    for label, kwargs in [("reduced motion", {"reduced": True}), ("no script", {"js": False})]:
        ctx, page, _, _ = opened(browser, 1440, 900, **kwargs)
        page.locator('[data-chapter="why"] figure').scroll_into_view_if_needed()
        page.wait_for_timeout(300)
        if kwargs.get("js", True):
            state = page.evaluate(SOAK)
            check(f"soak {label}: whole from the first paint", state["lit"] == 1, str(state["lit"]))
        shot = OUT / f"soak-{label.replace(' ', '-')}.png"
        page.locator('[data-chapter="why"] figure').screenshot(path=str(shot))
        share = gold_share(Image.open(shot))
        check(f"soak {label}: the gold shows", share > 0.05, f"{share:.3f} of pixels gold")
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
        check(f"{tag}: the real bottle photo", "turmerific.png" in m["src"], m["src"][:90])
        check(f"{tag}: the bottle named", "Turmerific" in m["alt"], m["alt"])
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
    """Both bottles exactly NuriCell's size (Mo, October 14, for Propolis; October 16 for
    Turmerific: "both bottles as big as NuriCell's"), at a laptop, a tablet and a phone."""
    for w, h in [(1440, 900), (1024, 768), (390, 844)]:
        sizes = {}
        for slug in ["nuricell", "turmerific"]:
            ctx, page, _, _ = opened(browser, w, h, f"/en/products/{slug}", reduced=True)
            sizes[slug] = page.evaluate(SIZE)
            ctx.close()
        a, b = sizes["nuricell"], sizes["turmerific"]
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


NEW = {
    "kr": "캡슐 하나에 성분 하나.",
    "jp": "1カプセルに、成分はひとつ。",
    "cns": "每粒胶囊，只有一种成分。",
    "vn": "Mỗi viên nang, một thành phần.",
}


def languages(browser):
    for locale, heading in NEW.items():
        ctx, page, response, errors = opened(browser, 1440, 900, f"/{locale}/products/turmerific", reduced=True)
        tag = f"languages {locale}"
        check(f"{tag}: 200", response is not None and response.status == 200)
        check(f"{tag}: no console errors", not errors, "; ".join(errors[:2]))
        check(f"{tag}: the one-ingredient heading translated", page.locator("#chapter-inside-title").inner_text().strip() == heading,
              page.locator("#chapter-inside-title").inner_text().strip())
        english = page.evaluate("() => [...document.querySelectorAll('main figure img[alt]')].map(i => i.alt).filter(a => /painted in|turmeric plant/.test(a))")
        check(f"{tag}: the paintings described in {locale}", not english, "; ".join(english[:2]))
        ctx.close()


SECTIONS = {
    "shell": shell,
    "name": name,
    "chapters": chapters,
    "soak": soak,
    "multiply": multiply,
    "buy": buy,
    "size": bottle_size,
    "layout": layout,
    "deep_links": deep_links,
    "languages": languages,
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

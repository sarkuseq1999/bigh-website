"""QA for Nature Calm's ink page (Mo, October 16, 2026; picks and paintings in
reference/ink-pages/nature-calm/README.md). The template is NuriCell's (qa_nuricell_ink.py); this
checks what Nature Calm brings: its name fitted round the bottle, the lake going still as the light
gathers (the lantern's cross-fade with this painting's own meaning), eighteen ingredients beside the
pine cone, Dr. Liu's painting reused, no painted sum, the real bottle between lavender rows.

Sections (all, or --only=a,b):
  shell       200 in the ink look, one h1 (Nature Calm), the real bottle, no canvas, no console
              errors (1440x900, 390x844)
  name        1920 to 360: both halves inside the wrap and clear of the bottle, on one row from 960px,
              "Nature" over "Calm" over the bottle below; vi too
  chapters    overview, why, inside, research, people, daily, buy (no sum); each its own painting;
              "18 ingredients."; 100 mg; every study; Dr. Liu's portrait painting; the page's words;
              the three capsules on the "One bottle" card
  light       the lake is ruffled until seen, then the still water fades up over it; its glint
              follows; reduced motion and no script: still from the first paint
  multiply    every painting multiplies onto the paper with no box
  buy         the real bottle (nature-calm.png) stands inside the lavender scene, centred; the front
              layer multiplies over its foot and changes nothing beside it; captioned; Add to cart
  size        both bottles exactly NuriCell's size (1440, 1024, 390)
  layout      sizes 1536 to 360: no sideways scroll, painting left of its words from 960px and above
              them below, text 15px+
  deep_links  #chapter-<id> lands its heading under the menu bar
  languages   kr, jp, cns, vn: 200, no console errors, the paintings described in that language
Pictures: scripts/qa/out/nature-calm-ink/.

usage: python -X utf8 scripts/qa/qa_nature_calm_ink.py [base-url] [--only=shell,name,...]
"""

import io
import re
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = ARGS[0] if ARGS else "http://localhost:3056"
ONLY = next((a.split("=", 1)[1].split(",") for a in sys.argv[1:] if a.startswith("--only=")), None)
REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "scripts/qa/out/nature-calm-ink"
OUT.mkdir(parents=True, exist_ok=True)
SLUG = "nature-calm"
PATH = f"/en/products/{SLUG}"
CHAPTERS = ["overview", "why", "inside", "research", "people", "daily", "buy"]
PAINTED = ["why", "inside", "research", "people", "daily"]
PREFETCH_CSS = re.compile(r"was preloaded using link preload but not used")
SIZES = [(1920, 1080), (1536, 864), (1440, 900), (1280, 800), (1024, 768), (960, 800), (900, 900), (768, 1024), (390, 844), (360, 780)]
# Words from src/components/product/products/nature-calm.ts that every build must keep.
EXPECT = [
    "For life’s demanding days",
    "Everyday stress.",
    "A cellular approach.",
    "Nature Calm brings together nutrients involved in cellular energy and antioxidant defenses, with everyday stress in mind.",
    "Cellular energy",
    "Everyday stress",
    "90 vegetarian capsules",
    "30-day supply",
    "Why stress matters to your cells",
    "Stress, seen from inside the cell.",
    "Under stress, your body releases hormones that get it ready to respond.",
    "In animal studies, Dr. Liu and Dr. Wang found that stress raised oxidative damage in the brain.",
    "Nature Calm brings their research into a formula for life’s demanding days.",
    "Inside every capsule, 18 ingredients.",
    "Coenzyme Q10",
    "N-acetylcysteine",
    "L-theanine",
    "Phosphatidylserine",
    "Pantothenic acid (vitamin B5)",
    "Amounts per serving of 3 capsules, as printed on the Nature Calm label.",
    "Other ingredients: rice flour, silicon dioxide, magnesium stearate and cellulose. Capsule: vegetable cellulose.",
    "Ingredient research does not establish the effects of the finished product.",
    "The research behind the formula",
    "None of them tested Nature Calm itself.",
    "Stress and the body’s antioxidant defenses",
    "Stress and oxidative damage in the brain",
    "Stress, aging and oxidative damage",
    "How N-acetylcysteine works",
    "L-theanine and everyday stress",
    "The trial used 200 mg a day; Nature Calm has 100 mg per serving.",
    "Dr. Jiankang Liu",
    "Chief Scientific Advisor, BiGH",
    "Dr. Iris Wang",
    "Co-developer of Nature Calm",
    "Dr. Wang developed Nature Calm with Dr. Liu.",
    "Portrait painting",
    "One bottle, one month.",
    "Take 3 capsules once a day, with or after a meal.",
    "Developed by Dr. Jiankang Liu and Dr. Iris Wang.",
    "How do I take Nature Calm?",
    "Has Nature Calm itself been tested in a clinical trial?",
    "Can I take it with medicines or other supplements?",
    "As with any supplement, ask your doctor before taking Nature Calm",
    "Keep out of reach of children.",
]
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


def shell(browser):
    for w, h in [(1440, 900), (390, 844)]:
        ctx, page, response, errors = opened(browser, w, h)
        tag = f"shell {w}x{h}"
        check(f"{tag}: 200", response is not None and response.status == 200)
        check(f"{tag}: the ink look", page.locator('[data-look="ink"][data-page="products"]').count() == 1)
        check(f"{tag}: the ink page for Nature Calm", page.locator(f'[data-product-ink="{SLUG}"]').count() == 1)
        check(f"{tag}: one h1", page.locator("h1").count() == 1)
        check(
            f"{tag}: the h1's accessible name is Nature Calm",
            page.get_by_role("heading", level=1, name="Nature Calm", exact=True).count() == 1,
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
  const bottle = h.querySelector('[class*=stand] img');
  // The bottle's glass: the photo has a wide transparent margin (its visible part is 52% of its
  // width, centred).
  const b = box(bottle), mid = (b.l + b.r) / 2, half = (b.r - b.l) * 0.52 / 2;
  return { inner, first: box(first), second: box(second), glass: { l: mid - half, r: mid + half, t: b.t, b: b.b },
           words: [first.textContent, second.textContent] };
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
            if w == 1440:
                check(f"{tag}: Nature and Calm", m["words"] == ["Nature", "Calm"], str(m["words"]))
            lo, hi = m["inner"]
            inside = m["first"]["l"] >= lo - 1 and m["second"]["r"] <= hi + 1 and m["first"]["r"] <= hi + 1 and m["second"]["l"] >= lo - 1
            check(f"{tag}: both halves inside the wrap", inside, f"wrap {lo:.0f}-{hi:.0f}, first {m['first']['l']:.0f}-{m['first']['r']:.0f}, second {m['second']['l']:.0f}-{m['second']['r']:.0f}")
            if w >= 960:
                row = abs(m["first"]["t"] - m["second"]["t"]) < 2
                clear = m["first"]["r"] <= m["glass"]["l"] + 1 and m["second"]["l"] >= m["glass"]["r"] - 1
                check(f"{tag}: one row, clear of the bottle's glass", row and clear,
                      f"first ends {m['first']['r']:.0f}, glass {m['glass']['l']:.0f}-{m['glass']['r']:.0f}, second starts {m['second']['l']:.0f}")
            else:
                stacked = m["second"]["t"] >= m["first"]["b"] - 2 and m["glass"]["t"] >= m["second"]["b"] - 30
                check(f"{tag}: Nature over Calm over the bottle", stacked,
                      f"first {m['first']['t']:.0f}-{m['first']['b']:.0f}, second {m['second']['t']:.0f}-{m['second']['b']:.0f}, bottle top {m['glass']['t']:.0f}")
            if locale == "en" and w in (1440, 1024, 390):
                page.screenshot(path=str(OUT / f"name-{w}.png"))
            ctx.close()


def chapters(browser):
    ctx, page, _, _ = opened(browser, 1440, 900, reduced=True)
    found = page.evaluate("() => [...document.querySelectorAll('[data-chapter]')].map(c => c.dataset.chapter)")
    check("chapters: all seven, in order", found == CHAPTERS, ", ".join(found))
    check("chapters: no painted or typed sum", page.locator("[data-sum]").count() == 0)
    srcs = page.evaluate(
        """(ids) => ids.map(id => { const i = document.querySelector(`[data-chapter="${id}"] figure[data-picture] img`);
             return i ? decodeURIComponent(i.currentSrc || i.src) : null; })""",
        PAINTED + ["buy"],
    )
    check("chapters: each its own painting", all(srcs) and len(set(srcs)) == len(srcs), "; ".join(s or "none" for s in srcs))
    own = [s for s in srcs if s and f"{SLUG}/ink/" in s]
    check("chapters: Nature Calm's own paintings, Dr. Liu's from NuriCell", len(own) == 5 and srcs[3] and "nuricell/ink/liu" in srcs[3], "; ".join(s.split("/ink/")[-1][:24] for s in srcs if s))
    check("chapters: the lake's lit layer", page.locator('[data-chapter="why"] figure img[data-lit][src*="lake-still"]').count() == 1)
    check("chapters: Dr. Liu captioned Portrait painting", page.locator('[data-chapter="people"] figcaption').inner_text().strip() == "Portrait painting")
    check("chapters: 18 rows of ingredients", page.locator('[data-chapter="inside"] tbody tr').count() == 18)
    check("chapters: 100 mg", page.locator('[data-chapter="inside"]').get_by_text("100").count() >= 1)
    card = page.locator('[data-chapter="overview"] img[class*=bottleCardPicture]')
    check("chapters: the three capsules on the One bottle card", card.count() == 1 and "capsules" in (card.get_attribute("src") or ""))
    page.evaluate("""() => { document.querySelector('[data-chapter="research"] button[aria-expanded="false"]')?.click();
                         document.querySelectorAll('main details').forEach(d => { d.open = true; }); }""")
    page.wait_for_timeout(300)
    text = page.evaluate("() => document.body.innerText.replace(/\\s+/g, ' ')")
    missing = [e for e in EXPECT if e not in text]
    check("chapters: the page's words", not missing, "; ".join(missing))
    studies = page.locator("[data-study]").count()
    check("chapters: all seven studies", studies == 7, f"{studies}")
    check("chapters: no rats", "rats" not in text.lower().split("animal study")[0] and " rats" not in text.lower())
    alts = page.evaluate("() => [...document.querySelectorAll('main figure img[alt]')].map(i => i.alt).filter(Boolean)")
    check("chapters: every painting described", len(alts) >= 6, "; ".join(a[:30] for a in alts))
    ctx.close()


LIGHT = """() => { const f = document.querySelector('[data-chapter="why"] figure[data-lantern]');
  const lit = f && f.querySelector('img[data-lit]'); const gold = f && f.querySelector('[class*=litGold]');
  return f ? { light: f.dataset.light, lit: Number(getComputedStyle(lit).opacity),
               bloom: f.querySelector('img:not([data-lit])').dataset.bloom,
               glint: gold ? Number(getComputedStyle(gold).opacity) : null } : null; }"""


def light(browser):
    ctx, page, _, _ = opened(browser, 1440, 900)
    first = page.evaluate(LIGHT)
    check("light: the Why figure cross-fades (the lantern's mode, not a spread)", first is not None and page.locator("[data-spread]").count() == 0)
    if first is None:
        ctx.close()
        return
    check("light: ruffled before the chapter is seen", first["light"] == "off" and first["lit"] == 0, str(first))
    bring(page, '[data-chapter="why"] figure', 120)
    seen = []
    for _ in range(14):
        page.wait_for_timeout(500)
        seen.append(page.evaluate(LIGHT))
    partial = [s["lit"] for s in seen if s["light"] == "on" and 0.02 < s["lit"] < 0.98]
    check("light: comes on once seen", seen[-1]["light"] == "on", str(seen[-1]))
    check("light: the still water fades up (not a pop)", len(partial) >= 1, ", ".join(f"{s['lit']:.2f}" for s in seen))
    check("light: ends still", seen[-1]["lit"] == 1, str(seen[-1]["lit"]))
    check("light: the gold's glint after", seen[-1]["glint"] == 1, str(seen[-1]["glint"]))
    page.screenshot(path=str(OUT / "light-1440.png"))
    ctx.close()
    for label, kwargs in [("reduced motion", {"reduced": True}), ("no script", {"js": False})]:
        ctx, page, _, _ = opened(browser, 1440, 900, **kwargs)
        page.locator('[data-chapter="why"] figure').scroll_into_view_if_needed()
        page.wait_for_timeout(300)
        state = page.evaluate(LIGHT) if kwargs.get("js", True) else None
        if state is not None:
            check(f"light {label}: still from the first paint", state["lit"] == 1, str(state))
        else:
            shot = OUT / "light-nojs.png"
            page.locator('[data-chapter="why"] figure').screenshot(path=str(shot))
            img = Image.open(shot).convert("RGB").convert("HSV")
            sat = img.tobytes()[1::3]
            gold = sum(1 for s in sat if s > 90) / len(sat)
            check(f"light {label}: the gold shows", gold > 0.002, f"{gold:.4f} of pixels gold")
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
        # Every picture of the chapter decoded before the comparison below: on the public CDN a
        # lazily loaded scene can finish a sharper copy between its two screenshots, and edge
        # pixels far from the bottle then differ (October 16, 2026: 15 pixels at the rows' ends).
        page.evaluate("""() => Promise.all([...document.querySelectorAll('[data-chapter="buy"] img')]
                            .map(i => i.decode().catch(() => {})))""")
        page.wait_for_timeout(600)
        m = page.evaluate(BUY)
        tag = f"buy {w}x{h}"
        check(f"{tag}: a painted scene", m is not None)
        if m is None:
            ctx.close()
            continue
        check(f"{tag}: the real bottle photo", f"{SLUG}.png" in m["src"], m["src"][:90])
        check(f"{tag}: the bottle named", "Nature Calm" in m["alt"], m["alt"])
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
    """Both bottles exactly NuriCell's size (Mo, October 14 and 16), at a laptop, a tablet and a phone."""
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


def languages(browser):
    for locale in ["kr", "jp", "cns", "vn"]:
        ctx, page, response, errors = opened(browser, 1440, 900, f"/{locale}/products/{SLUG}", reduced=True)
        tag = f"languages {locale}"
        check(f"{tag}: 200", response is not None and response.status == 200)
        check(f"{tag}: no console errors", not errors, "; ".join(errors[:2]))
        check(f"{tag}: the ink page", page.locator(f'[data-product-ink="{SLUG}"]').count() == 1)
        english = page.evaluate("() => [...document.querySelectorAll('main figure img[alt]')].map(i => i.alt).filter(a => /painted in|in ink/.test(a))")
        check(f"{tag}: the paintings described in {locale}", not english, "; ".join(english[:2]))
        ctx.close()


SECTIONS = {
    "shell": shell,
    "name": name,
    "chapters": chapters,
    "light": light,
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

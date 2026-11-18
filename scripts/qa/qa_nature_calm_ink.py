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
  meadow      the opening's painting, the high meadow (Mo picked A, November 16, 2026), 2560 to 360:
              drawn and multiplied behind the name, the window's width and up to its top, the
              bottle's foot on its ground with its own grass in front, the name over the land from
              960px, the words under the painting, no sideways scroll; without scripts too; Green
              Bee Propolis keeps its own opening
  chapters    overview, why, inside, research, people, daily, buy (no sum); each its own painting;
              "18 ingredients."; 100 mg; every study; Dr. Liu's portrait painting; the page's words;
              the three capsules on the "One bottle" card; the paintings in colour (November 17)
  light       the lake is ruffled until seen, then the still water fades up over it; its glint
              follows; reduced motion and no script: still from the first paint
  multiply    every painting multiplies onto the paper with no box
  buy         the real bottle (nature-calm.png) stands inside the lavender scene, centred; the front
              layer multiplies over its foot and changes nothing beside it; captioned; Add to cart
  size        both bottles exactly NuriCell's size (1440, 1024, 390)
  layout      sizes 1536 to 360: no sideways scroll, painting on its own side of its words from 960px (alternating) and above
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
import stall_guard  # noqa: E402,F401  (ends a frozen run; see stall_guard.py)
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
GONE = ['Why stress matters to your cells', 'What’s inside', 'The people behind the formula']

EXPECT = [
    "For life’s demanding days",
    "Everyday stress.",
    "A cellular approach.",
    "Nature Calm brings together nutrients involved in cellular energy and antioxidant defenses, with everyday stress in mind.",
    "Cellular energy",
    "Everyday stress",
    "90 vegetarian capsules",
    "30-day supply",
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
  // The bottle photo itself: since November 16, 2026 the bottle's box also holds the meadow painting
  // and its front grass (painted-opening.tsx).
  const bottle = h.querySelector('[class*=stand] img[class*=bottle]');
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
    check("chapters: the lake's lit layer", page.locator('[data-chapter="why"] figure img[data-lit][src*="tahoe-still"]').count() == 1)
    check("chapters: Dr. Liu captioned Portrait painting", page.locator('[data-chapter="people"] figcaption').inner_text().strip() == "Portrait painting")
    check("chapters: 18 rows of ingredients", page.locator('[data-chapter="inside"] tbody tr').count() == 18)
    check("chapters: 100 mg", page.locator('[data-chapter="inside"]').get_by_text("100").count() >= 1)
    card = page.locator('[data-chapter="overview"] img[class*=bottleCardPicture]')
    check("chapters: the three capsules on the One bottle card", card.count() == 1 and "capsules" in (card.get_attribute("src") or ""))
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
    # The paintings in colour (Mo, November 17, 2026: the same pictures in color, page by page): the
    # Big Dipper and the moon are the colour takes, the five questions v2 (no powders). Since
    # November 18 the Big Dipper's sky is painted at dusk (stars-dusk).
    srcs = page.evaluate("""() => [...document.querySelectorAll('main img')].map((i) => decodeURIComponent(i.currentSrc || i.src).split('/').pop().split('&')[0])""")
    colour = [n for n in ["stars-dusk-v1.webp", "moon-colour-v1.webp"] if n not in srcs]
    check("chapters: the Big Dipper and the moon in colour", not colour, "missing " + ", ".join(colour))
    qs = page.evaluate("""() => [...document.querySelectorAll('#questions img')].map((i) => decodeURIComponent(i.currentSrc || i.src).split('/').pop().split('&')[0])""")
    old_q = [q for q in qs if not q.endswith("-v2.webp")]
    check("chapters: the question paintings in colour", len(set(qs)) == 5 and not old_q, ", ".join(sorted(set(qs))))
    # No small label over a chapter's heading (Mo, November 16, 2026; NuriCell's since October 26):
    # each chapter starts with its heading; the buy chapter's line is the product's tagline.
    labels = page.evaluate("""() => [...document.querySelectorAll('[data-chapter]:not([data-chapter="overview"]):not([data-chapter="buy"]) [data-words] > p[class*="label"]')].map((p) => p.textContent.trim())""")
    check("chapters: no small label over the chapters' headings", not labels, "; ".join(labels))
    gone = [g for g in GONE if g in text]
    check("chapters: the old labels are gone", not gone, "; ".join(gone))
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

    def pair():
        with_front = Image.open(io.BytesIO(page.screenshot(clip=clip))).convert("RGB")
        page.evaluate("() => { document.querySelector('[data-scene-front]').style.visibility = 'hidden'; }")
        page.wait_for_timeout(200)
        without = Image.open(io.BytesIO(page.screenshot(clip=clip))).convert("RGB")
        page.evaluate("() => { document.querySelector('[data-scene-front]').style.visibility = ''; }")
        page.wait_for_timeout(200)
        return with_front.load(), without.load(), with_front.size

    # Two pairs of captures: a pixel counts only if the front layer changes it in both. Since the
    # opening's painting made the page taller (November 16, 2026) the scene sits at a fractional
    # pixel on a phone, and about one capture in five then draws a few edge pixels of the hidden
    # layer's stage differently, beside the bottle; a real stray mark changes them every time.
    (a, b, (w, h)), (a2, b2, _) = pair(), pair()
    bl, br, bt, bb = m["bottle"]
    outside = inside = 0
    for y in range(h):
        for x in range(w):
            if max(abs(c1 - c2) for c1, c2 in zip(a[x, y], b[x, y])) > 10 and max(abs(c1 - c2) for c1, c2 in zip(a2[x, y], b2[x, y])) > 10:
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


# From 960px the chapters alternate sides (November 18, 2026; AGENTS.md "Even rhythm"): these
# have their painting right of their words, the others left.
RIGHT_SIDE = ['inside', 'people', 'buy']


def layout(browser):
    for w, h in SIZES[1:]:
        ctx, page, _, _ = opened(browser, w, h, reduced=True)
        tag = f"layout {w}x{h}"
        wide = page.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
        check(f"{tag}: no sideways scroll", wide <= 0, f"{wide}px")
        bad = page.evaluate(
            """([two, right]) => [...document.querySelectorAll('[data-chapter]:not([data-chapter="overview"])')].map(c => {
                 const f = c.querySelector('figure[data-picture]').getBoundingClientRect();
                 const t = c.querySelector('[data-words]').getBoundingClientRect();
                 const ok = !two ? f.bottom <= t.top + 1
                   : right.includes(c.dataset.chapter) ? t.right <= f.left + 1 : f.right <= t.left + 1;
                 return ok ? null : c.dataset.chapter; }).filter(Boolean)""",
            [w >= 960, RIGHT_SIDE],
        )
        check(f"{tag}: each painting {'on its own side of' if w >= 960 else 'above'} its words", not bad, ", ".join(bad))
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


MEADOW = """() => {
  const sec = document.querySelector('[data-chapter="overview"]');
  const v = sec.querySelector('[data-opening-painting]');
  if (!v) return null;
  const css = getComputedStyle(sec);
  const num = (n) => parseFloat(css.getPropertyValue(n));
  const box = (el) => { const r = el.getBoundingClientRect(); return { l: r.left, r: r.right, t: r.top, b: r.bottom }; };
  const img = v.querySelector('picture img');
  const bottle = sec.querySelector('h1 img[class*=bottle]'), b = box(bottle), bh = b.b - b.t;
  const front = sec.querySelector('img[class*=paintingFront]');
  const second = sec.querySelector('h1 [class*=second]');
  const probe = document.createElement('span');
  Object.assign(probe.style, { display: 'inline-block', width: '0', height: '0', verticalAlign: 'baseline' });
  second.append(probe); const baseline = probe.getBoundingClientRect().top; probe.remove();
  const p = box(v), rows = num('--paint-rows');
  const at = (row) => p.t + (row / rows) * (p.b - p.t);
  return { src: decodeURIComponent(img.currentSrc || img.src), decoded: img.complete && img.naturalWidth > 1,
           blend: getComputedStyle(v).mixBlendMode, z: getComputedStyle(v).zIndex,
           painting: p, W: document.documentElement.clientWidth,
           sideways: document.documentElement.scrollWidth - document.documentElement.clientWidth,
           hills: at(num('--paint-hills')), ground: at(num('--paint-ground')), end: at(num('--paint-end')),
           foot: b.t + (1242 / 1278) * bh, bottleH: bh, glassMid: (b.l + b.r) / 2,
           front: front ? { ...box(front), z: getComputedStyle(front).zIndex, decoded: front.complete && front.naturalWidth > 1 } : null,
           baseline, size: parseFloat(getComputedStyle(sec.querySelector('h1')).fontSize),
           words: sec.querySelector('h1 + div').getBoundingClientRect().top };
}"""

MEADOW_SIZES = [(2560, 1300), (1920, 1080), (1536, 864), (1440, 900), (1440, 700), (1280, 800), (1024, 768), (960, 800), (768, 1024), (390, 844), (360, 780)]


def meadow(browser):
    """The opening's high meadow (Mo picked A, November 16, 2026; painted-opening.tsx, shared with
    Advanced OPC Formula's vineyard and Turmerific's field): one painting behind the name and the
    bottle, multiplied, the window's width and up to the window's top, the bottle's foot on its
    ground with the painting's own grass in front, the name over the land from 960px, the words on
    bare paper under the last of the painting."""
    for w, h in MEADOW_SIZES:
        ctx, page, _, errors = opened(browser, w, h, reduced=True)
        page.wait_for_function("() => [...document.querySelectorAll('[data-chapter=\"overview\"] img')].every((i) => i.complete)")
        page.wait_for_timeout(300)
        m = page.evaluate(MEADOW)
        tag = f"meadow {w}x{h}"
        if m is None:
            check(f"{tag}: the painting is there", False)
            ctx.close()
            continue
        wide = w >= 960
        want = "opening-meadow-v1" if wide else "opening-meadow-phone-v1"
        check(f"{tag}: the painting ({'whole' if wide else 'its closer middle'}) is drawn", m["decoded"] and want in m["src"], m["src"][-70:])
        check(f"{tag}: it multiplies behind the name and the bottle", m["blend"] == "multiply" and m["z"] == "-1", f"{m['blend']}, z {m['z']}")
        left, right = m["painting"]["l"], m["painting"]["r"]
        check(f"{tag}: it spans the window's width", left <= 0.5 and right >= m["W"] - 0.5, f"{left:.0f} to {right:.0f} of {m['W']}")
        check(f"{tag}: its sky reaches the window's top", m["painting"]["t"] <= 0, f"top {m['painting']['t']:.0f}")
        sink = (m["foot"] - m["ground"]) / m["bottleH"]
        check(f"{tag}: the bottle's foot stands on its ground", 0 <= sink <= 0.03, f"foot {sink * 100:.1f}% of the bottle under the ground")
        f = m["front"]
        check(f"{tag}: its own grass lies over the bottle's foot", f is not None and f["decoded"] and f["z"] == "1"
              and f["t"] < m["foot"] < f["b"] and f["l"] < m["glassMid"] < f["r"],
              f"grass {f['t']:.0f}-{f['b']:.0f}, foot {m['foot']:.0f}" if f else "no grass")
        if wide:
            # Where the painting is drawn at the name's size (wider than the window) the name's foot
            # rests over the hills with a strip of sky; where it is drawn as wide as the window (a
            # window wider than about 1600px, or a short one) it stands on the bottle's foot and its
            # land rises a little behind the name, but the name stays above the meadow (its baseline
            # in the upper half between the hills' row and the ground).
            at_name = m["painting"]["r"] - m["painting"]["l"] > m["W"] + 20
            if at_name:
                check(f"{tag}: the name's foot over the land (a strip of sky)", m["baseline"] <= m["hills"] - 0.05 * m["size"],
                      f"baseline {m['baseline']:.0f}, hills {m['hills']:.0f}")
            else:
                check(f"{tag}: the name above the meadow (the painting as wide as the window)",
                      m["baseline"] <= m["hills"] + 0.5 * (m["ground"] - m["hills"]),
                      f"baseline {m['baseline']:.0f}, hills {m['hills']:.0f}, ground {m['ground']:.0f}")
        check(f"{tag}: the words on bare paper under the painting", m["words"] >= m["end"] + 8, f"words {m['words']:.0f}, painting ends {m['end']:.0f}")
        check(f"{tag}: no sideways scroll", m["sideways"] <= 0, f"{m['sideways']}px")
        check(f"{tag}: no console errors", not errors, "; ".join(errors[:2]))
        if w in (1440, 390, 2560):
            page.screenshot(path=str(OUT / f"meadow-{w}x{h}.png"))
        ctx.close()
    # Without scripts the painting is there all the same (it is the page's markup, not a script's).
    for w, h in [(1440, 900), (390, 844)]:
        ctx, page, _, _ = opened(browser, w, h, js=False)
        page.wait_for_timeout(800)
        shown = page.evaluate("() => { const i = document.querySelector('[data-opening-painting] picture img'); return !!i && i.complete && i.naturalWidth > 1; }")
        check(f"meadow {w}x{h} no script: the painting is drawn", shown)
        ctx.close()
    # Green Bee Propolis keeps its own opening (Mo's approved lockup, its own painting since
    # November 18, 2026: qa_propolis_ink `opening`), never the shared painted opening.
    ctx, page, _, _ = opened(browser, 1440, 900, "/en/products/green-bee-propolis")
    check("meadow: Green Bee Propolis keeps its own opening", page.locator("[data-name-left]").count() == 1 and page.locator("h1 [data-half]").count() == 0 and page.locator("[data-opening-painting] picture").count() == 0)
    ctx.close()


SECTIONS = {
    "shell": shell,
    "name": name,
    "meadow": meadow,
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

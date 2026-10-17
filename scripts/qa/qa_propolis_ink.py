"""QA for Green Bee Propolis's ink page (Mo, October 13-14, 2026; picks and paintings in
reference/ink-pages/propolis/README.md). The template is NuriCell's (qa_nuricell_ink.py); this
checks what Propolis brings: its name fitted round the bottle, the gold running into the hive's
cracks, one ingredient, no painted sum, the real bottle inside a painted scene.

Sections (all, or --only=a,b):
  shell       200 in the ink look, one h1 (Green Bee Propolis), the real bottle, no canvas, no console
              errors (1440x900, 390x844)
  name        1920 to 360: readable Ysabeau title, clear of the real bottle; Vietnamese too.
              Keyboard chapter navigation and the honest checkout preview.
  chapters    overview, why, inside, research, daily, buy (no people, no sum); each its own painting;
              "Inside every capsule, one ingredient."; 200 mg; every study; the questions
  spread      the gold waits, then fills the cracks from their middle; reduced motion and no script:
              filled from the first paint; its glint mask follows
  multiply    every painting multiplies onto the paper with no box
  buy         the real bottle (green-bee-propolis.png) stands inside the scene, centred; the front layer
              multiplies over its foot and changes nothing beside it; captioned; Add to cart
  size        both original bottles undistorted and uncropped (1440, 1024, 390)
  layout      sizes 1536 to 360: no sideways scroll, paintings alternate beside their words from 960px and above
              them below, text 15px+
  deep_links  #chapter-<id> lands its heading under the menu bar
  languages   kr, jp, cns, vn: 200, no console errors, the new strings translated
Pictures: scripts/qa/out/propolis-ink/.

usage: python -X utf8 scripts/qa/qa_propolis_ink.py [base-url] [--only=shell,name,...]
"""

import re
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = ARGS[0] if ARGS else "http://localhost:3046"
ONLY = next((a.split("=", 1)[1].split(",") for a in sys.argv[1:] if a.startswith("--only=")), None)
REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "scripts/qa/out/propolis-ink"
OUT.mkdir(parents=True, exist_ok=True)
PATH = "/en/products/green-bee-propolis"
CHAPTERS = ["overview", "why", "inside", "research", "daily", "buy"]
PAINTED = ["why", "inside", "research", "daily"]
PREFETCH_CSS = re.compile(r"was preloaded using link preload but not used")
SIZES = [(1920, 1080), (1536, 864), (1440, 900), (1280, 800), (1024, 768), (960, 800), (900, 900), (768, 1024), (390, 844), (360, 780)]
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f"  ({detail})" if detail else ""), flush=True)


def opened(browser, w, h, path=PATH, reduced=False, js=True, touch=False):
    ctx = browser.new_context(
        viewport={"width": w, "height": h},
        reduced_motion="reduce" if reduced else "no-preference",
        java_script_enabled=js,
        is_mobile=touch,
        has_touch=touch,
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
        check(f"{tag}: the ink page for Propolis", page.locator('[data-product-ink="green-bee-propolis"]').count() == 1)
        check(f"{tag}: one h1", page.locator("h1").count() == 1)
        check(
            f"{tag}: the h1's accessible name is Green Bee Propolis",
            page.get_by_role("heading", level=1, name="Green Bee Propolis", exact=True).count() == 1,
        )
        check(f"{tag}: the real bottle in the opening", page.locator('[data-chapter="overview"] img[src*="green-bee-propolis.png"]').count() >= 1)
        check(f"{tag}: no canvas", page.locator("canvas").count() == 0)
        check(f"{tag}: supply visible in the opening", "60-day supply" in page.locator('[data-chapter="overview"]').inner_text())
        check(f"{tag}: no console errors", not errors, "; ".join(errors[:3]))
        page.wait_for_timeout(2500)
        page.screenshot(path=str(OUT / f"shell-{w}.png"))
        ctx.close()


def name(browser):
    """Check the new opening's readable name, real bottle and working chapter links."""
    for locale in ["en", "vn"]:
        for w, h in SIZES:
            if locale == "vn" and w not in (1440, 1024, 390):
                continue
            ctx, page, _, _ = opened(browser, w, h, f"/{locale}/products/green-bee-propolis", reduced=True)
            page.evaluate("document.fonts.ready")
            m = page.evaluate("""() => {
              const h = document.querySelector('#product-name');
              const image = document.querySelector('[data-chapter=overview] img');
              const box = e => { const r=e.getBoundingClientRect(); return {l:r.left,r:r.right,t:r.top,b:r.bottom}; };
              const range = document.createRange(); range.selectNodeContents(h);
              return {name:box(h), bottle:box(image), font:getComputedStyle(h).fontFamily,
                      lines:[...range.getClientRects()].map(r=>({l:r.left,r:r.right}))};
            }""")
            tag = f"name {locale} {w}x{h}"
            check(f"{tag}: title fits the window", all(15 <= r["l"] and r["r"] <= w-15 for r in m["lines"]))
            check(f"{tag}: title font loaded", "Ysabeau" in m["font"] and page.evaluate("document.fonts.check('500 64px Ysabeau')"))
            a, b = m["name"], m["bottle"]
            clear = a["r"] <= b["l"] if w >= 960 else a["b"] <= b["t"]
            check(f"{tag}: name and bottle do not overlap", clear, str(m))
            check(f"{tag}: bottle stays within the screen", b["l"] >= 0 and b["r"] <= w)
            if locale == "en" and w in (1440, 390):
                nav = page.get_by_role("navigation", name="Green Bee Propolis", exact=True)
                check(f"{tag}: four chapter links", nav.get_by_role("link").count() == 4)
                link = nav.get_by_role("link").nth(1)
                link.focus()
                page.keyboard.press("Enter")
                page.wait_for_timeout(1000)
                top = page.locator("#chapter-inside-title").bounding_box()["y"]
                bottom = page.locator("header").bounding_box()
                check(f"{tag}: keyboard chapter link lands below the header", bottom["y"] + bottom["height"] <= top < h - 60, f"{top:.0f}px")
                page.locator('[data-chapter=overview] button').click()
                check(f"{tag}: checkout remains an honest preview", page.get_by_text("Checkout isn't connected yet. This page is a design preview.", exact=True).is_visible())
            ctx.close()


EXPECT = [
    "Why green propolis",
    "Gathered by bees, from one Brazilian shrub.",
    "Bees make propolis from the resin they gather from plants. They line their hive with it and seal its cracks.",
    "Inside every capsule, one ingredient.",
    "Green propolis extract",
    "Amount per serving of 1 capsule, as printed on the Green Bee Propolis label.",
    "Other ingredients: rice flour, silicon dioxide and magnesium stearate.",
    "These studies are about propolis, not the finished product.",
    "One bottle, two months.",
    "Take 1 capsule a day.",
    "Developed under the direction and guidance of Dr.",
    "I’m allergic to bee products. Can I take it?",
    "These statements have not been evaluated by the Food and Drug Administration.",
]


def chapters(browser):
    ctx, page, _, _ = opened(browser, 1440, 900, reduced=True)
    found = page.evaluate("() => [...document.querySelectorAll('[data-chapter]')].map(c => c.dataset.chapter)")
    check("chapters: in order, no people", found == CHAPTERS, ", ".join(found))
    check("chapters: no painted or typed sum", page.locator("[data-sum]").count() == 0)
    srcs = page.evaluate(
        """(ids) => ids.map(id => { const i = document.querySelector(`[data-chapter="${id}"] figure[data-picture] img`);
             return i ? decodeURIComponent(i.currentSrc || i.src) : null; })""",
        PAINTED + ["buy"],
    )
    check("chapters: each its own painting", all(srcs) and len(set(srcs)) == len(srcs), "; ".join(s or "none" for s in srcs))
    check("chapters: Propolis's own paintings", all("green-bee-propolis/ink/" in s for s in srcs if s), "")
    check("chapters: 200 mg", page.locator('[data-chapter="inside"]').get_by_text("200").count() >= 1)
    page.evaluate("""() => { document.querySelector('[data-chapter="research"] button[aria-expanded="false"]')?.click();
                         document.querySelectorAll('main details').forEach(d => { d.open = true; }); }""")
    page.wait_for_timeout(300)
    # The FDA statement is in the site footer (every page since October 13), outside main.
    text = page.evaluate("() => document.body.innerText.replace(/\\s+/g, ' ')")
    missing = [e for e in EXPECT if e not in text]
    check("chapters: the page's words", not missing, "; ".join(missing))
    studies = page.locator("[data-study]").count()
    check("chapters: all seven studies", studies == 7, f"{studies}")
    alts = page.evaluate("() => [...document.querySelectorAll('main figure img[alt]')].map(i => i.alt).filter(Boolean)")
    check("chapters: every painting described", len(alts) >= 5, "; ".join(a[:30] for a in alts))
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
    check("spread: radial from the cracks' middle", "radial-gradient" in (first["mask"] or ""), (first["mask"] or "")[:80])
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
    # The glint fades in a breath and a half after the light comes on, over one breath.
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
    import io

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
        check(f"{tag}: the real bottle photo", m["src"].split("?")[0].endswith("green-bee-propolis.png") or "green-bee-propolis.png" in m["src"], m["src"][:90])
        check(f"{tag}: the bottle named", "Green Bee Propolis" in m["alt"], m["alt"])
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


def bottle_size(browser):
    """The approved image keeps its natural proportions and stays uncropped at both placements."""
    for w, h in [(1440, 900), (1024, 768), (390, 844)]:
        ctx, page, _, _ = opened(browser, w, h, reduced=True)
        for chapter in ["overview", "buy"]:
            image = page.locator(f'[data-chapter="{chapter}"] img[src*="green-bee-propolis.png"]').first
            image.scroll_into_view_if_needed()
            image.evaluate("i => i.decode()")
            m = image.evaluate("""i => {const r=i.getBoundingClientRect(); return {w:r.width,h:r.height,nw:i.naturalWidth,nh:i.naturalHeight,l:r.left,r:r.right};}""")
            check(f"bottle {w} {chapter}: original proportions", abs(m["w"]/m["h"] - m["nw"]/m["nh"]) < 0.01)
            check(f"bottle {w} {chapter}: fully within the page", m["l"] >= 0 and m["r"] <= w)
        ctx.close()


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
                 const reverse = ['inside', 'daily'].includes(c.dataset.chapter);
                 const ok = two ? (reverse ? t.right <= f.left + 1 : f.right <= t.left + 1) : f.bottom <= t.top + 1;
                 return ok ? null : c.dataset.chapter; }).filter(Boolean)""",
            w >= 960,
        )
        check(f"{tag}: each painting {'alternates beside' if w >= 960 else 'sits above'} its words", not bad, ", ".join(bad))
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
        ctx, page, response, errors = opened(browser, 1440, 900, f"/{locale}/products/green-bee-propolis", reduced=True)
        tag = f"languages {locale}"
        check(f"{tag}: 200", response is not None and response.status == 200)
        check(f"{tag}: no console errors", not errors, "; ".join(errors[:2]))
        check(f"{tag}: the one-ingredient heading translated", page.locator("#chapter-inside-title").inner_text().strip() == heading,
              page.locator("#chapter-inside-title").inner_text().strip())
        english = page.evaluate("() => [...document.querySelectorAll('main figure img[alt]')].map(i => i.alt).filter(a => /painted in|bee flying/.test(a))")
        check(f"{tag}: the paintings described in {locale}", not english, "; ".join(english[:2]))
        ctx.close()


def navigation(browser):
    """Native focus/auto-scroll must not leave the smooth-scroll clock behind the link target."""
    for w, h, touch in [(1440, 900, False), (390, 844, False), (390, 844, True)]:
        ctx, page, _, errors = opened(browser, w, h, touch=touch)
        page.wait_for_timeout(2200)
        nav = page.get_by_role("navigation", name="Green Bee Propolis", exact=True)
        for index, chapter in enumerate(["why", "inside", "research", "daily"]):
            link = nav.get_by_role("link").nth(index)
            link.focus()
            page.keyboard.press("Enter")
            page.wait_for_timeout(1800)
            target = page.locator(f"#chapter-{chapter}-title")
            top = target.bounding_box()["y"]
            header = page.locator("header").bounding_box()
            check(f"navigation {w} {chapter}: heading near the top, below the menu", header["y"] + header["height"] <= top <= h / 2, f"{top:.0f}px")
            check(f"navigation {w} {chapter}: focus and address follow the chapter", target.evaluate("e => e === document.activeElement") and page.url.endswith(f"#chapter-{chapter}"))
        check(f"navigation {w}: no page errors", not errors, str(errors))
        ctx.close()


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
    "navigation": navigation,
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

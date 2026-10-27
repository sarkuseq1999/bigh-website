"""QA for the product pages' questions (Mo's pick A, October 26, 2026; questions.tsx): each answer with
its own painting, on all five ink product pages.

Checks, per page:
  wide        1440x900 and 960x800: the questions on the left (on the heading's edge), the picked one's
              painting and answer on the right; the first picked as the page opens and its wash laid,
              its round toggle gone and the others' showing;
              picking each in turn shows only its panel (painting loaded, answer readable), moves the
              wash, and never changes the section's height; every answer sits at the same height
              under its painting; the painting multiplies with no group around it; Up and Down move
              between questions; no sideways scroll
  phone       390x844: the first open with its painting; tapping it closes it, tapping another opens
              that one alone; the toggles turn; targets 44px or taller; no sideways scroll
  noscript    no script: the first answer and its painting are on the page
  languages   kr, jp, cns, vn: 200, every question and answer has words, no console errors
Pictures: scripts/qa/out/questions/.

usage: python -X utf8 scripts/qa/qa_questions.py [base-url] [--only=wide,phone,...] [--pages=nuricell,...]
"""

import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = ARGS[0] if ARGS else "http://localhost:3007"
ONLY = next((a.split("=", 1)[1].split(",") for a in sys.argv[1:] if a.startswith("--only=")), None)
PAGES_ARG = next((a.split("=", 1)[1].split(",") for a in sys.argv[1:] if a.startswith("--pages=")), None)
REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "scripts/qa/out/questions"
OUT.mkdir(parents=True, exist_ok=True)
# Each page's number of questions (its `faq`).
PAGES = {"nuricell": 6, "advanced-opc": 6, "green-bee-propolis": 6, "nature-calm": 5, "turmerific": 5}
PREFETCH_CSS = re.compile(r"was preloaded using link preload but not used")
CHUNK_404 = re.compile(r"/_next/static/chunks/.*404")
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f"  ({detail})" if detail else ""), flush=True)


def opened(browser, w, h, path, reduced=True, js=True, mobile=False):
    ctx = browser.new_context(
        viewport={"width": w, "height": h},
        device_scale_factor=2 if mobile else 1,
        is_mobile=mobile,
        has_touch=mobile,
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


def bring(page, top=96):
    for _ in range(2):
        page.evaluate(f"() => {{ const e = document.querySelector('#questions'); window.scrollBy(0, e.getBoundingClientRect().top - {top}); }}")
        page.wait_for_timeout(400)


STATE = """() => {
  const items = [...document.querySelectorAll('#questions ol > li')];
  const section = document.querySelector('#questions');
  return {
    height: Math.round(section.getBoundingClientRect().height),
    heading: document.querySelector('#questions h2').getBoundingClientRect().left,
    items: items.map((li) => {
      const button = li.querySelector('button');
      const panel = li.querySelector('[role="region"]');
      const img = panel.querySelector('img');
      const answer = panel.querySelector('p');
      const words = li.querySelector('button > span');
      const pr = panel.getBoundingClientRect(), br = button.getBoundingClientRect();
      return {
        expanded: button.getAttribute('aria-expanded'),
        controls: button.getAttribute('aria-controls') === panel.id,
        shown: getComputedStyle(panel).display !== 'none' && getComputedStyle(panel).visibility === 'visible',
        img: !!img, loaded: !!img && img.complete && img.naturalWidth > 0,
        blend: img ? getComputedStyle(img).mixBlendMode : '',
        opacity: img ? getComputedStyle(img).opacity : '',
        answerOpacity: getComputedStyle(answer).opacity,
        answerTop: Math.round(answer.getBoundingClientRect().top - pr.top),
        answerText: answer.innerText.trim().length,
        wash: getComputedStyle(words, '::after').scale,
        buttonLeft: br.left, buttonRight: br.right, buttonHeight: br.height,
        panelLeft: pr.left, panelWidth: pr.width,
        toggle: (() => { const t = button.querySelector('[aria-hidden]'); const r = t.getBoundingClientRect(); return { w: r.width, h: r.height, rotate: getComputedStyle(t).rotate, display: getComputedStyle(t).display, opacity: getComputedStyle(t).opacity }; })(),
      };
    }),
    scrollW: document.documentElement.scrollWidth, innerW: innerWidth,
  };
}"""

# Anything between the painting and the section that would make its own group (and show the
# painting's white paper instead of multiplying it onto the page).
GROUPS = """() => {
  const out = [];
  for (const img of document.querySelectorAll('#questions img')) {
    for (let e = img.parentElement; e && e.id !== 'questions'; e = e.parentElement) {
      const s = getComputedStyle(e);
      if (s.opacity !== '1' || s.transform !== 'none' || s.filter !== 'none' || s.isolation === 'isolate' || s.mixBlendMode !== 'normal' || (s.zIndex !== 'auto' && s.position !== 'static') || s.willChange !== 'auto' || s.contain !== 'none')
        out.push(e.tagName + '.' + e.className);
    }
  }
  return [...new Set(out)];
}"""


def wide(browser, slug, n):
    for w, h in [(1440, 900), (960, 800)]:
        tag = f"{slug} {w}"
        ctx, page, response, errors = opened(browser, w, h, f"/en/products/{slug}")
        check(f"{tag}: 200", response.status == 200, str(response.status))
        bring(page)
        page.wait_for_timeout(600)
        s = page.evaluate(STATE)
        items = s["items"]
        check(f"{tag}: {n} questions, each with a painting", len(items) == n and all(i["img"] for i in items), str(len(items)))
        check(f"{tag}: the first is picked", [i["expanded"] for i in items] == ["true"] + ["false"] * (n - 1), str([i["expanded"] for i in items]))
        check(f"{tag}: buttons control their answers", all(i["controls"] for i in items))
        check(f"{tag}: only the first answer shows", [i["shown"] for i in items] == [True] + [False] * (n - 1), str([i["shown"] for i in items]))
        check(f"{tag}: questions on the heading's edge", all(abs(i["buttonLeft"] - s["heading"]) <= 1 for i in items), str([round(i["buttonLeft"]) for i in items]))
        check(f"{tag}: the answer stands right of the questions", all(i["panelLeft"] > i["buttonRight"] + 30 for i in items), f"{items[0]['buttonRight']:.0f} -> {items[0]['panelLeft']:.0f}")
        check(f"{tag}: the others keep their toggles, the picked one lets its go", items[0]["toggle"]["opacity"] == "0" and all(i["toggle"]["opacity"] == "1" and i["toggle"]["display"] != "none" for i in items[1:]), str([i["toggle"]["opacity"] for i in items]))
        check(f"{tag}: every answer at one height under its painting", len({i["answerTop"] for i in items}) == 1, str([i["answerTop"] for i in items]))
        check(f"{tag}: the paintings multiply", all(i["blend"] == "multiply" for i in items))
        groups = page.evaluate(GROUPS)
        check(f"{tag}: nothing groups the paintings", not groups, ", ".join(groups))
        check(f"{tag}: the first's wash is laid, the others' not", items[0]["wash"] in ("1 1", "1") and all(i["wash"] == "0 1" for i in items[1:]), str([i["wash"] for i in items]))
        page.screenshot(path=str(OUT / f"{slug}-{w}-0.png"))
        height = s["height"]
        for k in range(n):
            page.locator("#questions ol > li > h3 button").nth(k).click()
            page.wait_for_timeout(250)
            page.wait_for_function(
                f"() => {{ const i = document.querySelectorAll('#questions ol > li img')[{k}]; return i.complete && i.naturalWidth > 0; }}",
                timeout=8000,
            )
            t = page.evaluate(STATE)
            it = t["items"]
            check(
                f"{tag}: pick {k + 1} shows only its answer, its painting loaded",
                [i["shown"] for i in it] == [j == k for j in range(n)] and it[k]["loaded"] and it[k]["answerText"] > 0 and it[k]["opacity"] == "1" and it[k]["answerOpacity"] == "1",
                str([i["shown"] for i in it]),
            )
            check(f"{tag}: pick {k + 1} moves the wash", it[k]["wash"] in ("1 1", "1") and all(i["wash"] == "0 1" for j, i in enumerate(it) if j != k), str([i["wash"] for i in it]))
            check(f"{tag}: pick {k + 1} keeps the section's height", abs(t["height"] - height) <= 1, f"{height} -> {t['height']}")
            if k == 2 and w == 1440:
                page.screenshot(path=str(OUT / f"{slug}-{w}-pick3.png"))
            if k == n - 1 and w == 1440:
                page.screenshot(path=str(OUT / f"{slug}-{w}-last.png"))
        page.locator("#questions ol > li > h3 button").first.focus()
        page.keyboard.press("ArrowDown")
        focused = page.evaluate("() => [...document.querySelectorAll('#questions ol > li > h3 button')].indexOf(document.activeElement)")
        page.keyboard.press("End")
        last = page.evaluate("() => [...document.querySelectorAll('#questions ol > li > h3 button')].indexOf(document.activeElement)")
        check(f"{tag}: Down and End move between questions", focused == 1 and last == n - 1, f"{focused}, {last}")
        check(f"{tag}: no sideways scroll", s["scrollW"] <= s["innerW"], f"{s['scrollW']} vs {s['innerW']}")
        check(f"{tag}: no console errors", not errors, "; ".join(errors[:2]))
        ctx.close()


def phone(browser, slug, n):
    tag = f"{slug} 390"
    ctx, page, response, errors = opened(browser, 390, 844, f"/en/products/{slug}", mobile=True)
    bring(page, 70)
    page.wait_for_timeout(600)
    s = page.evaluate(STATE)
    items = s["items"]
    check(f"{tag}: the first open with its painting", [i["shown"] for i in items] == [True] + [False] * (n - 1) and items[0]["loaded"], str([i["shown"] for i in items]))
    check(f"{tag}: the open toggle turned", items[0]["toggle"]["rotate"] == "45deg" and all(i["toggle"]["rotate"] in ("none", "0deg") for i in items[1:]), str([i["toggle"]["rotate"] for i in items]))
    check(f"{tag}: targets 44px or taller", all(i["buttonHeight"] >= 44 and i["toggle"]["w"] >= 44 and i["toggle"]["h"] >= 44 for i in items))
    check(f"{tag}: the painting spans the column", items[0]["panelWidth"] >= 390 - 2 * 32, f"{items[0]['panelWidth']:.0f}px")
    page.screenshot(path=str(OUT / f"{slug}-390-0.png"))
    buttons = page.locator("#questions ol > li > h3 button")
    buttons.first.tap()
    page.wait_for_timeout(300)
    t = page.evaluate(STATE)["items"]
    check(f"{tag}: tapping the open question closes it", all(not i["shown"] for i in t) and t[0]["expanded"] == "false", str([i["shown"] for i in t]))
    buttons.nth(2).tap()
    page.wait_for_timeout(300)
    page.wait_for_function("() => { const i = document.querySelectorAll('#questions ol > li img')[2]; return i.complete && i.naturalWidth > 0; }", timeout=8000)
    t = page.evaluate(STATE)["items"]
    check(f"{tag}: tapping another opens it alone", [i["shown"] for i in t] == [j == 2 for j in range(n)] and t[2]["loaded"] and t[2]["answerText"] > 0, str([i["shown"] for i in t]))
    page.evaluate("() => document.querySelectorAll('#questions ol > li')[2].scrollIntoView({ block: 'start' })")
    page.evaluate("() => window.scrollBy(0, -80)")
    page.wait_for_timeout(400)
    page.screenshot(path=str(OUT / f"{slug}-390-pick3.png"))
    t2 = page.evaluate(STATE)
    check(f"{tag}: no sideways scroll", t2["scrollW"] <= t2["innerW"], f"{t2['scrollW']} vs {t2['innerW']}")
    check(f"{tag}: no console errors", not errors, "; ".join(errors[:2]))
    ctx.close()


def noscript(browser, slug, n):
    ctx, page, response, _ = opened(browser, 1440, 900, f"/en/products/{slug}", js=False)
    first = page.evaluate(
        """() => { const li = document.querySelector('#questions ol > li'); const panel = li.querySelector('[role="region"]');
             return { shown: getComputedStyle(panel).visibility === 'visible', img: !!panel.querySelector('img'), text: panel.innerText.trim().length,
                      all: document.querySelectorAll('#questions [role="region"] p').length }; }"""
    )
    check(f"{slug} no script: the first answer and its painting", first["shown"] and first["img"] and first["text"] > 0 and first["all"] == n, str(first))
    ctx.close()


def languages(browser, slug, n):
    for locale in ("kr", "jp", "cns", "vn"):
        ctx, page, response, errors = opened(browser, 1440, 900, f"/{locale}/products/{slug}")
        words = page.evaluate("() => [...document.querySelectorAll('#questions ol > li')].map((li) => [li.querySelector('button').textContent.trim().length, li.querySelector('[role=region] p').textContent.trim().length])")
        check(f"{slug} {locale}: 200, every question and answer has words", response.status == 200 and len(words) == n and all(q and a for q, a in words), str(response.status))
        check(f"{slug} {locale}: no console errors", not errors, "; ".join(errors[:2]))
        ctx.close()


SECTIONS = {"wide": wide, "phone": phone, "noscript": noscript, "languages": languages}

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--use-angle=d3d11"])
        for slug, n in PAGES.items():
            if PAGES_ARG and slug not in PAGES_ARG:
                continue
            for name, run in SECTIONS.items():
                if ONLY and name not in ONLY:
                    continue
                print(f"\n== {slug} {name}", flush=True)
                run(browser, slug, n)
        browser.close()
    failed = [r for r in results if not r[1]]
    print(f"\n{len(results) - len(failed)}/{len(results)} passed")
    sys.exit(1 if failed else 0)

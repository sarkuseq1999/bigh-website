"""QA for the refined Glass cell: topic tabs, topic pictures, the age dial, explainers, reduced motion."""
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3007"
LOCALES = sys.argv[2].split(",") if len(sys.argv) > 2 else ["", "kr"]
passed = failed = 0


def check(name, ok, detail=""):
    global passed, failed
    passed += bool(ok)
    failed += not ok
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))


def open_page(browser, w, h, url, reduced=False):
    ctx = browser.new_context(viewport={"width": w, "height": h}, reduced_motion="reduce" if reduced else "no-preference")
    page = ctx.new_page()
    problems = []
    page.on("pageerror", lambda e: problems.append(f"pageerror {e}"))
    page.on("console", lambda m: problems.append(f"console {m.text[:140]}") if m.type == "error" else None)
    page.on("response", lambda r: problems.append(f"{r.status} {r.url[-50:]}") if r.status >= 400 else None)
    page.goto(url, wait_until="networkidle")
    page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
    return ctx, page, problems


def walk(page, y, steps=8):
    current = page.evaluate("scrollY")
    for s in range(1, steps + 1):
        page.evaluate(f"window.scrollTo(0, {current + (y - current) * s / steps})")
        page.wait_for_timeout(50)


STATE = """(() => {
  const root = document.querySelector('#learn [data-chapter]');
  const tabs = [...document.querySelectorAll('#learn nav button')];
  return {
    chapter: root.dataset.chapter,
    tab: tabs.findIndex(t => t.getAttribute('aria-current') === 'step'),
    age: document.querySelector('#learn [class*=age] strong').textContent,
    visibleParts: [...document.querySelectorAll('#learn [data-part]')].filter(e => +getComputedStyle(e).opacity > 0.9).map(e => e.dataset.part),
  };
})()"""

with sync_playwright() as p:
    browser = p.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    for loc in LOCALES:
        tag0 = loc or "en"
        for label, (w, h) in {"desk": (1440, 900), "phone": (390, 844)}.items():
            ctx, page, problems = open_page(browser, w, h, f"{BASE}/{loc}")
            top, height = page.evaluate("(() => { const t = document.querySelector('#learn [class*=track]'); return [t.getBoundingClientRect().top + scrollY, t.offsetHeight]; })()")
            states = []
            for at in (0.14, 0.5, 0.97):
                walk(page, top + (height - h) * at)
                page.wait_for_timeout(1400)
                states.append(page.evaluate(STATE))
            ready = page.evaluate("document.querySelector('#learn [data-ready]').dataset.ready")
            chapters = [s["chapter"] for s in states]
            tabs = [s["tab"] for s in states]
            parts = [sorted(set(s["visibleParts"])) for s in states]
            ok = (ready == "true" and chapters == ["0", "1", "2"] and tabs == [0, 1, 2]
                  and parts == [["0"], ["1"], ["2"]])
            overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            check(f"{tag0}-{label}: WebGL ready; scrolling moves topics 1-2-3 with the matching tab and picture; no overflow/errors",
                  ok and overflow == 0 and not problems,
                  f"ready={ready} chapters={chapters} tabs={tabs} parts={parts} age={states[2]['age']} overflow={overflow} {problems[:2]}")
            # Topic 3: the slider. The first visit demonstrates it; then keyboard and pointer drive it.
            page.wait_for_timeout(1500)  # the demo sweep takes 0.5 s + 1.8 s after arrival
            demo = page.evaluate(STATE)["age"]
            slider = page.locator("#learn input[type=range]")
            slider.focus()
            page.keyboard.press("End")
            page.wait_for_timeout(700)
            end = page.evaluate("[document.querySelector('#learn [class*=age] strong').textContent, getComputedStyle(document.querySelector('#learn [data-chapter]')).getPropertyValue('--age').trim()]")
            box = slider.bounding_box()
            page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.mouse.down()
            page.mouse.move(box["x"] + 2, box["y"] + box["height"] / 2, steps=8)
            page.mouse.up()
            page.wait_for_timeout(600)
            dragged = page.evaluate(STATE)["age"]
            check(f"{tag0}-{label}: age slider demo, End key to 80 (glow fully aged), drag back to 20",
                  demo == "45" and end[0] == "80" and float(end[1] or 0) > 0.99 and dragged == "20",
                  f"demo={demo} end={end} dragged={dragged}")
            # Topic 2: the scene walks through its three steps.
            page.locator("#learn nav button").nth(1).click()
            seen = set()
            for _ in range(60):
                lit = page.evaluate("[...document.querySelectorAll('#learn [data-step]')].findIndex(e => e.dataset.lit === 'true')")
                seen.add(lit)
                page.wait_for_timeout(200)
            check(f"{tag0}-{label}: the free-radical scene lights steps 1, 2 and 3 in turn", {0, 1, 2} <= seen, str(sorted(seen)))
            # Tabs jump straight to a topic.
            page.locator("#learn nav button").nth(1).click()
            page.wait_for_timeout(1800)
            jumped = page.evaluate(STATE)
            page.locator("#learn nav button").nth(0).click()
            page.wait_for_timeout(1800)
            back = page.evaluate(STATE)
            check(f"{tag0}-{label}: tabs jump to Free radicals and back to Mitochondria",
                  jumped["chapter"] == "1" and jumped["tab"] == 1 and back["chapter"] == "0", f"{jumped['chapter']} then {back['chapter']}")
            page.locator("#learn article[data-active='true'] button").click()
            page.wait_for_timeout(500)
            title = page.locator("dialog[open] h2").inner_text() if page.locator("dialog[open]").count() else None
            page.keyboard.press("Escape")
            page.wait_for_timeout(300)
            check(f"{tag0}-{label}: the topic's explainer opens and closes",
                  bool(title) and page.locator("dialog[open]").count() == 0, f"dialog={title!r}")
            ctx.close()

    ctx, page, problems = open_page(browser, 1440, 900, f"{BASE}/", reduced=True)
    page.evaluate("document.getElementById('learn').scrollIntoView()")
    page.wait_for_timeout(600)
    active = page.evaluate("[...document.querySelectorAll('#learn article')].filter(a => a.dataset.active === 'true').length")
    canvas = page.locator("#learn canvas").count()
    still = page.evaluate("getComputedStyle(document.querySelector('#learn [class*=still]')).visibility")
    check("Reduced motion: still cell, all three topics readable, no WebGL, no errors",
          active == 3 and canvas == 0 and still == "visible" and not problems, f"active={active} canvas={canvas} still={still} {problems[:2]}")
    ctx.close()
    browser.close()

print(f"\n{passed} passed, {failed} failed")

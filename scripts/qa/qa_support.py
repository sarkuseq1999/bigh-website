"""QA for the Support page, "Pull up a chair" (Mo, October 14, 2026; spec
docs/superpowers/specs/2026-10-14-support-page-design.md; mockups reference/ink-pages/mockups/support/).

opening (1440x900, 390x844): 200; the title "BiGH — Support"; no console errors or warnings (but
PREFETCH_CSS); no failed requests; one h1 "How can we help?"; the lead; the phone number as a tel:
link in Switzer, the email as a mailto: link, the hours; the porch painting multiplies; its steam is
gold leaf over the porch, not multiplied; nothing scrolls sideways; text 15px+; the menu bar marks
Support (Task 5 adds the link; until then the bar's root says data-page="support").
motion (1440x900): with motion the steam waits while the porch waits, then rises (its --rise grows
from under 30% to 100%+ within 6s of the porch's bloom; sampled every frame from the page's first
one, since the rise has begun by the time the page is idle); reduced motion: the steam is whole at
once.
(Later tasks add: rhythm, questions, form, languages, links.)

Pictures: scripts/qa/out/support/<tag>.png.

Usage: python -X utf8 scripts/qa/qa_support.py [base-url] [--only=opening,motion,...]
"""

import os
import re
import sys

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = ARGS[0] if ARGS else "http://localhost:3060"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "support")
os.makedirs(OUT, exist_ok=True)
results = []

PREFETCH_CSS = re.compile(
    r"^The resource \S+/_next/static/\S+\.css was preloaded using link preload but not used "
    r"within a few seconds from the window's load event\."
)


def check(name, ok, detail=""):
    results.append((name, bool(ok)))
    print(f"{'PASS' if ok else 'FAIL'} {name}{(' — ' + str(detail)) if detail and not ok else ''}")


def counted(message):
    return message.type != "warning" or not PREFETCH_CSS.match(message.text)


def open_page(browser, width, height, path="/support", reduced=False):
    context = browser.new_context(
        viewport={"width": width, "height": height},
        reduced_motion="reduce" if reduced else "no-preference",
    )
    page = context.new_page()
    errors, failed = [], []
    page.on("console", lambda m: errors.append(m.text) if m.type in ("error", "warning") and counted(m) else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("requestfailed", lambda r: failed.append(r.url))
    response = page.goto(f"{BASE}{path}", wait_until="networkidle", timeout=120000)
    page.evaluate("document.fonts.ready.then(() => true)")
    page.wait_for_timeout(1200)
    return context, page, response, errors, failed


def scroll_through(page, step=450, pause=250):
    """Read to the end like a visitor (lazy pictures load, blooms fire), then back to the top."""
    total = page.evaluate("document.documentElement.scrollHeight")
    y = 0
    while y < total:
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(pause)
        y += step
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(600)


SMALL_TEXT_JS = """[...document.querySelectorAll('main *')].filter(e => {
  if (!e.childNodes.length || ![...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) return false;
  const s = getComputedStyle(e); return s.visibility !== 'hidden' && s.display !== 'none' && parseFloat(s.fontSize) < 15;
}).map(e => [e.textContent.trim().slice(0, 30), getComputedStyle(e).fontSize])"""


def opening(browser):
    for width, height in ((1440, 900), (390, 844)):
        tag = f"opening {width}"
        context, page, response, errors, failed = open_page(browser, width, height)
        check(f"{tag}: 200", response and response.status == 200, response and response.status)
        check(f"{tag}: the title", page.title() == "BiGH — Support", page.title())
        h1 = page.evaluate("[...document.querySelectorAll('h1')].map(h => h.textContent.trim())")
        check(f"{tag}: one h1, 'How can we help?'", h1 == ["How can we help?"], h1)
        main = page.inner_text("main")
        for words in ["Pull up a chair. We’re listening.", "Call us", "Email us", "Hours",
                      "Monday to Friday, 9am to 6pm Pacific"]:
            check(f"{tag}: says {words!r}", words in main)
        tel = page.evaluate("""(() => { const a = document.querySelector('main a[href^="tel:"]');
          return a ? [a.getAttribute('href'), a.textContent.trim(), getComputedStyle(a).fontFamily] : null; })()""")
        check(f"{tag}: the number is a tel: link in Switzer",
              tel and tel[0] == "tel:+18009192089" and tel[1] == "800-919-2089" and "ysabeau" not in tel[2].lower(), tel)
        mail = page.evaluate("document.querySelector('main a[href^=\"mailto:\"]')?.getAttribute('href')")
        check(f"{tag}: the email is a mailto: link", mail == "mailto:support@bighnow.com", mail)
        blend = page.evaluate("""[...document.querySelectorAll('[data-part="opening"] img')].map(i =>
          [i.getAttribute('src').includes('steam') ? 'steam' : 'ink', getComputedStyle(i).mixBlendMode])""")
        check(f"{tag}: the porch multiplies, its steam does not",
              ["ink", "multiply"] in blend and ["steam", "normal"] in blend, blend)
        title_font = page.evaluate("getComputedStyle(document.querySelector('h1')).fontFamily")
        check(f"{tag}: the title is in Ysabeau", "ysabeau" in title_font.lower(), title_font)
        sideways = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
        check(f"{tag}: nothing scrolls sideways", sideways <= 0, sideways)
        small = page.evaluate(SMALL_TEXT_JS)
        check(f"{tag}: text 15px or more", not small, small[:3])
        check(f"{tag}: the page says it is Support", page.evaluate("document.querySelector('[data-look]')?.dataset.page") == "support")
        page.screenshot(path=os.path.join(OUT, f"opening-{width}.png"))
        scroll_through(page)
        check(f"{tag}: no errors", not errors, errors[:3])
        check(f"{tag}: no failed requests", not failed, failed[:3])
        context.close()


RISE_JS = "parseFloat(getComputedStyle(document.querySelector('[data-steam]')).getPropertyValue('--rise'))"

# Watches the steam from the first frame the page has one (open_page waits for the network, the
# fonts and 1.2s, by when the steam has long been rising): one sample per frame,
# [ms since the page began, the steam's --rise, the porch's data-bloom].
WATCH_RISE = """
window.__rise = [];
const t0 = performance.now();
const tick = () => {
  const steam = document.querySelector('[data-steam]');
  const porch = document.querySelector('[data-part="opening"] [data-bloom]');
  if (steam) window.__rise.push([performance.now() - t0,
    parseFloat(getComputedStyle(steam).getPropertyValue('--rise')), porch && porch.dataset.bloom]);
  if (window.__rise.length < 4000) requestAnimationFrame(tick);
};
requestAnimationFrame(tick);
"""


def motion(browser):
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="no-preference")
    context.add_init_script(WATCH_RISE)
    page = context.new_page()
    page.goto(f"{BASE}/support", wait_until="domcontentloaded", timeout=120000)
    page.wait_for_function("window.__rise.some(s => s[2] && s[2] !== 'waiting')", timeout=30000)
    page.wait_for_timeout(6500)
    samples = page.evaluate("window.__rise")
    waiting = [s for s in samples if s[2] == "waiting"]
    bloomed = [s for s in samples if s[2] != "waiting"]
    check("motion: the steam waits while the porch waits",
          waiting and all(s[1] < 30 for s in waiting), [round(s[1]) for s in waiting[:5]])
    start, end = bloomed[0], max(s[1] for s in bloomed if s[0] <= bloomed[0][0] + 6000)
    check("motion: the steam rises after the porch blooms", start[1] < 30 and end >= 100,
          [round(start[1]), round(end)])
    context.close()
    context, page, *_ = open_page(browser, 1440, 900, reduced=True)
    whole = page.evaluate(RISE_JS)
    check("motion (reduced): the steam is whole at once", whole >= 100, whole)
    context.close()


GROUPS = [opening, motion]
ONLY = next((a.split("=", 1)[1].split(",") for a in sys.argv[1:] if a.startswith("--only=")), None)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--use-angle=d3d11"])
        for group in GROUPS:
            if ONLY is None or group.__name__ in ONLY:
                group(browser)
        browser.close()
    passed = sum(ok for _, ok in results)
    print(f"\n{passed}/{len(results)} passed")
    sys.exit(0 if passed == len(results) else 1)

"""Viewport shots of the Science ink page for review (viewport shots, as a visitor sees them). Each
screen as a visitor scrolls to it: the opening (the title and Dr. Liu), each place of his path in the
middle of the window (Mo's pick B, October 26, 2026), each strip (its header and painting, then its
words), the formulas, the footer.

usage: python -X utf8 scripts/qa/shoot_science_ink.py [base-url] [--sizes=1440x900,390x844] [--lang=en]
       [--screens=footer,opening]  (only those screens, same file names; default all)
Pictures: scripts/qa/out/science-ink/final/<size>-<nn>-<screen>.png
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = ARGS[0] if ARGS else "http://localhost:3050"
OPTS = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
SIZES = [tuple(map(int, s.split("x"))) for s in OPTS.get("sizes", "1440x900,1280x720,1024x768,390x844").split(",")]
LANG = OPTS.get("lang", "en")
SCREENS = set(OPTS["screens"].split(",")) if "screens" in OPTS else None
OUT = Path(__file__).resolve().parents[2] / "scripts/qa/out/science-ink/final"
OUT.mkdir(parents=True, exist_ok=True)

def settle(page, y, wait=3600):
    # Arrive the way a visitor does (a few steps), so the strips' paintings bloom on the way in.
    current = page.evaluate("scrollY")
    for i in range(1, 5):
        page.evaluate(f"window.scrollTo(0, {current + (y - current) * i / 4})")
        page.wait_for_timeout(60)
    page.wait_for_timeout(wait)


def to(page, selector, top):
    return page.evaluate(
        "([s, t]) => document.querySelector(s).getBoundingClientRect().top + scrollY - t", [selector, top]
    )


def shoot(browser, w, h):
    ctx = browser.new_context(viewport={"width": w, "height": h})
    page = ctx.new_page()
    page.goto(f"{BASE}/{LANG}/science", wait_until="networkidle")
    page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
    page.wait_for_timeout(3500)
    bar = page.evaluate("document.querySelector('header').getBoundingClientRect().bottom")
    screens = [("opening", None)]
    # Each place in the middle of what the menu bar leaves (or under the bar, if it is taller).
    places = page.evaluate(
        """bar => [...document.querySelectorAll('[data-place]')].map(li => { const r = li.getBoundingClientRect();
          return [li.dataset.place, r.top + scrollY - bar - Math.max(0, (innerHeight - bar - r.height) / 2)]; })""",
        bar,
    )
    screens += [(f"path-{key}", y) for key, y in places]
    for part in ["research", "health", "formulas", "ask"]:
        if part == "formulas":
            screens.append((part, to(page, "#formulas header", bar + 40)))
            continue
        screens.append((part, to(page, f"#{part} header", bar + 40)))
        # The words from the painting's caption down: the painting itself just gone under the
        # menu bar, so no sliver of it (or a half-hidden caption) sits under the bar.
        shown = page.evaluate(f"!!document.querySelector('#{part} figure[data-picture]').offsetParent")
        if shown:
            y = page.evaluate(f"document.querySelector('#{part} figure[data-picture] img').getBoundingClientRect().bottom + scrollY - {bar - 4}")
        else:
            y = to(page, f"#{part} ul, #{part} ol", bar + 40)
        screens.append((f"{part}-words", y))
    screens.append(("footer", page.evaluate("document.documentElement.scrollHeight - innerHeight")))
    for n, (name, y) in enumerate(screens, 1):
        if SCREENS is not None and name not in SCREENS:
            continue
        if y is not None:
            settle(page, max(0, y))
        path = OUT / f"{w}x{h}-{n:02d}-{name}{'' if LANG == 'en' else '-' + LANG}.png"
        page.screenshot(path=str(path))
        print(path.name, flush=True)
    ctx.close()


if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for w, h in SIZES:
            shoot(browser, w, h)
        browser.close()

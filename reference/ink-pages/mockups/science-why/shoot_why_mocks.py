"""Film each picture idea for "Why start with the cell?" on the real Science page (November 6, 2026).

The page is the real one (a dev or built server of the Science round-3 branch); for each idea the
town's pictures are swapped as the browser fetches them (the base, its six lamp layers, the phone
cut and its lit cut, from build_why_mocks.py) and the figure's ratios and caption are set to the
idea's. "town" is the page as built. Frames, at each size, with the picture in the middle of the
window: early (painted in, nothing lit), mid (some lit), lit (all lit), and "head" (the heading
with the picture under it, all lit).

usage: python -X utf8 reference/ink-pages/mockups/science-why/shoot_why_mocks.py [base-url]
       [--ideas=town,monarchs] [--sizes=1440x900,390x844]
Pictures: reference/ink-pages/mockups/science-why/shots/<idea>-<w>-<frame>.png
"""

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = ARGS[0] if ARGS else "http://localhost:3094"
OPTS = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
IDEAS = OPTS.get("ideas", "town,monarchs,sunflowers,cheek").split(",")
SIZES = [tuple(map(int, s.split("x"))) for s in OPTS.get("sizes", "1440x900,390x844").split(",")]
OUT = HERE / "shots"
OUT.mkdir(parents=True, exist_ok=True)
CAPTIONS = {
    "monarchs": "Like monarchs on a cold morning in Pacific Grove: each one warms up its own flight muscles before it can fly.",
    "sunflowers": "Like a sunflower field in the Sacramento Valley at sunrise: every plant makes its own food from the light.",
    "cheek": "A few of your own cheek cells, as a school microscope shows them. Each one makes its own energy.",
}
FILES = {"town": "base.webp", "town-phone": "phone.webp", "town-phone-lit": "phone-lit.webp"}
FILES.update({f"town-lamps-{k}": f"lamps-{k}.webp" for k in range(1, 7)})
PICTURE = re.compile(r"/images/science/ink/(town[a-z0-9-]*?)-v3\.webp")


def swap(idea):
    def handle(route):
        m = PICTURE.search(unquote(route.request.url))
        if not m or m.group(1) not in FILES:
            return route.continue_()
        body = (HERE / idea / FILES[m.group(1)]).read_bytes()
        route.fulfill(status=200, body=body, headers={"content-type": "image/webp", "cache-control": "no-store"})

    return handle


def film(browser, idea, w, h):
    ctx = browser.new_context(viewport={"width": w, "height": h})
    if idea != "town":
        ctx.route("**/*", swap(idea))
    page = ctx.new_page()
    page.goto(f"{BASE}/en/science", wait_until="networkidle")
    page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
    if idea != "town":
        meta = json.loads((HERE / idea / "meta.json").read_text(encoding="utf-8"))
        page.evaluate(
            """([m, caption]) => { const f = document.querySelector('#health figure');
              f.style.setProperty('--ar-wide', `${m.width} / ${m.height}`);
              f.style.setProperty('--ar-narrow', `${m.phone[0]} / ${m.phone[1]}`);
              f.querySelector('figcaption span').textContent = caption; }""",
            [meta, CAPTIONS[idea]],
        )
    page.wait_for_timeout(2500)
    bar = page.evaluate("document.querySelector('header').getBoundingClientRect().bottom")
    y = page.evaluate(
        """bar => { const r = document.querySelector('#health figure').getBoundingClientRect();
          return r.top + scrollY - bar - Math.max(0, (innerHeight - bar - r.height) / 2); }""",
        bar,
    )
    current = page.evaluate("scrollY")
    for i in range(1, 5):
        page.evaluate(f"window.scrollTo(0, {current + (y - current) * i / 4})")
        page.wait_for_timeout(60)
    t = 0
    for frame, at in (("early", 900), ("mid", 2200), ("lit", 8000)):
        page.wait_for_timeout(at - t)
        t = at
        page.screenshot(path=str(OUT / f"{idea}-{w}-{frame}.png"))
    head = page.evaluate(f"document.querySelector('#health').getBoundingClientRect().top + scrollY - {bar}")
    page.evaluate(f"window.scrollTo(0, {head})")
    page.wait_for_timeout(1200)
    page.screenshot(path=str(OUT / f"{idea}-{w}-head.png"))
    print(idea, w, "done", flush=True)
    ctx.close()


if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for idea in IDEAS:
            for w, h in SIZES:
                film(browser, idea, w, h)
        browser.close()

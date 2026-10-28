"""Shoot the California opening ideas on the real homepage (October 28, 2026).

Each idea swaps the live opening's landscape (and, with a crane take, its crane) for the cut
mockup pictures by script and CSS; the sun, the words, the brush line and the layout stay the
live page's own. Nothing in src/ changes.

    python -X utf8 reference/ink-pages/home-california/shoot_california.py [base-url] [idea ...]

Ideas are keys of IDEAS ("now" is the live opening, unchanged). Pictures come from
cut_california.py (plates/img/); shots go to plates/shots/ (both git-ignored).
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
IMG = HERE / "plates" / "img"
SHOTS = HERE / "plates" / "shots"

# idea -> (landscape take, crane take); None keeps the live one.
IDEAS = {
    "now": (None, None),
    "a1": ("big-sur-1", "sandhill-crane-1"),
    "a2": ("big-sur-2", "sandhill-crane-1"),
    "b1": ("golden-hills-1", "sandhill-crane-1"),
    "b2": ("golden-hills-2", "sandhill-crane-1"),
    "c1": ("yosemite-1", "sandhill-crane-1"),
    "c2": ("yosemite-2", "sandhill-crane-1"),
}

SIZES = [("wide", 1920, 1040), ("desk", 1440, 900), ("phone", 390, 844)]

# Per idea: extra CSS. A's sun sets: it comes down until its foot dips just under the sea's
# horizon (measured for the two desktop sizes shot: the horizon is 26% down the cut painting);
# on a phone it moves over its path of light on the water (the phone shows the painting at 175%
# of the window, 55% off its left edge).
SUNSET = """
@media (min-width: 721px) and (max-width: 1699px) { section#top span[class*='__sun'] { top: 21.3% !important; } }
@media (min-width: 1700px) { section#top span[class*='__sun'] { top: 14.3% !important; } }
@media (max-width: 720px) { section#top span[class*='__sun'] { left: 52% !important; } }
"""
EXTRA = {"a1": SUNSET, "a2": SUNSET}

# The mist canvas and the wingbeat would draw the live pictures: off, and the stills shown. The
# page's brush line is routed for the live mountains (it would cut across El Capitan), so the
# mockups leave it out; a build would draw it again for the chosen scene.
CSS = """
[data-brush-layer] { display: none !important; }
section#top canvas { display: none !important; }
section#top img[class*="__landscape"] { visibility: visible !important; }
section#top img[class*="__wingbeat"] { display: none !important; }
section#top img[class*="__bird"] { visibility: visible !important; }
"""


def serve(route):
    name = route.request.url.split("/__mock/")[1].split("?")[0]
    route.fulfill(path=str(IMG / name), content_type="image/png")


def dress(page, land, bird, extra=""):
    page.add_style_tag(content=CSS + extra)
    page.evaluate(
        """([land, bird]) => {
          const swap = (sel, src) => {
            const img = document.querySelector(sel);
            if (!img || !src) return;
            img.removeAttribute('srcset');
            img.removeAttribute('sizes');
            img.src = src;
          };
          swap('section#top img[class*="__landscape"]', land && `/__mock/${land}.png`);
          swap('section#top img[class*="__bird"]', bird && `/__mock/${bird}.png`);
        }""",
        [land, bird],
    )
    page.evaluate(
        """() => Promise.all([...document.images].filter(i => i.src.includes('__mock'))
             .map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })))"""
    )
    page.wait_for_timeout(500)


def main():
    args = sys.argv[1:]
    base = next((a.rstrip("/") for a in args if "://" in a), "https://bigh-website-demo.vercel.app")
    picks = [a for a in args if "://" not in a] or list(IDEAS)
    SHOTS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for key in picks:
            land, bird = IDEAS[key]
            for size, w, h in SIZES:
                phone = size == "phone"
                ctx = browser.new_context(
                    viewport={"width": w, "height": h},
                    device_scale_factor=2 if phone else 1,
                    reduced_motion="reduce",
                    is_mobile=phone,
                    has_touch=phone,
                )
                page = ctx.new_page()
                page.route("**/__mock/**", serve)
                page.goto(f"{base}/", wait_until="networkidle")
                page.evaluate("document.fonts.ready")
                if key != "now":
                    dress(page, land, bird, EXTRA.get(key, ""))
                page.screenshot(path=str(SHOTS / f"{key}-{size}.png"))
                print(key, size, "ok")
                ctx.close()
        browser.close()


if __name__ == "__main__":
    main()

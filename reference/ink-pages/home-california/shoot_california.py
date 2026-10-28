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
    "d1": ("sequoia-1", "sandhill-crane-1"),
    "d2": ("sequoia-2", "sandhill-crane-1"),
    "d3": ("sequoia-3", "sandhill-crane-1"),
    "d2line": ("sequoia-2", "sandhill-crane-1"),
    # D round 2: the clearing, with the sandhill crane (g), the hummingbird (e) or the eagle (f).
    "g1": ("sequoia-2-clear-1", "sandhill-crane-1"),
    "g2": ("sequoia-2-clear-2", "sandhill-crane-1"),
    "e1": ("sequoia-2-clear-1", "hummingbird-1"),
    "e2": ("sequoia-2-clear-1", "hummingbird-2"),
    "f1": ("sequoia-2-clear-1", "golden-eagle-1"),
    "f2": ("sequoia-2-clear-1", "golden-eagle-2"),
    # Mo picked the hummingbird: its wings repainted narrow and blurred (h1, h2 edit
    # hummingbird-1; h3 is painted again over the crane's original).
    "h1": ("sequoia-2-clear-1", "hummingbird-wings-1"),
    "h2": ("sequoia-2-clear-1", "hummingbird-wings-2"),
    "h3": ("sequoia-2-clear-1", "hummingbird-3"),
}
LINE = {"d2line", "g1", "g2", "e1", "e2", "f1", "f2", "h1", "h2", "h3"}

# D is painted as the whole first screen (the trunks rise out of its top): its picture fills the
# opening, its foot dissolving; on a phone the whole painting shows at the painting's height, its
# right two-thirds in the window, so the grove stays in.
# The trunks' tops dissolve into the morning light, so the menu's words never sit on bark. Codex
# put a far trunk at 71-76% across, where the sun was asked to go, so the sun moves left into the
# open haze between the crane and the grove (53% at 1440; at most 833 px in from the column's
# start, so at 1920 its right edge stays at the far trunk's left, 1363 px). On a phone it moves
# left and shrinks a little, and the crane comes down a little, to fit between them.
FULL = """
@media (min-width: 721px) {
  section#top img[class*="__landscape"] { top: 0 !important; height: 100% !important;
    object-position: 62% 100% !important;
    -webkit-mask-image: linear-gradient(to bottom, transparent 0, #000 22%, #000 84%, transparent) !important;
    mask-image: linear-gradient(to bottom, transparent 0, #000 22%, #000 84%, transparent) !important; }
  section#top span[class*='__sun'] { left: calc(var(--inset) + min(53%, 833px)) !important; }
}
@media (max-width: 720px) {
  section#top img[class*="__landscape"] { top: 0 !important; bottom: auto !important;
    height: 100% !important; left: -48% !important; width: 150% !important; object-position: 100% 100% !important;
    -webkit-mask-image: linear-gradient(to bottom, transparent 0, #000 14%, #000 80%, transparent) !important;
    mask-image: linear-gradient(to bottom, transparent 0, #000 14%, #000 80%, transparent) !important; }
  section#top span[class*='__sun'] { left: 34vw !important; top: 2% !important; width: 24vw !important; }
  section#top span[class*='__crane'] { top: calc(4% + 24vw) !important; }
}
"""

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
# D round 2: the clearing (sequoia-2-clear-*) lets the sun go home: its own place at 1440, held
# at most 1000 px in from the column's start on wider windows so it stays in the clearing (60-78%
# across at 1440, 64-80% at 1920; the giant's trunk starts at 84%). On a phone it moves only to
# the clearing's middle, at its own size.
FULL2 = FULL.replace(
    "left: calc(var(--inset) + min(53%, 833px)) !important;",
    "left: calc(var(--inset) + min(60%, 1000px)) !important;",
).replace(
    "left: 34vw !important; top: 2% !important; width: 24vw !important;",
    "left: 50vw !important;",
)
EXTRA = {"a1": SUNSET, "a2": SUNSET, "d1": FULL, "d2": FULL, "d3": FULL, "d2line": FULL}
for key in ("e1", "e2", "f1", "f2", "g1", "g2", "h1", "h2", "h3"):
    EXTRA[key] = FULL2

# The mist canvas and the wingbeat would draw the live pictures: off, and the stills shown. The
# page's brush line is routed for the live mountains (it would cut across El Capitan), so A to D
# leave it out; the bird ideas (Mo likes the stroke that goes down) keep it, as routed now.
NO_LINE = "[data-brush-layer] { display: none !important; }"
CSS = """
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
                    line = "" if key in LINE else NO_LINE
                    dress(page, land, bird, EXTRA.get(key, "") + line)
                page.screenshot(path=str(SHOTS / f"{key}-{size}.png"))
                print(key, size, "ok")
                ctx.close()
        browser.close()


if __name__ == "__main__":
    main()

"""Shoot the About opening ideas on the real page (October 27, 2026).

Mo found the opening's big ink circle scary ("the movie The Ring") and asked for new concepts:
A a poppy superbloom, B a morning walk, C the name painted (B, i, G, H brushed as the title's
capitals). Each is laid over the live About page by injected CSS; nothing in src/ changes.

    python -X utf8 reference/ink-pages/about-opening/shoot_mockups.py [base-url] [concept=take ...]

Defaults: the public demo, and every take in TAKES. Pictures come from cut_mockups.py
(plates/img/); shots go to plates/shots/ (both git-ignored).
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
IMG = HERE / "plates" / "img"
SHOTS = HERE / "plates" / "shots"

TAKES = {
    "a1": "superbloom-a1",
    "a2": "superbloom-a2",
    "b1": "walk-b1",
    "b2": "walk-b2",
    "c": None,
}

SIZES = [("desk", 1440, 900), ("wide", 1920, 1000), ("phone", 390, 844)]

OPENING = 'section[data-part="opening"]'

# Where a take's picture is framed on a phone (object-position x): B1's walker stands at 38%.
PHONE_X = {"walk-b1": "33%"}

# Common: the circle goes.
BASE_CSS = f"""
{OPENING} [data-enso] {{ display: none !important; }}
"""

# A and B: one landscape fills the first screen, its sky holds the words.
SCENE_CSS = f"""
{OPENING} {{ position: relative; min-height: 100svh; padding-top: 0 !important;
  padding-bottom: 0 !important; display: block !important; overflow: clip; }}
{OPENING} img[data-picture-band] {{ display: none !important; }}
.mock-scene {{ position: absolute; inset: 0; z-index: 0; pointer-events: none; }}
.mock-scene img {{ width: 100%; height: 100%; object-fit: cover; object-position: 50% 30%;
  -webkit-mask-image: linear-gradient(to bottom, #000 86%, transparent);
  mask-image: linear-gradient(to bottom, #000 86%, transparent); }}
{OPENING} > div[class*="openingWords"] {{ position: relative; z-index: 1; grid-template-rows: auto auto auto !important;
  padding-top: calc(88px + 7vh); }}
{OPENING} h1 {{ max-width: none !important; font-size: clamp(44px, 5vw, 80px) !important;
  translate: none !important; }}
{OPENING} > div[class*="openingWords"] > p {{ translate: none !important; }}
{OPENING} > div[class*="openingWords"] > p:last-child {{ grid-area: 3 / 1 !important; }}
@media (max-width: 599px) {{
  {OPENING} > div[class*="openingWords"] {{ padding-top: calc(88px + 4vh); margin-block: 0 !important; }}
  {OPENING} h1 {{ max-width: 6em !important; font-size: 40px !important; }}
}}
"""

# C: the title's four capitals brushed (the October 6 letter paintings); the hills stay.
NAME_CSS = f"""
{OPENING} {{ display: flex !important; flex-direction: column; min-height: 100svh;
  padding-bottom: 0 !important; }}
{OPENING} > div[class*="openingWords"] {{ flex: 1 0 auto; grid-template-rows: auto auto auto !important;
  align-content: center; margin-block: 0 !important; }}
{OPENING} img[data-picture-band] {{ margin-top: 0 !important; }}
{OPENING} h1 {{ max-width: none !important; font-size: clamp(56px, 6.6vw, 112px) !important;
  translate: none !important; line-height: 1.25 !important; margin-block: 0.15em 0.25em; }}
{OPENING} > div[class*="openingWords"] > p {{ translate: none !important; }}
{OPENING} > div[class*="openingWords"] > p:last-child {{ grid-area: 3 / 1 !important; }}
{OPENING} h1 .w {{ white-space: nowrap; }}
{OPENING} h1 {{ width: max-content; }}
{OPENING} h1 img.cap {{ display: inline-block; height: 1.18em; width: auto; vertical-align: -0.2em;
  margin-right: -0.03em; }}
{OPENING} h1 img.cap.i {{ margin-left: 0.02em; }}
{OPENING} h1 img.cap.h {{ margin-right: -0.13em; }}
@media (max-width: 599px) {{
  {OPENING} h1 {{ max-width: 4.6em !important; font-size: 52px !important; line-height: 1.3 !important; }}
}}
"""

NAME_HTML = (
    '<span class="w"><img class="cap" src="/__mock/letter-b.png" alt="">e</span> '
    '<span class="w"><img class="cap i" src="/__mock/letter-i.png" alt="">n</span> '
    '<span class="w"><img class="cap" src="/__mock/letter-g.png" alt="">ood</span> '
    '<span class="w"><img class="cap h" src="/__mock/letter-h.png" alt="">ealth.</span>'
)


def serve(route):
    name = route.request.url.split("/__mock/")[1].split("?")[0]
    route.fulfill(path=str(IMG / name), content_type="image/png")


def dress(page, take):
    if take:
        page.add_style_tag(content=BASE_CSS + SCENE_CSS)
        if take in PHONE_X:
            page.add_style_tag(
                content=f"@media (max-width: 599px) {{ .mock-scene img {{ object-position: {PHONE_X[take]} 30%; }} }}"
            )
        page.evaluate(
            """(src) => {
              const s = document.querySelector('section[data-part="opening"]');
              const d = document.createElement('div');
              d.className = 'mock-scene';
              d.innerHTML = `<img src="${src}" alt="">`;
              s.prepend(d);
            }""",
            f"/__mock/{take}.png",
        )
    else:
        page.add_style_tag(content=BASE_CSS + NAME_CSS)
        page.evaluate(
            """(html) => { document.querySelector('#about-title').innerHTML = html; }""",
            NAME_HTML,
        )
    page.evaluate(
        """() => Promise.all([...document.images].filter(i => i.src.includes('__mock'))
             .map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })))"""
    )
    page.wait_for_timeout(400)


def main():
    base = sys.argv[1].rstrip("/") if len(sys.argv) > 1 and "://" in sys.argv[1] else "https://bigh-website-demo.vercel.app"
    picks = [a for a in sys.argv[1:] if "://" not in a] or list(TAKES)
    SHOTS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for key in picks:
            take = TAKES[key]
            for size, w, h in SIZES:
                ctx = browser.new_context(
                    viewport={"width": w, "height": h},
                    device_scale_factor=2 if size == "phone" else 1,
                    reduced_motion="reduce",
                    is_mobile=size == "phone",
                    has_touch=size == "phone",
                )
                page = ctx.new_page()
                page.route("**/__mock/**", serve)
                page.goto(f"{base}/about", wait_until="networkidle")
                page.evaluate("document.fonts.ready")
                dress(page, take)
                page.screenshot(path=str(SHOTS / f"{key}-{size}.png"))
                # Scrolled like a visitor: the opening's foot meeting the purpose's oak.
                page.mouse.wheel(0, int(h * 0.7))
                page.wait_for_timeout(900)
                page.screenshot(path=str(SHOTS / f"{key}-{size}-scrolled.png"))
                print(key, size, "ok")
                ctx.close()
        browser.close()


if __name__ == "__main__":
    main()

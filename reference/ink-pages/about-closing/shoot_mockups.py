"""Shoot the About "Curious about the science?" ideas on the real page (November 13, 2026).

Mo asked for About's last three parts to take the site's California colour, one part at a time;
Our experience (the sequoia, a little coloured) and Our promise (the dots in colour) went live,
this is the third: the grey ink reading glasses on an open notebook beside "Curious about the
science?". Each idea's painting is swapped in for the glasses on the live About page by injected
script and CSS; nothing in src/ changes.

    python -X utf8 reference/ink-pages/about-closing/shoot_mockups.py [base-url] [key=take@height ...]

`height` is the painting's height as a multiple of the page's plain height --h (the glasses are
0.72, the sequoia 1.35; circle.module.css). Defaults: the public demo, and TAKES. Pictures come
from cut_closing.py (plates/img/); shots go to plates/shots/ (both git-ignored).
"""

import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
IMG = HERE / "plates" / "img"
SHOTS = HERE / "plates" / "shots"

# key -> (take, height as a multiple of --h)
TAKES = {
    "today": (None, 0.72),
    "a": ("glasses-colour-1", 0.72),
    "b": ("tidepool-1", 1.0),
    "c": ("notebook-1", 1.0),
}

SIZES = [("desk", 1440, 900, 1), ("tablet", 768, 1024, 1), ("phone", 390, 844, 2)]

SWAP = """([take, w, h, mult]) => {
  const img = document.querySelector('[data-part="closing"] [data-picture] img');
  const style = document.createElement('style');
  style.textContent = `[data-part="closing"] [data-picture] { --picture: calc(var(--h) * ${mult} * ${(w / h).toFixed(3)}) !important; }`;
  document.head.append(style);
  return new Promise((done) => {
    img.loading = 'eager';
    img.removeAttribute('srcset');
    img.removeAttribute('sizes');
    img.setAttribute('width', w);
    img.setAttribute('height', h);
    img.removeAttribute('data-bloom');
    img.src = `/__mock/${take}.png`;
    if (img.complete && img.naturalWidth) done(true);
    else { img.onload = () => done(true); img.onerror = () => done(false); }
    setTimeout(() => done(false), 20000);
  });
}"""

# The part in the middle of the window (a part taller than the window starts under the menu bar).
CENTRE = """() => {
  const r = document.querySelector('[data-part="closing"]').getBoundingClientRect();
  const y = r.top + scrollY;
  const bar = document.querySelector('header')?.getBoundingClientRect().bottom ?? 0;
  scrollTo(0, Math.max(0, r.height < innerHeight - bar ? y - bar - (innerHeight - bar - r.height) / 2 : y - bar));
}"""

# Scrolled like a visitor: the promises above going out, the closing coming up.
ARRIVE = """() => {
  const r = document.querySelector('[data-part="closing"]').getBoundingClientRect();
  scrollTo(0, Math.max(0, r.top + scrollY - innerHeight * 0.5));
}"""


def serve(route):
    name = route.request.url.split("/__mock/")[1].split("?")[0]
    route.fulfill(path=str(IMG / name), content_type="image/png")


def main():
    args = sys.argv[1:]
    base = next((a for a in args if "://" in a), "https://bigh-website-demo.vercel.app").rstrip("/")
    takes = dict(TAKES)
    picks = []
    for a in args:
        if "://" in a:
            continue
        key, _, rest = a.partition("=")
        if rest:
            take, _, mult = rest.partition("@")
            takes[key] = (take, float(mult or 1.0))
        picks.append(key)
    picks = picks or list(takes)
    SHOTS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for key in picks:
            take, mult = takes[key]
            size_of = Image.open(IMG / f"{take}.png").size if take else None
            for size, vw, vh, dpr in SIZES:
                ctx = browser.new_context(
                    viewport={"width": vw, "height": vh},
                    device_scale_factor=dpr,
                    reduced_motion="reduce",
                    is_mobile=dpr == 2,
                    has_touch=dpr == 2,
                )
                page = ctx.new_page()
                page.route("**/__mock/**", serve)
                page.goto(f"{base}/about", wait_until="networkidle")
                page.evaluate("document.fonts.ready")
                page.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
                if take and not page.evaluate(SWAP, [take, size_of[0], size_of[1], mult]):
                    print("FAIL picture did not load", key, size)
                page.evaluate(CENTRE)
                page.wait_for_timeout(1200)
                box = page.evaluate("(() => { const r = document.querySelector('[data-part=\"closing\"] [data-picture] img').getBoundingClientRect(); return [Math.round(r.width), Math.round(r.height)]; })()")
                page.screenshot(path=str(SHOTS / f"{key}-{take}-{size}.png"))
                page.evaluate(ARRIVE)
                page.wait_for_timeout(900)
                page.screenshot(path=str(SHOTS / f"{key}-{take}-{size}-arrive.png"))
                print(key, take, size, "painting", box)
                ctx.close()
        browser.close()


if __name__ == "__main__":
    main()

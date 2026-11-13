"""Shoot the About "Our promise" ideas on the real page (November 12, 2026).

Mo asked for About's last three parts to take the site's California colour, one part at a time;
Our experience (the sequoia, a little coloured) went live, Our promise is next: its four grey ink
dots over the four promises. Each idea's four small paintings are swapped in for the dots on the
live About page by injected script and CSS; nothing in src/ changes.

    python -X utf8 reference/ink-pages/about-promise/shoot_mockups.py [base-url] [key=take@px ...]

Defaults: the public demo, and TAKES. Pictures come from cut_promise.py (plates/img/); shots go to
plates/shots/ (both git-ignored).
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
IMG = HERE / "plates" / "img"
SHOTS = HERE / "plates" / "shots"

# key -> (take, the pictures' size at 1440px; the dots are clamp(64px, 5.6vw, 92px))
TAKES = {
    "today": (None, 92),
    "a": ("dots-colour-1", 92),
    "b": ("wildflowers-1", 112),
    "c": ("poppy-count-1", 120),
}

SIZES = [("desk", 1440, 900), ("tablet", 768, 1024), ("phone", 390, 844)]

SWAP = """([take, px, phone]) => {
  const imgs = [...document.querySelectorAll('[data-part="promise"] [data-promise] > img')];
  // A size like the dots' own clamp, scaled to this idea's size at 1440px; phones keep a row picture.
  const style = document.createElement('style');
  style.textContent = `
    [data-part="promise"] [data-promise] > img { width: clamp(${Math.round(px * 0.7)}px, ${(px / 14.4).toFixed(2)}vw, ${px}px) !important; }
    @media (max-width: 599px) {
      [data-part="promise"] [data-promise] { --row-picture: ${phone}px !important; }
      [data-part="promise"] [data-promise] > img { width: 100% !important; }
    }`;
  document.head.append(style);
  return Promise.all(imgs.map((img, i) => new Promise((done) => {
    img.loading = 'eager';
    img.removeAttribute('srcset');
    img.removeAttribute('sizes');
    img.src = `/__mock/${take}-${i + 1}.png`;
    img.removeAttribute('data-bloom');
    if (img.complete && img.naturalWidth) done(true);
    else { img.onload = () => done(true); img.onerror = () => done(false); }
    setTimeout(() => done(false), 20000);
  }))).then((all) => all.every(Boolean));
}"""

# The part in the middle of the window (a part taller than the window starts under the menu bar).
CENTRE = """() => {
  const r = document.querySelector('[data-part="promise"]').getBoundingClientRect();
  const y = r.top + scrollY;
  const bar = document.querySelector('header')?.getBoundingClientRect().bottom ?? 0;
  scrollTo(0, Math.max(0, r.height < innerHeight - bar ? y - bar - (innerHeight - bar - r.height) / 2 : y - bar));
}"""

# Scrolled like a visitor: the sequoia above going out, the promises coming up.
ARRIVE = """() => {
  const r = document.querySelector('[data-part="promise"]').getBoundingClientRect();
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
    sizes = SIZES
    for a in args:
        if "://" in a:
            continue
        if a.startswith("sizes="):
            only = a[6:].split(",")
            sizes = [s for s in SIZES if s[0] in only]
            continue
        key, _, rest = a.partition("=")
        if rest:
            take, _, px = rest.partition("@")
            px, _, phone = (px or "92").partition("/")
            takes[key] = (take, int(px), int(phone) if phone else None)
        picks.append(key)
    picks = picks or list(takes)
    SHOTS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for key in picks:
            take, px, *rest = takes[key]
            phone = (rest[0] if rest else None) or round(px * 0.78)
            for size, vw, vh in sizes:
                ctx = browser.new_context(
                    viewport={"width": vw, "height": vh},
                    device_scale_factor=2 if size == "phone" else 1,
                    reduced_motion="reduce",
                    is_mobile=size == "phone",
                    has_touch=size == "phone",
                )
                page = ctx.new_page()
                page.route("**/__mock/**", serve)
                page.goto(f"{base}/about", wait_until="networkidle")
                page.evaluate("document.fonts.ready")
                if take and not page.evaluate(SWAP, [take, px, phone]):
                    print("FAIL pictures did not load", key, size)
                page.evaluate(CENTRE)
                page.wait_for_timeout(900)
                page.screenshot(path=str(SHOTS / f"{key}-{take}-{size}.png"))
                page.evaluate(ARRIVE)
                page.wait_for_timeout(900)
                page.screenshot(path=str(SHOTS / f"{key}-{take}-{size}-arrive.png"))
                print(key, take, size, "ok")
                ctx.close()
        browser.close()


if __name__ == "__main__":
    main()

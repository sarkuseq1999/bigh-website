"""Shoot the About "Our purpose" ideas on the real page (November 10, 2026).

Mo found the purpose's oak "a little dark or scary" (black ink, bare roots hanging in empty paper,
an empty swing) and asked for ideas that fit the page's sunny, soft-colour paintings. Three:
A the same oak on a sunny afternoon (the swing in use, the roots inside warm earth), B Monterey
Bay above and below the water (a golden kelp forest under a sea otter), C a San Francisco cable
car and the gold cable under its street. Each painting is swapped in for the oak on the live
About page by injected script and CSS; nothing in src/ changes.

    python -X utf8 reference/ink-pages/about-purpose/shoot_mockups.py [base-url] [key=take ...]

Defaults: the public demo, and TAKES. Pictures come from cut_mockups.py (plates/img/); shots go to
plates/shots/ (both git-ignored).
"""

import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
IMG = HERE / "plates" / "img"
SHOTS = HERE / "plates" / "shots"

# key -> (take, how many plain heights tall the painting stands; the oak it replaces is 1.72)
TAKES = {
    "today": (None, 1.72),  # the page as it is, for the comparison
    "a": ("oak-1-b", 1.72),
    "b": ("bay-1-b", 1.72),
    "c": ("cable-2-b", 1.72),
}

SIZES = [("desk", 1440, 900), ("wide", 1920, 1000), ("phone", 390, 844)]

SWAP = """([src, w, h, tall]) => {
  const fig = document.querySelector('[data-part="purpose"] [data-picture]');
  const img = fig.querySelector('img');
  img.removeAttribute('srcset');
  img.removeAttribute('sizes');
  img.setAttribute('width', w);
  img.setAttribute('height', h);
  img.src = src;
  img.style.aspectRatio = `${w} / ${h}`;
  // The oak's gold-leaf light mask belongs to the oak.
  for (const gold of fig.querySelectorAll('span > span')) gold.style.display = 'none';
  fig.style.setProperty('--picture', `calc(var(--h) * ${tall} * ${w / h})`);
  return new Promise((done) => {
    if (img.complete && img.naturalWidth) done(true);
    else { img.onload = () => done(true); img.onerror = () => done(false); }
  });
}"""

CENTRE = """() => {
  const r = document.querySelector('[data-part="purpose"]').getBoundingClientRect();
  const y = r.top + scrollY;
  scrollTo(0, Math.max(0, r.height < innerHeight ? y - (innerHeight - r.height) / 2 : y));
}"""

# Scrolled like a visitor: the meadow's last poppies above, the painting coming up.
ARRIVE = """() => {
  const r = document.querySelector('[data-part="purpose"]').getBoundingClientRect();
  scrollTo(0, Math.max(0, r.top + scrollY - innerHeight * 0.42));
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
            take, _, tall = rest.partition("@")
            takes[key] = (take, float(tall) if tall else 1.72)
        picks.append(key)
    picks = picks or list(takes)
    SHOTS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for key in picks:
            take, tall = takes[key]
            w, h = Image.open(IMG / f"{take}.png").size if take else (0, 0)
            for size, vw, vh in SIZES:
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
                if take and not page.evaluate(SWAP, [f"/__mock/{take}.png", w, h, tall]):
                    print("FAIL picture did not load", key, size)
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

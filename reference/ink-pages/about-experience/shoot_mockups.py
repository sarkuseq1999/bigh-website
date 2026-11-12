"""Shoot the About "Our experience" ideas on the real page (November 11, 2026).

Mo asked for the About page's last three parts to match the site's newer California look, more
colour, one part at a time, starting with "Our experience" (the grey ink giant sequoia beside a
young one, which also repeats the homepage opening's sequoias). Each idea's painting is swapped in
for the sequoia on the live About page by injected script and CSS; nothing in src/ changes. An
idea may carry one short line under its painting (new words, marked as such for Mo).

    python -X utf8 reference/ink-pages/about-experience/shoot_mockups.py [base-url] [key=take ...]

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

# key -> (take, how many plain heights tall the painting stands; the sequoia it replaces is 1.35)
TAKES = {
    "today": (None, 1.35),  # the page as it is, for the comparison
    "a": ("orchard-1-a", 1.35),
    "b": ("sourdough-1-a", 1.35),
    "c": ("carousel-1-a", 1.35),
}

# One short line under the painting (new words; Mo has not seen them).
NOTES = {
    # California State Parks, landmark 20: two young navel trees sent to Riverside in 1873; one
    # still stands (kept alive by inarching, 1918 and 1951) and bears fruit.
    "a": "Riverside’s parent navel orange tree was planted in 1873. The groves came after it, and it still bears fruit.",
    "b": "One San Francisco bakery says it still bakes every loaf from the starter it began in 1849.",
}

SIZES = [("desk", 1440, 900), ("wide", 1920, 1000), ("phone", 390, 844)]

SWAP = """([src, w, h, tall, note]) => {
  const fig = document.querySelector('[data-part="experience"] [data-picture]');
  const img = fig.querySelector('img');
  // The painting sits far down the page and is lazy: it would never load off screen.
  img.loading = 'eager';
  img.removeAttribute('srcset');
  img.removeAttribute('sizes');
  img.setAttribute('width', w);
  img.setAttribute('height', h);
  img.src = src;
  img.style.aspectRatio = `${w} / ${h}`;
  // The sequoia's gold-leaf light mask belongs to the sequoia.
  for (const gold of fig.querySelectorAll('span > span')) gold.style.display = 'none';
  fig.style.setProperty('--picture', `calc(var(--h) * ${tall} * ${w / h})`);
  if (note) {
    const p = document.createElement('p');
    p.textContent = note;
    p.setAttribute('data-mock-note', '');
    Object.assign(p.style, {
      margin: '6px 0 0', color: 'var(--muted)', fontSize: '15px', fontWeight: '450',
      lineHeight: '1.45', textAlign: 'left', maxWidth: '34em',
    });
    fig.querySelector('figcaption').before(p);
  }
  return new Promise((done) => {
    if (img.complete && img.naturalWidth) done(true);
    else { img.onload = () => done(true); img.onerror = () => done(false); }
    setTimeout(() => done(false), 20000);
  });
}"""

# A part taller than the window starts just under the sticky menu bar (its top was hidden under it).
CENTRE = """() => {
  const r = document.querySelector('[data-part="experience"]').getBoundingClientRect();
  const y = r.top + scrollY;
  const bar = document.querySelector('header')?.getBoundingClientRect().bottom ?? 0;
  scrollTo(0, Math.max(0, r.height < innerHeight ? y - (innerHeight - r.height) / 2 : y - bar));
}"""

# Scrolled like a visitor: the valley at dawn above, the painting coming up.
ARRIVE = """() => {
  const r = document.querySelector('[data-part="experience"]').getBoundingClientRect();
  scrollTo(0, Math.max(0, r.top + scrollY - innerHeight * 0.45));
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
            take, _, tall = rest.partition("@")
            takes[key] = (take, float(tall) if tall else 1.35)
        picks.append(key)
    picks = picks or list(takes)
    SHOTS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for key in picks:
            take, tall = takes[key]
            w, h = Image.open(IMG / f"{take}.png").size if take else (0, 0)
            note = NOTES.get(key[0], "")
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
                if take and not page.evaluate(SWAP, [f"/__mock/{take}.png", w, h, tall, note]):
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

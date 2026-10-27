"""NuriCell How-to-take-it, idea A ("brush the habit, not the math"), injected into the running page
(nothing in the repo changes). Shoots the current chapter and the mockup at desktop and phone sizes.

usage: python -X utf8 mock_daily.py <base-url> <out-dir> [caps-a|caps-b]
"""

import base64
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE, OUT = sys.argv[1], Path(sys.argv[2])
CAPS = sys.argv[3] if len(sys.argv) > 3 else "caps-b"
HERE = Path(__file__).resolve().parent
OUT.mkdir(parents=True, exist_ok=True)


def data_url(name):
    return "data:image/png;base64," + base64.b64encode((HERE / name).read_bytes()).decode()


CSS = """
[data-chapter="daily"] .mockDaily {
  display: grid !important;
  grid-template-columns: 1fr !important;
  justify-items: center;
  text-align: center;
}
[data-chapter="daily"] .mockDaily .mockHead { display: grid; justify-items: center; }
[data-chapter="daily"] .mockDaily .mockHead p { margin: 0 0 0.35em; }
[data-chapter="daily"] .mockDaily .mockHead h2 { margin: 0; }

/* The lockup: the brushed 3 tall on the left; the habit and the painted capsules to its right. */
[data-chapter="daily"] .mockHabit {
  display: grid;
  grid-template-columns: auto auto;
  grid-template-rows: auto auto;
  column-gap: clamp(20px, 3vw, 48px);
  align-items: center;
  margin-top: clamp(40px, 5vw, 72px);
  text-align: left;
}
[data-chapter="daily"] .mockThree {
  grid-column: 1; grid-row: 1 / span 2;
  height: clamp(150px, 24vw, 340px); width: auto;
  align-self: center;
}
[data-chapter="daily"] .mockLines {
  grid-column: 2; grid-row: 1; align-self: end;
  margin: 0;
  font-size: clamp(23px, 3vw, 42px);
  line-height: 1.18;
  letter-spacing: -0.02em;
  font-weight: 450;
  color: rgb(12, 11, 10);
}
[data-chapter="daily"] .mockLines span { display: block; }
[data-chapter="daily"] .mockCapsFig {
  grid-column: 2; grid-row: 2; align-self: start;
  margin: clamp(10px, 1.4vw, 22px) 0 0;
  width: clamp(200px, 32vw, 460px);
}
[data-chapter="daily"] .mockCapsFig img { display: block; width: 100%; height: auto; }
[data-chapter="daily"] .mockCapsFig figcaption {
  margin-top: 4px; text-align: right;
  font-size: 13px; color: rgb(81, 78, 72);
}
[data-chapter="daily"] .mockNote {
  margin: clamp(28px, 3.5vw, 52px) 0 0;
  font-size: 20px; line-height: 1.6; color: rgb(81, 78, 72);
}

@media (max-width: 599px) {
  [data-chapter="daily"] .mockDaily { justify-items: start; text-align: left; }
  [data-chapter="daily"] .mockDaily .mockHead { justify-items: start; }
  [data-chapter="daily"] .mockHabit {
    grid-template-columns: auto 1fr;
    column-gap: 14px;
    width: 100%;
  }
  [data-chapter="daily"] .mockThree { grid-row: 1; height: 136px; margin-left: -10px; }
  [data-chapter="daily"] .mockLines { grid-row: 1; align-self: center; font-size: 22px; white-space: nowrap; }
  [data-chapter="daily"] .mockCapsFig { grid-column: 1 / -1; grid-row: 2; width: 100%; margin-top: 20px; }
  [data-chapter="daily"] .mockNote { font-size: 18px; margin-top: 24px; }
}
"""

JS = """([three, caps]) => {
  const c = document.querySelector('[data-chapter="daily"]');
  const wrap = c.querySelector(':scope > div');
  const label = c.querySelector('[data-words] > p').className;
  const h2 = c.querySelector('h2');
  const wrapClass = wrap.className.split(' ').filter(k => !/spread/.test(k)).join(' ');
  wrap.className = wrapClass + ' mockDaily';
  wrap.innerHTML = `
    <div class="mockHead">
      <p class="${label}">How to take it</p>
      <h2 id="${h2.id}" class="${h2.className}">One bottle, one month.</h2>
    </div>
    <div class="mockHabit">
      <img class="mockThree" src="${three}" alt="3">
      <p class="mockLines"><span>capsules</span><span>once a day</span><span>with or after a meal</span></p>
      <figure class="mockCapsFig">
        <img src="${caps}" alt="Three capsules, painted in ink">
        <figcaption>Illustration</figcaption>
      </figure>
    </div>
    <p class="mockNote">90 capsules in each bottle.</p>`;
}"""

SIZES = {"desktop": dict(width=1440, height=900, scale=1), "phone": dict(width=390, height=844, scale=2)}


def settle(page):
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(900)


def shoot_chapter(page, tag):
    """Viewport shots down the chapter, from its top under the menu bar, like a visitor scrolling."""
    top = page.evaluate(
        "() => document.querySelector('[data-chapter=\"daily\"]').getBoundingClientRect().top + scrollY"
    )
    height = page.evaluate("() => document.querySelector('[data-chapter=\"daily\"]').offsetHeight")
    vh = page.viewport_size["height"]
    shots, y, k = [], top - 40, 0
    while True:
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(3500)
        path = OUT / f"{tag}-{k}.png"
        page.screenshot(path=str(path))
        shots.append(path)
        k += 1
        if y + vh >= top + height + 40 or k >= 3:
            break
        y += vh - 120
    print(tag, "chapter height", height, "shots", len(shots))
    return shots


with sync_playwright() as p:
    browser = p.chromium.launch()
    for name, s in SIZES.items():
        ctx = browser.new_context(
            viewport={"width": s["width"], "height": s["height"]},
            device_scale_factor=s["scale"],
            is_mobile=name == "phone",
            has_touch=name == "phone",
        )
        page = ctx.new_page()
        page.goto(BASE + "/en/products/nuricell", wait_until="networkidle")
        settle(page)
        shoot_chapter(page, f"{name}-now")
        page.add_style_tag(content=CSS)
        page.evaluate(JS, [data_url("three.png"), data_url(f"{CAPS}.png")])
        settle(page)
        shoot_chapter(page, f"{name}-a")
        ctx.close()
    browser.close()

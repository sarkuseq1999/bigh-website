"""NuriCell How-to-take-it, round 2 ideas, injected into the running page (nothing in the repo changes).

  now  the live chapter
  d    a painted hand holding three capsules, its words beside it
  e    a painted month of ticks (the Questions' month painting), its words beside it
  e12  E while it fills in as you scroll (12 days ticked)
  f    the live egg painting, big, its words beside it; no painted numbers
  g    no chapter: Dr. Liu runs into the buy box, which already says how to take it

usage: python -X utf8 mock_ideas.py <base-url> <out-dir> <hand.png> <month-12.png> [variant ...]
"""

import base64
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE, OUT = sys.argv[1], Path(sys.argv[2])
HAND, MONTH12 = Path(sys.argv[3]), Path(sys.argv[4])
WANTED = sys.argv[5:] or ["now", "d", "e", "e12", "f", "g"]
OUT.mkdir(parents=True, exist_ok=True)


def data_url(path):
    kind = "png" if path.suffix == ".png" else "webp"
    return f"data:image/{kind};base64," + base64.b64encode(path.read_bytes()).decode()


INK, GREY = "rgb(12, 11, 10)", "rgb(81, 78, 72)"
CSS = f"""
[data-chapter="daily"] .mockPair {{
  display: grid !important;
  grid-template-columns: minmax(0, 5fr) minmax(0, 7fr) !important;
  column-gap: clamp(40px, 5vw, 96px);
  align-items: center !important;
}}
[data-chapter="daily"] .mockWords h2 {{ margin: 0; }}
[data-chapter="daily"] .mockLead {{
  margin: 0.55em 0 0; font-size: clamp(24px, 2.1vw, 31px); line-height: 1.3;
  font-weight: 450; letter-spacing: -0.01em; color: {INK};
}}
[data-chapter="daily"] .mockSmall {{ margin: 1.5em 0 0; font-size: 20px; line-height: 1.55; color: {GREY}; }}
[data-chapter="daily"] .mockFig {{ margin: 0; grid-row: 1 !important; grid-column: 2 !important; }}
[data-chapter="daily"] .mockWords {{ grid-row: 1; grid-column: 1; }}
[data-chapter="daily"] .mockFig img {{ display: block; width: 100%; height: auto; }}
[data-chapter="daily"] .mockFig img.mult {{ mix-blend-mode: multiply; }}
[data-chapter="daily"] .mockFig figcaption {{ margin-top: 6px; text-align: right; font-size: 13px; color: {GREY}; }}
[data-chapter="daily"] .mockPair.egg {{ grid-template-columns: minmax(0, 6fr) minmax(0, 5fr) !important; }}
[data-chapter="daily"] .mockPair.egg .mockFig {{ max-width: 520px; justify-self: center; width: 100%; }}

@media (max-width: 599px) {{
  [data-chapter="daily"] .mockPair, [data-chapter="daily"] .mockPair.egg {{
    grid-template-columns: 1fr !important; row-gap: 28px;
  }}
  [data-chapter="daily"] .mockFig {{ grid-row: auto !important; grid-column: 1 !important; }}
  [data-chapter="daily"] .mockWords {{ grid-row: auto; grid-column: 1; }}
  [data-chapter="daily"] .mockLead {{ font-size: 23px; }}
  [data-chapter="daily"] .mockSmall {{ font-size: 18px; margin-top: 0; }}
  [data-chapter="daily"] .mockPair.egg .mockFig {{ max-width: 300px; }}
}}
"""

WORDS = {
    "dose": ("Three capsules, once a day.", "With or after a meal.",
             "90 capsules in each bottle, so one bottle lasts a month."),
    "month": ("One bottle, one month.", "Take 3 capsules once a day, with or after a meal.",
              "90 capsules in each bottle."),
}

JS = """([words, src, mult, alt, extra]) => {
  const c = document.querySelector('[data-chapter="daily"]');
  const wrap = c.querySelector(':scope > div');
  const h2 = c.querySelector('h2');
  wrap.className = wrap.className.split(' ').filter(k => !/spread/.test(k)).join(' ') + ' mockPair ' + extra;
  const [title, lead, small] = words;
  wrap.innerHTML = `
    <div class="mockWords">
      <h2 id="${h2.id}" class="${h2.className}">${title}</h2>
      <p class="mockLead">${lead}</p>
    </div>
    <figure class="mockFig">
      <img class="${mult ? 'mult' : ''}" src="${src}" alt="${alt}">
      <figcaption>Illustration</figcaption>
    </figure>
    <p class="mockSmall">${small}</p>`;
  // The small line sits under the words on a laptop, under the picture on a phone.
  if (innerWidth >= 600) wrap.querySelector('.mockWords').append(wrap.querySelector('.mockSmall'));
}"""

SIZES = {"desktop": dict(width=1440, height=900, scale=1), "phone": dict(width=390, height=844, scale=2)}


def settle(page):
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(900)


def top_of(page, sel):
    return page.evaluate(f"() => document.querySelector('{sel}').getBoundingClientRect().top + scrollY")


def shoot(page, tag, start, end, most=3):
    """Viewport shots from start to end, like a visitor scrolling."""
    vh = page.viewport_size["height"]
    y, k = start, 0
    while True:
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(3500)
        page.screenshot(path=str(OUT / f"{tag}-{k}.png"))
        k += 1
        if y + vh >= end or k >= most:
            break
        y += vh - 120
    print(tag, "shots", k, flush=True)


def chapter_span(page):
    top = top_of(page, '[data-chapter="daily"]')
    h = page.evaluate("() => document.querySelector('[data-chapter=\"daily\"]').offsetHeight")
    return top - 40, top + h + 40


with sync_playwright() as p:
    browser = p.chromium.launch()
    for size, s in SIZES.items():
        ctx = browser.new_context(
            viewport={"width": s["width"], "height": s["height"]},
            device_scale_factor=s["scale"],
            is_mobile=size == "phone",
            has_touch=size == "phone",
        )
        for v in WANTED:
            page = ctx.new_page()
            page.goto(BASE + "/en/products/nuricell", wait_until="networkidle")
            settle(page)
            page.add_style_tag(content=CSS)
            if v in ("d", "e", "e12", "f"):
                if v == "d":
                    args = [WORDS["dose"], data_url(HAND), False, "A hand holding three capsules", ""]
                elif v == "f":
                    args = [WORDS["dose"], "/images/products/nuricell/ink/breakfast-v1.webp", True,
                            "A soft-boiled egg beside a dish of three capsules", "egg"]
                else:
                    src = data_url(MONTH12) if v == "e12" else "/images/products/nuricell/ink/q-month-v1.webp"
                    args = [WORDS["month"], src, True, "A month of days ticked off", ""]
                page.evaluate(JS, args)
                settle(page)
                start, end = chapter_span(page)
                shoot(page, f"{size}-{v}", start, end, most=1 if v == "e12" else 3)
            elif v == "g":
                page.evaluate("() => document.querySelector('[data-chapter=\"daily\"]').remove()")
                settle(page)
                buy = top_of(page, '[data-chapter="buy"]')
                q = top_of(page, "#questions")
                shoot(page, f"{size}-g", buy - (360 if size == "desktop" else 200), q + 700, most=4)
            else:
                start, end = chapter_span(page)
                shoot(page, f"{size}-now", start, end)
            page.close()
        ctx.close()
    browser.close()

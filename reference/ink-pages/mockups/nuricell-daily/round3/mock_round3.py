"""NuriCell daily chapter, round 3: new content in place of the dose, injected into the running page
(nothing in the repo changes).

  day    1  A good day for your cells: one painted California day, a line under each moment;
            on a phone the moments sit in a strip you swipe, the next one peeking in
  rings  2  The same formula for about 20 years: a redwood round with one ring in gold leaf

usage: python -X utf8 mock_round3.py <base-url> <out-dir> <plates-dir> [variant ...]
"""

import base64
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE, OUT, PLATES = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
WANTED = sys.argv[4:] or ["day", "rings"]
OUT.mkdir(parents=True, exist_ok=True)


def data_url(path):
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()


INK, GREY = "rgb(12, 11, 10)", "rgb(81, 78, 72)"
C = '[data-chapter="daily"]'
CSS = f"""
{C} .r3 h2 {{ margin: 0; }}
{C} .r3Lead {{
  margin: 0.55em 0 0; font-size: clamp(24px, 2.1vw, 31px); line-height: 1.3;
  font-weight: 450; letter-spacing: -0.01em; color: {INK}; max-width: 30em; text-wrap: pretty;
}}
{C} .r3Small {{ margin: 1.4em 0 0; font-size: 20px; line-height: 1.55; color: {GREY}; max-width: 30em; }}
{C} figure {{ margin: 0; }}
{C} img.mult {{ mix-blend-mode: multiply; display: block; }}
{C} figcaption {{ margin-top: 6px; text-align: right; font-size: 13px; color: {GREY}; }}

/* 1: the day */
{C} .r3.day {{ display: block !important; }}
{C} .day .r3Pano {{ margin-top: clamp(32px, 4vw, 56px); }}
{C} .day .r3Pano img {{ width: 100%; height: auto; }}
{C} .day .r3Moments {{
  list-style: none; margin: 20px 0 0; padding: 0;
  display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); column-gap: clamp(20px, 2.5vw, 40px);
}}
{C} .day .r3Moments li {{ font-size: 19px; line-height: 1.5; color: {GREY}; }}
{C} .day .r3Moments b {{ display: block; font-weight: 550; color: {INK}; font-size: 21px; margin-bottom: 4px; }}
{C} .day .r3Strip {{ display: none; }}
{C} .day .r3Src {{ margin: 28px 0 0; font-size: 14px; line-height: 1.5; color: {GREY}; }}

/* 2: the rings */
{C} .r3.rings {{
  display: grid !important; grid-template-columns: minmax(0, 6fr) minmax(0, 5fr) !important;
  column-gap: clamp(40px, 5vw, 96px); align-items: center !important;
}}
{C} .rings .r3Words {{ grid-row: 1; grid-column: 1; }}
{C} .rings .r3Log {{ grid-row: 1 !important; grid-column: 2 !important; max-width: 560px; width: 100%; justify-self: center; }}
{C} .rings .r3Log img {{ width: 100%; height: auto; }}

@media (max-width: 599px) {{
  {C} .r3Lead {{ font-size: 23px; }}
  {C} .r3Small {{ font-size: 18px; }}
  {C} .day .r3Pano, {C} .day .r3Moments {{ display: none; }}
  {C} .day .r3Strip {{
    display: flex; gap: 16px; margin: 28px -20px 0; padding: 0 20px;
    overflow-x: auto; scroll-snap-type: x mandatory; scrollbar-width: none;
  }}
  {C} .day .r3Slide {{ flex: 0 0 80%; scroll-snap-align: start; }}
  {C} .day .r3Crop {{ position: relative; height: 230px; overflow: hidden; }}
  {C} .day .r3Crop img {{ position: absolute; top: 0; height: 100%; width: auto; max-width: none; }}
  {C} .day .r3Slide p {{ margin: 14px 0 0; font-size: 18px; line-height: 1.5; color: {GREY}; }}
  {C} .day .r3Slide b {{ display: block; font-weight: 550; color: {INK}; font-size: 20px; margin-bottom: 2px; }}
  {C} .day .r3Slide figcaption {{ display: none; }}
  {C} .day .r3Src::before {{ content: 'Illustration. '; }}
  {C} .r3.rings {{ grid-template-columns: 1fr !important; row-gap: 28px; }}
  {C} .rings .r3Log {{ grid-row: 2 !important; grid-column: 1 !important; max-width: 340px; }}
  {C} .rings .r3Words {{ display: contents; }}
  {C} .rings .r3Words .r3Head {{ grid-row: 1; }}
  {C} .rings .r3Small {{ grid-row: 3; margin-top: 0; }}
}}
"""

MOMENTS = [  # (bold, line, scene centre as a fraction of the painting's width)
    ("Morning: move.", "Moving is the best-supported way to keep mitochondria healthy.", 0.13),
    ("Breakfast: NuriCell.", "3 capsules once a day, with or after a meal.", 0.40),
    ("Afternoon: friends.", "Time with people is linked to healthier aging.", 0.60),
    ("Night: sleep.", "Adults need 7 to 9 hours.", 0.90),
]
DAY = {
    "title": "A good day for your cells.",
    "lead": "NuriCell is one part of it. The rest is how you spend the day.",
    "src": "Sources: a review of exercise and mitochondria (J Physiol, 2021); the National Institute on Aging.",
}
RINGS = {
    "title": "The same formula for about 20 years.",
    "lead": "Dr. Liu chose its four nutrients. We haven’t changed them since.",
    "small": "The gold ring is about 20 years ago. Each ring outside it is a year with the same four: "
    "acetyl-L-carnitine, creatine, alpha-lipoic acid and choline.",
}

JS = """([kind, words, src, moments]) => {
  const c = document.querySelector('[data-chapter="daily"]');
  const wrap = c.querySelector(':scope > div');
  const h2 = c.querySelector('h2');
  wrap.className = wrap.className.split(' ').filter(k => !/spread/.test(k)).join(' ') + ' r3 ' + kind;
  const head = `<div class="r3Head"><h2 id="${h2.id}" class="${h2.className}">${words.title}</h2>
    <p class="r3Lead">${words.lead}</p></div>`;
  if (kind === 'day') {
    const lis = moments.map(([b, t]) => `<li><b>${b}</b>${t}</li>`).join('');
    const slides = moments.map(([b, t, x]) => `<div class="r3Slide" data-x="${x}">
      <figure class="r3Crop"><img class="mult" src="${src}" alt=""></figure>
      <figcaption>Illustration</figcaption><p><b>${b}</b>${t}</p></div>`).join('');
    wrap.innerHTML = `${head}
      <figure class="r3Pano"><img class="mult" src="${src}" alt="One California day on a hillside: a morning walk, breakfast under an oak, friends on a bench, a farmhouse at night"><figcaption>Illustration</figcaption></figure>
      <ol class="r3Moments">${lis}</ol>
      <div class="r3Strip">${slides}</div>
      <p class="r3Src">${words.src}</p>`;
  } else {
    wrap.innerHTML = `<div class="r3Words">${head}<p class="r3Small">${words.small}</p></div>
      <figure class="r3Log"><img class="mult" src="${src}" alt="The cut end of a young redwood log, one of its rings in gold leaf"><figcaption>Illustration</figcaption></figure>`;
  }
}"""

# Each phone slide frames its own moment: the painting at the crop's height, its scene centred.
FRAME = """() => {
  const c = document.querySelector('[data-chapter="daily"]'), strip = c.querySelector('.r3Strip');
  if (!strip || !strip.offsetWidth) return;
  // The strip runs to the window's edges; its first slide starts on the heading's left edge.
  strip.style.margin = '28px 0 0';
  const L = c.querySelector('h2').getBoundingClientRect().left, r = strip.getBoundingClientRect();
  Object.assign(strip.style, { marginLeft: -r.left + 'px', marginRight: -(innerWidth - r.right) + 'px',
    paddingLeft: L + 'px', paddingRight: L + 'px', scrollPaddingLeft: L + 'px' });
  for (const s of strip.querySelectorAll('.r3Slide')) {
    const box = s.querySelector('.r3Crop'), img = box.querySelector('img');
    const W = box.clientWidth, H = box.clientHeight, full = img.naturalWidth * H / img.naturalHeight;
    const left = Math.min(0, Math.max(W - full, W / 2 - (+s.dataset.x) * full));
    img.style.left = left + 'px';
    // Each frame dissolves into the paper at its sides instead of ending on a cut.
    const a = -left, f = 0.16 * W;
    const m = `linear-gradient(to right, transparent ${a}px, #000 ${a + f}px, #000 ${a + W - f}px, transparent ${a + W}px)`;
    img.style.maskImage = m; img.style.webkitMaskImage = m;
  }
}"""

SIZES = {"desktop": dict(width=1440, height=900, scale=1), "phone": dict(width=390, height=844, scale=2)}


def settle(page, ms=900):
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(ms)


def shoot(page, tag, start, end, most=3):
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


def span(page):
    return page.evaluate("""() => { const c = document.querySelector('[data-chapter="daily"]');
      const r = c.getBoundingClientRect(); return [r.top + scrollY, r.top + scrollY + c.offsetHeight]; }""")


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
            if v == "day":
                page.evaluate(JS, ["day", DAY, data_url(PLATES / "day.png"), MOMENTS])
            else:
                page.evaluate(JS, ["rings", RINGS, data_url(PLATES / "rings.png"), []])
            settle(page)
            page.evaluate(FRAME)
            top, bottom = span(page)
            shoot(page, f"{size}-{v}", top - (140 if size == "desktop" else 60), bottom + 40)
            if v == "day" and size == "phone":
                # The strip swiped on to breakfast, where the capsules are.
                strip = page.locator('[data-chapter="daily"] .r3Strip')
                strip.scroll_into_view_if_needed()
                page.evaluate("""() => { const s = document.querySelector('[data-chapter="daily"] .r3Strip');
                  const r = s.getBoundingClientRect(); window.scrollTo(0, r.top + scrollY - 260);
                  s.scrollTo({ left: s.querySelectorAll('.r3Slide')[1].offsetLeft - 20 }); }""")
                page.wait_for_timeout(2500)
                page.screenshot(path=str(OUT / f"{size}-{v}-swiped.png"))
                print("swiped shot", flush=True)
            page.close()
        ctx.close()
    browser.close()

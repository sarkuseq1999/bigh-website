"""Mockups for Mo (November 11, 2026): three ideas for the Science page's Dr. Liu part.

  python -X utf8 reference/ink-pages/mockups/science-liu/shoot.py <base-url> [a] [b] [c] [now]

Mo found the part plain: a small dark studio photograph on bare paper, between a page of paintings.
Each idea is put into the real page in the browser (nothing in src/ changes): the script opens
<base-url>/science, replaces what stands inside #liu, and takes a desktop, a laptop and a phone
picture into shots/ beside this script (and smaller copies into review/ for the review page).

  now  the part as it is live
  a    "In his own words": his painted portrait, large, beside one sentence of his own
  b    "Office hours": he leans on a desk, a blackboard with a chalk mitochondrion behind him
  c    "The gold he studies": he sits at the edge of one huge cell, its mitochondria in gold

The plates of b and c come from plates.py (reference/ink-pages/science/plates/liu/, git-ignored).
His portrait is the shipped liu-v1 (his real face, never generated).
"""

import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
PLATES = HERE.parent.parent / "science" / "plates" / "liu"
OUT = HERE / "shots"
REVIEW = HERE / "review"
OUT.mkdir(exist_ok=True)
REVIEW.mkdir(exist_ok=True)

args = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = args[0].rstrip("/") if args else "https://bigh-website-demo.vercel.app"
WANT = args[1:] or ["now", "a", "b", "c", "d", "e"]
SIZES = (("desk", 1440, 900, 1), ("laptop", 1280, 720, 1), ("phone", 390, 844, 2))

PORTRAIT = "/images/products/nuricell/ink/liu-v1.webp"
GOLD = "/images/home-v2/ink/gold-leaf-word.webp"

# The words every idea keeps are the live ones (science-content.ts, approved September 21, 2026).
NAME = "Dr. Jiankang Liu"
ROLE = "Chief Scientific Advisor, BiGH"
HEADLINE = "Recognized internationally. Focused on cellular health."
INTRO = (
    "Dr. Liu is an internationally recognized scientist in mitochondrial biology and aging. His "
    "research explores the connections between cellular energy, nutrition, and how we age."
)
# A's sentence is a stand-in: no quote is ever invented for Dr. Liu. Its length is the length a real
# one should have.
STAND_IN = "One real sentence from Dr. Liu goes here, in his own words, on why he studies the cell."
# Three facts the page already tells, with their sources, in his path below.
FACTS = "<span>Research at UC Berkeley from 1994</span> <span>280+ scientific papers</span> <span>European Academy of Sciences and Arts, 2025</span>"

COMMON = """
#liu.mock { display: block; max-width: none; padding: 0; }
#liu.mock * { box-sizing: border-box; }
#liu.mock .ink { display: block; mix-blend-mode: multiply; }
#liu.mock .name { margin: 0; font-family: var(--display-font); font-weight: 500; line-height: 1.04; }
#liu.mock .role { margin: 8px 0 0; color: var(--muted); font-size: 18px; line-height: 1.4; }
#liu.mock .headline { margin: 14px 0 0; color: var(--ink); font-size: 21px; line-height: 1.4; }
#liu.mock .intro { margin: 10px 0 0; max-width: 640px; color: var(--muted); font-size: 19px; line-height: 1.6; }
#liu.mock .story { margin-top: 22px; }
#liu.mock .tag { margin: 0; color: var(--muted); font-size: 15px; line-height: 1.4; }
"""

IDEAS = {
    "now": None,
    "a": {
        "css": """
#liu.mock .a { display: grid; gap: 28px; width: 100%; max-width: calc(1180px + 2 * var(--gutter));
  margin: 0 auto; padding: 0 var(--gutter); }
#liu.mock .a .portrait { margin: 0; justify-self: center; width: min(78vw, 330px); }
#liu.mock .a .portrait img { width: 100%; height: auto; }
#liu.mock .a .mark { display: block; height: 0.5em; margin: 0 0 6px -0.04em; font-family: var(--display-font);
  font-size: 150px; font-weight: 600; line-height: 1; color: #b98a2c;
  background: url(GOLD) center / 330px 330px; -webkit-background-clip: text; background-clip: text;
  -webkit-text-fill-color: transparent; }
#liu.mock .a blockquote { margin: 0; }
#liu.mock .a .say { margin: 0; max-width: 16em; font-family: var(--display-font); font-size: clamp(31px, 3.25vw, 47px);
  font-weight: 500; line-height: 1.14; letter-spacing: -0.005em; text-wrap: balance; color: var(--ink); }
#liu.mock .a .who { margin-top: 30px; }
#liu.mock .a .name { font-size: clamp(27px, 2.2vw, 32px); }
#liu.mock .a .facts { margin: 10px 0 0; max-width: 34em; color: var(--ink); font-size: 18px; line-height: 1.5; }
#liu.mock .a .facts span { display: block; }
#liu.mock .a .tag { margin-top: 18px; }
@media (min-width: 960px) {
  #liu.mock .a { grid-template-columns: minmax(0, 0.8fr) minmax(0, 1fr); gap: 76px; align-items: center; }
  #liu.mock .a .portrait { width: auto; justify-self: end; }
  /* He fits a laptop's window whole, under the menu bar. */
  #liu.mock .a .portrait img { width: auto; max-width: 100%; height: min(694px, 100vh - 170px); }
}
""",
            "html": """
<div class="a">
  <figure class="portrait"><img class="ink" src="PORTRAIT" alt=""></figure>
  <div>
    <blockquote>
      <span class="mark" aria-hidden="true">&ldquo;</span>
      <p class="say">STAND_IN</p>
    </blockquote>
    <div class="who">
      <h2 class="name">NAME</h2>
      <p class="role">ROLE</p>
      <p class="facts">FACTS</p>
      <span data-story></span>
    </div>
  </div>
</div>
""",
    },
    "b": {
        "css": """
#liu.mock .b { display: grid; gap: 26px; width: 100%; }
#liu.mock .b .scene { margin: 0; position: relative; }
#liu.mock .b .scene img { width: 100%; height: auto; }
#liu.mock .b .words { padding: 0 var(--gutter); }
#liu.mock .b .name { font-size: clamp(40px, 3.6vw, 52px); }
#liu.mock .b .tag { margin-top: 6px; padding: 0 var(--gutter); }
@media (min-width: 960px) {
  #liu.mock .b { grid-template-columns: minmax(0, 1.5fr) minmax(0, 1fr); gap: 0; align-items: center; }
  #liu.mock .b .words { padding: 0 var(--gutter) 0 34px; }
  #liu.mock .b .tag { position: absolute; left: var(--gutter); bottom: -6px; margin: 0; padding: 0; }
}
""",
        "html": """
<div class="b">
  <figure class="scene">
    <picture>
      <source media="(max-width: 959px)" srcset="/__mock/b-phone.webp">
      <img class="ink" src="/__mock/b-desk.webp" alt="">
    </picture>
    <p class="tag">Portrait painting &middot; Illustration</p>
  </figure>
  <div class="words">
    <h2 class="name">NAME</h2>
    <p class="role">ROLE</p>
    <p class="headline">HEADLINE</p>
    <p class="intro">INTRO</p>
    <span data-story></span>
  </div>
</div>
""",
    },
    "c": {
        "css": """
#liu.mock .c { position: relative; display: grid; gap: 18px; width: 100%; }
#liu.mock .c .scene { margin: 0; }
#liu.mock .c .scene img { width: 100%; height: auto; }
#liu.mock .c .words { padding: 0 var(--gutter); }
#liu.mock .c .name { font-size: clamp(40px, 3.6vw, 52px); }
#liu.mock .c .gold { display: flex; align-items: baseline; gap: 10px; margin: 22px 0 0; color: var(--ink); font-size: 18px; line-height: 1.45; }
#liu.mock .c .gold i { flex: none; width: 30px; height: 7px; border-radius: 60% 40% 60% 40%; transform: rotate(-14deg) translateY(-2px);
  background: #c49a3a url(GOLD) center / 200px 200px; }
@media (min-width: 960px) {
  #liu.mock .c { display: block; }
  /* The words end clear of the cell's edge (about 46% across the window). */
  #liu.mock .c .words { position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 42%; padding: 0 0 0 var(--gutter); }
  #liu.mock .c .intro { max-width: 30em; }
}
""",
        "html": """
<div class="c">
  <figure class="scene">
    <picture>
      <source media="(max-width: 959px)" srcset="/__mock/c-phone.webp">
      <img class="ink" src="/__mock/c-desk.webp" alt="">
    </picture>
  </figure>
  <div class="words">
    <h2 class="name">NAME</h2>
    <p class="role">ROLE</p>
    <p class="headline">HEADLINE</p>
    <p class="intro">INTRO</p>
    <p class="gold"><i></i><span>In gold: mitochondria. He has studied them since 1994.</span></p>
    <span data-story></span>
  </div>
</div>
""",
    },
}

# Round 2 (Mo, November 11: C is good but its cell repeats the page's opening; two more ideas, and
# for mockups Dr. Liu's picture may be redrawn). Both are Codex paintings WITH him in them, painted
# from his photograph: a redrawn Dr. Liu, for Mo and Dr. Liu to judge, never live as it is.
IDEAS["d"] = {
    "css": """
#liu.mock .d { position: relative; display: grid; gap: 18px; width: 100%; }
#liu.mock .d .scene { margin: 0; }
#liu.mock .d .scene img { width: 100%; height: auto; }
#liu.mock .d .words { padding: 0 var(--gutter); }
#liu.mock .d .name { font-size: clamp(40px, 3.6vw, 52px); }
#liu.mock .d .tag { margin-top: 14px; }
@media (min-width: 960px) {
  #liu.mock .d { display: block; }
  #liu.mock .d .words { position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 44%; padding: 0 0 0 var(--gutter); }
  #liu.mock .d .intro { max-width: 30em; }
}
""",
    "html": """
<div class="d">
  <figure class="scene">
    <picture>
      <source media="(max-width: 959px)" srcset="/__mock/d-phone.webp">
      <img class="ink" src="/__mock/d-desk.webp" alt="">
    </picture>
  </figure>
  <div class="words">
    <h2 class="name">NAME</h2>
    <p class="role">ROLE</p>
    <p class="headline">HEADLINE</p>
    <p class="intro">INTRO</p>
    <span data-story></span>
    <p class="tag">Illustration</p>
  </div>
</div>
""",
}
IDEAS["e"] = {
    "css": """
#liu.mock .e { position: relative; display: grid; gap: 18px; width: 100%; }
#liu.mock .e .scene { margin: 0; }
#liu.mock .e .scene img { width: 100%; height: auto; }
#liu.mock .e .words { padding: 0 var(--gutter); }
#liu.mock .e .name { font-size: clamp(40px, 3.6vw, 52px); }
#liu.mock .e .count { display: flex; align-items: baseline; gap: 14px; margin: 20px 0 0; }
#liu.mock .e .count b { font-family: var(--display-font); font-size: clamp(54px, 5vw, 76px); font-weight: 500; line-height: 0.9;
  font-variant-numeric: lining-nums; font-feature-settings: "lnum" 1;
  background: #b98a2c url(GOLD) center / 330px 330px; -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; }
#liu.mock .e .count span { color: var(--ink); font-size: 19px; line-height: 1.35; }
#liu.mock .e .tag { margin-top: 14px; }
@media (min-width: 960px) {
  #liu.mock .e { display: block; }
  #liu.mock .e .words { position: absolute; left: 0; bottom: 4%; width: 46%; padding: 0 0 0 var(--gutter); }
  #liu.mock .e .intro { max-width: 30em; }
}
""",
    "html": """
<div class="e">
  <figure class="scene">
    <picture>
      <source media="(max-width: 959px)" srcset="/__mock/e-phone.webp">
      <img class="ink" src="/__mock/e-desk.webp" alt="">
    </picture>
  </figure>
  <div class="words">
    <h2 class="name">NAME</h2>
    <p class="role">ROLE</p>
    <p class="headline">HEADLINE</p>
    <p class="intro">INTRO</p>
    <p class="count"><b>280+</b><span>scientific papers,<br>sent out into the world.</span></p>
    <span data-story></span>
    <p class="tag">Illustration</p>
  </div>
</div>
""",
}

FILL = {
    "PORTRAIT": PORTRAIT,
    "GOLD": GOLD,
    "STAND_IN": STAND_IN,
    "FACTS": FACTS,
    "NAME": NAME,
    "ROLE": ROLE,
    "HEADLINE": HEADLINE,
    "INTRO": INTRO,
}


def filled(text: str) -> str:
    for key, value in FILL.items():
        text = text.replace(key, value)
    return text


# Put an idea in #liu's place: its own markup, the live "Read his story" button moved into it (it
# keeps the kit's look), every picture loaded before the screenshot.
SWAP = """async ([css, html]) => {
  const liu = document.querySelector('#liu');
  const story = liu.querySelector('button');
  const style = document.createElement('style');
  style.textContent = css;
  document.head.append(style);
  liu.className = liu.className + ' mock';
  liu.innerHTML = html;
  const slot = liu.querySelector('[data-story]');
  if (slot && story) { story.classList.add('story'); slot.replaceWith(story); }
  await Promise.all([...liu.querySelectorAll('img')].map((img) => img.decode().catch(() => {})));
  await document.fonts.ready;
}"""

MEASURE = """() => { const r = document.querySelector('#liu').getBoundingClientRect();
  return { top: r.top + scrollY, height: r.height }; }"""


def serve(route):
    name = route.request.url.split("/__mock/", 1)[1].split("?")[0]
    path = PLATES / name
    route.fulfill(path=str(path)) if path.exists() else route.fulfill(status=404, body="missing " + name)


with sync_playwright() as p:
    browser = p.chromium.launch()
    for key in WANT:
        idea = IDEAS[key]
        for name, w, h, dense in SIZES:
            ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=dense)
            ctx.route("**/__mock/**", serve)
            page = ctx.new_page()
            page.goto(BASE + "/science", wait_until="networkidle")
            page.wait_for_timeout(1500)
            if idea:
                page.evaluate(SWAP, [filled(COMMON + idea["css"]), filled(idea["html"])])
            box = page.evaluate(MEASURE)
            # The part as a visitor meets it: centred in the window when it fits, else its top a
            # little under the menu bar.
            bar = 96
            top = box["top"] - max(bar, (h - box["height"]) / 2) if box["height"] < h - bar else box["top"] - bar
            page.evaluate("y => scrollTo({ top: y, behavior: 'instant' })", top)
            page.wait_for_timeout(1300)
            page.screenshot(path=str(OUT / f"{key}-{name}.png"))
            if name == "phone" and box["height"] > h - bar:
                # A phone's second screen of the part.
                page.evaluate("y => scrollTo({ top: y, behavior: 'instant' })", top + h - bar - 40)
                page.wait_for_timeout(900)
                page.screenshot(path=str(OUT / f"{key}-{name}-2.png"))
            print(key, name, {k: round(v) for k, v in box.items()})
            ctx.close()
    browser.close()

for shot in sorted(OUT.glob("*.png")):
    im = Image.open(shot).convert("RGB")
    width = 780 if "-phone" in shot.stem else 1280
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(REVIEW / f"{shot.stem}.jpg", "JPEG", quality=86, optimize=True, progressive=True)
print("pictures in", OUT, "and", REVIEW)

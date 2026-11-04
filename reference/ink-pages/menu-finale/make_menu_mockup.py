"""Mockup page for part 6 of the homepage's California pass (November 3, 2026): what stands at the
foot of the phone menu in place of the crane at rest, the last crane on the site. Cuts the shots that
shoot_menu.py took into a whole phone screen, a close-up and a tablet close-up per option and writes
reference/ink-pages/mockups/menu-finale/menu-finale.html. An option with the opening's bird (its
<key>-bird.json from shoot_menu.py) gets the bird's body and wings laid over its shots. Mo
(November 3): the beating wings were "annoying, like flys" at the menu's size, so they rest on the
first frame, raised as painted, as the homepage's do with reduced motion.

usage: python -X utf8 reference/ink-pages/menu-finale/make_menu_mockup.py [option ...]
(only the options named are cut again; their shots must exist; `html` cuts none, only the page)
"""

import json
import shutil
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
OUT = HERE.parents[0] / "mockups" / "menu-finale"
INK = HERE.parents[2] / "public" / "images" / "home-v2" / "ink"
ONLY = sys.argv[1:]

# Each view: its shot and the part of it shown (css px: x, y, w, h), as shots() cuts it.
VIEWS = {
    "screen": ("phone", (0, 0, 390, 844), "The phone menu, whole"),
    "close": ("phone", (20, 500, 350, 344), "Phone, close-up"),
    "tablet": ("tablet", (150, 750, 468, 274), "Tablet, close-up"),
}

TODAY = {
    "key": "now",
    "name": "Today: the crane at rest",
    "what": "Tap Menu on a phone and a small crane stands at the bottom, on a black brush line. It was the footer's crane in miniature. The footer has quail now, so the two no longer match.",
}

BUILT = "Your pick, built into the site on this computer (not live yet). The homepage's own hummingbird, its wings resting, raised as painted, sipping from the California fuchsia. Nothing moves; it stands where the crane stood, and Log in and Sign up stay where they were."
CHOICES = [
    {
        "key": "d",
        "group": "The hummingbird (new)",
        "name": "The hummingbird, at rest",
        "score": "8.5",
        "pick": False,
        "what": "Allen's hummingbird on a bare twig, the way it sits and keeps watch over its flowers. A new painting of the homepage's bird, in the same calm copper.",
        "note": "Still and quiet, like the crane at rest. Its beak is a fine dark line, a little sharper than the rest of the painting.",
    },
    {
        "key": "e",
        "name": "The hummingbird at a flower",
        "score": "9",
        "pick": True,
        "what": "The homepage's own hummingbird, sipping from California fuchsia, a wildflower of the dry hills that hummingbirds love. Only the flower is a new painting.",
        "note": "Now still: its wings rest, raised, as they are painted, and nothing moves beside the menu's words. The bird that greets you on the homepage is waiting at the end of the menu.",
    },
    {
        "key": "a",
        "group": "Earlier ideas",
        "name": "One quail",
        "score": "9",
        "pick": False,
        "what": "The footer's lookout quail, standing on its own. The same bird and the same few wet washes as the two quail at the bottom of every page. One bird fits the tall spot the crane stood in.",
        "note": "Softer and paler than the crane, so it sits quietly under the menu's words. On a tablet it is small, as the crane was.",
    },
    {
        "key": "b",
        "name": "The footer's two quail",
        "score": "8",
        "pick": False,
        "what": "The footer's own painting, made smaller. No new painting.",
        "note": "You would see the same picture twice in one visit. On a phone the bending quail gets small.",
    },
    {
        "key": "c",
        "name": "California poppies",
        "score": "8",
        "pick": False,
        "what": "California's state flower, the poppy from the park sign, on its own: two flowers and a bud.",
        "note": "The brightest thing in the menu: its orange pulls your eye away from the words. Poppies are already on About and on the park sign.",
    },
]


def shots(key):
    p = Image.open(OUT / f"{key}-phone.png").convert("RGB")  # 390 x 844 at 2x
    p.resize((520, 1125), Image.LANCZOS).save(OUT / f"{key}-screen.jpg", quality=84)
    p.crop((40, 1000, 740, 1688)).save(OUT / f"{key}-close.jpg", quality=86)
    t = Image.open(OUT / f"{key}-tablet.png").convert("RGB")  # 768 x 1024 at 2x
    t.crop((300, 1500, 1236, 2048)).save(OUT / f"{key}-tablet.jpg", quality=86)


CSS = """
  /* Layout: one column; today's crane first, then each idea: its words, then a whole phone screen
     of the real menu, a close-up of its foot and the same on a tablet. */
  :root {
    --paper: #f6f1e7;
    --ink: #1d1b18;
    --ink-soft: #5d574e;
    --rule: #ddd4c4;
    --gold: #a77c25;
    --pick: #2f4a3a;
    --title: "Ysabeau", "Palatino Linotype", Palatino, Georgia, serif;
    --body: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --paper: #1b1a17; --ink: #f1ece2; --ink-soft: #b9b0a2;
      --rule: #3a3630; --gold: #d6aa52; --pick: #9cc3a8; color-scheme: dark;
    }
  }
  :root[data-theme="dark"] {
    --paper: #1b1a17; --ink: #f1ece2; --ink-soft: #b9b0a2;
    --rule: #3a3630; --gold: #d6aa52; --pick: #9cc3a8; color-scheme: dark;
  }
  body {
    background: var(--paper);
    color: var(--ink);
    font: 17px/1.55 var(--body);
    padding-left: max(16px, env(safe-area-inset-left, 0px));
    padding-right: max(16px, env(safe-area-inset-right, 0px));
  }
  main { max-width: 1000px; margin: 0 auto; padding-block: 40px 72px; display: grid; gap: 52px; }
  h1, h2 { font-family: var(--title); font-weight: 650; text-wrap: balance; margin: 0; letter-spacing: -0.01em; }
  h1 { font-size: clamp(34px, 6vw, 52px); line-height: 1.05; }
  h2 { font-size: clamp(26px, 4vw, 34px); line-height: 1.1; }
  p { margin: 0; max-width: 62ch; }
  .intro { display: grid; gap: 12px; }
  .intro p { color: var(--ink-soft); font-size: 18px; }
  .choice { display: grid; gap: 14px; padding-top: 26px; border-top: 1px solid var(--rule); }
  .head { display: flex; flex-wrap: wrap; align-items: baseline; gap: 10px 16px; }
  .letter { font-family: var(--title); font-size: clamp(44px, 7vw, 60px); line-height: 0.8; color: var(--gold); font-weight: 650; }
  .score { font: 600 15px/1 var(--body); font-variant-numeric: tabular-nums; padding: 7px 11px; border: 1px solid var(--rule); border-radius: 999px; color: var(--ink-soft); }
  .tag { font: 600 13px/1 var(--body); letter-spacing: 0.06em; text-transform: uppercase; color: var(--paper); background: var(--pick); padding: 7px 10px; border-radius: 999px; }
  .what { font-size: 18px; }
  .note { color: var(--ink-soft); }
  .shots { display: grid; grid-template-columns: 1fr 1.35fr; gap: 12px; align-items: start; }
  .shots .tablet { grid-column: 2; }
  .shots .screen { grid-row: span 2; }
  figure { margin: 0; display: grid; gap: 6px; min-width: 0; }
  figure img { display: block; width: 100%; height: auto; border: 1px solid var(--rule); border-radius: 6px; }
  figcaption { font-size: 13px; color: var(--ink-soft); letter-spacing: 0.02em; }
  .group { font: 600 14px/1.2 var(--body); letter-spacing: 0.08em; text-transform: uppercase; color: var(--ink-soft); margin-bottom: -30px; }
  /* The opening's hummingbird laid over a shot: its far wing behind its body, its near wing over
     it, both on their first frame, raised as painted (the homepage's rest). */
  .scene { position: relative; overflow: hidden; border: 1px solid var(--rule); border-radius: 6px; }
  .scene img { border: 0; border-radius: 0; }
  .bird { position: absolute; aspect-ratio: 1600 / 1062; }
  .bird .body { position: absolute; inset: 0; width: 100%; height: 100%; }
  .wing {
    position: absolute; left: 16.19%; top: 14.174%; width: 45.644%; height: 76.931%;
    background-size: 600% 100%; background-repeat: no-repeat; background-position: 0 0;
  }
  @media (max-width: 640px) {
    .shots { grid-template-columns: 1fr; }
    .shots .tablet, .shots .screen { grid-column: auto; grid-row: auto; }
    .shots .close { order: -1; }
    .shots .screen { width: 72%; }
  }
"""


def pct(v):
    return f"{v:.3f}%"


def picture(k, view, alt, birds):
    """A view's picture; with the opening's bird, its body and resting wings over the shot."""
    img = f'<img src="{k}-{view}.jpg" alt="{alt}">'
    if not birds:
        return img
    shot, (cx, cy, cw, ch), _ = VIEWS[view]
    x, y, w, _ = birds[shot]
    at = f"left:{pct((x - cx) / cw * 100)};top:{pct((y - cy) / ch * 100)};width:{pct(w / cw * 100)}"
    return f"""<div class="scene">{img}<span class="bird" style="{at}"><span class="wing" style="background-image:url({k}-far.webp)"></span><img class="body" src="{k}-body.webp" alt=""><span class="wing" style="background-image:url({k}-near.webp)"></span></span></div>"""


def figures(k, name):
    path = OUT / f"{k}-bird.json"
    birds = json.loads(path.read_text(encoding="utf-8")) if path.exists() else None
    where = {"screen": "the whole phone menu", "close": "the foot of the phone menu", "tablet": "the foot of the tablet menu"}
    rows = "\n".join(
        f'      <figure class="{v}">{picture(k, v, f"{name}, {where[v]}", birds)}<figcaption>{VIEWS[v][2]}</figcaption></figure>'
        for v in VIEWS
    )
    return f"""    <div class="shots">
{rows}
    </div>
"""


def section(c):
    k = c["key"]
    tag = '<span class="tag">My pick</span>' if c["pick"] else ""
    group = f'  <p class="group">{c["group"]}</p>\n' if c.get("group") else ""
    return f"""{group}  <section class="choice" aria-labelledby="{k}-name">
    <div class="head">
      <span class="letter">{k.upper()}</span>
      <h2 id="{k}-name">{c["name"]}</h2>
      <span class="score">{c["score"]} / 10</span>
      {tag}
    </div>
    <p class="what">{c["what"]}</p>
    <p class="note">{c["note"]}</p>
{figures(k, c["name"])}  </section>
"""


def main():
    for k in ["now"] + [c["key"] for c in CHOICES]:
        if ONLY and k not in ONLY:
            continue
        shots(k)
        if (OUT / f"{k}-bird.json").exists():
            shutil.copyfile(INK / "hummingbird-v2.webp", OUT / f"{k}-body.webp")
            for side in ("near", "far"):
                shutil.copyfile(INK / f"hummingbird-v2-{side}.webp", OUT / f"{k}-{side}.webp")
    # Built (Mo picked E, wings still): shots of the built site (npm run build + npm start), cut by
    # hand to the same three views into built-*.jpg.
    built = ""
    if (OUT / "built-screen.jpg").exists():
        built = f"""  <section class="choice" aria-labelledby="built-name">
    <div class="head"><span class="letter">E</span><h2 id="built-name">Built: the hummingbird at a flower</h2><span class="tag">Mo's pick</span></div>
    <p class="what">{BUILT}</p>
{figures("built", "The hummingbird, built")}  </section>
"""
    today = f"""  <section class="choice" aria-labelledby="now-name">
    <div class="head"><h2 id="now-name">{TODAY["name"]}</h2></div>
    <p class="what">{TODAY["what"]}</p>
{figures("now", "The crane")}  </section>
"""
    html = f"""<title>Phone Menu Finale</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Ysabeau:wght@650&display=swap">
<style>{CSS}</style>
<main>
  <header class="intro">
    <h1>The phone menu's last crane</h1>
    <p>Tap Menu on a phone: a small crane stands at the bottom. It is the last crane on the site. Here are California ideas to replace it, put into the real menu of the demo. Nothing on the site has changed.</p>
    <p>Mo picked E with its wings still. It is built first below, then the ideas as they were mocked. The black line under the crane goes in all of them: each stands on its own painted ground.</p>
  </header>
{built}{today}{"".join(section(c) for c in CHOICES)}</main>
"""
    (OUT / "menu-finale.html").write_text(html, encoding="utf-8", newline="\n")
    print("wrote", OUT / "menu-finale.html")


if __name__ == "__main__":
    main()

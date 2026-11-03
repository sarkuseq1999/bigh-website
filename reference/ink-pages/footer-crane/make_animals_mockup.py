"""Mockup page for part 5 of the homepage's California pass (November 3, 2026): which California
animal stands by the FDA park sign in place of the red-crowned crane. Cuts the shots that
shoot_animals.py took into laptop, phone and close-up pictures and writes
reference/ink-pages/mockups/footer-crane/animals/footer-animal.html.

Round 2 (Mo, November 3: the quail and the bear cub "a little more painting like") replaces the
page with each of them painted two ways.

usage: python -X utf8 reference/ink-pages/footer-crane/make_animals_mockup.py [1 | 2]
"""

import sys

from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
OUT = HERE.parents[0] / "mockups" / "footer-crane" / "animals"

CHOICES = [
    {
        "key": "a",
        "name": "California quail",
        "score": "9",
        "pick": True,
        "what": "California's state bird. One stands tall on watch while the other bends to the poppy: a quail covey always keeps a lookout. Stay sharp.",
        "note": "The smallest of the three. On a phone the birds are small, but their curled plumes still read.",
    },
    {
        "key": "b",
        "name": "Desert tortoise",
        "score": "8",
        "pick": False,
        "what": "California's state reptile. It lives among the Mojave's spring poppies and can live more than 50 years. It walks up and sniffs the poppy.",
        "note": "Slow can read as tired on a site about energy. Its shell is the most drawn of the three.",
    },
    {
        "key": "c",
        "name": "Black bear cub",
        "score": "8.5",
        "pick": False,
        "what": "A young black bear, the kind that lives in California's state parks. A bear stands on the state flag. It sniffs the poppy.",
        "note": "The biggest and darkest of the three: it pulls your eye away from the sign. A bear by a park sign can also read as a warning.",
    },
]


# Round 2: per animal, last round's close-up, then the two new hands.
ROUND2 = [
    {
        "title": "A, the quail",
        "before": "a",
        "takes": [
            {
                "key": "a1",
                "name": "Wet wash",
                "score": "9",
                "pick": True,
                "what": "A few soft wet washes and no outlines, like the hummingbird at the top of the homepage. The most painted of the four.",
                "note": "Softer and paler than before, so it sits quietly next to the dark sign.",
            },
            {
                "key": "a2",
                "name": "Ink and wash",
                "score": "8.5",
                "pick": False,
                "what": "Brush lines with pale colour laid over them, like the Big Sur painting at the end of the homepage. Their legs and feet show.",
                "note": "A little more drawn than A1; up close, the fine lines around the eyes are busy.",
            },
        ],
    },
    {
        "title": "C, the bear cub",
        "before": "c",
        "takes": [
            {
                "key": "c1",
                "name": "Wet wash",
                "score": "8.5",
                "pick": False,
                "what": "Soft brown washes, like the hummingbird. It reads as a grizzly cub, the bear on California's flag.",
                "note": "Softer and lighter than before, so it pulls less on your eye; still the biggest thing in the footer, and its body is a little long.",
            },
            {
                "key": "c2",
                "name": "Ink and wash",
                "score": "7",
                "pick": False,
                "what": "Bold black ink with bare paper left as the light, like the Big Sur painting.",
                "note": "At footer size the bare patches on its back look like markings, like a badger.",
            },
        ],
    },
]


def shots(key):
    d = Image.open(OUT / f"{key}-home-desktop.png")  # 1440 x 900 at 2x
    d.crop((0, 1000, 2880, 1800)).resize((1440, 400), Image.LANCZOS).convert("RGB").save(
        OUT / f"{key}-laptop.jpg", quality=86
    )
    d.crop((1150, 1150, 2450, 1620)).convert("RGB").save(OUT / f"{key}-close.jpg", quality=88)
    p = Image.open(OUT / f"{key}-home-phone.png")  # 390 x 844 at 2x
    p.crop((0, 720, 780, 1688)).convert("RGB").save(OUT / f"{key}-phone.jpg", quality=86)


CSS = """
  /* Layout: one column; today's crane first, then each animal: its words, then the laptop and
     phone footers of the real homepage and a close-up. */
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
  main { max-width: 1100px; margin: 0 auto; padding-block: 40px 72px; display: grid; gap: 52px; }
  h1, h2 { font-family: var(--title); font-weight: 650; text-wrap: balance; margin: 0; letter-spacing: -0.01em; }
  h1 { font-size: clamp(34px, 6vw, 52px); line-height: 1.05; }
  h2 { font-size: clamp(26px, 4vw, 34px); line-height: 1.1; }
  p { margin: 0; max-width: 62ch; }
  ul { margin: 0; padding-left: 1.2em; max-width: 62ch; color: var(--ink-soft); display: grid; gap: 4px; }
  .intro { display: grid; gap: 12px; }
  .intro p { color: var(--ink-soft); font-size: 18px; }
  .choice { display: grid; gap: 14px; padding-top: 26px; border-top: 1px solid var(--rule); }
  .head { display: flex; flex-wrap: wrap; align-items: baseline; gap: 10px 16px; }
  .letter { font-family: var(--title); font-size: clamp(44px, 7vw, 60px); line-height: 0.8; color: var(--gold); font-weight: 650; }
  .score { font: 600 15px/1 var(--body); font-variant-numeric: tabular-nums; padding: 7px 11px; border: 1px solid var(--rule); border-radius: 999px; color: var(--ink-soft); }
  .tag { font: 600 13px/1 var(--body); letter-spacing: 0.06em; text-transform: uppercase; color: var(--paper); background: var(--pick); padding: 7px 10px; border-radius: 999px; }
  .what { font-size: 18px; }
  .note { color: var(--ink-soft); }
  .shots { display: grid; grid-template-columns: 3fr 1fr; gap: 12px; align-items: start; }
  figure { margin: 0; display: grid; gap: 6px; min-width: 0; }
  figure img { display: block; width: 100%; height: auto; border: 1px solid var(--rule); border-radius: 6px; }
  figcaption { font-size: 13px; color: var(--ink-soft); letter-spacing: 0.02em; }
  @media (max-width: 640px) {
    .shots { grid-template-columns: 1fr; }
    .shots figure:last-child { width: 62%; }
  }
"""


def section(c):
    k = c["key"]
    tag = '<span class="tag">My pick</span>' if c["pick"] else ""
    return f"""  <section class="choice" aria-labelledby="{k}-name">
    <div class="head">
      <span class="letter">{k.upper()}</span>
      <h2 id="{k}-name">{c["name"]}</h2>
      <span class="score">{c["score"]} / 10</span>
      {tag}
    </div>
    <p class="what">{c["what"]}</p>
    <p class="note">{c["note"]}</p>
    <div class="shots">
      <figure><img src="{k}-laptop.jpg" alt="{c["name"]} by the park sign, laptop"><figcaption>Laptop</figcaption></figure>
      <figure><img src="{k}-phone.jpg" alt="{c["name"]} by the park sign, phone"><figcaption>Phone</figcaption></figure>
    </div>
    <figure><img src="{k}-close.jpg" alt="{c["name"]}, close-up"><figcaption>Close-up, full size</figcaption></figure>
  </section>
"""


def section2(c):
    k = c["key"]
    tag = '<span class="tag">My pick</span>' if c["pick"] else ""
    return f"""  <section class="choice" aria-labelledby="{k}-name">
    <div class="head">
      <span class="letter">{k.upper()}</span>
      <h2 id="{k}-name">{c["name"]}</h2>
      <span class="score">{c["score"]} / 10</span>
      {tag}
    </div>
    <p class="what">{c["what"]}</p>
    <p class="note">{c["note"]}</p>
    <div class="shots">
      <figure><img src="{k}-laptop.jpg" alt="{c["name"]} by the park sign, laptop"><figcaption>Laptop</figcaption></figure>
      <figure><img src="{k}-phone.jpg" alt="{c["name"]} by the park sign, phone"><figcaption>Phone</figcaption></figure>
    </div>
    <figure><img src="{k}-close.jpg" alt="{c["name"]}, close-up"><figcaption>Close-up, full size</figcaption></figure>
  </section>
"""


def main2():
    keys = [g["before"] for g in ROUND2] + [t["key"] for g in ROUND2 for t in g["takes"]]
    for key in keys:
        shots(key)
    body = ""
    for g in ROUND2:
        b = g["before"]
        body += f"""  <section class="scene" aria-labelledby="{b}-scene">
    <h2 id="{b}-scene" class="scene-title">{g["title"]}</h2>
    <figure class="before"><img src="{b}-close.jpg" alt="Last round's {g["title"]}, close-up"><figcaption>Last round, close-up</figcaption></figure>
  </section>
{"".join(section2(t) for t in g["takes"])}"""
    css = CSS + """  .scene { display: grid; gap: 12px; padding-top: 34px; border-top: 3px solid var(--ink); }
  .scene-title { font-size: clamp(30px, 5vw, 42px); }
  .before { width: min(100%, 640px); }
"""
    html = f"""<title>Footer Animal by the Sign</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Ysabeau:wght@500;650&display=swap">
<style>{css}</style>
<main>
  <header class="intro">
    <h1>The quail and the bear, as paintings</h1>
    <p>You asked for the quail and the bear cub to look more like paintings. Each is painted again two ways, in the two hands you already picked for the homepage, and laid on the real footer. The sign, its poppy and the words stay.</p>
    <ul>
      <li><b>1, wet wash:</b> a few soft wet washes, like the hummingbird at the top of the homepage.</li>
      <li><b>2, ink and wash:</b> brush lines with pale colour over them, like the Big Sur painting at its end.</li>
      <li>On a phone the sign keeps its seven lines. B, the tortoise, is as it was.</li>
    </ul>
  </header>
{body}</main>
"""
    (OUT / "footer-animal.html").write_text(html, encoding="utf-8", newline="\n")
    print("wrote", OUT / "footer-animal.html")


def main():
    for key in ["now"] + [c["key"] for c in CHOICES]:
        shots(key)
    html = f"""<title>Footer Animal by the Sign</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Ysabeau:wght@500;650&display=swap">
<style>{CSS}</style>
<main>
  <header class="intro">
    <h1>Who stands by the park sign?</h1>
    <p>Part 5: the red-crowned crane at the bottom of every page reads as Chinese, like the old opening's crane did. Here are three California animals in its place, laid on the real footer. The sign, its poppy and the words stay.</p>
    <ul>
      <li>Each one looks at the sign's poppy, like the crane does today.</li>
      <li>The same painting on every page, in the sign's own quiet colours.</li>
      <li>On a phone the sign keeps its seven lines.</li>
    </ul>
  </header>
  <section class="choice" aria-labelledby="now-name">
    <div class="head"><h2 id="now-name">Today: the red-crowned crane</h2></div>
    <div class="shots">
      <figure><img src="now-laptop.jpg" alt="Today's footer with the crane, laptop"><figcaption>Laptop</figcaption></figure>
      <figure><img src="now-phone.jpg" alt="Today's footer with the crane, phone"><figcaption>Phone</figcaption></figure>
    </div>
  </section>
{"".join(section(c) for c in CHOICES)}</main>
"""
    (OUT / "footer-animal.html").write_text(html, encoding="utf-8", newline="\n")
    print("wrote", OUT / "footer-animal.html")


if __name__ == "__main__":
    main2() if sys.argv[1:] == ["2"] or not sys.argv[1:] else main()

"""Part 4's page for Mo (October 30 - November 2, 2026): three California closing paintings for "Our
purpose is simple. Help you live fully.", each shot on the live homepage by shoot_purpose.py.

    python -X utf8 reference/ink-pages/home-purpose/make_purpose_mockup.py [2 | 3]

Round 2 (November 2): Mo tried A and B live and found the walk on the ridge doesn't give the vibe
of California; three more Californian walks. Round 3 (November 2): the coast walk, live, looked
"a little bit simple" next to the old pine painting; three richer Big Sur paintings.

Out: reference/ink-pages/mockups/home-purpose/ (home-purpose.html and its pictures).
"""

import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
SHOTS = HERE / "plates" / "shots"
OUT = HERE.parent / "mockups" / "home-purpose"

LOOKS = [
    {
        "key": "big-sur",
        "letter": "A",
        "name": "Big Sur at evening",
        "score": "8.5 / 10",
        "pick": False,
        "what": "The coast's green headland, the Pacific, the gold sun setting on the sea. Brown pelicans fly in as you scroll, where the cranes fly today.",
        "note": "The most beautiful place of the three. But it's only a place: nothing in it says \"live fully\".",
    },
    {
        "key": "ridge",
        "letter": "B",
        "name": "An evening walk on the ridge",
        "score": "9 / 10",
        "pick": True,
        "what": "An older couple and their dog walk a golden ridge toward the sea and the setting sun. The pelicans fly in above them.",
        "note": "It shows the words: people living fully. The one worry: golden hills are also About's first screen (there in spring poppies, here an evening walk).",
    },
    {
        "key": "beach",
        "letter": "C",
        "name": "A surfer at low tide",
        "score": "8 / 10",
        "pick": False,
        "what": "A surfer walks out across the wet sand toward the waves, the sun low on the sea, the pelicans above.",
        "note": "As California as it gets. But a surfer reads young and sporty for older readers, and the figure is the most detailed thing in it.",
    },
]


ROUND2 = [
    {
        "key": "coast-walk",
        "letter": "1",
        "name": "The walk on the Big Sur coast",
        "score": "9 / 10",
        "pick": True,
        "what": "The same couple and dog walk a cliff-top trail above the Pacific, poppies by the path, the sun setting on the sea.",
        "note": "A's coast with B's people: you know it's California, and it shows living fully. On a phone the people are small, at the left edge.",
    },
    {
        "key": "oak-walk",
        "letter": "2",
        "name": "The walk among oaks and poppies",
        "score": "8.5 / 10",
        "pick": False,
        "what": "The same ridge, now with a big California valley oak, orange poppies and purple lupine along the trail, the sea behind.",
        "note": "The most California of the three, and the best on a phone. But About already has both: its first screen is poppies on golden hills, and its purpose is a big valley oak. The homepage would echo it.",
    },
    {
        "key": "palm-walk",
        "letter": "3",
        "name": "The walk under palm trees",
        "score": "8 / 10",
        "pick": False,
        "what": "A bluff-top path by the ocean, a row of tall palms, the couple and dog walking toward the sunset.",
        "note": "Postcard California. But it reads beach town and Los Angeles more than calm health, and the tall trunks cut across the sky near the words.",
    },
]

INTRO2 = """<header class="intro">
    <h1>A more California walk</h1>
    <p>You found the walk on the ridge didn't feel like California: bare golden hills could be anywhere. Three ways to fix it, each laid on the real homepage. The words, the gold sun and the pelicans stay.</p>
  </header>"""


ROUND3 = [
    {
        "key": "rich-long",
        "letter": "1",
        "name": "The long view down the coast",
        "score": "9 / 10",
        "pick": True,
        "what": "The couple and their dog on the cliff-top trail, headland after headland fading into the evening haze, Bixby Bridge small in the middle, the sun's path glittering on the sea.",
        "note": "The depth and light of the old painting, and the bridge says Big Sur at once. On a phone the painting is shown smaller, so both the walkers and the sun fit.",
    },
    {
        "key": "rich-same",
        "letter": "2",
        "name": "Today's view, painted richer",
        "score": "8.5 / 10",
        "pick": False,
        "what": "The scene that is live now, repainted: more coast behind it, gold light on the cliffs, long swells and glitter on the sea.",
        "note": "Much richer than today's, but nothing in it you would remember on its own.",
    },
    {
        "key": "rich-falls",
        "letter": "3",
        "name": "McWay Falls",
        "score": "9 / 10",
        "pick": False,
        "what": "From the trail you look down on Big Sur's waterfall dropping onto a little beach, a turquoise cove and rocks, the coast fading behind.",
        "note": "The most \"wow\", and a real Big Sur landmark. But the cove's rocks make the foot busier, and the waterfall is small at laptop size.",
    },
]

INTRO3 = """<header class="intro">
    <h1>Big Sur, painted richer</h1>
    <p>You found the live ending a little simple next to the old pine painting. These three are painted at the old one's level: deep layers fading into the haze, gold evening light, fine brushwork up close. Each is laid on the real homepage; the words, the gold sun and the pelicans stay.</p>
  </header>"""


def jpg(src, name, width):
    im = Image.open(src).convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(OUT / name, "JPEG", quality=84, optimize=True)


def choice(look):
    k = look["key"]
    jpg(SHOTS / f"{k}-1440.png", f"{k}-laptop.jpg", 1500)
    jpg(SHOTS / f"{k}-390.png", f"{k}-phone.jpg", 620)
    tag = '<span class="tag">My pick</span>' if look["pick"] else ""
    return f"""<section class="choice" aria-labelledby="{k}-name">
    <div class="head">
      <span class="letter">{look['letter']}</span>
      <h2 id="{k}-name">{look['name']}</h2>
      <span class="score">{look['score']}</span>
      {tag}
    </div>
    <p class="what">{look['what']}</p>
    <p class="note">{look['note']}</p>
    <div class="shots">
      <figure><img src="{k}-laptop.jpg" alt="{look['name']} on the homepage, laptop"><figcaption>Laptop</figcaption></figure>
      <figure><img src="{k}-phone.jpg" alt="{look['name']} on the homepage, phone"><figcaption>Phone</figcaption></figure>
    </div>
  </section>"""


PAGE = """<title>Our Purpose Painting</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Ysabeau:wght@500;650&display=swap">
<style>
  /* Layout: one column; each idea is its words, then the laptop and phone screens of the real
     homepage. */
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
  .today { width: min(100%, 560px); }
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
</style>
<main>
  <header class="intro">
    <h1>Our purpose, without the pine and the cranes</h1>
    <p>Three California endings for the homepage. Each is laid on the real page; the words stay.</p>
    <ul>
      <li>All three are evening: the page opens in the morning sequoias and ends at sunset, one full day.</li>
      <li>The gold sun is the same gold leaf as the opening's.</li>
      <li>The painting is a little taller than today's, so the land stays clear of the words.</li>
    </ul>
    <figure class="today"><img src="today.jpg" alt="Today's closing painting on the homepage"><figcaption>Today: the pine, the misty peaks and the cranes</figcaption></figure>
  </header>
  __CHOICES__
</main>
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if sys.argv[1:] == ["3"]:
        page = PAGE.split("<main>")[0] + "<main>\n  " + INTRO3 + "\n  __CHOICES__\n</main>\n"
        html = page.replace("__CHOICES__", "\n  ".join(choice(look) for look in ROUND3))
        (OUT / "home-purpose.html").write_text(html, encoding="utf-8", newline="\n")
        return
    if sys.argv[1:] == ["2"]:
        page = PAGE.split("<main>")[0] + "<main>\n  " + INTRO2 + "\n  __CHOICES__\n</main>\n"
        html = page.replace("__CHOICES__", "\n  ".join(choice(look) for look in ROUND2))
        (OUT / "home-purpose.html").write_text(html, encoding="utf-8", newline="\n")
        return
    jpg(SHOTS / "today-1440.png", "today.jpg", 1120)
    html = PAGE.replace("__CHOICES__", "\n  ".join(choice(look) for look in LOOKS))
    (OUT / "home-purpose.html").write_text(html, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()

"""Part 9's page for Mo (November 6, 2026): "In their own words." without the plum blossom and tea
bowl. Each idea is the first story's still life, shot on the live homepage by shoot_stories.py (its
own <img> swapped, laptop and phone), with how the other two stories would follow.

    python -X utf8 reference/ink-pages/home-stories/make_stories_mockup.py

Out: reference/ink-pages/mockups/home-stories/ (home-stories.html and its pictures).
"""

import json
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
SHOTS = HERE / "plates" / "shots"
OUT = HERE.parent / "mockups" / "home-stories"
LOOKS = json.loads((HERE / "mockup-looks.json").read_text(encoding="utf-8"))


def jpg(src, name, width, box=None):
    im = Image.open(src).convert("RGB")
    if box:
        im = im.crop(box)
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(OUT / name, "JPEG", quality=84, optimize=True)
    return im.size


def choice(look):
    t = look["take"]
    jpg(SHOTS / f"{t}-1440.png", f"{t}-laptop.jpg", 1500)
    jpg(SHOTS / f"{t}-390.png", f"{t}-phone.jpg", 620)
    tag = '<span class="tag">My pick</span>' if look["pick"] else ""
    rest = "".join(f"<li>{line}</li>" for line in look["rest"])
    return f"""<section class="choice" aria-labelledby="{t}-name">
    <div class="head">
      <span class="letter">{look['letter']}</span>
      <h2 id="{t}-name">{look['name']}</h2>
      <span class="score">{look['score']}</span>
      {tag}
    </div>
    <p class="what">{look['what']}</p>
    <p class="note">{look['note']}</p>
    <div class="shots">
      <figure><img src="{t}-laptop.jpg" alt="{look['name']} on the homepage, laptop"><figcaption>Laptop</figcaption></figure>
      <figure><img src="{t}-phone.jpg" alt="{look['name']} on the homepage, phone"><figcaption>Phone</figcaption></figure>
    </div>
    <div class="rest"><p>The other two stories, in the same place:</p><ul>{rest}</ul></div>
  </section>"""


PAGE = """<title>Stories Painting</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Ysabeau:wght@500;650&display=swap">
<style>
  /* Layout: one column; each idea is its words, the laptop and phone screens of the real
     homepage, then how the other two stories follow. */
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
  .rest { display: grid; gap: 4px; color: var(--ink-soft); }
  .rest ul { margin: 0; padding-left: 1.2em; display: grid; gap: 4px; }
  @media (max-width: 640px) {
    .shots { grid-template-columns: 1fr; }
    .shots figure:last-child { width: 62%; }
  }
</style>
<main>
  <header class="intro">
    <h1>In their own words, without the tea bowl</h1>
    <p>__INTRO__</p>
    <figure class="today"><img src="today.jpg" alt="Today's blossom, tea bowl and pear on the homepage"><figcaption>Today: plum blossom, tea bowl, sliced pear</figcaption></figure>
  </header>
  __CHOICES__
</main>
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    jpg(SHOTS / "today-1440.png", "today.jpg", 1120)
    html = PAGE.replace("__INTRO__", LOOKS["intro"]).replace(
        "__CHOICES__", "\n  ".join(choice(look) for look in LOOKS["looks"])
    )
    (OUT / "home-stories.html").write_text(html, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()

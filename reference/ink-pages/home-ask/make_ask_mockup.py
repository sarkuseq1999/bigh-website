"""Part 3's page for Mo (October 30, 2026): three California pictures for "Good questions deserve
clear answers.", each shot on the live homepage by shoot_ask.py (its own <img> swapped, laptop and
phone), with the picture up close.

    python -X utf8 reference/ink-pages/home-ask/make_ask_mockup.py <shot of today's laptop screen>

Out: reference/ink-pages/mockups/home-ask/ (home-ask.html and its pictures).
"""

import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
SHOTS = HERE / "plates" / "shots"
OUT = HERE.parent / "mockups" / "home-ask"

CLOSE = (1040, 480, 1840, 1100)  # the picture and its caption on the 2x laptop shot

LOOKS = [
    {
        "take": "mailbox-4",
        "letter": "A",
        "name": "A country mailbox",
        "score": "9 / 10",
        "pick": True,
        "what": "Its flag is up, in gold leaf. You send your question, and an answer comes back.",
        "note": "Plainly American, and you get it in one look. The one stretch: Ask BiGH Science won't be real mail, so this is a picture of the idea.",
    },
    {
        "take": "gold-pan-3",
        "letter": "B",
        "name": "A Gold Rush pan",
        "score": "8 / 10",
        "pick": False,
        "what": "A prospector's pan and pick in a creek, a few flakes of gold left in the pan. Sift through it all until only what's true remains.",
        "note": "The most California idea, but you have to think for a second. Without the pick it looked like a kitchen bowl, and a pick is an odd thing to see on a health site.",
    },
    {
        "take": "field-book-3",
        "letter": "C",
        "name": "A naturalist's notebook",
        "score": "8 / 10",
        "pick": False,
        "what": "A pressed poppy and a hand lens on an open page. Someone looked closely and noted what they found.",
        "note": "Pretty and calm, and the closest to science. But the story just above it on the page already shows an open book.",
    },
]


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
    jpg(SHOTS / f"{t}-1440.png", f"{t}-close.jpg", 800, CLOSE)
    jpg(SHOTS / f"{t}-1440.png", f"{t}-laptop.jpg", 1500)
    jpg(SHOTS / f"{t}-390.png", f"{t}-phone.jpg", 620)
    tag = '<span class="tag">My pick</span>' if look["pick"] else ""
    return f"""<section class="choice" aria-labelledby="{t}-name">
    <div class="head">
      <span class="letter">{look['letter']}</span>
      <h2 id="{t}-name">{look['name']}</h2>
      <span class="score">{look['score']}</span>
      {tag}
    </div>
    <p class="what">{look['what']}</p>
    <p class="note">{look['note']}</p>
    <figure class="close"><img src="{t}-close.jpg" alt="{look['name']}, up close on the page"></figure>
    <div class="shots">
      <figure><img src="{t}-laptop.jpg" alt="{look['name']} on the homepage, laptop"><figcaption>Laptop</figcaption></figure>
      <figure><img src="{t}-phone.jpg" alt="{look['name']} on the homepage, phone"><figcaption>Phone</figcaption></figure>
    </div>
  </section>"""


PAGE = """<title>Good Questions Picture</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Ysabeau:wght@500;650&display=swap">
<style>
  /* Layout: one column; each idea is its words, the picture up close, then the laptop and phone
     screens of the real homepage. */
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
  .today { width: min(100%, 420px); }
  .choice { display: grid; gap: 14px; padding-top: 26px; border-top: 1px solid var(--rule); }
  .head { display: flex; flex-wrap: wrap; align-items: baseline; gap: 10px 16px; }
  .letter { font-family: var(--title); font-size: clamp(44px, 7vw, 60px); line-height: 0.8; color: var(--gold); font-weight: 650; }
  .score { font: 600 15px/1 var(--body); font-variant-numeric: tabular-nums; padding: 7px 11px; border: 1px solid var(--rule); border-radius: 999px; color: var(--ink-soft); }
  .tag { font: 600 13px/1 var(--body); letter-spacing: 0.06em; text-transform: uppercase; color: var(--paper); background: var(--pick); padding: 7px 10px; border-radius: 999px; }
  .what { font-size: 18px; }
  .note { color: var(--ink-soft); }
  .close { width: min(100%, 560px); }
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
    <h1>Good questions, without the inkstone</h1>
    <p>Three California pictures to take its place. Each is laid on the real homepage. Only the picture changes: the words and the button stay.</p>
    <figure class="today"><img src="today.jpg" alt="Today's inkstone and brush on the homepage"><figcaption>Today: the inkstone and brush</figcaption></figure>
  </header>
  __CHOICES__
</main>
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    jpg(sys.argv[1], "today.jpg", 840, (780, 340, 1380, 840))
    html = PAGE.replace("__CHOICES__", "\n  ".join(choice(look) for look in LOOKS))
    (OUT / "home-ask.html").write_text(html, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()

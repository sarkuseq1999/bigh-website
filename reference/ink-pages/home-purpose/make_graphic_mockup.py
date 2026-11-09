"""Part 10's page for Mo (November 9, 2026): "Small beginnings. Bigger possibilities." in the title
face, shot on the live homepage by shoot_graphic.py (laptop and phone).

    python -X utf8 reference/ink-pages/home-purpose/make_graphic_mockup.py

Out: reference/ink-pages/mockups/home-graphic/ (home-graphic.html and its pictures).
"""

from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
SHOTS = HERE / "plates" / "graphic"
OUT = HERE.parent / "mockups" / "home-graphic"
BAND = (0, 240, 2880, 1200)  # the words and the close's foot on the 2x laptop shot

LOOKS = [
    ("today", "Today", "", "The plain body font, heavy, with a grey second line. No other title on the page looks like this.", False),
    ("a", "A", "The title face, second line still grey", "The brush-like title face every other heading uses. The second line stays grey, as now.", False),
    ("b", "B", "The title face, both lines in ink", "The same face, and both lines in ink like every other title on the page. The grey second line was the only one on the homepage.", True),
]


def jpg(src, name, width, box=None):
    im = Image.open(src).convert("RGB")
    if box:
        im = im.crop(box)
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(OUT / name, "JPEG", quality=84, optimize=True)


def block(key, letter, name, what, pick):
    jpg(SHOTS / f"{key}-1440.png", f"{key}-laptop.jpg", 1500, BAND)
    jpg(SHOTS / f"{key}-390.png", f"{key}-phone.jpg", 620)
    head = f'<span class="letter">{letter}</span><h2>{name}</h2>' if name else f"<h2>{letter}</h2>"
    tag = '<span class="tag">My pick</span>' if pick else ""
    return f"""<section class="choice">
    <div class="head">{head}{tag}</div>
    <p class="what">{what}</p>
    <div class="shots">
      <figure><img src="{key}-laptop.jpg" alt="{letter} on the homepage, laptop"><figcaption>Laptop</figcaption></figure>
      <figure><img src="{key}-phone.jpg" alt="{letter} on the homepage, phone"><figcaption>Phone</figcaption></figure>
    </div>
  </section>"""


PAGE = """<title>Small Beginnings Heading</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Ysabeau:wght@500;650&display=swap">
<style>
  /* Layout: one column; today, then each look: its words, the laptop band and the phone screen. */
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
  main { max-width: 1100px; margin: 0 auto; padding-block: 40px 72px; display: grid; gap: 44px; }
  h1, h2 { font-family: var(--title); font-weight: 650; text-wrap: balance; margin: 0; letter-spacing: -0.01em; }
  h1 { font-size: clamp(34px, 6vw, 52px); line-height: 1.05; }
  h2 { font-size: clamp(24px, 4vw, 32px); line-height: 1.1; }
  p { margin: 0; max-width: 62ch; }
  .intro { display: grid; gap: 12px; }
  .intro p { color: var(--ink-soft); font-size: 18px; }
  .choice { display: grid; gap: 14px; padding-top: 24px; border-top: 1px solid var(--rule); }
  .head { display: flex; flex-wrap: wrap; align-items: baseline; gap: 10px 16px; }
  .letter { font-family: var(--title); font-size: clamp(44px, 7vw, 60px); line-height: 0.8; color: var(--gold); font-weight: 650; }
  .tag { font: 600 13px/1 var(--body); letter-spacing: 0.06em; text-transform: uppercase; color: var(--paper); background: var(--pick); padding: 7px 10px; border-radius: 999px; }
  .what { font-size: 18px; }
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
    <h1>Small beginnings, in the title face</h1>
    <p>Under the Big Sur painting at the end of the homepage. Only the font and colour change; the words stay. Each look is laid on the real homepage.</p>
  </header>
  __BLOCKS__
</main>
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    html = PAGE.replace("__BLOCKS__", "\n  ".join(block(*look) for look in LOOKS))
    (OUT / "home-graphic.html").write_text(html, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()

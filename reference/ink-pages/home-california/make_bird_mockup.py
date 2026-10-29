"""Part 2's page for Mo (October 29, 2026): three hummingbird looks, each with its wings beating,
laid on the live homepage.

The live first screen is shot with its bird hidden and the line kept (desktop 1440 x 900 and a
390 x 844 phone, both at 2x), with the bird's frame box measured; each look's wingless body and
its two wing sprites (build_wings.py) are laid back into that box in the page, so the wings beat
in Mo's browser exactly as they would on the site: six frames a beat, ten beats a second, the far
wing behind the body and the near wing over it, the whole bird riding the air as it does live.

    python -X utf8 reference/ink-pages/home-california/make_bird_mockup.py <birdless dir>

<birdless dir> holds desktop.png, phone.png and rects.json (from the shooting script). Out:
reference/ink-pages/mockups/home-bird/ (home-bird.html and its pictures).
"""

import json
import shutil
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
WINGS = HERE / "plates" / "wings"
OUT = HERE.parent / "mockups" / "home-bird"
DENSITY = 2  # both shots are 2x

# Round 2 (Mo, October 29: "Allen's is pretty good. But can we try to make them look more
# painting-like?"). Round 1 (today's Anna's, a green female, Allen's) is in git history.
LOOKS = [
    {
        "key": "allens",
        "letter": "A",
        "name": "Allen's, as shown before",
        "score": "8 / 10",
        "what": "The copper bird from the last page: fine brushwork, every feather speckled in.",
        "note": "Pretty, but it reads more like a field-guide picture than a painting.",
    },
    {
        "key": "allens-loose",
        "letter": "B",
        "name": "A little looser",
        "score": "8 / 10",
        "what": "Softer washes on the breast, wings of quick dry strokes.",
        "note": "A step toward a painting, but up close the body still has the same fine speckle.",
    },
    {
        "key": "allens-few",
        "letter": "C",
        "name": "Painted in a few strokes",
        "score": "9 / 10",
        "pick": True,
        "what": "A fresh painting: a few wet washes of copper and green that bleed into each other, wings of pale grey strokes, bare paper for the breast.",
        "note": "Clearly a painting, in the hand of the old crane. Its orange came out loud, so it is calmed toward the redwood's copper and the gold sun still leads.",
    },
]

# Each view: which shot, and the part of it shown (css px: x, y, w, h).
VIEWS = {
    "close": ("desktop", (330, 140, 400, 250), "Up close, laptop"),
    "desktop": ("desktop", (0, 0, 1440, 900), "Laptop, 1440 wide"),
    "phone": ("phone", (0, 0, 390, 844), "Phone"),
}


def pct(v):
    return f"{v:.4f}%"


def scene(look, view, shots, rects, rigs):
    shot, (cx, cy, cw, ch), caption = VIEWS[view]
    sw, sh = shots[shot]
    sw, sh = sw / DENSITY, sh / DENSITY
    r = rects[shot]
    box = rigs[look["key"]]["box"]
    k = look["key"]
    img_style = f"width:{pct(sw / cw * 100)};left:{pct(-cx / cw * 100)};top:{pct(-cy / ch * 100)}"
    bird_style = (
        f"left:{pct((r['x'] - cx) / cw * 100)};top:{pct((r['y'] - cy) / ch * 100)};"
        f"width:{pct(r['w'] / cw * 100)};height:{pct(r['h'] / ch * 100)}"
    )
    wing_style = f"left:{box['left']}%;top:{box['top']}%;width:{box['width']}%;height:{box['height']}%"
    alt = f"{look['name']} on the homepage ({caption.lower()})"
    return f"""<figure class="view view-{view}">
        <div class="scene" style="aspect-ratio:{cw}/{ch}" role="img" aria-label="{alt}">
          <img class="shot" src="{shot}.jpg" alt="" style="{img_style}">
          <div class="bird" style="{bird_style}">
            <span class="wing" style="{wing_style};background-image:url({k}-far.webp)"></span>
            <img class="body" src="{k}-body.webp" alt="">
            <span class="wing" style="{wing_style};background-image:url({k}-near.webp)"></span>
          </div>
        </div>
        <figcaption>{caption}</figcaption>
      </figure>"""


def section(look, shots, rects, rigs):
    tag = '<span class="tag">My pick</span>' if look.get("pick") else ""
    views = "\n      ".join(scene(look, v, shots, rects, rigs) for v in VIEWS)
    return f"""<section class="choice" aria-labelledby="{look['key']}-name">
    <div class="head">
      <span class="letter">{look['letter']}</span>
      <h2 id="{look['key']}-name">{look['name']}</h2>
      <span class="score">{look['score']}</span>
      {tag}
    </div>
    <p class="what">{look['what']}</p>
    <p class="note">{look['note']}</p>
    <div class="shots">
      {views}
    </div>
  </section>"""


PAGE = """<title>Hummingbird Looks</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Ysabeau:wght@500;650&display=swap">
<style>
  /* Layout: one column; each look is a close-up, then the laptop and phone screens. The bird in
     each is the live homepage's bird box, its wings beating as they would on the site. */
  :root {
    --paper: #f6f1e7;
    --sheet: #fbf8f2;
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
      --paper: #1b1a17; --sheet: #24221e; --ink: #f1ece2; --ink-soft: #b9b0a2;
      --rule: #3a3630; --gold: #d6aa52; --pick: #9cc3a8; color-scheme: dark;
    }
  }
  :root[data-theme="dark"] {
    --paper: #1b1a17; --sheet: #24221e; --ink: #f1ece2; --ink-soft: #b9b0a2;
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
  .choice { display: grid; gap: 14px; padding-top: 26px; border-top: 1px solid var(--rule); }
  .head { display: flex; flex-wrap: wrap; align-items: baseline; gap: 10px 16px; }
  .letter { font-family: var(--title); font-size: clamp(44px, 7vw, 60px); line-height: 0.8; color: var(--gold); font-weight: 650; }
  .score { font: 600 15px/1 var(--body); font-variant-numeric: tabular-nums; padding: 7px 11px; border: 1px solid var(--rule); border-radius: 999px; color: var(--ink-soft); }
  .tag { font: 600 13px/1 var(--body); letter-spacing: 0.06em; text-transform: uppercase; color: var(--paper); background: var(--pick); padding: 7px 10px; border-radius: 999px; }
  .what { font-size: 18px; }
  .note { color: var(--ink-soft); }
  .shots { display: grid; grid-template-columns: 3fr 1fr; gap: 12px; align-items: start; }
  .view-close { grid-column: 1 / -1; width: min(100%, 680px); }
  figure { margin: 0; display: grid; gap: 6px; min-width: 0; }
  figcaption { font-size: 13px; color: var(--ink-soft); letter-spacing: 0.02em; }

  /* A shot of the live page, cut to the view, the bird laid back in its own box. */
  .scene { position: relative; overflow: hidden; border-radius: 6px; border: 1px solid var(--rule); background: #f4efe4; }
  .shot { position: absolute; max-width: none; height: auto; display: block; }
  .bird {
    position: absolute;
    transform-origin: 62% 60%;
    animation: ride 13s ease-in-out infinite alternate, pitch 21s ease-in-out -3s infinite alternate;
  }
  .body { position: absolute; inset: 0; width: 100%; height: 100%; display: block; }
  .wing {
    position: absolute;
    background-size: 600% 100%;
    background-repeat: no-repeat;
    animation: beat 0.1s steps(6) infinite;
  }
  @keyframes beat { from { background-position: 0 0; } to { background-position: 120% 0; } }
  @keyframes ride { from { translate: -0.15% 0.9%; } to { translate: 0.15% -0.9%; } }
  @keyframes pitch { from { rotate: 0.3deg; } to { rotate: -0.45deg; } }

  @media (max-width: 720px) {
    body { font-size: 16px; }
    main { gap: 40px; padding-block: 24px 56px; }
    .shots { grid-template-columns: 1fr; }
    .view-phone { width: min(100%, 300px); justify-self: center; }
  }
</style>

<main>
  <header class="intro">
    <h1>The hummingbird</h1>
    <p>Allen's hummingbird three ways, from today's brushwork to a loose painting, each laid on the live homepage. On all three the wings never stop: about ten beats a second, blurred the way your eye sees a real hummingbird.</p>
    <p>For visitors whose phone asks for less motion, the wings would rest in the raised pose. Nothing on the live site has changed.</p>
  </header>

  %SECTIONS%
</main>
"""


def main():
    src = Path(sys.argv[1])
    OUT.mkdir(parents=True, exist_ok=True)
    rects = json.loads((src / "rects.json").read_text(encoding="utf-8"))
    shots = {}
    for name in ("desktop", "phone"):
        img = Image.open(src / f"{name}.png").convert("RGB")
        shots[name] = img.size
        img.save(OUT / f"{name}.jpg", quality=86, optimize=True, progressive=True)
    rigs = {}
    for look in LOOKS:
        k = look["key"]
        rigs[k] = json.loads((WINGS / k / "rig.json").read_text(encoding="utf-8"))
        body = Image.open(WINGS / k / "body.png")
        body.thumbnail((1000, 1000), Image.LANCZOS)
        body.save(OUT / f"{k}-body.webp", quality=88, method=6)
        for side in ("near", "far"):
            shutil.copyfile(WINGS / k / f"{side}.webp", OUT / f"{k}-{side}.webp")
    html = PAGE.replace("%SECTIONS%", "\n\n  ".join(section(look, shots, rects, rigs) for look in LOOKS))
    (OUT / "home-bird.html").write_text(html, encoding="utf-8", newline="\n")
    for f in sorted(OUT.iterdir()):
        print(f.name, f.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()

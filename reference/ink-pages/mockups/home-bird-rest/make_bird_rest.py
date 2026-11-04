"""Mockup for Mo (November 4, 2026): the homepage hummingbird's wings beat as it arrives, then rest.

Shoots the built homepage (desktop 1440x900 and phone 390x844) with the bird hidden, notes the
bird's box, and writes bird-rest.html: the live bird and wings laid back on each shot with the
site's new timing (3 s at ten beats a second, three slower beats, then the first frame, raised as
painted), a fade standing in for the ink bloom, and a Play again button.

    python -X utf8 make_bird_rest.py [base-url]   (default http://localhost:3006)
"""

import shutil
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
ROOT = HERE.parents[3]
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3006"
INK = ROOT / "public" / "images" / "home-v2" / "ink"
BOX = {"left": 16.19, "top": 14.174, "width": 45.644, "height": 76.931}
VIEWS = (("desktop", 1440, 900, False), ("phone", 390, 844, True))


def pct(v):
    return f"{v:.4f}%"


def shoot():
    rects = {}
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=["--use-angle=d3d11"])
        for name, w, h, mobile in VIEWS:
            ctx = b.new_context(viewport={"width": w, "height": h}, is_mobile=mobile, has_touch=mobile,
                                device_scale_factor=2 if mobile else 1)
            p = ctx.new_page()
            p.goto(BASE + "/", wait_until="networkidle", timeout=120000)
            p.wait_for_timeout(6000)
            r = p.evaluate("(() => { const r = document.querySelector('#top [data-brush=crane]').getBoundingClientRect();"
                           " return [r.x, r.y, r.width, r.height]; })()")
            p.add_style_tag(content="#top [data-brush=crane]{visibility:hidden!important}")
            p.wait_for_timeout(300)
            p.screenshot(path=str(HERE / f"{name}.jpg"), type="jpeg", quality=88)
            rects[name] = (r, w, h)
            ctx.close()
        b.close()
    return rects


def bird(r, w, h):
    x, y, bw, bh = r
    style = f"left:{pct(x / w * 100)};top:{pct(y / h * 100)};width:{pct(bw / w * 100)};height:{pct(bh / h * 100)}"
    wing = (f"left:{BOX['left']}%;top:{BOX['top']}%;width:{BOX['width']}%;height:{BOX['height']}%;"
            "background-image:url({src})")
    return (f'<div class="bird" style="{style}">'
            f'<span class="wing" style="{wing.format(src="hummingbird-v2-far.webp")}"></span>'
            '<img class="body" src="hummingbird-v2.webp" alt="">'
            f'<span class="wing" style="{wing.format(src="hummingbird-v2-near.webp")}"></span></div>')


def page(rects):
    d, dw, dh = rects["desktop"]
    m, mw, mh = rects["phone"]
    return f"""<title>Hummingbird Wings</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Ysabeau:wght@500;650&display=swap">
<style>
  /* One column: the laptop screen, then the phone, each the built homepage with its bird laid
     back on it, wings timed as on the site. Play again restarts both. */
  :root {{
    --paper: #f6f1e7; --ink: #1d1b18; --ink-soft: #5d574e; --rule: #ddd4c4; --gold: #a77c25;
    --title: "Ysabeau", "Palatino Linotype", Palatino, Georgia, serif;
    --body: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{ --paper: #1b1a17; --ink: #f1ece2; --ink-soft: #b9b0a2; --rule: #3a3630; --gold: #d6aa52; color-scheme: dark; }}
  }}
  :root[data-theme="dark"] {{ --paper: #1b1a17; --ink: #f1ece2; --ink-soft: #b9b0a2; --rule: #3a3630; --gold: #d6aa52; color-scheme: dark; }}
  body {{ background: var(--paper); color: var(--ink); font: 17px/1.55 var(--body); margin: 0;
    padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }}
  main {{ max-width: 1100px; margin: 0 auto; padding-block: 40px 72px; display: grid; gap: 28px; }}
  h1 {{ font-family: var(--title); font-weight: 650; font-size: clamp(34px, 6vw, 52px); line-height: 1.05; margin: 0; letter-spacing: -0.01em; }}
  p {{ margin: 0; max-width: 62ch; }}
  .intro {{ display: grid; gap: 12px; }}
  .intro p {{ color: var(--ink-soft); font-size: 18px; }}
  .bar {{ display: flex; flex-wrap: wrap; gap: 12px 18px; align-items: center; position: sticky; top: 0; z-index: 2;
    background: var(--paper); padding-block: 10px; }}
  button {{ font: 600 17px/1 var(--body); color: var(--paper); background: var(--ink); border: 0; border-radius: 999px; padding: 14px 22px; min-height: 48px; cursor: pointer; }}
  .clock {{ font: 600 15px/1 var(--body); font-variant-numeric: tabular-nums; color: var(--ink-soft); }}
  .shots {{ display: grid; grid-template-columns: 3fr 1fr; gap: 12px; align-items: start; }}
  figure {{ margin: 0; display: grid; gap: 6px; min-width: 0; }}
  figcaption {{ font-size: 13px; color: var(--ink-soft); }}
  .scene {{ position: relative; overflow: hidden; border-radius: 6px; border: 1px solid var(--rule); background: #f4efe4; }}
  .shot {{ position: absolute; inset: 0; width: 100%; height: 100%; display: block; }}
  .bird {{ position: absolute; transform-origin: 62% 60%;
    animation: ride 6.5s ease-in-out infinite alternate, pitch 10.3s ease-in-out -3s infinite alternate; }}
  .body {{ position: absolute; inset: 0; width: 100%; height: 100%; display: block; }}
  .wing {{ position: absolute; background-size: 600% 100%; background-repeat: no-repeat; }}
  /* The site's timing (opening.module.css), started when the bird starts to show. */
  .play .bird {{ animation: arrive 3s ease 0.6s both, ride 6.5s ease-in-out infinite alternate, pitch 10.3s ease-in-out -3s infinite alternate; }}
  .play .wing {{ animation: beat 0.1s steps(6) 30, beat 0.16s steps(6) 3s 2, beat 0.24s steps(6) 3.32s 1; }}
  @keyframes arrive {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
  @keyframes beat {{ from {{ background-position: 0 0; }} to {{ background-position: 120% 0; }} }}
  @keyframes ride {{ from {{ translate: -0.15% 0.9%; }} to {{ translate: 0.15% -0.9%; }} }}
  @keyframes pitch {{ from {{ rotate: 0.3deg; }} to {{ rotate: -0.45deg; }} }}
  @media (max-width: 720px) {{
    body {{ font-size: 16px; }}
    main {{ padding-block: 24px 56px; }}
    .shots {{ grid-template-columns: 1fr; }}
    .phone {{ width: min(100%, 300px); justify-self: center; order: -1; }}
  }}
</style>

<main>
  <header class="intro">
    <h1>The hummingbird's wings</h1>
    <p>Your pick, A: the wings beat while the bird appears, slow down over three beats, then rest, raised as painted. About 3.5 seconds of beating, then still.</p>
    <p>Built on the real homepage, not live yet. If you scroll down before it finishes, the beat waits and finishes when you come back up.</p>
  </header>
  <div class="bar">
    <button type="button" id="again">Play again</button>
    <span class="clock" id="clock" aria-live="off"></span>
  </div>
  <div class="shots" id="shots">
    <figure>
      <div class="scene" style="aspect-ratio:{dw}/{dh}" role="img" aria-label="The homepage on a laptop, the hummingbird's wings beating, then at rest">
        <img class="shot" src="desktop.jpg" alt="">
        {bird(d, dw, dh)}
      </div>
      <figcaption>Laptop, 1440 wide</figcaption>
    </figure>
    <figure class="phone">
      <div class="scene" style="aspect-ratio:{mw}/{mh}" role="img" aria-label="The homepage on a phone, the hummingbird's wings beating, then at rest">
        <img class="shot" src="phone.jpg" alt="">
        {bird(m, mw, mh)}
      </div>
      <figcaption>Phone</figcaption>
    </figure>
  </div>
</main>
<script>
  const shots = document.getElementById("shots");
  const clock = document.getElementById("clock");
  let start = 0;
  function play() {{
    shots.classList.remove("play");
    void shots.offsetWidth;
    shots.classList.add("play");
    start = performance.now();
  }}
  function tick() {{
    const t = (performance.now() - start) / 1000;
    clock.textContent = t < 3.6 ? "Beating… " + t.toFixed(1) + " s" : "At rest";
    requestAnimationFrame(tick);
  }}
  document.getElementById("again").addEventListener("click", play);
  play();
  tick();
</script>
"""


def main():
    rects = shoot()
    for f in ("hummingbird-v2.webp", "hummingbird-v2-near.webp", "hummingbird-v2-far.webp"):
        shutil.copy(INK / f, HERE / f)
    (HERE / "bird-rest.html").write_text(page(rects), encoding="utf-8", newline="\n")
    print(rects)


if __name__ == "__main__":
    main()

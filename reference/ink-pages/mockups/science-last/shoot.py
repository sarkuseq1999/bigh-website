"""Mockups for Mo (November 12, 2026, round 3 of the zoom's last view): the same grandfather and
child, now in a scene where something happens.

  python -X utf8 reference/ink-pages/mockups/science-last/shoot.py [base-url] [name ...]

Mo liked the pull-back from the cell to the hands and the pair, but found the last picture (the
pair walking away from us down the trail) "a little boring". Each choice is a Codex painting
(reference/ink-pages/science/originals/last-<idea>-<take>.png, and a tall take for phones). This
script divides out the paper (science/plates/last/, git-ignored), opens the Science page (the public
demo by default), scrolls to the zoom's last view, puts the painting in the hills' place (the kite's
gold-leaf kite rides on a layer of its own, made by gild_kite.py), and takes a desktop, a laptop
and a phone picture into science/plates/last/shots/. Nothing in src/ changes.
"""

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
SCIENCE = HERE.parent.parent / "science"
ORIG = SCIENCE / "originals"
PLATES = SCIENCE / "plates" / "last"
PLATES.mkdir(parents=True, exist_ok=True)
# Full-size shots stay in the git-ignored plates; review/ gets the small copies Mo sees.
OUT = PLATES / "shots"
OUT.mkdir(exist_ok=True)

args = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = (args[0] if args and args[0].startswith("http") else "https://bigh-website-demo.vercel.app").rstrip("/")
NAMES = [a for a in args if not a.startswith("http")]

# name: the wide take and the part a wide window keeps (object-position); the tall take for an
# upright window and the part it keeps; optional layers on top ([name, plate], plates of the same
# size made by gild_kite.py) and the point they sway about (shares of the painting).
CHOICES = json.loads((HERE / "choices.json").read_text(encoding="utf-8"))
WANT = NAMES or list(CHOICES)
SIZES = (("desk", 1440, 900, 1), ("laptop", 1280, 720, 1), ("phone", 390, 844, 2))


def plate(take: str) -> str:
    """The painting with its paper divided out, as the site ships its paintings (multiplied)."""
    dst = PLATES / f"{take}.webp"
    src = ORIG / f"{take}.png"
    if not src.exists():
        src = PLATES / f"{take}.png"  # a plate made by another script (already divided)
        Image.open(src).save(dst, "WEBP", quality=90, method=6)
        return dst.name
    a = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
    lum = a.mean(axis=2)
    paper = np.median(a[lum >= np.quantile(lum, 0.9)], axis=0)
    a = np.clip(a / paper * 255.0 * 1.04, 0, 255).astype(np.uint8)
    Image.fromarray(a).save(dst, "WEBP", quality=90, method=6)
    return dst.name


def serve(route):
    name = route.request.url.split("/__mock/", 1)[1].split("?")[0]
    path = PLATES / name
    route.fulfill(path=str(path)) if path.exists() else route.fulfill(status=404, body="missing " + name)


# Put the choice's painting in the hills' place (the tall one on an upright window), and its layers
# (if any) over it, framed the same way. The kite's layers sway about its lower point (where the
# string is tied on, so the string stays on): the kite a little, catching the light as gold leaf
# does as it tilts; the tail a little more and a beat behind it.
SWAP = """async ([src, position, layers, pivot]) => {
  const img = document.querySelector('[data-zoom-layer="hills"]');
  const pic = img.closest('picture');
  pic.querySelectorAll('source').forEach((s) => s.remove());
  img.removeAttribute('srcset');
  img.removeAttribute('sizes');
  img.src = '/__mock/' + src;
  img.style.objectPosition = position;
  const ready = (el) => new Promise((done) => (el.complete && el.naturalWidth ? done() : el.addEventListener('load', done, { once: true })));
  await ready(img);
  document.querySelectorAll('[data-mock-layer]').forEach((el) => el.remove());
  let after = img;
  for (const [name, file] of layers || []) {
    const top = img.cloneNode();
    top.removeAttribute('data-zoom-layer');
    top.alt = '';
    top.dataset.mockLayer = name;
    top.src = '/__mock/' + file;
    after.after(top);
    after = top;
    await ready(top);
    // The pivot in the window's pixels: the painting's share, moved by how the box crops it.
    const box = { w: top.offsetWidth, h: top.offsetHeight };
    const cover = Math.max(box.w / top.naturalWidth, box.h / top.naturalHeight);
    const drawn = { w: top.naturalWidth * cover, h: top.naturalHeight * cover };
    const at = position.split(' ').map((v) => parseFloat(v) / 100);
    const x = (box.w - drawn.w) * at[0] + drawn.w * pivot[0];
    const y = (box.h - drawn.h) * at[1] + drawn.h * pivot[1];
    top.style.transformOrigin = `${x}px ${y}px`;
  }
  if (!document.getElementById('mock-sway')) {
    const style = document.createElement('style');
    style.id = 'mock-sway';
    style.textContent = `
      @keyframes mock-kite { from { rotate: -3.6deg; } to { rotate: 3.8deg; } }
      @keyframes mock-tail { from { rotate: -6deg; } to { rotate: 6.5deg; } }
      @keyframes mock-glint { from { filter: brightness(1); } to { filter: brightness(1.1); } }
      [data-mock-layer="kite"] { animation: mock-kite 4.8s ease-in-out infinite alternate, mock-glint 4.8s ease-in-out infinite alternate; }
      [data-mock-layer="tail"] { animation: mock-tail 4.8s ease-in-out 0.7s infinite alternate both; }`;
    document.head.append(style);
  }
}"""
TO_END = """() => { const t = document.querySelector('[data-zoom]');
  scrollTo({ top: t.offsetTop + (t.offsetHeight - innerHeight), behavior: 'instant' }); }"""


def shoot(pg, key: str, size: str):
    choice = CHOICES.get(key)
    pg.goto(BASE + "/science", wait_until="networkidle")
    pg.wait_for_timeout(2500)
    pg.evaluate(TO_END)
    pg.wait_for_timeout(900)
    if choice:
        tall = size == "phone" and choice.get("tall")
        take = choice["tall"] if tall else choice["wide"]
        position = choice["tall_at"] if tall else choice["wide_at"]
        layers = choice.get("tall_layers" if tall else "layers") or []
        pivot = choice.get("tall_pivot" if tall else "pivot")
        pg.evaluate(SWAP, [plate(take), position, [[k, plate(v)] for k, v in layers], pivot])
        pg.wait_for_timeout(700)
    return pg


if __name__ == "__main__":
    with sync_playwright() as p:
        b = p.chromium.launch()
        for key in WANT:
            for size, w, h, dense in SIZES:
                ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=dense)
                ctx.route("**/__mock/**", serve)
                pg = ctx.new_page()
                shoot(pg, key, size)
                # The kite rests near the middle of its sway for the still.
                pg.evaluate("document.getAnimations().forEach(a => { if (a.animationName && a.animationName.startsWith('mock-')) { a.pause(); a.currentTime = 2400; } })")
                pg.wait_for_timeout(150)
                pg.screenshot(path=str(OUT / f"{key}-{size}.png"))
                ctx.close()
            print("shot", key, flush=True)
        b.close()

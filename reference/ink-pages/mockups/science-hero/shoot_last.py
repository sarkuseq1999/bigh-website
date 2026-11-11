"""Mockups for Mo (November 10, 2026, round 2): choices for the picture the zoom pulls back to.

  python -X utf8 reference/ink-pages/mockups/science-hero/shoot_last.py <base-url> [name ...]

Mo found the last view (the small walker on the hills) plain. Each choice is a Codex painting
(reference/ink-pages/science/originals/out-<name>-<take>.png); this script divides its paper out
(plates/out/, git-ignored), opens the built draft's Science page, scrolls to the zoom's last view
and puts the painting in the hills' place, then takes a desktop and a phone picture into last/
beside this script. Nothing in src/ changes.
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
SCIENCE = HERE.parent.parent / "science"
ORIG = SCIENCE / "originals"
PLATES = SCIENCE / "plates" / "out"
PLATES.mkdir(parents=True, exist_ok=True)
OUT = HERE / "last"
OUT.mkdir(exist_ok=True)

args = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = args[0].rstrip("/") if args else "http://localhost:3107"

# name: the take, which part a window keeps (object-position; desktop, phone), and for a phone how
# far down the painting starts (a share of the window; its own sky is bare paper, so the page's
# paper carries on above it) when the figure would otherwise stand under the words.
CHOICES = {
    "today": {"take": None},
    "near": {"take": "out-near-1", "desk": "60% 0%", "phone": "64% 100%", "drop": 0.12},
    "pair": {"take": "zoom-pair-1", "desk": "60% 30%", "phone": "71% 100%", "drop": 0.04},
    "grove": {"take": "out-grove-2", "desk": "62% 0%", "phone": "76% 100%", "drop": 0.31},
    "surf": {"take": "out-surf-1", "desk": "60% 40%", "phone": "73% 100%", "drop": 0.0},
}
WANT = args[1:] or list(CHOICES)
SIZES = (("desk", 1440, 900, 1), ("phone", 390, 844, 2))


def plate(take: str) -> Path:
    dst = PLATES / f"{take}.webp"
    a = np.asarray(Image.open(ORIG / f"{take}.png").convert("RGB")).astype(np.float32)
    # The paper: the median of the brightest tenth of the picture.
    lum = a.mean(axis=2)
    paper = np.median(a[lum >= np.quantile(lum, 0.9)], axis=0)
    a = np.clip(a / paper * 255.0 * 1.04, 0, 255).astype(np.uint8)
    Image.fromarray(a).save(dst, "WEBP", quality=88, method=6)
    return dst


def serve(route):
    name = route.request.url.split("/__mock/", 1)[1].split("?")[0]
    path = PLATES / name
    route.fulfill(path=str(path)) if path.exists() else route.fulfill(status=404, body="missing " + name)


SWAP = """async ([src, position, drop]) => {
  const img = document.querySelector('[data-zoom-layer="hills"]');
  img.removeAttribute('srcset');
  img.removeAttribute('sizes');
  img.src = '/__mock/' + src;
  img.style.objectPosition = position;
  if (drop) {
    img.style.top = (drop * 100) + '%';
    img.style.height = ((1 - drop) * 100) + '%';
    img.style.webkitMaskImage = img.style.maskImage = 'linear-gradient(transparent, #000 16%)';
  }
  await new Promise((done) => (img.complete && img.naturalWidth ? done() : img.addEventListener('load', done, { once: true })));
}"""
TO_END = """() => { const t = document.querySelector('[data-zoom]');
  scrollTo({ top: t.offsetTop + (t.offsetHeight - innerHeight), behavior: 'instant' }); }"""

with sync_playwright() as p:
    b = p.chromium.launch()
    for key in WANT:
        choice = CHOICES[key]
        if choice["take"]:
            plate(choice["take"])
        for name, w, h, dense in SIZES:
            ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=dense)
            ctx.route("**/__mock/**", serve)
            pg = ctx.new_page()
            pg.goto(BASE + "/en/science", wait_until="networkidle")
            pg.wait_for_timeout(2500)
            pg.evaluate(TO_END)
            pg.wait_for_timeout(900)
            if choice["take"]:
                phone = name == "phone"
                pg.evaluate(SWAP, [choice["take"] + ".webp", choice["phone" if phone else "desk"], choice["drop"] if phone else 0])
                pg.wait_for_timeout(700)
            pg.screenshot(path=str(OUT / f"{key}-{name}.png"))
            ctx.close()
        print("shot", key)
    b.close()
REVIEW = HERE / "review"
for shot in sorted(OUT.glob("*.png")):
    im = Image.open(shot).convert("RGB")
    width = 780 if shot.stem.endswith("-phone") else 1280
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(REVIEW / f"last-{shot.stem}.jpg", "JPEG", quality=86, optimize=True, progressive=True)
print("pictures in", OUT, "and", REVIEW)

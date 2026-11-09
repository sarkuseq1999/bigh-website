"""Part 9 of the homepage's California pass (November 6, 2026): "In their own words." The three
still lifes were painted as East Asian ink still lifes (plum blossom in a vase, tea bowls, a low
table) and read as Asian. Each take for the first story (Lisa, "It fits into my mornings.") is cut
from its paper the site's way (paper divided out, so it multiplies onto the page) and swapped into
the live homepage's own <img>; nothing in src/ changes. A take whose name starts with "counter"
gets the real NuriCell bottle (public/images/products/nuricell.png, unchanged) stood in its empty
spot on a soft ink ground wash. Shots: laptop and phone, the section as a visitor scrolls to it.

    python -X utf8 reference/ink-pages/home-stories/shoot_stories.py [base-url] [take ...]

Cuts go to plates/cut/, shots to plates/shots/ (both git-ignored). The take "today" shoots the
page as it is.
"""

import base64
import io
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CUT = HERE / "plates" / "cut"
SHOTS = HERE / "plates" / "shots"
BOTTLE = ROOT / "public" / "images" / "products" / "nuricell.png"
FLOOR = 10.0
FADE = 24.0
SIZES = [("1440", 1440, 900, False), ("390", 390, 844, True)]
TAKES = ["today", "kitchen-1", "porch-1", "counter-1"]
# The counter's empty spot (fractions of the painting): its centre across, the bottle's base and
# its height.
SPOT = {"x": 0.52, "base": 0.80, "h": 0.29}


def cut(name):
    """The painting on white (white = no paint), the paper divided out, the edges faded."""
    a = np.asarray(Image.open(HERE / "originals" / f"{name}.png").convert("RGB")).astype(float)
    top = a[: a.shape[0] // 5].reshape(-1, 3)
    paper = np.percentile(top, 70, axis=0)
    dark = 255.0 - np.clip(a / paper * 255.0, 0, 255)
    dark = np.clip((dark - FLOOR) / (1 - FLOOR / 255.0), 0, 255)
    h, w = dark.shape[:2]
    ramp = lambda n: np.clip(np.minimum(np.arange(n), np.arange(n)[::-1]) / FADE, 0, 1)
    dark *= (ramp(h)[:, None] * ramp(w)[None, :])[..., None]
    im = Image.fromarray((255.0 - dark).astype(np.uint8))
    if name.startswith("counter"):
        im = stand_bottle(im)
    return im


def stand_bottle(im):
    """The real bottle in the empty spot, seated on a soft grey wash (multiplied under it)."""
    w, h = im.size
    bottle = Image.open(BOTTLE).convert("RGBA")
    bottle = bottle.crop(bottle.getchannel("A").getbbox())
    bh = round(h * SPOT["h"])
    bw = round(bottle.width * bh / bottle.height)
    bottle = bottle.resize((bw, bh), Image.LANCZOS)
    cx, base = round(w * SPOT["x"]), round(h * SPOT["base"])
    # The ground wash: a flat soft ellipse of warm grey ink, wider than the bottle.
    wash = Image.new("L", im.size, 0)
    d = ImageDraw.Draw(wash)
    rx, ry = bw * 0.85, bh * 0.06
    d.ellipse((cx - rx, base - ry, cx + rx, base + ry), fill=120)
    wash = wash.filter(ImageFilter.GaussianBlur(bh * 0.05))
    ink = np.array([96, 92, 86], float)
    k = np.asarray(wash).astype(float)[..., None] / 255.0
    rgb = np.asarray(im).astype(float)
    rgb = rgb * (1 - k) + (rgb * ink / 255.0) * k
    im = Image.fromarray(rgb.astype(np.uint8)).convert("RGBA")
    im.alpha_composite(bottle, (cx - bw // 2, base - bh + round(bh * 0.01)))
    return im.convert("RGB")


def data_url(im):
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=92)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()


SWAP = """(url) => {
  const img = document.querySelector('[data-brush=story-painting] img[data-on=true]');
  img.removeAttribute('srcset');
  img.removeAttribute('sizes');
  img.src = url;
  // The new still lifes are square, framed whole (not the old portrait's 82% crop). From 900px the
  // old one ran off the window's left edge at 14% of its width, which cut the new mug in half:
  // the window's edge now falls at 6%, inside the painting's own faded edge.
  img.style.objectPosition = '50% 50%';
  const fig = img.closest('figure');
  if (innerWidth >= 900) fig.style.setProperty('--w', 'min((var(--area) + var(--room)) / 0.94, 860px)');
  return img.decode();
}"""

# Laptop: the section's heading under the menu bar, as a visitor arrives. Phone: the painting and
# Lisa's words under it.
PLACE = {
    "1440": "document.querySelector('#stories').getBoundingClientRect().top + scrollY - 20",
    "390": "document.querySelector('[data-brush=story-painting]').getBoundingClientRect().top + scrollY - 90",
}


# The take "set" shoots all three stories with the picked porch (Mo picked A, November 6): each
# story's own <img> swapped, then each name clicked as a visitor would, so its still life blooms in.
SET = {"lisa": "porch-2", "michael": "porch-dusk-1", "susan": "porch-source-2"}

SWAP_ALL = """(urls) => {
  const imgs = [...document.querySelectorAll('[data-brush=story-painting] img')];
  imgs.forEach((img, i) => {
    img.removeAttribute('srcset');
    img.removeAttribute('sizes');
    img.src = urls[i];
    img.style.objectPosition = '50% 50%';
  });
  const fig = imgs[0].closest('figure');
  if (innerWidth >= 900) fig.style.setProperty('--w', 'min((var(--area) + var(--room)) / 0.94, 860px)');
  return Promise.all(imgs.map((img) => img.decode()));
}"""


def main():
    args = sys.argv[1:]
    base = next((a.rstrip("/") for a in args if "://" in a), "https://bigh-website-demo.vercel.app")
    takes = [a for a in args if "://" not in a] or TAKES
    CUT.mkdir(parents=True, exist_ok=True)
    SHOTS.mkdir(parents=True, exist_ok=True)
    urls = {}
    for name in takes:
        if name == "today":
            urls[name] = None
            continue
        if name == "set":
            parts = []
            for take in SET.values():
                im = cut(take)
                im.save(CUT / f"{take}.png")
                parts.append(data_url(im))
            urls[name] = parts
            continue
        im = cut(name)
        im.save(CUT / f"{name}.png")
        urls[name] = data_url(im)
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--use-angle=d3d11"])
        for size, w, h, mobile in SIZES:
            ctx = browser.new_context(
                viewport={"width": w, "height": h},
                is_mobile=mobile,
                has_touch=mobile,
                device_scale_factor=2,
            )
            page = ctx.new_page()
            page.goto(base + "/", wait_until="networkidle")
            page.wait_for_timeout(1500)
            # Scroll there in wheel notches, so the brush line and the bloom run as for a visitor.
            # The page eases the wheel, so keep turning it until the place stops moving.
            for _ in range(400):
                left = round(page.evaluate(PLACE[size]) - page.evaluate("scrollY"))
                if abs(left) < 24:
                    break
                page.mouse.wheel(0, max(-240, min(240, left)))
                page.wait_for_timeout(60 if abs(left) > 600 else 250)
            page.wait_for_timeout(3500)
            for name, url in urls.items():
                if name == "set":
                    page.evaluate(SWAP_ALL, url)
                    page.wait_for_timeout(500)
                    for i, story in enumerate(SET):
                        page.evaluate(
                            f"document.querySelectorAll('#stories [aria-pressed]')[{i}].click()"
                        )
                        page.wait_for_timeout(3500)
                        page.screenshot(path=str(SHOTS / f"set-{story}-{size}.png"))
                    continue
                if url:
                    page.evaluate(SWAP, url)
                    page.wait_for_timeout(500)
                page.screenshot(path=str(SHOTS / f"{name}-{size}.png"))
            ctx.close()
        browser.close()


if __name__ == "__main__":
    main()

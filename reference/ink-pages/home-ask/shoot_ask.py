"""Part 3 of the homepage's California follow-ups (October 30, 2026): "Good questions deserve clear
answers." The inkstone and brush read as Chinese. Each take is cut from its paper the site's way
(paper divided out, so it multiplies onto the page), framed 4:3 like the inkstone, and swapped into
the live homepage's own <img>, nothing in src/ changes. Shots: laptop and phone, the section as a
visitor scrolls to it.

    python -X utf8 reference/ink-pages/home-ask/shoot_ask.py [base-url] [take ...]

Cuts go to plates/cut/, shots to plates/shots/ (both git-ignored).
"""

import base64
import io
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
CUT = HERE / "plates" / "cut"
SHOTS = HERE / "plates" / "shots"
FRAME = (1200, 896)  # the inkstone's frame
FILL = 0.84  # how much of the frame the painting's widest side takes
FLOOR = 14.0
FADE = 30.0
SIZES = [("1440", 1440, 900, False), ("390", 390, 844, True)]
TAKES = ["mailbox-4", "gold-pan-3", "field-book-3"]


def cut(name):
    """The painting on white (white = no paint), cropped to its ink and centred in the frame."""
    a = np.asarray(Image.open(HERE / "originals" / f"{name}.png").convert("RGB")).astype(float)
    edge = np.concatenate([a[:50].reshape(-1, 3), a[-50:].reshape(-1, 3)])
    paper = np.percentile(edge, 60, axis=0)
    dark = 255.0 - np.clip(a / paper * 255.0, 0, 255)
    # The paper's grain would show as a pale box: dropped under the floor.
    dark = np.clip((dark - FLOOR) / (1 - FLOOR / 255.0), 0, 255)
    h, w = dark.shape[:2]
    ramp = lambda n: np.clip(np.minimum(np.arange(n), np.arange(n)[::-1]) / FADE, 0, 1)
    dark *= (ramp(h)[:, None] * ramp(w)[None, :])[..., None]
    c = (255.0 - dark).astype(np.uint8)
    ys, xs = np.where((255 - c.min(axis=2)) > 12)
    box = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
    art = Image.fromarray(c).crop(box)
    k = min(FRAME[0] * FILL / art.width, FRAME[1] * FILL / art.height)
    art = art.resize((round(art.width * k), round(art.height * k)), Image.LANCZOS)
    frame = Image.new("RGB", FRAME, "white")
    frame.paste(art, ((FRAME[0] - art.width) // 2, (FRAME[1] - art.height) // 2))
    return frame


def data_url(im):
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=92)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()


SWAP = """(url) => {
  const img = document.querySelector('[data-brush=ask-art] img');
  img.removeAttribute('srcset');
  img.removeAttribute('sizes');
  img.src = url;
  return img.decode();
}"""


def main():
    args = sys.argv[1:]
    base = next((a.rstrip("/") for a in args if "://" in a), "https://bigh-website-demo.vercel.app")
    takes = [a for a in args if "://" not in a] or TAKES
    CUT.mkdir(parents=True, exist_ok=True)
    SHOTS.mkdir(parents=True, exist_ok=True)
    urls = {}
    for name in takes:
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
            page.evaluate("document.querySelector('[data-brush=ask]').scrollIntoView({block:'center'})")
            page.wait_for_timeout(3000)
            for name, url in urls.items():
                page.evaluate(SWAP, url)
                page.wait_for_timeout(400)
                page.screenshot(path=str(SHOTS / f"{name}-{size}.png"))
            ctx.close()
        browser.close()


if __name__ == "__main__":
    main()

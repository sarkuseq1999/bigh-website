"""Part 4 of the homepage's California follow-ups (October 30, 2026): the closing painting (old pine,
misty peaks, two cranes) reads as Chinese. Each take is cut from its paper the site's way, the live
gold-leaf sun set on its horizon, and swapped into the live homepage's own <img> with a little CSS;
nothing in src/ changes. Shots: big screen, laptop and phone, scrolled to the section as a visitor.

    python -X utf8 reference/ink-pages/home-purpose/shoot_purpose.py [base-url] [scene ...]

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
LIVE = HERE.parents[2] / "public" / "images" / "home-v2" / "ink"

W, H = 2400, 1200  # 2:1: the live 7:3 band was too shallow to hold the land and the words
SCALE = W / 1536
FLOOR = 6.0
SUN_X = 1938  # the live sun's centre, in the painting's 2400 px
SUN_D = 186  # its size (the live closing sun's)
SUN_SET = 0.22  # how much of it the sea or land hides

# take: y = where the crop starts in the 1024 px original, horizon = the sea's or far hills' line
# there, birds = the pelicans fly over it
SCENES = {
    "big-sur": {"take": "big-sur-1", "y": 130, "horizon": 663, "birds": True},
    "ridge": {"take": "ridge-2", "y": 140, "horizon": 644, "birds": True},
    "beach": {"take": "beach-2", "y": 150, "horizon": 654, "birds": True},
}
BIRDS = {"take": "pelicans-2", "left": 0.52, "top": 0.43, "width": 0.17}
HIDDEN = 0.38  # how much of the plate lies under the statement on a phone (its sky)
SIZES = [("1920", 1920, 1080, False), ("1440", 1440, 900, False), ("390", 390, 844, True)]


def divide(a):
    """The painting on white (white = no paint): its paper divided out, its grain under the floor."""
    paper = np.percentile(a[:50].reshape(-1, 3), 60, axis=0)
    dark = 255.0 - np.clip(a / paper * 255.0, 0, 255)
    return np.clip((dark - FLOOR) / (1 - FLOOR / 255.0), 0, 255)


def sun_leaf():
    """The opening's gold-leaf sun (the same leaf), at the closing sun's size: colour and alpha."""
    im = Image.open(LIVE / "sun.webp").convert("RGBA").resize((SUN_D, round(SUN_D * 743 / 760)), Image.LANCZOS)
    a = np.asarray(im).astype(float)
    return a[..., :3], a[..., 3] / 255.0


def cut(scene, with_mask=False):
    """The painting at 2400 x 1200, its sun set in; with_mask also returns where the leaf is."""
    s = SCENES[scene]
    a = np.asarray(Image.open(HERE / "originals" / f"{s['take']}.png").convert("RGB")).astype(float)
    y0 = s["y"]
    crop = a[y0 : y0 + round(H / SCALE)]
    dark = divide(crop)
    dark *= np.clip(np.arange(dark.shape[0]) / 30.0, 0, 1)[:, None, None]
    im = Image.fromarray((255.0 - dark).astype(np.uint8)).resize((W, H), Image.LANCZOS)
    out = np.asarray(im).astype(float)

    # The sun on the horizon: the leaf is cut level where the land or sea stands in front of it.
    leaf, alpha = sun_leaf()
    line = round((s["horizon"] - y0) * SCALE)
    top = round(line - leaf.shape[0] * (1 - SUN_SET))
    left = SUN_X - leaf.shape[1] // 2
    rows = max(0, min(leaf.shape[0], line - top))
    k = alpha[:rows, :, None].copy()
    # Its foot softened over a few pixels, as the water or grass laps it.
    k[-6:] *= np.linspace(1.0, 0.25, min(6, rows))[:, None, None]
    box = out[top : top + rows, left : left + leaf.shape[1]]
    out[top : top + rows, left : left + leaf.shape[1]] = box * (1 - k) + leaf[:rows] * k
    im = Image.fromarray(out.astype(np.uint8))
    if not with_mask:
        return im
    mask = np.zeros((H, W))
    mask[top : top + rows, left : left + leaf.shape[1]] = k[..., 0]
    return im, mask


def cut_birds():
    a = np.asarray(Image.open(HERE / "originals" / f"{BIRDS['take']}.png").convert("RGB")).astype(float)
    c = (255.0 - divide(a)).astype(np.uint8)
    ys, xs = np.where((255 - c.min(axis=2)) > 12)
    box = (int(xs.min()) - 6, int(ys.min()) - 6, int(xs.max()) + 7, int(ys.max()) + 7)
    art = Image.fromarray(c).crop(box)
    return art


def data_url(im):
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=90)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()


CSS = f"""
#purpose [data-brush=purpose-painting] {{ --edge: linear-gradient(to bottom, #000 84%, transparent 100%) !important; }}
#purpose [data-brush=purpose-painting] + span {{ display: none !important; }}
@media (max-width: 899px) {{
  #purpose [data-brush=purpose-painting] {{ min-height: 0; }}
  #purpose div:has(> [data-brush=purpose-painting]) {{ margin-top: calc(60px - {HIDDEN * H / W} * min(220vw, 1500px)) !important; }}
}}
"""

SWAP = """([url, birds, box, ratio]) => {
  const img = document.querySelector('#purpose [data-brush=purpose-painting]');
  img.loading = 'eager'; img.removeAttribute('srcset'); img.removeAttribute('sizes'); img.removeAttribute('height'); img.src = url;
  img.style.aspectRatio = '2 / 1';
  const f = document.querySelector('#purpose img[src*=purpose-cranes], #purpose img[data-birds]');
  const flight = f.parentElement;
  if (!birds) { flight.style.display = 'none'; return img.decode(); }
  flight.style.display = '';
  flight.style.left = box.left * 100 + '%'; flight.style.top = box.top * 100 + '%'; flight.style.width = box.width * 100 + '%';
  flight.style.aspectRatio = ratio;
  f.dataset.birds = '1';
  f.loading = 'eager'; f.removeAttribute('srcset'); f.removeAttribute('sizes'); f.removeAttribute('height'); f.src = birds;
  return Promise.all([img.decode(), f.decode()]);
}"""


def main():
    args = sys.argv[1:]
    base = next((a.rstrip("/") for a in args if "://" in a), "https://bigh-website-demo.vercel.app")
    scenes = [a for a in args if "://" not in a] or list(SCENES)
    CUT.mkdir(parents=True, exist_ok=True)
    SHOTS.mkdir(parents=True, exist_ok=True)
    art = cut_birds()
    art.save(CUT / "pelicans.png")
    birds = data_url(art)
    ratio = f"{art.width} / {art.height}"
    urls = {}
    for name in scenes:
        im = cut(name)
        im.save(CUT / f"{name}.png")
        urls[name] = data_url(im)
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--use-angle=d3d11"])
        for size, w, h, mobile in SIZES:
            ctx = browser.new_context(
                viewport={"width": w, "height": h}, is_mobile=mobile, has_touch=mobile, device_scale_factor=2
            )
            page = ctx.new_page()
            page.goto(base + "/", wait_until="networkidle")
            if size == "1440":
                top = page.evaluate("document.querySelector('#purpose').getBoundingClientRect().top + scrollY")
                page.evaluate(f"window.scrollTo({{top: {top - 96}, behavior: 'instant'}})")
                page.wait_for_timeout(3200)
                page.screenshot(path=str(SHOTS / "today-1440.png"))
            page.add_style_tag(content=CSS)
            for name, url in urls.items():
                page.evaluate(SWAP, [url, birds if SCENES[name]["birds"] else None, BIRDS, ratio])
                top = page.evaluate("document.querySelector('#purpose').getBoundingClientRect().top + scrollY")
                page.evaluate(f"window.scrollTo({{top: {top + (-60 if mobile else -96)}, behavior: 'instant'}})")
                page.wait_for_timeout(3200)
                page.screenshot(path=str(SHOTS / f"{name}-{size}.png"))
            ctx.close()
        browser.close()


if __name__ == "__main__":
    main()

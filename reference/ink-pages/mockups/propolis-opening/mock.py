"""Green Bee Propolis's opening with a painting behind the approved name and bottle (November 18,
2026), mocked on the live page: each Codex take is laid behind "Green [bottle] Bee Propolis" the
way the other painted openings are (its paper divided out, multiplied onto the page's paper, the
bottle standing on its ground, a little of that ground laid in front of its foot), then shot at
desktop and phone sizes. Nothing on the site changes.

    python -X utf8 reference/ink-pages/mockups/propolis-opening/mock.py <take> [take ...]

A take is originals/<take>.png in reference/ink-pages/propolis/. Shots land in shots/.
"""

import io
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ORIG = HERE.parents[1] / "propolis" / "originals"
SHOTS = HERE / "shots"
SHOTS.mkdir(exist_ok=True)
BASE = "https://bigh-website-demo.vercel.app"
SIZES = [(1440, 900), (1920, 1080), (1024, 768), (390, 844)]


def plate(take, at=None):
    a = np.asarray(Image.open(ORIG / f"{take}.png").convert("RGB")).astype(np.float32)
    h, w, _ = a.shape
    paper = np.median(a[int(h * 0.93) :].reshape(-1, 3), axis=0)
    d = np.clip(a / paper * 255.0, 0, 255)
    d = np.where(d.min(axis=2, keepdims=True) > 249, 255.0, d)
    painted = np.where((d.min(axis=2) < 244).sum(axis=1) > 3)[0]
    end = int(painted[-1])
    rows = min(h, end + 24)
    d = d[:rows]
    ease = np.clip((np.arange(rows) - (rows - 16)) / 14, 0, 1)[:, None, None]
    d = d * (1 - ease) + 255 * ease
    # The empty spot's ground: the last paint in the middle columns, a little up into it.
    mid = d[:, int(w * 0.46) : int(w * 0.54)]
    rows_mid = np.where((mid.min(axis=2) < 235).sum(axis=1) > 2)[0]
    ground = int(rows_mid[-1]) - 22 if at is None else int(at * h)
    return d, ground, end


def front(d, ground):
    h, w, _ = d.shape
    x0, x1 = int(w * 0.43), int(w * 0.57)
    y0, y1 = ground - 26, min(h, ground + 40)
    tuft = d[y0:y1, x0:x1]
    th, tw, _ = tuft.shape
    alpha = 1 - tuft.min(axis=2) / 255
    paint = np.where(alpha[..., None] > 0.03, (tuft - 255 * (1 - alpha[..., None])) / np.maximum(alpha[..., None], 0.03), 255)
    blade = np.clip((alpha - 0.25) / 0.3, 0, 1)
    alpha = alpha * np.maximum(blade, 0.35)
    xs, ys = np.arange(tw), np.arange(th)
    sides = np.clip(np.minimum(xs, tw - 1 - xs) / 30, 0, 1)
    top = np.clip(ys / 16, 0, 1)
    alpha = alpha * (sides * sides * (3 - 2 * sides))[None, :] * (top * top * (3 - 2 * top))[:, None]
    rgba = np.dstack([np.clip(paint, 0, 255), alpha * 255])
    return Image.fromarray(np.clip(np.rint(rgba), 0, 255).astype(np.uint8), "RGBA"), x0, y0


def png(img):
    b = io.BytesIO()
    img.save(b, "PNG")
    return b.getvalue()


INJECT = """([sky, fr, W, ground, fx, fy, fw, end]) => {
  const sec = document.querySelector('[data-chapter="overview"]');
  const img = sec.querySelector('img');
  const r = img.getBoundingClientRect();
  const s = sec.getBoundingClientRect();
  const wide = innerWidth >= 960;
  // The glass's foot: 96.2% down the bottle's picture.
  const foot = r.top - s.top + r.height * 0.962;
  const cx = r.left + r.width / 2;
  // From 960px the painting is the window's width; one column draws it 2.2 windows wide.
  const pw = wide ? innerWidth + 8 : innerWidth * 2.2;
  const k = pw / W;
  sec.style.position = 'relative';
  sec.style.overflowX = 'clip';
  const p = document.createElement('img');
  p.src = sky;
  Object.assign(p.style, {position: 'absolute', zIndex: -1, left: (cx - pw / 2) + 'px', top: (foot - ground * k) + 'px',
    width: pw + 'px', maxWidth: 'none', mixBlendMode: 'multiply', pointerEvents: 'none'});
  sec.prepend(p);
  const f = document.createElement('img');
  f.src = fr;
  Object.assign(f.style, {position: 'absolute', zIndex: 2, left: (cx - pw / 2 + fx * k) + 'px', top: (foot - ground * k + fy * k) + 'px',
    width: (fw * k) + 'px', maxWidth: 'none', pointerEvents: 'none'});
  sec.append(f);
  // The words start 14px under the last of the painting.
  const det = sec.querySelector('h1 + div');
  const last = foot + (end - ground) * k;
  const dt = det.getBoundingClientRect().top - s.top;
  if (dt < last + 14) det.style.marginTop = (parseFloat(getComputedStyle(det).marginTop) + last + 14 - dt) + 'px';
  return {foot, top: foot - ground * k, k, pushed: Math.max(0, last + 14 - dt)};
}"""


def main(takes):
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--use-angle=d3d11", "--enable-gpu"])
        for arg in takes:
            take, _, at = arg.partition(":")
            d, ground, end = plate(take, float(at) if at else None)
            sky = Image.fromarray(np.clip(np.rint(d), 0, 255).astype(np.uint8))
            fr, fx, fy = front(d, ground)
            files = {f"/mock/{take}-sky.png": png(sky), f"/mock/{take}-front.png": png(fr)}
            for w, h in SIZES:
                pg = b.new_page(viewport={"width": w, "height": h})
                pg.route("**/mock/**", lambda route: route.fulfill(status=200, content_type="image/png",
                                                                   body=files[route.request.url.split(BASE)[-1]]))
                pg.goto(f"{BASE}/products/green-bee-propolis", wait_until="networkidle")
                pg.wait_for_timeout(2200)
                info = pg.evaluate(INJECT, [f"{BASE}/mock/{take}-sky.png", f"{BASE}/mock/{take}-front.png",
                                            sky.width, ground, fx, fy, fr.width, end])
                pg.wait_for_timeout(900)
                out = SHOTS / f"{take}{'-' + at if at else ''}-{w}.png"
                pg.screenshot(path=str(out))
                print(take, w, info)
                pg.close()
        b.close()


if __name__ == "__main__":
    main(sys.argv[1:])

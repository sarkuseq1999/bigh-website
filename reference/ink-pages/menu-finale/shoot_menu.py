"""Mockups for part 6 of the homepage's California pass (Mo, November 3, 2026): the crane at rest at
the foot of the phone menu, the footer's finale in miniature, is the last crane on the site. Each
option's painting has its paper divided out and is trimmed, then stands in the crane's room on the
public demo: the crane's picture is swapped for it, the room takes the painting's proportions and
the option's size, and the brush stroke under the crane's feet moves to the option's feet. Nothing
in the site changes. Pictures land in reference/ink-pages/mockups/menu-finale/.

usage: python -X utf8 reference/ink-pages/menu-finale/shoot_menu.py [base] [option ...]
"""

import base64
import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "footer-crane"))
from cut_cranes import divide_paper  # noqa: E402

OUT = HERE.parents[0] / "mockups" / "menu-finale"
BASE = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].startswith("http") else "https://bigh-website-demo.vercel.app"
ONLY = [a for a in sys.argv[1:] if not a.startswith("http")]

# Per option: the painting, the line its feet stand on (y in the original's pixels) and the room's
# height as a share of the crane's room (on a 390 x 844 phone the crane's is 221px tall).
OPTIONS = {
    "now": None,
    # A: one quail, the footer's lookout, standing alone. B: the footer's own two quail, smaller.
    # C: a clump of California poppies, the park sign's flower. The crane's black stroke under them
    # cut through their grass like a bar: each stands on its painting's own grass, as the footer's
    # quail do ("bare"); feetY still says where the stroke would go.
    "a": {"take": "menu-quail-1", "feetY": 1125, "room": 0.82, "bare": True},
    "b": {"take": "../../footer-crane/originals/quail-wash-2", "feetY": 850, "room": 0.62, "bare": True},
    "c": {"take": "menu-poppy-1", "feetY": 1140, "room": 0.82, "bare": True},
    "a-stroke": {"take": "menu-quail-1", "feetY": 1125, "room": 0.82},
    # Mo (November 3): "Can we try with the hummingbird?" D: Allen's at rest on a bare twig, a new
    # painting in the opening bird's hand. E: the opening's own bird, its wings beating, at a sprig
    # of California fuchsia (a new painting of the flower only); "bird" puts its bill tip at the
    # flower's mouth (x, y in the painting's pixels) at `scale` of the bird's 1600 x 1062 frame.
    # D is calmed as the opening's bird was (build_wings.py CALM): its orange came out as loud. The
    # fuchsia's coral a little less, so the bird leads. Both take the crane's whole room: a small
    # bird needs it, and the menu has paper to spare above it.
    "d": {"take": "menu-perch-2", "feetY": None, "room": 1.0, "bare": True, "calm": (0.72, 0.94)},
    "e": {
        "take": "menu-fuchsia-1",
        "feetY": None,
        "room": 1.0,
        "bare": True,
        "calm": (0.8, 0.96),
        "bird": {"x": 552, "y": 392, "scale": 0.58},
    },
}
SIZES = {"phone": (390, 844), "small": (360, 740), "tablet": (768, 1024)}

# The opening's bird (assets.ts): its frame, its bill tip and the box its wings and body fill.
BIRD = {"w": 1600, "h": 1062, "bill": (1154, 409), "box": (283, 167, 1154, 946)}


def bird_box(b):
    """The bird's frame and its painted box in a painting's pixels, its bill tip at (x, y)."""
    s = b["scale"]
    fx, fy = b["x"] - BIRD["bill"][0] * s, b["y"] - BIRD["bill"][1] * s
    bx0, by0, bx1, by1 = BIRD["box"]
    return (fx, fy, BIRD["w"] * s, BIRD["h"] * s), (fx + bx0 * s, fy + by0 * s, fx + bx1 * s, fy + by1 * s)


def calmed(rgb, sat, val):
    """Less saturation, and the strongest colours up to `val` as bright; bare paper stays white."""
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
    s = hsv[..., 1] / 255
    hsv[..., 1] *= sat
    hsv[..., 2] *= 1 - (1 - val) * s
    return cv2.cvtColor(np.clip(hsv, 0, 255).astype(np.uint8), cv2.COLOR_HSV2RGB)


def cut(take, keep=None, calm=None):
    """The painting, its paper divided out, trimmed to its ink (and to `keep`, a box the bird will
    fill, so the empty paper it hovers over stays)."""
    src = Image.open(HERE / "originals" / f"{take}.png").convert("RGB")
    c = divide_paper(np.asarray(src))
    if calm:
        c = calmed(np.ascontiguousarray(c), *calm)
    ink = (255 - c.min(axis=2)) > 10
    ys, xs = np.where(ink)
    lo_x, lo_y, hi_x, hi_y = xs.min(), ys.min(), xs.max(), ys.max()
    if keep:
        lo_x, lo_y = min(lo_x, keep[0]), min(lo_y, keep[1])
        hi_x, hi_y = max(hi_x, keep[2]), max(hi_y, keep[3])
    pad = 12
    x0, x1 = int(max(lo_x - pad, 0)), int(min(hi_x + pad, c.shape[1]))
    y0, y1 = int(max(lo_y - pad, 0)), int(min(hi_y + pad, c.shape[0]))
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{Path(take).name}-cut.png"
    Image.fromarray(c[y0:y1, x0:x1]).save(path, optimize=True)
    return path, (x0, y0, x1 - x0, y1 - y0)


# Swaps the crane's picture, gives its room the painting's proportions and the option's size, and
# lays the brush stroke under the option's feet.
PLACE = """([src, m]) => {
  const img = document.querySelector('header img[src*=crane-rest]');
  const stand = img.parentElement, ground = stand.querySelector('span');
  img.removeAttribute('srcset');
  img.src = src;
  stand.style.aspectRatio = `${m.w} / ${m.h}`;
  // A tablet keeps the crane's room (130px to 230px tall): a smaller one lifted Log in and Sign up
  // off the foot of the window.
  if (innerWidth < 700) {
    stand.style.height = `calc(clamp(130px, calc(44svh - 150px), 230px) * ${m.room})`;
  }
  const feet = (m.feetY / m.h) * 100;
  // The crane's stroke is 126% of its room's width: keep its length, or a little wider than a wide
  // painting.
  const wide = 100 * Math.max((1.26 * 560) / 864 / (m.room * (m.w / m.h)), 1.1);
  Object.assign(ground.style, { top: `${feet - 4.5}%`, left: `${(100 - wide) / 2}%`, width: `${wide}%` });
  if (m.bare) ground.style.display = 'none';
  // The opening's bird: only its frame is laid in (hidden), measured for the mockup page, which
  // lays the body and its beating wings over the shot.
  let bird = null;
  if (m.bird) {
    bird = document.createElement('span');
    Object.assign(bird.style, {
      position: 'absolute', left: `${m.bird.left}%`, top: `${m.bird.top}%`, width: `${m.bird.width}%`,
      aspectRatio: '1600 / 1062', visibility: 'hidden',
    });
    stand.append(bird);
  }
  img.getAnimations().forEach((a) => a.finish());
  return new Promise((done) => img.decode().then(() => {
    const box = (e) => { const r = e.getBoundingClientRect(); return [r.x, r.y, r.width, r.height]; };
    done({ img: box(img).map(Math.round), ground: box(ground).map(Math.round), bird: bird && box(bird) });
  }));
}"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=["--use-angle=d3d11"])
        for name, opt in OPTIONS.items():
            if ONLY and name not in ONLY:
                continue
            src = m = None
            rects = {}
            if opt:
                frame = keep = None
                if opt.get("bird"):
                    frame, keep = bird_box(opt["bird"])
                path, (x0, y0, w, h) = cut(opt["take"], keep, opt.get("calm"))
                feet = opt["feetY"] if opt["feetY"] is not None else y0 + h - 12
                m = {"w": w, "h": h, "feetY": feet - y0, "room": opt["room"], "bare": opt.get("bare", False)}
                if frame:
                    fx, fy, fw, _ = frame
                    m["bird"] = {"left": (fx - x0) / w * 100, "top": (fy - y0) / h * 100, "width": fw / w * 100}
                src = "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()
            for size_name, (vw, vh) in SIZES.items():
                mobile = vw < 768
                ctx = browser.new_context(
                    viewport={"width": vw, "height": vh},
                    is_mobile=mobile,
                    has_touch=mobile,
                    device_scale_factor=2,
                )
                page = ctx.new_page()
                page.goto(BASE + "/", wait_until="networkidle", timeout=120000)
                page.wait_for_timeout(1200)
                page.locator("header button[aria-expanded]").first.click()
                page.wait_for_timeout(2500)
                if opt:
                    info = page.evaluate(PLACE, [src, m])
                    page.wait_for_timeout(500)
                    print(name, size_name, json.dumps(info))
                    if info["bird"]:
                        rects[size_name] = info["bird"]
                page.screenshot(path=str(OUT / f"{name}-{size_name}.png"))
                print("saved", f"{name}-{size_name}.png")
                ctx.close()
            if rects:
                (OUT / f"{name}-bird.json").write_text(json.dumps(rects, indent=1), encoding="utf-8")
        browser.close()


if __name__ == "__main__":
    main()

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
}
SIZES = {"phone": (390, 844), "small": (360, 740), "tablet": (768, 1024)}


def cut(take):
    src = Image.open(HERE / "originals" / f"{take}.png").convert("RGB")
    c = divide_paper(np.asarray(src))
    ink = (255 - c.min(axis=2)) > 10
    ys, xs = np.where(ink)
    pad = 12
    x0, x1 = int(max(xs.min() - pad, 0)), int(min(xs.max() + pad, c.shape[1]))
    y0, y1 = int(max(ys.min() - pad, 0)), int(min(ys.max() + pad, c.shape[0]))
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
  img.getAnimations().forEach((a) => a.finish());
  return new Promise((done) => img.decode().then(() => {
    const r = img.getBoundingClientRect(), g = ground.getBoundingClientRect();
    done({ img: [r.x, r.y, r.width, r.height].map(Math.round), ground: [g.x, g.y, g.width, g.height].map(Math.round) });
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
            if opt:
                path, (x0, y0, w, h) = cut(opt["take"])
                feet = opt["feetY"] if opt["feetY"] is not None else y0 + h - 12
                m = {"w": w, "h": h, "feetY": feet - y0, "room": opt["room"], "bare": opt.get("bare", False)}
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
                page.screenshot(path=str(OUT / f"{name}-{size_name}.png"))
                print("saved", f"{name}-{size_name}.png")
                ctx.close()
        browser.close()


if __name__ == "__main__":
    main()

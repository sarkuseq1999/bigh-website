"""Mockups for part 5 of the homepage's California pass (Mo, November 3, 2026): the red-crowned crane
by the FDA park sign reads as Chinese. Each California animal Codex painted (originals/<take>.png)
has its paper divided out and is trimmed, then stands where the crane stands on the built site:
the live crane's picture is swapped for it and resized in the sign's own measure (--k), its feet
on the sign's ground and --gap right of the sign, as `.look .rest` places the crane. Nothing in
the site changes. Pictures land in reference/ink-pages/mockups/footer-crane/animals/.

usage: python -X utf8 reference/ink-pages/footer-crane/shoot_animals.py [base] [option ...]
"""

import base64
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

from cut_cranes import divide_paper

HERE = Path(__file__).parent
OUT = HERE.parents[0] / "mockups" / "footer-crane" / "animals"
BASE = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].startswith("http") else "http://localhost:3006"
ONLY = [a for a in sys.argv[1:] if not a.startswith("http")]

# Per option: the painting, where the animal meets the ground (its "feet", in the original's
# pixels: the point the CSS stands on the sign's ground, --gap right of the sign) and the top of the
# animal, read off the painting; then its height from feet to top and its gap, in the sign's
# measure (the crane today: 250 tall, 208 gap; phones 183 and 117).
OPTIONS = {
    "now": None,
    # A: California quail, the state bird: the covey's lookout stands tall, the other bends to the
    # poppy. B: a desert tortoise, the state reptile, sniffing the poppy. C: a black bear cub.
    # The first quail came out a detailed field-guide bird and the first tortoise a Galapagos
    # giant: their second, looser takes. The second bear's back read as a pale stripe: its first.
    "a": {"take": "quail-2", "feet": (620, 820), "top": 130, "tall": 210, "gap": 44, "phoneTall": 180, "phoneGap": 36},
    "b": {"take": "tortoise-2", "feet": (650, 780), "top": 262, "tall": 165, "gap": 62, "phoneTall": 118, "phoneGap": 38},
    "c": {"take": "bear-1", "feet": (640, 810), "top": 225, "tall": 230, "gap": 83, "phoneTall": 140, "phoneGap": 52},
}
PAGES = {"home": "/", "science": "/science"}
SIZES = {"desktop": (1440, 900), "phone": (390, 844)}


def cut(take):
    src = Image.open(HERE / "originals" / f"{take}.png").convert("RGB")
    c = divide_paper(np.asarray(src))
    ink = (255 - c.min(axis=2)) > 10
    ys, xs = np.where(ink)
    pad = 12
    x0, x1 = int(max(xs.min() - pad, 0)), int(min(xs.max() + pad, c.shape[1]))
    y0, y1 = int(max(ys.min() - pad, 0)), int(min(ys.max() + pad, c.shape[0]))
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{take}-cut.png"
    Image.fromarray(c[y0:y1, x0:x1]).save(path, optimize=True)
    return path, (x0, y0, x1 - x0, y1 - y0)


# Swaps the crane's picture and places it as `.look .rest` does, with this animal's measurements.
PLACE = """([src, m, o]) => {
  const img = document.querySelector('footer img[src*=crane-poppy]');
  const fda = document.querySelector('[data-fda]');
  const phone = innerWidth <= 720;
  const tall = (phone && o.phoneTall) || o.tall, gap = (phone && o.phoneGap) || o.gap;
  img.removeAttribute('srcset');
  img.src = src;
  const s = `var(--k)`;
  Object.assign(img.style, {
    width: `calc(${tall}px * ${s} * ${m.w / m.tall})`,
    height: `calc(${tall}px * ${s} * ${m.h / m.tall})`,
    margin: `0 0 calc(62.5px * ${s} - ${tall}px * ${s} * ${(m.h - m.feetY) / m.tall}) calc(${gap}px * ${s} - ${tall}px * ${s} * ${m.feetX / m.tall})`,
    opacity: '1', clipPath: 'none', maskImage: 'none', webkitMaskImage: 'none',
  });
  img.getAnimations().forEach((a) => a.finish());
  const r = img.getBoundingClientRect(), f = fda.getBoundingClientRect();
  return { img: [r.x, r.y, r.width, r.height].map(Math.round), sign: [f.x, f.y, f.width, f.height].map(Math.round), vw: innerWidth };
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
                fx, fy = opt["feet"]
                m = {"w": w, "h": h, "feetX": fx - x0, "feetY": fy - y0, "tall": fy - opt["top"]}
                src = "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()
            for page_name, route in PAGES.items():
                for size_name, (vw, vh) in SIZES.items():
                    mobile = vw < 768
                    ctx = browser.new_context(
                        viewport={"width": vw, "height": vh},
                        is_mobile=mobile,
                        has_touch=mobile,
                        device_scale_factor=2,
                    )
                    page = ctx.new_page()
                    page.goto(BASE + route, wait_until="networkidle", timeout=120000)
                    page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
                    for _ in range(2):
                        page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
                        page.wait_for_timeout(2000)
                    if opt:
                        info = page.evaluate(PLACE, [src, m, opt])
                        page.wait_for_timeout(600)
                        print(name, page_name, size_name, info)
                    page.screenshot(path=str(OUT / f"{name}-{page_name}-{size_name}.png"))
                    print("saved", f"{name}-{page_name}-{size_name}.png")
                    ctx.close()
        browser.close()


if __name__ == "__main__":
    main()

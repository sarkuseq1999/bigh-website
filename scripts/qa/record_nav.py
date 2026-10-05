"""Record the menu bar options in use, for Mo's comparison (October 5, 2026).

usage: python -X utf8 scripts/qa/record_nav.py [today,a,b,c] [--base http://localhost:3027]
       [--out scripts/qa/out/nav-videos] [--phone]
Desktop (1536x864): the opening, pointing at links, Products and Science opened and browsed, a
scroll down, Products from the scrolled bar, back to the top. Phone (390x844): a scroll down and
back, the menu opened, Products unfolded, closed. A drawn pointer (or tap ring) shows what is being
touched. H.264, no sound. Uses the contract in shoot_nav.py.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

argv = sys.argv[1:]
opts = {"--base": "http://localhost:3027", "--out": "scripts/qa/out/nav-videos"}
for key in list(opts):
    if key in argv:
        opts[key] = argv[argv.index(key) + 1]
PHONE = "--phone" in argv
positional = [
    a for i, a in enumerate(argv) if not a.startswith("--") and (i == 0 or argv[i - 1] not in opts)
]
OPTIONS = positional[0].split(",") if positional else ["today", "a", "b", "c"]
OUT = Path(opts["--out"])
OUT.mkdir(parents=True, exist_ok=True)
SIZE = {"width": 390, "height": 844} if PHONE else {"width": 1536, "height": 864}

POINTER = """
(() => {
  const add = () => {
    const dot = document.createElement('div');
    dot.id = '__rec_pointer';
    Object.assign(dot.style, {
      position: 'fixed', left: '0', top: '0', width: '22px', height: '22px', zIndex: '2147483647',
      pointerEvents: 'none', borderRadius: '50%', transform: 'translate(-200px,-200px)',
      background: 'rgba(12,11,10,0.18)', border: '2px solid rgba(12,11,10,0.55)',
      transition: 'opacity .3s', boxSizing: 'border-box', marginLeft: '-11px', marginTop: '-11px',
    });
    document.body.appendChild(dot);
    const move = (x, y) => (dot.style.transform = `translate(${x}px, ${y}px)`);
    addEventListener('mousemove', e => move(e.clientX, e.clientY), true);
    addEventListener('touchstart', e => {
      const t = e.touches[0]; if (!t) return;
      move(t.clientX, t.clientY);
      dot.animate([{ scale: 0.6, opacity: 1 }, { scale: 1.8, opacity: 0 }], { duration: 650 });
    }, true);
  };
  if (document.body) add(); else addEventListener('DOMContentLoaded', add);
})();
"""

SMOOTH = """async ({ to, ms }) => {
  document.documentElement.style.scrollBehavior = 'auto';
  const from = scrollY, t0 = performance.now();
  await new Promise(done => {
    const tick = now => {
      const k = Math.min(1, (now - t0) / ms);
      const e = k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
      scrollTo(0, from + (to - from) * e);
      k < 1 ? requestAnimationFrame(tick) : done();
    };
    requestAnimationFrame(tick);
  });
}"""


def encode(raw: str, target: Path) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-c:v", "libx264", "-preset", "slow",
         "-crf", "27", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", str(target)],
        check=True,
    )
    print(target, round(target.stat().st_size / 1e6, 1), "MB")


def centre(page, selector, nth=0):
    loc = page.locator(selector)
    if loc.count() <= nth:
        return None
    box = loc.nth(nth).bounding_box()
    if not box or box["width"] == 0:
        return None
    return box["x"] + box["width"] / 2, box["y"] + box["height"] / 2


def glide(page, point, steps=28, wait=0):
    if point:
        page.mouse.move(point[0], point[1], steps=steps)
    if wait:
        page.wait_for_timeout(wait)


def desktop(page):
    page.wait_for_timeout(3600)
    page.mouse.move(1500, 600)
    for label in ("About", "Support"):
        glide(page, centre(page, f'header a:text-is("{label}"), header button:text-is("{label}")'), wait=1000)
    glide(page, centre(page, '[data-nav-trigger="products"]'), wait=2400)
    glide(page, centre(page, '[data-nav-panel="products"] a[href^="/products/"]', 1), steps=36, wait=1600)
    glide(page, centre(page, '[data-nav-panel="products"] a[href^="/products/"]', 3), steps=30, wait=1300)
    glide(page, centre(page, '[data-nav-trigger="science"]'), steps=36, wait=2400)
    glide(page, centre(page, '[data-nav-panel="science"] a[href^="/science#"]', 0), steps=36, wait=1500)
    glide(page, centre(page, '[data-nav-panel="science"] a[href^="/science#"]', 2), steps=24, wait=1300)
    glide(page, (760, 840), steps=30, wait=1400)
    page.evaluate(SMOOTH, {"to": 1600, "ms": 2600})
    page.wait_for_timeout(1600)
    glide(page, centre(page, '[data-nav-trigger="products"]'), steps=36, wait=2400)
    glide(page, (760, 840), steps=30, wait=1100)
    page.evaluate(SMOOTH, {"to": 0, "ms": 2200})
    page.wait_for_timeout(2200)


def phone(page):
    page.wait_for_timeout(3200)
    page.evaluate(SMOOTH, {"to": 1500, "ms": 2600})
    page.wait_for_timeout(1800)
    page.evaluate(SMOOTH, {"to": 0, "ms": 1800})
    page.wait_for_timeout(1400)
    button = page.locator("[data-nav-menu-button]:visible").first
    if button.count():
        button.tap()
        page.wait_for_timeout(2200)
        toggle = page.locator('[data-nav-sheet-toggle="products"]:visible').first
        if toggle.count():
            toggle.tap()
            page.wait_for_timeout(2600)
        page.keyboard.press("Escape")
        page.wait_for_timeout(1500)


with sync_playwright() as p:
    browser = p.chromium.launch(
        args=["--use-gl=angle", "--use-angle=d3d11", "--enable-gpu", "--ignore-gpu-blocklist"]
    )
    for option in OPTIONS:
        query = "?rec=1" if option == "today" else f"?nav={option}&rec=1"
        with tempfile.TemporaryDirectory() as raw:
            ctx = browser.new_context(
                viewport=SIZE, record_video_dir=raw, record_video_size=SIZE, is_mobile=PHONE,
                has_touch=PHONE, device_scale_factor=2 if PHONE else 1,
            )
            ctx.add_init_script(POINTER)
            page = ctx.new_page()
            page.goto(f"{opts['--base']}/{query}", wait_until="networkidle", timeout=120000)
            (phone if PHONE else desktop)(page)
            video = page.video.path()
            ctx.close()
            encode(video, OUT / f"{option}{'-phone' if PHONE else ''}.mp4")
    browser.close()

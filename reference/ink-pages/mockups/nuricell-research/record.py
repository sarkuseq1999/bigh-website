"""Record short clips of the NuriCell research mockup: a desktop visitor and a phone visitor.

usage: python -X utf8 record.py <outdir> [base-url]   (then ffmpeg the .webm files to .mp4)
"""

import shutil
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

out = Path(sys.argv[1])
base = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:3090"
out.mkdir(parents=True, exist_ok=True)

CHAPTER = '[data-chapter="research"]'
BOOK_AT = """(n) => {
  const b = document.querySelector('[data-chapter="research"] [data-book="' + n + '"]');
  const r = b.getBoundingClientRect();
  const pts = [...b.style.clipPath.matchAll(/([\\d.]+)% ([\\d.]+)%/g)].map((m) => [+m[1], +m[2]]);
  const cx = pts.reduce((s, p) => s + p[0], 0) / pts.length;
  const cy = pts.reduce((s, p) => s + p[1], 0) / pts.length;
  return [r.left + (r.width * cx) / 100, r.top + (r.height * cy) / 100];
}"""


def scroll_to(pg, selector, gap):
    top = pg.evaluate(
        f"() => document.querySelector('{selector}').getBoundingClientRect().top + scrollY"
    )
    pg.evaluate(f"window.scrollTo(0, {top - gap})")


def save(ctx, pg, name):
    video = pg.video
    ctx.close()
    shutil.move(video.path(), out / name)


with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-angle=d3d11"])

    # Desktop: point at the far books, open the 2003 pair, then the 2018 question from its row.
    size = {"width": 1440, "height": 900}
    ctx = b.new_context(viewport=size, record_video_dir=str(out / "raw"), record_video_size=size)
    pg = ctx.new_page()
    pg.goto(base + "/products/nuricell", wait_until="networkidle")
    scroll_to(pg, f"{CHAPTER} h2", 110)
    pg.mouse.move(1400, 860)
    pg.wait_for_timeout(2200)
    for n in (7, 6, 5):
        x, y = pg.evaluate(BOOK_AT, n)
        pg.mouse.move(x, y, steps=18)
        pg.wait_for_timeout(900)
    x, y = pg.evaluate(BOOK_AT, 3)
    pg.mouse.move(x, y, steps=18)
    pg.wait_for_timeout(500)
    pg.mouse.click(x, y)
    pg.wait_for_timeout(1200)
    pg.mouse.move(1100, 650, steps=20)
    pg.wait_for_timeout(2800)
    row = pg.locator(f"{CHAPTER} [data-study]:nth-child(6) button")
    box = row.bounding_box()
    pg.mouse.move(box["x"] + 200, box["y"] + box["height"] / 2, steps=20)
    pg.wait_for_timeout(700)
    pg.mouse.click(box["x"] + 200, box["y"] + box["height"] / 2)
    pg.wait_for_timeout(3000)
    save(ctx, pg, "desk.webm")

    # Phone: tap a book, read its answer, go back up, tap another.
    size = {"width": 390, "height": 844}
    ctx = b.new_context(
        viewport=size,
        device_scale_factor=2,
        is_mobile=True,
        has_touch=True,
        record_video_dir=str(out / "raw"),
        record_video_size=size,
    )
    pg = ctx.new_page()
    pg.goto(base + "/products/nuricell", wait_until="networkidle")
    scroll_to(pg, f"{CHAPTER} figure", 90)
    pg.wait_for_timeout(2200)
    x, y = pg.evaluate(BOOK_AT, 6)
    pg.touchscreen.tap(x, y)
    pg.wait_for_timeout(3600)
    pg.evaluate(
        f"document.querySelector('{CHAPTER} figure').scrollIntoView({{behavior: 'smooth'}})"
    )
    pg.wait_for_timeout(1600)
    scroll_to(pg, f"{CHAPTER} figure", 90)
    pg.wait_for_timeout(600)
    x, y = pg.evaluate(BOOK_AT, 3)
    pg.touchscreen.tap(x, y)
    pg.wait_for_timeout(4200)
    save(ctx, pg, "phone.webm")
    b.close()
print("done", out)

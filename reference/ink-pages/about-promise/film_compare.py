"""Film ideas B and C arriving on the real About page, motion on (November 12, 2026).

Mo asked to compare B (four wildflowers) and C (one poppy counting to four). The still shots are
taken with reduced motion; these films show what a visitor sees: scrolling down from the sequoia,
the four small paintings bloom in one after another (the kit's ink bloom, 260ms apart), then rest.
The pictures are swapped in for the dots before they come into view, so the page's own bloom runs.

    python -X utf8 reference/ink-pages/about-promise/film_compare.py [base-url] [key=take@px/phone ...]

Out: plates/films/<key>-<size>.mp4 (git-ignored), trimmed to the scroll and the bloom.
"""

import shutil
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
IMG = HERE / "plates" / "img"
FILMS = HERE / "plates" / "films"
RAW = FILMS / "raw"

TAKES = {"b": ("wildflowers-2", 112, 80), "c": ("poppy-count-1", 170, 92)}
SIZES = [("desk", 1440, 900, 1), ("phone", 390, 844, 2)]
# Seconds kept after the scroll starts: the glide (1.6s) and the blooms (the last starts 780ms in,
# each takes about 3.4s to settle), and a moment of rest.
KEEP = 6.0

SWAP = """([take, px, phone]) => {
  const imgs = [...document.querySelectorAll('[data-part="promise"] [data-promise] > img')];
  const style = document.createElement('style');
  style.textContent = `
    [data-part="promise"] [data-promise] > img { width: clamp(${Math.round(px * 0.7)}px, ${(px / 14.4).toFixed(2)}vw, ${px}px) !important; }
    @media (max-width: 599px) {
      [data-part="promise"] [data-promise] { --row-picture: ${phone}px !important; }
      [data-part="promise"] [data-promise] > img { width: 100% !important; }
    }`;
  document.head.append(style);
  return Promise.all(imgs.map((img, i) => new Promise((done) => {
    img.loading = 'eager';
    img.removeAttribute('srcset');
    img.removeAttribute('sizes');
    img.src = `/__mock/${take}-${i + 1}.png`;
    if (img.complete && img.naturalWidth) done(true);
    else { img.onload = () => done(true); img.onerror = () => done(false); }
    setTimeout(() => done(false), 20000);
  }))).then((all) => all.every(Boolean));
}"""

# Start with the part just below the window (the sequoia's numbers in view).
BEFORE = """() => {
  const r = document.querySelector('[data-part="promise"]').getBoundingClientRect();
  scrollTo(0, r.top + scrollY - innerHeight * 0.98);
}"""

# Glide down until the part sits in the middle of the window (or starts under the menu bar).
GLIDE = """() => new Promise((done) => {
  const r = document.querySelector('[data-part="promise"]').getBoundingClientRect();
  const bar = document.querySelector('header')?.getBoundingClientRect().bottom ?? 0;
  const y = r.top + scrollY;
  const to = Math.max(0, r.height < innerHeight - bar ? y - bar - (innerHeight - bar - r.height) / 2 : y - bar);
  const from = scrollY, t0 = performance.now(), ms = 1600;
  const step = (now) => {
    const k = Math.min(1, (now - t0) / ms);
    const e = k < 0.5 ? 2 * k * k : 1 - (-2 * k + 2) ** 2 / 2;
    scrollTo(0, from + (to - from) * e);
    if (k < 1) requestAnimationFrame(step); else done(true);
  };
  requestAnimationFrame(step);
})"""


def serve(route):
    name = route.request.url.split("/__mock/")[1].split("?")[0]
    route.fulfill(path=str(IMG / name), content_type="image/png")


def main():
    args = sys.argv[1:]
    base = next((a for a in args if "://" in a), "https://bigh-website-demo.vercel.app").rstrip("/")
    takes = dict(TAKES)
    for a in args:
        key, _, rest = a.partition("=")
        if rest and "://" not in a:
            take, _, sizes = rest.partition("@")
            px, _, phone = sizes.partition("/")
            takes[key] = (take, int(px), int(phone))
    FILMS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--use-angle=d3d11"])
        for key, (take, px, phone) in takes.items():
            for size, vw, vh, dpr in SIZES:
                shutil.rmtree(RAW, ignore_errors=True)
                ctx = browser.new_context(
                    viewport={"width": vw, "height": vh},
                    device_scale_factor=dpr,
                    is_mobile=dpr == 2,
                    has_touch=dpr == 2,
                    record_video_dir=str(RAW),
                    # The recording is in CSS pixels whatever the device scale (a larger size only pads it).
                    record_video_size={"width": vw, "height": vh},
                )
                t0 = time.monotonic()
                page = ctx.new_page()
                page.route("**/__mock/**", serve)
                page.goto(f"{base}/about", wait_until="networkidle")
                page.evaluate("document.fonts.ready")
                if not page.evaluate(SWAP, [take, px, phone]):
                    print("FAIL pictures did not load", key, size)
                page.evaluate(BEFORE)
                page.wait_for_timeout(1500)
                start = time.monotonic() - t0 - 0.6
                page.evaluate(GLIDE)
                page.wait_for_timeout(int((KEEP - 1.6) * 1000) + 400)
                states = page.evaluate(
                    "[...document.querySelectorAll('[data-part=\"promise\"] [data-promise] > img')].map(i => i.dataset.bloom)"
                )
                video = page.video.path()
                ctx.close()
                out = FILMS / f"{key}-{size}.mp4"
                width = 1280 if size == "desk" else vw
                subprocess.run(
                    ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{max(0, start):.2f}", "-i", str(video),
                     "-t", f"{KEEP + 0.6:.2f}", "-vf", f"scale={width}:-2,fps=30", "-c:v", "libx264",
                     "-pix_fmt", "yuv420p", "-crf", "24", "-preset", "slow", "-movflags", "+faststart",
                     "-an", str(out)],
                    check=True,
                )
                print(key, size, "blooms", states, out.name, out.stat().st_size)
        browser.close()


if __name__ == "__main__":
    main()

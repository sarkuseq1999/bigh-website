"""Film the built About page's closing arriving, motion on (Mo picked B, November 13, 2026).

Scrolling down from the promise dots, the tide pool blooms in (the kit's ink bloom), then rests.

    python -X utf8 reference/ink-pages/about-closing/film_built.py [base-url]

Out: plates/films/built-<size>.mp4 (git-ignored).
"""

import shutil
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
FILMS = HERE / "plates" / "films"
RAW = FILMS / "raw"
SIZES = [("desk", 1440, 900, 1), ("phone", 390, 844, 2)]
# Seconds kept after the scroll starts: the glide (1.6s), the bloom (about 3.4s) and a moment of rest.
KEEP = 5.5

# Start with the part just below the window (the sequoia's numbers in view).
BEFORE = """() => {
  const r = document.querySelector('[data-part="closing"]').getBoundingClientRect();
  scrollTo(0, r.top + scrollY - innerHeight * 0.98);
}"""

# Glide down until the part sits in the middle of the window (or starts under the menu bar).
GLIDE = """() => new Promise((done) => {
  const r = document.querySelector('[data-part="closing"]').getBoundingClientRect();
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



def main():
    base = next((a for a in sys.argv[1:] if "://" in a), "http://localhost:3105").rstrip("/")
    FILMS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--use-angle=d3d11"])
        for size, vw, vh, dpr in SIZES:
            shutil.rmtree(RAW, ignore_errors=True)
            ctx = browser.new_context(
                viewport={"width": vw, "height": vh},
                device_scale_factor=dpr,
                is_mobile=dpr == 2,
                has_touch=dpr == 2,
                record_video_dir=str(RAW),
                record_video_size={"width": vw, "height": vh},
            )
            t0 = time.monotonic()
            page = ctx.new_page()
            page.goto(f"{base}/about", wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            page.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
            page.evaluate(BEFORE)
            page.wait_for_timeout(1500)
            start = time.monotonic() - t0 - 0.6
            page.evaluate(GLIDE)
            page.wait_for_timeout(int((KEEP - 1.6) * 1000) + 400)
            state = page.evaluate("document.querySelector('[data-part=closing] [data-picture] img').dataset.bloom")
            video = page.video.path()
            ctx.close()
            out = FILMS / f"built-{size}.mp4"
            width = 1280 if size == "desk" else vw
            subprocess.run(
                ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{max(0, start):.2f}", "-i", str(video),
                 "-t", f"{KEEP + 0.6:.2f}", "-vf", f"scale={width}:-2,fps=30", "-c:v", "libx264",
                 "-pix_fmt", "yuv420p", "-crf", "24", "-preset", "slow", "-movflags", "+faststart",
                 "-an", str(out)],
                check=True,
            )
            print(size, "bloom", state, out.name, out.stat().st_size)
        browser.close()


if __name__ == "__main__":
    main()

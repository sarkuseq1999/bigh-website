"""Film the built About page's coloured dots arriving, motion on (Mo picked A, November 12, 2026).

As film_compare.py, but on the page's own pictures (nothing swapped in): scrolling down from the
sequoia, the four dots bloom in one after another (the kit's ink bloom, 260ms apart), then rest.

    python -X utf8 reference/ink-pages/about-promise/film_built.py [base-url]

Out: plates/films/built-<size>.mp4 (git-ignored).
"""

import shutil
import subprocess
import sys
import time

from playwright.sync_api import sync_playwright

from film_compare import BEFORE, FILMS, GLIDE, KEEP, RAW, SIZES


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
            states = page.evaluate(
                "[...document.querySelectorAll('[data-part=\"promise\"] [data-promise] > img')].map(i => i.dataset.bloom)"
            )
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
            print(size, "blooms", states, out.name, out.stat().st_size)
        browser.close()


if __name__ == "__main__":
    main()

"""A short film of the built Science opening for Mo: it rests on the first screen (the gold adrift),
scrolls through the whole pull-back, and rests on the last view.

  python -X utf8 reference/ink-pages/mockups/science-hero/film_built.py <base-url> [desk|phone ...]

Each frame is set by hand (the scroll's place, and the drift's clock), so the film is even however
slowly the pictures are taken. Films land in built/ beside this script: <size>.mp4 and its first
and last frames as <size>-first.jpg and <size>-last.jpg.
"""

import subprocess
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
OUT = HERE / "built"
OUT.mkdir(exist_ok=True)
args = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = args[0].rstrip("/") if args else "http://localhost:3107"
WANT = args[1:] or ["desk", "phone"]
SIZES = {"desk": (1440, 900, 1, 1280), "phone": (390, 844, 2, 780)}
FPS = 15
REST, RUN = 2.5, 13.0  # seconds: at each end, and for the scroll between them
TO = """([s, t]) => {
  const track = document.querySelector('[data-zoom]');
  scrollTo({ top: track.offsetTop + (track.offsetHeight - innerHeight) * s, behavior: 'instant' });
  for (const a of document.getAnimations()) {
    const target = a.effect && a.effect.target;
    if (target && target.closest('[data-zoom-layer=inside]')) { a.pause(); a.currentTime = t; }
  }
}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    for name in WANT:
        w, h, dense, width = SIZES[name]
        ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=dense)
        pg = ctx.new_page()
        pg.goto(BASE + "/en/science", wait_until="networkidle")
        pg.wait_for_timeout(5000)
        # Every painting on its way out is asked for now, so none arrives mid-film.
        pg.evaluate("document.querySelectorAll('[data-zoom] img').forEach(i => { i.loading = 'eager'; })")
        pg.wait_for_function("[...document.querySelectorAll('[data-zoom] img')].every(i => i.complete && i.naturalWidth > 0)", timeout=15000)
        frames = OUT / f"{name}-frames"
        frames.mkdir(exist_ok=True)
        for old in frames.glob("*.jpg"):
            old.unlink()
        total = int((REST * 2 + RUN) * FPS)
        for f in range(total):
            t = f / FPS
            s = min(1.0, max(0.0, (t - REST) / RUN))
            pg.evaluate(TO, [s, t * 1000])
            # Two frames of the page's own clock, so the scroll script has drawn this place.
            pg.evaluate("() => new Promise(done => requestAnimationFrame(() => requestAnimationFrame(done)))")
            pg.screenshot(path=str(frames / f"{f:04d}.jpg"), type="jpeg", quality=93)
        ctx.close()
        out = OUT / f"{name}.mp4"
        subprocess.run(
            [
                "ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(frames / "%04d.jpg"),
                "-vf", f"scale={width}:-2:flags=lanczos", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-crf", "24", "-preset", "slow", "-movflags", "+faststart", "-an", str(out),
            ],
            check=True,
        )
        for which, index in (("first", 0), ("last", total - 1)):
            im = Image.open(frames / f"{index:04d}.jpg").convert("RGB")
            im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
            im.save(OUT / f"{name}-{which}.jpg", "JPEG", quality=86, optimize=True, progressive=True)
        print("film", out.name, round(out.stat().st_size / 1024), "KB")
    b.close()

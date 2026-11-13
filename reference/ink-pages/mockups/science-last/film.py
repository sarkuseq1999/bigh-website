"""A short looping film of a choice at rest (the kite swaying), for Mo's review page.

  python -X utf8 reference/ink-pages/mockups/science-last/film.py <name> [base-url] [desk|phone ...]

Opens the page as shoot.py does, then sets the mock layers' clock by hand for each frame (one
whole sway, there and back), so the film is even however slowly the pictures are taken. Writes
review/<name>-<size>.mp4 beside this script (h264, no sound) and its first frame as the poster.
"""

import subprocess
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

from shoot import BASE, PLATES, serve, shoot

HERE = Path(__file__).resolve().parent
REVIEW = HERE / "review"
REVIEW.mkdir(exist_ok=True)
args = [a for a in sys.argv[1:] if not a.startswith("http")]
NAME = args[0]
WANT = args[1:] or ["desk", "phone"]
SIZES = {"desk": (1440, 900, 1, 1280), "phone": (390, 844, 2, 600)}
FPS = 12
CYCLE = 9.6  # seconds: the sway there and back (4.8 s each way)
SET = """(t) => { for (const a of document.getAnimations()) {
  if (a.animationName && a.animationName.startsWith('mock-')) { a.pause(); a.currentTime = t; } } }"""

with sync_playwright() as p:
    b = p.chromium.launch()
    for size in WANT:
        w, h, dense, width = SIZES[size]
        ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=dense)
        ctx.route("**/__mock/**", serve)
        pg = ctx.new_page()
        shoot(pg, NAME, "phone" if size == "phone" else "desk")
        frames = PLATES / "films" / f"{NAME}-{size}"
        frames.mkdir(parents=True, exist_ok=True)
        for old in frames.glob("*.jpg"):
            old.unlink()
        total = round(CYCLE * FPS)
        for f in range(total):
            pg.evaluate(SET, 1000 + f * 1000 / FPS)
            pg.evaluate("() => new Promise(done => requestAnimationFrame(() => requestAnimationFrame(done)))")
            pg.screenshot(path=str(frames / f"{f:04d}.jpg"), type="jpeg", quality=92)
        ctx.close()
        out = REVIEW / f"{NAME}-{size}.mp4"
        subprocess.run(
            [
                "ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(frames / "%04d.jpg"),
                "-vf", f"scale={width}:-2:flags=lanczos", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-crf", "24", "-preset", "slow", "-movflags", "+faststart", "-an", str(out),
            ],
            check=True,
        )
        im = Image.open(frames / "0000.jpg").convert("RGB")
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        im.save(REVIEW / f"{NAME}-{size}-poster.jpg", "JPEG", quality=84, optimize=True, progressive=True)
        print("film", out.name, round(out.stat().st_size / 1024), "KB", flush=True)
    b.close()

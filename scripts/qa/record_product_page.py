"""Record calm scroll-through videos of the product page on the real GPU.

Usage: python -X utf8 scripts/qa/record_product_page.py [base] [out-dir] [--only opening,page]
Writes <out-dir>/opening.mp4 (the first screen: the arrival, a moment of stillness with the
pointer drifting across, then the first scroll away) and page.mp4 (the whole page, top to
bottom). H.264, 1280×800. The page scrolls at a steady reading pace; the long 3D moments get a
slower pace so each beat can be read.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].startswith("http") else "http://localhost:3007"
OUT = (
    Path(sys.argv[2])
    if len(sys.argv) > 2 and not sys.argv[2].startswith("--")
    else Path(__file__).parent / "out" / "videos"
)
OUT.mkdir(parents=True, exist_ok=True)
SIZE = {"width": 1280, "height": 800}

# Scroll to `end` (or the bottom) at `speed` px/s; sections marked slow get `slow` px/s.
SCROLL = """async ({ speed, slow, pause, end }) => {
  document.documentElement.style.scrollBehavior = 'auto';
  await new Promise(r => setTimeout(r, pause));
  const bottom = end ?? document.documentElement.scrollHeight - innerHeight;
  const slowZones = [...document.querySelectorAll("[aria-label='Inside the capsule'], #chapter-why")]
    .map(e => { const r = e.getBoundingClientRect(); return [r.top + scrollY, r.bottom + scrollY - innerHeight]; });
  let y = scrollY;
  let last = performance.now();
  await new Promise(resolve => {
    const tick = now => {
      const inSlow = slowZones.some(([a, b]) => y >= a && y <= b);
      y = Math.min(bottom, y + (inSlow ? slow : speed) * (now - last) / 1000);
      last = now;
      window.scrollTo(0, y);
      if (y >= bottom) return resolve();
      requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  });
  await new Promise(r => setTimeout(r, 1500));
}"""


def encode(raw: str, target: Path) -> None:
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error", "-i", raw,
            "-c:v", "libx264", "-preset", "slow", "-crf", "27", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", "-an", str(target),
        ],
        check=True,
    )
    print(target, round(target.stat().st_size / 1e6, 1), "MB")


with sync_playwright() as p:
    browser = p.chromium.launch(args=["--use-gl=angle", "--use-angle=d3d11", "--enable-gpu", "--ignore-gpu-blocklist"])
    runs = (("opening", False), ("page", True))
    # --only page records just that one (a stalled capture can be redone alone).
    only = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
    for name, full in runs:
        if only and name not in only:
            continue
        with tempfile.TemporaryDirectory() as raw:
            ctx = browser.new_context(viewport=SIZE, record_video_dir=raw, record_video_size=SIZE)
            page = ctx.new_page()
            page.goto(f"{BASE}/products/nuricell", wait_until="networkidle")
            if full:
                page.evaluate(SCROLL, {"speed": 560, "slow": 300, "pause": 4200, "end": None})
            else:
                page.wait_for_timeout(3600)
                # A slow drift of the pointer, so the bottle turns toward it.
                for step in range(60):
                    page.mouse.move(300 + step * 11, 420 + (step % 20) * 2)
                    page.wait_for_timeout(45)
                page.evaluate(SCROLL, {"speed": 320, "slow": 320, "pause": 400, "end": 800 * 1.3})
            video = page.video.path()
            ctx.close()
            encode(video, OUT / f"{name}.mp4")
    browser.close()

"""Record calm scroll-through videos of the homepage redesign looks on the real GPU.

Usage: python -X utf8 scripts/qa/record_home_looks.py [base] [out-dir] [--looks home,kr,jp]
       [--phone] [--pause 11000]
Writes <out-dir>/<look>.mp4 (desktop 1280×800) or <look>-phone.mp4 (390×844). H.264, no sound.
The page waits on the opening (--pause, milliseconds; 4500 by default, 11000 shows the crane's
first wingbeat), then scrolls at a steady reading pace to the bottom. The review switcher is
hidden.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

PAUSE = int(sys.argv[sys.argv.index("--pause") + 1]) if "--pause" in sys.argv else 4500
skip = {sys.argv[i + 1] for i, a in enumerate(sys.argv[:-1]) if a in ("--looks", "--pause")}
args = [a for a in sys.argv[1:] if not a.startswith("--") and a not in skip]
BASE = args[0] if args else "http://localhost:3014"
OUT = Path(args[1]) if len(args) > 1 else Path(__file__).parent / "out" / "home-videos"
OUT.mkdir(parents=True, exist_ok=True)
LOOKS = (
    sys.argv[sys.argv.index("--looks") + 1].split(",")
    if "--looks" in sys.argv
    else ["home"]
)
PHONE = "--phone" in sys.argv
SIZE = {"width": 390, "height": 844} if PHONE else {"width": 1280, "height": 800}

SCROLL = """async ({ speed, pause }) => {
  document.documentElement.style.scrollBehavior = 'auto';
  await new Promise(r => setTimeout(r, pause));
  let y = scrollY;
  let last = performance.now();
  await new Promise(resolve => {
    const tick = now => {
      const bottom = document.documentElement.scrollHeight - innerHeight;
      y = Math.min(bottom, y + speed * (now - last) / 1000);
      last = now;
      window.scrollTo(0, y);
      if (y >= bottom) return resolve();
      requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  });
  await new Promise(r => setTimeout(r, 1800));
}"""


def encode(raw: str, target: Path) -> None:
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error", "-i", raw,
            "-c:v", "libx264", "-preset", "slow", "-crf", "28", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", "-an", str(target),
        ],
        check=True,
    )
    print(target, round(target.stat().st_size / 1e6, 1), "MB")


with sync_playwright() as p:
    browser = p.chromium.launch(
        args=["--use-gl=angle", "--use-angle=d3d11", "--enable-gpu", "--ignore-gpu-blocklist"]
    )
    for look in LOOKS:
        with tempfile.TemporaryDirectory() as raw:
            ctx = browser.new_context(
                viewport=SIZE,
                record_video_dir=raw,
                record_video_size=SIZE,
                is_mobile=PHONE,
                has_touch=PHONE,
                device_scale_factor=2 if PHONE else 1,
            )
            page = ctx.new_page()
            url = f"{BASE}/" if look == "home" else f"{BASE}/{look}"  # "home" = the homepage; else a locale
            page.goto(url, wait_until="networkidle", timeout=120000)
            page.add_style_tag(content="[data-look-switcher]{display:none!important}")
            page.evaluate(SCROLL, {"speed": 300 if PHONE else 420, "pause": PAUSE})
            video = page.video.path()
            ctx.close()
            encode(video, OUT / f"{look}{'-phone' if PHONE else ''}.mp4")
    browser.close()

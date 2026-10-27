"""Films of the About circle mockups (shoot.py's looks), so the motion can be judged: the page opens,
the circle paints itself, and whatever the gold does. Laptop (1440x900) and phone (390x844).

    python -X utf8 reference/ink-pages/mockups/about-circle-size/film.py [base] [look,look,...]
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

from shoot import BASE, INIT, LOOKS, OUT

ONLY = next((a.split(",") for a in sys.argv[1:] if not a.startswith("http")), None)
FILMS = {
    "laptop": dict(width=1440, height=900),
    "phone": dict(width=390, height=844),
}
SECONDS = 11


def encode(raw: str, target: Path) -> None:
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error", "-i", raw,
            "-c:v", "libx264", "-preset", "slow", "-crf", "26", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", "-an", str(target),
        ],
        check=True,
    )
    print(target.name, round(target.stat().st_size / 1e6, 2), "MB")


with sync_playwright() as p:
    browser = p.chromium.launch(args=["--use-angle=d3d11"])
    for look, css in LOOKS.items():
        if ONLY and look not in ONLY:
            continue
        for size, vp in FILMS.items():
            with tempfile.TemporaryDirectory() as raw:
                ctx = browser.new_context(
                    viewport=vp,
                    record_video_dir=raw,
                    record_video_size=vp,
                    is_mobile=size == "phone",
                    has_touch=size == "phone",
                )
                page = ctx.new_page()
                page.add_init_script(INIT % json.dumps(css))
                page.goto(f"{BASE}/about", wait_until="domcontentloaded")
                page.wait_for_timeout(SECONDS * 1000)
                video = page.video.path()
                ctx.close()
                encode(video, OUT / f"{look}-{size}.mp4")
    browser.close()

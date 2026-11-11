"""Turn shoot_hero.py's frames into short looping films, and its stills into the review's pictures.

  python -X utf8 reference/ink-pages/mockups/science-hero/make_loops.py

Reads reference/ink-pages/science/plates/hero/shots/ and writes into review/ beside this script:
  <idea>-<size>.mp4   one loop of the idea's resting motion (h264, no sound)
  <idea>-<size>.jpg   the still (the film's poster, and what shows if a film cannot play)
  step-*.jpg          today's views used in the "when you scroll" strips
"""

import subprocess
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
SHOTS = HERE.parent.parent / "science" / "plates" / "hero" / "shots"
OUT = HERE / "review"
OUT.mkdir(exist_ok=True)
FPS = 10
WIDTH = {"desk": 1280, "phone": 780}

for frames in sorted(SHOTS.glob("*-frames")):
    key, size = frames.name.removesuffix("-frames").rsplit("-", 1)
    if not any(frames.glob("*.jpg")):
        continue
    out = OUT / f"{key}-{size}.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(frames / "%04d.jpg"),
            "-vf", f"scale={WIDTH[size]}:-2:flags=lanczos", "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-crf", "23", "-preset", "slow", "-movflags", "+faststart", "-an", str(out),
        ],
        check=True,
    )
    print("film", out.name, round(out.stat().st_size / 1024), "KB")

for still in sorted(SHOTS.glob("*.png")):
    name = still.stem
    if not name.endswith(("-desk", "-phone", "-s1", "-s2")):
        continue  # a check sheet, not a page picture
    im = Image.open(still).convert("RGB")
    if name.startswith("today-") and "-s" in name:
        # today-desk-s1 (the hand), today-desk-s2 (the cell): small pictures for the strips
        out = OUT / f"step-{name.removeprefix('today-')}.jpg"
        im.thumbnail((640, 640), Image.LANCZOS)
    else:
        out = OUT / f"{name}.jpg"
        size = name.rsplit("-", 1)[1]
        if im.width > WIDTH.get(size, 1280):
            im = im.resize((WIDTH[size], round(im.height * WIDTH[size] / im.width)), Image.LANCZOS)
    im.save(out, "JPEG", quality=86, optimize=True, progressive=True)
print("pictures in", OUT)

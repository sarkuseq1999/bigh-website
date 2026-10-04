"""Build the opening crane's wingbeat from the Kling loop (round 5, October 3, 2026).

The loop (originals/crane-fly-v1.mp4, Kling 3.0 pro from the approved crane painting, first and
last frame the same) is the crane on plain rice paper. Every second frame is cut out the same way
the still crane was (BiRefNet, local) at the still's own registration (the full frame at 1600 px
wide), then the frames are saved as one animated webp with alpha: the glide pose is held a moment,
one slow wingbeat plays, the glide pose is held again for longer, and so on forever (the first
beat comes soon after the picture appears; after that, about one beat every four breaths). The
page shows it in the still crane's place once it has loaded.

Output: public/images/home-v2/ink/crane-flight.webp (900 px) and crane-flight-600.webp (phones).

usage: python -X utf8 reference/home-v2/ink/build_crane_flight.py [--frames-only]
"""

import subprocess
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SOURCE = HERE / "originals" / "crane-fly-v1.mp4"
WORK = HERE / "work" / "crane-flight"
OUT = REPO / "public/images/home-v2/ink"
STEP = 2  # every second frame: 12 a second from Kling's 24
FRAME_MS = 70  # a little faster than filmed (83 ms), so the beat is about four seconds
LEAD_MS = 1400  # the glide before the first beat (and the start of every glide after it)
HOLD_MS = 4200  # the rest of the glide after a beat: with the beat, about four of the page's breaths


def frames():
    raw = WORK / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    if not any(raw.glob("f*.png")):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(SOURCE), str(raw / "f%03d.png")],
                       check=True)
    files = sorted(raw.glob("f*.png"))
    # The last frame repeats the first (the loop's end pose), so it is left out.
    return files[:-1:STEP]


def cut_all(files):
    from rembg import new_session, remove

    session = new_session("birefnet-general")
    cut = WORK / "cut"
    cut.mkdir(parents=True, exist_ok=True)
    out = []
    for i, path in enumerate(files):
        target = cut / f"c{i:03d}.png"
        if not target.exists():
            frame = Image.open(path).convert("RGB").resize((1600, 1062), Image.LANCZOS)
            remove(frame, session=session).save(target)
            print("cut", target.name, flush=True)
        out.append(target)
    return out


def animate(cuts, width, name, quality):
    height = round(1062 * width / 1600)
    images = [Image.open(c).convert("RGBA").resize((width, height), Image.LANCZOS) for c in cuts]
    # Glide (the first frame), the beat, then the first frame again for the long glide.
    durations = [LEAD_MS] + [FRAME_MS] * (len(images) - 1) + [HOLD_MS]
    images = images + [images[0]]
    path = OUT / name
    images[0].save(path, "WEBP", save_all=True, append_images=images[1:], duration=durations,
                   loop=0, quality=quality, method=4, minimize_size=False, allow_mixed=False)
    print(f"{path.relative_to(REPO)}  {width}x{height}  {len(images) - 1} frames  "
          f"{path.stat().st_size // 1024} KB")


if __name__ == "__main__":
    chosen = frames()
    print(len(chosen), "frames")
    cuts = cut_all(chosen)
    if "--frames-only" not in sys.argv:
        animate(cuts, 900, "crane-flight.webp", 76)
        animate(cuts, 600, "crane-flight-600.webp", 74)

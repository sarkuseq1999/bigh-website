"""Build the opening crane's wingbeat from a Kling loop (round 5, October 3, 2026; v2 October 4;
general for any take from round 8, October 5).

A take (originals/crane-fly-v*.mp4, Kling 3.0 pro from the approved crane painting, first and
last frame the same) is the crane on plain rice paper. Every second frame is cut out the same way
the still crane was (BiRefNet, local) at the still's own registration (the full frame at 1600 px
wide), then the frames are saved as one animated webp with alpha: the glide pose is held a moment,
one slow wingbeat plays, the glide pose is held again for longer, and so on forever (the first
beat comes soon after the picture appears; after that, about one beat every four breaths). The
page shows it in the still crane's place once it has loaded.

Each shipped version is a row in TAKES: its footage, its cut-frame cache, the frames that are
still the first pose (dropped), and its retouch.

v2 (night loop, October 4), from crane-fly-v1, all from the same cut frames, no new footage:
  - the far wing stays behind the head. In two frames of the down-stroke (c020, c021) Kling drew
    its tip across the head, which read as a forked second beak. The head does not move in those
    frames, so the clean head, beak and neck of the next frame (c022) are laid over them and the
    stray feather tips under the neck are cleared. In the frames on either side (c019, c022) the
    tips that reach towards the beak end a little sooner.
  - the cut-out's alpha is cleaned: BiRefNet leaves the bird's inside at 240 to 254 instead of
    255, which the lossless alpha plane paid for in every frame. Snapping it (and the faint haze
    outside the bird) made the file a third smaller with the same picture.
  - the two frames after the first (c001, c002) are the same pose as the first; they are dropped
    (the glide before the beat is as long as before).
  - the held pose keeps full alpha and a higher quality; the moving frames keep the old quality
    with a coarser alpha on their edges (16 levels), which nobody can see in motion.

v3 (round 8, October 5), from a new take, crane-fly-v3 (prompt in originals/crane-fly-v3.json):
in v1 the wings turned into an outline drawing for most of the down-stroke (the grey wash and the
black flight feathers dropped out). The new prompt asks for the painting to stay a painting on
every frame; in this take the black flight feathers stay broad and the wash stays on the far wing
and the body through the beat. The beat starts at once, so no frame is dropped; the far wing goes
behind the head by itself. One retouch: a brush knot at the far wing's tip (c045). Two other takes
were not used: crane-fly-v4 (cfg_scale 0.7) lost the wash like v1, and crane-fly-v5 painted the
crown red. The moving frames are a notch lower in quality (74), for the same weight as v2.

Output: public/images/home-v2/ink/crane-flight-<version>.webp (900 px) and
crane-flight-<version>-600.webp (phones).

usage: python -X utf8 reference/home-v2/ink/build_crane_flight.py <version> [--frames-only]
           [--cut A-B]   (cut only frames A to B, e.g. to judge a take's mid-beat on grey)
"""

import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, _webp  # _webp: Pillow's own animation encoder (12.1), for per-frame quality

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
OUT = REPO / "public/images/home-v2/ink"
STEP = 2  # every second frame: 12 a second from Kling's 24
FRAME_MS = 70  # a little faster than filmed (83 ms), so the beat is about four seconds
LEAD_MS = 1400  # the glide before the first beat (and the start of every glide after it)
HOLD_MS = 4200  # the rest of the glide after a beat: with the beat, about four of the page's breaths


def retouch_v2(images):
    """crane-fly-v1: the far wing kept behind the head (c019 to c022)."""
    clean = images[22].copy()  # the first frame after the far wing has passed the head
    # c019: the wing is still above the head, its tips reaching 100 px up past the crown before
    # they vanish behind it in the next frame. They end sooner (fading over 26 px), so the wing
    # goes behind the head in two steps, not one.
    yy, xx = np.mgrid[380:504, 1100:1340]
    along = (xx - 1150) * 0.66 + (470 - yy) * 0.75
    keep = np.clip(1 - along / 26, 0, 1)
    images[19][380:504, 1100:1340, 3] = (images[19][380:504, 1100:1340, 3] * keep).astype(np.uint8)
    # c020: the wing's tips fork up from behind the forehead, over the beak.
    images[20][420:548, 1166:1340] = clean[420:548, 1166:1340]
    # c021: the tips cross the beak and run on under it, beside the neck.
    images[21][420:597, 1100:1340] = clean[420:597, 1100:1340]
    images[21][573:597, 1040:1100] = clean[573:597, 1040:1100]
    images[21][597:665, 1066:1340, 3] = 0
    # c022: the wing is out from under the neck, but its outer tips still hook up towards the
    # beak. They end sooner, fading over 22 px along the stroke.
    yy, xx = np.mgrid[560:700, 1190:1340]
    along = (xx - 1205) * 0.75 + (648 - yy) * 0.66
    keep = np.clip(1 - along / 22, 0, 1)
    images[22][560:700, 1190:1340, 3] = (images[22][560:700, 1190:1340, 3] * keep).astype(np.uint8)
    return images


def retouch_v3(images):
    """crane-fly-v3: one stray brush knot at the far wing's tip on the up-stroke (c045)."""
    # c045: the tip of the far wing ends in a small closed loop with a dot in it, which reads as
    # a tiny second head for one frame. The wing ends a few pixels sooner instead.
    xx = np.mgrid[325:375, 970:1040][1]
    keep = np.clip((990 - xx) / 10, 0, 1)
    images[45][325:375, 970:1040, 3] = (images[45][325:375, 970:1040, 3] * keep).astype(np.uint8)
    return images


TAKES = {
    "v2": {"source": "crane-fly-v1.mp4", "work": "crane-flight", "same_as_first": (1, 2),
           "retouch": retouch_v2, "quality": 76},
    "v3": {"source": "crane-fly-v3.mp4", "work": "crane-flight-v3", "same_as_first": (),
           "retouch": retouch_v3, "quality": 74},
}


def frames(take):
    raw = HERE / "work" / take["work"] / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    if not any(raw.glob("f*.png")):
        source = HERE / "originals" / take["source"]
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(source), str(raw / "f%03d.png")],
                       check=True)
    files = sorted(raw.glob("f*.png"))
    # The last frame repeats the first (the loop's end pose), so it is left out.
    return files[:-1:STEP]


def cut_all(take, files, only=None):
    cut = HERE / "work" / take["work"] / "cut"
    cut.mkdir(parents=True, exist_ok=True)
    session = None
    out = []
    for i, path in enumerate(files):
        target = cut / f"c{i:03d}.png"
        if not target.exists() and (only is None or only[0] <= i <= only[1]):
            from rembg import new_session, remove

            session = session or new_session("birefnet-general")
            frame = Image.open(path).convert("RGB").resize((1600, 1062), Image.LANCZOS)
            remove(frame, session=session).save(target)
            print("cut", target.name, flush=True)
        out.append(target)
    return out


def sized(image, width):
    """One frame at the shipping width, its alpha snapped to solid inside and clear outside."""
    height = round(1062 * width / 1600)
    small = np.asarray(Image.fromarray(image, "RGBA").resize((width, height), Image.LANCZOS)).copy()
    alpha = small[..., 3].astype(np.float32)
    small[..., 3] = (np.clip((alpha - 8) / (247 - 8), 0, 1) * 255).round().astype(np.uint8)
    return Image.fromarray(small, "RGBA")


def animate(take, images, width, name, quality):
    beat = [i for i in range(1, len(images)) if i not in take["same_as_first"]]
    # Glide (the first frame), the beat, then the first frame again for the long glide.
    # (frame, milliseconds, quality, alpha quality)
    plan = [(0, LEAD_MS, 82, 100)] + [(i, FRAME_MS, quality, 70) for i in beat] + [(0, HOLD_MS, 82, 100)]
    ready = {i: sized(images[i], width) for i in {0, *beat}}
    encoder = _webp.WebPAnimEncoder(ready[0].size, 0, 0, False, 3, 5, False, False)
    at = 0
    for i, ms, q, alpha_q in plan:
        encoder.add(ready[i].getim(), at, False, q, alpha_q, 4)  # method 6 hangs for minutes
        at += ms
    encoder.add(None, at, False, quality, 100, 0)
    path = OUT / name
    path.write_bytes(encoder.assemble("", "", ""))
    print(f"{path.relative_to(REPO)}  {ready[0].width}x{ready[0].height}  {len(plan)} frames  "
          f"{at / 1000:.2f} s a loop  {path.stat().st_size // 1024} KB")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args or args[0] not in TAKES:
        raise SystemExit(f"usage: build_crane_flight.py <{'|'.join(TAKES)}> [--frames-only] [--cut A-B]")
    version = args[0]
    take = TAKES[version]
    only = None
    if "--cut" in sys.argv:
        a, b = sys.argv[sys.argv.index("--cut") + 1].split("-")
        only = (int(a), int(b))
    chosen = frames(take)
    print(len(chosen), "frames")
    cuts = cut_all(take, chosen, only)
    if "--frames-only" not in sys.argv and only is None:
        images = [np.asarray(Image.open(c).convert("RGBA")).copy() for c in cuts]
        fixed = take["retouch"](images) if take["retouch"] else images
        animate(take, fixed, 900, f"crane-flight-{version}.webp", take["quality"])
        animate(take, fixed, 600, f"crane-flight-{version}-600.webp", take["quality"])

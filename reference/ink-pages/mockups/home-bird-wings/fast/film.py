"""Side-by-side before/after films of the hummingbird's wings, from the sprites the page steps through.

    python -X utf8 film.py <before-plates> <after-plates> <out-dir>

Before: 6 frames, the page's old timing (0.1 s beats for 3 s, two of 0.16 s, one of 0.24 s, rest).
After: 11 frames (rest, 8 haze, 2 settle): the haze one frame per screen frame for about 2.93 s,
the settle 0.07 s a frame, then rest. Films at 60 frames a second: arrive.mp4 (real speed, then
2 s of rest), and still frames lowest.jpg (one haze frame beside the old lowest frame).
"""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FPS = 60
PAPER = (245, 240, 230, 255)
CROP = (180, 90, 1180, 960)


def frames(plates):
    rig = json.loads((plates / "rig.json").read_text(encoding="utf-8"))
    body = Image.open(plates / "body.png").convert("RGBA")
    W, H = body.size
    b = rig["box"]
    box = (round(b["left"] / 100 * W), round(b["top"] / 100 * H))
    size = (round(b["width"] / 100 * W), round(b["height"] / 100 * H))
    n = rig["frames"]
    strips = {s: Image.open(plates / f"{s}.png").convert("RGBA") for s in ("near", "far")}
    fw = strips["near"].width // n
    out = []
    for k in range(n):
        layers = {}
        for s, strip in strips.items():
            f = strip.crop((k * fw, 0, (k + 1) * fw, strip.height)).resize(size, Image.LANCZOS)
            layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            layer.paste(f, box)
            layers[s] = layer
        img = Image.new("RGBA", (W, H), PAPER)
        img = Image.alpha_composite(img, layers["far"])
        img = Image.alpha_composite(img, body)
        img = Image.alpha_composite(img, layers["near"])
        out.append(img.convert("RGB").crop(CROP))
    return out


def before_seq(total):
    seq = []
    for _ in range(30):
        seq += list(range(6))
    for _ in range(2):
        for k in range(6):
            seq += [k] * (2 if k % 2 == 0 else 1)  # 0.16 s a beat, about 9.6 screen frames
    for k in range(6):
        seq += [k] * (3 if k % 2 == 0 else 2)  # 0.24 s a beat
    return (seq + [0] * total)[:total]


def after_seq(total):
    seq = []
    for _ in range(22):
        seq += list(range(1, 9))
    seq += [9] * 4 + [10] * 4
    return (seq + [0] * total)[:total]


def main():
    before, after, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    out.mkdir(parents=True, exist_ok=True)
    fb, fa = frames(before), frames(after)
    font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 30)
    w, h = fb[0].size

    def pair(a, b):
        img = Image.new("RGB", (w * 2 + 12, h + 50), (255, 255, 255))
        d = ImageDraw.Draw(img)
        for i, (im, label) in enumerate(zip((a, b), ("A  Today", "B  Fast"))):
            img.paste(im, (i * (w + 12), 50))
            d.text((i * (w + 12) + 16, 6), label, fill=(40, 40, 40), font=font)
        return img

    total = 5 * FPS
    sb, sa = before_seq(total), after_seq(total)
    tmp = Path(tempfile.mkdtemp())
    cache = {}
    for i in range(total):
        key = (sb[i], sa[i])
        if key not in cache:
            cache[key] = pair(fb[sb[i]], fa[sa[i]])
        cache[key].save(tmp / f"f{i:05d}.png")
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(tmp / "f%05d.png"),
         "-vf", "scale=1200:-2", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
         "-movflags", "+faststart", str(out / "arrive.mp4")],
        check=True,
    )
    shutil.rmtree(tmp)
    pair(fb[3], fa[2]).save(out / "lowest.jpg", quality=88)
    print("films in", out)


if __name__ == "__main__":
    main()

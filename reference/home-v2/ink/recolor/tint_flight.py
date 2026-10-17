"""Turn the flying crane's ochre crown red in every frame of the animated wingbeat (green spring,
October 16, 2026): public/images/home-v2/ink/spring/crane-flight-a2-twice[-600].webp.
usage: python -X utf8 reference/home-v2/ink/recolor/tint_flight.py"""
from pathlib import Path
import numpy as np
from PIL import Image

INK = Path(__file__).resolve().parents[4] / "public" / "images" / "home-v2" / "ink"
CROWN = {"spring": "#d4482f"}


def smooth(x, a, b):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def tint(frame, hexc):
    a = np.asarray(frame.convert("RGBA"), dtype=np.float64) / 255
    rgb, al = a[..., :3], a[..., 3:]
    h, w = rgb.shape[:2]
    sat = rgb.max(2) - rgb.min(2)
    warm = (rgb[..., 0] > rgb[..., 2] + 0.03).astype(float)
    core = (sat > 0.15) & (rgb[..., 0] > rgb[..., 2] + 0.08) & (al[..., 0] > 0.5)
    ys, xs = np.nonzero(core[:, int(w * 0.62):])
    xs = xs + int(w * 0.62)
    if not len(xs):
        return frame.convert("RGBA")
    cx, cy = np.median(xs) / w, np.median(ys) / h
    yy, xx = np.mgrid[0:h, 0:w]
    box = np.exp(-(((xx / w - cx) / 0.035) ** 2 + ((yy / h - cy) / 0.03) ** 2) * 2.2)
    m = (smooth(sat, 0.04, 0.12) * warm * box)[..., None]
    c = np.array([int(hexc[i:i + 2], 16) for i in (1, 3, 5)]) / 255
    lum = rgb.mean(2, keepdims=True)
    red = np.clip(c * (lum / c.mean()) ** 0.8, 0, 1)
    out = rgb * (1 - m) + red * m
    return Image.fromarray((np.concatenate([out, al], 2) * 255 + 0.5).astype(np.uint8), "RGBA")


for name in ["crane-flight-a2-twice.webp", "crane-flight-a2-twice-600.webp"]:
    src = Image.open(INK / name)
    frames, durations = [], []
    for i in range(src.n_frames):
        src.seek(i)
        durations.append(src.info.get("duration", 40))
        frames.append(src.copy().convert("RGBA"))
    loop = src.info.get("loop", 0)
    for look, hexc in CROWN.items():
        tinted = [tint(f, hexc) for f in frames]
        out = INK / look / name
        tinted[0].save(out, "WEBP", save_all=True, append_images=tinted[1:], duration=durations,
                       loop=loop, quality=76, method=4)
        print(look, name, src.n_frames, "frames", round(out.stat().st_size / 1e6, 2), "MB (was",
              round((INK / name).stat().st_size / 1e6, 2), ")", "durations", sorted(set(durations))[:4])

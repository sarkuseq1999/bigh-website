"""Turmerific's opening (November 16, 2026): get a Codex painting ready to lie on
the page as art/<out>.png, and print where its ridge and its foreground are for the mock.

usage: python -X utf8 prep.py <take> <out> [end] [fade]
       python -X utf8 prep.py front <out> <stand>   (after the first: art/<out>-front.png)
  <take>  originals/<take>.png in reference/ink-pages/turmerific/ ("opening-spring-ah", ...)
  <out>   art/<out>.png here
  end     the row (share of the height) where the painting is over (default 0.8)
  fade    over how much of the height its last specks fade into bare paper (default 0.035)

The sheet's own white is divided out (its foot is bare paper), so the painting multiplies onto the
page's paper with no box, as NuriCell's clear day does (prep6.py in mockups/nuricell-opening/).
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).parent
ART = HERE / "art"
ART.mkdir(exist_ok=True)
ORIG = HERE.parents[1] / "turmerific" / "originals"


def main(take, out, end=0.8, fade=0.035):
    a = np.asarray(Image.open(ORIG / f"{take}.png").convert("RGB")).astype(np.float32)
    h, w, _ = a.shape
    paper = np.median(a[int(h * 0.93) :].reshape(-1, 3), axis=0)
    d = np.clip(a / paper * 255.0, 0, 255)
    d = np.where(d.min(axis=2, keepdims=True) > 249, 255.0, d)
    # The sky's foot: where the middle columns stop being sky blue (blue well over red).
    mid = d[:, int(w * 0.3) : int(w * 0.7)].mean(axis=1)
    blue = mid[:, 2] - mid[:, 0]
    sky = np.where(blue[int(h * 0.3) :] < blue[int(h * 0.3)] * 0.45)[0]
    ridge = int(sky[0] + h * 0.3) if len(sky) else int(h * 0.6)
    # The middle's ground: the lowest painted row of the middle 42-58% (the empty spot).
    centre = d[:, int(w * 0.42) : int(w * 0.58)]
    painted = np.where((centre.min(axis=2) < 230).sum(axis=1) > 4)[0]
    ground = int(painted[painted > ridge][-1]) if len(painted[painted > ridge]) else int(h * 0.72)
    allp = np.where((d.min(axis=2) < 240).sum(axis=1) > 3)[0]
    print(f"{take}: {w}x{h} ridge {ridge} ({ridge / h:.4f}) middle ground to {ground} ({ground / h:.4f}) last paint {allp[-1]} ({allp[-1] / h:.4f})")
    y = (np.arange(h) / h)[:, None, None]
    k = np.clip((y - (float(end) - float(fade))) / float(fade), 0, 1)
    d = d * (1 - k) + 255 * k
    Image.fromarray(np.clip(d, 0, 255).astype(np.uint8)).save(ART / f"{out}.png")
    return d


def front(out, stand, half=250, up=34, down=40):
    """The painting's own grass round the bottle's foot, as a layer laid over the bottle: only its
    strokes (the pale ground wash under them becomes transparent), fading out upward, so the bottle
    stands in the grass rather than on top of the picture (AGENTS.md: a front layer seats it).
    Written as art/<out>-front.png; its box in the painting is printed for sky_<name>.json."""
    d = np.asarray(Image.open(ART / f"{out}.png").convert("RGB")).astype(np.float32)
    h, w, _ = d.shape
    g = int(float(stand) * h)
    c0, c1, r0, r1 = w // 2 - half, w // 2 + half, g - up, g + down
    crop = d[r0:r1, c0:c1]
    # Only the darker strokes (the ground's pale wash would lie twice over the painting's own and
    # show as a darker box), soft at the sides and fading out upward.
    alpha = np.clip((200 - crop.min(axis=2)) / 60, 0, 1)
    t = np.clip(np.arange(r1 - r0) / up, 0, 1)[:, None]
    xs = np.arange(c1 - c0)
    s = np.clip(np.minimum(xs, c1 - c0 - 1 - xs) / 90, 0, 1)[None, :]
    alpha *= (t * t) * (s * s * (3 - 2 * s))
    rgba = np.dstack([crop, alpha * 255]).astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(ART / f"{out}-front.png")
    print(f'front box: "front": [{c0}, {r0}, {c1}, {r1}]')


if __name__ == "__main__":
    if sys.argv[1] == "front":
        front(*sys.argv[2:])
    else:
        main(*sys.argv[1:])

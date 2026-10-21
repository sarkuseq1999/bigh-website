"""Mockup only (October 21, 2026): idea A for "Make sense of the science." -- a hiker on a
California trail, and a round peek inside their cells, tied to the hiker by a 1px ink leader.

Makes two ink plates per stage state (paper divided out, so the page multiplies them onto its
rice paper): the hiker scene (1600 x 1195, the stage) and the cell for the round window (900 x 900,
cropped closer where the detail is small). The page lays the window over the scene and draws
the ring and the leader itself (SVG, 1px at any size). img/leads.json gives each state's leader
start, the hiker's thigh, in stage units.

usage: python -X utf8 reference/ink-pages/mockups/home-science-hiker/compose.py
"""

import json
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ORIG = HERE.parents[1] / "home-science" / "originals"
OUT = HERE / "img"
W, H = 1600, 1195
CELL = 900

# state -> hiker original, cell original, thigh point (hiker original px), cell crop box or None
STATES = {
    "energy": ("hiker-trailhead-a1", "cell-energy-a1", (395, 640), None),
    # the sparks are small: look closer, at the sparking power plant on the right
    "sparks": ("hiker-climb-a1", "cell-sparks-a2", (452, 556), (790, 330, 1230, 770)),
    "age-30": ("hiker-30-a1", "cell-young-a1", (440, 680), None),
    "age-55": ("hiker-55-a1", "cell-middle-a1", (444, 686), None),
    "age-80": ("hiker-80-a1", "cell-old-a1", (440, 690), None),
}


def plate(im, fade=0.08):
    """The painting with its paper divided out and its edges dissolved, floats 0..255."""
    im = np.asarray(im.convert("RGB")).astype(np.float32)
    h, w, _ = im.shape
    b = max(8, min(h, w) // 40)
    border = np.concatenate(
        [im[:b].reshape(-1, 3), im[-b:].reshape(-1, 3), im[:, :b].reshape(-1, 3), im[:, -b:].reshape(-1, 3)]
    )
    flat = np.clip(im / np.median(border, axis=0) * 255.0, 0, 255)
    if not fade:
        return flat
    yy = np.linspace(0, 1, h)[:, None]
    xx = np.linspace(0, 1, w)[None, :]
    d = np.minimum(np.minimum(yy, 1 - yy) / fade, np.minimum(xx, 1 - xx) / (fade * h / w))
    a = np.clip(d, 0, 1)
    a = (a * a * (3 - 2 * a))[..., None]
    return 255 - (255 - flat) * a


def save(arr, name):
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(OUT / f"{name}.webp", quality=88)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    leads = {}
    for state, (hiker, cell, thigh, crop) in STATES.items():
        # the scene: the hiker painting scaled to the stage's width, standing on its foot
        him = Image.open(ORIG / f"{hiker}.png")
        k = W / him.width
        hh = round(him.height * k)
        scene = np.full((H, W, 3), 255.0, np.float32)
        scene[H - hh :] = plate(him.resize((W, hh), Image.LANCZOS))
        save(scene, f"scene-{state}")
        leads[state] = [round(thigh[0] * k), round(H - hh + thigh[1] * k)]
        # the cell: whole, or a closer crop, as a square for the round window
        cim = Image.open(ORIG / f"{cell}.png").convert("RGB")
        flat = Image.fromarray(plate(cim, fade=0).astype(np.uint8))
        if crop:
            flat = flat.crop(crop)
        save(np.asarray(flat.resize((CELL, CELL), Image.LANCZOS)).astype(np.float32), f"cell-{state}")
        print(state, "ok")
    (OUT / "leads.json").write_text(json.dumps(leads), encoding="utf-8")
    print(json.dumps(leads))


if __name__ == "__main__":
    main()

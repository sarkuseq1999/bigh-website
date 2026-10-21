"""Build the homepage science section's hiker paintings (October 21, 2026, idea A: "a hiker, and a
peek inside") from the Codex originals.

Two ink plates per stage state (the paper divided out, so the page multiplies them onto its rice
paper): the hiker scene, scaled to the stage's width and standing on its foot (1600 x 1195, every
edge dissolving), and the cell for the round window (900 x 900; the sparks are small, so that
cell is cropped closer, round the power plant that sparks). The page lays the window over the
scene and draws its ring and the leader from the hiker's thigh; LEADS prints where each leader
starts, in the stage's units, for science.tsx.

Output: public/images/home-v2/ink/science/hiker-<state>-v1.webp and cell-<state>-v1.webp.

usage: python -X utf8 reference/ink-pages/home-science/build_hiker.py
"""

import json
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
ORIG = HERE / "originals"
OUT = REPO / "public/images/home-v2/ink/science"
W, H = 1600, 1195
CELL = 900

# state -> hiker original, cell original, the hiker's thigh (original px), the cell's crop or None
STATES = {
    "energy": ("hiker-trailhead-a1", "cell-energy-a1", (395, 640), None),
    "sparks": ("hiker-climb-a1", "cell-sparks-a2", (452, 556), (790, 330, 1230, 770)),
    "young": ("hiker-30-a1", "cell-young-a1", (440, 680), None),
    "middle": ("hiker-55-a1", "cell-middle-a1", (444, 686), None),
    "old": ("hiker-80-a1", "cell-old-a1", (440, 690), None),
}


def plate(im, fade=0.08):
    """The painting with its paper divided out (and its edges dissolved), floats 0..255."""
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
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(OUT / f"{name}.webp", quality=86, method=6)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    leads = {}
    for state, (hiker, cell, thigh, crop) in STATES.items():
        him = Image.open(ORIG / f"{hiker}.png")
        k = W / him.width
        hh = round(him.height * k)
        scene = np.full((H, W, 3), 255.0, np.float32)
        scene[H - hh :] = plate(him.resize((W, hh), Image.LANCZOS))
        save(scene, f"hiker-{state}-v1")
        leads[state] = [round(thigh[0] * k), round(H - hh + thigh[1] * k)]
        flat = Image.fromarray(plate(Image.open(ORIG / f"{cell}.png"), fade=0).astype(np.uint8))
        if crop:
            flat = flat.crop(crop)
        save(np.asarray(flat.resize((CELL, CELL), Image.LANCZOS)).astype(np.float32), f"cell-{state}-v1")
    print("LEADS", json.dumps(leads))


if __name__ == "__main__":
    main()

"""Cut the footer cranes Codex painted (October 26, 2026, originals/crane-sign-*.png) for the
mockups: the paper is divided out (white = no paint, so the picture multiplies onto the site's
paper), the picture is trimmed to its paint, and the feet's height is measured.

usage: python -X utf8 reference/ink-pages/footer-crane/cut_cranes.py
"""

import json
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).parent
OUT = HERE.parents[0] / "mockups" / "footer-crane" / "img"

# Per take: the feet (where the legs meet the ground), the top of the bird and the gold crown's box,
# in the original's pixels, read off the paintings.
TAKES = {
    "a1": {"feet": (575, 1295), "top": 165, "crown": (310, 150, 420, 200)},
    "b1": {"feet": (515, 1245), "top": 262, "crown": (275, 250, 350, 310)},
    "c1": {"feet": (878, 862), "top": 218, "crown": (270, 385, 345, 480)},
}
# The homepage's "green spring" crown (reference/home-v2/ink/recolor/recolor.py, crane_tint).
CROWN = np.array([0xD4, 0x48, 0x2F]) / 255.0


def spring(c, box):
    """The homepage's crane wears a red crown: the gold inside the crown's box turns red."""
    a = c.astype(float) / 255.0
    sat = a.max(axis=2) - a.min(axis=2)
    warm = a[..., 0] > a[..., 2] + 0.03
    t = np.clip((sat - 0.04) / 0.08, 0, 1)
    inside = np.zeros(sat.shape)
    x0, y0, x1, y1 = box
    inside[y0:y1, x0:x1] = 1
    m = (t * t * (3 - 2 * t) * warm * inside)[..., None]
    lum = a.mean(axis=2, keepdims=True)
    red = np.clip(CROWN * (lum / CROWN.mean()) ** 0.8, 0, 1)
    return (np.clip(a * (1 - m) + red * m, 0, 1) * 255 + 0.5).astype(np.uint8)


FLOOR = 15  # the generated paper's grain reaches about 13 below its mean: no paint under this
FADE = 48  # px: the cut edges fade out, so no edge of the picture shows as a line


def divide_paper(rgb):
    a = rgb.astype(float)
    paper = np.percentile(a[:60].reshape(-1, 3), 60, axis=0)
    dark = 255.0 - np.clip(a / paper * 255.0, 0, 255)
    # The paper's grain and faint unevenness would show as a pale box: dropped under the floor.
    dark = np.clip((dark - FLOOR) / (1 - FLOOR / 255.0), 0, 255)
    h, w = dark.shape[:2]
    ramp = lambda n: np.clip(np.minimum(np.arange(n), np.arange(n)[::-1]) / FADE, 0, 1)
    dark *= (ramp(h)[:, None] * ramp(w)[None, :])[..., None]
    return (255.0 - dark).astype(np.uint8)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    meta = {}
    for take, info in TAKES.items():
        src = Image.open(HERE / "originals" / f"crane-sign-{take}.png").convert("RGB")
        c = divide_paper(np.asarray(src))
        ink = (255 - c.min(axis=2)) > 10
        ys, xs = np.where(ink)
        pad = 12
        x0, x1 = int(max(xs.min() - pad, 0)), int(min(xs.max() + pad, c.shape[1]))
        y0, y1 = int(max(ys.min() - pad, 0)), int(min(ys.max() + pad, c.shape[0]))
        Image.fromarray(c[y0:y1, x0:x1]).save(OUT / f"crane-{take}.png", optimize=True)
        red = spring(c, info["crown"])
        Image.fromarray(red[y0:y1, x0:x1]).save(OUT / f"crane-{take}-spring.png", optimize=True)
        fx, fy = info["feet"]
        meta[take] = {
            "w": x1 - x0,
            "h": y1 - y0,
            "feetX": fx - x0,
            "feetY": fy - y0,
            "top": info["top"] - y0,
        }
        print(take, meta[take])
    (OUT / "cranes.json").write_text(json.dumps(meta, indent=2), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()

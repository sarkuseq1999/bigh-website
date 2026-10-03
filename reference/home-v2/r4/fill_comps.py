"""Put the real BiGH assets into the round-4 full-page comps (October 2, 2026).

The comps were generated with empty placeholders (a pale-grey portrait frame and five blank
bottles) because product labels and Dr. Liu's face must never be generated. This script finds
those placeholders and pastes the real assets over them: Dr. Liu's photo
(public/images/jiankang-liu.jpg) cropped to the frame, and the approved bottle PNGs
(public/images/products/*.png) scaled to each blank bottle.

usage: python -X utf8 reference/home-v2/r4/fill_comps.py <comp.jpg> <out.png> <spec-json>
spec-json: {"frame": [x0,y0,x1,y1], "bottles": [x0,y0,x1,y1], "bottle_mode": "white"|"any"}
           (search boxes in comp pixels; the script finds the exact placeholder inside each)
"""

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

REPO = Path(__file__).resolve().parents[3]
BOTTLES = ["nuricell", "green-bee-propolis", "advanced-opc", "turmerific", "nature-calm"]


def frame_box(img: np.ndarray, box):
    x0, y0, x1, y1 = box
    sub = img[y0:y1, x0:x1].astype(int)
    spread = sub.max(axis=2) - sub.min(axis=2)
    lum = sub.mean(axis=2)
    mask = (spread < 14) & (lum > 185) & (lum < 228)
    rows = np.where(mask.mean(axis=1) > 0.45)[0]
    cols = np.where(mask.mean(axis=0) > 0.45)[0]
    # longest run of consecutive rows / cols
    def run(idx):
        best, start, prev = (0, 0, 0), idx[0], idx[0]
        for i in list(idx[1:]) + [None]:
            if i is None or i != prev + 1:
                if prev - start > best[0]:
                    best = (prev - start, start, prev)
                if i is not None:
                    start = i
            if i is not None:
                prev = i
        return best[1], best[2]
    r0, r1 = run(rows)
    c0, c1 = run(cols)
    return x0 + c0, y0 + r0, x0 + c1, y0 + r1


def bottle_boxes(img: np.ndarray, box, mode):
    x0, y0, x1, y1 = box
    sub = img[y0:y1, x0:x1].astype(int)
    r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
    if mode == "white":
        mask = (r > 236) & (np.abs(r - b) < 7) & (np.abs(r - g) < 7)
    else:
        mask = (r > 225) & (g > 225) & (b > 225)
    colfrac = mask.mean(axis=0)
    cols = colfrac > 0.12
    runs, start = [], None
    for i, v in enumerate(list(cols) + [False]):
        if v and start is None:
            start = i
        if not v and start is not None:
            if i - start > 25:
                runs.append((start, i - 1))
            start = None
    out = []
    for c0, c1 in runs:
        rowsel = mask[:, c0 : c1 + 1].mean(axis=1) > 0.35
        ys = np.where(rowsel)[0]
        if len(ys) == 0:
            continue
        out.append((x0 + c0, y0 + ys.min(), x0 + c1, y0 + ys.max()))
    return out


def alpha_bbox(im: Image.Image):
    return im.getchannel("A").point(lambda a: 255 if a > 20 else 0).getbbox()


def main():
    src, dst, spec = sys.argv[1], sys.argv[2], json.loads(sys.argv[3])
    comp = Image.open(src).convert("RGB")
    arr = np.asarray(comp)
    out = comp.convert("RGBA")

    fx0, fy0, fx1, fy1 = frame_box(arr, spec["frame"])
    fw, fh = fx1 - fx0 + 1, fy1 - fy0 + 1
    liu = Image.open(REPO / "public/images/jiankang-liu.jpg").convert("RGB")
    scale = max(fw / liu.width, fh / liu.height)
    lw, lh = round(liu.width * scale), round(liu.height * scale)
    liu = liu.resize((lw, lh), Image.LANCZOS)
    left = (lw - fw) // 2
    top = min(int((lh - fh) * 0.25), lh - fh)  # keep his face, crop more from the bottom
    out.paste(liu.crop((left, top, left + fw, top + fh)), (fx0, fy0))
    print("frame", (fx0, fy0, fx1, fy1))

    if "bottle_centers" in spec:
        # Placeholders drawn as outlines can't be found by colour: give centres + top/bottom.
        t, b = spec["bottle_top"], spec["bottle_bottom"]
        boxes = [(c - 2, t, c + 2, b) for c in spec["bottle_centers"]]
    else:
        boxes = bottle_boxes(arr, spec["bottles"], spec.get("bottle_mode", "white"))
    print("bottles", boxes)
    if spec.get("erase"):
        # Paint the blank placeholder bottles out first, so none peeks from behind a real one.
        import cv2

        base = np.asarray(out.convert("RGB")).copy()
        mask = np.zeros(base.shape[:2], np.uint8)
        half = spec["erase"]
        for bx0, by0, bx1, by1 in boxes:
            cx = (bx0 + bx1) // 2
            x0, x1, y0, y1 = cx - half, cx + half, by0 - 14, by1 + 6
            reg = base[y0:y1, x0:x1].astype(int)
            white = (reg.min(axis=2) > 215) & (reg.max(axis=2) - reg.min(axis=2) < 12)
            mask[y0:y1, x0:x1][white] = 255
        mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=2)
        base = cv2.inpaint(base, mask, 9, cv2.INPAINT_TELEA)
        out = Image.fromarray(base).convert("RGBA")
    for name, (bx0, by0, bx1, by1) in zip(BOTTLES, boxes):
        bottle = Image.open(REPO / f"public/images/products/{name}.png").convert("RGBA")
        bottle = bottle.crop(alpha_bbox(bottle))
        h = (by1 - by0 + 1) * 1.06
        w = bottle.width * h / bottle.height
        bottle = bottle.resize((round(w), round(h)), Image.LANCZOS)
        cx = (bx0 + bx1) / 2
        px, py = round(cx - bottle.width / 2), round(by1 + 2 - bottle.height)
        # soft contact shadow under the real bottle
        shadow = Image.new("RGBA", out.size, (0, 0, 0, 0))
        sh = Image.new("RGBA", (round(bottle.width * 1.1), max(8, round(bottle.height * 0.07))), (30, 28, 24, 90))
        shadow.paste(sh, (round(cx - sh.width / 2), by1 - sh.height // 2))
        shadow = shadow.filter(ImageFilter.GaussianBlur(6))
        out = Image.alpha_composite(out, shadow)
        out.alpha_composite(bottle, (px, py))

    out.convert("RGB").save(dst)
    print("saved", dst)


if __name__ == "__main__":
    main()

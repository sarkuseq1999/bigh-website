"""Solid figure mask for Dr. Liu's portrait painting (liu-v1.webp, paper already divided out).

Inside the silhouette (face, white shirt, hands) the landscape behind must not show through when
the portrait is multiplied over it, so the mask is filled solid and feathered at the edge.
Usage: python -I liu_mask.py <portrait.webp> <out-mask.png> <out-preview.png>
"""

import sys

import cv2
import numpy as np
from PIL import Image
from scipy import ndimage


def figure_mask(rgb: np.ndarray) -> np.ndarray:
    ink = 255 - rgb.min(axis=2).astype(np.int16)  # 0 on bare paper
    solid = ink > 18
    # Join the splashes and brush gaps into one body, then fill the light areas inside it.
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41))
    solid = cv2.morphologyEx(solid.astype(np.uint8), cv2.MORPH_CLOSE, k) > 0
    solid = ndimage.binary_fill_holes(solid)
    # Keep the main body only (drop loose specks: they stay ink over the landscape, which is fine).
    labels, n = ndimage.label(solid)
    if n > 1:
        sizes = ndimage.sum(solid, labels, range(1, n + 1))
        solid = labels == (1 + int(np.argmax(sizes)))
    # Pull the edge in a little so the ragged brush edge itself sits over the landscape, then feather.
    solid = cv2.erode(solid.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (23, 23)))
    soft = cv2.GaussianBlur(solid.astype(np.float32), (0, 0), 7)
    return np.clip(soft, 0, 1)


def main() -> None:
    src, out_mask, out_prev = sys.argv[1:4]
    rgb = np.asarray(Image.open(src).convert("RGB"))
    m = figure_mask(rgb)
    Image.fromarray((m * 255).astype(np.uint8)).save(out_mask)
    prev = rgb.astype(np.float32) * 0.5 + np.dstack([m * 255, m * 60, m * 60]) * 0.5
    Image.fromarray(prev.clip(0, 255).astype(np.uint8)).save(out_prev)


if __name__ == "__main__":
    main()

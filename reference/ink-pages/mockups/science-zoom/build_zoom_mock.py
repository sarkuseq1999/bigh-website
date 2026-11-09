"""Mockup for Mo: the Science opening as a slow zoom (hills -> hand -> one cell).

  python -X utf8 reference/ink-pages/mockups/science-zoom/build_zoom_mock.py

Reads the Codex originals in reference/ink-pages/science/originals/, divides each painting's paper
out (so it multiplies onto the page's paper) and writes one self-contained index.html beside this
script. A throwaway sample, not site code.
"""

import base64
import io
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ORIG = HERE.parent.parent / "science" / "originals"
PLATES = {"hills": "zoom-hills-1.png", "hand": "zoom-hand-2.png", "cell": "zoom-cell-2.png"}


def plate(name: str) -> str:
    im = Image.open(ORIG / name).convert("RGB")
    a = np.asarray(im).astype(np.float32)
    # the paper: the median of the brightest tenth of the picture
    lum = a.mean(axis=2)
    paper = np.median(a[lum >= np.quantile(lum, 0.9)], axis=0)
    a = np.clip(a / paper * 255.0 * 1.04, 0, 255).astype(np.uint8)
    buf = io.BytesIO()
    Image.fromarray(a).save(buf, "WEBP", quality=84, method=6)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


html = (HERE / "template.html").read_text(encoding="utf-8")
for key, name in PLATES.items():
    html = html.replace("{{" + key + "}}", plate(name))
(HERE / "index.html").write_text(html, encoding="utf-8", newline="\n")
print("wrote", HERE / "index.html", round(len(html) / 1024), "KB")

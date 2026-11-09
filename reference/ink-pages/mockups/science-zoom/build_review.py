"""The review page for Mo: screenshots of the built Science page's zoom opening.

  python -X utf8 reference/ink-pages/mockups/science-zoom/build_review.py <shots-dir>

<shots-dir> holds shoot_zoom.py's pictures (desk-000.png ...). Writes built.html beside this script,
self-contained (the pictures inline), for an Artifact link Mo can open on a phone.
"""

import base64
import io
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
SHOTS = Path(sys.argv[1])

DESK = [
    ("desk-000", "1. The first screen. The headline sits in the sky."),
    ("desk-020", "2. Scrolling: the picture moves in on the walker."),
    ("desk-050", "3. The walker's hand in the grass."),
    ("desk-100", "4. One cell. &ldquo;Why start with the cell?&rdquo; lands here."),
    ("desk-after", "5. Then the three lines, and Dr. Liu."),
]
PHONE = [
    ("phone-000", "1. First screen"),
    ("phone-050", "2. The hand"),
    ("phone-100", "3. One cell"),
    ("phone-after", "4. The three lines"),
]


def uri(name, width):
    im = Image.open(SHOTS / f"{name}.png").convert("RGB")
    im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=82, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def figures(items, width, cls):
    return "\n".join(
        f'<figure class="{cls}"><img alt="" src="{uri(name, width)}"><figcaption>{text}</figcaption></figure>'
        for name, text in items
    )


html = (HERE / "review-template.html").read_text(encoding="utf-8")
html = html.replace("{{desk}}", figures(DESK, 1280, "desk")).replace("{{phone}}", figures(PHONE, 390, "phone"))
(HERE / "built.html").write_text(html, encoding="utf-8", newline="\n")
print("wrote", HERE / "built.html", round(len(html) / 1024), "KB")

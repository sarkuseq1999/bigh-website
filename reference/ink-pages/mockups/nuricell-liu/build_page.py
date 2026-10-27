"""Builds Mo's mockup page for NuriCell chapter 5 idea A (the Berkeley story), October 26, 2026.

Turns the Playwright screenshots (shots/*.png, made by mock_people.py) into webp files here and
inlines them into page.template.html -> page.html (one self-contained file for the Artifact).
Usage: python build_page.py <shots-dir>
"""

import base64
import io
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
SHOTS = Path(sys.argv[1])
NAMES = ["now-desktop", "a1-desktop", "a1-phone", "a2-desktop", "a2-phone", "a2v2b-desktop", "a2v2b-phone"]

html = (HERE / "page.template.html").read_text(encoding="utf-8")
for name in NAMES:
    im = Image.open(SHOTS / f"{name}.png").convert("RGB")
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=82, method=6)
    (HERE / f"{name}.webp").write_bytes(buf.getvalue())
    uri = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode("ascii")
    html = html.replace("{{" + name + "}}", uri)
    print(name, im.size, f"{len(buf.getvalue()) // 1024} KB")

assert "{{" not in html
(HERE / "page.html").write_text(html, encoding="utf-8", newline="\n")
print("page.html", f"{len(html) // 1024} KB")

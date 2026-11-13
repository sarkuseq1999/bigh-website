"""Small copies of shoot.py's shots for Mo's review page (review/index.html).

  python -X utf8 reference/ink-pages/mockups/science-last/review.py
"""

from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
SHOTS = HERE.parent.parent / "science" / "plates" / "last" / "shots"
OUT = HERE / "review"
OUT.mkdir(exist_ok=True)
WIDTH = {"desk": 1280, "laptop": 1280, "phone": 600}

for key in ("today", "kite", "spin", "climb", "row", "dance"):
    for size in ("desk", "phone"):
        shot = SHOTS / f"{key}-{size}.png"
        if not shot.exists():
            continue
        im = Image.open(shot).convert("RGB")
        width = WIDTH[size]
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        im.save(OUT / f"{key}-{size}.jpg", "JPEG", quality=84, optimize=True, progressive=True)
        print("wrote", f"{key}-{size}.jpg")

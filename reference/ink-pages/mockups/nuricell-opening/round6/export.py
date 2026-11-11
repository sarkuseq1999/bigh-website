"""Round 6: turn the mockup screenshots in shots/ into the JPEGs the review page shows (img/).

usage: python -X utf8 export.py
"""

from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
SHOTS = HERE / "shots"
IMG = HERE / "img"
IMG.mkdir(exist_ok=True)

# page name -> screenshot
PICTURES = {
    "now-desk": "now-desk1600-0",
    "now-phone": "now-phone-0",
    "a-desk": "sky-desk1600-0",
    "a-fog": "skyfog-desk1600-0",
    "a-phone": "sky-phone-0",
    "a-fog-phone": "skyfog-phone-0",
    "b-desk": "blue-desk1600-0",
    "b-phone": "blue-phone-0",
    "c-desk": "shade-desk1600-0",
    "c-phone": "shade-phone-0",
    "c-palm": "shadepalm-desk1600-0",
}

for name, shot in PICTURES.items():
    im = Image.open(SHOTS / f"{shot}.png").convert("RGB")
    im.save(IMG / f"{name}.jpg", quality=88, optimize=True, progressive=True)
    print(name, im.size, (IMG / f"{name}.jpg").stat().st_size // 1024, "KB")

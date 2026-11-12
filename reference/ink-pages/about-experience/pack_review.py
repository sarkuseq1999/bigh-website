"""Pack the shots Mo is shown into reference/ink-pages/mockups/about-experience/web/ as webp.

    python -X utf8 reference/ink-pages/about-experience/pack_review.py [web-name=shot ...]

Laptop shots keep their 1440 x 900; phone shots (taken at 2x) come down to 600px wide. With no
arguments, PICKS; each argument adds or replaces one (shot = a file name in plates/shots/, no .png).
"""

import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
SHOTS = HERE / "plates" / "shots"
WEB = HERE.parent / "mockups" / "about-experience" / "web"

# web name -> shot
PICKS = {
    "today-1440": "today-None-desk",
    "today-390": "today-None-phone",
    "a-1440": "a-orchard-1-a-desk",
    "a-1440-arrive": "a-orchard-1-a-desk-arrive",
    "a-390": "a-orchard-1-a-phone",
    "b-1440": "b-sourdough-1-a-desk",
    "b-390": "b-sourdough-1-a-phone",
    "c-1440": "c-carousel-1-a-desk",
    "c-390": "c-carousel-1-a-phone",
}


def main():
    picks = dict(PICKS)
    for arg in sys.argv[1:]:
        name, _, shot = arg.partition("=")
        picks[name] = shot
    WEB.mkdir(parents=True, exist_ok=True)
    for name, shot in picks.items():
        path = SHOTS / f"{shot}.png"
        if not path.exists():
            print("skip (no shot)", name, shot)
            continue
        img = Image.open(path).convert("RGB")
        if name.endswith("-390"):
            img = img.resize((600, round(img.height * 600 / img.width)), Image.LANCZOS)
        img.save(WEB / f"{name}.webp", quality=84, method=6)
        print(name, img.size, (WEB / f"{name}.webp").stat().st_size)


main()

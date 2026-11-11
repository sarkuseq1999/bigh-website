"""Pack the shots Mo is shown into reference/ink-pages/mockups/about-purpose/web/ as webp.

    python -X utf8 reference/ink-pages/about-purpose/pack_review.py

Laptop shots keep their 1440 x 900; phone shots (taken at 2x) come down to 600px wide.
"""

from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
SHOTS = HERE / "plates" / "shots"
WEB = HERE.parent / "mockups" / "about-purpose" / "web"

# web name -> shot
PICKS = {
    "today-1440": "today-None-desk",
    "today-390": "today-None-phone",
    "a-1440": "a-oak-1-b-desk",
    "a-1440-arrive": "a-oak-1-b-desk-arrive",
    "a-390": "a-oak-1-b-phone",
    "b-1440": "b-bay-1-b-desk",
    "b-390": "b-bay-1-b-phone",
    "c-1440": "c2-cable-2-b-desk",
    "c-390": "c2-cable-2-b-phone",
}


# The built page (shoot_built.py against the built site): web name -> shot in plates/built/
BUILT = {
    "built-1440-arrive": "desk-arrive",
    "built-1440": "desk",
    "built-1440-light": "desk-glint",
    "built-768": "tablet",
    "built-390": "phone",
}


def main():
    WEB.mkdir(parents=True, exist_ok=True)
    shots = {name: SHOTS / f"{shot}.png" for name, shot in PICKS.items()}
    shots.update({name: HERE / "plates" / "built" / f"{shot}.png" for name, shot in BUILT.items()})
    for name, path in shots.items():
        img = Image.open(path).convert("RGB")
        if name.endswith("-390"):
            img = img.resize((600, round(img.height * 600 / img.width)), Image.LANCZOS)
        img.save(WEB / f"{name}.webp", quality=84, method=6)
        print(name, img.size, (WEB / f"{name}.webp").stat().st_size)


main()

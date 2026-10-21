"""Export the mockup screenshots (webp) into the repo's mockups folder, with the scripts that made them."""

import shutil
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
DEST = Path(r"C:\Users\mcbig\Documents\codes\bigh-website\reference\ink-pages\mockups\nav\2026-10-21")
DEST.mkdir(parents=True, exist_ok=True)


def save(src: Path, name: str, box=None, width=None, quality=84):
    image = Image.open(src).convert("RGB")
    if box:
        image = image.crop(box)
    if width and image.width > width:
        image = image.resize((width, round(image.height * width / image.width)), Image.LANCZOS)
    image.save(DEST / name, "WEBP", quality=quality, method=6)
    print(name, image.size, (DEST / name).stat().st_size // 1024, "KB")


BAR = (0, 0, 1536, 210)
PHONE = (0, 0, 780, 1100)

save(HERE / "now" / "home-top.png", "today-home.webp")
save(HERE / "now" / "nuricell-top.png", "today-nuricell-bar.webp", BAR)
save(HERE / "now" / "phone-home-top.png", "today-phone.webp", PHONE)
for letter in "ABC":
    shots = HERE / "shots"
    save(shots / f"{letter}-home-top.png", f"{letter}-home.webp")
    save(shots / f"{letter}-nuricell-top.png", f"{letter}-nuricell-bar.webp", BAR)
    save(shots / f"{letter}-home-settled.png", f"{letter}-settled-bar.webp", (0, 0, 1536, 150))
    save(shots / f"{letter}-phone-home.png", f"{letter}-phone.webp", PHONE)
save(HERE / "shots" / "A-home-hover.png", "A-hover-bar.webp", (0, 0, 1536, 150))

for script in ("mock.py", "cut_strokes.py", "shoot_now.py", "export.py"):
    shutil.copy(HERE / script, DEST / script)
shutil.copy(HERE / "assets" / "band.webp", DEST / "stroke-band.webp")
shutil.copy(HERE / "assets" / "swash.webp", DEST / "stroke-swash.webp")

"""Make the compare page's pictures (JPEG) from the shots and the paintings. -> page/"""

from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
OUT = HERE / "page"
OUT.mkdir(exist_ok=True)

SHOTS = {
    "now.jpg": "now/desk1440-1.png",
    "a-desk.jpg": "shots/a0-desk1440-0.png",
    "a-desk-pick3.jpg": "shots/a2-desk1440-0.png",
    "a-phone.jpg": "shots/a0-phone-0.png",
    "b-desk.jpg": "shots/c-desk1440-0.png",
    "b-desk-key.jpg": "shots/c-desk1440-1.png",
    "b-phone.jpg": "shots/c-phone-0.png",
}
for name, src in SHOTS.items():
    Image.open(HERE / src).convert("RGB").save(OUT / name, quality=84, optimize=True)

paper = (248, 243, 234)
for i, art in enumerate(["q1-take", "q2-month", "q3-capsule", "q4-studied", "q5-doctor", "q6-pregnancy"], 1):
    im = Image.open(HERE / "art" / "div" / f"{art}.png").convert("RGB")
    im.thumbnail((560, 560))
    # Multiply onto the page's paper colour, as the site would show it.
    bg = Image.new("RGB", im.size, paper)
    from PIL import ImageChops

    ImageChops.multiply(im, bg).save(OUT / f"a-paint-{i}.jpg", quality=84, optimize=True)

for f in sorted(OUT.iterdir()):
    print(f.name, f.stat().st_size // 1024, "KB")

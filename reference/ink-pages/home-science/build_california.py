"""Encode the complete California science painting set for the homepage.

November 14, 2026: Mo asked to place the full set on the actual page, using C's ranch
workshop, the matching sparks, and all three neuron ages. Only format compression:
keep original framing, colours and generated alpha. The age layers get their opaque
white backing in CSS, inside the existing multiply group, so they cover younger ages.

Usage: python reference/ink-pages/home-science/build_california.py
"""

from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[2] / "public/images/home-v2/ink/science"
PAINTINGS = {
    "workshop-fuel-v2": "california-workshop-shed-v1",
    "workshop-sparks-v1": "california-sparks-v1",
    "cell-young-v3": "california-neuron-young-v1",
    "cell-middle-v3": "california-neuron-middle-v1",
    "cell-old-v3": "california-neuron-old-v1",
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, original in PAINTINGS.items():
        with Image.open(HERE / f"originals/{original}.png") as painting:
            target = OUT / f"{name}.webp"
            painting.save(target, format="WEBP", quality=90, method=6)
            print(f"{target.name}: {painting.width}x{painting.height}, {painting.mode}, {target.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()

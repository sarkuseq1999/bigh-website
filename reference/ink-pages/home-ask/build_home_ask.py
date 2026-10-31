"""Build the homepage's "Good questions" picture (Mo picked A, the country mailbox, October 30, 2026).

The Codex painting, its paper divided out so it multiplies onto the page, cut to its ink and centred
in the 4:3 frame the inkstone had (shoot_ask.py's `cut`, the same cut Mo saw on the mockup page).

    python -X utf8 reference/ink-pages/home-ask/build_home_ask.py

Out: public/images/home-v2/ink/mailbox-v1.webp; lossless plate plates/mailbox-v1.png (git-ignored).
"""

from pathlib import Path

from shoot_ask import cut

HERE = Path(__file__).resolve().parent
SITE = HERE.parents[2] / "public" / "images" / "home-v2" / "ink"
PLATES = HERE / "plates"


def main():
    img = cut("mailbox-4")
    img.save(PLATES / "mailbox-v1.png", optimize=True)
    img.save(SITE / "mailbox-v1.webp", quality=88, method=6)
    print(img.size, (SITE / "mailbox-v1.webp").stat().st_size)


if __name__ == "__main__":
    main()

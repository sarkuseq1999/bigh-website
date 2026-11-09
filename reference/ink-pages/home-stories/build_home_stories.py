"""Part 9 of the homepage's California pass (Mo picked A, the back porch, November 6, 2026): the
three "In their own words." still lifes, built for the site.

Each Codex painting is cut from its paper exactly as Mo saw it on the real page
(shoot_stories.cut: the paper divided out, so it multiplies onto the page, the edges faded), then
enlarged with Lanczos from 1024 to 1744 px square, the old still lifes' width, as the opening and
the close are enlarged to 2400 (no detail is added; the browser is spared scaling a small file up
on 2x screens). Each picture carries its own thin colour, so it has no green-spring twin.

    python -X utf8 reference/ink-pages/home-stories/build_home_stories.py

Out: public/images/home-v2/ink/story-porch-<moment>-v1.webp and a .webp.json note beside each
(its order, its original, when it was built), as the old still lifes had.
"""

import json
from datetime import date
from pathlib import Path

from PIL import Image

from shoot_stories import cut

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = ROOT / "public" / "images" / "home-v2" / "ink"
SIZE = 1744
# The story, its painting and the site picture's name.
STORIES = {
    "lisa": ("porch-2", "story-porch-morning-v1.webp"),
    "michael": ("porch-dusk-1", "story-porch-dusk-v1.webp"),
    "susan": ("porch-source-2", "story-porch-afternoon-v1.webp"),
}


def main():
    style = (HERE / "prompts" / "_style.txt").read_text(encoding="utf-8")
    for story, (take, name) in STORIES.items():
        im = cut(take).resize((SIZE, SIZE), Image.LANCZOS)
        im.save(OUT / name, "WEBP", quality=88, method=6)
        note = {
            "prompt": style + "\n" + (HERE / "prompts" / f"{take}.txt").read_text(encoding="utf-8"),
            "original": f"reference/ink-pages/home-stories/originals/{take}.png",
            "built": f"{date.today().isoformat()}: {story}'s still life, paper divided out, "
            f"enlarged to {SIZE} px (build_home_stories.py)",
        }
        (OUT / f"{name}.json").write_text(
            json.dumps(note, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
        )
        print(name, im.size, (OUT / name).stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()

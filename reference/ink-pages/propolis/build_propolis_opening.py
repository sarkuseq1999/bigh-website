"""Build Green Bee Propolis's opening painting, the hills of Minas Gerais (November 18, 2026, on
Mo's go-ahead for the product pages; mockups reference/ink-pages/mockups/propolis-opening/).

One Codex painting (originals/opening-ipemid-bh.png, prompt prompts/opening-ipemid-1.txt,
paint_opening.sh): the rolling hills of Minas Gerais on a clear dry-season morning, a big sky, a
thin band of far hills with one golden ipê tree in bloom just right of the middle and a few tiny
hive boxes on the left, a red earth track, and low alecrim shrubs (the shrub the bees gather the
resin from) in front, painted on white paper. The page lays it behind the approved "Green [bottle]
Bee Propolis" (propolis-opening.tsx, propolis.module.css): the name stays in the sky, the bottle
stands on the far hills, the shrubs below it.

The other painted openings (painted-opening.tsx) stand the bottle on the painting's empty spot in
front, with the name lifted off the far land. Propolis's name sits much lower against its bottle
(its baselines are only about a fifth of the bottle's height above its foot), so here the bottle
stands further back, on the far hills (GROUND, a little under their crest), where the land from
the crest to the bottle's foot is thin enough to stay under the name at every width. The shrubs
and the track run on below its foot.

What this script does to it:

- The paper is divided out and lifted to white, so the painting multiplies onto the page's own
  paper with no box. It is cut ROWS down (bare paper under the last shrubs).
- GROUND is the row the bottle's foot stands on; END the last paint (the words start under it).
- A front layer (`front`): the painting's own ground round the bottle's foot (FRONT_BOX), its
  paper transparent, its darker strokes kept and its pale wash laid thin, laid over the bottle's
  foot, so the bottle stands in the land, not on top of the picture (AGENTS.md: "a front layer
  seats it in the painting").

    python -X utf8 reference/ink-pages/propolis/build_propolis_opening.py

Writes public/images/products/green-bee-propolis/ink/opening-minas-*.webp and
src/components/product/ink/propolis-opening-art.ts.
"""

import json
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
OUT = REPO / "public/images/products/green-bee-propolis/ink"
URL = "/images/products/green-bee-propolis/ink"
TS = REPO / "src/components/product/ink/propolis-opening-art.ts"
TAKE = "opening-ipemid-bh"
# Bump when a shipped picture changes after it has been pushed (the image optimizer caches by URL).
V = "v1"
# The bottle's foot: on the far hills, about 70 rows under their crest in the middle (the land
# between them must stay under the name's baselines at every width).
GROUND = 768
# The ground round the bottle's foot (x0, y0, x1, y1), between the middle shrubs.
FRONT_BOX = (690, GROUND - 26, 846, GROUND + 34)
WASH = 0.35
QUALITY = 84


def plate():
    a = np.asarray(Image.open(HERE / "originals" / f"{TAKE}.png").convert("RGB")).astype(np.float32)
    h = a.shape[0]
    paper = np.median(a[int(h * 0.93) :].reshape(-1, 3), axis=0)
    d = np.clip(a / paper * 255.0, 0, 255)
    d = np.where(d.min(axis=2, keepdims=True) > 249, 255.0, d)
    painted = np.where((d.min(axis=2) < 244).sum(axis=1) > 3)[0]
    rows = min(h, int(painted[-1]) + 24)
    d = d[:rows]
    # The last rows are bare paper already; make sure of it, so the picture never ends on a line.
    ease = np.clip((np.arange(rows) - (rows - 16)) / 14, 0, 1)[:, None, None]
    return d * (1 - ease) + 255 * ease


def last_paint(d):
    painted = np.where((d.min(axis=2) < 244).sum(axis=1) > 3)[0]
    return int(painted[-1])


def front(d):
    """The ground round the bottle's foot (RGBA): its paper transparent, its ink strokes keeping
    their paint, its pale wash laid thin (WASH of it: the painting under it has the wash already),
    soft at the sides and the top."""
    x0, y0, x1, y1 = FRONT_BOX
    tuft = d[y0:y1, x0:x1]
    h, w, _ = tuft.shape
    alpha = 1 - tuft.min(axis=2) / 255
    paint = np.where(alpha[..., None] > 0.03, (tuft - 255 * (1 - alpha[..., None])) / np.maximum(alpha[..., None], 0.03), 255)
    blade = np.clip((alpha - 0.25) / 0.3, 0, 1)
    alpha = alpha * np.maximum(blade, WASH)
    xs = np.arange(w)
    sides = np.clip(np.minimum(xs, w - 1 - xs) / 30, 0, 1)
    ys = np.arange(h)
    top = np.clip(ys / 16, 0, 1)
    alpha = alpha * (sides * sides * (3 - 2 * sides))[None, :] * (top * top * (3 - 2 * top))[:, None]
    rgba = np.dstack([np.clip(paint, 0, 255), alpha * 255])
    return Image.fromarray(np.clip(np.rint(rgba), 0, 255).astype(np.uint8), "RGBA")


def shipped(img, name):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"opening-minas{name}-{V}.webp"
    img.save(path, "WEBP", quality=QUALITY, method=6)
    print(f"{path.relative_to(REPO)}  {img.width}x{img.height}  {path.stat().st_size // 1024} KB")
    return {"src": f"{URL}/{path.name}", "width": img.width, "height": img.height}


def main():
    d = plate()
    end = last_paint(d)
    whole = Image.fromarray(np.clip(np.rint(d), 0, 255).astype(np.uint8))
    art = {
        "sky": shipped(whole, ""),
        "front": {**shipped(front(d), "-front"), "x": FRONT_BOX[0], "y": FRONT_BOX[1]},
        "ground": GROUND,
        "end": end,
    }
    head = [
        "// Generated by reference/ink-pages/propolis/build_propolis_opening.py. Do not edit by hand:",
        "// change the script and run it again. Green Bee Propolis's opening painting, the hills of",
        "// Minas Gerais (November 18, 2026): a Codex painting, its paper divided out so it multiplies",
        "// onto the page's paper. `front`, its ground laid in front of the bottle's foot at `x`, `y` of",
        "// `sky`. Rows of `sky`: `ground` (where the bottle's foot stands, on the far hills) and `end`",
        "// (the last paint).",
        "",
    ]
    TS.write_text("\n".join(head) + f"export const propolisOpening = {json.dumps(art, indent=2)} as const;\n", encoding="utf-8", newline="\n")
    prettier = REPO / "node_modules/prettier/bin/prettier.cjs"
    subprocess.run(["node", str(prettier), "--write", str(TS)], cwd=REPO, check=True, capture_output=True)
    print(TS.relative_to(REPO), f"ground {GROUND}, end {end}")


if __name__ == "__main__":
    main()

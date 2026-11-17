"""Build Turmerific's opening painting, the turmeric field (Mo picked A of three, November 16,
2026; mockups reference/ink-pages/mockups/turmerific-opening/). Advanced OPC Formula's vineyard
(../opc/build_opc_opening.py) made the same way.

One Codex painting (originals/opening-field-ah.png, prompt prompts/opening-field-1.txt,
paint_opening.sh): a clear sky with a warm haze over soft hills and a eucalyptus windbreak, and
in front the rows of a small Southern California farm's turmeric field, a few freshly dug roots
with bright orange cut ends beside them, bare warm earth between them, painted on white paper. The page lays it behind the name and the bottle (opening.tsx, painted-opening.tsx,
painted-opening.module.css), as NuriCell's clear day is laid (build_nuricell_opening.py): from 960px the name
rests over the far hills and the bottle stands on the bare earth between the rows; in one column
the bottle stands on the earth under the name.

What this script does to it:

- The paper is divided out and lifted to white, so the painting multiplies onto the page's own
  paper with no box. It is cut ROWS down (bare paper under the last earth).
- HILLS is the row the hills top out at under the name; GROUND the row the bottle's foot stands on
  in the middle (inside the earth's wash). The stylesheet scales the painting so these two rows
  fall on the name's baseline and the glass's foot, or draws it as wide as the window where that
  would be narrower than the window (the field has much land between the two rows), and lifts the
  name LIFT of its size, as far as in the mockup Mo picked.
- The whole painting ships for two columns (`sky`). One column shows only its middle, which would
  hold only bare earth: for it (`phone`) the painting is drawn closer, a band of bare earth taken
  out either side of the bottle (CLOSER), so turmeric and a dug root stand either side of it on a
  phone. Its middle PHONE columns ship; the bottle's spot stays in the middle.
- A front layer (`front`): the painting's own earth round the bottle's foot (FRONT_BOX), its paper
  transparent, its darker strokes kept and its pale wash laid thin, laid over the bottle's foot,
  so the bottle stands in the earth, not on top of the picture (AGENTS.md: "a front layer seats it
  in the painting"). `front.x` and `front.y` place it on the painting.

    python -X utf8 reference/ink-pages/turmerific/build_turmerific_opening.py

Writes public/images/products/turmerific/ink/opening-field-*.webp and
src/components/product/ink/turmerific-opening-art.ts.
"""

import json
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
OUT = REPO / "public/images/products/turmerific/ink"
URL = "/images/products/turmerific/ink"
TS = REPO / "src/components/product/ink/turmerific-opening-art.ts"
TAKE = "opening-field-ah"
# Bump when a shipped picture changes after it has been pushed (the image optimizer caches by URL).
V = "v1"
ROWS = 880
HILLS = 575
GROUND = 785
# One column shows only the painting's middle, which on a phone would hold only bare earth: for it the
# painting is drawn closer, a band of bare earth taken out either side of the bottle (CLOSER, each
# cross-faded over CLOSER_SEAM columns), so turmeric and a dug root stand either side of it on a phone.
# The bands are equal, so the bottle's spot stays in the middle; PHONE columns of the closer
# painting ship (its middle 1000).
CLOSER = [(606, 690), (846, 930)]
CLOSER_SEAM = 44
PHONE = (184, 1184)
# Where "erific"'s baseline sits in the bottle's box, as a share of its height (measured on the
# page, November 16, 2026, the name unlifted), and how far the name is lifted off the hills, in
# name-sizes: as far as in the mockup Mo picked (the field has more land between its hills and its
# ground than the vineyard, so at the name's size the painting would be narrower than the window).
BASE = 0.6545
LIFT = 0.41
# The front earth covers only the glass's foot (between the CLOSER bands), so it lies on the same
# earth in both paintings.
FRONT_BOX = (690, GROUND - 30, 846, GROUND + 50)
WASH = 0.35
QUALITY = 84


def plate():
    a = np.asarray(Image.open(HERE / "originals" / f"{TAKE}.png").convert("RGB")).astype(np.float32)
    h = a.shape[0]
    paper = np.median(a[int(h * 0.93) :].reshape(-1, 3), axis=0)
    d = np.clip(a / paper * 255.0, 0, 255)
    d = np.where(d.min(axis=2, keepdims=True) > 249, 255.0, d)[:ROWS]
    # The last rows are bare paper already; make sure of it, so the picture never ends on a line.
    ease = np.clip((np.arange(ROWS) - (ROWS - 16)) / 14, 0, 1)[:, None, None]
    return d * (1 - ease) + 255 * ease


def closer(d):
    """The painting with its CLOSER bands taken out: each seam is a cross-fade from the columns
    before the band into the columns that end it (build_nuricell_opening.py's closer)."""
    parts, at = [], 0
    t = (np.arange(CLOSER_SEAM) / (CLOSER_SEAM - 1))[None, :, None]
    t = t * t * (3 - 2 * t)
    for a, b in CLOSER:
        parts.append(d[:, at : a - CLOSER_SEAM])
        parts.append(d[:, a - CLOSER_SEAM : a] * (1 - t) + d[:, b - CLOSER_SEAM : b] * t)
        at = b
    parts.append(d[:, at:])
    return np.concatenate(parts, axis=1)


def last_paint(d):
    painted = np.where((d.min(axis=2) < 244).sum(axis=1) > 3)[0]
    return int(painted[-1])


def front(d):
    """The earth round the bottle's foot (RGBA): its paper transparent, its ink blades keeping
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
    top = np.clip(ys / 18, 0, 1)
    alpha = alpha * (sides * sides * (3 - 2 * sides))[None, :] * (top * top * (3 - 2 * top))[:, None]
    rgba = np.dstack([np.clip(paint, 0, 255), alpha * 255])
    return Image.fromarray(np.clip(np.rint(rgba), 0, 255).astype(np.uint8), "RGBA")


def shipped(img, name):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"opening-field{name}-{V}.webp"
    img.save(path, "WEBP", quality=QUALITY, method=6)
    print(f"{path.relative_to(REPO)}  {img.width}x{img.height}  {path.stat().st_size // 1024} KB")
    return {"src": f"{URL}/{path.name}", "width": img.width, "height": img.height}


def main():
    d = plate()
    end = last_paint(d)
    whole = Image.fromarray(np.clip(np.rint(d), 0, 255).astype(np.uint8))
    art = {
        "sky": shipped(whole, ""),
        "phone": shipped(Image.fromarray(np.clip(np.rint(closer(d)), 0, 255).astype(np.uint8)).crop((PHONE[0], 0, PHONE[1], ROWS)), "-phone"),
        "front": {**shipped(front(d), "-front"), "x": FRONT_BOX[0], "y": FRONT_BOX[1]},
        "hills": HILLS,
        "ground": GROUND,
        "end": end,
        "base": BASE,
        "lift": LIFT,
    }
    head = [
        "// Generated by reference/ink-pages/turmerific/build_turmerific_opening.py. Do not edit by hand:",
        "// change the script and run it again. Turmerific's opening painting, the turmeric field (Mo",
        "// picked A, November 16, 2026): a Codex painting, its paper divided out so it multiplies onto",
        "// the page's paper. `sky` from 960px, `phone` (its middle, drawn closer) in one column;",
        "// `front`, its earth laid in front of the bottle's foot at `x`, `y` of `sky`. Rows of `sky`:",
        "// `hills` (the hills' tops under the name), `ground` (where the bottle stands) and `end` (the",
        "// last paint); `base`, where the name's baseline sits in the bottle's box, and `lift`, how far",
        "// the name is lifted off the hills (painted-opening.tsx).",
        "",
    ]
    TS.write_text("\n".join(head) + f"export const turmerificOpening = {json.dumps(art, indent=2)} as const;\n", encoding="utf-8", newline="\n")
    prettier = REPO / "node_modules/prettier/bin/prettier.cjs"
    subprocess.run(["node", str(prettier), "--write", str(TS)], cwd=REPO, check=True, capture_output=True)
    print(TS.relative_to(REPO), f"hills {HILLS}, ground {GROUND}, end {end}")


if __name__ == "__main__":
    main()

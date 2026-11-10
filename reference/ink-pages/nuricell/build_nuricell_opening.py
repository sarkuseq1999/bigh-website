"""Build NuriCell's opening painting, "A clear day" (Mo picked A of three, November 10, 2026;
mockups reference/ink-pages/mockups/nuricell-opening/round6/).

One Codex painting (originals/opening-clearday2-ch.png, prompt prompts/opening-clearday2-1.txt): a
clear morning sky over the Pacific and a low grassy bluff, painted on white paper. The page lays it
behind the name and the bottle (src/components/product/ink/opening.tsx, nuricell.module.css): from
960px the name sits on the horizon and the bottle stands on the bluff; in one column the bottle
stands on the bluff under the name.

What this script does to it:

- SEA_CUT rows of open sea are taken out (cross-faded over SEAM rows), so the bluff's top sits as
  far under the horizon as the bottle's foot sits under the letters' baseline: both can then line
  up at one scale.
- The paper is divided out and lifted to white, so the painting multiplies onto the page's own
  paper with no box. It is cut ROWS down (bare paper under the last grass).
- The whole painting ships for two columns (`sky`). One column shows only its middle, which is
  sky, sea and short grass: for it (`phone`) the painting is drawn closer, two bands of plain
  columns (CLOSER, either side of the middle) taken out with a cross-fade, so a phone has the
  poppies at its edges and a tablet the stones. Its middle PHONE columns ship; the bottle's spot
  stays in the middle.
- A window wider than the painting gets two side pieces (`left`, `right`): the painting's own
  middle SIDE columns (sky, sea and grass, no stone or poppy), laid mirrored then plain so each
  runs on without a seam, their sky toned to the edge they meet, lying LAP columns over that edge
  and fading in there (alpha: across the whole LAP in the sky, only past the edge's stone in the
  grass), their outer end easing into bare paper.
- A front layer (`front`): two tufts of the painting's own grass (FRONT columns), cut out with
  their paper and the sea behind them turned to transparency, laid in front of the bottle's foot,
  so the bottle stands in the grass, not on top of the picture (AGENTS.md: "a front layer seats
  it in the painting"). `front.x` and `front.y` place it on the painting.

    python -X utf8 reference/ink-pages/nuricell/build_nuricell_opening.py

Writes public/images/products/nuricell/ink/opening-sky-*.webp and
src/components/product/ink/nuricell-opening-art.ts (the rows the stylesheet lines things up by).
"""

import json
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, gaussian_filter1d

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
OUT = REPO / "public/images/products/nuricell/ink"
URL = "/images/products/nuricell/ink"
TS = REPO / "src/components/product/ink/nuricell-opening-art.ts"
TAKE = "opening-clearday2-ch"
# Bump when a shipped picture changes after it has been pushed (the image optimizer caches by URL).
V = "v1"
SEA_CUT = (613, 649)
SEAM = 12
ROWS = 800
# One column: the bands of columns taken out (sky, sea and grass, no poppy or stone), the columns
# each seam is cross-faded over, and the columns of the closer painting that ship: 500 either side
# of the bottle's spot (column 768 less the first band's 256), enough for a 959px window.
CLOSER = [(364, 620), (905, 1135)]
CLOSER_SEAM = 44
PHONE = (12, 1012)
SIDE = (520, 1150)
LAP = 220
GRASS = 50
OUTER = 70
# The front grass: each tuft's columns in the painting, the column its middle is laid on, and
# whether it is mirrored; the rows they are taken from, how far down they are laid, and the canvas
# they are laid on (the painting's columns and rows it covers).
FRONT = [((330, 500), 688, False), ((1000, 1160), 850, False)]
FRONT_ROWS = (664, 768)
FRONT_DOWN = 8
WASH = 0.3
FRONT_BOX = (590, 668, 946, 780)
QUALITY = 84


def divided(a):
    """The sheet's own white divided out (its foot is bare paper), near-white lifted to white."""
    h = a.shape[0]
    paper = np.median(a[int(h * 0.93) :].reshape(-1, 3), axis=0)
    d = np.clip(a / paper * 255.0, 0, 255)
    return np.where(d.min(axis=2, keepdims=True) > 249, 255.0, d)


def plate():
    a = np.asarray(Image.open(HERE / "originals" / f"{TAKE}.png").convert("RGB")).astype(np.float32)
    c0, c1 = SEA_CUT
    t = (np.arange(SEAM) / (SEAM - 1))[:, None, None]
    seam = a[c0 - SEAM : c0] * (1 - t) + a[c1 - SEAM : c1] * t
    a = np.concatenate([a[: c0 - SEAM], seam, a[c1:]])
    d = divided(a)[:ROWS]
    # The last rows are bare paper already; make sure of it, so the picture never ends on a line.
    ease = np.clip((np.arange(ROWS) - (ROWS - 16)) / 14, 0, 1)[:, None, None]
    return d * (1 - ease) + 255 * ease


def closer(d):
    """The painting with its CLOSER bands taken out: each seam is a cross-fade from the columns
    before the band into the columns that end it."""
    parts, at = [], 0
    t = (np.arange(CLOSER_SEAM) / (CLOSER_SEAM - 1))[None, :, None]
    t = t * t * (3 - 2 * t)
    for a, b in CLOSER:
        parts.append(d[:, at : a - CLOSER_SEAM])
        parts.append(d[:, a - CLOSER_SEAM : a] * (1 - t) + d[:, b - CLOSER_SEAM : b] * t)
        at = b
    parts.append(d[:, at:])
    return np.concatenate(parts, axis=1)


def landmarks(d):
    """The horizon (the sharpest step down the middle columns), the bluff's top in the middle
    (where the sea's blue ends) and the last painted row."""
    h, w, _ = d.shape
    mid = d[:, int(w * 0.45) : int(w * 0.55)].mean(axis=1)
    step = np.abs(np.diff(mid.mean(axis=1)))
    horizon = int(np.argmax(step[int(h * 0.6) : int(h * 0.9)]) + h * 0.6)
    blue = mid[:, 2] - mid[:, 0]
    bluff = horizon + 5 + int(np.where(blue[horizon + 5 :] < 25)[0][0])
    painted = np.where((d.min(axis=2) < 244).sum(axis=1) > 3)[0]
    return horizon, bluff, int(painted[-1])


def side(d, which, horizon):
    """A side piece. `right`: the middle mirrored, then plain (its left edge meets the painting's
    right edge); `left`: plain, then mirrored (its right edge meets the painting's left edge)."""
    a, b = SIDE
    sec = d[:, a:b]
    piece = np.concatenate([sec[:, ::-1], sec], axis=1) if which == "right" else np.concatenate([sec, sec[:, ::-1]], axis=1)
    w = piece.shape[1]
    inner = slice(0, GRASS) if which == "right" else slice(w - GRASS, w)
    edge = d[:, -GRASS:] if which == "right" else d[:, :GRASS]
    # Tone the piece's sky to the edge it meets (row by row, smoothed), fading the correction out
    # over 500 columns; the grass and sea keep their own paint.
    gain = edge.mean(axis=1) / np.maximum(piece[:, inner].mean(axis=1), 1)
    gain = np.clip(gaussian_filter1d(gain, 10, axis=0), 0.9, 1.1)
    sky_only = np.clip((horizon - 14 - np.arange(d.shape[0])) / 20, 0, 1)[:, None]
    gain = 1 + (gain - 1) * sky_only
    x = np.arange(w) if which == "right" else np.arange(w)[::-1]
    reach = np.clip(1 - x / 500, 0, 1)[None, :, None]
    piece = np.clip(piece * (1 + (gain[:, None, :] - 1) * reach), 0, 255)
    # The piece lies LAP columns over the painting's edge and fades in there (alpha). In the sky the
    # fade takes the whole LAP. From the horizon down it takes only the last GRASS columns, past the
    # stone that stands near each edge, along a ragged line (a straight one read as a cut tuft).
    h = d.shape[0]
    rng = np.random.default_rng(11 if which == "right" else 12)
    ragged = gaussian_filter(rng.normal(0, 1, (h, w)), (5, 9))
    ragged = ragged / np.abs(ragged).max() * 18
    low = np.clip((np.arange(h) - (horizon - 40)) / 28, 0, 1)[:, None]
    low = low * low * (3 - 2 * low)
    start = (LAP - GRASS) * low
    across = np.clip((x[None, :] - start + ragged * low) / (LAP - start), 0, 1)
    alpha = across * across * (3 - 2 * across)
    # The outer end eases into bare paper.
    out = np.clip((w - 1 - x) / OUTER, 0, 1)
    out = (out * out * (3 - 2 * out))[None, :, None]
    piece = piece * out + 255 * (1 - out)
    rgba = np.dstack([piece, alpha * 255])
    return Image.fromarray(np.clip(np.rint(rgba), 0, 255).astype(np.uint8), "RGBA")


def front(d):
    """The front grass on its canvas (RGBA). A tuft's paper and the sea behind it are transparent;
    its ink blades and its dry-grass wash keep their paint."""
    x0, y0, x1, y1 = FRONT_BOX
    canvas = np.zeros((y1 - y0, x1 - x0, 4), np.float32)
    r0, r1 = FRONT_ROWS
    for (a, b), middle, mirrored in FRONT:
        tuft = d[r0:r1, a:b]
        if mirrored:
            tuft = tuft[:, ::-1]
        h, w, _ = tuft.shape
        # Paint over white: the alpha that would give this colour over white paper, and the paint.
        alpha = 1 - tuft.min(axis=2) / 255
        sea = np.clip(((tuft[..., 2] - tuft[..., 0]) - 10) / 14, 0, 1)
        alpha = alpha * (1 - sea)
        paint = np.where(alpha[..., None] > 0.03, (tuft - 255 * (1 - alpha[..., None])) / np.maximum(alpha[..., None], 0.03), 255)
        # The ink blades keep their paint; the pale dry-grass wash is laid thin (WASH of it), or it
        # would lie twice where the tuft covers the painting's own grass. Soft sides, top and foot.
        blade = np.clip((alpha - 0.3) / 0.3, 0, 1)
        alpha = alpha * np.maximum(blade, WASH)
        xs = np.arange(w)
        side = np.clip(np.minimum(xs, w - 1 - xs) / 34, 0, 1)
        ys = np.arange(h)
        updown = np.clip(ys / 16, 0, 1) * np.clip((h - 1 - ys) / 22, 0, 1)
        alpha = alpha * (side * side * (3 - 2 * side))[None, :] * (updown * updown * (3 - 2 * updown))[:, None]
        left = middle - w // 2 - x0
        top = r0 + FRONT_DOWN - y0
        under = canvas[top : top + h, left : left + w]
        out_a = alpha + under[..., 3] * (1 - alpha)
        rgb = (np.clip(paint, 0, 255) * alpha[..., None] + under[..., :3] * (under[..., 3] * (1 - alpha))[..., None]) / np.maximum(out_a[..., None], 1e-4)
        canvas[top : top + h, left : left + w] = np.dstack([rgb, out_a])
    canvas[..., 3] *= 255
    return Image.fromarray(np.clip(np.rint(canvas), 0, 255).astype(np.uint8), "RGBA")


def shipped(img, name):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"opening-sky{name}-{V}.webp"
    img.save(path, "WEBP", quality=QUALITY, method=6)
    print(f"{path.relative_to(REPO)}  {img.width}x{img.height}  {path.stat().st_size // 1024} KB")
    return {"src": f"{URL}/{path.name}", "width": img.width, "height": img.height}


def main():
    d = plate()
    horizon, bluff, end = landmarks(d)
    whole = Image.fromarray(np.clip(np.rint(d), 0, 255).astype(np.uint8))
    art = {
        "sky": shipped(whole, ""),
        "phone": shipped(Image.fromarray(np.clip(np.rint(closer(d)), 0, 255).astype(np.uint8)).crop((PHONE[0], 0, PHONE[1], ROWS)), "-phone"),
        "left": shipped(side(d, "left", horizon), "-left"),
        "right": shipped(side(d, "right", horizon), "-right"),
        "front": {**shipped(front(d), "-front"), "x": FRONT_BOX[0], "y": FRONT_BOX[1]},
        "lap": LAP,
        "horizon": horizon,
        "bluff": bluff,
        "end": end,
    }
    head = [
        "// Generated by reference/ink-pages/nuricell/build_nuricell_opening.py. Do not edit by hand:",
        "// change the script and run it again. NuriCell's opening painting, \"A clear day\" (Mo picked A,",
        "// November 10, 2026): a Codex painting, its paper divided out so it multiplies onto the page's",
        "// paper. `sky` from 960px, `phone` (its middle, drawn closer) in one column, `left` and `right` beside `sky`",
        "// in a window wider than it (each lies `lap` columns over its edge and fades in there); `front`,",
        "// two tufts of its grass laid in front of the bottle's foot at `x`, `y` of `sky`. Rows of `sky`:",
        "// `horizon`, `bluff` (the bluff's top in the middle, where the bottle stands) and `end` (the",
        "// last painted row).",
        "",
    ]
    TS.write_text("\n".join(head) + f"export const nuricellOpening = {json.dumps(art, indent=2)} as const;\n", encoding="utf-8", newline="\n")
    prettier = REPO / "node_modules/prettier/bin/prettier.cjs"
    subprocess.run(["node", str(prettier), "--write", str(TS)], cwd=REPO, check=True, capture_output=True)
    print(TS.relative_to(REPO), f"horizon {horizon}, bluff {bluff}, end {end}")


if __name__ == "__main__":
    main()

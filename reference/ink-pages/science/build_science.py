"""Build the Science page's ink paintings (Mo, October 13-14, 2026; spec
docs/superpowers/specs/2026-10-14-science-ink-design.md).

Originals: reference/ink-pages/science/originals/gpt25-<take>.png (GPT Image 2.5 on rice paper;
prompts in prompts/). Output: public/images/science/ink/*.webp (lossless plates in plates/, not
committed) and src/components/science/ink/science-art.ts.

The handscroll is three 21:9 panels painted to one horizon with mist at their ends. Each panel's
paper is divided out; the panels are shifted to one horizon (DY, measured October 14: the sea's top
row is 653 at panel 1's right and 696 at panel 2's left; the hills' top row is 498 at panel 2's
right and 503 at panel 3's left) and laid side by side, overlapping by OVERLAP px. Join 2 (the
hills): both inner ends fade to paper (a smoothstep over FADES px) and meet in a darken blend, so
ink stays ink and the mists join. Join 1 (the open sea) is a crossfade instead (CROSSFADE): both
panels paint spray and mist at that end (panel 1's last ~300px, panel 2's first ~550px), so two ends
fading to paper left a blank gap that read as two seas (October 14 review); over a 900px overlap
panel 1 fades out exactly as panel 2 fades in (weights summing to one), and the sea runs on through
the spray. The band is then cropped to its ink and levelled to white. STOP_X: where each stop's
place stands on the joined canvas, read off its contact sheet (Okayama's castle, Berkeley's tower,
the hills of 2002, Salzburg's fortress, the oaks under the sun).

The strips are cropped to their ink; phones get narrower crops (the scrolls' and the mugs' middle,
their cut ends faded to paper) and the health strip's three scenes, cut where the ink is thinnest
near its thirds.

usage: python -X utf8 reference/ink-pages/science/build_science.py
"""

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "reference/ink-pages/about"))
import build_about as bd  # noqa: E402

ba = bd.ba
OUT = REPO / "public/images/science/ink"
URL = "/images/science/ink"
TS = REPO / "src/components/science/ink/science-art.ts"
# Bump when a shipped picture changes after it has been pushed (the image optimizer caches by URL).
V = "v1"
TAKES = {
    "panel1": "S-panel-1",
    "panel2": "S-panel-2",
    "panel3": "S-panel-3",
    "scrolls": "R-scrolls",
    "health": "S-health-poppy",
    "mugs": "S-mugs",
}
OVERLAP = (900, 300)
CROSSFADE = (True, False)
DY = (0, -43, -48)
FADES = ((0, 0), (0, 420), (420, 0))
STOP_X = {"okayama": 756, "berkeley": 3508, "y2002": 4118, "salzburg": 5000, "today": 6488}
PHONE_H = 400  # the scroll's phone picture: 300px tall on screen, 1.33x
EDGE = 0.03
PHONE_FADE = 0.08  # the phone crops' cut ends (middle()): fade to paper over this share of their width

bd.ORIG = HERE / "originals"
bd.URL = URL
bd.V = V
bd.TAKES = TAKES
ba.OUT = OUT
ba.PLATES = HERE / "plates"


def faded(arr, left, right):
    """Fade an array's left and right ends to white (smoothstep over `left` / `right` px)."""
    w = arr.shape[1]
    x = np.arange(w, dtype=np.float32)
    k = np.ones(w, np.float32)
    if left:
        k = np.minimum(k, np.clip(x / left, 0, 1))
    if right:
        k = np.minimum(k, np.clip((w - 1 - x) / right, 0, 1))
    k = k * k * (3 - 2 * k)
    return arr * k[None, :, None] + 255.0 * (1 - k[None, :, None])


def handscroll():
    panels = [np.asarray(bd.divided(bd.load(TAKES[f"panel{i}"]))).astype(np.float32) for i in (1, 2, 3)]
    h, w, _ = panels[0].shape
    top = max(0, -min(DY))
    xs = [0, w - OVERLAP[0], 2 * w - OVERLAP[0] - OVERLAP[1]]
    canvas = np.full((h + top + max(0, max(DY)), xs[2] + w, 3), 255.0, np.float32)
    for i, (arr, x, dy, (fade_l, fade_r)) in enumerate(zip(panels, xs, DY, FADES)):
        # The panel on a layer as tall as the canvas (paper above and below it), so a crossfade
        # also fades the rows of the panel before that this one does not cover.
        layer = np.full((canvas.shape[0], w, 3), 255.0, np.float32)
        layer[top + dy : top + dy + h] = faded(arr, fade_l, fade_r)
        region = canvas[:, x : x + w]
        out = np.minimum(region, layer)
        if i and CROSSFADE[i - 1]:
            o = OVERLAP[i - 1]
            t = np.linspace(0.0, 1.0, o, dtype=np.float32)
            k = (t * t * (3 - 2 * t))[None, :, None]
            out[:, :o] = region[:, :o] * (1 - k) + layer[:, :o] * k
        canvas[:, x : x + w] = out
    joined = Image.fromarray(np.clip(np.rint(canvas), 0, 255).astype(np.uint8))
    x0, y0, x1, y1 = bd.ink_box(np.asarray(joined), pad=0.02)
    band = bd.feathered(bd.levelled(joined.crop((x0, y0, x1, y1))), EDGE)
    art = bd.art_of(band, f"scroll-{V}", None)
    art["phone"] = bd.art_of(band, f"scroll-phone-{V}", round(band.width * PHONE_H / band.height))
    art["stops"] = {key: round((x - x0) / (x1 - x0), 4) for key, x in STOP_X.items()}
    return art


def strip(key, pad=0.04):
    flat = bd.divided(bd.load(TAKES[key]))
    return bd.levelled(flat.crop(bd.ink_box(np.asarray(flat), pad=pad)))


def middle(img, start, end):
    """The middle of a strip for phones. The cut runs through the shelf and the table, so its two
    ends dissolve into paper (a smoothstep over PHONE_FADE of the crop's width) instead of ending
    in a straight edge that would show on the page."""
    crop = img.crop((round(img.width * start), 0, round(img.width * end), img.height))
    side = round(crop.width * PHONE_FADE)
    arr = faded(np.asarray(crop).astype(np.float32), side, side)
    return Image.fromarray(np.clip(np.rint(arr), 0, 255).astype(np.uint8))


def finish(img, name, width):
    return bd.art_of(bd.feathered(img, EDGE), f"{name}-{V}", width)


def cut_near(img, frac, span=0.08):
    """The column with the least ink within `span` of `frac` of the width (smoothed)."""
    ink = 255.0 - np.asarray(img.convert("L")).astype(np.float32)
    profile = np.convolve(ink.mean(axis=0), np.ones(31) / 31, mode="same")
    a, b = round(img.width * (frac - span)), round(img.width * (frac + span))
    return a + int(np.argmin(profile[a:b]))


def scenes(img):
    cuts = [0, cut_near(img, 1 / 3), cut_near(img, 2 / 3), img.width]
    out = []
    for i, (a, b) in enumerate(zip(cuts, cuts[1:])):
        piece = img.crop((a, 0, b, img.height))
        # level 200: the scene's own ink, not the faint mist between scenes
        box = bd.ink_box(np.asarray(piece), level=200, pad=0.12)
        out.append(finish(piece.crop(box), f"health-scene-{i + 1}", 900))
    return out


def write_ts(art):
    head = [
        "// Generated by reference/ink-pages/science/build_science.py. Do not edit by hand: change",
        "// the script (or its TAKES) and run it again. The Science page's ink paintings (October 14,",
        "// 2026): GPT Image 2.5 on rice paper, the paper divided out so each multiplies onto the page's",
        "// own paper. scroll.stops: where each stop's place stands, as fractions of the scroll's width.",
        "",
    ]
    TS.parent.mkdir(parents=True, exist_ok=True)
    TS.write_text("\n".join(head) + f"export const scienceArt = {json.dumps(art, indent=2)} as const;\n", encoding="utf-8", newline="\n")
    prettier = REPO / "node_modules/prettier/bin/prettier.cjs"
    subprocess.run(["node", str(prettier), "--write", str(TS)], cwd=REPO, check=True, capture_output=True)
    print(TS.relative_to(REPO))


if __name__ == "__main__":
    scrolls = strip("scrolls")
    health = strip("health")
    mugs = strip("mugs")
    write_ts(
        {
            "scroll": handscroll(),
            "scrolls": {**finish(scrolls, "scrolls", 2400), "phone": finish(middle(scrolls, 0.3, 0.7), "scrolls-phone", 1000)},
            "health": {**finish(health, "health", 2400), "scenes": scenes(health)},
            "mugs": {**finish(mugs, "mugs", 2400), "phone": finish(middle(mugs, 0.22, 0.78), "mugs-phone", 1000)},
        }
    )

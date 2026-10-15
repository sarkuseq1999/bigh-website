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
trimmed to their own ink, their cut ends faded to paper) and the health strip's three scenes, cut
where the ink is thinnest near its thirds. The mugs' crop (0.27-0.70 of the strip) is the tightest
that keeps both mugs, handles included, clear of the faded ends, so they are as large as they can
be on a phone.

The mugs' steam (Task 6 review, October 14): its strokes are thin and light, so the ink box (a
blurred mask) missed them and cut the strip's top at the mugs' rims, and the steam the painting was
made for was gone. TOPS keeps each named strip's top at that row of the original (the steam starts
at about row 250), on the wide strip and the phone crop. The mugs' pictures are v2 (MUGS_V): a
picture whose content changes gets a new name, so no cache serves the old one.

A shorter crossing (Task 6 fix round 1, Ruling 13): the first screen at 1440 showed the castle, a
wide empty ocean and nothing else, and a phone passed screens of sky over sea. CROPS cuts each
panel before it is laid down: panel 1 loses 260px of mist at its left (its castle's left pine still
clear of the band's misty end) and ends a short run of sea after the castle's rocks (they end near
x 1500, it is cut at 1760); panel 2 starts just before the boat (x 620; its first 450px are mist,
then open sea). Join 1 is still a crossfade, now over 200px of sea in both panels (panel 1's
1560-1760, panel 2's 620-820, the boat just after it), to one horizon (DY re-measured there:
panel 1's sea top is row 654 at x 1550-1750, panel 2's about 700 at x 560-760; panel 3 keeps its
5px under panel 2). The band is 5756 x 651 (6864 x 705 before: the sea's low spray at panel 1's
right was its lowest ink). The tower's trees now stand about 2200px from the band's left (3290
before), so they and the spire are in the first screen at 1280x720 and 1440x900. STOP_X is on the
new canvas (checked on plates/contact.jpg). The scroll ships as v2 (SCROLL_V).

The health strip's wide picture (Ruling 14): two grey washes between the lamp, the stones and the
poppies read as dirty marks. clean() keeps each scene's own box (the boxes its phone pictures are
cut to, so the scenes' ground shadows stay) and fades everything else to paper over CLEAN_FEATHER
px outside them. The wide picture ships as v2 (HEALTH_V); the phone scenes are cut from the
uncleaned strip, so they do not change.

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
# Each panel's columns kept (left, right) in its own pixels; None keeps the rest.
CROPS = ((260, 1760), (620, None), (0, None))
OVERLAP = (200, 300)
CROSSFADE = (True, False)
DY = (0, -46, -51)
FADES = ((0, 0), (0, 420), (420, 0))
# On the joined canvas: panel 1 at 0 (its x less 260), panel 2 at 1300 (its x less 620), panel 3 at
# 3068. Castle 756-260; tower 1720-620+1300; the hills of 2002 2330-620+1300; fortress 824+3068;
# oaks 2312+3068.
STOP_X = {"okayama": 496, "berkeley": 2400, "y2002": 3010, "salzburg": 3892, "today": 5380}
SCROLL_V = "v2"
HEALTH_V = "v2"
CLEAN_FEATHER = 60
PHONE_H = 400  # the scroll's phone picture: 300px tall on screen, 1.33x
EDGE = 0.03
PHONE_FADE = 0.08  # the phone crops' cut ends (middle()): fade to paper over this share of their width
TOPS = {"mugs": 225}  # a strip's top row on its original, where the ink box misses light strokes
MUGS_V = "v2"

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
    panels = []
    for i, (left, right) in zip((1, 2, 3), CROPS):
        arr = np.asarray(bd.divided(bd.load(TAKES[f"panel{i}"]))).astype(np.float32)
        panels.append(arr[:, left:right])
    h = panels[0].shape[0]
    widths = [arr.shape[1] for arr in panels]
    top = max(0, -min(DY))
    xs = [0, widths[0] - OVERLAP[0], widths[0] - OVERLAP[0] + widths[1] - OVERLAP[1]]
    canvas = np.full((h + top + max(0, max(DY)), xs[2] + widths[2], 3), 255.0, np.float32)
    for i, (arr, x, dy, (fade_l, fade_r)) in enumerate(zip(panels, xs, DY, FADES)):
        w = arr.shape[1]
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
    print("handscroll canvas", canvas.shape[1], "x", canvas.shape[0], "panels at", xs, "ink box x", x0, x1)
    art = bd.art_of(band, f"scroll-{SCROLL_V}", None)
    art["phone"] = bd.art_of(band, f"scroll-phone-{SCROLL_V}", round(band.width * PHONE_H / band.height))
    art["stops"] = {key: round((x - x0) / (x1 - x0), 4) for key, x in STOP_X.items()}
    return art


def strip(key, pad=0.04):
    flat = bd.divided(bd.load(TAKES[key]))
    x0, y0, x1, y1 = bd.ink_box(np.asarray(flat), pad=pad)
    return bd.levelled(flat.crop((x0, min(y0, TOPS.get(key, y0)), x1, y1)))


def middle(img, start, end, keep_top=False):
    """The middle of a strip for phones, trimmed to its ink. The cut drops the shelf's and the
    table's legs, so the rows the strip kept for them would be dead paper under the ink (about 40%
    of the mugs', 15% of the scrolls': October 14 review): the crop's ink box (bd.ink_box, on the
    crop itself) sets its top and bottom. The cut runs through the shelf and the table, so its two
    ends dissolve into paper (a smoothstep over PHONE_FADE of the crop's width) instead of ending
    in a straight edge that would show on the page. keep_top keeps the strip's own top (TOPS: light
    strokes above the ink box, the mugs' steam)."""
    crop = img.crop((round(img.width * start), 0, round(img.width * end), img.height))
    _, top, _, bottom = bd.ink_box(np.asarray(crop), pad=0.04)
    top = 0 if keep_top else top
    crop = crop.crop((0, top, crop.width, bottom))
    side = round(crop.width * PHONE_FADE)
    arr = faded(np.asarray(crop).astype(np.float32), side, side)
    return Image.fromarray(np.clip(np.rint(arr), 0, 255).astype(np.uint8))


def finish(img, name, width, v=V):
    return bd.art_of(bd.feathered(img, EDGE), f"{name}-{v}", width)


def cut_near(img, frac, span=0.08):
    """The column with the least ink within `span` of `frac` of the width (smoothed)."""
    ink = 255.0 - np.asarray(img.convert("L")).astype(np.float32)
    profile = np.convolve(ink.mean(axis=0), np.ones(31) / 31, mode="same")
    a, b = round(img.width * (frac - span)), round(img.width * (frac + span))
    return a + int(np.argmin(profile[a:b]))


def scene_boxes(img):
    """Each health scene's box on the strip: cut where the ink is thinnest near the thirds, then
    the box of the scene's own ink (level 200: not the faint washes between scenes), padded."""
    cuts = [0, cut_near(img, 1 / 3), cut_near(img, 2 / 3), img.width]
    boxes = []
    for a, b in zip(cuts, cuts[1:]):
        x0, y0, x1, y1 = bd.ink_box(np.asarray(img.crop((a, 0, b, img.height))), level=200, pad=0.12)
        boxes.append((a + x0, y0, a + x1, y1))
    return boxes


def scenes(img):
    return [finish(img.crop(box), f"health-scene-{i + 1}", 900) for i, box in enumerate(scene_boxes(img))]


def clean(img):
    """The strip with only its scenes: inside each scene's box the painting as it is, outside it
    paper, with a smoothstep over CLEAN_FEATHER px (Ruling 14: the washes between the scenes)."""
    arr = np.asarray(img).astype(np.float32)
    h, w = arr.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    keep = np.zeros((h, w), np.float32)
    for x0, y0, x1, y1 in scene_boxes(img):
        dx = np.maximum(np.maximum(x0 - xx, xx - (x1 - 1)), 0)
        dy = np.maximum(np.maximum(y0 - yy, yy - (y1 - 1)), 0)
        k = np.clip(1 - np.hypot(dx, dy) / CLEAN_FEATHER, 0, 1)
        keep = np.maximum(keep, k * k * (3 - 2 * k))
    out = arr * keep[..., None] + 255.0 * (1 - keep[..., None])
    return Image.fromarray(np.clip(np.rint(out), 0, 255).astype(np.uint8))


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
            "health": {**finish(clean(health), "health", 2400, HEALTH_V), "scenes": scenes(health)},
            "mugs": {
                **finish(mugs, "mugs", 2400, MUGS_V),
                "phone": finish(middle(mugs, 0.27, 0.70, keep_top=True), "mugs-phone", 1000, MUGS_V),
            },
        }
    )

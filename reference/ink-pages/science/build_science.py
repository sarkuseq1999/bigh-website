"""Build the Science page's paintings.

Round 3 (Mo, November 4, 2026; spec docs/superpowers/specs/2026-11-04-science-california-design.md):
the page opens on the science ("Our science starts in the cell.") and turns from an Asian feel to
California. Every picture is a Codex painting (Mo's ChatGPT plan, no API spend; orders in prompts/,
sent by paint.sh) in the homepage close's way of painting, ink and wash with light colour:

- zoom: the opening and "Why start with the cell?" as one slow zoom (Mo, November 9, 2026: the
  desk at the window was plain and the town did not say "cell"). Since November 10 it starts
  inside the cell and pulls back (Mo picked A of four ideas for the first screen): the inside of
  one cell (zoom-inside-1), that cell whole, its mitochondria as slivers of gold (zoom-cell-2),
  the walker's hand in the dry grass (zoom-hand-2), the walker on golden hills (zoom-hills-1).
  The inside view, the hand and the hills fill the window, so they keep their whole frame and no
  feathered edge; the cell is cropped to its ink. The inside view's gold slivers are lifted off
  it (lifted()) and ship beside it as one picture of pieces, so each can drift on its own.
- places: Dr. Liu's path, Berkeley, Salzburg and Today, each a Codex repaint of the October
  handscroll's cut with light washes (wash-<place>-1). Today keeps the handscroll's own gold-leaf
  sun, cut from its old picture and set in the new sky (SUN).
- journals: the research, bound journals on a library table, three laid open (journals-1).
- picnic: Ask BiGH Science, two camp mugs on a redwood picnic table (picnic-1).

Each painting's paper is divided out and lifted to white (reference/ink-pages/about/build_about.py),
so it multiplies onto the page's paper with no box, and its outer edge is feathered. Phones get
tighter cuts. The October pictures (the handscroll's Okayama cut, the scrolls, the health scenes,
the mugs) and round 3's desk and town no longer ship; their originals stay in originals/.

usage: python -X utf8 reference/ink-pages/science/build_science.py
"""

import json
import subprocess
import sys
from pathlib import Path

import cv2
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
ORIG = HERE / "originals"
PLATES = HERE / "plates"
# Bump when a shipped picture changes after it has been pushed (the image optimizer caches by URL).
V = "v3"
# The loose takes (November 4): the first takes (journals-1, picnic-1) read as tidy illustrations;
# each was painted again far more loosely (paint.sh loose-*). The zoom (November 9): the hand's and
# the cell's first takes read as a realistic hand and a schoolbook diagram; each was ordered again
# looser (prompts/zoom-hand-2.txt, zoom-cell-2.txt).
TAKES = {
    "zoom-inside": "zoom-inside-1",
    "zoom-hills": "zoom-hills-1",
    "zoom-hand": "zoom-hand-2",
    "zoom-cell": "zoom-cell-2",
    "berkeley": "wash-berkeley-1",
    "salzburg": "wash-salzburg-1",
    "today": "wash-today-1",
    "journals": "loose-journals-1-1",
    "picnic": "loose-picnic-1-1",
}
EDGE = 0.03
PHONE_FADE = 0.08
# Phone cuts (left, right) as shares of the wide picture's width; their cut ends fade to paper.
PHONE = {
    "berkeley": (0.14, 0.86),
    "salzburg": (0.1, 0.94),
    "today": (0.12, 0.92),
    "journals": (0.18, 0.82),
    "picnic": (0.12, 0.88),
}
# Today's sun: the handscroll's gold leaf (old place-today-v1.webp), set at this point of the new
# painting (shares of its width and height), this wide (a share of its width).
SUN = (0.6, 0.2, 0.062)

bd.ORIG = ORIG
bd.URL = URL
bd.V = V
ba.OUT = OUT
ba.PLATES = PLATES


def load(key):
    return Image.open(ORIG / f"{TAKES[key]}.png").convert("RGB")


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


def to_img(arr):
    return Image.fromarray(np.clip(np.rint(arr), 0, 255).astype(np.uint8))


def flat(img):
    """Paper divided out and lifted to white."""
    return bd.levelled(bd.divided(img))


def inked(img, pad=0.04, level=236):
    """Cropped to its ink (the box found on the picture itself)."""
    return img.crop(bd.ink_box(np.asarray(img), level=level, pad=pad))


def phone_cut(img, key):
    """The phone's cut of a wide picture: its middle (PHONE), trimmed to its ink, ends faded."""
    a, b = PHONE[key]
    crop = img.crop((round(img.width * a), 0, round(img.width * b), img.height))
    _, top, _, bottom = bd.ink_box(np.asarray(crop), pad=0.04)
    crop = crop.crop((0, top, crop.width, bottom))
    side = round(crop.width * PHONE_FADE)
    return to_img(faded(np.asarray(crop).astype(np.float32), side if a > 0 else 0, side if b < 1 else 0))


def art(img, name, width):
    return bd.art_of(bd.feathered(img, EDGE), f"{name}-{V}", width)


def with_phone(img, key, width=2400, phone_width=1100):
    out = art(img, key, width)
    out["phone"] = art(phone_cut(img, key), f"{key}-phone", phone_width)
    return out


def lifted(img, sat0=0.24):
    """A painting's gold slivers lifted off it: the painting with its gold painted out, and each
    sliver as (x0, y0, RGBA piece, area). Only for a painting whose one warm, strong colour is its
    gold (the inside of the cell). Two rounds: a colour key finds the gold roughly and the
    painting is filled in behind it (the hole cut wide, so it swallows each sliver's pale middle
    and leaves no gold-tinted edge to bleed back in); then a sliver is wherever the painting
    differs from that filled-in version and is warm, joined into one solid piece so it travels
    whole. The colour key alone broke the slivers into dashes."""
    rgb = np.asarray(img.convert("RGB"))
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
    hue, sat, val = hsv[..., 0] * 2.0, hsv[..., 1] / 255.0, hsv[..., 2] / 255.0

    def disc(n):
        return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (n, n))

    warm = np.clip(1.0 - np.abs(hue - 44.0) / 16.0, 0, 1)
    key = warm * np.clip((sat - sat0) / 0.2, 0, 1) * np.clip((val - 0.55) / 0.15, 0, 1)
    key = cv2.GaussianBlur(key, (0, 0), 0.8)
    seed = cv2.morphologyEx((key > 0.35).astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    pale = ((np.abs(hue - 47.0) < 12.0) & (sat > 0.10) & (val > 0.86)).astype(np.uint8)
    hole = cv2.dilate(seed, disc(23))
    for _ in range(2):
        base = cv2.inpaint(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), hole * 255, 9, cv2.INPAINT_TELEA)
        base = cv2.cvtColor(base, cv2.COLOR_BGR2RGB)
        far = np.linalg.norm(rgb.astype(np.float32) - base.astype(np.float32), axis=2)
        # Only what is warm: the filled-in wash is smoother than the painted one, so the wash
        # itself differs a little too, and a sliver must not carry a ragged patch of it along.
        warmth = np.clip((rgb[..., 0].astype(np.float32) - rgb[..., 2].astype(np.float32) - 18.0) / 22.0, 0, 1)
        alpha = cv2.GaussianBlur(np.clip((far - 10.0) / 30.0, 0, 1) * warmth * hole, (0, 0), 0.7)
        body = cv2.morphologyEx((alpha > 0.3).astype(np.uint8), cv2.MORPH_CLOSE, disc(11))
        beside = cv2.morphologyEx(pale * cv2.dilate(hole, disc(41)), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        hole = np.maximum(hole, cv2.dilate(np.maximum(body, beside), disc(19)))
    alpha = np.maximum(alpha, cv2.GaussianBlur(body.astype(np.float32), (0, 0), 1.0) * 0.95)

    count, labels, stats, _ = cv2.connectedComponentsWithStats(body, connectivity=8)
    slivers = []
    for i in range(1, count):
        x, y, w, h, area = (int(v) for v in stats[i])
        if area < 70:
            continue
        pad = 8
        x0, y0 = max(0, x - pad), max(0, y - pad)
        x1, y1 = min(rgb.shape[1], x + w + pad), min(rgb.shape[0], y + h + pad)
        own = cv2.dilate((labels[y0:y1, x0:x1] == i).astype(np.uint8), np.ones((7, 7), np.uint8))
        a = (alpha[y0:y1, x0:x1] * own * 255).clip(0, 255).astype(np.uint8)
        slivers.append((x0, y0, Image.fromarray(np.dstack([rgb[y0:y1, x0:x1], a]), "RGBA"), area))
    return Image.fromarray(base), slivers


def pieces(slivers, size, name, width=1024, gap=2):
    """The slivers packed into one picture (rows, tallest first), and where each one is: its box
    in the painting and in that picture (shares of each), and how it drifts. A big sliver is near
    and travels further; a small one is far and barely moves. The drift is fixed here, so the
    page's first paint and its script agree."""
    order = sorted(range(len(slivers)), key=lambda i: -slivers[i][2].height)
    spots, x, y, row = {}, gap, gap, 0
    for i in order:
        piece = slivers[i][2]
        if x + piece.width + gap > width:
            x, y, row = gap, y + row + gap, 0
        spots[i] = (x, y)
        x += piece.width + gap
        row = max(row, piece.height)
    sheet = Image.new("RGBA", (width, y + row + gap), (0, 0, 0, 0))
    for i, (px, py) in spots.items():
        sheet.paste(slivers[i][2], (px, py))
    OUT.mkdir(parents=True, exist_ok=True)
    sheet.save(OUT / f"{name}.webp", "WEBP", quality=90, alpha_quality=92, method=6)

    rng = np.random.default_rng(11)
    w, h = size
    items = []
    for i, (x0, y0, piece, area) in enumerate(slivers):
        px, py = spots[i]
        near = min(1.0, area**0.5 / 60)
        reach = 0.35 + 0.65 * near
        angle = rng.random() * np.pi * 2
        items.append(
            {
                "box": [round(x0 / w, 4), round(y0 / h, 4), round(piece.width / w, 4), round(piece.height / h, 4)],
                "at": [round(px / sheet.width, 5), round(py / sheet.height, 5), round(piece.width / sheet.width, 5), round(piece.height / sheet.height, 5)],
                "drift": [round(float(np.cos(angle) * reach), 3), round(float(np.sin(angle) * reach * 0.6), 3)],
                "turn": round(float((rng.random() - 0.5) * 9), 1),
                "delay": [round(float(rng.random()), 3), round(float(rng.random()), 3)],
            }
        )
    return {"src": f"{URL}/{name}.webp", "width": sheet.width, "height": sheet.height, "slivers": items}


def zoom():
    """The opening's four views, in the order the page shows them. The inside of the cell, the
    hand and the hills fill the window (object-fit: cover), so they keep their whole 3:2 frame,
    unfeathered; the cell stands alone on the paper, cropped to its ink and feathered like every
    other painting. The inside view ships without its gold (inside), which rides above it in
    pieces (inside.gold)."""
    wash, slivers = lifted(flat(load("zoom-inside")))
    out = {"inside": bd.art_of(wash, f"zoom-inside-{V}", 1536)}
    out["inside"]["gold"] = pieces(slivers, wash.size, f"zoom-inside-gold-{V}")
    out["cell"] = art(inked(flat(load("zoom-cell")), pad=0.03), "zoom-cell", 1400)
    out.update({key: bd.art_of(flat(load(f"zoom-{key}")), f"zoom-{key}-{V}", 1536) for key in ("hand", "hills")})
    return out


def sun_leaf():
    """The handscroll's gold-leaf sun as an RGBA cut-out, from its old Today picture."""
    old = Image.open(PLATES / "place-today.png").convert("RGB")
    arr = np.asarray(old)
    m = cv2.morphologyEx(bd.gold_pixels(arr).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    i = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    x, y, w, h = (int(v) for v in st[i, :4])
    pad = int(max(w, h) * 0.3)
    return ba.leaf(old.crop((x - pad, y - pad, x + w + pad, y + h + pad))), w


def today(img):
    """Today's new painting with the handscroll's own gold sun in its sky."""
    leaf, disc = sun_leaf()
    cx, cy, size = SUN
    k = size * img.width / disc
    leaf = leaf.resize((round(leaf.width * k), round(leaf.height * k)), Image.LANCZOS)
    canvas = img.convert("RGBA")
    canvas.alpha_composite(leaf, (round(cx * img.width - leaf.width / 2), round(cy * img.height - leaf.height / 2)))
    return canvas.convert("RGB")


def place(key):
    img = flat(load(key))
    if key == "today":
        img = today(img)
    return inked(img, pad=0.03)


def write_ts(data):
    head = [
        "// Generated by reference/ink-pages/science/build_science.py. Do not edit by hand: change",
        "// the script (or its TAKES) and run it again. The Science page's paintings (round 3,",
        "// November 4, 2026; the zoom opening, November 9, from inside the cell since November 10):",
        "// Codex paintings in ink and wash, the paper divided out so each multiplies onto the page's",
        "// own paper.",
        "",
    ]
    TS.write_text("\n".join(head) + f"export const scienceArt = {json.dumps(data, indent=2)} as const;\n", encoding="utf-8", newline="\n")
    prettier = REPO / "node_modules/prettier/bin/prettier.cjs"
    subprocess.run(["node", str(prettier), "--write", str(TS)], cwd=REPO, check=True, capture_output=True)
    print(TS.relative_to(REPO))


if __name__ == "__main__":
    data = {
        "zoom": zoom(),
        "places": {key: with_phone(place(key), key, 1600, 1100) for key in ("berkeley", "salzburg", "today")},
        "journals": with_phone(inked(flat(load("journals")), pad=0.03), "journals"),
        "picnic": with_phone(inked(flat(load("picnic")), pad=0.03), "picnic"),
    }
    write_ts(data)

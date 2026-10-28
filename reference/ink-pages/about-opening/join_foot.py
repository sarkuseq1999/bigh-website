"""A painted end for the superbloom's foot (Mo, October 28, 2026: A's first screen "and the second
section don't transition well"; the meadow stopped in a straight line).

    python -X utf8 reference/ink-pages/about-opening/join_foot.py canvas
    python -X utf8 reference/ink-pages/about-opening/join_foot.py join <edit-take> [seam_rows]

`canvas` writes plates/join/foot-canvas.png, the picture Codex is asked to edit: the painting's
bottom half on top, bare paper (cut from its sky) below. Codex continues the meadow into the paper
(prompts/superbloom-foot-*.txt, takes in originals/superbloom-foot-*.png).

`join` lines the edit's top half up with the painting's bottom half (it should need no shift),
keeps the painting down to its foot less seam_rows, cross-fades into the edit over seam_rows, and
runs the edit's continuation below: a 1536 x 1536 painting whose original foot is row 1024. It
writes plates/join/<take>.png and the two layers the page would ship, as build_about_opening
makes them (the painting with its gold a pale ghost, and the gold alone), with no feather but a
short ease over the last 4% in case the edit's paper is not quite bare.
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image

from cut_mockups import divided, to_alpha

HERE = Path(__file__).resolve().parent
OUT = HERE / "plates" / "join"
TAKE = "superbloom-a1"
CHROMA = (34.0, 80.0)
GHOST = 0.4


def smoothstep(x, lo, hi):
    t = np.clip((x - lo) / (hi - lo), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def painting():
    return np.asarray(Image.open(HERE / "originals" / f"{TAKE}.png").convert("RGB")).astype(np.float32)


def canvas():
    img = Image.open(HERE / "originals" / f"{TAKE}.png").convert("RGB")
    w, h = img.size
    out = Image.new("RGB", (w, h))
    out.paste(img.crop((0, h // 2, w, h)), (0, 0))
    # Bare paper from the sky, clear of the far ridge's oaks (they start near row 440).
    out.paste(img.crop((0, 0, w, 400)), (0, h // 2))
    out.paste(img.crop((0, 0, w, h - h // 2 - 400)), (0, h // 2 + 400))
    out.save(OUT / "foot-canvas.png")
    print("foot-canvas.png", out.size)


def best_shift(orig, edit):
    """Rows the edit sits off the painting's bottom half (edit row r ~ painting row 512 + r - dy)."""
    o, e = orig.mean(axis=2), edit.mean(axis=2)
    errs = {dy: float(np.abs(o[700:980] - e[188 + dy : 468 + dy]).mean()) for dy in range(-40, 41)}
    dy = min(errs, key=errs.get)
    return dy, errs[dy]


def joined(take, seam=60):
    """The painting with the edit's continuation under it, full colour, paper kept: 1536 wide, its
    original foot at row 1024."""
    orig = painting()
    edit = Image.open(HERE / "originals" / f"{take}.png").convert("RGB")
    if edit.size != (1536, 1024):
        edit = edit.resize((1536, 1024), Image.LANCZOS)
    edit = np.asarray(edit).astype(np.float32)
    dy, err = best_shift(orig, edit)
    print(f"{take}: shift {dy}px, mean difference {err:.1f}")
    start = 1024 - seam
    tail = edit[start - 512 + dy :]
    out = np.empty((start + tail.shape[0], 1536, 3), np.float32)
    out[:start] = orig[:start]
    out[start:] = tail
    t = smoothstep(np.linspace(0, 1, seam, dtype=np.float32), 0, 1)[:, None, None]
    out[start : start + seam] = orig[start:1024] * (1 - t) + tail[:seam] * t
    return Image.fromarray(out.clip(0, 255).astype(np.uint8))


def layers(whole, ease=0.04):
    """The two layers the page ships, as build_about_opening makes them: the painting with its gold
    a pale ghost, and the gold alone; no feather, but a short ease over the last `ease` of the
    height in case the paper there is not quite bare."""
    h = whole.height
    flat = divided(whole, top=True)
    gold = smoothstep(flat.max(axis=2) - flat.min(axis=2), *CHROMA)[..., None]
    grey = flat.mean(axis=2, keepdims=True).repeat(3, axis=2)
    ghost = 255.0 - (255.0 - grey) * GHOST
    base = np.asarray(to_alpha(flat * (1 - gold) + ghost * gold)).astype(np.float32)
    top = np.asarray(to_alpha(flat)).astype(np.float32)
    n = round(h * ease)
    ramp = np.ones(h, np.float32)
    ramp[h - n :] = smoothstep(np.linspace(1, 0, n, dtype=np.float32), 0, 1)
    base[..., 3] *= ramp[:, None]
    top[..., 3] *= gold[..., 0] * ramp[:, None]
    return base, top


def painted_to(base):
    """The row under the last painted one: rows with more than 0.5% of their pixels inked."""
    return int(np.nonzero((base[..., 3] > 30).mean(axis=1) > 0.005)[0].max()) + 1


def join(take, seam=60):
    whole = joined(take, seam)
    whole.save(OUT / f"{take}.png")
    base, top = layers(whole)
    for arr, suffix in ((base, "base"), (top, "gold")):
        Image.fromarray(arr.clip(0, 255).astype(np.uint8), "RGBA").save(
            OUT / f"{take}-{suffix}.webp", quality=84, method=6
        )
    ink = painted_to(base)
    print(f"  {whole.width}x{whole.height}; painted down to row {ink} ({ink / 1536:.3f} of its width)")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    if sys.argv[1] == "canvas":
        canvas()
    else:
        join(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 60)

# About "The Name, on a Folded Letter" Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the first ink About page (a copy of the homepage) with Mo's approved design D: one sheet of slightly aged, folded paper; BiGH written by hand at the top; one brushed letter opening each part (Be, in, Good, Health).

**Architecture:** New paintings are made with GPT Image 2.5 and turned into web pictures by a small build script that reuses the homepage's picture tools; it also writes a generated TypeScript file with each picture's size and the gold dots' places. The shared `InkPage` shell gains two optional props (no brush route, a root class) so About can drop the brush line and dress the paper. About is rewritten as five parts on a two-column grid split by a CSS fold; motion is CSS keyed to the kit's existing hooks (`useArrival`, `useBloom`).

**Tech Stack:** Next.js 16 (App Router, Turbopack), React, TypeScript, CSS Modules, next-intl (`useCopy`), Playwright for Python (QA), Pillow, NumPy and OpenCV (pictures), the Higgsfield API helper for GPT Image 2.5.

**Spec:** `docs/superpowers/specs/2026-10-05-ink-pages-design.md`, section "About (stage 1), redesigned October 6: 'The name, on a folded letter'". Mockup: `reference/ink-pages/mockups/about-d.png`. Design system: `DESIGN.md`.

## Global Constraints

- Read `AGENTS.md` first. This Next.js has breaking changes: check `node_modules/next/dist/docs/` before using a Next API you have not seen in this repo. The repo's existing `next/image` usage (`priority`, `sizes`) is the pattern to follow.
- Worktree `C:/Users/mcbig/Documents/codes/bigh-ink`, branch `ink-pages`. Commit locally; never push (the GitHub repo is public; Mo approves every push).
- Bash: never `cd`; use absolute paths, `git -C`, `npm --prefix`. Files are LF and the checkout has `core.autocrlf=true`: never `git stash`; write files with LF (`newline="\n"` in Python); `npx prettier --write <file>` restores LF.
- The homepage must not change. Task 2 touches the shared kit and runs the homepage gate; Task 6 runs it again on the built site.
- Words: every line of `src/components/about/about-content.ts` stays (locked by Mo, September 25, 2026). The h1 stays English "Be in Good Health." with `lang="en"` in every language. The chapter words (Be, in, Good, Health) stay English in every language and are `aria-hidden="true"`.
- DESIGN.md rules: One Gold Leaf (gold only inside paintings), No Red No Seal, Sentence Case, Multiply (every ink painting `mix-blend-mode: multiply`), no cards or boxes, the photo mount is the only shadow, text 15px or larger, navigation 18px or larger, targets 48px or taller, one breath `--breath: 2.4s` with `--ease: cubic-bezier(0.22, 0.61, 0.36, 1)`, reduced motion complete and still, honesty tag "Illustration" on pictures that depict something (here: the tree rings only).
- **Multiply trap:** a painting multiplies onto the page root's paper only if no element between it and the root creates a stacking context. Never put `z-index` on a positioned ancestor, `isolation`, `opacity < 1`, `transform`, `filter` or `will-change` on `.sheet`, a part, a grid or a figure that holds paintings. (The kit's bloom puts `filter` on the image itself; that is fine.)
- **Specificity:** `homepage.module.css` resets `.site p`, `.site button`, `.site h2` (0,1,1) and the kit uses `.look …` (0,2,0). Every About rule is scoped under `.letterPage` (the page root's class) so it wins whatever order the built stylesheets load in.
- Real assets only: Dr. Liu's photo `public/images/jiankang-liu.jpg` as it is; bottles and faces are never generated.
- Spend: GPT Image 2.5 jobs through `reference/home-v2/r4/hf_unquoted.py` only, with `HF_RUN_STATE=C:/Users/mcbig/AppData/Local/HiggsfieldAPI/bigh-about-letter` (its own ledger; the helper stops at 30 jobs, about $1.50, at most $2.10). Never read or print the Higgsfield credential. Never retry a failed job automatically: a ledger line means it was billed; read the ledger before deciding. Log every job in `reference/ink-pages/spend.md`.
- Dev server: preview entry `bigh-ink` (port 3025). Built site: `bigh-ink-prod` (port 3026) after `npm --prefix C:/Users/mcbig/Documents/codes/bigh-ink run build`. If the preview tool refuses, start the same command from the shell with `run_in_background`. A new or deleted file can need a dev-server restart.
- Look at every screenshot you take at full size before calling something done; the bar is 9/10 as a visitor would see it (scroll it, don't just read numbers). Anything that looks broken is a defect, even if it was "on purpose".

## Review Focus

- Translated words are longer (Vietnamese) or break differently (Japanese, Chinese, Korean): in the two-sided parts no line may cross the middle fold, at 1440 and 1024 wide. Test in Task 5 (`languages_layout`, CREASE_JS).
- JavaScript is slow or off: the written name must still appear (its animation is pure CSS, never waiting on a script). Test in Task 4 (`motion`, JavaScript off).
- The window sits right at the 899/900px switch: no sideways scrolling, the middle fold shows at 900 only, and no words cross it there. Test in Task 3 (`boundary`).
- Pictures are slow or blocked: every heading and paragraph is still visible, nothing waits at opacity 0 for a picture. Test in Task 3 (`focus`).
- A short desktop window (1280x720, 1536x864): the written name, the title and the start of the band are in the first screen, so it does not open on an empty sheet. Test in Task 3 (`first_screen`).

---

### Task 1: The paintings and their build

**Files:**

- Create: `reference/ink-pages/about/prompts/word-v1.txt`, `letter-b-v1.txt`, `letter-i-v1.txt`, `letter-g-v1.txt`, `letter-h-v1.txt`, `band-v1.txt`, `pool-v1.txt`, `rings-v1.txt`, `dots-v1.txt`
- Create: `reference/ink-pages/about/refs/ref-word.png` (a crop of the mockup)
- Create: `reference/ink-pages/about/originals/gpt25-*.png` (the helper writes them)
- Create: `reference/ink-pages/about/build_about.py`
- Create: `reference/ink-pages/about/check_art.py`
- Create: `reference/ink-pages/spend.md`
- Create (generated): `src/components/about/letter-art.ts`, `public/images/about-ink/*.webp`, `public/images/about-ink/wipe-v1.png`, `reference/ink-pages/about/plates/*.png`

**Interfaces:**

- Consumes: `reference/home-v2/ink/build_assets.py` (`leaf(img)`, `save(img, name, width, quality)`, `gold_mask(name, ...)`; module globals `OUT` and `PLATES` are read at call time, so they can be pointed elsewhere).
- Produces: `src/components/about/letter-art.ts` exporting
  - `type Art = { src: string; width: number; height: number }`
  - `type Dot = Art & { left: number; top: number; size: number }` (fractions of the painting's width, height, width)
  - `paperAged: string`, `wipe: string`
  - `word: Art & { dot: Dot }`
  - `letters: { B: Art; i: Art & { dot: Dot }; G: Art; H: Art }`
  - `band: Art`, `pool: Art`, `rings: Art & { gold: string }`, `dots: Art[]` (four, deep to pale)
  - (all `as const`)
- Produces: `/images/about-ink/wipe-v1.png` (the brush wipe mask) and `/images/about-ink/paper-aged-v1.webp` (the aged paper tile), used by Task 3 and Task 4 CSS by these exact URLs.

- [ ] **Step 1: Make the reference crop of the mockup's written name**

Run:

```bash
python -X utf8 -c "from PIL import Image; from pathlib import Path; R=Path('C:/Users/mcbig/Documents/codes/bigh-ink/reference/ink-pages'); (R/'about/refs').mkdir(parents=True, exist_ok=True); Image.open(R/'mockups/about-d.png').convert('RGB').crop((360,180,1190,500)).save(R/'about/refs/ref-word.png'); print('ok')"
```

Then look at `reference/ink-pages/about/refs/ref-word.png` with the Read tool. Expected: the brushed word BiGH with the gold dot, whole, nothing cut off. If a letter is cut, widen the box and run again.

- [ ] **Step 2: Write the nine prompts**

Every prompt starts with this paragraph (call it STYLE):

```text
Traditional East Asian ink painting on one plain sheet of warm, light rice paper with fine fibres, seen flat from straight above, evenly lit, no shadow, no frame, no table, no other objects, no text, no signature, no red seal, no stamp. Sumi ink only, from deep black to soft grey washes, plus real gold leaf only where stated. Generous empty paper on every side.
```

`word-v1.txt` = STYLE, a blank line, then:

```text
The word BiGH (capital B, lowercase i, capital G, capital H) written once, large, by hand with a loaded calligraphy brush in sumi ink, in a calm, steady, skilled calligrapher's hand: each stroke made in one confident movement, swelling and thinning naturally, softly irregular edges where the ink sinks into the fibres, a light hint of dry-brush texture only at some stroke ends. Easy to read, dignified and warm; never wild: no splatter, no drips, no flying flicks, no graffiti energy. The four letters sit on one baseline, evenly spaced, not touching. The dot of the i is a small round dot of real gold leaf with a softly torn leaf edge, clearly separate from the stem. Match the letter shapes of the reference picture. Centred, the word about 70% of the picture's width.
```

`letter-b-v1.txt` = STYLE, then:

```text
One capital letter B, written once, large, by hand with a loaded calligraphy brush in sumi ink, in the same calm, steady hand as the B of the reference picture: one confident movement per stroke, natural swelling and thinning, softly irregular edges, a light hint of dry-brush texture only at some stroke ends. Easy to read; no splatter, no drips, no flicks. Centred, the letter about 70% of the picture's height.
```

`letter-i-v1.txt` = STYLE, then:

```text
One lowercase letter i, written once, large, by hand with a loaded calligraphy brush in sumi ink, in the same calm, steady hand as the i of the reference picture. The stem is one confident downward stroke, slightly swelling, with a clean soft end: clearly the letter i, never a blot, comma or teardrop. Above it, separated from the stem by about the stem's own width, a small round dot of real gold leaf with a softly torn leaf edge. No splatter, no drips. Centred, stem and dot together about 70% of the picture's height.
```

`letter-g-v1.txt` = STYLE, then:

```text
One capital letter G, written once, large, by hand with a loaded calligraphy brush in sumi ink, in the same calm, steady hand as the G of the reference picture: an open round bowl and a short firm bar, one confident movement per stroke, natural swelling and thinning, softly irregular edges, a light hint of dry-brush texture only at some stroke ends. Easy to read; no splatter, no drips, no flicks. Centred, the letter about 70% of the picture's height.
```

`letter-h-v1.txt` = STYLE, then:

```text
One capital letter H, written once, large, by hand with a loaded calligraphy brush in sumi ink, in the same calm, steady hand as the H of the reference picture: two upright strokes and a crossbar that runs a little past the right stroke, one confident movement per stroke, natural swelling and thinning, softly irregular edges, a light hint of dry-brush texture only at some stroke ends. Easy to read; no splatter, no drips, no flicks. Centred, the letter about 70% of the picture's height.
```

`band-v1.txt` = STYLE, then:

```text
One long horizontal band of thinned grey sumi ink wash, laid in one wide pass of a broad wet brush from the far left of the picture to the far right: soft mid grey in the middle, paler towards both ends, feathering out into the paper at both ends and along its top and bottom edges, with gentle watercolor blooms and a little granulation. No black strokes, no shapes, nothing else. The band about 92% of the picture's width and 16% of its height, centred.
```

`pool-v1.txt` = STYLE, then:

```text
One soft pool of pale grey watercolor ink, as if a wet brush loaded with thinned sumi ink was laid down and the wash spread out on its own: roughly oval, a little taller than wide, irregular feathered edges with small blooms, slightly darker towards its lower left, pale and quiet. Nothing else. The pool about 70% of the picture's height, centred.
```

`rings-v1.txt` = STYLE, then:

```text
A tree trunk's cross-section seen straight on, painted in sumi ink: a slightly irregular round slice with a rough bark edge, at least 24 organic growth rings drawn with a fine brush, unevenly spaced and gently wavering like real wood, a small dark heart slightly off centre, two or three fine radial cracks, soft grey washes between some rings. Exactly one ring, about ten rings in from the bark, is laid in real gold leaf: a thin continuous gold circle following the wood's wavering line. Hand-painted, never mechanical or perfectly concentric. The slice about 76% of the picture's height, centred.
```

`dots-v1.txt` = STYLE, then:

```text
Four small round watercolor dots of sumi ink in one row across the middle of the picture, evenly spaced and well apart, each laid with one touch of a round wet brush, softly irregular edges with tiny blooms: from left to right deep black, dark grey, mid grey and pale grey. Each dot about 15% of the picture's height. Nothing else.
```

- [ ] **Step 3: Start the spend log**

Create `reference/ink-pages/spend.md`:

```markdown
# Ink pages: picture spend

GPT Image 2.5 through `reference/home-v2/r4/hf_unquoted.py`, about $0.05 a picture (billed $0.07,
$0.02 refunded on reconcile). Check open.higgsfield.ai/billing for the real total.

## About redesign, "The name, on a folded letter" (Mo's $5, October 6, 2026)

Ledger: `C:/Users/mcbig/AppData/Local/HiggsfieldAPI/bigh-about-letter/ledger-nav-gpt.jsonl` (cap 30 jobs).
Mockup round before this plan: 13 jobs in `bigh-about2` (about $0.65).

| Job | Picture | Kept | Note |
| --- | ------- | ---- | ---- |
```

- [ ] **Step 4: Run the first take of each painting, one at a time**

For each `NAME` in `word-v1 letter-b-v1 letter-i-v1 letter-g-v1 letter-h-v1` (these use the reference crop):

```bash
HF_RUN_STATE=C:/Users/mcbig/AppData/Local/HiggsfieldAPI/bigh-about-letter python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/reference/home-v2/r4/hf_unquoted.py NAME C:/Users/mcbig/Documents/codes/bigh-ink/reference/ink-pages/about/prompts/NAME.txt --aspect 16:9 --ref C:/Users/mcbig/Documents/codes/bigh-ink/reference/ink-pages/about/refs/ref-word.png --out C:/Users/mcbig/Documents/codes/bigh-ink/reference/ink-pages/about/originals
```

For each `NAME` in `band-v1 pool-v1 rings-v1 dots-v1` (no reference), the same command without `--ref`.

Expected for each: `submitted …`, `status completed`, `saved …/gpt25-NAME.png`, `jobs this round: N of 30`. Run them in the background if you like (one at a time: the helper holds a lock). If a job ends in an error, do NOT run it again before reading the ledger file named in Global Constraints: a ledger line for that name means it was billed. Add one row per job to `spend.md`.

- [ ] **Step 5: Look at every original at full size and keep or retake**

Read each `originals/gpt25-*.png` with the Read tool (crop halves with PIL if needed to see detail). Keep a take only if it passes:

- Word and letters: legible at a glance; calm, controlled strokes; no splatter, drips or flicks; the same hand as `ref-word.png`; the i reads as an i with a round gold dot clearly apart from its stem; plain paper; no red.
- Band: soft grey, feathered at both ends and edges; no black, no hard end.
- Pool: pale, irregular, no hard rim, nothing else.
- Rings: hand-painted, not mechanical; 20 or more rings; exactly one gold ring roughly ten rings in from the bark.
- Dots: four separate dots, clearly four tones from deep to pale.

A failed picture gets at most two retakes. For a retake copy its prompt to `NAME-v2.txt` (then `-v3`), add one sentence naming the defect ("The dot must be round and sit clearly above the stem, not touching it."), and run Step 4's command with the new name. Record every job and which take is kept in `spend.md`.

- [ ] **Step 6: Write the build script**

Create `reference/ink-pages/about/build_about.py`:

```python
"""Build the About page's paintings ("The name, on a folded letter", Mo's design D, October 6, 2026).

Originals: reference/ink-pages/about/originals/gpt25-<take>.png (GPT Image 2.5 on rice paper; prompts
in prompts/, spend in reference/ink-pages/spend.md). Output: public/images/about-ink/*.webp (lossless
plates in plates/), the brush wipe mask wipe-<V>.png, and src/components/about/letter-art.ts (sizes
and the gold dots' places), which the page imports. The treatments are the homepage's
(reference/home-v2/ink/build_assets.py): the paper divided out so a painting multiplies onto the
page's own paper, gold leaf cut out with its torn edge, and the gold-leaf light mask.

usage: python -X utf8 reference/ink-pages/about/build_about.py
"""

import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "reference/home-v2/ink"))
import build_assets as ba  # noqa: E402

ORIG = HERE / "originals"
OUT = REPO / "public/images/about-ink"
ba.OUT = OUT  # ba.save and ba.gold_mask write here (module globals, read at call time)
ba.PLATES = HERE / "plates"
URL = "/images/about-ink"
TS = REPO / "src/components/about/letter-art.ts"
# Bump when a shipped picture changes: the image optimizer caches by URL.
V = "v1"
# The take of each painting that ships (the original's name after "gpt25-").
TAKES = {
    "word": "word-v1",
    "B": "letter-b-v1",
    "i": "letter-i-v1",
    "G": "letter-g-v1",
    "H": "letter-h-v1",
    "band": "band-v1",
    "pool": "pool-v1",
    "rings": "rings-v1",
    "dots": "dots-v1",
}
# The shared rice-paper tile, aged a little for this page (warmer, never dirty).
TINT = (247, 239, 226)


def load(take):
    return Image.open(ORIG / f"gpt25-{take}.png").convert("RGB")


def divided(img):
    """Paper -> white, ink kept. The paper colour is the median of the picture's outer frame."""
    arr = np.asarray(img).astype(np.float32)
    h, w, _ = arr.shape
    fh, fw = max(h // 20, 1), max(w // 20, 1)
    frame = np.concatenate(
        [arr[:fh].reshape(-1, 3), arr[-fh:].reshape(-1, 3), arr[:, :fw].reshape(-1, 3), arr[:, -fw:].reshape(-1, 3)]
    )
    paper = np.median(frame, axis=0)
    return Image.fromarray(np.clip(arr / paper * 255.0, 0, 255).astype(np.uint8))


def ink_box(arr, level=236, pad=0.04):
    """The box around the ink on a divided picture (any channel under `level`), padded by `pad` of
    its size; stray specks outside the 0.1-99.9 percentiles are ignored."""
    h, w, _ = arr.shape
    ys, xs = np.nonzero(arr.min(axis=2) < level)
    if not len(xs):
        raise SystemExit("no ink found")
    x0, x1 = np.percentile(xs, [0.1, 99.9])
    y0, y1 = np.percentile(ys, [0.1, 99.9])
    pw, ph = (x1 - x0) * pad, (y1 - y0) * pad
    return int(max(0, x0 - pw)), int(max(0, y0 - ph)), int(min(w, x1 + pw)), int(min(h, y1 + ph))


def gold_pixels(arr):
    """Gold leaf: warm, clearly saturated, bright enough (the test ba.gold_mask uses)."""
    a = arr.astype(np.float32) / 255
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    hi, lo = a.max(axis=2), a.min(axis=2)
    sat = (hi - lo) / np.maximum(hi, 1e-4)
    warm = (r >= g) & (g > b)
    hue = np.where(warm, 60 * (g - b) / np.maximum(hi - lo, 1e-4), 0)
    return warm & (hue > 22) & (hue < 60) & (sat > 0.3) & (hi > 0.3)


def split_dot(img):
    """Lift the gold-leaf dot out of a painting. Returns (painting with paper where the dot was,
    the dot as a gold-leaf cut-out, the cut-out's box in the painting)."""
    arr = np.asarray(img)
    mask = cv2.morphologyEx(gold_pixels(arr).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(mask, 8)
    if n < 2:
        raise SystemExit("no gold dot found")
    i = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    x, y, w, h = (int(v) for v in st[i, :4])
    blob = cv2.dilate((lab == i).astype(np.uint8) * 255, np.ones((15, 15), np.uint8))
    clean = cv2.inpaint(arr, blob, 7, cv2.INPAINT_TELEA)
    m = int(max(w, h) * 0.25)
    box = (max(0, x - m), max(0, y - m), min(arr.shape[1], x + w + m), min(arr.shape[0], y + h + m))
    return Image.fromarray(clean), ba.leaf(img.crop(box)), box


def art_of(img, name, width):
    """Save a picture through ba.save and describe it as it ships (its size after the resize)."""
    ba.save(img, name, width, 86)
    s = min(1.0, width / img.width) if width else 1.0
    return {"src": f"{URL}/{name}.webp", "width": round(img.width * s), "height": round(img.height * s)}


def painting(key, name, width, with_dot=False):
    """A painting cropped to its ink (and its gold dot, kept in its own picture)."""
    img = load(TAKES[key])
    if with_dot:
        img, dot, dbox = split_dot(img)
    flat = divided(img)
    x0, y0, x1, y1 = ink_box(np.asarray(flat))
    if with_dot:
        x0, y0, x1, y1 = min(x0, dbox[0]), min(y0, dbox[1]), max(x1, dbox[2]), max(y1, dbox[3])
    crop = flat.crop((x0, y0, x1, y1))
    art = art_of(crop, f"{name}-{V}", width)
    if with_dot:
        ba.save(dot, f"{name}-dot-{V}", None, 88)
        art["dot"] = {
            "src": f"{URL}/{name}-dot-{V}.webp",
            "width": dot.width,
            "height": dot.height,
            "left": round((dbox[0] - x0) / crop.width, 4),
            "top": round((dbox[1] - y0) / crop.height, 4),
            "size": round((dbox[2] - dbox[0]) / crop.width, 4),
        }
    return art


def dots_sheet():
    """The four watercolor dots, from one painting: the four largest marks, left to right."""
    flat = divided(load(TAKES["dots"]))
    arr = np.asarray(flat)
    marks = cv2.morphologyEx((arr.min(axis=2) < 242).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    n, _, st, _ = cv2.connectedComponentsWithStats(marks, 8)
    big = sorted(range(1, n), key=lambda i: -st[i, cv2.CC_STAT_AREA])[:4]
    if len(big) < 4:
        raise SystemExit(f"found {len(big)} dots, want 4")
    out = []
    for k, i in enumerate(sorted(big, key=lambda i: st[i, 0]), 1):
        x, y, w, h = (int(v) for v in st[i, :4])
        m = int(max(w, h) * 0.18)
        crop = flat.crop((max(0, x - m), max(0, y - m), min(arr.shape[1], x + w + m), min(arr.shape[0], y + h + m)))
        out.append(art_of(crop, f"dot-{k}-{V}", 360))
    return out


def paper_aged():
    """The shared paper tile multiplied by TINT (a constant, so it still repeats without a seam)."""
    tile = np.asarray(Image.open(REPO / "public/images/home-v2/ink/paper.webp").convert("RGB")).astype(np.float32)
    aged = np.clip(tile * (np.array(TINT, np.float32) / 255), 0, 255).astype(np.uint8)
    ba.save(Image.fromarray(aged), f"paper-aged-{V}", 1600, 80)
    median = np.median(aged.reshape(-1, 3), axis=0).astype(int)
    print("paper-aged median: #%02x%02x%02x  (about-letter.module.css --paper)" % tuple(median))
    return f"{URL}/paper-aged-{V}.webp"


def wipe(width=1536, height=256, seed=11):
    """The brush wipe the letters are written through: opaque on the left 36%, transparent on the
    right 36%, and between them a dry brush's ragged edge (each row ends at its own place, a few
    bristles run ahead). At mask-size 300% 100%, moving it from 100% to 0% writes left to right."""
    rng = np.random.default_rng(seed)
    xs = np.arange(width, dtype=np.float32) / width
    rows = np.arange(height, dtype=np.float32) / height
    wobble = sum(np.sin(rows * np.pi * f + rng.uniform(0, 6.28)) / f for f in (2, 5, 11, 23))
    edge = 0.5 + 0.035 * wobble + rng.random(height).astype(np.float32) ** 6 * 0.06
    alpha = np.clip((edge[:, None] - xs[None, :]) / 0.03 + 0.5, 0, 1)
    alpha[:, : int(width * 0.36)] = 1
    alpha[:, int(width * 0.64) :] = 0
    a = Image.fromarray((alpha * 255).astype(np.uint8), "L")
    OUT.mkdir(parents=True, exist_ok=True)
    Image.merge("RGBA", (a, a, a, a)).save(OUT / f"wipe-{V}.png", optimize=True)
    print(f"public/images/about-ink/wipe-{V}.png")
    return f"{URL}/wipe-{V}.png"


def write_ts(entries):
    head = [
        "// Generated by reference/ink-pages/about/build_about.py. Do not edit by hand: change the",
        "// script (or its TAKES) and run it again. The About page's paintings (Mo's design D, October 6,",
        "// 2026): GPT Image 2.5 on rice paper, the paper divided out so each multiplies onto the page's",
        "// own paper; gold leaf as cut-out pictures (the dots of the i) and as a light mask (the rings).",
        "",
        "export type Art = { src: string; width: number; height: number };",
        "/** A gold-leaf dot: its own picture, placed by fractions of its painting's width and height. */",
        "export type Dot = Art & { left: number; top: number; size: number };",
        "",
    ]
    body = [f"export const {name} = {json.dumps(value, indent=2)} as const;\n" for name, value in entries]
    TS.write_text("\n".join(head) + "\n".join(body), encoding="utf-8", newline="\n")
    print(TS.relative_to(REPO))


if __name__ == "__main__":
    rings = painting("rings", "rings", 1400)
    ba.gold_mask(f"rings-{V}", sat_from=0.3)
    rings["gold"] = f"{URL}/rings-{V}-gold.webp"
    write_ts(
        [
            ("paperAged", paper_aged()),
            ("wipe", wipe()),
            ("word", painting("word", "word", 1800, with_dot=True)),
            (
                "letters",
                {
                    "B": painting("B", "letter-b", 900),
                    "i": painting("i", "letter-i", 700, with_dot=True),
                    "G": painting("G", "letter-g", 900),
                    "H": painting("H", "letter-h", 1100),
                },
            ),
            ("band", painting("band", "band", 2400)),
            ("pool", painting("pool", "pool", 1200)),
            ("rings", rings),
            ("dots", dots_sheet()),
        ]
    )
```

- [ ] **Step 7: Write the check script (it fails before the build runs)**

Create `reference/ink-pages/about/check_art.py`:

```python
"""Check the About page's built paintings (build_about.py): every picture letter-art.ts names
exists at its stated size; ink pictures have white paper at their corners (they multiply);
the gold dots are cut-outs with real transparency; the word and the i keep no gold in their ink
picture (the dot is its own picture); the rings' gold mask covers a thin ring; four dots, deep
to pale; the letters are sharp enough for their largest size on a 2x screen.

usage: python -X utf8 reference/ink-pages/about/check_art.py   (exit 0 when all pass)
"""

import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[3]
TS = (REPO / "src/components/about/letter-art.ts").read_text(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_about import gold_pixels  # noqa: E402

results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"{'PASS' if ok else 'FAIL'} {name}{(' — ' + str(detail)) if detail and not ok else ''}")


def file_of(src):
    return REPO / "public" / src.lstrip("/")


# Prettier unquotes the generated object's keys, so a key may or may not be in quotes.
srcs = re.findall(r'"?src"?:\s*"([^"]+)"', TS) + re.findall(r'"(/images/about-ink/[^"]+)"', TS)
missing = sorted({s for s in srcs if not file_of(s).exists()})
check("every picture letter-art.ts names exists", not missing, missing)

for src, w, h in re.findall(r'"?src"?:\s*"([^"]+)",\s*"?width"?:\s*(\d+),\s*"?height"?:\s*(\d+)', TS):
    if file_of(src).exists():
        size = Image.open(file_of(src)).size
        check(f"{src} is {w}x{h}", size == (int(w), int(h)), size)

for name in ["word", "letter-b", "letter-i", "letter-g", "letter-h", "band", "pool", "rings", "dot-1", "dot-4"]:
    p = REPO / f"public/images/about-ink/{name}-v1.webp"
    if p.exists():
        a = np.asarray(Image.open(p).convert("RGB")).astype(int)
        corners = [a[:8, :8], a[:8, -8:], a[-8:, :8], a[-8:, -8:]]
        check(f"{name}: paper divided out (corners white)", min(c.mean() for c in corners) >= 248, [round(c.mean()) for c in corners])

for name in ["word-dot", "letter-i-dot"]:
    p = REPO / f"public/images/about-ink/{name}-v1.webp"
    if p.exists():
        alpha = np.asarray(Image.open(p).convert("RGBA"))[..., 3]
        check(f"{name}: a gold cut-out with transparency", (alpha < 20).mean() > 0.2 and (alpha > 200).mean() > 0.05, [round((alpha < 20).mean(), 2), round((alpha > 200).mean(), 2)])

for name in ["word", "letter-i"]:
    p = REPO / f"public/images/about-ink/{name}-v1.webp"
    if p.exists():
        left = gold_pixels(np.asarray(Image.open(p).convert("RGB"))).mean()
        check(f"{name}: no gold left in the ink picture", left < 0.0002, left)

gold = REPO / "public/images/about-ink/rings-v1-gold.webp"
if gold.exists():
    cover = (np.asarray(Image.open(gold).convert("RGBA"))[..., 3] > 128).mean()
    check("rings: the gold mask is a thin ring (0.3%-12% of the picture)", 0.003 <= cover <= 0.12, round(cover, 4))

tones = []
for k in range(1, 5):
    p = REPO / f"public/images/about-ink/dot-{k}-v1.webp"
    if p.exists():
        a = np.asarray(Image.open(p).convert("L")).astype(int)
        tones.append(np.percentile(a, 5))
check("four dots, deep to pale", len(tones) == 4 and all(x < y for x, y in zip(tones, tones[1:])), tones)

for name, least in [("letter-b", 520), ("letter-i", 520), ("letter-g", 520), ("letter-h", 640)]:
    p = REPO / f"public/images/about-ink/{name}-v1.webp"
    if p.exists():
        check(f"{name}: at least {least}px tall (sharp on a 2x screen)", Image.open(p).height >= least, Image.open(p).size)

print(f"\n{sum(results)}/{len(results)} passed")
sys.exit(0 if all(results) else 1)
```

Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/reference/ink-pages/about/check_art.py`
Expected: it stops with `FileNotFoundError` for `letter-art.ts` (nothing built yet).

- [ ] **Step 8: Build, then check**

Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/reference/ink-pages/about/build_about.py`
Expected: one line per picture written (`public/images/about-ink/…  WxH  N KB`), a `rings-v1-gold.webp … gold N%` line, `paper-aged median: #……`, and `src/components/about/letter-art.ts`. Note the paper median: Task 3 uses it.

Then: `npx --prefix C:/Users/mcbig/Documents/codes/bigh-ink prettier --write C:/Users/mcbig/Documents/codes/bigh-ink/src/components/about/letter-art.ts`

Then run the check script again. Expected: `N/N passed`. If "four dots, deep to pale" or the gold checks fail, look at the pictures: a retake (Step 5) is the fix, not loosening the check. If `split_dot` picked something other than the dot, look at `plates/word-v1.png` and `plates/word-dot-v1.png`.

- [ ] **Step 9: Look at the built pictures**

Read `reference/ink-pages/about/plates/word-v1.png`, `letter-i-v1.png`, `word-dot-v1.png`, `rings-v1.png` and `band-v1.png` at full size. Expected: the word and the i show no grey smudge where the dot was lifted (if one shows, the inpaint mask is too small: raise the dilate kernel in `split_dot` from 15 to 21 and build again); the crops keep every stroke whole.

- [ ] **Step 10: Commit**

```bash
git -C C:/Users/mcbig/Documents/codes/bigh-ink add reference/ink-pages/about reference/ink-pages/spend.md public/images/about-ink src/components/about/letter-art.ts
git -C C:/Users/mcbig/Documents/codes/bigh-ink commit -m "feat(about): paintings for the folded letter

The written name, the four chapter letters, the watercolor band, the pool,
the tree rings with one gold ring and four dots (GPT Image 2.5), built by
build_about.py into web pictures and letter-art.ts.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 2: InkPage without a brush line, with a root class

**Files:**

- Modify: `src/components/ink/ink-page.tsx` (props and the last line of the JSX)

**Interfaces:**

- Produces: `InkPage({ current, route?, className?, children })`. `route` omitted renders no `BrushLine`; `className` is added to the root `div` beside the kit's `look` class. The homepage and the product pages keep passing `route` and nothing else changes for them.

- [ ] **Step 1: Confirm the homepage gate passes before the change**

Start the dev server (`preview_start {name: "bigh-ink"}`, or in the background: `npm --prefix C:/Users/mcbig/Documents/codes/bigh-ink run dev -- --hostname localhost --port 3025`).
Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/scripts/qa/home_snapshot.py compare http://localhost:3025 letter-t2-before baseline-nav`
Expected: `PASS`. If it fails before any change, stop and report: the baseline is stale, not your change.

- [ ] **Step 2: Change the props**

In `src/components/ink/ink-page.tsx` replace the function's signature (from `export function InkPage({` down to the line `}) {`) with:

```tsx
export function InkPage({
  current,
  route,
  className = "",
  children,
}: {
  current: Current;
  /**
   * The page's brush route for each layout. Pass a stable reference (a module-level function):
   * the brush layer is rebuilt whenever the route's identity changes. Leave it out for a page
   * without a brush line (About's folded letter: its folds divide the page).
   */
  route?: (layout: Layout) => Waypoint[];
  /** A class for the page's root, for a page that dresses the shared paper (About ages it). */
  className?: string;
  /** The page's sections; given whether motion is allowed. */
  children: (motion: boolean) => ReactNode;
}) {
```

and the root `div` opening tag becomes:

```tsx
    <div
      ref={root}
      className={className ? `${styles.look} ${className}` : styles.look}
      data-look="ink"
      data-page={current}
    >
```

and the last child becomes:

```tsx
{
  route ? <BrushLine motion={motion} route={route} /> : null;
}
```

Also change the comment above the function from "and the page's own brush line drawing itself down the page" to "and, where the page has one, its own brush line drawing itself down the page".

- [ ] **Step 3: Type-check and lint**

Run: `npx --prefix C:/Users/mcbig/Documents/codes/bigh-ink tsc --noEmit -p C:/Users/mcbig/Documents/codes/bigh-ink`
Expected: no errors.
Run: `npm --prefix C:/Users/mcbig/Documents/codes/bigh-ink run lint`
Expected: no errors in `ink-page.tsx`.

- [ ] **Step 4: Run the homepage gate**

Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/scripts/qa/home_snapshot.py compare http://localhost:3025 letter-t2 baseline-nav` → Expected: `PASS`.
Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/scripts/qa/qa_home_ink.py http://localhost:3025` → Expected: the last line reads `N/N passed` (all pass).

- [ ] **Step 5: Commit**

```bash
git -C C:/Users/mcbig/Documents/codes/bigh-ink add src/components/ink/ink-page.tsx
git -C C:/Users/mcbig/Documents/codes/bigh-ink commit -m "feat(ink): InkPage takes an optional brush route and a root class

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: The folded letter, still (layout, paper, folds, every size)

**Files:**

- Rewrite: `scripts/qa/qa_about.py` (new checks first)
- Rewrite: `src/components/about/about-ink.tsx`
- Create: `src/components/about/chapter-word.tsx`
- Create: `src/components/about/about-letter.module.css`
- Delete: `src/components/about/about-ink.module.css`, `src/components/about/about-route.ts`
- Modify: `src/components/about/about-content.ts` (the header comment only)

**Interfaces:**

- Consumes: `letter-art.ts` (Task 1), `InkPage` with `className` and no `route` (Task 2), `Acronym` (`./acronym`, props `className`, `id`, `delay`), `CountUp` (`./count-up`, props `to`, `suffix`, `className`), `Greetings` (`./greetings`, prop `className`), `liu` from `@/components/home-v2/look-ink/assets`, kit classes from `@/components/ink/ink.module.css` (`wrap`, `ink`, `display`, `label`, `body`, `caption`, `pill`, `pillGhost`, `gold`).
- Produces (QA hooks, used by Tasks 4-6): `[data-sheet]` (the sheet), `[data-part="purpose"|"roots"|"good"|"closing"]` (each part, with its fold across), `[data-chapter="B"|"i"|"G"|"H"]` (chapter word root; its painting is its first `img`; the i's dot has `[data-dot]`), `[data-word]` (the opening's written name; its painting is its first `img`; its dot `[data-dot]`), `[data-band]`, `[data-label]` (each part's label), `[data-print]` / `[data-mount]` / `[data-pool]` (Dr. Liu), `[data-rings]`, `[data-promise]` (each promise `li`). Section ids stay: `purpose`, `roots`, `experience`, `promise`, `closing`; headings `#<id>-title`.
- Produces: `ChapterWord({ initial: "B" | "i" | "G" | "H"; rest: string; size?: "chapter" | "closing"; className?: string })`, exported `RINGS_ALT` string from `about-ink.tsx`.

- [ ] **Step 1: Write the new QA file**

Replace `scripts/qa/qa_about.py` with:

```python
"""QA for the About page, "The name, on a folded letter" (Mo approved design D on October 6, 2026;
mockup reference/ink-pages/mockups/about-d.png; spec docs/superpowers/specs/2026-10-05-ink-pages-design.md).

desktop_and_phone (1440x900, 390x844): answers 200; no console errors or warnings (except the built
site's link-prefetch CSS note, PREFETCH_CSS); no failed requests; one h1, English "Be in Good
Health." with lang="en"; every locked line on the page; no canvas and no brush layer; every painting
multiplies onto the paper; the page wears the aged paper; the menu bar marks About (bar and narrow
menu), has no Home link, and its Products drop-down holds the five products and "Explore our
products."; no sideways scrolling; text 15px+, navigation 18px+, targets 48px+; the four chapter
words B, i, G, H, hidden from screen readers, in English, their paintings loaded; the written name
loads eagerly and is preloaded; the Support and Ask sheets open, close and hand focus back.
letter_layout (1440x900, 1280x800, 1024x768, 768x1024, 390x844): the middle fold from 900px up
(centred within 2px), none below; four folds across; on two columns Be's letter left and words
right, in's words left and letter and portrait right, Good's letter and rings left and words right,
each 24px or more clear of the middle fold; the promise heading centred; four promises in one row
from 1200px, two by two below that, one column on one column; the closing centred; the closing H
24px or more above its heading; no words over a painting; Dr. Liu's photo in the middle of its pool;
the rings carry "Illustration". On one column each part's chapter word stands over its label, over
its heading.
focus: Skip to content puts focus at the words; with pictures blocked every heading and paragraph
is visible.
boundary (899x900, 900x900): no sideways scrolling; the middle fold shows at 900 only; at 900 no
words cross it.
first_screen (1280x720, 1440x900, 1536x864, 390x844): the written name and the title in the first
screen; from 900px the band starts in it too.

Pictures: scripts/qa/out/about-letter/<size>-NN.png (viewport shots while scrolling).

Usage: python -X utf8 scripts/qa/qa_about.py [base-url] [--only=desktop_and_phone,letter_layout,focus,boundary,first_screen]
"""

import os
import re
import sys

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = ARGS[0] if ARGS else "http://localhost:3025"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "about-letter")
os.makedirs(OUT, exist_ok=True)
results = []

# The locked words (src/components/about/about-content.ts), as they appear on the page.
LOCKED = [
    "What our name stands for.",
    "What our work is for.",
    "Our purpose",
    "A full life has many parts.",
    "We focus on one you can’t see: your cells.",
    "Our mission is to support cellular health and mental energy, helping people live life to the fullest.",
    "Our scientific roots",
    "Our key formulas begin with scientists.",
    "Dr. Jiankang Liu, our Chief Scientific Advisor, studies mitochondria and aging. He formulated NuriCell, and with Dr. Iris Wang, he developed Nature Calm.",
    "Meet our scientists",
    "Our experience",
    "Our flagship formula is older than BiGH.",
    "scientific papers by Dr. Liu",
    "BiGH founded in California",
    "NuriCell’s formula, unchanged",
    "Our promise",
    "What you can count on.",
    "Made in California.",
    "By GMP-certified manufacturers.",
    "Know where it comes from.",
    "Our green propolis comes only from Minas Gerais, Brazil.",
    "45 days to decide.",
    "Not right for you? Send it back for a refund.",
    "Answers in your language.",
    "We reply in the language you write in.",
    "Curious about the science?",
    "Ask BiGH Science. We help you explore the research, with guidance from the scientists we work with.",
    "Ask BiGH Science",
    "Explore our products",
]


def check(name, ok, detail=""):
    results.append((name, bool(ok)))
    print(f"{'PASS' if ok else 'FAIL'} {name}{(' — ' + str(detail)) if detail and not ok else ''}")


# One warning is not counted, and only on the built site: Chrome's note that a stylesheet of
# ANOTHER route was preloaded and not used (Next's <Link> prefetch adds <link rel="preload"
# as="style"> for each linked route's CSS; with the router's prefetch blocked it never appears).
# Only this exact message for a /_next/static/*.css file is ignored.
PREFETCH_CSS = re.compile(
    r"^The resource \S+/_next/static/\S+\.css was preloaded using link preload but not used "
    r"within a few seconds from the window's load event\."
)


def counted(message):
    return message.type != "warning" or not PREFETCH_CSS.match(message.text)


def open_page(browser, width, height, path="/about", reduced=False, block_images=False):
    context = browser.new_context(
        viewport={"width": width, "height": height},
        reduced_motion="reduce" if reduced else "no-preference",
    )
    page = context.new_page()
    errors, failed = [], []
    page.on(
        "console",
        lambda m: errors.append(m.text) if m.type in ("error", "warning") and counted(m) else None,
    )
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("requestfailed", lambda r: failed.append(r.url))
    if block_images:
        page.route("**/*.{webp,png,jpg,jpeg,avif}", lambda route: route.abort())
        page.route("**/_next/image**", lambda route: route.abort())
    response = page.goto(f"{BASE}{path}", wait_until="networkidle", timeout=120000)
    page.evaluate("document.fonts.ready.then(() => true)")
    page.wait_for_timeout(1200)
    return context, page, response, errors, failed


def shots(page, tag, height):
    total = page.evaluate("document.documentElement.scrollHeight")
    y, i = 0, 0
    while y < total:
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(900)
        page.screenshot(path=os.path.join(OUT, f"{tag}-{i:02d}.png"))
        y += height
        i += 1


def scroll_through(page, step=450, pause=250):
    """Read to the end like a visitor (lazy pictures load, arrivals fire), then back to the top."""
    total = page.evaluate("document.documentElement.scrollHeight")
    for y in range(0, total, step):
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(pause)
    page.wait_for_timeout(800)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(400)


# The folds: the middle one is the sheet's ::before (from 900px), each part's fold across is its
# own ::before. The page's middle is the document's (scrollbar excluded).
FOLDS_JS = """() => {
  const sheet = document.querySelector('[data-sheet]');
  const v = getComputedStyle(sheet, '::before');
  const sb = sheet.getBoundingClientRect();
  const shown = v.content !== 'none' && v.display !== 'none';
  return { middle: shown, centre: shown ? sb.left + parseFloat(v.left) + parseFloat(v.width) / 2 : null,
           mid: document.documentElement.clientWidth / 2,
           across: [...document.querySelectorAll('[data-part]')].filter(p => getComputedStyle(p, '::before').content !== 'none').length };
}"""

# Each side's horizontal extent: the union of the matched boxes.
SIDES_JS = """() => {
  const side = (sel) => { const b = [...document.querySelectorAll(sel)].filter(e => e.offsetParent).map(e => e.getBoundingClientRect());
    return b.length ? { left: Math.min(...b.map(x => x.left)), right: Math.max(...b.map(x => x.right)) } : null; };
  return { mid: document.documentElement.clientWidth / 2,
    purposeLetter: side('#purpose [data-chapter]'), purposeWords: side('#purpose [data-label], #purpose h2, #purpose p'),
    rootsWords: side('#roots [data-label], #roots h2, #roots p, #roots a'), rootsLetter: side('#roots [data-chapter]'), rootsPrint: side('#roots [data-mount]'),
    goodLetter: side('#experience [data-chapter]'), goodRings: side('#experience [data-rings] img'), goodWords: side('#experience [data-label], #experience h2, #experience dl') };
}"""

# Words over paintings: glyph rectangles of the page's words (not the chapter words' own letters)
# against the boxes of the paintings that are not meant to sit under words (the pool is: Dr. Liu's
# print rests on it).
OVERLAP_JS = """() => {
  const words = [...document.querySelectorAll('main h1, main h2, main h3, main p, main dt, main dd, main a, main button, main figcaption')]
    .filter(e => e.offsetParent && !e.closest('[data-chapter], [data-word]'));
  const art = [...document.querySelectorAll('[data-chapter] img, [data-word] img, [data-rings] img, [data-band], [data-promise] img')].filter(e => e.offsetParent);
  const hits = [];
  for (const w of words) {
    const range = document.createRange(); range.selectNodeContents(w);
    const rects = [...range.getClientRects()].filter(r => r.width > 1);
    for (const a of art) {
      const b = a.getBoundingClientRect();
      if (rects.some(r => r.left < b.right - 2 && r.right > b.left + 2 && r.top < b.bottom - 2 && r.bottom > b.top + 2))
        hits.push([w.textContent.trim().slice(0, 24), (a.getAttribute('src') || a.tagName).slice(-32)]);
    }
  }
  return hits;
}"""

# Words crossing the middle fold, in the two-sided parts (from 900px): glyph rectangles that come
# within 24px of the page's middle.
CREASE_JS = """() => {
  const mid = document.documentElement.clientWidth / 2;
  const out = [];
  for (const el of document.querySelectorAll('#purpose [data-label], #purpose h2, #purpose p, #roots [data-label], #roots h2, #roots p, #roots a, #experience [data-label], #experience h2, #experience dt, #experience dd')) {
    if (!el.offsetParent) continue;
    const range = document.createRange(); range.selectNodeContents(el);
    for (const r of range.getClientRects()) {
      if (r.width > 1 && r.left < mid + 24 && r.right > mid - 24) { out.push([el.textContent.trim().slice(0, 20), Math.round(r.left), Math.round(r.right), Math.round(mid)]); break; }
    }
  }
  return out;
}"""


def desktop_and_phone(browser):
    for width, height in [(1440, 900), (390, 844)]:
        tag = f"{width}x{height}"
        context, page, response, errors, failed = open_page(browser, width, height)
        check(f"{tag} answers 200", response.status == 200, response.status)
        text = page.evaluate("document.body.innerText")
        missing = [line for line in LOCKED if line not in text]
        check(f"{tag} every locked line", not missing, missing)
        h1 = page.evaluate(
            "[...document.querySelectorAll('h1')].map(h => [h.getAttribute('aria-label') || h.textContent.trim(), h.lang])"
        )
        check(f"{tag} one English h1", h1 == [["Be in Good Health.", "en"]], h1)
        check(f"{tag} no canvas in the page", page.evaluate("document.querySelectorAll('main canvas').length") == 0)
        check(f"{tag} no brush layer", page.evaluate("!document.querySelector('[data-lifts]')"))
        blends = page.evaluate(
            "[...document.querySelectorAll('main img')].filter(i => !i.closest('[data-mount]') && !i.matches('[data-dot]')).map(i => getComputedStyle(i).mixBlendMode)"
        )
        check(f"{tag} paintings multiply", blends and all(b == "multiply" for b in blends), blends)
        paper = page.evaluate("getComputedStyle(document.querySelector('[data-look=\"ink\"]')).backgroundImage")
        check(f"{tag} the aged paper", "paper-aged" in paper, paper)
        chapters = page.evaluate(
            "[...document.querySelectorAll('[data-chapter]')].map(c => [c.dataset.chapter, c.getAttribute('aria-hidden'), c.lang])"
        )
        check(
            f"{tag} four chapter words, hidden from screen readers, in English",
            chapters == [["B", "true", "en"], ["i", "true", "en"], ["G", "true", "en"], ["H", "true", "en"]],
            chapters,
        )
        eager = page.evaluate(
            """(() => { const i = document.querySelector('[data-word] img');
                 const preload = [...document.querySelectorAll('link[rel=preload][as=image]')]
                   .some(l => ((l.getAttribute('imagesrcset') || '') + (l.getAttribute('href') || '')).includes('word-v'));
                 return { loading: i.getAttribute('loading'), preload }; })()"""
        )
        check(f"{tag} the written name loads eagerly and is preloaded", eager["loading"] != "lazy" and eager["preload"], eager)
        nav = page.evaluate(
            """() => { const n = document.querySelector('#site-navigation');
                 const sheet = document.querySelector('[data-nav-sheet]');
                 const panel = document.querySelector('[data-nav-panel="products"]');
                 const trigger = document.querySelector('[data-nav-trigger="products"]');
                 return { current: [...n.querySelectorAll('[aria-current="page"]')].map(a => a.textContent.trim()),
                          menuCurrent: [...sheet.querySelectorAll('[aria-current="page"]')].map(a => a.textContent.trim()),
                          home: [...document.querySelectorAll('header a')].filter(a => a.textContent.trim() === 'Home').length,
                          mark: n.querySelector('[data-nav-logo]')?.getAttribute('href') ?? null,
                          productsControls: trigger?.getAttribute('aria-controls') === panel?.id,
                          productPages: [...panel.querySelectorAll('a[href*="/products/"]')].length,
                          productsAll: [...panel.querySelectorAll('a')].map(a => a.getAttribute('href')).filter(h => h.endsWith('/#products')) }; }"""
        )
        check(f"{tag} header marks About", nav["current"] == ["About"] and nav["menuCurrent"] == ["About"], nav)
        check(f"{tag} no Home link; the mark goes home", nav["home"] == 0 and nav["mark"] == "/", nav)
        check(
            f"{tag} Products opens the five products and Explore goes home",
            nav["productsControls"] and nav["productPages"] == 5 and len(nav["productsAll"]) == 1,
            nav,
        )
        if width >= 1101:
            words = page.evaluate(
                "[...document.querySelectorAll('#site-navigation [data-nav-trigger], #site-navigation a[href$=\"/about\"], #site-navigation button')].filter(e => e.offsetParent && ['Products', 'Science', 'About', 'Support'].includes(e.textContent.trim())).map(e => [e.textContent.trim(), parseFloat(getComputedStyle(e).fontSize)])"
            )
            check(f"{tag} navigation at least 18px", len(words) == 4 and all(s >= 18 for _, s in words), words)
        sideways = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
        check(f"{tag} no sideways scrolling", sideways <= 0, sideways)
        small = page.evaluate(
            """[...document.querySelectorAll('main *')].filter(e => e.childNodes.length && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && e.offsetParent)
                 .map(e => [e.textContent.trim().slice(0, 30), parseFloat(getComputedStyle(e).fontSize)]).filter(([, s]) => s < 15)"""
        )
        check(f"{tag} text at least 15px", not small, small[:5])
        targets = page.evaluate(
            """[...document.querySelectorAll('main a, main button')].filter(e => e.offsetParent)
                 .map(e => [e.textContent.trim().slice(0, 30), Math.round(e.getBoundingClientRect().height)]).filter(([, h]) => h < 48)"""
        )
        check(f"{tag} targets at least 48px", not targets, targets)
        if width < 1101:
            page.click("[data-nav-menu-button]")
            page.wait_for_timeout(900)
            page.click("[data-nav-sheet] button:has-text('Support')")
        else:
            page.click("#site-navigation button:has-text('Support')")
        page.wait_for_timeout(900)
        check(f"{tag} Support sheet opens", page.evaluate("!!document.querySelector('dialog[open]')"))
        page.keyboard.press("Escape")
        page.wait_for_timeout(600)
        ask = page.locator("main button:has-text('Ask BiGH Science')")
        ask.scroll_into_view_if_needed()
        ask.click()
        page.wait_for_timeout(900)
        sheet = page.evaluate("document.querySelector('dialog[open]')?.innerText ?? ''")
        check(f"{tag} Ask sheet opens", "Ask BiGH Science" in sheet, sheet[:80])
        page.keyboard.press("Escape")
        page.wait_for_timeout(600)
        back = page.evaluate("document.activeElement?.textContent?.trim()")
        check(f"{tag} focus returns to Ask", back == "Ask BiGH Science", back)
        page.evaluate("window.scrollTo(0, 0)")
        shots(page, tag, height)
        loaded = page.evaluate(
            "[...document.querySelectorAll('[data-chapter] img, [data-word] img')].map(i => i.complete && i.naturalWidth > 0)"
        )
        check(f"{tag} every letter's painting loaded", loaded and all(loaded), loaded)
        check(f"{tag} no console errors or warnings", not errors, errors[:3])
        check(f"{tag} no failed requests", not failed, failed[:3])
        context.close()


def letter_layout(browser):
    for width, height in [(1440, 900), (1280, 800), (1024, 768), (768, 1024), (390, 844)]:
        tag = f"{width}x{height}"
        two = width >= 900
        context, page, response, errors, failed = open_page(browser, width, height, reduced=True)
        folds = page.evaluate(FOLDS_JS)
        if two:
            check(f"{tag} the middle fold, centred", folds["middle"] and abs(folds["centre"] - folds["mid"]) <= 2, folds)
        else:
            check(f"{tag} no middle fold on one column", not folds["middle"], folds)
        check(f"{tag} four folds across", folds["across"] == 4, folds)
        if two:
            s = page.evaluate(SIDES_JS)
            m = s["mid"]
            left_ok = lambda b: b is not None and b["right"] <= m - 24
            right_ok = lambda b: b is not None and b["left"] >= m + 24
            check(f"{tag} Be: letter left, words right", left_ok(s["purposeLetter"]) and right_ok(s["purposeWords"]), s)
            check(f"{tag} in: words left, letter and portrait right", left_ok(s["rootsWords"]) and right_ok(s["rootsLetter"]) and right_ok(s["rootsPrint"]), s)
            check(f"{tag} Good: letter and rings left, words right", left_ok(s["goodLetter"]) and left_ok(s["goodRings"]) and right_ok(s["goodWords"]), s)
        centred = page.evaluate(
            """() => { const mid = document.documentElement.clientWidth / 2;
                 const c = (sel) => { const b = document.querySelector(sel).getBoundingClientRect(); return Math.round(b.left + b.width / 2 - mid); };
                 return { promise: c('#promise-title'), closing: c('#closing-title'), closingWord: c('#closing [data-chapter]') }; }"""
        )
        check(
            f"{tag} the promise heading and the closing are centred",
            abs(centred["promise"]) <= 4 and abs(centred["closing"]) <= 4 and abs(centred["closingWord"]) <= 32,
            centred,
        )
        rows = page.evaluate("new Set([...document.querySelectorAll('[data-promise]')].map(li => Math.round(li.getBoundingClientRect().top / 4))).size")
        want = 1 if width >= 1200 else 2 if two else 4
        check(f"{tag} the promises in {want} row(s)", rows == want, rows)
        gap = page.evaluate(
            "document.querySelector('#closing-title').getBoundingClientRect().top - document.querySelector('#closing [data-chapter] img').getBoundingClientRect().bottom"
        )
        check(f"{tag} clear paper under the closing H (24px or more)", gap >= 24, round(gap))
        hits = page.evaluate(OVERLAP_JS)
        check(f"{tag} no words over a painting", not hits, hits[:4])
        liu = page.evaluate(
            """() => { const p = document.querySelector('[data-pool]').getBoundingClientRect();
                 const f = document.querySelector('[data-mount] img').getBoundingClientRect();
                 return { dx: (f.left + f.width / 2 - p.left - p.width / 2) / p.width, dy: (f.top + f.height / 2 - p.top - p.height / 2) / p.height }; }"""
        )
        check(f"{tag} Dr. Liu's photo in the middle of its pool", abs(liu["dx"]) <= 0.15 and abs(liu["dy"]) <= 0.15, liu)
        caption = page.evaluate("document.querySelector('[data-rings] figcaption')?.textContent.trim()")
        check(f"{tag} the rings carry Illustration", caption == "Illustration", caption)
        if not two:
            order = page.evaluate(
                """() => ['purpose', 'roots', 'experience'].map(id => { const s = document.getElementById(id);
                     const t = (sel) => s.querySelector(sel).getBoundingClientRect().top;
                     return [id, t('[data-chapter]') < t('[data-label]') && t('[data-label]') < t('h2')]; })"""
            )
            check(f"{tag} one column: chapter word, then label, then heading", all(ok for _, ok in order), order)
        page.screenshot(path=os.path.join(OUT, f"layout-{tag}.png"), full_page=False)
        context.close()


def focus(browser):
    context, page, response, errors, failed = open_page(browser, 1440, 900)
    page.keyboard.press("Tab")
    skip = page.evaluate("document.activeElement?.textContent?.trim()")
    page.keyboard.press("Enter")
    page.wait_for_timeout(300)
    where = page.evaluate("document.activeElement?.id")
    check("Skip to content puts focus at the words", skip == "Skip to content" and where == "main", [skip, where])
    context.close()
    context, page, response, errors, failed = open_page(browser, 1440, 900, block_images=True)
    scroll_through(page)
    hidden = page.evaluate(
        """[...document.querySelectorAll('main h1, main h2, main h3, main p')].filter(e => {
             let n = e; while (n) { if (parseFloat(getComputedStyle(n).opacity) < 0.05) return true; n = n.parentElement; } return false; })
           .map(e => e.textContent.trim().slice(0, 30))"""
    )
    check("pictures blocked: every heading and paragraph visible", not hidden, hidden[:5])
    context.close()


def boundary(browser):
    for width in (899, 900):
        context, page, response, errors, failed = open_page(browser, width, 900, reduced=True)
        sideways = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
        check(f"{width} no sideways scrolling", sideways <= 0, sideways)
        folds = page.evaluate(FOLDS_JS)
        check(f"{width} the middle fold {'shows' if width == 900 else 'is gone'}", folds["middle"] == (width == 900), folds)
        if width == 900:
            crossing = page.evaluate(CREASE_JS)
            check("900 no words cross the middle fold", not crossing, crossing[:3])
        context.close()


def first_screen(browser):
    for width, height in [(1280, 720), (1440, 900), (1536, 864), (390, 844)]:
        tag = f"{width}x{height}"
        context, page, response, errors, failed = open_page(browser, width, height, reduced=True)
        geo = page.evaluate(
            """() => ({ word: document.querySelector('[data-word] img').getBoundingClientRect().bottom,
                        title: document.querySelector('h1').getBoundingClientRect().bottom,
                        band: document.querySelector('[data-band]').getBoundingClientRect().top, win: innerHeight })"""
        )
        check(f"{tag} the written name and the title in the first screen", geo["word"] <= geo["win"] and geo["title"] <= geo["win"], geo)
        if width >= 900:
            check(f"{tag} the band starts in the first screen", geo["band"] < geo["win"], geo)
        context.close()


# --only=letter_layout,boundary runs just those groups (while working on one thing); the full run is the gate.
GROUPS = [desktop_and_phone, letter_layout, focus, boundary, first_screen]
ONLY = next((a.split("=", 1)[1].split(",") for a in sys.argv[1:] if a.startswith("--only=")), None)

with sync_playwright() as p:
    browser = p.chromium.launch(args=["--use-angle=d3d11"])
    for group in GROUPS:
        if ONLY is None or group.__name__ in ONLY:
            group(browser)
    browser.close()

passed = sum(ok for _, ok in results)
print(f"\n{passed}/{len(results)} passed")
sys.exit(0 if passed == len(results) else 1)
```

- [ ] **Step 2: Run it against the old page to see it fail**

Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/scripts/qa/qa_about.py http://localhost:3025 --only=letter_layout`
Expected: FAIL lines (no `[data-sheet]`: an evaluation error or `folds` failures). That is the point: the new page does not exist yet.

- [ ] **Step 3: Write the chapter word**

Create `src/components/about/chapter-word.tsx`:

```tsx
"use client";

import Image from "next/image";
import base from "@/components/ink/ink.module.css";
import { letters } from "./letter-art";
import styles from "./about-letter.module.css";

// A part's chapter word (October 6, 2026): its initial painted with the brush, the rest of the word
// in the page's type ("B" + "e"). Together they spell the brand's name, like the logo, so the word
// stays English in every language and is hidden from screen readers: the part's heading carries
// the meaning in the reader's language.
export function ChapterWord({
  initial,
  rest,
  size = "chapter",
  className = "",
}: {
  initial: keyof typeof letters;
  rest: string;
  /** "closing": the big H of Health, about the height of the written name. */
  size?: "chapter" | "closing";
  className?: string;
}) {
  const art = letters[initial];
  const dot = "dot" in art ? art.dot : null;
  return (
    <span
      className={`${styles.chapter} ${className}`}
      data-chapter={initial}
      data-size={size}
      lang="en"
      aria-hidden="true"
    >
      <span className={styles.initial}>
        <Image
          className={`${base.ink} ${styles.paint}`}
          src={art.src}
          alt=""
          width={art.width}
          height={art.height}
          sizes={
            size === "closing" ? "(max-width: 899px) 44vw, 300px" : "(max-width: 899px) 36vw, 240px"
          }
        />
        {dot ? (
          <Image
            className={styles.dot}
            src={dot.src}
            alt=""
            width={dot.width}
            height={dot.height}
            sizes="64px"
            data-dot=""
            style={{
              left: `${dot.left * 100}%`,
              top: `${dot.top * 100}%`,
              width: `${dot.size * 100}%`,
            }}
          />
        ) : null}
      </span>
      <span className={styles.rest}>{rest}</span>
    </span>
  );
}
```

- [ ] **Step 4: Rewrite the page**

Replace `src/components/about/about-ink.tsx` with:

```tsx
"use client";

import Image from "next/image";
import type { CSSProperties } from "react";
import { ArrowRight } from "lucide-react";
import { liu } from "@/components/home-v2/look-ink/assets";
import { useSiteDialogs } from "@/components/ink/dialogs";
import { InkPage } from "@/components/ink/ink-page";
import base from "@/components/ink/ink.module.css";
import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import { about, drafts, routes } from "./about-content";
import { Acronym } from "./acronym";
import { ChapterWord } from "./chapter-word";
import { CountUp } from "./count-up";
import { Greetings } from "./greetings";
import { band, dots, pool, rings, word } from "./letter-art";
import styles from "./about-letter.module.css";

// The About page, "The name, on a folded letter" (Mo approved design D on October 6, 2026; mockup
// reference/ink-pages/mockups/about-d.png; spec docs/superpowers/specs/2026-10-05-ink-pages-design.md).
// One sheet of slightly aged paper, folded like a letter and opened again: BiGH written by hand at
// the top, then one brushed letter opening each part (Be, in, Good, Health), the parts alternating
// sides of the middle fold. The words are the locked ones in about-content.ts. No brush line here:
// the folds divide the page (the brush line is the homepage's signature).

export const RINGS_ALT =
  "Tree rings in ink. A gold ring marks 2016, when BiGH began; the rings inside it are the years the formula is older.";

function sentences(text: string) {
  return text.match(/[^.!?。！？]+[.!?。！？]*\s*/gu)?.map((part) => part.trim()) ?? [text];
}

function Opening() {
  const copy = useCopy();
  return (
    <section className={styles.opening} aria-labelledby="about-title">
      <div className={`${base.wrap} ${styles.openingWords}`}>
        <span className={styles.word} data-word="" aria-hidden="true">
          <Image
            className={`${base.ink} ${styles.paint}`}
            src={word.src}
            alt=""
            width={word.width}
            height={word.height}
            sizes="(max-width: 899px) 86vw, min(50vw, 780px)"
            priority
          />
          <Image
            className={styles.dot}
            src={word.dot.src}
            alt=""
            width={word.dot.width}
            height={word.dot.height}
            sizes="64px"
            priority
            data-dot=""
            style={{
              left: `${word.dot.left * 100}%`,
              top: `${word.dot.top * 100}%`,
              width: `${word.dot.size * 100}%`,
            }}
          />
        </span>
        <p className={styles.kicker}>{copy(about.hero.label)}</p>
        <Acronym className={styles.title} />
        <p className={styles.lead}>
          {sentences(copy(about.hero.lead)).map((sentence) => (
            <span key={sentence}>{sentence}</span>
          ))}
        </p>
      </div>
      <Image
        className={`${base.ink} ${styles.band}`}
        src={band.src}
        alt=""
        width={band.width}
        height={band.height}
        sizes="100vw"
        data-band=""
        data-bloom="waiting"
      />
    </section>
  );
}

function Purpose() {
  const copy = useCopy();
  return (
    <section
      id="purpose"
      className={styles.part}
      data-part="purpose"
      aria-labelledby="purpose-title"
    >
      <div className={`${base.wrap} ${styles.grid}`}>
        <ChapterWord initial="B" rest="e" className={styles.areaLetter} />
        <div className={styles.areaWords}>
          <p className={`${base.label} ${styles.label}`} data-label="">
            {copy(about.purpose.label)}
          </p>
          <h2 id="purpose-title" className={`${base.display} ${styles.heading}`}>
            {about.purpose.lines.map((line) => (
              <span key={line}>{copy(line)}</span>
            ))}
          </h2>
          <p className={styles.body}>{copy(about.purpose.mission)}</p>
        </div>
      </div>
    </section>
  );
}

function Roots() {
  const copy = useCopy();
  return (
    <section id="roots" className={styles.part} data-part="roots" aria-labelledby="roots-title">
      <div className={`${base.wrap} ${styles.grid}`}>
        <ChapterWord initial="i" rest="n" className={styles.areaLetter} />
        <div className={styles.areaWords}>
          <p className={`${base.label} ${styles.label}`} data-label="">
            {copy(about.roots.label)}
          </p>
          <h2 id="roots-title" className={`${base.display} ${styles.heading}`}>
            {copy(about.roots.title)}
          </h2>
          <p className={styles.body}>{copy(about.roots.text)}</p>
          <Link
            href={routes.scientists}
            className={`${base.pill} ${base.pillGhost} ${styles.more}`}
          >
            {copy(about.roots.link)} <ArrowRight size={18} aria-hidden="true" />
          </Link>
        </div>
        <figure className={`${styles.print} ${styles.areaArt}`} data-print="">
          <Image
            className={`${base.ink} ${styles.pool}`}
            src={pool.src}
            alt=""
            width={pool.width}
            height={pool.height}
            sizes="(max-width: 899px) 90vw, 560px"
            data-pool=""
            data-bloom=""
          />
          <span className={styles.mount} data-mount="">
            <Image
              src={liu.src}
              alt={copy(about.roots.photo.alt)}
              width={liu.width}
              height={liu.height}
              sizes="(max-width: 899px) 220px, 260px"
            />
          </span>
        </figure>
      </div>
    </section>
  );
}

function Good() {
  const copy = useCopy();
  const years = copy(about.experience.stats[1].unit);
  return (
    <div className={styles.part} data-part="good">
      <section
        id="experience"
        className={`${base.wrap} ${styles.grid} ${styles.experience}`}
        aria-labelledby="experience-title"
      >
        <ChapterWord initial="G" rest="ood" className={styles.areaLetter} />
        <div className={styles.areaWords}>
          <p className={`${base.label} ${styles.label}`} data-label="">
            {copy(about.experience.label)}
          </p>
          <h2 id="experience-title" className={`${base.display} ${styles.heading}`}>
            {copy(about.experience.title)}
          </h2>
          <dl className={styles.figures}>
            <div>
              <dt>{copy(about.roots.stat.label)}</dt>
              <dd>
                <CountUp to={280} suffix="+" className={styles.figure} />
              </dd>
            </div>
            <div>
              <dt>{copy(about.experience.stats[0].label)}</dt>
              <dd>
                <span className={styles.figure}>{about.experience.stats[0].value}</span>
              </dd>
            </div>
            <div>
              <dt>{copy(about.experience.stats[1].label)}</dt>
              <dd>
                <CountUp to={20} suffix="+" className={styles.figure} />
                <span className={styles.unit}> {years}</span>
              </dd>
            </div>
          </dl>
        </div>
        <figure className={`${styles.rings} ${styles.areaArt}`} data-rings="">
          <span className={styles.ringsBody}>
            <Image
              className={base.ink}
              src={rings.src}
              alt={copy(RINGS_ALT)}
              width={rings.width}
              height={rings.height}
              sizes="(max-width: 899px) 70vw, 340px"
              data-bloom=""
            />
            <span className={base.gold} style={{ ["--gold" as string]: `url(${rings.gold})` }} />
          </span>
          <figcaption className={base.caption}>{copy(drafts.illustration)}</figcaption>
        </figure>
      </section>
      <section
        id="promise"
        className={`${base.wrap} ${styles.promise}`}
        aria-labelledby="promise-title"
      >
        <p className={`${base.label} ${styles.label}`} data-label="">
          {copy(about.promise.label)}
        </p>
        <h2 id="promise-title" className={`${base.display} ${styles.heading}`}>
          {copy(about.promise.title)}
        </h2>
        <ul className={styles.promises}>
          {about.promise.items.map((item, i) => (
            <li key={item.title} data-promise="">
              <Image
                className={`${base.ink} ${styles.promiseDot}`}
                src={dots[i].src}
                alt=""
                width={dots[i].width}
                height={dots[i].height}
                sizes="92px"
                data-bloom=""
                style={{ "--bloom-delay": i * 260 } as CSSProperties}
              />
              <h3>{copy(item.title)}</h3>
              <p>{copy(item.text)}</p>
              {i === 3 && <Greetings className={styles.greetings} />}
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}

function Closing() {
  const copy = useCopy();
  const dialogs = useSiteDialogs();
  return (
    <section
      id="closing"
      className={`${styles.part} ${styles.closing}`}
      data-part="closing"
      aria-labelledby="closing-title"
    >
      <div className={`${base.wrap} ${styles.pause}`}>
        <ChapterWord initial="H" rest="ealth" size="closing" />
        <h2 id="closing-title" className={`${base.display} ${styles.heading}`}>
          {copy(about.closing.title)}
        </h2>
        <p className={styles.body}>{copy(about.closing.text)}</p>
        <div className={styles.actions}>
          <button type="button" className={base.pill} onClick={dialogs.openAsk}>
            {copy(about.closing.primary)}
          </button>
          <Link href={routes.products} className={`${base.pill} ${base.pillGhost}`}>
            {copy(about.closing.secondary)}
          </Link>
        </div>
      </div>
    </section>
  );
}

export function AboutInk() {
  return (
    <InkPage current="about" className={styles.letterPage}>
      {() => (
        <div className={styles.sheet} data-sheet="">
          <Opening />
          <Purpose />
          <Roots />
          <Good />
          <Closing />
        </div>
      )}
    </InkPage>
  );
}
```

- [ ] **Step 5: Write the styles**

Create `src/components/about/about-letter.module.css` (use the paper median Task 1 printed for `--paper` and the body background if it differs from `#f0e4cf`):

```css
/* About, "The name, on a folded letter" (Mo approved design D on October 6, 2026; mockup
   reference/ink-pages/mockups/about-d.png). One sheet of slightly aged rice paper, folded like a
   letter and opened again: the folds divide the page (no brush line here). BiGH is written by hand
   at the top; each brushed letter opens one part, the parts alternating sides of the middle fold.
   Every rule is scoped under .letterPage (the page root, InkPage className), so it outranks the
   kit's .look rules and the homepage resets whatever order the built stylesheets load in.
   Multiply: the paintings blend with the root's paper, so nothing between them and the root may
   make a stacking context (no z-index on a positioned ancestor, no isolation, opacity, transform
   or filter on the sheet, a part, a grid or a figure). */

/* The paper, aged a little for this page: the shared tile multiplied warmer (build_about.py TINT).
   The header's paper reads --paper and --paper-fibre from here, so the bar settles on the same
   sheet. */
:global([data-look="ink"]).letterPage {
  --paper: #f0e4cf;
  --paper-fibre: url("/images/about-ink/paper-aged-v1.webp");
  --crease-shade: rgb(92 70 40 / 0.11);
  --crease-light: rgb(255 252 244 / 0.6);
  --fold-gap: clamp(64px, 8vw, 150px);
  --part-half: clamp(56px, 6vw, 112px);
  --letter: clamp(128px, 15vw, 250px);
  background-image: url("/images/about-ink/paper-aged-v1.webp");
}

:global(body):has(.letterPage) {
  background: #f0e4cf;
}

/* The sheet: its age (darker towards both sides, a few faint spots) and its middle fold. */
.letterPage .sheet {
  position: relative;
  background:
    radial-gradient(circle at 7% 18%, rgb(150 112 62 / 0.07), transparent 120px),
    radial-gradient(circle at 93% 41%, rgb(150 112 62 / 0.05), transparent 160px),
    radial-gradient(circle at 12% 67%, rgb(150 112 62 / 0.05), transparent 90px),
    radial-gradient(circle at 88% 86%, rgb(150 112 62 / 0.06), transparent 140px),
    linear-gradient(
      90deg,
      rgb(120 88 46 / 0.08),
      transparent 9%,
      transparent 91%,
      rgb(120 88 46 / 0.08)
    );
}

/* A fold is a soft shadow beside a thin highlight. z-index -1 puts it under the words and the
   paintings but over the root's paper (the root is the stacking context; nothing between it and
   the fold makes another). */
@media (min-width: 900px) {
  .letterPage .sheet::before {
    content: "";
    position: absolute;
    z-index: -1;
    top: 0;
    bottom: 0;
    left: calc(50% - 8px);
    width: 16px;
    pointer-events: none;
    background: linear-gradient(
      90deg,
      transparent,
      var(--crease-shade) 44%,
      var(--crease-light) 56%,
      transparent
    );
  }
}

.letterPage .part {
  position: relative;
  padding-block: var(--part-half);
  /* Deep links (/about#purpose): the part's first content lands 108px from the window's top, just
     under the settled bar; the document keeps 150px of scroll-padding-top (globals.css). */
  scroll-margin-top: calc(108px - 150px - var(--part-half));
}

.letterPage .part::before {
  content: "";
  position: absolute;
  z-index: -1;
  top: -8px;
  left: 0;
  right: 0;
  height: 16px;
  pointer-events: none;
  background: linear-gradient(
    180deg,
    transparent,
    var(--crease-shade) 44%,
    var(--crease-light) 56%,
    transparent
  );
}

/* ---- The opening: the written name, the title, the band ------------------------------------- */

/* The header floats over the opening (clear there), so the opening starts 88px down. */
.letterPage .opening {
  padding: calc(88px + clamp(24px, 3.4vw, 64px)) 0 var(--part-half);
  text-align: center;
}

.letterPage .openingWords {
  display: grid;
  justify-items: center;
}

.letterPage .word {
  position: relative;
  display: block;
  width: clamp(280px, 50vw, 780px);
  margin: 0 0 clamp(14px, 1.6vw, 28px);
}

.letterPage .paint {
  display: block;
  width: 100%;
  height: auto;
}

.letterPage .dot {
  position: absolute;
  max-width: none;
  height: auto;
}

.letterPage .kicker {
  margin: 0 0 10px;
  color: var(--muted);
  font-size: 19px;
  font-weight: 450;
}

/* The acronym: the four initials in sumi ink, the rest of each word ink-wash grey (3.4:1 on the
   aged paper, large text). */
.letterPage .title {
  --acronym-accent: var(--ink);
  margin: 0;
  color: #7f7a72;
  font-family: var(--display-font);
  font-weight: var(--display-weight);
  font-size: clamp(min(40px, 10.26vw), 4.2vw, 68px);
  line-height: 1.02;
  letter-spacing: -0.03em;
}

.letterPage .lead {
  margin: clamp(14px, 1.4vw, 22px) 0 0;
  color: var(--muted);
  font-size: clamp(19px, 1.5vw, 23px);
  line-height: 1.45;
}

.letterPage .lead span {
  display: block;
}

.letterPage .band {
  display: block;
  width: 100%;
  height: auto;
  margin-top: clamp(4px, 1vw, 16px);
}

/* ---- The parts: two sides of the middle fold ------------------------------------------------ */

.letterPage .grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  column-gap: var(--fold-gap);
  row-gap: clamp(28px, 3vw, 48px);
  align-items: center;
}

.letterPage .areaLetter {
  grid-area: letter;
}

.letterPage .areaWords {
  grid-area: words;
}

.letterPage .areaArt {
  grid-area: art;
}

.letterPage [data-part="purpose"] .grid {
  grid-template-areas: "letter words";
}

.letterPage [data-part="purpose"] .areaLetter {
  justify-self: center;
}

.letterPage [data-part="roots"] .grid {
  grid-template-areas:
    "words letter"
    "words art";
}

.letterPage [data-part="roots"] .areaLetter {
  justify-self: start;
  align-self: end;
}

.letterPage .experience {
  grid-template-areas:
    "letter words"
    "art words";
}

.letterPage .experience .areaLetter {
  justify-self: start;
  align-self: end;
}

/* The chapter word: the painted initial, then the rest of the word in the page's type, standing on
   the initial's baseline (the paintings' ink ends about 8% above their box's bottom). */
.letterPage .chapter {
  display: inline-flex;
  align-items: flex-end;
  line-height: 1;
}

.letterPage .initial {
  position: relative;
  display: block;
  height: var(--letter);
}

.letterPage .initial .paint {
  width: auto;
  height: 100%;
}

.letterPage .rest {
  margin: 0 0 calc(var(--letter) * 0.1) calc(var(--letter) * -0.02);
  font-family: var(--display-font);
  font-weight: var(--display-weight);
  font-size: calc(var(--letter) * 0.42);
  letter-spacing: -0.03em;
}

.letterPage .chapter[data-size="closing"] {
  --letter: clamp(170px, 19vw, 320px);
}

/* p.label: the kit's .look .label (margin 0) has the same weight as a plain .letterPage .label. */
.letterPage p.label {
  margin: 0 0 14px;
}

/* The parts' headings sit a step under the opening's title, as in the mockup. Qualified by its
   element so it outranks the kit's .look .display. */
.letterPage h2.heading {
  font-size: clamp(min(36px, 9.2vw), 3.2vw, 50px);
  line-height: 1.08;
}

.letterPage h2.heading > span {
  display: block;
}

.letterPage .body {
  max-width: 30em;
  margin: clamp(18px, 1.8vw, 28px) 0 0;
  color: var(--muted);
  font-size: 19px;
  line-height: 1.6;
}

.letterPage .more {
  margin-top: clamp(24px, 2.4vw, 36px);
}

/* ---- Dr. Liu: his real photograph on its paper mat, resting on a pool of grey wash ----------- */

.letterPage .print {
  --mat: clamp(200px, 15vw, 248px);
  position: relative;
  justify-self: center;
  width: var(--mat);
  margin: calc(var(--mat) * 0.25) 0;
}

.letterPage .pool {
  position: absolute;
  top: 50%;
  left: 50%;
  width: calc(var(--mat) * 2.1);
  max-width: none;
  height: auto;
  translate: -50% -50%;
  pointer-events: none;
}

/* The photo mount: the page's only shadow. */
.letterPage .mount {
  position: relative;
  display: block;
  width: 100%;
  padding: 12px;
  background: #fbf9f4;
  box-shadow:
    0 22px 44px -22px rgb(12 11 10 / 0.42),
    0 3px 8px rgb(12 11 10 / 0.1);
}

.letterPage .mount img {
  display: block;
  width: 100%;
  height: auto;
  aspect-ratio: 4 / 5;
  object-fit: cover;
  object-position: 50% 26%;
}

/* ---- Good: the rings and the figures --------------------------------------------------------- */

.letterPage .rings {
  justify-self: center;
  width: clamp(220px, 21vw, 340px);
  margin: 0;
}

.letterPage .ringsBody {
  position: relative;
  display: block;
}

.letterPage .ringsBody img {
  display: block;
  width: 100%;
  height: auto;
}

.letterPage .rings figcaption {
  margin-top: 8px;
  text-align: right;
}

.letterPage .figures {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: clamp(18px, 1.8vw, 28px);
  margin: clamp(28px, 3vw, 48px) 0 0;
}

/* Each figure stands on its hairline, its words under it. */
.letterPage .figures > div {
  display: flex;
  flex-direction: column-reverse;
  justify-content: flex-end;
}

.letterPage .figures dt {
  margin-top: 12px;
  padding-top: 10px;
  border-top: 1px solid var(--line);
  color: var(--muted);
  font-size: 17px;
  font-weight: 450;
  line-height: 1.4;
}

.letterPage .figures dd {
  margin: 0;
  white-space: nowrap;
}

.letterPage .figure {
  font-size: clamp(48px, 4.6vw, 76px);
  font-weight: 300;
  line-height: 1;
  letter-spacing: -0.03em;
  font-variant-numeric: tabular-nums;
}

.letterPage .unit {
  font-size: clamp(26px, 2.4vw, 38px);
  font-weight: 300;
  line-height: 1;
}

/* ---- Our promise: across both sides, four promises under four watercolor dots --------------- */

.letterPage .promise {
  margin-top: clamp(72px, 7vw, 130px);
  text-align: center;
  scroll-margin-top: calc(108px - 150px);
}

.letterPage .experience {
  scroll-margin-top: calc(108px - 150px);
}

.letterPage .promise h2.heading {
  margin-inline: auto;
}

.letterPage .promises {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: clamp(32px, 3vw, 48px) clamp(24px, 2.4vw, 40px);
  margin: clamp(36px, 3.4vw, 56px) 0 0;
  padding: 0;
  list-style: none;
}

.letterPage .promiseDot {
  display: block;
  width: clamp(64px, 5.6vw, 92px);
  height: auto;
  margin: 0 auto 18px;
}

.letterPage .promises h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 500;
  line-height: 1.3;
}

.letterPage .promises p {
  margin: 6px 0 0;
  color: var(--muted);
  font-size: 19px;
  line-height: 1.5;
}

.letterPage .greetings {
  margin-top: 14px;
}

/* ---- Health: the closing, centred across the fold ------------------------------------------- */

.letterPage .closing {
  padding-bottom: clamp(40px, 4vw, 64px);
}

.letterPage .pause {
  display: grid;
  justify-items: center;
  text-align: center;
}

.letterPage .pause .chapter {
  margin-bottom: clamp(28px, 3vw, 48px);
}

.letterPage .pause .body {
  margin-inline: auto;
}

.letterPage .actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 14px;
  margin-top: clamp(28px, 2.6vw, 40px);
}

/* ---- Narrower two-column windows, then one column ------------------------------------------- */

@media (min-width: 900px) and (max-width: 1199px) {
  .letterPage .promises {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 899px) {
  :global([data-look="ink"]).letterPage {
    --letter: clamp(104px, 28vw, 160px);
    --part-half: clamp(48px, 9vw, 72px);
  }

  .letterPage .sheet {
    background:
      radial-gradient(circle at 6% 20%, rgb(150 112 62 / 0.06), transparent 80px),
      radial-gradient(circle at 94% 58%, rgb(150 112 62 / 0.05), transparent 100px),
      linear-gradient(
        90deg,
        rgb(120 88 46 / 0.07),
        transparent 6%,
        transparent 94%,
        rgb(120 88 46 / 0.07)
      );
  }

  .letterPage .word {
    width: 86vw;
  }

  .letterPage .grid,
  .letterPage [data-part="purpose"] .grid,
  .letterPage [data-part="roots"] .grid,
  .letterPage .experience {
    grid-template-columns: minmax(0, 1fr);
    grid-template-areas:
      "letter"
      "words"
      "art";
    row-gap: clamp(20px, 5vw, 32px);
  }

  .letterPage .grid .areaLetter {
    justify-self: start;
  }

  .letterPage .promises {
    grid-template-columns: minmax(0, 1fr);
  }

  .letterPage .chapter[data-size="closing"] {
    --letter: clamp(140px, 40vw, 220px);
  }
}

/* ---- Other languages (DESIGN.md, The CJK Room Rule) ----------------------------------------- */

.letterPage :is(h2, h3):lang(ko) {
  word-break: keep-all;
}

.letterPage :is(h2, h3):lang(ja) {
  word-break: auto-phrase;
}
```

- [ ] **Step 6: Remove the old page's files and fix the words file's header**

```bash
git -C C:/Users/mcbig/Documents/codes/bigh-ink rm src/components/about/about-ink.module.css src/components/about/about-route.ts
```

In `src/components/about/about-content.ts` replace only the comment line `// The page is the Ink & Gold About (October 5, 2026). The earlier Glass page (Mo picked look B` with these two lines:

```ts
// The page is "The name, on a folded letter" (Mo's design D, October 6, 2026). Before it: the first
// ink About (October 5, commits up to c30a489) and the Glass page (Mo picked look B
```

(keep the line that follows, `// with opening 3 and Switzer on Sept 28, 2026) is in the backup zip named in docs/about-page.md.`).

Run: `npx --prefix C:/Users/mcbig/Documents/codes/bigh-ink tsc --noEmit -p C:/Users/mcbig/Documents/codes/bigh-ink`
Expected: no errors. (If something else still imports `about-route` or `about-ink.module.css`, `grep -rn "about-route\|about-ink.module" C:/Users/mcbig/Documents/codes/bigh-ink/src` finds it; remove that import.)

- [ ] **Step 7: Run the checks**

Restart the dev server (files were added and deleted). Then:
`python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/scripts/qa/qa_about.py http://localhost:3025`
Expected: `N/N passed`. For each FAIL, open the matching screenshot in `scripts/qa/out/about-letter/` and fix the CSS (sizes, gaps, the letter's `justify-self`), not the check. Typical: the sides check fails at 1024 when the fold gap is too small for a long heading; the closing-H gap fails when the H's padded box runs into the heading (raise `.pause .chapter` margin-bottom).

- [ ] **Step 8: Look at the page like a visitor**

Read every `scripts/qa/out/about-letter/1440x900-*.png` and `390x844-*.png` and the `layout-*.png` shots at full size, top to bottom. Compare with `reference/ink-pages/mockups/about-d.png`. Expected: it reads as one folded letter; letters calm and legible; the rest of each chapter word sits on the initial's baseline (adjust `.rest` margin-bottom if it floats or sinks); no element touches a fold; no empty half-screen. Score it out of 10 in your report, honestly; fix what keeps it under 9 now if it is layout (motion comes in Task 4).

- [ ] **Step 9: Lint, format and commit**

```bash
npx --prefix C:/Users/mcbig/Documents/codes/bigh-ink prettier --write C:/Users/mcbig/Documents/codes/bigh-ink/src/components/about C:/Users/mcbig/Documents/codes/bigh-ink/src/components/ink/ink-page.tsx
npm --prefix C:/Users/mcbig/Documents/codes/bigh-ink run lint
git -C C:/Users/mcbig/Documents/codes/bigh-ink add -A src/components/about scripts/qa/qa_about.py
git -C C:/Users/mcbig/Documents/codes/bigh-ink commit -m "feat(about): the name, on a folded letter

Mo's design D (October 6, 2026): one sheet of aged paper with CSS folds,
BiGH written by hand, a brushed letter opening each part on alternating
sides, Dr. Liu on a pool of wash, tree rings, four watercolor dots and the
big H. Replaces the first ink About and its brush line.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: Motion: the name writes itself

**Files:**

- Modify: `scripts/qa/qa_about.py` (add the `motion` group)
- Modify: `src/components/about/chapter-word.tsx` (arrival)
- Modify: `src/components/about/about-ink.tsx` (the title's delay)
- Modify: `src/components/about/about-letter.module.css` (append the motion section)

**Interfaces:**

- Consumes: `useArrival(target, motion, share, duration)` and `useMotionOk()` from `@/components/ink/motion` (arrival marks `data-arrive="waiting"` only when the element starts out of the window, then `"in"`, then `"done"` after `duration` ms; nothing is marked with reduced motion or when it starts in view). The kit's `[data-bloom]` rules and `--bloom-delay` (a unitless number of ms, read by `useBloom`).
- Produces: CSS keyframes whose names contain `write` (the name) and `leaf` (its dot), used by the QA.

- [ ] **Step 1: Add the motion checks**

In `scripts/qa/qa_about.py`, add `import io` and `from PIL import Image` to the imports, add this function above `GROUPS`, put `motion` in `GROUPS` after `letter_layout`, and add `motion` to the docstring's usage line and this paragraph to the docstring after `letter_layout`'s: "motion: reduced motion is complete and still (no waiting letters, every bloom done, the dots up, no running animation); with motion the name is written (its animation, one breath) and its gold dot comes up after it; a chapter letter waits out of view, is written as it comes in and ends unmasked; the band blooms. With JavaScript off the written name is visible."

```python
def motion(browser):
    # Reduced motion: complete and still.
    context, page, response, errors, failed = open_page(browser, 1440, 900, reduced=True)
    scroll_through(page)
    still = page.evaluate(
        """() => ({ waiting: document.querySelectorAll('[data-arrive]').length,
             blooms: [...document.querySelectorAll('[data-bloom]')].filter(e => e.dataset.bloom !== 'done').length,
             dots: [...document.querySelectorAll('[data-dot]')].map(d => getComputedStyle(d).opacity),
             word: getComputedStyle(document.querySelector('[data-word] img')).animationName,
             masks: [...document.querySelectorAll('[data-chapter] img, [data-word] img')].map(i => getComputedStyle(i).maskImage).filter(m => m !== 'none'),
             running: document.getAnimations().filter(a => { const t = a.effect && a.effect.target;
               return t && t.closest && t.closest('main') && !t.closest('[class*=greetings]'); }).length })"""
    )
    check("reduced motion: no letter waits", still["waiting"] == 0, still)
    check("reduced motion: every bloom done", still["blooms"] == 0, still)
    check("reduced motion: the gold dots are up", still["dots"] and all(float(o) == 1 for o in still["dots"]), still)
    check("reduced motion: the name is still and nothing is masked", still["word"] == "none" and not still["masks"], still)
    check("reduced motion: nothing moves", still["running"] == 0, still)
    context.close()

    # With motion: the name is written in one breath, then its gold dot comes up.
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="no-preference")
    page = context.new_page()
    page.goto(f"{BASE}/about", wait_until="domcontentloaded", timeout=120000)
    # The page's stylesheet first (the dot's delay is 2.75s, so this still reads it waiting).
    page.wait_for_function(
        "getComputedStyle(document.querySelector('[data-word] img')).animationName !== 'none'", timeout=5000
    )
    early = page.evaluate(
        """() => { const i = getComputedStyle(document.querySelector('[data-word] img'));
             return { name: i.animationName, duration: i.animationDuration,
                      dot: getComputedStyle(document.querySelector('[data-word] [data-dot]')).opacity }; }"""
    )
    check("motion: the name is written (its animation, one breath)", "write" in early["name"] and early["duration"] == "2.4s", early)
    check("motion: the gold dot waits for the name", float(early["dot"]) < 0.5, early)
    page.wait_for_timeout(6000)
    late = page.evaluate(
        """() => ({ mask: getComputedStyle(document.querySelector('[data-word] img')).maskPosition,
             dot: getComputedStyle(document.querySelector('[data-word] [data-dot]')).opacity,
             band: document.querySelector('[data-band]').dataset.bloom })"""
    )
    check("motion: the name ends whole", late["mask"].startswith("0%"), late)
    check("motion: then its gold dot is up", float(late["dot"]) == 1, late)
    check("motion: the band has bloomed", late["band"] == "done", late)

    # A chapter letter out of the window waits, is written as it comes in, and ends unmasked.
    state = lambda: page.evaluate(
        """() => { const c = document.querySelector('[data-chapter="G"]');
             return [c.dataset.arrive ?? null, getComputedStyle(c.querySelector('img')).maskImage]; }"""
    )
    first = state()
    check("motion: the G waits out of the window", first[0] == "waiting", first)
    page.evaluate(
        """() => { const c = document.querySelector('[data-chapter="G"]');
             window.scrollTo(0, c.getBoundingClientRect().top + window.scrollY - innerHeight / 2); }"""
    )
    page.wait_for_timeout(700)
    second = state()
    check("motion: the G is being written as it comes in", second[0] == "in" and second[1] != "none", second)
    page.wait_for_timeout(3200)
    third = state()
    check("motion: the G ends written and unmasked", third[0] == "done" and third[1] == "none", third)
    context.close()

    # JavaScript off: the written name still appears (its animation is CSS only). Read from pixels:
    # the word's band of the first screen holds ink.
    context = browser.new_context(viewport={"width": 1440, "height": 900}, java_script_enabled=False)
    page = context.new_page()
    page.goto(f"{BASE}/about", wait_until="load", timeout=120000)
    page.wait_for_timeout(4500)
    shot = Image.open(io.BytesIO(page.screenshot(clip={"x": 360, "y": 110, "width": 720, "height": 330}))).convert("L")
    dark = sum(1 for v in shot.getdata() if v < 90) / (shot.width * shot.height)
    check("JavaScript off: the written name is visible", dark >= 0.02, round(dark, 4))
    context.close()
```

- [ ] **Step 2: Run them to see them fail**

Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/scripts/qa/qa_about.py http://localhost:3025 --only=motion`
Expected: FAIL for "the name is written", "the gold dot waits", "the G waits out of the window" (no animation, no arrival yet). The reduced-motion and JavaScript-off checks may already pass.

- [ ] **Step 3: Give the chapter word its arrival**

In `src/components/about/chapter-word.tsx`:

- add the imports `import { useRef } from "react";` and `import { useArrival, useMotionOk } from "@/components/ink/motion";`
- extend the comment above the function with: "As it reaches the reading line its initial is written through the brush wipe, left to right, in one breath; the rest of the word follows and the i's gold-leaf dot comes up last. Already in the window when the page opens, or with reduced motion: there, complete."
- inside the function, before `const art`, add:

```tsx
const motion = useMotionOk();
const root = useRef<HTMLSpanElement>(null);
useArrival(root, motion, 0.6, 2400);
```

- add `ref={root}` to the outer `<span>`.

- [ ] **Step 4: Let the title unfold after the name is written**

In `src/components/about/about-ink.tsx` change `<Acronym className={styles.title} />` to `<Acronym className={styles.title} delay={2700} />`.

- [ ] **Step 5: Append the motion styles**

Append to `src/components/about/about-letter.module.css`:

```css
/* ---- Motion: the name writes itself (one breath, the shared ease) ---------------------------
   The letters are written through the brush wipe (wipe-v1.png: opaque, a dry brush's ragged edge,
   clear; at 300% wide, moving it from 100% to 0% writes left to right). The opening's name is pure
   CSS, so it never waits on a script; its gold dot comes up once the name is written. A chapter
   letter is written as it reaches the reading line (useArrival in chapter-word.tsx). Reduced
   motion: no mask, no animation, everything there. */
@media (prefers-reduced-motion: no-preference) {
  .letterPage .word .paint {
    -webkit-mask: url("/images/about-ink/wipe-v1.png") 100% 0 / 300% 100% no-repeat;
    mask: url("/images/about-ink/wipe-v1.png") 100% 0 / 300% 100% no-repeat;
    animation: write var(--breath) var(--ease) 0.35s both;
  }

  .letterPage .word .dot {
    animation: leaf-up 1.2s var(--ease) calc(0.35s + var(--breath)) both;
  }

  .letterPage .chapter[data-arrive="waiting"] .paint,
  .letterPage .chapter[data-arrive="in"] .paint {
    -webkit-mask: url("/images/about-ink/wipe-v1.png") 100% 0 / 300% 100% no-repeat;
    mask: url("/images/about-ink/wipe-v1.png") 100% 0 / 300% 100% no-repeat;
  }

  .letterPage .chapter[data-arrive="in"] .paint {
    -webkit-mask-position: 0 0;
    mask-position: 0 0;
    transition:
      -webkit-mask-position var(--breath) var(--ease),
      mask-position var(--breath) var(--ease);
  }

  .letterPage .chapter .rest,
  .letterPage .chapter .dot {
    transition:
      opacity 1.2s var(--ease),
      scale 1.2s var(--ease);
  }

  .letterPage .chapter[data-arrive="waiting"] .rest {
    opacity: 0;
  }

  .letterPage .chapter[data-arrive="in"] .rest {
    transition-delay: calc(var(--breath) * 0.55);
  }

  .letterPage .chapter[data-arrive="waiting"] .dot,
  .letterPage .chapter[data-arrive="in"] .dot {
    opacity: 0;
    scale: 0.6;
  }

  /* The band spreads from the middle as the name finishes. */
  .letterPage .band {
    --bloom-delay: 1500;
  }
}

@keyframes write {
  from {
    -webkit-mask-position: 100% 0;
    mask-position: 100% 0;
  }

  to {
    -webkit-mask-position: 0 0;
    mask-position: 0 0;
  }
}

@keyframes leaf-up {
  from {
    opacity: 0;
    scale: 0.6;
  }

  to {
    opacity: 1;
    scale: 1;
  }
}
```

- [ ] **Step 6: Run the checks**

Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/scripts/qa/qa_about.py http://localhost:3025 --only=motion` → Expected: all PASS.
Run the full file → Expected: `N/N passed` (the motion changes must not break Task 3's checks).

- [ ] **Step 7: Watch it like a visitor**

Take viewport screenshots of the opening at 0.6s, 1.4s, 2.4s and 3.6s after load (a small Playwright script with `page.wait_for_timeout` between `page.screenshot` calls, 1440x900, motion on), and two of a chapter letter mid-write (scroll it to the middle, wait 0.8s and 1.6s). Read them at full size. Expected: the name appears left to right like ink being laid down (no hard vertical edge, no flash of the whole word first), the dot lands after the H, the band spreads from the middle, the title unfolds after. If the wipe edge looks mechanical, raise the `0.035` wobble or the streak share in `wipe()` (Task 1's script), bump `V`, rebuild, and update the four `wipe-v1.png` URLs in the CSS.

- [ ] **Step 8: Commit**

```bash
npx --prefix C:/Users/mcbig/Documents/codes/bigh-ink prettier --write C:/Users/mcbig/Documents/codes/bigh-ink/src/components/about
git -C C:/Users/mcbig/Documents/codes/bigh-ink add -A src/components/about scripts/qa/qa_about.py
git -C C:/Users/mcbig/Documents/codes/bigh-ink commit -m "feat(about): the name writes itself

The written name is laid down through a dry-brush wipe in one breath, its
gold dot lands after it; each chapter letter writes itself as it arrives;
the band, pool, rings and dots bloom. Reduced motion is complete and still.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: Languages and deep links

**Files:**

- Create: `reference/ink-pages/about/translations.cjs`
- Modify: `src/i18n/copy-keys.json`, `messages/en.json`, `messages/cns.json`, `messages/kr.json`, `messages/vn.json`, `messages/jp.json` (the script writes them)
- Modify: `scripts/qa/qa_about.py` (add `deep_links`, `languages`, `languages_layout`, `nav_locales`)
- Modify: `src/components/about/about-letter.module.css` (only where a check finds a fault)

**Interfaces:**

- Consumes: `RINGS_ALT` (Task 3), the QA hooks of Task 3, `CREASE_JS`, `open_page`, `check` in `qa_about.py`.
- Produces: catalog entries for `RINGS_ALT` in all five languages.

- [ ] **Step 1: Add the four checks**

Add to `scripts/qa/qa_about.py` above `GROUPS` (and extend `GROUPS` to `[desktop_and_phone, letter_layout, motion, focus, deep_links, languages, languages_layout, nav_locales, boundary, first_screen]`; add the four names to the usage line and these lines to the docstring: "deep_links (1440x900, 1024x768, 768x1024, 390x844, 360x780): /about#purpose, #roots, #experience, #promise land the part's first content 0-64px under the header, nothing of it under the bar, its heading fully in the window. languages (kr, jp, cns, vn): 200, no console errors, the h1 and the chapter words stay English, no English source sentence left visible. languages_layout (every language at 1440x900, 1024x768, 768x1024, 390x844, 360x780): no word crosses the side margins; in Korean, Japanese, Chinese and Vietnamese no bad line break; from 900px no words cross the middle fold; Vietnamese at 390: the closing pills balance their two lines. nav_locales: from /vn/about and /kr/about the bar and the narrow menu stay in the language."):

```python
def settle(page, still=300, limit=5000):
    """Wait for a smooth scroll to end: scrollY unchanged for `still` ms (at most `limit` ms)."""
    last, held, waited = None, 0, 0
    while held < still and waited < limit:
        page.wait_for_timeout(50)
        waited += 50
        y = page.evaluate("window.scrollY")
        held = held + 50 if y == last else 0
        last = y
    return last


# Where a deep link lands: the part's first content (its chapter word or its label, whichever is
# higher) 0-64px under the header's bottom (measured at run time), and its heading fully in the
# window below the bar.
LANDING_JS = """(id) => {
  const s = document.getElementById(id);
  const tops = [...s.querySelectorAll('[data-chapter], [data-label]')].filter(e => e.offsetParent).map(e => e.getBoundingClientRect().top);
  const head = document.getElementById(id + '-title').getBoundingClientRect();
  const bar = document.querySelector('header').getBoundingClientRect();
  return { scrollY: Math.round(window.scrollY), bar: Math.round(bar.bottom), first: Math.round(Math.min(...tops)),
           headTop: Math.round(head.top), headBottom: Math.round(head.bottom), win: window.innerHeight };
}"""


def deep_links(browser):
    # Each size is one browser context: a first visit warms the fonts into the cache (a cold dev
    # font can reflow the page after the browser has aimed its scroll), then every deep link is a
    # fresh load.
    for width, height in [(1440, 900), (1024, 768), (768, 1024), (390, 844), (360, 780)]:
        context = browser.new_context(viewport={"width": width, "height": height}, reduced_motion="no-preference")
        warm = context.new_page()
        warm.goto(f"{BASE}/about", wait_until="networkidle", timeout=120000)
        warm.evaluate("document.fonts.ready.then(() => true)")
        warm.close()
        for anchor in ["purpose", "roots", "experience", "promise"]:
            page = context.new_page()
            page.goto(f"{BASE}/about#{anchor}", wait_until="networkidle", timeout=120000)
            page.evaluate("document.fonts.ready.then(() => true)")
            settle(page)
            at = page.evaluate(LANDING_JS, anchor)
            gap = at["first"] - at["bar"]
            check(
                f"{width}x{height} /about#{anchor}: lands 0-64px under the header ({gap}px), heading in the window",
                at["scrollY"] > 0 and 0 <= gap <= 64 and at["headTop"] >= at["bar"] and at["headBottom"] <= at["win"],
                at,
            )
            page.close()
        context.close()


def languages(browser):
    english = [line for line in LOCKED if len(line) > 24]
    for lang in ["kr", "jp", "cns", "vn"]:
        context, page, response, errors, failed = open_page(browser, 1440, 900, path=f"/{lang}/about", reduced=True)
        check(f"{lang} answers 200", response.status == 200, response.status)
        h1 = page.evaluate("document.querySelector('h1').getAttribute('aria-label')")
        check(f"{lang} h1 stays English", h1 == "Be in Good Health.", h1)
        chapters = page.evaluate("[...document.querySelectorAll('[data-chapter]')].map(c => [c.dataset.chapter, c.lang, c.textContent.trim()])")
        check(
            f"{lang} the chapter words stay English",
            chapters == [["B", "en", "e"], ["i", "en", "n"], ["G", "en", "ood"], ["H", "en", "ealth"]],
            chapters,
        )
        text = page.evaluate("document.querySelector('main').innerText")
        left = [line for line in english if line in text]
        check(f"{lang} no English sentence left", not left, left[:3])
        alt = page.evaluate("document.querySelector('[data-rings] img').alt")
        check(f"{lang} the rings' description is translated", alt and not alt.startswith("Tree rings"), alt)
        check(f"{lang} no console errors or warnings", not errors, errors[:3])
        page.screenshot(path=os.path.join(OUT, f"{lang}-opening.png"))
        context.close()
```

Then copy these blocks **verbatim** from the previous version of the file (`git -C C:/Users/mcbig/Documents/codes/bigh-ink show 5165359:scripts/qa/qa_about.py`, the file as it was before this plan; find them by name): `BREAKS_JS` with its three comment lines, `MARGINS_JS` with its two comment lines, `languages_layout`, the comment block above `NAV_LINKS_JS`, `NAV_LINKS_JS` and `nav_locales`. In the copied `languages_layout`, after the line `check(f"{tag} words inside the margins", not over, over[:3])` add:

```python
            if width >= 900:
                crossing = page.evaluate(CREASE_JS)
                check(f"{tag} no words cross the middle fold", not crossing, crossing[:3])
```

- [ ] **Step 2: Run them to see what fails**

Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/scripts/qa/qa_about.py http://localhost:3025 --only=deep_links,languages,languages_layout,nav_locales`
Expected: at least the four "the rings' description is translated" FAILs (no translations yet). Note every other FAIL; they are layout faults to fix in Step 4.

- [ ] **Step 3: Translate the rings' description**

Create `reference/ink-pages/about/translations.cjs`:

```js
// Adds the folded-letter About page's new strings (October 6, 2026) to the five catalogs.
// DRAFT translations, not native-reviewed: same understated voice, no new claims. hken.json stays
// {} (/hken redirects to /cns). Run from the repo root:
//   node reference/ink-pages/about/translations.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  [
    "Tree rings in ink. A gold ring marks 2016, when BiGH began; the rings inside it are the years the formula is older.",
    "水墨绘制的树木年轮。一圈金色年轮标记着 BiGH 创立的 2016 年；其内的年轮，是这个配方早于 BiGH 的岁月。",
    "먹으로 그린 나이테. 금빛 나이테 하나가 BiGH가 시작된 2016년을 표시하고, 그 안쪽의 나이테는 포뮬러가 BiGH보다 앞선 세월입니다.",
    "Vân gỗ vẽ bằng mực. Một vòng vàng đánh dấu năm 2016, khi BiGH ra đời; những vòng bên trong là những năm công thức đã có trước đó.",
    "墨で描いた年輪。金の輪は BiGH が始まった2016年を示し、その内側の輪はフォーミュラが BiGH より古い年月です。",
  ],
];
const path = "src/i18n/copy-keys.json";
const keys = JSON.parse(fs.readFileSync(path, "utf8"));
const locales = ["en", "cns", "kr", "vn", "jp"];
const catalogs = locales.map((l) => JSON.parse(fs.readFileSync("messages/" + l + ".json", "utf8")));
let next = Math.max(...Object.values(keys).map((k) => Number(k.slice(1)))) + 1;
const added = [];
for (const row of entries) {
  const key = keys[row[0]] ?? "m" + next++;
  keys[row[0]] = key;
  added.push(key + " " + row[0]);
  row.forEach((value, i) => {
    catalogs[i].Copy[key] = value;
  });
}
fs.writeFileSync(path, JSON.stringify(keys, null, 2) + "\n");
locales.forEach((l, i) =>
  fs.writeFileSync("messages/" + l + ".json", JSON.stringify(catalogs[i], null, 2) + "\n"),
);
console.log(added.join("\n"));
console.log("next id m" + next);
```

Run it from the repo root (Node resolves the relative paths from the working directory, so use the PowerShell tool, whose working directory can be the worktree, or `node --prefix`-free: `node -e "process.chdir('C:/Users/mcbig/Documents/codes/bigh-ink'); require('C:/Users/mcbig/Documents/codes/bigh-ink/reference/ink-pages/about/translations.cjs')"`).
Expected: one line `m5NN Tree rings in ink. …` and `next id m5NN`.

- [ ] **Step 4: Fix the layout faults the checks found, then run them again**

Typical faults and fixes (all in `about-letter.module.css`, inside the matching media query):

- A long Vietnamese or Japanese heading crosses the middle fold at 1024: lower `h2.heading`'s size for that language under 1200px (`.letterPage h2.heading:lang(vi)` etc.) or let the column gap grow.
- A deep link lands more than 64px under the header: the part's first content starts lower than `--part-half` (for example the roots' chapter word sits under its words on one column); adjust that part's `scroll-margin-top`.
- A bad line break in Chinese at punctuation: add `line-break: strict` for `:lang(zh)` headings.

Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/scripts/qa/qa_about.py http://localhost:3025`
Expected: `N/N passed` (the whole file).

- [ ] **Step 5: Look at the other languages**

Read `scripts/qa/out/about-letter/{kr,jp,cns,vn}-opening.png`, and take and read one 1024x768 and one 390x844 screenshot per language of the Good part. Expected: nothing crowds a fold, CJK headings break between phrases, the English chapter words sit naturally beside translated headings.

- [ ] **Step 6: Commit**

```bash
npx --prefix C:/Users/mcbig/Documents/codes/bigh-ink prettier --write C:/Users/mcbig/Documents/codes/bigh-ink/src/components/about C:/Users/mcbig/Documents/codes/bigh-ink/src/i18n/copy-keys.json C:/Users/mcbig/Documents/codes/bigh-ink/messages
git -C C:/Users/mcbig/Documents/codes/bigh-ink add reference/ink-pages/about/translations.cjs src/i18n/copy-keys.json messages src/components/about scripts/qa/qa_about.py
git -C C:/Users/mcbig/Documents/codes/bigh-ink commit -m "feat(about): the folded letter in five languages, deep links

Draft translations of the rings' description; deep links land each part
under the header; no words cross the middle fold in any language.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 6: The built site, the homepage gate, a fresh review, the notes

**Files:**

- Modify: `docs/about-page.md` (add the current page at the top)
- Modify: `src/components/about/about-letter.module.css` and others only for faults found here

**Interfaces:**

- Consumes: everything above.
- Produces: a branch ready to show Mo (not pushed).

- [ ] **Step 1: Build and start the built site**

Run: `npm --prefix C:/Users/mcbig/Documents/codes/bigh-ink run build`
Expected: the build ends without errors. Start `bigh-ink-prod` (port 3026) with the preview tool (or `npm --prefix C:/Users/mcbig/Documents/codes/bigh-ink run start -- --hostname localhost --port 3026` in the background).

- [ ] **Step 2: Run every check on the built site**

Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/scripts/qa/qa_about.py http://localhost:3026` → Expected: `N/N passed`.
Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/scripts/qa/home_snapshot.py compare http://localhost:3026 letter-t6-prod baseline-nav-prod` → Expected: `PASS`.
Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/scripts/qa/qa_home_ink.py http://localhost:3026` → Expected: all pass.
Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/scripts/qa/home_snapshot.py nav http://localhost:3026 -` → Expected: an `ok` line for / and /about.
The built site orders CSS differently from dev: a check that passes on dev and fails here is a real fault (usually a rule that is not scoped under `.letterPage`).

- [ ] **Step 3: Screenshots at every size, read like a visitor**

Take viewport screenshots, scrolling top to bottom, on the built site at 1536x864, 1440x900, 1280x720, 1024x768, 900x1100, 768x1024, 390x844 and 360x780, with motion (wait for each part's arrival before the shot) and once with reduced motion at 1440x900. Read every one at full size. Also check: once scrolled, the bar sits on the same aged paper as the page (no lighter band under it); the folds read as paper, not as drawn lines; "Illustration" sits under the rings, not over them. Write a short honest score per size. Anything under 9/10 gets fixed now (then rerun Step 2).

- [ ] **Step 4: Fresh review**

Dispatch the `impeccable-finish-reviewer` agent with: the page URL `http://localhost:3026/about`, the mockup `reference/ink-pages/mockups/about-d.png`, `DESIGN.md`, the spec section, and the Step 3 screenshots folder. Ask for an ordered list of material fixes only. Fix each finding that is a real defect; for a finding you reject, write one line why. Rerun Step 2 after fixes.

- [ ] **Step 5: Write the notes**

At the top of `docs/about-page.md` (under its title) add:

```markdown
## Current page: "The name, on a folded letter" (October 6, 2026)

Mo's design D, a blend of three concepts: one sheet of slightly aged paper folded like a letter
(CSS folds, no brush line), BiGH written by hand (the opening's name writes itself in one breath,
its gold dot lands after), a brushed letter opening each part on alternating sides of the middle
fold (Be: purpose; in: scientific roots, Dr. Liu on a pool of wash; Good: experience with tree
rings, one ring gold for 2016, and the promises under four watercolor dots; Health: Ask BiGH
Science under the big H).

- Code: `src/components/about/about-ink.tsx`, `chapter-word.tsx`, `about-letter.module.css`,
  `letter-art.ts` (generated).
- Paintings: `reference/ink-pages/about/` (prompts, originals, `build_about.py`, `check_art.py`),
  spend in `reference/ink-pages/spend.md`. Shipped in `public/images/about-ink/`.
- Checks: `scripts/qa/qa_about.py` (dev and `next start`).
- Draft translation: the rings' description (`reference/ink-pages/about/translations.cjs`), for a
  native check before launch.
- Replaced: the first ink About (October 5, commits up to c30a489, a copy of the homepage's look
  with the brush line), and before it the Glass page.
```

- [ ] **Step 6: Commit**

```bash
git -C C:/Users/mcbig/Documents/codes/bigh-ink add -A docs/about-page.md src/components/about scripts/qa/qa_about.py
git -C C:/Users/mcbig/Documents/codes/bigh-ink commit -m "docs(about): the folded letter, checked on the built site

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

- [ ] **Step 7: Stop and report**

Do not push and do not touch the demo alias. Report: the pass counts (About, homepage gate), the per-size scores, the reviewer's findings and what was done with each, the picture spend (jobs and dollars from `spend.md`), and the draft translation that needs a native check. Showing Mo a preview needs a push, which only Mo approves.

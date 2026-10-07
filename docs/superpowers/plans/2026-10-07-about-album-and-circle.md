# About B "The Album" and C "The Circle" Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build two real About pages for Mo to compare, each on its own branch: B "The album" (`about-b`) and C "The circle" (`about-c`), from her approved mockups, replacing the rejected design D.

**Architecture:** One painting build makes every new picture for both pages and writes `src/components/about/about-art.ts`. A shared `Spread` / `Painting` pair and a shared stylesheet (`about-page.module.css`) give every part the same rhythm (one picture, its words, sides swapping); each page adds its own stylesheet scoped under its own root class. B is built first on `about-b`; `about-c` branches from `about-b` and swaps the page for C, reusing the shared pieces. The QA script is rewritten per page from D's, keeping its generic checks.

**Tech Stack:** Next.js 16 (App Router, Turbopack), React, TypeScript, CSS Modules, next-intl (`useCopy`), Playwright for Python (QA), Pillow / NumPy / OpenCV (pictures), the Higgsfield API helper for GPT Image 2.5.

**Spec:** `docs/superpowers/specs/2026-10-05-ink-pages-design.md`, section "About (stage 1), October 7: B 'The album' and C 'The circle', built side by side" (commit fb9ecbc). Mockups: `reference/ink-pages/mockups/about-b.png`, `about-c.png`. Design system: `DESIGN.md`.

## Global Constraints

- Read `AGENTS.md` first. This Next.js has breaking changes: check `node_modules/next/dist/docs/` before using a Next API you have not seen in this repo. The repo's existing `next/image` usage (`priority`, `sizes`) is the pattern to follow.
- Worktree `C:/Users/mcbig/Documents/codes/bigh-ink`. Branches: `about-b` (Tasks 1-3, created in Task 1 from `ink-pages` at fb9ecbc) and `about-c` (Tasks 4-5, created in Task 4 from `about-b`). Commit locally; never push (the GitHub repo is public; Mo approves every push).
- Bash: never `cd`; use absolute paths, `git -C`, `npm --prefix`. Files are LF; `core.autocrlf=true` makes working copies CRLF, which is expected. Never `git stash`. Write new files with LF (`newline="\n"` in Python); `npx prettier --write <file>` restores LF.
- The homepage must not change: `scripts/qa/home_snapshot.py compare <url> <name> baseline-main997` (dev) / `baseline-main997-prod` (built) passes and `scripts/qa/qa_home_ink.py` passes in full.
- Mo's rules from the rejected D (bind both pages): no fold lines and no aged paper (the kit's plain rice paper); the name once (the logo, then the h1 "Be in Good Health." in plain ink; no painted BiGH, no unfolding acronym); one rhythm for every part (one picture on one side, its words on the other, sides swapping; the promises the one centred row; the closing has its own picture); phones one column, picture first.
- Words: every line of `src/components/about/about-content.ts` stays, the four section labels included. The h1 stays English with `lang="en"` in every language.
- California, not zen: no bamboo, pines or tea in any painting.
- DESIGN.md rules: One Gold Leaf (gold only inside paintings), No Red No Seal, Sentence Case, Multiply (every ink painting `mix-blend-mode: multiply`), no cards or boxes, the photo mount is the only shadow, text 15px or larger, navigation 18px or larger, targets 48px or taller, one breath `--breath: 2.4s` with `--ease`, reduced motion complete and still, honesty tag "Illustration" under each painting that pictures something.
- Multiply trap: nothing between a painting and the page root may make a stacking context (no z-index on a positioned ancestor, isolation, opacity < 1, transform, filter, mask or will-change on a part, a spread, a figure or a wrapper). The kit's bloom puts its mask and filter on the image itself; that is fine.
- Specificity: every page rule is scoped under the page root's class (`.aboutPage` for shared rules, `.album` / `.circle` for page rules), so it outranks the kit's `.look …` rules and the homepage resets in any stylesheet order.
- Real assets only: Dr. Liu's photo `public/images/jiankang-liu.jpg` as it is, placed in code. Never generate or edit a picture from a version that has his photo in it (an edit redraws his face).
- Spend: GPT Image 2.5 only through `reference/home-v2/r4/hf_unquoted.py` with `HF_RUN_STATE=C:/Users/mcbig/AppData/Local/HiggsfieldAPI/bigh-about-bc` (its own ledger); at most 30 jobs (about $1.50). Never read or print the Higgsfield credential. Never retry a failed job automatically: read the ledger first (a line for that job name means it was billed). Log every job in `reference/ink-pages/spend.md`.
- Servers: dev `npm --prefix C:/Users/mcbig/Documents/codes/bigh-ink run dev -- --hostname localhost --port 3025`, built `npm --prefix C:/Users/mcbig/Documents/codes/bigh-ink run build` then `... run start -- --hostname localhost --port 3026`, each in the background. Stop servers you start before you finish. Clear `.next/dev/cache/images` and `.next/cache/images` when a picture changes under the same name.
- Look at every screenshot full size before calling something done; the bar is 9/10 as a visitor sees it; anything that looks broken is a defect.

## Review Focus

- A translated part's words run taller than its picture (Vietnamese, Japanese): the spread must still read as a pair, its words inside their column and never over the picture. Test in Task 3 and Task 5 (`languages_layout` runs OVERLAP_JS per language).
- JavaScript is off: every painting shows (no painting left waiting for a bloom) and C's circle shows whole. Test in Task 2 (`motion`, JS off) and Task 4 (`motion`, JS off).
- The window sits at the 719/720 switch: no sideways scrolling; at 719 each part shows its picture first, at 720 picture and words stand side by side on the right sides. Test in Task 2 (`boundary`).
- Pictures are slow or blocked: every heading and paragraph is still visible, nothing waits at opacity 0 for a picture. Test in Task 2 (`focus`).
- A short desktop window (1280x720): the title and the top of the opening's picture are in the first screen. Test in Task 2 (`first_screen`) and Task 4 (`first_screen`).

---

### Task 1: The paintings for both pages

**Files:**

- Create: `reference/ink-pages/about-bc/prompts/*.txt` (12), `reference/ink-pages/about-bc/refs/*.png`, `reference/ink-pages/about-bc/originals/` (the helper writes it)
- Create: `reference/ink-pages/about-bc/build_bc.py`, `reference/ink-pages/about-bc/check_bc.py`
- Modify: `reference/ink-pages/spend.md` (a new section)
- Create (generated): `public/images/about-bc/*.webp`, `reference/ink-pages/about-bc/plates/*.png`, `src/components/about/about-art.ts`

**Interfaces:**

- Consumes: `reference/ink-pages/about/build_about.py` (functions `load`, `divided`, `levelled`, `ink_box`, `split_dot`, `art_of`, `painting`, `feathered`, `gold_pixels`; module globals `ORIG`, `URL`, `V`, `TAKES` read at call time) and through it `reference/home-v2/ink/build_assets.py` (`save`, `gold_mask`, `leaf`; globals `OUT`, `PLATES`).
- Produces: `src/components/about/about-art.ts` exporting (all `as const`):
  - `type Art = { src: string; width: number; height: number }`
  - `type Dot = Art & { left: number; top: number; size: number }`
  - `book`, `seedling`, `sequoia`, `lamp`: `Art & { gold: string }` (gold = a light mask URL)
  - `desk`, `hills`, `glasses`, `pool`: `Art`
  - `vignettes`: `{ palms: Art; bee: Art; moon: Art; letter: Art }`
  - `enso`: `Art & { dot: Dot; startDeg: number }` (`startDeg`: where the brush began, in CSS conic degrees, clockwise from 12 o'clock)
  - `dots`: `Art[]` (four, deep to pale; copies of D's)
  - every `src` under `/images/about-bc/`.

- [ ] **Step 1: Create the branch**

Run: `git -C C:/Users/mcbig/Documents/codes/bigh-ink switch -c about-b` (it starts from `ink-pages` at fb9ecbc; no files change).
Expected: `Switched to a new branch 'about-b'`.

- [ ] **Step 2: Crop the style references from the approved mockups**

Run:

```bash
python -X utf8 -c "from PIL import Image; from pathlib import Path; R=Path('C:/Users/mcbig/Documents/codes/bigh-ink/reference/ink-pages'); o=R/'about-bc/refs'; o.mkdir(parents=True, exist_ok=True); b=Image.open(R/'mockups/about-b.png').convert('RGB'); c=Image.open(R/'mockups/about-c.png').convert('RGB'); [b.crop(box).save(o/f'ref-{n}.png') for n, box in {'book':(788,197,1460,520),'seedling':(125,484,681,968),'desk':(788,1021,1452,1434),'sequoia':(54,1416,753,1953),'vignettes':(45,1989,1470,2258),'lamp':(878,2365,1398,2670)}.items()]; [c.crop(box).save(o/f'ref-{n}.png') for n, box in {'enso':(573,152,950,520),'hills':(0,672,1520,860),'glasses':(914,2383,1416,2643)}.items()]; print('ok')"
```

Look at each `refs/ref-*.png` with the Read tool. Each must hold its whole painting and nothing of Dr. Liu's photo; widen a box and run again if a painting is cut.

- [ ] **Step 3: Write the twelve prompts**

Each prompt is STYLE, a blank line, then its subject. STYLE:

```text
Traditional ink painting on one plain sheet of warm, light rice paper with fine fibres, seen flat from straight above, evenly lit, no shadow, no frame, no table, no other objects, no text, no signature, no red seal, no stamp. Sumi ink only, from deep black to soft grey washes, plus real gold leaf only where stated. Generous empty paper on every side. Match the brushwork and mood of the reference picture.
```

Subjects (file name → text):

- `book-v1.txt`: `An old open book lying flat, its pages softly fanned, painted in ink with grey washes, a ribbon bookmark of real gold leaf lying across the pages and hanging over the edge. Centred, about 70% of the picture's width.`
- `seedling-v1.txt`: `A young oak seedling growing from an acorn: a slender stem with a few lobed oak leaves above a soft soil line, the split acorn at the stem's foot, and below the soil line its fine roots spreading downward. One small acorn of real gold leaf lies among the roots. Centred, about 75% of the picture's height.`
- `desk-v1.txt`: `A scientist's desk in ink: a calligraphy brush on its rest, a classic microscope painted entirely in ink and grey wash (no gold, no brass, no colour), and a small stack of old books. Soft grey washes around them. Centred, about 75% of the picture's width.`
- `sequoia-v1.txt`: `The massive, deeply furrowed trunk of one ancient giant sequoia rising out of soft mist, its crown fading upward into the wash, a young sequoia sapling standing beside its foot, faint misty trees behind. A small touch of real gold leaf on the old trunk. Majestic and calm. About 80% of the picture's height.`
- `palms-v1.txt`: `Two tall, slender California fan palms standing in front of softly rolling hills, a small sun of real gold leaf low in the sky, the hills touched with pale gold wash. Elegant and quiet, not a beach: no sand, no waves, no umbrellas. Centred, about 70% of the picture's height.`
- `bee-v1.txt`: `A small leafy branch with one bee flying beside it, painted in ink, delicate and calm. Centred, about 60% of the picture's height.`
- `moon-v1.txt`: `A crescent moon of real gold leaf with a soft grey wash of cloud beneath it. Centred, about 55% of the picture's height.`
- `letter-v1.txt`: `A folded letter in an open envelope with a fountain pen resting across it, painted in ink with soft grey washes. Centred, about 60% of the picture's height.`
- `lamp-v1.txt`: `A small desk lamp bending over an open journal, casting a soft pool of warm light painted in real gold leaf onto the pages, a sprig of leaves beside the journal. Centred, about 70% of the picture's width.`
- `enso-v1.txt`: `One large circle brushed in a single confident stroke (an enso), open where the stroke lifts, its ink rich and black where the brush started and dry-brushed where it lifted, with a small touch of real gold leaf on the paper at the point where the brush began, clearly separate from nothing but the stroke. Calm and balanced. Centred, the circle about 72% of the picture's height.`
- `hills-v1.txt`: `A soft, wide band of low, gently rolling California coastal hills painted in pale grey ink wash, layer behind layer, feathering out at both ends and at the bottom into the paper, with a faint glow of real gold leaf light along one hilltop. No sharp peaks, no trees, no buildings, no mountains like Chinese landscapes. The band about 92% of the picture's width and 25% of its height, centred.`
- `glasses-v1.txt`: `A pair of round reading glasses resting on an open notebook, a few soft grey strokes suggesting handwriting (nothing legible), a small touch of real gold leaf on the glasses' hinge. Centred, about 70% of the picture's width.`

- [ ] **Step 4: Start the spend log section**

Append to `reference/ink-pages/spend.md`:

```markdown
## About B and C, built side by side (October 7, 2026)

Ledger: `C:/Users/mcbig/AppData/Local/HiggsfieldAPI/bigh-about-bc/` (this plan caps it at 30 jobs).
Mockup rounds before this plan: 7 jobs in `bigh-about2` (about $0.35).

| Job | Picture | Kept | Note |
| --- | ------- | ---- | ---- |
```

- [ ] **Step 5: Run the first take of each painting, one at a time**

For each `NAME` and its reference `REF` in `book-v1 book`, `seedling-v1 seedling`, `desk-v1 desk`, `sequoia-v1 sequoia`, `palms-v1 vignettes`, `bee-v1 vignettes`, `moon-v1 vignettes`, `letter-v1 vignettes`, `lamp-v1 lamp`, `enso-v1 enso`, `hills-v1 hills`, `glasses-v1 glasses`:

```bash
HF_RUN_STATE=C:/Users/mcbig/AppData/Local/HiggsfieldAPI/bigh-about-bc python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/reference/home-v2/r4/hf_unquoted.py NAME C:/Users/mcbig/Documents/codes/bigh-ink/reference/ink-pages/about-bc/prompts/NAME.txt --aspect 16:9 --ref C:/Users/mcbig/Documents/codes/bigh-ink/reference/ink-pages/about-bc/refs/ref-REF.png --out C:/Users/mcbig/Documents/codes/bigh-ink/reference/ink-pages/about-bc/originals
```

Expected each time: `status completed`, `saved …/gpt25-NAME.png`. One job at a time (the helper holds a lock). Add one row per job to `spend.md`.

- [ ] **Step 6: Look at every original at full size; keep or retake**

Keep a take only if: the subject reads at a glance; calm, real ink brushwork matching its reference; gold leaf only where the prompt asks (the desk has none); plain paper; no red; nothing East-Asian-zen beyond the enso (no bamboo, pines, tea); the enso is one stroke, open, with its gold touch clearly at the stroke's start; the hills are low and rolling, not peaks. At most two retakes per painting: copy the prompt to `NAME-v2.txt` (then `-v3`), add one sentence naming the defect, run Step 5's command with the new name, and point TAKES (Step 7) at the kept take. Record every job and the kept take in `spend.md`.

- [ ] **Step 7: Write the build script**

Create `reference/ink-pages/about-bc/build_bc.py`:

```python
"""Build the paintings for About B "The album" and C "The circle" (Mo, October 7, 2026).

Originals: reference/ink-pages/about-bc/originals/gpt25-<take>.png (GPT Image 2.5 on rice paper;
prompts in prompts/, spend in reference/ink-pages/spend.md). Output: public/images/about-bc/*.webp
(lossless plates in plates/) and src/components/about/about-art.ts, which both pages import. The
treatments are D's (reference/ink-pages/about/build_about.py): the paper divided out and lifted to
pure white so a painting multiplies onto the page's paper with no box, gold leaf cut out (the
enso's start) or kept as a light mask (build_assets.gold_mask). D's pool and four dots are copied
in, so the pages depend on this folder only.

usage: python -X utf8 reference/ink-pages/about-bc/build_bc.py
"""

import json
import math
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "reference/ink-pages/about"))
import build_about as bd  # noqa: E402

ba = bd.ba
OUT = REPO / "public/images/about-bc"
URL = "/images/about-bc"
TS = REPO / "src/components/about/about-art.ts"
# Bump when a shipped picture changes after it has been pushed (the image optimizer caches by URL).
V = "v1"
# The take of each painting that ships (the original's name after "gpt25-").
TAKES = {
    "book": "book-v1",
    "seedling": "seedling-v1",
    "desk": "desk-v1",
    "sequoia": "sequoia-v1",
    "palms": "palms-v1",
    "bee": "bee-v1",
    "moon": "moon-v1",
    "letter": "letter-v1",
    "lamp": "lamp-v1",
    "enso": "enso-v1",
    "hills": "hills-v1",
    "glasses": "glasses-v1",
}

# D's helpers read these module globals at call time: point them at this folder.
bd.ORIG = HERE / "originals"
bd.URL = URL
bd.V = V
bd.TAKES = TAKES
ba.OUT = OUT
ba.PLATES = HERE / "plates"


def gilded(key, width, pad=0.04):
    """A painting with gold leaf, and the light mask for the kit's glint over its leaf."""
    art = bd.painting(key, key, width, pad=pad)
    ba.gold_mask(f"{key}-{V}", sat_from=0.3)
    art["gold"] = f"{URL}/{key}-{V}-gold.webp"
    return art


def vignette(key):
    """A small promise picture: cropped to its ink, its edges feathered to white."""
    img = bd.load(TAKES[key])
    flat = bd.divided(img)
    x0, y0, x1, y1 = bd.ink_box(np.asarray(flat), pad=0.12)
    crop = bd.feathered(bd.levelled(flat.crop((x0, y0, x1, y1))), 0.06)
    return bd.art_of(crop, f"{key}-{V}", 480)


def enso():
    """The circle, its gold start as its own picture, and where the brush began: the angle of the
    gold's centre around the circle's centre (CSS conic degrees, clockwise from 12 o'clock)."""
    art = bd.painting("enso", "enso", 1400, with_dot=True)
    dot = art["dot"]
    w, h = art["width"], art["height"]
    cx = (dot["left"] + dot["size"] / 2) * w
    cy = dot["top"] * h + dot["size"] * w * dot["height"] / dot["width"] / 2
    angle = math.degrees(math.atan2(cx - w / 2, -(cy - h / 2))) % 360
    art["startDeg"] = round(angle, 1)
    return art


def copied(name):
    """One of D's pictures, copied in as it shipped."""
    src = REPO / "public/images/about-ink" / f"{name}-v1.webp"
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, OUT / f"{name}-v1.webp")
    with Image.open(src) as im:
        return {"src": f"{URL}/{name}-v1.webp", "width": im.width, "height": im.height}


def write_ts(entries):
    head = [
        "// Generated by reference/ink-pages/about-bc/build_bc.py. Do not edit by hand: change the",
        "// script (or its TAKES) and run it again. The paintings of About B (the album) and C (the",
        "// circle), October 7, 2026: GPT Image 2.5 on rice paper, the paper divided out so each multiplies",
        "// onto the page's own paper; gold leaf as a light mask (`gold`) or a cut-out (the enso's dot).",
        "",
        "export type Art = { src: string; width: number; height: number };",
        "/** A gold-leaf cut-out, placed by fractions of its painting's width and height. */",
        "export type Dot = Art & { left: number; top: number; size: number };",
        "",
    ]
    body = [f"export const {name} = {json.dumps(value, indent=2)} as const;\n" for name, value in entries]
    TS.write_text("\n".join(head) + "\n".join(body), encoding="utf-8", newline="\n")
    print(TS.relative_to(REPO))


if __name__ == "__main__":
    write_ts(
        [
            ("book", gilded("book", 1400)),
            ("seedling", gilded("seedling", 1200)),
            ("desk", bd.painting("desk", "desk", 1400)),
            ("sequoia", gilded("sequoia", 1200)),
            ("vignettes", {k: vignette(k) for k in ("palms", "bee", "moon", "letter")}),
            ("lamp", gilded("lamp", 1200)),
            ("enso", enso()),
            # The hills' pale fringes run well past their body: a wide pad keeps them whole.
            ("hills", bd.painting("hills", "hills", 2400, pad=0.2)),
            ("glasses", bd.painting("glasses", "glasses", 1200)),
            ("pool", copied("pool")),
            ("dots", [copied(f"dot-{k}") for k in range(1, 5)]),
        ]
    )
```

- [ ] **Step 8: Write the check script (it fails before the build)**

Create `reference/ink-pages/about-bc/check_bc.py`:

```python
"""Check the B and C paintings (build_bc.py): every picture about-art.ts names exists at its
stated size; ink pictures are pure white to their edges (no box on the page); gold masks cover a
small, real share; the enso's dot is a cut-out and its start angle is a real angle; the desk has
no gold; four dots, deep to pale.

usage: python -X utf8 reference/ink-pages/about-bc/check_bc.py   (exit 0 when all pass)
"""

import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[3]
TS = (REPO / "src/components/about/about-art.ts").read_text(encoding="utf-8")
sys.path.insert(0, str(REPO / "reference/ink-pages/about"))
from build_about import gold_pixels  # noqa: E402

results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"{'PASS' if ok else 'FAIL'} {name}{(' — ' + str(detail)) if detail and not ok else ''}")


def file_of(src):
    return REPO / "public" / src.lstrip("/")


# Prettier unquotes the generated object's keys, so a key may or may not be in quotes.
srcs = set(re.findall(r'"(/images/about-bc/[^"]+)"', TS))
check("about-art.ts names pictures", len(srcs) >= 20, len(srcs))
missing = sorted(s for s in srcs if not file_of(s).exists())
check("every picture about-art.ts names exists", not missing, missing)
for src, w, h in re.findall(r'"?src"?:\s*"([^"]+)",\s*"?width"?:\s*(\d+),\s*"?height"?:\s*(\d+)', TS):
    if file_of(src).exists():
        size = Image.open(file_of(src)).size
        check(f"{src} is {w}x{h}", size == (int(w), int(h)), size)

for name in ["book", "seedling", "desk", "sequoia", "palms", "bee", "moon", "letter", "lamp", "enso", "hills", "glasses"]:
    p = REPO / f"public/images/about-bc/{name}-v1.webp"
    if p.exists():
        a = np.asarray(Image.open(p).convert("L")).astype(int)
        strip = np.concatenate([a[:3].ravel(), a[-3:].ravel(), a[:, :3].ravel(), a[:, -3:].ravel()])
        check(f"{name}: white to its edge (outer 3px mean ≥ 254.5, < 1% under 235)", strip.mean() >= 254.5 and (strip < 235).mean() < 0.01, [round(strip.mean(), 2), round((strip < 235).mean(), 4)])

for name in ["book", "seedling", "sequoia", "lamp"]:
    p = REPO / f"public/images/about-bc/{name}-v1-gold.webp"
    if p.exists():
        cover = (np.asarray(Image.open(p).convert("RGBA"))[..., 3] > 128).mean()
        check(f"{name}: a gold light mask (0.1%-15% of the picture)", 0.001 <= cover <= 0.15, round(cover, 4))
    else:
        check(f"{name}: gold mask exists", False, p.name)

desk = REPO / "public/images/about-bc/desk-v1.webp"
if desk.exists():
    check("desk: no gold leaf", gold_pixels(np.asarray(Image.open(desk).convert("RGB"))).mean() < 0.0005)

dot = REPO / "public/images/about-bc/enso-dot-v1.webp"
if dot.exists():
    alpha = np.asarray(Image.open(dot).convert("RGBA"))[..., 3]
    check("enso dot: a gold cut-out with transparency", (alpha < 20).mean() > 0.2 and (alpha > 200).mean() > 0.05)
m = re.search(r'"?startDeg"?:\s*([\d.]+)', TS)
check("enso: a start angle in [0, 360)", bool(m) and 0 <= float(m.group(1)) < 360, m.group(1) if m else None)

tones = []
for k in range(1, 5):
    p = REPO / f"public/images/about-bc/dot-{k}-v1.webp"
    if p.exists():
        tones.append(np.percentile(np.asarray(Image.open(p).convert("L")).astype(int), 5))
check("four dots, deep to pale", len(tones) == 4 and all(x < y for x, y in zip(tones, tones[1:])), tones)

print(f"\n{sum(results)}/{len(results)} passed")
sys.exit(0 if all(results) else 1)
```

Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/reference/ink-pages/about-bc/check_bc.py`
Expected: `FileNotFoundError` for `about-art.ts` (nothing built yet).

- [ ] **Step 9: Build, format, check**

Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/reference/ink-pages/about-bc/build_bc.py`
Then: `npx --prefix C:/Users/mcbig/Documents/codes/bigh-ink prettier --write C:/Users/mcbig/Documents/codes/bigh-ink/src/components/about/about-art.ts`
Then run the check script. Expected: `N/N passed`. A failure is fixed by a retake or by the build (never by loosening the check). If `split_dot` found something other than the enso's gold start, look at `plates/enso-v1.png` and `plates/enso-dot-v1.png`.

- [ ] **Step 10: Look at the built plates**

Read every `reference/ink-pages/about-bc/plates/*-v1.png` at full size. Expected: whole paintings, no smudge where the enso's dot was lifted, nothing cut at a crop edge.

- [ ] **Step 11: Commit**

```bash
git -C C:/Users/mcbig/Documents/codes/bigh-ink add reference/ink-pages/about-bc reference/ink-pages/spend.md public/images/about-bc src/components/about/about-art.ts
git -C C:/Users/mcbig/Documents/codes/bigh-ink commit -m "feat(about): paintings for the album and the circle

Twelve GPT Image 2.5 paintings (book, oak seedling, desk, giant sequoia,
four promise vignettes, lamp; enso, California hills, reading glasses),
built by build_bc.py into about-art.ts with D's pool and dots copied in.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 2: B "The album" page, with its checks

**Files:**

- Create: `src/components/about/spread.tsx`, `src/components/about/about-page.module.css`, `src/components/about/album.module.css`
- Rewrite: `src/components/about/about-ink.tsx`, `scripts/qa/qa_about.py`
- Delete: `src/components/about/chapter-word.tsx`, `src/components/about/about-letter.module.css`, `src/components/about/letter-art.ts`, `src/components/about/acronym.tsx`, `src/components/about/acronym.module.css`, `public/images/about-ink/` (D's pictures; the pool and dots were copied in Task 1)
- Modify: `src/components/about/about-content.ts` (header comment only)

**Interfaces:**

- Consumes: `about-art.ts` (Task 1); `InkPage({ current, route?, follow?, className?, children })`; `CountUp({ to, suffix, className })`, `Greetings({ className })`, `about`, `drafts`, `routes` from `about-content.ts`; `liu` from `@/components/home-v2/look-ink/assets`; kit classes from `@/components/ink/ink.module.css` (`wrap`, `ink`, `display`, `label`, `caption`, `pill`, `pillGhost`, `gold`).
- Produces (Task 4 reuses them unchanged):
  - `Painting({ art, alt, sizes, caption?, gold?, delay?, priority?, waiting?, className? })` and `Spread({ id, part, side, labelledBy, picture, children })` from `spread.tsx`
  - `about-page.module.css` classes: `aboutPage`, `opening`, `kicker`, `title`, `lead`, `part`, `spread`, `words`, `painting`, `paintingBody`, `label`, `heading`, `body`, `more`, `mount`, `figures`, `figure`, `unit`, `promise`, `promises`, `promiseDot`, `greetings`, `actions`
  - QA hooks: `[data-about="album"|"circle"]` on the page's wrapper; `[data-part]` on every part (`opening`, `purpose`, `roots`, `experience`, `promise`, `closing`); `[data-picture]` (one per spread part) holding its painting `img`; `[data-words]`; `[data-side]` on each `.spread`; `[data-label]`; `[data-mount]`; `[data-promise]` on each promise `li`. Section ids and `#<id>-title` headings as before.
  - `ALT` (the paintings' alt texts) exported from `about-ink.tsx`.

- [ ] **Step 1: Write the new QA file**

Rewrite `scripts/qa/qa_about.py`. Build it in this order:

1. The docstring below.
2. Copied **verbatim** from the previous file (`git -C C:/Users/mcbig/Documents/codes/bigh-ink show 27e71b7:scripts/qa/qa_about.py`), found by name: the imports (`io`, `os`, `re`, `sys`, `from PIL import Image`, playwright), `ARGS`, `BASE`, `results`, `LOCKED`, `check`, `PREFETCH_CSS` with its comment, `counted`, `open_page`, `shots`, `scroll_through`, `GREETINGS_JS`, `STACKING_JS` with its comment, `focus`, `wait_until`, `settle`, `BREAKS_JS`, `MARGINS_JS`, `PHRASES_JS`, `NAV_LINKS_JS` with its comment, `nav_locales`. Change only: `OUT` ends in `"about-album"`.
3. The new code below, then `GROUPS`, `ONLY` and the runner block copied from the previous file's end, with `GROUPS = [desktop_and_phone, rhythm, motion, focus, boundary, first_screen]`.

Docstring:

```python
"""QA for About B, "The album" (Mo, October 7, 2026; mockup reference/ink-pages/mockups/about-b.png;
spec docs/superpowers/specs/2026-10-05-ink-pages-design.md, "About (stage 1), October 7").

desktop_and_phone (1440x900, 390x844): 200; no console errors or warnings (but PREFETCH_CSS); no
failed requests; one h1, English "Be in Good Health." with lang="en"; every locked line; no canvas,
no brush layer, no folds, no aged paper; every painting multiplies and nothing between a painting
and the page root makes a stacking context; the menu bar marks About; no sideways scrolling; text
15px+, navigation 18px+, targets 48px+; the opening's painting loads eagerly; the Support and Ask
sheets open, close and hand focus back.
rhythm (1440x900, 1280x800, 1024x768, 768x1024, 390x844): every spread part has one picture and its
words; on two columns the pictures stand opening right, purpose left, roots right, experience left,
closing right, and are about the same size; on one column each picture comes first; the name once
(nothing in the page but the h1 at 56px or larger, no painted name); "Illustration" under each
picture, "Illustrations" under the promise row; no words over a painting; four promises in one row
from 1200px, two by two from 600px, one column below; Dr. Liu's photo beside his words.
motion: reduced motion complete and still; with motion the opening's painting blooms on arrival and
a lower painting waits out of view, then blooms; a waiting painting is hidden; with JavaScript off
every painting shows.
focus: Skip to content puts focus at the words; with pictures blocked every heading and paragraph
is visible.
boundary (719x900, 720x900): no sideways scrolling; one column at 719 (picture first), two at 720.
first_screen (1280x720, 1440x900, 1536x864, 390x844): the title and the top of the opening's picture
in the first screen.

Pictures: scripts/qa/out/about-album/<size>-NN.png.

Usage: python -X utf8 scripts/qa/qa_about.py [base-url] [--only=desktop_and_phone,rhythm,motion,focus,boundary,first_screen]
"""
```

New code:

```python
DESIGN = "album"
# Each spread part and the side its picture stands on from 720px (the promise is the centred row).
SIDES = {"opening": "right", "purpose": "left", "roots": "right", "experience": "left", "closing": "right"}
TWO_COLUMNS = 720

RHYTHM_JS = """(sides) => {
  const out = {};
  for (const part of Object.keys(sides)) {
    const p = document.querySelector(`[data-part="${part}"]`);
    if (!p) { out[part] = null; continue; }
    const pics = [...p.querySelectorAll('[data-picture]')], words = [...p.querySelectorAll('[data-words]')];
    const pb = pics[0]?.querySelector('img')?.getBoundingClientRect(), wb = words[0]?.getBoundingClientRect();
    out[part] = { pictures: pics.length, words: words.length,
      side: pb && wb ? ((pb.left + pb.width / 2) < (wb.left + wb.width / 2) ? 'left' : 'right') : null,
      first: pb && wb ? (pb.top < wb.top ? 'picture' : 'words') : null,
      height: pb ? Math.round(pb.height) : 0, captions: [...p.querySelectorAll('[data-picture] figcaption')].map(c => c.textContent.trim()) };
  }
  return out;
}"""

# Words over paintings: glyph rectangles of the page's words against the boxes of its paintings
# (Dr. Liu's photo is not a painting; the promise pictures are).
OVERLAP_JS = """() => {
  const words = [...document.querySelectorAll('main h1, main h2, main h3, main p, main dt, main dd, main a, main button, main figcaption')]
    .filter(e => e.offsetParent && !e.closest('[data-picture]'));
  const art = [...document.querySelectorAll('[data-picture] img, [data-promise] img, [data-picture-band]')].filter(e => e.offsetParent && !e.closest('[data-mount]'));
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

# The name once: nothing in the page but the h1 is set at 56px or larger, and no picture is a
# painted name.
NAME_ONCE_JS = """() => ({
  big: [...document.querySelectorAll('main *')].filter(e => e.offsetParent && e.tagName !== 'H1' && !e.closest('h1')
      && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && parseFloat(getComputedStyle(e).fontSize) >= 56)
    .map(e => [e.textContent.trim().slice(0, 20), getComputedStyle(e).fontSize]),
  painted: [...document.querySelectorAll('main img')].map(i => i.getAttribute('src') || '').filter(s => /word-v[0-9]|letter-[bigh]-v[0-9]/.test(s)) })"""


def desktop_and_phone(browser):
    for width, height in [(1440, 900), (390, 844)]:
        tag = f"{width}x{height}"
        context, page, response, errors, failed = open_page(browser, width, height)
        check(f"{tag} answers 200", response.status == 200, response.status)
        check(f"{tag} the {DESIGN} page", page.evaluate(f"!!document.querySelector('[data-about=\"{DESIGN}\"]')"))
        text = page.evaluate("document.body.innerText")
        missing = [line for line in LOCKED if line not in text]
        check(f"{tag} every locked line", not missing, missing)
        h1 = page.evaluate("[...document.querySelectorAll('h1')].map(h => [h.textContent.trim(), h.lang])")
        check(f"{tag} one English h1", h1 == [["Be in Good Health.", "en"]], h1)
        check(f"{tag} no canvas and no brush layer", page.evaluate("!document.querySelector('main canvas') && !document.querySelector('[data-lifts]')"))
        folds = page.evaluate(
            "[...document.querySelectorAll('[data-part]')].filter(p => getComputedStyle(p, '::before').content !== 'none').length + document.querySelectorAll('[data-sheet]').length"
        )
        check(f"{tag} no folds", folds == 0, folds)
        paper = page.evaluate("getComputedStyle(document.querySelector('[data-look=\"ink\"]')).backgroundImage")
        check(f"{tag} the kit's plain rice paper", "paper.webp" in paper and "aged" not in paper, paper)
        blends = page.evaluate(
            "[...document.querySelectorAll('main img')].filter(i => !i.closest('[data-mount]') && !i.matches('[data-dot]')).map(i => getComputedStyle(i).mixBlendMode)"
        )
        check(f"{tag} paintings multiply", blends and all(b == "multiply" for b in blends), blends)
        stacking = page.evaluate(STACKING_JS)
        check(f"{tag} nothing between a painting and the page root makes a stacking context", stacking["paintings"] > 0 and not stacking["found"], stacking["found"][:4])
        nav = page.evaluate(
            """() => { const n = document.querySelector('#site-navigation'); const sheet = document.querySelector('[data-nav-sheet]');
                 return { current: [...n.querySelectorAll('[aria-current="page"]')].map(a => a.textContent.trim()),
                          menuCurrent: [...sheet.querySelectorAll('[aria-current="page"]')].map(a => a.textContent.trim()) }; }"""
        )
        check(f"{tag} the menu bar marks About", nav["current"] == ["About"] and nav["menuCurrent"] == ["About"], nav)
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
        eager = page.evaluate("(() => { const i = document.querySelector('[data-part=\"opening\"] img'); return i ? i.getAttribute('loading') : 'missing'; })()")
        check(f"{tag} the opening's painting loads eagerly", eager != "lazy" and eager != "missing", eager)
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
        check(f"{tag} Ask sheet opens", "Ask BiGH Science" in page.evaluate("document.querySelector('dialog[open]')?.innerText ?? ''"))
        page.keyboard.press("Escape")
        page.wait_for_timeout(600)
        check(f"{tag} focus returns to Ask", page.evaluate("document.activeElement?.textContent?.trim()") == "Ask BiGH Science")
        page.evaluate("window.scrollTo(0, 0)")
        shots(page, tag, height)
        loaded = page.evaluate("[...document.querySelectorAll('main img')].map(i => i.complete && i.naturalWidth > 0)")
        check(f"{tag} every picture loaded", loaded and all(loaded), loaded)
        check(f"{tag} no console errors or warnings", not errors, errors[:3])
        check(f"{tag} no failed requests", not failed, failed[:3])
        context.close()


def rhythm(browser):
    for width, height in [(1440, 900), (1280, 800), (1024, 768), (768, 1024), (390, 844)]:
        tag = f"{width}x{height}"
        context, page, response, errors, failed = open_page(browser, width, height, reduced=True)
        r = page.evaluate(RHYTHM_JS, SIDES)
        pairs = {p: v and (v["pictures"], v["words"]) for p, v in r.items()}
        check(f"{tag} every spread part: one picture and its words", all(v == (1, 1) for v in pairs.values()), pairs)
        if width >= TWO_COLUMNS:
            sides = {p: v and v["side"] for p, v in r.items()}
            check(f"{tag} pictures on alternating sides", sides == SIDES, sides)
            heights = sorted(v["height"] for v in r.values() if v)
            median = heights[len(heights) // 2]
            check(f"{tag} the pictures about the same size (0.55-1.6 of the median)", all(0.55 <= h / median <= 1.6 for h in heights), heights)
        else:
            firsts = {p: v and v["first"] for p, v in r.items()}
            check(f"{tag} one column: each picture first", all(f == "picture" for f in firsts.values()), firsts)
        once = page.evaluate(NAME_ONCE_JS)
        check(f"{tag} the name once", not once["big"] and not once["painted"], once)
        captions = {p: v and v["captions"] for p, v in r.items()}
        check(f"{tag} Illustration under each picture", all(c == ["Illustration"] for c in captions.values()), captions)
        row_caption = page.evaluate("document.querySelector('[data-part=\"promise\"] [data-row-caption]')?.textContent.trim() ?? null")
        check(f"{tag} Illustrations under the promise row", row_caption == "Illustrations", row_caption)
        hits = page.evaluate(OVERLAP_JS)
        check(f"{tag} no words over a painting", not hits, hits[:4])
        rows = page.evaluate("new Set([...document.querySelectorAll('[data-promise]')].map(li => Math.round(li.getBoundingClientRect().top / 4))).size")
        want = 1 if width >= 1200 else 2 if width >= 600 else 4
        check(f"{tag} the promises in {want} row(s)", rows == want, rows)
        mount = page.evaluate(
            """() => { const m = document.querySelector('#roots [data-mount]'), w = document.querySelector('#roots [data-words]');
                 if (!m || !w) return null; const a = m.getBoundingClientRect(), b = w.getBoundingClientRect();
                 return a.left >= b.left - 1 && a.right <= b.right + 1 && a.top >= b.top - 1 && a.bottom <= b.bottom + 1; }"""
        )
        check(f"{tag} Dr. Liu's photo beside his words", mount is True, mount)
        page.screenshot(path=os.path.join(OUT, f"rhythm-{tag}.png"))
        context.close()


def motion(browser):
    # Reduced motion: complete and still.
    context, page, response, errors, failed = open_page(browser, 1440, 900, reduced=True)
    scroll_through(page)
    still = page.evaluate(
        """() => ({ blooms: [...document.querySelectorAll('[data-bloom]')].filter(e => e.dataset.bloom !== 'done').length,
             hidden: [...document.querySelectorAll('main img')].filter(i => parseFloat(getComputedStyle(i).opacity) < 1).length,
             running: document.getAnimations().filter(a => { const t = a.effect && a.effect.target;
               return t && t.closest && t.closest('main') && !t.closest('[class*=greetings]'); }).length })"""
    )
    check("reduced motion: every painting shown, still", still["blooms"] == 0 and still["hidden"] == 0 and still["running"] == 0, still)
    context.close()

    # With motion: the opening's painting blooms on arrival; a lower painting waits, then blooms.
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="no-preference")
    page = context.new_page()
    page.goto(f"{BASE}/about", wait_until="domcontentloaded", timeout=120000)
    first = page.evaluate("document.querySelector('[data-part=\"opening\"] img').dataset.bloom ?? null")
    check("motion: the opening's painting starts waiting (server-marked)", first == "waiting", first)
    check("motion: the opening's painting blooms", wait_until(page, "document.querySelector('[data-part=\"opening\"] img').dataset.bloom === 'done'"))
    low = "document.querySelector('[data-part=\"experience\"] [data-picture] img')"
    state = page.evaluate(f"[{low}.dataset.bloom ?? null, getComputedStyle({low}).opacity]")
    check("motion: a lower painting waits out of view, hidden", state[0] == "waiting" and float(state[1]) == 0, state)
    page.evaluate(f"(() => {{ const i = {low}; window.scrollTo(0, i.getBoundingClientRect().top + window.scrollY - innerHeight / 2); }})()")
    check("motion: then it blooms", wait_until(page, f"{low}.dataset.bloom === 'done'"))
    context.close()

    # JavaScript off: every painting shows (nothing waits for a bloom that will not come).
    context = browser.new_context(viewport={"width": 1440, "height": 900}, java_script_enabled=False)
    page = context.new_page()
    page.goto(f"{BASE}/about", wait_until="load", timeout=120000)
    page.wait_for_timeout(1500)
    box = page.locator('[data-part="opening"] img').bounding_box()
    shot = Image.open(io.BytesIO(page.screenshot(clip=box))).convert("L")
    ink = sum(shot.histogram()[:180]) / (shot.width * shot.height)
    check("JavaScript off: the opening's painting is visible", ink >= 0.02, round(ink, 4))
    context.close()


def boundary(browser):
    for width in (719, 720):
        context, page, response, errors, failed = open_page(browser, width, 900, reduced=True)
        sideways = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
        check(f"{width} no sideways scrolling", sideways <= 0, sideways)
        r = page.evaluate(RHYTHM_JS, SIDES)
        if width == 719:
            firsts = {p: v and v["first"] for p, v in r.items()}
            check("719 one column: each picture first", all(f == "picture" for f in firsts.values()), firsts)
        else:
            sides = {p: v and v["side"] for p, v in r.items()}
            check("720 two columns: pictures on alternating sides", sides == SIDES, sides)
        context.close()


def first_screen(browser):
    for width, height in [(1280, 720), (1440, 900), (1536, 864), (390, 844)]:
        tag = f"{width}x{height}"
        context, page, response, errors, failed = open_page(browser, width, height, reduced=True)
        geo = page.evaluate(
            """() => ({ title: document.querySelector('h1').getBoundingClientRect().bottom,
                        picture: document.querySelector('[data-part="opening"] img').getBoundingClientRect().top, win: innerHeight })"""
        )
        check(f"{tag} the title and the top of the opening's picture in the first screen", geo["title"] <= geo["win"] and geo["picture"] < geo["win"], geo)
        context.close()
```

- [ ] **Step 2: Run it against D to see it fail**

Start the dev server (3025). Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/scripts/qa/qa_about.py http://localhost:3025 --only=rhythm`
Expected: FAIL lines (no `[data-part="opening"]` spreads; D's page is still there).

- [ ] **Step 3: Write the shared pieces**

Create `src/components/about/spread.tsx`:

```tsx
"use client";

import Image from "next/image";
import type { CSSProperties, ReactNode } from "react";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { drafts } from "./about-content";
import type { Art } from "./about-art";
import page from "./about-page.module.css";

// The About page's one rhythm (Mo, October 7, 2026: every part paired the same way): one picture,
// its words beside it, the sides swapping part by part. `side` is where the picture stands from
// 720px; on one column the picture always comes first. Paintings multiply onto the page's paper
// and bloom in as they arrive (the kit's useBloom); an opening painting is marked "waiting" by the
// server so it blooms on arrival instead of flashing.

export function Painting({
  art,
  alt,
  sizes,
  caption = false,
  gold,
  delay = 0,
  priority = false,
  waiting = false,
  className = "",
}: {
  art: Art;
  /** The painting's description (English source; translated through the catalogs), or "" when it only decorates. */
  alt: string;
  sizes: string;
  /** "Illustration" under a painting that pictures something (DESIGN.md honesty tags). */
  caption?: boolean;
  /** The painting's gold-leaf light mask (about-art.ts), for the kit's glint. */
  gold?: string;
  /** Milliseconds its bloom waits (the kit's --bloom-delay). */
  delay?: number;
  /** The first screen's painting: eager and preloaded. */
  priority?: boolean;
  /** Marked "waiting" by the server (an opening painting). */
  waiting?: boolean;
  className?: string;
}) {
  const copy = useCopy();
  return (
    <figure className={`${page.painting} ${className}`} data-picture="">
      <span className={page.paintingBody}>
        <Image
          className={base.ink}
          src={art.src}
          alt={alt ? copy(alt) : ""}
          width={art.width}
          height={art.height}
          sizes={sizes}
          priority={priority}
          data-bloom={waiting ? "waiting" : ""}
          style={delay ? ({ "--bloom-delay": delay } as CSSProperties) : undefined}
        />
        {gold ? (
          <span className={base.gold} style={{ ["--gold" as string]: `url(${gold})` }} />
        ) : null}
      </span>
      {caption ? (
        <figcaption className={base.caption}>{copy(drafts.illustration)}</figcaption>
      ) : null}
    </figure>
  );
}

export function Spread({
  id,
  part,
  side,
  labelledBy,
  picture,
  children,
}: {
  id: string;
  /** The part's name, for its hooks and its page's styles. */
  part: string;
  /** Where the picture stands from 720px. */
  side: "left" | "right";
  labelledBy: string;
  /** A Painting, or a figure marked data-picture. */
  picture: ReactNode;
  children: ReactNode;
}) {
  return (
    <section id={id} className={page.part} data-part={part} aria-labelledby={labelledBy}>
      <div className={`${base.wrap} ${page.spread}`} data-side={side}>
        {picture}
        <div className={page.words} data-words="">
          {children}
        </div>
      </div>
    </section>
  );
}
```

Create `src/components/about/about-page.module.css`: write the header comment and the rules below, then append the blocks copied from `git -C C:/Users/mcbig/Documents/codes/bigh-ink show 27e71b7:src/components/about/about-letter.module.css` listed after them, renaming every `.letterPage` to `.aboutPage`.

```css
/* About, shared by B "The album" and C "The circle" (Mo, October 7, 2026; spec
   docs/superpowers/specs/2026-10-05-ink-pages-design.md, "About (stage 1), October 7"). One
   rhythm for every part: one picture on one side, its words on the other, the sides swapping part
   by part (from 720px; one column below, picture first). The kit's plain rice paper, no folds.
   Every rule is scoped under .aboutPage (the page root, InkPage className), so it outranks the
   kit's .look rules and the homepage resets in any stylesheet order. Multiply: nothing between a
   painting and the page root may make a stacking context (no z-index on a positioned ancestor, no
   isolation, opacity, transform, filter or mask on a part, a spread, a figure or a wrapper). */

.aboutPage {
  --part-half: clamp(56px, 6vw, 112px);
  --gap: clamp(40px, 6vw, 112px);
}

/* The header floats over the opening (clear there), so the opening starts 88px down. */
.aboutPage .opening {
  padding: calc(88px + clamp(24px, 3.4vw, 64px)) 0 var(--part-half);
}

.aboutPage p.kicker {
  margin: 0 0 12px;
  color: var(--muted);
  font-size: 19px;
  font-weight: 450;
}

/* The name once: the title in plain ink at display size (no painted name, no unfolding acronym,
   which showed "BiGH" before the sentence). */
.aboutPage h1.title {
  margin: 0;
  font-family: var(--display-font);
  font-weight: var(--display-weight);
  font-size: clamp(min(44px, 11vw), 5.4vw, 84px);
  line-height: 1.02;
  letter-spacing: -0.03em;
  text-wrap: balance;
}

.aboutPage p.lead {
  margin: clamp(16px, 1.6vw, 24px) 0 0;
  color: var(--muted);
  font-size: clamp(19px, 1.5vw, 23px);
  line-height: 1.45;
}

.aboutPage .lead span {
  display: block;
}

.aboutPage .part {
  padding-block: var(--part-half);
  /* Deep links (/about#purpose): the part's first content lands 108px from the window's top, just
     under the settled bar; the document keeps 150px of scroll-padding-top (globals.css). */
  scroll-margin-top: calc(108px - 150px - var(--part-half));
}

/* One picture with its words. */
.aboutPage .spread {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  row-gap: clamp(24px, 5vw, 40px);
  align-items: center;
}

@media (min-width: 720px) {
  .aboutPage .spread {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    column-gap: var(--gap);
  }

  .aboutPage .spread[data-side="right"] > [data-picture] {
    order: 2;
  }
}

/* Each page sets --picture per part (its painting's width), so the pictures read about the same size. */
.aboutPage .painting {
  justify-self: center;
  width: min(100%, var(--picture, 520px));
  margin: 0;
}

.aboutPage .paintingBody {
  position: relative;
  display: block;
}

.aboutPage .paintingBody img {
  display: block;
  width: 100%;
  height: auto;
}

.aboutPage .painting figcaption {
  margin-top: 8px;
  text-align: right;
}

.aboutPage .actions {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  margin-top: clamp(28px, 2.6vw, 40px);
}
```

Blocks to copy (by selector, from D's file, `.letterPage` → `.aboutPage`): `p.label`; `h2.heading`; `h2.heading > span`; `.body`; `.more`; `.mount` and `.mount img`; `.figures`, `.figures > div`, `.figures dt`, `.figures dd`, `.figure`, `.unit`; the figures-in-a-row media block (`@media (min-width: 1200px), (min-width: 600px) and (max-width: 899px)`) with its comment, changing its condition to `@media (min-width: 1200px), (min-width: 600px) and (max-width: 719px)`; `.promise` with only its `text-align: center` (drop its `margin-top` and its `scroll-margin-top`: the section also carries `.part`, whose padding and scroll margin apply), `.promise h2.heading`, `.promises`, `.promiseDot` with its comment, `.promises h3`, `.promises p`, `.greetings` and its reduced-motion block with comments; the two promises media blocks (`600-1199`, `max-width: 599px`); the whole "Other languages" section (Korean keep-all, Japanese auto-phrase, `main:is(:lang(ja), :lang(zh))` strict, Chinese keep-all, the ja/zh heading sizes with their 900-959px block changed to `@media (min-width: 720px) and (max-width: 959px)`, the Vietnamese pill balance); and from the motion section only the bloom hold: the `[data-bloom="waiting"]` / `[data-bloom="in"]` / `@media (scripting: none)` rules with their comment (wrapped in `@media (prefers-reduced-motion: no-preference)`), the reduced-motion/no-script `filter: none` block (its selector becomes `:global([data-look="ink"]).aboutPage [data-bloom="waiting"]`) and `@keyframes bloom-hold`. Nothing else of D's file (no paper, folds, chapter words, rings, pool, closing word or writing motion).

Create `src/components/about/album.module.css`:

```css
/* About B, "The album" (Mo, October 7, 2026; mockup reference/ink-pages/mockups/about-b.png): an
   old painting album, each part a spread, the same rhythm throughout. Shared rules live in
   about-page.module.css; these are the album's own, scoped under .album (the page root carries both
   classes). */

.album [data-part="opening"] .painting {
  --picture: 600px;
}

.album [data-part="purpose"] .painting {
  --picture: 460px;
}

.album [data-part="roots"] .painting {
  --picture: 540px;
}

.album [data-part="experience"] .painting {
  --picture: 480px;
}

.album [data-part="closing"] .painting {
  --picture: 460px;
}

/* Dr. Liu's photo beside his paragraph, inside the words (as in the mockup). */
.album .rootsBody {
  display: grid;
  grid-template-columns: clamp(120px, 11vw, 168px) minmax(0, 1fr);
  gap: clamp(18px, 2vw, 28px);
  align-items: start;
  margin-top: clamp(18px, 1.8vw, 28px);
}

.album .rootsBody p {
  margin-top: 0;
}

/* The promise pictures: small vignettes over each promise, one caption under the row. */
.album .vignette {
  display: block;
  width: clamp(120px, 12vw, 184px);
  height: auto;
  margin: 0 auto 16px;
}

.album .rowCaption {
  margin-top: 18px;
  text-align: right;
}

@media (max-width: 719px) {
  .album .painting {
    --picture: 420px;
  }

  .album .rootsBody {
    grid-template-columns: 120px minmax(0, 1fr);
  }
}
```

- [ ] **Step 4: Write the album page**

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
import { about, routes } from "./about-content";
import { book, desk, lamp, seedling, sequoia, vignettes } from "./about-art";
import { CountUp } from "./count-up";
import { Greetings } from "./greetings";
import { Painting, Spread } from "./spread";
import page from "./about-page.module.css";
import styles from "./album.module.css";

// About B, "The album" (Mo, October 7, 2026; mockup reference/ink-pages/mockups/about-b.png; spec
// docs/superpowers/specs/2026-10-05-ink-pages-design.md, "About (stage 1), October 7"). An old
// painting album: every part a spread, one painting beside its words, the sides swapping. The name
// once (the logo, then the title). California, not zen. The words are the locked ones in
// about-content.ts.

export const ALT = {
  book: "An old open book, painted in ink, with a gold ribbon bookmark",
  seedling:
    "An oak seedling growing from an acorn, painted in ink; a gold acorn lies among its roots",
  desk: "A scientist's desk in ink: a brush on its rest, a microscope and a stack of books",
  sequoia: "An ancient giant sequoia rising from mist beside a young sequoia, painted in ink",
  lamp: "A desk lamp casting gold light onto an open journal, painted in ink",
} as const;

const PROMISE_ART = [vignettes.palms, vignettes.bee, vignettes.moon, vignettes.letter];
const HALF = "(max-width: 719px) 90vw, 46vw";

function sentences(text: string) {
  return text.match(/[^.!?。！？]+[.!?。！？]*\s*/gu)?.map((part) => part.trim()) ?? [text];
}

function Opening() {
  const copy = useCopy();
  return (
    <section className={page.opening} data-part="opening" aria-labelledby="about-title">
      <div className={`${base.wrap} ${page.spread}`} data-side="right">
        <Painting
          art={book}
          alt={ALT.book}
          sizes={HALF}
          gold={book.gold}
          caption
          priority
          waiting
        />
        <div className={page.words} data-words="">
          <p className={page.kicker}>{copy(about.hero.label)}</p>
          <h1 id="about-title" lang="en" className={page.title}>
            {about.hero.title}
          </h1>
          <p className={page.lead}>
            {sentences(copy(about.hero.lead)).map((sentence) => (
              <span key={sentence}>{sentence}</span>
            ))}
          </p>
        </div>
      </div>
    </section>
  );
}

function Purpose() {
  const copy = useCopy();
  return (
    <Spread
      id="purpose"
      part="purpose"
      side="left"
      labelledBy="purpose-title"
      picture={
        <Painting art={seedling} alt={ALT.seedling} sizes={HALF} gold={seedling.gold} caption />
      }
    >
      <p className={`${base.label} ${page.label}`} data-label="">
        {copy(about.purpose.label)}
      </p>
      <h2 id="purpose-title" className={`${base.display} ${page.heading}`}>
        {about.purpose.lines.map((line) => (
          <span key={line}>{copy(line)}</span>
        ))}
      </h2>
      <p className={page.body}>{copy(about.purpose.mission)}</p>
    </Spread>
  );
}

function Roots() {
  const copy = useCopy();
  return (
    <Spread
      id="roots"
      part="roots"
      side="right"
      labelledBy="roots-title"
      picture={<Painting art={desk} alt={ALT.desk} sizes={HALF} caption />}
    >
      <p className={`${base.label} ${page.label}`} data-label="">
        {copy(about.roots.label)}
      </p>
      <h2 id="roots-title" className={`${base.display} ${page.heading}`}>
        {copy(about.roots.title)}
      </h2>
      <div className={styles.rootsBody}>
        <span className={page.mount} data-mount="">
          <Image
            src={liu.src}
            alt={copy(about.roots.photo.alt)}
            width={liu.width}
            height={liu.height}
            sizes="168px"
          />
        </span>
        <div>
          <p className={page.body}>{copy(about.roots.text)}</p>
          <Link href={routes.scientists} className={`${base.pill} ${base.pillGhost} ${page.more}`}>
            {copy(about.roots.link)} <ArrowRight size={18} aria-hidden="true" />
          </Link>
        </div>
      </div>
    </Spread>
  );
}

function Experience() {
  const copy = useCopy();
  const years = copy(about.experience.stats[1].unit);
  return (
    <Spread
      id="experience"
      part="experience"
      side="left"
      labelledBy="experience-title"
      picture={
        <Painting art={sequoia} alt={ALT.sequoia} sizes={HALF} gold={sequoia.gold} caption />
      }
    >
      <p className={`${base.label} ${page.label}`} data-label="">
        {copy(about.experience.label)}
      </p>
      <h2 id="experience-title" className={`${base.display} ${page.heading}`}>
        {copy(about.experience.title)}
      </h2>
      <dl className={page.figures}>
        <div>
          <dt>{copy(about.roots.stat.label)}</dt>
          <dd>
            <CountUp to={280} suffix="+" className={page.figure} />
          </dd>
        </div>
        <div>
          <dt>{copy(about.experience.stats[0].label)}</dt>
          <dd>
            <span className={page.figure}>{about.experience.stats[0].value}</span>
          </dd>
        </div>
        <div>
          <dt>{copy(about.experience.stats[1].label)}</dt>
          <dd>
            <CountUp to={20} suffix="+" className={page.figure} />
            <span className={page.unit}> {years}</span>
          </dd>
        </div>
      </dl>
    </Spread>
  );
}

function Promises() {
  const copy = useCopy();
  return (
    <section
      id="promise"
      className={`${page.part} ${page.promise}`}
      data-part="promise"
      aria-labelledby="promise-title"
    >
      <div className={base.wrap}>
        <p className={`${base.label} ${page.label}`} data-label="">
          {copy(about.promise.label)}
        </p>
        <h2 id="promise-title" className={`${base.display} ${page.heading}`}>
          {copy(about.promise.title)}
        </h2>
        <ul className={page.promises}>
          {about.promise.items.map((item, i) => (
            <li key={item.title} data-promise="">
              <Image
                className={`${base.ink} ${styles.vignette}`}
                src={PROMISE_ART[i].src}
                alt=""
                width={PROMISE_ART[i].width}
                height={PROMISE_ART[i].height}
                sizes="184px"
                data-bloom=""
                style={{ "--bloom-delay": i * 220 } as CSSProperties}
              />
              <h3>{copy(item.title)}</h3>
              <p>{copy(item.text)}</p>
              {i === 3 && <Greetings className={page.greetings} />}
            </li>
          ))}
        </ul>
        <p className={`${base.caption} ${styles.rowCaption}`} data-row-caption="">
          {copy("Illustrations")}
        </p>
      </div>
    </section>
  );
}

function Closing() {
  const copy = useCopy();
  const dialogs = useSiteDialogs();
  return (
    <Spread
      id="closing"
      part="closing"
      side="right"
      labelledBy="closing-title"
      picture={<Painting art={lamp} alt={ALT.lamp} sizes={HALF} gold={lamp.gold} caption />}
    >
      <h2 id="closing-title" className={`${base.display} ${page.heading}`}>
        {copy(about.closing.title)}
      </h2>
      <p className={page.body}>{copy(about.closing.text)}</p>
      <div className={page.actions}>
        <button type="button" className={base.pill} onClick={dialogs.openAsk}>
          {copy(about.closing.primary)}
        </button>
        <Link href={routes.products} className={`${base.pill} ${base.pillGhost}`}>
          {copy(about.closing.secondary)}
        </Link>
      </div>
    </Spread>
  );
}

export function AboutInk() {
  return (
    <InkPage current="about" className={`${page.aboutPage} ${styles.album}`}>
      {() => (
        <div data-about="album">
          <Opening />
          <Purpose />
          <Roots />
          <Experience />
          <Promises />
          <Closing />
        </div>
      )}
    </InkPage>
  );
}
```

- [ ] **Step 5: Remove D's page files and fix the words file's header**

```bash
git -C C:/Users/mcbig/Documents/codes/bigh-ink rm src/components/about/chapter-word.tsx src/components/about/about-letter.module.css src/components/about/letter-art.ts src/components/about/acronym.tsx src/components/about/acronym.module.css
git -C C:/Users/mcbig/Documents/codes/bigh-ink rm -r public/images/about-ink
```

In `src/components/about/about-content.ts`, replace the comment lines that begin `// The page is "The name, on a folded letter"` (two lines) with:

```ts
// The page is About B, "The album" (October 7, 2026), with C "The circle" built beside it on its own
// branch. Before them: D (the folded letter, branch ink-pages), the first ink About (git history, up
// to c30a489) and the Glass page
```

keeping the line that follows (`// with opening 3 and Switzer on Sept 28, 2026) is in the backup zip named in docs/about-page.md.`), so the sentence still ends there.

Run: `npx --prefix C:/Users/mcbig/Documents/codes/bigh-ink tsc --noEmit -p C:/Users/mcbig/Documents/codes/bigh-ink`
Expected: no errors. (`grep -rn "acronym\|letter-art\|chapter-word\|about-letter" C:/Users/mcbig/Documents/codes/bigh-ink/src` must find nothing.)

- [ ] **Step 6: Run the checks**

Restart the dev server (files were added and deleted). Run the whole file: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/scripts/qa/qa_about.py http://localhost:3025`
Expected: `N/N passed`. Fix the page (sizes, gaps, `--picture`), never a check. If the pictures-same-size check fails, set `--picture` per part in `album.module.css` until the painted heights sit within the band.

- [ ] **Step 7: Look like a visitor**

Read every `scripts/qa/out/about-album/1440x900-*.png`, `390x844-*.png` and `rhythm-*.png` at full size against `reference/ink-pages/mockups/about-b.png`. Expected: one calm album, a steady left-right rhythm, no box around any painting, Dr. Liu's photo beside his words, nothing crowded. Score it out of 10 honestly in the report; fix layout that keeps it under 9.

- [ ] **Step 8: Lint, format, commit**

```bash
npx --prefix C:/Users/mcbig/Documents/codes/bigh-ink prettier --write C:/Users/mcbig/Documents/codes/bigh-ink/src/components/about
npm --prefix C:/Users/mcbig/Documents/codes/bigh-ink run lint
git -C C:/Users/mcbig/Documents/codes/bigh-ink add -A src/components/about scripts/qa/qa_about.py public/images
git -C C:/Users/mcbig/Documents/codes/bigh-ink commit -m "feat(about): B, the album

One rhythm for every part: a painting beside its words, sides swapping;
the name once; plain rice paper; California paintings. Shared Spread and
Painting pieces and about-page.module.css for both new pages. Replaces D.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: B in five languages, deep links, the built site, the notes

**Files:**

- Create: `reference/ink-pages/about-bc/translations-b.cjs`
- Modify: `src/i18n/copy-keys.json`, `messages/{en,cns,kr,vn,jp}.json` (the script writes them), `scripts/qa/qa_about.py` (four groups), `src/components/about/*.css` (only for faults found), `docs/about-page.md`

**Interfaces:**

- Consumes: `ALT` (Task 2), the QA hooks of Task 2.
- Produces: catalog entries for the five `ALT` strings (Task 4 reuses the seedling and sequoia ones).

- [ ] **Step 1: Add the language and deep-link checks**

Add to `scripts/qa/qa_about.py` above `GROUPS`, extend `GROUPS` to `[desktop_and_phone, rhythm, motion, focus, deep_links, languages, languages_layout, nav_locales, boundary, first_screen]`, and add the four names and these lines to the docstring: "deep_links (1440x900, 1024x768, 768x1024, 390x844, 360x780): /about#purpose, #roots, #experience, #promise, #closing land the part's first content 0-64px under the header, its heading in the window. languages (kr, jp, cns, vn): 200, no console errors, the h1 English, no English source sentence left, the paintings' descriptions translated. languages_layout (every language at 1440x900, 1024x768, 768x1024, 600x900, 390x844, 360x780; jp and cns also 900x900): no word crosses the side margins; no words over a painting; in kr, jp, cns, vn no bad line break; jp and cns heading phrases whole on a phone and at 900; Vietnamese at 390: the closing pills balance their lines. nav_locales: from /vn/about and /kr/about the bar and menu stay in the language."

```python
LANDING_JS = """(id) => {
  const s = document.getElementById(id);
  const tops = [...s.querySelectorAll('[data-picture], [data-label], h2')].filter(e => e.offsetParent).map(e => e.getBoundingClientRect().top);
  const head = document.getElementById(id + '-title').getBoundingClientRect();
  const bar = document.querySelector('header').getBoundingClientRect();
  return { scrollY: Math.round(window.scrollY), bar: Math.round(bar.bottom), first: Math.round(Math.min(...tops)),
           headTop: Math.round(head.top), headBottom: Math.round(head.bottom), win: window.innerHeight };
}"""


def deep_links(browser):
    # One browser context per size: a first visit warms the fonts into the cache, then every deep
    # link is a fresh load.
    for width, height in [(1440, 900), (1024, 768), (768, 1024), (390, 844), (360, 780)]:
        context = browser.new_context(viewport={"width": width, "height": height}, reduced_motion="no-preference")
        warm = context.new_page()
        warm.goto(f"{BASE}/about", wait_until="networkidle", timeout=120000)
        warm.evaluate("document.fonts.ready.then(() => true)")
        warm.close()
        for anchor in ["purpose", "roots", "experience", "promise", "closing"]:
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
        h1 = page.evaluate("[document.querySelector('h1').textContent.trim(), document.querySelector('h1').lang]")
        check(f"{lang} the h1 stays English", h1 == ["Be in Good Health.", "en"], h1)
        text = page.evaluate("document.querySelector('main').innerText")
        left = [line for line in english if line in text]
        check(f"{lang} no English sentence left", not left, left[:3])
        alts = page.evaluate("[...document.querySelectorAll('[data-picture] img')].map(i => i.alt).filter(a => a)")
        check(f"{lang} the paintings' descriptions translated", alts and not any(" painted in ink" in a or a.startswith("An ") or a.startswith("A ") for a in alts), alts)
        check(f"{lang} no console errors or warnings", not errors, errors[:3])
        page.screenshot(path=os.path.join(OUT, f"{lang}-opening.png"))
        context.close()


def languages_layout(browser):
    """Each language at desktop, tablet and phone sizes: no word crosses the side margins, no
    words over a painting, and in Korean, Japanese, Chinese and Vietnamese no bad line break.
    Japanese and Chinese also at 900x900, and on a phone and at 900px no heading phrase is split."""
    for lang in ["en", "kr", "jp", "cns", "vn"]:
        sizes = [(1440, 900), (1024, 768), (768, 1024), (600, 900), (390, 844), (360, 780)]
        if lang in ("jp", "cns"):
            sizes.append((900, 900))
        for width, height in sizes:
            tag = f"{lang} {width}x{height}"
            path = "/about" if lang == "en" else f"/{lang}/about"
            context, page, response, errors, failed = open_page(browser, width, height, path=path, reduced=True)
            over = page.evaluate(MARGINS_JS)
            check(f"{tag} words inside the margins", not over, over[:3])
            hits = page.evaluate(OVERLAP_JS)
            check(f"{tag} no words over a painting", not hits, hits[:3])
            if lang != "en":
                bad = page.evaluate(BREAKS_JS, lang)
                check(f"{tag} no bad line break", not bad, bad[:3])
            if lang in ("jp", "cns") and width in (390, 360, 900):
                phrases = page.evaluate(PHRASES_JS, lang)
                check(
                    f"{tag} no heading phrase is broken across lines ({phrases['examined']} read)",
                    phrases["examined"] > 0 and not phrases["split"],
                    phrases,
                )
            if lang == "vn" and width == 390:
                pills = page.evaluate(
                    """[...document.querySelectorAll('main [class*=actions] a, main [class*=actions] button')].map(e => {
                         const r = document.createRange(); r.selectNodeContents(e);
                         const widths = {}; for (const x of r.getClientRects()) if (x.width > 4) widths[Math.round(x.top)] = (widths[Math.round(x.top)] || 0) + x.width;
                         return { wrap: getComputedStyle(e).textWrap, widths: Object.values(widths).map(Math.round) }; })"""
                )
                check(f"{tag} closing pills balance their lines (computed text-wrap)", len(pills) == 2 and all(p["wrap"] == "balance" for p in pills), pills)
                two = [p["widths"] for p in pills if len(p["widths"]) == 2]
                check(f"{tag} the pill's two lines are even", not two or all(min(w) / max(w) >= 0.6 for w in two), pills)
            context.close()
```

- [ ] **Step 2: Run them to see what fails**

Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/scripts/qa/qa_about.py http://localhost:3025 --only=deep_links,languages,languages_layout,nav_locales`
Expected: at least the four "the paintings' descriptions translated" FAILs. Note the others.

- [ ] **Step 3: Translate the five descriptions**

Create `reference/ink-pages/about-bc/translations-b.cjs` with the same body as `reference/ink-pages/about/translations.cjs` (read it: keys file, five catalogs, next id, writes back) and these rows ([en, cns, kr, vn, jp]; DRAFT, for a native check):

```js
const entries = [
  [
    "An old open book, painted in ink, with a gold ribbon bookmark",
    "一本水墨绘制的旧书，夹着金色丝带书签。",
    "금색 리본 책갈피가 끼워진, 먹으로 그린 오래된 펼친 책.",
    "Một cuốn sách cũ mở ra, vẽ bằng mực, với dải ruy băng đánh dấu màu vàng.",
    "金色のしおり紐をはさんだ、墨で描いた古い本。",
  ],
  [
    "An oak seedling growing from an acorn, painted in ink; a gold acorn lies among its roots",
    "水墨绘制的橡树幼苗从橡子中长出，根间有一颗金色的橡子。",
    "도토리에서 자라난 참나무 새싹을 먹으로 그린 그림. 뿌리 사이에 금빛 도토리가 있습니다.",
    "Cây sồi non mọc lên từ quả sồi, vẽ bằng mực; một quả sồi vàng nằm giữa rễ cây.",
    "どんぐりから芽吹いたオークの若木を墨で描いた絵。根のあいだに金色のどんぐりがあります。",
  ],
  [
    "A scientist's desk in ink: a brush on its rest, a microscope and a stack of books",
    "水墨绘制的科学家书桌：笔架上的毛笔、显微镜和一摞书。",
    "먹으로 그린 과학자의 책상: 붓걸이의 붓, 현미경, 쌓인 책.",
    "Bàn làm việc của nhà khoa học vẽ bằng mực: cây bút lông trên giá, kính hiển vi và chồng sách.",
    "墨で描いた研究者の机。筆置きの筆、顕微鏡、積まれた本。",
  ],
  [
    "An ancient giant sequoia rising from mist beside a young sequoia, painted in ink",
    "水墨绘制的古老巨杉从雾中升起，旁边是一棵年轻的巨杉。",
    "안개 속에서 솟은 오래된 자이언트 세쿼이아와 그 옆의 어린 세쿼이아를 먹으로 그린 그림.",
    "Cây cự sam cổ thụ vươn lên giữa sương mù bên cạnh một cây cự sam non, vẽ bằng mực.",
    "霧の中にそびえる古いジャイアントセコイアと、その隣の若いセコイアを墨で描いた絵。",
  ],
  [
    "A desk lamp casting gold light onto an open journal, painted in ink",
    "水墨绘制的台灯，在打开的笔记本上投下金色的光。",
    "펼친 노트 위로 금빛을 비추는 탁상 램프를 먹으로 그린 그림.",
    "Chiếc đèn bàn chiếu ánh vàng lên cuốn sổ đang mở, vẽ bằng mực.",
    "開いたノートに金色の光を落とすデスクランプを墨で描いた絵。",
  ],
];
```

Run it with Node's working directory at the worktree: `node -e "process.chdir('C:/Users/mcbig/Documents/codes/bigh-ink'); require('C:/Users/mcbig/Documents/codes/bigh-ink/reference/ink-pages/about-bc/translations-b.cjs')"`. Expected: five `m5NN …` lines. Then `npx --prefix C:/Users/mcbig/Documents/codes/bigh-ink prettier --write` on `src/i18n/copy-keys.json` and the five catalogs.

- [ ] **Step 4: Fix what the checks found; run the whole file**

Fix layout faults in the CSS (per-language sizes, column widths, scroll margins), never the checks. Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/scripts/qa/qa_about.py http://localhost:3025` → Expected: `N/N passed`.

- [ ] **Step 5: The built site and the homepage gate**

Stop the dev server. Delete `.next/cache/images` and `.next/dev/cache/images`. Build, start on 3026, then run on 3026: `qa_about.py` (all pass), `home_snapshot.py compare http://localhost:3026 bc-b-prod baseline-main997-prod` (PASS), `qa_home_ink.py http://localhost:3026` (all pass), `home_snapshot.py nav http://localhost:3026 -` (ok). Take viewport screenshots at 1536x864, 1440x900, 1280x720, 1024x768, 768x1024, 390x844 and 360x780 (scrolling, motion on, waiting for each painting to bloom) into `scripts/qa/out/about-album-built/`, read every one full size, score per size honestly, fix what keeps a size under 9, re-run. Stop the server.

- [ ] **Step 6: The notes**

At the top of `docs/about-page.md` (under its title) add a section "## Current page: B, "The album" (October 7, 2026)" describing: the album (each part a spread, the paintings and what each means, the rhythm, the name once, plain paper), the files (`about-ink.tsx`, `spread.tsx`, `about-page.module.css`, `album.module.css`, `about-art.ts` generated by `reference/ink-pages/about-bc/build_bc.py`), the checks (`scripts/qa/qa_about.py`, its count on dev and built), the draft translations (the five painting descriptions, keys from translations-b.cjs, for a native check), and that C "The circle" is built beside it on branch `about-c` and D on `ink-pages`. Mark the existing D section as replaced.

- [ ] **Step 7: Commit**

```bash
npx --prefix C:/Users/mcbig/Documents/codes/bigh-ink prettier --write C:/Users/mcbig/Documents/codes/bigh-ink/src/components/about C:/Users/mcbig/Documents/codes/bigh-ink/docs/about-page.md
git -C C:/Users/mcbig/Documents/codes/bigh-ink add -A reference/ink-pages/about-bc/translations-b.cjs src/i18n/copy-keys.json messages src/components/about scripts/qa/qa_about.py docs/about-page.md
git -C C:/Users/mcbig/Documents/codes/bigh-ink commit -m "feat(about): the album in five languages, deep links, checked built

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: C "The circle" page, with its checks and the circle that paints itself

**Files:**

- Create: `src/components/about/circle.module.css`
- Rewrite: `src/components/about/about-ink.tsx`
- Modify: `scripts/qa/qa_about.py` (album groups → circle groups)
- Delete: `src/components/about/album.module.css`

**Interfaces:**

- Consumes: `Painting`, `Spread`, `about-page.module.css` (Task 2, unchanged); `about-art.ts` (`seedling`, `sequoia`, `enso`, `hills`, `glasses`, `pool`, `dots`); `ALT.seedling`, `ALT.sequoia` strings (translated in Task 3).
- Produces: `[data-about="circle"]`; `[data-enso]` (the opening circle's figure; its painting `img` and its gold `[data-dot]`); `[data-picture-band]` on the hills image; `[data-pool]` on the pool image.

- [ ] **Step 1: Create the branch**

Run: `git -C C:/Users/mcbig/Documents/codes/bigh-ink switch -c about-c` (from `about-b`'s head; no files change).

- [ ] **Step 2: Change the QA file for the circle (failing first)**

In `scripts/qa/qa_about.py`:

- `OUT` ends in `"about-circle"`; the docstring's first line becomes `"""QA for About C, "The circle" (Mo, October 7, 2026; mockup reference/ink-pages/mockups/about-c.png;` and every "album" mention in it becomes "circle"; its motion paragraph becomes: "motion: reduced motion complete and still (the circle whole, its gold up, every painting shown); with motion the circle paints itself around in one breath from where the brush began, then its gold comes up, and the hills bloom; a lower painting waits, then blooms; with JavaScript off the circle shows whole".
- `DESIGN = "circle"`.
- `SIDES = {"purpose": "left", "roots": "right", "experience": "left", "closing": "right"}` (the opening is centred).
- In `rhythm`: the "Illustrations under the promise row" check is replaced by `check(f"{tag} no caption under the promise dots", row_caption is None, row_caption)`; the Illustration-captions check uses `want_captions = {"purpose": ["Illustration"], "roots": [], "experience": ["Illustration"], "closing": ["Illustration"]}` and `captions == want_captions`; the Dr. Liu check becomes:

```python
        liu = page.evaluate(
            """() => { const p = document.querySelector('[data-pool]'), f = document.querySelector('[data-mount] img');
                 if (!p || !f) return null; const a = p.getBoundingClientRect(), b = f.getBoundingClientRect();
                 return { dx: (b.left + b.width / 2 - a.left - a.width / 2) / a.width, dy: (b.top + b.height / 2 - a.top - a.height / 2) / a.height }; }"""
        )
        check(f"{tag} Dr. Liu's photo in the middle of its pool", liu is not None and abs(liu["dx"]) <= 0.15 and abs(liu["dy"]) <= 0.15, liu)
        once_circle = page.evaluate("document.querySelectorAll('main img[src*=\"enso\"]').length")
        check(f"{tag} the circle appears once", once_circle == 1, once_circle)
```

- In `first_screen` the opening's picture is the circle: `document.querySelector('[data-enso] img')`.
- In `desktop_and_phone` the eager check reads `[data-enso] img`.
- `motion` is replaced by:

```python
def motion(browser):
    # Reduced motion: complete and still.
    context, page, response, errors, failed = open_page(browser, 1440, 900, reduced=True)
    scroll_through(page)
    still = page.evaluate(
        """() => { const e = document.querySelector('[data-enso] img'), d = document.querySelector('[data-enso] [data-dot]');
             return { blooms: [...document.querySelectorAll('[data-bloom]')].filter(x => x.dataset.bloom !== 'done').length,
                      hidden: [...document.querySelectorAll('main img')].filter(i => parseFloat(getComputedStyle(i).opacity) < 1).length,
                      draw: getComputedStyle(e).animationName, mask: getComputedStyle(e).maskImage, dot: getComputedStyle(d).opacity,
                      running: document.getAnimations().filter(a => { const t = a.effect && a.effect.target;
                        return t && t.closest && t.closest('main') && !t.closest('[class*=greetings]'); }).length }; }"""
    )
    check("reduced motion: the circle whole, its gold up, every painting shown, still",
          still["blooms"] == 0 and still["hidden"] == 0 and still["draw"] == "none" and still["mask"] == "none"
          and float(still["dot"]) == 1 and still["running"] == 0, still)
    context.close()

    # With motion: the circle paints itself in one breath, then its gold; the hills bloom.
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="no-preference")
    page = context.new_page()
    page.goto(f"{BASE}/about", wait_until="domcontentloaded", timeout=120000)
    wait_until(page, "getComputedStyle(document.querySelector('[data-enso] img')).animationName !== 'none'", 5000)
    early = page.evaluate(
        """() => { const e = getComputedStyle(document.querySelector('[data-enso] img'));
             return { name: e.animationName, duration: e.animationDuration, start: e.getPropertyValue('--start').trim(),
                      dot: getComputedStyle(document.querySelector('[data-enso] [data-dot]')).opacity,
                      delay: parseFloat(getComputedStyle(document.querySelector('[data-enso] [data-dot]')).animationDelay) }; }"""
    )
    check("motion: the circle paints itself (its animation, one breath, from where the brush began)",
          "draw" in early["name"] and early["duration"] == "2.4s" and early["start"].endswith("deg"), early)
    check("motion: its gold waits for the stroke", float(early["dot"]) < 0.5 and early["delay"] >= 2.4, early)
    check("motion: then the gold is up", wait_until(page, "getComputedStyle(document.querySelector('[data-enso] [data-dot]')).opacity === '1'"))
    check("motion: the hills bloom", wait_until(page, "document.querySelector('[data-picture-band]').dataset.bloom === 'done'"))
    low = "document.querySelector('[data-part=\"experience\"] [data-picture] img')"
    state = page.evaluate(f"[{low}.dataset.bloom ?? null, getComputedStyle({low}).opacity]")
    check("motion: a lower painting waits out of view, hidden", state[0] == "waiting" and float(state[1]) == 0, state)
    page.evaluate(f"(() => {{ const i = {low}; window.scrollTo(0, i.getBoundingClientRect().top + window.scrollY - innerHeight / 2); }})()")
    check("motion: then it blooms", wait_until(page, f"{low}.dataset.bloom === 'done'"))
    context.close()

    # JavaScript off: the circle shows whole (its stroke is pure CSS).
    context = browser.new_context(viewport={"width": 1440, "height": 900}, java_script_enabled=False)
    page = context.new_page()
    page.goto(f"{BASE}/about", wait_until="load", timeout=120000)
    page.wait_for_timeout(4000)
    box = page.locator("[data-enso] img").bounding_box()
    shot = Image.open(io.BytesIO(page.screenshot(clip=box))).convert("L")
    ink = sum(shot.histogram()[:120]) / (shot.width * shot.height)
    check("JavaScript off: the circle is visible", ink >= 0.04, round(ink, 4))
    context.close()
```

Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/scripts/qa/qa_about.py http://localhost:3025 --only=rhythm,motion` → Expected: FAILs (the album is still the page).

- [ ] **Step 3: Write the circle's styles**

`git -C C:/Users/mcbig/Documents/codes/bigh-ink rm src/components/about/album.module.css`, then create `src/components/about/circle.module.css`:

```css
/* About C, "The circle" (Mo, October 7, 2026; mockup reference/ink-pages/mockups/about-c.png): one
   circle brushed in a single stroke (a whole, complete life) opens the page, once only; then the
   same rhythm as every About page. Shared rules live in about-page.module.css; these are the
   circle's own, scoped under .circle (the page root carries both classes). */

.circle .opening {
  text-align: center;
}

.circle .openingWords {
  display: grid;
  justify-items: center;
}

.circle .enso {
  position: relative;
  width: clamp(200px, 24vw, 360px);
  margin: 0 0 clamp(16px, 2vw, 28px);
}

.circle .enso img {
  display: block;
  width: 100%;
  height: auto;
}

.circle .dot {
  position: absolute;
  max-width: none;
  height: auto;
}

.circle .hills {
  display: block;
  width: 100%;
  height: auto;
  margin-top: clamp(8px, 1.4vw, 24px);
}

.circle [data-part="purpose"] .painting {
  --picture: 440px;
}

.circle [data-part="experience"] .painting {
  --picture: 460px;
}

.circle [data-part="closing"] .painting {
  --picture: 420px;
}

/* Dr. Liu's photo on its mat, resting on a wide, low pool of grey wash (D's pool, laid on its
   side: a wash has no up or down). --pool-ratio is the pool's height over its width. */
.circle .print {
  --mat: clamp(180px, 15vw, 240px);
  position: relative;
  justify-self: center;
  width: var(--mat);
  margin: calc(var(--mat) * 0.3) 0;
}

.circle .pool {
  position: absolute;
  top: 50%;
  left: 50%;
  width: calc(var(--mat) * 1.25 * 1.6);
  max-width: none;
  height: auto;
  translate: -50% -50%;
  rotate: 90deg;
  pointer-events: none;
}

@media (max-width: 719px) {
  .circle .painting {
    --picture: 400px;
  }

  .circle .print {
    --mat: 200px;
  }
}

/* ---- The circle paints itself: one stroke around in one breath, from where the brush began --
   A conic mask sweeps around from --start (about-art.ts enso.startDeg), its leading edge soft.
   It is pure CSS, so it never waits on a script; once the sweep ends the mask is whole (--sweep's
   initial value is 360deg), so the circle never depends on the animation finishing. The gold
   start comes up after. Reduced motion: no mask, no animation. */
@property --sweep {
  syntax: "<angle>";
  inherits: false;
  initial-value: 360deg;
}

@media (prefers-reduced-motion: no-preference) {
  .circle .enso .paint {
    -webkit-mask-image: conic-gradient(
      from var(--start),
      #000 var(--sweep),
      transparent calc(var(--sweep) + 6deg)
    );
    mask-image: conic-gradient(
      from var(--start),
      #000 var(--sweep),
      transparent calc(var(--sweep) + 6deg)
    );
    animation: draw var(--breath) var(--ease) 0.3s backwards;
  }

  .circle .enso .dot {
    animation: leaf-up 1.2s var(--ease) calc(0.3s + var(--breath)) backwards;
  }

  /* The hills spread from the middle as the stroke closes. */
  .circle .hills {
    --bloom-delay: 1400;
  }
}

@keyframes draw {
  from {
    --sweep: 0deg;
  }

  to {
    --sweep: 360deg;
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

- [ ] **Step 4: Write the circle page**

Replace `src/components/about/about-ink.tsx` with the same file as Task 2 Step 4, except:

- the header comment describes C ("About C, "The circle" (Mo, October 7, 2026; mockup reference/ink-pages/mockups/about-c.png; …). One circle brushed in a single stroke (a whole, complete life) opens the page, once only; then the same rhythm as the album: one picture beside its words, the sides swapping. California, not zen.");
- imports: `import { dots, enso, glasses, hills, pool, seedling, sequoia } from "./about-art";` and `import styles from "./circle.module.css";` (no `book`, `desk`, `lamp`, `vignettes`);
- `ALT` keeps `seedling` and `sequoia` and adds `glasses: "Reading glasses resting on an open notebook, painted in ink"` (no book, desk, lamp);
- `Opening` becomes:

```tsx
function Opening() {
  const copy = useCopy();
  return (
    <section
      className={`${page.opening} ${styles.opening}`}
      data-part="opening"
      aria-labelledby="about-title"
    >
      <div className={`${base.wrap} ${styles.openingWords}`}>
        <span className={styles.enso} data-enso="" aria-hidden="true">
          <Image
            className={`${base.ink} ${styles.paint}`}
            src={enso.src}
            alt=""
            width={enso.width}
            height={enso.height}
            sizes="(max-width: 719px) 60vw, 360px"
            priority
            style={{ "--start": `${enso.startDeg}deg` } as CSSProperties}
          />
          <Image
            className={styles.dot}
            src={enso.dot.src}
            alt=""
            width={enso.dot.width}
            height={enso.dot.height}
            sizes="48px"
            priority
            data-dot=""
            style={{
              left: `${enso.dot.left * 100}%`,
              top: `${enso.dot.top * 100}%`,
              width: `${enso.dot.size * 100}%`,
            }}
          />
        </span>
        <p className={page.kicker}>{copy(about.hero.label)}</p>
        <h1 id="about-title" lang="en" className={page.title}>
          {about.hero.title}
        </h1>
        <p className={page.lead}>
          {sentences(copy(about.hero.lead)).map((sentence) => (
            <span key={sentence}>{sentence}</span>
          ))}
        </p>
      </div>
      <Image
        className={`${base.ink} ${styles.hills}`}
        src={hills.src}
        alt=""
        width={hills.width}
        height={hills.height}
        sizes="100vw"
        data-bloom="waiting"
        data-picture-band=""
      />
    </section>
  );
}
```

(`styles.paint` is the class circle.module.css's motion rules name the stroke by; `.circle .enso img` already sizes it);

- `Roots` keeps its words but its picture is Dr. Liu on the pool, and its words lose `rootsBody` (photo now in the picture):

```tsx
function Roots() {
  const copy = useCopy();
  return (
    <Spread
      id="roots"
      part="roots"
      side="right"
      labelledBy="roots-title"
      picture={
        <figure className={styles.print} data-picture="">
          <Image
            className={`${base.ink} ${styles.pool}`}
            src={pool.src}
            alt=""
            width={pool.width}
            height={pool.height}
            sizes="(max-width: 719px) 90vw, 560px"
            data-pool=""
            data-bloom=""
          />
          <span className={page.mount} data-mount="">
            <Image
              src={liu.src}
              alt={copy(about.roots.photo.alt)}
              width={liu.width}
              height={liu.height}
              sizes="240px"
            />
          </span>
        </figure>
      }
    >
      <p className={`${base.label} ${page.label}`} data-label="">
        {copy(about.roots.label)}
      </p>
      <h2 id="roots-title" className={`${base.display} ${page.heading}`}>
        {copy(about.roots.title)}
      </h2>
      <p className={page.body}>{copy(about.roots.text)}</p>
      <Link href={routes.scientists} className={`${base.pill} ${base.pillGhost} ${page.more}`}>
        {copy(about.roots.link)} <ArrowRight size={18} aria-hidden="true" />
      </Link>
    </Spread>
  );
}
```

- `Promises`' list items use the dots: `<Image className={`${base.ink} ${page.promiseDot}`} src={dots[i].src} alt="" width={dots[i].width} height={dots[i].height} sizes="92px" data-bloom="" style={{ "--bloom-delay": i * 260 } as CSSProperties} />`, and there is no row caption (`PROMISE_ART` and the caption `<p>` go);
- `Closing`'s picture is `<Painting art={glasses} alt={ALT.glasses} sizes={HALF} caption />`;
- `AboutInk` uses `className={`${page.aboutPage} ${styles.circle}`}` and `<div data-about="circle">`.

Run `npx --prefix C:/Users/mcbig/Documents/codes/bigh-ink tsc --noEmit -p C:/Users/mcbig/Documents/codes/bigh-ink` → no errors.

- [ ] **Step 5: Run the checks**

Restart the dev server. Run the whole file → Expected: `N/N passed`. Fix the page, never a check.

- [ ] **Step 6: Watch the circle like a visitor**

Take viewport screenshots of the opening at 0.5s, 1.1s, 1.7s, 2.4s and 3.6s after load (1440x900, motion on) and read them at full size. Expected: the circle is drawn around from its gold start in one even stroke (no flash of the whole circle first, no hard clock-hand look; if the leading edge looks mechanical, widen the 6deg feather), the gold comes up after, the hills spread. Then read every `scripts/qa/out/about-circle/1440x900-*.png`, `390x844-*.png` and `rhythm-*.png` against the mockup and score honestly; fix layout that keeps it under 9.

- [ ] **Step 7: Lint, format, commit**

```bash
npx --prefix C:/Users/mcbig/Documents/codes/bigh-ink prettier --write C:/Users/mcbig/Documents/codes/bigh-ink/src/components/about
npm --prefix C:/Users/mcbig/Documents/codes/bigh-ink run lint
git -C C:/Users/mcbig/Documents/codes/bigh-ink add -A src/components/about scripts/qa/qa_about.py
git -C C:/Users/mcbig/Documents/codes/bigh-ink commit -m "feat(about): C, the circle

One circle painted in a single stroke opens the page, once only, and draws
itself in one breath from its gold start; then the album's rhythm with the
oak seedling, Dr. Liu on a pool of wash, the sequoia, ink dots and reading
glasses.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: C in five languages, the built site, the notes

**Files:**

- Create: `reference/ink-pages/about-bc/translations-c.cjs`
- Modify: `src/i18n/copy-keys.json`, `messages/*.json`, `src/components/about/*.css` (only for faults found), `docs/about-page.md`

**Interfaces:**

- Consumes: Task 3's checks and catalogs (the seedling and sequoia descriptions are already translated); `ALT.glasses` (Task 4).

- [ ] **Step 1: Run the language and deep-link checks to see what fails**

Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/scripts/qa/qa_about.py http://localhost:3025 --only=deep_links,languages,languages_layout,nav_locales`
Expected: the four "the paintings' descriptions translated" FAILs (the glasses).

- [ ] **Step 2: Translate the glasses**

Create `reference/ink-pages/about-bc/translations-c.cjs` (the same body as translations-b.cjs) with one row:

```js
const entries = [
  [
    "Reading glasses resting on an open notebook, painted in ink",
    "水墨绘制的老花镜，放在打开的笔记本上。",
    "펼친 노트 위에 놓인 돋보기안경을 먹으로 그린 그림.",
    "Cặp kính đọc sách đặt trên cuốn sổ đang mở, vẽ bằng mực.",
    "開いたノートの上に置かれた老眼鏡を墨で描いた絵。",
  ],
];
```

Run it as in Task 3 Step 3 and prettier the catalogs.

- [ ] **Step 3: Fix what the checks found; run the whole file**

Run the whole file on dev → `N/N passed`.

- [ ] **Step 4: The built site and the homepage gate**

As Task 3 Step 5, with the gate name `bc-c-prod` and screenshots into `scripts/qa/out/about-circle-built/`. Fix what keeps a size under 9; re-run. Stop the server.

- [ ] **Step 5: The notes**

In `docs/about-page.md`, change the top section to "## Current page: C, "The circle" (October 7, 2026)" describing the circle (its meaning, the stroke that paints itself, the gold, the hills, the shared rhythm and paintings, the files `circle.module.css` and the shared ones, the checks and their counts, the draft translation of the glasses description), and note that B "The album" is on branch `about-b`.

- [ ] **Step 6: Commit**

```bash
npx --prefix C:/Users/mcbig/Documents/codes/bigh-ink prettier --write C:/Users/mcbig/Documents/codes/bigh-ink/src/components/about C:/Users/mcbig/Documents/codes/bigh-ink/docs/about-page.md
git -C C:/Users/mcbig/Documents/codes/bigh-ink add -A reference/ink-pages/about-bc/translations-c.cjs src/i18n/copy-keys.json messages src/components/about docs/about-page.md
git -C C:/Users/mcbig/Documents/codes/bigh-ink commit -m "feat(about): the circle in five languages, checked built

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

- [ ] **Step 7: Stop and report**

Do not push. Report both branches' heads, pass counts (About on dev and built, homepage gate), per-size scores, the picture spend from `spend.md`, and the draft translations that need a native check.

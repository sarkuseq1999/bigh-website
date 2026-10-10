# NuriCell Ink Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** NuriCell's product page in the site's Ink & Gold look, with its own layout: seven chapters, each one painting beside its words, the lantern's light coming on in "Why it matters"; the other four product pages unchanged.

**Architecture:** A product whose data carries `ink` (its paintings) is rendered by a new page, `src/components/product/ink/`, inside the shared `InkPage` (menu bar, crane footer, bloom); every other product keeps `ProductPageView`. Paintings come from GPT Image 2.5 originals through a build script that divides the paper out and writes webp files plus a generated `nuricell-art.ts`. Each painting is its own `mix-blend-mode: multiply` group (the figure), so it can be sticky and the lantern can cross-fade lit over unlit without a white box or a lighter flash.

**Tech Stack:** Next.js 16 (App Router; read `node_modules/next/dist/docs/` before code, AGENTS.md), React 19, CSS modules, next-intl via `useCopy`, Python 3.13 (Pillow, OpenCV, NumPy) for paintings, Playwright for Python for QA.

**Spec:** `docs/superpowers/specs/2026-10-09-nuricell-ink-design.md` (approved by Mo, October 9, 2026). Mockups: `reference/ink-pages/mockups/nuricell-ink/`.

## Global Constraints

- Worktree `C:\Users\mcbig\Documents\codes\bigh-nuricell-ink`, branch `nuricell-ink`. Local commits only: **no push, no Vercel, no demo alias** without Mo's yes.
- No page loses words: every string in `src/components/product/products/nuricell.ts` (except picture `alt`s of pictures the ink page does not show) appears on the page.
- One painting per chapter, on the left from 960px, about the same size in every chapter; phones (under 960px): the painting first, then its words.
- Gold only where energy is meant: the lantern's light, the capsule's sparks, the yolk. No gold on the research painting, Dr. Liu or the buy stroke.
- No WebGL, no 3D, no `<canvas>`, no scroll-scrubbed film on this page.
- The other four product pages render exactly as today (`ProductPageView`); shared files they use are not changed in behaviour.
- Chapter anchors stay `anchorId(id)` = `chapter-<id>` (`overview`, `why`, `inside`, `research`, `people`, `daily`, `buy`).
- Honesty captions: "Illustration" (catalog key m574) under each painting that pictures something; "Portrait painting" under Dr. Liu. Dr. Liu's portrait is in colour, never black-and-white.
- Every CSS rule is scoped under `.page` (the `InkPage` className); a rule that must beat a kit `.look` rule of equal weight is qualified one step deeper (the built site orders CSS differently from dev).
- Multiply: nothing between a painting's blend group and the page root makes a stacking context (no transform, opacity < 1, filter, mask, isolation, z-index on a positioned ancestor, will-change).
- Files are LF. Python writes text with `newline="\n"`. Never `git stash`. Run `npx prettier --write` on changed files before each commit.
- Painting spend: the lantern only, at most 5 GPT Image 2.5 jobs, inside Mo's $5 (ledger `%LOCALAPPDATA%/HiggsfieldAPI/bigh-nuricell-mock/ledger-nuricell-mock.jsonl`, cap 70; 65 used by the mockups).
- Dev server: preview "bigh-nuricell-ink" (port 3032); built site: "bigh-nuricell-ink-prod" (`next start`, port 3033).
- Every task's code passes `npm --prefix C:/Users/mcbig/Documents/codes/bigh-nuricell-ink run lint` and `npx tsc --noEmit -p C:/Users/mcbig/Documents/codes/bigh-nuricell-ink` before its commit.
- Every commit message ends with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Review Focus

1. **A white box around a painting.** A sticky figure, an arrival transform or an opacity on a chapter makes a stacking context, and the painting's white paper stops multiplying. Expected: every painting reads as ink on the page's paper. Pinned by the `multiply` QA section (Task 4).
2. **The lantern's light misbehaving.** It comes on before the lantern has bloomed, never comes on, or flashes lighter mid-change (lit and unlit layers multiplying separately). Expected: unlit blooms in, then the light comes up smoothly, once. Pinned by the `lantern` QA section (Task 4).
3. **Long words under a sticky painting.** Every study open, or a long Vietnamese column, makes the words taller than the painting. Expected: the painting stays inside its own chapter and never slides over the next chapter's words. Pinned by the `sticky` QA section (Task 5).
4. **No script, or pictures blocked.** Expected: every painting is shown (not stuck at the bloom's 0%), the lantern is lit, and every heading and paragraph is readable with pictures blocked. Pinned by the `nojs` QA section (Task 4) and `layout` (Task 9).
5. **The painted sum disagreeing with the serving.** The data changes (another product, a new label) but the painted "3 × 30 = 90" stays. Expected: the painting is shown only when its numbers match the serving; otherwise the sum is set in type. Pinned by the `sum` QA section and the `Daily` guard (Task 6).

---

## File map

| File                                                     | Responsibility                                                                                               |
| -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `reference/ink-pages/nuricell/hf_nuricell.py`            | GPT Image 2.5 helper for this page (its own ledger, cap 70)                                                  |
| `reference/ink-pages/nuricell/prompts/lantern-*.txt`     | The lantern prompts                                                                                          |
| `reference/ink-pages/nuricell/build_nuricell.py`         | Originals → `public/images/products/nuricell/ink/*.webp` + `src/components/product/ink/nuricell-art.ts`      |
| `reference/ink-pages/nuricell/check_nuricell_art.py`     | Checks on the built paintings                                                                                |
| `reference/ink-pages/nuricell/translations-nuricell.cjs` | The page's new strings in five languages                                                                     |
| `src/components/product/product-types.ts`                | `InkArt`, `InkPainting`, `ProductInk`, `InkProduct`; `ink?` on `ProductPage`; `painting?` on `ProductPerson` |
| `src/components/product/products/nuricell.ts`            | NuriCell's `ink` and Dr. Liu's `painting`                                                                    |
| `src/app/[locale]/products/[slug]/page.tsx`              | Picks the ink page or today's template                                                                       |
| `src/components/product/ink/product-ink.tsx`             | The ink page: `InkPage` + chapters in order                                                                  |
| `src/components/product/ink/ink-chapter.tsx`             | `InkChapter` (one painting + words) and `InkFigure` (a painting as its own blend group)                      |
| `src/components/product/ink/opening.tsx`                 | Chapter 1: the giant name round the real bottle                                                              |
| `src/components/product/ink/why.tsx`                     | Chapter 2: the lantern and its light                                                                         |
| `src/components/product/ink/inside.tsx`                  | Chapter 3: ingredients and how they work together                                                            |
| `src/components/product/ink/research.tsx`                | Chapter 4: the studies                                                                                       |
| `src/components/product/ink/people.tsx`                  | Chapter 5: Dr. Liu                                                                                           |
| `src/components/product/ink/daily.tsx`                   | Chapter 6: breakfast and the painted sum                                                                     |
| `src/components/product/ink/buy.tsx`                     | Chapter 7: the bottle on its stroke                                                                          |
| `src/components/product/ink/after.tsx`                   | Questions, More from BiGH, caution and FDA notes                                                             |
| `src/components/product/ink/product-ink.module.css`      | All of the page's styles, scoped under `.page`                                                               |
| `src/components/product/template-chapters-kit.ts`        | Gains `WORDS` (moved from the cutaway)                                                                       |
| `src/components/product/template-chapters-hero.tsx`      | Exports `splitName` (no behaviour change)                                                                    |
| `src/components/product/template-chapters-daily.tsx`     | Exports `titleFor` (no behaviour change)                                                                     |
| `scripts/qa/qa_nuricell_ink.py`                          | The page's QA, one section per review concern                                                                |

---

### Task 1: The lantern, unlit and lit

**Files:**

- Create: `reference/ink-pages/nuricell/hf_nuricell.py` (copy of the session helper `mock/mock_gpt.py`)
- Create: `reference/ink-pages/nuricell/prompts/lantern-lit-v1.txt`, `reference/ink-pages/nuricell/prompts/lantern-unlit-v1.txt`
- Create: `reference/ink-pages/nuricell/originals/gpt25-lantern-lit-v1.png`, `gpt25-lantern-unlit-v1.png` (+ `.json`)
- Modify: `reference/ink-pages/spend.md` (append a section)

**Interfaces:**

- Produces: the two originals named above, read by Task 2's `TAKES`.

- [ ] **Step 1: Put the helper in the repo**

Copy `C:/Users/mcbig/AppData/Local/Temp/claude/C--Users-mcbig-Documents-codes-bigh-website/ff082d14-ea43-4e8f-8b4b-9173744abb97/scratchpad/mock/mock_gpt.py` to `reference/ink-pages/nuricell/hf_nuricell.py`, then change its docstring's first line and default output:

```python
"""GPT Image 2.5 (Higgsfield "Marketing Studio Image 2.5 Flare") jobs for NuriCell's ink page.

Mo gave $5 on October 9, 2026 for the mockups and the lantern (cap 70 jobs, worst case $4.90 at the
$0.07 billed before refunds). Ledger: %LOCALAPPDATA%/HiggsfieldAPI/bigh-nuricell-mock (set
HF_RUN_STATE to it). One job at a time; never retried automatically.

usage: HF_RUN_STATE=... python -X utf8 reference/ink-pages/nuricell/hf_nuricell.py <name> <prompt.txt>
          [--aspect 3:4] [--quality high] [--resolution 2k] [--ref img.png ...]
"""
```

and keep `ap.add_argument("--out", default=str(Path(__file__).parent / "originals"))`, `LEDGER = STATE / "ledger-nuricell-mock.jsonl"`, `MAX_JOBS = 70`.

- [ ] **Step 2: Write the lit prompt** — `reference/ink-pages/nuricell/prompts/lantern-lit-v1.txt`:

```text
A traditional East Asian ink-wash painting (sumi-e) on one plain sheet of warm, light rice paper with fine fibres, seen flat from straight above, evenly lit, no shadow, no frame, no table, no text, no signature, no red seal, no stamp. Paint it the way a master ink painter works: a few confident, loose brush strokes, wet ink bleeding softly into the paper, dry-brush texture where the brush runs out, simplified forms that suggest rather than describe, lots of white paper. It must look like a painting, expressive and artistic, with the brushwork of the reference picture: never a realistic drawing, never a detailed illustration, never a 3D render. Copy only the reference's brushwork, never its subject: no bird, no crane, no reeds, no water, no landscape. Sumi ink only, from deep black to soft grey washes, plus real gold leaf only where stated. The subject fills most of the picture (about 85% of its height), centred, with paper on every side.

A tall cylindrical paper lantern hanging from a thin black cord that comes down from the top edge of the picture: its top and bottom rims bold dark strokes, its paper ribs a few fine grey lines. The lantern is lit from within: its paper glows with real gold leaf, warm and steady from rim to rim, the leaf's crackle visible, and a soft warm haze of gold spreads a little way onto the paper around it. Nothing else on the paper.
```

- [ ] **Step 3: Paint it and look**

Run (Bash, one job):

```bash
cd "C:/Users/mcbig/Documents/codes/bigh-nuricell-ink" && HF_RUN_STATE="$LOCALAPPDATA/HiggsfieldAPI/bigh-nuricell-mock" python -X utf8 reference/ink-pages/nuricell/hf_nuricell.py lantern-lit-v1 reference/ink-pages/nuricell/prompts/lantern-lit-v1.txt --aspect 3:4 --ref reference/home-v2/ink/originals/gpt25-crane-rest-v2.png
```

Expected: `saved ...gpt25-lantern-lit-v1.png` and `jobs this round: 66 of 70`. Open the picture (Read tool) and check: one lantern, loose brushwork (not a realistic drawing), gold leaf only in the lantern and its haze, no landscape, paper on every side, cord reaching the top edge. If any fails, write `lantern-lit-v2.txt` naming the fix and run once more (at most 2 lit takes).

- [ ] **Step 4: Write the unlit prompt** — `reference/ink-pages/nuricell/prompts/lantern-unlit-v1.txt`:

```text
Edit the reference picture, an ink painting of a lit paper lantern on rice paper. Keep everything exactly as it is: the same paper, the same lantern in exactly the same place, size and shape, the same cord, rims, ribs and brushwork. Change one thing only: the lantern is unlit. Remove all gold leaf, all glow and all warm haze, inside the lantern and around it, so its paper is a pale, cool grey ink wash with the ribs showing as fine grey lines, and the paper around it plain rice paper. No gold anywhere. No text, no signature, no red seal, no stamp.
```

- [ ] **Step 5: Paint the unlit take from the chosen lit one and look**

```bash
cd "C:/Users/mcbig/Documents/codes/bigh-nuricell-ink" && HF_RUN_STATE="$LOCALAPPDATA/HiggsfieldAPI/bigh-nuricell-mock" python -X utf8 reference/ink-pages/nuricell/hf_nuricell.py lantern-unlit-v1 reference/ink-pages/nuricell/prompts/lantern-unlit-v1.txt --aspect 3:4 --ref reference/ink-pages/nuricell/originals/gpt25-lantern-lit-v1.png
```

Expected: `jobs this round: 67 of 70` (68 if a lit retake was needed). Put the two side by side and check: same lantern, same place (a few px of drift is fine: Task 2 registers it), no gold left in the unlit one.

- [ ] **Step 6: Record the spend** — append to `reference/ink-pages/spend.md`:

```markdown
## NuriCell ink page (October 9, 2026)

Ledger: `C:/Users/mcbig/AppData/Local/HiggsfieldAPI/bigh-nuricell-mock/` (cap 70). Mockup rounds 1-11:
65 jobs (about $3.25, at most $4.55 before refunds), Mo's $5. Kept mockup paintings (finals):
P7-capsule, P7-stepping-books, P11-liu-face-bold (Dr. Liu, from his real photo; Mo's call, October 9),
P7-egg-capsules, P7-sum, P5-stroke.

| Job              | Picture                                                 | Kept | Note           |
| ---------------- | ------------------------------------------------------- | ---- | -------------- |
| lantern-lit-v1   | Lantern lit by gold leaf (ref: crane-rest-v2 brushwork) | yes  | <what you saw> |
| lantern-unlit-v1 | Edit of the lit take: unlit, no gold                    | yes  | <what you saw> |
```

Fill the two Note cells with what you actually saw (one line each).

- [ ] **Step 7: Commit**

```bash
cd "C:/Users/mcbig/Documents/codes/bigh-nuricell-ink" && npx prettier --write reference/ink-pages/spend.md && git add reference/ink-pages/nuricell reference/ink-pages/spend.md && git commit -m "feat(nuricell): the lantern, unlit and lit, for the light that comes on" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 2: Build the paintings

**Files:**

- Create: `reference/ink-pages/nuricell/check_nuricell_art.py`
- Create: `reference/ink-pages/nuricell/build_nuricell.py`
- Create: `reference/ink-pages/nuricell/.gitignore` (one line: `plates/`)
- Create (generated): `public/images/products/nuricell/ink/*.webp`, `src/components/product/ink/nuricell-art.ts`

**Interfaces:**

- Consumes: originals `gpt25-{lantern-lit-v1, lantern-unlit-v1, P7-capsule, P7-stepping-books, P11-liu-face-bold, P7-egg-capsules, P7-sum, P5-stroke}.png`.
- Produces: `export const nuricellArt` in `src/components/product/ink/nuricell-art.ts`, shaped:

```ts
{
  lanternUnlit: { src, width, height },
  lanternLit: { src, width, height, gold },   // same width and height as lanternUnlit
  capsule: { src, width, height, gold },
  books: { src, width, height },
  liu: { src, width, height },
  breakfast: { src, width, height, gold },
  sum: { src, width, height, numbers: [3, 30, 90], centres: [x0, x1, x2] }, // centres: fractions of width
  stroke: { src, width, height },
}
```

- [ ] **Step 1: Write the failing check** — `reference/ink-pages/nuricell/check_nuricell_art.py`:

```python
"""Checks on NuriCell's built paintings (run after build_nuricell.py).

usage: python -X utf8 reference/ink-pages/nuricell/check_nuricell_art.py
"""
import json
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[3]
TS = REPO / "src/components/product/ink/nuricell-art.ts"
fails = []


def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f"  ({detail})" if detail else ""))
    if not ok:
        fails.append(name)


def pixels(src):
    return np.asarray(Image.open(REPO / "public" / src.lstrip("/")).convert("RGB")).astype(np.float32)


if not TS.exists():
    sys.exit("FAIL nuricell-art.ts missing: run build_nuricell.py")
text = TS.read_text(encoding="utf-8")
# The file is Prettier's TypeScript: unquoted keys and trailing commas. Make it JSON again.
body = re.search(r"nuricellArt = (\{.*\}) as const", text, re.S).group(1)
body = re.sub(r"(?m)^(\s*)([A-Za-z_]\w*):", r'\1"\2":', body)
body = re.sub(r",(\s*[}\]])", r"\1", body)
art = json.loads(body)

for key, entry in art.items():
    arr = pixels(entry["src"])
    h, w = arr.shape[:2]
    check(f"{key}: size as listed", (w, h) == (entry["width"], entry["height"]), f"{w}x{h}")
    rim = np.concatenate([arr[:3].reshape(-1, 3), arr[-3:].reshape(-1, 3), arr[:, :3].reshape(-1, 3), arr[:, -3:].reshape(-1, 3)])
    check(f"{key}: white rim (no box on the page)", rim.mean() >= 254.0, f"{rim.mean():.1f}")
    if "gold" in entry:
        mask = np.asarray(Image.open(REPO / "public" / entry["gold"].lstrip("/")).split()[-1])
        share = float((mask > 128).mean())
        check(f"{key}: gold mask covers its leaf", 0.001 <= share <= 0.35, f"{share:.2%}")

check("lantern: lit and unlit the same size", (art["lanternLit"]["width"], art["lanternLit"]["height"]) == (art["lanternUnlit"]["width"], art["lanternUnlit"]["height"]))
lit, unlit = pixels(art["lanternLit"]["src"]), pixels(art["lanternUnlit"]["src"])
# Registered: the dark outlines (rims, cord) sit in the same place; compare edge maps.
def edges(a):
    g = a.mean(axis=2)
    return (np.abs(np.diff(g, axis=0))[:, :-1] + np.abs(np.diff(g, axis=1))[:-1]) > 40
e1, e2 = edges(lit), edges(unlit)
overlap = (e1 & e2).sum() / max(1, min(e1.sum(), e2.sum()))
check("lantern: lit and unlit in register", overlap > 0.35, f"edge overlap {overlap:.2f}")
warm = lambda a: float(((a[..., 0] - a[..., 2]) > 40).mean())
check("lantern: the unlit one has no gold", warm(unlit) < 0.002, f"{warm(unlit):.3%}")
check("lantern: the lit one glows", warm(lit) > 0.03, f"{warm(lit):.2%}")

liu = pixels(art["liu"]["src"])
hi, lo = liu.max(axis=2), liu.min(axis=2)
sat = (hi - lo) / np.maximum(hi, 1)
skin = (sat > 0.12) & (hi > 120)
check("liu: in colour, never black-and-white", skin.mean() > 0.03, f"coloured pixels {skin.mean():.1%}")
books = pixels(art["books"]["src"])
check("books: no gold", warm(books) < 0.001, f"{warm(books):.3%}")
stroke = pixels(art["stroke"]["src"])
check("stroke: no gold", warm(stroke) < 0.001, f"{warm(stroke):.3%}")

c = art["sum"]["centres"]
check("sum: numbers 3, 30, 90", art["sum"]["numbers"] == [3, 30, 90])
check("sum: three centres left to right, apart", len(c) == 3 and c[0] < c[1] < c[2] and min(c[1] - c[0], c[2] - c[1]) > 0.15, str(c))

print("ALL PASS" if not fails else f"{len(fails)} FAIL")
sys.exit(1 if fails else 0)
```

- [ ] **Step 2: Run it to see it fail**

Run: `python -X utf8 reference/ink-pages/nuricell/check_nuricell_art.py`
Expected: `FAIL nuricell-art.ts missing: run build_nuricell.py` (exit 1).

- [ ] **Step 3: Write the build** — `reference/ink-pages/nuricell/build_nuricell.py`:

```python
"""Build NuriCell's ink paintings (Mo, October 9, 2026; spec
docs/superpowers/specs/2026-10-09-nuricell-ink-design.md).

Originals: reference/ink-pages/nuricell/originals/gpt25-<take>.png (GPT Image 2.5 on rice paper;
prompts in prompts/; spend in reference/ink-pages/spend.md). Output: public/images/products/
nuricell/ink/*.webp (lossless plates in plates/, not committed) and
src/components/product/ink/nuricell-art.ts. About's treatments (reference/ink-pages/about/
build_about.py): the paper divided out and lifted to white so each painting multiplies onto the
page's paper with no box, the outer edge feathered, gold leaf kept as a light mask for the kit's
glint. The lantern's unlit take is registered onto its lit take and both share one crop, so the
light comes on in place. The painted sum is laid out again with even gaps.

usage: python -X utf8 reference/ink-pages/nuricell/build_nuricell.py
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
OUT = REPO / "public/images/products/nuricell/ink"
URL = "/images/products/nuricell/ink"
TS = REPO / "src/components/product/ink/nuricell-art.ts"
# Bump when a shipped picture changes after it has been pushed (the image optimizer caches by URL).
V = "v1"
TAKES = {
    "lantern-lit": "lantern-lit-v1",
    "lantern-unlit": "lantern-unlit-v1",
    "capsule": "P7-capsule",
    "books": "P7-stepping-books",
    "liu": "P11-liu-face-bold",
    "breakfast": "P7-egg-capsules",
    "sum": "P7-sum",
    "stroke": "P5-stroke",
}
EDGE = 0.03

bd.ORIG = HERE / "originals"
bd.URL = URL
bd.V = V
bd.TAKES = TAKES
ba.OUT = OUT
ba.PLATES = HERE / "plates"


def finish(img, name, width):
    """Paper lifted to white, the outer edge feathered to white, saved; its art entry."""
    return bd.art_of(bd.feathered(bd.levelled(img), EDGE), f"{name}-{V}", width)


def cropped(key, pad=0.04):
    flat = bd.divided(bd.load(TAKES[key]))
    return flat.crop(bd.ink_box(np.asarray(flat), pad=pad))


def gilded(key, width, sat_from=0.3, pad=0.04):
    art = finish(cropped(key, pad), key, width)
    ba.gold_mask(f"{key}-{V}", sat_from=sat_from)
    art["gold"] = f"{URL}/{key}-{V}-gold.webp"
    return art


def lantern():
    """The unlit take (an edit of the lit one) registered onto the lit take, both cut by one box."""
    lit = bd.divided(bd.load(TAKES["lantern-lit"]))
    unlit = bd.divided(bd.load(TAKES["lantern-unlit"]))
    if unlit.size != lit.size:
        unlit = unlit.resize(lit.size, Image.LANCZOS)
    grey = lambda im: cv2.GaussianBlur(np.asarray(im.convert("L")).astype(np.float32) / 255, (0, 0), 3)
    warp = np.eye(2, 3, dtype=np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6)
    _, warp = cv2.findTransformECC(grey(lit), grey(unlit), warp, cv2.MOTION_EUCLIDEAN, criteria, None, 5)
    w, h = lit.size
    moved = cv2.warpAffine(
        np.asarray(unlit), warp, (w, h), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE
    )
    unlit = Image.fromarray(moved)
    print(f"lantern: unlit registered by ({warp[0, 2]:.1f}, {warp[1, 2]:.1f}) px")
    a, b = bd.ink_box(np.asarray(lit), pad=0.06), bd.ink_box(np.asarray(unlit), pad=0.06)
    box = (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))
    lit_art = finish(lit.crop(box), "lantern-lit", 1100)
    ba.gold_mask(f"lantern-lit-{V}", sat_from=0.25)
    lit_art["gold"] = f"{URL}/lantern-lit-{V}-gold.webp"
    return finish(unlit.crop(box), "lantern-unlit", 1100), lit_art


def brushed_sum():
    """The painted 3 × 30 = 90 with even gaps (the model wrote 30 and = touching), and the centres
    of its three numbers as fractions of its width (the page sets a caption under each)."""
    flat = np.asarray(bd.levelled(bd.divided(bd.load(TAKES["sum"]))))
    dark = (flat.min(axis=2) < 150).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(cv2.dilate(dark, np.ones((5, 5), np.uint8)), 8)
    comps = [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] > 200]
    tallest = max(st[i, cv2.CC_STAT_HEIGHT] for i in comps)
    digits = sorted((i for i in comps if st[i, cv2.CC_STAT_HEIGHT] > 0.5 * tallest), key=lambda i: st[i, 0])
    signs = sorted((i for i in comps if i not in digits), key=lambda i: st[i, 0])
    if len(digits) != 5:
        raise SystemExit(f"expected the five digits of 3 30 90, found {len(digits)}")
    groups = [[digits[0]], digits[1:3], digits[3:5]]
    # Each sign belongs between the two groups its centre lies between.
    times = [i for i in signs if st[groups[0][-1], 0] < st[i, 0] < st[groups[1][0], 0]]
    equals = [i for i in signs if st[groups[1][-1], 0] < st[i, 0] < st[groups[2][0], 0]]
    pieces = [groups[0], times, groups[1], equals, groups[2]]
    if not times or not equals:
        raise SystemExit("the × or the = sign was not found")
    y0 = max(0, min(st[i, 1] for i in comps) - 40)
    y1 = min(flat.shape[0], max(st[i, 1] + st[i, 3] for i in comps) + 40)
    gap, pad = int(0.32 * tallest), int(0.25 * tallest)
    spans = [(min(st[i, 0] for i in p), max(st[i, 0] + st[i, 2] for i in p)) for p in pieces]
    width = sum(b - a for a, b in spans) + gap * 4 + pad * 2
    canvas = np.full((y1 - y0, width, 3), 255, np.uint8)
    x, centres = pad, []
    for k, (piece, (a, b)) in enumerate(zip(pieces, spans)):
        own = np.isin(lab[y0:y1, a:b], piece)[..., None]
        region = canvas[:, x : x + b - a]
        canvas[:, x : x + b - a] = np.where(own, np.minimum(region, flat[y0:y1, a:b]), region)
        if k % 2 == 0:
            centres.append(round((x + (b - a) / 2) / width, 4))
        x += b - a + gap
    art = bd.art_of(bd.feathered(Image.fromarray(canvas), EDGE), f"sum-{V}", 1400)
    art["numbers"] = [3, 30, 90]
    art["centres"] = centres
    return art


def write_ts(art):
    head = [
        "// Generated by reference/ink-pages/nuricell/build_nuricell.py. Do not edit by hand: change",
        "// the script (or its TAKES) and run it again. NuriCell's ink paintings (October 9, 2026): GPT",
        "// Image 2.5 on rice paper, the paper divided out so each multiplies onto the page's own paper;",
        "// gold leaf as a light mask (`gold`). sum.centres: its three numbers, as fractions of its width.",
        "",
    ]
    TS.parent.mkdir(parents=True, exist_ok=True)
    TS.write_text("\n".join(head) + f"export const nuricellArt = {json.dumps(art, indent=2)} as const;\n", encoding="utf-8", newline="\n")
    prettier = REPO / "node_modules/prettier/bin/prettier.cjs"
    subprocess.run(["node", str(prettier), "--write", str(TS)], cwd=REPO, check=True, capture_output=True)
    print(TS.relative_to(REPO))


if __name__ == "__main__":
    unlit, lit = lantern()
    write_ts(
        {
            "lanternUnlit": unlit,
            "lanternLit": lit,
            "capsule": gilded("capsule", 1200),
            "books": finish(cropped("books"), "books", 1100),
            "liu": finish(cropped("liu"), "liu", 1000),
            "breakfast": gilded("breakfast", 1100),
            "sum": brushed_sum(),
            "stroke": finish(cropped("stroke", pad=0.08), "stroke", 1400),
        }
    )
```

- [ ] **Step 4: Build, then check**

```bash
cd "C:/Users/mcbig/Documents/codes/bigh-nuricell-ink" && printf 'plates/\n' > reference/ink-pages/nuricell/.gitignore && python -X utf8 reference/ink-pages/nuricell/build_nuricell.py && python -X utf8 reference/ink-pages/nuricell/check_nuricell_art.py
```

Expected: the build lists each `public/images/products/nuricell/ink/<name>-v1.webp` and three `-gold.webp` masks, prints the lantern registration shift, and the check ends `ALL PASS`. Then open each webp (Read tool) and look: no box, no stray paper, the sum evenly spaced and legible, Dr. Liu in colour.

- [ ] **Step 5: Commit**

```bash
cd "C:/Users/mcbig/Documents/codes/bigh-nuricell-ink" && npx prettier --write src/components/product/ink/nuricell-art.ts && git add reference/ink-pages/nuricell public/images/products/nuricell/ink src/components/product/ink/nuricell-art.ts && git commit -m "feat(nuricell): build the ink paintings, the lantern in register, the sum evenly spaced" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: The ink page's frame, the opening, and the route

**Files:**

- Modify: `src/components/product/product-types.ts`
- Modify: `src/components/product/products/nuricell.ts`
- Modify: `src/components/product/template-chapters-hero.tsx` (export `splitName`)
- Modify: `src/app/[locale]/products/[slug]/page.tsx`
- Create: `src/components/product/ink/product-ink.tsx`, `src/components/product/ink/opening.tsx`, `src/components/product/ink/product-ink.module.css`
- Create: `scripts/qa/qa_nuricell_ink.py`
- Modify (not committed, gitignored): `C:\Users\mcbig\Documents\codes\bigh-website\.claude\launch.json`

**Interfaces:**

- Consumes: `nuricellArt` (Task 2).
- Produces:
  - `export type InkArt = { src: string; width: number; height: number; gold?: string }`
  - `export type InkPainting = InkArt & { alt: string }`
  - `export type ProductInk = { why: { unlit: InkArt; lit: InkArt; alt: string }; inside: InkPainting; research: InkPainting; daily: { picture: InkPainting; sum: InkArt & { numbers: readonly number[]; centres: readonly number[] } }; buy: { stroke: InkArt } }`
  - `export type InkProduct = ProductPage & { ink: ProductInk }`
  - `ProductPage.ink?: ProductInk`; `ProductPerson.painting?: InkPainting`
  - `export function ProductInkPage({ product }: { product: InkProduct })`
  - CSS module class names used by later tasks: `page`, `chapter`, `spread`, `words`, `figure`, `body`, `art`, `caption`, `label`, `heading`, `text`, `small`.

- [ ] **Step 1: Read the docs this task leans on**

Read `node_modules/next/dist/docs/` for `next/image` (the `preload` and `fetchPriority` props About uses) and for dynamic route pages; note anything that differs from `src/app/[locale]/about/page.tsx`.

- [ ] **Step 2: Add the previews** — in `C:\Users\mcbig\Documents\codes\bigh-website\.claude\launch.json`, append two entries to `configurations`:

```json
    {
      "name": "bigh-nuricell-ink",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["--prefix", "C:/Users/mcbig/Documents/codes/bigh-nuricell-ink", "run", "dev", "--", "--hostname", "localhost", "--port", "3032"],
      "port": 3032
    },
    {
      "name": "bigh-nuricell-ink-prod",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["--prefix", "C:/Users/mcbig/Documents/codes/bigh-nuricell-ink", "run", "start", "--", "--hostname", "localhost", "--port", "3033"],
      "port": 3033
    }
```

Then `preview_start {name: "bigh-nuricell-ink"}`. If the preview tool refuses (its 5-server cap), start it from Bash in the background: `npm --prefix C:/Users/mcbig/Documents/codes/bigh-nuricell-ink run dev -- --hostname localhost --port 3032`.

- [ ] **Step 3: Write the failing test** — `scripts/qa/qa_nuricell_ink.py` with its frame, `shell` and `others` (later tasks add sections to `SECTIONS`):

```python
"""QA for NuriCell's ink page (Mo, October 9, 2026; spec
docs/superpowers/specs/2026-10-09-nuricell-ink-design.md; plan
docs/superpowers/plans/2026-10-09-nuricell-ink.md).

Sections (all, or --only=a,b):
  shell       200 in the ink look, the menu bar marks Products, one h1 (the name), the real bottle,
              no canvas, no console errors (1440x900, 390x844)
  others      the other four product pages keep today's template
  multiply    every painting multiplies onto the paper: no stacking context in between, no box
  lantern     unlit blooms, then the light comes on once with no lighter flash; reduced motion: lit
  nojs        with JavaScript off every painting shows and the lantern is lit
  words       every word in nuricell.ts on the page; each chapter its own painting
  sticky      with every study open a sticky painting stays inside its chapter
  sum         the painted sum matches the serving, a caption under each number
  layout      sizes 1536 to 360: no sideways scroll, the painting left of its words from 960px and above
              them below, text 15px+, targets 44px+, words readable with pictures blocked
  deep_links  /en/products/nuricell#chapter-<id> lands its heading under the menu bar
  languages   kr, jp, cns, vn: 200, no console errors, the new strings translated
Pictures: scripts/qa/out/nuricell-ink/.

usage: python -X utf8 scripts/qa/qa_nuricell_ink.py [base-url] [--only=shell,others,...]
"""

import re
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = ARGS[0] if ARGS else "http://localhost:3032"
ONLY = next((a.split("=", 1)[1].split(",") for a in sys.argv[1:] if a.startswith("--only=")), None)
REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "scripts/qa/out/nuricell-ink"
OUT.mkdir(parents=True, exist_ok=True)
PATH = "/en/products/nuricell"
OTHERS = ["green-bee-propolis", "advanced-opc", "turmerific", "nature-calm"]
CHAPTERS = ["overview", "why", "inside", "research", "people", "daily", "buy"]
# Next's prefetched-CSS warning is not an error of this page (qa_about.py's PREFETCH_CSS).
PREFETCH_CSS = re.compile(r"was preloaded using link preload but not used")
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f"  ({detail})" if detail else ""), flush=True)


def opened(browser, w, h, path=PATH, reduced=False, js=True):
    ctx = browser.new_context(
        viewport={"width": w, "height": h},
        reduced_motion="reduce" if reduced else "no-preference",
        java_script_enabled=js,
    )
    page = ctx.new_page()
    errors = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" and not PREFETCH_CSS.search(m.text) else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    response = page.goto(BASE + path, wait_until="networkidle")
    if js:
        page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
    return ctx, page, response, errors


def bring(page, selector, top=140):
    """Scroll the element's top to `top` px under the window's top (scrollBy: the document's 150px
    scroll-padding stops scrollIntoView short)."""
    page.evaluate(
        "([s, t]) => { const e = document.querySelector(s); window.scrollBy(0, e.getBoundingClientRect().top - t); }",
        [selector, top],
    )


def shell(browser):
    for w, h in [(1440, 900), (390, 844)]:
        ctx, page, response, errors = opened(browser, w, h)
        tag = f"shell {w}x{h}"
        check(f"{tag}: 200", response is not None and response.status == 200)
        check(f"{tag}: the ink look", page.locator('[data-look="ink"][data-page="products"]').count() == 1)
        check(f"{tag}: the menu bar marks Products", page.locator('[data-nav-trigger="products"][data-current]').count() >= 1)
        name = page.locator("h1").all_inner_texts()
        check(f"{tag}: one h1, the name", len(name) == 1 and re.sub(r"\s", "", name[0]) == "NuriCell", str(name))
        check(f"{tag}: the real bottle", page.locator('[data-chapter="overview"] img[src*="nuricell.png"]').count() >= 1)
        check(f"{tag}: no canvas", page.locator("canvas").count() == 0)
        check(f"{tag}: no console errors", not errors, "; ".join(errors[:3]))
        page.screenshot(path=str(OUT / f"shell-{w}.png"))
        ctx.close()


def others(browser):
    for slug in OTHERS:
        ctx, page, response, errors = opened(browser, 1440, 900, f"/en/products/{slug}")
        check(f"others {slug}: 200", response is not None and response.status == 200)
        check(f"others {slug}: today's template", page.locator('[data-look="ink"]').count() == 0 and page.locator("#main-content").count() == 1)
        check(f"others {slug}: no console errors", not errors, "; ".join(errors[:3]))
        ctx.close()


SECTIONS = {"shell": shell, "others": others}

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name, run in SECTIONS.items():
            if ONLY is None or name in ONLY:
                run(browser)
        browser.close()
    failed = [r for r in results if not r[1]]
    print(f"\n{len(results) - len(failed)}/{len(results)} passed")
    sys.exit(1 if failed else 0)
```

- [ ] **Step 4: Run it to see it fail**

Run: `python -X utf8 scripts/qa/qa_nuricell_ink.py http://localhost:3032 --only=shell,others`
Expected: `others` all PASS; `shell` FAILs on "the ink look", "the menu bar marks Products", "no canvas" (today's NuriCell page has the 3D canvas).

- [ ] **Step 5: Add the types** — in `src/components/product/product-types.ts`, after `export type Picture`:

```ts
/** A painting from a page's build script: its paper divided out to white, so it multiplies onto the
 *  page's own paper; `gold` is its gold-leaf light mask, for the kit's glint. */
export type InkArt = { src: string; width: number; height: number; gold?: string };
export type InkPainting = InkArt & { alt: string };

/**
 * The product's paintings for its ink page (NuriCell, October 9, 2026; spec
 * docs/superpowers/specs/2026-10-09-nuricell-ink-design.md). A product with `ink` gets the ink page
 * (one painting per chapter, beside its words); the others keep the Chapters template.
 */
export type ProductInk = {
  /** Why it matters: one painting unlit and lit, in register (its light comes on). */
  why: { unlit: InkArt; lit: InkArt; alt: string };
  inside: InkPainting;
  research: InkPainting;
  /** How to take it: a picture of when, and the serving as a painted sum (its numbers and their centres). */
  daily: {
    picture: InkPainting;
    sum: InkArt & { numbers: readonly number[]; centres: readonly number[] };
  };
  buy: { stroke: InkArt };
};
```

In `ProductPerson`, after `photo?: Picture;`:

```ts
  /** A painting of the person, for the ink page (Dr. Liu, October 9, 2026: Mo's call). */
  painting?: InkPainting;
```

In `ProductPage`, after `related: string[];`:

```ts
  /** The product's paintings: with them the product gets the ink page. */
  ink?: ProductInk;
```

and at the end of the file:

```ts
export type InkProduct = ProductPage & { ink: ProductInk };
```

- [ ] **Step 6: Give NuriCell its paintings** — in `src/components/product/products/nuricell.ts` add `import { nuricellArt } from "../ink/nuricell-art";` and, after `related: [...]`:

```ts
  // The ink page (Mo, October 9, 2026; spec docs/superpowers/specs/2026-10-09-nuricell-ink-design.md).
  ink: {
    why: {
      unlit: nuricellArt.lanternUnlit,
      lit: nuricellArt.lanternLit,
      alt: "A paper lantern whose light comes on, painted in ink and gold leaf",
    },
    inside: {
      ...nuricellArt.capsule,
      alt: "An opened capsule with its four powders in a row and gold sparks rising, painted in ink",
    },
    research: {
      ...nuricellArt.books,
      alt: "Seven books as stepping stones across a calm stream, painted in ink",
    },
    daily: {
      picture: {
        ...nuricellArt.breakfast,
        alt: "A soft-boiled egg with a gold yolk beside a dish of three capsules, painted in ink",
      },
      sum: nuricellArt.sum,
    },
    buy: { stroke: nuricellArt.stroke },
  },
```

and in Dr. Liu's entry in `people`, after `photo: {...},`:

```ts
      painting: {
        ...nuricellArt.liu,
        alt: "A portrait painting of Dr. Jiankang Liu in ink and colour",
      },
```

- [ ] **Step 7: Export `splitName`** — in `src/components/product/template-chapters-hero.tsx` change `function splitName(` to `export function splitName(` (nothing else).

- [ ] **Step 8: The page and its opening** — `src/components/product/ink/product-ink.tsx`:

```tsx
"use client";

import { InkPage } from "@/components/ink/ink-page";
import type { InkProduct } from "../product-types";
import { Opening } from "./opening";
import styles from "./product-ink.module.css";

// The product page in Ink & Gold (NuriCell first, October 9, 2026; spec
// docs/superpowers/specs/2026-10-09-nuricell-ink-design.md; mockups
// reference/ink-pages/mockups/nuricell-ink/). The shared theme (paper, menu bar, crane footer,
// bloom); its own layout: seven chapters, each one painting beside its words, the lantern's light
// coming on in "Why it matters". Every word of the product's data stays.
export function ProductInkPage({ product }: { product: InkProduct }) {
  return (
    <InkPage current="products" className={styles.page}>
      {() => (
        <div data-product-ink={product.slug}>
          <Opening product={product} />
        </div>
      )}
    </InkPage>
  );
}
```

`src/components/product/ink/opening.tsx`:

```tsx
"use client";

import Image from "next/image";
import { contactShadow, shadow } from "@/components/home-v2/look-ink/assets";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { AddToCart } from "../add-to-cart";
import type { ProductPage } from "../product-types";
import { splitName } from "../template-chapters-hero";
import { anchorId } from "../template-chapters-kit";
import styles from "./product-ink.module.css";

// Chapter 1: the giant name parts round the real bottle, which stands in the kit's ink pool (the
// Ink Pool Rule), on paper. Phones stack the name over the bottle. The bottle photo never
// multiplies; only its pools do.
export function Opening({ product }: { product: ProductPage }) {
  const copy = useCopy();
  const [first, second] = product.nameHalves ?? splitName(product.name);
  return (
    <section
      id={anchorId("overview")}
      className={styles.opening}
      data-chapter="overview"
      aria-labelledby="product-name"
    >
      <div className={base.wrap}>
        <p className={`${base.label} ${styles.eyebrow}`}>{copy(product.eyebrow)}</p>
        <h1 id="product-name" className={styles.name}>
          <span className={styles.first}>{first}</span>
          <span className={styles.stand} aria-hidden="true">
            <Image
              className={`${base.ink} ${styles.pool}`}
              src={shadow.src}
              alt=""
              width={shadow.width}
              height={shadow.height}
              sizes="(max-width: 959px) 50vw, 300px"
              loading="eager"
            />
            <Image
              className={`${base.ink} ${styles.contact}`}
              src={contactShadow.src}
              alt=""
              width={contactShadow.width}
              height={contactShadow.height}
              sizes="(max-width: 959px) 44vw, 260px"
              loading="eager"
            />
            <Image
              className={styles.bottle}
              src={product.bottle.src}
              alt=""
              width={product.bottle.width}
              height={product.bottle.height}
              sizes="(max-width: 959px) 60vw, 440px"
              preload
              fetchPriority="high"
            />
          </span>
          <span className={styles.second}>{second}</span>
        </h1>
        <div className={styles.openingWords}>
          <div>
            <p className={styles.headline}>
              {product.headlineLines.map((line) => (
                <span key={line}>{copy(line)}</span>
              ))}
            </p>
            <p className={styles.text}>{copy(product.purpose)}</p>
          </div>
          <div className={styles.openingBuy}>
            <ul className={styles.highlights}>
              {product.highlights.map((item) => (
                <li key={item}>{copy(item)}</li>
              ))}
            </ul>
            <AddToCart />
            <p className={base.caption}>{copy(product.serving.supply)}</p>
          </div>
        </div>
      </div>
    </section>
  );
}
```

`src/components/product/ink/product-ink.module.css` (this task's part; later tasks append):

```css
/* NuriCell's ink page (spec docs/superpowers/specs/2026-10-09-nuricell-ink-design.md). Every rule
   is scoped under .page (InkPage's root class), so it outranks the kit's .look rules and the
   homepage resets in any stylesheet order (the built site orders CSS differently from dev).
   Multiply: a chapter's figure is its painting's blend group (mix-blend-mode on the figure, its
   pictures drawn normally inside it); nothing between a figure and the page root may make a
   stacking context (no transform, opacity, filter, mask, isolation or z-index on a positioned
   chapter, spread or wrapper). */

.page {
  --gap: clamp(40px, 6vw, 112px);
  --chapter-half: clamp(48px, 5.5vw, 96px);
  --picture-width: 520px;
}

/* 1. The opening: the header floats over it, so it starts 88px down. */
.page .opening {
  padding: calc(88px + clamp(20px, 3vw, 56px)) 0 var(--chapter-half);
}

.page p.eyebrow {
  margin: 0 0 clamp(8px, 1.4vw, 20px);
  text-align: center;
}

/* The name parts round the bottle: three columns, the bottle a little taller than the letters. */
.page h1.name {
  display: grid;
  grid-template-columns: minmax(0, 1fr) clamp(180px, 22vw, 360px) minmax(0, 1fr);
  align-items: end;
  margin: 0;
  font-family: var(--display-font);
  font-weight: var(--display-weight);
  font-size: clamp(64px, 12.4vw, 220px);
  line-height: 0.86;
  letter-spacing: -0.045em;
}

.page .first {
  justify-self: end;
}

.page .second {
  justify-self: start;
}

.page .stand {
  position: relative;
  display: block;
  aspect-ratio: 1230 / 1278;
  align-self: end;
  margin-bottom: -0.06em;
}

.page .pool {
  position: absolute;
  left: 52%;
  top: 79%;
  width: 92%;
  height: auto;
  aspect-ratio: 1 / 0.42;
  object-fit: fill;
  translate: -50% 0;
  opacity: 0.92;
}

.page .contact {
  position: absolute;
  left: 50%;
  top: 92.6%;
  width: 56%;
  height: auto;
  aspect-ratio: 1 / 0.12;
  object-fit: fill;
  translate: -50% 0;
}

.page .bottle {
  position: relative;
  display: block;
  width: 100%;
  height: auto;
}

.page .openingWords {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  column-gap: var(--gap);
  margin-top: clamp(28px, 4vw, 64px);
}

.page p.headline {
  margin: 0 0 16px;
  font-family: var(--display-font);
  font-weight: var(--display-weight);
  font-size: clamp(30px, 2.8vw, 42px);
  line-height: 1.12;
  letter-spacing: -0.022em;
}

.page .headline span {
  display: block;
}

.page p.text {
  margin: 0;
  max-width: 30em;
  color: var(--muted);
  font-size: 19px;
  line-height: 1.6;
  text-wrap: pretty;
}

.page .openingBuy {
  display: grid;
  justify-items: start;
  gap: 16px;
}

.page ul.highlights {
  display: grid;
  gap: 6px;
  margin: 0;
  padding: 0;
  list-style: none;
  font-size: 19px;
  font-weight: 450;
}

.page .highlights li::before {
  content: "— ";
  color: var(--muted);
}

/* The opening arrives like ink settling (the homepage's words): the bottle rises 10px onto its
   pool, then the words settle, 0.14s apart. Only the bottle and the word blocks move: neither
   holds a painting, so the pools still multiply onto the paper. Reduced motion: there at once. */
@media (prefers-reduced-motion: no-preference) {
  .page img.bottle {
    animation: rise calc(var(--breath) * 0.75) var(--ease) both;
  }

  .page .openingWords > * {
    animation: settle calc(var(--breath) * 0.75) var(--ease) 0.2s both;
  }

  .page .openingWords > :nth-child(2) {
    animation-delay: 0.34s;
  }
}

@keyframes rise {
  from {
    translate: 0 10px;
    opacity: 0.6;
  }
}

@keyframes settle {
  from {
    translate: 0 0.24em;
    filter: blur(8px);
    opacity: 0;
  }
}

/* Phones: the name over the bottle, then the words in one column. */
@media (max-width: 959px) {
  .page h1.name {
    grid-template-columns: minmax(0, 1fr);
    justify-items: center;
    font-size: clamp(64px, 26vw, 150px);
  }

  .page .first,
  .page .second {
    justify-self: center;
  }

  .page .stand {
    order: 3;
    width: min(64vw, 320px);
    margin: 12px 0 0;
  }

  .page .openingWords {
    grid-template-columns: minmax(0, 1fr);
    row-gap: 24px;
  }

  .page .openingBuy {
    justify-items: stretch;
  }
}
```

- [ ] **Step 9: Route NuriCell to it** — `src/app/[locale]/products/[slug]/page.tsx`, replace the last line of `ProductRoute`:

```tsx
if (product.ink) {
  // The ink page (October 9, 2026): the shared header's sheets and the product links need the
  // same providers as About.
  return (
    <ProductPagesProvider pages={productPageLinks()}>
      <SiteDialogs>
        <ProductInkPage product={{ ...product, ink: product.ink }} />
      </SiteDialogs>
    </ProductPagesProvider>
  );
}
return <ProductPageView product={product} />;
```

with imports:

```tsx
import { ProductPagesProvider } from "@/components/home/product-action";
import { SiteDialogs } from "@/components/ink/dialogs";
import { getProduct, productPageLinks, productSlugs } from "@/components/product/catalog";
import { ProductInkPage } from "@/components/product/ink/product-ink";
```

- [ ] **Step 10: Run the test to see it pass**

Run: `python -X utf8 scripts/qa/qa_nuricell_ink.py http://localhost:3032 --only=shell,others`
Expected: all PASS. Look at `scripts/qa/out/nuricell-ink/shell-1440.png` and `shell-390.png`: the name parts round the bottle on paper (desktop), stacks over it (phone), menu bar and crane footer present. Run `npm --prefix C:/Users/mcbig/Documents/codes/bigh-nuricell-ink run lint` and `npx tsc --noEmit -p C:/Users/mcbig/Documents/codes/bigh-nuricell-ink`: no errors.

- [ ] **Step 11: Commit**

```bash
cd "C:/Users/mcbig/Documents/codes/bigh-nuricell-ink" && npx prettier --write src/components/product src/app/[locale]/products scripts/qa/qa_nuricell_ink.py && git add -A src scripts/qa/qa_nuricell_ink.py && git commit -m "feat(nuricell): the ink page's frame and opening; other products keep their template" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: One painting per chapter, and the lantern's light

**Files:**

- Create: `src/components/product/ink/ink-chapter.tsx`, `src/components/product/ink/why.tsx`
- Modify: `src/components/product/ink/product-ink.tsx`, `src/components/product/ink/product-ink.module.css`, `scripts/qa/qa_nuricell_ink.py`

**Interfaces:**

- Consumes: `ProductInk`, `InkProduct`, `InkArt` (Task 3).
- Produces:
  - `export const CAPTIONS = { illustration: "Illustration", portrait: "Portrait painting" } as const`
  - `export const PICTURE_SIZES: string`
  - `export function titleId(id: ChapterId): string` → `"chapter-<id>-title"`
  - `export function InkChapter(props: { id: ChapterId; picture: ReactNode; children: ReactNode; className?: string })`
  - `export function InkFigure(props: { art: InkArt; alt: string; caption?: string | null; imgRef?: Ref<HTMLImageElement>; attrs?: Record<string, string | undefined>; eager?: boolean; children?: ReactNode })`
  - `export function Why(props: { product: InkProduct; motion: boolean })`

- [ ] **Step 1: Write the failing tests** — add to `scripts/qa/qa_nuricell_ink.py` (before `SECTIONS`) and register them: `SECTIONS = {"shell": shell, "others": others, "multiply": multiply, "lantern": lantern, "nojs": nojs}`.

```python
STACKING = """(el) => {
  // Each element from the figure's parent up to the page root that makes a stacking context.
  const found = [];
  for (let e = el.parentElement; e && !e.matches('[data-look="ink"]'); e = e.parentElement) {
    const s = getComputedStyle(e);
    const why = [];
    if (s.transform !== 'none') why.push('transform');
    if (s.translate !== 'none' || s.scale !== 'none' || s.rotate !== 'none') why.push('translate/scale/rotate');
    if (Number(s.opacity) < 1) why.push('opacity');
    if (s.filter !== 'none') why.push('filter');
    if (s.maskImage && s.maskImage !== 'none') why.push('mask');
    if (s.isolation === 'isolate') why.push('isolation');
    if (s.mixBlendMode !== 'normal') why.push('blend');
    if (s.position !== 'static' && s.zIndex !== 'auto') why.push('z-index');
    if (['fixed', 'sticky'].includes(s.position)) why.push(s.position);
    if (s.willChange && s.willChange !== 'auto') why.push('will-change');
    if (/paint|layout|strict|content/.test(s.contain)) why.push('contain');
    if (why.length) found.push((e.tagName + '.' + e.className).slice(0, 60) + ': ' + why.join(','));
  }
  return found;
}"""


def multiply(browser):
    for w, h in [(1440, 900), (390, 844)]:
        ctx, page, _, _ = opened(browser, w, h, reduced=True)
        figures = page.locator("[data-chapter] figure[data-picture]:not([data-stand])")
        check(f"multiply {w}: a painting in every chapter but the opening and buy", figures.count() >= 1, str(figures.count()))
        for i in range(figures.count()):
            fig = figures.nth(i)
            chapter = fig.evaluate("f => f.closest('[data-chapter]').dataset.chapter")
            blend = fig.evaluate("f => getComputedStyle(f).mixBlendMode")
            check(f"multiply {w} {chapter}: the figure multiplies", blend == "multiply", blend)
            found = fig.evaluate(STACKING)
            check(f"multiply {w} {chapter}: no stacking context above it", not found, "; ".join(found))
            # The picture's top-left corner matches the paper just outside it (no box).
            bring(page, f'[data-chapter="{chapter}"] figure[data-picture]', 160)
            page.wait_for_timeout(300)
            box = fig.locator("img").first.bounding_box()
            shot = OUT / f"multiply-{w}-{chapter}.png"
            page.screenshot(path=str(shot))
            img = Image.open(shot).convert("RGB")
            x, y = int(box["x"]) + 3, int(box["y"]) + 3
            inside = img.getpixel((x, y))
            outside = img.getpixel((max(0, int(box["x"]) - 12), y))
            diff = max(abs(a - b) for a, b in zip(inside, outside))
            check(f"multiply {w} {chapter}: no box at its corner", diff <= 6, f"{inside} vs {outside}")
        ctx.close()


def lantern_state(page):
    return page.evaluate(
        """() => { const f = document.querySelector('[data-lantern]');
                   const lit = f.querySelector('[data-lit]'); const unlit = f.querySelector('img:not([data-lit])');
                   return { light: f.dataset.light, bloom: unlit.dataset.bloom, lit: Number(getComputedStyle(lit).opacity) }; }"""
    )


def lantern(browser):
    ctx, page, _, _ = opened(browser, 1440, 900)
    first = lantern_state(page)
    check("lantern: off before it arrives", first["light"] == "off" and first["lit"] < 0.05, str(first))
    # No lighter flash by construction: both layers draw normally inside the figure, which alone
    # multiplies, so the change is a plain cross-fade (two multiplied layers would lighten mid-way).
    blends = page.evaluate(
        """() => { const f = document.querySelector('[data-lantern]');
                   return [getComputedStyle(f).mixBlendMode, ...[...f.querySelectorAll('img')].map(i => getComputedStyle(i).mixBlendMode)]; }"""
    )
    check("lantern: one blend group (figure multiplies, its layers normal)", blends[0] == "multiply" and all(b == "normal" for b in blends[1:]), str(blends))
    bring(page, "[data-lantern]", 160)
    page.wait_for_timeout(500)
    early = lantern_state(page)
    check("lantern: still off as it starts to bloom", early["bloom"] in ("in", "done") and early["lit"] < 0.05, str(early))
    page.wait_for_timeout(1700)
    page.screenshot(path=str(OUT / "lantern-unlit-1440.png"))
    page.wait_for_timeout(5000)
    last = lantern_state(page)
    check("lantern: the light comes on", last["light"] == "on" and last["lit"] > 0.95, str(last))
    page.screenshot(path=str(OUT / "lantern-lit-1440.png"))
    before = Image.open(OUT / "lantern-unlit-1440.png").convert("RGB")
    after = Image.open(OUT / "lantern-lit-1440.png").convert("RGB")
    box = page.locator("[data-lantern] img").first.bounding_box()
    centre = (int(box["x"] + box["width"] / 2), int(box["y"] + box["height"] / 2))
    warm = lambda px: px[0] - px[2]
    check("lantern: it glows warmer once lit", warm(after.getpixel(centre)) > warm(before.getpixel(centre)) + 20, f"{before.getpixel(centre)} -> {after.getpixel(centre)}")
    ctx.close()
    ctx, page, _, _ = opened(browser, 1440, 900, reduced=True)
    still = lantern_state(page)
    check("lantern: reduced motion, lit from the start", still["light"] == "on" and still["lit"] > 0.95, str(still))
    ctx.close()


def nojs(browser):
    ctx, page, _, _ = opened(browser, 1440, 900, js=False)
    shown = page.evaluate(
        """() => [...document.querySelectorAll('[data-chapter] figure[data-picture] img')].map(i => {
             const s = getComputedStyle(i); return { src: i.getAttribute('src'), o: Number(s.opacity), m: s.maskSize || s.webkitMaskSize };
           })"""
    )
    hidden = [s["src"] for s in shown if s["o"] < 0.95 or (s["m"] and s["m"].startswith("0%"))]
    check("nojs: every painting shown", shown and not hidden, ", ".join(hidden[:4]))
    lit = page.evaluate("() => Number(getComputedStyle(document.querySelector('[data-lantern] [data-lit]')).opacity)")
    check("nojs: the lantern lit", lit > 0.95, str(lit))
    ctx.close()
```

- [ ] **Step 2: Run them to see them fail**

Run: `python -X utf8 scripts/qa/qa_nuricell_ink.py http://localhost:3032 --only=multiply,lantern,nojs`
Expected: FAIL (no figures, no `[data-lantern]` yet: a Playwright error on `lantern_state` counts as the failure).

- [ ] **Step 3: The chapter and figure** — `src/components/product/ink/ink-chapter.tsx`:

```tsx
"use client";

import Image from "next/image";
import type { CSSProperties, ReactNode, Ref } from "react";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import type { InkArt } from "../product-types";
import { anchorId, type ChapterId } from "../template-chapters-kit";
import styles from "./product-ink.module.css";

/** The honesty tags (DESIGN.md): "Illustration" (catalog m574) and Dr. Liu's "Portrait painting". */
export const CAPTIONS = { illustration: "Illustration", portrait: "Portrait painting" } as const;

/** Every chapter painting is drawn the same size: its column up to --picture-width (520px). */
export const PICTURE_SIZES = "(max-width: 599px) 88vw, (max-width: 959px) 520px, 520px";

export function titleId(id: ChapterId) {
  return `${anchorId(id)}-title`;
}

/**
 * One painting as its own blend group: the figure multiplies onto the page's paper and its pictures
 * draw normally inside it, so the figure may be sticky, and a lit layer may cross-fade over an
 * unlit one, without a white box or a lighter flash. The painting blooms in (the kit's useBloom,
 * server-marked "waiting" so it never paints whole first); gold leaf takes the kit's glint.
 */
export function InkFigure({
  art,
  alt,
  caption = CAPTIONS.illustration,
  imgRef,
  attrs,
  eager = false,
  children,
}: {
  art: InkArt;
  /** English source of the painting's description (translated through the catalogs). */
  alt: string;
  caption?: string | null;
  imgRef?: Ref<HTMLImageElement>;
  attrs?: Record<string, string | undefined>;
  eager?: boolean;
  /** Layers drawn over the painting, inside its blend group (the lantern's light). */
  children?: ReactNode;
}) {
  const copy = useCopy();
  return (
    <figure className={styles.figure} data-picture="" {...attrs}>
      <span className={styles.body}>
        <Image
          ref={imgRef}
          className={styles.art}
          src={art.src}
          alt={copy(alt)}
          width={art.width}
          height={art.height}
          sizes={PICTURE_SIZES}
          loading={eager ? "eager" : undefined}
          data-bloom="waiting"
        />
        {art.gold ? (
          <span
            className={base.gold}
            style={{ ["--gold" as string]: `url(${art.gold})` } as CSSProperties}
          />
        ) : null}
        {children}
      </span>
      {caption ? (
        <figcaption className={`${base.caption} ${styles.caption}`}>{copy(caption)}</figcaption>
      ) : null}
    </figure>
  );
}

/** One chapter: its painting (left from 960px, first on phones) and its words. */
export function InkChapter({
  id,
  picture,
  children,
  className = "",
}: {
  id: ChapterId;
  picture: ReactNode;
  children: ReactNode;
  className?: string;
}) {
  return (
    <section
      id={anchorId(id)}
      className={`${styles.chapter} ${className}`}
      data-chapter={id}
      aria-labelledby={titleId(id)}
    >
      <div className={`${base.wrap} ${styles.spread}`}>
        {picture}
        <div className={styles.words} data-words="">
          {children}
        </div>
      </div>
    </section>
  );
}
```

- [ ] **Step 4: The lantern** — `src/components/product/ink/why.tsx`:

```tsx
"use client";

import Image from "next/image";
import { useEffect, useRef, useState, type CSSProperties, type RefObject } from "react";
import { CountUp } from "@/components/about/count-up";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import type { InkProduct } from "../product-types";
import { CAPTIONS, InkChapter, InkFigure, PICTURE_SIZES, titleId } from "./ink-chapter";
import styles from "./product-ink.module.css";

/** How long after the unlit lantern starts to bloom its light starts to come on (the blot is then
 *  well over half grown; the light takes one and a quarter breaths, product-ink.module.css). */
const LIGHT_AFTER = 1800;

/**
 * The signature moment: the light comes on once, a breath after the lantern starts to bloom. It
 * watches the unlit picture's data-bloom, which the kit's useBloom sets as it enters the window.
 * Reduced motion: lit from the first paint. No script: the stylesheet shows it lit.
 */
function useLightComesOn(unlit: RefObject<HTMLImageElement | null>, motion: boolean) {
  const [on, setOn] = useState(false);
  useEffect(() => {
    const img = unlit.current;
    if (!img) return;
    if (!motion) {
      setOn(true);
      return;
    }
    let timer = 0;
    const observer = new MutationObserver(() => check());
    const check = () => {
      if (img.dataset.bloom !== "in" && img.dataset.bloom !== "done") return;
      observer.disconnect();
      timer = window.setTimeout(() => setOn(true), LIGHT_AFTER);
    };
    observer.observe(img, { attributes: true, attributeFilter: ["data-bloom"] });
    check();
    return () => {
      observer.disconnect();
      window.clearTimeout(timer);
    };
  }, [unlit, motion]);
  return on;
}

export function Why({ product, motion }: { product: InkProduct; motion: boolean }) {
  const copy = useCopy();
  const why = product.why;
  const art = product.ink.why;
  const unlit = useRef<HTMLImageElement>(null);
  const on = useLightComesOn(unlit, motion);
  if (!why) return null;
  return (
    <InkChapter
      id="why"
      picture={
        <InkFigure
          art={art.unlit}
          alt={art.alt}
          caption={CAPTIONS.illustration}
          imgRef={unlit}
          attrs={{ "data-lantern": "", "data-light": on ? "on" : "off" }}
        >
          <Image
            className={styles.lit}
            src={art.lit.src}
            alt=""
            width={art.lit.width}
            height={art.lit.height}
            sizes={PICTURE_SIZES}
            data-lit=""
          />
          {art.lit.gold ? (
            <span
              className={`${base.gold} ${styles.litGold}`}
              style={{ ["--gold" as string]: `url(${art.lit.gold})` } as CSSProperties}
            />
          ) : null}
        </InkFigure>
      }
    >
      <p className={`${base.label} ${styles.label}`}>{copy(why.label)}</p>
      <h2 id={titleId("why")} className={`${base.display} ${styles.heading}`}>
        {copy(why.title)}
      </h2>
      {why.lines.map((line) => (
        <p key={line} className={styles.text}>
          {copy(line)}
        </p>
      ))}
      {why.facts?.length ? (
        <dl className={styles.facts}>
          {why.facts.map((fact) => (
            <div key={fact.line}>
              <dt className={styles.figureNumber}>
                <CountUp to={fact.figure} suffix={fact.unit} />
              </dt>
              <dd>{copy(fact.line)}</dd>
            </div>
          ))}
        </dl>
      ) : null}
      {why.comparison ? <p className={styles.comparison}>{copy(why.comparison)}</p> : null}
      {why.source ? <p className={`${base.caption} ${styles.source}`}>{copy(why.source)}</p> : null}
    </InkChapter>
  );
}
```

- [ ] **Step 5: Wire it in** — in `product-ink.tsx` import `{ Why } from "./why"` and change the render prop to `{(motion) => (` … `<Opening product={product} />` then `<Why product={product} motion={motion} />`.

- [ ] **Step 6: Append the chapter styles** to `product-ink.module.css`:

```css
/* 2-7. Chapters: one painting and its words, the painting left from 960px, first on phones. */
.page .chapter {
  padding-block: var(--chapter-half);
  /* Deep links land the chapter's first content just under the settled bar (globals.css keeps a
     150px scroll-padding-top). */
  scroll-margin-top: calc(108px - 150px - var(--chapter-half));
}

.page .spread {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  row-gap: clamp(24px, 5vw, 40px);
  align-items: center;
}

.page .words {
  min-width: 0;
}

@media (min-width: 600px) and (max-width: 959px) {
  .page .spread {
    max-width: calc(640px + 2 * var(--gutter));
  }
}

@media (min-width: 960px) {
  .page .spread {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    column-gap: var(--gap);
  }
}

/* The painting: its own blend group. From 960px it stays put while long words scroll beside it,
   inside its own grid cell (so it leaves with its chapter). */
.page figure.figure {
  justify-self: center;
  width: min(100%, var(--picture-width));
  margin: 0;
  mix-blend-mode: multiply;
}

@media (min-width: 960px) {
  .page figure.figure {
    position: sticky;
    top: 120px;
  }
}

.page .body {
  position: relative;
  display: block;
}

.page img.art {
  display: block;
  width: 100%;
  height: auto;
}

.page figcaption.caption {
  margin-top: 8px;
  text-align: right;
}

.page p.label {
  margin: 0 0 14px;
}

.page h2.heading {
  margin: 0 0 clamp(16px, 1.6vw, 24px);
  font-size: clamp(min(36px, 9.2vw), 3.2vw, 50px);
  line-height: 1.08;
  text-wrap: balance;
}

.page .words p.text + p.text {
  margin-top: 12px;
}

.page p.small {
  margin: 14px 0 0;
  max-width: 34em;
  color: var(--muted);
  font-size: 15px;
  line-height: 1.5;
}

/* The lantern's light: the lit painting over the unlit one, in the same blend group, so the change
   is a plain cross-fade with no lighter step. It waits while the unlit one waits to bloom. */
.page img.lit {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
}

.page [data-light="on"] img.lit {
  opacity: 1;
  transition: opacity calc(var(--breath) * 1.25) var(--ease);
}

.page [data-light] [data-bloom="waiting"] ~ img.lit {
  opacity: 0;
  transition: none;
}

.page .litGold {
  opacity: 0;
}

.page [data-light="on"] .litGold {
  opacity: 1;
}

.page dl.facts {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 24px;
  margin: clamp(24px, 3vw, 40px) 0 0;
  padding-top: 20px;
  border-top: 1px solid var(--hair);
}

.page .facts dd {
  margin: 8px 0 0;
  color: var(--muted);
  font-size: 17px;
  line-height: 1.45;
}

.page .figureNumber {
  font-family: var(--display-font);
  font-size: clamp(56px, 6vw, 92px);
  font-weight: 300;
  line-height: 1;
  letter-spacing: -0.03em;
  font-variant-numeric: tabular-nums;
}

.page p.comparison {
  margin: clamp(24px, 3vw, 36px) 0 0;
  font-size: clamp(22px, 1.9vw, 28px);
  line-height: 1.3;
  text-wrap: balance;
}

.page p.source {
  margin-top: 16px;
}

/* No script: nothing ever blooms, so every painting is shown whole and the lantern lit. Reduced
   motion, too, is complete from the first paint (no blur). :global([data-look]) puts these above
   the kit's .look rules whatever order they load in. */
@media (scripting: none) {
  :global([data-look="ink"]).page [data-bloom="waiting"] {
    -webkit-mask: none;
    mask: none;
    filter: none;
  }

  :global([data-look="ink"]).page img.lit {
    opacity: 1;
  }
}

@media (prefers-reduced-motion: reduce) {
  :global([data-look="ink"]).page [data-bloom="waiting"] {
    filter: none;
  }
}
```

- [ ] **Step 7: Run the tests to see them pass**

Run: `python -X utf8 scripts/qa/qa_nuricell_ink.py http://localhost:3032 --only=shell,multiply,lantern,nojs`
Expected: all PASS. If "no stacking context above it" fails, the detail names the element and the property: remove that property from the element (never move the blend off the figure). If "one blend group" fails, the lit layer is outside the figure or has its own `mix-blend-mode` (the kit's `.ink` class must not be on either lantern picture). Look at `lantern-unlit-1440.png` then `lantern-lit-1440.png`: the same lantern, then glowing beside its words.

- [ ] **Step 8: Commit**

```bash
cd "C:/Users/mcbig/Documents/codes/bigh-nuricell-ink" && npx prettier --write src/components/product/ink scripts/qa/qa_nuricell_ink.py && git add -A src/components/product/ink scripts/qa/qa_nuricell_ink.py && git commit -m "feat(nuricell): one painting per chapter, and the lantern's light comes on" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: What's inside and the research

**Files:**

- Create: `src/components/product/ink/inside.tsx`, `src/components/product/ink/research.tsx`
- Modify: `src/components/product/template-chapters-kit.ts` (gain `WORDS`), `src/components/product/signature/capsule-cutaway.tsx` (import `WORDS` from the kit), `product-ink.tsx`, `product-ink.module.css`, `scripts/qa/qa_nuricell_ink.py`

**Interfaces:**

- Consumes: `InkChapter`, `InkFigure`, `titleId` (Task 4).
- Produces: `export const WORDS: readonly string[]` in `template-chapters-kit.ts`; `export function Inside({ product }: { product: InkProduct })`; `export function Research({ product }: { product: InkProduct })`.

- [ ] **Step 1: Write the failing tests** — add `words` and `sticky` and register them in `SECTIONS`:

```python
def nuricell_strings():
    """Every word of nuricell.ts the page must show: its string literals, less picture alts and
    pictures, keys, units and colours."""
    source = (REPO / "src/components/product/products/nuricell.ts").read_text(encoding="utf-8")
    keep = []
    for line in source.splitlines():
        if re.search(r"\b(alt|src|accent|key|from|to|unit|signature)\s*:", line) or line.strip().startswith("//"):
            continue
        for text in re.findall(r'"((?:[^"\\]|\\.)*)"', line):
            if len(text) < 4 or text.startswith(("/", "#", "../", "./")) or re.fullmatch(r"[a-z0-9-]+/?", text):
                continue
            keep.append(text)
    return keep


EXPECT = {
    "why": "lantern-unlit",
    "inside": "capsule",
    "research": "books",
    "people": "liu",
    "daily": "breakfast",
    "buy": "stroke",
}


def words(browser, chapters=("overview", "why", "inside", "research")):
    ctx, page, _, _ = opened(browser, 1440, 900, reduced=True)
    text = re.sub(r"\s+", " ", page.locator("main").text_content())
    # Words of chapters not built yet are left for the task that builds them.
    missing = [s for s in nuricell_strings() if re.sub(r"\s+", " ", s) not in text]
    print(f"words: {len(missing)} strings not on the page yet: {missing[:6]}")
    for chapter in chapters:
        if chapter in EXPECT:
            n = page.locator(f'[data-chapter="{chapter}"] img[src*="{EXPECT[chapter]}"]').count()
            check(f"words {chapter}: its own painting", n >= 1)
    built = {
        "inside": ["Inside every capsule, four ingredients.", "Acetyl-L-carnitine", "Creatine", "Alpha-lipoic acid",
                   "Choline", "Why these four work together", "Fuel in, energy out", "Energy on hand",
                   "Two halves of a messenger"],
        "research": ["The research on the ingredients", "Show all 7 studies"],
    }
    for chapter in chapters:
        for s in built.get(chapter, []):
            check(f"words {chapter}: “{s}”", s in text)
    ctx.close()
    return missing


def sticky(browser):
    ctx, page, _, _ = opened(browser, 1440, 900, reduced=True)
    page.locator('[data-chapter="research"] button[aria-expanded]').click()
    for summary in page.locator('[data-chapter="research"] summary').all():
        summary.click()
    for chapter in ("inside", "research"):
        bring(page, f'[data-chapter="{chapter}"]', 0)
        tall = page.evaluate(f"() => document.querySelector('[data-chapter=\"{chapter}\"]').getBoundingClientRect().height")
        worst = 0.0
        for step in range(0, int(tall) + 900, 120):
            r = page.evaluate(
                f"""() => {{ const c = document.querySelector('[data-chapter="{chapter}"]');
                    const f = c.querySelector('figure[data-picture]').getBoundingClientRect();
                    const s = c.getBoundingClientRect(); return [f.top - s.top, s.bottom - f.bottom]; }}"""
            )
            worst = min(worst, r[0], r[1])
            page.mouse.wheel(0, 120)
            page.wait_for_timeout(30)
        check(f"sticky {chapter}: the painting stays inside its chapter", worst >= -1, f"worst {worst:.1f}px")
    ctx.close()
```

and change the main loop's `words` call to accept the default (it is a section like the others).

- [ ] **Step 2: Run them to see them fail**

Run: `python -X utf8 scripts/qa/qa_nuricell_ink.py http://localhost:3032 --only=words,sticky`
Expected: FAIL (`words inside: its own painting`, the inside and research strings, and the sticky section's missing elements).

- [ ] **Step 3: Move `WORDS` to the kit** — in `template-chapters-kit.ts` add:

```ts
/** Small counts as words, for headings ("Inside every capsule, four ingredients."). */
export const WORDS = [
  "",
  "one",
  "two",
  "three",
  "four",
  "five",
  "six",
  "seven",
  "eight",
  "nine",
  "ten",
] as const;
```

In `signature/capsule-cutaway.tsx` delete its `const WORDS = [...]` line and add `WORDS` to its import from `"../template-chapters-kit"` (behaviour unchanged).

- [ ] **Step 4: What's inside** — `src/components/product/ink/inside.tsx`:

```tsx
"use client";

import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import type { InkProduct, ProductSynergy } from "../product-types";
import { WORDS } from "../template-chapters-kit";
import { InkChapter, InkFigure, titleId } from "./ink-chapter";
import styles from "./product-ink.module.css";

// Chapter 3: the capsule open, its four heaps sized by amount, beside the ingredients (amount,
// name, what it does, the label's form when it differs) and how they work together.
export function Inside({ product }: { product: InkProduct }) {
  const copy = useCopy();
  const count = product.ingredients.length;
  const names = Object.fromEntries(product.ingredients.map((item) => [item.key, item.name]));
  return (
    <InkChapter
      id="inside"
      picture={<InkFigure art={product.ink.inside} alt={product.ink.inside.alt} />}
    >
      <p className={`${base.label} ${styles.label}`}>{copy("What’s inside")}</p>
      <h2 id={titleId("inside")} className={`${base.display} ${styles.heading}`}>
        {copy("Inside every capsule, {count} ingredients.", {
          count: copy(WORDS[count] ?? String(count)),
        })}
      </h2>
      <table className={styles.ingredients}>
        <caption className={`${base.caption} ${styles.tableNote}`}>
          {copy(product.notes.label)}
        </caption>
        <tbody>
          {product.ingredients.map((item) => (
            <tr key={item.key}>
              <td className={styles.amount}>
                {item.amount}
                <span className={styles.unit}> {item.unit}</span>
              </td>
              <th scope="row">
                <span className={styles.ingredient}>{copy(item.name)}</span>
                {item.role ? <span className={styles.role}>{copy(item.role)}</span> : null}
                {item.form !== item.name ? (
                  <span className={styles.form}>
                    {copy("On the label: {form}", { form: copy(item.form) })}
                  </span>
                ) : null}
              </th>
            </tr>
          ))}
        </tbody>
      </table>
      <p className={styles.small}>{copy(product.otherIngredients)}</p>
      <p className={styles.small}>{copy(product.notes.science)}</p>
      {product.synergy ? <Synergy synergy={product.synergy} names={names} /> : null}
    </InkChapter>
  );
}

function Synergy({ synergy, names }: { synergy: ProductSynergy; names: Record<string, string> }) {
  const copy = useCopy();
  return (
    <div className={styles.synergy} data-synergy="">
      <h3 className={styles.subheading}>{copy(synergy.title)}</h3>
      <ul className={styles.pairs}>
        {synergy.links.map((link) => (
          <li key={link.title}>
            <p className={styles.pairOf}>
              {copy(names[link.from] ?? link.from)} + {copy(names[link.to] ?? link.to)}
            </p>
            <h4 className={styles.pairTitle}>{copy(link.title)}</h4>
            <p className={styles.pairLine}>{copy(link.line)}</p>
            {link.evidence ? <p className={styles.small}>{copy(link.evidence)}</p> : null}
          </li>
        ))}
      </ul>
      <p className={`${base.caption} ${styles.note}`}>{copy(synergy.note)}</p>
    </div>
  );
}
```

- [ ] **Step 5: The research** — `src/components/product/ink/research.tsx`:

```tsx
"use client";

import { useState } from "react";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import type { InkProduct } from "../product-types";
import { InkChapter, InkFigure, titleId } from "./ink-chapter";
import styles from "./product-ink.module.css";

/** Studies shown before "Show all": the list stays about as tall as its painting. */
const FIRST = 5;

// Chapter 4: seven books as stepping stones (seven studies) beside the studies on hairlines; each
// opens with its round toggle to what it found and a link to it.
export function Research({ product }: { product: InkProduct }) {
  const copy = useCopy();
  const [all, setAll] = useState(false);
  const studies = product.studies;
  return (
    <InkChapter
      id="research"
      picture={<InkFigure art={product.ink.research} alt={product.ink.research.alt} />}
    >
      <p className={`${base.label} ${styles.label}`}>{copy("The research")}</p>
      <h2 id={titleId("research")} className={`${base.display} ${styles.heading}`}>
        {copy(product.researchTitle ?? "The research on the ingredients")}
      </h2>
      <p className={styles.small}>{copy(product.notes.research)}</p>
      <ul className={styles.studies}>
        {studies.map((study, i) => (
          <li key={study.url} hidden={!all && i >= FIRST} data-study="">
            <details className={styles.study}>
              <summary className={styles.summary}>
                <span className={styles.year}>{study.year}</span>
                <span className={styles.what}>
                  <span className={styles.studyTitle}>{copy(study.title)}</span>
                  <span className={styles.meta}>
                    {copy(study.kind)} · {study.journal}
                  </span>
                </span>
                <span className={styles.toggle} aria-hidden="true">
                  +
                </span>
              </summary>
              <div className={styles.open}>
                <p className={styles.small}>{copy(study.note)}</p>
                <a
                  href={study.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={base.textLink}
                >
                  {copy("Read the study")}
                  <span className={base.visuallyHidden}> {copy("(opens in a new tab)")}</span>
                </a>
              </div>
            </details>
          </li>
        ))}
      </ul>
      {studies.length > FIRST ? (
        <button
          type="button"
          className={`${base.pill} ${base.pillGhost} ${styles.showAll}`}
          aria-expanded={all}
          onClick={() => setAll((open) => !open)}
        >
          {copy(all ? "Show fewer studies" : "Show all {count} studies", { count: studies.length })}
        </button>
      ) : null}
    </InkChapter>
  );
}
```

- [ ] **Step 6: Wire them in and style them** — in `product-ink.tsx` render `<Inside product={product} />` and `{product.studies.length > 0 ? <Research product={product} /> : null}` after `<Why …/>`. Append to `product-ink.module.css`:

```css
/* 3. What's inside. */
.page table.ingredients {
  width: 100%;
  margin-top: clamp(16px, 2vw, 24px);
  border-collapse: collapse;
  caption-side: bottom;
}

.page .ingredients tr {
  border-top: 1px solid var(--hair);
}

.page .ingredients td,
.page .ingredients th {
  padding: 16px 0;
  vertical-align: top;
  text-align: left;
  font-weight: inherit;
}

.page td.amount {
  width: 9.5ch;
  padding-right: 20px;
  font-family: var(--display-font);
  font-size: clamp(40px, 3.6vw, 56px);
  font-weight: 300;
  line-height: 1;
  letter-spacing: -0.03em;
  white-space: nowrap;
  font-variant-numeric: tabular-nums;
}

.page .unit {
  font-size: 0.42em;
  letter-spacing: 0;
}

.page .ingredient {
  display: block;
  font-size: 20px;
  font-weight: 500;
}

.page .role,
.page .form {
  display: block;
  margin-top: 4px;
  color: var(--muted);
  font-size: 16px;
  line-height: 1.45;
}

.page caption.tableNote {
  padding-top: 12px;
  text-align: left;
}

.page .synergy {
  margin-top: clamp(32px, 4vw, 56px);
}

.page h3.subheading {
  margin: 0 0 8px;
  font-size: clamp(24px, 2vw, 30px);
  font-weight: 500;
  letter-spacing: -0.015em;
}

.page ul.pairs {
  display: grid;
  margin: 0;
  padding: 0;
  list-style: none;
}

.page .pairs li {
  padding: 16px 0;
  border-top: 1px solid var(--hair);
}

.page p.pairOf {
  margin: 0;
  color: var(--muted);
  font-size: 15px;
}

.page h4.pairTitle {
  margin: 4px 0;
  font-size: 19px;
  font-weight: 500;
}

.page p.pairLine {
  margin: 0;
  font-size: 17px;
  line-height: 1.5;
}

.page p.note {
  margin-top: 12px;
}

/* 4. The research: studies on hairlines with round toggles (the homepage's research list). */
.page ul.studies {
  display: grid;
  margin: clamp(16px, 2vw, 24px) 0 0;
  padding: 0;
  list-style: none;
}

.page .studies li {
  border-top: 1px solid var(--hair);
}

.page summary.summary {
  display: grid;
  grid-template-columns: 4.5ch minmax(0, 1fr) 44px;
  align-items: center;
  gap: 16px;
  min-height: 56px;
  padding: 12px 0;
  cursor: pointer;
  list-style: none;
}

.page summary.summary::-webkit-details-marker {
  display: none;
}

.page .year {
  font-size: 22px;
  font-weight: 300;
  font-variant-numeric: tabular-nums;
}

.page .studyTitle {
  display: block;
  font-size: 17px;
  font-weight: 500;
}

.page .meta {
  display: block;
  color: var(--muted);
  font-size: 15px;
}

.page .toggle {
  display: grid;
  place-items: center;
  width: 44px;
  height: 44px;
  border: 1px solid var(--hair);
  border-radius: 50%;
  font-size: 22px;
  transition: rotate 0.6s var(--ease);
}

.page details[open] .toggle {
  rotate: 45deg;
}

.page .open {
  display: grid;
  justify-items: start;
  gap: 8px;
  padding: 0 0 20px calc(4.5ch + 16px);
}

.page button.showAll {
  margin-top: 20px;
}
```

- [ ] **Step 7: Run the tests to see them pass**

Run: `python -X utf8 scripts/qa/qa_nuricell_ink.py http://localhost:3032 --only=shell,multiply,words,sticky`
Expected: all PASS; the `words:` line lists only people, daily, buy and after strings as not yet on the page. Look at `multiply-1440-inside.png` and `multiply-1440-research.png` against the mockups `3-inside.jpg` and `4-research.jpg`.

- [ ] **Step 8: Commit**

```bash
cd "C:/Users/mcbig/Documents/codes/bigh-nuricell-ink" && npx prettier --write src/components/product scripts/qa/qa_nuricell_ink.py && git add -A src/components/product scripts/qa/qa_nuricell_ink.py && git commit -m "feat(nuricell): what's inside, how the four work together, and the research" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 6: Dr. Liu, how to take it, and buy

**Files:**

- Create: `src/components/product/ink/people.tsx`, `src/components/product/ink/daily.tsx`, `src/components/product/ink/buy.tsx`
- Modify: `src/components/product/template-chapters-daily.tsx` (export `titleFor`), `product-ink.tsx`, `product-ink.module.css`, `scripts/qa/qa_nuricell_ink.py`

**Interfaces:**

- Consumes: `InkChapter`, `InkFigure`, `CAPTIONS`, `titleId` (Task 4); `monthPlan` and `titleFor` from `template-chapters-daily.tsx`.
- Produces: `People({ product })`, `Daily({ product })`, `Buy({ product })`, each `{ product: InkProduct }`.

- [ ] **Step 1: Write the failing tests** — add `sum` and extend `words` (the default chapters become all seven), register `sum`:

```python
def sum_check(browser):
    ctx, page, _, _ = opened(browser, 1440, 900, reduced=True)
    painted = page.locator('[data-sum] img[src*="sum-"]')
    check("sum: painted for NuriCell's 3 × 30 = 90", painted.count() == 1)
    said = page.locator("[data-sum] [data-sum-text]").text_content()
    check("sum: said in words for screen readers", "3" in said and "30" in said and "90" in said, said)
    labels = page.evaluate(
        """() => { const img = document.querySelector('[data-sum] img').getBoundingClientRect();
                   return [...document.querySelectorAll('[data-sum] [data-sum-label]')].map(l => {
                     const r = l.getBoundingClientRect(); return { centre: (r.left + r.width / 2 - img.left) / img.width, top: r.top - img.bottom }; }); }"""
    )
    art = page.evaluate("() => JSON.parse(document.querySelector('[data-sum]').dataset.centres)")
    check("sum: three captions", len(labels) == 3, str(labels))
    near = all(abs(l["centre"] - c) < 0.06 for l, c in zip(labels, art))
    check("sum: each caption under its number", near, f"{[round(l['centre'], 3) for l in labels]} vs {art}")
    ctx.close()
```

Register as `"sum": sum_check`. In `words`, change the default to `chapters=tuple(CHAPTERS)` and add to `built`:

```python
        "people": ["The people behind the formula", "Dr. Jiankang Liu", "Chief Scientific Advisor, BiGH", "Portrait painting"],
        "daily": ["How to take it", "One bottle, one month.", "Take 3 capsules once a day, with or after a meal.",
                  "capsules a day", "days", "capsules in each bottle"],
        "buy": ["In each bottle", "Formulated by Dr. Jiankang Liu.", "Add to cart"],
```

- [ ] **Step 2: Run them to see them fail**

Run: `python -X utf8 scripts/qa/qa_nuricell_ink.py http://localhost:3032 --only=words,sum`
Expected: FAIL on the people, daily and buy checks and on `sum`.

- [ ] **Step 3: Export `titleFor`** — in `template-chapters-daily.tsx` change `function titleFor(` to `export function titleFor(` (nothing else).

- [ ] **Step 4: Dr. Liu** — `src/components/product/ink/people.tsx`:

```tsx
"use client";

import Image from "next/image";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import type { InkProduct } from "../product-types";
import { CAPTIONS, InkChapter, InkFigure, titleId } from "./ink-chapter";
import styles from "./product-ink.module.css";

// Chapter 5: the person behind the formula. Dr. Liu as a painting in ink and colour (Mo's call,
// October 9, 2026; never black-and-white: in Asia that signals a person has died); a person
// without a painting keeps their photo on its mat; anyone else is text only, under the first.
export function People({ product }: { product: InkProduct }) {
  const copy = useCopy();
  const [lead, ...others] = product.people;
  if (!lead) return null;
  const picture = lead.painting ? (
    <InkFigure art={lead.painting} alt={lead.painting.alt} caption={CAPTIONS.portrait} />
  ) : lead.photo ? (
    <figure className={styles.photo} data-picture="" data-stand="">
      <Image
        src={lead.photo.src}
        alt={copy(lead.photo.alt)}
        width={lead.photo.width}
        height={lead.photo.height}
        sizes="320px"
      />
    </figure>
  ) : null;
  return (
    <InkChapter id="people" picture={picture}>
      <p className={`${base.label} ${styles.label}`}>{copy("The people behind the formula")}</p>
      <h2 id={titleId("people")} className={`${base.display} ${styles.heading}`}>
        {copy(lead.name)}
      </h2>
      <p className={styles.role}>{copy(lead.title)}</p>
      {lead.lines.map((line) => (
        <p key={line} className={styles.text}>
          {copy(line)}
        </p>
      ))}
      {others.map((person) => (
        <div key={person.name} className={styles.otherPerson}>
          <h3 className={styles.subheading}>{copy(person.name)}</h3>
          <p className={styles.role}>{copy(person.title)}</p>
          {person.lines.map((line) => (
            <p key={line} className={styles.text}>
              {copy(line)}
            </p>
          ))}
        </div>
      ))}
    </InkChapter>
  );
}
```

- [ ] **Step 5: How to take it** — `src/components/product/ink/daily.tsx`:

```tsx
"use client";

import Image from "next/image";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import type { InkProduct } from "../product-types";
import { monthPlan, titleFor } from "../template-chapters-daily";
import { InkChapter, InkFigure, titleId } from "./ink-chapter";
import styles from "./product-ink.module.css";

const LABELS = ["capsules a day", "days", "capsules in each bottle"] as const;

// Chapter 6: when (a light breakfast, three capsules beside it, the yolk the only gold) and how
// much (the serving as one painted sum, a caption under each number). The painted sum is shown
// only when its numbers are the serving's; otherwise the sum is set in type, so a changed label
// can never show a wrong painting.
export function Daily({ product }: { product: InkProduct }) {
  const copy = useCopy();
  const plan = monthPlan(product.serving);
  const { picture, sum } = product.ink.daily;
  const numbers = [plan.perDay, plan.days, plan.total];
  const painted = sum.numbers.length === 3 && sum.numbers.every((n, i) => n === numbers[i]);
  return (
    <InkChapter id="daily" picture={<InkFigure art={picture} alt={picture.alt} />}>
      <p className={`${base.label} ${styles.label}`}>{copy("How to take it")}</p>
      <h2 id={titleId("daily")} className={`${base.display} ${styles.heading}`}>
        {copy(titleFor(plan.days), { days: plan.days })}
      </h2>
      <figure
        className={styles.sum}
        data-sum=""
        data-centres={JSON.stringify(painted ? sum.centres : [1 / 6, 1 / 2, 5 / 6])}
      >
        {painted ? (
          <Image
            className={`${base.ink} ${styles.sumArt}`}
            src={sum.src}
            alt=""
            width={sum.width}
            height={sum.height}
            sizes="(max-width: 959px) 88vw, 560px"
            data-bloom="waiting"
            aria-hidden="true"
          />
        ) : (
          <p className={styles.sumType} aria-hidden="true">
            {plan.perDay} × {plan.days} = {plan.total}
          </p>
        )}
        <figcaption className={styles.sumLabels}>
          <span className={base.visuallyHidden} data-sum-text="">
            {copy("{perDay} capsules a day for {days} days: {total} capsules in each bottle.", {
              perDay: plan.perDay,
              days: plan.days,
              total: plan.total,
            })}
          </span>
          {LABELS.map((label, i) => (
            <span
              key={label}
              className={styles.sumLabel}
              data-sum-label=""
              aria-hidden="true"
              style={{
                left: `${((painted ? sum.centres[i] : [1 / 6, 1 / 2, 5 / 6][i]) * 100).toFixed(2)}%`,
              }}
            >
              {copy(label)}
            </span>
          ))}
        </figcaption>
      </figure>
      <p className={styles.text}>{copy(product.serving.use)}</p>
    </InkChapter>
  );
}
```

- [ ] **Step 6: Buy** — `src/components/product/ink/buy.tsx`:

```tsx
"use client";

import Image from "next/image";
import { contactShadow } from "@/components/home-v2/look-ink/assets";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { AddToCart } from "../add-to-cart";
import type { InkProduct } from "../product-types";
import { InkChapter, titleId } from "./ink-chapter";
import styles from "./product-ink.module.css";

// Chapter 7: the real bottle standing on one bold brush stroke (Mo, round 6). The stroke and the
// contact shadow multiply onto the paper; the bottle photo never does, so this figure is not a
// blend group (data-stand) and not sticky.
export function Buy({ product }: { product: InkProduct }) {
  const copy = useCopy();
  const stroke = product.ink.buy.stroke;
  return (
    <InkChapter
      id="buy"
      picture={
        <figure className={styles.buyStand} data-picture="" data-stand="">
          <Image
            className={`${base.ink} ${styles.stroke}`}
            src={stroke.src}
            alt=""
            width={stroke.width}
            height={stroke.height}
            sizes="(max-width: 959px) 88vw, 560px"
            data-bloom="waiting"
          />
          <Image
            className={`${base.ink} ${styles.buyContact}`}
            src={contactShadow.src}
            alt=""
            width={contactShadow.width}
            height={contactShadow.height}
            sizes="200px"
          />
          <Image
            className={styles.buyBottle}
            src={product.bottle.src}
            alt={copy("{name} bottle", { name: product.name })}
            width={product.bottle.width}
            height={product.bottle.height}
            sizes="(max-width: 959px) 56vw, 320px"
          />
        </figure>
      }
    >
      <p className={`${base.label} ${styles.label}`}>{copy(product.eyebrow)}</p>
      <h2 id={titleId("buy")} className={`${base.display} ${styles.buyName}`}>
        {product.name}
      </h2>
      <p className={styles.focus}>{copy(product.focus)}</p>
      <dl className={styles.rows}>
        <div>
          <dt>{copy("How to take it")}</dt>
          <dd>{copy(product.serving.use)}</dd>
        </div>
        <div>
          <dt>{copy("In each bottle")}</dt>
          <dd>{copy(product.serving.supply)}</dd>
        </div>
      </dl>
      <AddToCart wide />
      {product.credit ? <p className={styles.small}>{copy(product.credit)}</p> : null}
    </InkChapter>
  );
}
```

- [ ] **Step 7: Wire them in and style them** — in `product-ink.tsx` render, after Research: `{product.people.length > 0 ? <People product={product} /> : null}`, `<Daily product={product} />`, `<Buy product={product} />`. Append:

```css
/* 5. People. */
.page p.role {
  margin: -8px 0 16px;
  color: var(--muted);
  font-size: 19px;
}

.page .otherPerson {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid var(--hair);
}

.page figure.photo {
  justify-self: center;
  width: min(100%, 320px);
  margin: 0;
}

.page figure.photo img {
  display: block;
  width: 100%;
  height: auto;
  box-shadow: 0 18px 40px -24px rgb(20 19 17 / 0.45);
}

/* 6. How to take it: the painted sum, a caption under each number. */
.page figure.sum {
  position: relative;
  width: min(100%, 560px);
  margin: clamp(20px, 2.4vw, 32px) 0 0;
  padding-bottom: 52px;
}

.page img.sumArt {
  display: block;
  width: 100%;
  height: auto;
}

.page p.sumType {
  margin: 0;
  font-family: var(--display-font);
  font-size: clamp(48px, 5vw, 80px);
  font-weight: 300;
  letter-spacing: -0.03em;
}

.page .sumLabel {
  position: absolute;
  bottom: 0;
  translate: -50% 0;
  width: max-content;
  max-width: 34%;
  color: var(--muted);
  font-size: 15px;
  line-height: 1.35;
  text-align: center;
}

/* 7. Buy: the bottle stands on its stroke. */
.page figure.buyStand {
  position: relative;
  justify-self: center;
  width: min(100%, var(--picture-width));
  aspect-ratio: 4 / 3;
  margin: 0;
}

.page img.stroke {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 14%;
  width: 100%;
  height: auto;
}

.page img.buyContact {
  position: absolute;
  left: 50%;
  bottom: 20%;
  width: 34%;
  height: auto;
  translate: -50% 0;
}

.page img.buyBottle {
  position: absolute;
  left: 50%;
  bottom: 21%;
  width: 46%;
  height: auto;
  translate: -50% 0;
}

.page h2.buyName {
  margin: 0;
  font-size: clamp(48px, 5vw, 80px);
  line-height: 1;
}

.page p.focus {
  margin: 8px 0 20px;
  color: var(--muted);
  font-size: clamp(19px, 1.6vw, 24px);
}

.page dl.rows {
  display: grid;
  margin: 0 0 24px;
}

.page .rows div {
  display: grid;
  grid-template-columns: 11ch minmax(0, 1fr);
  gap: 16px;
  padding: 14px 0;
  border-top: 1px solid var(--hair);
}

.page .rows div:last-child {
  border-bottom: 1px solid var(--hair);
}

.page .rows dt {
  color: var(--muted);
}

.page .rows dd {
  margin: 0;
}
```

Note: `img.buyContact`/`img.buyBottle` use `translate` on the images themselves (not on an ancestor of a blend group): fine for the multiply rule. The `multiply` section skips `[data-stand]` figures.

- [ ] **Step 8: Run the tests to see them pass**

Run: `python -X utf8 scripts/qa/qa_nuricell_ink.py http://localhost:3032 --only=shell,multiply,words,sticky,sum`
Expected: all PASS; the `words:` line lists only Questions, More from BiGH, caution and FDA strings. Look at the people, daily and buy screenshots against mockups `5-people.jpg`, `6-daily.jpg`, `7-buy.jpg`.

- [ ] **Step 9: Commit**

```bash
cd "C:/Users/mcbig/Documents/codes/bigh-nuricell-ink" && npx prettier --write src/components/product scripts/qa/qa_nuricell_ink.py && git add -A src/components/product scripts/qa/qa_nuricell_ink.py && git commit -m "feat(nuricell): Dr. Liu painted, how to take it as a painted sum, and buy" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 7: Questions, more from BiGH, and the notes

**Files:**

- Create: `src/components/product/ink/after.tsx`
- Modify: `product-ink.tsx`, `product-ink.module.css`, `scripts/qa/qa_nuricell_ink.py`

**Interfaces:**

- Consumes: `getSummary`, `productSlugs` from `../catalog`; `shadow` from the homepage assets.
- Produces: `After({ product }: { product: InkProduct })`.

- [ ] **Step 1: Write the failing test** — at the end of `words`, after the per-chapter checks, add:

```python
    check("words: every string of nuricell.ts on the page", not missing, f"{len(missing)} missing: {missing[:5]}")
    for slug in OTHERS:
        check(f"words: More from BiGH links {slug}", page.locator(f'#more a[href$="/products/{slug}"]').count() == 1)
```

(move `ctx.close()` after these lines).

- [ ] **Step 2: Run it to see it fail**

Run: `python -X utf8 scripts/qa/qa_nuricell_ink.py http://localhost:3032 --only=words`
Expected: FAIL on "every string" (the FAQ, caution and FDA lines) and on the four links.

- [ ] **Step 3: Write `after.tsx`**:

```tsx
"use client";

import Image from "next/image";
import { shadow } from "@/components/home-v2/look-ink/assets";
import base from "@/components/ink/ink.module.css";
import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import { getSummary, productSlugs } from "../catalog";
import type { InkProduct, ProductSummary } from "../product-types";
import styles from "./product-ink.module.css";

// After Buy, full width on paper: the questions on hairlines with round toggles, the other bottles
// small in pale pools (each links to its page), then the caution and FDA notes, before the shared
// footer.
export function After({ product }: { product: InkProduct }) {
  const copy = useCopy();
  const related = product.related
    .map((slug) => getSummary(slug))
    .filter((summary): summary is ProductSummary => Boolean(summary));
  return (
    <>
      {product.faq.length > 0 ? (
        <section id="questions" className={styles.after} aria-labelledby="questions-title">
          <div className={`${base.wrap} ${styles.afterWrap}`}>
            <h2 id="questions-title" className={`${base.display} ${styles.heading}`}>
              {copy("Questions")}
            </h2>
            <ul className={styles.faq}>
              {product.faq.map((item) => (
                <li key={item.question}>
                  <details className={styles.question}>
                    <summary className={`${styles.summary} ${styles.faqSummary}`}>
                      <span className={styles.studyTitle}>{copy(item.question)}</span>
                      <span className={styles.toggle} aria-hidden="true">
                        +
                      </span>
                    </summary>
                    <p className={styles.answer}>{copy(item.answer)}</p>
                  </details>
                </li>
              ))}
            </ul>
          </div>
        </section>
      ) : null}
      {related.length > 0 ? (
        <section id="more" className={styles.after} aria-labelledby="more-title">
          <div className={base.wrap}>
            <h2 id="more-title" className={`${base.display} ${styles.heading}`}>
              {copy("More from BiGH")}
            </h2>
            <ul className={styles.more}>
              {related.map((summary) => (
                <li key={summary.slug}>
                  <Link
                    href={
                      productSlugs.includes(summary.slug)
                        ? `/products/${summary.slug}`
                        : "/#products"
                    }
                    className={styles.moreLink}
                  >
                    <span className={styles.moreStand} aria-hidden="true">
                      <Image
                        className={`${base.ink} ${styles.morePool}`}
                        src={shadow.src}
                        alt=""
                        width={shadow.width}
                        height={shadow.height}
                        sizes="180px"
                      />
                      <Image
                        className={styles.moreBottle}
                        src={summary.bottle.src}
                        alt=""
                        width={summary.bottle.width}
                        height={summary.bottle.height}
                        sizes="160px"
                      />
                    </span>
                    <span className={styles.moreName}>{summary.name}</span>
                    <span className={styles.meta}>{copy(summary.focus)}</span>
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </section>
      ) : null}
      <div className={`${base.wrap} ${styles.notes}`}>
        <p>{copy(product.caution)}</p>
        <p>{copy(product.notes.fda)}</p>
      </div>
    </>
  );
}
```

- [ ] **Step 4: Wire it in and style it** — render `<After product={product} />` last in `product-ink.tsx`. Append:

```css
/* After Buy: questions, more from BiGH, notes. */
.page .after {
  padding-block: var(--chapter-half);
}

.page .afterWrap {
  max-width: calc(820px + 2 * var(--gutter));
}

.page ul.faq {
  display: grid;
  margin: 0;
  padding: 0;
  list-style: none;
}

.page .faq li {
  border-top: 1px solid var(--hair);
}

.page .faq li:last-child {
  border-bottom: 1px solid var(--hair);
}

.page summary.faqSummary {
  grid-template-columns: minmax(0, 1fr) 44px;
}

.page p.answer {
  margin: 0 0 20px;
  max-width: 34em;
  color: var(--muted);
  font-size: 17px;
  line-height: 1.55;
}

.page ul.more {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 32px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.page a.moreLink {
  display: grid;
  justify-items: center;
  gap: 6px;
  min-height: 48px;
  color: inherit;
  text-align: center;
  text-decoration: none;
}

.page .moreStand {
  position: relative;
  display: block;
  width: 140px;
  aspect-ratio: 1230 / 1278;
}

.page img.morePool {
  position: absolute;
  left: 52%;
  top: 79%;
  width: 92%;
  height: auto;
  aspect-ratio: 1 / 0.42;
  object-fit: fill;
  translate: -50% 0;
  opacity: 0.5;
}

.page img.moreBottle {
  position: relative;
  display: block;
  width: 100%;
  height: auto;
}

.page .moreName {
  font-size: 18px;
  font-weight: 500;
}

.page .notes {
  display: grid;
  gap: 8px;
  padding-block: 0 var(--chapter-half);
  color: var(--muted);
  font-size: 15px;
  line-height: 1.5;
}

.page .notes p {
  margin: 0;
  max-width: 60em;
}
```

- [ ] **Step 5: Run the tests to see them pass**

Run: `python -X utf8 scripts/qa/qa_nuricell_ink.py http://localhost:3032 --only=shell,others,multiply,lantern,nojs,words,sticky,sum`
Expected: all PASS, and the `words:` line reports 0 strings not on the page.

- [ ] **Step 6: Commit**

```bash
cd "C:/Users/mcbig/Documents/codes/bigh-nuricell-ink" && npx prettier --write src/components/product scripts/qa/qa_nuricell_ink.py && git add -A src/components/product scripts/qa/qa_nuricell_ink.py && git commit -m "feat(nuricell): questions, more from BiGH, and the notes; every word on the page" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 8: The new strings in five languages

**Files:**

- Create: `reference/ink-pages/nuricell/translations-nuricell.cjs`
- Modify (generated): `src/i18n/copy-keys.json`, `messages/{en,cns,kr,vn,jp}.json`
- Modify: `scripts/qa/qa_nuricell_ink.py`

**Interfaces:**

- Consumes: the English strings used in Tasks 3-7.
- Produces: catalog keys for every new English string (next free `mNNN`).

- [ ] **Step 1: Write the failing test** — add `languages` and register it:

```python
NEW = ["Portrait painting", "capsules a day", "capsules in each bottle"]


def languages(browser):
    for locale in ["kr", "jp", "cns", "vn"]:
        ctx, page, response, errors = opened(browser, 1440, 900, f"/{locale}/products/nuricell", reduced=True)
        check(f"languages {locale}: 200", response is not None and response.status == 200)
        check(f"languages {locale}: no console errors", not errors, "; ".join(errors[:2]))
        text = page.locator("main").text_content()
        left = [s for s in NEW if s in text]
        check(f"languages {locale}: new strings translated", not left, ", ".join(left))
        alt = page.locator("[data-lantern] img").first.get_attribute("alt")
        check(f"languages {locale}: painting descriptions translated", alt and "lantern" not in alt, alt)
        ctx.close()
```

- [ ] **Step 2: Run it to see it fail**

Run: `python -X utf8 scripts/qa/qa_nuricell_ink.py http://localhost:3032 --only=languages`
Expected: FAIL in every locale (English shown).

- [ ] **Step 3: Write the translations** — `reference/ink-pages/nuricell/translations-nuricell.cjs` (DRAFT, not native-reviewed; same understated voice, no new claims; Dr. Liu's name as in m198 per language):

```js
// Adds NuriCell's ink page strings (October 9, 2026) to the five catalogs. DRAFT translation, not
// native-reviewed: the site's understated voice, no new claims; Dr. Liu named as in m198. hken.json
// stays {} (/hken redirects to /cns). Run from the repo root:
//   node reference/ink-pages/nuricell/translations-nuricell.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  ["Portrait painting", "肖像画", "초상화", "Tranh chân dung", "肖像画"],
  ["The research", "研究", "연구", "Nghiên cứu", "研究"],
  [
    "Show all {count} studies",
    "显示全部 {count} 项研究",
    "연구 {count}건 모두 보기",
    "Xem tất cả {count} nghiên cứu",
    "{count} 件の研究をすべて表示",
  ],
  ["Show fewer studies", "收起研究", "연구 접기", "Thu gọn nghiên cứu", "研究を折りたたむ"],
  ["capsules a day", "每日胶囊数", "하루 캡슐 수", "viên mỗi ngày", "1日のカプセル数"],
  ["days", "天", "일", "ngày", "日"],
  ["capsules in each bottle", "每瓶胶囊数", "한 병의 캡슐 수", "viên mỗi lọ", "1本のカプセル数"],
  [
    "{perDay} capsules a day for {days} days: {total} capsules in each bottle.",
    "每日 {perDay} 粒，共 {days} 天：每瓶 {total} 粒。",
    "하루 {perDay}캡슐씩 {days}일: 한 병에 {total}캡슐.",
    "Mỗi ngày {perDay} viên trong {days} ngày: mỗi lọ {total} viên.",
    "1日 {perDay} カプセルを {days} 日間：1本に {total} カプセル。",
  ],
  [
    "A paper lantern whose light comes on, painted in ink and gold leaf",
    "一盏纸灯笼亮起，以水墨与金箔绘成。",
    "불이 켜지는 종이 등롱을 먹과 금박으로 그린 그림.",
    "Chiếc đèn lồng giấy sáng lên, vẽ bằng mực và lá vàng.",
    "明かりがともる紙の提灯を墨と金箔で描いた絵。",
  ],
  [
    "An opened capsule with its four powders in a row and gold sparks rising, painted in ink",
    "打开的胶囊，四堆粉末排成一行，金色火花升起，以水墨绘成。",
    "열린 캡슐과 나란히 놓인 네 가지 가루, 피어오르는 금빛 불꽃을 먹으로 그린 그림.",
    "Viên nang mở ra, bốn đống bột xếp thành hàng và những tia vàng bay lên, vẽ bằng mực.",
    "開いたカプセルと一列に並ぶ4つの粉、立ちのぼる金色の火花を墨で描いた絵。",
  ],
  [
    "Seven books as stepping stones across a calm stream, painted in ink",
    "七本书如踏脚石横跨平静的溪流，以水墨绘成。",
    "잔잔한 시냇물을 건너는 징검돌이 된 일곱 권의 책을 먹으로 그린 그림.",
    "Bảy cuốn sách làm đá kê chân bắc qua dòng suối êm, vẽ bằng mực.",
    "静かな小川に渡した飛び石のような7冊の本を墨で描いた絵。",
  ],
  [
    "A portrait painting of Dr. Jiankang Liu in ink and colour",
    "刘健康博士的水墨设色肖像画。",
    "Dr. Jiankang Liu의 먹과 채색 초상화.",
    "Tranh chân dung Dr. Jiankang Liu vẽ bằng mực và màu.",
    "Dr. Jiankang Liu の墨と彩色による肖像画。",
  ],
  [
    "A soft-boiled egg with a gold yolk beside a dish of three capsules, painted in ink",
    "金色蛋黄的半熟蛋，旁边一小碟三粒胶囊，以水墨绘成。",
    "금빛 노른자의 반숙 달걀과 캡슐 세 개가 담긴 접시를 먹으로 그린 그림.",
    "Quả trứng lòng đào với lòng đỏ vàng óng bên đĩa ba viên nang, vẽ bằng mực.",
    "金色の黄身の半熟卵と、3つのカプセルをのせた小皿を墨で描いた絵。",
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

- [ ] **Step 4: Run it, then the test**

```bash
cd "C:/Users/mcbig/Documents/codes/bigh-nuricell-ink" && node reference/ink-pages/nuricell/translations-nuricell.cjs && python -X utf8 scripts/qa/qa_nuricell_ink.py http://localhost:3032 --only=languages
```

Expected: the script lists 13 keys (`m…`); the `languages` section all PASS. Note the new key range for Mo's native check.

- [ ] **Step 5: Commit**

```bash
cd "C:/Users/mcbig/Documents/codes/bigh-nuricell-ink" && npx prettier --write src/i18n/copy-keys.json messages scripts/qa/qa_nuricell_ink.py && git add reference/ink-pages/nuricell/translations-nuricell.cjs src/i18n/copy-keys.json messages scripts/qa/qa_nuricell_ink.py && git commit -m "feat(nuricell): the ink page's new strings in five languages (drafts)" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 9: Every size, the built site, the gates, and a fresh review

**Files:**

- Modify: `scripts/qa/qa_nuricell_ink.py` (add `layout`, `deep_links`), `scripts/qa/README.md`, `product-ink.module.css` (fixes the checks find)

**Interfaces:**

- Consumes: the whole page.
- Produces: a green QA run on dev and on `next start`; screenshots for Mo.

- [ ] **Step 1: Write the failing tests** — add and register `layout` and `deep_links`:

```python
SIZES = [(1536, 864), (1440, 900), (1280, 800), (1024, 768), (960, 800), (900, 900), (768, 1024), (390, 844), (360, 780)]


def layout(browser):
    for w, h in SIZES:
        ctx, page, _, _ = opened(browser, w, h, reduced=True)
        tag = f"layout {w}x{h}"
        wide = page.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
        check(f"{tag}: no sideways scroll", wide <= 0, f"{wide}px")
        bad = page.evaluate(
            """(two) => [...document.querySelectorAll('[data-chapter]:not([data-chapter="overview"])')].map(c => {
                 const f = c.querySelector('figure[data-picture]').getBoundingClientRect();
                 const t = c.querySelector('[data-words]').getBoundingClientRect();
                 const ok = two ? f.right <= t.left + 1 : f.bottom <= t.top + 1;
                 return ok ? null : c.dataset.chapter; }).filter(Boolean)""",
            w >= 960,
        )
        check(f"{tag}: each painting {'left of' if w >= 960 else 'above'} its words", not bad, ", ".join(bad))
        small = page.evaluate(
            """() => [...document.querySelectorAll('main p, main li, main dd, main dt, main td, main th, main figcaption')]
                 .filter(e => e.offsetParent && e.textContent.trim() && parseFloat(getComputedStyle(e).fontSize) < 15)
                 .map(e => e.textContent.trim().slice(0, 30))"""
        )
        check(f"{tag}: text 15px or larger", not small, "; ".join(small[:3]))
        tiny = page.evaluate(
            """() => [...document.querySelectorAll('main button, main summary, main a')]
                 .filter(e => e.offsetParent).map(e => e.getBoundingClientRect())
                 .filter(r => r.height < 44).length"""
        )
        check(f"{tag}: targets 44px or taller", tiny == 0, f"{tiny} small")
        y, n, total = 0, 0, page.evaluate("() => document.documentElement.scrollHeight")
        while y < total and n < 30:
            page.evaluate(f"window.scrollTo(0, {y})")
            page.wait_for_timeout(150)
            page.screenshot(path=str(OUT / f"layout-{w}-{n:02d}.png"))
            y, n = y + h, n + 1
        ctx.close()
    ctx = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    page = ctx.new_page()
    page.route(re.compile(r"\.(webp|png|jpg|jpeg|avif)(\?|$)|/_next/image"), lambda route: route.abort())
    page.goto(BASE + PATH, wait_until="networkidle")
    hidden = page.evaluate(
        """() => [...document.querySelectorAll('main h1, main h2, main p')]
             .filter(e => e.textContent.trim() && (e.offsetParent === null || getComputedStyle(e).visibility === 'hidden' || Number(getComputedStyle(e).opacity) < 0.9))
             .map(e => e.textContent.trim().slice(0, 30))"""
    )
    check("layout: words readable with pictures blocked", not hidden, "; ".join(hidden[:3]))
    ctx.close()


def deep_links(browser):
    for w, h in [(1440, 900), (1024, 768), (390, 844)]:
        for chapter in CHAPTERS[1:]:
            ctx, page, _, _ = opened(browser, w, h, f"{PATH}#chapter-{chapter}", reduced=True)
            page.wait_for_timeout(400)
            top = page.evaluate(f"() => document.getElementById('chapter-{chapter}-title').getBoundingClientRect().top")
            bar = page.evaluate("() => document.querySelector('header').getBoundingClientRect().bottom")
            check(f"deep link {w} #{chapter}: heading under the bar, in the window", bar <= top <= h - 80, f"top {top:.0f}, bar {bar:.0f}")
            ctx.close()
```

Note for phones: the heading sits under the chapter's painting, so on 390x844 the check allows the heading anywhere in the window (`h - 80`); if a tall painting pushes it out, the chapter's `scroll-margin-top` is wrong for one column: fix the CSS, not the check.

- [ ] **Step 2: Run them to see them fail (or pass)**

Run: `python -X utf8 scripts/qa/qa_nuricell_ink.py http://localhost:3032 --only=layout,deep_links`
Expected: some FAILs are likely (the first real run at nine sizes). Each FAIL names the size and the chapter or element.

- [ ] **Step 3: Fix what the run finds, in `product-ink.module.css`** — one fix per failure, scoped under `.page`, re-running only the failing section after each. Then look at every `layout-<w>-NN.png` full size, scrolled like a visitor, against the mockups, and score each size honestly (9/10 is the bar). Fix what looks wrong even when no check fails (a check that passes on something odd is not proof it looks right).

- [ ] **Step 4: The full run on dev**

Run: `python -X utf8 scripts/qa/qa_nuricell_ink.py http://localhost:3032`
Expected: `N/N passed`.

- [ ] **Step 5: The full run on the built site**

```bash
cd "C:/Users/mcbig/Documents/codes/bigh-nuricell-ink" && npm run build
```

Then `preview_start {name: "bigh-nuricell-ink-prod"}` (or `npm --prefix C:/Users/mcbig/Documents/codes/bigh-nuricell-ink run start -- --hostname localhost --port 3033` in the background), and:

Run: `python -X utf8 scripts/qa/qa_nuricell_ink.py http://localhost:3033`
Expected: `N/N passed`. Compare the built site's page height with dev's at 1440x900 (`document.documentElement.scrollHeight`): within 2%.

- [ ] **Step 6: The gates** — the homepage, About and the other products unchanged:

```bash
cd "C:/Users/mcbig/Documents/codes/bigh-nuricell-ink" && python -X utf8 scripts/qa/qa_home_ink.py http://localhost:3033 && python -X utf8 scripts/qa/qa_about.py http://localhost:3033 && python -X utf8 scripts/qa/qa_nav.py http://localhost:3033 && python -X utf8 scripts/qa/qa_green_bee_propolis.py http://localhost:3033 && python -X utf8 scripts/qa/qa_advanced_opc.py http://localhost:3033 && python -X utf8 scripts/qa/qa_turmerific.py http://localhost:3033 && python -X utf8 scripts/qa/qa_nature_calm.py http://localhost:3033
```

Expected: each ends all passed. A failure that also fails on `origin/main` (check the same script against the live demo `https://bigh-website-demo.vercel.app`) is pre-existing: record it, don't fix it here.

- [ ] **Step 7: Document the script** — in `scripts/qa/README.md` add, with the other page scripts:

```markdown
- `qa_nuricell_ink.py [base] [--only=...]` — NuriCell's ink page (October 9, 2026): the ink look and
  menu bar, the other four products on today's template, every painting multiplying with no box,
  the lantern's light coming on (no lighter flash; lit with reduced motion and without script),
  every word of nuricell.ts, sticky paintings inside their chapters, the painted sum and its
  captions, nine sizes, deep links, and the new strings in kr/jp/cns/vn. Pictures in
  `out/nuricell-ink/`.
```

- [ ] **Step 8: Commit**

```bash
cd "C:/Users/mcbig/Documents/codes/bigh-nuricell-ink" && npx prettier --write src/components/product scripts/qa && npm run format:check && git add -A src/components/product scripts/qa && git commit -m "test(nuricell): every size, deep links and the built site for the ink page" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

- [ ] **Step 9: A fresh review** — dispatch the `impeccable-finish-reviewer` agent with: the spec, the mockups folder, `DESIGN.md`, the built site at `http://localhost:3033/en/products/nuricell`, and the screenshots in `scripts/qa/out/nuricell-ink/`. Fix each material finding (re-run the QA after), and commit the fixes the same way.

- [ ] **Step 10: Show Mo** — publish an Artifact (the session's review page, a new version) with the built page's screenshots at 1440x900 and 390x844, one per chapter, the lantern lit, and a short list: what was built, the QA count, the draft translation keys for a native check, the spend. Ask her: (1) changes, or (2) push the branch for a Vercel preview. Do not push without her yes.

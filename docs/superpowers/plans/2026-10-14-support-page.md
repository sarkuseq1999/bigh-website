# Support Page ("Pull up a chair") Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A real `/support` page in the Ink & Gold look (Mo's mockup A, the California porch) that replaces the Support pop-up everywhere, with a complete preview form that sends nothing yet.

**Architecture:** A new route `src/app/[locale]/support/page.tsx` renders `SupportInk` (in `src/components/support/`) inside the shared `InkPage` shell, which brings the site menu bar, the footer, Lenis scrolling and the ink bloom. The page has its own small `Spread`/`Painting` pair (modelled on About's, kept local so the live About page is not touched), a client-side form with plain validation and a made-up ticket number, and CSS-only motion for the gold steam. Paintings are built from GPT Image 2.5 originals by a Python script into `public/images/support/` plus a generated `support-art.ts`. Every "Support" control on the site becomes a link to `/support`; the pop-up is removed.

**Tech Stack:** Next.js 16 (App Router, `src/proxy.ts`, `next/image` with the `preload` prop), React 19, next-intl (`useCopy`), CSS modules, Python 3.13 + Pillow + OpenCV + NumPy for the paintings, Playwright for Python for every check (`scripts/qa/`).

**Spec:** `docs/superpowers/specs/2026-10-14-support-page-design.md` (read it first; this plan argues from it). Mockups: `reference/ink-pages/mockups/support/a-desk.jpg`, `a-phone.jpg`, `a-sent-desk.jpg`.

## Global Constraints

- Work only in the worktree `C:\Users\mcbig\Documents\codes\bigh-support`, branch `support-page`. Never push, never touch `main`, never move the demo alias: each needs Mo's yes.
- `AGENTS.md`: this is a newer Next.js than your training data; read `node_modules/next/dist/docs/` before using an API you are unsure of. Use the Context7 MCP tools for library questions.
- Files are LF. The checkout has `core.autocrlf=true`: never `git stash`, never `git checkout -- <file>`; Python writes use `newline="\n"`. `npx prettier --write <files>` restores LF.
- Never `cd` in Bash commands; use absolute paths, `git -C`, `npm --prefix`.
- `DESIGN.md` applies: rice paper, sumi ink, gold leaf only inside paintings and only for energy (here: the cup's steam), no red, no seals or stamps, no boxes or cards, sentence case (never letter-spaced capitals), pills are the only constructed shape, hairlines 1px, every target 48px or more, text 15px or more, reduced motion complete and still.
- Paintings multiply (`mix-blend-mode: multiply`, the kit's `.ink` class). Nothing between a painting and the page root may create a stacking context (no `z-index` on a positioned ancestor, no `isolation`, `opacity < 1`, `transform`, `filter` or `mask` on a part, spread, figure or wrapper).
- Titles in Ysabeau (the homepage's title face, `--font-ysabeau`), reading text and controls in Switzer. The phone number and the ticket number are set in Switzer (`font-family: var(--sans)`), never Ysabeau, whose old-style digits rise and fall.
- English only: the page's new words get **no** copy keys. `useCopy` returns the English source for a string without a key in every locale (`src/i18n/use-copy.ts`), so `/kr/support` shows the page's words in English and the menu and footer in Korean. (This replaces the spec's "keys from m612 in the English catalog"; the behaviour is the same and nothing has to be undone when translations come.)
- `/hken/support` redirects to `/cns/support`, as every page does.
- The form sends nothing. `SENDING_LIVE = false` in `support-content.ts`; while it is false the honesty tag "Preview: messages aren’t sent yet" stands beside Send and the thank-you carries the preview line.
- Image spend: one GPT Image 2.5 job (the book) under Mo's $1 cap; the ledger `%LOCALAPPDATA%\HiggsfieldAPI\bigh-support-mock` holds 8 of 14 jobs. Never submit a job twice after a timeout.
- Dev server: `bigh-support` on port 3050; built site: `bigh-support-prod` on port 3051 (entries added to the main checkout's `.claude/launch.json` in Task 2).

## Review Focus

1. **Double Send / Enter in a field.** Pressing Enter in a text field or clicking Send twice must give one thank-you with one ticket number, never two panels or a changing number. (Task 4: QA `form` group presses Enter in "Your name" with everything filled and clicks Send twice quickly.)
2. **A real customer on the public demo.** Someone sends a real complaint through the preview. Expected: they can see it was not sent and how to reach the team now. (Task 4: QA asserts the honesty tag beside Send and the preview line with the phone number and email in the thank-you.)
3. **A photo that is not a picture, or is huge.** A PDF or a 12 MB photo from a phone. Expected: a plain message, the file not kept, the form still usable. (Task 4: QA sets a 5 MB file and a `.pdf`.)
4. **Long words in other languages and tiny phones.** At 360px wide, and with the Korean menu around English words, nothing scrolls sideways and the chips never leave one alone on a row. (Task 3 and Task 4: `rhythm` at 360x780 and `languages` at 390x844.)
5. **Arriving from the menu on a page that is scrolled.** Clicking Support in the menu while deep in another page must land at the top of `/support` with the bar marking Support, not mid-page. (Task 5: QA `links` scrolls `/about` to its foot, clicks Support, checks `scrollY === 0` and `aria-current`.)

---

### Task 1: The paintings

**Files:**
- Create: `reference/ink-pages/support/prompts/a-book-v2.txt`
- Create: `reference/ink-pages/support/originals/gpt25-a-book-v2.png` (+ `.json` sidecar; written by the job helper)
- Create: `reference/ink-pages/support/build_support.py`
- Create: `reference/ink-pages/support/check_support.py`
- Create (generated): `public/images/support/porch-v1.webp`, `porch-steam-v1.webp`, `cup-v1.webp`, `mailbox-v1.webp`, `parcel-v1.webp`, `book-v1.webp`
- Create (generated): `src/components/support/support-art.ts`
- Create: `reference/ink-pages/spend-support.md`

**Interfaces:**
- Produces `src/components/support/support-art.ts` exporting:
  - `type Art = { src: string; width: number; height: number }`
  - `type Steam = Art & { left: number; top: number; size: number }` (fractions of its painting's width/height/width)
  - `porch: Art & { steam: Steam }`, `cup: Art & { steam: Steam }`, `mailbox: Art`, `parcel: Art`, `book: Art`

- [ ] **Step 1: Write the book prompt**

The mockup's book was the plainest picture (spec, "Paintings"). Write `reference/ink-pages/support/prompts/a-book-v2.txt` (LF), the shared style paragraph from `prompts/a-book.txt` (first paragraph, unchanged) followed by:

```text
A worn hardback book lies open on the flat top of a weathered wooden porch rail, its pages lifting and fanning in a breeze, a few loose pages caught mid-turn. One dry California oak leaf rests against its spine, and a strand of dry golden grass leans in from the edge of the rail, painted in grey ink only. Beyond the rail, very faint in mist, a single low hill in the palest grey wash. The rail runs out of the picture to one side in two quick dry-brush strokes. No gold anywhere. The book sits a little left of the middle of the sheet.
```

- [ ] **Step 2: Paint it (one paid job, about 5¢)**

Run (the helper is the mockup round's, with its own ledger and a 14-job cap):

```bash
HF_RUN_STATE="C:/Users/mcbig/AppData/Local/HiggsfieldAPI/bigh-support-mock" python -X utf8 "C:/Users/mcbig/AppData/Local/Temp/claude/C--Users-mcbig-Documents-codes-bigh-website/52d9c8ad-69f2-4461-bc8d-fdfe7746fe59/scratchpad/support/hf_support.py" a-book-v2 C:/Users/mcbig/Documents/codes/bigh-support/reference/ink-pages/support/prompts/a-book-v2.txt --aspect 3:4 --ref C:/Users/mcbig/Documents/codes/bigh-support/reference/home-v2/ink/originals/gpt25-crane-paint-a.png --out C:/Users/mcbig/Documents/codes/bigh-support/reference/ink-pages/support/originals
```

Expected: `status completed`, `saved ...gpt25-a-book-v2.png`, `jobs this round: 9 of 14`. If the scratchpad helper is gone, copy `reference/home-v2/r4/hf_unquoted.py` to the scratchpad, set `LEDGER = STATE / "ledger-support-mock-gpt.jsonl"` and `MAX_JOBS = 14`, and run that. Aspect `4:5` is refused by the service (HTTP 400): use `3:4`. On a timeout, do not resubmit: check https://open.higgsfield.ai/usage.

Look at the picture (shrink it to 600px with Pillow and open it with Read). It must be loose sumi-e brushwork like the crane, not a detailed drawing; the book must read at a glance. If it fails that look, report to the lead instead of painting again (a second job needs the lead's go).

- [ ] **Step 3: Write the failing check**

Create `reference/ink-pages/support/check_support.py`:

```python
"""Check the Support page's built paintings (run after build_support.py).

usage: python -X utf8 reference/ink-pages/support/check_support.py
"""

import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "reference/ink-pages/about"))
import build_about as bd  # noqa: E402

OUT = REPO / "public/images/support"
TS = REPO / "src/components/support/support-art.ts"
fails = []


def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'} {name}{(' - ' + str(detail)) if detail and not ok else ''}")
    if not ok:
        fails.append(name)


names = ["porch", "porch-steam", "cup", "mailbox", "parcel", "book"]
for n in names:
    check(f"{n}-v1.webp exists", (OUT / f"{n}-v1.webp").exists())
if not fails:
    for n in ["porch", "cup", "mailbox", "parcel", "book"]:
        arr = np.asarray(Image.open(OUT / f"{n}-v1.webp").convert("RGB"))
        edge = np.concatenate([arr[0], arr[-1], arr[:, 0], arr[:, -1]])
        check(f"{n}: its edge is white paper (multiplies with no box)", edge.min() >= 238, int(edge.min()))
        gold = int(bd.gold_pixels(arr).sum())
        check(f"{n}: no gold left in the ink plate", gold < 40, gold)
    for n in ["porch-steam"]:
        img = Image.open(OUT / f"{n}-v1.webp")
        check(f"{n}: has transparency", img.mode == "RGBA")
        rgba = np.asarray(img.convert("RGBA"))
        shown = rgba[..., 3] > 128
        check(f"{n}: holds gold leaf", shown.sum() > 400 and bd.gold_pixels(rgba[..., :3])[shown].mean() > 0.3,
              int(shown.sum()))
    ts = TS.read_text(encoding="utf-8")
    for n in ["porch", "cup", "mailbox", "parcel", "book"]:
        check(f"support-art.ts exports {n}", re.search(rf"export const {n} = ", ts) is not None)
    # Prettier unquotes the keys (quoteProps "as-needed"), so look for `steam: {`.
    check("support-art.ts places the steam on the porch and the cup", len(re.findall(r"\bsteam: \{", ts)) == 2)
print(f"\n{'ALL PASS' if not fails else f'{len(fails)} FAILED'}")
sys.exit(1 if fails else 0)
```

- [ ] **Step 4: Run it to see it fail**

Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-support/reference/ink-pages/support/check_support.py`
Expected: FAIL on every `exists` line, exit 1.

- [ ] **Step 5: Write the build script**

Create `reference/ink-pages/support/build_support.py`. It reuses About's treatments (`reference/ink-pages/about/build_about.py`: `divided` paper to white, `levelled` KNEE 220 / WHITE 245, `ink_box`, `feathered`, `gold_pixels`, `art_of`; `ba` = `reference/home-v2/ink/build_assets.py` for `leaf` and `save`):

```python
"""Build the Support page's paintings (Mo, October 14, 2026; mockup A, "Pull up a chair").

Originals: reference/ink-pages/support/originals/gpt25-<take>.png (GPT Image 2.5 on rice paper,
the homepage crane as the brushwork reference; prompts in prompts/, spend in
reference/ink-pages/spend-support.md). Output: public/images/support/*.webp and
src/components/support/support-art.ts. The treatments are About's (build_about.py): the paper
divided out and lifted to pure white, so a painting multiplies onto the page's paper with no box.
The porch's gold steam is lifted out into its own picture (the page lets it rise), and the cup with
its steam is cut from the same painting for the thank-you.

usage: python -X utf8 reference/ink-pages/support/build_support.py
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
OUT = REPO / "public/images/support"
URL = "/images/support"
TS = REPO / "src/components/support/support-art.ts"
# Bump when a shipped picture changes after it has been pushed (the image optimizer caches by URL).
V = "v1"
TAKES = {"porch": "a-porch-v2", "mailbox": "a-mailbox", "parcel": "a-parcel", "book": "a-book-v2"}
# The cup, its saucer and the steam over it, on the porch original (2048x1360), measured by eye on
# the mockup round (the cut in the mockup's thank-you).
CUP_BOX = (850, 470, 1110, 840)

bd.ORIG = HERE / "originals"
bd.URL = URL
bd.V = V
bd.TAKES = TAKES
ba.OUT = OUT
ba.PLATES = HERE / "plates"


def split_steam(img):
    """Lift every gold flake of the steam out of the painting. Returns (painting with paper where
    the steam was, the steam as a transparent gold-leaf picture, its box on the original). The
    steam is many small flakes, so all of them are kept (About's split_dot keeps one blob)."""
    arr = np.asarray(img.convert("RGB"))
    mask = cv2.morphologyEx(bd.gold_pixels(arr).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(mask, 8)
    keep = np.zeros_like(mask, dtype=bool)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] >= 12:
            keep |= lab == i
    if keep.sum() < 200:
        raise SystemExit("no steam found")
    blob = cv2.dilate(keep.astype(np.uint8), np.ones((9, 9), np.uint8)).astype(bool)
    ring = cv2.dilate(blob.astype(np.uint8), np.ones((41, 41), np.uint8)).astype(bool) & ~blob
    ring &= arr.max(axis=2) > 200  # bare paper only, never the cup or the rail
    clean = arr.copy()
    clean[blob] = np.median(arr[ring], axis=0).astype(np.uint8)
    ys, xs = np.where(blob)
    m = 12
    box = (max(0, xs.min() - m), max(0, ys.min() - m), min(arr.shape[1], xs.max() + m), min(arr.shape[0], ys.max() + m))
    steam = np.asarray(ba.leaf(img.convert("RGB").crop(box))).copy()
    soft = cv2.GaussianBlur(blob.astype(np.float32), (0, 0), 2)[box[1] : box[3], box[0] : box[2]]
    steam[..., 3] = np.clip(steam[..., 3] * soft, 0, 255).astype(np.uint8)
    return Image.fromarray(clean), Image.fromarray(steam, "RGBA"), box


def placed(steam_box, crop_box, crop_w, crop_h, steam):
    """Where the steam stands on a picture cropped at crop_box (fractions, as the page reads them)."""
    return {
        "src": f"{URL}/porch-steam-{V}.webp",
        "width": steam.width,
        "height": steam.height,
        "left": round((steam_box[0] - crop_box[0]) / crop_w, 4),
        "top": round((steam_box[1] - crop_box[1]) / crop_h, 4),
        "size": round((steam_box[2] - steam_box[0]) / crop_w, 4),
    }


def porch_and_cup():
    img = bd.load(TAKES["porch"])
    clean, steam, sbox = split_steam(img)
    ba.save(steam, f"porch-steam-{V}", None, 90)
    flat = bd.divided(clean)
    # The porch: cropped to its ink (and its steam), the outer edge feathered to white.
    x0, y0, x1, y1 = bd.ink_box(np.asarray(flat), pad=0.04)
    x0, y0, x1, y1 = min(x0, sbox[0]), min(y0, sbox[1]), max(x1, sbox[2]), max(y1, sbox[3])
    crop = bd.feathered(bd.levelled(flat.crop((x0, y0, x1, y1))), 0.03)
    porch = bd.art_of(crop, f"porch-{V}", 1640)
    porch["steam"] = placed(sbox, (x0, y0), crop.width, crop.height, steam)
    # The cup: the hills and the rail behind it are pale washes; lifted to white with an oval fade,
    # so only the cup, its saucer and the table's edge remain.
    cb = (min(CUP_BOX[0], sbox[0]), min(CUP_BOX[1], sbox[1]), max(CUP_BOX[2], sbox[2]), max(CUP_BOX[3], sbox[3]))
    cup_arr = np.asarray(bd.levelled(flat.crop(cb))).astype(np.float32)
    cup_arr = np.where(cup_arr.mean(axis=2, keepdims=True) > 190, 255, cup_arr)
    h, w = cup_arr.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h * 0.62) / (h * 0.62)) ** 2)
    k = np.clip((1.0 - d) / 0.3, 0, 1)[..., None]
    cup_img = Image.fromarray((255 - (255 - cup_arr) * k).astype(np.uint8))
    cup = bd.art_of(cup_img, f"cup-{V}", 600)
    cup["steam"] = placed(sbox, cb, cup_img.width, cup_img.height, steam)
    return porch, cup


def write_ts(entries):
    head = [
        "// Generated by reference/ink-pages/support/build_support.py. Do not edit by hand: change the",
        "// script (or its TAKES) and run it again. The Support page's paintings (October 14, 2026): GPT",
        "// Image 2.5 on rice paper, the paper divided out so each multiplies onto the page's own paper;",
        "// the porch's gold steam as its own picture (`steam`), placed by fractions of its painting.",
        "",
        "export type Art = { src: string; width: number; height: number };",
        "/** The gold steam, placed by fractions of its painting's width (left, size) and height (top). */",
        "export type Steam = Art & { left: number; top: number; size: number };",
        "",
    ]
    body = [f"export const {name} = {json.dumps(value, indent=2)} as const;\n" for name, value in entries]
    TS.parent.mkdir(parents=True, exist_ok=True)
    TS.write_text("\n".join(head) + "\n".join(body), encoding="utf-8", newline="\n")
    prettier = REPO / "node_modules/prettier/bin/prettier.cjs"
    subprocess.run(["node", str(prettier), "--write", str(TS)], cwd=REPO, check=True, capture_output=True)
    print(TS.relative_to(REPO))


if __name__ == "__main__":
    porch, cup = porch_and_cup()
    write_ts(
        [
            ("porch", porch),
            ("cup", cup),
            ("mailbox", bd.painting("mailbox", "mailbox", 1100)),
            ("parcel", bd.painting("parcel", "parcel", 1100)),
            ("book", bd.painting("book", "book", 1100)),
        ]
    )
```

Check before running that `bd.load`, `bd.divided`, `bd.levelled`, `bd.ink_box`, `bd.feathered`, `bd.art_of`, `bd.painting`, `bd.gold_pixels`, `ba.leaf` and `ba.save` have the signatures used here (read `build_about.py` lines 51-175 and `reference/home-v2/ink/build_assets.py` lines 40-60 and 190-205). `bd.painting(key, name, width)` reads `TAKES[key]`; `bd.art_of(img, name, width)` saves `<name>.webp` through `ba.save` and returns `{src, width, height}`.

- [ ] **Step 6: Run the build, then the check**

Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-support/reference/ink-pages/support/build_support.py`
Expected: six `public/images/support/*.webp` lines and `src/components/support/support-art.ts`.
Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-support/reference/ink-pages/support/check_support.py`
Expected: `ALL PASS`, exit 0. If "no gold left in the ink plate" fails for the porch, the steam's dilation (9x9) is too tight: widen it to 11x11 and rebuild.

- [ ] **Step 7: Look at every plate**

Multiply each plate onto `public/images/home-v2/ink/paper.webp` (Pillow `ImageChops.multiply` on a tile of the paper the plate's size), save as JPEG in the scratchpad, open each with Read. Check by eye: no rectangle edge around any painting; the porch has no gold and no grey smudge where the steam was; the steam picture is only gold flakes on transparency; the cup cut has no hills, no rail, no chair edges, and its steam (placed by `cup.steam`) sits right over the cup. Fix the script and rebuild until all hold.

- [ ] **Step 8: Record the spend**

Create `reference/ink-pages/spend-support.md`:

```markdown
# Support page: image spend

Mo's cap: $1 (October 14, 2026, "2 yes"). GPT Image 2.5 through the Higgsfield API, about $0.05 a
picture (billed $0.07, $0.02 refunded on reconcile). Ledger:
`%LOCALAPPDATA%\HiggsfieldAPI\bigh-support-mock\ledger-support-mock-gpt.jsonl` (cap 14).

| # | Take | Use |
|---|------|-----|
| 1 | a-porch | first porch, too detailed (not used) |
| 2 | a-porch-v2 | the porch (shipped: porch, steam, cup) |
| 3 | c-circles | mockup C (not used) |
| 4 | a-mailbox | Write to us (shipped) |
| 5 | a-parcel | Returns (shipped) |
| 6 | a-book | mockup's book (replaced) |
| 7 | b-door-open | mockup B (not used) |
| 8 | b-door-closed | mockup B (not used) |
| 9 | a-book-v2 | Questions (shipped) |

Four first tries at 4:5 were refused at submit (HTTP 400) and never charged.
```

- [ ] **Step 9: Commit**

```bash
git -C C:/Users/mcbig/Documents/codes/bigh-support add reference/ink-pages/support reference/ink-pages/spend-support.md public/images/support src/components/support/support-art.ts
git -C C:/Users/mcbig/Documents/codes/bigh-support commit -m "feat(support): the porch, mailbox, parcel and book paintings, the steam lifted out" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

(`reference/ink-pages/support/plates/` holds lossless working copies; commit it as About does with its `plates/`.)

---

### Task 2: The route, the page shell and the opening

**Files:**
- Modify (outside the repo, gitignored): `C:\Users\mcbig\Documents\codes\bigh-website\.claude\launch.json`
- Modify: `src/components/ink/nav/nav-inscription.tsx:73` (the `NavCurrent` union)
- Create: `src/app/[locale]/support/page.tsx`
- Create: `src/components/support/support-content.ts`
- Create: `src/components/support/spread.tsx`
- Create: `src/components/support/support-ink.tsx`
- Create: `src/components/support/support-page.module.css`
- Create: `scripts/qa/qa_support.py`

**Interfaces:**
- Consumes: `porch` from `support-art.ts` (Task 1).
- Produces:
  - `support` (words) and `SENDING_LIVE: boolean` from `support-content.ts`
  - `Painting({ art, alt, sizes, eager?, preload?, steam?, className? })` and `Spread({ id, part, side, labelledBy, picture, children })` from `src/components/support/spread.tsx`
  - `SupportInk()` from `support-ink.tsx`, whose root carries `data-page="support"` and the class `supportPage`; sections `data-part="opening" | "write" | "returns" | "questions"`
  - `NavCurrent` now includes `"support"`
  - `scripts/qa/qa_support.py [base] [--only=group,...]` with `check()`/`open_page()` helpers and a `GROUPS` list later tasks append to

- [ ] **Step 1: Add the preview entries and capture the homepage baseline**

Add two entries to the main checkout's `.claude/launch.json` `configurations` (keep the file's 2-space JSON):

```json
{
  "name": "bigh-support",
  "runtimeExecutable": "npm",
  "runtimeArgs": ["--prefix", "C:/Users/mcbig/Documents/codes/bigh-support", "run", "dev", "--", "--hostname", "localhost", "--port", "3050"],
  "port": 3050
},
{
  "name": "bigh-support-prod",
  "runtimeExecutable": "npm",
  "runtimeArgs": ["--prefix", "C:/Users/mcbig/Documents/codes/bigh-support", "run", "start", "--", "--hostname", "localhost", "--port", "3051"],
  "port": 3051
}
```

Before any source change, capture the homepage baselines the later tasks compare against, on the dev server and on the built site (the built site orders CSS differently, so each is compared with its own kind):

1. `preview_start {name: "bigh-support"}`, then run `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-support/scripts/qa/home_snapshot.py capture http://localhost:3050 baseline-support`. Expected: shots in `scripts/qa/out/baseline-support/`.
2. `npm --prefix C:/Users/mcbig/Documents/codes/bigh-support run build`, `preview_start {name: "bigh-support-prod"}`, then `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-support/scripts/qa/home_snapshot.py capture http://localhost:3051 baseline-support-prod`. Expected: shots in `scripts/qa/out/baseline-support-prod/`. Then `preview_stop` the built site.

- [ ] **Step 2: Write the failing QA**

Create `scripts/qa/qa_support.py` with the harness and the first two groups:

```python
"""QA for the Support page, "Pull up a chair" (Mo, October 14, 2026; spec
docs/superpowers/specs/2026-10-14-support-page-design.md; mockups reference/ink-pages/mockups/support/).

opening (1440x900, 390x844): 200; the title "BiGH — Support"; no console errors or warnings (but
PREFETCH_CSS); no failed requests; one h1 "How can we help?"; the lead; the phone number as a tel:
link in Switzer, the email as a mailto: link, the hours; the porch painting multiplies; its steam is
gold leaf over the porch, not multiplied; nothing scrolls sideways; text 15px+; the menu bar marks
Support (Task 5 adds the link; until then the bar's root says data-page="support").
motion (1440x900): with motion the steam waits while the porch waits, then rises (its --rise grows
from under 30% to 100%+ within 6s of the porch's bloom); reduced motion: the steam is whole at once.
(Later tasks add: rhythm, questions, form, languages, links.)

Pictures: scripts/qa/out/support/<tag>.png.

Usage: python -X utf8 scripts/qa/qa_support.py [base-url] [--only=opening,motion,...]
"""

import os
import re
import sys

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = ARGS[0] if ARGS else "http://localhost:3050"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "support")
os.makedirs(OUT, exist_ok=True)
results = []

PREFETCH_CSS = re.compile(
    r"^The resource \S+/_next/static/\S+\.css was preloaded using link preload but not used "
    r"within a few seconds from the window's load event\."
)


def check(name, ok, detail=""):
    results.append((name, bool(ok)))
    print(f"{'PASS' if ok else 'FAIL'} {name}{(' — ' + str(detail)) if detail and not ok else ''}")


def counted(message):
    return message.type != "warning" or not PREFETCH_CSS.match(message.text)


def open_page(browser, width, height, path="/support", reduced=False):
    context = browser.new_context(
        viewport={"width": width, "height": height},
        reduced_motion="reduce" if reduced else "no-preference",
    )
    page = context.new_page()
    errors, failed = [], []
    page.on("console", lambda m: errors.append(m.text) if m.type in ("error", "warning") and counted(m) else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("requestfailed", lambda r: failed.append(r.url))
    response = page.goto(f"{BASE}{path}", wait_until="networkidle", timeout=120000)
    page.evaluate("document.fonts.ready.then(() => true)")
    page.wait_for_timeout(1200)
    return context, page, response, errors, failed


def scroll_through(page, step=450, pause=250):
    """Read to the end like a visitor (lazy pictures load, blooms fire), then back to the top."""
    total = page.evaluate("document.documentElement.scrollHeight")
    y = 0
    while y < total:
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(pause)
        y += step
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(600)


SMALL_TEXT_JS = """[...document.querySelectorAll('main *')].filter(e => {
  if (!e.childNodes.length || ![...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) return false;
  const s = getComputedStyle(e); return s.visibility !== 'hidden' && s.display !== 'none' && parseFloat(s.fontSize) < 15;
}).map(e => [e.textContent.trim().slice(0, 30), getComputedStyle(e).fontSize])"""


def opening(browser):
    for width, height in ((1440, 900), (390, 844)):
        tag = f"opening {width}"
        context, page, response, errors, failed = open_page(browser, width, height)
        check(f"{tag}: 200", response and response.status == 200, response and response.status)
        check(f"{tag}: the title", page.title() == "BiGH — Support", page.title())
        h1 = page.evaluate("[...document.querySelectorAll('h1')].map(h => h.textContent.trim())")
        check(f"{tag}: one h1, 'How can we help?'", h1 == ["How can we help?"], h1)
        main = page.inner_text("main")
        for words in ["Pull up a chair. We’re listening.", "Call us", "Email us", "Hours",
                      "Monday to Friday, 9am to 6pm Pacific"]:
            check(f"{tag}: says {words!r}", words in main)
        tel = page.evaluate("""(() => { const a = document.querySelector('main a[href^="tel:"]');
          return a ? [a.getAttribute('href'), a.textContent.trim(), getComputedStyle(a).fontFamily] : null; })()""")
        check(f"{tag}: the number is a tel: link in Switzer",
              tel and tel[0] == "tel:+18009192089" and tel[1] == "800-919-2089" and "ysabeau" not in tel[2].lower(), tel)
        mail = page.evaluate("document.querySelector('main a[href^=\"mailto:\"]')?.getAttribute('href')")
        check(f"{tag}: the email is a mailto: link", mail == "mailto:support@bighnow.com", mail)
        blend = page.evaluate("""[...document.querySelectorAll('[data-part="opening"] img')].map(i =>
          [i.getAttribute('src').includes('steam') ? 'steam' : 'ink', getComputedStyle(i).mixBlendMode])""")
        check(f"{tag}: the porch multiplies, its steam does not",
              ["ink", "multiply"] in blend and ["steam", "normal"] in blend, blend)
        title_font = page.evaluate("getComputedStyle(document.querySelector('h1')).fontFamily")
        check(f"{tag}: the title is in Ysabeau", "ysabeau" in title_font.lower(), title_font)
        sideways = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
        check(f"{tag}: nothing scrolls sideways", sideways <= 0, sideways)
        small = page.evaluate(SMALL_TEXT_JS)
        check(f"{tag}: text 15px or more", not small, small[:3])
        check(f"{tag}: the page says it is Support", page.evaluate("document.querySelector('[data-look]')?.dataset.page") == "support")
        page.screenshot(path=os.path.join(OUT, f"opening-{width}.png"))
        scroll_through(page)
        check(f"{tag}: no errors", not errors, errors[:3])
        check(f"{tag}: no failed requests", not failed, failed[:3])
        context.close()


RISE_JS = "parseFloat(getComputedStyle(document.querySelector('[data-steam]')).getPropertyValue('--rise'))"


def motion(browser):
    context, page, *_ = open_page(browser, 1440, 900)
    page.wait_for_function("document.querySelector('[data-part=\"opening\"] [data-bloom]')?.dataset.bloom !== 'waiting'", timeout=10000)
    start = page.evaluate(RISE_JS)
    page.wait_for_timeout(6000)
    end = page.evaluate(RISE_JS)
    check("motion: the steam rises after the porch blooms", start < 30 and end >= 100, [start, end])
    context.close()
    context, page, *_ = open_page(browser, 1440, 900, reduced=True)
    whole = page.evaluate(RISE_JS)
    check("motion (reduced): the steam is whole at once", whole >= 100, whole)
    context.close()


GROUPS = [opening, motion]
ONLY = next((a.split("=", 1)[1].split(",") for a in sys.argv[1:] if a.startswith("--only=")), None)

if __name__ == "__main__":
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

- [ ] **Step 3: Run it to see it fail**

Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-support/scripts/qa/qa_support.py http://localhost:3050 --only=opening`
Expected: FAIL `opening 1440: 200` (404).

- [ ] **Step 4: Widen the menu's current page**

In `src/components/ink/nav/nav-inscription.tsx` line 73:

```ts
/** Which page the bar is on (its link is marked as the current page); the homepage marks none. */
export type NavCurrent = "home" | "products" | "science" | "about" | "support";
```

(Task 5 makes Support a link that uses it; nothing else changes here now.)

- [ ] **Step 5: Write the words**

Create `src/components/support/support-content.ts`:

```ts
// The Support page's words (Mo, October 13-14, 2026; spec
// docs/superpowers/specs/2026-10-14-support-page-design.md). The contact and return details are the
// 2016 ones, which Mo confirmed are still true on October 13. English only for now: none of these
// has a copy key, so every language shows them in English (useCopy returns the source when a
// string has no key). The four answers are drafts Mo approved with the spec on October 14.

/** Real sending (the email service, Resend through Vercel, and bighnow.com's DNS records at
 *  GoDaddy) comes later (Mo, October 14). Until then the form sends nothing and says so; set this
 *  to true when it does, and both preview lines go. */
export const SENDING_LIVE = false;

export const support = {
  opening: {
    title: "How can we help?",
    lead: "Pull up a chair. We’re listening.",
    call: { label: "Call us", value: "800-919-2089", href: "tel:+18009192089" },
    email: { label: "Email us", value: "support@bighnow.com", href: "mailto:support@bighnow.com" },
    hours: { label: "Hours", value: "Monday to Friday, 9am to 6pm Pacific" },
  },
  write: {
    label: "Write to us",
    title: "Send us a message.",
    lead: "We reply within 1–2 business days. Your ticket number comes by email.",
    name: "Your name",
    email: "Email",
    order: "Order number (optional)",
    topic: "What is it about?",
    topics: ["An order", "A return", "A product question", "I had a reaction", "Something else"],
    message: "Your message",
    photo: "Add a photo (optional)",
    removePhoto: "Remove photo",
    send: "Send message",
    reaction:
      "Had a reaction to a product? Choose “I had a reaction” and a person reads it first. In an emergency, call 911.",
    preview: "Preview: messages aren’t sent yet",
    errors: {
      name: "Please add your name.",
      email: "Please add an email we can reply to.",
      topic: "Please choose what it’s about.",
      message: "Please write your message.",
      photoSize: "Photos up to 4 MB, please.",
      photoType: "Please choose a photo (JPG, PNG or HEIC).",
    },
  },
  sent: {
    title: "Thank you.",
    ticket: "Your ticket number",
    reply: "We’ll reply by email within 1–2 business days.",
    preview:
      "This is a preview, so nothing was sent. To reach us today, call 800-919-2089 or email support@bighnow.com.",
    again: "Write another message",
  },
  returns: {
    label: "Returns",
    title: "45 days to decide.",
    lead: "Not happy with a product? Send it back within 45 days for a full refund, no questions asked. Shipping costs aren’t refunded.",
    after: "After 45 days, unopened bottles can still be returned for up to a year.",
    to: "Send returns to",
    address: ["BiGH, 2200 E Route 66, Suite 103", "Glendora, CA 91740"],
    ordersLabel: "Orders and shipping",
    orders: "Our new store opens soon. Until then, no orders or payments are taken on this site.",
  },
  questions: {
    label: "Questions",
    title: "Common questions.",
    items: [
      {
        q: "How do I take my supplements?",
        a: "Follow the directions on your bottle’s label. For questions about your own health, ask your doctor or pharmacist.",
      },
      {
        q: "Can I take them with my medicines?",
        a: "Please ask your doctor or pharmacist first. They know your medicines and your health.",
      },
      {
        q: "Where is my order?",
        a: "Our new store opens soon. Until then, call or email us and we’ll help.",
      },
      {
        q: "Is this site in my language?",
        a: "Choose English, Chinese, Korean, Vietnamese or Japanese at the top of any page. Write to us in any of them, and we’ll reply in yours.",
      },
    ],
    more: "A question about health or science?",
    // Has a copy key already (the homepage's and About's button).
    ask: "Ask BiGH Science",
  },
} as const;

export const ALT = {
  porch:
    "Two empty wooden chairs on a California porch, a cup of coffee on a small table between them, its steam in gold leaf, painted in ink",
  mailbox: "A rural mailbox on a wooden post in tall dry grass, its flag raised, painted in ink",
  parcel: "A parcel tied with twine on wooden porch steps, painted in ink",
  book: "An open book on a porch rail, its pages lifting in a breeze, painted in ink",
} as const;
```

- [ ] **Step 6: Write the local Spread and Painting**

Create `src/components/support/spread.tsx`:

```tsx
"use client";

import Image from "next/image";
import type { CSSProperties, ReactNode } from "react";
import base from "@/components/ink/ink.module.css";
import type { Art, Steam } from "./support-art";
import page from "./support-page.module.css";

// The Support page's one rhythm (as About's, kept here so the live About page is untouched): one
// painting, its words beside it, the sides taking turns from 960px; on one column the painting
// comes first. Paintings multiply onto the page's paper and bloom in as they arrive (the kit's
// useBloom); the server marks them "waiting" so none paints whole first.

export function Painting({
  art,
  alt,
  sizes,
  eager = false,
  preload = false,
  steam,
  className = "",
}: {
  art: Art;
  alt: string;
  sizes: string;
  /** Reaches into the first screen on some windows: loading="eager". */
  eager?: boolean;
  /** The first screen's main painting: Next's preload and fetchPriority="high". */
  preload?: boolean;
  /** The gold steam over this painting (support-art.ts), which rises after the bloom. */
  steam?: Steam;
  className?: string;
}) {
  return (
    <figure className={`${page.painting} ${className}`} data-picture="">
      <span className={page.paintingBody}>
        <Image
          className={base.ink}
          src={art.src}
          alt={alt}
          width={art.width}
          height={art.height}
          sizes={sizes}
          preload={preload}
          fetchPriority={preload ? "high" : undefined}
          loading={eager && !preload ? "eager" : undefined}
          data-bloom="waiting"
        />
        {steam ? (
          <Image
            className={page.steam}
            src={steam.src}
            alt=""
            width={steam.width}
            height={steam.height}
            sizes="200px"
            loading="eager"
            data-steam=""
            style={
              {
                left: `${(steam.left * 100).toFixed(2)}%`,
                top: `${(steam.top * 100).toFixed(2)}%`,
                width: `${(steam.size * 100).toFixed(2)}%`,
              } as CSSProperties
            }
          />
        ) : null}
      </span>
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
  part: string;
  /** Where the painting stands from 960px. */
  side: "left" | "right";
  labelledBy: string;
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

- [ ] **Step 7: Write the page component (opening only for now)**

Create `src/components/support/support-ink.tsx`:

```tsx
"use client";

import { InkPage } from "@/components/ink/ink-page";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { porch } from "./support-art";
import { ALT, support } from "./support-content";
import { Painting } from "./spread";
import page from "./support-page.module.css";

// Support, "Pull up a chair" (Mo, October 14, 2026; mockup reference/ink-pages/mockups/support/;
// spec docs/superpowers/specs/2026-10-14-support-page-design.md). A California porch opens the
// page; its cup's gold steam rises once the porch has bloomed (support-page.module.css), and again
// when a message is sent. Then Write to us, Returns and Questions, one painting each, sides taking
// turns. No brush line.

function Opening() {
  const copy = useCopy();
  const o = support.opening;
  return (
    <section className={page.opening} data-part="opening" aria-labelledby="support-title">
      <div className={base.wrap}>
        <Painting
          art={porch}
          alt={copy(ALT.porch)}
          sizes="(max-width: 599px) 92vw, 780px"
          preload
          steam={porch.steam}
          className={page.porch}
        />
        <h1 id="support-title" className={page.title}>
          {copy(o.title)}
        </h1>
        <p className={page.lead}>{copy(o.lead)}</p>
        <dl className={page.contact}>
          <div>
            <dt>{copy(o.call.label)}</dt>
            <dd>
              <a className={page.number} href={o.call.href}>
                {o.call.value}
              </a>
            </dd>
          </div>
          <div>
            <dt>{copy(o.email.label)}</dt>
            <dd>
              <a href={o.email.href}>{o.email.value}</a>
            </dd>
          </div>
          <div>
            <dt>{copy(o.hours.label)}</dt>
            <dd>{copy(o.hours.value)}</dd>
          </div>
        </dl>
      </div>
    </section>
  );
}

export function SupportInk({ titleFont }: { titleFont: string }) {
  return (
    <InkPage current="support" className={`${page.supportPage} ${titleFont}`}>
      {() => (
        <div data-support="porch">
          <Opening />
        </div>
      )}
    </InkPage>
  );
}
```

- [ ] **Step 8: Write the page's styles (opening part)**

Create `src/components/support/support-page.module.css`:

```css
/* Support, "Pull up a chair" (Mo, October 14, 2026; spec
   docs/superpowers/specs/2026-10-14-support-page-design.md). Every rule is scoped under
   .supportPage (the page root, InkPage className), so it outranks the kit's .look rules in any
   stylesheet order. Multiply: nothing between a painting and the page root may make a stacking
   context (no z-index on a positioned ancestor, no isolation, opacity, transform, filter or mask on
   a part, a spread, a figure or a wrapper). */

/* Titles in Ysabeau, the homepage's title face; menus, words and pills stay in Switzer. The
   attribute outranks the kit's .look rule in either order (as home-titles.module.css does). */
.supportPage[data-look="ink"] {
  --display-font: var(--font-ysabeau), var(--font-dm-sans), Arial, sans-serif;
  --part-half: clamp(40px, 4.4vw, 84px);
  --gap: clamp(40px, 6vw, 112px);
}

.supportPage[data-look="ink"] main :is(h1, h2, h3) {
  font-family: var(--display-font);
  font-variant-numeric: lining-nums;
}

/* ---- The opening: the porch, the question, how to reach us -------------------------------- */

.supportPage .opening {
  padding: calc(88px + clamp(8px, 2vw, 40px)) 0 var(--part-half);
  text-align: center;
}

.supportPage .porch {
  --picture: 780px;
  margin-inline: auto;
}

.supportPage h1.title {
  margin: clamp(4px, 1vw, 16px) 0 0;
  font-family: var(--display-font);
  font-weight: var(--display-weight);
  font-size: clamp(min(44px, 11vw), 4.4vw, 68px);
  line-height: 1.04;
  letter-spacing: -0.03em;
  text-wrap: balance;
}

.supportPage p.lead {
  margin: clamp(12px, 1.2vw, 18px) 0 0;
  color: var(--muted);
  font-size: clamp(19px, 1.5vw, 23px);
  line-height: 1.45;
}

/* Three ways to reach us, split by hairlines; stacked on a phone. */
.supportPage .contact {
  display: grid;
  grid-template-columns: repeat(3, auto);
  justify-content: center;
  margin: clamp(36px, 3.6vw, 56px) 0 0;
}

.supportPage .contact > div {
  padding: 0 clamp(24px, 3vw, 52px);
  border-left: 1px solid var(--line);
}

.supportPage .contact > div:first-child {
  border-left: 0;
}

.supportPage .contact dt {
  color: var(--muted);
  font-size: 17px;
  font-weight: 450;
}

.supportPage .contact dd {
  margin: 6px 0 0;
  font-size: 21px;
  font-weight: 450;
}

.supportPage .contact a {
  display: inline-flex;
  align-items: center;
  min-height: 48px;
  color: var(--ink);
  text-decoration: underline;
  text-decoration-thickness: 1px;
  text-underline-offset: 8px;
  text-decoration-color: var(--hair);
}

.supportPage .contact a:hover {
  text-decoration-color: var(--ink);
}

/* The number in Switzer (never Ysabeau, whose old-style digits rise and fall), large. */
.supportPage .contact a.number {
  font-family: var(--sans);
  font-size: clamp(28px, 2.3vw, 36px);
  font-weight: 500;
  letter-spacing: -0.01em;
  font-variant-numeric: lining-nums tabular-nums;
}

@media (max-width: 759px) {
  .supportPage .contact {
    grid-template-columns: minmax(0, 1fr);
    row-gap: 22px;
  }

  .supportPage .contact > div {
    padding: 0;
    border-left: 0;
  }
}

/* ---- Paintings ------------------------------------------------------------------------------ */

.supportPage .painting {
  justify-self: center;
  width: min(100%, var(--picture, 520px));
  margin: 0;
}

.supportPage .paintingBody {
  position: relative;
  display: block;
}

.supportPage .paintingBody img {
  display: block;
  width: 100%;
  height: auto;
}

/* The gold steam over the cup: gold leaf, not multiplied, placed by support-art.ts. */
.supportPage .paintingBody img.steam {
  position: absolute;
  max-width: none;
  height: auto;
}

/* ---- Motion: the steam rises from the cup once the porch has bloomed ----------------------- */

@property --rise {
  syntax: "<percentage>";
  inherits: false;
  initial-value: 112%;
}

.supportPage [data-steam] {
  -webkit-mask-image: linear-gradient(to top, #000 calc(var(--rise) - 14%), transparent var(--rise));
  mask-image: linear-gradient(to top, #000 calc(var(--rise) - 14%), transparent var(--rise));
}

@media (prefers-reduced-motion: no-preference) and (scripting: enabled) {
  .supportPage [data-steam] {
    --rise: 0%;
  }

  .supportPage :is([data-bloom="in"], [data-bloom="done"]) ~ [data-steam] {
    animation: steam-rise var(--breath) var(--ease) 1.1s both;
  }
}

@keyframes steam-rise {
  from {
    --rise: 0%;
  }

  to {
    --rise: 112%;
  }
}

/* A painting waiting to bloom is hidden until its bloom is under way (About's hold, for the same
   Chrome bug: a mask layer of no size is dropped, so a waiting painting showed whole). */
@media (prefers-reduced-motion: no-preference) {
  .supportPage [data-bloom="waiting"] {
    opacity: 0;
  }

  @media (scripting: none) {
    .supportPage [data-bloom="waiting"] {
      opacity: 1;
    }
  }
}

@media (prefers-reduced-motion: reduce), (scripting: none) {
  :global([data-look="ink"]).supportPage [data-bloom="waiting"] {
    filter: none;
  }
}
```

- [ ] **Step 9: Write the route**

Create `src/app/[locale]/support/page.tsx`:

```tsx
import { Ysabeau } from "next/font/google";
import type { Metadata } from "next";
import { getTranslations, setRequestLocale } from "next-intl/server";
import { ProductPagesProvider } from "@/components/home/product-action";
import { SiteDialogs } from "@/components/ink/dialogs";
import { productPageLinks } from "@/components/product/catalog";
import { SupportInk } from "@/components/support/support-ink";
import copyKeys from "@/i18n/copy-keys.json";
import { redirect } from "@/i18n/navigation";

type Params = Promise<{ locale: string }>;

// Ysabeau, the homepage's title face (src/app/[locale]/page.tsx): not preloaded, so the build does
// not hoist its preload onto every page.
const titles = Ysabeau({
  subsets: ["latin", "vietnamese"],
  variable: "--font-ysabeau",
  display: "swap",
  preload: false,
});

// "BiGH — Support", with "Support" from the catalogs (the menu's own word for this page).
export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const { locale } = await params;
  const translate = await getTranslations({ locale, namespace: "Copy" });
  return { title: `BiGH — ${translate(copyKeys["Support"])}` };
}

// The Support page in the Ink & Gold look (Mo, October 14, 2026), on the shared kit and sheets.
// /hken goes to Chinese, as on every page.
export default async function Page({ params }: { params: Params }) {
  const { locale } = await params;
  if (locale === "hken") redirect({ href: "/support", locale: "cns" });
  setRequestLocale(locale);

  return (
    <ProductPagesProvider pages={productPageLinks()}>
      <SiteDialogs>
        <SupportInk titleFont={titles.variable} />
      </SiteDialogs>
    </ProductPagesProvider>
  );
}
```

- [ ] **Step 10: Restart the dev server and run the QA**

A new route folder 404s until the dev server restarts (`preview_stop` then `preview_start {name: "bigh-support"}`).

Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-support/scripts/qa/qa_support.py http://localhost:3050 --only=opening,motion`
Expected: all PASS. Then `npm --prefix C:/Users/mcbig/Documents/codes/bigh-support run type-check` and `npx --prefix C:/Users/mcbig/Documents/codes/bigh-support eslint src/components/support "src/app/[locale]/support"`: no errors.

- [ ] **Step 11: Look at it**

Open `scripts/qa/out/support/opening-1440.png` and `opening-390.png` with Read, beside `reference/ink-pages/mockups/support/a-desk.jpg` and `a-phone.jpg`. The opening should read as the mockup's: the porch centred and large, the title under it, the three ways to reach us in one row (stacked on the phone), the gold steam over the cup. Score it honestly out of 10; under 8, fix and look again.

- [ ] **Step 12: Commit**

```bash
git -C C:/Users/mcbig/Documents/codes/bigh-support add "src/app/[locale]/support" src/components/support src/components/ink/nav/nav-inscription.tsx scripts/qa/qa_support.py
git -C C:/Users/mcbig/Documents/codes/bigh-support commit -m "feat(support): the /support page and its opening, the porch's gold steam rising" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: Returns and Questions

**Files:**
- Modify: `src/components/support/support-ink.tsx`
- Modify: `src/components/support/support-page.module.css`
- Modify: `scripts/qa/qa_support.py`

**Interfaces:**
- Consumes: `Spread`, `Painting` (Task 2), `parcel`, `book`, `mailbox` (Task 1), `support.returns`, `support.questions`, `ALT` (Task 2), `useSiteDialogs().openAsk` (`src/components/ink/dialogs.tsx`).
- Produces: sections `#write` (a placeholder Spread with the mailbox and the write heading; Task 4 fills the form), `#returns`, `#questions`; the CSS classes `.part`, `.spread`, `.words`, `.label`, `.heading`, `.body`, `.address`, `.rule`, `.faq`, `.answer`, `.more`.

- [ ] **Step 1: Write the failing QA groups**

Append to `scripts/qa/qa_support.py` (before `GROUPS`), and set `GROUPS = [opening, motion, rhythm, questions]`:

```python
SIDES_JS = """[...document.querySelectorAll('main [data-part]')].filter(s => s.querySelector('[data-picture]') && s.dataset.part !== 'opening').map(s => {
  const p = s.querySelector('[data-picture]').getBoundingClientRect(), w = s.querySelector('[data-words]').getBoundingClientRect();
  return [s.dataset.part, p.left < w.left ? 'left' : p.top < w.top ? 'first' : 'right', Math.round(w.right), Math.round(p.width)]; })"""


def rhythm(browser):
    for width, height in ((1440, 900), (1280, 800), (1024, 768), (960, 800), (768, 1024), (390, 844), (360, 780)):
        tag = f"rhythm {width}"
        context, page, *_ = open_page(browser, width, height)
        scroll_through(page)
        sides = page.evaluate(SIDES_JS)
        parts = [s[0] for s in sides]
        check(f"{tag}: write, returns and questions each have a painting", parts == ["write", "returns", "questions"], parts)
        if width >= 960:
            check(f"{tag}: sides take turns (left, right, left)", [s[1] for s in sides] == ["left", "right", "left"], sides)
        else:
            check(f"{tag}: one column, each painting first", all(s[1] == "first" for s in sides), sides)
        over = page.evaluate("""[...document.querySelectorAll('main [data-words] *')].filter(e => e.getBoundingClientRect().right > window.innerWidth - 16 && e.textContent.trim()).map(e => e.textContent.trim().slice(0, 24))""")
        check(f"{tag}: no words past the right margin", not over, over[:3])
        sideways = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
        check(f"{tag}: nothing scrolls sideways", sideways <= 0, sideways)
        main = page.inner_text("main")
        for words in ["45 days to decide.", "Send returns to", "Glendora, CA 91740", "Orders and shipping",
                      "Common questions.", "A question about health or science?"]:
            check(f"{tag}: says {words!r}", words in main)
        page.screenshot(path=os.path.join(OUT, f"rhythm-{width}.png"), full_page=False)
        context.close()


def questions(browser):
    context, page, *_ = open_page(browser, 1440, 900)
    faq = page.locator("#questions details")
    check("questions: four questions", faq.count() == 4, faq.count())
    check("questions: the first is open at rest", faq.nth(0).get_attribute("open") is not None)
    faq.nth(2).locator("summary").click()
    page.wait_for_timeout(300)
    opened = page.evaluate("[...document.querySelectorAll('#questions details')].map(d => d.open)")
    check("questions: opening one closes the others", opened == [False, False, True, False], opened)
    heights = page.evaluate("[...document.querySelectorAll('#questions summary')].map(s => Math.round(s.getBoundingClientRect().height))")
    check("questions: every question is a 48px+ target", all(h >= 48 for h in heights), heights)
    ask = page.locator("#questions button", has_text="Ask BiGH Science")
    ask.scroll_into_view_if_needed()
    ask.click()
    page.wait_for_timeout(1200)
    check("questions: Ask BiGH Science opens its sheet", page.evaluate("!!document.querySelector('dialog[open]')"))
    page.keyboard.press("Escape")
    context.close()
```

- [ ] **Step 2: Run them to see them fail**

Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-support/scripts/qa/qa_support.py http://localhost:3050 --only=rhythm,questions`
Expected: FAIL (no parts, no details).

- [ ] **Step 3: Add the three parts**

In `support-ink.tsx`, add the imports and parts, and render them after `<Opening />`:

```tsx
import type { ReactNode } from "react";
import { useSiteDialogs } from "@/components/ink/dialogs";
import { book, mailbox, parcel, porch } from "./support-art";
import { Painting, Spread } from "./spread";

// What each painting asks the server for follows the width it is drawn at: --picture per part
// (support-page.module.css), the column's width below that.
const MAILBOX = "(max-width: 599px) 70vw, (max-width: 959px) 360px, 380px";
const WIDE = "(max-width: 599px) 86vw, (max-width: 959px) 520px, 520px";

function Write({ children }: { children?: ReactNode }) {
  const copy = useCopy();
  const w = support.write;
  return (
    <Spread
      id="write"
      part="write"
      side="left"
      labelledBy="write-title"
      picture={<Painting art={mailbox} alt={copy(ALT.mailbox)} sizes={MAILBOX} className={page.mailbox} />}
    >
      <p className={page.label}>{copy(w.label)}</p>
      <h2 id="write-title" className={page.heading}>
        {copy(w.title)}
      </h2>
      <p className={page.body}>{copy(w.lead)}</p>
      {children}
    </Spread>
  );
}

function Returns() {
  const copy = useCopy();
  const r = support.returns;
  return (
    <Spread
      id="returns"
      part="returns"
      side="right"
      labelledBy="returns-title"
      picture={<Painting art={parcel} alt={copy(ALT.parcel)} sizes={WIDE} className={page.parcel} />}
    >
      <p className={page.label}>{copy(r.label)}</p>
      <h2 id="returns-title" className={page.heading}>
        {copy(r.title)}
      </h2>
      <p className={page.body}>{copy(r.lead)}</p>
      <p className={page.body}>{copy(r.after)}</p>
      <p className={page.address}>
        <span>{copy(r.to)}</span>
        {r.address.map((line) => (
          <span key={line}>{line}</span>
        ))}
      </p>
      <hr className={page.rule} />
      <p className={page.label}>{copy(r.ordersLabel)}</p>
      <p className={page.body}>{copy(r.orders)}</p>
    </Spread>
  );
}

function Questions() {
  const copy = useCopy();
  const dialogs = useSiteDialogs();
  const q = support.questions;
  return (
    <Spread
      id="questions"
      part="questions"
      side="left"
      labelledBy="questions-title"
      picture={<Painting art={book} alt={copy(ALT.book)} sizes={WIDE} className={page.book} />}
    >
      <p className={page.label}>{copy(q.label)}</p>
      <h2 id="questions-title" className={page.heading}>
        {copy(q.title)}
      </h2>
      <div className={page.faq}>
        {q.items.map((item, i) => (
          <details key={item.q} name="support-questions" open={i === 0}>
            <summary>
              <span>{copy(item.q)}</span>
              <span className={page.toggle} aria-hidden="true" />
            </summary>
            <p className={page.answer}>{copy(item.a)}</p>
          </details>
        ))}
      </div>
      <p className={page.more}>{copy(q.more)}</p>
      <button type="button" className={`${base.pill} ${base.pillGhost}`} onClick={dialogs.openAsk}>
        {copy(q.ask)}
      </button>
    </Spread>
  );
}
```

`SupportInk`'s body becomes:

```tsx
        <div data-support="porch">
          <Opening />
          <Write />
          <Returns />
          <Questions />
        </div>
```

(Merge these imports with the ones Task 2 wrote: one `./support-art` import, one `./spread` import.)

- [ ] **Step 4: Add the parts' styles**

Append to `support-page.module.css`:

```css
/* ---- The parts: one painting, its words beside it, sides taking turns -------------------- */

.supportPage .part {
  padding-block: var(--part-half);
  scroll-margin-top: calc(108px - 150px - var(--part-half));
}

.supportPage .spread {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  row-gap: clamp(24px, 5vw, 40px);
  align-items: center;
}

.supportPage .words {
  min-width: 0;
}

@media (min-width: 600px) and (max-width: 959px) {
  .supportPage .spread {
    max-width: calc(640px + 2 * var(--gutter));
  }
}

@media (min-width: 960px) {
  .supportPage .spread {
    grid-template-columns: 5fr 7fr;
    column-gap: var(--gap);
  }

  .supportPage .spread[data-side="right"] {
    grid-template-columns: 7fr 5fr;
  }

  .supportPage .spread[data-side="right"] > [data-picture] {
    order: 2;
  }
}

.supportPage .mailbox {
  --picture: 380px;
}

.supportPage .parcel,
.supportPage .book {
  --picture: 520px;
}

.supportPage p.label {
  margin: 0 0 14px;
  color: var(--muted);
  font-size: 17px;
  font-weight: 450;
  line-height: 1.3;
}

.supportPage h2.heading {
  margin: 0;
  font-family: var(--display-font);
  font-weight: var(--display-weight);
  font-size: clamp(min(36px, 9.2vw), 3.2vw, 50px);
  line-height: 1.08;
  letter-spacing: -0.025em;
  text-wrap: balance;
}

.supportPage p.body {
  max-width: 32em;
  margin: clamp(14px, 1.4vw, 20px) 0 0;
  color: var(--muted);
  font-size: 19px;
  line-height: 1.6;
}

.supportPage p.address {
  margin: 26px 0 0;
  font-size: 19px;
  line-height: 1.5;
}

.supportPage .address > span {
  display: block;
}

.supportPage .address > span:first-child {
  color: var(--muted);
}

.supportPage hr.rule {
  max-width: 32em;
  margin: 40px 0 34px;
  border: 0;
  border-top: 1px solid var(--line);
}

/* Questions on hairlines; one open at a time (the details share a name). */
.supportPage .faq {
  margin-top: clamp(24px, 2.4vw, 36px);
  border-top: 1px solid var(--line);
}

.supportPage .faq details {
  border-bottom: 1px solid var(--line);
}

.supportPage .faq summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  min-height: 64px;
  padding: 12px 0;
  font-size: 21px;
  font-weight: 450;
  line-height: 1.35;
  list-style: none;
  cursor: pointer;
}

.supportPage .faq summary::-webkit-details-marker {
  display: none;
}

/* A plus that becomes a minus: two 1.5px ink strokes, the upright one folding away. */
.supportPage .toggle {
  position: relative;
  flex: none;
  width: 18px;
  height: 18px;
}

.supportPage .toggle::before,
.supportPage .toggle::after {
  content: "";
  position: absolute;
  inset: 8.25px 0 auto;
  height: 1.5px;
  background: var(--ink);
  transition: rotate 0.5s var(--ease);
}

.supportPage .toggle::after {
  rotate: 90deg;
}

.supportPage details[open] .toggle::after {
  rotate: 0deg;
}

.supportPage p.answer {
  max-width: 32em;
  margin: 0;
  padding: 0 0 22px;
  color: var(--muted);
  font-size: 19px;
  line-height: 1.6;
}

.supportPage p.more {
  margin: clamp(32px, 3vw, 44px) 0 16px;
  font-size: 21px;
  font-weight: 450;
}

/* The page's last part leads into the footer's finale, which opens on its own paper. */
.supportPage section[data-part="questions"] {
  padding-bottom: 0;
}
```

- [ ] **Step 5: Run the QA**

Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-support/scripts/qa/qa_support.py http://localhost:3050 --only=opening,motion,rhythm,questions`
Expected: all PASS.

- [ ] **Step 6: Look at it**

Open `rhythm-1440.png`, `rhythm-960.png`, `rhythm-390.png` and `rhythm-360.png`, scroll-stitching more screens where needed (never a full-page screenshot: the page's svh opening breaks it). Compare with the mockup. The paintings should read about the same size, the parcel's part should not look denser than the others, and the questions should sit calmly on their hairlines. Score out of 10; under 8, fix and look again.

- [ ] **Step 7: Commit**

```bash
git -C C:/Users/mcbig/Documents/codes/bigh-support add src/components/support scripts/qa/qa_support.py
git -C C:/Users/mcbig/Documents/codes/bigh-support commit -m "feat(support): Write to us, Returns and Questions parts, sides taking turns" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: The form and the moment

**Files:**
- Create: `src/components/support/support-form.ts` (the rules: checks and the ticket number, no React)
- Create: `src/components/support/support-form.tsx` (the form and the thank-you)
- Modify: `src/components/support/support-ink.tsx` (render the form inside `Write`)
- Modify: `src/components/support/support-page.module.css`
- Modify: `scripts/qa/qa_support.py`

**Interfaces:**
- Consumes: `support.write`, `support.sent`, `SENDING_LIVE` (Task 2); `cup` (Task 1); `Write` accepts `children` (Task 3).
- Produces:
  - `support-form.ts`: `type Fields = { name: string; email: string; topic: string; message: string; photo: File | null }`, `type FieldName = "name" | "email" | "topic" | "message" | "photo"`, `type Problems = Partial<Record<FieldName, string>>`, `const PHOTO_MAX = 4 * 1024 * 1024`, `function checkPhoto(file: File): string | null` (returns an English message source or null), `function checkFields(fields: Fields): Problems`, `function ticketNumber(now?: Date, random?: () => number): string`
  - `support-form.tsx`: `export function SupportForm()`; DOM hooks `form[data-support-form]`, inputs `#support-name`, `#support-email`, `#support-order`, radio `name="topic"`, `#support-message`, `#support-photo`, the thank-you `[data-sent]` with `h3#sent-title` and `[data-ticket]`, the honesty tags `[data-honesty]`

- [ ] **Step 1: Write the failing QA group**

Append to `qa_support.py` and set `GROUPS = [opening, motion, rhythm, questions, form]`:

```python
import tempfile

TICKET = re.compile(r"^BH-\d{4}-[A-HJKMNP-Z2-9]{4}$")


def fill(page, name="Ana Ruiz", email="ana@example.com", topic="A return", message="The seal on my bottle was broken."):
    page.fill("#support-name", name)
    page.fill("#support-email", email)
    if topic:
        page.locator("label", has_text=topic).click()
    page.fill("#support-message", message)


def form(browser):
    for width, height in ((1440, 900), (390, 844), (360, 780)):
        tag = f"form {width}"
        context, page, *_ = open_page(browser, width, height)
        page.locator("#write").scroll_into_view_if_needed()
        page.wait_for_timeout(600)
        main = page.inner_text("#write")
        for words in ["Your name", "Email", "Order number (optional)", "What is it about?", "Your message",
                      "Add a photo (optional)", "I had a reaction", "In an emergency, call 911."]:
            check(f"{tag}: says {words!r}", words in main)
        check(f"{tag}: the preview tag stands beside Send", page.locator("form [data-honesty]").inner_text().strip() == "Preview: messages aren’t sent yet")
        rows = page.evaluate("""(() => { const tops = {}; document.querySelectorAll('[data-topics] label').forEach(l => { const t = Math.round(l.getBoundingClientRect().top); tops[t] = (tops[t] || 0) + 1; }); return Object.values(tops); })()""")
        check(f"{tag}: the topic chips never leave one alone on a row", rows == [1, 1, 1, 1, 1] or 1 not in rows, rows)
        targets = page.evaluate("""[...document.querySelectorAll('form input:not([type=radio]):not([type=file]), form textarea, form button, [data-topics] label, form label[for=support-photo]')]
          .map(e => [e.id || e.textContent.trim().slice(0, 20), Math.round(e.getBoundingClientRect().height)]).filter(([, h]) => h < 48)""")
        check(f"{tag}: every control is 48px or more", not targets, targets)
        boxes = page.evaluate("""[...document.querySelectorAll('form input:not([type=radio]):not([type=file]), form textarea')].filter(e => {
          const s = getComputedStyle(e); return parseFloat(s.borderTopWidth) > 0 || parseFloat(s.borderLeftWidth) > 0; }).map(e => e.id)""")
        check(f"{tag}: fields are writing lines, never boxes", not boxes, boxes)

        # Send with nothing filled: four plain messages, focus on the first field.
        page.click("form button[type=submit]")
        page.wait_for_timeout(300)
        errs = page.evaluate("[...document.querySelectorAll('form [data-error]')].map(e => e.textContent.trim())")
        check(f"{tag}: empty Send says what is missing", errs == ["Please add your name.", "Please add an email we can reply to.", "Please choose what it’s about.", "Please write your message."], errs)
        check(f"{tag}: focus goes to the first missing field", page.evaluate("document.activeElement.id") == "support-name")
        check(f"{tag}: the missing fields are marked invalid", page.evaluate("document.querySelector('#support-name').getAttribute('aria-invalid')") == "true")

        # A wrong email, then a fix.
        fill(page, email="ana@")
        page.click("form button[type=submit]")
        page.wait_for_timeout(300)
        errs = page.evaluate("[...document.querySelectorAll('form [data-error]')].map(e => e.textContent.trim())")
        check(f"{tag}: a wrong email is caught", errs == ["Please add an email we can reply to."], errs)

        # Photos: too big, not a picture, then a good one, removed.
        with tempfile.TemporaryDirectory() as tmp:
            big = os.path.join(tmp, "big.jpg")
            with open(big, "wb") as f:
                f.write(b"\xff\xd8\xff" + b"0" * (5 * 1024 * 1024))
            pdf = os.path.join(tmp, "label.pdf")
            with open(pdf, "wb") as f:
                f.write(b"%PDF-1.4\n%%EOF\n")
            small = os.path.join(tmp, "bottle.png")
            with open(small, "wb") as f:
                f.write(bytes.fromhex("89504e470d0a1a0a0000000d4948445200000001000000010806000000"
                                      "1f15c4890000000d49444154789c6360000002000154a24f5d0000000049454e44ae426082"))
            page.set_input_files("#support-photo", big)
            page.wait_for_timeout(200)
            check(f"{tag}: a 5 MB photo is refused", "Photos up to 4 MB, please." in page.inner_text("form"))
            page.set_input_files("#support-photo", pdf)
            page.wait_for_timeout(200)
            check(f"{tag}: a PDF is refused", "Please choose a photo (JPG, PNG or HEIC)." in page.inner_text("form"))
            page.set_input_files("#support-photo", small)
            page.wait_for_timeout(200)
            check(f"{tag}: a picture is kept, by name", "bottle.png" in page.inner_text("form"))
            page.click("form button:has-text('Remove photo')")
            page.wait_for_timeout(200)
            check(f"{tag}: the photo can be removed", "bottle.png" not in page.inner_text("form"))

        # Send twice quickly and Enter in a field: one thank-you, one number.
        fill(page)
        page.focus("#support-name")
        page.keyboard.press("Enter")
        page.click("form button[type=submit]", timeout=1000) if page.locator("form button[type=submit]").count() else None
        page.wait_for_timeout(500)
        panels = page.locator("[data-sent]").count()
        ticket = page.locator("[data-ticket]").inner_text().strip() if panels else ""
        check(f"{tag}: one thank-you", panels == 1, panels)
        check(f"{tag}: a ticket number like BH-1014-7K3Q", TICKET.match(ticket) is not None, ticket)
        today = page.evaluate("(() => { const d = new Date(); return String(d.getMonth() + 1).padStart(2, '0') + String(d.getDate()).padStart(2, '0'); })()")
        check(f"{tag}: the ticket carries today's month and day", ticket[3:7] == today, [ticket, today])
        check(f"{tag}: focus moves to the thank-you", page.evaluate("document.activeElement.id") == "sent-title")
        sent = page.inner_text("[data-sent]")
        check(f"{tag}: the thank-you says nothing was sent, and how to reach us",
              "This is a preview, so nothing was sent." in sent and "800-919-2089" in sent and "support@bighnow.com" in sent, sent)
        page.wait_for_timeout(1500)
        check(f"{tag}: the number holds still", page.locator("[data-ticket]").inner_text().strip() == ticket)
        page.screenshot(path=os.path.join(OUT, f"sent-{width}.png"))

        # Write another message: an empty form, focus on the name.
        page.click("[data-sent] button:has-text('Write another message')")
        page.wait_for_timeout(400)
        check(f"{tag}: Write another message brings back an empty form",
              page.locator("form[data-support-form]").count() == 1 and page.input_value("#support-name") == "")
        check(f"{tag}: focus goes to Your name", page.evaluate("document.activeElement.id") == "support-name")
        context.close()

    # Reduced motion: the thank-you is there at once, its steam whole.
    context, page, *_ = open_page(browser, 1440, 900, reduced=True)
    page.locator("#write").scroll_into_view_if_needed()
    fill(page)
    page.click("form button[type=submit]")
    page.wait_for_timeout(100)
    rise = page.evaluate("parseFloat(getComputedStyle(document.querySelector('[data-sent] [data-steam]')).getPropertyValue('--rise'))")
    check("form (reduced): the thank-you at once, its steam whole", page.locator("[data-sent]").count() == 1 and rise >= 100, rise)
    context.close()
```

Note on the double send: the Enter press submits; the second click is skipped when the form has gone (the thank-you replaced it). The check is that one panel and one stable number result either way.

- [ ] **Step 2: Run it to see it fail**

Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-support/scripts/qa/qa_support.py http://localhost:3050 --only=form`
Expected: FAIL on the first "says" lines (no form yet).

- [ ] **Step 3: Write the rules**

Create `src/components/support/support-form.ts`:

```ts
// The Support form's rules (spec "The form"): what must be filled, what a photo may be, and the
// ticket number. Plain functions, no React, so the form and its checks read the same rules.
import { support } from "./support-content";

export type Fields = { name: string; email: string; topic: string; message: string; photo: File | null };
export type FieldName = "name" | "email" | "topic" | "message" | "photo";
export type Problems = Partial<Record<FieldName, string>>;

export const PHOTO_MAX = 4 * 1024 * 1024;
const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const PICTURE = /^image\/(jpeg|png|heic|heif|webp|gif)$/;
const errors = support.write.errors;

/** A photo's problem (an English source for copy()), or null when it may be kept. */
export function checkPhoto(file: File): string | null {
  if (!PICTURE.test(file.type) && !/\.(jpe?g|png|heic|heif|webp|gif)$/i.test(file.name)) return errors.photoType;
  if (file.size > PHOTO_MAX) return errors.photoSize;
  return null;
}

/** Every field's problem, in the form's order (an empty object when it may be sent). */
export function checkFields(fields: Fields): Problems {
  const problems: Problems = {};
  if (!fields.name.trim()) problems.name = errors.name;
  if (!EMAIL.test(fields.email.trim())) problems.email = errors.email;
  if (!fields.topic) problems.topic = errors.topic;
  if (!fields.message.trim()) problems.message = errors.message;
  if (fields.photo) {
    const photo = checkPhoto(fields.photo);
    if (photo) problems.photo = photo;
  }
  return problems;
}

// No 0/O, 1/I/L: a number read over the phone is never mistaken.
const SIGNS = "ABCDEFGHJKMNPQRSTUVWXYZ23456789";

/** BH- + the month and day + four signs, e.g. BH-1014-7K3Q. Until real sending, the page makes it
 *  up; the email service will issue it then (spec "Not in this spec"). */
export function ticketNumber(now = new Date(), random: () => number = Math.random): string {
  const mmdd = `${String(now.getMonth() + 1).padStart(2, "0")}${String(now.getDate()).padStart(2, "0")}`;
  let tail = "";
  for (let i = 0; i < 4; i += 1) tail += SIGNS[Math.floor(random() * SIGNS.length)];
  return `BH-${mmdd}-${tail}`;
}
```

(The QA's `TICKET` pattern `[A-HJKMNP-Z2-9]` matches exactly these signs.)

- [ ] **Step 4: Write the form and the thank-you**

Create `src/components/support/support-form.tsx`:

```tsx
"use client";

import Image from "next/image";
import { ArrowRight } from "lucide-react";
import { useEffect, useRef, useState, type CSSProperties, type FormEvent } from "react";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { cup } from "./support-art";
import { SENDING_LIVE, support } from "./support-content";
import { checkFields, checkPhoto, ticketNumber, type FieldName, type Problems } from "./support-form";
import page from "./support-page.module.css";

// The Support form (spec "The form", "The moment", "Honesty"): writing lines on the paper, never
// boxes; checks on Send in plain words beside each field, focus to the first; on Send the form
// gives way to the cup, its gold steam rising again, and a ticket number. It sends nothing until
// SENDING_LIVE: the preview tag and the thank-you's preview line say so.

const ORDER: FieldName[] = ["name", "email", "topic", "message", "photo"];
const FOCUS: Record<FieldName, string> = {
  name: "support-name",
  email: "support-email",
  topic: "support-topic-0",
  message: "support-message",
  photo: "support-photo",
};

export function SupportForm() {
  const copy = useCopy();
  const w = support.write;
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [order, setOrder] = useState("");
  const [topic, setTopic] = useState("");
  const [message, setMessage] = useState("");
  const [photo, setPhoto] = useState<File | null>(null);
  const [problems, setProblems] = useState<Problems>({});
  const [ticket, setTicket] = useState<string | null>(null);
  const photoInput = useRef<HTMLInputElement>(null);
  const sentTitle = useRef<HTMLHeadingElement>(null);
  const nameInput = useRef<HTMLInputElement>(null);
  // Flipped by "Write another message", so the fresh form's name field takes focus (never on the
  // page's first render: the first run of the effect is skipped).
  const [again, setAgain] = useState(false);
  const firstRender = useRef(true);

  useEffect(() => {
    if (ticket) sentTitle.current?.focus();
  }, [ticket]);
  useEffect(() => {
    if (firstRender.current) {
      firstRender.current = false;
      return;
    }
    nameInput.current?.focus();
  }, [again]);

  const send = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (ticket) return; // one thank-you, one number
    const found = checkFields({ name, email, topic, message, photo });
    setProblems(found);
    const first = ORDER.find((field) => found[field]);
    if (first) {
      document.getElementById(FOCUS[first])?.focus();
      return;
    }
    setTicket(ticketNumber());
  };

  const choosePhoto = (file: File | undefined) => {
    if (!file) return;
    const problem = checkPhoto(file);
    if (problem) {
      setPhoto(null);
      if (photoInput.current) photoInput.current.value = "";
      setProblems((p) => ({ ...p, photo: problem }));
      return;
    }
    setPhoto(file);
    setProblems((p) => ({ ...p, photo: undefined }));
  };

  const removePhoto = () => {
    setPhoto(null);
    if (photoInput.current) photoInput.current.value = "";
  };

  const reset = () => {
    setName("");
    setEmail("");
    setOrder("");
    setTopic("");
    setMessage("");
    setPhoto(null);
    setProblems({});
    setTicket(null);
    setAgain((a) => !a);
  };

  const error = (field: FieldName) =>
    problems[field] ? (
      <p id={`support-${field}-error`} className={page.error} data-error="">
        {copy(problems[field]!)}
      </p>
    ) : null;
  const described = (field: FieldName) => (problems[field] ? `support-${field}-error` : undefined);

  if (ticket) {
    const s = support.sent;
    return (
      <div className={page.sent} data-sent="" aria-live="polite">
        <span className={page.cup}>
          <Image className={`${base.ink} ${page.cupInk}`} src={cup.src} alt="" width={cup.width} height={cup.height} sizes="300px" />
          <Image
            className={page.steam}
            src={cup.steam.src}
            alt=""
            width={cup.steam.width}
            height={cup.steam.height}
            sizes="120px"
            data-steam=""
            data-sent-steam=""
            style={
              {
                left: `${(cup.steam.left * 100).toFixed(2)}%`,
                top: `${(cup.steam.top * 100).toFixed(2)}%`,
                width: `${(cup.steam.size * 100).toFixed(2)}%`,
              } as CSSProperties
            }
          />
        </span>
        <h3 id="sent-title" ref={sentTitle} tabIndex={-1} className={page.sentTitle}>
          {copy(s.title)}
        </h3>
        <p className={page.sentLabel}>{copy(s.ticket)}</p>
        <p className={page.ticket} data-ticket="">
          {ticket}
        </p>
        <p className={page.body}>{copy(s.reply)}</p>
        {SENDING_LIVE ? null : (
          <p className={page.previewLine} data-honesty="">
            {copy(s.preview)}
          </p>
        )}
        <button type="button" className={base.textLink} onClick={reset}>
          {copy(s.again)}
        </button>
      </div>
    );
  }

  return (
    <form className={page.form} onSubmit={send} noValidate data-support-form="">
      <div className={page.field}>
        <label htmlFor="support-name">{copy(w.name)}</label>
        <input
          ref={nameInput}
          id="support-name"
          name="name"
          autoComplete="name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          aria-invalid={problems.name ? true : undefined}
          aria-describedby={described("name")}
        />
        {error("name")}
      </div>
      <div className={page.field}>
        <label htmlFor="support-email">{copy(w.email)}</label>
        <input
          id="support-email"
          name="email"
          type="email"
          autoComplete="email"
          inputMode="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          aria-invalid={problems.email ? true : undefined}
          aria-describedby={described("email")}
        />
        {error("email")}
      </div>
      <div className={page.field}>
        <label htmlFor="support-order">{copy(w.order)}</label>
        <input id="support-order" name="order" value={order} onChange={(e) => setOrder(e.target.value)} />
      </div>
      <fieldset className={page.field} aria-describedby={described("topic")}>
        <legend>{copy(w.topic)}</legend>
        <div className={page.topics} data-topics="">
          {w.topics.map((t, i) => (
            <span key={t} className={page.topicChoice}>
              <input
                id={`support-topic-${i}`}
                type="radio"
                name="topic"
                value={t}
                checked={topic === t}
                onChange={() => setTopic(t)}
                aria-invalid={problems.topic ? true : undefined}
              />
              <label htmlFor={`support-topic-${i}`}>{copy(t)}</label>
            </span>
          ))}
        </div>
        {error("topic")}
      </fieldset>
      <div className={page.field}>
        <label htmlFor="support-message">{copy(w.message)}</label>
        <textarea
          id="support-message"
          name="message"
          rows={4}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          aria-invalid={problems.message ? true : undefined}
          aria-describedby={described("message")}
        />
        {error("message")}
      </div>
      <div className={page.field}>
        <input
          ref={photoInput}
          id="support-photo"
          className={base.visuallyHidden}
          type="file"
          accept="image/*"
          onChange={(e) => choosePhoto(e.target.files?.[0])}
          aria-describedby={described("photo")}
        />
        <label htmlFor="support-photo" className={base.textLink}>
          {copy(w.photo)}
        </label>
        {photo ? (
          <p className={page.photoName}>
            <span>{photo.name}</span>
            <button type="button" className={base.textLink} onClick={removePhoto}>
              {copy(w.removePhoto)}
            </button>
          </p>
        ) : null}
        {error("photo")}
      </div>
      <div className={page.sendRow}>
        <button type="submit" className={base.pill}>
          {copy(w.send)} <ArrowRight size={18} aria-hidden="true" />
        </button>
        {SENDING_LIVE ? null : (
          <span className={page.honesty} data-honesty="">
            {copy(w.preview)}
          </span>
        )}
      </div>
      <p className={page.note}>{copy(w.reaction)}</p>
    </form>
  );
}
```

The visually hidden file input still takes focus: its label is the visible target, and `.supportPage input[type=file]:focus-visible + label` draws the ring (Step 5).

- [ ] **Step 5: Style the form and the thank-you**

Append to `support-page.module.css`:

```css
/* ---- The form: writing lines on the paper, never boxes ------------------------------------- */

.supportPage .form {
  display: grid;
  gap: 28px;
  max-width: 640px;
  margin-top: clamp(28px, 2.8vw, 40px);
}

.supportPage .field {
  min-width: 0;
  margin: 0;
  padding: 0;
  border: 0;
}

.supportPage .field > label,
.supportPage .field > legend {
  display: block;
  padding: 0;
  color: var(--muted);
  font-size: 17px;
  font-weight: 450;
}

.supportPage .field input:not([type="radio"]):not([type="file"]),
.supportPage .field textarea {
  display: block;
  width: 100%;
  min-height: 48px;
  margin: 0;
  padding: 8px 0;
  border: 0;
  border-radius: 0;
  background: transparent;
  box-shadow: inset 0 -1px 0 var(--hair);
  color: var(--ink);
  font: inherit;
  font-size: 20px;
  transition: box-shadow 0.4s var(--ease);
}

.supportPage .field input:not([type="radio"]):not([type="file"]):focus,
.supportPage .field textarea:focus {
  outline: 0;
  box-shadow: inset 0 -2px 0 var(--ink);
}

.supportPage .field [aria-invalid="true"]:not([type="radio"]) {
  box-shadow: inset 0 -2px 0 var(--ink);
}

/* The message on ruled lines (40px apart), growing as it fills. */
.supportPage .field textarea {
  min-height: 160px;
  padding: 6px 0 0;
  border: 0;
  box-shadow: none;
  background: repeating-linear-gradient(to bottom, transparent 0 39px, var(--hair) 39px 40px);
  line-height: 40px;
  resize: none;
  field-sizing: content;
}

.supportPage .field textarea:focus {
  box-shadow: none;
  background: repeating-linear-gradient(to bottom, transparent 0 39px, var(--ink) 39px 40px);
}

/* What it's about: the kit's filter chips (outlined pills, 48px), three and two from 600px; a
   column of full-width rows on a phone, so none stands alone on a row. */
.supportPage .topics {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  max-width: 560px;
  margin-top: 12px;
}

.supportPage .topicChoice {
  position: relative;
  display: inline-flex;
}

.supportPage .topicChoice input {
  position: absolute;
  inset: 0;
  opacity: 0;
  margin: 0;
}

.supportPage .topicChoice label {
  display: inline-flex;
  align-items: center;
  min-height: 48px;
  padding: 0 18px;
  border: 1px solid var(--hair);
  border-radius: 999px;
  font-size: 18px;
  font-weight: 450;
  cursor: pointer;
  transition:
    background-color 0.4s var(--ease),
    color 0.4s var(--ease),
    border-color 0.4s var(--ease);
}

.supportPage .topicChoice label:hover {
  border-color: var(--ink);
}

.supportPage .topicChoice input:checked + label {
  background: var(--ink);
  border-color: var(--ink);
  color: var(--paper);
}

.supportPage .topicChoice input:focus-visible + label,
.supportPage input[type="file"]:focus-visible + label {
  outline: 2px solid var(--ink);
  outline-offset: 4px;
}

@media (max-width: 599px) {
  .supportPage .topics {
    flex-direction: column;
  }

  .supportPage .topicChoice,
  .supportPage .topicChoice label {
    width: 100%;
  }
}

.supportPage p.error {
  margin: 8px 0 0;
  color: var(--ink);
  font-size: 17px;
  font-weight: 500;
}

.supportPage p.photoName {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px 18px;
  margin: 4px 0 0;
  font-size: 17px;
}

.supportPage .sendRow {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 14px 18px;
}

/* The honesty tag (DESIGN.md honesty-tag: caption type, Ink Grey, an outlined pill, 30px). */
.supportPage .honesty {
  display: inline-flex;
  align-items: center;
  min-height: 30px;
  padding: 0 12px;
  border: 1px solid var(--hair);
  border-radius: 999px;
  color: var(--muted);
  font-size: 15px;
  font-weight: 450;
}

.supportPage p.note {
  max-width: 34em;
  margin: 0;
  color: var(--muted);
  font-size: 16px;
  line-height: 1.5;
}

/* ---- The moment: the cup, its steam rising again, the ticket number ----------------------- */

.supportPage .sent {
  display: grid;
  justify-items: center;
  max-width: 640px;
  margin-top: clamp(20px, 2vw, 32px);
  text-align: center;
}

.supportPage .cup {
  position: relative;
  display: block;
  width: min(300px, 70%);
}

.supportPage .cup img {
  display: block;
  width: 100%;
  height: auto;
}

.supportPage .cup img.steam {
  position: absolute;
  max-width: none;
}

.supportPage h3.sentTitle {
  margin: 6px 0 0;
  font-family: var(--display-font);
  font-weight: var(--display-weight);
  font-size: clamp(32px, 2.8vw, 44px);
  line-height: 1.1;
}

.supportPage h3.sentTitle:focus-visible {
  outline-offset: 6px;
}

.supportPage p.sentLabel {
  margin: 14px 0 0;
  color: var(--muted);
  font-size: 19px;
}

/* The number in Switzer (never Ysabeau's old-style digits), large, letter by letter clear. */
.supportPage p.ticket {
  margin: 4px 0 0;
  font-family: var(--sans);
  font-size: clamp(32px, 2.8vw, 42px);
  font-weight: 500;
  letter-spacing: 0.01em;
  font-variant-numeric: lining-nums tabular-nums;
}

.supportPage .sent p.body {
  margin-inline: auto;
}

.supportPage p.previewLine {
  max-width: 32em;
  margin: 18px 0 6px;
  padding: 10px 16px;
  border: 1px solid var(--hair);
  border-radius: 22px;
  color: var(--muted);
  font-size: 16px;
  line-height: 1.5;
}

@media (prefers-reduced-motion: no-preference) {
  .supportPage .sent .cupInk {
    animation: cup-in var(--breath) var(--ease) both;
  }

  .supportPage .sent [data-sent-steam] {
    animation: steam-rise var(--breath) var(--ease) 0.9s both;
  }

  .supportPage .sent > :not(.cup) {
    animation: words-in 0.9s var(--ease) 0.4s both;
  }
}

@keyframes cup-in {
  from {
    opacity: 0;
    filter: blur(5px);
  }
}

@keyframes words-in {
  from {
    opacity: 0;
    translate: 0 8px;
  }
}
```

Two rules the implementer must hold to:

- `.sent [data-sent-steam]` starts at `--rise: 0%` only under motion. The opening's rule (`@media (prefers-reduced-motion: no-preference) and (scripting: enabled) { .supportPage [data-steam] { --rise: 0% } }`) already sets that for every `[data-steam]`, and the sent steam's own animation (`both`) takes it to 112%. Under reduced motion `--rise` stays at its initial 112% (whole).
- `.cupInk` animates `opacity` and `filter` on the img itself (not on a wrapper), so its multiply is kept for the rest of the page. Confirm with the QA that nothing between the cup and the root makes a stacking context, and look at it.

In `support-ink.tsx`, render the form inside `Write`:

```tsx
import { SupportForm } from "./support-form";
...
          <Write>
            <SupportForm />
          </Write>
```

- [ ] **Step 6: Run the QA**

Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-support/scripts/qa/qa_support.py http://localhost:3050`
Expected: all groups PASS. Then type-check and lint as in Task 2 Step 10.

- [ ] **Step 7: Look at it**

Open `sent-1440.png`, `sent-390.png` and `sent-360.png`, plus a fresh screenshot of the empty form at 1440 and 390 and of the form with all four messages showing. Compare with `reference/ink-pages/mockups/support/a-desk.jpg` and `a-sent-desk.jpg`. The form must read as lines on paper (no boxes), the chips 3 + 2 on a desktop and full-width rows on a phone, the honesty tag quiet beside Send, the thank-you calm and centred with the steam over the cup. Score honestly; under 8, fix and look again.

- [ ] **Step 8: Commit**

```bash
git -C C:/Users/mcbig/Documents/codes/bigh-support add src/components/support scripts/qa/qa_support.py
git -C C:/Users/mcbig/Documents/codes/bigh-support commit -m "feat(support): the message form and its moment, a preview that sends nothing yet" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: Every Support link leads here; the pop-up goes

**Files:**
- Modify: `src/components/ink/nav/nav-inscription.tsx` (lines 246-255, 435-437, 567-569; and `useSiteDialogs` if it becomes unused there)
- Modify: `src/components/ink/chrome.tsx:203-205` (and the `useSiteDialogs` import if unused)
- Modify: `src/components/ink/dialogs.tsx` (remove `openSupport`, lines 24 and 241-285, and any styles only it used in `dialogs.module.css`, e.g. `.faq`/`.toggle` if no other sheet uses them: check with grep first)
- Modify: `src/components/science/site-chrome.tsx` (lines 41-55, 108-117, 136-150, 160-170)
- Modify: `src/components/science/science-page.tsx` (lines 13, 38, 43, 99-129)
- Modify: `scripts/qa/qa_nav.py:1356-1360, 1724-1728`
- Modify: `scripts/qa/qa_home_ink.py:1744-1757, 2040-2047, 2082-2099`
- Modify: `scripts/qa/qa_about.py:713-717`
- Modify: `scripts/qa/home_snapshot.py:115-150` (`NAV_STATE_JS` and `nav_check`'s expectations)
- Modify: `scripts/qa/qa_support.py`

**Interfaces:**
- Consumes: `NavCurrent` with `"support"` (Task 2); `/support` exists (Task 2).
- Produces: `useSiteDialogs()` without `openSupport` (`openProduct`, `openScientist`, `openAsk`, `openArticle` stay). `ScienceHeader`/`ScienceFooter` without the `onSupport` prop.

- [ ] **Step 1: Write the failing QA group**

Append to `qa_support.py`, set `GROUPS = [opening, motion, rhythm, questions, form, links, languages]`:

```python
def links(browser):
    # Desktop: from the foot of /about, the bar's Support goes to the top of /support, marked.
    context, page, *_ = open_page(browser, 1440, 900, path="/about")
    page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
    page.wait_for_timeout(800)
    page.locator("#site-navigation a", has_text="Support").click()
    page.wait_for_url("**/support", timeout=30000)
    page.wait_for_timeout(1500)
    check("links: the bar's Support goes to /support", page.url.endswith("/support"), page.url)
    check("links: it lands at the top", page.evaluate("window.scrollY") < 4, page.evaluate("window.scrollY"))
    current = page.evaluate("[...document.querySelectorAll('#site-navigation [aria-current=page]')].map(a => a.textContent.trim())")
    check("links: the bar marks Support as the current page", current == ["Support"], current)
    check("links: no Support pop-up opened", not page.evaluate("!!document.querySelector('dialog[open]')"))
    # The footer's Support & FAQs.
    page.goto(f"{BASE}/", wait_until="networkidle")
    page.locator("footer a", has_text="Support & FAQs").click()
    page.wait_for_url("**/support", timeout=30000)
    check("links: the footer's Support & FAQs goes to /support", page.url.endswith("/support"), page.url)
    # The Science page's own header.
    page.goto(f"{BASE}/science", wait_until="networkidle")
    page.locator("header a", has_text="Support").first.click()
    page.wait_for_url("**/support", timeout=30000)
    check("links: the Science page's Support goes to /support", page.url.endswith("/support"), page.url)
    context.close()
    # Phone: the menu's Support.
    context, page, *_ = open_page(browser, 390, 844, path="/")
    page.click("[data-nav-menu-button]")
    page.wait_for_timeout(900)
    page.locator("[data-nav-sheet] a", has_text="Support").click()
    page.wait_for_url("**/support", timeout=30000)
    page.wait_for_timeout(900)
    check("links: the phone menu's Support goes to /support", page.url.endswith("/support"), page.url)
    check("links: the menu closed behind it", page.evaluate("document.querySelector('[data-nav-menu-button]').getAttribute('aria-expanded')") != "true")
    context.close()


def languages(browser):
    for lang in ("kr", "jp", "cns", "vn"):
        tag = f"languages {lang}"
        context, page, response, errors, _ = open_page(browser, 390, 844, path=f"/{lang}/support")
        check(f"{tag}: 200", response and response.status == 200, response and response.status)
        check(f"{tag}: the page's words in English", page.evaluate("document.querySelector('h1').textContent.trim()") == "How can we help?")
        sideways = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
        check(f"{tag}: nothing scrolls sideways", sideways <= 0, sideways)
        check(f"{tag}: no errors", not errors, errors[:3])
        context.close()
    context, page, *_ = open_page(browser, 390, 844, path="/hken/support")
    check("languages: /hken/support goes to /cns/support", page.url.endswith("/cns/support"), page.url)
    context.close()
```

- [ ] **Step 2: Run it to see it fail**

Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-support/scripts/qa/qa_support.py http://localhost:3050 --only=links`
Expected: FAIL (the bar's Support is a button: no `a` to click; timeout).

- [ ] **Step 3: The menu bar**

In `nav-inscription.tsx`, delete `openSupport` (lines 246-255). Replace the desktop button (lines 435-437) with:

```tsx
            <Link
              href="/support"
              className={styles.link}
              aria-current={current === "support" ? "page" : undefined}
              data-ink={inked("support")}
            >
              <span className={styles.word}>
                {copy("Support")}
                <Ink />
              </span>
            </Link>
```

and the phone sheet's button (lines 567-569) with:

```tsx
          <Link
            href="/support"
            className={styles.sheetLink}
            aria-current={current === "support" ? "page" : undefined}
            onClick={() => setMenuOpen(false)}
          >
            {copy("Support")}
          </Link>
```

If `dialogs` (from `useSiteDialogs()`) and `menuButton` are now unused in this file, remove them (and the import) so lint stays clean; check with grep before removing. Keep the comment block above the old function out of the file (it described the pop-up's focus hand-back).

- [ ] **Step 4: The footer**

In `src/components/ink/chrome.tsx`, replace lines 203-205 with:

```tsx
            <Link href="/support">{copy("Support & FAQs")}</Link>
```

Remove `const dialogs = useSiteDialogs();` and the import if nothing else in the file uses them.

- [ ] **Step 5: Remove the pop-up**

In `src/components/ink/dialogs.tsx`: delete `openSupport: () => void;` from `type Dialogs` and the whole `openSupport() { ... }` member. Update the file's header comment that lists the sheets (drop "support"). Grep `dialogs.module.css` for classes only the support sheet used (`.faq`, `.toggle`, `name="home-support"` styling); remove those only if `grep -rn "styles.faq\|styles.toggle" src/components/ink` finds no other user.

- [ ] **Step 6: The Science page's own chrome**

In `src/components/science/site-chrome.tsx`: drop the `onSupport` prop from both components' parameter lists and types; replace the header's Support button with `<Link href="/support" onClick={close}>{copy("Support")}</Link>` and the footer's with `<Link href="/support">{copy("Support & FAQs")}</Link>`. In `science-page.tsx`: `type Panel = "story" | null;`, stop passing `onSupport`, and delete the `panel === "support"` block (lines 99-129). Leave the Science chrome's other links (including its `"/#about"` links) as they are: out of scope, and the Science ink session may replace this chrome.

- [ ] **Step 7: Update the checks that expected the pop-up**

- `qa_nav.py` 1356-1360: click `page.locator("#site-navigation a", has_text="Support")`, wait for `**/support`, check `"desk: Support goes to its page"` with `page.url.endswith("/support")`, then `page.go_back()` and wait 1200ms before the scroll that follows. 1724-1728: click `page.locator("[data-nav-sheet] a", has_text="Support")`, wait for `**/support`, check `"phone: Support goes to its page"`, `page.go_back()`, wait 900ms; the following `btn.click()` reopens the menu as before.
- `qa_home_ink.py`: remove the two `Support (...)` rows from `SHEETS` (1744-1757) and the `SUPPORT` constant; replace the menu block at 2040-2047 with a check that the menu's Support link has `href` ending `/support` (`page.evaluate("document.querySelector('[data-nav-sheet] a[href$=\"/support\"]') !== null")`), and change the Korean block at 2082-2099 to check the menu's four words (`len(links) == 4`, every link inside 390px and 48px+, `"고객" in links[3][0]`) without opening a sheet.
- `qa_about.py` 713-717: replace the click and `Support sheet opens` with `check(f"{tag} Support links to its page", page.evaluate("[...document.querySelectorAll('a')].some(a => a.textContent.trim() === 'Support' && a.getAttribute('href').endsWith('/support'))"))`.
- `home_snapshot.py`: `NAV_STATE_JS`'s `about` stays; add `support: [...nav.querySelectorAll('a')].find(a => a.textContent.trim() === 'Support')?.getAttribute('href') ?? null,` and expect `"support": "/support"` in every page's expectation dict in `nav_check` (add a `/support` entry: `{"page": "support", "words": words, "current": ["Support"], "menuCurrent": ["Support"], "mark": "/", "triggers": ["products", "science"], "about": "/about", "support": "/support"}`).

Read each block before editing; keep the scripts' own style.

- [ ] **Step 8: Run every affected check**

Run, each against the dev server (http://localhost:3050):
- `python -X utf8 scripts/qa/qa_support.py http://localhost:3050` → all PASS
- `python -X utf8 scripts/qa/qa_nav.py http://localhost:3050` → all PASS
- `python -X utf8 scripts/qa/qa_home_ink.py http://localhost:3050` → all PASS
- `python -X utf8 scripts/qa/qa_about.py http://localhost:3050` → all PASS
- `python -X utf8 scripts/qa/home_snapshot.py nav http://localhost:3050` → PASS
- `python -X utf8 scripts/qa/home_snapshot.py compare http://localhost:3050 after-links baseline-support` → PASS (the homepage is pixel-identical: links and buttons share the footer's and the bar's styles)

(Full paths: `C:/Users/mcbig/Documents/codes/bigh-support/scripts/qa/...`.) If a pre-existing check fails that has nothing to do with Support, report it with its output instead of changing it.

Then `npm --prefix C:/Users/mcbig/Documents/codes/bigh-support run type-check`, `npx --prefix C:/Users/mcbig/Documents/codes/bigh-support eslint src`, `npx --prefix C:/Users/mcbig/Documents/codes/bigh-support prettier --check src scripts/qa docs/superpowers reference/ink-pages/support` → clean (prettier may not cover .py; that is fine).

- [ ] **Step 9: Commit**

```bash
git -C C:/Users/mcbig/Documents/codes/bigh-support add src scripts/qa
git -C C:/Users/mcbig/Documents/codes/bigh-support commit -m "feat(support): every Support link leads to the page; the pop-up goes" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 6: The built site, a visitor's look, and the hand-off

**Files:**
- Create: `docs/support-page.md`
- Modify: `C:\Users\mcbig\.claude\projects\C--Users-mcbig-Documents-codes-bigh-website\memory\project_support_page.md` (outside the repo)

**Interfaces:**
- Consumes: everything above.
- Produces: a built site on :3051 that passes every check; screenshots for Mo; a short doc.

- [ ] **Step 1: Build and start the built site**

Run: `npm --prefix C:/Users/mcbig/Documents/codes/bigh-support run build`
Expected: the build succeeds and lists `/[locale]/support`. Then `preview_start {name: "bigh-support-prod"}`.

- [ ] **Step 2: Run every check on the built site**

The built site orders CSS differently from dev: run the same commands as Task 5 Step 8 against `http://localhost:3051`, with the pixel compare against the built baseline from Task 2 Step 1: `home_snapshot.py compare http://localhost:3051 after-links-prod baseline-support-prod`.
Expected: all PASS.

- [ ] **Step 3: Look like a visitor**

At 1440x900 and 390x844 (and 1024x768, 768x1024), on the built site: scroll the page slowly from top to foot, taking viewport screenshots (never full-page), open a question, fill the form badly then well, send, write another. Open every screenshot with Read at full size. Look for what a visitor would call broken: a painting with a box edge, a word alone on a line in a title, a chip alone, uneven gaps between parts, the steam not over the cup, anything that "looks on purpose" but reads as a mistake. Score each screen out of 10; the bar is 8 (the homepage's is 9). Fix and repeat until it holds.

- [ ] **Step 4: Write the doc**

Create `docs/support-page.md` (LF), one page: what the page is (mockup A, the porch), where its parts live (route, components, art build script, QA script, ports 3050/3051), the preview switch (`SENDING_LIVE`) and what real sending will need (Resend through Vercel, the GoDaddy DNS records, a server route that mails support@bighnow.com with the customer as reply-to, a ticket number the service issues, spam guards), English only (no copy keys yet; translations later through a `translations-support.cjs` like `reference/ink-pages/about-bc/translations-c.cjs`, starting at the next free key, m612 on October 14), and the checks to run.

- [ ] **Step 5: Commit**

```bash
git -C C:/Users/mcbig/Documents/codes/bigh-support add docs/support-page.md
git -C C:/Users/mcbig/Documents/codes/bigh-support commit -m "docs(support): how the Support page is built and what real sending will need" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

- [ ] **Step 6: Show Mo, ask before any push**

Publish the screenshots (desktop and phone: opening, form, thank-you, returns, questions) on the session's comparison artifact (the same file path as the mockups page, so its link stays), with the mockup beside each. Tell Mo plainly what was checked and what was not. Ask one question: push the branch for a Vercel preview link (yes/no). Do not push, merge or alias without that yes. Update the memory note with the branch head and the state.

If Mo says yes: other sessions push to `main` within minutes, so first `git -C C:/Users/mcbig/Documents/codes/bigh-support fetch origin` and `git -C C:/Users/mcbig/Documents/codes/bigh-support merge origin/main` (resolve the shared menu bar, footer and Science chrome by hand, keeping both sides' intent), re-run Task 5 Step 8's checks on the dev server, and only then push the branch (never `main`).

# Ink Kit and About Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move the homepage's Ink & Gold pieces into a shared kit without changing the homepage, then rebuild the About page on that kit in the approved ink mockup's look.

**Architecture:** The shared pieces (paper and tokens, pills, stations, bloom and gold light, brush line, site header and footer, sheets, motion hooks) move from `src/components/home-v2/` into `src/components/ink/`, unchanged except for names and two new props (the brush line's `route`, the header's `current`). A new `InkPage` shell wraps any page in the kit. The homepage is guarded by pixel snapshots taken before the move. About becomes an `InkPage` with its own sections and brush route, reusing the homepage's existing paintings (no new pictures in this plan).

**Tech Stack:** Next.js 16 (App Router, Turbopack), React, TypeScript, CSS Modules, next-intl (`useCopy`), Lenis smooth scroll, Playwright for Python (QA), Pillow and NumPy (snapshot compare).

**Spec:** `docs/superpowers/specs/2026-10-05-ink-pages-design.md` (stage 0 and stage 1). Reference pictures: `reference/ink-pages/mockups/about.jpg`. Design system: `DESIGN.md`.

## Global Constraints

- Read `AGENTS.md` first. This Next.js has breaking changes: check `node_modules/next/dist/docs/` before using any Next API you have not seen in this repo.
- The homepage must look and behave the same after every task: `scripts/qa/home_snapshot.py compare` passes and `scripts/qa/qa_home_ink.py` passes in full, on dev and on `next start`.
- DESIGN.md rules apply unchanged: One Gold Leaf (gold only inside paintings), No Red No Seal, Sentence Case (no letter-spaced capitals), Multiply (every ink painting `mix-blend-mode: multiply`), no cards or boxed panels, the photo mount is the only shadow, text 15px or larger, navigation 18px or larger, targets 48px or taller, one breath `--breath: 2.4s` and ease `cubic-bezier(0.22, 0.61, 0.36, 1)`, reduced motion complete and still.
- Component CSS must be scoped under the kit's root class (`.look …`) or the page's own root class: `homepage.module.css` resets `.site p`, `.site button`, `.site h2` at specificity 0,1,1.
- About keeps every word in `src/components/about/about-content.ts` (locked by Mo, September 25, 2026). The h1 stays English "Be in Good Health." with `lang="en"` in every locale.
- Real assets only: Dr. Liu's photo `public/images/jiankang-liu.jpg` as it is; paintings are the homepage's existing files.
- Files are LF; this checkout has `core.autocrlf=true`. Never `git stash`. On Windows write files with LF (`newline="\n"` in Python). `npx prettier --write` restores LF.
- Bash: never `cd` in a command; use absolute paths or `git -C`. Worktree: `C:/Users/mcbig/Documents/codes/bigh-ink`, branch `ink-pages`, no upstream (do not push; Mo approves every push).
- Dev server: preview entry `bigh-ink` on port 3025; built site: `bigh-ink-prod` on port 3026 (Task 1 adds both).

## Review Focus

- A visitor opens `/about#promise` from a link: the page lands with the "What you can count on." heading below the header, not under it (test in Task 5).
- A late-loading face (Vietnamese) changes line lengths after the brush line was measured: each station's leader still meets the line (test in Task 7).
- The window is resized from desktop to tablet while the page is open: the page-long line is redrawn for one column and never runs through the words (test in Task 3 and Task 7, via `data-layout`).
- A keyboard user: the first Tab shows "Skip to content", Enter puts focus at the page's words; a sheet hands focus back to the button that opened it (test in Task 5).
- Pictures are slow or blocked: every heading and paragraph is still visible; nothing waits at `opacity: 0` for a picture (test in Task 5).

---

### Task 1: Worktree setup and the homepage snapshot guard

**Files:**

- Modify: `C:/Users/mcbig/Documents/codes/bigh-website/.claude/launch.json` (the main checkout's; the preview tool reads that one)
- Create: `scripts/qa/home_snapshot.py`

**Interfaces:**

- Produces: `python -X utf8 scripts/qa/home_snapshot.py capture <base-url> <name>` writes viewport PNGs to `scripts/qa/out/home-snapshots/<name>/`; `python -X utf8 scripts/qa/home_snapshot.py compare <base-url> <name> [against]` captures `<name>` and compares it with `against` (default `baseline`), exit code 0 only when every shot matches.

- [ ] **Step 1: Install dependencies in the worktree**

Run: `npm --prefix C:/Users/mcbig/Documents/codes/bigh-ink ci`
Expected: finishes with "added N packages", no errors.

- [ ] **Step 2: Add the two preview entries**

Add to the `configurations` array of `C:/Users/mcbig/Documents/codes/bigh-website/.claude/launch.json` (keep the others):

```json
{
  "name": "bigh-ink",
  "runtimeExecutable": "npm",
  "runtimeArgs": ["--prefix", "C:/Users/mcbig/Documents/codes/bigh-ink", "run", "dev", "--", "--hostname", "localhost", "--port", "3025"],
  "port": 3025
},
{
  "name": "bigh-ink-prod",
  "runtimeExecutable": "npm",
  "runtimeArgs": ["--prefix", "C:/Users/mcbig/Documents/codes/bigh-ink", "run", "start", "--", "--hostname", "localhost", "--port", "3026"],
  "port": 3026
}
```

Start `bigh-ink` with the preview tool (`preview_start {name: "bigh-ink"}`). If the preview tool refuses (server cap), start it from the shell in the background instead: `npm --prefix C:/Users/mcbig/Documents/codes/bigh-ink run dev -- --hostname localhost --port 3025` with `run_in_background`.
Expected: `curl -s -o /dev/null -w "%{http_code}" http://localhost:3025/` prints 200.

- [ ] **Step 3: Write the snapshot script**

Create `scripts/qa/home_snapshot.py`:

```python
"""Homepage snapshot guard for the ink kit (October 5, 2026).

The kit move must not change the homepage. This takes viewport shots of / with reduced motion (the
page is then complete and still: every painting shown, the whole brush line drawn, no mist, no
wingbeat), at four sizes, scrolling one window at a time (never full-page: svh layouts), and
compares them with a saved set.

usage:
  python -X utf8 scripts/qa/home_snapshot.py capture <base-url> <name>
  python -X utf8 scripts/qa/home_snapshot.py compare <base-url> <name> [against=baseline]
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path(__file__).resolve().parent / "out" / "home-snapshots"
SIZES = [(1536, 1000), (1280, 800), (900, 1100), (390, 844)]
# A shot matches when under 0.3% of its pixels differ by more than 24 levels (text antialiasing
# and the paper texture's sub-pixel placement move a few pixels between runs).
MAX_SHARE = 0.003
LEVEL = 24


def capture(base: str, name: str) -> Path:
    folder = OUT / name
    folder.mkdir(parents=True, exist_ok=True)
    for old in folder.glob("*.png"):
        old.unlink()
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--use-angle=d3d11"])
        for width, height in SIZES:
            context = browser.new_context(
                viewport={"width": width, "height": height},
                reduced_motion="reduce",
                device_scale_factor=1,
            )
            page = context.new_page()
            page.goto(f"{base}/", wait_until="networkidle", timeout=120000)
            page.evaluate("document.fonts.ready.then(() => true)")
            page.wait_for_timeout(1500)
            total = page.evaluate("document.documentElement.scrollHeight")
            y, index = 0, 0
            while y < total:
                page.evaluate(f"window.scrollTo(0, {y})")
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(600)
                page.screenshot(path=str(folder / f"{width}-{index:02d}.png"))
                y += height
                index += 1
                total = page.evaluate("document.documentElement.scrollHeight")
            context.close()
        browser.close()
    return folder


def compare(name: str, against: str) -> bool:
    new, old = OUT / name, OUT / against
    ok = True
    names = sorted({f.name for f in old.glob("*.png")} | {f.name for f in new.glob("*.png")})
    for file in names:
        a, b = old / file, new / file
        if not a.exists() or not b.exists():
            print(f"FAIL {file}: missing in {'baseline' if not a.exists() else name}")
            ok = False
            continue
        x = np.asarray(Image.open(a).convert("RGB"), dtype=np.int16)
        y = np.asarray(Image.open(b).convert("RGB"), dtype=np.int16)
        if x.shape != y.shape:
            print(f"FAIL {file}: size {x.shape} vs {y.shape}")
            ok = False
            continue
        share = float((np.abs(x - y).max(axis=2) > LEVEL).mean())
        status = "ok  " if share <= MAX_SHARE else "FAIL"
        ok &= share <= MAX_SHARE
        print(f"{status} {file}: {share * 100:.3f}% of pixels differ")
    return ok


if __name__ == "__main__":
    mode, base, name = sys.argv[1], sys.argv[2], sys.argv[3]
    capture(base, name)
    if mode == "compare":
        against = sys.argv[4] if len(sys.argv) > 4 else "baseline"
        passed = compare(name, against)
        print("PASS" if passed else "FAIL")
        sys.exit(0 if passed else 1)
```

- [ ] **Step 4: Prove the guard is steady before anything changes**

Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/scripts/qa/home_snapshot.py capture http://localhost:3025 baseline`
Then: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/scripts/qa/home_snapshot.py compare http://localhost:3025 rerun`
Expected: every line `ok`, last line `PASS` (the same code twice matches). If a shot fails on unchanged code, find what moves between runs (a late image, a timer) and make the script wait for it; do not raise `MAX_SHARE`.

- [ ] **Step 5: Baseline of the built site**

Run: `npm --prefix C:/Users/mcbig/Documents/codes/bigh-ink run build`, start `bigh-ink-prod`, then
`python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/scripts/qa/home_snapshot.py capture http://localhost:3026 baseline-prod`
Expected: build succeeds; shots written. Stop `bigh-ink-prod` afterwards.

- [ ] **Step 6: Commit**

```bash
git -C C:/Users/mcbig/Documents/codes/bigh-ink add scripts/qa/home_snapshot.py
git -C C:/Users/mcbig/Documents/codes/bigh-ink commit -m "test(home): snapshot guard for the ink kit move"
```

---

### Task 2: Move the shared pieces into `src/components/ink/` (homepage unchanged)

**Files:**

- Move (git mv, contents unchanged except import paths):
  - `src/components/home-v2/look-ink/look-ink.module.css` → `src/components/ink/ink.module.css`
  - `src/components/home-v2/look-ink/motion.ts` → `src/components/ink/motion.ts`
  - `src/components/home-v2/lock-scroll.ts` → `src/components/ink/lock-scroll.ts`
  - `src/components/home-v2/dialogs.tsx` → `src/components/ink/dialogs.tsx`
  - `src/components/home-v2/dialogs.module.css` → `src/components/ink/dialogs.module.css`
  - `src/components/home-v2/chrome.tsx` → `src/components/ink/chrome.tsx`
  - `src/components/home-v2/chrome.module.css` → `src/components/ink/chrome.module.css`
  - `src/components/home-v2/look-ink/closing-crane.tsx` → `src/components/ink/closing-crane.tsx`
  - `src/components/home-v2/look-ink/brush.tsx` → `src/components/ink/brush.tsx`
  - `src/components/home-v2/look-ink/brush.module.css` → `src/components/ink/brush.module.css`
- Modify: every importer (the script in Step 2 lists them), `src/app/[locale]/page.tsx`
- Create: `scripts/qa/rewrite_imports.py` (kept for the record; used once here)

**Interfaces:**

- Consumes: nothing new.
- Produces: the same exports as before, now at `@/components/ink/*`: `HomeHeader`, `HomeFooter`, `Sentences` (chrome), `HomeDialogs`, `useHomeDialogs` (dialogs), `useMotionOk`, `useInkFill`, `useArrival`, `useBloom` (motion), `lockPageScroll` (lock-scroll), `ClosingCrane`, `BrushLine` (signature unchanged in this task), and the class map `ink.module.css` (classes `look`, `wrap`, `pill`, `pillGhost`, `textLink`, `station`, `display`, `body`, `label`, `caption`, `ink`, `gold`, `rest`, `skip`, `visuallyHidden`).

- [ ] **Step 1: Move the files**

```bash
W=C:/Users/mcbig/Documents/codes/bigh-ink
mkdir -p $W/src/components/ink
git -C $W mv src/components/home-v2/look-ink/look-ink.module.css src/components/ink/ink.module.css
git -C $W mv src/components/home-v2/look-ink/motion.ts src/components/ink/motion.ts
git -C $W mv src/components/home-v2/lock-scroll.ts src/components/ink/lock-scroll.ts
git -C $W mv src/components/home-v2/dialogs.tsx src/components/ink/dialogs.tsx
git -C $W mv src/components/home-v2/dialogs.module.css src/components/ink/dialogs.module.css
git -C $W mv src/components/home-v2/chrome.tsx src/components/ink/chrome.tsx
git -C $W mv src/components/home-v2/chrome.module.css src/components/ink/chrome.module.css
git -C $W mv src/components/home-v2/look-ink/closing-crane.tsx src/components/ink/closing-crane.tsx
git -C $W mv src/components/home-v2/look-ink/brush.tsx src/components/ink/brush.tsx
git -C $W mv src/components/home-v2/look-ink/brush.module.css src/components/ink/brush.module.css
```

- [ ] **Step 2: Rewrite the import paths with a script (exact mapping, nothing else)**

Create `scripts/qa/rewrite_imports.py`:

```python
"""Rewrite import specifiers after the ink kit move (October 5, 2026). Exact strings only."""

import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) / "src"
INK = "@/components/ink"
RULES = {
    # files that stayed in home-v2/look-ink
    "components/home-v2/look-ink": {
        '"./look-ink.module.css"': f'"{INK}/ink.module.css"',
        '"./motion"': f'"{INK}/motion"',
        '"../chrome"': f'"{INK}/chrome"',
        '"../dialogs"': f'"{INK}/dialogs"',
        '"./brush"': f'"{INK}/brush"',
        '"./closing-crane"': f'"{INK}/closing-crane"',
    },
    # files that moved into ink/
    "components/ink": {
        '"./content"': '"@/components/home-v2/content"',
        '"./assets"': '"@/components/home-v2/look-ink/assets"',
        '"./look-ink.module.css"': '"./ink.module.css"',
        '"./brush-route"': '"@/components/home-v2/look-ink/brush-route"',
    },
    "app": {
        '"@/components/home-v2/dialogs"': f'"{INK}/dialogs"',
        '"@/components/home-v2/chrome"': f'"{INK}/chrome"',
    },
}

changed = []
for folder, mapping in RULES.items():
    for file in (ROOT / folder).rglob("*.ts*"):
        text = file.read_text(encoding="utf-8")
        new = text
        for old, replacement in mapping.items():
            new = new.replace(f"from {old}", f"from {replacement}")
        if new != text:
            file.write_text(new, encoding="utf-8", newline="\n")
            changed.append(str(file.relative_to(ROOT)))
print("\n".join(changed))
```

Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/scripts/qa/rewrite_imports.py C:/Users/mcbig/Documents/codes/bigh-ink`
Expected: it lists the changed files (the look-ink sections, `look-ink.tsx`, the moved chrome, dialogs, closing-crane and brush, `app/[locale]/page.tsx`).

- [ ] **Step 3: Find anything the mapping missed**

Run: `grep -rnE "from \"(\./|\.\./)(look-ink\.module\.css|motion|chrome|dialogs|brush|closing-crane|lock-scroll|content|assets|brush-route)\"" C:/Users/mcbig/Documents/codes/bigh-ink/src/components/ink C:/Users/mcbig/Documents/codes/bigh-ink/src/components/home-v2`
Expected: only imports that still resolve (inside `ink/`: `./dialogs`, `./lock-scroll`, `./chrome.module.css`, `./dialogs.module.css`, `./brush.module.css`, `./ink.module.css`; inside `home-v2/look-ink/`: `./assets`, `./brush-route`, `./mist`, its own `*.module.css`, `../content`). Fix any other by hand. Also check CSS `composes:` and relative `url()` in the moved CSS: `grep -n "composes\|url(\"\.\|url(\.\." C:/Users/mcbig/Documents/codes/bigh-ink/src/components/ink/*.css` must print nothing.

- [ ] **Step 4: Type check and lint**

Run: `npm --prefix C:/Users/mcbig/Documents/codes/bigh-ink run lint` and `npx --prefix C:/Users/mcbig/Documents/codes/bigh-ink tsc --noEmit -p C:/Users/mcbig/Documents/codes/bigh-ink/tsconfig.json`
Expected: both clean.

- [ ] **Step 5: The homepage is unchanged**

Run (dev server on 3025 picks up the change; restart it if it reports a missing module):
`python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/scripts/qa/home_snapshot.py compare http://localhost:3025 task2`
Expected: `PASS`.
Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/scripts/qa/qa_home_ink.py http://localhost:3025`
Expected: the same pass count as on main (276/276 on October 5); no new failures.

- [ ] **Step 6: The built homepage is unchanged**

Build, start `bigh-ink-prod`, run `home_snapshot.py compare http://localhost:3026 task2-prod baseline-prod` and `qa_home_ink.py http://localhost:3026`.
Expected: `PASS` and the full pass count. The built site orders CSS differently from dev: if only the built site differs, the moved CSS now loads in a different order; restore the order (import `ink.module.css` before the block modules in each section file, as `look-ink.module.css` was) rather than adding specificity.

- [ ] **Step 7: Commit**

```bash
git -C C:/Users/mcbig/Documents/codes/bigh-ink add -A src/components/ink src/components/home-v2 src/app scripts/qa/rewrite_imports.py
git -C C:/Users/mcbig/Documents/codes/bigh-ink commit -m "refactor(ink): move the homepage's shared ink pieces into components/ink"
```

---

### Task 3: The brush line takes its route; shared route helpers

**Files:**

- Create: `src/components/ink/route-kit.ts`
- Modify: `src/components/ink/brush.tsx` (props, publish `data-layout`), `src/components/home-v2/look-ink/brush-route.ts` (import the helpers instead of defining them), `src/components/home-v2/look-ink/look-ink.tsx` (pass the route)

**Interfaces:**

- Produces (in `route-kit.ts`, moved verbatim from `brush-route.ts`): `type Waypoint`, `type Layout = "phone" | "column" | "page"`, `on(at, fx, fy, w?, ink?, dx?, dy?)`, `station(id, side)`, `gap(after, at, fy, dx?, dy?, ink?)`, `fresh(point, load?)`, `lift(at, fx, fy)`, `rule(at): Waypoint[]`, and `footerEnding: Waypoint[]` (the former `promise` constant under the footer's promise, anchor `footer-promise`). All exported.
- Produces: `BrushLine({ motion, route }: { motion: boolean; route: (layout: Layout) => Waypoint[] })`. The host element publishes `data-layout` = the current layout.
- The homepage's `route` stays in `home-v2/look-ink/brush-route.ts` with the same name and output.

- [ ] **Step 1: Write the failing check**

Add to the end of `scripts/qa/home_snapshot.py` a mode `layout` (so the guard file holds the homepage's checks of this move):

```python
def layout_check(base: str) -> bool:
    """The brush layer says which layout it drew, and redraws when the window crosses 900px."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(f"{base}/", wait_until="networkidle", timeout=120000)
        page.wait_for_timeout(800)
        first = page.evaluate("document.querySelector('[data-lifts]')?.dataset.layout ?? null")
        page.set_viewport_size({"width": 800, "height": 900})
        page.wait_for_timeout(1200)
        second = page.evaluate("document.querySelector('[data-lifts]')?.dataset.layout ?? null")
        browser.close()
    ok = first == "page" and second == "column"
    print(f"{'ok  ' if ok else 'FAIL'} layout: {first} at 1440, {second} at 800")
    return ok
```

and in `__main__`, before the capture line, add:

```python
    if mode == "layout":
        sys.exit(0 if layout_check(base) else 1)
```

(`name` is still read from `sys.argv[3]`; pass `-` for it in this mode.)

Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/scripts/qa/home_snapshot.py layout http://localhost:3025 -`
Expected: FAIL (`data-layout` does not exist yet: `None at 1440`).

- [ ] **Step 2: Create `route-kit.ts`**

Cut these definitions out of `src/components/home-v2/look-ink/brush-route.ts` and paste them, with their comments, into `src/components/ink/route-kit.ts`, adding `export` to each: the `Waypoint` type, the `Layout` type, `on`, `station`, `gap`, `fresh`, `lift`, `rule`, and the `promise` array (rename it `footerEnding`, together with its `const T = "footer-promise"`). Start the file with:

```ts
// The brush line's route helpers, shared by every ink page (moved from the homepage's
// brush-route.ts, October 5, 2026). A route is a list of waypoints pinned to the page's own
// [data-brush] anchors; each page writes its own route from these.
```

- [ ] **Step 3: The homepage's route imports them**

At the top of `brush-route.ts` add:

```ts
import {
  footerEnding,
  fresh,
  gap,
  lift,
  on,
  rule,
  station,
  type Layout,
  type Waypoint,
} from "@/components/ink/route-kit";

export type { Layout, Waypoint };
```

Replace every use of `promise` in `route()` with `footerEnding`. Nothing else in `route()` changes.

- [ ] **Step 4: `BrushLine` takes the route**

In `src/components/ink/brush.tsx`:

- change the import `import { route, type Layout, type Waypoint } from "@/components/home-v2/look-ink/brush-route";` to `import type { Layout, Waypoint } from "./route-kit";`
- change the signature to:

```tsx
export function BrushLine({
  motion,
  route,
}: {
  motion: boolean;
  /** The page's route for each layout (the page's own [data-brush] anchors). */
  route: (layout: Layout) => Waypoint[];
}) {
```

- inside `layout()`, right after `host.dataset.lifts = JSON.stringify(lifts(samples));` add `host.dataset.layout = layout;`
- add `route` to the dependency array of the effect that defines `layout()` (it was `[motion]`; it becomes `[motion, route]`).

In `src/components/home-v2/look-ink/look-ink.tsx` import `{ route } from "./brush-route"` and render `<BrushLine motion={motion} route={route} />`.

- [ ] **Step 5: Run the checks**

Run: `python -X utf8 …/home_snapshot.py layout http://localhost:3025 -` → Expected: `ok   layout: page at 1440, column at 800`.
Run: `python -X utf8 …/home_snapshot.py compare http://localhost:3025 task3` → Expected: `PASS`.
Run: `python -X utf8 …/qa_home_ink.py http://localhost:3025` → Expected: full pass count (its line checks read `data-lifts`, which is unchanged).
Run lint and `tsc --noEmit` → clean.

- [ ] **Step 6: Commit**

```bash
git -C C:/Users/mcbig/Documents/codes/bigh-ink add -A src/components/ink src/components/home-v2 scripts/qa/home_snapshot.py
git -C C:/Users/mcbig/Documents/codes/bigh-ink commit -m "refactor(ink): the brush line takes its route; shared route helpers"
```

---

### Task 4: `InkPage` shell, one site header and footer for every page

**Files:**

- Create: `src/components/ink/ink-page.tsx`
- Modify: `src/components/ink/chrome.tsx` (rename to `SiteHeader` / `SiteFooter`, add `current`), `src/components/ink/dialogs.tsx` (rename to `SiteDialogs` / `useSiteDialogs`), every importer of the old names, `src/components/home-v2/look-ink/look-ink.tsx` (use `InkPage`)

**Interfaces:**

- Produces: `type Current = "home" | "products" | "science" | "about"` (exported from `chrome.tsx`).
- Produces: `SiteHeader({ current, overlay?, tone?, solidAfter? })` — `HomeHeader`'s props plus `current: Current`. On `current === "home"` the Products link is the in-page `<a href="#products">` as today; elsewhere `<Link href="/#products">`. The link of the current page carries `aria-current="page"`.
- Produces: `SiteFooter({ closing? })` — `HomeFooter` renamed, unchanged.
- Produces: `SiteDialogs({ children, articleImages? })` and `useSiteDialogs()` — renamed, unchanged.
- Produces: `InkPage({ current, route, children }: { current: Current; route: (layout: Layout) => Waypoint[]; children: (motion: boolean) => ReactNode })` — renders the kit root (`<div className={ink.look} data-look="ink" data-page={current}>`), the skip link, `SiteHeader current={current} overlay solidAfter={48}`, `<main id="main" tabIndex={-1}>`, `SiteFooter closing={<ClosingCrane />}`, `BrushLine`; runs `useSmoothScroll`, `useBloom`, `useInkFill`. Must be rendered inside `SiteDialogs` (and `ProductPagesProvider` for product links).

- [ ] **Step 1: Write the failing check**

Add to `home_snapshot.py` a mode `nav`:

```python
def nav_check(base: str) -> bool:
    """One header for every ink page: the homepage marks Home as the current page and keeps its
    in-page Products link; the root carries data-page."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(f"{base}/", wait_until="networkidle", timeout=120000)
        state = page.evaluate(
            """() => {
              const nav = document.querySelector('#home-navigation');
              const current = [...nav.querySelectorAll('[aria-current="page"]')].map(a => a.textContent.trim());
              const products = [...nav.querySelectorAll('a')].find(a => a.textContent.trim() === 'Products');
              return { current, products: products?.getAttribute('href'),
                       page: document.querySelector('[data-look="ink"]')?.dataset.page ?? null };
            }"""
        )
        browser.close()
    ok = state == {"current": ["Home"], "products": "#products", "page": "home"}
    print(f"{'ok  ' if ok else 'FAIL'} nav: {state}")
    return ok
```

and in `__main__`: `if mode == "nav": sys.exit(0 if nav_check(base) else 1)`.

Run: `python -X utf8 …/home_snapshot.py nav http://localhost:3025 -`
Expected: FAIL (`page: None`).

- [ ] **Step 2: Rename across the code**

Run this once (exact identifiers, word boundaries):

```bash
W=C:/Users/mcbig/Documents/codes/bigh-ink
grep -rlE "\b(HomeHeader|HomeFooter|HomeDialogs|useHomeDialogs)\b" $W/src | while read f; do
  python -X utf8 -c "
import re,sys
p=sys.argv[1]; s=open(p,encoding='utf-8').read()
for a,b in [('useHomeDialogs','useSiteDialogs'),('HomeDialogs','SiteDialogs'),('HomeHeader','SiteHeader'),('HomeFooter','SiteFooter')]:
    s=re.sub(r'\b'+a+r'\b',b,s)
open(p,'w',encoding='utf-8',newline='\n').write(s)" "$f"
done
```

Also update the error text in `useSiteDialogs` to `"useSiteDialogs needs <SiteDialogs>"`.

- [ ] **Step 3: `current` in the header**

In `chrome.tsx` add above `SiteHeader`:

```tsx
/** Which page the header is on: its link is marked as the current page. */
export type Current = "home" | "products" | "science" | "about";
```

Add `current: Current;` (documented "The page this header is on.") to `SiteHeader`'s props and destructure it. Replace the four page links in the `<nav>` with:

```tsx
<Link href="/" aria-current={current === "home" ? "page" : undefined} onClick={close}>
  {copy("Home")}
</Link>
{current === "home" ? (
  <a href="#products" onClick={close}>
    {copy("Products")}
  </a>
) : (
  <Link
    href="/#products"
    aria-current={current === "products" ? "page" : undefined}
    onClick={close}
  >
    {copy("Products")}
  </Link>
)}
<Link href="/science" aria-current={current === "science" ? "page" : undefined} onClick={close}>
  {copy("Science")}
</Link>
<Link href="/about" aria-current={current === "about" ? "page" : undefined} onClick={close}>
  {copy("About")}
</Link>
```

Update the file's opening comment: "Header and footer for every ink page (the homepage first, October 2; shared October 5, 2026)."

- [ ] **Step 4: Create `ink-page.tsx`**

```tsx
"use client";

import { useRef, type ReactNode } from "react";
import { useSmoothScroll } from "@/components/science/smooth-scroll";
import { useCopy } from "@/i18n/use-copy";
import { BrushLine } from "./brush";
import { SiteFooter, SiteHeader, type Current } from "./chrome";
import { ClosingCrane } from "./closing-crane";
import { useBloom, useInkFill, useMotionOk } from "./motion";
import type { Layout, Waypoint } from "./route-kit";
import styles from "./ink.module.css";

// Any page in the Ink & Gold look (October 5, 2026): rice paper, the site header (clear over the
// opening, paper once scrolled), the page's sections, the footer that closes on the crane at
// rest, and the page's own brush line drawing itself down the page. Paintings marked
// [data-bloom] bloom as they enter; outlined pills fill like ink in water. Reduced motion: a
// complete still page with the whole line. Keyboard: the first Tab shows "Skip to content".
// Render it inside <SiteDialogs> (and <ProductPagesProvider> where products link to pages).
export function InkPage({
  current,
  route,
  children,
}: {
  current: Current;
  /** The page's brush route for each layout. */
  route: (layout: Layout) => Waypoint[];
  /** The page's sections; given whether motion is allowed. */
  children: (motion: boolean) => ReactNode;
}) {
  const copy = useCopy();
  const root = useRef<HTMLDivElement>(null);
  const main = useRef<HTMLElement>(null);
  const motion = useMotionOk();
  useSmoothScroll(motion);
  useBloom(root, motion);
  useInkFill(root);

  return (
    <div ref={root} className={styles.look} data-look="ink" data-page={current}>
      <a
        href="#main"
        className={styles.skip}
        onClick={(event) => {
          // Focus moves by hand: the page's smooth scrolling takes over links to #anchors.
          event.preventDefault();
          window.scrollTo(0, 0);
          main.current?.focus({ preventScroll: true });
        }}
      >
        {copy("Skip to content")}
      </a>
      <SiteHeader current={current} overlay solidAfter={48} />
      <main ref={main} id="main" tabIndex={-1}>
        {children(motion)}
      </main>
      <SiteFooter closing={<ClosingCrane />} />
      <BrushLine motion={motion} route={route} />
    </div>
  );
}
```

- [ ] **Step 5: The homepage uses it**

Replace the body of `LookInk` in `src/components/home-v2/look-ink/look-ink.tsx` (keep its comment block) with:

```tsx
export function LookInk() {
  return (
    <InkPage current="home" route={route}>
      {(motion) => (
        <>
          <OpeningCrane motion={motion} />
          <Cellular />
          <Scientists />
          <Products />
          <Stories />
          <Science />
          <Research />
          <Purpose />
        </>
      )}
    </InkPage>
  );
}
```

with imports `InkPage` from `@/components/ink/ink-page`, `route` from `./brush-route` and the section components; remove the now unused imports (`useRef`, `useSmoothScroll`, `useCopy`, chrome, `BrushLine`, `ClosingCrane`, motion hooks, `styles`).

- [ ] **Step 6: Run the checks**

`home_snapshot.py nav` → `ok   nav: {'current': ['Home'], 'products': '#products', 'page': 'home'}`.
`home_snapshot.py compare http://localhost:3025 task4` → `PASS`.
`qa_home_ink.py http://localhost:3025` → full pass count.
Lint and `tsc --noEmit` → clean.
Then build, `bigh-ink-prod`, `home_snapshot.py compare http://localhost:3026 task4-prod baseline-prod` and `qa_home_ink.py http://localhost:3026` → `PASS`, full count.

- [ ] **Step 7: Commit**

```bash
git -C C:/Users/mcbig/Documents/codes/bigh-ink add -A src scripts/qa/home_snapshot.py
git -C C:/Users/mcbig/Documents/codes/bigh-ink commit -m "feat(ink): InkPage shell and one site header and footer for every page"
```

---

### Task 5: The About page on the kit (structure, words, paintings, line, sheets)

**Files:**

- Create: `src/components/about/about-ink.tsx`, `src/components/about/about-ink.module.css`, `src/components/about/about-route.ts`
- Modify: `src/app/[locale]/about/page.tsx`
- Rewrite: `scripts/qa/qa_about.py` (the old one tests the glass page, which this replaces)

**Interfaces:**

- Consumes: `InkPage`, `SiteDialogs`, `useSiteDialogs` (Task 4); `on`, `station`, `fresh`, `lift`, `rule`, `footerEnding`, `type Layout`, `type Waypoint` (Task 3); `ink.module.css` classes (Task 2); `mito`, `gold`, `halo`, `inkstone`, `liu` from `@/components/home-v2/look-ink/assets`; `about`, `drafts`, `routes` from `./about-content`; `Acronym`, `CountUp`, `Greetings` (existing About components).
- Produces: `AboutInk()` (default About page body); `aboutRoute(layout: Layout): Waypoint[]`.
- Anchors the route uses (all `data-brush`): `opening` (the opening section), `about-cell` (the cell's figure), `st-purpose`, `st-roots`, `st-experience`, `st-promise` (stations), `promise-0` … `promise-3` (the four promises), and the footer's `footer-promise`.

- [ ] **Step 1: Write the failing QA**

Replace `scripts/qa/qa_about.py` with:

```python
"""QA for the About page in the Ink & Gold look (October 5, 2026; Mo approved the mockup
reference/ink-pages/mockups/about.jpg).

At 1440x900 and 390x844, then the opening at 1280x720, 1536x1000, 1024x768, 900x1100, 768x1024
and 360x780: answers 200; no console errors or warnings; no failed requests; one h1, English
"Be in Good Health." with lang="en"; every locked line is on the page; no WebGL canvas in the
page; every painting multiplies onto the paper and the page wears the paper texture; the header
marks About as the current page and its Products link goes to /#products; no sideways scrolling;
text at least 15px and navigation at least 18px; links and buttons in the page at least 48px tall;
the cell sits in the first screen and never touches the title or the opening words; four
stations; the Support and Ask BiGH Science sheets open, close and hand focus back.
Desktop only (900px and wider): the brush layer draws the page layout, and its ink passes each
station's leader. Review focus: /about#promise lands below the header; Skip to content puts focus
at the words; with pictures blocked every heading and paragraph is visible.
Reduced motion: every painting shown, the gold leaf fully up, the whole line drawn.
Other languages (kr, jp, cns, vn): 200, no console errors, the h1 stays English, no English
source sentence left visible.

Pictures: scripts/qa/out/about-ink/<size>-NN.png (viewport shots while scrolling).

Usage: python -X utf8 scripts/qa/qa_about.py [base-url]
"""

import os
import sys

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = ARGS[0] if ARGS else "http://localhost:3025"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "about-ink")
os.makedirs(OUT, exist_ok=True)
results = []

# The locked words (src/components/about/about-content.ts), as they appear on the page.
LOCKED = [
    "What our name stands for.",
    "What our work is for.",
    "A full life has many parts.",
    "We focus on one you can’t see: your cells.",
    "Our mission is to support cellular health and mental energy, helping people live life to the fullest.",
    "Our key formulas begin with scientists.",
    "Dr. Jiankang Liu, our Chief Scientific Advisor, studies mitochondria and aging. He formulated NuriCell, and with Dr. Iris Wang, he developed Nature Calm.",
    "Meet our scientists",
    "Our flagship formula is older than BiGH.",
    "scientific papers by Dr. Liu",
    "BiGH founded in California",
    "NuriCell’s formula, unchanged",
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
STATIONS = ["Our purpose", "Our scientific roots", "Our experience", "Our promise"]


def check(name, ok, detail=""):
    results.append((name, bool(ok)))
    print(f"{'PASS' if ok else 'FAIL'} {name}{(' — ' + str(detail)) if detail and not ok else ''}")


def open_page(browser, width, height, path="/about", reduced=False, block_images=False):
    context = browser.new_context(
        viewport={"width": width, "height": height},
        reduced_motion="reduce" if reduced else "no-preference",
    )
    page = context.new_page()
    errors, failed = [], []
    page.on("console", lambda m: errors.append(m.text) if m.type in ("error", "warning") else None)
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
        check(f"{tag} no WebGL canvas in the page", page.evaluate("document.querySelectorAll('main canvas').length") == 0)
        blends = page.evaluate(
            "[...document.querySelectorAll('main img[data-bloom]')].map(i => getComputedStyle(i).mixBlendMode)"
        )
        check(f"{tag} paintings multiply", blends and all(b == "multiply" for b in blends), blends)
        paper = page.evaluate("getComputedStyle(document.querySelector('[data-look=\"ink\"]')).backgroundImage")
        check(f"{tag} paper texture", "paper.webp" in paper, paper)
        nav = page.evaluate(
            """() => { const n = document.querySelector('#home-navigation');
                 return { current: [...n.querySelectorAll('[aria-current="page"]')].map(a => a.textContent.trim()),
                          products: [...n.querySelectorAll('a')].find(a => a.textContent.trim() === 'Products')?.getAttribute('href') }; }"""
        )
        check(f"{tag} header marks About", nav["current"] == ["About"], nav)
        check(f"{tag} Products goes home", (nav["products"] or "").endswith("/#products"), nav)
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
        stations = page.evaluate("[...document.querySelectorAll('[data-station]')].map(s => s.textContent.trim())")
        check(f"{tag} four stations", stations == STATIONS, stations)
        cell = page.evaluate(
            """() => { const c = document.querySelector('[data-brush="about-cell"] img').getBoundingClientRect();
                 const words = [...document.querySelectorAll('[data-brush="opening"] h1, [data-brush="opening"] p')].map(e => e.getBoundingClientRect());
                 const hit = words.some(w => !(c.right <= w.left || c.left >= w.right || c.bottom <= w.top || c.top >= w.bottom));
                 return { top: c.top, inFirst: c.top < innerHeight, hit }; }"""
        )
        check(f"{tag} cell in the first screen", cell["inFirst"], cell)
        check(f"{tag} cell clear of the words", not cell["hit"], cell)
        # Sheets: Support from the header (menu on a phone), Ask from the pause.
        if width < 1101:
            page.click("button[aria-controls='home-navigation']")
        page.click("#home-navigation button:has-text('Support')")
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
        check(f"{tag} no console errors or warnings", not errors, errors[:3])
        check(f"{tag} no failed requests", not failed, failed[:3])
        page.evaluate("window.scrollTo(0, 0)")
        shots(page, tag, height)
        context.close()


def openings(browser):
    for width, height in [(1280, 720), (1536, 1000), (1024, 768), (900, 1100), (768, 1024), (360, 780)]:
        tag = f"{width}x{height}"
        context, page, response, errors, failed = open_page(browser, width, height)
        cell = page.evaluate(
            """() => { const c = document.querySelector('[data-brush="about-cell"] img').getBoundingClientRect();
                 const words = [...document.querySelectorAll('[data-brush="opening"] h1, [data-brush="opening"] p')].map(e => e.getBoundingClientRect());
                 return { inFirst: c.top < innerHeight, hit: words.some(w => !(c.right <= w.left || c.left >= w.right || c.bottom <= w.top || c.top >= w.bottom)) }; }"""
        )
        check(f"{tag} cell in the first screen", cell["inFirst"], cell)
        check(f"{tag} cell clear of the words", not cell["hit"], cell)
        sideways = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
        check(f"{tag} no sideways scrolling", sideways <= 0, sideways)
        page.screenshot(path=os.path.join(OUT, f"opening-{tag}.png"))
        context.close()


def line_and_focus(browser):
    context, page, response, errors, failed = open_page(browser, 1440, 900, reduced=True)
    layout = page.evaluate("document.querySelector('[data-lifts]')?.dataset.layout")
    check("1440 brush draws the page layout", layout == "page", layout)
    # Each station's leader ends at the line: some ink within 14px right of the label's leader.
    meets = page.evaluate(
        """() => [...document.querySelectorAll('[data-station]')].map(s => {
             const box = s.getBoundingClientRect(); const x = box.right + window.scrollX; const y = box.top + box.height / 2 + window.scrollY;
             const host = document.querySelector('[data-lifts]'); const top = host.getBoundingClientRect().top + window.scrollY;
             for (const c of host.querySelectorAll('canvas')) {
               const t = parseFloat(c.style.top); const h = parseFloat(c.style.height); if (y - top < t || y - top > t + h) continue;
               const ctx = c.getContext('2d'); const sx = c.width / c.clientWidth;
               const data = ctx.getImageData(Math.round((x - host.getBoundingClientRect().left - window.scrollX) * sx), Math.round((y - top - t) * sx), Math.round(28 * sx), 1).data;
               for (let i = 3; i < data.length; i += 4) if (data[i] > 40) return true;
             } return false; })"""
    )
    check("1440 line meets every station", meets and all(meets), meets)
    bloom = page.evaluate("[...document.querySelectorAll('[data-bloom]')].every(e => e.dataset.bloom === 'done')")
    check("reduced motion: every painting shown", bloom)
    charge = page.evaluate("getComputedStyle(document.querySelector('[data-charge]')).opacity")
    check("reduced motion: gold leaf fully up", float(charge) == 0, charge)
    context.close()
    # Deep link lands below the header.
    context, page, response, errors, failed = open_page(browser, 1440, 900, path="/about#promise")
    page.wait_for_timeout(1500)
    gap = page.evaluate(
        "document.querySelector('#promise-title').getBoundingClientRect().top - document.querySelector('header').getBoundingClientRect().bottom"
    )
    check("/about#promise lands below the header", gap >= 0, gap)
    # Skip to content.
    page.evaluate("window.scrollTo(0, 0)")
    page.keyboard.press("Tab")
    skip = page.evaluate("document.activeElement?.textContent?.trim()")
    page.keyboard.press("Enter")
    page.wait_for_timeout(300)
    focus = page.evaluate("document.activeElement?.id")
    check("Skip to content puts focus at the words", skip == "Skip to content" and focus == "main", [skip, focus])
    context.close()
    # Pictures blocked: words still visible.
    context, page, response, errors, failed = open_page(browser, 1440, 900, block_images=True)
    hidden = page.evaluate(
        """[...document.querySelectorAll('main h1, main h2, main p')].filter(e => {
             let n = e; while (n) { if (parseFloat(getComputedStyle(n).opacity) < 0.05) return true; n = n.parentElement; } return false; })
           .map(e => e.textContent.trim().slice(0, 30))"""
    )
    check("pictures blocked: every heading and paragraph visible", not hidden, hidden[:5])
    context.close()


def languages(browser):
    english = [line for line in LOCKED if len(line) > 24]
    for lang in ["kr", "jp", "cns", "vn"]:
        context, page, response, errors, failed = open_page(browser, 1440, 900, path=f"/{lang}/about")
        check(f"{lang} answers 200", response.status == 200, response.status)
        h1 = page.evaluate("document.querySelector('h1').getAttribute('aria-label')")
        check(f"{lang} h1 stays English", h1 == "Be in Good Health.", h1)
        text = page.evaluate("document.querySelector('main').innerText")
        left = [line for line in english if line in text]
        check(f"{lang} no English sentence left", not left, left[:3])
        check(f"{lang} no console errors or warnings", not errors, errors[:3])
        page.screenshot(path=os.path.join(OUT, f"{lang}-opening.png"))
        context.close()


with sync_playwright() as p:
    browser = p.chromium.launch(args=["--use-angle=d3d11"])
    desktop_and_phone(browser)
    openings(browser)
    line_and_focus(browser)
    languages(browser)
    browser.close()

passed = sum(ok for _, ok in results)
print(f"\n{passed}/{len(results)} passed")
sys.exit(0 if passed == len(results) else 1)
```

Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/scripts/qa/qa_about.py http://localhost:3025`
Expected: FAIL on most checks (the glass page is still served: WebGL canvas, no `data-look="ink"`, no stations).

- [ ] **Step 2: The route**

Create `src/components/about/about-route.ts`:

```ts
import {
  footerEnding,
  fresh,
  lift,
  on,
  rule,
  station,
  type Layout,
  type Waypoint,
} from "@/components/ink/route-kit";

// The About page's brush line (October 5, 2026; mockup reference/ink-pages/mockups/about.jpg).
// On two columns it leaves the foot of the ink cell, sweeps down to the left and runs down the
// page's left margin, past the four stations (each label sits left of the line, its leader
// pointing at it), reloading beside each. Then it touches down four times, one short rule over
// each promise, travels to the footer and lays the stroke the crane at rest stands on.
// Under 900px the line would run through the words: only the four rules and the footer's stroke.
const promises: Waypoint[] = [0, 1, 2, 3].flatMap((i) => rule(`promise-${i}`));

const page: Waypoint[] = [
  on("about-cell", 0.34, 0.86, 1.2, 0.6),
  on("about-cell", 0.18, 0.98, 2.6),
  fresh(station("purpose", "left"), 1),
  station("roots", "left"),
  fresh(station("roots", "left")),
  fresh(station("experience", "left")),
  fresh(station("promise", "left")),
  lift("st-promise", 1, 3),
];

export function aboutRoute(layout: Layout): Waypoint[] {
  if (layout === "page") return [...page, ...promises, ...footerEnding];
  return [...promises, ...footerEnding];
}
```

(The duplicate `station("roots", "left")` before its `fresh` copy is intentional: the stroke arrives at the station, then a new loaded stroke leaves it. Tune the waypoints by eye in Step 5; keep the shape: one calm vertical with one sweep out of the cell.)

- [ ] **Step 3: The page component**

Create `src/components/about/about-ink.tsx`:

```tsx
"use client";

import Image from "next/image";
import { ArrowRight } from "lucide-react";
import { gold, halo, inkstone, liu, mito } from "@/components/home-v2/look-ink/assets";
import { useSiteDialogs } from "@/components/ink/dialogs";
import { InkPage } from "@/components/ink/ink-page";
import base from "@/components/ink/ink.module.css";
import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import { about, drafts, routes } from "./about-content";
import { aboutRoute } from "./about-route";
import { Acronym } from "./acronym";
import { CountUp } from "./count-up";
import { Greetings } from "./greetings";
import styles from "./about-ink.module.css";

// The About page in the Ink & Gold look (October 5, 2026; Mo approved the mockup
// reference/ink-pages/mockups/about.jpg; the words are the locked ones in about-content.ts).
// "Be in Good Health." beside the ink cell (the homepage's painting), whose gold leaf comes up as
// the page opens; then four parts down the brush line (purpose, scientific roots, experience,
// promise) and the page's one centred pause, Ask BiGH Science, under the inkstone.

const CELL_ALT = "A mitochondrion, painted in ink, with two gold folds where energy is made";

function sentences(text: string) {
  return text.match(/[^.!?。！？]+[.!?。！？]*\s*/gu)?.map((part) => part.trim()) ?? [text];
}

function Station({ id, label }: { id: string; label: string }) {
  return (
    <p
      className={`${base.station} ${styles.station}`}
      data-station=""
      data-side="left"
      data-brush={`st-${id}`}
    >
      {label}
    </p>
  );
}

function Opening() {
  const copy = useCopy();
  return (
    <section className={styles.opening} data-brush="opening" aria-labelledby="about-title">
      <div className={`${base.wrap} ${styles.openingGrid}`}>
        <div className={styles.openingWords}>
          <p className={styles.kicker}>{copy(about.hero.label)}</p>
          <Acronym className={styles.title} />
          <p className={styles.lead}>
            {sentences(copy(about.hero.lead)).map((sentence) => (
              <span key={sentence}>{sentence}</span>
            ))}
          </p>
        </div>
        <figure className={styles.cell} data-brush="about-cell">
          <span className={styles.cellBody}>
            <Image
              className={base.ink}
              src={mito.glow.src}
              alt={copy(CELL_ALT)}
              width={mito.glow.width}
              height={mito.glow.height}
              sizes="(max-width: 899px) 100vw, 52vw"
              priority
              data-bloom="waiting"
            />
            <span className={base.gold} style={{ ["--gold" as string]: `url(${gold.mito})` }} />
            <span
              className={styles.charge}
              data-charge=""
              style={{ ["--gold" as string]: `url(${gold.mito})` }}
            />
          </span>
          <figcaption className={base.caption}>{copy(drafts.illustration)}</figcaption>
        </figure>
      </div>
    </section>
  );
}

function Purpose() {
  const copy = useCopy();
  return (
    <section id="purpose" className={styles.part} aria-labelledby="purpose-title">
      <div className={`${base.wrap} ${styles.partGrid}`}>
        <Station id="purpose" label={copy(about.purpose.label)} />
        <div className={styles.content}>
          <h2 id="purpose-title" className={`${base.display} ${styles.statement}`}>
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
    <section id="roots" className={styles.part} aria-labelledby="roots-title">
      <div className={`${base.wrap} ${styles.partGrid}`}>
        <Station id="roots" label={copy(about.roots.label)} />
        <div className={`${styles.content} ${styles.roots}`}>
          <figure className={styles.print}>
            <Image
              className={`${base.ink} ${styles.halo}`}
              src={halo.src}
              alt=""
              width={halo.width}
              height={halo.height}
              sizes="560px"
              data-bloom=""
            />
            <span className={styles.mount}>
              <Image
                src={liu.src}
                alt={copy(about.roots.photo.alt)}
                width={liu.width}
                height={liu.height}
                sizes="(max-width: 899px) 220px, 300px"
              />
            </span>
          </figure>
          <div className={styles.rootsWords}>
            <h2 id="roots-title" className={`${base.display} ${styles.heading}`}>
              {copy(about.roots.title)}
            </h2>
            <p className={styles.body}>{copy(about.roots.text)}</p>
            <Link href={routes.scientists} className={base.pillGhost}>
              {copy(about.roots.link)} <ArrowRight size={18} aria-hidden="true" />
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}

function Experience() {
  const copy = useCopy();
  const years = copy(about.experience.stats[1].unit);
  return (
    <section id="experience" className={styles.part} aria-labelledby="experience-title">
      <div className={`${base.wrap} ${styles.partGrid}`}>
        <Station id="experience" label={copy(about.experience.label)} />
        <div className={styles.content}>
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
      </div>
    </section>
  );
}

function Promises() {
  const copy = useCopy();
  return (
    <section id="promise" className={styles.part} aria-labelledby="promise-title">
      <div className={`${base.wrap} ${styles.partGrid}`}>
        <Station id="promise" label={copy(about.promise.label)} />
        <div className={`${styles.content} ${styles.promise}`}>
          <h2 id="promise-title" className={`${base.display} ${styles.heading}`}>
            {copy(about.promise.title)}
          </h2>
          <ul className={styles.promises}>
            {about.promise.items.map((item, i) => (
              <li key={item.title} data-brush={`promise-${i}`}>
                <h3>{copy(item.title)}</h3>
                <p>{copy(item.text)}</p>
                {i === 3 && <Greetings className={styles.greetings} />}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}

function Closing() {
  const copy = useCopy();
  const dialogs = useSiteDialogs();
  return (
    <section id="closing" className={styles.closing} aria-labelledby="closing-title">
      <div className={`${base.wrap} ${styles.pause}`}>
        <figure className={styles.inkstone}>
          <Image
            className={base.ink}
            src={inkstone.src}
            alt=""
            width={inkstone.width}
            height={inkstone.height}
            sizes="(max-width: 720px) 70vw, min(26vw, 400px)"
            data-bloom=""
          />
          <figcaption className={base.caption}>{copy(drafts.illustration)}</figcaption>
        </figure>
        <h2 id="closing-title" className={`${base.display} ${styles.heading}`}>
          {copy(about.closing.title)}
        </h2>
        <p className={styles.body}>{copy(about.closing.text)}</p>
        <div className={styles.actions}>
          <button type="button" className={base.pill} onClick={dialogs.openAsk}>
            {copy(about.closing.primary)}
          </button>
          <Link href={routes.products} className={base.pillGhost}>
            {copy(about.closing.secondary)}
          </Link>
        </div>
      </div>
    </section>
  );
}

export function AboutInk() {
  return (
    <InkPage current="about" route={aboutRoute}>
      {() => (
        <>
          <Opening />
          <Purpose />
          <Roots />
          <Experience />
          <Promises />
          <Closing />
        </>
      )}
    </InkPage>
  );
}
```

Check before moving on: the cell's alt text and "Illustration" are existing catalog strings (`grep -n "A mitochondrion, painted in ink" src/i18n/copy-keys.json` and `"Illustration"` must both find a key). If the alt text has no key, use the key the homepage's `cellular.tsx` uses.

- [ ] **Step 4: The page's styles**

Create `src/components/about/about-ink.module.css`. Every rule is scoped under the kit root `:global([data-page="about"])` so the homepage resets never win. Starting values (from DESIGN.md and the mockup; tune by eye in Step 5):

```css
/* About in the Ink & Gold look (October 5, 2026). Layout from the approved mockup
   (reference/ink-pages/mockups/about.jpg): an opening of words beside the ink cell, then four
   parts in a three-zone grid (station, the brush line's lane, content), then the centred pause.
   Rhythm Rule spacing: 215px of paper before a chapter, 160px between blocks, 110px between the
   parts of a block, 70-100px inside one. */

:global([data-page="about"]) .opening {
  padding: calc(var(--header-h, 88px) + clamp(40px, 6vw, 96px)) 0 clamp(64px, 8vw, 140px);
}

:global([data-page="about"]) .openingGrid {
  display: grid;
  grid-template-columns: minmax(0, 6fr) minmax(0, 6fr);
  align-items: center;
  gap: clamp(24px, 4vw, 72px);
}

:global([data-page="about"]) .kicker {
  margin: 0 0 18px;
  color: var(--muted);
  font-size: 19px;
  font-weight: 450;
}

/* The acronym: the four initials in sumi ink, the rest of each word in ink grey. */
:global([data-page="about"]) .title {
  --acronym-accent: var(--ink);
  margin: 0;
  color: var(--muted);
  font-family: var(--display-font);
  font-weight: var(--display-weight);
  font-size: clamp(56px, 7.4vw, 124px);
  line-height: 0.96;
  letter-spacing: -0.035em;
}

:global([data-page="about"]) .lead {
  margin: clamp(22px, 2.4vw, 36px) 0 0;
  color: var(--muted);
  font-size: clamp(19px, 1.5vw, 23px);
  line-height: 1.45;
}

:global([data-page="about"]) .lead span {
  display: block;
}

:global([data-page="about"]) .cell {
  position: relative;
  margin: 0;
  /* The painting runs a little past the column into the gutter, as on the homepage. */
  margin-right: calc(-0.5 * var(--gutter));
}

:global([data-page="about"]) .cellBody {
  position: relative;
  display: block;
  isolation: isolate;
}

:global([data-page="about"]) .cellBody img {
  display: block;
  width: 100%;
  height: auto;
}

/* The gold leaf comes up as the page opens: until the painting has bloomed, its leaf is
   drained of colour (a grey layer, masked to the leaf, in saturation blend); then the layer
   fades over one and a half breaths. Reduced motion: no layer, the leaf is up. */
:global([data-page="about"]) .charge {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: #8a867e;
  -webkit-mask: var(--gold) center / 100% 100% no-repeat;
  mask: var(--gold) center / 100% 100% no-repeat;
  mix-blend-mode: saturation;
  opacity: 0;
}

@media (prefers-reduced-motion: no-preference) {
  :global([data-page="about"]) .charge {
    opacity: 1;
    transition: opacity calc(var(--breath) * 1.5) var(--ease) calc(var(--breath) * 0.4);
  }

  :global([data-page="about"]) [data-bloom="done"] ~ .charge {
    opacity: 0;
  }
}

:global([data-page="about"]) .cell figcaption {
  position: absolute;
  right: calc(0.5 * var(--gutter));
  bottom: 4%;
}

/* The four parts: station | the line's lane | content. */
:global([data-page="about"]) .part {
  padding: clamp(80px, 8.3vw, 160px) 0 0;
  scroll-margin-top: calc(var(--header-h, 88px) + 24px);
}

:global([data-page="about"]) .partGrid {
  display: grid;
  grid-template-columns: minmax(150px, 1.5fr) clamp(48px, 5vw, 88px) minmax(0, 8.5fr);
  align-items: start;
}

:global([data-page="about"]) .station {
  grid-column: 1;
  justify-self: end;
  margin-top: 0.55em;
}

:global([data-page="about"]) .content {
  grid-column: 3;
  min-width: 0;
}

:global([data-page="about"]) .statement > span {
  display: block;
}

:global([data-page="about"]) .heading {
  max-width: 18ch;
}

:global([data-page="about"]) .body {
  max-width: 30em;
  margin: clamp(20px, 2vw, 32px) 0 0;
  color: var(--muted);
  font-size: 19px;
  line-height: 1.6;
}

:global([data-page="about"]) .roots {
  display: grid;
  grid-template-columns: minmax(0, 5fr) minmax(0, 7fr);
  align-items: center;
  gap: clamp(32px, 5vw, 88px);
}

:global([data-page="about"]) .print {
  position: relative;
  margin: 0;
  display: grid;
  place-items: center;
}

:global([data-page="about"]) .halo {
  position: absolute;
  width: 184%;
  max-width: none;
  height: auto;
  inset: 50% auto auto 50%;
  translate: -50% -50%;
  z-index: -1;
}

/* The photo mount: the page's only shadow. */
:global([data-page="about"]) .mount {
  display: block;
  width: min(100%, 300px);
  padding: 14px;
  background: #fbf9f4;
  box-shadow:
    0 22px 44px -22px rgba(12, 11, 10, 0.42),
    0 3px 8px rgba(12, 11, 10, 0.1);
}

:global([data-page="about"]) .mount img {
  display: block;
  width: 100%;
  height: auto;
}

:global([data-page="about"]) .rootsWords {
  display: grid;
  justify-items: start;
  gap: 0;
}

:global([data-page="about"]) .rootsWords > a {
  margin-top: clamp(24px, 2.4vw, 36px);
}

:global([data-page="about"]) .figures {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: clamp(20px, 3vw, 48px);
  margin: clamp(32px, 3.4vw, 56px) 0 0;
}

:global([data-page="about"]) .figures > div {
  display: flex;
  flex-direction: column-reverse;
  gap: 10px;
  padding-top: 18px;
  border-top: 1px solid var(--line);
}

:global([data-page="about"]) .figures dt {
  color: var(--muted);
  font-size: 17px;
  font-weight: 450;
}

:global([data-page="about"]) .figures dd {
  margin: 0;
}

:global([data-page="about"]) .figure {
  font-size: clamp(48px, 4.6vw, 76px);
  font-weight: 300;
  line-height: 1;
  letter-spacing: -0.03em;
  font-variant-numeric: tabular-nums;
}

:global([data-page="about"]) .unit {
  font-size: clamp(26px, 2.4vw, 38px);
  font-weight: 300;
}

:global([data-page="about"]) .promise {
  display: grid;
  grid-template-columns: minmax(0, 4fr) minmax(0, 8fr);
  gap: clamp(28px, 4vw, 72px);
}

:global([data-page="about"]) .promises {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: clamp(40px, 4vw, 64px) clamp(28px, 3vw, 56px);
  margin: 0;
  padding: 0;
  list-style: none;
}

/* Each promise sits under a short rule the brush paints (the route's rule over promise-N). */
:global([data-page="about"]) .promises li {
  padding-top: 22px;
}

:global([data-page="about"]) .promises h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 500;
  line-height: 1.3;
}

:global([data-page="about"]) .promises p {
  margin: 6px 0 0;
  color: var(--muted);
  font-size: 19px;
  line-height: 1.5;
}

:global([data-page="about"]) .greetings {
  margin-top: 14px;
}

/* The pause: centred, the inkstone small over the words. */
:global([data-page="about"]) .closing {
  padding: clamp(120px, 11vw, 215px) 0 clamp(120px, 11vw, 215px);
}

:global([data-page="about"]) .pause {
  display: grid;
  justify-items: center;
  text-align: center;
}

:global([data-page="about"]) .inkstone {
  position: relative;
  width: min(26vw, 400px);
  margin: 0 0 clamp(24px, 2.4vw, 40px);
}

:global([data-page="about"]) .inkstone img {
  display: block;
  width: 100%;
  height: auto;
}

:global([data-page="about"]) .inkstone figcaption {
  position: absolute;
  right: -2em;
  bottom: 0;
}

:global([data-page="about"]) .pause .heading {
  max-width: none;
}

:global([data-page="about"]) .pause .body {
  margin-inline: auto;
}

:global([data-page="about"]) .actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 14px;
  margin-top: clamp(28px, 2.6vw, 40px);
}

/* One column (under 900px): no page-long line, so the stations sit over their parts. */
@media (max-width: 899px) {
  :global([data-page="about"]) .openingGrid,
  :global([data-page="about"]) .roots,
  :global([data-page="about"]) .promise {
    grid-template-columns: minmax(0, 1fr);
  }

  :global([data-page="about"]) .cell {
    margin-right: 0;
    order: -1;
  }

  :global([data-page="about"]) .partGrid {
    grid-template-columns: minmax(0, 1fr);
    gap: 22px;
  }

  :global([data-page="about"]) .station,
  :global([data-page="about"]) .content {
    grid-column: 1;
    justify-self: start;
  }

  :global([data-page="about"]) .part {
    padding-top: 104px;
  }

  :global([data-page="about"]) .closing {
    padding: 96px 0 120px;
  }

  :global([data-page="about"]) .inkstone {
    width: 70vw;
  }
}

@media (max-width: 720px) {
  :global([data-page="about"]) .figures,
  :global([data-page="about"]) .promises {
    grid-template-columns: minmax(0, 1fr);
  }

  :global([data-page="about"]) .figures > div {
    flex-direction: row-reverse;
    justify-content: space-between;
    align-items: baseline;
  }
}
```

- [ ] **Step 5: The route file serves it**

Replace `src/app/[locale]/about/page.tsx`'s render with the providers and the new page:

```tsx
import { AboutInk } from "@/components/about/about-ink";
import { ProductPagesProvider } from "@/components/home/product-action";
import { SiteDialogs } from "@/components/ink/dialogs";
import { productPageLinks } from "@/components/product/catalog";
```

```tsx
return (
  <ProductPagesProvider pages={productPageLinks()}>
    <SiteDialogs>
      <AboutInk />
    </SiteDialogs>
  </ProductPagesProvider>
);
```

Remove the `AboutPage` import. Keep `generateMetadata` and the `/hken` redirect as they are. Update the comment above `Page`: "The About page in the Ink & Gold look (October 5, 2026), on the shared kit and sheets."

- [ ] **Step 6: Look, tune, check**

Open `http://localhost:3025/about` in the preview at 1536x1000, 1440x900 and 390x844 (Playwright viewport shots, full size, scrolled like a visitor). Compare each screen with `reference/ink-pages/mockups/about.jpg`: words beside the cell in the first screen; one calm line out of the cell down the left margin through the station leaders; four rules over the promises; the pause centred; the footer's crane at rest. Tune `about-route.ts` waypoints and the CSS values above until it reads like the mockup and DESIGN.md's Rhythm Rule.
Run: `python -X utf8 C:/Users/mcbig/Documents/codes/bigh-ink/scripts/qa/qa_about.py http://localhost:3025`
Expected: every check passes except possibly the languages block (Task 7) and `reduced motion: gold leaf fully up` (Task 6). Note which fail.
Run the homepage guard: `home_snapshot.py compare http://localhost:3025 task5` → `PASS` (About must not touch the homepage).

- [ ] **Step 7: Commit**

```bash
git -C C:/Users/mcbig/Documents/codes/bigh-ink add -A src/components/about src/app scripts/qa/qa_about.py
git -C C:/Users/mcbig/Documents/codes/bigh-ink commit -m "feat(about): the About page in the Ink & Gold look"
```

---

### Task 6: About's gold leaf comes up; counts; reduced motion

**Files:**

- Modify: `src/components/about/about-ink.module.css`, `docs/superpowers/specs/2026-10-05-ink-pages-design.md` (the spec's charge sentence)

**Interfaces:**

- Consumes: `.charge` with `data-charge` (Task 5), `useBloom` marking the cell `done` (kit).

- [ ] **Step 1: Write the failing check**

Add to `line_and_focus()` in `qa_about.py`, after the reduced-motion block, a motion run:

```python
    context, page, response, errors, failed = open_page(browser, 1440, 900)
    early = float(page.evaluate("getComputedStyle(document.querySelector('[data-charge]')).opacity"))
    page.wait_for_timeout(9000)
    late = float(page.evaluate("getComputedStyle(document.querySelector('[data-charge]')).opacity"))
    check("motion: the gold leaf comes up after the bloom", early > 0.5 and late < 0.05, [early, late])
    context.close()
```

Run `qa_about.py`. Expected: this check and `reduced motion: gold leaf fully up` show their real state; if both pass already from Task 5's CSS, move on to Step 3.

- [ ] **Step 2: Make it pass**

If `early` is 0: the opening's cell is in view at load, so `useBloom` may mark it `in` before first paint; keep `.charge` at opacity 1 while `[data-bloom="waiting"]` or `[data-bloom="in"]` precedes it (the `~` selector in Task 5's CSS only clears on `done`). If `late` stays 1: confirm the image and `.charge` are siblings inside `.cellBody` with the image first. If reduced motion shows the layer: the base rule must be `opacity: 0` outside the `no-preference` block.

- [ ] **Step 3: Record the decision in the spec**

In the spec's About section replace the sentence beginning "The glass cell's charge becomes gold leaf" with: "The glass cell's charge becomes gold leaf: the cell blooms with its leaf drained of colour, and the leaf comes up over one and a half breaths once the bloom is done (the page opening is the charge). Light crosses the leaf as on the homepage. The count-up figures stay, as large thin numerals on hairlines."

- [ ] **Step 4: Run, commit**

`qa_about.py` → both gold checks pass. `home_snapshot.py compare … task6` → `PASS`.

```bash
git -C C:/Users/mcbig/Documents/codes/bigh-ink add -A src/components/about scripts/qa/qa_about.py docs/superpowers/specs
git -C C:/Users/mcbig/Documents/codes/bigh-ink commit -m "feat(about): the cell's gold leaf comes up as the page opens"
```

---

### Task 7: Phone, tablet and the other languages

**Files:**

- Modify: `src/components/about/about-ink.module.css`, `src/components/about/about-route.ts` (only if the vn check fails), `messages/*.json` and `src/i18n/copy-keys.json` (only for new strings)

- [ ] **Step 1: Add the late-font and resize checks**

Add to `languages()` in `qa_about.py`, inside the loop, for `lang == "vn"` only:

```python
        if lang == "vn":
            page.evaluate("document.fonts.ready.then(() => true)")
            page.wait_for_timeout(1500)
            meets = page.evaluate(
                """() => [...document.querySelectorAll('[data-station]')].map(s => {
                     const box = s.getBoundingClientRect(); const host = document.querySelector('[data-lifts]');
                     const hb = host.getBoundingClientRect(); const y = box.top + box.height / 2 - hb.top;
                     for (const c of host.querySelectorAll('canvas')) {
                       const t = parseFloat(c.style.top), h = parseFloat(c.style.height); if (y < t || y > t + h) continue;
                       const sx = c.width / c.clientWidth;
                       const d = c.getContext('2d').getImageData(Math.round((box.right - hb.left) * sx), Math.round((y - t) * sx), Math.round(28 * sx), 1).data;
                       for (let i = 3; i < d.length; i += 4) if (d[i] > 40) return true; } return false; })"""
            )
            check("vn line meets every station after the font arrives", meets and all(meets), meets)
```

(The line is drawn only as the brush reaches it with motion on; open this page with `reduced=True` so the whole line is drawn: change this loop's `open_page(...)` call to pass `reduced=True`.)

And add to `desktop_and_phone()` after the 1440 shots, a resize check:

```python
        if width == 1440:
            page.set_viewport_size({"width": 820, "height": 900})
            page.wait_for_timeout(1200)
            layout = page.evaluate("document.querySelector('[data-lifts]')?.dataset.layout")
            check("resize to 820: the line redraws for one column", layout == "column", layout)
```

Run `qa_about.py`. Expected: the language block shows which locales fail and why.

- [ ] **Step 2: Fix what fails**

- An English sentence left in a locale: the string is missing from `copy-keys.json` or a catalog. Add a key: next free id is one above the highest `mNNN` (584 on October 5; compute it again), the English source in `copy-keys.json`, and a draft translation in `messages/{kr,jp,cns,vn,hken}.json` (and the English in `en.json`). Mark each new key's draft status in `docs/about-page.md` under "Draft translations".
- Korean, Japanese and Chinese headlines: the CJK Room Rule (line-height 1.22, tracking -0.01em, `word-break: keep-all`) on `.statement`, `.heading` and `.title` under `:lang(ko), :lang(ja), :lang(zh)` ancestors.
- A station whose leader misses the line in Vietnamese: the stations' column is too narrow for the longer label; widen the first grid column (`minmax(150px, 1.5fr)` → `minmax(180px, 1.8fr)`) rather than moving the line.

- [ ] **Step 3: Phone and tablet by eye**

Viewport shots at 390x844, 360x780 and 768x1024: the cell first, then the words; stations over their parts; one column for promises on phones; the pause's inkstone at 70vw; nothing crosses anything. Fix in CSS.

- [ ] **Step 4: Run, commit**

`qa_about.py` → all checks pass. `home_snapshot.py compare … task7` → `PASS`.

```bash
git -C C:/Users/mcbig/Documents/codes/bigh-ink add -A src messages scripts/qa/qa_about.py docs
git -C C:/Users/mcbig/Documents/codes/bigh-ink commit -m "feat(about): phone, tablet and the other languages"
```

---

### Task 8: Retire the glass page

**Files:**

- Delete: `src/components/about/about-page.tsx`, `about-page.module.css`, `look-glass.tsx`, `look-glass.module.css`, `look-glass-scene.ts`, `site-chrome.tsx`, `site-chrome.module.css`
- Modify: `src/components/about/about-content.ts` (drop `media`), `docs/about-page.md`
- Keep: `public/images/science/glass-cell.webp` and its depth map if anything else uses them (check first)

- [ ] **Step 1: Back up**

```bash
mkdir -p C:/Users/mcbig/Documents/codes/bigh-archive
python -X utf8 -c "import shutil; shutil.make_archive(r'C:/Users/mcbig/Documents/codes/bigh-archive/about-glass-2026-10-05', 'zip', r'C:/Users/mcbig/Documents/codes/bigh-ink/src/components/about')"
```

Expected: `about-glass-2026-10-05.zip` exists and lists `look-glass.tsx` (`python -m zipfile -l <zip>`).

- [ ] **Step 2: Nothing else imports what goes**

Run: `grep -rnE "about-page|look-glass|about/site-chrome|AboutHeader|AboutFooter|media\.mitochondrion" C:/Users/mcbig/Documents/codes/bigh-ink/src`
Expected: only the files being deleted. Run `grep -rn "glass-cell" C:/Users/mcbig/Documents/codes/bigh-ink/src`: if the homepage's old components or the Science page still use `glass-cell.webp`, keep the picture.

- [ ] **Step 3: Delete, tidy, check**

```bash
git -C C:/Users/mcbig/Documents/codes/bigh-ink rm src/components/about/about-page.tsx src/components/about/about-page.module.css src/components/about/look-glass.tsx src/components/about/look-glass.module.css src/components/about/look-glass-scene.ts src/components/about/site-chrome.tsx src/components/about/site-chrome.module.css
```

Remove the `media` export and its comment from `about-content.ts`. Update `docs/about-page.md`: the page is the Ink & Gold About (October 5, 2026), where it lives, how to check it (`qa_about.py`), the backup zip, and the draft translations list.
Run: lint, `tsc --noEmit`, `npm run build`, `npm run format:check`.
Expected: all clean.

- [ ] **Step 4: Full checks on the built site**

Start `bigh-ink-prod`; run `qa_about.py http://localhost:3026`, `qa_home_ink.py http://localhost:3026`, `home_snapshot.py compare http://localhost:3026 task8-prod baseline-prod`.
Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git -C C:/Users/mcbig/Documents/codes/bigh-ink add -A src docs
git -C C:/Users/mcbig/Documents/codes/bigh-ink commit -m "chore(about): retire the glass page (backup in bigh-archive)"
```

---

### Task 9: Finish review and the preview for Mo

**Files:**

- Modify: whatever the review's fixes touch (About files only)

- [ ] **Step 1: My own look**

Viewport shots of the built site at 1536x1000, 1440x900, 1280x720, 1024x768, 768x1024, 390x844 and 360x780, full size, scrolled like a visitor, plus reduced motion. Score honestly against the mockup and DESIGN.md; the bar is 9/10. Anything that looks broken is a defect even if it was "on purpose".

- [ ] **Step 2: Fresh reviewer**

Dispatch `impeccable-finish-reviewer` with: the spec's About section, DESIGN.md, `reference/ink-pages/mockups/about.jpg`, the shot folder, and the URL. Fix every material item it returns; re-run `qa_about.py` and the homepage guard after the fixes.

- [ ] **Step 3: Preview for Mo**

Ask Mo before pushing the branch (public repository). With her yes: fetch and merge `origin/main` into `ink-pages` (resolve conflicts, re-run all checks), push the branch, let Vercel build the preview (or create it through the Vercel MCP with the full commit SHA if the Git integration does not fire), check the preview signed out, and send Mo the link with a short note of what changed and what is still a draft (translations). Do not touch the demo alias without her yes.

- [ ] **Step 4: Commit any review fixes**

```bash
git -C C:/Users/mcbig/Documents/codes/bigh-ink add -A src
git -C C:/Users/mcbig/Documents/codes/bigh-ink commit -m "fix(about): finish review"
```

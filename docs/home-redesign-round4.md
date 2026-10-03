# Homepage redesign, round 4: the Ink & Gold build (October 2, 2026)

Mo chose the Ink & Gold world after a proper Impeccable round (PRODUCT.md interview, concept roll,
picture comps first, a GPT Image 2.5 vs Gemini test) and asked for BOTH approved openings to be
built so they can be compared: 2 "the crane" (primary) and 1 "the cell". One look, two openings,
everything below the opening shared.

## Final: Ink & Gold, the crane (October 2, 2026)

Mo picked the crane ("This Crane one is amazing."). It is now the homepage itself at `/` in every
language: `src/app/[locale]/page.tsx` renders `HomeDialogs` around `LookInk`
(`src/components/home-v2/look-ink/`). There is no `?look=` and no switcher any more.

- Removed: the cell opening (code, `mito-cell` picture and plate, its comp spec) and the eight test
  looks (daylight, night, words, sunrise, pop, iris, everyday, botanical): their components, pictures,
  clips, reference folders and QA scripts, plus `home-v2.tsx` and the look switcher. All of it is in
  the backup `C:\Users\mcbig\Documents\codes\bigh-archive\home-redesign-all-looks-2026-10-02.zip`.
- Kept: `chrome.tsx`, `content.ts`, `dialogs.tsx`, `reference/home-v2/ink/` (prompts, originals,
  plates, `build_assets.py`, `translations.cjs`), `reference/home-v2/r4/`, `hf_run.py`, `.impeccable/`.
- New words: ten strings (m575-m584: the four section labels, Dr. Liu's role, "20+ years", the
  mitochondrion's alt text, "Illustrations", "BiGH products", "Choose a story") added by
  `node reference/home-v2/ink/translations.cjs`. Their translations are DRAFTS, not native-reviewed.
- Checks: `python -X utf8 scripts/qa/qa_home_ink.py` (runs against `/` and `/kr`), `npm run build`.
- The brush line is drawn on desktop only; phones keep the opening's own line (lead's decision).

## Read first, in order

1. `docs/home-redesign.md` (worktree, dev server http://localhost:3014, shared files you must not
   edit, Mo's standing rules, checks). Rounds 2–3 rules about budgets are replaced by this page.
2. `PRODUCT.md` (product truth: midlife buyers; "real scientists" in ten seconds; today's words
   verbatim; real bottles and Dr. Liu photo only; Switzer site-wide; honesty labels).
3. The surface brief with the DIRECTION CONTRACT: run
   `C:\Users\mcbig\.claude\skills\impeccable\scripts\impeccable.cmd surface-brief read src/components/home-v2/look-ink/look-ink.tsx`
   from the worktree. Every block of it binds the build.
4. Impeccable's build references: `C:\Users\mcbig\.claude\skills\impeccable\reference\new-work.md`
   section 6 ("Build with full commitment", the comp-led phases) and section 7 up to the reviewer
   spawn (the lead spawns the reviewer, not you), `reference\visualize.md` "After approval" and
   "Plates and provenance", and `reference\craft-floor.md` IMMEDIATELY before your first UI edit.
5. `AGENTS.md` (Next.js 16: read `node_modules/next/dist/docs/` before Next-specific code; CSS
   specificity trap; LF line endings).

## The approved comps (Mo's approval, recorded in the `.json` sidecars)

| Opening           | First viewport (the measured contract)                      | Full page (reference below the fold) |
| ----------------- | ----------------------------------------------------------- | ------------------------------------ |
| 2 Crane (primary) | `.impeccable/mocks/approved/ink-crane-hero.png` (1536×1000) | `ink-crane-page.png`                 |
| 1 Cell            | `.impeccable/mocks/approved/ink-cell-hero.png` (1536×1000)  | `ink-cell-page.png`                  |

Also `approved/ref-gpt25-ink-crane-page.png`: GPT Image 2.5's take on the crane page. Mo saw it;
its ink landscape is the painting quality bar for the plates (not its tiny menu or fonts).
Comp text defects to ignore: stray commas in "Good health, starts with, your cells." — the words
are always today's exact copy from `src/components/home-v2/content.ts`.

## The state machine (already started by the lead)

`impeccable build-phase start --comp .impeccable/mocks/approved/ink-crane-hero.png` has run
(breakpoint 1536×1000; comps phase skipped because Mo approved). Run
`impeccable build-phase status` and follow it: spec → plates → hero → sections → motion →
responsive, each closed by `build-phase advance`. All commands are
`C:\Users\mcbig\.claude\skills\impeccable\scripts\impeccable.cmd <verb>` run from the worktree.

- **Fonts:** Switzer is a pinned brand face (PRODUCT.md). Run `font-match --measure` and
  `--rank <headline> --candidates Switzer` as the gate requires and let the tool record its
  result; implement Switzer in CSS regardless ("the brief wins: honor pinned fonts"). Note any
  gate friction in your report instead of forcing it.
- **Navigation size:** the comp's nav is the floor, never smaller. Shared `HomeHeader` stays
  (large nav for older readers, Design Vault #045).
- **The cell opening** is a variant of the same page (`opening="cell"`). After the crane hero
  passes its gate, build the cell opening and check it yourself with
  `impeccable comp-diff --comp .impeccable/mocks/approved/ink-cell-hero.png --build <capture> --out-dir .impeccable/review/diff/hero-cell`.

## Pictures and video

- **Plates = GPT Image 2.5** (Mo's test winner for paintings), through
  `python -X utf8 reference/home-v2/r4/hf_unquoted.py <name> <prompt.txt> --aspect <ratio> --ref <comp-spec crop.png> --out reference/home-v2/ink/originals`
  (~$0.05 a job, hard cap 60 jobs this round, one at a time, 2–10 min each: run in the
  background and keep working). Use the crop from `comp-spec --crop <id>` and the prompt from
  `comp-spec --plate-prompt <id>` as the starting point; aspect options 1:1, 3:2, 2:3, 4:3, 3:4,
  16:9, 9:16, 21:9. It has no transparent background: paint ink plates on plain white or on the
  page's rice paper and place them with `mix-blend-mode: multiply` on the paper ground (ink on
  paper multiplies naturally), or cut them out locally (rembg is installed) when a plate must
  float. Ship webp in `public/images/home-v2/ink/` (≤ 2400 px, aim < 350 KB) and run
  `impeccable embed-prompt <file> --prompt-file <prompt.txt>` on every shipped raster.
- **Layers for motion:** for the crane landscape, consider generating separate plates (far
  mountains, near mountains, crane, gold sun, mist) so code can give slow depth parallax and mist
  drift, matching the comp when composed.
- **Video (optional):** Kling 3.0 loops through
  `python -X utf8 reference/home-v2/hf_run.py video --look ink --name <n> --image <still> --last-image <same still> --model kling-video/v3.0/pro/image-to-video --prompt "..."`
  ($0.25–0.31 per 5 s; `ink` budget $5). Prompt for calm motion only (the crane's wings slowly
  beating, mist drifting, camera still). Reject any clip that warps the painting.
- **Real assets only:** bottles from `public/images/products/*.png` (never generated), Dr. Liu
  from `public/images/jiankang-liu.jpg` (512×768, never upscaled past sharp). Comps show where they
  go (`reference/home-v2/r4/fill_comps.py` placed them).

## What the page must carry (content.ts, all words through copy())

Opening (crane or cell) · "Tiny power plants." with the three numbered lines · scientists (Dr.
Liu photo, 280+ / 2016 / 20+ years, Dr. Iris Wang text only, Ask BiGH Science) · products (five
real bottles, choosing one shows its headline, words, credit and Discover; every picture through
ProductAction) · stories (fictional samples, labeled "Fictional sample" / "Illustrative photo";
no generated faces next to quotes) · science (three topics + an age slider with "Illustration,
not a measurement", using renders of the same ink mitochondrion) · research (filters + show all,
the research note) · purpose + three standards · shared footer. Sections the comps don't show
inherit the world: rice paper, ink, one gold, hairline labels, the brush line. No cards-with-
icons, no gradients, no red.

**Signature interaction:** one continuous ink brush line that draws itself as you scroll, from
the crane's flight path (or the cell's foot) through every section to the purpose; ink that
"blooms" softly as each painting enters. One breathing rhythm for all motion. Reduced motion: a
complete still page with the full brush line.

## Ownership and checks

Only create/edit: `src/components/home-v2/look-ink/**`, `public/images/home-v2/ink/**`,
`public/media/home-v2/ink/**`, `reference/home-v2/ink/**`, `scripts/qa/qa_home_ink.py`,
`.impeccable/build/**`, `.impeccable/review/**`. No git, no new npm packages, no shared-file
edits (ask the lead). Keep files compiling.

Write `scripts/qa/qa_home_ink.py` (both `?look=ink` and `?look=ink-cell`, desktop 1440×900 and
1280×720, phone 390×844, Korean, reduced motion): blocks in order, header links, dialogs, product
choice + NuriCell link, stories labels, topics + slider + honesty label, research filters + show
all, brush line draws, no sideways scroll, images loaded, text ≥ 15 px, targets ≥ 44 px, no
console errors.

Finish per new-work section 7 up to the reviewer: two inspection rounds at most, captures in
`.impeccable/review/` (`desktop.png` 1440 full page from the top, `mobile.png` 390, plus
`desktop-cell.png` and `mobile-cell.png` for the cell opening), the final `comp-diff` into
`.impeccable/review/diff/final/`, then `impeccable detect --json` on `src/components/home-v2/look-ink`
once, fix what is mechanical. Then report to the lead; the lead runs the finish reviewer.

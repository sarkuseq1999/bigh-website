# About page: handoff (final, September 28, 2026)

Branch `about-page` in its own worktree `C:\Users\mcbig\Documents\codes\bigh-about`, preview
"bigh-about" on port 3009 (its entry lives in the MAIN folder's `.claude/launch.json`). Nothing is
committed or pushed: ask Mo before every commit, push or demo-alias change.

## Mo's picks

- Sept 25: the locked words (`about` in `src/components/about/about-content.ts`).
- Sept 28: look B "Glass" (a glass mitochondrion "battery" docks at the top and fills with golden
  light chapter by chapter, Timeline-style fact list), opening 3 (the glass set in the title like
  a word: "Be in Good / Health." and the glass), and Switzer type, replacing both review pairs.
  He also said yes to removing the unpicked looks and options.

## What is on the page

`/about` renders `AboutPage` (`about-page.tsx`: header, body, footer, Ask BiGH Science / support
panel). The body is `look-glass.tsx` + `look-glass.module.css` + `look-glass-scene.ts` (three.js
shader on the approved render). Shared pieces still used: `acronym.tsx` (the h1 unfold),
`greetings.tsx`, `count-up.tsx`, `site-chrome.tsx`. The still is
`public/images/about/glass-battery-lifted.webp` (sidecar in `reference/about/originals/`).

## Removed on Sept 28 (backup first)

Looks A Golden hour and C Deep space (all `look-golden*`, `look-space*`), the look switcher,
openings 1 and 2, type pair 2, the Type/Opening review pill, the `?look`, `?hero` and `?type`
params, `looks`/`Look`/`toLook`, unused `drafts.timeline` and `media` entries, the unused helpers
(`sentences.tsx`, `use-reveal.ts`, `use-sticky-progress.ts`, `use-scroll-progress.ts`), the dark
header mode (only look C used it), every golden-_ and space-_ picture with its original and
sidecar, and `qa_about_a.py` / `qa_about_c.py`. Verified backup of all 87 uncommitted files from
before the cleanup: `C:\Users\mcbig\Documents\codes\bigh-archive\about-page-before-cleanup-2026-09-28.zip`.
Round 1 is also in the history (`2db8f07`, `57a1494`).

## Switzer

Switzer for everything (headings, body, header, footer, panel), with main's tokens on `.page` in
`about-page.module.css` (`--display-font`, `--display-weight` 460, `--display-track` -0.015em,
`--lead-weight`, `--lead-track`). It loads from Fontshare in `src/app/[locale]/about/page.tsx`:
the same `<link rel="stylesheet" precedence="default">` href as main's locale layout (07529d5), so
React renders it once after the merge; delete it there once this branch has merged main. NEVER
commit the Switzer font files: the licence forbids redistribution and the repo is public. CJK and
other scripts fall through to the locale fonts in `globals.css`.

## At the merge (TODO)

- The header and footer are this page's own copy (`site-chrome.tsx`); fold them into the shared
  site header/footer when the branches land.
- Remove the Fontshare link from `about/page.tsx` (main's layout loads it).
- Point `routes.scientists` at `/science` once the Science page lands.

## Words

Locked words: `about` in `about-content.ts` (use verbatim). DRAFT extras (`drafts`: greetings,
languages, "Illustration") need Mo's OK before launch. Facts: formula ~23 years (show "20+"); never
name CellGen or say Asia knew it first; GMP-certified maker in California (confirm the
certificate); 45-day refund current; BiGH incorporated 05/11/2016.

## Check

`python -X utf8 scripts/qa/qa_about.py http://localhost:3009` (real GPU by default; add
`--swiftshader` for the software renderer): 66 checks on Sept 28, including Switzer loaded and
first in every text role, the opening glass never touching a letter at six sizes, chapters taking
turns (sampled every 40 px), reduced motion, no WebGL, footer and Korean. Also
`npx prettier --check src/components/about`, `npx tsc --noEmit`, `npx eslint src/components/about`.
Review screenshots: `scripts/qa/out/about-final/`.

## Traps

- `var(--font-sans)` is EMPTY (Tailwind `@theme inline` never emits it): use `--sans` / `--font-dm-sans`.
- `useReducedMotion()` is true on the server: render moving parts as their own components.
- A sticky stage with a negative bottom margin rides over the footer: keep it in the absolute track.
- The opening glass is placed by measuring the real font (`openingGlass()`); it re-measures when
  fonts finish loading. It stays hidden until placed, so without JavaScript the opening shows no glass.
- Worktree guard: no `git -C <main>`, no compound shell commands with git; plain commands only.

## Mo's standing rules

Timeline (timeline.com) is the #1 reference: calm, premium, one idea per screen. Never draw vector
shapes on a photoreal render. No pathogen/red-dot visuals. Big text and nav for older readers.
Plans in chat, ELI5, labeled choices. Few words. Dr. Iris Wang in words only, never a photo.

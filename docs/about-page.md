# About page: handoff (Ink & Gold, October 5, 2026)

Branch `ink-pages`, worktree `C:\Users\mcbig\Documents\codes\bigh-ink`. Nothing is pushed: ask Mo
before every push or demo-alias change.

## What is on the page

`/about` renders `AboutInk` (`src/components/about/about-ink.tsx`, `about-ink.module.css`,
`about-route.ts`) on the shared ink kit in `src/components/ink/` (`InkPage`, the brush line, the
site header and footer, the Support and Ask BiGH Science sheets, `route-kit.ts`). Design: the
approved mockup `reference/ink-pages/mockups/about.jpg` and `DESIGN.md`. The paintings are the
homepage's (`src/components/home-v2/look-ink/assets`), and Dr. Liu's photo is
`public/images/jiankang-liu.jpg`.

Pieces of the About folder still in use: `about-content.ts` (the words), `acronym.tsx` (the h1
unfold), `greetings.tsx`, `count-up.tsx`.

## Retired: the Glass page

Mo picked look B "Glass" (opening 3, Switzer) on September 28, 2026. It was retired on October 5,
2026, when the Ink & Gold About replaced it. Deleted: `about-page.tsx`, `look-glass.tsx`,
`look-glass-scene.ts`, `site-chrome.tsx` and their CSS, plus the `media` export in
`about-content.ts`. Backup of the whole `src/components/about` folder as it was before:
`C:\Users\mcbig\Documents\codes\bigh-archive\about-glass-2026-10-05.zip`. An older backup
(Sept 28, before the look cleanup) is `about-page-before-cleanup-2026-09-28.zip` in the same folder,
and the first round is in the history (`2db8f07`, `57a1494`).
`public/images/science/glass-cell.webp` and its depth map stay: the Science page and the
homepage still use them. `public/images/about/glass-battery-lifted.webp` (and `originals/`) belong
to the old Glass page and nothing uses them now.

## Words

Locked words: `about` in `about-content.ts` (use verbatim; Mo, September 25, 2026). DRAFT extras
(`drafts`: greetings, the language list, "Illustration") need Mo's OK before launch. Facts: formula
about 23 years (show "20+"); never name CellGen or say Asia knew it first; GMP-certified maker in
California (confirm the certificate); 45-day refund is current; BiGH was incorporated 05/11/2016.
The h1 stays English "Be in Good Health." with `lang="en"` in every language (`TITLE_ALWAYS_ENGLISH`
in `acronym.tsx`).

## Languages

Korean, Japanese, Simplified Chinese and Vietnamese: 67 strings, of which 37 reuse existing keys
(header, footer, the two sheets) and 30 are the About keys m545 to m574 from September 28.
`hken.json` stays `{}`, and `/hken/about` redirects to `/cns/about`.

Draft translations, not native-reviewed: the 30 About keys (m545 to m574) and the tab title.
New keys on this branch: none (the Ink page reuses the same ones; the m600 range is unused).

Vietnamese uses Be Vietnam Pro site-wide (see `docs/header-and-languages.md`, "Vietnamese type").
Line breaks are scoped to this page in `about-ink.module.css`: Japanese breaks between phrases
(`auto-phrase`, Chrome and Edge only) with `line-break: strict`; Chinese keeps phrases whole
(`keep-all`), so put a comma where a line may end; the Vietnamese closing pills balance their
lines on phones.

## Check

`python -X utf8 scripts/qa/qa_about.py http://localhost:3025` (dev) or `http://localhost:3026`
(built site, `next start`): 129 checks on October 5, 2026 (dev). It covers the h1, the locked
words, every painting multiplying onto the paper, the brush line meeting each station, text,
navigation and target sizes, no sideways scrolling at eight sizes (1536 down to 360 wide), the
Support and Ask sheets,
the review anchors, reduced motion, and each language (200, no console errors, English h1, no
English source sentence left, no lone characters, no word crossing the margins). Screenshots go to
`scripts/qa/out/about-ink/`. Also run `scripts/qa/qa_home_ink.py` and
`scripts/qa/home_snapshot.py compare <url> <tag> baseline-prod`: the homepage must not change.

## Traps

- `var(--font-sans)` is EMPTY (Tailwind `@theme inline` never emits it): use `--sans` or
  `--font-dm-sans`.
- Scope component CSS under the page's root class: `homepage.module.css` resets `.site p`,
  `.site button`, `.site h2` at specificity 0,1,1.

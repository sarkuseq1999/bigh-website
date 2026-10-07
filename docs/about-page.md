# About page: handoff ("The name, on a folded letter", October 6, 2026)

Branch `ink-pages`, worktree `C:\Users\mcbig\Documents\codes\bigh-ink`. Nothing is pushed: ask Mo
before every push or demo-alias change.

## Current page: "The name, on a folded letter" (October 6, 2026)

Mo's design D, a blend of three concepts: one sheet of slightly aged paper folded like a letter
(CSS folds, no brush line), BiGH written by hand (the opening's name writes itself in one breath,
its gold dot lands after), a brushed letter opening each part on alternating sides of the middle
fold (Be: purpose; in: scientific roots, Dr. Liu on a pool of wash; Good: experience with tree
rings, one ring gold for 2016, and the promises under four watercolor dots; Health: Ask BiGH
Science under the big H).

- Design: the approved mockup `reference/ink-pages/mockups/about-d.png`, `DESIGN.md`, and the
  About section of `docs/superpowers/specs/2026-10-05-ink-pages-design.md`.
- Layout: on two columns (900px and wider) Dr. Liu's print stands beside the "in", its foot level
  with "Meet our scientists", on the pool laid on its side (a wash has no up or down). From 1200px
  the G stands with the rings beside it and the three figures sit in one row with a hairline
  between them; from 900 to 1199px the rings stand under the G and the figures stack. The middle
  fold starts under the header (where the opening's words start) and fades in, so it never runs
  through the logo. "Health" is set tight like the other chapter words ("ealth" tucked under the
  H's crossbar tip) and, across the fold, placed from its H, so the crossbar crosses the crease
  and ends clear of it in every language and the crease grazes the left edge of the "e". The H's
  stem and tip columns behind those numbers are in `about-letter.module.css`; measure them again
  if the H is regenerated. Dr. Liu's pool is not measured by hand: its height over its width
  (`--pool-ratio`) is passed to the CSS from `letter-art.ts` in `about-ink.tsx`.
- Tablets held upright (600 to 899px) are one column like phones, but the three figures stand in
  one row and the four promises two by two (stacked, they made a 5,900px page at 768px; now about
  5,400px). Under 600px the figures stack and the promises stand one per row. Under 900px there is
  no middle fold, only the folds across. Open point: on a tablet the Be, in and Good parts are
  still one left-aligned column with the right third bare; two columns from 600px would be a
  redesign, left for Mo's call.
- Motion: the name is written left to right through a soft ink front (one wide feathered edge
  that wanders gently; a bristle edge was tried and read as stripes on screen), in one breath
  (2.4s, the shared ease). The band spreads from the middle as the name finishes, the gold dot
  comes up at about 1.8s and the title unfolds at about 2.0s. Each chapter letter writes itself
  the same way as it reaches the reading line. Reduced motion: complete and still from the first
  paint.
- Code: `src/components/about/about-ink.tsx`, `chapter-word.tsx`, `about-letter.module.css`,
  `letter-art.ts` (generated), on the shared ink kit in `src/components/ink/` (`InkPage` with no
  brush route, the site header and footer, the Support and Ask BiGH Science sheets). Still in use
  from earlier rounds: `about-content.ts` (the words), `acronym.tsx` (the h1 unfold),
  `greetings.tsx`, `count-up.tsx`. The site header is the menu bar Mo picked on October 5,
  "Inscription" (`src/components/ink/nav/`): on /about it starts clear over the opening, marks
  About as the current page and settles on the page's aged paper once scrolled.
- Paintings: `reference/ink-pages/about/` (prompts, originals, `build_about.py`, `check_art.py`),
  spend in `reference/ink-pages/spend.md`. Shipped in `public/images/about-ink/`. Dr. Liu's photo
  is the real one, `public/images/jiankang-liu.jpg`.
- Draft translation: one new key on this branch, m587, the rings' description ("Tree rings in ink.
  A gold ring marks 2016, ..."), added by `reference/ink-pages/about/translations.cjs` in Korean,
  Japanese, Chinese and Vietnamese. It needs Mo's native check before launch. One open question in
  the Vietnamese: it says "Vân gỗ" (wood grain), where "vòng tuổi" (tree rings) may be the right
  words.
- Replaced: the first ink About (October 5, commits up to c30a489, a copy of the homepage's look
  with the brush line, `about-ink.module.css` and `about-route.ts`, now deleted), and before it
  the Glass page.

## Retired: the Glass page

Mo picked look B "Glass" (opening 3, Switzer) on September 28, 2026. It was retired on October 5,
2026, when the first ink About replaced it. Deleted: `about-page.tsx`, `look-glass.tsx`,
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
in `acronym.tsx`). The chapter words (Be, in, Good, Health) stay English in every language and are
hidden from screen readers; each part's heading carries the meaning.

## Languages

Korean, Japanese, Simplified Chinese and Vietnamese. The page uses the About keys m545 to m574
(September 28), the shared header, footer and sheet keys, and m587 (the rings' description, new on
this branch). The tab title uses the shared "About" key. `hken.json` stays `{}`, and `/hken/about`
redirects to `/cns/about`.

Draft translations, not native-reviewed: the About keys m545 to m574 and m587 (see the Vietnamese
question above).

Vietnamese uses Be Vietnam Pro site-wide (see `docs/header-and-languages.md`, "Vietnamese type").
Line breaks are scoped to this page in `about-letter.module.css`: Korean headings keep words whole;
Japanese breaks between phrases (`auto-phrase`, Chrome and Edge only) with `line-break: strict`;
Chinese keeps phrases whole (`keep-all`), so put a comma where a line may end; Japanese and Chinese
headings get a size that keeps their longest phrase on one line on phones and at 900-959px; the
Vietnamese closing pills balance their lines on phones.

## Check

`python -X utf8 scripts/qa/qa_about.py http://localhost:3025` (dev) or `http://localhost:3026`
(built site, `next start`; the built site orders CSS differently, so run both). Groups:
`desktop_and_phone`, `letter_layout`, `fold_header`, `motion`, `focus`, `deep_links`, `languages`,
`languages_layout`, `nav_locales`, `boundary`, `first_screen` (`--only=` runs some). It covers the
h1 and the locked words, every painting multiplying onto the paper (with no stacking context
between it and the page root), the folds and the parts' sides,
the arrangement of in and Good, the middle fold clear of the header, "Health" set tight with the
H's crossbar tip off the fold (read from the H's picture), text, navigation and target sizes, no
sideways scrolling, the Support and Ask sheets, the motion (the written name, the band's bloom,
the soft ink front, the name standing whole once written even with the wipe picture blocked, the
title reading "Be in Good Health." with JavaScript off) and reduced motion, deep links (every part,
the closing too), the tablet band (600 to 899px), and every language's words and line breaks:
382 checks, all passing on the built site on October 6, 2026.
Screenshots go to `scripts/qa/out/about-letter/`.

The homepage must not change: also run `scripts/qa/qa_home_ink.py <url>` and
`scripts/qa/home_snapshot.py compare <url> <new-tag> baseline-main997-prod` (built site) or
`baseline-main997` (dev), and `scripts/qa/home_snapshot.py nav <url> -` (the menu bar on / and
/about).

## Traps

- `var(--font-sans)` is EMPTY (Tailwind `@theme inline` never emits it): use `--sans` or
  `--font-dm-sans`.
- Scope component CSS under the page's root class: `homepage.module.css` resets `.site p`,
  `.site button`, `.site h2` at specificity 0,1,1, and the kit uses `.look ...` (0,2,0). Every
  About rule is scoped under `.letterPage`.
- Multiply: a painting multiplies onto the page root's paper only if nothing between it and the
  root makes a stacking context (no z-index on a positioned ancestor, no isolation, opacity,
  transform, filter or will-change on the sheet, a part, a grid or a figure). A transform on the
  painting itself is fine (the pool is turned with `rotate`).
- Replacing a picture under the same file name: delete `.next/cache/images` and
  `.next/dev/cache/images` before building, or the old optimized picture is served.

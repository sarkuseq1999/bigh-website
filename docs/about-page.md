# About page: handoff (C, "The circle", October 7, 2026)

Worktree `C:\Users\mcbig\Documents\codes\bigh-ink`. C "The circle" is on branch `about-c`. B "The
album" is on branch `about-b` (`about-c` was cut from it, so everything B shares is here too), and
D, the folded letter Mo rejected on October 7, stays on `ink-pages`. Nothing is pushed: ask Mo
before every push or demo-alias change.

## Current page: C, "The circle" (October 7, 2026)

Mo rejected D on October 7 ("I don't think this design looks good": the CSS folds read as tiles on a
wall, the name was said three times, the parts were uneven) and asked for B and C as real pages,
shaped through mockups (`reference/ink-pages/mockups/about-b.png`, `about-c.png`). The spec is the
section "About (stage 1), October 7" in `docs/superpowers/specs/2026-10-05-ink-pages-design.md`;
her rules for both pages are there too. B "The album" (an old painting album, each part a spread)
is on branch `about-b`; its notes are in that branch's copy of this file, and its own CSS is
`album.module.css`, which this branch no longer has.

- The circle: one large ink circle (an ensō: a whole, complete life), brushed in a single stroke
  and open where the stroke lifts, stands once, at the top, over the title. A small torn leaf of
  gold sits where the brush began, at 1 o'clock (the picture ships mirrored, so the page's clockwise
  sweep follows the brush from its wet head to its dry tail; the mockup has the gold at 11).
  Under the opening's words a band of low California hills in grey wash feathers out to both edges,
  with a faint gold glow on one hilltop. On a phone the band runs 1.8 times the window's width,
  clipped at both edges (the strip shown keeps the gold hilltop), so it reads as a band, not a
  55px smudge. From 1200px the seedling tucks in close under the hills, as in the mockup (the
  opening keeps no padding under them and the purpose part's top padding lies over their foot).
  The circle's stroke is preloaded at high priority; its gold leaf loads at once at low priority,
  with no preload, so the circle is asked for first (that only orders the requests; the hold below
  ties the two).
- The circle paints itself, in CSS: a conic-gradient mask sweeps clockwise around the picture in
  one breath (`--breath` 2.4s, `--ease`, after 0.3s), starting 26 degrees before the gold (where
  the brush's wet head begins, so the blackest part is drawn first), its leading edge soft over 12
  degrees, from 12 degrees back so nothing shows during the delay. The registered property `--sweep` has 360deg as its initial value, so once the sweep
  ends the mask is whole and the circle never depends on the animation finishing. The gold comes up
  after the stroke (0.3s plus one breath), and the hills spread from the middle as it closes
  (`--bloom-delay` 1400). Reduced motion: no mask, no animation, everything shown at once. With
  JavaScript off the circle is whole too.
- The circle waits for its picture (October 8, 2026). CSS started the sweep when the page was
  styled, not when the stroke's picture was in, so on a slow link the gold rose alone on bare paper
  (about 3s) and then the circle snapped in, or showed part drawn. Now, with script on
  (`@media (scripting: enabled)`), the stroke's and the gold's animations are paused before their
  delays (their backwards fill keeps the stroke masked and the gold at 0) until the stroke's
  picture is in, then both are let go together, so the gold still follows the stroke by 0.3s plus
  one breath. Two keys, neither touching a node React rendered before it hydrates: an inline script
  after the page's HTML (`src/app/[locale]/about/page.tsx`) adopts a constructed sheet that sets
  `[data-enso] img` running; once hydrated the Opening sets `data-stroke="ready"` on the circle
  (Next's `onLoad` plus a check on mount). Neither has a timer, and a failed picture never lets
  them go: the circle waits for its picture however late it comes, and the gold never rises alone
  on bare paper (if the picture never arrives, neither shows). The script is rendered through
  `before-hydration.tsx` (server HTML only), so a client-side navigation to /about neither builds a
  dead script nor logs React's "Encountered a script tag" warning; the hydrated key covers that
  case. With script off, or in a browser that does not know `scripting`,
  nothing is paused (as before).
- The rhythm is the album's (Mo's rule: one picture on one side, its words on the other, the sides
  swapping part by part from 960px; 600 to 959px is one centred column about 640px wide, picture
  first; a phone is one column, picture first), on the shared `spread.tsx` and
  `about-page.module.css`. The paper is the kit's plain rice paper (no folds, no ageing), and the
  name is said once (the logo, then the title "Be in Good Health." in plain ink).
  - Our purpose, picture left: B's oak seedling with its gold acorn.
  - Our scientific roots, picture right: Dr. Liu's real photo (`public/images/jiankang-liu.jpg`) on
    its paper mount, resting on a wide, low pool of grey wash (D's pool, turned a quarter round
    inside a box of its own shape so the page keeps room for the whole wash; on a phone the pool
    reaches to 8px from the window's edges so the photo is not a thumbnail).
  - Our experience, picture left: B's giant sequoia (a touch of gold on the old trunk).
  - Our promise: the one centred row of four small round ink dots (D's, deep black to pale grey),
    bigger than the shared size (84 to 132px).
  - Curious about the science?, picture right: round reading glasses on an open notebook, a touch
    of gold leaf on the hinge.
  - "Illustration" under the seedling, the sequoia and the glasses; none under the photo or the
    dots.
- Sizes: each painting's height is a multiple of one plain height, `--h` (`circle.module.css`: the
  seedling 1.2, the sequoia 1.35, the glasses 0.72), and its width that height times its shape,
  capped by its column. `--h` is 330px or 0.6 of the column's width, whichever is less (300px or
  0.7 of it under 960px). From 960 to 1279px the sequoia and the glasses take a plain height of
  300px (at 960 to 1100px the words beside them, stacked figures and pills, stand taller than a
  painting from 0.6 of the column). Each
  painting's `sizes` attribute (`SEEDLING`, `SEQUOIA`, `GLASSES` in `about-ink.tsx`) follows the
  width it is drawn at (within 3%, measured at 21 window widths from 360 to 1920px); if the CSS
  widths change, change those too.
- Paintings that bloom in as they arrive are server-marked `data-bloom="waiting"` (the circle draws
  itself instead; the gold leaf catches the light after). Reduced motion shows them at once.
- Deep links `/about#purpose`, `#roots`, `#experience`, `#promise`, `#closing` land each part's
  first content 0 to 64px under the header. The shared rule is the `scroll-margin-top` on `.part`
  in `about-page.module.css`.
- Files: `src/components/about/about-ink.tsx` (the page: `data-about="circle"`; its `ALT` holds the
  three painting descriptions), `circle.module.css` (C's own: the opening, the circle's mask, the
  hills, the pool and the per-part sizes, all under `.circle`), `spread.tsx` (`Painting` and
  `Spread`), `about-page.module.css` (rules shared with B, all under `.aboutPage`), `about-art.ts`
  (generated by `reference/ink-pages/about-bc/build_bc.py` from the originals in
  `reference/ink-pages/about-bc/`; pictures in `public/images/about-bc/`), `about-content.ts` (the
  locked words), `greetings.tsx`, `count-up.tsx`. `about-art.ts` still exports B's book, desk, lamp
  and four vignettes (the file is generated and shared by both branches; C does not use them).
  Spend for the paintings is in `reference/ink-pages/spend.md` (the "About B and C" section).
- Draft translations (Korean, Japanese, Simplified Chinese, Vietnamese; for a native check before
  launch): the glasses' description, key m593, added by
  `reference/ink-pages/about-bc/translations-c.cjs` (the seedling and sequoia descriptions, m589
  and m591, are B's, from `translations-b.cjs`; B's book, desk and lamp descriptions, m588, m590
  and m592, stay in the catalogs and nothing on C uses them). The photo's description is Dr. Liu's
  name in each language (in Korean and Japanese it stays "Dr. Jiankang Liu"). The opening's
  circle, the hills and the dots have no description (decorative, `alt=""`).
- Checks: `python -X utf8 scripts/qa/qa_about.py http://localhost:3025` (dev) or
  `http://localhost:3026` (built site; the built site orders CSS differently, so run both).
  Groups: `desktop_and_phone`, `rhythm`, `motion`, `focus`, `deep_links`, `languages`,
  `languages_layout`, `nav_locales`, `boundary`, `first_screen` (`--only=` runs some). It covers the
  h1 and the locked words, every painting multiplying onto the paper (with no stacking context
  between it and the page root), the rhythm and the sides, the circle appearing once, the name
  once, text, navigation and target sizes, no sideways scrolling, the Support and Ask sheets,
  reduced motion complete and still, the circle drawing itself (stopped in the frame its clock
  reaches 1.1s it must be part drawn, the last quarter under half its ink, then whole; with
  JavaScript off every quarter as inked as the still circle, and every other painting as inked as
  it is still), the bloom, deep links at five sizes, and every language's words and line breaks
  (Japanese and Chinese heading phrases on phones and at 960px, the narrowest two-column words
  column): 299 checks, all passing on the dev server and on the built site on October 7, 2026
  (after the final fix round). Screenshots go to `scripts/qa/out/about-circle/` (the built site's,
  read by hand, to `scripts/qa/out/about-circle-built/`, and the opening and the seam under the
  hills after the final fixes to `about-circle-built2/`). On the built site the homepage gate also
  passed (`home_snapshot.py compare` against `baseline-main997-prod`: 48 of 48 shots, at most
  0.008% of pixels differing, last run after the final fixes; before them also `qa_home_ink.py`,
  282/282, and `home_snapshot.py nav`, ok). October 8 (the circle waits for its picture): `motion`
  adds three slow-link checks (the stroke's picture held 3s: 2.5s in nothing shows; the stroke
  starts only once its picture is in; the gold rises a breath after it), red on the old code;
  341 checks, all passing on the dev server (not yet run on the built site).

## Replaced: "The name, on a folded letter" (D, October 6, 2026)

Replaced by B and C on October 7 (Mo rejected it; see above). The notes below are D's, kept for
reference: its files (`chapter-word.tsx`, `about-letter.module.css`, `letter-art.ts`,
`acronym.tsx`, `acronym.module.css` and its own `about-ink.tsx`) live on branch `ink-pages` only,
and its checks (`letter_layout`, `fold_header`, the 382) are no longer in `qa_about.py` on this
branch.

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
  brush route, the site header and footer, the Support and Ask BiGH Science sheets). D's own
  `acronym.tsx` (the h1 unfold) is on `ink-pages` only; `about-content.ts` (the words),
  `greetings.tsx` and `count-up.tsx` are still in use on both new pages. The site header is the menu bar Mo picked on October 5,
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
The h1 stays English "Be in Good Health." with `lang="en"` in every language (set in `about-ink.tsx`;
the line under it is translated). The four section labels (Our purpose, Our scientific roots, Our
experience, Our promise) stay.

## Languages

Korean, Japanese, Simplified Chinese and Vietnamese. The page uses the About keys m545 to m574
(September 28), "Illustration" (m574) and "Illustrations" (m582), the shared header, footer and
sheet keys, and the painting descriptions: m588 to m592 (B's five, new with B; C uses m589, the
seedling, and m591, the sequoia) and m593 (the glasses, new with C). The tab title uses the
shared "About" key. `hken.json` stays `{}`, and `/hken/about` redirects to `/cns/about`.

Draft translations, not native-reviewed: the About keys m545 to m574 and m588 to m593. (m587, D's
tree rings, is still in the catalogs; nothing on B or C uses it. The Vietnamese for it says "Vân gỗ"
where "vòng tuổi" may be the right words, if D ever comes back. m588, m590 and m592, B's book,
desk and lamp, are unused on C.)

Vietnamese uses Be Vietnam Pro site-wide (see `docs/header-and-languages.md`, "Vietnamese type").
Line breaks are scoped to this page in `about-page.module.css` ("Other languages"): Korean headings keep words whole;
Japanese breaks between phrases (`auto-phrase`, Chrome and Edge only) with `line-break: strict`;
Chinese keeps phrases whole (`keep-all`), so put a comma where a line may end; Japanese and Chinese
headings get a size that keeps their longest phrase on one line on phones and at 900-959px; the
Vietnamese closing pills balance their lines on phones.

## Check

`python -X utf8 scripts/qa/qa_about.py http://localhost:3025` (dev) or `http://localhost:3026`
(built site, `next start`; the built site orders CSS differently, so run both). Groups and counts
are in the C section above; the file's docstring lists what each checks (the h1 and the locked
words, every painting multiplying onto the paper with no stacking context between it and the page
root, the rhythm and the sides, the circle once, the name once, text, navigation and target sizes,
no sideways scrolling, the Support and Ask sheets, the circle drawing itself and reduced motion,
the bloom, deep links, and every language's words and line breaks). Screenshots go to
`scripts/qa/out/about-circle/`.

The homepage must not change: also run `scripts/qa/qa_home_ink.py <url>` and
`scripts/qa/home_snapshot.py compare <url> <new-tag> baseline-main997-prod` (built site) or
`baseline-main997` (dev), and `scripts/qa/home_snapshot.py nav <url> -` (the menu bar on / and
/about).

## Traps

- `var(--font-sans)` is EMPTY (Tailwind `@theme inline` never emits it): use `--sans` or
  `--font-dm-sans`.
- Scope component CSS under the page's root class: `homepage.module.css` resets `.site p`,
  `.site button`, `.site h2` at specificity 0,1,1, and the kit uses `.look ...` (0,2,0). Every
  About rule is scoped under `.aboutPage` (shared with B) or `.circle` (C's own).
- Multiply: a painting multiplies onto the page root's paper only if nothing between it and the
  root makes a stacking context (no z-index on a positioned ancestor, no isolation, opacity,
  transform, filter or will-change on a part, a spread, a figure or a wrapper). The kit's bloom puts
  its mask and filter on the painting itself, which is fine.
- Replacing a picture under the same file name: delete `.next/cache/images` and
  `.next/dev/cache/images` before building, or the old optimized picture is served.
- An inline `<script>` placed straight in the page's tree runs on a first load, but after a
  client-side navigation React builds it without running it and, in development, logs
  "Encountered a script tag while rendering React component". Render a before-hydration script
  through `src/components/about/before-hydration.tsx` (server HTML only), and keep a hydrated key
  for pages reached by navigation. `next/script`'s `beforeInteractive` belongs in the root layout
  only and does not promise to run before hydration.

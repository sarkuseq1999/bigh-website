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
`--lead-weight`, `--lead-track`). It loads from Fontshare in main's locale layout
(`src/app/[locale]/layout.tsx`). Headings sit at -0.02em in all; tighter closes Switzer's word
spaces. NEVER commit the Switzer font files: the licence forbids redistribution and the repo is
public. CJK and other scripts fall through to the locale fonts in `globals.css`.

## Follow-ups (TODO)

- The header and footer are this page's own copy (`site-chrome.tsx`); fold them into the shared
  site header/footer.
- Point `routes.scientists` at `/science` once the Science page lands.

## Words

Locked words: `about` in `about-content.ts` (use verbatim). DRAFT extras (`drafts`: greetings,
languages, "Illustration") need Mo's OK before launch. Facts: formula ~23 years (show "20+"); never
name CellGen or say Asia knew it first; GMP-certified maker in California (confirm the
certificate); 45-day refund current; BiGH incorporated 05/11/2016.

## Languages (Sept 28, 2026)

- Translated into Korean, Japanese, Simplified Chinese and Vietnamese: 67 strings (37 already had
  keys and are reused, such as the header, footer and the two panels; 30 new keys, m545–m574), plus
  the tab title, "BiGH — " and the existing "About" key. `hken.json` stays `{}`. `/hken/about` now
  redirects to `/cns/about`, as the homepage and product pages do (before, it showed English and
  logged an invalid-locale error).
- DRAFT translations, not native-reviewed. Same understated voice; no new claims. Names and terms
  follow the catalogs; credits follow m198's style (NuriCell by Dr. Liu alone, Nature Calm by Dr. Liu
  with Dr. Iris Wang). Some Chinese and Japanese lines were reworded slightly so they break well (below).
- The title stays English everywhere: "Be in Good Health." with the unfold, `lang="en"`, because it is
  what the name BiGH stands for; the translated lead under it explains it. To show translated titles
  instead, set `TITLE_ALWAYS_ENGLISH = false` in `acronym.tsx` (one line). The glass after "Health."
  then sits the same in every language (checked in Japanese at three sizes).
- Line breaks (CSS scoped to this page): Korean keeps whole words (globals.css). Japanese breaks
  headings, labels and the promises between phrases (`word-break: auto-phrase`, Chrome and Edge
  only) and never starts a line with small kana, "ー" or closing punctuation (`line-break: strict`).
  Chinese headings, labels and promises break only at punctuation (`keep-all`): when editing them,
  put a comma where a line may end and keep each phrase to 12 characters or fewer, or a lone "。" can
  land on a line at 1100 px. Headings get line-height 1.26 in CJK; Japanese and Chinese drop the
  negative tracking. Non-English number labels and the footer tagline wrap evenly (`balance`).
- Vietnamese font: Switzer (as Fontshare serves it) has no Vietnamese stacked or hooked letters.
  It lacks 92 of the 134 Vietnamese letters (ơ, ư, and every ạ ả ấ ầ ẩ ẫ ậ ẹ ẻ ẽ ế ề ể ễ ệ ọ ỏ ố ồ ổ ỗ
  ộ ớ ờ ở ỡ ợ ụ ủ ứ ừ … form), checked in its cmap. Chrome then draws those letters one by one in
  Arial (DM Sans, next in the stack, has no Vietnamese subset at all, so it can't help): the
  Vietnamese purpose heading is 92 Switzer glyphs and 17 Arial glyphs (DevTools protocol), and it
  shows up close (`scripts/qa/out/about-i18n/vn-font-mix-purpose.png`). This affects every
  Switzer text in Vietnamese, header included. Not changed: the site-wide font loading is Mo's call
  (one option: a face with a `vietnamese` subset in next/font, such as Be Vietnam Pro or Inter, for
  `:lang(vi)` only).

## Check

`python -X utf8 scripts/qa/qa_about.py http://localhost:3009` (real GPU by default; add
`--swiftshader` for the software renderer): 101 checks on Sept 28 (after the translations), including
Switzer loaded and first in every text role, the opening glass never touching a letter at six sizes,
chapters taking turns (sampled every 40 px), reduced motion, no WebGL, footer, and per language: the
catalogs (keys, same key sets, placeholders), 200 with no console errors, the English h1, the
translated tab title, no English source sentence left (page, panels, aria-labels, alt texts), no
lone character or line-initial punctuation, `/hken/about` → `/cns/about`, and the Japanese opening
glass. Also `npx prettier --check src/components/about messages src/i18n`, `npx tsc --noEmit`,
`npm run lint`. Review screenshots: `scripts/qa/out/about-final/` (English) and
`scripts/qa/out/about-i18n/<kr|jp|cns|vn>-<desk|phone>-N-<part>.png` (1575x940 and 390x844).

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

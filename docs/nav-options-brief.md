# Menu bar options — builder brief (October 5, 2026)

Mo (the owner, non-coder, decides by looking) picked the crane homepage, "Ink & Gold". She now wants
two or three designs for the **menu bar** (the site header) whose vibe matches that homepage. She will
pick one from videos and screenshots. Her bar for homepage work is **9 out of 10**, judged from real
screenshots at full size, the way a visitor sees the page. Passing checks is not the same as good design.

## Where you work

- Worktree `C:\Users\mcbig\Documents\codes\bigh-nav`, branch `nav-options` (local only; never push,
  never commit — the lead commits). Dev server already running: http://localhost:3027 (HMR). Do not
  start another server and do NOT run `npm run build` (it would fight the dev server's `.next`).
- Your option renders at `http://localhost:3027/?nav=<a|b|c>` (the review chip in the bottom-left
  corner flips options; Alt+H hides it; `&rec=1` removes it). `?` alone = today's bar, for comparison.
- Read first: `DESIGN.md` (the homepage's design system: Overview, Colors, Navigation, Menu, Sheets),
  `src/components/home-v2/chrome.tsx` (today's bar = `TodayHeader`) and `chrome.module.css`,
  `src/components/home-v2/look-ink/look-ink.module.css` (tokens; header overrides at the top),
  and the scaffolding in `src/components/home-v2/nav/`:
  - `nav-data.ts` — the links, the five products (real bottle PNGs, names, focus lines, page links),
    the Science page's four parts with their paintings and captions. Every string there already
    exists on the site (translated). Do not invent new visible words; if you truly need one, use an
    existing string from `content.ts` or the footer, and tell the lead.
  - `use-nav.ts` — shared behaviour: `solid` (scrolled past the opening's first pixels), `direction`,
    the desktop drop-down `panel` (hover-intent open/close, click toggle, Escape returns focus,
    outside click and page scroll close it) with `triggerProps(id)` / `panelProps(id)`, and the narrow
    window's `menuOpen` sheet (scroll lock, Escape, closes on growing to desktop) + `onHeaderBlur`.
    Use it. If it is missing something you need, extend it carefully (the other two builders use it
    too: additive changes only, nothing that changes existing behaviour) and say so in your report.
  - `nav-logo.tsx` — the BiGH mark; size it with `className` (width). `light` = white mark.
  - Images: `public/images/home-v2/nav/brush-1..7.webp` — seven real sumi-ink brush strokes (black
    on transparent, ~1:9, wavy, loaded left end, dry-brush flying-white tail on the right), made for
    this work; good as CSS masks (`mask-image`) on a `currentColor` element. Paintings in
    `public/images/home-v2/ink/` (ink with the paper divided out — show them with
    `mix-blend-mode: multiply` on paper): `mito.webp` (cell), `inkstone-v2.webp`,
    `story-reading-v2.webp`, `crane-rest-v2.webp` (the crane standing), `crane.webp`,
    `purpose-land.webp`, `landscape.webp`; `paper.webp` is the page's rice-paper fibre (800px tile).
    Dr. Liu's real photo: `/images/jiankang-liu.jpg` (a photo, never multiplied: on a paper mat).
    Bottles: `/images/products/<slug>.png` (approved, transparent; never redraw or generate bottles).
- Your files: `src/components/home-v2/nav/nav-<yours>.tsx` + `nav-<yours>.module.css`, and any new
  assets under `public/images/home-v2/nav/<yours>/`. Touch nothing else except additive changes to
  `use-nav.ts` (announce them). Other builders are editing the sibling files at the same time.
- Your component receives `HeaderProps` (`overlay`, `tone`, `solidAfter`) and renders the whole
  `<header>` (bar + drop-down panels + narrow-window menu). Support opens a sheet:
  `useHomeDialogs().openSupport()` from `../dialogs`. Log in / Sign up / language picker: reuse
  `HeaderUtilities` from `@/components/home/header-utilities` and restyle it from YOUR stylesheet
  only, scoped under your root class (see how `chrome.module.css` does it under `.header`).

## Contract (the screenshot script drives these)

- Desktop drop-down buttons: `data-nav-trigger="products"` / `"science"`; their panels
  `data-nav-panel="products"` / `"science"`.
- Narrow-window menu button: `data-nav-menu-button`; the open sheet: `data-nav-sheet`; a Products
  disclosure inside the sheet (if your design has one): `data-nav-sheet-toggle="products"`.
- Use `id="site-navigation"` for your `<nav>` — NOT `home-navigation` (look-ink.module.css restyles
  anything under `#home-navigation`). Beware `.look :global(header) a[href]:first-child:has(img)`
  in look-ink.module.css: it forces the first logo link's width to ~98px; beat it with your own
  scoped selector if you size the logo differently.
- The homepage resets `.site p / button / h2` style in places: scope every rule under your
  component's root class so single-class rules don't lose silently.

## The links

The logo goes home (no separate "Home" link in the options). Then: **Products ▾** (drop-down:
the five bottles → `/products/<slug>`, plus "Explore our products." → `/#products`), **Science ▾**
(drop-down: the four parts → `/science#…`, plus "Explore the science" → `/science`), **About**
(`/about`), **Support** (opens the Support sheet). Then Log in, Sign up, language.

## Non-negotiables (from DESIGN.md and Mo's Design Vault)

- Ink on rice paper. Sumi ink `#0c0b0a`, ink grey `#514e48`, rice paper `#f8f3ea`, hairlines
  `rgba(28,27,25,.16/.28)`. **No gold on any UI element** (gold lives only inside paintings).
  **No red, no seals, no drop shadows, no gradient fills, no glassy blur cards.** Sentence case,
  never letter-spaced capitals. Switzer (the page's `--sans` / `--display-font`), 400/450/500.
- Older readers (40–65): navigation text **≥ 18px** (20px at 1536), every target **≥ 48px**, the
  logo clearly visible (Mo saved Timeline's tiny header as an AVOID: "too small for older
  customers"). Words, not bare icons (a menu button may say "Menu").
- Mo's saved LIKES for menus: Timeline's drop-down (Design #004: simple, not boring, clear — big
  list of links on the left, three pictures with captions and arrows on the right, full-width
  under the bar) and Seed's Shop drop-down (#039: a big rounded panel, products as rows with small
  bottle thumbnails, calm, easy to scan). The current bar's behaviour: clear over the opening
  painting, 93% paper + hairline once scrolled 48px, 80–90px tall.
- Motion breathes slowly: `--breath: 2.4s`, ease `var(--ease)` = cubic-bezier(.22,.61,.36,1);
  panels arrive in ~0.6–0.9s and leave in ~0.25–0.3s. `prefers-reduced-motion`: everything simply
  there / gone, no movement.
- Keyboard: Tab order sensible, visible focus ring (2px ink, offset 4px), Escape closes, focus
  returns to the button. Drop-downs work by click/Enter too (not hover-only). Touch laptops: tap
  toggles. The narrow-window sheet scrolls by itself (`data-lenis-prevent` while open).
- Widths that must look designed, not merely survive: 390x844 (phone), 834x1112 (tablet, menu),
  1101–1220 (tightest desktop; Vietnamese and Japanese run long — check `/vn/?nav=…` and
  `/jp/?nav=…`), 1280x800, 1536x900, 1920x1080. The opening painting runs under the bar: the
  crane's wingtips start ~135px down at 1536x900 — the bar must not crowd them.
- Paintings are ink on paper: on paper use `mix-blend-mode: multiply`; on dark ground show them on
  a paper leaf. Bottles are photos: they need a pale pool / ground under them, never a box.

## How to check your work

1. `python -X utf8 scripts/qa/shoot_nav.py <a|b|c>` (add `--locale vn` / `--locale jp` for the
   long languages; `--only desk|phone|tablet`) → PNGs in `scripts/qa/out/nav/<option>/`.
2. LOOK at every PNG at full size with the Read tool, as a picky senior designer and as a 60-year-old
   visitor. Write down a score out of 10 with reasons (type, spacing, alignment, how it sits on the
   crane painting, the drop-downs' composition, the phone sheet, "does it look generated or
   template-y?"). Anything a first-time visitor would read as a mistake is a defect, whatever your
   intent. Fix the weakest points and re-shoot. Iterate until **≥ 9** honestly (max ~4 rounds).
3. `npx prettier --write <your files>`, `npx eslint <your files>`,
   `npx tsc --noEmit -p .` (ignore errors in other builders' files; yours must be clean). Files are
   LF; never `git stash`/`checkout`.
4. Test the behaviour for real with Playwright: hover opens, moving into the panel keeps it, leaving
   closes; click toggles; Escape returns focus; Tab through; the phone sheet opens, locks the page,
   closes on Escape and ✕; Support opens its sheet; a product link navigates to its page.

## Report back (short)

What you built (the idea in two lines), the files, the screenshot folder, your honest score with the
one or two things still holding it back, any `use-nav.ts` changes, and any new strings.

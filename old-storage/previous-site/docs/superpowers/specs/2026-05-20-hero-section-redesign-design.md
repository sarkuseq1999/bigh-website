# Hero Section Redesign — Design Spec

**Date:** 2026-05-20
**Section:** Homepage section 1 (`Hero`), the first section on `src/app/[locale]/page.tsx`
**Status:** Approved, ready for implementation planning

## Overview

A full redesign of the homepage hero. It is a brand-statement / manifesto
moment: a single typographic claim — *"Your mind has no expiration date."* —
set against a cinematic looping aurora background. The hero owns the worldview;
the science and product reveal in the sections below it.

The visible result is a full-bleed dark hero with a slow, seamlessly-looping
aurora video filling the upper-right two-thirds, a dark gradient fade on the
lower-left third for type legibility, and a confident lower-left content stack
(headline, subhead, one CTA, scroll cue). The image and the headline share a
vocabulary: *eternal, undimmed, unending.*

It replaces the current `src/components/site/hero.tsx` entirely.

## Goals

- Deliver one quiet, monumental brand statement instead of a busy split-layout.
- Use cinematic motion (a real looping video, not CSS overlays) so the hero
  feels alive on every visit while remaining calm and premium.
- Keep accessibility intact: full reduced-motion fallback, no autoplay issues
  on mobile, type legibility never relies on a specific video frame.
- Introduce no new dependencies; use only the libraries already in the project
  (`motion/react`, `next/image`, native `<video>`).

## Non-goals / out of scope

- Wiring the primary CTA to a real route. The CTA scrolls to section 2;
  routing across the site is a separate task.
- Generating localized aurora videos or providing real localized copy. Locale
  files mirror the new English keys with English placeholders; translation is
  a follow-up.
- Mobile-specific video variant. We ship the same 2.1 MB MP4 to all devices
  for v1; a separate lower-res mobile encode is a follow-up optimization.
- Deleting `public/hero/hero-76-star-trails-ridge.jpg`. The old image stays on
  disk (unused) so it can be referenced or restored without re-checkout.
- Changes to any other section or to `page.tsx` (the `Hero` import and export
  name are preserved). The only out-of-file change is a single `id="yourmind"`
  attribute added to the section 2 root — see [Primary CTA behavior](#primary-cta-behavior).

## Content (final, approved copy)

All copy lives under the existing `Hero` namespace in the message files.

| Key | Value |
|-----|-------|
| `headline` | `Your mind has no <em>expiration date.</em>` |
| `subhead` | `Sharpness at every age isn't luck — it's nature and science. BiGH gives your brain the fuel and protection it needs — in one daily ritual.` |
| `cta` | `Continue` |
| `scrollCue` | `Scroll` |
| `imageAlt` | `Slow amber aurora over a distant mountain horizon` |

The `headline` value uses the same `<em>` rich-text tag pattern as the current
hero. `t.rich("headline", { em })` renders the sienna italic accent.

### Keys removed from `Hero` namespace

- `ctaSecondary` — removed (single-CTA hero)

### Section-2 phrase overlap

The phrase *"fuel and protection"* appears in both the hero subhead and in
`messages/*.json` under `YourMind.body` ("a brain needs just two things to stay
extraordinary: protection, and fuel"). This is an intentional brand-master-phrase
pattern, approved during brainstorming: the hero establishes the phrase, section 2
develops it. No section-2 changes are required for this hero to ship. A
future revision of `YourMind` may want to recast its line as a development of
the hero's claim rather than a statement of it — out of scope here.

## Layout & composition

### Section element

- Full-bleed: `<section>` with `relative`, `isolate`, `overflow-hidden`,
  `min-h-[100dvh]`. Dark base background (`bg-[#0a0a1a]`) so any video
  load-flash blends.
- Padding: `px-6 py-16` on mobile, `px-14 py-24` on desktop (match the
  existing hero scale).
- No top spacing for nav — the nav floats over the hero.

### Composition (C1 · lower-left anchor)

- **Nav (`SiteHeader`):** floats over the hero as it does today — see
  [SiteHeader interaction](#siteheader-interaction) below for the required
  visual changes. The hero's content stack sits well below the header
  (`bottom: 8%`), so there is no z-order or overlap concern for the content
  itself.
- **Content stack:** absolutely positioned at `left: 5%` `bottom: 8%`,
  `max-w-[58%]` on desktop. On mobile (sub-`md`), full-width with
  `left: 6%`, `right: 6%`, `bottom: 12%`.
  Vertical order: **headline → subhead → CTA**.
- **Scroll cue:** small uppercase label, centered horizontally at the bottom
  edge, ~24px from the bottom. Hidden on `prefers-reduced-motion: reduce`.
- **No eyebrow.** Confirmed during brainstorming — the headline carries the
  full weight.

### Typography

- **Headline** — serif (the site's `--font-display`), `font-weight: 300`,
  fluid size `clamp(2.5rem, 6.4vw, 4.875rem)`, `line-height: 1.02`,
  `letter-spacing: -0.025em`, `text-wrap: balance`. Color `cream-50`.
  - `<em>` (the "expiration date" span): color `sienna`, italic
    (`font-style: italic`), weight `400`. No underline; the italic and color
    carry the emphasis.
- **Subhead** — sans, `clamp(0.95rem, 1.2vw, 1.125rem)`, `line-height: 1.62`,
  `max-w-[560px]`, color `rgba(250, 246, 239, 0.82)` (cream at 82% opacity for
  a soft second-rank read).
- **CTA pill** — cream background, espresso text, `rounded-full`, `~14px/28px`
  padding, `14px` medium label, trailing arrow icon. Hover: background →
  `sienna`, text → `cream-50`, lifts 1px, arrow nudges right (reuse the
  existing site CTA hover treatment).
- **Scroll cue** — sans, `10px`, uppercase, letter-spacing `0.32em`, color
  `rgba(250, 246, 239, 0.5)`, with a 1px × 18px vertical line below it at
  `rgba(250, 246, 239, 0.35)`.

### Dark gradient overlay (for legibility)

A single absolutely-positioned `<div>` between the video (`z-1`) and the
content (`z-5`), at `z-2`:

```css
background:
  linear-gradient(95deg,
    rgba(15, 10, 25, 0.85) 0%,
    rgba(15, 10, 25, 0.55) 28%,
    rgba(15, 10, 25, 0.12) 52%,
    transparent 72%),
  linear-gradient(180deg,
    transparent 50%,
    rgba(15, 10, 25, 0.55) 100%);
```

The first gradient darkens the left third (where the type sits). The second
darkens the bottom edge so the scroll cue and CTA remain readable against the
brightest aurora frames.

## Background — video + still fallback

### Assets (already on disk in `public/hero/`)

| File | Purpose | Size |
|------|---------|------|
| `aurora-loop-1.5x.mp4` | Looping video, primary background | 2.1 MB |
| `candidate-aurora.jpg` | Poster + reduced-motion fallback + LCP image | 2.8 MB |
| `hero-76-star-trails-ridge.jpg` | Old image, kept on disk, unused | — |

### Video element

```html
<video
  autoplay
  muted
  loop
  playsInline
  preload="auto"
  poster="/hero/candidate-aurora.jpg"
  class="absolute inset-0 w-full h-full object-cover z-0"
  aria-hidden="true"
>
  <source src="/hero/aurora-loop-1.5x.mp4" type="video/mp4" />
</video>
```

- `playsInline` — required for iOS Safari to play inline rather than fullscreen.
- `muted` — required to satisfy autoplay policies across browsers.
- `aria-hidden="true"` — the video is decorative; the `imageAlt` on the
  reduced-motion `<img>` carries the accessible description.
- `preload="auto"` — small enough (2.1 MB) that prefetching is acceptable for
  the hero on a hero page.
- `poster` — the still image shows during load, then the video takes over
  seamlessly when ready.

### Reduced-motion fallback

When `useReducedMotion()` returns `true`, render an `<img>` instead of the
`<video>`:

```html
<img
  src="/hero/candidate-aurora.jpg"
  alt="{t('imageAlt')}"
  class="absolute inset-0 w-full h-full object-cover z-0"
/>
```

The reveal sequence (below) is also skipped in this case — all content renders
in final state immediately.

## Motion — reveal sequence

Built with `motion/react` (already a dependency). The hero is above-the-fold,
so the reveal triggers on mount, not on scroll. Easing
`cubic-bezier(0.2, 0.7, 0.2, 1)` (the site's standard `ease`).

| Step | Element | Delay | Motion |
|------|---------|-------|--------|
| 1 | Video element | 0s | begins autoplay (no CSS reveal) |
| 2 | Headline | 0.30s | fade (opacity 0 → 1) + rise (translateY 16px → 0), duration 0.9s |
| 3 | Subhead | 0.70s | fade + rise (12px), duration 0.9s |
| 4 | CTA | 1.00s | fade + rise (12px), duration 0.9s |
| 5 | Scroll cue | 1.40s | fade only (opacity 0 → 1), duration 0.9s |

The reveal plays once per page load (not on every navigation, which Next.js's
client-side routing means is automatic — the `<Hero>` component re-mounts on
route change anyway).

## SiteHeader interaction

The existing `SiteHeader` (`src/components/site/site-header.tsx`) is already
`position: absolute` over the page (`top-0 right-0 left-0 z-50`). Today it
renders with:

- `bg-cream-50/70` background with `backdrop-blur-md`
- Dark text (`text-espresso`) on nav links
- A dark logo (`logo-black.png`, with a `dark:`-class light variant)
- An espresso/15 separator before the language switcher

On the new dark hero, this cream pop + dark text looks mismatched and the
dark logo becomes nearly invisible against the aurora. The hero design
assumes the header is rendered in **dark-context mode** while the hero is in
view: transparent (or dark-translucent) background, cream/light text, the
light-logo variant, a cream-tinted separator.

**Required:** the `SiteHeader` gains a scroll-aware state. While the hero
section is in view (top of page, before the user has scrolled past the hero),
the header renders in dark-context mode. Once the user scrolls past the
hero, it transitions back to its current cream-light state for the rest of
the page (where the page background is light again).

**Implementation guidance** (deferred to the plan, not prescribed here):

- An `IntersectionObserver` on the hero section is preferred over a scroll
  listener (better performance, declarative).
- The transition between states should be a short opacity/color crossfade,
  not an instant snap.
- The mobile menu trigger needs the same dark/light awareness.
- The language switcher needs the same dark/light awareness.

If the implementer determines that a scroll-aware header is too large a
scope item for this task, the acceptable fallback is to ship the header
locally overridden by the hero — i.e., the hero renders its own inline
nav-row over the video and the global `SiteHeader` is suppressed on the
homepage. This is the cheap path and creates code duplication, so it should
only be chosen if scroll-aware state is genuinely out of scope.

## Primary CTA behavior

The CTA scrolls smoothly to section 2 (`YourMind`).

- **Implementation:** the CTA is a `<button>` (not an `<a>`), with an
  `onClick` handler that calls `document.getElementById("yourmind")?.scrollIntoView({ behavior: "smooth", block: "start" })`.
- **Required change in `src/components/site/your-mind.tsx`:** add
  `id="yourmind"` to the `<section>` element at line 101 (the only
  out-of-file change).
- **Fallback:** if the element is not found (defensive), `window.scrollTo({ top: window.innerHeight, behavior: "smooth" })`.
- **Reduced motion:** if `useReducedMotion()` returns `true`, the scroll
  behavior is `"auto"` instead of `"smooth"` (no animated scroll).

## Reduced motion

Under `prefers-reduced-motion: reduce` (detected via `useReducedMotion()` from
`motion/react`):

- Replace `<video>` with `<img>` (the still poster image).
- Skip the staged reveal — `motion.div` `initial` and `animate` are set to the
  same final state (or `motion` wrappers are not used and content renders
  directly).
- Scroll cue is hidden (it implies motion).
- Primary CTA scroll uses `behavior: "auto"` instead of `"smooth"`.

## Component structure

- File: `src/components/site/hero.tsx` — rewritten in place. Keeps the
  `Hero` named export, so `src/app/[locale]/page.tsx` is untouched.
- Client component (`"use client"`) — required for `motion/react`,
  `useReducedMotion()`, and the `<video>` autoplay effect.
- Internal helper(s) kept in the same file (single-purpose component, no need
  to extract):
  - `AuroraBackground` — renders the `<video>` (or `<img>` under reduced
    motion) + the dark gradient overlay. Receives `imageAlt` as a prop.
  - `ScrollCue` — small visual-only component for the bottom-center cue.
- The dark-gradient overlay can be inlined in `AuroraBackground` (small,
  feature-local).

## Internationalization

- Replace the `Hero` namespace contents in `messages/en.json` with the five
  keys above (`headline`, `subhead`, `cta`, `scrollCue`, `imageAlt`).
- Remove the `ctaSecondary` key from `Hero` across **all** locale files.
- Mirror the new key structure into the other locale files
  (`ko.json`, `zh.json`, `ja.json`, `es.json`). Real translations are out of
  scope — copy the English strings as placeholders so the build does not
  break on missing keys. Localization is a follow-up task.
- The `headline` key continues to use the `<em>` rich-text tag and is
  rendered via `t.rich("headline", { em: (chunks) => ... })` exactly as the
  current hero does.

## Design tokens used

All already defined in `globals.css` — no new tokens:

- `bg-cream-50` (`#FAF6EF`) — CTA pill background, headline text color
- `text-espresso` (`#2A211A`) — CTA pill text color
- `text-sienna` (`#B85426`) — headline `<em>` accent
- Site fonts via Tailwind: `font-display` for headline, default sans for
  subhead and UI

The dark overlay color `#0a0a1a` and the cream-with-opacity tints
(`rgba(250, 246, 239, 0.82)`, `rgba(250, 246, 239, 0.5)`) are inlined — they
are local to this feature and don't need new global tokens.

## Assets list

Files added to `public/hero/` (already on disk):

- `candidate-aurora.jpg` (2.8 MB, 2K JPEG, generated via Gemini)
- `aurora-loop-1.5x.mp4` (2.1 MB, 1928×1076 H.264, 24fps, 10s seamless loop,
  derived via `ffmpeg setpts=PTS/1.5` from the Kling 3.0 source clip)

Files **not** removed:

- `hero-76-star-trails-ridge.jpg` — kept on disk for reference / quick rollback.
- `hero-41-greenhouse.jpg` — unchanged (used elsewhere or kept as legacy).

## Testing / acceptance

- Hero renders on `/en` as the first section of the homepage, dark background,
  no horizontal overflow at mobile/tablet/desktop widths.
- The aurora video autoplays muted on first visit (Chrome, Safari, Firefox,
  Edge desktop) and on iOS Safari mobile (via `playsInline` + `muted`).
- The video loops without a visible cut. Watch through at least two full
  cycles (~20 seconds).
- The still image (`candidate-aurora.jpg`) is visible as the poster during
  the video's initial fetch, with no flash of unstyled background.
- The staged reveal plays once on mount in the order: headline → subhead →
  CTA → scroll cue.
- With `prefers-reduced-motion: reduce`:
  - `<img>` is rendered instead of `<video>`.
  - All content renders immediately (no reveal).
  - The scroll cue is hidden.
  - The CTA's scroll behavior is `"auto"`, not `"smooth"`.
- The "Continue" CTA scrolls smoothly to the YourMind section (section 2)
  and the YourMind section's `<section>` has `id="yourmind"`.
- The `SiteHeader` is rendered in dark-context mode (cream/light text, light
  logo, transparent or dark-translucent background) while the hero is in
  view, and transitions to its existing cream-light state once the user has
  scrolled past the hero.
- The CTA hover state is the same treatment used elsewhere on the site
  (background → sienna, lifts 1px, arrow nudges right).
- All five locale files have the new `Hero` key structure (no missing keys
  causing `next-intl` errors at build time).
- No new console errors. `npm run build` and `npm run type-check` both pass.

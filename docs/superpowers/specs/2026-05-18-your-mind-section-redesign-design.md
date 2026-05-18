# YourMind Section Redesign — Design Spec

**Date:** 2026-05-18
**Section:** Homepage section 2 (`YourMind`), between `Hero` and `BrainScience`
**Status:** Approved, ready for implementation planning

## Overview

A full redesign of the homepage's second section. It is a narrative-bridge
"moment": after the hero establishes that the mind has no expiration date, this
section argues that in the age of AI the mind is what matters most — and that
keeping it sharp comes down to protecting and fueling the brain. It hands off
into the science section that follows.

The visible result is a tall, white, centered section with a faint animated
"thought-lines" background motif and a typographic statement that assembles
itself with a staged scroll-triggered reveal.

It replaces the current `src/components/site/your-mind.tsx` entirely.

## Goals

- Deliver one unified, empowering statement — not a wall of centered text.
- The animated background should evoke "mind / thinking" while staying faint
  and calm enough never to compete with the type.
- Keep the section consistent with the existing site (warm palette, motion
  library, i18n setup) and introduce no new dependencies.

## Non-goals / out of scope

- Wiring the CTA to a real route. All site CTAs are currently `#` placeholders;
  this section follows that convention. Routing all CTAs is a separate task.
- Translating the copy into the non-English locale files beyond mirroring the
  key structure (see Internationalization).
- Changes to any other section or to `page.tsx` (the `YourMind` import and
  export name are preserved).

## Content (final, approved copy)

All copy lives under the existing `YourMind` namespace in the message files.

| Key | Value |
|-----|-------|
| `eyebrow` | `The human advantage` |
| `headlineSetup` | `Everyone is talking about artificial intelligence.` |
| `headlinePunch` | `They're missing <point>the point</point>.` |
| `body` | `The most powerful intelligence you will ever use is your own mind — your taste, your judgment, your imagination. A machine can be trained. It cannot be you. Your mind runs on a healthy brain, and a brain needs just two things to stay extraordinary: protection, and fuel.` |
| `coda` | `That's the whole idea.` |
| `cta` | `Discover the line` |

`headlinePunch` is rendered with `t.rich()` and a `<point>` tag (same pattern as
the hero's `t.rich("headline", { em })`). The `<point>` tag renders the sienna
accented span carrying the draw-in underline.

## Layout & composition

- `<section>`: full-bleed, `bg-white`, `relative`, `overflow-hidden`.
  Pure white (`#ffffff`) — deliberately distinct from the hero's `cream-50`.
- Vertical padding generous: roughly `pt-28 pb-28` on mobile, `pt-36 pb-32` on
  desktop (match the breathing-room scale of the existing section).
- A thin sienna hairline (`bg-sienna/35`, 1px tall, ~120px wide) is centered on
  the top edge and animates in (see Motion).
- Content is centered and symmetric inside a `max-w-[920px]` container; the
  body paragraph is held narrower (`max-w-[600px]`) for readability.
- Vertical order: eyebrow → headline (setup line, then punch line) → body →
  coda → CTA.

### Typography

- **Headline** — sans-serif (the site's `--font-sans`, Geist; same family used
  for the hero's "AI" word). `font-weight: 400`, fluid size
  `clamp(2.3rem, 4.5vw, 4.1rem)`, `line-height ~1.09`,
  `letter-spacing -0.032em`, `text-wrap: balance`, `max-w-[21ch]`.
  - `headlineSetup` line: color `espresso-60` (the quiet setup).
  - `headlinePunch` line: color `espresso` (full-weight punch).
  - `<point>` span: color `sienna`, `font-weight: 500`, with a 2px sienna
    underline drawn via an absolutely-positioned `::after` (or motion span).
- **Eyebrow** — sans, `~12px`, `uppercase`, `letter-spacing .32em`, italic,
  color `espresso-40`.
- **Body** — sans, `~1.1rem`, `line-height 1.72`, color `espresso/75`.
- **Coda** — sans, italic, `~1.3rem`, color `espresso-60`. Standalone line
  below the body, above the CTA.
- **CTA** — pill button: `bg-espresso text-cream-50`, `rounded-full`,
  `~16px/28px` padding, `14px` medium label, trailing arrow icon.
  Hover: background → `sienna`, gap widens, lifts 1px, arrow nudges right.
  (Reuse the hover/active treatment already used by the hero/other CTAs.)

### Background motif — "thought-lines" (B1)

- Four horizontal brainwave/contour lines spanning the full section width,
  rendered as one inline `<svg>` (`viewBox="0 0 1000 620"`,
  `preserveAspectRatio="none"`), absolutely positioned, `z-0`.
- Line paths (seamless-loop wave, period 600):
  - `M0 120 q150 -34 300 0 t300 0 t300 0 t300 0 t300 0 t300 0` — stroke `sienna`, opacity `0.30`
  - `M0 250 q150 32 300 0 t300 0 t300 0 t300 0 t300 0 t300 0` — stroke `espresso-40`, opacity `0.34`
  - `M0 380 q150 -30 300 0 t300 0 t300 0 t300 0 t300 0 t300 0` — stroke `sienna`, opacity `0.30`
  - `M0 500 q150 28 300 0 t300 0 t300 0 t300 0 t300 0 t300 0` — stroke `espresso-40`, opacity `0.30`
  - `stroke-width: 1.1`, `fill: none`.
- Each line drifts horizontally via a CSS keyframe (`translateX(0)` →
  `translateX(-600px)`, `linear`, `infinite`), with per-line durations of
  ~21s / 27s / 24s / 32s so they never sync up.
- **Focus-fade:** a white radial-gradient overlay sits above the SVG
  (`z-1`, below content at `z-2`):
  `radial-gradient(ellipse 46% 60% at 50% 48%, #fff 0%, #fff 40%, rgba(255,255,255,0) 80%)`.
  This keeps the lines full-bleed but invisible directly behind the text.
- The whole motif fades in (opacity 0 → 1) after the headline lands.

## Motion

Built with `motion/react` (already a dependency), consistent with the rest of
the site. The reveal is triggered once when the section scrolls into view
(`whileInView`, `viewport={{ once: true, margin: "-80px" }}`), matching the
existing section pattern.

Reveal sequence (approximate delays from when the section enters view; easing
`cubic-bezier(0.2, 0.7, 0.2, 1)`, the site's standard `ease`):

| Step | Element | Delay | Motion |
|------|---------|-------|--------|
| 1 | Top hairline | 0.10s | scaleX 0 → 1 (~1.6s) |
| 2 | Eyebrow | 0.15s | fade + rise 16px |
| 3 | Headline setup line | 0.30s | fade + rise 16px |
| 4 | Headline punch line | 0.80s | fade + rise 16px |
| 5 | `the point` underline | 1.40s | scaleX 0 → 1, origin left |
| 6 | Background motif | ~1.20s | opacity 0 → 1 (~1.8s) |
| 7 | Body | 1.90s | fade + rise 16px |
| 8 | Coda | 2.50s | fade + rise 16px |
| 9 | CTA | 2.85s | fade + rise 16px |

**Reduced motion:** when `prefers-reduced-motion: reduce` is set (detect via
`useReducedMotion()` from `motion/react`):
- Skip the staged reveal — all content renders in its final state immediately.
- The thought-lines render static — the horizontal drift keyframe is disabled
  (gate the CSS animation behind a `@media (prefers-reduced-motion: no-preference)`
  query, or remove the animation class).
- The underline renders fully drawn.

## Component structure

- File: `src/components/site/your-mind.tsx` — rewritten in place. Keeps the
  `YourMind` named export, so `src/app/[locale]/page.tsx` is untouched.
- Client component (`"use client"`) — required for `motion/react` and
  `useReducedMotion()`.
- Internal helper(s) kept in the same file (small section, single purpose):
  - `ThoughtLines` — the inline SVG motif + focus-fade overlay.
  - `Point` — the sienna accented span with the draw-in underline, used as the
    `<point>` tag renderer for `t.rich`.
- The horizontal-drift keyframe and the `prefers-reduced-motion` gate are
  defined in the component (inline `<style>` scoped to the section, or added to
  `globals.css` if a shared location is preferred — implementer's call, keep it
  local to this feature).

## Internationalization

- Replace the `YourMind` namespace contents in `messages/en.json` with the six
  keys above.
- Mirror the same key structure into the other locale files present in
  `messages/` (`ko.json`, `zh.json`, `ja.json`, `es.json`). Real translations
  are out of scope — copy the English strings as placeholders so the build does
  not break on missing keys. Localization is a follow-up task.
- The headline is split into `headlineSetup` (plain) and `headlinePunch` (rich,
  with the `<point>` tag) so translators can move the accented phrase naturally
  within the sentence.

## Design tokens used

All already defined in `globals.css` — no new tokens:
`bg-white`, `text-espresso` (`#2A211A`), `text-espresso-60` (`#6B5C4F`),
`text-espresso-40` (`#9C8F82`), `text-sienna` (`#B85426`),
`text-cream-50` (`#FAF6EF`).

## Testing / acceptance

- Section renders on `/en` between the hero and the science section, white
  background, no horizontal overflow at mobile/tablet/desktop widths.
- On scroll into view, the staged reveal plays once in the order above.
- The thought-lines are visible but faint, drift slowly, and loop seamlessly
  (no visible jump); they are not visible directly behind the headline.
- With `prefers-reduced-motion: reduce`, all content is immediately visible and
  the lines do not drift.
- No new console errors; `npm run build` and `npm run type-check` pass.

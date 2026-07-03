# Design

Visual system of the BiGH redesign ("Golden Hour" direction), as shipping on branch `golden-hour-home`. The old clone pages under the `(clone)` route group keep their own celadon-apothecary system and are NOT covered here.

## Theme

Dark editorial. Espresso-navy ground, silk-shader atmosphere, serif elegance, warmth delivered in ember micro-doses. Feels like dusk light on dark silk — premium-calm, never clinical. Individual sections may break to a light "daylight" scope when the narrative demands it (art direction per section; consistency of voice over consistency of treatment).

## Color — `.gh` scope (globals.css + `src/components/home/theme.ts`)

| Token | Value | Role |
|---|---|---|
| `--gh-bg` | `#04080f` | espresso-navy ground |
| `--gh-fg` | `#e6f0f7` | primary ink (on dark) |
| `--gh-muted` | `#b9cbd9` | secondary text |
| `--gh-faint` | `#6f8aa0` | tertiary / labels |
| `--gh-ember` | `#e9946a` | THE warm accent — micro-doses only (reveal phrase, CTA underline/arrow, selection) |
| `--gh-line` | `rgba(230,240,247,.12)` | hairlines |

Ember discipline: at most two ember touches at rest per screen. Silk shader palette: navy (default) / gold (`?silk=gold`, A/B retained for comparison).

For light-break sections, derive tokens from the same hues: bg tinted toward the navy (not warm-cream), ink from the espresso-navy, ember darkened to keep ≥4.5:1 on white (e.g. `#b05a2c` family).

## Typography

- **Display/serif**: Fraunces (`--font-gh-serif`, `.gh-serif`), weights 400/500/600 + italic. The brand voice: big serif statements, italic = the emotional turn (hero line 2, reveal accent).
- **Body**: Roboto (via clone base layer) for plain text.
- **Utility**: `font-mono` (system mono) 12–13px, uppercase, tracking 0.22–0.24em — kickers + CTAs only.
- CJK/VN locales: Noto Serif/Sans companions via unicode-range.
- Headline scale: hero `clamp(3.4rem, 9.2vw, 8.6rem)` leading 0.93; section statements `clamp(1.6rem, 3.4vw, 2.6rem)` leading ~1.35.

## Motion

- GSAP page-load choreography on the hero (word-by-word serif rise, then sub, then CTA; power4.out).
- Scroll reveals via the `Reveal` component (IntersectionObserver, translate+fade, stagger by `delay` prop).
- Number count-ups on stats (eased cubic, IntersectionObserver-triggered).
- three.js atmospherics: hero silk shader (fbm flow + pointer ripple drops). Canvas per section only when it serves the story; cap DPR at 2, dispose on unmount.
- **Reduced motion**: every animation checks `prefers-reduced-motion` and renders the final state instantly. Non-negotiable.

## Layout

- Full-viewport narrative screens (`min-h-svh`), one idea per fold, long scroll.
- Content column `max-w-5xl`, gutters `px-6 sm:px-12`; section padding `py-28 sm:py-36`.
- Hairline `border-t` (`--gh-line`) separates dark screens.
- Chrome: GhHeader (wordmark, 6-product menu, lang/login/signup) + GhFooter (DSHEA disclaimer lives here).

## Components (`src/components/home/`)

`hero` (silk + word-rise + ember reveal) · `truth` (screen 2, the mechanism) · `scientist` (Dr. Liu) · `nuricell` (hero product) · `family` (5 one-job cards) · `heart` · `honest` · `ritual` (CTA) · `silk` (shader) · `theme.ts` (JS tokens).

## Bans (project-specific, on top of impeccable's)

- No side-stripe borders (`border-l` accents) — replaced during the 2026-07-03 polish.
- No hype visuals (timers, badges, 10× claims) — compliance is a design constraint here.
- Ember never carries text below 4.5:1 contrast; darken it on light grounds.

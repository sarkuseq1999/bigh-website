# Hero 3D Redesign — "Ignite + Protect" (2026-06-10)

## Goal

Replace the photo-editorial hero with a stunning Three.js + GSAP hero: a living
neural scene where the brain's batteries (mitochondria → glowing gold cores)
ignite one by one, and toxic debris is visibly swept away by a protective
sweep. Dark hero that hands off into the existing cream page. Existing copy and
i18n stay.

## Decisions (approved by Mo, 2026-06-10)

- **Concept:** single-viewport "ignite + protect" scene. No scroll pinning, no
  scroll-jacking — the page scrolls normally.
- **Mood:** dark-to-light. Deep warm near-black hero (harmonizing with
  `--forest #16201B` / `--ink #1B1A17`), warm gold glows (`--amber #C28A3A`,
  `--amber-hi #DDA94E`); the teal `--glow #44CDA9` may appear sparingly as the
  "clean energy" accent. As the hero scrolls out, the site brightens into the
  existing cream (`--paper`).
- **Copy:** unchanged. (A small subhead tweak is allowed but default to no
  change so the 5 locale files stay untouched.)
- **Layout:** keep the text stack left with the same hierarchy (eyebrow →
  headline → subhead → paragraph → CTAs → ctaNote), restyled for dark
  (paper-colored text, amber CTA). The 3D scene fills the whole hero as a
  background with visual density biased to the right. The portrait photo is
  removed.
- **Header:** unchanged. The solid paper band sits above the dark hero like a
  letterhead. Do not redesign the header in this job.

## Scene spec

- **Canvas:** full-bleed behind the text, deep gradient background
  (forest-black, ~`#0E1411`), soft vignette.
- **Neuron field:** ~2,500 points (THREE.Points, custom shader, additive
  blending), dim warm-white, slow drift.
- **Connections:** faint precomputed line segments between near neighbors
  (~1–2k), very low opacity.
- **Mitochondria cores:** 14–18 larger radial-glow sprites in amber. They
  flicker-ignite like embers catching.
- **Toxic debris:** ~300 dark matte particles drifting near the center. During
  the intro a soft expanding "protective sweep" shell passes once; debris
  accelerates outward and dissolves (opacity → 0, slight shrink).
- **Energy pulses:** after ignition, small bright sparks travel along random
  connection lines every ~1–2 s (the "sharpness" signals).
- **Idle state:** slow scene drift + cores "breathing" (gentle sine on scale /
  intensity), mouse parallax (camera lerps toward pointer, ±3°).
- **Intro (GSAP master timeline, ~2.8 s):** darkness with debris visible →
  first core ignites (~0.4 s) → staggered cascade ignition → sweep clears the
  debris (~0.8–1.8 s) → points/lines brighten to idle levels. Text staggers in
  from ~1.2 s (eyebrow → headline → subhead → paragraph → CTAs → ctaNote,
  0.12 s stagger) with the existing premium ease `cubic-bezier(0.2,0.7,0.2,1)`.
- **Scroll-out (GSAP ScrollTrigger, no pin):** as the hero leaves the viewport
  the scene fades/brightens to hand off to the cream page; subtle y-parallax on
  the text stack.

## Tech

- **New deps:** `three`, `gsap`, and `@types/three` (dev). **No
  react-three-fiber** — vanilla Three.js in one client component is simpler and
  avoids version risk with React 19 / Next 16.
- **Files:**
  - `src/components/site/hero.tsx` — layout, text, dark styles, GSAP text
    intro (replaces the motion/react reveals in this component only).
  - `src/components/site/hero-scene.tsx` — all WebGL, loaded client-only via
    `next/dynamic` with `ssr: false`; exposes an `onReady`/ignition hook so the
    text timeline syncs with the scene.
- **Fallback ladder (no layout shift; headline is the LCP and is visible
  immediately):**
  1. While JS/WebGL loads → static CSS dark gradient with a few blurred gold
     radial glows.
  2. WebGL unavailable → keep that static fallback permanently.
  3. `prefers-reduced-motion` → static *lit* scene (no intro, no pulses,
     no parallax); text appears instantly. Reuse the hydration-safe pattern
     from `use-reduced-motion-safe.ts`.
- **Performance:** device-pixel-ratio cap ~1.75; particle counts scale down on
  small viewports / low `hardwareConcurrency`; RAF pauses when the tab is
  hidden or the hero is fully scrolled out (IntersectionObserver); full
  geometry/material/renderer disposal on unmount; `three` must not land in the
  initial critical chunk (dynamic import).
- **i18n:** all 5 locale files untouched (unless the optional subhead tweak is
  taken, in which case all 5 get the equivalent line).

## Acceptance checks

1. `npm run type-check` and `npm run build` pass in the bigh-website repo.
2. Dev server renders the new hero with **zero console errors**.
3. Desktop (1440×900) and mobile (390×844) screenshots show: dark scene,
   ignited gold cores, debris gone after intro, headline/subhead/CTAs readable.
4. All 5 locales (`en`, `ko`, `es`, `ja`, `zh`) render the hero.
5. Reduced-motion emulation: text is immediately visible; no animation runs;
   no errors.
6. Fallback: with WebGL unavailable, the headline is still readable on the
   static dark gradient.
7. The `three`/`gsap` scene code is lazy-loaded (not in the first-paint
   critical path for the headline).

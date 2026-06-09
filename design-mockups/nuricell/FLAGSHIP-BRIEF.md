# NuriCell FLAGSHIP Product Page — Build Brief

Build ONE award-level product page for NuriCell. Target: an Awwwards Site-of-the-Day
calibre page that three expert judges (a creative director, an Awwwards-style
interaction juror, and a DTC conversion strategist) each score **9.5/10**.

Read **`CONTENT-BRIEF.md`** (same folder) for ALL copy, facts, claims, ingredient
data, testimonials, FAQ, and price. Every claim is approved there — do not invent
new claims; keep structure/function language (it is a dietary supplement).

OUTPUT FILE — write exactly here:
`c:/Users/mcbig/Documents/codes/bigh-website/design-mockups/nuricell/nuricell-flagship.html`

---

## The concept

**"The Mitochondrial Renewal."** A cinematic, dark, scroll-told product page. The
narrative arc: *your brain's power plants are aging → here is the science of why →
here is the Berkeley discovery that reverses it → here is the formula → here is the
proof → begin.* Immersive and emotional, but it SELLS — trust and proof land before
the first scroll, every section has one clear job, every CTA is obvious.

## Research baseline (2026 award-winning wellness pages)

- Immersive, scroll-narrative journeys win (e.g. Awwwards "Vibrant Wellness").
- Motion must *demonstrate*, never just decorate. Scroll-triggered reveals, depth,
  parallax — all lightweight, all gracefully degrading.
- Supplement pages live and die on **trust**: prove safety, prove results, prove it
  fits real life — *before the first scroll*. Clinical proof beats lifestyle fluff.
- Focused sections: one headline, one idea, one visual, one move per viewport.

## Art direction

**Mood:** deep space, luminous, scientific, premium, awe. Light emerging from dark.

**Palette (use these exact values):**
- `--bg: #0B0A09` (near-black, warm) · `--bg-2: #14110E` (raised panels) · `--bg-3: #1C1813`
- `--text: #EDE6DA` (warm off-white) · `--text-soft: #A89E8E` (muted)
- `--amber: #E9A23C` · `--amber-hi: #F6C667` (energy accent, glow) · `--ember: #B5651E` (deep)
- `--hairline: rgba(237,230,218,0.12)`
- Amber is the ONLY chromatic accent. Everything else is the warm grayscale.

**Type (Google Fonts):**
- Display: **Fraunces** — use optical sizing (`opsz`), light/regular weights, italic
  for emphasis words. Big, confident, emotional headlines.
- Body & UI: **Inter**.
- Data, eyebrows, section numbers, doses, citations: **IBM Plex Mono** — uppercase,
  tracked. The monospace is the "scientific instrument" texture; use it deliberately.

**Imagery (all in `assets/`, already produced — use them):**
- `hero-mitochondria.jpg` (2560×1429) — glowing mitochondria in dark space, negative
  space on the LEFT. The hero background.
- `mito-macro.jpg` (2000×1342) — one stunning hero mitochondrion, detailed cristae.
  Use in the problem/"your mitochondria are aging" or science section.
- `decay-renewal.jpg` (1920×1072) — split image: grey "DECAY / AGED" left, glowing
  "RENEWAL / RESTORED" right. NOTE: those four words are baked into the image — treat
  it as a scientific figure in the "how it works" section; design around the baked
  labels, do not overlay conflicting headings on top of them.
- `particle-field.jpg` (1920×1072) — golden bokeh particle field, very dark. Use as
  a subtle full-bleed background behind a section or two (low opacity, with scrim).
- `nuricell.png` — the product bottle, cleanly isolated transparent PNG (the hero
  product and closing-CTA product).
- `logo-white.png` — BiGH logo for the dark header.

## Page structure (top to bottom)

1. **Header** — fixed, transparent over hero, gains a blurred dark background after
   scroll. `logo-white.png` left; minimal nav (The Science / How It Works / Formula /
   Reviews); an "Add to Cart · $49" pill right. A thin amber **scroll-progress bar**.
2. **Hero** — full-bleed `hero-mitochondria.jpg` with a dark gradient scrim for text
   legibility. Eyebrow (mono): `DAILY COGNITIVE SUPPORT — BACKED BY UC BERKELEY SCIENCE`.
   Headline in Fraunces: **"Energy for the cells that *remember*."** Supporting
   sentence. Two CTAs (primary "Add to Cart — $49", ghost "See the science"). Below
   them, a row of 3–4 **proof chips** (PNAS-published research · 23 years · third-party
   tested) — trust before the first scroll. The bottle floats to the right with a soft
   amber radial glow behind it. A subtle scroll cue.
3. **Proof strip** — thin band directly under the hero: the institutions, set in mono
   on hairline dividers — `PNAS` · `FASEB JOURNAL` · `NY ACADEMY OF SCIENCES` ·
   `UC BERKELEY` · `cGMP` · `THIRD-PARTY TESTED`.
4. **The problem** — "Your mind runs on power plants. They're aging." The mitochondrial
   theory of brain aging, told as an editorial moment with `mito-macro.jpg`. Calm,
   a little ominous.
5. **The science / Dr. Liu** — the Berkeley discovery. The landmark PNAS 2002 finding
   presented as a hero result — a big number/stat treatment, a pull-quote, Dr. Jian
   Kang Liu and UC Berkeley as provenance. This is the proof spine of the page.
6. **How it works — the renewal** — the mechanism: aged mitochondria → fed the
   nutrients → restored. Use `decay-renewal.jpg`. Make this a genuine signature
   interactive moment: a scroll-scrubbed or hover/drag reveal that transitions decay→
   renewal, OR an animated 3-step. Big key numbers.
7. **The formula** — the 4 actives (N-Acetyl L-Carnitine, Creatine Monohydrate,
   Alpha-Lipoic Acid, Choline Bitartrate) with doses (mono) and roles. Glowing dark
   cards or an interactive list. Tell the synergy story (carnitine + lipoic acid).
8. **Results / reviews** — the testimonials from the brief, elegantly.
9. **Trust & guarantee** — certifications, made-in-USA cGMP, third-party tested,
   the 60-day money-back guarantee.
10. **FAQ** — the brief's FAQ, as an accordion.
11. **Closing CTA** — the bottle, `$49`, "Add to Cart — $49", the guarantee line,
    against `particle-field.jpg`.
12. **Footer** — BiGH brand line, nav, and the FDA disclaimer (verbatim from brief §7).

## Signature interactions (all gated behind `prefers-reduced-motion`)

- Hero: gentle parallax on the mitochondria background as you scroll; the bottle's
  amber glow softly breathes.
- A thin amber scroll-progress bar in/under the header.
- Scroll-reveal entrances — staggered, transform/opacity only, with refined easing.
- Key numbers **count up** when they enter the viewport.
- The how-it-works decay→renewal is the hero interaction — make it feel crafted.
- CTAs: tactile (`hover:-translate-y` + `active` press), with an amber glow on hover.
- FAQ accordion animates open via `grid-template-rows`.

## CRITICAL — robust reveal (do NOT repeat a known failure)

Scroll-revealed content MUST NOT be permanently invisible if the observer misfires.
Use this exact pattern:
- `.reveal { opacity:0; transform:translateY(24px); transition:...; }` /
  `.reveal.in { opacity:1; transform:none; }`
- JS: if `prefers-reduced-motion` OR no `IntersectionObserver` → add `.in` to all.
- Otherwise: on init, immediately reveal every element already in or above the
  viewport; observe the rest.
- Add a safety net: `window.load` + `setTimeout(...,6000)` reveals anything still
  not `.in`. Content can never stay stuck hidden.

## Hard technical requirements

- ONE self-contained `.html` file. All CSS in a single `<style>`. Vanilla JS inline.
- Google Fonts via `<link>` is allowed. No other external dependencies, no frameworks.
- Images by relative path (`assets/...`). Must render opened from `file://` with no
  server or build step. Add `loading="lazy"` + `decoding="async"` to below-fold images.
- Responsive and beautiful from 375px to 1920px. Test the hero headline at 375px —
  use regular spaces (never `&nbsp;`) and `minmax(0,1fr)` grid tracks so nothing
  overflows.
- Every interactive element has real `:hover`, `:active`, and `:focus-visible` states.
- Animate transform/opacity only — never layout properties. Respect
  `prefers-reduced-motion: reduce` everywhere.
- Semantic HTML, sensible heading order, alt text, AA contrast on the dark theme.
- Expect 1100–1600 lines. Every section fully designed with the real approved copy —
  no placeholders, no lorem ipsum, no stubbed sections.

Build it like it's going on the Awwwards homepage. Sweat the type, the spacing, the
easing, the detail. Make it inevitable.

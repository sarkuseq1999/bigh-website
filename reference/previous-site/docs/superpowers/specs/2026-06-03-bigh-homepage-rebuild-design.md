# BiGH Homepage Rebuild — Design Spec

**Date:** 2026-06-03
**Status:** Approved direction; pending spec review → implementation plan
**Source brief:** "BiGH — Homepage Build Brief for Claude Code" (provided by user)

---

## 1. Decision & Scope

Rebuild the BiGH homepage as a **full "warm laboratory" aesthetic** — light warm-paper background, amber accent, Fraunces/Hanken/Spline typography — replacing the current dark/cosmic aurora design.

The page is a **nine-section persuasion arc**, each section making exactly one argument, read top-to-bottom as one story:

> The best is still ahead → because your mind is your edge in the age of AI → which runs on tiny batteries → cared for by a real scientist → in one flagship formula → backed by a full team → proven by people and research → so find out where you stand → from someone real.

**In scope:** all 9 sections, the global header + footer, and the design-system foundation (tokens, fonts, layout shell).

**Confirmed scope decisions:**
- **Images:** placeholders first (correctly sized, labeled), real images generated in a later pass.
- **Languages:** English copy only now, written into `messages/en.json`; `next-intl` architecture kept; language toggle shows EN / 한국어 / Tiếng Việt / 中文 but only EN is wired. `es`/`ja` locale routes left as-is (stale, untouched).
- **Ask Dr. Liu** chat section: **dropped** (delete `ask-dr-liu.tsx`).
- **Brain Age Quiz CTA:** links to `#` for now (no quiz page exists).

---

## 2. Design System Foundation

### 2.1 Color tokens (CONFIRMED with user)

```css
:root {
  --paper:    #F6F1E8;  /* warm ivory — primary background */
  --paper-2:  #EFE8DA;  /* deeper paper — alternating sections */
  --ink:      #1B1A17;  /* warm near-black — primary text */
  --ink-soft: #6E665A;  /* muted warm grey — secondary text */
  --forest:   #16201B;  /* deep ink-green — dark sections (Scientist, Flagship beat 1) */
  --amber:    #C28A3A;  /* accent — CTA fills, "From the Lab" badge, highlights */
  --amber-hi: #DDA94E;  /* hover / lighter amber */
  --glow:     #44CDA9;  /* bioluminescent teal — RESERVED for battery/mitochondria visuals only */
  --line:     #D8CEBD;  /* hairline borders on paper */
}
```

Dominant = paper + ink. Sharp accent = amber. `--glow` appears **only** inside the Section 3 (and lightly Section 5) battery/mitochondria art — the one "alive" element on the page.

### 2.2 Typography (CONFIRMED)

Load via `next/font/google`, map in Tailwind v4 `@theme`:
- **Display / headlines:** **Fraunces** (optical serif). Use heavy `opsz`, light/regular weight, italic for emphasis words.
- **Body:** **Hanken Grotesk** (humanist sans, chosen for 50+ readability). Default body font.
- **Labels / eyebrows / stats:** **Spline Sans Mono** — uppercase, tracked, "lab notebook" texture.

Tailwind mapping: `font-display` → Fraunces, `font-mono` → Spline Sans Mono, default sans / body → Hanken Grotesk.

### 2.3 Type scale & accessibility (strict — 50+ standard)

- Body text **min 18px**; default **19–20px** at line-height 1.6.
- Hero headline `clamp(3.5rem, 6vw, 6rem)`. Section headlines `clamp(2.5rem, 4vw, 4rem)`.
- **WCAG AA contrast on every text/background pair.**
  - **Hard rule discovered in palette review:** `--amber` as *text* on `--paper` measures ~2.7:1 → **fails AA**. Therefore **amber is used only as a fill** (CTA backgrounds, badges — with dark ink text on top) and as **hover state**. Amber is NEVER used as text on paper. Body/eyebrow/secondary text stays `--ink` or `--ink-soft`. On `--forest`, use `--amber-hi` (passes) where an amber accent is wanted.
- Large tap targets (min 48px), visible `:focus-visible` states, semantic HTML, alt text on all imagery.

### 2.4 Spacing & layout

- Generous vertical rhythm — ~8–12rem top/bottom padding per section on desktop.
- Editorial, slightly asymmetric layouts (overlap, off-grid, big negative space) over centered-card monotony.
- Max content width ~1200px; display type/imagery may break wider for drama.
- Alternate section backgrounds between `--paper` and `--paper-2`; Sections 4 and Flagship beat 1 go dark (`--forest`).

### 2.5 Motion (Motion / Framer Motion — already a dependency)

- **One orchestrated hero load:** staggered reveal eyebrow → headline → subhead → paragraph → CTAs. Slow ease-out.
- **Scroll-triggered reveals** per section (fade + subtle rise), staggered for multi-item groups.
- **Signature moment:** Section 3 battery/mitochondria glow charges up and settles into a slow breathe-loop.
- Premium easing (`cubic-bezier(0.2, 0.7, 0.2, 1)`-ish, 0.6–0.9s). Nothing bouncy/fast.
- **`prefers-reduced-motion` respected everywhere** — disable transforms/loops; show charged/final states.

### 2.6 Foundation changes to existing code

- **Replace** the starter-demo tokens in `src/app/globals.css` (currently `#ffffff` / `#2563eb` blue / Georgia) with the warm-paper system above.
- **Replace** fonts in `src/app/[locale]/layout.tsx` (currently Geist / Geist Mono) with Fraunces / Hanken Grotesk / Spline Sans Mono.
- **Remove the `next-themes` dark-mode toggle / ThemeProvider dark behavior.** The design is a *fixed* light palette with deliberate dark *sections*, not a user-switchable theme. (Keep the provider only if trivially needed for `suppressHydrationWarning`; otherwise remove.)
- Fix the dangling references in existing components to `font-display` and `var(--muted)` that are currently undefined — they resolve correctly once the design system is in place (or are removed during each section rewrite).

---

## 3. Global Layout

### 3.1 Header (`site-header.tsx` — rewrite)
Sticky, minimal. Transparent over the hero, transitions to solid `--paper` (with hairline + subtle blur) on scroll.
- Left: **BiGH** wordmark.
- Right: `Science · Products · Quiz · [language toggle: EN / 한국어 / Tiếng Việt / 中文]`.
- One amber pill CTA: **"Take the Quiz"** (→ `#`).
- Sparse and premium. Mobile: hamburger sheet.

### 3.2 Footer (`site-footer.tsx` — rewrite)
Four columns: brand + short mission line; product/company links; the four-language toggle repeated; newsletter mini-signup.
Below, in `--ink-soft` small print (VERBATIM):
> These statements have not been evaluated by the Food and Drug Administration. This product is not intended to diagnose, treat, cure, or prevent any disease.

Then `© BiGH`.

### 3.3 Scroll behavior
Smooth, sectioned; each section full-bleed width with its own vertical breathing room. Alternate `--paper` / `--paper-2`; Sections 4 + Flagship beat 1 dark.

---

## 4. ⚖️ Compliance Language Law (NON-NEGOTIABLE)

Applies to all copy including generated microcopy (alt text, button states, form labels).

- ✅ **Allowed:** supports, helps maintain, stay sharp, promotes, built on, shaped by the research.
- ⛔ **Forbidden anywhere:** cures, treats, reverses, restores, prevents, improves memory, prevents decline, fixes, heals, or any claim to diagnose/treat/prevent disease.
- Frame science as **"his research showed…"** or **"the published research"** — never as a promise of results to the buyer.
- **Attribution is sacred:** only **NuriCell** carries **"From the Lab"** (amber badge). All five other products carry **"Built on the Science."** Never conflate.
- FDA disclaimer in footer (§3.2).

A compliance pass runs against every section before it is considered done.

---

## 5. Component Architecture

One component per section under `src/components/site/`. All copy lives in `messages/en.json` via `next-intl` `useTranslations`.

| # | Brief section | File | Action |
|---|---|---|---|
| S1 | The Promise | `hero.tsx` | Rewrite |
| S2 | The New Reality | `your-mind.tsx` | Rewrite |
| S3 | The Reason ⭐ | `brain-science.tsx` | Rewrite (signature glow) |
| S4 | The Scientist | `credibility.tsx` | Rewrite (dark) |
| S5 | NuriCell flagship | `nuricell-flagship.tsx` | **New** (6-beat chapter) |
| S6 | The System | `the-system.tsx` | Rewrite (6 products) |
| S7 | The Proof | `customer-stories.tsx` | Rewrite |
| S8 | The Soft Entry | `email-signup.tsx` | Rewrite |
| S9 | The Founder | `founder.tsx` | **New** |
| — | Ask Dr. Liu | `ask-dr-liu.tsx` | **Delete** |
| — | Header | `site-header.tsx` | Rewrite |
| — | Footer | `site-footer.tsx` | Rewrite |

`page.tsx` composes them in order: Header → Hero → YourMind → BrainScience → Credibility → NuricellFlagship → TheSystem → CustomerStories → EmailSignup → Founder → Footer.

**Image placeholder convention:** a shared, correctly-sized placeholder component rendering a labeled block (e.g. `[REAL PHOTO: Dr. Liu]`, `[PLACEHOLDER RENDER — swap real bottle]`, `[IMAGE: section 1 portrait]`) in muted paper tones with a hairline border, so layouts are testable before real assets exist.

---

## 6. Section-by-Section Spec (copy VERBATIM)

### S1 — The Promise (`hero.tsx`) · bg `--paper`
**Argument:** The best is still ahead. Pure hope and dignity. No mechanism yet.
- Eyebrow (mono): `BACKED BY 30 YEARS OF PUBLISHED SCIENCE`
- Headline (display, huge): **The best is still ahead.**
- Subhead: Stay sharp for the years that matter most.
- Paragraph: *Most brain supplements sell you a list of ingredients. We start thirty years deeper — at your brain's own batteries, the mitochondria — with nutrition shaped by the published research of neuroscientist Dr. Jiankang Liu.*
- Primary CTA (amber fill): `Take the 3-Minute Brain Age Quiz` → `#`
- Secondary CTA (text + arrow): `Meet NuriCell →` (anchors to flagship)

**Layout:** Full-height hero. Headline dominant, left-aligned, breaks large. Atmospheric warm image bleeding off the right or as a soft full-bleed background with a paper-gradient scrim so text stays high-contrast. Lots of negative space. CTAs grouped lower-left.
**Motion:** Orchestrated staggered load (eyebrow → headline w/ subtle optical-weight settle → subhead → paragraph → CTAs). Slow ease-out. Faint slow drift on the background image.
**Image (placeholder now):** editorial portrait of a vibrant distinguished woman late 50s, silver-streaked hair, mid-thought in a sunlit room with books/warm wood; soft natural light, shallow DoF, ivory+amber palette, film grain, premium, not clinical.

### S2 — The New Reality (`your-mind.tsx`) · bg `--paper-2`
**Argument:** In the age of AI, your mind is your last advantage. Offense, not fear.
- Eyebrow: `THE NEW REALITY`
- Headline: **The smarter the world gets, the more your mind is worth.**
- Subhead: Everyone's bracing for machines to make them obsolete. They've got it backwards.
- Body: *For the first time, machines can do the things we thought made us smart. They remember everything. They calculate in an instant. They answer before you've finished the question.*
  *So what's left? The things they can't do.*
- Three capabilities (mono label + serif definition):
  - **Judgment** — knowing which answer is the right one.
  - **Wisdom** — knowing what actually matters.
  - **Taste** — knowing what's good and what isn't.
- Closing: *That last one is the rarest of all. It can't be downloaded. It can't be trained overnight. It's earned, over a lifetime, by a mind that stays sharp.*
- Pivot (smaller): *Which means staying sharp is no longer about holding on. It's about staying ahead. And it starts somewhere smaller than you'd ever think.*

**Layout:** Text-forward, editorial. The three capabilities are the centerpiece — stacked vertically, generous spacing, mono term (ink) + serif definition (ink). Minimal/no photography; optional faint abstract texture.
**Motion:** Scroll-reveal body, then **stagger the three capabilities** like a rising staircase (Judgment → Wisdom → Taste). Taste lands last and lingers (subtle scale; no amber-as-text — use weight/scale, not color, to emphasize).

### S3 — The Reason ⭐ (`brain-science.tsx`) · bg `--paper` · SIGNATURE MOMENT
**Argument:** Your brain runs on tiny batteries. Explain it like you're five. Plant the metaphor.
- Eyebrow: `THE REASON`
- Headline: **Your brain runs on tiny batteries.**
- Subhead: Billions of them. And they're the reason you feel sharp — or you don't.
- Body: *Your brain is the hungriest part of you. Just 2% of your body, burning 20% of your energy. It never stops, and it never coasts.*
  *All that energy is made inside your cells by microscopic power plants called mitochondria — your brain's batteries. When they're full and firing, you feel it. Quick. Clear. On.*
  *But like every battery, they fade with time. Scientists have a name for it: mitochondrial decay. As the batteries weaken, the brain gets less of the one thing it runs on.*
- Turn: *Here's what most people never hear: batteries can be looked after.*
- Differentiation line (large, set apart): **Not at the surface. At the source.**
- Pivot: *And we didn't guess at any of this. The roadmap came from thirty years of published research by one neuroscientist.*

**Layout:** Page centerpiece. Copy on one side; **custom animated battery/mitochondrion visual** on the other (glowing organic mitochondrion / stylized battery filling with `--glow`) against `--paper`. `2% / 20%` as a small mono callout. "Not at the surface. At the source." is large display type with its own breathing room.
**Motion (signature):** As section scrolls in, the battery/mito **charges up** — soft teal glow pulses to life and fills, settling into a slow living breathe-loop. Optionally tie glow intensity to scroll position. Elegant and quiet. **Reduced-motion → show charged end-state, no loop.**
**Image (optional base asset, placeholder now):** abstract macro of a single glowing mitochondrion, organic cristae, luminous teal-green core on warm ivory, soft volumetric glow, premium editorial science illustration, grain, negative space.

### S4 — The Scientist (`credibility.tsx`) · bg `--forest` (DARK)
**Argument:** Real science, by a real scientist. Credibility before any claim.
- Eyebrow: `THE SCIENTIST`
- Headline: **Meet Dr. Jiankang Liu.**
- Subhead: He has spent thirty years on a single question: how do you keep a brain sharp?
- **Anchor stat (HUGE, mono, centerpiece):** `3 papers. 1 issue. 22,000+ citations.`
- Body: *In February 2002, three of his papers ran in a single issue of PNAS — the Proceedings of the National Academy of Sciences, one of the most respected journals in science. Most researchers never place a single paper there in a lifetime. He placed three at once.*
  *His work has since been cited by other scientists more than 22,000 times.*
  *This isn't a wellness trend with a celebrity face. It's a life's work — trained at UC Berkeley, carried through laboratories in the US and abroad, focused on one idea: how the brain makes its energy, and how to help it keep making it.*
  *When our founder, Mo Chen, set out to build BiGH, he didn't start with a logo or a launch plan. He started with a scientist he's known for years — and the belief that this research deserved to reach the people who need it.*
- Pivot (large): *His research became a formula. We call it NuriCell.*

**Layout:** Dark — `--forest` bg, paper text, `--amber-hi` accents. Left: `[REAL PHOTO: Dr. Liu]` placeholder, dignified portrait frame with a thin amber hairline. Right: giant anchor stat dominating, body beneath. Reverent, weighty, lots of negative space around the stat.
**Motion:** Anchor stat reveals first and largest (three numbers count/settle subtly); everything else fades in quietly beneath. Slow, respectful pacing. Reduced-motion → final values, no count.
**🔒 Do NOT AI-generate Dr. Liu's face — placeholder only.**

### S5 — The Flagship: NuriCell (`nuricell-flagship.tsx`) · dark beat 1 → light beats 2–6
**Argument:** Thirty years of science became one formula — the flagship. Build as a vertical chapter of **6 single-idea beats**, each its own breathing screen with one visual.

**Beat 1 — The reveal** (bg `--forest`, cinematic)
- Eyebrow: `THE FLAGSHIP` · Headline (huge): **NuriCell.** · Subhead: Thirty years of research. Three capsules a day.
- Badge (amber pill): `FROM THE LAB`
- Visual: NuriCell bottle hero shot, lots of air — `[PLACEHOLDER RENDER — swap real bottle]`.

**Beat 2 — Whose formula it is** (bg `--paper`)
- Headline: **His formula. Not ours.**
- Body: *This is the one Dr. Liu built himself — straight from the research you just read about. Everything else we make is built on his science. This one is his science.*

**Beat 3 — The discovery** (bg `--paper-2`)
- Headline: **Two nutrients. Greater together.**
- Body: *Acetyl-L-carnitine and alpha-lipoic acid — the two his papers centered on. Alone, each supports the brain's batteries. Together, his research showed, they do far more. That pairing is the discovery.*
- Visual: quiet animation of two elements meeting/merging (light teal-glow echo).

**Beat 4 — The precision** (bg `--paper`)
- Headline: **More isn't better. Right is better.**
- Body: *We didn't chase the biggest numbers on the label. We matched the doses to the science — the amounts the research actually points to.* (Room left for added scientific rationale later.)

**Beat 5 — The full formula** (bg `--paper-2`)
- Headline: **Built complete.**
- Body: *Rounded out with creatine and choline — energy and signaling support for a brain that never clocks out.*

**Beat 6 — The close** (bg `--paper`)
- Headline: **Three capsules. Every morning.**
- Body: *Working where it counts — not at the surface, at the source.*
- CTA (amber fill): `Start with NuriCell →`
- Pivot: *It's the foundation. But it was never meant to work alone.*

**Layout:** Open dark on Beat 1 (cinematic unveiling), resolve to light paper for Beats 2–6. Each beat = one full breathing screen, single idea, one image. The flagship getting a sequence (while others get one screen) IS the merchandising.
**Motion:** Cinematic vertical scroll; each beat fades/rises on enter. Beat 1 bottle: slow reveal (light sweep). Slow and premium throughout.
**Images (placeholders now):** (1) premium studio render, minimalist amber-glass bottle, cream label "NuriCell", warm-ivory gradient bg, soft side light, photorealistic, negative space. (2) macro of a single capsule in an open palm of a person in their 50s, warm morning light, shallow DoF, ivory+amber, calm/intimate.

### S6 — The System (`the-system.tsx`) · bg `--paper-2`
**Argument:** NuriCell is the foundation — and it leads a complete team of six.
- Eyebrow: `THE SYSTEM`
- Headline: **One formula from the lab. Five more built on the science. One complete team.**
- Intro: *NuriCell is the foundation. Around it, five formulas — each with a job, each built on the same research. Together, they're a system, not a shelf.*
- Team cards (title · role · one-liner · tag):
  - **NuriCell** — *The Foundation* — Energy, at the source. — `FROM THE LAB`
  - **Nature Calm** — *The Shield* — Calm against the day's stress. — `Built on the Science`
  - **Turmerific** — *The Firefighter* — Cools the everyday fire. — `Built on the Science`
  - **Advanced OPC** — *The Plumber* — Protects the pathways. — `Built on the Science`
  - **Green Bee Propolis** — *The Builder* — Daily defense and repair. — `Built on the Science`
  - **Deer Horn Reishi** — *The Adapter* — Day-and-night balance, overnight restoration. — `Built on the Science`
- Bundle CTAs (push the system): `Shop the 3 Treasures` · `Shop the 4 Treasures` · `Build Your Protocol`

**Layout:** A team "lineup." NuriCell elevated/primary (slightly larger, amber `FROM THE LAB` badge); the other five in a clean grid, each with a **custom vector role icon** (foundation/shield/flame/pipe/brick/yin-yang — amber line glyphs; placeholder line-icons now). One role + one line each, no paragraphs. Bundles as prominent CTAs below.
**Motion:** Cards reveal in staggered cascade; gentle hover lift; NuriCell subtly emphasized.

### S7 — The Proof (`customer-stories.tsx`) · bg `--paper`
**Argument:** It's real — real people and real research.
- Eyebrow: `THE PROOF`
- Headline: **Real science. Real people.**
- Testimonials (placeholder, experience-based, NO medical claims):
  - *"At 62, I'm running my business better than I did at 45. I feel switched on."* — Ji-woo K., Seoul · (placeholder)
  - *"Part of my morning now. I just feel clear and steady through the day."* — Daniel R., California · (placeholder)
  - *"My whole family takes it. It's the one thing none of us skip."* — Mai T., Hanoi · (placeholder)
- The record (compact mono credibility strip): `Published in PNAS` · `22,000+ citations` · `30 years of research` · `UC Berkeley–trained` — link `Read the research →`

**Layout:** Two bands. Top: three testimonial cards (warm, `[real photo]` placeholders, name/age/country). Bottom: science "record" as a clean horizontal stat strip echoing the S4 anchor. The split proves both halves of the headline.
**Motion:** Testimonials fade in; record stats reveal in sequence.

### S8 — The Soft Entry (`email-signup.tsx`) · bg `--paper-2`
**Argument:** Not ready to buy? Find out where you stand. Low-friction on-ramp + list-builder.
- Eyebrow: `FIND YOUR BRAIN AGE`
- Headline: **How sharp is your brain, really?**
- Subhead: Three minutes. A few questions. Your Brain Age — and a protocol built for it.
- Primary CTA (amber, prominent): `Take the Brain Age Quiz →` → `#`
- Newsletter block: title **The Longevity Signal**; line *No spam. No schedule. Just science.*; email field + `Subscribe`.

**Layout:** Open, low-pressure. Quiz CTA is the hero — big, central, amber. Newsletter beneath as a quiet secondary capture. Optional faint battery-glow motif tying back to S3.
**Motion:** Quiz CTA subtle slow attention pulse (respect reduced-motion). Clean focus states on form fields. (Reuse existing email-signup success/error handling where sensible.)

### S9 — The Founder (`founder.tsx`) · bg `--paper`
**Argument:** A real person built this, for you. The human handshake that closes the trust.
- Eyebrow: `A NOTE FROM OUR FOUNDER`
- Headline: **Why I built this.**
- Body (editable placeholder, founder's voice):
  *I didn't set out to build a supplement company. I set out to bring one scientist's life's work to the people who need it — starting with my own family.*
  *Everything here rests on real, published research, and it's made the way I'd make it for the people I love. No shortcuts. No hype. Just the science, done right — so you can stay sharp for everything still ahead.*
- Sign-off: *— Mo Chen, Founder*
- Soft closing CTA (text): `Start with NuriCell →` or `Take the Quiz →`

**Layout:** Intimate, warm. `[REAL PHOTO: Founder]` placeholder beside the note — genuine, un-glossy. Smaller scale than the scientist section; a quiet personal close, not a billboard.
**Motion:** Simple gentle fade-in. Calm and sincere.
**🔒 Do NOT AI-generate the founder's face — placeholder only.**

---

## 7. Image Strategy

**Phase 1 (this build):** every image is a labeled placeholder via a shared placeholder component, correctly sized to prevent layout shift. Real-photo placeholders for Dr. Liu (S4) and Founder (S9) are mandatory and must never be AI-generated.

**Phase 2 (later pass):** generate section imagery via Gemini using the prompts in §6, maintaining a consistent art-directed look (warm natural light, soft film grain, muted earthy palette matching paper/amber, shallow DoF, editorial/premium). Product render + role icons refined in Adobe MCP; product render marked `[PLACEHOLDER RENDER — swap real bottle]` until real photography exists. Lifestyle models: vibrant, dignified, sharp adults 50+, diverse/ambiguous, never frail or "decline"-coded.

---

## 8. Definition of Done (QA checklist)

- [ ] All nine sections built in order; each makes exactly one argument; copy used verbatim.
- [ ] Tokens applied consistently; `--glow` used ONLY in battery/mitochondria visuals.
- [ ] Fonts: Fraunces (display), Hanken Grotesk (body), Spline Sans Mono (labels/stats). No Geist/Inter/Georgia.
- [ ] Body text ≥18px; WCAG AA verified on every pair; amber never used as text; visible focus states; semantic HTML; alt text everywhere.
- [ ] Fully responsive, mobile-first; no layout shift; placeholders correctly sized.
- [ ] Section 3 battery glow works and is elegant; Section 5 is a 6-beat chapter.
- [ ] `prefers-reduced-motion` respected throughout.
- [ ] Compliance law obeyed — no forbidden verbs anywhere; FDA disclaimer in footer.
- [ ] Attribution correct — only NuriCell tagged "From the Lab"; all others "Built on the Science."
- [ ] Real-photo placeholders for Dr. Liu (S4) and Founder (S9); product render marked placeholder.
- [ ] Four-language toggle present in nav + footer (EN / 한국어 / Tiếng Việt / 中文), EN wired, rest stubbed.
- [ ] Primary Quiz CTA appears in S1 and S8 (→ `#`); buy CTAs concentrated in S5–S6.
- [ ] `ask-dr-liu.tsx` deleted; `es`/`ja` routes left untouched; `next-themes` dark toggle removed.
- [ ] Verified in browser at section checkpoints (not just a green build).

---

## 9. Open Items / Future

- Real Gemini imagery + Adobe MCP refinement (Phase 2).
- Real KO/VI/ZH translations (compliance-reviewed, not machine-translated).
- Brain Age Quiz page (CTA currently `#`).
- Real product photography to replace renders; real Dr. Liu + founder photos.
- Possible re-introduction of an "Ask Dr. Liu" section later.

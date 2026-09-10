# BiGH Homepage Rebuild Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the BiGH homepage as a 9-section "warm laboratory" persuasion arc — light warm-paper aesthetic, amber accent, Fraunces/Hanken/Spline type — replacing the current dark/aurora design.

**Architecture:** Next.js App Router, one component per section under `src/components/site/`, composed by `src/app/[locale]/page.tsx`. All copy in `messages/en.json` via `next-intl`. A warm-paper design system in `globals.css` (Tailwind v4 `@theme`) + `next/font`. Motion via the `motion` library. Images are labeled placeholders now (real generation is a later pass).

**Tech Stack:** Next.js 16.2.6, React 19, TypeScript, Tailwind CSS v4, `motion`, `next-intl`, `next/font/google`.

**Companion spec (read alongside this plan):** `docs/superpowers/specs/2026-06-03-bigh-homepage-rebuild-design.md`. The spec is the source of truth for per-section layout/motion intent and the compliance law; this plan is the build order. When a task says "per spec §6.S3", open that section of the spec.

---

## Conventions (defined once — referenced by tasks below)

**Design-token rule (DTR):** Components use ONLY these utilities for color/type — never raw hex, never the old `bg-[#0a0a0a]`/`var(--muted)`:
- Backgrounds: `bg-paper`, `bg-paper-2`, `bg-forest`. Text: `text-ink`, `text-ink-soft`, on dark use `text-paper` / `text-ink-soft`.
- Accent: amber ONLY as a fill (`bg-amber` with `text-ink` on top) or hover (`hover:bg-amber-hi`); on `--forest` an amber accent uses `text-amber-hi`. **Amber is NEVER text on paper** (fails AA).
- `--glow` (`bg-glow`/`text-glow`) appears ONLY inside the Section 3 battery/mito visual (and a light echo in Flagship beat 3).
- Type: headlines `font-display` (Fraunces); eyebrows/stats `font-mono` (Spline, uppercase, tracked); body inherits Hanken at ≥18px / line-height 1.6.

**Build directive (BD):** Produce section markup using the `frontend-design` skill's principles (editorial, asymmetric, generous negative space — per spec). Wrap scroll-reveal content in the shared `Reveal` component (Task 3). Honor `prefers-reduced-motion`. Use the shared `Placeholder` (Task 3) for every image, sized to prevent layout shift.

**VERIFY(file) recipe** — run at the end of every section/chrome task:
1. `npm run type-check` → expect: no errors.
2. `npm run lint` → expect: clean (ignore pre-existing warnings unrelated to the touched file).
3. With the dev server running (`npm run dev`, http://localhost:3000), use Playwright to navigate to `http://localhost:3000/en`, scroll to the section, screenshot at viewport **1280px** and **375px**, and Read both screenshots. Confirm against the spec: correct fonts/colors, no text overflow, layout matches, amber never used as paper text, reduced-motion path renders.
4. Compliance scan: `grep -niE "c\b(cure|cures|treat|treats|reverse|reverses|restore|restores|prevent|prevents|heal|heals|fix|fixes)\b|improves memory|prevents decline" src/components/site/<file>` and the same against `messages/en.json` for the section's namespace → expect: no forbidden claim. (Review any hit in context; allowed words like "supports/helps maintain/stay sharp" are fine.)
5. Commit (message shown per task).

**Commit cadence:** one commit per task. Branch is `homepage-rebuild` (already created).

---

## Phase 0 — Foundation

### Task 1: Read Next 16 + Tailwind v4 conventions (recon, no code)

**Files:** none (reading only).

- [ ] **Step 1: Read the framework docs AGENTS.md requires.**
  - `node_modules/next/dist/docs/` — find and read the `next/font` (Google fonts) guide and any App-Router font/metadata notes for v16.
  - Confirm the current `next/font/google` signature for variable fonts (the `axes`, `weight`, `style`, `variable`, `display`, `subsets` options) for Fraunces/Hanken Grotesk/Spline Sans Mono.
  - Skim Tailwind v4 token conventions already in `src/app/globals.css` (`@theme inline`, `@import "tailwindcss"`).
  - Expected outcome: you can write Task 2's font config without guessing the API.

- [ ] **Step 2:** No commit (recon only).

### Task 2: Warm-paper design tokens + base styles

**Files:**
- Modify: `src/app/globals.css` (replace the starter-demo `:root`, `@theme inline`, and `@layer base` blocks)

- [ ] **Step 1: Replace the token + theme + base blocks.** Keep the three top `@import` lines and `@custom-variant dark`. Replace everything from `:root {` onward with:

```css
:root {
  /* warm-laboratory palette (confirmed) */
  --paper:    #F6F1E8;
  --paper-2:  #EFE8DA;
  --ink:      #1B1A17;
  --ink-soft: #6E665A;
  --forest:   #16201B;
  --amber:    #C28A3A;
  --amber-hi: #DDA94E;
  --glow:     #44CDA9;
  --line:     #D8CEBD;

  /* shadcn semantic tokens mapped onto the palette so existing utilities resolve */
  --background: var(--paper);
  --foreground: var(--ink);
  --muted: var(--paper-2);
  --muted-foreground: var(--ink-soft);
  --border: var(--line);
  --card: var(--paper);
  --card-foreground: var(--ink);
  --primary: var(--amber);
  --primary-foreground: var(--ink);
}

@theme inline {
  --color-paper: var(--paper);
  --color-paper-2: var(--paper-2);
  --color-ink: var(--ink);
  --color-ink-soft: var(--ink-soft);
  --color-forest: var(--forest);
  --color-amber: var(--amber);
  --color-amber-hi: var(--amber-hi);
  --color-glow: var(--glow);
  --color-line: var(--line);

  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-border: var(--border);
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);

  --font-display: var(--font-fraunces);
  --font-sans: var(--font-hanken);
  --font-mono: var(--font-spline);
}

@layer base {
  body {
    background-color: var(--paper);
    color: var(--ink);
    font-family: var(--font-hanken), system-ui, sans-serif;
    font-size: 1.1875rem;   /* 19px */
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
  }
  ::selection { background: var(--amber); color: var(--ink); }
}
```

- [ ] **Step 2: Verify it compiles.** Run `npm run dev` (if not already running) and load `http://localhost:3000/en`. Expected: page renders on an ivory background (it will look broken/unstyled in places — that's fine; tokens are the goal here). Run `npm run type-check` → expect no errors.

- [ ] **Step 3: Commit.**
```bash
git add src/app/globals.css
git commit -m "feat(design): warm-paper tokens + base type in globals.css"
```

### Task 3: Fonts + remove dark-mode theme

**Files:**
- Modify: `src/app/[locale]/layout.tsx`
- (Possibly delete) `src/components/theme-provider.tsx` if no longer referenced

- [ ] **Step 1: Swap Geist for the three brand fonts.** Replace the font imports/instances. Use the API confirmed in Task 1; this is the expected shape:

```tsx
import { Fraunces, Hanken_Grotesk, Spline_Sans_Mono } from "next/font/google";

const fraunces = Fraunces({
  subsets: ["latin"],
  variable: "--font-fraunces",
  axes: ["opsz", "SOFT"],
  style: ["normal", "italic"],
  display: "swap",
});
const hanken = Hanken_Grotesk({
  subsets: ["latin"],
  variable: "--font-hanken",
  display: "swap",
});
const splineMono = Spline_Sans_Mono({
  subsets: ["latin"],
  variable: "--font-spline",
  display: "swap",
});
```

- [ ] **Step 2: Apply the variables and drop the dark theme.** On `<html>`, set `className={`${fraunces.variable} ${hanken.variable} ${splineMono.variable} h-full antialiased`}`. Remove the `ThemeProvider` wrapper and its import (the design is fixed-light); keep `NextIntlClientProvider` and `suppressHydrationWarning`. The body className stays `bg-background text-foreground flex min-h-full flex-col`.

- [ ] **Step 3: Remove the now-unused theme-provider.** If nothing else imports `@/components/theme-provider`, delete `src/components/theme-provider.tsx`. Confirm with `grep -rn "theme-provider" src`.

- [ ] **Step 4: Verify.** `npm run type-check` → no errors. Reload `/en`; confirm headings will use Fraunces once components apply `font-display`, and body text is Hanken. `npm run build` → expect success (catches font-config errors).

- [ ] **Step 5: Commit.**
```bash
git add src/app/[locale]/layout.tsx
git rm src/components/theme-provider.tsx  # only if deleted
git commit -m "feat(design): load Fraunces/Hanken/Spline, remove dark-mode theme"
```

### Task 4: i18n English fallback (keep stale locales from crashing the build)

**Files:**
- Read then Modify: `src/i18n/request.ts` (the `getRequestConfig` setup)

- [ ] **Step 1: Read `src/i18n/request.ts`** to see how messages are currently loaded.

- [ ] **Step 2: Make non-English locales fall back to English** so the upcoming `en.json` namespace changes don't produce missing-message errors when `next build` statically renders `/zh`, `/ko`, `/es`, `/ja`. Load English as the base and spread the locale's own messages on top:

```ts
import {getRequestConfig} from "next-intl/server";
import {routing} from "./routing";

export default getRequestConfig(async ({requestLocale}) => {
  let locale = await requestLocale;
  if (!locale || !routing.locales.includes(locale as any)) {
    locale = routing.defaultLocale;
  }
  const en = (await import("../../messages/en.json")).default;
  const localeMessages =
    locale === "en" ? en : (await import(`../../messages/${locale}.json`)).default;
  return {locale, messages: {...en, ...localeMessages}};
});
```
Adapt to the file's actual structure (keep its existing patterns; only add the English-base merge).

- [ ] **Step 3: Verify.** `npm run type-check` → no errors. (Full build is verified in Task 4b after copy lands.)

- [ ] **Step 4: Commit.**
```bash
git add src/i18n/request.ts
git commit -m "feat(i18n): fall back to English for untranslated locales"
```

### Task 4b: Replace `messages/en.json` with brief copy (verbatim)

**Files:**
- Modify: `messages/en.json` (full replacement)

- [ ] **Step 1: Replace the entire file** with the copy below. This is the authoritative verbatim copy — every section task consumes its namespace and must not paraphrase. Apostrophes are straight `'` (safe with next-intl: no apostrophe precedes an ICU `{`/`}`/`#`). `<em>` marks italic-emphasis words rendered via `t.rich`.

```json
{
  "Brand": { "name": "BiGH" },
  "Nav": {
    "science": "Science",
    "products": "Products",
    "quiz": "Quiz",
    "cta": "Take the Quiz",
    "openMenu": "Open menu",
    "closeMenu": "Close menu",
    "language": "Language"
  },
  "Languages": { "en": "EN", "ko": "한국어", "vi": "Tiếng Việt", "zh": "中文" },
  "Hero": {
    "eyebrow": "BACKED BY 30 YEARS OF PUBLISHED SCIENCE",
    "headline": "The best is <em>still ahead</em>.",
    "subhead": "Stay sharp for the years that matter most.",
    "paragraph": "Most brain supplements sell you a list of ingredients. We start thirty years deeper — at your brain's own batteries, the mitochondria — with nutrition shaped by the published research of neuroscientist Dr. Jiankang Liu.",
    "ctaPrimary": "Take the 3-Minute Brain Age Quiz",
    "ctaSecondary": "Meet NuriCell →",
    "imageAlt": "A vibrant, distinguished woman in her late 50s caught mid-thought in a sunlit room with books and warm wood"
  },
  "NewReality": {
    "eyebrow": "THE NEW REALITY",
    "headline": "The smarter the world gets, the more your mind is worth.",
    "subhead": "Everyone's bracing for machines to make them obsolete. They've got it backwards.",
    "bodyP1": "For the first time, machines can do the things we thought made us smart. They remember everything. They calculate in an instant. They answer before you've finished the question.",
    "bodyP2": "So what's left? The things they can't do.",
    "capabilities": {
      "judgment": { "term": "Judgment", "definition": "knowing which answer is the right one." },
      "wisdom": { "term": "Wisdom", "definition": "knowing what actually matters." },
      "taste": { "term": "Taste", "definition": "knowing what's good and what isn't." }
    },
    "closing": "That last one is the rarest of all. It can't be downloaded. It can't be trained overnight. It's earned, over a lifetime, by a mind that stays sharp.",
    "pivot": "Which means staying sharp is no longer about holding on. It's about staying ahead. And it starts somewhere smaller than you'd ever think."
  },
  "Reason": {
    "eyebrow": "THE REASON",
    "headline": "Your brain runs on <em>tiny batteries</em>.",
    "subhead": "Billions of them. And they're the reason you feel sharp — or you don't.",
    "bodyP1": "Your brain is the hungriest part of you. Just 2% of your body, burning 20% of your energy. It never stops, and it never coasts.",
    "bodyP2": "All that energy is made inside your cells by microscopic power plants called mitochondria — your brain's batteries. When they're full and firing, you feel it. Quick. Clear. On.",
    "bodyP3": "But like every battery, they fade with time. Scientists have a name for it: mitochondrial decay. As the batteries weaken, the brain gets less of the one thing it runs on.",
    "turn": "Here's what most people never hear: batteries can be looked after.",
    "differentiation": "Not at the surface. At the source.",
    "pivot": "And we didn't guess at any of this. The roadmap came from thirty years of published research by one neuroscientist.",
    "calloutStat": "2% / 20%",
    "calloutLabel": "of the body / of its energy"
  },
  "Scientist": {
    "eyebrow": "THE SCIENTIST",
    "headline": "Meet Dr. Jiankang <em>Liu</em>.",
    "subhead": "He has spent thirty years on a single question: how do you keep a brain sharp?",
    "anchor": "3 papers. 1 issue. 22,000+ citations.",
    "bodyP1": "In February 2002, three of his papers ran in a single issue of PNAS — the Proceedings of the National Academy of Sciences, one of the most respected journals in science. Most researchers never place a single paper there in a lifetime. He placed three at once.",
    "bodyP2": "His work has since been cited by other scientists more than 22,000 times.",
    "bodyP3": "This isn't a wellness trend with a celebrity face. It's a life's work — trained at UC Berkeley, carried through laboratories in the US and abroad, focused on one idea: how the brain makes its energy, and how to help it keep making it.",
    "bodyP4": "When our founder, Mo Chen, set out to build BiGH, he didn't start with a logo or a launch plan. He started with a scientist he's known for years — and the belief that this research deserved to reach the people who need it.",
    "pivot": "His research became a formula. We call it NuriCell.",
    "photoLabel": "[REAL PHOTO: Dr. Liu]"
  },
  "Flagship": {
    "eyebrow": "THE FLAGSHIP",
    "badge": "FROM THE LAB",
    "beat1": { "headline": "NuriCell.", "subhead": "Thirty years of research. Three capsules a day." },
    "beat2": { "headline": "His formula. Not ours.", "body": "This is the one Dr. Liu built himself — straight from the research you just read about. Everything else we make is built on his science. This one is his science." },
    "beat3": { "headline": "Two nutrients. Greater together.", "body": "Acetyl-L-carnitine and alpha-lipoic acid — the two his papers centered on. Alone, each supports the brain's batteries. Together, his research showed, they do far more. That pairing is the discovery." },
    "beat4": { "headline": "More isn't better. Right is better.", "body": "We didn't chase the biggest numbers on the label. We matched the doses to the science — the amounts the research actually points to." },
    "beat5": { "headline": "Built complete.", "body": "Rounded out with creatine and choline — energy and signaling support for a brain that never clocks out." },
    "beat6": { "headline": "Three capsules. Every morning.", "body": "Working where it counts — not at the surface, at the source.", "cta": "Start with NuriCell →", "pivot": "It's the foundation. But it was never meant to work alone." },
    "bottleLabel": "[PLACEHOLDER RENDER — swap real bottle]",
    "capsuleLabel": "[IMAGE: a single capsule in an open palm]"
  },
  "System": {
    "eyebrow": "THE SYSTEM",
    "headline": "One formula from the lab. Five more built on the science. One complete team.",
    "intro": "NuriCell is the foundation. Around it, five formulas — each with a job, each built on the same research. Together, they're a system, not a shelf.",
    "products": {
      "nuricell":   { "name": "NuriCell",          "role": "The Foundation",  "line": "Energy, at the source.",                              "tag": "FROM THE LAB" },
      "natureCalm": { "name": "Nature Calm",        "role": "The Shield",      "line": "Calm against the day's stress.",                      "tag": "Built on the Science" },
      "turmerific": { "name": "Turmerific",         "role": "The Firefighter", "line": "Cools the everyday fire.",                            "tag": "Built on the Science" },
      "advancedOpc":{ "name": "Advanced OPC",       "role": "The Plumber",     "line": "Protects the pathways.",                              "tag": "Built on the Science" },
      "greenBee":   { "name": "Green Bee Propolis", "role": "The Builder",     "line": "Daily defense and repair.",                           "tag": "Built on the Science" },
      "deerHorn":   { "name": "Deer Horn Reishi",   "role": "The Adapter",     "line": "Day-and-night balance, overnight restoration.",       "tag": "Built on the Science" }
    },
    "bundles": { "three": "Shop the 3 Treasures", "four": "Shop the 4 Treasures", "protocol": "Build Your Protocol" }
  },
  "Proof": {
    "eyebrow": "THE PROOF",
    "headline": "Real science. Real people.",
    "testimonials": {
      "one":   { "quote": "At 62, I'm running my business better than I did at 45. I feel switched on.", "name": "Ji-woo K.", "location": "Seoul", "note": "(placeholder)" },
      "two":   { "quote": "Part of my morning now. I just feel clear and steady through the day.",        "name": "Daniel R.", "location": "California", "note": "(placeholder)" },
      "three": { "quote": "My whole family takes it. It's the one thing none of us skip.",                 "name": "Mai T.",    "location": "Hanoi", "note": "(placeholder)" }
    },
    "record": {
      "pnas": "Published in PNAS",
      "citations": "22,000+ citations",
      "years": "30 years of research",
      "berkeley": "UC Berkeley–trained",
      "cta": "Read the research →"
    }
  },
  "SoftEntry": {
    "eyebrow": "FIND YOUR BRAIN AGE",
    "headline": "How sharp is your brain, really?",
    "subhead": "Three minutes. A few questions. Your Brain Age — and a protocol built for it.",
    "quizCta": "Take the Brain Age Quiz →",
    "newsletter": {
      "title": "The Longevity Signal",
      "line": "No spam. No schedule. Just science.",
      "placeholder": "you@example.com",
      "cta": "Subscribe"
    }
  },
  "Founder": {
    "eyebrow": "A NOTE FROM OUR FOUNDER",
    "headline": "Why I built this.",
    "bodyP1": "I didn't set out to build a supplement company. I set out to bring one scientist's life's work to the people who need it — starting with my own family.",
    "bodyP2": "Everything here rests on real, published research, and it's made the way I'd make it for the people I love. No shortcuts. No hype. Just the science, done right — so you can stay sharp for everything still ahead.",
    "signoff": "— Mo Chen, Founder",
    "cta": "Start with NuriCell →",
    "photoLabel": "[REAL PHOTO: Founder]"
  },
  "Footer": {
    "mission": "Stay sharp for the years that matter most. Brain-health nutrition shaped by published science.",
    "columns": { "product": "Product", "company": "Company" },
    "links": {
      "nuricell": "NuriCell",
      "system": "The System",
      "science": "The Science",
      "quiz": "Brain Age Quiz",
      "about": "About",
      "founder": "Our Founder",
      "research": "Research",
      "contact": "Contact"
    },
    "newsletter": { "title": "The Longevity Signal", "placeholder": "you@example.com", "cta": "Subscribe" },
    "disclaimer": "These statements have not been evaluated by the Food and Drug Administration. This product is not intended to diagnose, treat, cure, or prevent any disease.",
    "copyright": "© {year} BiGH."
  },
  "Meta": {
    "title": "BiGH — Confidence in the Future of Your Mind",
    "description": "Premium brain-health nutrition, shaped by thirty years of published science. Stay sharp for the years that matter most."
  }
}
```

- [ ] **Step 2: Verify the build with stale locales.** `npm run build` → expect success (the Task 4 fallback prevents missing-message failures on `/zh`,`/ko`,`/es`,`/ja`). If a locale errors, fix the fallback in `src/i18n/request.ts` before continuing.

- [ ] **Step 3: Commit.**
```bash
git add messages/en.json
git commit -m "feat(copy): brief-verbatim homepage copy in en.json"
```

### Task 5: Shared primitives — Placeholder + Reveal

**Files:**
- Create: `src/components/site/placeholder.tsx`
- Create: `src/components/site/reveal.tsx`

- [ ] **Step 1: Placeholder.** A labeled image stand-in in warm tones with a hairline border, sized by an aspect-ratio class to prevent layout shift.

```tsx
import { clsx } from "clsx";

export function Placeholder({
  label,
  className,
}: {
  label: string;
  className?: string;
}) {
  return (
    <div
      role="img"
      aria-label={label}
      className={clsx(
        "flex items-center justify-center rounded-xl border border-line bg-paper-2 text-center",
        className,
      )}
    >
      <span className="font-mono text-xs tracking-widest text-ink-soft uppercase px-4">
        {label}
      </span>
    </div>
  );
}
```

- [ ] **Step 2: Reveal.** A motion wrapper: fade + rise on scroll into view; static under reduced motion.

```tsx
"use client";

import { motion, useReducedMotion } from "motion/react";
import type { ReactNode } from "react";

const EASE = [0.2, 0.7, 0.2, 1] as const;

export function Reveal({
  children,
  delay = 0,
  className,
}: {
  children: ReactNode;
  delay?: number;
  className?: string;
}) {
  const reduce = useReducedMotion();
  if (reduce) return <div className={className}>{children}</div>;
  return (
    <motion.div
      className={className}
      initial={{ opacity: 0, y: 16 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-15% 0px" }}
      transition={{ duration: 0.8, delay, ease: EASE }}
    >
      {children}
    </motion.div>
  );
}
```

- [ ] **Step 3: Verify.** `npm run type-check` → no errors. (Confirm `motion/react` is the correct import path for the installed `motion` v12 — it is used in the current `hero.tsx`.)

- [ ] **Step 4: Commit.**
```bash
git add src/components/site/placeholder.tsx src/components/site/reveal.tsx
git commit -m "feat(site): shared Placeholder and Reveal primitives"
```

---

## Phase 1 — Global chrome

### Task 6: Site header (rewrite)

**Files:**
- Modify (full rewrite): `src/components/site/site-header.tsx`

Spec: §3.1. Sticky; transparent over the hero, solid `--paper` + hairline + subtle blur after scroll (IntersectionObserver or scroll listener). Left: **BiGH** wordmark (text in `font-display`, or existing logo asset). Right: `Science · Products · Quiz` links + language toggle (EN / 한국어 / Tiếng Việt / 中文 from the `Languages` namespace — visual toggle only, EN active, others non-functional stubs) + one amber pill CTA **"Take the Quiz"** → `#`. Mobile: hamburger → sheet. Nav links anchor to in-page sections (`#science`, `#system`, `#quiz`/`#`). Use namespace `Nav` + `Languages`.

- [ ] **Step 1:** Apply BD + DTR. Rewrite the header per the spec above. Quiz CTA and language toggle are stubs (`href="#"`). Remove the old theme-toggle button.
- [ ] **Step 2:** VERIFY(`site-header.tsx`). Extra check: confirm the transparent→solid transition fires on scroll and the CTA pill has visible `:focus-visible` + ≥48px tap height.
- [ ] **Step 3: Commit** — `git commit -m "feat(site): warm-paper sticky header with quiz CTA + lang toggle"`

### Task 7: Site footer (rewrite)

**Files:**
- Modify (full rewrite): `src/components/site/site-footer.tsx`

Spec: §3.2. Four columns: brand + mission line (`Footer.mission`); Product links; Company links; the four-language toggle repeated; newsletter mini-signup (`Footer.newsletter`). Below: the FDA disclaimer (`Footer.disclaimer`) verbatim in `text-ink-soft` small print, then `Footer.copyright` (pass `{year}` — compute on the server or pass a fixed current year; do not use `new Date()` inside a workflow, but in app code it's fine). Namespace `Footer` + `Languages`.

- [ ] **Step 1:** Apply BD + DTR. Rewrite per spec. Disclaimer text must be exactly the string in `Footer.disclaimer`.
- [ ] **Step 2:** VERIFY(`site-footer.tsx`). Extra check: the disclaimer renders verbatim and passes AA as small print (ink-soft on paper at the chosen size — bump size/weight if needed to pass).
- [ ] **Step 3: Commit** — `git commit -m "feat(site): four-column footer with FDA disclaimer"`

---

## Phase 2 — Sections (build in order; verify each in browser)

> Each section: apply **BD + DTR**, consume the listed namespace, build markup to the spec section cited, then run **VERIFY(file)**. Ensure the component is rendered in `page.tsx` (Task 16 sets the final order; during the build it's fine to append). Add an `id` to each `<section>` as noted so nav anchors and the `Meet NuriCell →` link resolve.

### Task 8: S1 — Hero / The Promise

**Files:** Modify (full rewrite): `src/components/site/hero.tsx`. Namespace `Hero`. Spec §6.S1. `id` not required (top of page).

- [ ] **Step 1:** bg `--paper`, full-height. Dominant left-aligned `font-display` headline via `t.rich("headline", { em })`. Eyebrow (mono), subhead, paragraph, then two CTAs lower-left: primary amber pill `ctaPrimary` (→ `#`), secondary text+arrow `ctaSecondary` (→ `#nuricell`). Warm image bleeding right or full-bleed with a paper-gradient scrim (use `Placeholder` with `Hero.imageAlt`). **Orchestrated staggered load** (eyebrow→headline→subhead→paragraph→CTAs) — use `motion` with a stagger; reduced-motion renders static. Faint slow drift on the image (reduced-motion: none).
- [ ] **Step 2:** VERIFY(`hero.tsx`).
- [ ] **Step 3: Commit** — `git commit -m "feat(hero): The Promise section (warm-paper)"`

### Task 9: S2 — The New Reality

**Files:** Modify (full rewrite): `src/components/site/your-mind.tsx`. Namespace `NewReality`. Spec §6.S2.

- [ ] **Step 1:** bg `--paper-2`, text-forward, minimal/no imagery. Eyebrow, headline, subhead, two body paragraphs. The **three capabilities** are the centerpiece — stacked vertically, generous spacing, each: mono `term` (ink) + serif `definition` (ink). Closing + smaller pivot line. **Stagger the three capabilities** like a rising staircase (Judgment→Wisdom→Taste); Taste lingers via subtle scale/weight — **not color** (amber is never text). Reduced-motion: static.
- [ ] **Step 2:** VERIFY(`your-mind.tsx`).
- [ ] **Step 3: Commit** — `git commit -m "feat(section): The New Reality (Judgment/Wisdom/Taste)"`

### Task 10: S3 — The Reason ⭐ (signature glow)

**Files:** Modify (full rewrite): `src/components/site/brain-science.tsx`. Namespace `Reason`. Spec §6.S3. `id="science"`.

- [ ] **Step 1:** bg `--paper`. Two-column: copy one side, **custom animated battery/mitochondrion** the other (inline SVG + CSS/`motion`). The visual **charges up** when scrolled into view — teal `--glow` pulses to life and fills, then a slow breathe-loop. This is the ONLY place `--glow` is used. `calloutStat` ("2% / 20%") as a small mono callout. `differentiation` ("Not at the surface. At the source.") as large `font-display`, its own breathing room. Eyebrow/subhead/3 body paragraphs/turn/pivot. **Reduced-motion: render the charged end-state, no loop/scrub.** Provide a safety so the visual is never permanently invisible.
- [ ] **Step 2:** VERIFY(`brain-science.tsx`). Extra: toggle `prefers-reduced-motion` (Playwright `emulateMedia`) and confirm the charged end-state shows.
- [ ] **Step 3: Commit** — `git commit -m "feat(section): The Reason with battery-glow signature moment"`

### Task 11: S4 — The Scientist (dark)

**Files:** Modify (full rewrite): `src/components/site/credibility.tsx`. Namespace `Scientist`. Spec §6.S4. `id="scientist"`.

- [ ] **Step 1:** bg `--forest`, `text-paper`, `text-amber-hi` accents. Left: `Placeholder` with `photoLabel` ("[REAL PHOTO: Dr. Liu]") in a dignified frame with a thin amber hairline — **do NOT generate this face.** Right: the **anchor stat** huge in `font-mono`, dominating; four body paragraphs beneath; large pivot line. Motion: anchor reveals first/largest, the three numbers count/settle (reduced-motion: final values, no count); rest fades in beneath. Slow pacing.
- [ ] **Step 2:** VERIFY(`credibility.tsx`). Extra: AA check for `text-paper` and `text-amber-hi` on `--forest`.
- [ ] **Step 3: Commit** — `git commit -m "feat(section): The Scientist (dark forest, anchor stat)"`

### Task 12: S5 — NuriCell flagship (6-beat chapter)

**Files:** Create: `src/components/site/nuricell-flagship.tsx`. Namespace `Flagship`. Spec §6.S5. `id="nuricell"`.

- [ ] **Step 1:** One component rendering **6 beats**, each a full breathing screen, one idea, one visual:
  - Beat 1: bg `--forest` (cinematic), eyebrow, huge `font-display` "NuriCell.", subhead, amber pill badge `badge` ("FROM THE LAB"), bottle `Placeholder` (`bottleLabel`) with a slow light-sweep reveal.
  - Beats 2–6: resolve to light (`--paper`/`--paper-2` alternating per spec). Each: headline + body. Beat 3 has a quiet two-elements-meeting animation with a light `--glow` echo. Beat 6: amber CTA `cta` (→ `#`) + pivot line.
  - Each beat fades/rises on enter (reduced-motion: static).
- [ ] **Step 2:** Render `<NuricellFlagship />` in `page.tsx` after `<Credibility />` (import + place). `npm run type-check`.
- [ ] **Step 3:** VERIFY(`nuricell-flagship.tsx`). Extra: confirm only NuriCell carries "FROM THE LAB"; the dark→light transition reads cleanly.
- [ ] **Step 4: Commit** — `git commit -m "feat(section): NuriCell flagship 6-beat chapter"`

### Task 13: S6 — The System (6 products)

**Files:** Modify (full rewrite): `src/components/site/the-system.tsx`. Namespace `System`. Spec §6.S6. `id="system"`.

- [ ] **Step 1:** bg `--paper-2`. A team "lineup": **NuriCell elevated/primary** (slightly larger, amber `FROM THE LAB` badge), the other five in a clean grid, each card = a **role icon** (placeholder line glyph for now — foundation/shield/flame/pipe/brick/yin-yang as simple inline SVG or `Placeholder`), `name`, `role`, one `line`, and `tag`. **Only NuriCell tag = "FROM THE LAB"; the other five = "Built on the Science"** (the data already encodes this — do not alter). One role + one line each; no paragraphs. Below: three bundle CTAs (`bundles.three/four/protocol`, → `#`). Motion: staggered cascade reveal, gentle hover lift, NuriCell emphasized.
- [ ] **Step 2:** VERIFY(`the-system.tsx`). Extra: assert exactly one "FROM THE LAB" and five "Built on the Science" render.
- [ ] **Step 3: Commit** — `git commit -m "feat(section): The System (six-product team lineup)"`

### Task 14: S7 — The Proof

**Files:** Modify (full rewrite): `src/components/site/customer-stories.tsx`. Namespace `Proof`. Spec §6.S7. `id="proof"`.

- [ ] **Step 1:** bg `--paper`. Two bands. Top: three testimonial cards (warm, each with a small `[real photo]` `Placeholder`, quote, `name`, `location`, `note`). Bottom: the science **record** as a clean horizontal mono stat strip (`pnas` · `citations` · `years` · `berkeley`) echoing the S4 anchor, with `record.cta` link (→ `#`). Motion: testimonials fade in; record stats reveal in sequence. Testimonials are experience-based — confirm no medical claim slipped in.
- [ ] **Step 2:** VERIFY(`customer-stories.tsx`).
- [ ] **Step 3: Commit** — `git commit -m "feat(section): The Proof (testimonials + science record)"`

### Task 15: S8 — The Soft Entry

**Files:** Modify (full rewrite): `src/components/site/email-signup.tsx`. Namespace `SoftEntry`. Spec §6.S8. `id="quiz"`.

- [ ] **Step 1:** bg `--paper-2`, open and low-pressure. The **Quiz CTA is the hero** — big, central, amber pill `quizCta` (→ `#`), with a subtle slow attention pulse (reduced-motion: none). Eyebrow/headline/subhead above it. Beneath, a quiet newsletter block: `newsletter.title` ("The Longevity Signal"), `newsletter.line`, email input + `newsletter.cta`. Reuse the existing email-signup success/error/validation handling if present; clean `:focus-visible` states. Optional faint battery-glow motif tying back to S3 (still glow-only-here exception is S3; keep this as a non-`--glow` warm motif to avoid breaking the glow rule).
- [ ] **Step 2:** VERIFY(`email-signup.tsx`).
- [ ] **Step 3: Commit** — `git commit -m "feat(section): The Soft Entry (Brain Age quiz + newsletter)"`

### Task 16: S9 — The Founder

**Files:** Create: `src/components/site/founder.tsx`. Namespace `Founder`. Spec §6.S9. `id="founder"`.

- [ ] **Step 1:** bg `--paper`, intimate and warm, smaller scale than the Scientist section. `Placeholder` with `photoLabel` ("[REAL PHOTO: Founder]") beside the note — genuine, un-glossy — **do NOT generate this face.** Eyebrow, headline, two body paragraphs, `signoff`, soft text CTA `cta` (→ `#nuricell`). Motion: simple gentle fade-in (reduced-motion: static).
- [ ] **Step 2:** Render `<Founder />` last in `page.tsx`. `npm run type-check`.
- [ ] **Step 3:** VERIFY(`founder.tsx`).
- [ ] **Step 4: Commit** — `git commit -m "feat(section): The Founder note"`

---

## Phase 3 — Wiring, cleanup, QA

### Task 17: Finalize page composition + delete Ask Dr. Liu

**Files:**
- Modify: `src/app/[locale]/page.tsx`
- Delete: `src/components/site/ask-dr-liu.tsx`

- [ ] **Step 1: Set the final order** in `page.tsx`:
```tsx
<SiteHeader />
<main className="flex-1">
  <Hero />
  <YourMind />        {/* S2 New Reality */}
  <BrainScience />    {/* S3 Reason */}
  <Credibility />     {/* S4 Scientist */}
  <NuricellFlagship />{/* S5 */}
  <TheSystem />       {/* S6 */}
  <CustomerStories /> {/* S7 Proof */}
  <EmailSignup />     {/* S8 Soft Entry */}
  <Founder />         {/* S9 */}
</main>
<SiteFooter />
```
Remove the `AskDrLiu` import and usage. Add the `NuricellFlagship` and `Founder` imports.

- [ ] **Step 2: Delete the dropped section.** `git rm src/components/site/ask-dr-liu.tsx`. Confirm nothing imports it: `grep -rn "ask-dr-liu\|AskDrLiu" src` → expect no hits.

- [ ] **Step 3: Verify.** `npm run type-check` → no errors. `npm run build` → success.

- [ ] **Step 4: Commit.**
```bash
git add src/app/[locale]/page.tsx
git rm src/components/site/ask-dr-liu.tsx
git commit -m "feat(home): final 9-section order; drop Ask Dr. Liu"
```

### Task 18: Compliance + accessibility + reduced-motion sweep

**Files:** any flagged by the checks (fix in place).

- [ ] **Step 1: Compliance scan across the whole site.**
```bash
grep -rniE "\b(cure|cures|treat|treats|reverse|reverses|reversal|restore|restores|prevent|prevents|heal|heals)\b|improves memory|prevents decline|fixes" src/components/site messages/en.json
```
Expected: no forbidden *claim*. Review every hit in context; the only acceptable occurrences are inside the verbatim FDA disclaimer ("diagnose, treat, cure, or prevent any disease"). Remove/rephrase anything else.

- [ ] **Step 2: Attribution check.** `grep -rn "FROM THE LAB\|From the Lab\|Built on the Science" src messages/en.json` → confirm "From the Lab" attaches ONLY to NuriCell; all other products use "Built on the Science."

- [ ] **Step 3: Reduced-motion + a11y.** With Playwright `emulateMedia({ reducedMotion: "reduce" })`, load `/en` and confirm: no looping/auto animations run, the S3 visual shows its charged end-state, all content is visible. Tab through the page: visible `:focus-visible` on every interactive element; tap targets ≥48px. Confirm every `Placeholder`/image has an accessible label/alt.

- [ ] **Step 4: Contrast spot-check.** Verify amber is never rendered as text on paper anywhere (`grep -rn "text-amber\b" src` → expect none; only `bg-amber`, `hover:bg-amber-hi`, and `text-amber-hi` on forest are allowed).

- [ ] **Step 5: Commit** any fixes — `git commit -am "fix: compliance, a11y, and reduced-motion sweep"`.

### Task 19: Full-page browser walkthrough + responsive pass

- [ ] **Step 1:** With the dev server running, use Playwright to capture full-page screenshots of `/en` at **375px, 768px, 1280px, 1920px**. Read each. Confirm: no layout shift, no overflow, section background alternation reads correctly, dark sections (Scientist, Flagship beat 1) land with gravity, the persuasion arc flows top-to-bottom.

- [ ] **Step 2:** Fix any responsive issues found, re-verify the affected section, and commit per fix.

- [ ] **Step 3: Final DoD check** against spec §8 — tick every box. Anything unchecked is unfinished work, not a pass.

- [ ] **Step 4:** Stop the brainstorm visual-companion server if still running (`scripts/stop-server.sh`), and report status to the user (what's done, what's deferred to the image-generation pass).

---

## Self-Review (completed by plan author)

**Spec coverage:** S1–S9 → Tasks 8–16; design system §2 → Tasks 2–3,5; global layout §3 → Tasks 6–7; compliance law §4 → Conventions + Task 18; component map §5 → Tasks 8–17; image strategy §7 → Task 5 `Placeholder` + per-section use; DoD §8 → Task 19 Step 3; i18n decision → Task 4; drop Ask Dr. Liu → Task 17; remove dark theme → Task 3. No gaps found.

**Placeholder scan:** No "TBD/implement later". The only literal "[PLACEHOLDER …]" / "[REAL PHOTO …]" strings are intentional on-screen image labels per the brief, not plan gaps. "Room left for added scientific rationale" (Flagship beat 4) is verbatim brief copy, intentional.

**Type/name consistency:** Component/namespace pairs are consistent across Tasks 4b/8–17 (`Hero`/hero.tsx, `NewReality`/your-mind.tsx, `Reason`/brain-science.tsx, `Scientist`/credibility.tsx, `Flagship`/nuricell-flagship.tsx, `System`/the-system.tsx, `Proof`/customer-stories.tsx, `SoftEntry`/email-signup.tsx, `Founder`/founder.tsx). Token utilities (`bg-paper`, `text-ink`, `text-amber-hi`, `bg-amber`, `font-display`, `font-mono`) are defined in Task 2 and used consistently. `Reveal`/`Placeholder` defined in Task 5 before first use.

**Known acceptable risk:** non-English locales render English (Task 4 fallback) until real translations land — matches the agreed scope.

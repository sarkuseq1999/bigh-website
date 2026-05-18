# YourMind Section Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the homepage's second section (`YourMind`) with a white, centered "kinetic statement" section — a faint animated thought-lines background, Steve-Jobs-style "missing the point" copy, and a staged scroll-triggered reveal.

**Architecture:** A single client component (`src/components/site/your-mind.tsx`) rewritten in place, keeping the `YourMind` named export so `page.tsx` is untouched. Two small in-file helpers: `ThoughtLines` (the inline-SVG background motif) and `Point` (the sienna accent phrase with a draw-in underline). All copy lives in the `YourMind` namespace of the `next-intl` message catalogs. The staged reveal is driven by one `useInView` trigger on the section, with each element given its own animation delay; `useReducedMotion` collapses all animation to a static render.

**Tech Stack:** Next.js 16, React 19, `motion` (Framer Motion successor, `motion/react`), `next-intl` v4, Tailwind CSS v4, `lucide-react`. No new dependencies. The project has no unit-test runner; verification is `npm run type-check`, `npm run build`, `npm run lint`, and visual inspection of the running dev server.

---

## File structure

| File | Change | Responsibility |
|------|--------|----------------|
| `messages/en.json` | Modify — replace `YourMind` object | English copy |
| `messages/ko.json` | Modify — replace `YourMind` object | English placeholder copy |
| `messages/zh.json` | Modify — replace `YourMind` object | English placeholder copy |
| `messages/ja.json` | Modify — replace `YourMind` object | English placeholder copy |
| `messages/es.json` | Modify — replace `YourMind` object | English placeholder copy |
| `src/components/site/your-mind.tsx` | Modify — full rewrite | The section component + `ThoughtLines` + `Point` helpers |

`src/app/[locale]/page.tsx` is **not** changed — the `YourMind` export name and import path are preserved.

---

## Task 1: Replace the `YourMind` copy in all five message catalogs

**Files:**
- Modify: `messages/en.json`
- Modify: `messages/ko.json`
- Modify: `messages/zh.json`
- Modify: `messages/ja.json`
- Modify: `messages/es.json`

Each file currently has a `"YourMind"` object with the old keys
(`headlineBefore`, `headlineAI`, `headlineAfter`, `headlineEmphasis`,
`headlineEnd`, …). Replace the **entire `"YourMind"` object** in each file with
the new object below. The English copy is used for every locale — real
translation is a separate follow-up task, and `next-intl` errors on missing
keys, so every locale must carry the same key set.

- [ ] **Step 1: Replace the `YourMind` object in `messages/en.json`**

In `messages/en.json`, select from `"YourMind": {` through its matching closing
`}` and replace with exactly:

```json
  "YourMind": {
    "eyebrow": "The human advantage",
    "headlineSetup": "Everyone is talking about artificial intelligence.",
    "headlinePunch": "They're missing <point>the point</point>.",
    "body": "The most powerful intelligence you will ever use is your own mind — your taste, your judgment, your imagination. A machine can be trained. It cannot be you. Your mind runs on a healthy brain, and a brain needs just two things to stay extraordinary: protection, and fuel.",
    "coda": "That's the whole idea.",
    "cta": "Discover the line"
  }
```

Keep the surrounding commas correct: if `YourMind` is followed by another
key, keep the trailing comma after the closing `}`; if it is the last key, no
trailing comma.

- [ ] **Step 2: Replace the `YourMind` object in `messages/ko.json`, `zh.json`, `ja.json`, `es.json`**

In each of the four files, replace the entire `"YourMind"` object with the
**same object shown in Step 1** (identical English text — placeholder pending
localization). Preserve each file's existing comma placement.

- [ ] **Step 3: Verify every catalog is still valid JSON**

Run:
```bash
node -e "['en','ko','zh','ja','es'].forEach(l=>{const o=require('./messages/'+l+'.json').YourMind;const k=Object.keys(o).sort().join(',');if(k!=='body,coda,cta,eyebrow,headlinePunch,headlineSetup')throw new Error(l+' has wrong keys: '+k);});console.log('all 5 catalogs OK');"
```
Expected output: `all 5 catalogs OK`
(If any file is invalid JSON, `require` throws and names the file.)

- [ ] **Step 4: Commit**

```bash
git add messages/en.json messages/ko.json messages/zh.json messages/ja.json messages/es.json
git commit -m "Update YourMind section copy to AI-era messaging

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: Rewrite the `YourMind` component

**Files:**
- Modify: `src/components/site/your-mind.tsx` (full rewrite)

- [ ] **Step 1: Replace the entire contents of `src/components/site/your-mind.tsx`**

Write the file with exactly this content:

```tsx
"use client";

import { useRef, type ReactNode } from "react";
import { motion, useInView, useReducedMotion } from "motion/react";
import { useTranslations } from "next-intl";
import { ArrowRight } from "lucide-react";

const ease = [0.2, 0.7, 0.2, 1] as const;

/* ──────────────────────────────────────────────────────────────────────── */
/* ThoughtLines — four faint brainwave lines that drift behind the section.  */
/* preserveAspectRatio="none" lets the viewBox stretch full-bleed; each path  */
/* spans x:0..1800 so a -600px drift (one wave period) loops seamlessly.      */
/* ──────────────────────────────────────────────────────────────────────── */

function ThoughtLines({ reduce, inView }: { reduce: boolean; inView: boolean }) {
  const lines = [
    { d: "M0 120 q150 -34 300 0 t300 0 t300 0 t300 0 t300 0 t300 0", stroke: "#B85426", opacity: 0.3, dur: 21 },
    { d: "M0 250 q150 32 300 0 t300 0 t300 0 t300 0 t300 0 t300 0", stroke: "#9C8F82", opacity: 0.34, dur: 27 },
    { d: "M0 380 q150 -30 300 0 t300 0 t300 0 t300 0 t300 0 t300 0", stroke: "#B85426", opacity: 0.3, dur: 24 },
    { d: "M0 500 q150 28 300 0 t300 0 t300 0 t300 0 t300 0 t300 0", stroke: "#9C8F82", opacity: 0.3, dur: 32 },
  ];

  return (
    <motion.div
      aria-hidden="true"
      className="absolute inset-0 z-0"
      initial={reduce ? false : { opacity: 0 }}
      animate={reduce ? undefined : { opacity: inView ? 1 : 0 }}
      transition={{ duration: 1.8, delay: 1.2, ease: "linear" }}
    >
      <svg viewBox="0 0 1000 620" preserveAspectRatio="none" className="h-full w-full">
        {lines.map((line) => (
          <motion.path
            key={line.d}
            d={line.d}
            fill="none"
            stroke={line.stroke}
            strokeWidth={1.1}
            opacity={line.opacity}
            animate={reduce ? undefined : { x: [0, -600] }}
            transition={{ duration: line.dur, repeat: Infinity, ease: "linear" }}
          />
        ))}
      </svg>
    </motion.div>
  );
}

/* ──────────────────────────────────────────────────────────────────────── */
/* Point — the sienna accent phrase ("the point") with a draw-in underline.  */
/* Rendered as the <point> tag handler for the rich-text headline.           */
/* ──────────────────────────────────────────────────────────────────────── */

function Point({
  children,
  reduce,
  inView,
}: {
  children: ReactNode;
  reduce: boolean;
  inView: boolean;
}) {
  return (
    <span className="text-sienna relative inline-block font-medium whitespace-nowrap">
      {children}
      <motion.span
        aria-hidden="true"
        className="bg-sienna absolute right-0 -bottom-[0.04em] left-0 h-[2px] origin-left"
        initial={reduce ? false : { scaleX: 0 }}
        animate={reduce ? undefined : { scaleX: inView ? 1 : 0 }}
        transition={{ duration: 0.8, delay: 1.4, ease }}
      />
    </span>
  );
}

/* ──────────────────────────────────────────────────────────────────────── */
/* YourMind — homepage section 2. White, centered, with a staged reveal      */
/* triggered once when the section scrolls into view.                        */
/* ──────────────────────────────────────────────────────────────────────── */

export function YourMind() {
  const t = useTranslations("YourMind");
  const reduce = useReducedMotion() ?? false;
  const ref = useRef<HTMLElement>(null);
  const inView = useInView(ref, { once: true, margin: "-80px" });

  /* Motion props for a fade-and-rise element revealed `delay` seconds in.
     Under reduced motion this is empty, so the element renders statically. */
  const reveal = (delay: number) =>
    reduce
      ? {}
      : {
          initial: { opacity: 0, y: 16 },
          animate: inView ? { opacity: 1, y: 0 } : { opacity: 0, y: 16 },
          transition: { duration: 0.95, delay, ease },
        };

  return (
    <section ref={ref} className="relative overflow-hidden bg-white">
      {/* thin sienna hairline marking the section start */}
      <motion.div
        initial={reduce ? false : { scaleX: 0 }}
        animate={reduce ? undefined : { scaleX: inView ? 1 : 0 }}
        transition={{ duration: 1.6, delay: 0.1, ease }}
        className="bg-sienna/35 relative z-[2] mx-auto h-px w-[120px] origin-center"
      />

      {/* drifting background motif */}
      <ThoughtLines reduce={reduce} inView={inView} />

      {/* white focus-fade so the lines never sit behind the headline */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 z-[1]"
        style={{
          background:
            "radial-gradient(ellipse 46% 60% at 50% 48%, #fff 0%, #fff 40%, rgba(255,255,255,0) 80%)",
        }}
      />

      <div className="relative z-[2] mx-auto max-w-[920px] px-6 pt-28 pb-28 md:px-12 md:pt-36 md:pb-32">
        {/* eyebrow */}
        <motion.p
          {...reveal(0.15)}
          className="text-espresso-40 text-center text-[0.75rem] font-medium tracking-[0.32em] uppercase italic"
        >
          {t("eyebrow")}
        </motion.p>

        {/* headline — quiet setup line, then the full-weight punch */}
        <h2 className="font-sans mx-auto mt-10 max-w-[21ch] text-center text-[clamp(2.3rem,4.5vw,4.1rem)] leading-[1.09] font-normal tracking-[-0.032em] text-balance md:mt-12">
          <motion.span {...reveal(0.3)} className="text-espresso-60 block">
            {t("headlineSetup")}
          </motion.span>
          <motion.span {...reveal(0.8)} className="text-espresso block">
            {t.rich("headlinePunch", {
              point: (chunks) => (
                <Point reduce={reduce} inView={inView}>
                  {chunks}
                </Point>
              ),
            })}
          </motion.span>
        </h2>

        {/* body */}
        <motion.p
          {...reveal(1.9)}
          className="text-espresso/75 mx-auto mt-9 max-w-[600px] text-center text-[clamp(1.0625rem,1.2vw,1.1rem)] leading-[1.72]"
        >
          {t("body")}
        </motion.p>

        {/* coda — Jobs-style landing line */}
        <motion.p
          {...reveal(2.5)}
          className="text-espresso-60 mt-6 text-center text-[1.3rem] italic"
        >
          {t("coda")}
        </motion.p>

        {/* CTA */}
        <motion.div {...reveal(2.85)} className="mt-11 flex justify-center">
          <a
            href="#"
            className="group bg-espresso text-cream-50 hover:bg-sienna inline-flex items-center gap-3 rounded-full px-7 py-4 text-sm font-medium tracking-[0.01em] transition-all duration-300 ease-out hover:-translate-y-px hover:gap-5 active:translate-y-0 active:scale-[0.98]"
          >
            {t("cta")}
            <ArrowRight
              className="size-4 transition-transform duration-300 group-hover:translate-x-0.5"
              strokeWidth={1.5}
            />
          </a>
        </motion.div>
      </div>
    </section>
  );
}
```

- [ ] **Step 2: Type-check**

Run: `npm run type-check`
Expected: completes with no errors (exit 0, no output).

- [ ] **Step 3: Lint**

Run: `npm run lint`
Expected: no errors reported for `src/components/site/your-mind.tsx`.

- [ ] **Step 4: Visual check in the dev server**

Ensure the dev server is running (`npm run dev`; it serves `http://localhost:3000`). Open `http://localhost:3000/en`, scroll to the second section (just below the hero).

Confirm:
- White background, centered content, no horizontal scrollbar.
- Eyebrow "THE HUMAN ADVANTAGE", headline with the lighter setup line and the
  darker punch line, "the point" in sienna with an underline, body paragraph,
  italic coda "That's the whole idea.", and the dark pill CTA.
- On first scroll into view the elements fade/rise in sequence; the four faint
  lines drift slowly and are not visible directly behind the headline.

- [ ] **Step 5: Commit**

```bash
git add src/components/site/your-mind.tsx
git commit -m "Rebuild YourMind section: kinetic statement with thought-lines motif

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: Final verification

**Files:** none modified unless a check fails.

- [ ] **Step 1: Production build**

Run: `npm run build`
Expected: build completes successfully; the `/[locale]` route is listed; no
errors or new warnings referencing `your-mind.tsx`.

- [ ] **Step 2: Reduced-motion check**

Verify the section renders fully static when reduced motion is requested. With
Playwright MCP available, emulate it:
```js
// browser_run_code_unsafe is blocked; instead use the dev server with the OS
// "reduce motion" setting enabled, OR Chrome DevTools > Rendering >
// "Emulate CSS prefers-reduced-motion: reduce", then reload http://localhost:3000/en.
```
Confirm: all content (eyebrow, headline, body, coda, CTA) is visible
immediately with no entrance animation, the underline under "the point" is
fully drawn, and the background lines do not drift.

- [ ] **Step 3: Responsive check**

In the browser, view `http://localhost:3000/en` at ~375px (mobile), ~768px
(tablet), and ~1440px (desktop) widths. Confirm at every width: no horizontal
overflow, the headline stays readable and balanced, and the section keeps
generous vertical padding.

- [ ] **Step 4: Commit any fixes**

If Steps 1–3 surfaced issues and you changed files, commit them:
```bash
git add -A
git commit -m "Fix YourMind section issues found in verification

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```
If nothing changed, skip this step.

---

## Notes for the implementer

- **No test runner exists.** Do not add Vitest/Jest/RTL — that is out of scope.
  Verification is type-check + lint + build + visual inspection, as written.
- **`reveal()` returns `{}` under reduced motion** on purpose: spreading an
  empty object onto a `motion.*` element leaves it at its natural (final)
  state with no animation.
- **The drift loop is seamless** because each line's path spans x:0..1800 and
  the animation translates exactly one 600px wave period.
- **`page.tsx` must not change** — the `YourMind` export name is preserved.
- The CTA `href="#"` is intentional — every CTA on the site is currently a
  placeholder; wiring routes is a separate task (see the design spec).
```

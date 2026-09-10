# Golden Hour Homepage — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Each section's *visual* polish is driven with the **frontend-design** skill in the browser — the plan locks structure, copy, wiring, and verification; the pixel-feel is tuned live.

**Goal:** Build BiGH's new homepage as an 8-screen "Golden Hour" scroll on a side branch of `codes\bigh-website`, reusing the existing i18n/content/chrome, without touching the clone.

**Architecture:** Reuse the clone's infrastructure (next-intl 6-locale routing, `content/harvest` product data, shared `SiteHeader`/`SiteFooter`, `next/image` originals). REPLACE the homepage body (`src/app/[locale]/page.tsx`) with eight new section components under `src/components/home/`, wrapped in a Golden-Hour dark theme scope. Port the self-contained three.js silk shader from `bigh-for-real` for the hero. All copy lives in the `Home` namespace of `messages/en.json`; the other five locales fall back to English (existing behavior) until translated.

**Tech Stack:** Next.js 16.2.6 (App Router, RSC), next-intl 4.11, Tailwind CSS 4, GSAP 3.15, three 0.184, React 19, TypeScript 5.

## Global Constraints
- **Branch:** all work on `golden-hour-home`, cut from current `homepage-rebuild` HEAD. NEVER commit to `main` or force-change the clone pages. The clone must remain intact and deployable.
- **Locales (exact):** `en, kr, jp, cns, hken, vn`. English copy only in this plan; untranslated locales fall back to English via the existing `src/i18n/request.ts`.
- **Checkout = link-out:** Login → `https://aeg.imatrixoffice.com`; Signup → `/signup`. No on-site cart.
- **Compliance (verbatim rules from `Positioning-Statement.md`):** structure/function language only; DSHEA disclaimer stays in the footer; NO disease words; NO "boosts/sharpens memory" as a promise; NO "anti-aging/reverse aging"; NO "neutralizes free radicals"; Berkeley = factual backdrop only, never an endorsement; EASA = "elected Member of the European Academy of Sciences and Arts"; NuriCell heritage = "the same formula, trusted for over 20 years" (market track record, not proof); Dr. Liu is the sole public face (Iris Wang not named).
- **Design source of truth:** `Dropbox\In-Basket\bigh-website\materials\Site-Design\Homepage-Design.md` + `Brand-and-Strategy\Positioning-Statement.md`.
- **Verification model (this is a design build, NOT unit-test-shaped):** each task's gate = (1) `npm run type-check` clean, (2) `npm run build` succeeds, (3) Playwright screenshot at 1440px + 390px reviewed against the design doc. No unit tests — they'd be low-value for static marketing sections. Commit after each green task.

---

### Task 1: Branch + Golden Hour theme scaffold + silk hero background

**Files:**
- Create branch `golden-hour-home` from `homepage-rebuild`.
- Create: `src/components/home/silk.tsx` (port of `bigh-for-real/src/app/a/silk.tsx`, self-contained — only imports `three`).
- Create: `src/components/home/theme.ts` (Golden-Hour token constants used across sections).
- Modify: `src/app/globals.css` — add a `.gh` scope block with the dark palette + serif display variable (append; do not alter existing `:root`).
- Modify: `src/app/[locale]/layout.tsx` — load a serif display font via `next/font/google` (Fraunces) exposed as `--font-gh-serif` (self-hosted at build; no runtime external fetch).

**Interfaces:**
- Produces: `<Silk />` default export (a fixed/absolute full-bleed canvas, `aria-hidden`, respects `prefers-reduced-motion`); CSS class `.gh` establishing `background:#04080F; color:#E6F0F7` and `--font-gh-serif`.

- [ ] **Step 1: Create the branch**

```bash
cd "C:/Users/mcbig/Documents/codes/bigh-website"
git checkout homepage-rebuild && git pull --ff-only 2>/dev/null; git checkout -b golden-hour-home
```

- [ ] **Step 2: Port the silk shader**

Copy `bigh-for-real/src/app/a/silk.tsx` → `src/components/home/silk.tsx` verbatim (it imports only `three`; no other deps). Keep the ember/navy shader as-is for now — palette warmth is a live-tuning decision with Mo in Task 2 review.

- [ ] **Step 3: Add the `.gh` theme scope to globals.css**

Append to `src/app/globals.css`:

```css
/* ── Golden Hour homepage scope (new site) ─────────────── */
.gh {
  --gh-bg: #04080f;
  --gh-fg: #e6f0f7;
  --gh-muted: #b9cbd9;
  --gh-faint: #6f8aa0;
  --gh-ember: #e9946a;      /* warm accent (reconcile gold vs ember with Mo) */
  --gh-line: rgba(230, 240, 247, 0.12);
  background: var(--gh-bg);
  color: var(--gh-fg);
}
.gh-serif { font-family: var(--font-gh-serif), Georgia, serif; }
```

- [ ] **Step 4: Load the serif display font**

In `src/app/[locale]/layout.tsx`, add:

```ts
import { Fraunces } from "next/font/google";
const ghSerif = Fraunces({ subsets: ["latin"], weight: ["400","500","600"], style: ["normal","italic"], variable: "--font-gh-serif", display: "swap" });
```

Add `ghSerif.variable` to the `<body>` (or `<html>`) className list.

- [ ] **Step 5: Verify build + typecheck**

Run: `npm run type-check && npm run build`
Expected: both succeed; no new type or lint errors.

- [ ] **Step 6: Commit**

```bash
git add -A && git commit -m "feat(home): golden-hour theme scaffold + ported silk hero background"
```

---

### Task 2: Screen 1 — The Hook (hero)

**Files:**
- Create: `src/components/home/hero.tsx` (client; GSAP headline reveal + `<Silk/>`).
- Modify: `messages/en.json` — add `Home.hero` copy keys.
- Modify: `src/app/[locale]/page.tsx` — begin the new page: `<main className="gh">` rendering `<Hero/>` (remove the clone sections in Task 10's final wiring; for now render `<Hero/>` above the existing content is NOT allowed — instead replace the file body with just `<Hero/>` so review is clean).

**Interfaces:**
- Consumes: `<Silk/>` from Task 1; `getTranslations("Home")`.
- Produces: `<Hero/>` (server wrapper passing translated strings into a client subcomponent for GSAP).

- [ ] **Step 1: Add hero copy to `messages/en.json`** under a new `Home` object:

```json
"Home": {
  "hero": {
    "line1": "Your mind has no",
    "line2": "expiration date.",
    "reveal": "Because aging well starts in your cells.",
    "cta": "See the science"
  }
}
```

- [ ] **Step 2: Build the hero component**

`src/components/home/hero.tsx` — port the headline structure from `bigh-for-real/src/app/a/page.tsx` (word-by-word GSAP rise, `data-word`, serif via `.gh-serif`, italic on `line2`), render `<Silk/>` behind, subhead = `reveal`, a single underline-arrow CTA → `#truth`. Respect reduced-motion (early-return the GSAP context, matching the source).

- [ ] **Step 3: Wire the page** — set `src/app/[locale]/page.tsx` body to:

```tsx
return (<main className="gh min-h-svh"><Hero eyebrow="" reveal={t("hero.reveal")} l1={t("hero.line1")} l2={t("hero.line2")} cta={t("hero.cta")} /></main>);
```

(keep `generateStaticParams` + `setRequestLocale`.)

- [ ] **Step 4: Verify** — `npm run type-check && npm run build`; then `npm run dev` and Playwright screenshot `http://localhost:3000/` at 1440×900 and 390×844.
Expected: dark silk hero, serif headline animates in, reveal line + CTA visible, header floats above.

- [ ] **Step 5: Palette reconcile checkpoint (with Mo)** — confirm navy-ember vs literal gold for the silk. Adjust shader base colors in `silk.tsx` only if she wants warmer/gold. Re-screenshot.

- [ ] **Step 6: Commit** — `git add -A && git commit -m "feat(home): screen 1 — Golden Hour hero"`

---

### Tasks 3–9: Screens 2–8 (one section each)

Each follows the SAME shape — create `src/components/home/<name>.tsx`, add its copy to `messages/en.json` `Home.<key>`, append `<Section/>` into `page.tsx` in order, then verify (type-check + build + Playwright at 1440/390) and commit. Sections are server components unless they need motion (then a thin client child, GSAP `Reveal`-style, reduced-motion safe). Use the existing `src/components/clone/reveal.tsx` for scroll-reveal. Copy is verbatim-draft from `Homepage-Design.md` — final wording gets the compliance/lawyer pass in Task 10.

- [ ] **Task 3 — Screen 2 "The Honest Truth"** (`truth.tsx`, id `truth`): cells run on power plants; slow with age; brain = ~20% of energy. Animated stat "2% of your body. 20% of its energy." Copy keys `Home.truth.{kicker,body,stat}`.
- [ ] **Task 4 — Screen 3 "Meet Dr. Liu"** (`scientist.tsx`, id `scientist`): photo slot (placeholder until Mo supplies), name, **"elected Member of the European Academy of Sciences and Arts"**, life's-work line, Berkeley/PNAS *factual backdrop*, pull-quote, CTA → `/science`. Keys `Home.liu.{name,honor,body,quote,cta}`. COMPLIANCE: no endorsement phrasing; Iris not named.
- [ ] **Task 5 — Screen 4 "NuriCell"** (`nuricell.tsx`, id `nuricell`): stacked story — built on Liu's research → "Not the biggest dose. The right one." (golden ratio) → ingredients your body knows → **"the same formula, trusted for over 20 years"** heritage marker. Bottle image from `content/harvest` via `loadPage`/`productImages`. CTA → `/nuricell`. Keys `Home.nuricell.{lead,dose,doseBody,ingredients,heritage,cta}`.
- [ ] **Task 6 — Screen 5 "The Family"** (`family.tsx`): grid of the other 5 (Turmerific, Advanced OPC, Green Bee Propolis, Nature Calm, Deer Horn Reishi), each card = name + its ONE honest "supports…" job + link to its product page. Pull names via `productName(slug, locale)`; images via `productImages`. Keys `Home.family.{title, jobs.<slug>}`.
- [ ] **Task 7 — Screen 6 "Made with Heart"** (`heart.tsx`): emotional peak — "Age well, together." / "For the people you love." Warm imagery slot. Keys `Home.heart.{title,body}`.
- [ ] **Task 8 — Screen 7 "Honest by Design"** (`honest.tsx`): three pledges (real doses / real science / no hype). Keys `Home.honest.{title, pledges[]}`.
- [ ] **Task 9 — Screen 8 "Start the Ritual"** (`ritual.tsx`): soft CTA — "Start with NuriCell" (→ iMatrix `https://aeg.imatrixoffice.com` or `/nuricell`) + secondary "Talk to a BiGH advisor". Keys `Home.ritual.{title, primary, secondary}`. Confirm `SiteFooter` renders below (with the DSHEA disclaimer).

---

### Task 10: Copy + compliance pass, full-scroll review, deploy preview

**Files:** `messages/en.json` (final English), `src/app/[locale]/page.tsx` (final ordering + `id`s for anchor scroll).

- [ ] **Step 1: Compliance sweep** — grep the `Home` copy for banned terms; confirm none:

Run: `grep -inE "alzheimer|dementia|parkinson|cancer|cure|anti-aging|reverse aging|boosts? memory|sharpen(s)? (your )?memory|clinically proven|neutraliz" messages/en.json`
Expected: no matches in the `Home` block (fix any hit).

- [ ] **Step 2: Full-scroll Playwright review** — screenshot the whole page at 1440 and 390; verify the arc reads hook → truth → Liu → NuriCell → family → heart → honest → ritual → footer, header/footer legible over dark, no layout breaks. Check one non-English locale (e.g. `/kr`) falls back to English cleanly.

- [ ] **Step 3: `npm run build`** succeeds; **`npm run type-check`** clean.

- [ ] **Step 4: Commit + push branch** — `git add -A && git commit -m "feat(home): copy + compliance pass, full 8-screen scroll" && git push -u origin golden-hour-home`

- [ ] **Step 5: Vercel preview** — `vercel deploy --yes --cwd "C:/Users/mcbig/Documents/codes/bigh-website"` (preview, NOT `--prod`). Share the preview URL with Mo.

---

## Self-Review notes
- **Spec coverage:** all 8 screens (Tasks 2–9) + global chrome (reused) + deeper-page links (Science/product CTAs) present; deeper *pages* themselves are explicitly out of scope (separate future plan, per design doc).
- **Compliance:** encoded as a Global Constraint + an automated grep gate (Task 10 Step 1) + the lawyer review flagged as a pre-launch item (not pre-build).
- **Open inputs (do NOT block the build):** Dr. Liu photo + permission, ALA form answer, lawyer wording review — all pre-launch, use placeholders meanwhile.
- **Palette risk:** the `/a` source Mo picked renders navy+ember, while the label says "Golden Hour / gold." Reconciled explicitly at Task 2 Step 5 with Mo before proceeding.

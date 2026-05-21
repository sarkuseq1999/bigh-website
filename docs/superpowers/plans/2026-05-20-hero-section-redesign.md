# Hero Section Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite the homepage hero as a brand-statement manifesto with a
looping Kling 3.0 aurora video background, a single lower-left content stack,
and a scroll-aware `SiteHeader` that adapts to the dark hero while in view.

**Architecture:** Pure UI feature. New hero is a single `"use client"` React
component with two internal helpers (`AuroraBackground`, `ScrollCue`).
Background is a native HTML `<video>` (image-to-video loop from Kling 3.0,
sped up 1.5× via `ffmpeg setpts=PTS/1.5`) with a `next/image` fallback under
reduced motion. Staged reveal via `motion/react`. The `SiteHeader` gains a
scroll-aware "dark-context" state that crossfades to a cream-light state once
the user has scrolled past the hero, driven by an `IntersectionObserver`
on a `[data-dark-context]` attribute placed on the hero section.

**Tech Stack:** Next.js 16, React 19, TypeScript, Tailwind 4,
`motion/react` 12, `next-intl` 4, `next/image`, `lucide-react`. No new
dependencies.

**Testing approach:** This project has no test framework (no Jest/Vitest).
Verification is via `npm run type-check`, `npm run build`, and manual
inspection in the dev server (Playwright via the MCP browser tool is
optional). Each task ends with a concrete "verify" step.

**Spec reference:** `docs/superpowers/specs/2026-05-20-hero-section-redesign-design.md`

---

## File Structure

**New files (committed):**
- `public/hero/candidate-aurora.jpg` — already on disk, needs commit (2.8 MB JPEG)
- `public/hero/aurora-loop-1.5x.mp4` — already on disk, needs commit (2.1 MB MP4)

**Files modified:**
- `src/components/site/hero.tsx` — full rewrite in place (export name preserved)
- `src/components/site/site-header.tsx` — add scroll-aware dark-context state
- `src/components/site/your-mind.tsx` — add `id="yourmind"` and `data-dark-context` is NOT applied here (data-dark-context goes on the hero only)
- `messages/en.json` — update `Hero` namespace (5 new keys, drop `ctaSecondary`)
- `messages/es.json` / `ja.json` / `ko.json` / `zh.json` — mirror the new `Hero` key shape (English placeholders for non-EN)

**Files NOT touched (per spec non-goals):**
- `src/app/[locale]/page.tsx`
- Any other section component
- Any existing `public/hero/*.jpg` files (the old star-trails image stays on disk, unused)

---

## Task 1: Stage and commit the hero assets

Both assets exist on disk but are untracked. Commit them first so subsequent
code changes that reference them are reproducible from a fresh clone.

**Files:**
- Commit: `public/hero/candidate-aurora.jpg` (2.8 MB)
- Commit: `public/hero/aurora-loop-1.5x.mp4` (2.1 MB)

- [ ] **Step 1.1: Verify both files exist on disk**

Run from project root:

```bash
ls -la public/hero/candidate-aurora.jpg public/hero/aurora-loop-1.5x.mp4
```

Expected: both files listed, candidate-aurora.jpg ≈ 2.8 MB, aurora-loop-1.5x.mp4 ≈ 2.1 MB.

If either is missing: the brainstorm assets were lost. Stop and ask the user
to regenerate (Gemini for the still, Kling 3.0 for the loop, then
`ffmpeg -y -i aurora-loop.mp4 -filter:v "setpts=PTS/1.5" -an -c:v libx264 -crf 20 -preset slow aurora-loop-1.5x.mp4`).

- [ ] **Step 1.2: Stage and commit**

```bash
git add public/hero/candidate-aurora.jpg public/hero/aurora-loop-1.5x.mp4
git commit -m "Add hero aurora still and looping video assets

Generated still via Gemini (2.8 MB, 2K JPEG); video loop via
Kling 3.0 image-to-video (15s @ 4K) sped 1.5x via ffmpeg
(2.1 MB, 10s, 1080p, 24fps, H.264). Both required by the
hero section redesign spec dated 2026-05-20."
```

- [ ] **Step 1.3: Verify the commit landed**

```bash
git log --oneline -1
git status --short public/hero/
```

Expected: latest commit is the hero assets commit; `git status` shows no
output for `public/hero/candidate-aurora.jpg` or `aurora-loop-1.5x.mp4`
(both tracked and clean).

---

## Task 2: Update i18n message catalogs

The `Hero` namespace changes shape: drop `ctaSecondary`, update `headline` /
`subhead` / `cta`, add `scrollCue`, replace `imageAlt`. All five locale
files mirror the same key shape (English placeholders for non-EN locales —
real translations are a follow-up task).

**Files:**
- Modify: `messages/en.json`
- Modify: `messages/es.json`
- Modify: `messages/ja.json`
- Modify: `messages/ko.json`
- Modify: `messages/zh.json`

- [ ] **Step 2.1: Update `messages/en.json` — `Hero` namespace**

Find the `"Hero": { ... }` block (currently lines 15–21) and replace it
with:

```json
  "Hero": {
    "headline": "Your mind has no <em>expiration date.</em>",
    "subhead": "Sharpness at every age isn't luck — it's nature and science. BiGH gives your brain the fuel and protection it needs — in one daily ritual.",
    "cta": "Continue",
    "scrollCue": "Scroll",
    "imageAlt": "Slow amber aurora over a distant mountain horizon"
  },
```

Note: `ctaSecondary` is removed (single-CTA hero). The em-dashes (`—`) in
`subhead` are U+2014, the same character used elsewhere in `en.json`.

- [ ] **Step 2.2: Mirror the same `Hero` shape into `messages/es.json`**

Find the `"Hero": { ... }` block in `messages/es.json` and replace it with
**exactly the English values from Step 2.1** (placeholders — real Spanish
translations are out of scope). The build must not error on missing keys.

```json
  "Hero": {
    "headline": "Your mind has no <em>expiration date.</em>",
    "subhead": "Sharpness at every age isn't luck — it's nature and science. BiGH gives your brain the fuel and protection it needs — in one daily ritual.",
    "cta": "Continue",
    "scrollCue": "Scroll",
    "imageAlt": "Slow amber aurora over a distant mountain horizon"
  },
```

- [ ] **Step 2.3: Mirror the same `Hero` shape into `messages/ja.json`**

Same five English placeholder values, identical to Step 2.2.

- [ ] **Step 2.4: Mirror the same `Hero` shape into `messages/ko.json`**

Same five English placeholder values, identical to Step 2.2.

- [ ] **Step 2.5: Mirror the same `Hero` shape into `messages/zh.json`**

Same five English placeholder values, identical to Step 2.2.

- [ ] **Step 2.6: Validate every locale file is still valid JSON**

```bash
node -e "['en','es','ja','ko','zh'].forEach(l => { JSON.parse(require('fs').readFileSync('messages/'+l+'.json','utf8')); console.log(l, 'OK'); });"
```

Expected output:
```
en OK
es OK
ja OK
ko OK
zh OK
```

If any locale errors: open it and fix the syntax (usually a stray comma).

- [ ] **Step 2.7: Run type-check to confirm `next-intl` is happy**

```bash
npm run type-check
```

Expected: passes with no errors. `next-intl` doesn't validate keys at
type-check time by default; the real validation is at runtime / build time
(later).

- [ ] **Step 2.8: Commit**

```bash
git add messages/en.json messages/es.json messages/ja.json messages/ko.json messages/zh.json
git commit -m "Update Hero i18n namespace for new manifesto copy

- Replace headline (single line, sienna italic accent on 'expiration date')
- Replace subhead (introduces BiGH + 'daily ritual')
- Rename CTA: 'Discover the line' -> 'Continue' (scrolls to next section)
- Drop ctaSecondary (single-CTA hero)
- Add scrollCue ('Scroll')
- Replace imageAlt (now describes the aurora background)

Non-English locales mirror the English values as placeholders. Real
translations are a follow-up task."
```

---

## Task 3: Add anchor target to YourMind section

The hero's "Continue" CTA scrolls to the YourMind section. That section
needs an `id="yourmind"` on its root `<section>` so `getElementById` can
find it.

**Files:**
- Modify: `src/components/site/your-mind.tsx:101`

- [ ] **Step 3.1: Add `id="yourmind"` to the YourMind section element**

Open `src/components/site/your-mind.tsx` and find line 101:

```tsx
    <section ref={ref} className="relative overflow-hidden bg-white">
```

Replace it with:

```tsx
    <section id="yourmind" ref={ref} className="relative overflow-hidden bg-white">
```

That is the only change to this file.

- [ ] **Step 3.2: Type-check**

```bash
npm run type-check
```

Expected: passes.

- [ ] **Step 3.3: Commit**

```bash
git add src/components/site/your-mind.tsx
git commit -m "Add id='yourmind' anchor to YourMind section

Scoped change so the new hero's 'Continue' CTA can scrollIntoView
to this section. See docs/superpowers/specs/2026-05-20-hero-section-redesign-design.md"
```

---

## Task 4: Rewrite the Hero component

Replace `src/components/site/hero.tsx` with the new implementation. The
section is `min-h-[100dvh]`, dark, full-bleed video background with a still
fallback under reduced motion, a dark gradient overlay for legibility, and
a lower-left content stack revealed in sequence on mount.

**Files:**
- Modify (full rewrite): `src/components/site/hero.tsx`

- [ ] **Step 4.1: Replace the file with the new implementation**

Replace the **entire** contents of `src/components/site/hero.tsx` with:

```tsx
"use client";

import { useRef } from "react";
import Image from "next/image";
import { motion, useReducedMotion } from "motion/react";
import { useTranslations } from "next-intl";
import { ArrowRight } from "lucide-react";

const ease = [0.2, 0.7, 0.2, 1] as const;

/* ──────────────────────────────────────────────────────────────────────── */
/* AuroraBackground — looping aurora video with a still fallback under      */
/* reduced motion. The still also serves as the video's poster (visible     */
/* during initial fetch). A dark gradient overlay sits above the media for  */
/* type legibility on the lower-left content stack.                          */
/* ──────────────────────────────────────────────────────────────────────── */

function AuroraBackground({
  reduce,
  imageAlt,
}: {
  reduce: boolean;
  imageAlt: string;
}) {
  return (
    <>
      {reduce ? (
        <Image
          src="/hero/candidate-aurora.jpg"
          alt={imageAlt}
          fill
          priority
          sizes="100vw"
          className="absolute inset-0 -z-10 object-cover"
        />
      ) : (
        <video
          autoPlay
          muted
          loop
          playsInline
          preload="auto"
          poster="/hero/candidate-aurora.jpg"
          aria-hidden="true"
          className="absolute inset-0 -z-10 h-full w-full object-cover"
        >
          <source src="/hero/aurora-loop-1.5x.mp4" type="video/mp4" />
        </video>
      )}

      {/* Dark gradient overlay for legibility — z-0 so it sits above the
          media (which is -z-10) but below the content (which is z-10).     */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 z-0"
        style={{
          background:
            "linear-gradient(95deg, rgba(15,10,25,0.85) 0%, rgba(15,10,25,0.55) 28%, rgba(15,10,25,0.12) 52%, transparent 72%), linear-gradient(180deg, transparent 50%, rgba(15,10,25,0.55) 100%)",
        }}
      />
    </>
  );
}

/* ──────────────────────────────────────────────────────────────────────── */
/* ScrollCue — small uppercase label + hairline at the bottom-center.       */
/* Hidden under reduced motion (the cue implies motion).                     */
/* ──────────────────────────────────────────────────────────────────────── */

function ScrollCue({ label, reduce }: { label: string; reduce: boolean }) {
  if (reduce) return null;
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.9, delay: 1.4, ease }}
      className="absolute bottom-6 left-1/2 z-10 -translate-x-1/2 text-center"
      aria-hidden="true"
    >
      <span className="text-cream-50/50 text-[10px] tracking-[0.32em] uppercase">
        {label}
      </span>
      <span className="bg-cream-50/35 mx-auto mt-2 block h-[18px] w-px" />
    </motion.div>
  );
}

/* ──────────────────────────────────────────────────────────────────────── */
/* Hero — homepage section 1. Brand-statement manifesto with looping aurora */
/* video background and a lower-left content stack revealed in sequence on  */
/* mount. The CTA scrolls smoothly to the YourMind section (`#yourmind`).    */
/*                                                                          */
/* `data-dark-context` is read by SiteHeader (via IntersectionObserver) to  */
/* switch the header into its dark-context visual mode while the hero is in */
/* view.                                                                     */
/* ──────────────────────────────────────────────────────────────────────── */

export function Hero() {
  const t = useTranslations("Hero");
  const reduce = useReducedMotion() ?? false;
  const sectionRef = useRef<HTMLElement>(null);

  /* Motion props for a fade-and-rise element revealed `delay` seconds in.
     Under reduced motion this is empty, so the element renders statically. */
  const reveal = (delay: number) =>
    reduce
      ? {}
      : {
          initial: { opacity: 0, y: 16 },
          animate: { opacity: 1, y: 0 },
          transition: { duration: 0.9, delay, ease },
        };

  const scrollToNext = () => {
    const target = document.getElementById("yourmind");
    const behavior: ScrollBehavior = reduce ? "auto" : "smooth";
    if (target) {
      target.scrollIntoView({ behavior, block: "start" });
    } else {
      window.scrollTo({ top: window.innerHeight, behavior });
    }
  };

  return (
    <section
      ref={sectionRef}
      data-dark-context
      className="relative isolate min-h-[100dvh] overflow-hidden bg-[#0a0a1a]"
    >
      <AuroraBackground reduce={reduce} imageAlt={t("imageAlt")} />

      {/* Lower-left content stack. flex justify-end pushes content to the
          bottom of the section; max-width keeps it from spreading across
          the brightest aurora area.                                       */}
      <div className="relative z-10 mx-auto flex min-h-[100dvh] max-w-[1320px] flex-col justify-end px-6 pt-24 pb-20 md:px-14 md:pt-32 md:pb-24">
        <div className="max-w-[640px] md:max-w-[58%]">
          <motion.h1
            {...reveal(0.3)}
            className="font-display text-cream-50 m-0 text-[clamp(2.5rem,6.4vw,4.875rem)] leading-[1.02] font-light tracking-[-0.025em] text-balance"
          >
            {t.rich("headline", {
              em: (chunks) => (
                <em className="text-sienna font-normal not-italic [font-style:italic]">
                  {chunks}
                </em>
              ),
            })}
          </motion.h1>

          <motion.p
            {...reveal(0.7)}
            className="text-cream-50/80 mt-8 max-w-[560px] text-[clamp(0.95rem,1.2vw,1.125rem)] leading-[1.62]"
          >
            {t("subhead")}
          </motion.p>

          <motion.div {...reveal(1.0)} className="mt-9">
            <button
              type="button"
              onClick={scrollToNext}
              className="group bg-cream-50 text-espresso hover:bg-sienna hover:text-cream-50 inline-flex items-center gap-2.5 rounded-full px-7 py-3.5 text-sm font-medium tracking-[0.01em] transition-all duration-300 ease-out hover:-translate-y-px active:translate-y-0 active:scale-[0.98]"
            >
              {t("cta")}
              <ArrowRight
                className="size-4 transition-transform duration-300 group-hover:translate-x-0.5"
                strokeWidth={1.5}
              />
            </button>
          </motion.div>
        </div>
      </div>

      <ScrollCue label={t("scrollCue")} reduce={reduce} />
    </section>
  );
}
```

- [ ] **Step 4.2: Type-check**

```bash
npm run type-check
```

Expected: passes. If you see "Cannot find name `JSX`" or similar, you're
on an older TS config — this file uses React 19 / TS 5 idioms and the
project is already on those versions; the most likely real error is a
mis-typed import. Re-check the imports against the code block above.

- [ ] **Step 4.3: Start dev server and visually verify**

In a separate terminal:

```bash
npm run dev
```

Open `http://localhost:3000` (or whatever port Next reports).

Verify:
1. Hero takes the full viewport height.
2. Aurora video plays automatically, muted, looping. (If not playing on
   Safari, confirm `playsInline` is in the JSX.)
3. After ~0.3s, the headline fades up. ~0.7s the subhead. ~1.0s the CTA.
   ~1.4s the scroll cue. (Refresh to replay.)
4. The headline is light cream serif; the words "expiration date." are
   sienna italic.
5. The "Continue" CTA is a cream pill with espresso text. Hover: turns
   sienna with cream text, lifts 1px.
6. Click "Continue" — page should smooth-scroll down to the YourMind
   section. (If you only added the `id` in Task 3, this works. If not,
   it falls back to scrolling one viewport.)
7. Open DevTools → Console: no new errors. (The `SiteHeader` will still
   look wrong over the dark hero — cream/dark text — that's fixed in
   Task 5.)
8. Open DevTools → Rendering → Emulate "prefers-reduced-motion: reduce".
   Refresh. Expected: still image instead of video, all content visible
   immediately (no reveal), scroll cue hidden.

If the video shows a brief flash of an unstyled state before loading: the
`<section>` `bg-[#0a0a1a]` is supposed to mask that. If the flash is
white, double-check the section class string.

- [ ] **Step 4.4: Commit**

```bash
git add src/components/site/hero.tsx
git commit -m "Rewrite Hero as brand-statement manifesto with aurora video

- Full-bleed Kling 3.0 aurora loop (1.5x speed, 10s, H.264) with
  next/image still fallback under prefers-reduced-motion
- Single lower-left content stack: headline, subhead, one CTA
- Staged reveal on mount via motion/react (headline 0.30s,
  subhead 0.70s, CTA 1.00s, scroll cue 1.40s)
- 'Continue' CTA scrolls to YourMind section (#yourmind) with
  smooth or auto behavior based on reduced-motion preference
- data-dark-context attribute marks the hero for SiteHeader
  intersection observation (Task 5)

See docs/superpowers/specs/2026-05-20-hero-section-redesign-design.md"
```

---

## Task 5: Add scroll-aware dark-context state to SiteHeader

The current `SiteHeader` is cream/70 + dark text — invisible/mismatched
over the new dark hero. Add an `isDark` state that turns true while any
`[data-dark-context]` element is in view, and crossfade the header's
visual style between the two modes.

**Files:**
- Modify: `src/components/site/site-header.tsx`

- [ ] **Step 5.1: Replace the file with the new implementation**

Replace the **entire** contents of `src/components/site/site-header.tsx`
with:

```tsx
"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import { Menu } from "lucide-react";
import { useTranslations } from "next-intl";

import { Link } from "@/i18n/navigation";
import { Button } from "@/components/ui/button";
import {
  Sheet,
  SheetContent,
  SheetTrigger,
  SheetTitle,
  SheetDescription,
  SheetHeader,
} from "@/components/ui/sheet";
import { LanguageSwitcher } from "@/components/site/language-switcher";
import { cn } from "@/lib/utils";

const NAV_KEYS = ["home", "about", "products", "science", "support"] as const;
const NAV_HREFS: Record<(typeof NAV_KEYS)[number], string> = {
  home: "/",
  products: "/products",
  science: "/#science",
  about: "/about",
  support: "/support",
};

export function SiteHeader() {
  const tNav = useTranslations("Nav");
  const tBrand = useTranslations("Brand");
  const [open, setOpen] = useState(false);
  const [isDark, setIsDark] = useState(false);

  /* Watch any [data-dark-context] element on the page. While at least one is
     intersecting (with the header's 72px offset), the header is in dark
     mode. When none are intersecting (or none exist), it reverts to its
     default cream-light mode. The "h-24" header is 96px in Tailwind, but we
     use 72px so the transition fires slightly before the hero edge crosses
     the header's bottom — feels less abrupt.                                */
  useEffect(() => {
    const targets = document.querySelectorAll<HTMLElement>("[data-dark-context]");
    if (targets.length === 0) {
      setIsDark(false);
      return;
    }

    const visible = new Set<Element>();
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            visible.add(entry.target);
          } else {
            visible.delete(entry.target);
          }
        }
        setIsDark(visible.size > 0);
      },
      { rootMargin: "-72px 0px 0px 0px", threshold: 0 },
    );

    targets.forEach((el) => observer.observe(el));
    return () => observer.disconnect();
  }, []);

  return (
    <header
      data-mode={isDark ? "dark" : "light"}
      className={cn(
        "absolute top-0 right-0 left-0 z-50 w-full backdrop-blur-md transition-colors duration-300 ease-out",
        isDark ? "bg-[#0a0a1a]/30" : "bg-cream-50/70",
      )}
    >
      <div className="mx-auto flex h-24 max-w-6xl items-center justify-between px-6">
        <Link
          href="/"
          aria-label={tBrand("name")}
          className="relative inline-flex h-18 items-center"
        >
          {/* Two logos, crossfaded by opacity based on isDark. Keeping both
              mounted avoids a flash on the transition.                      */}
          <Image
            src="/logo-black.png"
            alt={tBrand("name")}
            width={768}
            height={430}
            priority
            className={cn(
              "block h-18 w-auto transition-opacity duration-300",
              isDark ? "opacity-0" : "opacity-100",
            )}
          />
          <Image
            src="/logo-white.png"
            alt=""
            width={300}
            height={168}
            priority
            aria-hidden="true"
            className={cn(
              "absolute inset-0 block h-18 w-auto transition-opacity duration-300",
              isDark ? "opacity-100" : "opacity-0",
            )}
          />
        </Link>

        <nav className="hidden items-center gap-8 md:flex">
          {NAV_KEYS.map((key) => (
            <Link
              key={key}
              href={NAV_HREFS[key]}
              className={cn(
                "hover:text-sienna text-xl font-medium transition-colors duration-300",
                isDark ? "text-cream-50" : "text-espresso",
              )}
            >
              {tNav(key)}
            </Link>
          ))}
          <span
            className={cn(
              "mx-2 block h-5 w-px transition-colors duration-300",
              isDark ? "bg-cream-50/25" : "bg-espresso/15",
            )}
          />
          <LanguageSwitcher />
        </nav>

        <div className="flex items-center gap-1 md:hidden">
          <Sheet open={open} onOpenChange={setOpen}>
            <SheetTrigger
              render={
                <Button
                  variant="ghost"
                  size="icon"
                  aria-label={tNav("openMenu")}
                  className={cn(
                    "transition-colors duration-300",
                    isDark
                      ? "text-cream-50 hover:bg-cream-50/10 hover:text-sienna"
                      : "",
                  )}
                />
              }
            >
              <Menu />
            </SheetTrigger>
            <SheetContent side="right" className="w-72">
              <SheetHeader>
                <SheetTitle>{tBrand("name")}</SheetTitle>
                <SheetDescription className="sr-only">
                  {tNav("openMenu")}
                </SheetDescription>
              </SheetHeader>
              <nav className="flex flex-col gap-1 px-4">
                {NAV_KEYS.map((key) => (
                  <Link
                    key={key}
                    href={NAV_HREFS[key]}
                    onClick={() => setOpen(false)}
                    className="text-foreground/80 hover:bg-foreground/5 hover:text-foreground rounded-md px-2 py-2 text-base font-medium transition-colors"
                  >
                    {tNav(key)}
                  </Link>
                ))}
                <LanguageSwitcher variant="mobile" />
              </nav>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  );
}
```

Note: the mobile sheet drawer keeps its existing styling — the sheet
itself has its own background/contrast and is unaffected by the page
context.

- [ ] **Step 5.2: Verify `LanguageSwitcher` works in dark mode**

Open `src/components/site/language-switcher.tsx` and skim its classes.
If the button face uses `text-espresso` or a similar dark-on-light token
without considering the surrounding context, note it.

```bash
grep -n "text-espresso\|text-cream" src/components/site/language-switcher.tsx
```

If the switcher's button surface uses dark-on-light tokens, it will be
hard to see over the dark hero. **Two acceptable resolutions:**

1. **Leave it as-is for now.** Most users won't open the language menu
   while on the hero, and the menu surface itself (the popover) is
   self-contained.
2. **Pass `isDark` down** as a prop. Out of scope for this task — log it
   as a follow-up if the visual is unacceptable.

For this plan, default to option 1. Do not modify `language-switcher.tsx`.

- [ ] **Step 5.3: Type-check**

```bash
npm run type-check
```

Expected: passes.

- [ ] **Step 5.4: Verify in the dev server**

With the dev server still running (Task 4.3), refresh the page.

Verify:
1. On page load (hero in view): header background is dark-translucent
   (`bg-[#0a0a1a]/30 backdrop-blur-md`); nav links are cream; logo is
   the white variant.
2. Scroll down slowly. Around the moment the hero's bottom edge crosses
   the bottom of the header (~72px from the top of the viewport), the
   header crossfades to its previous cream-light state (cream/70 bg,
   espresso text, black logo). This should take ~300ms.
3. Scroll back up. The header crossfades back to dark mode as the hero
   re-enters.
4. Resize the viewport to a narrow width (sub-768px). The mobile menu
   icon should also be cream over the hero, espresso below it.
5. No console errors. (`useEffect` cleanup unobserves on unmount.)

If the transition is visible but feels "jittery" (toggling rapidly near
the threshold), the rootMargin can be tightened to `-96px` (full header
height) for a sharper cutoff. Don't change it unless the jitter is real.

- [ ] **Step 5.5: Commit**

```bash
git add src/components/site/site-header.tsx
git commit -m "Add scroll-aware dark-context state to SiteHeader

While any [data-dark-context] element is intersecting (offset by
the 72px header height), the header crossfades to a
dark-translucent background, cream nav text, the white logo
variant, and a cream separator. Off-intersection, the header
reverts to its existing cream-light state.

IntersectionObserver-driven (single observer for all matching
targets); cleanup on unmount. No prop API change to SiteHeader."
```

---

## Task 6: Final verification — type-check, build, full visual pass

End-to-end sanity check. The previous tasks each ran their own type-check
and dev-server checks, but they were piecewise. Here we run a clean build
and walk through the full hero behavior once.

**Files:**
- (no code changes — verification only)

- [ ] **Step 6.1: Stop the dev server (if still running)**

In the dev-server terminal: `Ctrl+C`.

- [ ] **Step 6.2: Run a clean type-check**

```bash
npm run type-check
```

Expected: no errors.

- [ ] **Step 6.3: Run a production build**

```bash
npm run build
```

Expected: build completes successfully. Look for any `next-intl` warning
about missing keys in any locale — if you see one, go back to Task 2
and confirm all five locale files have the same five `Hero` keys.

If the build complains about the `<video>` tag being inside a
component that imports `next/image`, or any other Next.js-specific
warning: read the message carefully — it's almost certainly about a
missing import or stale cache. `rm -rf .next` and re-run.

- [ ] **Step 6.4: Run the production build locally and walk through the hero**

```bash
npm run start
```

Open `http://localhost:3000`.

Walk through this checklist (mark each in the commit message):

1. **Hero loads.** Section is full-bleed dark, video starts playing
   muted within a second of load.
2. **Reveal sequence.** Refresh once. Headline rises into place at
   ~0.30s, subhead at ~0.70s, CTA at ~1.00s, scroll cue at ~1.40s.
3. **Loop is seamless.** Watch the video for two full cycles (~20s).
   No visible cut at the loop point.
4. **Headline copy.** Reads exactly: *"Your mind has no expiration date."*
   with "expiration date." in sienna italic.
5. **Subhead copy.** Reads exactly: *"Sharpness at every age isn't luck —
   it's nature and science. BiGH gives your brain the fuel and protection
   it needs — in one daily ritual."*
6. **CTA copy and behavior.** Button reads *"Continue"* with an arrow.
   Hover: cream → sienna, lifts 1px. Click: smooth-scrolls down to the
   YourMind section (the "Everyone is talking about artificial
   intelligence" heading should be roughly centered in view).
7. **Header dark mode on hero.** Header shows cream nav text and white
   logo over the dark hero.
8. **Header light mode after hero.** Scroll down past the hero. Around
   the moment the hero's bottom crosses the header, the header
   crossfades to cream/70 + dark text + black logo.
9. **Header back to dark mode.** Scroll up. Header crossfades back.
10. **Mobile (≤ 767px).** Resize the window narrow. The content stack
    should still sit lower-left, headline fluid-scales smaller. Mobile
    menu icon is cream over the hero, espresso below.
11. **Reduced motion.** Open DevTools → Rendering → Emulate
    `prefers-reduced-motion: reduce`. Hard refresh. Video is replaced
    by the still image. No reveal — all content is visible immediately.
    Scroll cue is hidden. Click "Continue": page jumps (not scrolls
    smoothly) to YourMind.
12. **No console errors** on any of the above.

- [ ] **Step 6.5: Commit verification**

If everything passed, no code commit is needed (Task 6 is verification).

If you found and fixed a small issue during this pass, commit it as its
own small commit before stopping:

```bash
git add <changed-files>
git commit -m "Fix hero <thing> noticed during final verification"
```

- [ ] **Step 6.6: Tag the branch state for review**

```bash
git log --oneline -8
```

Confirm the recent commits in order:

```
<sha> Fix hero <thing> noticed during final verification   (only if 6.5 ran)
<sha> Add scroll-aware dark-context state to SiteHeader
<sha> Rewrite Hero as brand-statement manifesto with aurora video
<sha> Add id='yourmind' anchor to YourMind section
<sha> Update Hero i18n namespace for new manifesto copy
<sha> Add hero aurora still and looping video assets
<sha> Add design spec for hero section redesign       (already shipped pre-plan)
```

If the commits are in this order on the current branch, the hero
redesign is complete and ready for review.

---

## Self-review (already performed)

The spec's requirements were checked back against this plan:

- **Visual (video + still + dark overlay):** Task 4.1's `AuroraBackground`.
- **Composition (C1 lower-left anchor):** Task 4.1's content stack.
- **Copy (headline, subhead, CTA, scrollCue, imageAlt):** Task 2 + Task 4.1.
- **No eyebrow:** Task 4.1 has none.
- **No secondary CTA:** Task 4.1 has one button only; Task 2.1 drops `ctaSecondary`.
- **Reveal sequence with exact delays:** Task 4.1's `reveal(delay)` calls.
- **Reduced motion fallback:** Task 4.1's `reduce` branches; ScrollCue returns null.
- **Primary CTA scroll behavior:** Task 4.1's `scrollToNext`; Task 3 adds the `id`.
- **SiteHeader scroll-aware dark-context:** Task 5 in full.
- **Asset files committed:** Task 1.
- **i18n updated across all 5 locales:** Task 2.
- **No other files touched (per non-goals):** Task list does not include `page.tsx` or any other section.

No placeholders, no unimplemented references, no contradictions found.

"use client";

import Image from "next/image";
import { motion } from "motion/react";
import { useReducedMotionSafe } from "@/components/site/use-reduced-motion-safe";
import { useTranslations } from "next-intl";

/* ─────────────────────────────────────────────────────────────────────────
   Premium ease curve shared across all staggered elements.
   Spec §6.S1: "slow premium ease, ~0.8s duration"
───────────────────────────────────────────────────────────────────────── */
const ease = [0.2, 0.7, 0.2, 1] as const;

/* Mount-reveal factory.
   The `animate` target must ALWAYS be present: the reduced-motion hook is
   hydration-safe (false on first render, real value after mount), so if we
   returned {} under reduce the element would be stuck at the `initial`
   opacity-0 state it mounted with. Keeping `animate` (with zero duration
   under reduce) guarantees the text always lands visible. */
function makeReveal(reduce: boolean, delay: number) {
  if (reduce) {
    return {
      initial: false as const,
      animate: { opacity: 1, y: 0 },
      transition: { duration: 0 },
    };
  }
  return {
    initial: { opacity: 0, y: 18 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.8, delay, ease },
  };
}

/* ─────────────────────────────────────────────────────────────────────────
   Hero — Section 1 "The Promise"
   Layout: two-zone editorial. Text stack left (lower-left on desktop),
   warm portrait image bleeding off the right.
   On mobile: text stacks above a shorter image block.
───────────────────────────────────────────────────────────────────────── */

export function Hero() {
  const t = useTranslations("Hero");
  const reduce = useReducedMotionSafe();

  /* Stagger delays: eyebrow → headline → subhead → paragraph → CTAs */
  const r = (delay: number) => makeReveal(reduce, delay);

  return (
    <section className="relative isolate min-h-[100dvh] overflow-hidden bg-paper">

      {/* ── Grid wrapper ──────────────────────────────────────────────── */}
      {/* On desktop the grid is exactly one viewport tall (no extra section
          padding stacked on top), so the hero never exceeds 100dvh; on mobile
          it stacks (text over image) and may grow taller to fit the content. */}
      <div className="relative mx-auto flex min-h-[100dvh] max-w-[1400px] flex-col md:grid md:grid-cols-[1fr_45%]">

        {/* ── LEFT: text stack ─────────────────────────────────────────── */}
        {/* justify-center vertically balances the stack. The top padding
            clears the fixed header from *within* the viewport-tall column
            (rather than adding to the section height), so the CTAs always
            sit above the fold on laptop viewports. */}
        <div className="relative z-10 flex flex-col justify-center pt-28 pb-12 pl-6 pr-6 md:pt-12 md:pb-12 md:pl-14 md:pr-10">
          <div className="max-w-[640px]">

            {/* Eyebrow */}
            <motion.p
              {...r(0)}
              className="mb-5 font-mono text-[0.6875rem] font-normal tracking-[0.2em] uppercase text-ink-soft"
            >
              {t("eyebrow")}
            </motion.p>

            {/* Headline */}
            <motion.h1
              {...r(0.12)}
              className="m-0 font-display text-[clamp(3rem,5.4vw,5.25rem)] font-light leading-[1.03] tracking-[-0.02em] text-balance text-ink"
            >
              {t.rich("headline", {
                em: (chunks) => (
                  <em className="font-display italic font-normal">{chunks}</em>
                ),
              })}
            </motion.h1>

            {/* Subhead — serif middle register between display and body */}
            <motion.p
              {...r(0.24)}
              className="mt-6 font-display text-[1.375rem] font-light leading-[1.35] text-ink md:text-[1.625rem]"
            >
              {t("subhead")}
            </motion.p>

            {/* Paragraph */}
            <motion.p
              {...r(0.36)}
              className="mt-5 max-w-[54ch] text-[1.125rem] leading-[1.6] text-ink-soft md:text-[1.1875rem]"
            >
              {t("paragraph")}
            </motion.p>

            {/* CTAs */}
            <motion.div
              {...r(0.48)}
              className="mt-8 flex flex-col gap-4 sm:flex-row sm:items-center"
            >
              {/* Primary — high-contrast ink pill */}
              <a
                href="#quiz"
                className="inline-flex min-h-[52px] items-center justify-center rounded-full bg-ink px-8 py-3 text-[1.0625rem] font-medium text-paper transition-colors duration-200 hover:bg-forest focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ink"
              >
                {t("ctaPrimary")}
              </a>

              {/* Secondary — text + arrow */}
              <a
                href="#nuricell"
                className="inline-flex min-h-[52px] items-center gap-1 text-[1.0625rem] font-medium text-ink underline-offset-4 hover:underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ink"
              >
                {t("ctaSecondary")}
              </a>
            </motion.div>

            {/* CTA payoff — what the quiz buys (readable at 55) */}
            <motion.p
              {...r(0.56)}
              className="mt-4 font-mono text-[0.8125rem] tracking-[0.1em] uppercase text-ink"
            >
              {t("ctaNote")}
            </motion.p>

          </div>
        </div>

        {/* ── RIGHT: portrait image block ──────────────────────────────── */}
        {/* On mobile this renders below the text at a fixed height.        */}
        {/* On desktop the photo sits inset as a framed editorial card so   */}
        {/* it never collides with the fixed header.                        */}
        <div className="relative h-[110vw] shrink-0 sm:h-[80vw] md:h-auto md:self-stretch md:py-24 md:pr-14">
          <div className="relative h-full w-full overflow-hidden rounded-none md:rounded-3xl">
            <motion.div
              className="relative h-full w-full"
              {...(reduce
                ? {}
                : {
                    initial: { scale: 1.0 },
                    animate: { scale: 1.04 },
                    transition: {
                      duration: 20,
                      ease: "linear",
                      repeat: Infinity,
                      repeatType: "mirror",
                    },
                  })}
            >
              <Image
                src="/images/hero-portrait-v3.jpg"
                alt={t("imageAlt")}
                fill
                priority
                sizes="(min-width: 768px) 45vw, 100vw"
                className="object-cover object-[center_30%]"
              />
            </motion.div>
          </div>
        </div>

      </div>
    </section>
  );
}

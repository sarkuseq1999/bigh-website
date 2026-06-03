"use client";

import { motion, useReducedMotion } from "motion/react";
import { useTranslations } from "next-intl";
import { Placeholder } from "@/components/site/placeholder";

/* ─────────────────────────────────────────────────────────────────────────
   Premium ease curve shared across all staggered elements.
   Spec §6.S1: "slow premium ease, ~0.8s duration"
───────────────────────────────────────────────────────────────────────── */
const ease = [0.2, 0.7, 0.2, 1] as const;

/* Mount-reveal factory.
   Under reduced-motion we return an empty object so the element renders
   statically (no transforms, no fade). */
function makeReveal(reduce: boolean, delay: number) {
  if (reduce) return {};
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
  const reduce = useReducedMotion() ?? false;

  /* Stagger delays: eyebrow → headline → subhead → paragraph → CTAs */
  const r = (delay: number) => makeReveal(reduce, delay);

  return (
    <section className="relative isolate min-h-[100dvh] overflow-hidden bg-paper pt-28 md:pt-32">

      {/* ── Grid wrapper ──────────────────────────────────────────────── */}
      <div className="relative mx-auto flex min-h-[100dvh] max-w-[1400px] flex-col md:grid md:grid-cols-[1fr_45%]">

        {/* ── LEFT: text stack ─────────────────────────────────────────── */}
        <div className="relative z-10 flex flex-col justify-end pb-16 pl-6 pr-6 pt-0 md:pb-20 md:pl-14 md:pr-10">
          <div className="max-w-[640px]">

            {/* Eyebrow */}
            <motion.p
              {...r(0)}
              className="mb-6 font-mono text-[0.6875rem] font-normal tracking-[0.2em] uppercase text-ink-soft"
            >
              {t("eyebrow")}
            </motion.p>

            {/* Headline */}
            <motion.h1
              {...r(0.12)}
              className="m-0 font-display text-[clamp(3.5rem,6vw,6rem)] font-light leading-[1.02] tracking-[-0.02em] text-balance text-ink"
            >
              {t.rich("headline", {
                em: (chunks) => (
                  <em className="font-display italic font-normal">{chunks}</em>
                ),
              })}
            </motion.h1>

            {/* Subhead */}
            <motion.p
              {...r(0.24)}
              className="mt-6 text-[1.125rem] font-normal leading-[1.5] text-ink md:text-[1.25rem]"
            >
              {t("subhead")}
            </motion.p>

            {/* Paragraph */}
            <motion.p
              {...r(0.36)}
              className="mt-5 max-w-[58ch] text-[1rem] leading-[1.65] text-ink-soft md:text-[1.0625rem]"
            >
              {t("paragraph")}
            </motion.p>

            {/* CTAs */}
            <motion.div
              {...r(0.48)}
              className="mt-9 flex flex-col gap-4 sm:flex-row sm:items-center"
            >
              {/* Primary — amber pill */}
              <a
                href="#"
                className="inline-flex min-h-[48px] items-center justify-center rounded-full bg-amber px-7 py-3 text-[0.9375rem] font-medium text-ink transition-colors duration-200 hover:bg-amber-hi focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-amber"
              >
                {t("ctaPrimary")}
              </a>

              {/* Secondary — text + arrow */}
              <a
                href="#nuricell"
                className="inline-flex min-h-[48px] items-center gap-1 text-[0.9375rem] font-medium text-ink underline-offset-4 hover:underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ink"
              >
                {t("ctaSecondary")}
              </a>
            </motion.div>

          </div>
        </div>

        {/* ── RIGHT: portrait image block ──────────────────────────────── */}
        {/* On mobile this renders below the text at a fixed height.        */}
        {/* On desktop it fills the right column and bleeds to the edge.    */}
        <div className="relative h-[55vw] shrink-0 sm:h-[45vw] md:h-auto md:self-stretch">
          <motion.div
            className="h-full w-full"
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
            <Placeholder
              label={t("imageAlt")}
              className="h-full w-full rounded-none md:rounded-l-3xl"
            />
          </motion.div>
        </div>

      </div>
    </section>
  );
}

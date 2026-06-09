"use client";

import { useRef } from "react";
import Image from "next/image";
import { motion, useInView } from "motion/react";
import { useReducedMotionSafe } from "@/components/site/use-reduced-motion-safe";
import { useTranslations } from "next-intl";
import { Reveal } from "@/components/site/reveal";

/* ─────────────────────────────────────────────────────────────────────────
   Shared ease curve — premium slow feel
───────────────────────────────────────────────────────────────────────── */
const EASE = [0.2, 0.7, 0.2, 1] as const;

/* ─────────────────────────────────────────────────────────────────────────
   Beat 3 Synergy diagram — the two nutrients as labeled circles that
   overlap; the union holds the glow. Drift together when in view.
   The `animate` target is always present so the diagram can never be
   left stuck invisible (reduced-motion lands it instantly).
───────────────────────────────────────────────────────────────────────── */
function NutrientSynergy({
  reduced,
  labelA,
  labelB,
}: {
  reduced: boolean;
  labelA: string;
  labelB: string;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: "-10% 0px" });
  const settle = (x: number) => ({
    initial: reduced ? (false as const) : { x, opacity: 0 },
    animate: inView || reduced ? { x: 0, opacity: 1 } : { x, opacity: 0 },
    transition: { duration: reduced ? 0 : 1.4, ease: EASE, delay: 0.1 },
  });

  const circle =
    "flex size-48 md:size-64 shrink-0 items-center justify-center rounded-full " +
    "border border-ink/25 bg-amber/[0.05]";
  const label =
    "max-w-[12ch] text-center font-mono text-[0.6875rem] md:text-[0.8125rem] " +
    "uppercase tracking-[0.16em] leading-[1.6] text-ink";

  return (
    <div ref={ref} className="my-12 md:my-16 flex items-center justify-center">
      {/* Circle A — drifts in from the left */}
      <motion.div className={`${circle} z-10`} {...settle(-40)}>
        <span className={label}>{labelA}</span>
      </motion.div>

      {/* Union glow — confined to the lens where the circles overlap */}
      <motion.div
        aria-hidden="true"
        className="pointer-events-none -mx-[3.25rem] md:-mx-[4rem] z-0 h-32 w-20 md:h-44 md:w-26 rounded-full blur-lg bg-amber-hi"
        initial={reduced ? false : { opacity: 0, scale: 0.6 }}
        animate={
          inView || reduced
            ? { opacity: 0.5, scale: 1 }
            : { opacity: 0, scale: 0.6 }
        }
        transition={{ duration: reduced ? 0 : 1.2, ease: EASE, delay: 0.7 }}
      />

      {/* Circle B — drifts in from the right */}
      <motion.div className={`${circle} z-10`} {...settle(40)}>
        <span className={label}>{labelB}</span>
      </motion.div>
    </div>
  );
}

/* ─────────────────────────────────────────────────────────────────────────
   NuricellFlagship — 6-beat cinematic chapter
   Beat 1 = DARK (bg-forest), Beats 2–6 = LIGHT (bg-paper / bg-paper-2)
───────────────────────────────────────────────────────────────────────── */
export function NuricellFlagship() {
  const t = useTranslations("Flagship");
  const reduced = useReducedMotionSafe();

  return (
    <>
      {/* ──────────────────────────────────────────────────────────────────
          BEAT 1 — DARK unveiling, full-bleed cinema. id="nuricell" here.
      ────────────────────────────────────────────────────────────────────── */}
      <section
        id="nuricell"
        className="relative overflow-hidden bg-forest"
      >
        {/* Full-bleed product photography owns the band */}
        <div className="absolute inset-0">
          <Image
            src="/images/nuricell-bottle.jpg"
            alt=""
            aria-hidden="true"
            fill
            sizes="100vw"
            className="object-cover object-[70%_center] md:object-[72%_center]"
          />
          {/* Dark wash from the left so the words own their half */}
          <div
            aria-hidden="true"
            className="absolute inset-0 bg-gradient-to-r from-forest via-forest/85 to-forest/10"
          />
        </div>

        {/* Subtle top-edge separator to close previous section */}
        <div
          aria-hidden="true"
          className="pointer-events-none absolute inset-x-0 top-0 h-px bg-amber-hi/10"
        />

        <div className="relative mx-auto max-w-[1200px] px-6 py-28 md:px-14 md:py-40 flex flex-col justify-center min-h-[70vh]">

          {/* Eyebrow */}
          <Reveal>
            <p className="font-mono uppercase tracking-[0.2em] text-amber-hi text-[0.6875rem]">
              {t("eyebrow")}
            </p>
          </Reveal>

          {/* Headline — the flagship's name owns the frame */}
          <Reveal delay={0.1}>
            <h2 className="mt-6 font-display font-light text-paper text-[clamp(3.5rem,7vw,6rem)] leading-[1.0] tracking-[-0.02em]">
              {t("beat1.headline")}
            </h2>
          </Reveal>

          {/* Subhead */}
          <Reveal delay={0.2}>
            <p className="mt-6 text-paper/85 text-[1.1875rem] md:text-[1.3125rem] leading-[1.6] max-w-[40ch]">
              {t("beat1.subhead")}
            </p>
          </Reveal>

          {/* Provenance — a true sentence, not a sticker */}
          <Reveal delay={0.3}>
            <p className="mt-8 font-display italic font-light text-amber-hi text-[1.25rem] md:text-[1.5rem]">
              {t("badge")}
            </p>
          </Reveal>
        </div>
      </section>

      {/* ──────────────────────────────────────────────────────────────────
          BEAT 2 — bg-paper. His formula, not ours.
      ────────────────────────────────────────────────────────────────────── */}
      <section className="bg-paper">
        <div className="mx-auto max-w-[800px] px-6 py-20 md:px-14 md:py-28">

          <Reveal delay={0.1}>
            <h2 className="font-display font-light text-ink text-[clamp(2.25rem,3.5vw,3.5rem)] leading-[1.08] tracking-[-0.02em] text-balance">
              {t("beat2.headline")}
            </h2>
          </Reveal>

          <Reveal delay={0.2}>
            <p className="mt-7 text-ink text-[1.125rem] md:text-[1.1875rem] leading-[1.6] max-w-[52ch]">
              {t("beat2.body")}
            </p>
          </Reveal>

          {/* A door for the reader convinced by the proof */}
          <Reveal delay={0.3}>
            <a
              href="#quiz"
              className="mt-7 inline-block text-[1.0625rem] font-medium text-ink underline-offset-4 hover:underline"
            >
              {t("beat2.cta")}
            </a>
          </Reveal>

        </div>
      </section>

      {/* ──────────────────────────────────────────────────────────────────
          BEAT 3 — bg-paper-2. Two nutrients. Greater together.
          Spec §2.1 glow echo permitted here on the merging orbs only.
      ────────────────────────────────────────────────────────────────────── */}
      <section className="bg-paper-2">
        <div className="mx-auto max-w-[800px] px-6 py-20 md:px-14 md:py-28">

          <Reveal delay={0.1}>
            <h2 className="font-display font-light text-ink text-[clamp(2.25rem,3.5vw,3.5rem)] leading-[1.08] tracking-[-0.02em] text-balance">
              {t("beat3.headline")}
            </h2>
          </Reveal>

          {/* Nutrient synergy diagram — glow only here, as permitted */}
          <NutrientSynergy
            reduced={reduced}
            labelA={t("beat3.nutrientA")}
            labelB={t("beat3.nutrientB")}
          />

          {/* What the union actually did — the diagram's caption does work */}
          <Reveal delay={0.1}>
            <p className="text-center font-mono text-[0.75rem] uppercase tracking-[0.14em] leading-[1.7] text-ink-soft -mt-4 mb-10">
              {t("beat3.unionNote")}
            </p>
          </Reveal>

          <Reveal delay={0.15}>
            <p className="mt-7 text-ink text-[1.125rem] md:text-[1.1875rem] leading-[1.6] max-w-[52ch]">
              {t("beat3.body")}
            </p>
          </Reveal>

        </div>
      </section>

      {/* ──────────────────────────────────────────────────────────────────
          BEAT 4 — bg-paper. More isn't better. Right is better.
          Same alignment spine as the other beats — one grid, held.
      ────────────────────────────────────────────────────────────────────── */}
      <section className="bg-paper">
        <div className="mx-auto max-w-[800px] px-6 py-20 md:px-14 md:py-28">

          <Reveal delay={0.1}>
            <h2 className="font-display font-light text-ink text-[clamp(2.25rem,3.5vw,3.5rem)] leading-[1.08] tracking-[-0.02em] text-balance">
              {t("beat4.headline")}
            </h2>
          </Reveal>

          <Reveal delay={0.2}>
            <p className="mt-7 text-ink text-[1.125rem] md:text-[1.1875rem] leading-[1.6] max-w-[52ch]">
              {t("beat4.body")}
            </p>
          </Reveal>

        </div>
      </section>

      {/* ──────────────────────────────────────────────────────────────────
          BEAT 5 — bg-paper-2. Built complete.
      ────────────────────────────────────────────────────────────────────── */}
      <section className="bg-paper-2">
        <div className="mx-auto max-w-[1200px] px-6 py-20 md:px-14 md:py-28">

          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 md:gap-20 items-center">

            <div>
              <Reveal delay={0.1}>
                <h2 className="font-display font-light text-ink text-[clamp(2.25rem,3.5vw,3.5rem)] leading-[1.08] tracking-[-0.02em] text-balance">
                  {t("beat5.headline")}
                </h2>
              </Reveal>

              <Reveal delay={0.2}>
                <p className="mt-7 text-ink text-[1.125rem] md:text-[1.1875rem] leading-[1.6] max-w-[48ch]">
                  {t("beat5.body")}
                </p>
              </Reveal>
            </div>

            {/* Capsule visual */}
            <Reveal delay={0.1} className="w-full">
              <div className="relative aspect-[4/3] w-full overflow-hidden rounded-2xl">
                <Image
                  src="/images/capsule-trio-v2.jpg"
                  alt={t("capsuleLabel")}
                  fill
                  sizes="(min-width: 768px) 50vw, 100vw"
                  className="object-cover"
                />
              </div>
            </Reveal>

          </div>
        </div>
      </section>

      {/* ──────────────────────────────────────────────────────────────────
          BEAT 6 — bg-paper. Three capsules. Every morning. Chapter close.
      ────────────────────────────────────────────────────────────────────── */}
      <section className="bg-paper">
        <div className="mx-auto max-w-[800px] px-6 py-20 md:px-14 md:py-28">

          <Reveal delay={0.1}>
            <h2 className="font-display font-light text-ink text-[clamp(2.25rem,3.5vw,3.5rem)] leading-[1.08] tracking-[-0.02em] text-balance">
              {t("beat6.headline")}
            </h2>
          </Reveal>

          <Reveal delay={0.2}>
            <p className="mt-7 text-ink text-[1.125rem] md:text-[1.1875rem] leading-[1.6] max-w-[52ch]">
              {t("beat6.body")}
            </p>
          </Reveal>

          {/* The section's one decision — deep, large, inevitable */}
          <Reveal delay={0.3}>
            <div className="mt-10">
              <a
                href="#quiz"
                className="inline-flex min-h-[56px] items-center justify-center rounded-full bg-forest px-10 py-4 text-[1.125rem] font-medium text-paper transition-colors duration-200 hover:bg-ink focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-forest"
              >
                {t("beat6.cta")}
              </a>
            </div>
          </Reveal>

          {/* Pivot — quieter closing line */}
          <Reveal delay={0.4}>
            <p className="mt-10 text-ink text-[1.125rem] md:text-[1.1875rem] leading-[1.6] max-w-[52ch]">
              {t("beat6.pivot")}
            </p>
          </Reveal>

        </div>
      </section>
    </>
  );
}

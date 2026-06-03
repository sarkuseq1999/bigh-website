"use client";

import { useRef } from "react";
import { motion, useInView, useReducedMotion } from "motion/react";
import { useTranslations } from "next-intl";
import { Reveal } from "@/components/site/reveal";
import { Placeholder } from "@/components/site/placeholder";

/* ─────────────────────────────────────────────────────────────────────────
   Shared ease curve — premium slow feel
───────────────────────────────────────────────────────────────────────── */
const EASE = [0.2, 0.7, 0.2, 1] as const;

/* ─────────────────────────────────────────────────────────────────────────
   Beat 1 Bottle — slow cinematic reveal (scale + fade)
   Reduced motion: renders statically at final state.
───────────────────────────────────────────────────────────────────────── */
function BottleReveal({
  label,
  reduced,
}: {
  label: string;
  reduced: boolean;
}) {
  return (
    <motion.div
      className="w-full"
      {...(reduced
        ? {}
        : {
            initial: { opacity: 0, scale: 0.94 },
            whileInView: { opacity: 1, scale: 1 },
            viewport: { once: true, margin: "-10% 0px" },
            transition: { duration: 1.6, ease: EASE },
          })}
    >
      {/* Soft ambient glow behind the bottle — pure CSS, no raw hex */}
      <div className="relative mx-auto max-w-[280px] md:max-w-[340px]">
        <div
          aria-hidden="true"
          className="pointer-events-none absolute inset-[-20%] rounded-full opacity-20 blur-3xl bg-amber-hi"
        />
        <Placeholder
          label={label}
          className="relative aspect-[2/3] w-full border-amber-hi/20 bg-forest/60 text-paper/40 rounded-2xl"
        />
      </div>
    </motion.div>
  );
}

/* ─────────────────────────────────────────────────────────────────────────
   Beat 3 Orbs — drift together when in view.
   Reduced motion: render statically already merged.
───────────────────────────────────────────────────────────────────────── */
function MergingOrbs({ reduced }: { reduced: boolean }) {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: "-10% 0px" });

  /* Settled (merged) positions */
  const settled = { x: 0, opacity: 1 };

  return (
    <div
      ref={ref}
      aria-hidden="true"
      className="flex items-center justify-center gap-0 my-12 md:my-16"
    >
      {/* Orb A — drifts in from the left */}
      <motion.div
        className="size-20 md:size-28 rounded-full"
        style={{
          background:
            "radial-gradient(circle at 40% 40%, var(--glow), transparent 70%)",
          boxShadow: "0 0 40px 6px color-mix(in srgb, var(--glow) 18%, transparent)",
        }}
        {...(reduced
          ? {}
          : {
              initial: { x: -48, opacity: 0 },
              animate: inView ? settled : { x: -48, opacity: 0 },
              transition: { duration: 1.4, ease: EASE, delay: 0.1 },
            })}
      />

      {/* Overlap bridge — only visible when merged */}
      <motion.div
        className="-mx-6 size-10 md:size-14 rounded-full"
        style={{
          background:
            "radial-gradient(circle at 50% 50%, var(--glow), transparent 70%)",
          opacity: 0.45,
        }}
        {...(reduced
          ? {}
          : {
              initial: { opacity: 0, scale: 0.6 },
              animate: inView ? { opacity: 0.45, scale: 1 } : { opacity: 0, scale: 0.6 },
              transition: { duration: 1.0, ease: EASE, delay: 0.7 },
            })}
      />

      {/* Orb B — drifts in from the right */}
      <motion.div
        className="size-20 md:size-28 rounded-full"
        style={{
          background:
            "radial-gradient(circle at 60% 40%, var(--glow), transparent 70%)",
          boxShadow: "0 0 40px 6px color-mix(in srgb, var(--glow) 18%, transparent)",
        }}
        {...(reduced
          ? {}
          : {
              initial: { x: 48, opacity: 0 },
              animate: inView ? settled : { x: 48, opacity: 0 },
              transition: { duration: 1.4, ease: EASE, delay: 0.1 },
            })}
      />
    </div>
  );
}

/* ─────────────────────────────────────────────────────────────────────────
   NuricellFlagship — 6-beat cinematic chapter
   Beat 1 = DARK (bg-forest), Beats 2–6 = LIGHT (bg-paper / bg-paper-2)
───────────────────────────────────────────────────────────────────────── */
export function NuricellFlagship() {
  const t = useTranslations("Flagship");
  const reduced = useReducedMotion() ?? false;

  return (
    <>
      {/* ──────────────────────────────────────────────────────────────────
          BEAT 1 — DARK unveiling. id="nuricell" lives here (link target).
      ────────────────────────────────────────────────────────────────────── */}
      <section
        id="nuricell"
        className="relative overflow-hidden bg-forest"
      >
        {/* Subtle top-edge separator to close previous section */}
        <div
          aria-hidden="true"
          className="pointer-events-none absolute inset-x-0 top-0 h-px bg-amber-hi/10"
        />

        <div className="mx-auto max-w-[1200px] px-6 py-28 md:px-14 md:py-40 min-h-[90dvh] flex flex-col justify-center">

          {/* Eyebrow */}
          <Reveal>
            <p className="font-mono uppercase tracking-[0.2em] text-amber-hi text-[0.6875rem]">
              {t("eyebrow")}
            </p>
          </Reveal>

          <div className="mt-8 md:mt-12 grid grid-cols-1 md:grid-cols-[1fr_auto] gap-12 md:gap-20 items-center">

            {/* Left — text stack */}
            <div className="flex flex-col">
              {/* Headline */}
              <Reveal delay={0.1}>
                <h2 className="font-display font-light text-paper text-[clamp(2.5rem,4.5vw,4.25rem)] leading-[1.05] tracking-[-0.02em] text-balance">
                  {t("beat1.headline")}
                </h2>
              </Reveal>

              {/* Subhead */}
              <Reveal delay={0.2}>
                <p className="mt-5 text-paper/75 text-[1.125rem] md:text-[1.1875rem] leading-[1.6] max-w-[44ch]">
                  {t("beat1.subhead")}
                </p>
              </Reveal>

              {/* Badge pill */}
              <Reveal delay={0.3}>
                <div className="mt-8">
                  <span className="inline-flex items-center rounded-full bg-amber text-ink px-5 py-2 font-mono text-[0.6875rem] uppercase tracking-[0.2em]">
                    {t("badge")}
                  </span>
                </div>
              </Reveal>
            </div>

            {/* Right — bottle */}
            <div className="w-full md:w-auto flex justify-center md:justify-end">
              <BottleReveal label={t("bottleLabel")} reduced={reduced} />
            </div>

          </div>
        </div>
      </section>

      {/* ──────────────────────────────────────────────────────────────────
          BEAT 2 — bg-paper. His formula, not ours.
      ────────────────────────────────────────────────────────────────────── */}
      <section className="bg-paper">
        <div className="mx-auto max-w-[800px] px-6 py-28 md:px-14 md:py-40">

          <Reveal>
            <p className="font-mono uppercase tracking-[0.2em] text-ink-soft text-[0.6875rem]">
              {t("eyebrow")}
            </p>
          </Reveal>

          <Reveal delay={0.1}>
            <h2 className="mt-6 font-display font-light text-ink text-[clamp(2.25rem,3.5vw,3.5rem)] leading-[1.08] tracking-[-0.02em] text-balance">
              {t("beat2.headline")}
            </h2>
          </Reveal>

          <Reveal delay={0.2}>
            <p className="mt-7 text-ink-soft text-[1.125rem] md:text-[1.1875rem] leading-[1.6] max-w-[52ch]">
              {t("beat2.body")}
            </p>
          </Reveal>

        </div>
      </section>

      {/* ──────────────────────────────────────────────────────────────────
          BEAT 3 — bg-paper-2. Two nutrients. Greater together.
          Spec §2.1 glow echo permitted here on the merging orbs only.
      ────────────────────────────────────────────────────────────────────── */}
      <section className="bg-paper-2">
        <div className="mx-auto max-w-[800px] px-6 py-28 md:px-14 md:py-40">

          <Reveal>
            <p className="font-mono uppercase tracking-[0.2em] text-ink-soft text-[0.6875rem]">
              {t("eyebrow")}
            </p>
          </Reveal>

          <Reveal delay={0.1}>
            <h2 className="mt-6 font-display font-light text-ink text-[clamp(2.25rem,3.5vw,3.5rem)] leading-[1.08] tracking-[-0.02em] text-balance">
              {t("beat3.headline")}
            </h2>
          </Reveal>

          {/* Merging orbs — glow only here, as permitted */}
          <MergingOrbs reduced={reduced} />

          <Reveal delay={0.15}>
            <p className="text-ink-soft text-[1.125rem] md:text-[1.1875rem] leading-[1.6] max-w-[52ch]">
              {t("beat3.body")}
            </p>
          </Reveal>

        </div>
      </section>

      {/* ──────────────────────────────────────────────────────────────────
          BEAT 4 — bg-paper. More isn't better. Right is better.
      ────────────────────────────────────────────────────────────────────── */}
      <section className="bg-paper">
        <div className="mx-auto max-w-[800px] px-6 py-28 md:px-14 md:py-40">

          <Reveal>
            <p className="font-mono uppercase tracking-[0.2em] text-ink-soft text-[0.6875rem]">
              {t("eyebrow")}
            </p>
          </Reveal>

          <Reveal delay={0.1}>
            <h2 className="mt-6 font-display font-light text-ink text-[clamp(2.25rem,3.5vw,3.5rem)] leading-[1.08] tracking-[-0.02em] text-balance">
              {t("beat4.headline")}
            </h2>
          </Reveal>

          <Reveal delay={0.2}>
            <p className="mt-7 text-ink-soft text-[1.125rem] md:text-[1.1875rem] leading-[1.6] max-w-[52ch]">
              {t("beat4.body")}
            </p>
          </Reveal>

        </div>
      </section>

      {/* ──────────────────────────────────────────────────────────────────
          BEAT 5 — bg-paper-2. Built complete.
      ────────────────────────────────────────────────────────────────────── */}
      <section className="bg-paper-2">
        <div className="mx-auto max-w-[1200px] px-6 py-28 md:px-14 md:py-40">

          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 md:gap-20 items-center">

            <div>
              <Reveal>
                <p className="font-mono uppercase tracking-[0.2em] text-ink-soft text-[0.6875rem]">
                  {t("eyebrow")}
                </p>
              </Reveal>

              <Reveal delay={0.1}>
                <h2 className="mt-6 font-display font-light text-ink text-[clamp(2.25rem,3.5vw,3.5rem)] leading-[1.08] tracking-[-0.02em] text-balance">
                  {t("beat5.headline")}
                </h2>
              </Reveal>

              <Reveal delay={0.2}>
                <p className="mt-7 text-ink-soft text-[1.125rem] md:text-[1.1875rem] leading-[1.6] max-w-[48ch]">
                  {t("beat5.body")}
                </p>
              </Reveal>
            </div>

            {/* Capsule visual */}
            <Reveal delay={0.1} className="w-full">
              <Placeholder
                label={t("capsuleLabel")}
                className="aspect-[4/3] w-full border-line bg-paper text-ink-soft rounded-2xl"
              />
            </Reveal>

          </div>
        </div>
      </section>

      {/* ──────────────────────────────────────────────────────────────────
          BEAT 6 — bg-paper. Three capsules. Every morning. Chapter close.
      ────────────────────────────────────────────────────────────────────── */}
      <section className="bg-paper">
        <div className="mx-auto max-w-[800px] px-6 py-28 md:px-14 md:py-40">

          <Reveal>
            <p className="font-mono uppercase tracking-[0.2em] text-ink-soft text-[0.6875rem]">
              {t("eyebrow")}
            </p>
          </Reveal>

          <Reveal delay={0.1}>
            <h2 className="mt-6 font-display font-light text-ink text-[clamp(2.25rem,3.5vw,3.5rem)] leading-[1.08] tracking-[-0.02em] text-balance">
              {t("beat6.headline")}
            </h2>
          </Reveal>

          <Reveal delay={0.2}>
            <p className="mt-7 text-ink-soft text-[1.125rem] md:text-[1.1875rem] leading-[1.6] max-w-[52ch]">
              {t("beat6.body")}
            </p>
          </Reveal>

          {/* Amber CTA pill */}
          <Reveal delay={0.3}>
            <div className="mt-10">
              <a
                href="#"
                className="inline-flex min-h-[48px] items-center justify-center rounded-full bg-amber px-8 py-3 text-[0.9375rem] font-medium text-ink transition-colors duration-200 hover:bg-amber-hi focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-amber"
              >
                {t("beat6.cta")}
              </a>
            </div>
          </Reveal>

          {/* Pivot — quieter closing line */}
          <Reveal delay={0.4}>
            <p className="mt-10 text-ink-soft text-[1.125rem] md:text-[1.1875rem] leading-[1.6] max-w-[52ch]">
              {t("beat6.pivot")}
            </p>
          </Reveal>

        </div>
      </section>
    </>
  );
}

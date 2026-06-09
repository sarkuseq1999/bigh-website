"use client";

import { useRef } from "react";
import type { ReactNode } from "react";
import {
  motion,
  useInView,
  useMotionValue,
  useTransform,
  animate,
} from "motion/react";
import Image from "next/image";
import { useReducedMotionSafe } from "@/components/site/use-reduced-motion-safe";
import { useEffect } from "react";
import { useTranslations } from "next-intl";
import { Reveal } from "@/components/site/reveal";

const EASE = [0.2, 0.7, 0.2, 1] as const;

/* ─────────────────────────────────────────────────────────────────────── */
/* Count-up hook                                                           */
/* ─────────────────────────────────────────────────────────────────────── */

function useCountUp(
  target: number,
  duration: number,
  triggered: boolean,
  reduced: boolean,
) {
  const value = useMotionValue(reduced ? target : 0);
  const rounded = useTransform(value, (v) => Math.round(v));

  useEffect(() => {
    if (!triggered) return;
    if (reduced) {
      value.set(target);
      return;
    }
    const controls = animate(value, target, {
      duration,
      ease: "easeOut",
    });
    return () => controls.stop();
  }, [triggered, target, duration, reduced, value]);

  return rounded;
}

/* ─────────────────────────────────────────────────────────────────────── */
/* Anchor stat — one designed lockup: serif numerals, aligned baselines,   */
/* identical spacing row to row.                                           */
/* ─────────────────────────────────────────────────────────────────────── */

function AnchorStat({ reduced }: { reduced: boolean }) {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: "-10% 0px" });

  const count3 = useCountUp(3, 1.4, inView, reduced);
  const count1 = useCountUp(1, 1.1, inView, reduced);
  const count22k = useCountUp(22000, 2.6, inView, reduced);

  const count22kFormatted = useTransform(count22k, (v) => {
    if (v < 1000) return String(Math.round(v));
    const thousands = Math.floor(v / 1000);
    const remainder = String(Math.round(v % 1000)).padStart(3, "0");
    return `${thousands},${remainder}`;
  });

  const show = inView || reduced;

  const rows: { value: ReactNode; label: string; delay: number }[] = [
    { value: <motion.span>{count3}</motion.span>, label: "papers", delay: 0 },
    { value: <motion.span>{count1}</motion.span>, label: "issue of PNAS", delay: 0.2 },
    {
      value: (
        <>
          <motion.span>{count22kFormatted}</motion.span>
          <span>+</span>
        </>
      ),
      label: "citations",
      delay: 0.4,
    },
  ];

  return (
    <div
      ref={ref}
      aria-label="3 papers. 1 issue of PNAS. 22,000+ citations."
      className="flex flex-col gap-2"
    >
      {rows.map(({ value, label, delay }) => (
        <motion.div
          key={label}
          className="flex items-baseline gap-x-4"
          initial={reduced ? false : { opacity: 0, y: 10 }}
          animate={show ? { opacity: 1, y: 0 } : { opacity: 0, y: 10 }}
          transition={{ duration: reduced ? 0 : 0.7, delay: reduced ? 0 : delay, ease: EASE }}
        >
          <span className="font-display text-amber-hi text-[clamp(2.25rem,3.6vw,3.25rem)] font-light leading-none tracking-[-0.01em] tabular-nums">
            {value}
          </span>
          <span className="font-mono text-paper/75 text-[0.8125rem] uppercase tracking-[0.18em]">
            {label}
          </span>
        </motion.div>
      ))}
    </div>
  );
}

/* ─────────────────────────────────────────────────────────────────────── */
/* Main export                                                             */
/* ─────────────────────────────────────────────────────────────────────── */

export function Credibility() {
  const t = useTranslations("Scientist");
  const reduced = useReducedMotionSafe();

  return (
    <section
      id="scientist"
      className="bg-forest relative overflow-hidden"
    >
      {/* Subtle top edge separator */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-x-0 top-0 h-px bg-amber-hi/10"
      />

      <div className="mx-auto max-w-[1200px] px-6 py-28 md:px-14 md:py-40">

        {/* ─── EYEBROW ─── */}
        <Reveal>
          <p className="font-mono uppercase tracking-[0.2em] text-amber-hi text-[0.6875rem]">
            {t("eyebrow")}
          </p>
        </Reveal>

        {/* ─── HEADLINE + SUBHEAD ─── */}
        <Reveal delay={0.1}>
          <h2 className="font-display font-light text-paper mt-6 text-[clamp(2.5rem,4vw,4rem)] leading-[1.08] tracking-[-0.022em] max-w-[18ch]">
            {t("headline")}
          </h2>
        </Reveal>

        <Reveal delay={0.18}>
          <p className="text-paper/85 mt-5 max-w-[52ch] text-[1.125rem] md:text-[1.1875rem] leading-[1.6]">
            {t("subhead")}
          </p>
        </Reveal>

        {/* ─── MAIN TWO-COLUMN ZONE ─── */}
        <div className="mt-16 md:mt-20 grid grid-cols-1 md:grid-cols-[1fr_1.25fr] gap-12 md:gap-20 items-stretch">

          {/* LEFT — the research, in print (stands in until a real portrait
              of Dr. Liu is supplied; never a generated likeness) */}
          <Reveal delay={0.05} className="flex w-full">
            <figure className="m-0 flex w-full flex-col">
              <div className="relative w-full flex-1 border border-amber-hi/30 rounded-xl overflow-hidden min-h-[420px]">
                <Image
                  src="/images/research-journals-v2.jpg"
                  alt={t("photoAlt")}
                  fill
                  sizes="(min-width: 768px) 40vw, 100vw"
                  className="object-cover"
                />
              </div>
              <figcaption className="mt-4 font-mono text-[0.6875rem] uppercase tracking-[0.2em] text-paper/60">
                {t("photoCaption")}
              </figcaption>
            </figure>
          </Reveal>

          {/* RIGHT — stat + body */}
          <div className="flex flex-col gap-0">

            {/* Giant anchor stat — reveals first */}
            <AnchorStat reduced={reduced} />

            {/* Body paragraphs */}
            <Reveal delay={0.1} className="mt-10">
              <p className="text-paper/90 text-[1.125rem] md:text-[1.1875rem] leading-[1.6]">
                {t("bodyP1")}
              </p>
            </Reveal>

            <Reveal delay={0.15} className="mt-5">
              <p className="text-paper/90 text-[1.125rem] md:text-[1.1875rem] leading-[1.6]">
                {t("bodyP2")}
              </p>
            </Reveal>

            <Reveal delay={0.2} className="mt-5">
              <p className="text-paper/85 text-[1.125rem] md:text-[1.1875rem] leading-[1.6]">
                {t("bodyP3")}
              </p>
            </Reveal>

          </div>
        </div>

        {/* Pivot — full-width closing beat shared by both columns */}
        <Reveal delay={0.1}>
          <p className="mt-16 md:mt-20 font-display font-light italic text-paper text-[clamp(1.5rem,2.6vw,2.25rem)] leading-[1.3] tracking-[-0.01em] max-w-[30ch]">
            {t("pivot")}
          </p>
        </Reveal>

      </div>
    </section>
  );
}

"use client";

import { useRef } from "react";
import {
  motion,
  useInView,
  useMotionValue,
  useTransform,
  animate,
  useReducedMotion,
} from "motion/react";
import { useEffect } from "react";
import { useTranslations } from "next-intl";
import { Reveal } from "@/components/site/reveal";
import { Placeholder } from "@/components/site/placeholder";

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
/* Animated anchor stat                                                    */
/* ─────────────────────────────────────────────────────────────────────── */

function AnchorStat({ reduced }: { reduced: boolean }) {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: "-10% 0px" });

  const count3   = useCountUp(3,     1.4, inView, reduced);
  const count1   = useCountUp(1,     1.1, inView, reduced);
  const count22k = useCountUp(22000, 2.6, inView, reduced);

  // Format count22k as "22,000" while animating (hoisted — no hook-in-render)
  const count22kFormatted = useTransform(count22k, (v) => {
    if (v < 1000) return String(Math.round(v));
    const thousands = Math.floor(v / 1000);
    const remainder = String(Math.round(v % 1000)).padStart(3, "0");
    return `${thousands},${remainder}`;
  });

  return (
    <div
      ref={ref}
      className="font-mono text-paper leading-tight"
      aria-label="3 papers. 1 issue. 22,000+ citations."
    >
      {/* Row 1 */}
      <div className="flex items-baseline gap-[0.3em] text-[clamp(1.75rem,3.2vw,2.75rem)]">
        <motion.span
          className="text-amber-hi font-bold"
          initial={reduced ? false : { opacity: 0, y: 10 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.7, delay: 0.0, ease: EASE }}
        >
          <motion.span>{count3}</motion.span>
        </motion.span>
        <motion.span
          className="text-paper/80 text-[0.62em] tracking-[0.12em] uppercase"
          initial={reduced ? false : { opacity: 0 }}
          animate={inView ? { opacity: 1 } : {}}
          transition={{ duration: 0.7, delay: 0.2, ease: EASE }}
        >
          papers.
        </motion.span>
      </div>

      {/* Row 2 */}
      <div className="mt-2 flex items-baseline gap-[0.3em] text-[clamp(1.75rem,3.2vw,2.75rem)]">
        <motion.span
          className="text-amber-hi font-bold"
          initial={reduced ? false : { opacity: 0, y: 10 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.7, delay: 0.3, ease: EASE }}
        >
          <motion.span>{count1}</motion.span>
        </motion.span>
        <motion.span
          className="text-paper/80 text-[0.62em] tracking-[0.12em] uppercase"
          initial={reduced ? false : { opacity: 0 }}
          animate={inView ? { opacity: 1 } : {}}
          transition={{ duration: 0.7, delay: 0.5, ease: EASE }}
        >
          issue.
        </motion.span>
      </div>

      {/* Row 3 */}
      <div className="mt-2 flex items-baseline gap-[0.15em] text-[clamp(1.75rem,3.2vw,2.75rem)]">
        <motion.span
          className="text-amber-hi font-bold"
          initial={reduced ? false : { opacity: 0, y: 10 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.7, delay: 0.6, ease: EASE }}
        >
          <motion.span>{count22kFormatted}</motion.span>
          <span className="text-amber-hi">+</span>
        </motion.span>
        <motion.span
          className="text-paper/80 text-[0.62em] tracking-[0.12em] uppercase"
          initial={reduced ? false : { opacity: 0 }}
          animate={inView ? { opacity: 1 } : {}}
          transition={{ duration: 0.7, delay: 0.85, ease: EASE }}
        >
          citations.
        </motion.span>
      </div>
    </div>
  );
}

/* ─────────────────────────────────────────────────────────────────────── */
/* Main export                                                             */
/* ─────────────────────────────────────────────────────────────────────── */

export function Credibility() {
  const t = useTranslations("Scientist");
  const reduced = useReducedMotion() ?? false;

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

      <div className="mx-auto max-w-[1200px] px-6 py-28 md:px-14 md:py-44">

        {/* ─── EYEBROW ─── */}
        <Reveal>
          <p className="font-mono uppercase tracking-[0.2em] text-amber-hi text-[0.6875rem]">
            {t("eyebrow")}
          </p>
        </Reveal>

        {/* ─── HEADLINE + SUBHEAD ─── */}
        <Reveal delay={0.1}>
          <h2
            className="font-display font-light text-paper mt-6 text-[clamp(2.5rem,4vw,4rem)] leading-[1.08] tracking-[-0.022em] max-w-[18ch]"
          >
            {t.rich("headline", {
              em: (c) => (
                <em className="font-display italic font-normal">{c}</em>
              ),
            })}
          </h2>
        </Reveal>

        <Reveal delay={0.18}>
          <p className="text-paper/70 mt-5 max-w-[52ch] text-[1.125rem] md:text-[1.1875rem] leading-[1.6]">
            {t("subhead")}
          </p>
        </Reveal>

        {/* ─── MAIN TWO-COLUMN ZONE ─── */}
        <div className="mt-16 md:mt-24 grid grid-cols-1 md:grid-cols-[1fr_1.25fr] gap-12 md:gap-20 items-start">

          {/* LEFT — portrait placeholder */}
          <Reveal delay={0.05} className="w-full">
            <div className="border border-amber-hi/30 rounded-xl overflow-hidden">
              <Placeholder
                label={t("photoLabel")}
                className="aspect-3/4 w-full bg-forest/60 border-0 rounded-none text-paper/50"
              />
            </div>
          </Reveal>

          {/* RIGHT — stat + body */}
          <div className="flex flex-col gap-0">

            {/* Giant anchor stat — reveals first */}
            <AnchorStat reduced={reduced} />

            {/* Body paragraphs */}
            <Reveal delay={0.1} className="mt-10">
              <p className="text-paper text-[1.125rem] md:text-[1.1875rem] leading-[1.6]">
                {t("bodyP1")}
              </p>
            </Reveal>

            <Reveal delay={0.15} className="mt-5">
              <p className="text-paper/75 text-[1.125rem] md:text-[1.1875rem] leading-[1.6]">
                {t("bodyP2")}
              </p>
            </Reveal>

            <Reveal delay={0.2} className="mt-5">
              <p className="text-paper/75 text-[1.125rem] md:text-[1.1875rem] leading-[1.6]">
                {t("bodyP3")}
              </p>
            </Reveal>

            <Reveal delay={0.25} className="mt-5">
              <p className="text-paper/75 text-[1.125rem] md:text-[1.1875rem] leading-[1.6]">
                {t("bodyP4")}
              </p>
            </Reveal>

            {/* Pivot line — closing beat */}
            <Reveal delay={0.32} className="mt-14 md:mt-16">
              <p className="font-display font-light italic text-paper text-[clamp(1.375rem,2.2vw,1.875rem)] leading-[1.3] tracking-[-0.01em]">
                {t("pivot")}
              </p>
            </Reveal>

          </div>
        </div>

      </div>
    </section>
  );
}

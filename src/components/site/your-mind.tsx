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
    <section id="yourmind" ref={ref} className="relative overflow-hidden bg-white">
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

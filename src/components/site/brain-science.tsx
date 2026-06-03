"use client";

import { useRef } from "react";
import { motion, useInView } from "motion/react";
import { useReducedMotionSafe } from "@/components/site/use-reduced-motion-safe";
import { useTranslations } from "next-intl";
import { Reveal } from "@/components/site/reveal";

// Number of cell segments inside the battery visual
const CELL_COUNT = 5;

/* ─────────────────────────────────────────────────────────────────────────
   BrainScience — Section 3 "The Reason"
   Two-column on desktop: copy left, animated battery visual right.
   The battery charges up with a teal glow on scroll-in, then breathes.
   Reduced-motion: fully-charged static state, no animation.
───────────────────────────────────────────────────────────────────────── */

export function BrainScience() {
  const t = useTranslations("Reason");

  return (
    <section id="science" className="bg-paper scroll-mt-24">
      <div className="mx-auto max-w-[1200px] px-6 py-24 md:px-14 md:py-36">

        {/* Eyebrow */}
        <Reveal>
          <p className="font-mono text-[0.6875rem] uppercase tracking-[0.2em] text-ink-soft">
            {t("eyebrow")}
          </p>
        </Reveal>

        {/* Two-column grid: copy + visual */}
        <div className="mt-10 grid grid-cols-1 gap-16 md:mt-14 md:grid-cols-2 md:gap-20 lg:gap-28">

          {/* ── LEFT: Copy column ── */}
          <div className="flex flex-col justify-center">

            {/* Headline */}
            <Reveal delay={0.05}>
              <h2 className="font-display text-[clamp(2.5rem,4vw,4rem)] font-light leading-[1.1] tracking-[-0.02em] text-balance text-ink">
                {t.rich("headline", {
                  em: (c) => (
                    <em className="font-display italic font-normal">{c}</em>
                  ),
                })}
              </h2>
            </Reveal>

            {/* Subhead */}
            <Reveal delay={0.12}>
              <p className="mt-5 text-[1.125rem] leading-[1.6] text-ink-soft md:text-[1.1875rem]">
                {t("subhead")}
              </p>
            </Reveal>

            {/* Body P1 + stat callout inline */}
            <Reveal delay={0.2}>
              <p className="mt-8 text-[1.125rem] leading-[1.6] text-ink md:mt-10 md:text-[1.1875rem]">
                {t("bodyP1")}
              </p>
            </Reveal>

            {/* Mono callout stat */}
            <Reveal delay={0.28}>
              <div className="mt-6 inline-flex flex-col border-l-2 border-ink-soft/25 pl-4">
                <span className="font-mono text-[1.25rem] font-semibold tracking-[-0.01em] text-ink">
                  {t("calloutStat")}
                </span>
                <span className="mt-0.5 font-mono text-[0.6875rem] uppercase tracking-[0.2em] text-ink-soft">
                  {t("calloutLabel")}
                </span>
              </div>
            </Reveal>

            {/* Body P2 */}
            <Reveal delay={0.36}>
              <p className="mt-8 text-[1.125rem] leading-[1.6] text-ink md:text-[1.1875rem]">
                {t("bodyP2")}
              </p>
            </Reveal>

            {/* Body P3 */}
            <Reveal delay={0.44}>
              <p className="mt-5 text-[1.125rem] leading-[1.6] text-ink md:text-[1.1875rem]">
                {t("bodyP3")}
              </p>
            </Reveal>

            {/* Turn — the pivot moment */}
            <Reveal delay={0.52}>
              <p className="mt-8 text-[1.125rem] font-medium leading-[1.6] text-ink md:text-[1.1875rem]">
                {t("turn")}
              </p>
            </Reveal>
          </div>

          {/* ── RIGHT: Animated battery visual ── */}
          <div className="flex items-center justify-center md:justify-end">
            <BatteryVisual />
          </div>
        </div>

        {/* ── Brand-statement moment: "Not at the surface. At the source." ── */}
        <Reveal delay={0.1}>
          <div className="mt-24 border-t border-ink-soft/15 pt-16 md:mt-32 md:pt-20">
            <p className="font-display text-[clamp(2rem,3.5vw,3.25rem)] font-light leading-[1.1] tracking-[-0.02em] text-balance text-ink">
              {t("differentiation")}
            </p>
          </div>
        </Reveal>

        {/* Pivot — quieter, sets up next section */}
        <Reveal delay={0.18}>
          <p className="mt-8 max-w-[58ch] text-[1.125rem] leading-[1.6] text-ink-soft md:text-[1.1875rem]">
            {t("pivot")}
          </p>
        </Reveal>
      </div>
    </section>
  );
}

/* ─────────────────────────────────────────────────────────────────────────
   BatteryVisual
   A custom inline SVG battery that "charges up" with teal glow on scroll-in.
   After charging it breathes gently.
   Reduced-motion: shows fully-charged end state, no animation.

   Safety: cells start at opacity 0.15 (never invisible), animate to full.
   The SVG body always renders regardless of scroll/JS state.
───────────────────────────────────────────────────────────────────────── */

function BatteryVisual() {
  const ref = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotionSafe();
  const inView = useInView(ref, { once: true, margin: "-20%" });

  // When reduced-motion OR in-view has fired, show full charge
  const isCharged = reduce || inView;

  return (
    <div
      ref={ref}
      aria-hidden="true"
      className="relative flex items-center justify-center"
      style={{ width: 220, height: 380 }}
    >
      {/* Outer volumetric glow — behind the battery */}
      <BreatheGlow isCharged={isCharged} reduce={!!reduce} />

      {/* Battery SVG */}
      <svg
        viewBox="0 0 120 220"
        width={180}
        height={330}
        className="relative z-10"
        xmlns="http://www.w3.org/2000/svg"
        style={{ overflow: "visible" }}
      >
        {/* Terminal nub at the top */}
        <rect
          x="42"
          y="2"
          width="36"
          height="12"
          rx="5"
          ry="5"
          fill="none"
          stroke="var(--ink)"
          strokeWidth="2.5"
          strokeOpacity="0.35"
        />

        {/* Battery shell */}
        <rect
          x="6"
          y="14"
          width="108"
          height="200"
          rx="14"
          ry="14"
          fill="var(--paper-2)"
          stroke="var(--ink)"
          strokeWidth="2.5"
          strokeOpacity="0.2"
        />

        {/* Cell segments (5 cells, bottom to top = lowest to highest) */}
        {Array.from({ length: CELL_COUNT }, (_, i) => {
          // i=0 is bottom cell, i=4 is top cell
          // Cells fill from bottom (i=0) first
          const cellIndex = i; // 0 = bottom
          const cellW = 80;
          const cellH = 30;
          const cellX = (120 - cellW) / 2; // 20
          // Position from bottom: i=0 is lowest, i=4 is highest
          const cellY = 14 + 200 - 10 - (cellIndex + 1) * (cellH + 4);

          return (
            <BatteryCell
              key={i}
              x={cellX}
              y={cellY}
              width={cellW}
              height={cellH}
              rx={7}
              // Cells charge in order: bottom (0) first, top (4) last
              chargeDelay={cellIndex * 0.28}
              isCharged={isCharged}
              reduce={!!reduce}
            />
          );
        })}

        {/* Divider lines between cells (decorative) */}
        {Array.from({ length: CELL_COUNT - 1 }, (_, i) => {
          const cellH = 30;
          // Line between cell i and cell i+1 (counting from bottom)
          const lineY = 14 + 200 - 10 - (i + 1) * (cellH + 4) - 2;
          return (
            <line
              key={i}
              x1="20"
              y1={lineY}
              x2="100"
              y2={lineY}
              stroke="var(--ink)"
              strokeWidth="1"
              strokeOpacity="0.08"
            />
          );
        })}

        {/* Lightning bolt icon centered — suggests energy/power */}
        <LightningBolt isCharged={isCharged} reduce={!!reduce} />
      </svg>
    </div>
  );
}

/* Single battery cell that lights up with teal glow */
function BatteryCell({
  x,
  y,
  width,
  height,
  rx,
  chargeDelay,
  isCharged,
  reduce,
}: {
  x: number;
  y: number;
  width: number;
  height: number;
  rx: number;
  chargeDelay: number;
  isCharged: boolean;
  reduce: boolean;
}) {
  // Base fill — always visible at low opacity (never invisible safety)
  const baseOpacity = 0.15;
  const chargedOpacity = 0.88;

  return (
    <motion.rect
      x={x}
      y={y}
      width={width}
      height={height}
      rx={rx}
      ry={rx}
      // Start at low-but-visible state
      initial={reduce ? false : { opacity: baseOpacity, scaleY: 0.88 }}
      animate={
        isCharged
          ? {
              opacity: chargedOpacity,
              scaleY: 1,
            }
          : {
              opacity: baseOpacity,
              scaleY: 0.88,
            }
      }
      transition={
        reduce
          ? { duration: 0 }
          : {
              opacity: { duration: 0.5, delay: chargeDelay, ease: [0.2, 0.7, 0.2, 1] },
              scaleY: { duration: 0.45, delay: chargeDelay, ease: [0.2, 0.8, 0.2, 1] },
            }
      }
      style={{
        fill: "var(--glow)",
        transformBox: "fill-box",
        transformOrigin: "center",
        // Soft inner glow on the cell itself
        filter: isCharged ? "drop-shadow(0 0 6px var(--glow))" : "none",
      }}
    />
  );
}

/* Lightning bolt — glows when charged */
function LightningBolt({
  isCharged,
  reduce,
}: {
  isCharged: boolean;
  reduce: boolean;
}) {
  return (
    <motion.path
      // Simple lightning bolt centered in the battery body
      d="M 66 60 L 52 108 L 62 108 L 54 160 L 80 100 L 68 100 Z"
      initial={reduce ? false : { opacity: 0.2 }}
      animate={isCharged ? { opacity: 0.9 } : { opacity: 0.2 }}
      transition={
        reduce
          ? { duration: 0 }
          : {
              opacity: {
                duration: 0.6,
                delay: CELL_COUNT * 0.28 + 0.1,
                ease: [0.2, 0.7, 0.2, 1],
              },
            }
      }
      style={{
        fill: "var(--glow)",
        filter: isCharged ? "drop-shadow(0 0 8px var(--glow))" : "none",
      }}
    />
  );
}

/* Volumetric glow behind the battery — breathes after charging */
function BreatheGlow({
  isCharged,
  reduce,
}: {
  isCharged: boolean;
  reduce: boolean;
}) {
  if (reduce) {
    // Static full glow
    return (
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 rounded-full"
        style={{
          background:
            "radial-gradient(ellipse 70% 60% at 50% 55%, rgba(68,205,169,0.32) 0%, transparent 75%)",
          filter: "blur(32px)",
          opacity: 0.9,
        }}
      />
    );
  }

  return (
    <motion.div
      aria-hidden="true"
      className="pointer-events-none absolute inset-0 rounded-full"
      // Start barely visible (not 0 — never-invisible safety)
      initial={{ opacity: 0.08, scale: 0.85 }}
      animate={
        isCharged
          ? {
              // Breathe loop — gentle, slow, living
              opacity: [0.7, 0.9, 0.7],
              scale: [0.97, 1.04, 0.97],
            }
          : { opacity: 0.08, scale: 0.85 }
      }
      transition={
        isCharged
          ? {
              duration: 3.5,
              repeat: Infinity,
              ease: "easeInOut",
              // Charge-in delay: let the cells finish charging first
              delay: CELL_COUNT * 0.28 + 0.4,
            }
          : { duration: 0.8, ease: "easeOut" }
      }
      style={{
        background:
          "radial-gradient(ellipse 70% 60% at 50% 55%, rgba(68,205,169,0.32) 0%, transparent 75%)",
        filter: "blur(32px)",
      }}
    />
  );
}

"use client";

import { motion } from "motion/react";
import { useReducedMotionSafe } from "@/components/site/use-reduced-motion-safe";
import { useTranslations } from "next-intl";
import { Reveal } from "@/components/site/reveal";

// Subtle attention pulse for the Quiz CTA button
function QuizCta({ label }: { label: string }) {
  const reduce = useReducedMotionSafe();

  if (reduce) {
    return (
      <a
        href="#"
        className="inline-flex min-h-[52px] items-center justify-center rounded-full bg-amber px-10 py-4 font-display text-[1.125rem] font-medium tracking-[-0.01em] text-ink transition-colors duration-200 hover:bg-amber-hi focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-amber"
      >
        {label}
      </a>
    );
  }

  return (
    <motion.a
      href="#"
      animate={{
        scale: [1, 1.02, 1],
        boxShadow: [
          "0 4px 24px 0 rgba(194,138,58,0.18)",
          "0 6px 36px 4px rgba(194,138,58,0.32)",
          "0 4px 24px 0 rgba(194,138,58,0.18)",
        ],
      }}
      transition={{
        duration: 2.8,
        repeat: Infinity,
        ease: "easeInOut",
        repeatType: "loop",
      }}
      className="inline-flex min-h-[52px] items-center justify-center rounded-full bg-amber px-10 py-4 font-display text-[1.125rem] font-medium tracking-[-0.01em] text-ink transition-colors duration-200 hover:bg-amber-hi focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-amber"
    >
      {label}
    </motion.a>
  );
}

/* ─────────────────────────────────────────────────────────────────────────
   Sample Brain Age report — an instrument, not a decoration.
   270° gauge with tick marks, the score needle position, and a marker at
   the sample's actual age so the seven-year gap is legible at a glance.
───────────────────────────────────────────────────────────────────────── */
function BrainAgeSample({
  label,
  value,
  actual,
  note,
  rows,
}: {
  label: string;
  value: string;
  actual: string;
  note: string;
  rows: { label: string; level: number }[];
}) {
  const r = 84;
  const c = 2 * Math.PI * r;
  const arcFrac = 0.75; // 270° track
  const progress = 0.62; // Brain Age 47 on the sample scale
  const actualFrac = 0.78; // marker for actual age 54

  // Tick marks along the 270° track
  const ticks = Array.from({ length: 13 }, (_, i) => {
    const angle = (-225 + i * (270 / 12)) * (Math.PI / 180);
    const x1 = 100 + Math.cos(angle) * (r - 9);
    const y1 = 100 + Math.sin(angle) * (r - 9);
    const x2 = 100 + Math.cos(angle) * (r - 3);
    const y2 = 100 + Math.sin(angle) * (r - 3);
    return { x1, y1, x2, y2 };
  });

  // Marker dot at the sample's actual age
  const mAngle = (-225 + actualFrac * 270) * (Math.PI / 180);
  const mx = 100 + Math.cos(mAngle) * r;
  const my = 100 + Math.sin(mAngle) * r;

  return (
    <div className="relative">
      {/* Deliberate signal ripple — present, quiet, crisply drawn */}
      <svg
        aria-hidden="true"
        viewBox="0 0 480 480"
        className="pointer-events-none absolute left-1/2 top-1/2 -z-10 size-[150%] -translate-x-1/2 -translate-y-1/2"
      >
        {[130, 175, 220].map((rr, i) => (
          <circle
            key={rr}
            cx="240"
            cy="240"
            r={rr}
            fill="none"
            stroke="var(--amber)"
            strokeOpacity={0.4 - i * 0.11}
            strokeWidth="1"
          />
        ))}
      </svg>

      <div className="rounded-2xl border border-line bg-paper px-9 py-8 shadow-[0_8px_40px_rgba(27,26,23,0.07)]">
        <p className="font-mono text-[0.6875rem] uppercase tracking-[0.2em] text-ink-soft text-center">
          {label}
        </p>

        <div className="relative mx-auto mt-3 size-[190px]">
          <svg viewBox="0 0 200 200" className="size-full">
            {/* tick marks */}
            {ticks.map((tk, i) => (
              <line
                key={i}
                x1={tk.x1}
                y1={tk.y1}
                x2={tk.x2}
                y2={tk.y2}
                stroke="var(--line)"
                strokeWidth="1.5"
              />
            ))}
            <g className="-rotate-[225deg] origin-center">
              {/* track */}
              <circle
                cx="100"
                cy="100"
                r={r}
                fill="none"
                stroke="var(--line)"
                strokeWidth="6"
                strokeLinecap="round"
                strokeDasharray={`${c * arcFrac} ${c}`}
              />
              {/* progress — the sample's Brain Age */}
              <circle
                cx="100"
                cy="100"
                r={r}
                fill="none"
                stroke="var(--amber)"
                strokeWidth="6"
                strokeLinecap="round"
                strokeDasharray={`${c * arcFrac * progress} ${c}`}
              />
            </g>
            {/* marker at the sample's actual age — the 7-year gap, visible */}
            <circle cx={mx} cy={my} r="5" fill="var(--paper)" stroke="var(--ink)" strokeWidth="2" />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="font-display text-[3.75rem] font-light leading-none tracking-[-0.02em] text-ink">
              {value}
            </span>
            <span className="mt-2 font-mono text-[0.6875rem] uppercase tracking-[0.16em] text-ink-soft">
              {actual}
            </span>
          </div>
        </div>

        {/* sub-scores — the report has substance */}
        <div className="mt-4 flex flex-col gap-2.5">
          {rows.map(({ label: rowLabel, level }) => (
            <div key={rowLabel} className="grid grid-cols-[7ch_1fr] items-center gap-3">
              <span className="font-mono text-[0.625rem] uppercase tracking-[0.16em] text-ink-soft">
                {rowLabel}
              </span>
              <span className="relative block h-px bg-line">
                <span
                  className="absolute inset-y-[-1px] left-0 bg-amber"
                  style={{ width: `${level}%` }}
                />
              </span>
            </div>
          ))}
        </div>

        <p className="mt-5 text-center font-mono text-[0.625rem] uppercase tracking-[0.2em] text-ink-soft/80">
          {note}
        </p>
      </div>
    </div>
  );
}

export function EmailSignup() {
  const t = useTranslations("SoftEntry");

  const rows = [
    { label: t("sample.rowMemory"), level: 58 },
    { label: t("sample.rowFocus"), level: 72 },
    { label: t("sample.rowRecall"), level: 64 },
  ];

  return (
    <section id="quiz" className="relative overflow-hidden bg-paper-2 py-24 md:py-32">
      <div className="relative mx-auto max-w-[1100px] px-6 md:px-14">

        {/* ── Two-zone: the ask, and the artifact it buys ── */}
        <div className="grid grid-cols-1 items-center gap-14 md:grid-cols-[1.2fr_1fr] md:gap-20">

          {/* LEFT — question + CTA */}
          <div>
            <Reveal>
              <p className="font-mono text-[0.7rem] uppercase tracking-[0.2em] text-ink-soft">
                {t("eyebrow")}
              </p>
            </Reveal>

            <Reveal delay={0.1}>
              <h2 className="mt-6 font-display text-[clamp(2.25rem,4vw,3.75rem)] font-light leading-[1.08] tracking-[-0.02em] text-ink">
                {t("headlineA")}
                <br />
                {t("headlineB")}
              </h2>
            </Reveal>

            <Reveal delay={0.2}>
              <p className="mt-6 max-w-[44ch] text-[1.125rem] leading-[1.7] text-ink-soft">
                {t("subhead")}
              </p>
            </Reveal>

            <Reveal delay={0.3} className="mt-10">
              <div className="flex flex-col items-start gap-3">
                <QuizCta label={t("quizCta")} />
                <p className="font-mono text-[0.8125rem] uppercase tracking-[0.12em] text-ink">
                  {t("trust")}
                </p>
              </div>
            </Reveal>

            {/* Not ready? One quiet line — the footer holds the form. */}
            <Reveal delay={0.4}>
              <p className="mt-10 text-[1.0625rem] leading-[1.6] text-ink-soft">
                {t("newsletter.notReady")}{" "}
                <a
                  href="#newsletter"
                  className="text-ink underline-offset-4 hover:underline"
                >
                  {t("newsletter.notReadyCta")}
                </a>
              </p>
            </Reveal>
          </div>

          {/* RIGHT — the sample report */}
          <Reveal delay={0.25} className="justify-self-center md:justify-self-end">
            <BrainAgeSample
              label={t("sample.label")}
              value={t("sample.value")}
              actual={t("sample.actual")}
              note={t("sample.note")}
              rows={rows}
            />
          </Reveal>
        </div>
      </div>
    </section>
  );
}

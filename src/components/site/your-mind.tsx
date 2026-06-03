"use client";

import { useTranslations } from "next-intl";
import { Reveal } from "@/components/site/reveal";

/* ─────────────────────────────────────────────────────────────────────────
   YourMind — Section 2 "The New Reality"
   Editorial, text-forward. bg-paper-2. No imagery required.
   Stacked layout: eyebrow → headline → subhead → body → capabilities
   (three-row centerpiece) → closing → pivot.
───────────────────────────────────────────────────────────────────────── */

export function YourMind() {
  const t = useTranslations("NewReality");

  return (
    <section id="yourmind" className="bg-paper-2">
      <div className="mx-auto max-w-[1100px] px-6 py-24 md:px-14 md:py-36">

        {/* Eyebrow */}
        <Reveal>
          <p className="font-mono text-[0.6875rem] uppercase tracking-[0.2em] text-ink-soft">
            {t("eyebrow")}
          </p>
        </Reveal>

        {/* Headline */}
        <Reveal delay={0.1}>
          <h2 className="mt-6 font-display text-[clamp(2.5rem,4vw,4rem)] font-light leading-[1.1] tracking-[-0.02em] text-balance text-ink md:mt-8">
            {t("headline")}
          </h2>
        </Reveal>

        {/* Subhead */}
        <Reveal delay={0.2}>
          <p className="mt-5 max-w-[52ch] text-[1.125rem] leading-[1.6] text-ink-soft md:text-[1.1875rem]">
            {t("subhead")}
          </p>
        </Reveal>

        {/* Body P1 */}
        <Reveal delay={0.3}>
          <p className="mt-8 max-w-[62ch] text-[1.125rem] leading-[1.6] text-ink md:mt-10 md:text-[1.1875rem]">
            {t("bodyP1")}
          </p>
        </Reveal>

        {/* Body P2 */}
        <Reveal delay={0.4}>
          <p className="mt-5 max-w-[62ch] text-[1.125rem] font-medium leading-[1.6] text-ink md:text-[1.1875rem]">
            {t("bodyP2")}
          </p>
        </Reveal>

        {/* ── Capabilities centerpiece ──────────────────────────────────── */}
        <div
          className="mt-16 md:mt-20"
          aria-label="Human capabilities"
          role="list"
        >
          {/* Judgment */}
          <Reveal delay={0.1}>
            <div
              role="listitem"
              className="border-t border-line py-8 md:py-10"
            >
              <span className="font-mono text-[0.6875rem] uppercase tracking-[0.2em] text-ink-soft">
                {t("capabilities.judgment.term")}
              </span>
              <p className="mt-3 font-display text-[clamp(1.75rem,3vw,2.75rem)] font-light leading-[1.15] tracking-[-0.015em] text-ink">
                {t("capabilities.judgment.definition")}
              </p>
            </div>
          </Reveal>

          {/* Wisdom */}
          <Reveal delay={0.22}>
            <div
              role="listitem"
              className="border-t border-line py-8 md:py-10"
            >
              <span className="font-mono text-[0.6875rem] uppercase tracking-[0.2em] text-ink-soft">
                {t("capabilities.wisdom.term")}
              </span>
              <p className="mt-3 font-display text-[clamp(1.75rem,3vw,2.75rem)] font-light leading-[1.15] tracking-[-0.015em] text-ink">
                {t("capabilities.wisdom.definition")}
              </p>
            </div>
          </Reveal>

          {/* Taste — lands last, slightly heavier weight for emphasis */}
          <Reveal delay={0.34}>
            <div
              role="listitem"
              className="border-t border-b border-line py-8 md:py-10"
            >
              <span className="font-mono text-[0.6875rem] uppercase tracking-[0.2em] text-ink-soft">
                {t("capabilities.taste.term")}
              </span>
              <p className="mt-3 font-display text-[clamp(1.75rem,3vw,2.75rem)] font-normal leading-[1.15] tracking-[-0.015em] text-ink">
                {t("capabilities.taste.definition")}
              </p>
            </div>
          </Reveal>
        </div>

        {/* Closing */}
        <Reveal delay={0.1}>
          <p className="mt-14 max-w-[58ch] text-[1.125rem] leading-[1.6] text-ink md:mt-16 md:text-[1.1875rem]">
            {t("closing")}
          </p>
        </Reveal>

        {/* Pivot */}
        <Reveal delay={0.2}>
          <p className="mt-5 max-w-[58ch] text-[1.125rem] leading-[1.6] text-ink-soft text-pretty">
            {t("pivot")}
          </p>
        </Reveal>

      </div>
    </section>
  );
}

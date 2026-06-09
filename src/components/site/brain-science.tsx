"use client";

import Image from "next/image";
import { useTranslations } from "next-intl";
import { Reveal } from "@/components/site/reveal";

/* ─────────────────────────────────────────────────────────────────────────
   BrainScience — Section 3 "The Reason"
   Two-column on desktop: copy left, crafted mitochondria render right.
   The image carries the battery metaphor (a glowing cell among dimming
   ones); the 2%/20% stat gets display scale as the section's anchor fact.
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
        <div className="mt-10 grid grid-cols-1 gap-16 md:mt-14 md:grid-cols-[1.1fr_1fr] md:gap-16 lg:gap-24">

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

            {/* Body P1 */}
            <Reveal delay={0.2}>
              <p className="mt-8 text-[1.125rem] leading-[1.6] text-ink md:mt-10 md:text-[1.1875rem]">
                {t("bodyP1")}
              </p>
            </Reveal>

            {/* Anchor stat — each number paired with its own words */}
            <Reveal delay={0.28}>
              <div className="mt-8 flex gap-12">
                <div>
                  <span className="font-display text-[clamp(3rem,5vw,4.5rem)] font-light leading-none tracking-[-0.02em] text-ink">
                    {t("calloutStatA")}
                  </span>
                  <p className="mt-2 font-mono text-[0.75rem] uppercase tracking-[0.16em] text-ink-soft">
                    {t("calloutLabelA")}
                  </p>
                </div>
                <div>
                  <span className="font-display text-[clamp(3rem,5vw,4.5rem)] font-light leading-none tracking-[-0.02em] text-amber">
                    {t("calloutStatB")}
                  </span>
                  <p className="mt-2 font-mono text-[0.75rem] uppercase tracking-[0.16em] text-ink-soft">
                    {t("calloutLabelB")}
                  </p>
                </div>
              </div>
            </Reveal>

            {/* Body P2 + P3 */}
            <Reveal delay={0.36}>
              <p className="mt-8 text-[1.125rem] leading-[1.6] text-ink md:text-[1.1875rem]">
                {t("bodyP2")}
              </p>
            </Reveal>

            <Reveal delay={0.44}>
              <p className="mt-5 text-[1.125rem] leading-[1.6] text-ink md:text-[1.1875rem]">
                {t("bodyP3")}
              </p>
            </Reveal>

            {/* Turn — the revelation gets the display treatment */}
            <Reveal delay={0.52}>
              <p className="mt-10 font-display text-[clamp(1.5rem,2.4vw,2rem)] font-light italic leading-[1.3] text-ink">
                {t("turn")}
              </p>
            </Reveal>
          </div>

          {/* ── RIGHT: mitochondria render — biology and battery in one image ── */}
          <Reveal delay={0.15} className="flex">
            <figure className="m-0 flex w-full flex-col md:self-stretch">
              <div className="relative w-full flex-1 overflow-hidden rounded-md min-h-[420px] md:min-h-0">
                <Image
                  src="/images/mitochondria-v2.jpg"
                  alt={t("visualAlt")}
                  fill
                  sizes="(min-width: 768px) 45vw, 100vw"
                  className="object-cover"
                />
              </div>
              <figcaption className="mt-4 font-mono text-[0.75rem] uppercase tracking-[0.18em] text-ink-soft">
                {t("visualCaption")}
              </figcaption>
            </figure>
          </Reveal>
        </div>

        {/* ── Brand-statement moment — earned by a named contrast, set as
               its own centered event distinct from the headline ── */}
        <Reveal delay={0.1}>
          <div className="mt-16 border-t border-ink-soft/15 pt-12 md:mt-20 md:pt-14 text-center">
            <p className="mx-auto max-w-[56ch] text-[1.125rem] leading-[1.6] text-ink-soft md:text-[1.1875rem]">
              {t("surface")}
            </p>
            <p className="mt-6 font-display italic text-[clamp(1.75rem,3vw,2.75rem)] font-light leading-[1.15] tracking-[-0.015em] text-ink">
              {t("differentiation")}
            </p>
            <p className="mx-auto mt-6 max-w-[58ch] text-[1.125rem] leading-[1.6] text-ink-soft md:text-[1.1875rem]">
              {t("pivot")}
            </p>
          </div>
        </Reveal>
      </div>
    </section>
  );
}

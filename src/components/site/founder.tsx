"use client";

import { useTranslations } from "next-intl";
import { Reveal } from "@/components/site/reveal";
import { Placeholder } from "@/components/site/placeholder";

/* ─────────────────────────────────────────────────────────────────────────
   Founder — Section 9 "The Founder"
   Intimate two-column layout: portrait placeholder beside a personal note.
   Quieter in scale than the Scientist section — a sincere human close.
───────────────────────────────────────────────────────────────────────── */

export function Founder() {
  const t = useTranslations("Founder");

  return (
    <section id="founder" className="bg-paper scroll-mt-24">
      <div className="mx-auto max-w-[1000px] px-6 py-24 md:px-14 md:py-36">

        {/* Eyebrow */}
        <Reveal>
          <p className="font-mono text-[0.6875rem] uppercase tracking-[0.2em] text-ink-soft">
            {t("eyebrow")}
          </p>
        </Reveal>

        {/* Two-column: portrait + note */}
        <div className="mt-10 flex flex-col gap-12 md:mt-14 md:flex-row md:items-start md:gap-16">

          {/* Portrait placeholder — portrait ratio, smaller & warmer */}
          <Reveal delay={0.05} className="w-full md:w-auto md:flex-shrink-0">
            <Placeholder
              label={t("photoLabel")}
              className="aspect-[3/4] w-full border-line md:w-[220px]"
            />
          </Reveal>

          {/* Note column */}
          <div className="flex flex-col">

            {/* Headline */}
            <Reveal delay={0.1}>
              <h2 className="font-display font-light text-[clamp(2.25rem,3.5vw,3.25rem)] leading-[1.15] tracking-[-0.02em] text-ink">
                {t("headline")}
              </h2>
            </Reveal>

            {/* Body P1 */}
            <Reveal delay={0.18}>
              <p className="mt-6 text-[1.125rem] leading-[1.6] text-ink-soft md:text-[1.1875rem]">
                {t("bodyP1")}
              </p>
            </Reveal>

            {/* Body P2 */}
            <Reveal delay={0.26}>
              <p className="mt-5 text-[1.125rem] leading-[1.6] text-ink-soft md:text-[1.1875rem]">
                {t("bodyP2")}
              </p>
            </Reveal>

            {/* Signoff — font-display italic for letter warmth */}
            <Reveal delay={0.34}>
              <p className="mt-8 font-display italic text-[1.125rem] leading-[1.6] text-ink md:text-[1.1875rem]">
                {t("signoff")}
              </p>
            </Reveal>

            {/* CTA — text link only, no amber text */}
            <Reveal delay={0.42}>
              <a
                href="#nuricell"
                className="mt-6 inline-block text-[1.125rem] leading-[1.6] text-ink underline decoration-line decoration-1 underline-offset-4 transition-colors duration-200 hover:decoration-amber-hi md:text-[1.1875rem]"
              >
                {t("cta")}
              </a>
            </Reveal>

          </div>
        </div>
      </div>
    </section>
  );
}

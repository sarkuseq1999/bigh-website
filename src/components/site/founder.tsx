"use client";

import Image from "next/image";
import { useTranslations } from "next-intl";
import { Reveal } from "@/components/site/reveal";

/* ─────────────────────────────────────────────────────────────────────────
   Founder — Section 9 "The Founder"
   Intimate two-column close: the letter-in-progress beside a personal note
   set like correspondence (serif body, generous leading).
───────────────────────────────────────────────────────────────────────── */

export function Founder() {
  const t = useTranslations("Founder");

  return (
    <section id="founder" className="bg-paper scroll-mt-24">
      <div className="mx-auto max-w-[1000px] px-6 py-24 md:px-14 md:py-36">

        {/* Two-column: letter photo + note */}
        <div className="flex flex-col gap-12 md:flex-row md:items-stretch md:gap-16">

          {/* The letter, mid-thought — stands in until a real portrait of
              Mo Chen is supplied; never a generated likeness */}
          <Reveal delay={0.05} className="flex w-full md:w-[300px] md:flex-shrink-0">
            <div className="relative w-full overflow-hidden rounded-xl border border-line aspect-[3/4] md:aspect-auto md:min-h-full">
              <Image
                src="/images/founder-letter.jpg"
                alt={t("photoAlt")}
                fill
                sizes="(min-width: 768px) 300px, 100vw"
                className="object-cover"
              />
            </div>
          </Reveal>

          {/* Note column */}
          <div className="flex flex-col">

            {/* Eyebrow — anchored to the note it introduces */}
            <Reveal>
              <p className="font-mono text-[0.6875rem] uppercase tracking-[0.2em] text-ink-soft">
                {t("eyebrow")}
              </p>
            </Reveal>

            {/* Headline */}
            <Reveal delay={0.1}>
              <h2 className="mt-5 font-display font-light text-[clamp(2.25rem,3.5vw,3.25rem)] leading-[1.15] tracking-[-0.02em] text-ink">
                {t("headline")}
              </h2>
            </Reveal>

            {/* Body — set like correspondence, not interface text */}
            <Reveal delay={0.18}>
              <p className="mt-7 font-display text-[1.25rem] font-light leading-[1.65] text-ink md:text-[1.3125rem]">
                {t("bodyP1")}
              </p>
            </Reveal>

            <Reveal delay={0.26}>
              <p className="mt-5 font-display text-[1.25rem] font-light leading-[1.65] text-ink md:text-[1.3125rem]">
                {t("bodyP2")}
              </p>
            </Reveal>

            {/* Signoff */}
            <Reveal delay={0.34}>
              <p className="mt-8 font-display italic text-[1.375rem] leading-[1.5] text-ink">
                {t("signoff")}
              </p>
            </Reveal>

            {/* CTA — the last ask of the page deserves a real button */}
            <Reveal delay={0.42}>
              <div className="mt-8">
                <a
                  href="#nuricell"
                  className="inline-flex min-h-[52px] items-center justify-center rounded-full bg-amber px-8 py-3 text-[1.0625rem] font-medium text-ink transition-colors duration-200 hover:bg-amber-hi focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-amber"
                >
                  {t("cta")}
                </a>
              </div>
            </Reveal>

          </div>
        </div>
      </div>
    </section>
  );
}

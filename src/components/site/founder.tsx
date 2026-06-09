"use client";

import Image from "next/image";
import { useTranslations } from "next-intl";
import { Reveal } from "@/components/site/reveal";

/* ─────────────────────────────────────────────────────────────────────────
   Founder — Section 9 "The Founder"
   A letter, honored as a letter: salutation, serif correspondence body,
   signature mark, quiet close, and a P.S. for the almost-ready reader.
───────────────────────────────────────────────────────────────────────── */

export function Founder() {
  const t = useTranslations("Founder");

  return (
    <section id="founder" className="bg-paper scroll-mt-24">
      <div className="mx-auto max-w-[1060px] px-6 py-24 md:px-14 md:py-36">

        {/* Two-column: letter photo + note */}
        <div className="flex flex-col gap-12 md:flex-row md:items-stretch md:gap-16">

          {/* The letter, mid-thought — stands in until a real portrait of
              Mo Chen is supplied; never a generated likeness */}
          <Reveal delay={0.05} className="flex w-full md:w-[360px] md:flex-shrink-0">
            <div className="relative w-full overflow-hidden aspect-[3/4] md:aspect-auto md:min-h-full">
              <Image
                src="/images/founder-letter-v2.jpg"
                alt={t("photoAlt")}
                fill
                sizes="(min-width: 768px) 360px, 100vw"
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

            {/* Salutation — the form and the words agree */}
            <Reveal delay={0.16}>
              <p className="mt-8 font-display italic text-[1.25rem] font-light leading-[1.65] text-ink md:text-[1.3125rem]">
                {t("salutation")}
              </p>
            </Reveal>

            {/* Body — set like correspondence, not interface text */}
            <Reveal delay={0.22}>
              <p className="mt-5 font-display text-[1.25rem] font-light leading-[1.65] text-ink md:text-[1.3125rem]">
                {t("bodyP1")}
              </p>
            </Reveal>

            <Reveal delay={0.3}>
              <p className="mt-5 font-display text-[1.25rem] font-light leading-[1.65] text-ink md:text-[1.3125rem]">
                {t("bodyP2")}
              </p>
            </Reveal>

            {/* Signature — restrained typeset name until a real scan exists */}
            <Reveal delay={0.38}>
              <div className="mt-6">
                <p className="font-display italic text-[1.75rem] font-light leading-none text-ink">
                  Mo Chen
                </p>
                <p className="mt-2 font-mono text-[0.6875rem] uppercase tracking-[0.2em] text-ink-soft">
                  {t("signatureTitle")}
                </p>
              </div>
            </Reveal>

            {/* Quiet close — the intimacy is the sell */}
            <Reveal delay={0.46}>
              <a
                href="#nuricell"
                className="mt-9 inline-block border-b border-line pb-0.5 font-display text-[1.25rem] font-light text-ink transition-colors duration-200 hover:border-amber-hi"
              >
                {t("cta")}
              </a>
            </Reveal>

            {/* P.S. — same hand as the letter */}
            <Reveal delay={0.54}>
              <p className="mt-7 font-display text-[1.1875rem] font-light italic leading-[1.6] text-ink">
                {t("ps")}{" "}
                <a href="#quiz" className="border-b border-line pb-0.5 not-italic transition-colors duration-200 hover:border-amber-hi">
                  {t("psCta")}
                </a>
              </p>
            </Reveal>

          </div>
        </div>
      </div>
    </section>
  );
}

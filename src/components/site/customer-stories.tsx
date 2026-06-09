"use client";

import Image from "next/image";
import { useTranslations } from "next-intl";
import { Reveal } from "@/components/site/reveal";

const VIGNETTE_KEYS = ["one", "two", "three"] as const;

const VIGNETTE_IMAGES: Record<(typeof VIGNETTE_KEYS)[number], string> = {
  one: "/images/story-seoul.jpg",
  two: "/images/story-california-v2.jpg",
  three: "/images/story-hanoi.jpg",
};

const RECORD_KEYS = ["papers", "citations", "years"] as const;

const PNAS_ISSUE_URL = "https://www.pnas.org/toc/pnas/99/4";

export function CustomerStories() {
  const t = useTranslations("Proof");

  return (
    <section id="proof" className="bg-paper py-24 md:py-36">
      <div className="mx-auto max-w-[1200px] px-6 md:px-14">

        {/* ── EYEBROW ──────────────────────────────────────────────── */}
        <Reveal>
          <p className="font-mono uppercase tracking-[0.2em] text-[0.6875rem] text-ink-soft text-center">
            {t("eyebrow")}
          </p>
        </Reveal>

        {/* ── HEADLINE — leads with the proof the brand actually owns ── */}
        <Reveal delay={0.08}>
          <h2 className="font-display font-light text-ink text-center mt-5
                         text-[clamp(2.25rem,3.5vw,3.5rem)] leading-[1.1] tracking-[-0.02em]
                         max-w-[22ch] mx-auto">
            {t("headline")}
          </h2>
        </Reveal>

        {/* Pre-launch honesty, in plain sight and readable */}
        <Reveal delay={0.14}>
          <p className="text-ink-soft text-center mt-5 text-[1.125rem] leading-[1.7] max-w-[44ch] mx-auto">
            {t("subhead")}
          </p>
        </Reveal>

        {/* ── THE RECORD — dark exhibit band, four equal proofs ── */}
        <Reveal delay={0.2} className="mt-14 md:mt-16">
          <div className="rounded-2xl bg-forest px-8 py-12 md:px-14 md:py-14">
            <div className="grid grid-cols-3 gap-x-6">
              {RECORD_KEYS.map((key) => (
                <div key={key} className="flex flex-col items-center text-center">
                  <span className="font-display font-light text-amber-hi leading-none
                                   text-[clamp(2.5rem,4vw,3.75rem)] tracking-[-0.01em]">
                    {t(`record.${key}.value`)}
                  </span>
                  <span className="mt-3 font-mono uppercase tracking-[0.14em] text-[0.8125rem] leading-[1.6] text-paper/85 max-w-[14ch]">
                    {t(`record.${key}.label`)}
                  </span>
                </div>
              ))}
            </div>

            {/* The issue itself — the one verifiable action, set like one */}
            <div className="mt-10 flex flex-col items-center gap-4">
              <p className="font-mono text-[0.75rem] uppercase tracking-[0.16em] text-paper/70">
                {t("record.issueLine")}
              </p>
              <a
                href={PNAS_ISSUE_URL}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex min-h-[44px] items-center rounded-full border border-paper/40 px-6
                           font-mono text-[0.8125rem] uppercase tracking-[0.15em] text-paper
                           transition-colors duration-200 hover:border-paper hover:bg-paper/10
                           focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-amber-hi"
              >
                {t("record.cta")}
              </a>
            </div>
          </div>
        </Reveal>

        {/* ── THE PEOPLE WE BUILT IT FOR — portraits, not testimony ── */}
        <Reveal delay={0.08} className="mt-16 md:mt-20">
          <h3 className="font-display font-light text-ink text-center
                         text-[clamp(1.75rem,2.6vw,2.5rem)] leading-[1.15] tracking-[-0.015em]">
            {t("vignettesTitle")}
          </h3>
        </Reveal>
        <Reveal delay={0.14}>
          <p className="mt-4 text-center text-[0.9375rem] leading-[1.6] text-ink-soft max-w-[52ch] mx-auto">
            {t("vignettesNote")}
          </p>
        </Reveal>

        <div className="mt-10 md:mt-12 grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8">
          {VIGNETTE_KEYS.map((key, idx) => {
            const line = t(`portraits.${key}.line`);
            const place = t(`portraits.${key}.place`);
            return (
              <Reveal key={key} delay={0.1 + idx * 0.12}>
                <article className="flex flex-col h-full overflow-hidden rounded-2xl bg-paper border border-line">

                  {/* the place these lives happen — honest editorial stand-in */}
                  <div className="relative aspect-[16/10] w-full">
                    <Image
                      src={VIGNETTE_IMAGES[key]}
                      alt={place}
                      fill
                      sizes="(min-width: 768px) 33vw, 100vw"
                      className="object-cover"
                    />
                  </div>

                  <div className="flex flex-col flex-1 p-7">
                    <p className="m-0 font-display font-light text-ink leading-[1.45] text-[1.25rem] flex-1">
                      {line}
                    </p>
                    <p className="mt-5 font-mono text-[0.6875rem] tracking-[0.16em] uppercase text-ink-soft">
                      {place}
                    </p>
                  </div>

                </article>
              </Reveal>
            );
          })}
        </div>

      </div>
    </section>
  );
}

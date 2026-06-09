"use client";

import Image from "next/image";
import { useTranslations } from "next-intl";
import { Reveal } from "@/components/site/reveal";

const VIGNETTE_KEYS = ["one", "two", "three"] as const;

const VIGNETTE_IMAGES: Record<(typeof VIGNETTE_KEYS)[number], string> = {
  one: "/images/story-seoul.jpg",
  two: "/images/story-california.jpg",
  three: "/images/story-hanoi.jpg",
};

const RECORD_KEYS = ["papers", "citations", "years", "berkeley"] as const;

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

        {/* Dignified pre-launch honesty, up where it can be read */}
        <Reveal delay={0.14}>
          <p className="text-ink-soft text-center mt-5 text-[1.125rem] leading-[1.7] max-w-[52ch] mx-auto">
            {t("subhead")}
          </p>
        </Reveal>

        {/* ── THE RECORD — dark exhibit band, set like a spec to be proud of ── */}
        <Reveal delay={0.2} className="mt-14 md:mt-16">
          <div className="rounded-2xl bg-forest px-8 py-12 md:px-14 md:py-14">
            <div className="grid grid-cols-2 gap-x-6 gap-y-10 md:grid-cols-4">
              {RECORD_KEYS.map((key) => (
                <div key={key} className="flex flex-col items-center text-center">
                  <span className="font-display font-light text-amber-hi leading-none
                                   text-[clamp(2.25rem,3.6vw,3.5rem)] tracking-[-0.01em]">
                    {t(`record.${key}.value`)}
                  </span>
                  <span className="mt-3 font-mono uppercase tracking-[0.16em] text-[0.6875rem] text-paper/75 max-w-[18ch]">
                    {t(`record.${key}.label`)}
                  </span>
                </div>
              ))}
            </div>
            <div className="mt-10 flex justify-center">
              <a
                href="#scientist"
                className="font-mono text-[0.8125rem] uppercase tracking-[0.15em] text-paper
                           underline-offset-4 hover:underline focus-visible:outline-2
                           focus-visible:outline-offset-4 focus-visible:outline-amber-hi"
              >
                {t("record.cta")}
              </a>
            </div>
          </div>
        </Reveal>

        {/* ── THE PEOPLE WE BUILT IT FOR — honest vignettes, not testimony ── */}
        <Reveal delay={0.08} className="mt-20 md:mt-24">
          <h3 className="font-display font-light text-ink text-center
                         text-[clamp(1.75rem,2.6vw,2.5rem)] leading-[1.15] tracking-[-0.015em]">
            {t("vignettesTitle")}
          </h3>
        </Reveal>
        <Reveal delay={0.14}>
          <p className="mt-4 text-center font-mono text-[0.75rem] tracking-[0.1em] text-ink-soft max-w-[60ch] mx-auto">
            {t("vignettesNote")}
          </p>
        </Reveal>

        <div className="mt-10 md:mt-12 grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8">
          {VIGNETTE_KEYS.map((key, idx) => {
            const quote = t(`testimonials.${key}.quote`);
            const name = t(`testimonials.${key}.name`);
            const location = t(`testimonials.${key}.location`);
            return (
              <Reveal key={key} delay={0.1 + idx * 0.12}>
                <article className="flex flex-col h-full overflow-hidden rounded-2xl bg-paper border border-line">

                  {/* the place these lives happen — honest editorial stand-in */}
                  <div className="relative aspect-[16/10] w-full">
                    <Image
                      src={VIGNETTE_IMAGES[key]}
                      alt={location}
                      fill
                      sizes="(min-width: 768px) 33vw, 100vw"
                      className="object-cover"
                    />
                  </div>

                  <div className="flex flex-col flex-1 p-7">
                    <blockquote className="m-0 font-display font-light text-ink italic leading-normal text-[1.25rem] flex-1">
                      &ldquo;{quote}&rdquo;
                    </blockquote>
                    <figcaption className="mt-5">
                      <span className="font-mono text-[0.6875rem] tracking-[0.14em] uppercase text-ink">
                        {name}
                        <span className="text-ink-soft"> · {location}</span>
                      </span>
                    </figcaption>
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

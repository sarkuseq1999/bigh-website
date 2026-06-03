"use client";

import { useTranslations } from "next-intl";
import { Reveal } from "@/components/site/reveal";
import { Placeholder } from "@/components/site/placeholder";

const TESTIMONIAL_KEYS = ["one", "two", "three"] as const;
const RECORD_STAT_KEYS = ["pnas", "citations", "years", "berkeley"] as const;

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

        {/* ── HEADLINE ─────────────────────────────────────────────── */}
        <Reveal delay={0.08}>
          <h2 className="font-display font-light text-ink text-center mt-5
                         text-[clamp(2.25rem,3.5vw,3.5rem)] leading-[1.1] tracking-[-0.02em]
                         max-w-[22ch] mx-auto">
            {t("headline")}
          </h2>
        </Reveal>

        {/* ── BAND 1: TESTIMONIALS ─────────────────────────────────── */}
        <div className="mt-16 md:mt-20 grid grid-cols-1 md:grid-cols-3 gap-8 md:gap-10">
          {TESTIMONIAL_KEYS.map((key, idx) => {
            const quote    = t(`testimonials.${key}.quote`);
            const name     = t(`testimonials.${key}.name`);
            const location = t(`testimonials.${key}.location`);
            const note     = t(`testimonials.${key}.note`);
            return (
              <Reveal key={key} delay={0.1 + idx * 0.12}>
                <article className="flex flex-col gap-5 rounded-2xl bg-paper border border-line p-7 md:p-8 h-full">

                  {/* Avatar placeholder */}
                  <Placeholder
                    label={name}
                    className="w-16 h-16 rounded-full shrink-0 border-line"
                  />

                  {/* Quote — the focus */}
                  <blockquote className="font-display font-light text-ink italic leading-normal
                                          text-[1.25rem] md:text-[1.25rem] flex-1">
                    &ldquo;{quote}&rdquo;
                  </blockquote>

                  {/* Attribution */}
                  <figcaption className="flex flex-col gap-1 mt-auto">
                    <span className="font-mono text-[0.6875rem] tracking-[0.14em] uppercase text-ink">
                      {name}
                      <span className="text-ink-soft"> · {location}</span>
                    </span>
                    <span className="font-mono text-[0.6875rem] text-ink-soft">
                      {note}
                    </span>
                  </figcaption>

                </article>
              </Reveal>
            );
          })}
        </div>

        {/* ── BAND 2: THE RECORD — mono stat strip ─────────────────── */}
        <Reveal delay={0.1} className="mt-16 md:mt-20">
          <div className="border border-line rounded-2xl bg-paper px-6 py-8 md:px-10">

            {/* Stat pills row */}
            <div className="flex flex-wrap items-center justify-center gap-0">
              {RECORD_STAT_KEYS.map((key, idx) => (
                <div key={key} className="flex items-center">
                  <span className="font-mono text-[0.8125rem] uppercase tracking-[0.15em] text-ink-soft
                                    px-4 py-1 text-center">
                    {t(`record.${key}`)}
                  </span>
                  {idx < RECORD_STAT_KEYS.length - 1 && (
                    <span
                      aria-hidden="true"
                      className="block w-px h-4 bg-line shrink-0"
                    />
                  )}
                </div>
              ))}
            </div>

            {/* CTA link */}
            <div className="mt-5 flex justify-center">
              <a
                href="#"
                className="font-mono text-[0.8125rem] uppercase tracking-[0.15em] text-ink
                           hover:bg-amber-hi transition-colors duration-200 underline-offset-4
                           hover:underline"
              >
                {t("record.cta")}
              </a>
            </div>

          </div>
        </Reveal>

      </div>
    </section>
  );
}

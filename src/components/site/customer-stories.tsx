"use client";

import { motion } from "motion/react";
import { useTranslations } from "next-intl";

const ease = [0.2, 0.7, 0.2, 1] as const;
const SHORT_KEYS = ["one", "two", "three"] as const;

export function CustomerStories() {
  const t = useTranslations("Stories");

  return (
    <section className="relative overflow-hidden bg-white">
      <div className="mx-auto max-w-[1240px] px-6 pt-28 pb-32 md:px-12 md:pt-40 md:pb-44">
        {/* ─────────── EYEBROW ─────────── */}
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.7, ease }}
          className="flex justify-center"
        >
          <div className="inline-flex items-center gap-3">
            <span className="bg-sienna block size-1 rounded-full" />
            <p className="text-espresso-60 font-display text-[0.7rem] font-medium tracking-[0.32em] uppercase">
              {t("eyebrow")}
            </p>
            <span className="bg-sienna block size-1 rounded-full" />
          </div>
        </motion.div>

        {/* ─────────── HEADLINE ─────────── */}
        <motion.h2
          initial={{ opacity: 0, y: 18 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 1.05, delay: 0.15, ease }}
          className="font-display text-espresso mx-auto mt-10 max-w-[18ch] text-center text-[clamp(2.5rem,6vw,5.5rem)] font-light leading-[1.03] tracking-[-0.022em] md:mt-14"
          style={{ fontVariationSettings: '"opsz" 144, "SOFT" 30' }}
        >
          {t("headlineBefore")}
          <em className="text-sienna font-light italic">
            {t("headlineEmphasis")}
          </em>
        </motion.h2>

        {/* ─────────── INTRO ─────────── */}
        <motion.p
          initial={{ opacity: 0, y: 14 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 1, delay: 0.3, ease }}
          className="text-espresso/70 mx-auto mt-12 max-w-[580px] text-center text-[clamp(1rem,1.2vw,1.1875rem)] leading-[1.7] md:mt-16"
        >
          {t("intro")}
        </motion.p>

        {/* ─────────── FEATURED QUOTE ─────────── */}
        <motion.figure
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 1.1, delay: 0.45, ease }}
          className="relative mx-auto mt-28 max-w-[920px] md:mt-40"
        >
          {/* Massive decorative opening quote in sienna */}
          <motion.span
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 1.2, delay: 0.3, ease }}
            aria-hidden="true"
            className="font-display text-sienna pointer-events-none absolute -top-12 left-0 text-[10rem] leading-none font-light select-none md:-top-20 md:-left-4 md:text-[14rem]"
            style={{ fontVariationSettings: '"opsz" 144, "SOFT" 80' }}
          >
            &ldquo;
          </motion.span>

          <blockquote
            className="font-display text-espresso relative text-[clamp(1.5rem,2.6vw,2.25rem)] leading-[1.4] font-light italic md:pl-16"
            style={{ fontVariationSettings: '"opsz" 96, "SOFT" 50' }}
          >
            {t("featured.quote")}
          </blockquote>

          <figcaption className="text-espresso-60 mt-10 flex items-center gap-3 md:pl-16">
            <span className="bg-sienna block size-1 rounded-full" />
            <span className="font-display text-sm">
              <span className="text-espresso font-medium">
                {t("featured.name")}
              </span>
              {" — "}
              <span className="text-espresso-60">{t("featured.location")}</span>
            </span>
          </figcaption>
        </motion.figure>

        {/* ─────────── THREE SHORTER QUOTES ─────────── */}
        <div className="mx-auto mt-28 grid max-w-[1140px] grid-cols-1 gap-12 md:mt-40 md:grid-cols-3 md:gap-8">
          {SHORT_KEYS.map((key, idx) => (
            <SmallQuote
              key={key}
              quote={t(`shortQuotes.${key}.quote`)}
              name={t(`shortQuotes.${key}.name`)}
              location={t(`shortQuotes.${key}.location`)}
              delay={idx * 0.12}
            />
          ))}
        </div>
      </div>
    </section>
  );
}

/* ─────────────────────────────────────────────────────────────────────── */

function SmallQuote({
  quote,
  name,
  location,
  delay,
}: {
  quote: string;
  name: string;
  location: string;
  delay: number;
}) {
  return (
    <motion.figure
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-60px" }}
      transition={{ duration: 0.95, delay, ease }}
      className="border-espresso/12 group flex flex-col border-t pt-8"
    >
      <blockquote
        className="font-display text-espresso text-[clamp(1.0625rem,1.4vw,1.25rem)] leading-[1.55] font-light italic"
        style={{ fontVariationSettings: '"opsz" 24' }}
      >
        {quote}
      </blockquote>

      <figcaption className="mt-7 flex items-center gap-2.5">
        <span className="bg-sienna block size-1 rounded-full" />
        <span className="font-display text-sm">
          <span className="text-espresso font-medium">{name}</span>
          {" — "}
          <span className="text-espresso/55">{location}</span>
        </span>
      </figcaption>
    </motion.figure>
  );
}

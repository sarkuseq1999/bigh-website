"use client";

import { motion } from "motion/react";
import { useTranslations } from "next-intl";
import { ArrowRight } from "lucide-react";

const ease = [0.2, 0.7, 0.2, 1] as const;
const PAPER_KEYS = ["one", "two", "three"] as const;

export function Credibility() {
  const t = useTranslations("Credibility");

  return (
    <section className="relative overflow-hidden bg-white">
      <div className="mx-auto max-w-[1080px] px-6 pt-28 pb-32 md:px-12 md:pt-40 md:pb-44">
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
          className="font-display text-espresso mx-auto mt-10 max-w-[20ch] text-center text-[clamp(2.5rem,6vw,5.5rem)] font-light leading-[1.03] tracking-[-0.022em] md:mt-14"
          style={{ fontVariationSettings: '"opsz" 144, "SOFT" 30' }}
        >
          {t("headlineBefore")}
          <em className="text-sienna font-light italic">
            {t("headlineEmphasis")}
          </em>
          {t("headlineAfter")}
        </motion.h2>

        {/* ─────────── INTRO ─────────── */}
        <motion.p
          initial={{ opacity: 0, y: 14 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 1, delay: 0.3, ease }}
          className="text-espresso/80 mx-auto mt-14 max-w-[700px] text-center text-[clamp(1.0625rem,1.3vw,1.25rem)] leading-[1.75] md:mt-20"
        >
          {t("intro")}
        </motion.p>

        {/* ─────────── CITATIONS BLOCK ─────────── */}
        <div className="mx-auto mt-24 max-w-[860px] md:mt-32">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.7, ease }}
            className="flex items-center gap-4"
          >
            <span className="border-espresso/15 block h-px w-12 border-t" />
            <p className="text-espresso-60 font-display text-[0.7rem] font-medium tracking-[0.32em] uppercase">
              {t("papersLabel")}
            </p>
            <span className="border-espresso/15 block h-px flex-1 border-t" />
          </motion.div>

          <ol className="mt-10 space-y-0">
            {PAPER_KEYS.map((key, idx) => (
              <motion.li
                key={key}
                initial={{ opacity: 0, y: 16 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-60px" }}
                transition={{ duration: 0.85, delay: 0.1 + idx * 0.12, ease }}
                className={`group grid grid-cols-1 gap-2 py-7 md:grid-cols-[140px_1fr] md:gap-10 md:py-8 ${
                  idx > 0 ? "border-espresso/10 border-t" : ""
                }`}
              >
                <div className="flex items-baseline gap-3 md:flex-col md:gap-1">
                  <span className="font-display text-sienna text-xl font-light leading-none tracking-[-0.01em]">
                    0{idx + 1}
                  </span>
                  <span className="text-espresso-60 font-display text-[0.7rem] tracking-[0.24em] uppercase">
                    {t(`papers.${key}.tag`)}
                  </span>
                </div>
                <p
                  className="font-display text-espresso text-[clamp(1.0625rem,1.4vw,1.25rem)] leading-[1.5] font-light italic transition-colors duration-300 group-hover:text-sienna"
                  style={{ fontVariationSettings: '"opsz" 96, "SOFT" 40' }}
                >
                  {t(`papers.${key}.title`)}
                </p>
              </motion.li>
            ))}
          </ol>
        </div>

        {/* ─────────── CLOSING ─────────── */}
        <motion.p
          initial={{ opacity: 0, y: 14 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-60px" }}
          transition={{ duration: 1, ease }}
          className="font-display text-espresso mx-auto mt-28 max-w-[720px] text-center text-[clamp(1.25rem,1.85vw,1.625rem)] leading-[1.5] font-light italic md:mt-36"
          style={{ fontVariationSettings: '"opsz" 96, "SOFT" 50' }}
        >
          {t("closing")}
        </motion.p>

        {/* ─────────── STATS ROW ─────────── */}
        <div className="border-espresso/10 mx-auto mt-28 grid max-w-[900px] grid-cols-1 gap-12 border-t pt-16 md:mt-36 md:grid-cols-3 md:gap-8 md:pt-20">
          <Stat
            number={t("stats.yearsNumber")}
            label={t("stats.yearsLabel")}
            body={t("stats.yearsBody")}
            delay={0.05}
          />
          <Stat
            number={t("stats.customersNumber")}
            label={t("stats.customersLabel")}
            body={t("stats.customersBody")}
            delay={0.18}
          />
          <Stat
            number={t("stats.papersNumber")}
            label={t("stats.papersStatLabel")}
            body={t("stats.papersBody")}
            delay={0.31}
          />
        </div>

        {/* ─────────── CTA ROW ─────────── */}
        <motion.div
          initial={{ opacity: 0, y: 14 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-40px" }}
          transition={{ duration: 0.95, delay: 0.2, ease }}
          className="mt-24 flex flex-col items-center justify-center gap-4 sm:flex-row md:mt-32 md:gap-6"
        >
          <a
            href="#"
            className="group bg-espresso text-cream-50 hover:bg-sienna inline-flex items-center gap-3 rounded-full px-7 py-4 text-sm font-medium tracking-[0.02em] transition-all duration-300 ease-out hover:gap-5"
          >
            {t("ctaPrimary")}
            <ArrowRight className="size-4 transition-transform duration-300 group-hover:translate-x-0.5" />
          </a>
          <a
            href="#"
            className="group text-espresso border-espresso/25 hover:border-sienna hover:text-sienna inline-flex items-center gap-3 rounded-full border px-7 py-4 text-sm font-medium tracking-[0.02em] transition-all duration-300 ease-out hover:gap-5"
          >
            {t("ctaSecondary")}
            <ArrowRight className="size-4 transition-transform duration-300 group-hover:translate-x-0.5" />
          </a>
        </motion.div>
      </div>
    </section>
  );
}

/* ─────────────────────────────────────────────────────────────────────── */

function Stat({
  number,
  label,
  body,
  delay,
}: {
  number: string;
  label: string;
  body: string;
  delay: number;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-60px" }}
      transition={{ duration: 0.95, delay, ease }}
      className="flex flex-col items-center text-center"
    >
      <div
        className="font-display text-espresso flex items-baseline gap-1 text-[clamp(3.5rem,6vw,5rem)] leading-none font-light tracking-[-0.035em]"
        style={{ fontVariationSettings: '"opsz" 144, "SOFT" 30' }}
      >
        {number}
      </div>
      <p className="text-espresso-60 font-display mt-4 text-[0.7rem] font-medium tracking-[0.28em] uppercase">
        {label}
      </p>
      <p className="text-espresso/55 mt-2 max-w-[200px] text-sm leading-[1.5]">
        {body}
      </p>
    </motion.div>
  );
}

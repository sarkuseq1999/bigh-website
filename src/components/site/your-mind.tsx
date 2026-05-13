"use client";

import { motion } from "motion/react";
import { useTranslations } from "next-intl";
import { ArrowRight } from "lucide-react";

const ease = [0.2, 0.7, 0.2, 1] as const;

export function YourMind() {
  const t = useTranslations("YourMind");

  return (
    <section className="relative overflow-hidden bg-white">
      {/* Subtle thin sienna line entering from the top — visually marks the section start */}
      <motion.div
        initial={{ scaleX: 0 }}
        whileInView={{ scaleX: 1 }}
        viewport={{ once: true, margin: "-40px" }}
        transition={{ duration: 1.6, ease }}
        className="bg-sienna/30 mx-auto h-px max-w-[120px] origin-center"
      />

      <div className="mx-auto max-w-[1200px] px-6 pt-24 pb-32 md:px-12 md:pt-32 md:pb-44">
        {/* ─────────── EYEBROW ─────────── */}
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.7, ease }}
          className="flex justify-center"
        >
          <p className="text-espresso-40 font-display text-[0.7rem] font-medium tracking-[0.32em] uppercase italic">
            {t("eyebrow")}
          </p>
        </motion.div>

        {/* ─────────── HEADLINE ─────────── */}
        <motion.h2
          initial={{ opacity: 0, y: 18 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 1.1, delay: 0.15, ease }}
          className="font-display text-espresso mx-auto mt-14 max-w-[20ch] text-center text-[clamp(2.5rem,6.4vw,5.75rem)] font-light leading-[1.04] tracking-[-0.022em] md:mt-20"
          style={{ fontVariationSettings: '"opsz" 144, "SOFT" 30' }}
        >
          {t("headlineBefore")}
          <AIWord>{t("headlineAI")}</AIWord>
          {t("headlineAfter")}
          <em className="text-sienna font-light italic">
            {t("headlineEmphasis")}
          </em>
          {t("headlineEnd")}
        </motion.h2>

        {/* ─────────── BODY ─────────── */}
        <motion.p
          initial={{ opacity: 0, y: 14 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 1, delay: 0.35, ease }}
          className="text-espresso/75 mx-auto mt-16 max-w-[620px] text-center text-[clamp(1.0625rem,1.3vw,1.25rem)] leading-[1.7] md:mt-24"
        >
          {t("body")}
        </motion.p>

        {/* ─────────── CTA ─────────── */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-60px" }}
          transition={{ duration: 0.9, delay: 0.55, ease }}
          className="mt-14 flex justify-center md:mt-20"
        >
          <a
            href="#"
            className="group bg-espresso text-cream-50 hover:bg-sienna inline-flex items-center gap-3 rounded-full px-7 py-4 text-sm font-medium tracking-[0.02em] transition-all duration-300 ease-out hover:gap-5"
          >
            {t("cta")}
            <ArrowRight className="size-4 transition-transform duration-300 group-hover:translate-x-0.5" />
          </a>
        </motion.div>
      </div>
    </section>
  );
}

/* ──────────────────────────────────────────────────────────────────────── */
/* The AI word — sans-serif Geist treatment with a sienna underline marker. */
/* This is the design's central move: typographic contrast that visually   */
/* performs the headline's meaning.                                        */
/* ──────────────────────────────────────────────────────────────────────── */

function AIWord({ children }: { children: React.ReactNode }) {
  return (
    <span className="relative inline-block whitespace-nowrap">
      <span className="text-espresso font-sans text-[0.78em] font-medium tracking-[0.04em] uppercase">
        {children}
      </span>
      {/* Sienna underline marker — like a glossary term, but elegant */}
      <motion.span
        initial={{ scaleX: 0 }}
        whileInView={{ scaleX: 1 }}
        viewport={{ once: true, margin: "-80px" }}
        transition={{ duration: 0.9, delay: 0.6, ease }}
        aria-hidden="true"
        className="bg-sienna absolute -bottom-1 left-0 right-0 h-[2px] origin-left"
      />
    </span>
  );
}

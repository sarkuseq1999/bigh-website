"use client";

import { motion } from "motion/react";
import { useTranslations } from "next-intl";
import { ArrowRight } from "lucide-react";
import { useState } from "react";

const ease = [0.2, 0.7, 0.2, 1] as const;

export function EmailSignup() {
  const t = useTranslations("Signup");
  const [email, setEmail] = useState("");

  // No backend wiring yet — Resend / ConvertKit lands in a later session.
  return (
    <section
      className="relative overflow-hidden"
      style={{ backgroundColor: "#F2EAD8" }}
    >
      {/* ── Soft warm bokeh atmosphere behind, partially veiled ── */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 opacity-60"
        style={{
          backgroundImage: "url('/science/section-background-warm-bokeh.jpg')",
          backgroundSize: "cover",
          backgroundPosition: "center",
          backgroundRepeat: "no-repeat",
          mixBlendMode: "multiply",
        }}
      />

      {/* ── Top white → cream fade for smooth seam with section 6 ── */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-x-0 top-0 h-32"
        style={{
          background:
            "linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(255,255,255,0.55) 45%, rgba(255,255,255,0) 100%)",
        }}
      />

      {/* ── Subtle central cream wash to lift the form area ── */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0"
        style={{
          background:
            "radial-gradient(ellipse 55% 50% at 50% 50%, rgba(250,246,239,0.35) 0%, rgba(250,246,239,0) 70%)",
        }}
      />

      <div className="relative mx-auto max-w-[680px] px-6 py-32 text-center md:px-12 md:py-48">
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
            <p className="text-espresso/65 font-display text-[0.7rem] font-medium tracking-[0.32em] uppercase">
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
          className="font-display text-espresso mt-10 text-[clamp(2.5rem,5.5vw,4.5rem)] font-light leading-[1.04] tracking-[-0.02em] md:mt-14"
          style={{ fontVariationSettings: '"opsz" 144, "SOFT" 30' }}
        >
          {t("headlineBefore")}
          <em className="text-sienna font-light italic">
            {t("headlineEmphasis")}
          </em>
        </motion.h2>

        {/* ─────────── INTRO ─────────── */}
        <motion.p
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 1, delay: 0.3, ease }}
          className="text-espresso/75 mx-auto mt-10 max-w-[520px] text-[clamp(1rem,1.2vw,1.125rem)] leading-[1.7] md:mt-14"
        >
          {t("intro")}
        </motion.p>

        {/* ─────────── FORM ─────────── */}
        <motion.form
          initial={{ opacity: 0, y: 14 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 1, delay: 0.5, ease }}
          onSubmit={(e) => e.preventDefault()}
          className="mx-auto mt-14 max-w-[460px] md:mt-20"
        >
          <div className="group border-espresso/25 focus-within:border-espresso/55 flex items-center gap-3 border-b pb-3 transition-colors duration-300">
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder={t("placeholder")}
              aria-label={t("cta")}
              className="font-display text-espresso placeholder:text-espresso/40 flex-1 bg-transparent text-base outline-none md:text-lg"
              style={{ fontVariationSettings: '"opsz" 24' }}
            />
            <button
              type="submit"
              aria-label={t("cta")}
              className="group/btn bg-espresso text-cream-50 hover:bg-sienna flex size-10 shrink-0 items-center justify-center rounded-full transition-colors duration-300 md:size-11"
            >
              <ArrowRight className="size-4 transition-transform duration-300 group-hover/btn:translate-x-0.5" />
            </button>
          </div>

          {/* Tiny CTA label hint */}
          <p className="text-espresso/55 mt-4 text-xs tracking-[0.04em]">
            {t("cta")}
          </p>
        </motion.form>

        {/* ─────────── REASSURANCE ─────────── */}
        <motion.p
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true, margin: "-60px" }}
          transition={{ duration: 0.9, delay: 0.8, ease }}
          className="text-espresso/50 mt-12 text-xs tracking-[0.04em] md:mt-16"
        >
          {t("reassurance")}
        </motion.p>
      </div>
    </section>
  );
}

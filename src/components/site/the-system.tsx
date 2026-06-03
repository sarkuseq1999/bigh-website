"use client";

import { useTranslations } from "next-intl";
import {
  Anchor,
  Shield,
  Flame,
  Droplets,
  Hammer,
  MoonStar,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";
import { Reveal } from "@/components/site/reveal";

/* ── icon map keyed to product key ─────────────────────────────────────── */
const ICON_MAP: Record<string, LucideIcon> = {
  nuricell:    Anchor,
  natureCalm:  Shield,
  turmerific:  Flame,
  advancedOpc: Droplets,
  greenBee:    Hammer,
  deerHorn:    MoonStar,
};

/* ── the six product keys in display order ──────────────────────────────── */
const SUPPORTING_KEYS = [
  "natureCalm",
  "turmerific",
  "advancedOpc",
  "greenBee",
  "deerHorn",
] as const;

export function TheSystem() {
  const t = useTranslations("System");

  const nuricellName     = t("products.nuricell.name");
  const nuricellRole     = t("products.nuricell.role");
  const nuricellLine     = t("products.nuricell.line");
  const nuricellTag      = t("products.nuricell.tag");

  return (
    <section id="system" className="bg-paper-2 py-24 md:py-36">
      <div className="mx-auto max-w-[1200px] px-6 md:px-14">

        {/* ── EYEBROW ───────────────────────────────────────────────── */}
        <Reveal>
          <p className="font-mono uppercase tracking-[0.2em] text-[0.6875rem] text-ink-soft text-center">
            {t("eyebrow")}
          </p>
        </Reveal>

        {/* ── HEADLINE ──────────────────────────────────────────────── */}
        <Reveal delay={0.08}>
          <h2 className="font-display font-light text-ink text-center mt-5
                         text-[clamp(2.25rem,3.5vw,3.5rem)] leading-[1.1] tracking-[-0.02em]
                         max-w-[22ch] mx-auto">
            {t("headline")}
          </h2>
        </Reveal>

        {/* ── INTRO ─────────────────────────────────────────────────── */}
        <Reveal delay={0.16}>
          <p className="text-ink-soft text-center mt-6 text-[1.125rem] leading-[1.7]
                        max-w-[52ch] mx-auto">
            {t("intro")}
          </p>
        </Reveal>

        {/* ── NURICELL — featured / elevated card ───────────────────── */}
        <Reveal delay={0.22} className="mt-16 md:mt-20">
          <div className="group relative rounded-2xl bg-paper border border-line
                          p-8 md:p-10 flex flex-col md:flex-row md:items-center gap-8
                          transition-all duration-300 ease-out
                          hover:-translate-y-1 hover:shadow-[0_8px_32px_rgba(27,26,23,0.09)]">

            {/* left: icon + tag */}
            <div className="shrink-0 flex flex-col items-center md:items-start gap-4">
              <span className="inline-flex items-center justify-center w-14 h-14 rounded-xl
                               bg-paper-2">
                <Anchor className="text-amber-hi" size={28} strokeWidth={1.5} />
              </span>
              <span className="font-mono uppercase tracking-[0.18em] text-[0.6875rem]
                               bg-amber text-ink px-2.5 py-1 rounded-full">
                {nuricellTag}
              </span>
            </div>

            {/* right: name + role + line */}
            <div className="flex-1">
              <p className="font-mono uppercase tracking-[0.16em] text-[0.6875rem] text-ink-soft">
                {nuricellRole}
              </p>
              <h3 className="font-display font-light text-ink mt-2
                             text-[clamp(2rem,3vw,2.75rem)] leading-[1.05] tracking-[-0.015em]">
                {nuricellName}
              </h3>
              <p className="text-ink text-[1.125rem] leading-[1.6] mt-3">
                {nuricellLine}
              </p>
            </div>
          </div>
        </Reveal>

        {/* ── SUPPORTING FIVE — responsive grid ─────────────────────── */}
        <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 md:gap-6">
          {SUPPORTING_KEYS.map((key, idx) => {
            const Icon = ICON_MAP[key];
            const name = t(`products.${key}.name`);
            const role = t(`products.${key}.role`);
            const line = t(`products.${key}.line`);
            const tag  = t(`products.${key}.tag`);
            return (
              <Reveal key={key} delay={0.1 + idx * 0.07}>
                <article
                  className="group flex flex-col h-full rounded-xl bg-paper border border-line
                             p-6 transition-all duration-300 ease-out
                             hover:-translate-y-1 hover:shadow-[0_6px_24px_rgba(27,26,23,0.08)]"
                >
                  <div className="flex items-center justify-between">
                    <span className="inline-flex items-center justify-center w-11 h-11 rounded-lg bg-paper-2">
                      <Icon className="text-amber-hi" size={22} strokeWidth={1.5} />
                    </span>
                    <span className="font-mono uppercase tracking-[0.14em] text-[0.6875rem]
                                     text-ink-soft border border-line px-2 py-0.5 rounded-full">
                      {tag}
                    </span>
                  </div>

                  <p className="font-mono uppercase tracking-[0.16em] text-[0.6875rem] text-ink-soft mt-5">
                    {role}
                  </p>
                  <h3 className="font-display font-light text-ink mt-1.5
                                 text-[1.375rem] leading-[1.1] tracking-[-0.01em]">
                    {name}
                  </h3>
                  <p className="text-ink text-[1.125rem] leading-[1.6] mt-3">
                    {line}
                  </p>
                </article>
              </Reveal>
            );
          })}
        </div>

        {/* ── BUNDLE CTAs ───────────────────────────────────────────── */}
        <Reveal delay={0.1} className="mt-14 md:mt-16">
          <div className="flex flex-wrap justify-center gap-4">
            {/* primary */}
            <a
              href="#"
              className="inline-flex items-center justify-center min-h-[48px] rounded-full
                         bg-amber text-ink font-medium text-[1.0625rem] tracking-[0.01em]
                         px-7 py-3 transition-all duration-200
                         hover:bg-amber-hi focus-visible:outline-none
                         focus-visible:ring-2 focus-visible:ring-amber-hi focus-visible:ring-offset-2"
            >
              {t("bundles.three")}
            </a>

            {/* secondary outlined */}
            <a
              href="#"
              className="inline-flex items-center justify-center min-h-[48px] rounded-full
                         border-2 border-amber text-ink font-medium text-[1.0625rem] tracking-[0.01em]
                         px-7 py-3 transition-all duration-200
                         hover:bg-amber/10 focus-visible:outline-none
                         focus-visible:ring-2 focus-visible:ring-amber focus-visible:ring-offset-2"
            >
              {t("bundles.four")}
            </a>

            {/* ghost */}
            <a
              href="#"
              className="inline-flex items-center justify-center min-h-[48px] rounded-full
                         border border-line text-ink font-medium text-[1.0625rem] tracking-[0.01em]
                         px-7 py-3 transition-all duration-200
                         hover:border-amber hover:bg-amber/5 focus-visible:outline-none
                         focus-visible:ring-2 focus-visible:ring-amber focus-visible:ring-offset-2"
            >
              {t("bundles.protocol")}
            </a>
          </div>
        </Reveal>

      </div>
    </section>
  );
}

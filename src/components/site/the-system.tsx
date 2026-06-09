"use client";

import Image from "next/image";
import { useTranslations } from "next-intl";
import { Reveal } from "@/components/site/reveal";

/* ── ingredient still-life per product (no people; honest objects) ─────── */
const CARD_IMAGES: Record<string, string> = {
  natureCalm:  "/images/ing-calm-v2.jpg",
  turmerific:  "/images/ing-turmeric.jpg",
  advancedOpc: "/images/ing-grapeseed-v2.jpg",
  greenBee:    "/images/ing-propolis.jpg",
  deerHorn:    "/images/ing-reishi.jpg",
};

/* ── the five supporting product keys in display order ──────────────────── */
const SUPPORTING_KEYS = [
  "natureCalm",
  "turmerific",
  "advancedOpc",
  "greenBee",
  "deerHorn",
] as const;

export function TheSystem() {
  const t = useTranslations("System");

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
                         text-[clamp(2.5rem,4vw,4rem)] leading-[1.08] tracking-[-0.02em]
                         max-w-[18ch] mx-auto">
            {t("headline")}
          </h2>
        </Reveal>

        {/* ── INTRO — the one place "built on the science" is said ──── */}
        <Reveal delay={0.16}>
          <p className="text-ink-soft text-center mt-6 text-[1.125rem] leading-[1.7]
                        max-w-[52ch] mx-auto">
            {t("intro")}
          </p>
        </Reveal>

        {/* ── NURICELL — featured card with the product itself ──────── */}
        <Reveal delay={0.22} className="mt-16 md:mt-20">
          <div className="group relative overflow-hidden rounded-2xl bg-paper border border-line
                          grid grid-cols-1 md:grid-cols-[1.3fr_1fr]
                          transition-all duration-300 ease-out
                          hover:-translate-y-1 hover:shadow-[0_8px_32px_rgba(27,26,23,0.09)]">

            {/* left: name + role + line + ingredients */}
            <div className="p-8 md:p-12 flex flex-col justify-center">
              <div className="flex items-center gap-3">
                <p className="font-mono uppercase tracking-[0.16em] text-[0.6875rem] text-ink-soft">
                  {t("products.nuricell.role")}
                </p>
                <span className="font-mono uppercase tracking-[0.18em] text-[0.625rem]
                                 border border-amber text-ink px-2.5 py-1 rounded-full">
                  {t("products.nuricell.tag")}
                </span>
              </div>
              <h3 className="font-display font-light text-ink mt-3
                             text-[clamp(2.25rem,3.4vw,3.25rem)] leading-[1.05] tracking-[-0.015em]">
                {t("products.nuricell.name")}
              </h3>
              <p className="text-ink text-[1.1875rem] leading-[1.6] mt-4 max-w-[40ch]">
                {t("products.nuricell.line")}
              </p>
              <p className="font-mono uppercase tracking-[0.14em] text-[0.75rem] text-ink-soft mt-5">
                {t("products.nuricell.fact")}
              </p>
              <p className="text-ink-soft text-[1rem] leading-[1.6] mt-4">
                {t("products.nuricell.proof")}{" "}
                <a href="#scientist" className="text-ink underline-offset-4 hover:underline">
                  {t("products.nuricell.proofCta")}
                </a>
              </p>
            </div>

            {/* right: the product, photographed */}
            <div className="relative min-h-[280px] md:min-h-[340px]">
              <Image
                src="/images/nuricell-bottle.jpg"
                alt={t("products.nuricell.name")}
                fill
                sizes="(min-width: 768px) 40vw, 100vw"
                className="object-cover"
              />
            </div>
          </div>
        </Reveal>

        {/* ── SUPPORTING FIVE — one confident row under the foundation ── */}
        <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-5">
          {SUPPORTING_KEYS.map((key, idx) => {
            const name = t(`products.${key}.name`);
            const role = t(`products.${key}.role`);
            const line = t(`products.${key}.line`);
            const fact = t(`products.${key}.fact`);
            return (
              <Reveal key={key} delay={0.1 + idx * 0.07}>
                <article
                  className="group flex flex-col h-full overflow-hidden rounded-xl bg-paper border border-line
                             transition-all duration-300 ease-out
                             hover:-translate-y-1 hover:shadow-[0_6px_24px_rgba(27,26,23,0.08)]"
                >
                  {/* ingredient still-life */}
                  <div className="relative aspect-[4/3] w-full">
                    <Image
                      src={CARD_IMAGES[key]}
                      alt={fact}
                      fill
                      sizes="(min-width: 1024px) 20vw, (min-width: 640px) 50vw, 100vw"
                      className="object-cover"
                    />
                  </div>

                  <div className="p-5 flex flex-col flex-1">
                    <p className="font-mono uppercase tracking-[0.16em] text-[0.6875rem] text-amber">
                      {role}
                    </p>
                    <h3 className="font-display font-light text-ink mt-1.5
                                   text-[1.3125rem] leading-[1.1] tracking-[-0.01em]">
                      {name}
                    </h3>
                    <p className="text-ink text-[1rem] leading-[1.55] mt-2.5">
                      {line}
                    </p>
                    <p className="font-mono uppercase tracking-[0.14em] text-[0.6875rem] text-ink-soft mt-auto pt-4">
                      {fact}
                    </p>
                  </div>
                </article>
              </Reveal>
            );
          })}
        </div>

        {/* ── CTA — one clear door, one quiet alternative ───────────── */}
        <Reveal delay={0.1} className="mt-14 md:mt-16">
          <div className="flex flex-col items-center gap-5">
            <a
              href="#quiz"
              className="inline-flex items-center justify-center min-h-[56px] rounded-full
                         bg-ink text-paper font-medium text-[1.125rem] tracking-[0.01em]
                         px-10 py-4 transition-colors duration-200
                         hover:bg-forest focus-visible:outline-none
                         focus-visible:ring-2 focus-visible:ring-ink focus-visible:ring-offset-2"
            >
              {t("bundles.protocol")}
            </a>
            <a
              href="#nuricell"
              className="text-ink text-[1.0625rem] font-medium underline-offset-4 hover:underline"
            >
              {t("bundles.single")}
            </a>
          </div>
        </Reveal>

      </div>
    </section>
  );
}

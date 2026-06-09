"use client";

import { useTranslations } from "next-intl";
import { Reveal } from "@/components/site/reveal";

/* ─────────────────────────────────────────────────────────────────────────
   YourMind — Section 2 "The New Reality"
   Editorial, text-forward. bg-paper-2. No imagery required.
   Stacked layout: eyebrow → headline → subhead → body → capabilities
   (three-row centerpiece) → closing → pivot.
───────────────────────────────────────────────────────────────────────── */

export function YourMind() {
  const t = useTranslations("NewReality");

  return (
    <section id="yourmind" className="bg-paper-2">
      <div className="mx-auto max-w-[1100px] px-6 py-24 md:px-14 md:py-36">

        {/* Eyebrow */}
        <Reveal>
          <p className="font-mono text-[0.6875rem] uppercase tracking-[0.2em] text-ink-soft">
            {t("eyebrow")}
          </p>
        </Reveal>

        {/* Headline */}
        <Reveal delay={0.1}>
          <h2 className="mt-6 font-display text-[clamp(2.5rem,4vw,4rem)] font-light leading-[1.1] tracking-[-0.02em] text-balance text-ink md:mt-8">
            {t("headline")}
          </h2>
        </Reveal>

        {/* Subhead — the hook; punchline gets its own full line */}
        <Reveal delay={0.2}>
          <p className="mt-6 max-w-[44ch] font-display text-[1.375rem] font-light leading-[1.4] text-ink md:text-[1.5rem]">
            {t("subheadSetup")}
            <br />
            {t("subheadTurn")}
          </p>
        </Reveal>

        {/* Body P1 */}
        <Reveal delay={0.3}>
          <p className="mt-8 max-w-[62ch] text-[1.125rem] leading-[1.6] text-ink md:mt-10 md:text-[1.1875rem]">
            {t("bodyP1")}
          </p>
        </Reveal>

        {/* Body P2 */}
        <Reveal delay={0.4}>
          <p className="mt-5 max-w-[62ch] text-[1.125rem] font-medium leading-[1.6] text-ink md:text-[1.1875rem]">
            {t("bodyP2")}
          </p>
        </Reveal>

        {/* ── Capabilities centerpiece ──────────────────────────────────────
            The three words ARE the imagery: display-scale serif terms in a
            rising crescendo, definitions set quietly beneath. */}
        <div
          className="mt-16 md:mt-20"
          aria-label="Human capabilities"
          role="list"
        >
          {(
            [
              { key: "judgment", num: "01", size: "text-[clamp(2.5rem,4.6vw,4.25rem)]" },
              { key: "wisdom",   num: "02", size: "text-[clamp(2.75rem,5.2vw,4.75rem)]" },
              { key: "taste",    num: "03", size: "text-[clamp(3rem,5.8vw,5.25rem)]" },
            ] as const
          ).map(({ key, num, size }, idx) => (
            <Reveal key={key} delay={0.1 + idx * 0.12}>
              <div
                role="listitem"
                className={`flex items-baseline gap-6 border-t border-line py-9 md:gap-10 md:py-11 ${idx === 2 ? "border-b" : ""}`}
              >
                <span
                  aria-hidden="true"
                  className="font-mono text-[0.75rem] tracking-[0.2em] text-ink-soft shrink-0 translate-y-[-0.25em]"
                >
                  {num}
                </span>
                <div>
                  <h3
                    className={`m-0 font-display ${size} font-light leading-[1.02] tracking-[-0.02em] text-ink`}
                  >
                    {t(`capabilities.${key}.term`)}
                  </h3>
                  <p className="mt-3 max-w-[40ch] text-[1.0625rem] leading-[1.55] text-ink-soft md:text-[1.125rem]">
                    {t(`capabilities.${key}.definition`)}
                  </p>
                </div>
              </div>
            </Reveal>
          ))}
        </div>

        {/* Closing */}
        <Reveal delay={0.1}>
          <p className="mt-14 max-w-[58ch] text-[1.125rem] leading-[1.6] text-ink md:mt-16 md:text-[1.1875rem]">
            {t("closing")}
          </p>
        </Reveal>

        {/* Pivot — the hand-off line performs its own diminuendo */}
        <Reveal delay={0.2}>
          <p className="mt-10 text-ink font-display font-light italic leading-[1.3]">
            <span className="text-[1.75rem] md:text-[2rem]">{t("pivotLead")} </span>
            <span className="text-[1.375rem] md:text-[1.5rem]">{t("pivotMid")} </span>
            <span className="text-[1.0625rem] md:text-[1.125rem]">{t("pivotEnd")}</span>
          </p>
        </Reveal>

      </div>
    </section>
  );
}

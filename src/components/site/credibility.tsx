"use client";

import { useTranslations } from "next-intl";
import { Reveal } from "@/components/site/reveal";

/* The three papers from PNAS Vol. 99, No. 4 (February 19, 2002).
   Titles verified against pnas.org / the Linus Pauling Institute. */
const PAPERS = [
  "Memory loss in old rats is associated with brain mitochondrial decay and RNA/DNA oxidation: partial reversal by feeding acetyl-L-carnitine and/or R-α-lipoic acid",
  "Age-associated mitochondrial oxidative decay: improvement of carnitine acetyltransferase substrate-binding affinity and activity in brain",
  "Feeding acetyl-L-carnitine and lipoic acid to old rats significantly improves metabolic function while decreasing oxidative stress",
];

const PNAS_ISSUE_URL = "https://www.pnas.org/toc/pnas/99/4";

/* ─────────────────────────────────────────────────────────────────────── */
/* The issue plate — typeset evidence, not set-dressing.                   */
/* ─────────────────────────────────────────────────────────────────────── */

function IssuePlate({
  journalFull,
  issueLine,
  plateNote,
  plateCta,
}: {
  journalFull: string;
  issueLine: string;
  plateNote: string;
  plateCta: string;
}) {
  return (
    <div className="flex h-full w-full flex-col rounded-sm border border-amber-hi/20 bg-[#F4EEE1] px-8 py-9 shadow-[0_18px_50px_rgba(0,0,0,0.45)] md:px-10 md:py-10">
      {/* Masthead */}
      <p className="font-display text-[2.5rem] font-light leading-none tracking-[-0.01em] text-ink">
        PNAS
      </p>
      <p className="mt-2 font-mono text-[0.6875rem] uppercase tracking-[0.16em] text-ink-soft">
        {journalFull}
      </p>
      <p className="mt-1 font-mono text-[0.6875rem] uppercase tracking-[0.16em] text-ink-soft">
        {issueLine}
      </p>

      <div className="my-6 h-px w-full bg-line" aria-hidden="true" />

      {/* The three papers */}
      <ol className="m-0 flex list-none flex-col gap-5 p-0">
        {PAPERS.map((title, i) => (
          <li key={i} className="grid grid-cols-[auto_1fr] gap-3">
            <span className="font-mono text-[0.6875rem] tracking-[0.16em] text-amber pt-[0.3em]">
              {String(i + 1).padStart(2, "0")}
            </span>
            <span className="font-display text-[0.9375rem] italic font-light leading-[1.5] text-ink">
              {title}
            </span>
          </li>
        ))}
      </ol>

      <div className="mt-auto pt-7">
        <p className="font-mono text-[0.6875rem] uppercase tracking-[0.14em] leading-[1.7] text-ink-soft">
          {plateNote}
        </p>
        <a
          href={PNAS_ISSUE_URL}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-4 inline-flex min-h-[40px] items-center rounded-full border border-ink/30 px-5 font-mono text-[0.75rem] uppercase tracking-[0.14em] text-ink transition-colors duration-200 hover:border-ink hover:bg-ink/5"
        >
          {plateCta}
        </a>
      </div>
    </div>
  );
}

/* ─────────────────────────────────────────────────────────────────────── */
/* Main export                                                             */
/* ─────────────────────────────────────────────────────────────────────── */

export function Credibility() {
  const t = useTranslations("Scientist");

  return (
    <section
      id="scientist"
      className="bg-forest relative overflow-hidden"
    >
      {/* Subtle top edge separator */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-x-0 top-0 h-px bg-amber-hi/10"
      />

      <div className="mx-auto max-w-[1200px] px-6 py-24 md:px-14 md:py-32">

        {/* ─── EYEBROW ─── */}
        <Reveal>
          <p className="font-mono uppercase tracking-[0.2em] text-amber-hi text-[0.6875rem]">
            {t("eyebrow")}
          </p>
        </Reveal>

        {/* ─── HEADLINE + SUBHEAD ─── */}
        <Reveal delay={0.1}>
          <h2 className="font-display font-light text-paper mt-6 text-[clamp(2.5rem,4vw,4rem)] leading-[1.08] tracking-[-0.022em] max-w-[18ch]">
            {t("headline")}
          </h2>
        </Reveal>

        <Reveal delay={0.18}>
          <p className="text-paper/85 mt-5 max-w-[58ch] text-[1.125rem] md:text-[1.1875rem] leading-[1.6]">
            {t("subhead")}
          </p>
        </Reveal>

        {/* ─── ANCHOR — one line, one decision ─── */}
        <Reveal delay={0.24}>
          <p className="mt-10 font-display font-light text-amber-hi text-[clamp(1.5rem,2.8vw,2.375rem)] leading-[1.2] tracking-[-0.01em]">
            {t("anchor")}
          </p>
        </Reveal>

        {/* ─── MAIN TWO-COLUMN ZONE ─── */}
        <div className="mt-12 md:mt-16 grid grid-cols-1 md:grid-cols-[1fr_1.2fr] gap-12 md:gap-16 items-stretch">

          {/* LEFT — the issue itself, typeset (no portrait per the
              real-people constraint; the evidence carries the slot) */}
          <Reveal delay={0.05} className="flex w-full">
            <IssuePlate
              journalFull={t("journalFull")}
              issueLine={t("issueLine")}
              plateNote={t("plateNote")}
              plateCta={t("plateCta")}
            />
          </Reveal>

          {/* RIGHT — body, top-aligned to the plate's masthead */}
          <div className="flex flex-col justify-start gap-0 md:pt-2">

            <Reveal delay={0.1}>
              <p className="text-paper/90 text-[1.125rem] md:text-[1.1875rem] leading-[1.6]">
                {t("bodyP1")}
              </p>
            </Reveal>

            <Reveal delay={0.15} className="mt-5">
              <p className="text-paper/90 text-[1.125rem] md:text-[1.1875rem] leading-[1.6]">
                {t("bodyP2")}
              </p>
            </Reveal>

            <Reveal delay={0.2} className="mt-5">
              <p className="text-paper/85 text-[1.125rem] md:text-[1.1875rem] leading-[1.6]">
                {t("bodyP3")}
              </p>
            </Reveal>

          </div>
        </div>

        {/* Pivot — the reveal, set as the section's closing moment */}
        <Reveal delay={0.1}>
          <p className="mt-16 md:mt-20 font-display font-light italic text-paper text-[clamp(1.875rem,3.4vw,3rem)] leading-[1.25] tracking-[-0.01em]">
            {t("pivotA")}
            <br />
            {t("pivotB")}
          </p>
        </Reveal>

      </div>
    </section>
  );
}

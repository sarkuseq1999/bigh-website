import { setRequestLocale } from "next-intl/server";
import Link from "next/link";

import { SiteHeader } from "@/components/site/site-header";
import { SiteFooter } from "@/components/site/site-footer";

export default async function GamesHubPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  setRequestLocale(locale);

  return (
    <>
      <SiteHeader />
      <main className="bg-background flex-1 pt-32 pb-24">
        <section className="mx-auto max-w-5xl px-6">
          <div className="text-center">
            <p className="text-muted-foreground mb-3 text-xs tracking-[0.3em] uppercase">
              Brain Games
            </p>
            <h1 className="font-display text-foreground text-5xl leading-[0.95] font-light tracking-tight md:text-7xl">
              A small daily ritual <br />
              for a <em>sharper</em> mind.
            </h1>
            <p className="text-muted-foreground mx-auto mt-6 max-w-xl text-lg">
              Two-minute games designed to test attention, memory, and reaction —
              the cognitive signals that quietly fade when the brain's mitochondria
              slow down.
            </p>
          </div>

          <div className="mt-20 grid gap-8 md:grid-cols-2">
            <GameCard
              href={`/${locale}/games/daily-spark`}
              eyebrow="Daily · 2 min"
              title="Daily Spark"
              description="A single word puzzle that resets at midnight. Build a streak, share your result, train your brain's pattern-finding."
              gradient="from-[#e5e5e5] via-[#a3a3a3] to-[#171717]"
              accent="text-foreground"
              preview={
                <div className="grid grid-cols-5 gap-1.5">
                  {["S", "P", "A", "R", "K"].map((l, i) => (
                    <div
                      key={i}
                      className={`flex h-12 w-12 items-center justify-center rounded-md text-xl font-semibold ${
                        i === 0 || i === 4
                          ? "bg-[#171717] text-white"
                          : i === 2
                            ? "bg-[#525252] text-white"
                            : "bg-white/60 text-foreground/40"
                      }`}
                    >
                      {l}
                    </div>
                  ))}
                </div>
              }
            />

            <GameCard
              href={`/${locale}/games/catch-the-spark`}
              eyebrow="Anytime · 30 sec"
              title="Catch the Spark"
              description="Sparks of light drift across the dark. Catch the gold, dodge the red. A pure measure of attention and reaction time."
              gradient="from-[#0a0a1a] via-[#1a1530] to-[#2a1a3a]"
              accent="text-white"
              preview={
                <div className="relative h-24 w-full overflow-hidden rounded-lg">
                  <div className="absolute top-3 left-4 h-3 w-3 rounded-full bg-amber-300 shadow-[0_0_20px_rgba(252,211,77,0.8)]" />
                  <div className="absolute top-12 left-20 h-4 w-4 rounded-full bg-amber-200 shadow-[0_0_24px_rgba(254,243,199,0.8)]" />
                  <div className="absolute right-6 bottom-4 h-2.5 w-2.5 rounded-full bg-rose-400 shadow-[0_0_14px_rgba(251,113,133,0.8)]" />
                  <div className="absolute top-6 right-16 h-3 w-3 rounded-full bg-amber-300 shadow-[0_0_18px_rgba(252,211,77,0.8)]" />
                </div>
              }
            />
          </div>

          <p className="text-muted-foreground mx-auto mt-16 max-w-md text-center text-sm">
            More games are coming. These are prototypes — your sharpness data
            stays on this device.
          </p>
        </section>
      </main>
      <SiteFooter />
    </>
  );
}

function GameCard({
  href,
  eyebrow,
  title,
  description,
  gradient,
  accent,
  preview,
}: {
  href: string;
  eyebrow: string;
  title: string;
  description: string;
  gradient: string;
  accent: string;
  preview: React.ReactNode;
}) {
  return (
    <Link
      href={href}
      className="group relative block overflow-hidden rounded-3xl shadow-[0_30px_80px_-30px_rgba(0,0,0,0.25)] ring-1 ring-black/5 transition-shadow hover:shadow-[0_40px_100px_-30px_rgba(0,0,0,0.35)]"
    >
      <div className={`bg-gradient-to-br ${gradient} flex h-44 items-center justify-center p-6`}>
        {preview}
      </div>
      <div className="bg-white p-7">
        <p className={`mb-2 text-xs tracking-[0.25em] uppercase ${accent}/60`}>
          {eyebrow}
        </p>
        <h2 className="font-display text-foreground text-3xl font-light tracking-tight">
          {title}
        </h2>
        <p className="text-muted-foreground mt-3 text-base leading-relaxed">
          {description}
        </p>
        <p className="text-foreground mt-5 inline-flex items-center gap-1 text-sm font-medium transition-transform group-hover:translate-x-1">
          Play <span aria-hidden>→</span>
        </p>
      </div>
    </Link>
  );
}

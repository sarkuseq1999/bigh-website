import { setRequestLocale } from "next-intl/server";
import Link from "next/link";

import { SiteHeader } from "@/components/site/site-header";
import { SiteFooter } from "@/components/site/site-footer";
import { CatchTheSpark } from "@/components/games/catch-the-spark";

export default async function CatchTheSparkPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  setRequestLocale(locale);

  return (
    <>
      <SiteHeader />
      <main className="bg-background flex-1 pt-28 pb-12">
        <section className="mx-auto max-w-3xl px-6 py-6 text-center">
          <Link
            href={`/${locale}/games`}
            className="text-muted-foreground hover:text-foreground text-xs tracking-[0.25em] uppercase"
          >
            ← All games
          </Link>
          <h1 className="font-display text-foreground mt-4 text-4xl leading-tight font-light tracking-tight md:text-5xl">
            Catch the <em>Spark</em>
          </h1>
          <p className="text-muted-foreground mx-auto mt-3 max-w-md text-sm">
            Thirty seconds of reaction. Catch the gold, dodge the red.
          </p>
        </section>
        <CatchTheSpark />
      </main>
      <SiteFooter />
    </>
  );
}

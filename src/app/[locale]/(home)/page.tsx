import { setRequestLocale, getTranslations } from "next-intl/server";

import { Hero } from "@/components/home/hero";
import { Truth } from "@/components/home/truth";
import { routing, type Locale } from "@/i18n/routing";

export function generateStaticParams() {
  return routing.locales.map((locale) => ({ locale }));
}

export default async function HomePage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale: raw } = await params;
  const locale = raw as Locale;
  setRequestLocale(locale);
  const t = await getTranslations({ locale, namespace: "Home" });

  return (
    <>
      <Hero
        eyebrow=""
        l1={t("hero.line1")}
        l2={t("hero.line2")}
        reveal={t("hero.reveal")}
        cta={t("hero.cta")}
      />
      <Truth
        kicker={t("truth.kicker")}
        body={t("truth.body")}
        stat1={t("truth.stat1")}
        stat2={t("truth.stat2")}
      />
    </>
  );
}

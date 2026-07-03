import { setRequestLocale, getTranslations } from "next-intl/server";

import { Hero } from "@/components/home/hero";
import { Nuricell } from "@/components/home/nuricell";
import { Scientist } from "@/components/home/scientist";
import { Truth } from "@/components/home/truth";
import { productName } from "@/data/products";
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
      <Scientist
        kicker={t("liu.kicker")}
        name={t("liu.name")}
        honor={t("liu.honor")}
        body={t("liu.body")}
        quote={t("liu.quote")}
        cta={t("liu.cta")}
      />
      <Nuricell
        name={productName("nuricell", locale)}
        lead={t("nuricell.lead")}
        dose={t("nuricell.dose")}
        doseBody={t("nuricell.doseBody")}
        ingredients={t("nuricell.ingredients")}
        heritage={t("nuricell.heritage")}
        cta={t("nuricell.cta")}
      />
    </>
  );
}

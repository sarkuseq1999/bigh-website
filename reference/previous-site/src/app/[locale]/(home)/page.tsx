import { setRequestLocale, getTranslations } from "next-intl/server";

import { Family } from "@/components/home/family";
import { Heart } from "@/components/home/heart";
import { Hero } from "@/components/home/hero";
import { Honest } from "@/components/home/honest";
import { Nuricell } from "@/components/home/nuricell";
import { Ritual } from "@/components/home/ritual";
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
        revealAccent={t("hero.revealAccent")}
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
      <Family
        locale={locale}
        kicker={t("family.kicker")}
        title={t("family.title")}
        jobs={{
          turmerific: t("family.jobs.turmerific"),
          "advanced-opc-formula": t("family.jobs.advanced-opc-formula"),
          "green-bee-propolis": t("family.jobs.green-bee-propolis"),
          "nature-calm": t("family.jobs.nature-calm"),
          "deer-horn-reishi": t("family.jobs.deer-horn-reishi"),
        }}
      />
      <Heart title={t("heart.title")} body={t("heart.body")} />
      <Honest
        kicker={t("honest.kicker")}
        title={t("honest.title")}
        pledges={[
          { title: t("honest.pledges.doses.title"), body: t("honest.pledges.doses.body") },
          { title: t("honest.pledges.science.title"), body: t("honest.pledges.science.body") },
          { title: t("honest.pledges.hype.title"), body: t("honest.pledges.hype.body") },
        ]}
      />
      <Ritual
        title={t("ritual.title")}
        body={t("ritual.body")}
        primary={t("ritual.primary")}
        secondary={t("ritual.secondary")}
      />
    </>
  );
}

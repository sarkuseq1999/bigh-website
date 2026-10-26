import type { Metadata } from "next";
import { getTranslations, setRequestLocale } from "next-intl/server";
import { AboutInk } from "@/components/about/about-ink";
import { BeforeHydration } from "@/components/about/before-hydration";
import { LET_THE_CIRCLE_GO } from "@/components/about/let-the-circle-go";
import { ProductPagesProvider } from "@/components/home/product-action";
import { SiteDialogs } from "@/components/ink/dialogs";
import { productPageLinks } from "@/components/product/catalog";
import copyKeys from "@/i18n/copy-keys.json";
import { redirect } from "@/i18n/navigation";

type Params = Promise<{ locale: string }>;

// For comparison only (Mo, October 26, 2026): About with the bigger circle's other layout, the
// words under the circle; /about has them inside it. Remove this route once Mo has picked one.
export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const { locale } = await params;
  const translate = await getTranslations({ locale, namespace: "Copy" });
  return { title: `BiGH — ${translate(copyKeys["About"])}`, robots: { index: false } };
}

export default async function Page({ params }: { params: Params }) {
  const { locale } = await params;
  if (locale === "hken") redirect({ href: "/about-below", locale: "cns" });
  setRequestLocale(locale);

  return (
    <ProductPagesProvider pages={productPageLinks()}>
      <SiteDialogs>
        <AboutInk circle="below" />
        <BeforeHydration code={LET_THE_CIRCLE_GO} />
      </SiteDialogs>
    </ProductPagesProvider>
  );
}

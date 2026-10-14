import type { Metadata } from "next";
import { Ysabeau } from "next/font/google";
import { getTranslations, setRequestLocale } from "next-intl/server";
import { ProductPagesProvider } from "@/components/home/product-action";
import { SiteDialogs } from "@/components/ink/dialogs";
import { productPageLinks } from "@/components/product/catalog";
import { ScienceInk } from "@/components/science/ink/science-ink";
import copyKeys from "@/i18n/copy-keys.json";
import { redirect } from "@/i18n/navigation";

// Ysabeau, the homepage's title face (Mo, October 13, 2026), here for the Science page's titles as
// the other pages follow the homepage. Not preloaded, as on the homepage ([locale]/page.tsx).
const titles = Ysabeau({
  subsets: ["latin", "vietnamese"],
  variable: "--font-ysabeau",
  display: "swap",
  preload: false,
});

type Params = Promise<{ locale: string }>;

export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const { locale } = await params;
  const translate = await getTranslations({ locale, namespace: "Copy" });
  return { title: `BiGH — ${translate(copyKeys["Science"])}` };
}

// The Science page in Ink & Gold, "the handscroll" (Mo, October 13-14, 2026; spec
// docs/superpowers/specs/2026-10-14-science-ink-design.md). /hken goes to Chinese: a [locale]
// page without this redirect fails the build's static render.
export default async function Page({ params }: { params: Params }) {
  const { locale } = await params;
  if (locale === "hken") redirect({ href: "/science", locale: "cns" });
  setRequestLocale(locale);

  return (
    <ProductPagesProvider pages={productPageLinks()}>
      <SiteDialogs>
        <ScienceInk fontClass={titles.variable} />
      </SiteDialogs>
    </ProductPagesProvider>
  );
}

import { Ysabeau } from "next/font/google";
import type { Metadata } from "next";
import { getTranslations, setRequestLocale } from "next-intl/server";
import { ProductPagesProvider } from "@/components/home/product-action";
import { SiteDialogs } from "@/components/ink/dialogs";
import { productPageLinks } from "@/components/product/catalog";
import { SupportInk } from "@/components/support/support-ink";
import copyKeys from "@/i18n/copy-keys.json";
import { redirect } from "@/i18n/navigation";

type Params = Promise<{ locale: string }>;

// Ysabeau, the homepage's title face (src/app/[locale]/page.tsx): not preloaded, so the build does
// not hoist its preload onto every page.
const titles = Ysabeau({
  subsets: ["latin", "vietnamese"],
  variable: "--font-ysabeau",
  display: "swap",
  preload: false,
});

// "BiGH — Support", with "Support" from the catalogs (the menu's own word for this page).
export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const { locale } = await params;
  const translate = await getTranslations({ locale, namespace: "Copy" });
  return { title: `BiGH — ${translate(copyKeys["Support"])}` };
}

// The Support page in the Ink & Gold look (Mo, October 14, 2026), on the shared kit and sheets.
// /hken goes to Chinese, as on every page.
export default async function Page({ params }: { params: Params }) {
  const { locale } = await params;
  if (locale === "hken") redirect({ href: "/support", locale: "cns" });
  setRequestLocale(locale);

  return (
    <ProductPagesProvider pages={productPageLinks()}>
      <SiteDialogs>
        <SupportInk titleFont={titles.variable} />
      </SiteDialogs>
    </ProductPagesProvider>
  );
}

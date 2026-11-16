import type { Metadata } from "next";
import { getTranslations, setRequestLocale } from "next-intl/server";
import { AboutInk } from "@/components/about/about-ink";
import { ProductPagesProvider } from "@/components/home/product-action";
import { SiteDialogs } from "@/components/ink/dialogs";
import { productPageLinks } from "@/components/product/catalog";
import copyKeys from "@/i18n/copy-keys.json";
import { redirect } from "@/i18n/navigation";
import { pageMetadata } from "@/lib/seo";

type Params = Promise<{ locale: string }>;

// "BiGH — About", with "About" from the catalogs (the header's own word for this page).
export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const { locale } = await params;
  const translate = await getTranslations({ locale, namespace: "Copy" });
  return pageMetadata({
    locale,
    path: "/about",
    title:
      locale === "en"
        ? "About BiGH — Be in Good Health, made in California"
        : `${translate(copyKeys["About"])} — BiGH`,
    description:
      locale === "en"
        ? "Be in Good Health: why BiGH focuses on your cells, where our ingredients grow, and what you can count on. Made in California, with 45 days to decide."
        : translate("m169"),
    image: { url: "/og/about-v1.jpg", width: 1200, height: 630, alt: "About BiGH" },
  });
}

// The About page in the Ink & Gold look (October 5, 2026), on the shared kit and sheets.
// Switzer, the site's type, loads in the locale layout. /hken goes to Chinese, as on the homepage
// and the product pages.
export default async function Page({ params }: { params: Params }) {
  const { locale } = await params;
  if (locale === "hken") redirect({ href: "/about", locale: "cns" });
  setRequestLocale(locale);

  return (
    <ProductPagesProvider pages={productPageLinks()}>
      <SiteDialogs>
        <AboutInk />
      </SiteDialogs>
    </ProductPagesProvider>
  );
}

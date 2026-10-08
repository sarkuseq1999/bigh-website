import type { Metadata } from "next";
import { getTranslations, setRequestLocale } from "next-intl/server";
import { AboutAlbum } from "@/components/about/album-page";
import { ProductPagesProvider } from "@/components/home/product-action";
import { SiteDialogs } from "@/components/ink/dialogs";
import { productPageLinks } from "@/components/product/catalog";
import copyKeys from "@/i18n/copy-keys.json";
import { redirect } from "@/i18n/navigation";

type Params = Promise<{ locale: string }>;

export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const { locale } = await params;
  const translate = await getTranslations({ locale, namespace: "Copy" });
  return { title: `BiGH — ${translate(copyKeys["About"])}`, robots: { index: false } };
}

// Preview only (branch about-compare, October 8, 2026): About B, "The album", beside About C at
// /about, so Mo can compare both designs from one share link. The album's own code is on about-b.
export default async function Page({ params }: { params: Params }) {
  const { locale } = await params;
  if (locale === "hken") redirect({ href: "/about-album", locale: "cns" });
  setRequestLocale(locale);

  return (
    <ProductPagesProvider pages={productPageLinks()}>
      <SiteDialogs>
        <AboutAlbum />
      </SiteDialogs>
    </ProductPagesProvider>
  );
}

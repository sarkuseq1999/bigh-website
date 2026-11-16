import { Ysabeau } from "next/font/google";
import type { Metadata } from "next";
import { setRequestLocale } from "next-intl/server";
import { ProductPagesProvider } from "@/components/home/product-action";
import { SiteDialogs } from "@/components/ink/dialogs";
import { productPageLinks } from "@/components/product/catalog";
import { redirect } from "@/i18n/navigation";
import { pageMetadata } from "@/lib/seo";
import { legalDocs, type LegalDoc } from "./legal-content";
import { LegalPage } from "./legal-page";

// The Privacy, Terms and Returns routes share this: their metadata and the page, inside the
// dialogs and product links the shared footer needs. /hken goes to Chinese, as on every page.

const titles = Ysabeau({
  subsets: ["latin", "vietnamese"],
  variable: "--font-ysabeau",
  display: "swap",
  preload: false,
});

type Params = Promise<{ locale: string }>;

export async function legalMetadata(params: Params, slug: LegalDoc["slug"]): Promise<Metadata> {
  const { locale } = await params;
  const doc = legalDocs[slug];
  return pageMetadata({
    locale,
    path: `/${slug}`,
    title: `${doc.title} — BiGH`,
    description: doc.description,
  });
}

export async function LegalRoute({ params, slug }: { params: Params; slug: LegalDoc["slug"] }) {
  const { locale } = await params;
  if (locale === "hken") redirect({ href: `/${slug}`, locale: "cns" });
  setRequestLocale(locale);
  return (
    <ProductPagesProvider pages={productPageLinks()}>
      <SiteDialogs>
        <LegalPage slug={slug} titleFont={titles.variable} />
      </SiteDialogs>
    </ProductPagesProvider>
  );
}

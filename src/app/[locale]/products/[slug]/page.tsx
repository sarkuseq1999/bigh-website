import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { setRequestLocale } from "next-intl/server";
import { ProductPagesProvider } from "@/components/home/product-action";
import { SiteDialogs } from "@/components/ink/dialogs";
import { getProduct, productPageLinks, productSlugs } from "@/components/product/catalog";
import { ProductInkPage } from "@/components/product/ink/product-ink";
import { ProductPageView } from "@/components/product/product-page";
import { redirect } from "@/i18n/navigation";

type Params = Promise<{ locale: string; slug: string }>;

export const dynamicParams = false;

export function generateStaticParams() {
  return productSlugs.map((slug) => ({ slug }));
}

export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const { slug } = await params;
  const product = getProduct(slug);
  return {
    title: product ? `${product.name} — BiGH` : "BiGH",
    robots: { index: false, follow: false },
  };
}

export default async function ProductRoute({ params }: { params: Params }) {
  const { locale, slug } = await params;
  if (locale === "hken") redirect({ href: `/products/${slug}`, locale: "cns" });
  setRequestLocale(locale);
  const product = getProduct(slug);
  if (!product) notFound();

  if (product.ink) {
    // The ink page (October 9, 2026): the shared header's sheets and the product links need the
    // same providers as About.
    return (
      <ProductPagesProvider pages={productPageLinks()}>
        <SiteDialogs>
          <ProductInkPage product={{ ...product, ink: product.ink }} />
        </SiteDialogs>
      </ProductPagesProvider>
    );
  }
  return <ProductPageView product={product} />;
}

import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { setRequestLocale } from "next-intl/server";
import { getProduct, productSlugs } from "@/components/product/catalog";
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

  return <ProductPageView product={product} />;
}

import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { setRequestLocale } from "next-intl/server";
import { getProduct, productPageLinks, productSlugs } from "@/components/product/catalog";
import { ProductTemplate } from "@/components/product/product-template";
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

  // One template per page, each in its own chunks (product-template.tsx). The ink page's header
  // sheets and product links need the product pages, as About's do.
  return <ProductTemplate product={product} pages={product.ink ? productPageLinks() : undefined} />;
}

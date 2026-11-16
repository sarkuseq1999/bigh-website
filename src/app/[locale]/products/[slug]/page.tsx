import type { Metadata } from "next";
import { Ysabeau } from "next/font/google";
import { notFound } from "next/navigation";
import { getTranslations, setRequestLocale } from "next-intl/server";
import { getProduct, productPageLinks, productSlugs } from "@/components/product/catalog";
import { ProductTemplate } from "@/components/product/product-template";
import copyKeys from "@/i18n/copy-keys.json";
import { redirect } from "@/i18n/navigation";
import { JsonLd, productLd } from "@/lib/json-ld";
import { pageMetadata } from "@/lib/seo";
import { priceOf } from "@/components/shop/shop";

type Params = Promise<{ locale: string; slug: string }>;

// The Propolis editorial uses the same title face as the homepage and Science.
// No preload: other product pages do not request a font they do not use.
const propolisTitles = Ysabeau({
  subsets: ["latin", "vietnamese"],
  variable: "--font-ysabeau",
  display: "swap",
  preload: false,
});

export const dynamicParams = false;

export function generateStaticParams() {
  return productSlugs.map((slug) => ({ slug }));
}

export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const { locale, slug } = await params;
  const product = getProduct(slug);
  if (!product) return { title: "BiGH" };
  // The product's own purpose line (its opening's lead) describes it in search and link previews.
  const translate = await getTranslations({ locale, namespace: "Copy" });
  const key = (copyKeys as Record<string, string>)[product.purpose];
  return pageMetadata({
    locale,
    path: `/products/${slug}`,
    title: locale === "en" ? `${product.name}: ${product.focus} — BiGH` : `${product.name} — BiGH`,
    description: key ? translate(key) : product.purpose,
    image: { url: `/og/${slug}-v1.jpg`, width: 1200, height: 630, alt: product.name },
  });
}

export default async function ProductRoute({ params }: { params: Params }) {
  const { locale, slug } = await params;
  if (locale === "hken") redirect({ href: `/products/${slug}`, locale: "cns" });
  setRequestLocale(locale);
  const product = getProduct(slug);
  if (!product) notFound();

  // One template per page, each in its own chunks (product-template.tsx). The ink page's header
  // sheets and product links need the product pages, as About's do.
  const page = (
    <>
      <JsonLd
        data={productLd({
          name: product.name,
          description: product.purpose,
          image: product.bottle.src,
          path: `/products/${slug}`,
          price: priceOf(slug),
        })}
      />
      <ProductTemplate product={product} pages={product.ink ? productPageLinks() : undefined} />
    </>
  );
  return slug === "green-bee-propolis" ? (
    <div className={propolisTitles.variable}>{page}</div>
  ) : (
    page
  );
}

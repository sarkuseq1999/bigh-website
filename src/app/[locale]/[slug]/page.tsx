import type { Metadata } from "next";
import Image from "next/image";
import { notFound } from "next/navigation";
import { setRequestLocale, getTranslations } from "next-intl/server";

import { Reveal } from "@/components/clone/reveal";
import { Link } from "@/i18n/navigation";
import { routing, type Locale } from "@/i18n/routing";
import { isProductSlug, productName } from "@/data/products";
import {
  buyLink,
  listSlugs,
  loadPage,
  localesWithSlug,
  mdToHtml,
  pageHeading,
  productImages,
} from "@/lib/content";
import { imageDims } from "@/lib/images";

export function generateStaticParams() {
  return routing.locales.flatMap((locale) =>
    listSlugs(locale).map((slug) => ({ locale, slug })),
  );
}

function pageUrl(locale: Locale, slug: string): string {
  return locale === "en" ? `/${slug}` : `/${locale}/${slug}`;
}

function displayTitle(locale: Locale, slug: string): string {
  if (isProductSlug(slug)) return productName(slug, locale);
  const page = loadPage(locale, slug);
  const heading = page ? pageHeading(page) : null;
  if (heading && heading.length <= 80) return heading;
  return slug
    .split("-")
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ");
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string; slug: string }>;
}): Promise<Metadata> {
  const { locale: raw, slug } = await params;
  const locale = raw as Locale;
  const page = loadPage(locale, slug);
  if (!page) return {};

  const languages: Record<string, string> = {};
  for (const loc of localesWithSlug(slug)) {
    languages[loc === "en" ? "en" : loc === "kr" ? "ko" : loc === "jp" ? "ja" : loc === "cns" ? "zh-Hans" : loc === "hken" ? "zh-Hant-HK" : "vi"] =
      `https://www.bighnow.com${pageUrl(loc, slug)}`;
  }

  return {
    title: displayTitle(locale, slug),
    description: page.front.description || undefined,
    alternates: {
      canonical: `https://www.bighnow.com${pageUrl(locale, slug)}`,
      languages,
    },
  };
}

export default async function ClonePage({
  params,
}: {
  params: Promise<{ locale: string; slug: string }>;
}) {
  const { locale: raw, slug } = await params;
  const locale = raw as Locale;
  setRequestLocale(locale);

  const page = loadPage(locale, slug);
  if (!page) notFound();

  const title = displayTitle(locale, slug);

  if (isProductSlug(slug)) {
    const t = await getTranslations({ locale, namespace: "Product" });
    const images = productImages(page);
    const buy = buyLink(page);

    return (
      <article className="mx-auto max-w-4xl px-4 py-12 sm:px-6">
        <nav className="font-mono text-xs uppercase tracking-[0.25em] text-celadon-deep">
          <Link href="/#products" className="hover:text-amber">
            {t("allProducts")}
          </Link>
        </nav>
        <div className="mt-4 flex flex-wrap items-end justify-between gap-4 border-b border-line pb-8">
          <h1 className="font-display text-4xl text-pine md:text-5xl">{title}</h1>
          {buy && (
            <a
              href={buy}
              className="rounded-full bg-amber px-7 py-2.5 font-medium text-white shadow-[0_8px_24px_rgba(185,127,46,0.35)] transition-colors hover:bg-amber-hi"
            >
              {t("buyNow")}
            </a>
          )}
        </div>

        <div className="mt-10 space-y-8">
          {images.map((src, i) => (
            <Reveal key={src}>
              <Image
                src={src}
                alt={`${title} — ${i + 1}`}
                {...imageDims(src)}
                className="mx-auto h-auto w-full max-w-3xl rounded-2xl border border-line bg-white shadow-[0_10px_36px_rgba(23,52,43,0.08)]"
                sizes="(max-width: 768px) 95vw, 768px"
                priority={i === 0}
              />
            </Reveal>
          ))}
        </div>

        {buy && (
          <div className="mt-12 text-center">
            <a
              href={buy}
              className="inline-block rounded-full bg-amber px-10 py-3 text-lg font-medium text-white shadow-[0_8px_24px_rgba(185,127,46,0.35)] transition-colors hover:bg-amber-hi"
            >
              {t("buyNow")}
            </a>
          </div>
        )}
      </article>
    );
  }

  // generic harvested page (about, science, legal, badges, …)
  // drop the first heading when it's already rendered as the <h1>
  const heading = pageHeading(page);
  const markdown =
    heading === title
      ? page.markdown.replace(/^#{1,3}\s+.+$/m, "").trim()
      : page.markdown;
  const html = mdToHtml(markdown);

  return (
    <article className="mx-auto max-w-4xl px-4 py-12 sm:px-6">
      <h1 className="font-display max-w-2xl text-4xl leading-tight text-pine md:text-5xl">
        {title}
      </h1>
      <div
        className="prose-clone mt-8"
        // our own harvested, spam-stripped content — no third-party input
        dangerouslySetInnerHTML={{ __html: html }}
      />
    </article>
  );
}

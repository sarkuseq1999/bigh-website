import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { setRequestLocale, getTranslations } from "next-intl/server";

import { ProductGallery } from "@/components/clone/product-gallery";
import { Reveal } from "@/components/clone/reveal";
import { routing, type Locale } from "@/i18n/routing";
import { isProductSlug, productName, PRODUCT_HUES, type ProductSlug } from "@/data/products";
import {
  buyLink,
  listSlugs,
  loadPage,
  localesWithSlug,
  mdToHtml,
  pageHeading,
  parseProduct,
  productImages,
  type HarvestPage,
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

function ProductPage({
  page,
  slug,
  locale,
  buyLabel,
}: {
  page: HarvestPage;
  slug: ProductSlug;
  locale: Locale;
  buyLabel: string;
}) {
  const title = productName(slug, locale);
  const hue = PRODUCT_HUES[slug];
  const content = parseProduct(page);
  const gallery = productImages(page).map((src) => ({ src, ...imageDims(src) }));
  const buy = buyLink(page);

  return (
    <article>
      {/* wave hero in the product's label color, like the original */}
      <section
        className="relative overflow-hidden text-white"
        style={{
          background: `
            radial-gradient(90rem 42rem at 115% -18%, color-mix(in srgb, ${hue} 55%, white) 0%, transparent 55%),
            radial-gradient(70rem 36rem at -20% 118%, color-mix(in srgb, ${hue} 60%, #1c2340) 0%, transparent 60%),
            linear-gradient(155deg, color-mix(in srgb, ${hue} 82%, #10315c) 0%, ${hue} 48%, color-mix(in srgb, ${hue} 60%, white) 100%)`,
        }}
      >
        <div className="mx-auto grid max-w-6xl items-center gap-10 px-4 pb-24 pt-12 sm:px-6 md:grid-cols-[1fr_1.1fr]">
          <Reveal>
            <ProductGallery images={gallery} alt={title} />
          </Reveal>
          <Reveal delay={100}>
            <h1 className="text-4xl font-bold text-white md:text-5xl">{title}</h1>
            {content.intro.map((p) => (
              <p key={p.slice(0, 24)} className="mt-5 max-w-xl leading-relaxed text-white/95">
                {p}
              </p>
            ))}
            {content.factsLinks.length > 0 && (
              <div className="mt-7 flex flex-wrap gap-3">
                {content.factsLinks.map((f) => (
                  <a
                    key={f.href}
                    href={f.href}
                    target="_blank"
                    rel="noopener"
                    className="rounded border border-white/80 px-4 py-2 text-sm font-semibold text-white transition-colors hover:bg-white hover:text-heading"
                  >
                    {f.label}
                  </a>
                ))}
              </div>
            )}
            <div className="mt-8 flex flex-wrap items-center gap-5">
              {content.price && <p className="text-3xl font-bold text-white">{content.price}</p>}
              {buy && (
                <a
                  href={buy}
                  className="rounded bg-[#f2762e] px-8 py-3 text-lg font-bold text-white shadow-[0_8px_24px_rgba(0,0,0,0.3)] transition-transform hover:scale-[1.03]"
                >
                  {buyLabel}
                </a>
              )}
            </div>
          </Reveal>
        </div>
        {/* bottom white wave */}
        <svg
          aria-hidden
          className="absolute bottom-0 left-0 h-14 w-full text-white md:h-20"
          viewBox="0 0 1440 96"
          preserveAspectRatio="none"
        >
          <path
            fill="currentColor"
            d="M0,64 C240,96 480,16 720,32 C960,48 1200,96 1440,48 L1440,96 L0,96 Z"
          />
        </svg>
      </section>

      {/* parsed content sections (Key Ingredients cards, Synergistic Effects, …) */}
      <div className="mx-auto max-w-6xl px-4 pb-16 sm:px-6">
        {content.sections.map((sec) => (
          <section key={sec.title || sec.paragraphs[0]} className="mt-14">
            {sec.title && <h2 className="text-center text-3xl font-bold">{sec.title}</h2>}
            {sec.paragraphs.map((p) => (
              <p key={p.slice(0, 24)} className="mx-auto mt-5 max-w-3xl text-center">
                {p}
              </p>
            ))}
            {sec.cards.length > 0 && (
              <ul
                className={`mx-auto mt-10 grid max-w-5xl gap-5 sm:grid-cols-2 ${
                  sec.cards.length >= 4 ? "lg:grid-cols-4" : "lg:grid-cols-3"
                }`}
              >
                {sec.cards.map((c) => (
                  <li key={c.title} className="rounded-xl bg-muted px-5 py-6 text-center">
                    <h3 className="text-lg font-bold">{c.title}</h3>
                    <p className="mt-3 text-sm leading-relaxed">{c.text}</p>
                  </li>
                ))}
              </ul>
            )}
          </section>
        ))}

        {buy && (
          <div className="mt-16 text-center">
            <a
              href={buy}
              className="inline-block rounded bg-[#f2762e] px-10 py-3 text-lg font-bold text-white shadow-[0_8px_24px_rgba(0,0,0,0.2)] transition-transform hover:scale-[1.03]"
            >
              {buyLabel}
            </a>
          </div>
        )}
      </div>
    </article>
  );
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

  if (isProductSlug(slug)) {
    const t = await getTranslations({ locale, namespace: "Product" });
    return <ProductPage page={page} slug={slug} locale={locale} buyLabel={t("buyNow")} />;
  }

  // generic harvested page (about, science, legal, badges, …)
  const title = displayTitle(locale, slug);
  const heading = pageHeading(page);
  const markdown =
    heading === title
      ? page.markdown.replace(/^#{1,3}\s+.+$/m, "").trim()
      : page.markdown;
  const html = mdToHtml(markdown);

  return (
    <article className="mx-auto max-w-4xl px-4 py-12 sm:px-6">
      <h1 className="max-w-2xl text-4xl font-bold leading-tight md:text-5xl">{title}</h1>
      <div
        className="prose-clone mt-8"
        // our own harvested, spam-stripped content — no third-party input
        dangerouslySetInnerHTML={{ __html: html }}
      />
    </article>
  );
}

import type { Metadata } from "next";
import Image from "next/image";
import { notFound } from "next/navigation";
import { setRequestLocale } from "next-intl/server";

import { ProductGallery } from "@/components/clone/product-gallery";
import { Reveal } from "@/components/clone/reveal";
import { routing, type Locale } from "@/i18n/routing";
import { isProductSlug, productName, type ProductSlug } from "@/data/products";
import productLayout from "@/data/product-layout.json";
import {
  listSlugs,
  loadPage,
  localesWithSlug,
  mdToHtml,
  pageHeading,
  parseProduct,
  type HarvestPage,
} from "@/lib/content";
import { imageDims } from "@/lib/images";

const LAYOUT = productLayout as Record<
  string,
  { heroBg: string | null; bandBg: string | null; gallery: string[] }
>;

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
}: {
  page: HarvestPage;
  slug: ProductSlug;
  locale: Locale;
}) {
  const title = productName(slug, locale);
  const layout = LAYOUT[slug];
  const content = parseProduct(page);
  const gallery = layout.gallery.map((src) => ({ src, ...imageDims(src) }));

  // the original renders "Key Ingredients"-style card sections on white and
  // the remaining prose sections on the second themed band
  const cardSections = content.sections.filter((s) => s.cards.length > 0);
  const proseSections = content.sections.filter((s) => s.cards.length === 0);

  return (
    <article>
      {/* hero — the product's own background artwork, measured layout */}
      <section className="relative text-white">
        <div className="absolute inset-0 overflow-hidden">
          {layout.heroBg && (
            <Image src={layout.heroBg} alt="" fill priority className="object-cover object-top" sizes="100vw" />
          )}
        </div>
        <div className="relative mx-auto grid max-w-6xl gap-8 px-4 pb-28 pt-8 sm:px-6 md:grid-cols-[46%_54%] md:pb-36">
          <Reveal>
            <ProductGallery images={gallery} alt={title} />
          </Reveal>
          <Reveal delay={100} className="md:pt-10">
            <h1 className="text-4xl font-semibold text-white md:text-5xl">{title}</h1>
            {content.intro.map((p) => (
              <p key={p.slice(0, 24)} className="mt-5 max-w-xl text-justify font-medium leading-relaxed text-white">
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
                    className="rounded border border-white px-4 py-2.5 text-sm font-medium leading-none text-white transition-colors hover:bg-white hover:text-heading"
                  >
                    {f.label}
                  </a>
                ))}
              </div>
            )}
          </Reveal>
        </div>
        {/* the original's white wave divider image */}
        <Image
          src="/original/uploads/2019/04/nano_shapedivider7-1024x128.png"
          alt=""
          width={1024}
          height={128}
          unoptimized
          className="absolute bottom-0 left-0 h-auto w-full"
          sizes="100vw"
        />
      </section>

      {/* white content: ingredient card sections */}
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        {cardSections.map((sec) => (
          <section key={sec.title} className="mt-12">
            {sec.title && (
              <h2 className="text-center text-[clamp(1.9rem,3.3vw,3rem)] font-semibold">{sec.title}</h2>
            )}
            {sec.paragraphs.map((p) => (
              <p key={p.slice(0, 24)} className="mx-auto mt-4 max-w-3xl text-center">
                {p}
              </p>
            ))}
            <ul
              className={`mx-auto mt-9 grid max-w-5xl gap-5 sm:grid-cols-2 ${
                sec.cards.length >= 4 ? "lg:grid-cols-4" : "lg:grid-cols-3"
              }`}
            >
              {sec.cards.map((c) => (
                <li key={c.title} className="rounded-xl bg-[#f2f2f4] px-5 py-6 text-center">
                  <h3 className="text-lg font-semibold">{c.title}</h3>
                  <p className="mt-3 text-sm leading-relaxed">{c.text}</p>
                </li>
              ))}
            </ul>
            {sec.images.map((src) => (
              <Image
                key={src}
                src={src}
                alt=""
                {...imageDims(src)}
                className="mx-auto mt-10 h-auto w-full max-w-3xl"
                sizes="(max-width: 768px) 95vw, 768px"
              />
            ))}
          </section>
        ))}
      </div>

      {/* themed band: remaining prose sections over the product's band art */}
      {proseSections.length > 0 && (
        <section className="relative mt-14 overflow-hidden">
          {layout.bandBg && (
            <Image src={layout.bandBg} alt="" fill className="object-cover" sizes="100vw" />
          )}
          <div className="relative mx-auto grid max-w-6xl items-center gap-8 px-4 py-16 sm:px-6 md:grid-cols-2">
            {proseSections.map((sec, i) => (
              <Reveal key={sec.title || i} delay={i * 80}>
                {sec.paragraphs.length > 0 || sec.images.length > 0 ? (
                  <div className={layout.bandBg ? "rounded-xl bg-white/75 px-6 py-7 backdrop-blur-sm" : ""}>
                    {sec.title && (
                      <h2 className="text-center text-2xl font-semibold text-heading">{sec.title}</h2>
                    )}
                    {sec.paragraphs.map((p) => (
                      <p key={p.slice(0, 24)} className="mt-4 text-center text-[15px] leading-relaxed">
                        {p}
                      </p>
                    ))}
                    {sec.images.map((src) => (
                      <Image
                        key={src}
                        src={src}
                        alt=""
                        {...imageDims(src)}
                        className="mx-auto mt-6 h-auto w-full max-w-xl"
                        sizes="(max-width: 768px) 90vw, 560px"
                      />
                    ))}
                  </div>
                ) : (
                  <h2
                    className={`text-center text-[clamp(2rem,3.6vw,3.2rem)] font-semibold ${
                      layout.bandBg ? "text-heading" : ""
                    }`}
                  >
                    {sec.title}
                  </h2>
                )}
              </Reveal>
            ))}
          </div>
        </section>
      )}
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
    return <ProductPage page={page} slug={slug} locale={locale} />;
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
      <h1 className="max-w-2xl text-4xl font-semibold leading-tight md:text-5xl">{title}</h1>
      <div
        className="prose-clone mt-8"
        // our own harvested, spam-stripped content — no third-party input
        dangerouslySetInnerHTML={{ __html: html }}
      />
    </article>
  );
}

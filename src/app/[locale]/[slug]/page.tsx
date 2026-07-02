import type { Metadata } from "next";
import Image from "next/image";
import { notFound } from "next/navigation";
import { setRequestLocale } from "next-intl/server";

import { getTranslations } from "next-intl/server";

import { ProductGallery } from "@/components/clone/product-gallery";
import { Reveal } from "@/components/clone/reveal";
import { ScrollDrift } from "@/components/clone/scroll-drift";
import { SupportForm } from "@/components/clone/support-form";
import { routing, type Locale } from "@/i18n/routing";
import { isProductSlug, productName, type ProductSlug } from "@/data/products";
import { PAGE_BANNERS } from "@/data/page-banners";
import productDecor from "@/data/product-decor.json";
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
  {
    heroBg: string | null;
    bandBg: string | null;
    gallery: string[];
    divider: string;
    darkText: boolean;
  }
>;

interface DecorItem {
  img: string;
  x: number;
  y: number;
  w: number;
  h: number;
  yRel?: number;
}
const DECOR = productDecor as Record<
  string,
  { heroH: number; hero: DecorItem[]; body: DecorItem[] }
>;

function decorBase(p: string): string {
  return p.split("/").pop()!.replace(/-\d+x\d+(?=\.)/, "");
}

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
  const decor = DECOR[slug] ?? { heroH: 1150, hero: [], body: [] };
  const content = parseProduct(page);
  const gallery = layout.gallery.map((src) => ({ src, ...imageDims(src) }));

  // the original renders "Key Ingredients"-style card sections on white and
  // the remaining prose sections on the second themed band
  const cardSections = content.sections.filter((s) => s.cards.length > 0);
  const proseSections = content.sections.filter((s) => s.cards.length === 0);

  // only substantial images render as section content (e.g. the Reishi photo);
  // small ones are decorative floaters handled by the decor map
  const contentImages = (imgs: string[]) => imgs.filter((im) => imageDims(im).width >= 500);

  // decorations already shown as card icons or section images must not repeat
  const usedBases = new Set<string>();
  for (const s of content.sections) {
    for (const c of s.cards) if (c.icon) usedBases.add(decorBase(c.icon));
    for (const im of contentImages(s.images)) usedBases.add(decorBase(im));
  }
  const heroDecor = decor.hero.filter(
    (d) => !usedBases.has(decorBase(d.img)) && !/dividershape/i.test(d.img),
  );
  const bodyDecor = decor.body.filter((d) => !usedBases.has(decorBase(d.img)));

  return (
    <article>
      {/* hero — the product's own background artwork, measured layout */}
      <section className="relative text-white">
        <div className="absolute inset-0 overflow-hidden">
          {layout.heroBg && (
            <Image src={layout.heroBg} alt="" fill priority className="object-cover object-top" sizes="100vw" />
          )}
        </div>
        {/* measured floating decorations with light scroll drift */}
        {heroDecor.map((d, i) => (
          <div
            key={d.img}
            aria-hidden
            className="pointer-events-none absolute hidden md:block"
            style={{
              left: `${((d.x / 1440) * 100).toFixed(2)}%`,
              top: `${((d.y / decor.heroH) * 100).toFixed(2)}%`,
              width: `${((d.w / 1440) * 100).toFixed(2)}%`,
            }}
          >
            <ScrollDrift speed={i % 2 === 0 ? 0.07 : -0.05}>
              <Image src={d.img} alt="" {...imageDims(d.img)} className="h-auto w-full" sizes="30vw" />
            </ScrollDrift>
          </div>
        ))}
        <div className="relative mx-auto grid max-w-[70rem] gap-8 px-4 pb-24 pt-[10.3rem] sm:px-6 md:grid-cols-[550px_1fr] md:pb-[18rem]">
          <Reveal>
            <ProductGallery images={gallery} alt={title} dark={layout.darkText} />
          </Reveal>
          <Reveal delay={100} className="md:pt-2">
            <h1
              className={`text-4xl font-semibold md:text-[3.05rem] md:leading-tight ${
                layout.darkText ? "text-black/65" : "text-white"
              }`}
            >
              {title}
            </h1>
            {content.intro.map((p) => (
              <p
                key={p.slice(0, 24)}
                className={`mt-5 max-w-xl text-justify font-medium leading-relaxed ${
                  layout.darkText ? "text-black/70" : "text-white"
                }`}
              >
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
                    className={`rounded border px-4 py-2.5 text-sm font-medium leading-none transition-colors ${
                      layout.darkText
                        ? "border-black/50 text-black/70 hover:bg-black/70 hover:text-white"
                        : "border-white text-white hover:bg-white hover:text-heading"
                    }`}
                  >
                    {f.label}
                  </a>
                ))}
              </div>
            )}
          </Reveal>
        </div>
        {/* the product's own white wave divider image */}
        <Image
          src={layout.divider}
          alt=""
          {...imageDims(layout.divider)}
          unoptimized
          className="absolute bottom-0 left-0 h-auto w-full"
          sizes="100vw"
        />
      </section>

      {/* white content: ingredient card sections (+ measured floaters) */}
      <div className="relative mx-auto max-w-[90rem]">
        {bodyDecor.map((d, i) => (
          <div
            key={d.img}
            aria-hidden
            className="pointer-events-none absolute z-0 hidden lg:block"
            style={{
              left: `${((d.x / 1440) * 100).toFixed(2)}%`,
              top: `${d.yRel ?? 0}px`,
              width: `${((d.w / 1440) * 100).toFixed(2)}%`,
            }}
          >
            <ScrollDrift speed={i % 2 === 0 ? -0.06 : 0.08}>
              <Image src={d.img} alt="" {...imageDims(d.img)} className="h-auto w-full" sizes="20vw" />
            </ScrollDrift>
          </div>
        ))}
      <div className="relative z-10 mx-auto max-w-[70rem] px-4 pt-[3.3rem] sm:px-6">
        {cardSections.map((sec) => (
          <section key={sec.title}>
            {sec.title && (
              <h2 className="text-center text-[clamp(1.9rem,3.3vw,3.75rem)] font-semibold">{sec.title}</h2>
            )}
            {sec.paragraphs.map((p) => (
              <p key={p.slice(0, 24)} className="mx-auto mt-4 max-w-3xl text-center">
                {p}
              </p>
            ))}
            <ul
              className={`mx-auto mt-20 grid gap-x-9 gap-y-8 sm:grid-cols-2 ${
                sec.cards.length >= 4 ? "lg:grid-cols-4" : "lg:grid-cols-3"
              }`}
            >
              {sec.cards.map((c) => (
                <li key={c.title} className="rounded-lg bg-[#f6f6f7] px-5 py-6 text-center">
                  {c.icon && (
                    <Image
                      src={c.icon}
                      alt=""
                      {...imageDims(c.icon)}
                      className="mx-auto mb-4 h-24 w-auto object-contain"
                      sizes="130px"
                    />
                  )}
                  <h3 className="text-xl font-semibold">{c.title}</h3>
                  <p className="mt-3 text-sm leading-relaxed">{c.text}</p>
                </li>
              ))}
            </ul>
            {contentImages(sec.images).map((src) => (
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
      </div>

      {/* themed band: remaining prose sections over the product's band art */}
      {proseSections.length > 0 && (
        <section className="relative mt-14 overflow-hidden">
          {layout.bandBg && (
            <Image src={layout.bandBg} alt="" fill className="object-cover" sizes="100vw" />
          )}
          <div className="relative mx-auto grid min-h-[37.5rem] max-w-[70rem] items-center gap-8 px-4 py-16 sm:px-6 md:grid-cols-2">
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
                    {contentImages(sec.images).map((src) => (
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
  let markdown =
    heading === title
      ? page.markdown.replace(/^#{1,3}\s+.+$/m, "").trim()
      : page.markdown;
  if (slug === "support") {
    // the legacy form serialized as a heading + bare label lines; the live
    // form component replaces it, so cut from that heading onward
    const lines = markdown.split("\n");
    for (let i = 0; i < lines.length; i++) {
      if (/^#{2,3}\s/.test(lines[i])) {
        const rest = lines.slice(i + 1).filter((l) => l.trim());
        if (rest.length >= 3 && rest.every((l) => l.trim().length < 60 && !/^#|!\[|\]\(/.test(l.trim()))) {
          markdown = lines.slice(0, i).join("\n");
          break;
        }
      }
    }
  }
  const html = mdToHtml(markdown);
  const banner = PAGE_BANNERS[slug];

  if (banner) {
    const t = slug === "support" ? await getTranslations({ locale, namespace: "Support" }) : null;
    return (
      <article>
        {/* full-bleed banner with centered white title, per the original */}
        <section
          className="relative flex items-center justify-center overflow-hidden"
          style={{ height: `min(62vw, ${banner.h}px)` }}
        >
          <Image src={banner.img} alt="" fill priority className="object-cover" sizes="100vw" />
          <div aria-hidden className="absolute inset-0 bg-black/20" />
          <h1 className="relative px-4 text-center text-[clamp(2.4rem,4.4vw,3.95rem)] font-semibold text-white/95">
            {title}
          </h1>
        </section>
        {html.trim() && (
          <div className="mx-auto max-w-4xl px-4 py-12 sm:px-6">
            <div
              className="prose-clone mx-auto"
              // our own harvested, spam-stripped content — no third-party input
              dangerouslySetInnerHTML={{ __html: html }}
            />
          </div>
        )}
        {t && (
          <SupportForm
            labels={{
              title: t("title"),
              name: t("name"),
              namePh: t("namePh"),
              customerId: t("customerId"),
              customerIdPh: t("customerIdPh"),
              email: t("email"),
              phone: t("phone"),
              phonePh: t("phonePh"),
              subject: t("subject"),
              subjectPh: t("subjectPh"),
              message: t("message"),
              send: t("send"),
              sent: t("sent"),
              failed: t("failed"),
            }}
          />
        )}
      </article>
    );
  }

  return (
    <article className="mx-auto max-w-4xl px-4 pb-12 pt-44 sm:px-6">
      <h1 className="max-w-2xl text-4xl font-semibold leading-tight text-black/75 md:text-[3.44rem]">
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

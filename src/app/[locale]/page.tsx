import Image from "next/image";
import { setRequestLocale, getTranslations } from "next-intl/server";

import { Hero } from "@/components/clone/hero";
import { Reveal } from "@/components/clone/reveal";
import { Link } from "@/i18n/navigation";
import { routing, type Locale } from "@/i18n/routing";
import { PRODUCT_SLUGS, productName, isProductSlug, type ProductSlug } from "@/data/products";
import { loadPage, productImages } from "@/lib/content";
import { imageDims } from "@/lib/images";

export function generateStaticParams() {
  return routing.locales.map((locale) => ({ locale }));
}

/** First brochure/pack image of a product in this locale (falls back to EN). */
function cardImage(locale: Locale, slug: ProductSlug): string | null {
  const page = loadPage(locale, slug) ?? loadPage("en", slug);
  if (!page) return null;
  return productImages(page)[0] ?? null;
}

export default async function HomePage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale: raw } = await params;
  const locale = raw as Locale;
  setRequestLocale(locale);
  const t = await getTranslations({ locale, namespace: "Home" });
  const nav = await getTranslations({ locale, namespace: "Nav" });

  const featuredSlug = t("featuredSlug");
  const featured: ProductSlug = isProductSlug(featuredSlug) ? featuredSlug : "deer-horn-reishi";
  const featuredImg = cardImage(locale, featured);

  const badges = [
    { slug: "organic", label: nav("organic") },
    { slug: "non-gmo", label: nav("nonGmo") },
    { slug: "gluten-free", label: nav("glutenFree") },
    { slug: "vegan", label: nav("vegan") },
  ];

  return (
    <>
      <Hero
        eyebrow={t("eyebrow")}
        brand={t("brand")}
        tagline={t("tagline")}
        learnMore={t("learnMore")}
        viewProducts={t("viewProducts")}
      />

      {/* Latest release */}
      <section className="bg-hanji">
        <div className="mx-auto grid max-w-6xl items-center gap-10 px-4 py-16 sm:px-6 md:grid-cols-2">
          <Reveal>
            <p className="font-mono text-sm uppercase tracking-[0.25em] text-amber">
              {t("latestEyebrow")}
            </p>
            <h2 className="font-display mt-3 text-4xl text-pine">
              {productName(featured, locale)}
            </h2>
            <p className="mt-4 max-w-md text-lg text-pine-soft">{t("featuredBlurb")}</p>
            <Link
              href={`/${featured}`}
              className="mt-7 inline-block rounded-full bg-pine px-6 py-2.5 font-medium text-porcelain transition-colors hover:bg-celadon-deep"
            >
              {t("learnMore")}
            </Link>
          </Reveal>
          {featuredImg && (
            <Reveal delay={120} className="mx-auto w-full max-w-sm">
              <Image
                src={featuredImg}
                alt={productName(featured, locale)}
                {...imageDims(featuredImg)}
                className="h-auto w-full drop-shadow-[0_24px_40px_rgba(23,52,43,0.18)]"
                sizes="(max-width: 768px) 90vw, 400px"
              />
            </Reveal>
          )}
        </div>
      </section>

      {/* Product shelf */}
      <section id="products" className="mx-auto max-w-6xl scroll-mt-20 px-4 py-16 sm:px-6">
        <Reveal>
          <p className="font-mono text-sm uppercase tracking-[0.25em] text-celadon-deep">
            {t("popular")}
          </p>
        </Reveal>
        <ul className="mt-8 grid grid-cols-2 gap-x-6 gap-y-10 sm:grid-cols-3 lg:grid-cols-5">
          {PRODUCT_SLUGS.map((slug, i) => {
            const img = cardImage(locale, slug);
            return (
              <li key={slug}>
                <Reveal delay={(i % 5) * 60}>
                  <Link href={`/${slug}`} className="group block">
                    <div className="flex aspect-[4/5] items-center justify-center overflow-hidden rounded-2xl border border-line bg-white p-4 transition-shadow group-hover:shadow-[0_16px_40px_rgba(23,52,43,0.12)]">
                      {img && (
                        <Image
                          src={img}
                          alt=""
                          {...imageDims(img)}
                          className="h-full w-auto object-contain transition-transform duration-500 group-hover:scale-[1.04]"
                          sizes="(max-width: 640px) 45vw, 220px"
                        />
                      )}
                    </div>
                    <p className="mt-3 text-center text-[15px] font-medium text-pine group-hover:text-celadon-deep">
                      {productName(slug, locale)}
                    </p>
                  </Link>
                </Reveal>
              </li>
            );
          })}
        </ul>
      </section>

      {/* Made in California */}
      <section className="bg-hanji">
        <div className="mx-auto grid max-w-6xl items-center gap-10 px-4 py-16 sm:px-6 md:grid-cols-2">
          <Reveal className="order-2 md:order-1">
            <Image
              src="/original/uploads/2019/04/madeincalifornia4-981x1024.jpg"
              alt={t("madeTitle")}
              {...imageDims("/original/uploads/2019/04/madeincalifornia4-981x1024.jpg")}
              className="mx-auto h-auto w-full max-w-sm rounded-2xl shadow-[0_16px_40px_rgba(23,52,43,0.14)]"
              sizes="(max-width: 768px) 90vw, 400px"
            />
          </Reveal>
          <Reveal delay={120} className="order-1 md:order-2">
            <p className="font-mono text-sm uppercase tracking-[0.25em] text-celadon-deep">
              GLENDORA · CALIFORNIA
            </p>
            <h2 className="font-display mt-3 text-4xl text-pine">{t("madeTitle")}</h2>
            <p className="mt-4 text-pine-soft">{t("madeBody")}</p>
          </Reveal>
        </div>
      </section>

      {/* Standards */}
      <section className="mx-auto max-w-6xl px-4 py-16 sm:px-6">
        <Reveal>
          <p className="font-mono text-sm uppercase tracking-[0.25em] text-celadon-deep">
            {t("standards")}
          </p>
        </Reveal>
        <ul className="mt-8 grid grid-cols-2 gap-4 md:grid-cols-4">
          {badges.map((b, i) => (
            <li key={b.slug}>
              <Reveal delay={i * 60}>
                <Link
                  href={`/${b.slug}`}
                  className="flex h-full items-center justify-center rounded-2xl border border-line bg-porcelain px-4 py-6 text-center font-medium text-pine transition-colors hover:border-celadon hover:text-celadon-deep"
                >
                  {b.label}
                </Link>
              </Reveal>
            </li>
          ))}
        </ul>
      </section>
    </>
  );
}

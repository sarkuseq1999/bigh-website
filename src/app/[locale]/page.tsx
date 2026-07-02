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
  const featuredImg =
    featured === "deer-horn-reishi"
      ? "/original/uploads/2021/12/DeerHornv1_1.png"
      : cardImage(locale, featured);

  const pills = [
    { slug: "organic", label: nav("organic") },
    { slug: "non-gmo", label: nav("nonGmo") },
    { slug: "gluten-free", label: nav("glutenFree") },
    { slug: "vegan", label: nav("vegan") },
  ];

  return (
    <>
      <Hero eyebrow={t("eyebrow")} brand={t("brand")} tagline={t("tagline")} learnMore={t("learnMore")} />

      {/* Latest release */}
      <section className="mx-auto grid max-w-6xl items-center gap-10 px-4 py-16 sm:px-6 md:grid-cols-2">
        <Reveal>
          <p className="text-lg font-semibold text-green">{t("latestEyebrow")}</p>
          <h2 className="mt-2 text-4xl font-bold">{productName(featured, locale)}</h2>
          <p className="mt-4 max-w-md text-lg">{t("featuredBlurb")}</p>
          <Link
            href={`/${featured}`}
            className="mt-7 inline-block rounded bg-green px-6 py-2.5 font-semibold text-white transition-colors hover:bg-green-dark"
          >
            {t("learnMore")}
          </Link>
        </Reveal>
        {featuredImg && (
          <Reveal delay={120} className="mx-auto w-full max-w-xs">
            <Image
              src={featuredImg}
              alt={productName(featured, locale)}
              {...imageDims(featuredImg)}
              className="h-auto w-full drop-shadow-[0_24px_40px_rgba(23,23,31,0.22)]"
              sizes="(max-width: 768px) 80vw, 320px"
            />
          </Reveal>
        )}
      </section>

      {/* Made in California — teal band, faithful */}
      <section className="relative overflow-hidden bg-teal">
        <Image
          src="/original/uploads/2019/04/madeincalifornia_bg.png"
          alt=""
          fill
          className="object-cover"
          sizes="100vw"
        />
        <div className="relative mx-auto grid max-w-6xl items-center gap-10 px-4 py-14 sm:px-6 md:grid-cols-2">
          <Reveal>
            <Image
              src="/original/uploads/2019/04/madeincalifornia4.jpg"
              alt={t("madeTitle")}
              {...imageDims("/original/uploads/2019/04/madeincalifornia4.jpg")}
              className="mx-auto h-auto w-full max-w-md"
              sizes="(max-width: 768px) 90vw, 440px"
            />
          </Reveal>
          <Reveal delay={120} className="text-center md:pr-6">
            <h2 className="text-4xl font-bold text-white">{t("madeTitle")}</h2>
            <p className="mx-auto mt-5 max-w-md text-lg leading-relaxed text-white">{t("madeBody")}</p>
          </Reveal>
        </div>
      </section>

      {/* Most Popular — full shelf */}
      <section id="products" className="mx-auto max-w-6xl scroll-mt-24 px-4 py-16 sm:px-6">
        <Reveal>
          <h2 className="text-center text-4xl font-bold">{t("popular")}</h2>
        </Reveal>
        <ul className="mt-12 grid grid-cols-2 gap-x-6 gap-y-12 sm:grid-cols-3 lg:grid-cols-5">
          {PRODUCT_SLUGS.map((slug, i) => {
            const img = cardImage(locale, slug);
            return (
              <li key={slug}>
                <Reveal delay={(i % 5) * 60}>
                  <Link href={`/${slug}`} className="group block text-center">
                    <div className="flex aspect-[5/6] items-center justify-center">
                      {img && (
                        <Image
                          src={img}
                          alt=""
                          {...imageDims(img)}
                          className="h-full w-auto object-contain drop-shadow-[0_14px_24px_rgba(23,23,31,0.16)] transition-transform duration-500 group-hover:scale-[1.06]"
                          sizes="(max-width: 640px) 45vw, 220px"
                        />
                      )}
                    </div>
                    <p className="mt-3 text-[15px] font-semibold text-heading group-hover:text-green-dark">
                      {productName(slug, locale)}
                    </p>
                  </Link>
                </Reveal>
              </li>
            );
          })}
        </ul>
      </section>

      {/* Driven by Nature — forest band, faithful */}
      <section className="relative overflow-hidden">
        <Image
          src="/original/uploads/2019/03/Driven-by-nature-2.jpg"
          alt=""
          fill
          className="object-cover"
          sizes="100vw"
        />
        <div aria-hidden className="absolute inset-0 bg-black/25" />
        <div className="relative mx-auto max-w-3xl px-4 py-24 text-center sm:px-6">
          <Reveal>
            <h2 className="text-4xl font-bold text-white drop-shadow">{t("natureTitle")}</h2>
            <p className="mx-auto mt-4 max-w-xl text-white drop-shadow">{t("natureBody")}</p>
            <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
              {pills.map((p) => (
                <Link
                  key={p.slug}
                  href={`/${p.slug}`}
                  className="rounded bg-green px-4 py-1.5 text-sm font-semibold text-white transition-colors hover:bg-green-dark"
                >
                  {p.label}
                </Link>
              ))}
            </div>
          </Reveal>
        </div>
      </section>

      {/* Guided by Science — faithful */}
      <section className="mx-auto grid max-w-6xl items-center gap-10 px-4 py-16 sm:px-6 md:grid-cols-2">
        <Reveal className="text-center md:text-left">
          <h2 className="text-4xl font-bold">{t("scienceTitle")}</h2>
          <p className="mx-auto mt-4 max-w-md md:mx-0">{t("scienceBody")}</p>
          <Link
            href="/science"
            className="mt-7 inline-block rounded bg-green px-6 py-2.5 font-semibold text-white transition-colors hover:bg-green-dark"
          >
            {t("learnMore")}
          </Link>
        </Reveal>
        <Reveal delay={120} className="mx-auto w-full max-w-sm">
          <Image
            src="/original/uploads/2019/04/guidedbysciene_1-878x1024.png"
            alt={t("scienceTitle")}
            {...imageDims("/original/uploads/2019/04/guidedbysciene_1-878x1024.png")}
            className="h-auto w-full"
            sizes="(max-width: 768px) 80vw, 380px"
          />
        </Reveal>
      </section>

      {/* Learn more / Connect — faithful two-panel band */}
      <section className="grid md:grid-cols-2">
        <Link href="/about" className="group relative block aspect-[16/9] overflow-hidden">
          <Image
            src="/original/uploads/2019/04/Learn-More_3.jpg"
            alt={nav("aboutBigh")}
            fill
            className="object-cover transition-transform duration-700 group-hover:scale-[1.04]"
            sizes="(max-width: 768px) 100vw, 50vw"
          />
        </Link>
        <Link href="/support" className="group relative block aspect-[16/9] overflow-hidden">
          <Image
            src="/original/uploads/2019/04/Connect-with-Us_3.jpg"
            alt={nav("support")}
            fill
            className="object-cover transition-transform duration-700 group-hover:scale-[1.04]"
            sizes="(max-width: 768px) 100vw, 50vw"
          />
        </Link>
      </section>
    </>
  );
}

import Image from "next/image";
import { setRequestLocale, getTranslations } from "next-intl/server";

import { Hero } from "@/components/clone/hero";
import { ParticlesBg } from "@/components/clone/particles";
import { Reveal } from "@/components/clone/reveal";
import { Link } from "@/i18n/navigation";
import { routing, type Locale } from "@/i18n/routing";
import { productName, isProductSlug, type ProductSlug } from "@/data/products";
import { loadPage, productImages } from "@/lib/content";
import { imageDims } from "@/lib/images";

export function generateStaticParams() {
  return routing.locales.map((locale) => ({ locale }));
}

// the original home shows exactly these three under "Most Popular"
const POPULAR: { slug: ProductSlug; img: string }[] = [
  { slug: "nuricell", img: "/original/uploads/2019/03/1140_1183_nuri1-987x1024.png" },
  { slug: "advanced-opc-formula", img: "/original/uploads/2019/03/1140_1183_opc_1-987x1024.png" },
  { slug: "green-bee-propolis", img: "/original/uploads/2019/03/1140_1183_propolis_1-1-987x1024.png" },
];

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
  const isDeerHorn = featured === "deer-horn-reishi";
  const featuredImg = isDeerHorn
    ? "/original/uploads/2021/12/DeerHornv1_1-683x1024.png"
    : cardImage(locale, featured);

  const pills = [
    { slug: "organic", label: nav("organic") },
    { slug: "non-gmo", label: nav("nonGmo") },
    { slug: "gluten-free", label: nav("glutenFree") },
  ];

  return (
    <>
      <Hero eyebrow={t("eyebrow")} brand={t("brand")} tagline={t("tagline")} learnMore={t("learnMore")} />

      {/* Latest release — text | slice art | product bottle (measured columns) */}
      <section className="relative z-0 mx-auto grid max-w-6xl items-center gap-8 px-4 pb-16 pt-10 sm:px-6 md:grid-cols-[1.1fr_1fr_0.9fr] md:pt-16">
        <div className="text-center md:text-left">
          <p className="text-3xl font-semibold">{t("latestEyebrow")}</p>
          <h2 className="mt-2 text-[clamp(2.2rem,4vw,3.6rem)] font-semibold leading-tight">
            {productName(featured, locale)}
          </h2>
          <p className="mt-3 text-[clamp(1.2rem,2.4vw,2.2rem)] font-semibold leading-snug">
            {t("featuredBlurb")}
          </p>
          <Link
            href={`/${featured}`}
            className="mt-7 inline-block rounded bg-green px-[30px] py-[15px] text-base font-medium leading-none text-white transition-colors hover:bg-green-dark"
          >
            {t("learnMore")}
          </Link>
        </div>
        {isDeerHorn ? (
          <>
            <Reveal className="mx-auto hidden w-full max-w-[26rem] md:block">
              <Image
                src="/original/uploads/2021/12/Slice-1_latestrelease.png"
                alt=""
                {...imageDims("/original/uploads/2021/12/Slice-1_latestrelease.png")}
                className="h-auto w-full"
                sizes="420px"
              />
            </Reveal>
            <Reveal delay={100} className="mx-auto w-full max-w-[20rem]">
              {featuredImg && (
                <Image
                  src={featuredImg}
                  alt={productName(featured, locale)}
                  {...imageDims(featuredImg)}
                  className="h-auto w-full"
                  sizes="(max-width: 768px) 70vw, 320px"
                />
              )}
            </Reveal>
          </>
        ) : (
          <Reveal delay={100} className="mx-auto w-full max-w-[20rem] md:col-span-2">
            {featuredImg && (
              <Image
                src={featuredImg}
                alt={productName(featured, locale)}
                {...imageDims(featuredImg)}
                className="h-auto w-full"
                sizes="(max-width: 768px) 70vw, 320px"
              />
            )}
          </Reveal>
        )}
      </section>

      {/* Made in California — flush-left map on the teal art background */}
      <section className="relative overflow-hidden bg-teal">
        <Image
          src="/original/uploads/2019/04/madeincalifornia_bg.png"
          alt=""
          fill
          className="object-cover"
          sizes="100vw"
        />
        <div className="relative grid items-center md:grid-cols-2">
          <Image
            src="/original/uploads/2019/04/madeincalifornia4.jpg"
            alt={t("madeTitle")}
            {...imageDims("/original/uploads/2019/04/madeincalifornia4.jpg")}
            className="h-auto w-full max-w-[45rem]"
            sizes="(max-width: 768px) 100vw, 50vw"
          />
          <Reveal className="px-6 pb-12 text-center md:px-10 md:pb-0">
            <h2 className="text-[clamp(2rem,3.8vw,3.4rem)] font-semibold text-white/95">
              {t("madeTitle")}
            </h2>
            <p className="mx-auto mt-5 max-w-xl text-[clamp(1.05rem,2vw,1.8rem)] font-semibold leading-normal text-white/95">
              {t("madeBody")}
            </p>
          </Reveal>
        </div>
      </section>

      {/* Most Popular — exactly three, no captions, like the original */}
      <section id="products" className="mx-auto max-w-6xl scroll-mt-24 px-4 py-16 sm:px-6">
        <Reveal>
          <h2 className="text-center text-[clamp(2.4rem,4.5vw,4.1rem)] font-semibold">{t("popular")}</h2>
        </Reveal>
        <ul className="mt-10 grid grid-cols-1 items-end gap-6 sm:grid-cols-3">
          {POPULAR.map(({ slug, img }, i) => (
            <li key={slug}>
              <Reveal delay={i * 80}>
                <Link href={`/${slug}`} className="group block" aria-label={productName(slug, locale)}>
                  <Image
                    src={img}
                    alt={productName(slug, locale)}
                    {...imageDims(img)}
                    className="mx-auto h-auto w-full max-w-[22.5rem] transition-transform duration-500 group-hover:scale-[1.05]"
                    sizes="(max-width: 640px) 80vw, 360px"
                  />
                </Link>
              </Reveal>
            </li>
          ))}
        </ul>
      </section>

      {/* Driven by Nature — forest band with three green pills */}
      <section className="relative overflow-hidden">
        <Image
          src="/original/uploads/2019/03/Driven-by-nature-2.jpg"
          alt=""
          fill
          className="object-cover"
          sizes="100vw"
        />
        <div className="relative mx-auto max-w-3xl px-4 py-24 text-center sm:px-6">
          <Reveal>
            <h2 className="text-[clamp(2.4rem,4.9vw,4.4rem)] font-semibold text-[#ededed] drop-shadow">
              {t("natureTitle")}
            </h2>
            <p className="mx-auto mt-3 max-w-xl text-sm text-white drop-shadow md:text-base">
              {t("natureBody")}
            </p>
            <div className="mt-7 flex flex-wrap items-center justify-center gap-3">
              {pills.map((p) => (
                <Link
                  key={p.slug}
                  href={`/${p.slug}`}
                  className="rounded bg-green px-4 py-2 text-sm font-medium leading-none text-white transition-colors hover:bg-green-dark"
                >
                  {p.label}
                </Link>
              ))}
            </div>
          </Reveal>
        </div>
      </section>

      {/* Guided by Science — text left, large microscope right,
          particles.js-style network background like the original */}
      <section className="relative">
        <ParticlesBg className="absolute inset-0 h-full w-full" />
        <div className="relative mx-auto grid max-w-6xl items-center gap-8 px-4 py-14 sm:px-6 md:grid-cols-[1fr_1.15fr]">
        <Reveal className="text-center md:text-left">
          <h2 className="text-[clamp(2rem,3.8vw,3.4rem)] font-semibold">{t("scienceTitle")}</h2>
          <p className="mx-auto mt-4 max-w-md md:mx-0">{t("scienceBody")}</p>
          <Link
            href="/science"
            className="mt-7 inline-block rounded bg-green px-[30px] py-[15px] text-base font-medium leading-none text-white transition-colors hover:bg-green-dark"
          >
            {t("learnMore")}
          </Link>
        </Reveal>
        <Reveal delay={100} className="mx-auto w-full max-w-[44rem]">
          <Image
            src="/original/uploads/2019/04/guidedbysciene_1-878x1024.png"
            alt={t("scienceTitle")}
            {...imageDims("/original/uploads/2019/04/guidedbysciene_1-878x1024.png")}
            className="h-auto w-full"
            sizes="(max-width: 768px) 90vw, 700px"
          />
        </Reveal>
        </div>
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

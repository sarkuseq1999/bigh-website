import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { hasLocale, NextIntlClientProvider } from "next-intl";
import { getTranslations, setRequestLocale } from "next-intl/server";
import { Be_Vietnam_Pro, DM_Sans, Instrument_Serif } from "next/font/google";

import { routing, type Locale } from "@/i18n/routing";
import "../globals.css";

const sans = DM_Sans({
  subsets: ["latin", "latin-ext"],
  variable: "--font-dm-sans",
  display: "swap",
});
// Switzer, the brand face (Mo, September 28, 2026). Its licence (ITF Free Font License) allows
// web use but not redistributing the files, and this repository is public, so it loads from
// Fontshare's own stylesheet rather than next/font/local.
const SWITZER = "https://api.fontshare.com/v2/css?f[]=switzer@1,2&display=swap";

// Be Vietnam Pro, for Vietnamese only (Mo, September 28, 2026): Switzer lacks 92 of the 134
// Vietnamese letters, so Chrome drew them from Arial one by one. SIL Open Font License, so next/font
// self-hosts it. globals.css points the brand-face token (--font-brand) at it for lang="vi", and
// sets the headline weight (Switzer's 450/460) to 400, whose strokes match; the site's other
// weights map to the static ones as usual (550 draws 600). Not preloaded, so other languages
// never download it.
const vietnamese = Be_Vietnam_Pro({
  subsets: ["vietnamese", "latin"],
  weight: ["300", "400", "500", "600", "700"],
  style: ["normal", "italic"],
  variable: "--font-be-vietnam-pro",
  display: "swap",
  preload: false,
});

const serif = Instrument_Serif({
  subsets: ["latin"],
  weight: "400",
  style: "normal",
  variable: "--font-instrument",
  display: "swap",
});

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  if (!hasLocale(routing.locales, locale)) notFound();
  const translate = await getTranslations({ locale, namespace: "Copy" });
  return {
    title: `BiGH — ${translate("m149")}`,
    description: translate("m169"),
    robots: { index: false, follow: false },
  };
}

const languageTags: Record<Locale, string> = {
  en: "en",
  kr: "ko",
  jp: "ja",
  cns: "zh-Hans",
  hken: "zh-Hant-HK",
  vn: "vi",
};

export function generateStaticParams() {
  return routing.locales.map((locale) => ({ locale }));
}

export default async function LocaleLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!hasLocale(routing.locales, locale)) notFound();
  setRequestLocale(locale);

  // globals.css scrolls smoothly for in-page jumps. data-scroll-behavior lets Next.js switch that
  // off while it changes pages, so a new page opens at its top at once (Next.js 16 no longer does
  // this by default). Without it the product page's scroll animations measured mid-glide and put
  // visitors back where they were on the homepage (Mo, September 28, 2026).
  return (
    <html lang={languageTags[locale]} data-scroll-behavior="smooth">
      <body
        className={`${sans.variable} ${serif.variable}${locale === "vn" ? ` ${vietnamese.variable}` : ""}`}
      >
        <link rel="preconnect" href="https://api.fontshare.com" />
        <link rel="preconnect" href="https://cdn.fontshare.com" crossOrigin="anonymous" />
        <link rel="stylesheet" href={SWITZER} precedence="default" />
        <NextIntlClientProvider>{children}</NextIntlClientProvider>
      </body>
    </html>
  );
}

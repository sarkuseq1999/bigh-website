import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { hasLocale, NextIntlClientProvider } from "next-intl";
import { getTranslations, setRequestLocale } from "next-intl/server";
import { DM_Sans, Instrument_Serif } from "next/font/google";

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

  return (
    <html lang={languageTags[locale]}>
      <body className={`${sans.variable} ${serif.variable}`}>
        <link rel="preconnect" href="https://api.fontshare.com" />
        <link rel="preconnect" href="https://cdn.fontshare.com" crossOrigin="anonymous" />
        <link rel="stylesheet" href={SWITZER} precedence="default" />
        <NextIntlClientProvider>{children}</NextIntlClientProvider>
      </body>
    </html>
  );
}

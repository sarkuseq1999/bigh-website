import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { hasLocale, NextIntlClientProvider } from "next-intl";
import { getTranslations, setRequestLocale } from "next-intl/server";
import { Be_Vietnam_Pro, DM_Sans, Instrument_Serif, Ysabeau, Zilla_Slab } from "next/font/google";

import { routing, type Locale } from "@/i18n/routing";
import "../globals.css";

const sans = DM_Sans({
  subsets: ["latin", "latin-ext"],
  variable: "--font-dm-sans",
  display: "swap",
});
// Switzer, the brand face (Mo, September 28, 2026), is served from this site (October 23, 2026:
// Fontshare's stylesheet kept dropping the connection, and pages fell back to another face). Its
// licence (ITF Free Font License 2.0) allows self-hosting but not sharing the files through a
// public repository, and this one is public: so not next/font/local, whose files would have to be
// committed. scripts/fetch-fonts.mjs fetches the official files before each build into
// public/fonts/switzer/ (git-ignored); globals.css declares them. The upright face is preloaded,
// except on Vietnamese pages, which set their words in Be Vietnam Pro.
const SWITZER = "/fonts/switzer/switzer-variable-v1.woff2";

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

// Zilla Slab, for the words routed into the footer's trail sign only (ink/fda-statement.tsx; Mo,
// October 13, 2026): a slab serif reads like a carved California park sign. SIL Open Font License.
// Not preloaded: the sign is the page's last line.
const sign = Zilla_Slab({
  subsets: ["latin", "latin-ext"],
  weight: "600",
  variable: "--font-sign",
  display: "swap",
  preload: false,
});

// Ysabeau, the site's title face, is also the menu bar's (Mo's pick A, "Signed with one stroke",
// October 21, 2026), and the bar is on every page, so every page has it here. Not preloaded, as on
// the pages that set their titles in it: Chinese, Japanese and Korean pages keep their own letters
// in the bar and would never use a preloaded file.
const titles = Ysabeau({
  subsets: ["latin", "vietnamese"],
  variable: "--font-ysabeau",
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
        className={`${sans.variable} ${serif.variable} ${sign.variable} ${titles.variable}${locale === "vn" ? ` ${vietnamese.variable}` : ""}`}
      >
        {locale !== "vn" && (
          <link rel="preload" href={SWITZER} as="font" type="font/woff2" crossOrigin="anonymous" />
        )}
        <NextIntlClientProvider>{children}</NextIntlClientProvider>
      </body>
    </html>
  );
}

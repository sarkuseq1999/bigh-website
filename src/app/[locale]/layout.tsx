import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { NextIntlClientProvider, hasLocale } from "next-intl";
import { getTranslations, setRequestLocale } from "next-intl/server";
import { Roboto } from "next/font/google";

import { SiteFooter } from "@/components/clone/footer";
import { SiteHeader } from "@/components/clone/header";
import { routing, type Locale } from "@/i18n/routing";
import "../globals.css";

// The original site sets every heading and button in Roboto (600) — measured
// from the live pages, not guessed.
const roboto = Roboto({
  subsets: ["latin", "latin-ext", "vietnamese"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-roboto",
  display: "swap",
});

// CJK / Vietnamese companion faces, served by Google Fonts with unicode-range
// subsetting. Latin glyphs still come from Fraunces/Hanken; these fill the rest.
const CJK_FONTS: Partial<Record<Locale, string>> = {
  kr: "https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Noto+Serif+KR:wght@400;600;700&display=swap",
  jp: "https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&family=Noto+Serif+JP:wght@400;600;700&display=swap",
  cns: "https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&family=Noto+Serif+SC:wght@400;600;700&display=swap",
  hken: "https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&family=Noto+Serif+SC:wght@400;600;700&display=swap",
  vn: "https://fonts.googleapis.com/css2?family=Noto+Sans:ital,wght@0,400;0,500;0,700&family=Noto+Serif:wght@400;600;700&display=swap",
};

export function generateStaticParams() {
  return routing.locales.map((locale) => ({ locale }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "Meta" });

  return {
    title: {
      default: t("title"),
      template: "%s | BiGH",
    },
    description: t("description"),
    metadataBase: new URL("https://www.bighnow.com"),
    openGraph: {
      title: t("title"),
      description: t("description"),
      type: "website",
      locale,
    },
    robots: { index: true, follow: true },
  };
}

export default async function LocaleLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!hasLocale(routing.locales, locale)) {
    notFound();
  }
  setRequestLocale(locale);
  const cjkHref = CJK_FONTS[locale as Locale];

  return (
    <html
      lang={locale}
      suppressHydrationWarning
      className={`${roboto.variable} h-full antialiased`}
    >
      <body className="bg-background text-foreground flex min-h-full flex-col">
        {cjkHref && (
          <>
            <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
            {/* React 19 hoists precedence-tagged stylesheets into <head> */}
            <link rel="stylesheet" href={cjkHref} precedence="default" />
          </>
        )}
        <NextIntlClientProvider>
          <SiteHeader />
          <main className="flex-1">{children}</main>
          <SiteFooter locale={locale as Locale} />
        </NextIntlClientProvider>
      </body>
    </html>
  );
}

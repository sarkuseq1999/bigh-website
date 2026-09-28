import type { Metadata } from "next";
import { setRequestLocale } from "next-intl/server";
import { AboutPage } from "@/components/about/about-page";

export const metadata: Metadata = {
  title: "BiGH — About",
};

// Switzer, the site's type, loads in the locale layout.
export default async function Page({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  setRequestLocale(locale);

  return <AboutPage />;
}

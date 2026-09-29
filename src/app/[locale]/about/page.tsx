import type { Metadata } from "next";
import { getTranslations, setRequestLocale } from "next-intl/server";
import { AboutPage } from "@/components/about/about-page";
import copyKeys from "@/i18n/copy-keys.json";
import { redirect } from "@/i18n/navigation";

type Params = Promise<{ locale: string }>;

// "BiGH — About", with "About" from the catalogs (the header's own word for this page).
export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const { locale } = await params;
  const translate = await getTranslations({ locale, namespace: "Copy" });
  return { title: `BiGH — ${translate(copyKeys["About"])}` };
}

// Switzer, the site's type, loads in the locale layout. /hken goes to Chinese, as on the homepage
// and the product pages.
export default async function Page({ params }: { params: Params }) {
  const { locale } = await params;
  if (locale === "hken") redirect({ href: "/about", locale: "cns" });
  setRequestLocale(locale);

  return <AboutPage />;
}

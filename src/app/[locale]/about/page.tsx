import type { Metadata } from "next";
import { setRequestLocale } from "next-intl/server";
import { AboutPage } from "@/components/about/about-page";

export const metadata: Metadata = {
  title: "BiGH — About",
};

// Switzer, the site's type (Mo, Sept 28, 2026). Its licence allows web use but not redistributing
// the files, and the repository is public, so it loads from Fontshare's own stylesheet; never add
// the font files. This is the same link, href and precedence as main's locale layout (07529d5),
// so React renders it once after the merge. Remove it here once this branch has merged main.
const SWITZER = "https://api.fontshare.com/v2/css?f[]=switzer@1,2&display=swap";

export default async function Page({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  setRequestLocale(locale);

  return (
    <>
      <link rel="preconnect" href="https://api.fontshare.com" />
      <link rel="preconnect" href="https://cdn.fontshare.com" crossOrigin="anonymous" />
      <link rel="stylesheet" href={SWITZER} precedence="default" />
      <AboutPage />
    </>
  );
}

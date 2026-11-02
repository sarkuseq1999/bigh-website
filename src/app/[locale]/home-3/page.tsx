import type { Metadata } from "next";
import { Ysabeau } from "next/font/google";
import { setRequestLocale } from "next-intl/server";
import { ProductPagesProvider } from "@/components/home/product-action";
import { SiteDialogs } from "@/components/ink/dialogs";
import { LookInk } from "@/components/home-v2/look-ink/look-ink";
import { productPageLinks } from "@/components/product/catalog";
import { redirect } from "@/i18n/navigation";

// As the homepage (page.tsx), with its title face.
const titles = Ysabeau({
  subsets: ["latin", "vietnamese"],
  variable: "--font-ysabeau",
  display: "swap",
  preload: false,
});

// For comparison only (Mo, November 2, 2026): the homepage closing on 3, McWay Falls
// (assets.ts `purposeEndings`); /home-1 is the other one, "/" keeps the coast walk. Remove this
// route once Mo has picked one.
export const metadata: Metadata = { robots: { index: false } };

export default async function Page({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  if (locale === "hken") redirect({ href: "/home-3", locale: "cns" });
  setRequestLocale(locale);

  return (
    <ProductPagesProvider pages={productPageLinks()}>
      <SiteDialogs>
        <LookInk className={titles.variable} ending="rich-falls" />
      </SiteDialogs>
    </ProductPagesProvider>
  );
}

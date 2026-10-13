import { Ysabeau } from "next/font/google";
import { setRequestLocale } from "next-intl/server";
import { ProductPagesProvider } from "@/components/home/product-action";
import { SiteDialogs } from "@/components/ink/dialogs";
import { LookInk } from "@/components/home-v2/look-ink/look-ink";
import { productPageLinks } from "@/components/product/catalog";
import { redirect } from "@/i18n/navigation";

// Ysabeau, the homepage's title face (Mo, October 13, 2026; home-titles.module.css). SIL Open Font
// License, so next/font self-hosts it. It has Vietnamese, so /vn's titles use it too. Not preloaded:
// the build hoisted a page font's preload onto every page (5 font files on /about instead of 3), so
// the browser fetches it only where a title asks for it. The headline fades in over a second while
// it arrives.
const titles = Ysabeau({
  subsets: ["latin", "vietnamese"],
  variable: "--font-ysabeau",
  display: "swap",
  preload: false,
});

// The homepage: "Ink & Gold", the crane (Mo's pick, October 2, 2026). The preview dialogs wrap it
// (no explainer pictures: the look's own paintings carry the science). Products with their own
// page (from the catalog) link there; the rest open the preview dialog.
export default async function HomePage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  if (locale === "hken") redirect({ href: "/", locale: "cns" });
  setRequestLocale(locale);

  return (
    <ProductPagesProvider pages={productPageLinks()}>
      <SiteDialogs>
        <LookInk className={titles.variable} />
      </SiteDialogs>
    </ProductPagesProvider>
  );
}

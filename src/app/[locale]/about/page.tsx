import type { Metadata } from "next";
import { getTranslations, setRequestLocale } from "next-intl/server";
import { AboutInk } from "@/components/about/about-ink";
import { BeforeHydration } from "@/components/about/before-hydration";
import { ProductPagesProvider } from "@/components/home/product-action";
import { SiteDialogs } from "@/components/ink/dialogs";
import { productPageLinks } from "@/components/product/catalog";
import copyKeys from "@/i18n/copy-keys.json";
import { redirect } from "@/i18n/navigation";

type Params = Promise<{ locale: string }>;

// "BiGH — About", with "About" from the catalogs (the header's own word for this page).
export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const { locale } = await params;
  const translate = await getTranslations({ locale, namespace: "Copy" });
  return { title: `BiGH — ${translate(copyKeys["About"])}` };
}

// The circle waits for its picture (circle.module.css): with script on, its stroke and gold hold
// until the stroke's picture is in. This lets them go before React hydrates, where the parser
// reaches it (after the page's HTML): once the picture is in, however late, it adopts a sheet that
// sets them running. No timer and no release on a failed picture: either would let the gold rise
// alone on bare paper. It changes no node or attribute React rendered, so hydration cannot
// mismatch. Without constructed sheets it does nothing; once hydrated, the Opening lets them go too
// (about-ink.tsx). BeforeHydration renders it in the server's HTML only, so a client-side
// navigation to /about neither builds a dead script nor logs React's script warning.
const LET_THE_CIRCLE_GO = `(() => {
  const stroke = document.querySelector("[data-enso] img:not([data-dot])");
  if (!stroke || !document.adoptedStyleSheets) return;
  let sheet;
  try {
    sheet = new CSSStyleSheet();
    sheet.replaceSync("[data-enso] img { animation-play-state: running !important; }");
  } catch (e) {
    return;
  }
  const go = () => {
    document.adoptedStyleSheets = [...document.adoptedStyleSheets, sheet];
  };
  if (stroke.complete) {
    if (stroke.naturalWidth) go();
    return;
  }
  stroke.addEventListener("load", go, { once: true });
})();`;

// The About page in the Ink & Gold look (October 5, 2026), on the shared kit and sheets.
// Switzer, the site's type, loads in the locale layout. /hken goes to Chinese, as on the homepage
// and the product pages.
export default async function Page({ params }: { params: Params }) {
  const { locale } = await params;
  if (locale === "hken") redirect({ href: "/about", locale: "cns" });
  setRequestLocale(locale);

  return (
    <ProductPagesProvider pages={productPageLinks()}>
      <SiteDialogs>
        <AboutInk />
        <BeforeHydration code={LET_THE_CIRCLE_GO} />
      </SiteDialogs>
    </ProductPagesProvider>
  );
}

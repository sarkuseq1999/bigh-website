import type { Metadata } from "next";
import { Ysabeau } from "next/font/google";
import { getTranslations, setRequestLocale } from "next-intl/server";
import { ProductPagesProvider } from "@/components/home/product-action";
import { SiteDialogs } from "@/components/ink/dialogs";
import { productPageLinks } from "@/components/product/catalog";
import { ScienceInk } from "@/components/science/ink/science-ink";
import copyKeys from "@/i18n/copy-keys.json";
import { redirect } from "@/i18n/navigation";
import { pageMetadata } from "@/lib/seo";

// Ysabeau, the homepage's title face (Mo, October 13, 2026), here for the Science page's titles as
// the other pages follow the homepage. Not preloaded, as on the homepage ([locale]/page.tsx).
const titles = Ysabeau({
  subsets: ["latin", "vietnamese"],
  variable: "--font-ysabeau",
  display: "swap",
  preload: false,
});

type Params = Promise<{ locale: string }>;

export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const { locale } = await params;
  const translate = await getTranslations({ locale, namespace: "Copy" });
  return pageMetadata({
    locale,
    path: "/science",
    title:
      locale === "en"
        ? "Our science: cellular health, explained — BiGH"
        : `${translate(copyKeys["Science"])} — BiGH`,
    description:
      locale === "en"
        ? "Why BiGH starts with the cell: mitochondria, free radicals and aging, explained simply. Meet Dr. Jiankang Liu, and read the research yourself."
        : translate("m169"),
    image: { url: "/og/science-v1.jpg", width: 1200, height: 630, alt: "BiGH Science" },
  });
}

// The Science page in Ink & Gold, "the handscroll" (Mo, October 13-14, 2026; spec
// docs/superpowers/specs/2026-10-14-science-ink-design.md). /hken goes to Chinese: a [locale]
// page without this redirect fails the build's static render.
export default async function Page({ params }: { params: Params }) {
  const { locale } = await params;
  if (locale === "hken") redirect({ href: "/science", locale: "cns" });
  setRequestLocale(locale);

  return (
    <ProductPagesProvider pages={productPageLinks()}>
      <SiteDialogs>
        <ScienceInk fontClass={titles.variable} />
      </SiteDialogs>
    </ProductPagesProvider>
  );
}

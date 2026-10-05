import { setRequestLocale } from "next-intl/server";
import { ProductPagesProvider } from "@/components/home/product-action";
import { HomeDialogs } from "@/components/home-v2/dialogs";
import { LookInk } from "@/components/home-v2/look-ink/look-ink";
import { productPageLinks } from "@/components/product/catalog";
import { redirect } from "@/i18n/navigation";

// The homepage: "Ink & Gold", the crane (Mo's pick, October 2, 2026). The preview dialogs wrap it
// (no explainer pictures: the look's own paintings carry the science). Products with their own
// page (from the catalog) link there; the rest open the preview dialog.
// Review only (October 5, menu bar options): `?nav=a|b|c` swaps in one of the three menu bars
// (`?nav=today` = today's bar with the review chip; no `nav` = the page exactly as it is live).
export default async function HomePage({
  params,
  searchParams,
}: {
  params: Promise<{ locale: string }>;
  searchParams: Promise<{ nav?: string; rec?: string }>;
}) {
  const { locale } = await params;
  const { nav, rec } = await searchParams;
  if (locale === "hken") redirect({ href: "/", locale: "cns" });
  setRequestLocale(locale);

  return (
    <ProductPagesProvider pages={productPageLinks()}>
      <HomeDialogs>
        <LookInk nav={nav} review={Boolean(nav) && !rec} />
      </HomeDialogs>
    </ProductPagesProvider>
  );
}

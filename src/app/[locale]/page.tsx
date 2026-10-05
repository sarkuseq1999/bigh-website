import { setRequestLocale } from "next-intl/server";
import { ProductPagesProvider } from "@/components/home/product-action";
import { SiteDialogs } from "@/components/ink/dialogs";
import { LookInk } from "@/components/home-v2/look-ink/look-ink";
import { productPageLinks } from "@/components/product/catalog";
import { redirect } from "@/i18n/navigation";

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
        <LookInk />
      </SiteDialogs>
    </ProductPagesProvider>
  );
}

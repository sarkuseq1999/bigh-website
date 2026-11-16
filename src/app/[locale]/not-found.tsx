import type { Metadata } from "next";
import { ProductPagesProvider } from "@/components/home/product-action";
import { SiteDialogs } from "@/components/ink/dialogs";
import { NotFoundPage } from "@/components/not-found/not-found-page";
import { productPageLinks } from "@/components/product/catalog";

export const metadata: Metadata = {
  title: "Page not found — BiGH",
  robots: { index: false, follow: true },
};

export default function NotFound() {
  return (
    <ProductPagesProvider pages={productPageLinks()}>
      <SiteDialogs>
        <NotFoundPage />
      </SiteDialogs>
    </ProductPagesProvider>
  );
}

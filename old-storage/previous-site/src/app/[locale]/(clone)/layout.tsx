import { SiteFooter } from "@/components/clone/footer";
import { SiteHeader } from "@/components/clone/header";
import type { Locale } from "@/i18n/routing";

// Chrome for the legacy clone pages only — the new Golden Hour homepage
// lives in the (home) group with its own header/footer.
export default async function CloneLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;

  return (
    <>
      <SiteHeader />
      <main className="flex-1">{children}</main>
      <SiteFooter locale={locale as Locale} />
    </>
  );
}

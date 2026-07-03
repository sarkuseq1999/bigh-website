import { GhFooter } from "@/components/home/gh-footer";
import { GhHeader } from "@/components/home/gh-header";
import type { Locale } from "@/i18n/routing";

// Golden Hour chrome for the new homepage — completely separate from the
// clone's SiteHeader/SiteFooter, which only wrap the legacy (clone) pages.
export default async function GhLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;

  return (
    <div className="gh relative flex min-h-svh flex-col">
      <GhHeader />
      <main className="flex-1">{children}</main>
      <GhFooter locale={locale as Locale} />
    </div>
  );
}

import { setRequestLocale } from "next-intl/server";

import { SiteHeader } from "@/components/site/site-header";
import { Hero } from "@/components/site/hero";
import { FeatureGrid } from "@/components/site/feature-grid";
import { EmailSignup } from "@/components/site/email-signup";
import { SiteFooter } from "@/components/site/site-footer";

export default async function HomePage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  setRequestLocale(locale);

  return (
    <>
      <SiteHeader />
      <main className="flex-1">
        <Hero />
        <FeatureGrid />
        <EmailSignup />
      </main>
      <SiteFooter />
    </>
  );
}

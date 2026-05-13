import { setRequestLocale } from "next-intl/server";

import { SiteHeader } from "@/components/site/site-header";
import { Hero } from "@/components/site/hero";
import { BrainScience } from "@/components/site/brain-science";
import { YourMind } from "@/components/site/your-mind";
import { Credibility } from "@/components/site/credibility";
import { TheSystem } from "@/components/site/the-system";
import { CustomerStories } from "@/components/site/customer-stories";
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
        <YourMind />
        <BrainScience />
        <Credibility />
        <TheSystem />
        <CustomerStories />
        <FeatureGrid />
        <EmailSignup />
      </main>
      <SiteFooter />
    </>
  );
}

import type { Metadata } from "next";
import { setRequestLocale } from "next-intl/server";
import { SciencePage } from "@/components/science/science-page";
import { redirect } from "@/i18n/navigation";

export const metadata: Metadata = {
  title: "BiGH — Science",
};

export default async function Page({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  if (locale === "hken") redirect({ href: "/science", locale: "cns" });
  setRequestLocale(locale);

  return <SciencePage />;
}

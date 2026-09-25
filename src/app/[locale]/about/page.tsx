import type { Metadata } from "next";
import { setRequestLocale } from "next-intl/server";
import { AboutPage } from "@/components/about/about-page";
import { toLook } from "@/components/about/about-content";

export const metadata: Metadata = {
  title: "BiGH — About",
};

// Mo picked look A (Sept 25); /about shows it. ?look=b|ab|c still opens the other review looks
// until they are cleaned up.
export default async function Page({
  params,
  searchParams,
}: {
  params: Promise<{ locale: string }>;
  searchParams: Promise<Record<string, string | string[] | undefined>>;
}) {
  const { locale } = await params;
  setRequestLocale(locale);
  const { look } = await searchParams;

  return <AboutPage look={toLook(look)} />;
}

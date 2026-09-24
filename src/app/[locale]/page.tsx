import { setRequestLocale } from "next-intl/server";
import { Homepage } from "@/components/home/homepage";
import { redirect } from "@/i18n/navigation";

export default async function HomePage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  if (locale === "hken") redirect({ href: "/", locale: "cns" });
  setRequestLocale(locale);

  return <Homepage />;
}

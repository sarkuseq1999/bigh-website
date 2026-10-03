import { setRequestLocale } from "next-intl/server";
import { HomeDialogs } from "@/components/home-v2/dialogs";
import { LookInk } from "@/components/home-v2/look-ink/look-ink";
import { redirect } from "@/i18n/navigation";

// The homepage: "Ink & Gold", the crane (Mo's pick, October 2, 2026). The preview dialogs wrap it
// (no explainer pictures: the look's own paintings carry the science).
export default async function HomePage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  if (locale === "hken") redirect({ href: "/", locale: "cns" });
  setRequestLocale(locale);

  return (
    <HomeDialogs>
      <LookInk />
    </HomeDialogs>
  );
}

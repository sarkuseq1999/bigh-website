import { getTranslations } from "next-intl/server";

import { Link } from "@/i18n/navigation";
import type { Locale } from "@/i18n/routing";

// Faithful to the original: near-black band, bordered FDA disclaimer,
// pipe-separated legal links, copyright.
export async function SiteFooter({ locale }: { locale: Locale }) {
  const t = await getTranslations({ locale, namespace: "Footer" });
  const year = new Date().getFullYear();

  const links = [
    { href: "/privacy-notice", label: t("privacy") },
    { href: "/terms-and-conditions", label: t("terms") },
    { href: "/return-policy", label: t("returns") },
    { href: "/opportunity", label: t("opportunity") },
    { href: "/career", label: t("career") },
  ];

  return (
    <footer className="mt-20 bg-[#111114] text-white">
      <div className="mx-auto max-w-5xl px-4 py-10 sm:px-6">
        <p className="mx-auto max-w-4xl rounded-md border border-white/60 px-4 py-3 text-center text-sm font-semibold leading-snug">
          {t("disclaimer")}
        </p>
        <nav
          aria-label={t("legal")}
          className="mt-7 flex flex-wrap items-center justify-center gap-x-2 gap-y-1 text-sm font-semibold"
        >
          {links.map((l, i) => (
            <span key={l.href} className="flex items-center gap-2">
              {i > 0 && <span aria-hidden className="text-white/40">|</span>}
              <Link href={l.href} className="hover:text-green">
                {l.label}
              </Link>
            </span>
          ))}
        </nav>
        <p className="mt-4 text-center text-sm text-white/70">
          {/* year substituted in code: ICU {year} args break next-intl 4.11
              message parsing during `next build` static generation */}
          {t("rights").replace("{year}", String(year))}
        </p>
      </div>
    </footer>
  );
}

"use client";

import { useLocale, useTranslations } from "next-intl";
import { useParams } from "next/navigation";

import { usePathname, useRouter } from "@/i18n/navigation";
import type { Locale } from "@/i18n/routing";

const LANGS: { code: Locale; label: string }[] = [
  { code: "en", label: "English" },
  { code: "kr", label: "한국어" },
  { code: "jp", label: "日本語" },
  { code: "cns", label: "中文(简体)" },
  { code: "hken", label: "中文(香港)" },
  { code: "vn", label: "Tiếng Việt" },
];

export function LangSwitcher({ dark = false }: { dark?: boolean }) {
  const locale = useLocale();
  const t = useTranslations("Nav");
  const router = useRouter();
  const pathname = usePathname();
  const params = useParams();

  return (
    <label className={`flex items-center gap-1.5 text-sm ${dark ? "text-white/70" : "text-body-col"}`}>
      <span className="sr-only">{t("language")}</span>
      <svg aria-hidden viewBox="0 0 24 24" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="1.5">
        <circle cx="12" cy="12" r="9" />
        <path d="M3 12h18M12 3c2.5 2.6 3.8 5.7 3.8 9S14.5 18.4 12 21c-2.5-2.6-3.8-5.7-3.8-9S9.5 5.6 12 3z" />
      </svg>
      <select
        className={`cursor-pointer appearance-none bg-transparent pr-1 font-medium outline-none ${dark ? "text-white [&>option]:text-heading" : "text-heading"}`}
        value={locale}
        onChange={(e) => {
          const next = e.target.value as Locale;
          // slug may not exist in the target locale; the [slug] page 404s
          // gracefully, and next-intl keeps params intact for shared pages
          router.replace(
            // @ts-expect-error -- pathname/params pair is dynamic by design
            { pathname, params },
            { locale: next },
          );
        }}
      >
        {LANGS.map((l) => (
          <option key={l.code} value={l.code}>
            {l.label}
          </option>
        ))}
      </select>
    </label>
  );
}

"use client";

import { useLocale } from "next-intl";
import { useTransition } from "react";
import { ChevronDown, Globe2 } from "lucide-react";
import { usePathname, useRouter } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import type { Locale } from "@/i18n/routing";
import styles from "./header-utilities.module.css";

const languages = [
  { locale: "en", name: "English", tag: "en" },
  { locale: "cns", name: "简体中文", tag: "zh-Hans" },
  { locale: "kr", name: "한국어", tag: "ko" },
  { locale: "vn", name: "Tiếng Việt", tag: "vi" },
  { locale: "jp", name: "日本語", tag: "ja" },
] as const;

export function HeaderUtilities() {
  const copy = useCopy();
  const locale = useLocale();
  const pathname = usePathname();
  const router = useRouter();
  const [pending, startTransition] = useTransition();

  function changeLanguage(next: string) {
    if (!languages.some((language) => language.locale === next)) return;
    // Keep the visitor's current section and query while changing only the language.
    startTransition(() =>
      router.replace(`${pathname}${window.location.search}${window.location.hash}`, {
        locale: next as Locale,
        scroll: false,
      }),
    );
  }

  return (
    <div className={styles.utilities}>
      <a href="https://bigh-vn-demo.vercel.app" className={styles.login}>
        {copy("Log in")}
      </a>
      {/* Sign up stays a placeholder until Mo provides its link. */}
      <button type="button" className={styles.signup} disabled>
        {copy("Sign up")}
      </button>
      <label className={styles.language}>
        <Globe2 size={16} aria-hidden="true" />
        <select
          aria-label={copy("Choose language")}
          value={locale === "hken" ? "cns" : locale}
          disabled={pending}
          onChange={(event) => changeLanguage(event.target.value)}
        >
          {languages.map((language) => (
            <option key={language.locale} value={language.locale} lang={language.tag}>
              {language.name}
            </option>
          ))}
        </select>
        <ChevronDown size={13} aria-hidden="true" />
      </label>
      <span className={styles.status} role="status">
        {pending ? copy("Changing language…") : ""}
      </span>
    </div>
  );
}

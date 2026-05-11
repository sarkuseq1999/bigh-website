import Image from "next/image";
import { Camera, Play, Send, type LucideIcon } from "lucide-react";
import { useTranslations } from "next-intl";

import { Link } from "@/i18n/navigation";

type LinkKey =
  | "about"
  | "careers"
  | "press"
  | "journal"
  | "research"
  | "faq"
  | "privacy"
  | "terms"
  | "shipping";

const COLUMNS: { col: "company" | "resources" | "legal"; keys: LinkKey[] }[] = [
  { col: "company", keys: ["about", "careers", "press"] },
  { col: "resources", keys: ["journal", "research", "faq"] },
  { col: "legal", keys: ["privacy", "terms", "shipping"] },
];

// Lucide v1 ships no brand marks; using neutral placeholders. Swap with real
// brand SVGs (e.g. simple-icons) when those channels exist.
const SOCIALS: { key: "instagram" | "twitter" | "youtube"; Icon: LucideIcon }[] = [
  { key: "instagram", Icon: Camera },
  { key: "twitter", Icon: Send },
  { key: "youtube", Icon: Play },
];

export function SiteFooter() {
  const t = useTranslations("Footer");
  const tBrand = useTranslations("Brand");
  const year = new Date().getFullYear();

  return (
    <footer className="border-foreground/5 bg-card/40 mt-auto border-t">
      <div className="mx-auto max-w-6xl px-6 py-16">
        <div className="grid gap-12 md:grid-cols-[1.5fr_1fr_1fr_1fr]">
          <div>
            <Image
              src="/logo-black.png"
              alt={tBrand("name")}
              width={768}
              height={430}
              className="block h-24 w-auto dark:hidden"
            />
            <Image
              src="/logo-white.png"
              alt={tBrand("name")}
              width={300}
              height={168}
              className="hidden h-24 w-auto dark:block"
            />
            <p className="text-foreground/60 mt-4 max-w-xs text-sm">{t("tagline")}</p>
            <div className="mt-6 flex gap-3">
              {SOCIALS.map(({ key, Icon }) => (
                <a
                  key={key}
                  href="#"
                  aria-label={t(`social.${key}`)}
                  className="border-foreground/10 text-foreground/60 hover:border-brand-900 hover:text-brand-900 flex h-9 w-9 items-center justify-center rounded-full border transition-colors"
                >
                  <Icon className="h-4 w-4" />
                </a>
              ))}
            </div>
          </div>

          {COLUMNS.map(({ col, keys }) => (
            <div key={col}>
              <div className="text-foreground/40 mb-4 text-xs font-semibold tracking-widest uppercase">
                {t(`columns.${col}`)}
              </div>
              <ul className="space-y-3">
                {keys.map((k) => (
                  <li key={k}>
                    <Link
                      href={`/${k}`}
                      className="text-foreground/70 hover:text-foreground text-sm transition-colors"
                    >
                      {t(`links.${k}`)}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="border-foreground/5 text-foreground/50 mt-14 border-t pt-6 text-xs">
          {t("copyright", { year })}
        </div>
      </div>
    </footer>
  );
}

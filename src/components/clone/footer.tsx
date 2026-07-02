import { getTranslations } from "next-intl/server";

import { Link } from "@/i18n/navigation";
import type { Locale } from "@/i18n/routing";
import { PRODUCT_SLUGS, productName } from "@/data/products";

export async function SiteFooter({ locale }: { locale: Locale }) {
  const t = await getTranslations({ locale, namespace: "Footer" });
  const nav = await getTranslations({ locale, namespace: "Nav" });
  const year = new Date().getFullYear();

  return (
    <footer className="mt-24 bg-pine text-porcelain">
      <div className="mx-auto grid max-w-6xl gap-10 px-4 py-14 sm:px-6 md:grid-cols-[1.4fr_1fr_1fr_1fr]">
        <div>
          <p className="font-display text-3xl">BiGH</p>
          <p className="mt-2 max-w-xs text-sm text-porcelain/70">Be in Good Health</p>
          <p className="mt-6 font-mono text-xs uppercase tracking-widest text-celadon">
            {t("madeLine")}
          </p>
        </div>

        <nav aria-label={t("products")}>
          <p className="font-mono text-xs uppercase tracking-widest text-porcelain/60">
            {t("products")}
          </p>
          <ul className="mt-3 space-y-1.5">
            {PRODUCT_SLUGS.map((slug) => (
              <li key={slug}>
                <Link href={`/${slug}`} className="text-sm text-porcelain/85 hover:text-celadon">
                  {productName(slug, locale)}
                </Link>
              </li>
            ))}
          </ul>
        </nav>

        <nav aria-label={t("company")}>
          <p className="font-mono text-xs uppercase tracking-widest text-porcelain/60">
            {t("company")}
          </p>
          <ul className="mt-3 space-y-1.5">
            <li>
              <Link href="/about" className="text-sm text-porcelain/85 hover:text-celadon">
                {nav("aboutBigh")}
              </Link>
            </li>
            <li>
              <Link href="/science" className="text-sm text-porcelain/85 hover:text-celadon">
                {nav("science")}
              </Link>
            </li>
            <li>
              <Link href="/support" className="text-sm text-porcelain/85 hover:text-celadon">
                {nav("support")}
              </Link>
            </li>
            <li>
              <Link href="/opportunity" className="text-sm text-porcelain/85 hover:text-celadon">
                {t("opportunity")}
              </Link>
            </li>
            <li>
              <Link href="/career" className="text-sm text-porcelain/85 hover:text-celadon">
                {t("career")}
              </Link>
            </li>
          </ul>
        </nav>

        <nav aria-label={t("legal")}>
          <p className="font-mono text-xs uppercase tracking-widest text-porcelain/60">
            {t("legal")}
          </p>
          <ul className="mt-3 space-y-1.5">
            <li>
              <Link href="/privacy-notice" className="text-sm text-porcelain/85 hover:text-celadon">
                {t("privacy")}
              </Link>
            </li>
            <li>
              <Link href="/terms-and-conditions" className="text-sm text-porcelain/85 hover:text-celadon">
                {t("terms")}
              </Link>
            </li>
            <li>
              <Link href="/return-policy" className="text-sm text-porcelain/85 hover:text-celadon">
                {t("returns")}
              </Link>
            </li>
          </ul>
        </nav>
      </div>
      <div className="border-t border-porcelain/15">
        <p className="mx-auto max-w-6xl px-4 py-5 text-xs text-porcelain/55 sm:px-6">
          {/* year is substituted in code: ICU {year} args break next-intl 4.11
              message parsing during `next build` static generation */}
          {t("rights").replace("{year}", String(year))}
        </p>
      </div>
    </footer>
  );
}

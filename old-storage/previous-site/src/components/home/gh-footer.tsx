import { getTranslations } from "next-intl/server";

import { Link } from "@/i18n/navigation";
import type { Locale } from "@/i18n/routing";
import { GH_PRODUCT_SLUGS, productName } from "@/data/products";

// Golden Hour footer — quiet close of the scroll. Brand line, the six
// products, company links, legal + the DSHEA disclaimer (required near
// any product claims; keep it here always).
export async function GhFooter({ locale }: { locale: Locale }) {
  const nav = await getTranslations({ locale, namespace: "Nav" });
  const t = await getTranslations({ locale, namespace: "Footer" });
  const home = await getTranslations({ locale, namespace: "Home" });
  const year = new Date().getFullYear();

  return (
    <footer className="border-t border-[color:var(--gh-line)] px-6 pb-10 pt-16 sm:px-12">
      <div className="mx-auto max-w-7xl">
        <div className="grid gap-12 md:grid-cols-[1.4fr_1fr_1fr]">
          {/* brand */}
          <div>
            <p className="gh-serif text-[28px] leading-none text-[color:var(--gh-fg)]">
              BiGH
            </p>
            <p className="mt-3 max-w-xs text-[15px] leading-relaxed text-[color:var(--gh-muted)]">
              {home("footer.brandLine")}
            </p>
            <p className="mt-4 text-[11px] uppercase tracking-[0.22em] text-[color:var(--gh-faint)]">
              {t("madeLine")}
            </p>
          </div>

          {/* products */}
          <nav aria-label={t("products")}>
            <p className="text-[11px] uppercase tracking-[0.22em] text-[color:var(--gh-faint)]">
              {t("products")}
            </p>
            <ul className="mt-4 space-y-2">
              {GH_PRODUCT_SLUGS.map((slug) => (
                <li key={slug}>
                  <Link
                    href={`/${slug}`}
                    className="text-[15px] text-[color:var(--gh-muted)] transition-colors hover:text-[color:var(--gh-fg)]"
                  >
                    {productName(slug, locale)}
                  </Link>
                </li>
              ))}
            </ul>
          </nav>

          {/* company + legal */}
          <nav aria-label={t("company")}>
            <p className="text-[11px] uppercase tracking-[0.22em] text-[color:var(--gh-faint)]">
              {t("company")}
            </p>
            <ul className="mt-4 space-y-2">
              <li>
                <Link href="/science" className="text-[15px] text-[color:var(--gh-muted)] transition-colors hover:text-[color:var(--gh-fg)]">
                  {nav("science")}
                </Link>
              </li>
              <li>
                <Link href="/about" className="text-[15px] text-[color:var(--gh-muted)] transition-colors hover:text-[color:var(--gh-fg)]">
                  {nav("aboutBigh")}
                </Link>
              </li>
              <li>
                <Link href="/support" className="text-[15px] text-[color:var(--gh-muted)] transition-colors hover:text-[color:var(--gh-fg)]">
                  {nav("support")}
                </Link>
              </li>
              <li>
                <Link href="/privacy-notice" className="text-[15px] text-[color:var(--gh-muted)] transition-colors hover:text-[color:var(--gh-fg)]">
                  {t("privacy")}
                </Link>
              </li>
              <li>
                <Link href="/terms-and-conditions" className="text-[15px] text-[color:var(--gh-muted)] transition-colors hover:text-[color:var(--gh-fg)]">
                  {t("terms")}
                </Link>
              </li>
            </ul>
          </nav>
        </div>

        {/* DSHEA disclaimer — stays with the brand wherever products appear */}
        <p className="mt-14 max-w-3xl border-l border-[color:var(--gh-line)] pl-4 text-[12px] leading-relaxed text-[color:var(--gh-faint)]">
          {t("disclaimer")}
        </p>

        <p className="mt-8 text-[12px] text-[color:var(--gh-faint)]">
          {t("rights", { year })}
        </p>
      </div>
    </footer>
  );
}

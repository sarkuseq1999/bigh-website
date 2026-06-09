import { useTranslations } from "next-intl";

import { Link } from "@/i18n/navigation";

/* ─── column definitions ───────────────────────────────────────────── */
type ProductKey = "nuricell" | "system" | "science" | "quiz";
type CompanyKey = "about" | "founder" | "research" | "contact";

const PRODUCT_LINKS: ProductKey[] = ["nuricell", "system", "science", "quiz"];
const PRODUCT_HREFS: Record<ProductKey, string> = {
  nuricell: "#",
  system: "#system",
  science: "#science",
  quiz: "#",
};

const COMPANY_LINKS: CompanyKey[] = ["about", "founder", "research", "contact"];
const COMPANY_HREFS: Record<CompanyKey, string> = {
  about: "#",
  founder: "#",
  research: "#",
  contact: "#",
};

/* ─── language stub ────────────────────────────────────────────────── */
type LangCode = "en" | "ko" | "vi" | "zh";
const LANGS: LangCode[] = ["en", "ko", "vi", "zh"];

export function SiteFooter() {
  const t = useTranslations("Footer");
  const tNav = useTranslations("Nav");
  const tBrand = useTranslations("Brand");
  const tLangs = useTranslations("Languages");

  // Server component — compute year directly
  const year = new Date().getFullYear();

  return (
    <footer className="bg-paper-2 border-t border-line mt-auto">
      <div className="mx-auto max-w-6xl px-6 py-16">

        {/* ── four-column grid ── */}
        <div className="grid gap-12 sm:grid-cols-2 lg:grid-cols-[1.6fr_1fr_1fr_1.4fr]">

          {/* col 1: brand + mission */}
          <div>
            <Link
              href="/"
              className="font-display text-ink text-xl font-semibold tracking-tight focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-amber"
            >
              {tBrand("name")}
            </Link>
            <p className="text-ink-soft mt-4 max-w-xs text-sm leading-relaxed">
              {t("mission")}
            </p>
          </div>

          {/* col 2: product links */}
          <div>
            <h3 className="font-mono text-ink-soft mb-4 text-xs font-semibold tracking-widest uppercase">
              {t("columns.product")}
            </h3>
            <ul className="space-y-3">
              {PRODUCT_LINKS.map((key) => (
                <li key={key}>
                  <a
                    href={PRODUCT_HREFS[key]}
                    className="text-ink-soft hover:text-ink text-sm transition-colors duration-150 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-amber"
                  >
                    {t(`links.${key}`)}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* col 3: company links */}
          <div>
            <h3 className="font-mono text-ink-soft mb-4 text-xs font-semibold tracking-widest uppercase">
              {t("columns.company")}
            </h3>
            <ul className="space-y-3">
              {COMPANY_LINKS.map((key) => (
                <li key={key}>
                  <a
                    href={COMPANY_HREFS[key]}
                    className="text-ink-soft hover:text-ink text-sm transition-colors duration-150 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-amber"
                  >
                    {t(`links.${key}`)}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* col 4: language toggle + newsletter */}
          <div>
            {/* language toggle */}
            <h3 className="font-mono text-ink-soft mb-3 text-xs font-semibold tracking-widest uppercase">
              {tNav("language")}
            </h3>
            <div className="mb-8 flex flex-wrap gap-2">
              {LANGS.map((code) => {
                const isActive = code === "en";
                return (
                  <a
                    key={code}
                    href="#"
                    aria-current={isActive ? "true" : undefined}
                    className={[
                      "font-mono rounded-full border px-3.5 py-1.5 text-xs transition-colors duration-150 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-amber",
                      isActive
                        ? "bg-ink text-paper border-ink"
                        : "text-ink-soft border-line hover:border-ink hover:text-ink",
                    ].join(" ")}
                  >
                    {tLangs(code)}
                  </a>
                );
              })}
            </div>

            {/* newsletter mini-signup */}
            <p id="newsletter" className="text-ink mb-3 scroll-mt-24 text-sm font-semibold">
              {t("newsletter.title")}
            </p>
            <form
              className="flex flex-col gap-2"
              aria-label={t("newsletter.title")}
            >
              <input
                type="email"
                placeholder={t("newsletter.placeholder")}
                aria-label={t("newsletter.placeholder")}
                className="bg-paper text-ink placeholder:text-ink-soft border-line focus:border-ink w-full rounded-lg border px-4 py-2.5 text-sm outline-none transition-colors duration-150 focus-visible:ring-2 focus-visible:ring-amber"
              />
              <button
                type="submit"
                className="bg-amber hover:bg-amber-hi text-ink w-full rounded-full py-2.5 text-sm font-semibold transition-colors duration-150 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-amber"
              >
                {t("newsletter.cta")}
              </button>
            </form>
          </div>
        </div>

        {/* ── FDA disclaimer ── */}
        <div className="border-line mt-14 border-t pt-8">
          <p className="text-ink-soft text-xs leading-relaxed">
            {t("disclaimer")}
          </p>
        </div>

        {/* ── copyright ── */}
        <div className="text-ink-soft mt-4 text-xs">
          {t("copyright", { year })}
        </div>
      </div>
    </footer>
  );
}

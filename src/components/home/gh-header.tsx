"use client";

import { useEffect, useRef, useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import { useParams } from "next/navigation";

import { Link, usePathname, useRouter } from "@/i18n/navigation";
import type { Locale } from "@/i18n/routing";
import { GH_PRODUCT_SLUGS, productName } from "@/data/products";

const LOGIN_URL = "https://aeg.imatrixoffice.com";

const LANGS: { code: Locale; label: string }[] = [
  { code: "en", label: "English" },
  { code: "kr", label: "한국어" },
  { code: "jp", label: "日本語" },
  { code: "cns", label: "中文(简体)" },
  { code: "hken", label: "中文(香港)" },
  { code: "vn", label: "Tiếng Việt" },
];

function GhLangSwitcher() {
  const locale = useLocale();
  const t = useTranslations("Nav");
  const router = useRouter();
  const pathname = usePathname();
  const params = useParams();

  return (
    <label className="flex items-center gap-1.5 text-[13px] text-[color:var(--gh-muted)]">
      <span className="sr-only">{t("language")}</span>
      <svg
        aria-hidden
        viewBox="0 0 24 24"
        className="h-4 w-4"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.5"
      >
        <circle cx="12" cy="12" r="9" />
        <path d="M3 12h18M12 3c2.5 2.6 3.8 5.7 3.8 9S14.5 18.4 12 21c-2.5-2.6-3.8-5.7-3.8-9S9.5 5.6 12 3z" />
      </svg>
      <select
        className="cursor-pointer appearance-none bg-transparent pr-1 outline-none [&>option]:text-[#17171f]"
        value={locale}
        onChange={(e) => {
          const next = e.target.value as Locale;
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

// Golden Hour chrome — a quiet, transparent bar over the dark scroll.
// Wordmark left; Products / Science / About / Support center-right;
// language + Login/Sign-up at the edge. Nothing borrowed from the clone.
export function GhHeader() {
  const nav = useTranslations("Nav");
  const locale = useLocale() as Locale;
  const [productsOpen, setProductsOpen] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const productsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!productsOpen) return;
    const onDown = (e: PointerEvent) => {
      if (!productsRef.current?.contains(e.target as Node)) {
        setProductsOpen(false);
      }
    };
    window.addEventListener("pointerdown", onDown);
    return () => window.removeEventListener("pointerdown", onDown);
  }, [productsOpen]);

  const links = (
    <>
      <div
        ref={productsRef}
        className="relative"
        onMouseEnter={() => setProductsOpen(true)}
        onMouseLeave={() => setProductsOpen(false)}
      >
        <button
          type="button"
          onClick={() => setProductsOpen((v) => !v)}
          className="flex items-center gap-1 py-2 text-[13px] uppercase tracking-[0.18em] text-[color:var(--gh-muted)] transition-colors hover:text-[color:var(--gh-fg)]"
        >
          {nav("products")}
          <span aria-hidden className="text-[9px]">
            ▾
          </span>
        </button>
        {productsOpen && (
          <div className="absolute left-1/2 top-full z-30 w-60 -translate-x-1/2 rounded-lg border border-[color:var(--gh-line)] bg-[#070d17]/95 py-2 shadow-2xl backdrop-blur-md">
            {GH_PRODUCT_SLUGS.map((slug) => (
              <Link
                key={slug}
                href={`/${slug}`}
                className="block px-5 py-2.5 text-sm text-[color:var(--gh-muted)] transition-colors hover:bg-white/5 hover:text-[color:var(--gh-fg)]"
                onClick={() => setProductsOpen(false)}
              >
                {productName(slug, locale)}
              </Link>
            ))}
          </div>
        )}
      </div>
      <Link
        href="/science"
        className="py-2 text-[13px] uppercase tracking-[0.18em] text-[color:var(--gh-muted)] transition-colors hover:text-[color:var(--gh-fg)]"
      >
        {nav("science")}
      </Link>
      <Link
        href="/about"
        className="py-2 text-[13px] uppercase tracking-[0.18em] text-[color:var(--gh-muted)] transition-colors hover:text-[color:var(--gh-fg)]"
      >
        {nav("about")}
      </Link>
      <Link
        href="/support"
        className="py-2 text-[13px] uppercase tracking-[0.18em] text-[color:var(--gh-muted)] transition-colors hover:text-[color:var(--gh-fg)]"
      >
        {nav("support")}
      </Link>
    </>
  );

  return (
    <header className="absolute inset-x-0 top-0 z-20">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-6 px-6 py-6 sm:px-12">
        {/* wordmark */}
        <Link href="/" className="group flex items-baseline gap-2">
          <span className="gh-serif text-[26px] leading-none tracking-tight text-[color:var(--gh-fg)]">
            BiGH
          </span>
          <span className="hidden text-[10px] uppercase tracking-[0.28em] text-[color:var(--gh-faint)] sm:inline">
            Be in Good Health
          </span>
        </Link>

        {/* desktop nav */}
        <nav className="hidden items-center gap-7 md:flex">{links}</nav>

        <div className="hidden items-center gap-5 md:flex">
          <GhLangSwitcher />
          <span aria-hidden className="h-4 w-px bg-[color:var(--gh-line)]" />
          <a
            href={LOGIN_URL}
            className="text-[13px] uppercase tracking-[0.18em] text-[color:var(--gh-muted)] transition-colors hover:text-[color:var(--gh-fg)]"
          >
            {nav("login")}
          </a>
          <Link
            href="/signup"
            className="rounded-full border border-[color:var(--gh-line)] px-4 py-2 text-[13px] uppercase tracking-[0.18em] text-[color:var(--gh-fg)] transition-colors hover:border-[color:var(--gh-ember)] hover:text-[color:var(--gh-ember)]"
          >
            {nav("signup")}
          </Link>
        </div>

        {/* mobile toggle */}
        <button
          type="button"
          className="flex h-10 w-10 flex-col items-center justify-center gap-[5px] md:hidden"
          aria-label={nav("menu")}
          aria-expanded={menuOpen}
          onClick={() => setMenuOpen((v) => !v)}
        >
          <span
            className={`h-px w-5 bg-[color:var(--gh-fg)] transition-transform ${menuOpen ? "translate-y-[3px] rotate-45" : ""}`}
          />
          <span
            className={`h-px w-5 bg-[color:var(--gh-fg)] transition-transform ${menuOpen ? "-translate-y-[3px] -rotate-45" : ""}`}
          />
        </button>
      </div>

      {/* mobile panel */}
      {menuOpen && (
        <div className="mx-4 rounded-xl border border-[color:var(--gh-line)] bg-[#070d17]/95 p-6 shadow-2xl backdrop-blur-md md:hidden">
          <nav className="flex flex-col gap-1">
            {GH_PRODUCT_SLUGS.map((slug) => (
              <Link
                key={slug}
                href={`/${slug}`}
                className="py-2 text-base text-[color:var(--gh-muted)]"
                onClick={() => setMenuOpen(false)}
              >
                {productName(slug, locale)}
              </Link>
            ))}
            <span className="my-3 h-px w-full bg-[color:var(--gh-line)]" />
            <Link href="/science" className="py-2 text-base text-[color:var(--gh-muted)]" onClick={() => setMenuOpen(false)}>
              {nav("science")}
            </Link>
            <Link href="/about" className="py-2 text-base text-[color:var(--gh-muted)]" onClick={() => setMenuOpen(false)}>
              {nav("about")}
            </Link>
            <Link href="/support" className="py-2 text-base text-[color:var(--gh-muted)]" onClick={() => setMenuOpen(false)}>
              {nav("support")}
            </Link>
            <span className="my-3 h-px w-full bg-[color:var(--gh-line)]" />
            <div className="flex items-center justify-between">
              <GhLangSwitcher />
              <div className="flex items-center gap-4">
                <a href={LOGIN_URL} className="text-sm text-[color:var(--gh-muted)]">
                  {nav("login")}
                </a>
                <Link
                  href="/signup"
                  className="rounded-full border border-[color:var(--gh-line)] px-4 py-1.5 text-sm text-[color:var(--gh-fg)]"
                  onClick={() => setMenuOpen(false)}
                >
                  {nav("signup")}
                </Link>
              </div>
            </div>
          </nav>
        </div>
      )}
    </header>
  );
}

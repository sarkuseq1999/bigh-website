"use client";

import Image from "next/image";
import { useLocale, useTranslations } from "next-intl";
import { useEffect, useRef, useState } from "react";

import { Link, usePathname } from "@/i18n/navigation";
import type { Locale } from "@/i18n/routing";
import { ABOUT_SLUGS, PRODUCT_SLUGS, productName } from "@/data/products";

import { LangSwitcher } from "./lang-switcher";

const LOGIN_URL = "https://aeg.imatrixoffice.com";

function Dropdown({
  label,
  items,
}: {
  label: string;
  items: { href: string; label: string }[];
}) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    const onDown = (e: PointerEvent) => {
      if (!ref.current?.contains(e.target as Node)) setOpen(false);
    };
    window.addEventListener("pointerdown", onDown);
    return () => window.removeEventListener("pointerdown", onDown);
  }, [open]);

  return (
    <div
      ref={ref}
      className="relative"
      onMouseEnter={() => setOpen(true)}
      onMouseLeave={() => setOpen(false)}
    >
      <button
        type="button"
        className="flex items-center gap-1 rounded-full px-4 py-1.5 text-[15px] font-medium text-white/90 transition-colors hover:bg-green hover:text-white"
        aria-expanded={open}
        onClick={() => setOpen((v) => !v)}
      >
        {label}
        <svg aria-hidden viewBox="0 0 12 12" className="h-3 w-3 opacity-70">
          <path d="M2 4l4 4 4-4" fill="none" stroke="currentColor" strokeWidth="1.5" />
        </svg>
      </button>
      {open && (
        <div className="absolute left-1/2 top-full z-50 w-64 -translate-x-1/2 pt-2">
          <ul className="rounded-lg border border-white/10 bg-ink-dark/95 p-2 shadow-[0_16px_40px_rgba(0,0,0,0.4)] backdrop-blur">
            {items.map((item) => (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className="block rounded-md px-3 py-2 text-[15px] text-white/85 hover:bg-green hover:text-white"
                  onClick={() => setOpen(false)}
                >
                  {item.label}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export function SiteHeader() {
  const t = useTranslations("Nav");
  const locale = useLocale() as Locale;
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);

  const productItems = PRODUCT_SLUGS.map((slug) => ({
    href: `/${slug}`,
    label: productName(slug, locale),
  }));
  const aboutLabels: Record<(typeof ABOUT_SLUGS)[number], string> = {
    about: t("aboutBigh"),
    organic: t("organic"),
    "non-gmo": t("nonGmo"),
    "gluten-free": t("glutenFree"),
    vegan: t("vegan"),
  };
  const aboutItems = ABOUT_SLUGS.map((slug) => ({ href: `/${slug}`, label: aboutLabels[slug] }));

  return (
    <header className="sticky top-0 z-40 bg-ink-dark/95 backdrop-blur">
      {/* top microbar, as on the original */}
      <div className="border-b border-white/10">
        <div className="mx-auto flex h-8 max-w-6xl items-center justify-end gap-1 px-4 text-xs text-white/70 sm:px-6">
          <span aria-hidden>|</span>
          <a href={LOGIN_URL} className="px-1.5 font-semibold hover:text-green">
            {t("login")}
          </a>
          <span aria-hidden>|</span>
          <Link href="/signup" className="px-1.5 font-semibold hover:text-green">
            {t("signup")}
          </Link>
          <span aria-hidden>|</span>
        </div>
      </div>

      <div className="mx-auto flex h-[4.5rem] max-w-6xl items-center justify-between gap-4 px-4 sm:px-6">
        <Link href="/" className="flex shrink-0 items-center" aria-label="BiGH — Home">
          <Image
            src="/original/uploads/2019/04/logo_white_97.png"
            alt="BiGH — Be in Good Health"
            width={110}
            height={62}
            priority
            className="h-12 w-auto"
          />
        </Link>

        <nav className="hidden items-center gap-1 lg:flex" aria-label="Main">
          <Link
            href="/"
            className={`rounded-full px-4 py-1.5 text-[15px] font-medium transition-colors ${
              pathname === "/" ? "bg-green text-white" : "text-white/90 hover:bg-green hover:text-white"
            }`}
          >
            {t("home")}
          </Link>
          <Dropdown label={t("products")} items={productItems} />
          <Dropdown label={t("about")} items={aboutItems} />
          <Link
            href="/science"
            className="rounded-full px-4 py-1.5 text-[15px] font-medium text-white/90 transition-colors hover:bg-green hover:text-white"
          >
            {t("science")}
          </Link>
          <Link
            href="/support"
            className="rounded-full px-4 py-1.5 text-[15px] font-medium text-white/90 transition-colors hover:bg-green hover:text-white"
          >
            {t("support")}
          </Link>
          <div className="ml-3 border-l border-white/15 pl-4">
            <LangSwitcher dark />
          </div>
        </nav>

        <button
          type="button"
          className="rounded-lg border border-white/20 p-2 text-white lg:hidden"
          aria-expanded={mobileOpen}
          aria-label={t("menu")}
          onClick={() => setMobileOpen((v) => !v)}
        >
          <svg aria-hidden viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="1.8">
            {mobileOpen ? <path d="M5 5l14 14M19 5L5 19" /> : <path d="M4 7h16M4 12h16M4 17h16" />}
          </svg>
        </button>
      </div>

      {mobileOpen && (
        <div className="border-t border-white/10 bg-ink-dark px-4 pb-6 pt-3 lg:hidden">
          <p className="pb-1 pt-2 text-xs font-semibold uppercase tracking-widest text-white/50">
            {t("products")}
          </p>
          <ul className="grid grid-cols-2 gap-x-4">
            {productItems.map((item) => (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className="block py-1.5 text-[15px] text-white/85"
                  onClick={() => setMobileOpen(false)}
                >
                  {item.label}
                </Link>
              </li>
            ))}
          </ul>
          <p className="pb-1 pt-4 text-xs font-semibold uppercase tracking-widest text-white/50">
            {t("about")}
          </p>
          <ul className="grid grid-cols-2 gap-x-4">
            {[...aboutItems, { href: "/science", label: t("science") }, { href: "/support", label: t("support") }].map(
              (item) => (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    className="block py-1.5 text-[15px] text-white/85"
                    onClick={() => setMobileOpen(false)}
                  >
                    {item.label}
                  </Link>
                </li>
              ),
            )}
          </ul>
          <div className="mt-5 flex items-center justify-between border-t border-white/10 pt-4">
            <LangSwitcher dark />
            <div className="flex items-center gap-3">
              <a href={LOGIN_URL} className="text-[15px] font-medium text-white/85">
                {t("login")}
              </a>
              <Link
                href="/signup"
                className="rounded-full bg-green px-4 py-1.5 text-[15px] font-medium text-white"
                onClick={() => setMobileOpen(false)}
              >
                {t("signup")}
              </Link>
            </div>
          </div>
        </div>
      )}
    </header>
  );
}

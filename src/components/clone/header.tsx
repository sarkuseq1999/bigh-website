"use client";

import Image from "next/image";
import { useLocale, useTranslations } from "next-intl";
import { useEffect, useRef, useState } from "react";

import { Link } from "@/i18n/navigation";
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
        className="flex items-center gap-1 py-2 text-[15px] font-medium text-pine transition-colors hover:text-celadon-deep"
        aria-expanded={open}
        onClick={() => setOpen((v) => !v)}
      >
        {label}
        <svg aria-hidden viewBox="0 0 12 12" className="h-3 w-3 opacity-60">
          <path d="M2 4l4 4 4-4" fill="none" stroke="currentColor" strokeWidth="1.5" />
        </svg>
      </button>
      {open && (
        <div className="absolute left-1/2 top-full z-50 w-60 -translate-x-1/2 pt-2">
          <ul className="rounded-xl border border-line bg-porcelain p-2 shadow-[0_16px_40px_rgba(23,52,43,0.12)]">
            {items.map((item) => (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className="block rounded-lg px-3 py-2 text-[15px] text-pine hover:bg-hanji hover:text-celadon-deep"
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
    <header className="sticky top-0 z-40 border-b border-line bg-porcelain/90 backdrop-blur">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between gap-4 px-4 sm:px-6">
        <Link href="/" className="flex shrink-0 items-center" aria-label="BiGH — Home">
          <Image
            src="/original/uploads/2019/01/Black-Logo-300x168.png"
            alt="BiGH"
            width={84}
            height={47}
            priority
          />
        </Link>

        <nav className="hidden items-center gap-6 lg:flex" aria-label="Main">
          <Dropdown label={t("products")} items={productItems} />
          <Dropdown label={t("about")} items={aboutItems} />
          <Link href="/science" className="py-2 text-[15px] font-medium text-pine hover:text-celadon-deep">
            {t("science")}
          </Link>
          <Link href="/support" className="py-2 text-[15px] font-medium text-pine hover:text-celadon-deep">
            {t("support")}
          </Link>
        </nav>

        <div className="hidden items-center gap-4 lg:flex">
          <LangSwitcher />
          <a
            href={LOGIN_URL}
            className="text-[15px] font-medium text-pine hover:text-celadon-deep"
          >
            {t("login")}
          </a>
          <Link
            href="/signup"
            className="rounded-full bg-pine px-4 py-1.5 text-[15px] font-medium text-porcelain transition-colors hover:bg-celadon-deep"
          >
            {t("signup")}
          </Link>
        </div>

        <button
          type="button"
          className="rounded-lg border border-line p-2 lg:hidden"
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
        <div className="border-t border-line bg-porcelain px-4 pb-6 pt-3 lg:hidden">
          <p className="pb-1 pt-2 font-mono text-xs uppercase tracking-widest text-pine-soft">
            {t("products")}
          </p>
          <ul className="grid grid-cols-2 gap-x-4">
            {productItems.map((item) => (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className="block py-1.5 text-[15px] text-pine"
                  onClick={() => setMobileOpen(false)}
                >
                  {item.label}
                </Link>
              </li>
            ))}
          </ul>
          <p className="pb-1 pt-4 font-mono text-xs uppercase tracking-widest text-pine-soft">
            {t("about")}
          </p>
          <ul className="grid grid-cols-2 gap-x-4">
            {[...aboutItems, { href: "/science", label: t("science") }, { href: "/support", label: t("support") }].map(
              (item) => (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    className="block py-1.5 text-[15px] text-pine"
                    onClick={() => setMobileOpen(false)}
                  >
                    {item.label}
                  </Link>
                </li>
              ),
            )}
          </ul>
          <div className="mt-5 flex items-center justify-between border-t border-line pt-4">
            <LangSwitcher />
            <div className="flex items-center gap-3">
              <a href={LOGIN_URL} className="text-[15px] font-medium text-pine">
                {t("login")}
              </a>
              <Link
                href="/signup"
                className="rounded-full bg-pine px-4 py-1.5 text-[15px] font-medium text-porcelain"
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

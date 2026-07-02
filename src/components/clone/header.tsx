"use client";

import Image from "next/image";
import { useLocale, useTranslations } from "next-intl";
import { useEffect, useRef, useState } from "react";

import { Link, usePathname } from "@/i18n/navigation";
import type { Locale } from "@/i18n/routing";
import { ABOUT_SLUGS, PRODUCT_SLUGS, productName } from "@/data/products";

import { LangSwitcher } from "./lang-switcher";

const LOGIN_URL = "https://aeg.imatrixoffice.com";

// Measured from the original (1440px): header floats transparently over the
// page — 26px microbar + 109px main row; logo 157x88 at the content edge;
// nav items Roboto 600 24px with 13x20 padding; FOUR top-level items
// (Science lives in the About dropdown). Mobile: 185px row w/ 292px logo.
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
        className="flex items-center gap-1 rounded-[5px] px-5 py-[13px] text-2xl font-semibold leading-none text-[#efefef] transition-colors hover:bg-green hover:text-white"
        aria-expanded={open}
        onClick={() => setOpen((v) => !v)}
      >
        {label}
      </button>
      {open && (
        <div className="absolute left-1/2 top-full z-50 w-72 -translate-x-1/2 pt-1">
          <ul className="rounded-md border border-white/10 bg-[#1d1d25]/95 p-2 shadow-[0_16px_40px_rgba(0,0,0,0.4)] backdrop-blur">
            {items.map((item) => (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className="block rounded px-3 py-2 text-lg text-white/85 hover:bg-green hover:text-white"
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
  const aboutItems = [
    ...ABOUT_SLUGS.map((slug) => ({ href: `/${slug}`, label: aboutLabels[slug] })),
    { href: "/science", label: t("science") },
  ];

  return (
    <header className="absolute left-0 top-0 z-40 w-full">
      {/* 26px microbar: Login | Sign Up (+ language) */}
      <div className="mx-auto flex h-[26px] max-w-[70rem] items-center justify-end gap-1 px-4 text-xs text-white/80 sm:px-6">
        <div className="mr-3">
          <LangSwitcher dark />
        </div>
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

      {/* main row: 109px desktop / 185px mobile, translucent black */}
      <div className="bg-black/55">
        <div className="mx-auto flex max-w-[70rem] items-center justify-between gap-4 px-2.5 py-[10px] sm:px-6 lg:h-[109px] lg:py-0">
          <Link href="/" className="flex shrink-0 items-center" aria-label="BiGH — Home">
            <Image
              src="/original/uploads/2019/04/logo_white_97.png"
              alt="BiGH — Be in Good Health"
              width={292}
              height={164}
              priority
              className="h-auto w-[292px] max-w-[75vw] lg:h-[88px] lg:w-[157px]"
            />
          </Link>

          <nav className="hidden items-center lg:flex" aria-label="Main">
            <Link
              href="/"
              className={`rounded-[5px] px-5 py-[13px] text-2xl font-semibold leading-none transition-colors ${
                pathname === "/" ? "bg-green text-white" : "text-[#efefef] hover:bg-green hover:text-white"
              }`}
            >
              {t("home")}
            </Link>
            <Dropdown label={t("products")} items={productItems} />
            <Dropdown label={t("about")} items={aboutItems} />
            <Link
              href="/support"
              className="rounded-[5px] px-5 py-[13px] text-2xl font-semibold leading-none text-[#efefef] transition-colors hover:bg-green hover:text-white"
            >
              {t("support")}
            </Link>
          </nav>

          <button
            type="button"
            className="p-2 text-white lg:hidden"
            aria-expanded={mobileOpen}
            aria-label={t("menu")}
            onClick={() => setMobileOpen((v) => !v)}
          >
            <svg aria-hidden viewBox="0 0 24 24" className="h-8 w-8" fill="none" stroke="currentColor" strokeWidth="2">
              {mobileOpen ? <path d="M5 5l14 14M19 5L5 19" /> : <path d="M4 7h16M4 12h16M4 17h16" />}
            </svg>
          </button>
        </div>
      </div>

      {mobileOpen && (
        <div className="bg-[#1d1d25]/95 px-4 pb-6 pt-3 backdrop-blur lg:hidden">
          <ul>
            <li>
              <Link href="/" className="block py-2 text-lg font-semibold text-white" onClick={() => setMobileOpen(false)}>
                {t("home")}
              </Link>
            </li>
          </ul>
          <p className="pb-1 pt-3 text-xs font-semibold uppercase tracking-widest text-white/50">
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
            {[...aboutItems, { href: "/support", label: t("support") }].map((item) => (
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
          <div className="mt-5 flex items-center justify-between border-t border-white/10 pt-4">
            <LangSwitcher dark />
            <div className="flex items-center gap-3">
              <a href={LOGIN_URL} className="text-[15px] font-medium text-white/85">
                {t("login")}
              </a>
              <Link
                href="/signup"
                className="rounded bg-green px-4 py-1.5 text-[15px] font-medium text-white"
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

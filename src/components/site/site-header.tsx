"use client";

import { useEffect, useRef, useState } from "react";
import { ChevronDown, Menu, X } from "lucide-react";
import { useTranslations } from "next-intl";
import { AnimatePresence, motion } from "motion/react";
import { useReducedMotionSafe } from "@/components/site/use-reduced-motion-safe";

import { Link } from "@/i18n/navigation";

/* ─── language config ───────────────────────────────────────────────── */
type LangCode = "en" | "ko" | "vi" | "zh";
const LANGS: { code: LangCode; key: keyof { en: string; ko: string; vi: string; zh: string } }[] =
  [
    { code: "en", key: "en" },
    { code: "ko", key: "ko" },
    { code: "vi", key: "vi" },
    { code: "zh", key: "zh" },
  ];

/* ─── nav links ───────────────────────────────────────────────────────
   "quiz" lives only in the CTA link — a nav item AND a pill for the same
   destination reads as three doors to one room. */
const NAV_ITEMS: { key: "science" | "products"; href: string }[] = [
  { key: "science", href: "#science" },
  { key: "products", href: "#system" },
];

export function SiteHeader() {
  const tNav = useTranslations("Nav");
  const tBrand = useTranslations("Brand");
  const tLangs = useTranslations("Languages");

  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [langOpen, setLangOpen] = useState(false);
  const langRef = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotionSafe();

  /* close the language menu on outside click */
  useEffect(() => {
    if (!langOpen) return;
    const onDown = (e: MouseEvent) => {
      if (langRef.current && !langRef.current.contains(e.target as Node)) {
        setLangOpen(false);
      }
    };
    document.addEventListener("mousedown", onDown);
    return () => document.removeEventListener("mousedown", onDown);
  }, [langOpen]);

  /* scroll sentinel -------------------------------------------------- */
  const sentinelRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const el = sentinelRef.current;
    if (!el) return;
    const obs = new IntersectionObserver(
      ([entry]) => setScrolled(!entry.isIntersecting),
      { threshold: 0 },
    );
    obs.observe(el);
    return () => obs.disconnect();
  }, []);

  /* lock body scroll when mobile menu is open */
  useEffect(() => {
    document.body.style.overflow = mobileOpen ? "hidden" : "";
    return () => { document.body.style.overflow = ""; };
  }, [mobileOpen]);

  return (
    <>
      {/* sentinel placed just below the fold so the header knows it has been scrolled past */}
      <div ref={sentinelRef} aria-hidden className="pointer-events-none absolute top-[100dvh] h-px w-full" />

      {/* The header always keeps its own solid band — a transparent nav over
          the hero photograph collided with the image edge. */}
      <header
        className={[
          "fixed top-0 right-0 left-0 z-50 w-full transition-shadow duration-300",
          "bg-paper/95 border-b border-line backdrop-blur-md",
          scrolled ? "shadow-[0_1px_0_0_var(--color-line)]" : "",
        ].join(" ")}
      >
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">

          {/* ── wordmark ── */}
          <Link
            href="/"
            aria-label={tBrand("name")}
            className="font-display text-ink text-xl font-semibold tracking-tight select-none focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-amber"
          >
            {tBrand("name")}
          </Link>

          {/* ── desktop nav ── */}
          <nav aria-label="Main navigation" className="hidden items-center gap-7 md:flex">
            {NAV_ITEMS.map(({ key, href }) => (
              <a
                key={key}
                href={href}
                className="text-ink-soft hover:text-ink min-h-[48px] flex items-center text-base font-medium transition-colors duration-150 focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-amber"
              >
                {tNav(key)}
              </a>
            ))}

            {/* language switcher — one compact dropdown, not four loose links */}
            <div ref={langRef} className="relative">
              <button
                type="button"
                aria-haspopup="listbox"
                aria-expanded={langOpen}
                aria-label={tNav("language")}
                onClick={() => setLangOpen((o) => !o)}
                className="font-mono text-ink-soft hover:text-ink flex min-h-[48px] items-center gap-1 px-2 text-xs tracking-wide transition-colors duration-150 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-amber"
              >
                EN
                <ChevronDown className="size-3" aria-hidden />
              </button>
              {langOpen && (
                <div
                  role="listbox"
                  aria-label={tNav("language")}
                  className="bg-paper border-line absolute right-0 top-full z-50 min-w-[10rem] rounded-xl border p-1 shadow-lg"
                >
                  {LANGS.map(({ code, key }) => {
                    const isActive = code === "en";
                    return (
                      <a
                        key={code}
                        href="#"
                        role="option"
                        aria-selected={isActive}
                        onClick={() => setLangOpen(false)}
                        className={[
                          "flex min-h-[40px] items-center rounded-lg px-3 text-sm transition-colors duration-150",
                          isActive
                            ? "text-ink font-semibold"
                            : "text-ink-soft hover:text-ink hover:bg-paper-2",
                        ].join(" ")}
                      >
                        {tLangs(key)}
                      </a>
                    );
                  })}
                </div>
              )}
            </div>

            {/* CTA — quiet text link; the hero owns the loud version */}
            <a
              href="#quiz"
              className="text-ink inline-flex min-h-[48px] items-center text-sm font-semibold underline-offset-4 transition-colors duration-150 hover:underline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-amber"
            >
              {tNav("cta")}
            </a>
          </nav>

          {/* ── mobile hamburger ── */}
          <button
            aria-label={mobileOpen ? tNav("closeMenu") : tNav("openMenu")}
            aria-expanded={mobileOpen}
            aria-controls="mobile-nav-sheet"
            onClick={() => setMobileOpen((o) => !o)}
            className="text-ink flex h-12 w-12 items-center justify-center rounded-full transition-colors duration-150 hover:bg-black/5 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-amber md:hidden"
          >
            {mobileOpen ? <X className="size-5" /> : <Menu className="size-5" />}
          </button>
        </div>
      </header>

      {/* ── mobile sheet ── */}
      <AnimatePresence>
        {mobileOpen && (
          <>
            {/* backdrop */}
            <motion.div
              key="backdrop"
              aria-hidden
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: reduce ? 0 : 0.2 }}
              onClick={() => setMobileOpen(false)}
              className="fixed inset-0 z-40 bg-ink/30 md:hidden"
            />

            {/* sheet panel */}
            <motion.div
              id="mobile-nav-sheet"
              role="dialog"
              aria-modal="true"
              aria-label={tBrand("name")}
              key="sheet"
              initial={{ x: "100%" }}
              animate={{ x: 0 }}
              exit={{ x: "100%" }}
              transition={{ duration: reduce ? 0 : 0.28, ease: [0.2, 0.7, 0.2, 1] }}
              className="bg-paper fixed top-0 right-0 bottom-0 z-50 flex w-72 flex-col overflow-y-auto px-6 py-6 md:hidden"
            >
              {/* sheet header */}
              <div className="flex items-center justify-between">
                <span className="font-display text-ink text-lg font-semibold">
                  {tBrand("name")}
                </span>
                <button
                  aria-label={tNav("closeMenu")}
                  onClick={() => setMobileOpen(false)}
                  className="text-ink flex h-10 w-10 items-center justify-center rounded-full hover:bg-black/5 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-amber"
                >
                  <X className="size-5" />
                </button>
              </div>

              {/* nav links */}
              <nav aria-label="Mobile navigation" className="mt-8 flex flex-col gap-1">
                {NAV_ITEMS.map(({ key, href }) => (
                  <a
                    key={key}
                    href={href}
                    onClick={() => setMobileOpen(false)}
                    className="text-ink-soft hover:text-ink hover:bg-paper-2 min-h-[48px] flex items-center rounded-lg px-3 text-base font-medium transition-colors duration-150 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-amber"
                  >
                    {tNav(key)}
                  </a>
                ))}
              </nav>

              {/* CTA */}
              <div className="mt-6">
                <a
                  href="#"
                  onClick={() => setMobileOpen(false)}
                  className="bg-amber hover:bg-amber-hi text-ink flex min-h-[52px] w-full items-center justify-center rounded-full text-base font-semibold transition-colors duration-150 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-amber"
                >
                  {tNav("cta")}
                </a>
              </div>

              {/* language toggle */}
              <div className="mt-8 border-t border-line pt-6">
                <p className="font-mono text-ink-soft mb-3 text-xs tracking-widest uppercase">
                  {tNav("language")}
                </p>
                <div className="flex flex-wrap gap-2">
                  {LANGS.map(({ code, key }) => {
                    const isActive = code === "en";
                    return (
                      <a
                        key={code}
                        href="#"
                        aria-current={isActive ? "true" : undefined}
                        className={[
                          "font-mono rounded-full border px-4 py-2 text-sm transition-colors duration-150 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-amber",
                          isActive
                            ? "bg-ink text-paper border-ink"
                            : "text-ink-soft border-line hover:border-ink hover:text-ink",
                        ].join(" ")}
                      >
                        {tLangs(key)}
                      </a>
                    );
                  })}
                </div>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}

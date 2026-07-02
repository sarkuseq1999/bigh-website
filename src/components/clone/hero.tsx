"use client";

import { useEffect, useRef } from "react";

import { Link } from "@/i18n/navigation";

import { CellOrb } from "./cell-orb";

interface HeroProps {
  eyebrow: string;
  brand: string;
  tagline: string;
  learnMore: string;
  viewProducts: string;
}

// Home hero: quiet porcelain field, display type, and the breathing jade cell.
// One orchestrated GSAP entrance; nothing else on the page animates on load.
export function Hero({ eyebrow, brand, tagline, learnMore, viewProducts }: HeroProps) {
  const scope = useRef<HTMLElement>(null);

  useEffect(() => {
    const el = scope.current;
    if (!el) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      el.querySelectorAll<HTMLElement>("[data-hero]").forEach((n) => (n.style.opacity = "1"));
      return;
    }
    let ctx: { revert: () => void } | undefined;
    import("gsap").then(({ gsap }) => {
      ctx = gsap.context(() => {
        gsap
          .timeline({ defaults: { ease: "power3.out" } })
          .fromTo(
            "[data-hero='orb']",
            { opacity: 0, scale: 0.92 },
            { opacity: 1, scale: 1, duration: 1.6, ease: "power2.out" },
            0,
          )
          .fromTo(
            "[data-hero='eyebrow']",
            { opacity: 0, y: 14 },
            { opacity: 1, y: 0, duration: 0.7 },
            0.15,
          )
          .fromTo(
            "[data-hero='brand']",
            { opacity: 0, y: 22 },
            { opacity: 1, y: 0, duration: 0.9 },
            0.3,
          )
          .fromTo(
            "[data-hero='tagline']",
            { opacity: 0, y: 18 },
            { opacity: 1, y: 0, duration: 0.8 },
            0.5,
          )
          .fromTo(
            "[data-hero='cta']",
            { opacity: 0, y: 14 },
            { opacity: 1, y: 0, duration: 0.7 },
            0.7,
          );
      }, el);
    });
    return () => ctx?.revert();
  }, []);

  return (
    <section
      ref={scope}
      className="relative overflow-hidden border-b border-line"
      aria-label={`${brand} — ${tagline}`}
    >
      <div className="mx-auto grid max-w-6xl items-center gap-8 px-4 py-16 sm:px-6 md:grid-cols-2 md:py-24">
        <div className="relative z-10">
          <p data-hero="eyebrow" className="font-mono text-sm uppercase tracking-[0.25em] text-celadon-deep opacity-0">
            {eyebrow}
          </p>
          <h1 data-hero="brand" className="font-display mt-4 text-6xl leading-none text-pine opacity-0 md:text-7xl">
            {brand}
          </h1>
          <p data-hero="tagline" className="mt-6 max-w-md text-xl leading-relaxed text-pine-soft opacity-0">
            {tagline}
          </p>
          <div data-hero="cta" className="mt-9 flex flex-wrap gap-3 opacity-0">
            <Link
              href="/about"
              className="rounded-full bg-pine px-6 py-2.5 font-medium text-porcelain transition-colors hover:bg-celadon-deep"
            >
              {learnMore}
            </Link>
            <a
              href="#products"
              className="rounded-full border border-pine/25 px-6 py-2.5 font-medium text-pine transition-colors hover:border-celadon-deep hover:text-celadon-deep"
            >
              {viewProducts}
            </a>
          </div>
        </div>
        <div data-hero="orb" className="relative mx-auto aspect-square w-full max-w-[26rem] opacity-0">
          <CellOrb className="absolute inset-0" />
        </div>
      </div>
    </section>
  );
}

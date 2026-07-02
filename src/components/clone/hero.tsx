"use client";

import Image from "next/image";
import { useEffect, useRef } from "react";

import { Link } from "@/i18n/navigation";

interface HeroProps {
  eyebrow: string;
  brand: string;
  tagline: string;
  learnMore: string;
}

// Faithful recreation of the original hero: navy/yellow diagonal backdrop
// (the site's own testing6.jpg), fresh-produce collage on the yellow side,
// centered white type on the navy side, green CTA. Enhancement = a single
// orchestrated entrance and a slow drift on the produce.
export function Hero({ eyebrow, brand, tagline, learnMore }: HeroProps) {
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
          .fromTo("[data-hero='eyebrow']", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.7 }, 0.1)
          .fromTo("[data-hero='brand']", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.9 }, 0.25)
          .fromTo("[data-hero='tagline']", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.8 }, 0.45)
          .fromTo("[data-hero='cta']", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.7 }, 0.65)
          .fromTo(
            "[data-hero='fruit']",
            { opacity: 0, x: 60, rotate: 4 },
            { opacity: 1, x: 0, rotate: 0, duration: 1.1 },
            0.2,
          )
          .fromTo(
            "[data-hero='veg']",
            { opacity: 0, x: 80, rotate: -4 },
            { opacity: 1, x: 0, rotate: 0, duration: 1.1 },
            0.35,
          );
        // slow ambient drift on the collage
        gsap.to("[data-hero='fruit']", { y: -10, duration: 5, yoyo: true, repeat: -1, ease: "sine.inOut" });
        gsap.to("[data-hero='veg']", { y: 8, duration: 6, yoyo: true, repeat: -1, ease: "sine.inOut" });
      }, el);
    });
    return () => ctx?.revert();
  }, []);

  return (
    <section ref={scope} className="relative overflow-hidden bg-navy" aria-label={`${brand} — ${tagline}`}>
      <Image
        src="/original/uploads/2019/04/testing6.jpg"
        alt=""
        fill
        priority
        className="object-cover"
        sizes="100vw"
      />
      <div className="relative mx-auto grid min-h-[34rem] max-w-6xl items-center gap-8 px-4 py-14 sm:px-6 md:grid-cols-[1.05fr_1fr]">
        <div className="relative z-10 text-center">
          <p data-hero="eyebrow" className="font-display text-2xl italic text-white/95 opacity-0 md:text-3xl">
            {eyebrow}
          </p>
          <h1 data-hero="brand" className="font-display mt-2 text-7xl text-white opacity-0 md:text-8xl">
            {brand}
          </h1>
          <div aria-hidden className="mx-auto mt-5 h-px w-16 bg-white/50" />
          <p data-hero="tagline" className="mx-auto mt-6 max-w-sm text-lg leading-relaxed text-white opacity-0">
            {tagline}
          </p>
          <div data-hero="cta" className="mt-8 opacity-0">
            <Link
              href="/about"
              className="inline-block rounded bg-green px-7 py-2.5 font-semibold text-white shadow-[0_6px_20px_rgba(0,0,0,0.25)] transition-colors hover:bg-green-dark"
            >
              {learnMore}
            </Link>
          </div>
        </div>

        <div className="relative hidden min-h-[30rem] md:block">
          <div data-hero="fruit" className="absolute -right-8 -top-4 w-[125%] max-w-none opacity-0">
            <Image
              src="/original/uploads/2019/04/fruits-and-berry.png"
              alt=""
              width={300}
              height={182}
              priority
              unoptimized
              className="h-auto w-full"
            />
          </div>
          <div data-hero="veg" className="absolute -right-6 bottom-0 w-[115%] max-w-none opacity-0">
            <Image
              src="/original/uploads/2019/04/herbs-and-veg.png"
              alt=""
              width={300}
              height={244}
              unoptimized
              className="h-auto w-full"
            />
          </div>
        </div>
      </div>
    </section>
  );
}

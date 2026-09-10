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

// Measured clone of the original hero (1440px reference):
// section = 74vw tall; bg = testing6.jpg (navy/yellow diagonal);
// produce banner absolutely at 43% / 31%, 69% wide, overhanging the section
// bottom exactly like the original; centered white Roboto-600 text column
// on the navy side (49px / 154px / 28px at full width).
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
          .fromTo("[data-hero='text']", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.9 }, 0.1)
          .fromTo("[data-hero='banner']", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 1.1 }, 0.3);
      }, el);
    });
    return () => ctx?.revert();
  }, []);

  return (
    <section
      ref={scope}
      className="relative z-10 bg-navy md:h-[74vw] md:max-h-[67rem]"
      aria-label={`${brand} — ${tagline}`}
    >
      <div className="absolute inset-0 overflow-hidden">
        <Image
          src="/original/uploads/2019/04/testing6.jpg"
          alt=""
          fill
          priority
          className="object-cover"
          sizes="100vw"
        />
      </div>

      {/* text column — vertically centered on the navy side */}
      <div
        data-hero="text"
        className="relative px-6 pb-8 pt-60 text-center opacity-0 md:absolute md:left-[3%] md:top-[42%] md:w-[37%] md:-translate-y-1/2 md:px-0 md:pb-0 md:pt-0"
      >
        <p className="text-[clamp(1.6rem,3.4vw,3.06rem)] font-semibold leading-tight text-white/85">
          {eyebrow}
        </p>
        <h1 className="text-[clamp(4rem,10.7vw,9.6rem)] font-semibold leading-none text-white/85">
          {brand}
        </h1>
        <div aria-hidden className="mx-auto mt-6 h-px w-24 bg-white/40" />
        <p className="mx-auto mt-7 max-w-md text-[clamp(1.1rem,1.95vw,1.75rem)] font-semibold leading-snug text-white/85">
          {tagline}
        </p>
        <div className="mt-9">
          <Link
            href="/about"
            className="inline-block rounded bg-green px-[30px] py-[15px] text-base font-medium leading-none text-white transition-colors hover:bg-green-dark"
          >
            {learnMore}
          </Link>
        </div>
      </div>

      {/* produce banner — 43% left, 31% down, 69% wide, spills below the section */}
      <div
        data-hero="banner"
        className="relative mx-auto w-[94%] max-w-xl pb-4 opacity-0 md:absolute md:left-[43%] md:top-[31%] md:mx-0 md:w-[69%] md:max-w-none md:pb-0"
      >
        <Image
          src="/original/uploads/2019/04/bottle_banner_1@0.5x.png"
          alt=""
          width={986}
          height={1035}
          priority
          className="h-auto w-full"
          sizes="(max-width: 768px) 94vw, 69vw"
        />
      </div>
    </section>
  );
}

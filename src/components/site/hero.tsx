"use client";

import { useEffect, useRef, useState } from "react";
import dynamic from "next/dynamic";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { CustomEase } from "gsap/CustomEase";
import { useTranslations } from "next-intl";
import { useReducedMotionSafe } from "@/components/site/use-reduced-motion-safe";

/* ─────────────────────────────────────────────────────────────────────────
   Hero — Section 1 "The Promise", Ignite + Protect edition.
   Spec: docs/superpowers/specs/2026-06-10-hero-3d-redesign-design.md

   Deep forest-black hero with a living Three.js scene behind the text:
   amber mitochondria cores ignite, dark debris is swept away, sparks keep
   traveling the neuron threads. The page below stays cream — scrolling out
   of the hero is the dark-to-light handoff.

   The WebGL layer is client-only and lazy (next/dynamic): the server HTML
   is the readable headline on a CSS gradient, so the LCP never waits on
   three.js. A pure-CSS glow layer covers no-JS / no-WebGL; the scene
   unmounts it the moment WebGL takes over.
───────────────────────────────────────────────────────────────────────── */

const HeroScene = dynamic(() => import("@/components/site/hero-scene"), {
  ssr: false,
});

/* same premium ease the rest of the site uses: cubic-bezier(0.2,0.7,0.2,1).
   Registration is browser-only — client components still render on the
   server for HTML, and ScrollTrigger touches window on registration. */
const PREMIUM_EASE = "heroPremium";
if (typeof window !== "undefined") {
  gsap.registerPlugin(ScrollTrigger, CustomEase);
  CustomEase.create(PREMIUM_EASE, "M0,0 C0.2,0.7 0.2,1 1,1");
}

export function Hero() {
  const t = useTranslations("Hero");
  const reduce = useReducedMotionSafe();
  const scopeRef = useRef<HTMLElement>(null);
  const [sceneActive, setSceneActive] = useState(false);

  /* Text intro + scroll-out. The timeline starts on a fixed clock after
     mount (~1.2s, landing right after the first cores catch) rather than
     blocking on the scene — the headline must never wait for WebGL. */
  useEffect(() => {
    if (reduce) return; // server HTML is already fully visible
    const scope = scopeRef.current;
    if (!scope) return;

    const ctx = gsap.context(() => {
      gsap.set("[data-hero-reveal]", { opacity: 0, y: 18 });
      gsap.to("[data-hero-reveal]", {
        opacity: 1,
        y: 0,
        duration: 0.8,
        stagger: 0.12,
        delay: 1.15,
        ease: PREMIUM_EASE,
      });

      /* gentle parallax drift as the hero scrolls away — no pinning */
      gsap.to("[data-hero-content]", {
        y: 56,
        opacity: 0.4,
        ease: "none",
        scrollTrigger: {
          trigger: scope,
          start: "bottom 90%",
          end: "bottom 25%",
          scrub: true,
        },
      });
    }, scope);

    return () => ctx.revert();
  }, [reduce]);

  return (
    <section
      ref={scopeRef}
      className="hero-dark relative isolate overflow-hidden text-paper"
    >
      {/* base atmosphere: deep forest-black gradient + vignette (always on,
          doubles as the canvas backdrop and the no-WebGL floor) */}
      <div aria-hidden className="hero-base absolute inset-0" />

      {/* static glow fallback — fades in via CSS only if WebGL hasn't taken
          over by then; unmounted entirely once the scene is live */}
      {!sceneActive && <div aria-hidden className="hero-static-glow absolute inset-0" />}

      {/* living scene */}
      <HeroScene onActive={() => setSceneActive(true)} />

      {/* readability veil over the text column */}
      <div
        aria-hidden
        className="absolute inset-0 bg-gradient-to-r from-[#0B100D]/85 via-[#0B100D]/35 to-transparent md:via-[#0B100D]/20"
      />
      <div
        aria-hidden
        className="absolute inset-0 bg-gradient-to-t from-[#0B100D]/70 via-transparent to-transparent md:from-[#0B100D]/30"
      />

      {/* ── content ─────────────────────────────────────────────────── */}
      <div className="relative z-10 mx-auto flex min-h-[100dvh] max-w-[1400px] items-center px-6 pt-24 pb-16 md:px-14 md:pt-16">
        <div data-hero-content className="max-w-[640px]">
          {/* Eyebrow */}
          <p
            data-hero-reveal
            className="mb-5 font-mono text-[0.8125rem] font-normal tracking-[0.16em] uppercase text-amber-hi"
          >
            {t("eyebrow")}
          </p>

          {/* Headline */}
          <h1
            data-hero-reveal
            className="m-0 font-display text-[clamp(3rem,5.4vw,5.25rem)] font-light leading-[1.03] tracking-[-0.02em] text-balance text-paper"
          >
            {t.rich("headline", {
              em: (chunks) => (
                <em className="font-display italic font-normal text-amber-hi">
                  {chunks}
                </em>
              ),
            })}
          </h1>

          {/* Subhead */}
          <p
            data-hero-reveal
            className="mt-6 font-display text-[1.375rem] font-light leading-[1.35] text-paper/90 md:text-[1.625rem]"
          >
            {t("subhead")}
          </p>

          {/* Paragraph */}
          <p
            data-hero-reveal
            className="mt-5 max-w-[54ch] text-[1.125rem] leading-[1.6] text-paper/70 md:text-[1.1875rem]"
          >
            {t("paragraph")}
          </p>

          {/* CTAs */}
          <div
            data-hero-reveal
            className="mt-8 flex flex-col gap-4 sm:flex-row sm:items-center"
          >
            <a
              href="#quiz"
              className="inline-flex min-h-[52px] items-center justify-center rounded-full bg-amber px-8 py-3 text-[1.0625rem] font-medium text-ink transition-colors duration-200 hover:bg-amber-hi focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-amber-hi"
            >
              {t("ctaPrimary")}
            </a>

            <a
              href="#nuricell"
              className="inline-flex min-h-[52px] items-center gap-1 text-[1.0625rem] font-medium text-paper underline-offset-4 hover:underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-amber-hi"
            >
              {t("ctaSecondary")}
            </a>
          </div>

          {/* CTA payoff */}
          <p
            data-hero-reveal
            className="mt-4 font-mono text-[0.8125rem] tracking-[0.1em] uppercase text-paper/55"
          >
            {t("ctaNote")}
          </p>
        </div>
      </div>
    </section>
  );
}

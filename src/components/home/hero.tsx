"use client";

import { useEffect, useLayoutEffect, useRef, useState } from "react";
import gsap from "gsap";

import Silk, { type SilkPalette } from "./silk";

// Screen 1 · THE HOOK — brain hook up top, cellular reveal one line down.
// Ported from the Golden Hour design lab (bigh-for-real /a): word-by-word
// serif rise over the silk shader, one underline-arrow CTA into the story.
export function Hero({
  eyebrow,
  l1,
  l2,
  reveal,
  cta,
}: {
  eyebrow?: string;
  l1: string;
  l2: string;
  reveal: string;
  cta: string;
}) {
  const root = useRef<HTMLDivElement>(null);

  // Palette A/B for the design review: append ?silk=gold to compare the
  // molten-gold silk against the default navy. Default ships navy until
  // Mo locks the Golden Hour palette.
  const [palette, setPalette] = useState<SilkPalette>("navy");
  useEffect(() => {
    const p = new URLSearchParams(window.location.search).get("silk");
    if (p === "gold") setPalette("gold");
  }, []);

  useLayoutEffect(() => {
    const reduced = window.matchMedia(
      "(prefers-reduced-motion: reduce)",
    ).matches;
    if (reduced) return;

    const ctx = gsap.context(() => {
      const tl = gsap.timeline({
        defaults: { ease: "power4.out", duration: 1.2 },
      });
      tl.from("[data-word]", { yPercent: 115, duration: 1.4, stagger: 0.085 }, 0.15)
        .from("[data-sub]", { y: 28, autoAlpha: 0 }, 1.05)
        .from("[data-cta]", { y: 18, autoAlpha: 0, duration: 0.9 }, 1.3);
    }, root);

    return () => ctx.revert();
  }, []);

  const words = [
    ...l1.split(" ").map((t) => ({ t, italic: false })),
    ...l2.split(" ").map((t) => ({ t, italic: true })),
  ];

  return (
    <section ref={root} className="relative min-h-svh overflow-hidden">
      <Silk palette={palette} />

      <div className="relative z-10 flex min-h-svh flex-col px-6 pt-36 sm:px-12">
        <div className="mt-[6vh] sm:mt-[8vh]">
          {eyebrow ? (
            <p className="mb-6 font-mono text-[12px] uppercase tracking-[0.24em] text-[color:var(--gh-faint)]">
              {eyebrow}
            </p>
          ) : null}
          <h1 className="gh-serif max-w-[9em] text-[clamp(3.4rem,9.2vw,8.6rem)] leading-[0.93] tracking-[-0.01em]">
            {words.map((w, i) => (
              <span key={i}>
                <span className="inline-block overflow-hidden pb-[0.08em] align-bottom">
                  <span
                    data-word
                    className={`inline-block ${w.italic ? "italic" : ""}`}
                  >
                    {w.t}
                  </span>
                </span>{" "}
              </span>
            ))}
          </h1>

          <p
            data-sub
            className="mt-9 max-w-xl text-[22px] leading-[1.7] text-[color:var(--gh-muted)]"
          >
            {reveal}
          </p>
          <a
            data-cta
            href="#truth"
            className="group mt-10 inline-flex w-fit items-center gap-3 font-mono text-[13px] uppercase tracking-[0.22em]"
          >
            <span className="border-b border-[color:var(--gh-fg)] pb-1 transition-colors group-hover:border-[color:var(--gh-ember)] group-hover:text-[color:var(--gh-ember)]">
              {cta}
            </span>
            <span className="transition-transform duration-300 group-hover:translate-x-1.5">
              →
            </span>
          </a>
        </div>
      </div>
    </section>
  );
}

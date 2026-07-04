"use client";

import { useEffect, useRef, useState } from "react";

import { Reveal } from "@/components/clone/reveal";

// Counts 0 → target when the number scrolls into view; renders the final
// value immediately for reduced-motion users (and before hydration).
function CountUp({ target, suffix }: { target: number; suffix: string }) {
  const ref = useRef<HTMLSpanElement>(null);
  const [value, setValue] = useState(target);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    setValue(0);
    let raf = 0;
    const io = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting) return;
        io.disconnect();
        const t0 = performance.now();
        const dur = 1400;
        const tick = (now: number) => {
          const p = Math.min((now - t0) / dur, 1);
          const eased = 1 - Math.pow(1 - p, 3);
          setValue(Math.round(eased * target));
          if (p < 1) raf = requestAnimationFrame(tick);
        };
        raf = requestAnimationFrame(tick);
      },
      { rootMargin: "0px 0px -15% 0px" },
    );
    io.observe(el);
    return () => {
      io.disconnect();
      cancelAnimationFrame(raf);
    };
  }, [target]);

  return (
    <span ref={ref}>
      {value}
      {suffix}
    </span>
  );
}

// Screen 2 · THE HONEST TRUTH — the mechanism, told warmly. Cells run on
// power plants; they slow with age; the brain feels it first.
export function Truth({
  kicker,
  body,
  stat1,
  stat2,
}: {
  kicker: string;
  body: string;
  stat1: string;
  stat2: string;
}) {
  return (
    <section
      id="truth"
      className="relative scroll-mt-24 border-t border-[color:var(--gh-line)] px-6 py-28 sm:px-12 sm:py-36"
    >
      <div className="mx-auto max-w-5xl">
        <Reveal>
          <p className="font-mono text-[12px] uppercase tracking-[0.24em] text-[color:var(--gh-faint)]">
            {kicker}
          </p>
        </Reveal>
        <Reveal delay={80}>
          <p className="gh-serif mt-8 max-w-3xl text-[clamp(1.6rem,3.4vw,2.6rem)] leading-[1.35] text-[color:var(--gh-fg)]">
            {body}
          </p>
        </Reveal>

        {/* the one quiet animated stat */}
        <div className="mt-16 grid gap-10 sm:mt-20 sm:grid-cols-2 sm:gap-6">
          <Reveal delay={120}>
            <div className="border-l border-[color:var(--gh-line)] pl-6">
              <p className="gh-serif text-[clamp(3.2rem,7vw,5.5rem)] leading-none text-[color:var(--gh-muted)]">
                <CountUp target={2} suffix="%" />
              </p>
              <p className="mt-3 text-[15px] text-[color:var(--gh-faint)]">{stat1}</p>
            </div>
          </Reveal>
          <Reveal delay={220}>
            <div className="border-l border-[color:var(--gh-ember)] pl-6">
              <p className="gh-serif text-[clamp(3.2rem,7vw,5.5rem)] leading-none text-[color:var(--gh-fg)]">
                <CountUp target={20} suffix="%" />
              </p>
              <p className="mt-3 text-[15px] text-[color:var(--gh-muted)]">{stat2}</p>
            </div>
          </Reveal>
        </div>
      </div>
    </section>
  );
}

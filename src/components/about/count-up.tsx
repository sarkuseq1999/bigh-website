"use client";

import { useEffect, useRef } from "react";

// A number that counts up once when it scrolls into view ("280+", "20+"). The page renders the
// final number, so it is right without JavaScript and with reduced motion; the count only starts
// from `from` when the number is still below the fold on load.
export function CountUp({
  to,
  from = 0,
  suffix = "",
  duration = 1.6,
  className = "",
}: {
  to: number;
  from?: number;
  suffix?: string;
  duration?: number;
  className?: string;
}) {
  const ref = useRef<HTMLSpanElement>(null);

  useEffect(() => {
    const element = ref.current;
    if (!element || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    if (element.getBoundingClientRect().top < window.innerHeight) return;
    const show = (value: number) => (element.textContent = `${Math.round(value)}${suffix}`);
    show(from);
    let frame = 0;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting) return;
        observer.disconnect();
        const start = performance.now();
        const step = (now: number) => {
          const t = Math.min(1, (now - start) / (duration * 1000));
          const eased = 1 - Math.pow(1 - t, 3);
          show(from + (to - from) * eased);
          if (t < 1) frame = requestAnimationFrame(step);
        };
        frame = requestAnimationFrame(step);
      },
      { threshold: 0.6 },
    );
    observer.observe(element);
    return () => {
      observer.disconnect();
      cancelAnimationFrame(frame);
      show(to);
    };
  }, [to, from, suffix, duration]);

  // One text child, so writing textContent while counting never fights React's own text nodes.
  return <span ref={ref} className={className}>{`${to}${suffix}`}</span>;
}

"use client";

import { useEffect, useRef } from "react";

// Light scroll-parallax for decorative floaters (the original's Elementor
// scrolling effects). speed > 0 drifts down slightly slower than the page,
// speed < 0 drifts against it. Off under prefers-reduced-motion.
export function ScrollDrift({
  speed = 0.08,
  className = "",
  style,
  children,
}: {
  speed?: number;
  className?: string;
  style?: React.CSSProperties;
  children: React.ReactNode;
}) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    let raf = 0;
    let visible = true;
    const io = new IntersectionObserver(([e]) => {
      visible = e.isIntersecting;
    }, { rootMargin: "200px" });
    io.observe(el);

    const tick = () => {
      if (visible) {
        const rect = el.getBoundingClientRect();
        const offset = rect.top + rect.height / 2 - window.innerHeight / 2;
        el.style.transform = `translate3d(0, ${(-offset * speed).toFixed(1)}px, 0)`;
      }
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);

    return () => {
      cancelAnimationFrame(raf);
      io.disconnect();
    };
  }, [speed]);

  return (
    <div ref={ref} className={className} style={style}>
      {children}
    </div>
  );
}

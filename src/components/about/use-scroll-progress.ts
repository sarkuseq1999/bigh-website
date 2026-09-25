"use client";

import { useEffect, useRef } from "react";

// Writes --progress (0 → 1) on an element as it travels from the bottom of the window to the
// middle, so CSS can tie an effect to scrolling (look A's photo comes into focus this way).
// With reduced motion the CSS ignores the value.
export function useScrollProgress<T extends HTMLElement>() {
  const ref = useRef<T>(null);
  useEffect(() => {
    const element = ref.current;
    if (!element) return;
    let frame = 0;
    const update = () => {
      frame = 0;
      const box = element.getBoundingClientRect();
      const view = window.innerHeight;
      const center = box.top + box.height / 2;
      const progress = Math.min(1, Math.max(0, (view - center) / (view / 2)));
      element.style.setProperty("--progress", progress.toFixed(3));
    };
    const schedule = () => {
      if (!frame) frame = requestAnimationFrame(update);
    };
    update();
    window.addEventListener("scroll", schedule, { passive: true });
    window.addEventListener("resize", schedule);
    return () => {
      cancelAnimationFrame(frame);
      window.removeEventListener("scroll", schedule);
      window.removeEventListener("resize", schedule);
    };
  }, []);
  return ref;
}

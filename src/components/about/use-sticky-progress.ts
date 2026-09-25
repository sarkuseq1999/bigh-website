"use client";

import { useEffect, useRef } from "react";

// For a tall section with a sticky stage inside: writes --p (0 → 1) on the section as the page
// scrolls through it, from its top meeting the top of the window to its bottom meeting the
// bottom. CSS turns --p into the scene changes (look B's dive into the cells).
export function useStickyProgress<T extends HTMLElement>() {
  const ref = useRef<T>(null);
  useEffect(() => {
    const element = ref.current;
    if (!element) return;
    let frame = 0;
    const update = () => {
      frame = 0;
      const box = element.getBoundingClientRect();
      const travel = box.height - window.innerHeight;
      const progress = travel > 0 ? Math.min(1, Math.max(0, -box.top / travel)) : 0;
      element.style.setProperty("--p", progress.toFixed(3));
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

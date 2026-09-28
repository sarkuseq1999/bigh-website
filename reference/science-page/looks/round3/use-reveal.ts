"use client";

import { useEffect, useRef } from "react";

// Marks an element with data-shown once it scrolls into view; CSS does the easing. With reduced
// motion the CSS shows everything at once, so nothing waits on this.
export function useReveal<T extends HTMLElement>(threshold = 0.2) {
  const ref = useRef<T>(null);
  useEffect(() => {
    const element = ref.current;
    if (!element) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          element.dataset.shown = "true";
          observer.disconnect();
        }
      },
      { threshold },
    );
    observer.observe(element);
    return () => observer.disconnect();
  }, [threshold]);
  return ref;
}

"use client";

import { useEffect, useState, type RefObject } from "react";

/** False when the visitor asks for reduced motion (then the page is a complete still). */
export function useMotionOk() {
  const [ok, setOk] = useState(true);
  useEffect(() => {
    const query = window.matchMedia("(prefers-reduced-motion: reduce)");
    const update = () => setOk(!query.matches);
    update();
    query.addEventListener("change", update);
    return () => query.removeEventListener("change", update);
  }, []);
  return ok;
}

/**
 * Ink-fill pills: an outlined pill fills from the point where the pointer came in, as a drop of
 * ink spreads in water (look-ink.module.css reads --mx / --my). One listener for the whole look.
 */
export function useInkFill(root: RefObject<HTMLElement | null>) {
  useEffect(() => {
    const element = root.current;
    if (!element) return;
    const onOver = (event: PointerEvent) => {
      if (event.pointerType !== "mouse") return;
      const pill = (event.target as HTMLElement).closest<HTMLElement>("a, button");
      const from = event.relatedTarget as Node | null;
      if (!pill || (from && pill.contains(from))) return;
      const box = pill.getBoundingClientRect();
      pill.style.setProperty("--mx", `${(event.clientX - box.left).toFixed(0)}px`);
      pill.style.setProperty("--my", `${(event.clientY - box.top).toFixed(0)}px`);
    };
    element.addEventListener("pointerover", onOver, { passive: true });
    return () => element.removeEventListener("pointerover", onOver);
  }, [root]);
}

/**
 * Ink blooms: every painting marked [data-bloom] spreads into the paper through an ink blot's
 * soft edge as it enters the window, in the page's one breath (look-ink.module.css). The
 * opening's paintings are marked "waiting" from the server, so they bloom on arrival instead of
 * flashing; reduced motion shows everything at once.
 */
export function useBloom(root: RefObject<HTMLElement | null>, motion: boolean) {
  useEffect(() => {
    const element = root.current;
    if (!element) return;
    const targets = [...element.querySelectorAll<HTMLElement>("[data-bloom]")];
    if (!motion) {
      targets.forEach((target) => (target.dataset.bloom = "done"));
      return;
    }
    const timers: number[] = [];
    const open = (target: HTMLElement) => {
      if (target.dataset.bloom === "in" || target.dataset.bloom === "done") return;
      target.dataset.bloom = "in";
      const delay = Number(getComputedStyle(target).getPropertyValue("--bloom-delay")) || 0;
      timers.push(window.setTimeout(() => (target.dataset.bloom = "done"), 3400 + delay));
    };
    const observer = new IntersectionObserver(
      (entries) =>
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          observer.unobserve(entry.target);
          open(entry.target as HTMLElement);
        }),
      { rootMargin: "0px 0px -8% 0px" },
    );
    targets.forEach((target) => {
      if (target.dataset.bloom !== "done" && target.dataset.bloom !== "in") {
        target.dataset.bloom = "waiting";
      }
      observer.observe(target);
    });
    return () => {
      observer.disconnect();
      timers.forEach((timer) => window.clearTimeout(timer));
    };
  }, [root, motion]);
}

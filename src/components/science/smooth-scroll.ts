"use client";

import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Lenis from "lenis";
import { useEffect } from "react";

// Lenis smooth scrolling (Mo's design toolkit note, September 27, 2026), driven by GSAP's ticker so
// every ScrollTrigger on the page stays in step with it. Off with reduced motion and on touch
// screens, where native scrolling already feels right.
export function useSmoothScroll(enabled: boolean) {
  useEffect(() => {
    if (!enabled) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    if (window.matchMedia("(pointer: coarse)").matches) return;
    gsap.registerPlugin(ScrollTrigger);
    document.documentElement.style.scrollBehavior = "auto";
    const lenis = new Lenis({ duration: 1.15, smoothWheel: true });
    lenis.on("scroll", ScrollTrigger.update);
    const tick = (time: number) => lenis.raf(time * 1000);
    gsap.ticker.add(tick);
    gsap.ticker.lagSmoothing(0);
    // Links to #anchors glide instead of jumping.
    const onClick = (event: MouseEvent) => {
      const link = (event.target as HTMLElement).closest<HTMLAnchorElement>('a[href^="#"]');
      if (!link || link.getAttribute("href") === "#") return;
      const target = document.querySelector(link.getAttribute("href")!);
      if (!target) return;
      // Opt-in chapter shortcuts (Propolis): native focus/auto-scroll can move the window
      // before Lenis's next frame. Measure the actual document position, resync that frame,
      // and land on the heading. Other site anchors retain their existing behavior below.
      const heading = link.hasAttribute("data-scroll-heading")
        ? target.querySelector<HTMLElement>("h2")
        : null;
      if (heading) {
        if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || event.button !== 0)
          return;
        event.preventDefault();
        const destination = heading.getBoundingClientRect().top + window.scrollY - 120;
        const finish = () => {
          heading.tabIndex = -1;
          heading.dataset.inkJumpTarget = "";
          heading.focus({ preventScroll: true });
        };
        window.history.pushState(null, "", link.hash);
        lenis.scrollTo(window.scrollY, { immediate: true });
        if (Math.abs(window.scrollY - destination) < 1) finish();
        else lenis.scrollTo(destination, { onComplete: finish });
        return;
      }
      event.preventDefault();
      lenis.scrollTo(target as HTMLElement, { offset: -84 });
    };
    document.addEventListener("click", onClick);
    return () => {
      document.removeEventListener("click", onClick);
      gsap.ticker.remove(tick);
      lenis.destroy();
      document.documentElement.style.scrollBehavior = "";
    };
  }, [enabled]);
}

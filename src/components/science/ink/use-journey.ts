"use client";

import { useEffect, type RefObject } from "react";

/**
 * The handscroll's travel (spec, "The handscroll"). The room after the pinned box (journey.module.css)
 * is as tall as the painting's overflow (never less than the band is wide), so the page is already
 * as tall as the travel before any script runs; this hook only reads the scroll position. While the
 * pinned box is stuck under the menu bar, scrolling through the room moves the painting through its
 * overflow: about one pixel for one, more slowly on a short window. It starts with the first place
 * no further right than the band's middle (on a phone's narrow band the castle would otherwise
 * stand in the right-hand mist; on wider bands it already is). Writes on the section: --x (px
 * moved), --walked (px of the line inked, up to the stop in view), --view (the band's width) and
 * data-now (that stop's index). The stop in view is the last whose place has crossed a reading line
 * that moves from the band's middle to 95% of its width as the painting travels: each stop lights
 * once its place is in view (on a phone's narrow band too, where the places are screens apart), the
 * first is current at the start and the last at the end. On a short window it also shrinks the
 * painting (--band-h) until the pinned box fits under the menu bar. Reduced motion: nothing runs;
 * the stylesheet shows the still scroll.
 */
export function useJourney(
  section: RefObject<HTMLElement | null>,
  motion: boolean,
  at: readonly number[],
) {
  useEffect(() => {
    const root = section.current;
    const pin = root?.querySelector<HTMLElement>("[data-pin]");
    const band = root?.querySelector<HTMLElement>("[data-band]");
    const painting = root?.querySelector<HTMLImageElement>("[data-painting]");
    const room = root?.querySelector<HTMLElement>("[data-room]");
    if (!root || !pin || !band || !painting || !room || !motion) return;
    let travel = 0;
    let overflow = 0;
    let from = 0;
    let width = 0;
    let start = 0;
    let frame = 0;
    let now = -1;

    const update = () => {
      frame = 0;
      const p = Math.min(1, Math.max(0, (window.scrollY - start) / Math.max(1, travel)));
      const x = from + p * (overflow - from);
      const read = x + (0.5 + 0.45 * p) * band.clientWidth;
      let best = 0;
      at.forEach((f, i) => {
        if (f * width <= read) best = i;
      });
      root.style.setProperty("--x", `${x.toFixed(1)}px`);
      root.style.setProperty("--walked", `${Math.max(0, at[best] * width - x).toFixed(1)}px`);
      if (best !== now) {
        now = best;
        root.dataset.now = String(best);
      }
    };
    const schedule = () => {
      if (!frame) frame = requestAnimationFrame(update);
    };
    const fit = () => {
      // The pinned box must fit between the menu bar and the window's foot: a long title (vn, kr)
      // or a short window takes the room from the painting, never from the words.
      root.style.removeProperty("--band-h");
      const pinTop = parseFloat(getComputedStyle(pin).top) || 0;
      const over = pin.getBoundingClientRect().height + pinTop + 12 - window.innerHeight;
      if (over > 0) {
        const h = Math.max(180, painting.getBoundingClientRect().height - over);
        root.style.setProperty("--band-h", `${h}px`);
      }
    };
    const measure = () => {
      fit();
      width = painting.getBoundingClientRect().width;
      overflow = Math.max(0, width - band.clientWidth);
      from = Math.min(overflow, Math.max(0, at[0] * width - band.clientWidth / 2));
      travel = room.offsetHeight;
      root.style.setProperty("--view", `${band.clientWidth}px`);
      const pinTop = parseFloat(getComputedStyle(pin).top) || 0;
      const padTop = parseFloat(getComputedStyle(root).paddingTop) || 0;
      start = root.getBoundingClientRect().top + window.scrollY + padTop - pinTop;
      update();
    };
    const resize = new ResizeObserver(() => measure());
    resize.observe(band);
    window.addEventListener("scroll", schedule, { passive: true });
    window.addEventListener("resize", measure);
    measure();
    return () => {
      resize.disconnect();
      window.removeEventListener("scroll", schedule);
      window.removeEventListener("resize", measure);
      if (frame) cancelAnimationFrame(frame);
      root.style.removeProperty("--x");
      root.style.removeProperty("--walked");
      root.style.removeProperty("--view");
      root.style.removeProperty("--band-h");
    };
  }, [section, motion, at]);
}

"use client";

import { useEffect, useState, type RefObject } from "react";

/**
 * The first words of the last resort's console warning. The QA (qa_science_ink.py, settled) looks
 * for them, so keep them as they are when the words after them change.
 */
const LAST_RESORT = "[science-journey:last-resort]";

/** The track's misty ends, as a share of the band's width at each end (journey.module.css: the
 *  track's mask and the stop in view's --pos clamp use the same 6%). */
const MIST = 0.06;

/**
 * The handscroll's travel (spec, "The handscroll"). The room after the pinned box (journey.module.css)
 * is as tall as the painting's overflow (never less than the band is wide), so the page is already
 * as tall as the travel before any script runs; this hook only reads the scroll position. While the
 * pinned box is stuck under the menu bar, scrolling through the room moves the painting through its
 * overflow: about one pixel for one, more slowly on a short window. It starts with the first place
 * no further right than the band's middle (on a phone's narrow band the castle would otherwise
 * stand in the right-hand mist; on wider bands it already is). Writes on the section: --x (px
 * moved), --walked (px of the line inked, up to the stop in view's dot, which stays over its words
 * inside the misty ends), --view (the band's width) and data-now (that stop's index); on the other
 * stops, data-out where their words would stand in the misty ends (the stylesheet fades them from
 * 960px); data-stuck once the box has stuck (a lifted title then fades, where the stylesheet's
 * --settle stops it short of the menu bar). The stop in view is the last whose place has crossed a reading line
 * that moves from the band's middle to 95% of its width as the painting travels: each stop lights
 * once its place is in view (on a phone's narrow band too, where the places are screens apart), the
 * first is current at the start and the last at the end.
 *
 * Every stop's words stay in the page for screen readers (the others are only transparent); only
 * the stop in view's link can be reached with Tab (the others' links get tabindex -1), so the
 * keyboard never lands on a link that cannot be seen.
 *
 * fit() follows the stylesheet's --mode and decides nothing by measuring (journey.module.css: the
 * stylesheet alone sets the painting's height, so the page's height is the same before and after
 * this runs). "lift" (a short window): the title goes on under the menu bar once the box sticks
 * (--lift, the title's height and its gap: the box sticks that much higher; only the sticky top
 * changes, no height). "still": the still scroll. The last resort, for a box the stylesheet's room
 * did not cover (a translation that grew): the painting gives way, down to 180px, then the section
 * is marked data-still; both change the page's height, so the rooms are measured to keep this rare,
 * and it says so in the console (console.warn, starting with LAST_RESORT) when it acts. It waits
 * while the page's fonts are still arriving (a fallback face is no shortfall of the rooms). It
 * measures against the small viewport height (100svh, through --journey-svh), not innerHeight, so
 * a phone's toolbars coming and going cannot change the layout (innerHeight only in a browser that
 * cannot register the probe). Returns whether it is the still scroll. Reduced motion: nothing
 * runs; the stylesheet shows the still scroll.
 */
export function useJourney(
  section: RefObject<HTMLElement | null>,
  motion: boolean,
  at: readonly number[],
) {
  const [still, setStill] = useState(false);
  useEffect(() => {
    const root = section.current;
    const pin = root?.querySelector<HTMLElement>("[data-pin]");
    const words = pin?.firstElementChild;
    const band = root?.querySelector<HTMLElement>("[data-band]");
    const painting = root?.querySelector<HTMLImageElement>("[data-painting]");
    const room = root?.querySelector<HTMLElement>("[data-room]");
    if (!root || !pin || !words || !band || !painting || !room || !motion) return;
    const links = [...root.querySelectorAll<HTMLAnchorElement>("li[data-stop] a")];
    const items = [...root.querySelectorAll<HTMLElement>("li[data-stop]")];
    const out = items.map(() => false);
    let travel = 0;
    let overflow = 0;
    let from = 0;
    let width = 0;
    let view = 0;
    let half = 0;
    let halves = items.map(() => 0);
    let start = 0;
    let frame = 0;
    let pending = 0;
    let now = -1;
    let fixed = false;
    let warned = "";
    let live = true;

    // Half the width a stop's words take (its mark and title as set, not the stop's 230px box).
    const extent = (item: HTMLElement) => {
      let wide = 0;
      item.querySelectorAll("span").forEach((span) => {
        const range = document.createRange();
        range.selectNodeContents(span);
        wide = Math.max(wide, range.getBoundingClientRect().width);
      });
      return wide / 2;
    };
    // The stops whose words would stand in the track's misty ends (journey.module.css fades them
    // from 960px); null clears every mark (the still scroll, and on the way out).
    const fade = (marks: boolean[] | null) =>
      items.forEach((item, i) => {
        const value = marks ? marks[i] : false;
        if (value === out[i]) return;
        out[i] = value;
        item.toggleAttribute("data-out", value);
      });

    const reachable = (current: number | null) =>
      links.forEach((link) => {
        const stop = Number(link.closest<HTMLElement>("[data-stop]")?.dataset.stop);
        if (current === null || stop === current) link.removeAttribute("tabindex");
        else link.tabIndex = -1;
      });
    const update = () => {
      frame = 0;
      if (fixed) return;
      const p = Math.min(1, Math.max(0, (window.scrollY - start) / Math.max(1, travel)));
      const x = from + p * (overflow - from);
      const read = x + (0.5 + 0.45 * p) * view;
      let best = 0;
      at.forEach((f, i) => {
        if (f * width <= read) best = i;
      });
      // The clear part of the track, inside its misty ends (MIST of the band's width at each end,
      // as journey.module.css's --pos clamp and track mask).
      const left = x + MIST * view;
      const right = x + (1 - MIST) * view;
      // The stop in view's words and dot stand at its place, held half a stop's box inside the
      // mist (--pos in journey.module.css); the line is inked up to that dot.
      const held = Math.min(Math.max(at[best] * width, left + half), right - half);
      root.style.setProperty("--x", `${x.toFixed(1)}px`);
      root.style.setProperty("--walked", `${Math.max(0, held - x).toFixed(1)}px`);
      // The box has stuck (the stylesheet fades a lifted title then: journey.module.css).
      root.toggleAttribute("data-stuck", window.scrollY >= start - 0.5);
      // The others' words show only while they stand wholly in the clear part.
      fade(
        at.map(
          (f, i) => i !== best && (f * width - halves[i] < left || f * width + halves[i] > right),
        ),
      );
      if (best !== now) {
        now = best;
        root.dataset.now = String(best);
        reachable(best);
      }
    };
    const schedule = () => {
      if (!frame) frame = requestAnimationFrame(update);
    };
    const fit = () => {
      root.style.removeProperty("--band-h");
      root.style.removeProperty("--lift");
      delete root.dataset.still;
      const style = getComputedStyle(root);
      const mode = style.getPropertyValue("--mode").trim();
      if (mode === "still") return true;
      if (mode === "lift") {
        const gap = parseFloat(getComputedStyle(pin).rowGap) || 0;
        root.style.setProperty("--lift", `${words.getBoundingClientRect().height + gap}px`);
      }
      // The probe is a registered <length>, so it computes to px; a browser without @property
      // keeps the string "100svh" (which would parse as 100), so only a px value is trusted.
      const probe = style.getPropertyValue("--journey-svh").trim();
      const small = probe.endsWith("px") && parseFloat(probe) > 0 ? parseFloat(probe) : innerHeight;
      const over =
        pin.getBoundingClientRect().height +
        (parseFloat(getComputedStyle(pin).top) || 0) +
        12 -
        small;
      if (over <= 0) return false;
      // The page's fonts still arriving (a cold first visit): a fallback face can set the words
      // a line longer (the Korean lead takes two lines until Switzer is in, 3.6px over at
      // 1440x900), which is no shortfall of the rooms. The box is judged again once the fonts
      // are in, instead of shrinking the painting and moving the anchors meanwhile.
      if (document.fonts?.status === "loading") {
        document.fonts.ready.then(() => {
          if (live) remeasure();
        });
        return false;
      }
      const h = painting.getBoundingClientRect().height - over;
      // A room the stylesheet did not measure: say so (once per window size and shortfall).
      const note = `${innerWidth}x${Math.round(small)}: ${over.toFixed(1)}px`;
      if (note !== warned) {
        warned = note;
        console.warn(
          `${LAST_RESORT} Science handscroll: the pinned box is ${over.toFixed(1)}px too tall for this ${innerWidth}x${Math.round(small)} window (small viewport height), so ${h >= 180 ? "the painting shrinks" : "it falls back to the still scroll"} after load and the anchors below move. Measure --words-room / --stops-room again (journey.module.css).`,
        );
      }
      if (h >= 180) {
        root.style.setProperty("--band-h", `${h}px`);
        return false;
      }
      root.style.removeProperty("--lift");
      root.dataset.still = "";
      return true;
    };
    const measure = () => {
      pending = 0;
      fixed = fit();
      setStill(fixed);
      if (fixed) {
        now = -1;
        reachable(null);
        fade(null);
        root.removeAttribute("data-stuck");
        return;
      }
      width = painting.getBoundingClientRect().width;
      view = band.clientWidth;
      half = (items[0]?.offsetWidth ?? 0) / 2;
      halves = items.map(extent);
      overflow = Math.max(0, width - view);
      from = Math.min(overflow, Math.max(0, at[0] * width - view / 2));
      travel = room.offsetHeight;
      root.style.setProperty("--view", `${view}px`);
      // The sticky top as set (less the lift when the title goes on): the travel starts when the
      // box sticks, so it runs from 0 to 1 over exactly the room.
      const pinTop = parseFloat(getComputedStyle(pin).top) || 0;
      const padTop = parseFloat(getComputedStyle(root).paddingTop) || 0;
      start = root.getBoundingClientRect().top + window.scrollY + padTop - pinTop;
      update();
    };
    // One measure per frame, whoever asks: the band or the box changing size (a late font swap
    // changes the title's height) or the window's height alone (the band may be at its least).
    const remeasure = () => {
      if (!pending) pending = requestAnimationFrame(measure);
    };
    const resize = new ResizeObserver(remeasure);
    resize.observe(band);
    resize.observe(pin);
    window.addEventListener("scroll", schedule, { passive: true });
    window.addEventListener("resize", remeasure);
    measure();
    // The stops' words are measured as set: again once the page's fonts have arrived.
    document.fonts?.ready.then(() => {
      if (live) remeasure();
    });
    return () => {
      live = false;
      resize.disconnect();
      window.removeEventListener("scroll", schedule);
      window.removeEventListener("resize", remeasure);
      if (frame) cancelAnimationFrame(frame);
      if (pending) cancelAnimationFrame(pending);
      reachable(null);
      fade(null);
      root.removeAttribute("data-stuck");
      delete root.dataset.still;
      for (const name of ["--x", "--walked", "--view", "--band-h", "--lift"]) {
        root.style.removeProperty(name);
      }
      setStill(false);
    };
  }, [section, motion, at]);
  return still;
}

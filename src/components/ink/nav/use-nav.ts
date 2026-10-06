"use client";

import { useCallback, useEffect, useRef, useState, type FocusEvent } from "react";
import { lockPageScroll } from "../lock-scroll";
import type { NavPanelId } from "./nav-data";

/** The bar holds every link from this width up; under it the links are the phone/tablet menu. */
export const DESKTOP_QUERY = "(min-width: 1101px)";

/** Reduced motion: the bar has two states, the title over the opening and the bar on paper. */
const REDUCED = "(prefers-reduced-motion: reduce)";

/** Where the browser runs scroll-driven animation, the bar's stylesheet settles the title itself. */
const scrollTimelines = () =>
  typeof CSS !== "undefined" && CSS.supports("animation-timeline: scroll()");

/**
 * The title settling with the scroll (round 9), as the browser's own scroll-driven animation does
 * it in the stylesheet (nav-inscription.module.css, "The title settles with the scroll"): where
 * that is missing (Firefox), the same values are written from the page's scroll position on each
 * frame it moves. `t` is how far through the settle the page is (0 at its start, 1 at its end).
 * - g, the bar's geometry (the mark, the words, the bar's height): eased in and out, so the title
 *   starts to settle gently and lands softly.
 * - q, the paper under the words: in early, so the bar's words always stand on paper by the time
 *   the painting slides up behind them.
 * - m, the mist the painting dissolves into at the bar's foot: in with the paper, and gone as the
 *   bar lands (from then on the painted rule is the bar's edge).
 * - d, how far the painted rule is laid: with the scroll, from just after the paper starts.
 */
function settleValues(t: number) {
  const clamp = (v: number) => Math.min(1, Math.max(0, v));
  const stops = (points: [number, number][]) => {
    const x = clamp(t);
    for (let i = 1; i < points.length; i++) {
      const [x0, y0] = points[i - 1];
      const [x1, y1] = points[i];
      if (x <= x1) return y0 + ((y1 - y0) * (x - x0)) / (x1 - x0);
    }
    return points[points.length - 1][1];
  };
  return {
    g: bezier(SETTLE_EASE, clamp(t)),
    q: stops(PAPER_STOPS),
    m: stops(MIST_STOPS),
    d: clamp((t - RULE_FROM) / (1 - RULE_FROM)),
  };
}

// Keep these four in step with the stylesheet's (insc-g's timing function, insc-q's and insc-m's
// keyframes, insc-d's range).
const SETTLE_EASE = [0.45, 0, 0.3, 1] as const;
const PAPER_STOPS: [number, number][] = [
  [0, 0],
  [0.08, 0.9],
  [0.25, 0.97],
  [0.5, 1],
  [1, 1],
];
const MIST_STOPS: [number, number][] = [
  [0, 0],
  [0.08, 0.9],
  [0.4, 0.85],
  [1, 0],
];
const RULE_FROM = 1 / 12;

/** A CSS cubic-bezier timing function at progress x. */
function bezier([x1, y1, x2, y2]: readonly [number, number, number, number], x: number) {
  const curve = (a: number, b: number, s: number) =>
    3 * a * s * (1 - s) ** 2 + 3 * b * s ** 2 * (1 - s) + s ** 3;
  let lo = 0;
  let hi = 1;
  for (let i = 0; i < 24; i++) {
    const mid = (lo + hi) / 2;
    if (curve(x1, x2, mid) < x) lo = mid;
    else hi = mid;
  }
  return curve(y1, y2, (lo + hi) / 2);
}

/**
 * What every menu bar option shares, so the three designs differ in looks, not in manners:
 *
 * - `solid`: the bar has left the opening painting and stands small on paper. With `settledBy`
 *   (round 9) the title settles with the scroll from `solidAfter` to `settledBy` and is solid from
 *   there (with reduced motion: two states, solid past `solidAfter`); without it, solid past
 *   `solidAfter`.
 * - `direction`: the last scroll direction, for a bar that steps aside while you read down.
 * - `panel`: the desktop drop-down that is open (Products or Science). A pointer opens it after a
 *   short pause and closes it a moment after leaving both the button and the panel; a click or
 *   Enter toggles it; Escape closes it and hands focus back to its button; focus leaving the
 *   header closes it; scrolling the page closes it.
 * - `menuOpen`: the narrow window's menu sheet. While it is open the page under it stays put,
 *   Escape closes it (focus back to its button), and it closes when the window grows into the bar.
 */
export function useNav({
  overlay,
  solidAfter,
  settledBy,
}: {
  overlay: boolean;
  solidAfter: number;
  settledBy?: number;
}) {
  const [solid, setSolid] = useState(!overlay);
  const [direction, setDirection] = useState<"up" | "down">("up");
  const [panel, setPanel] = useState<NavPanelId | null>(null);
  const [menuOpen, setMenuOpen] = useState(false);
  const header = useRef<HTMLElement>(null);
  const menuButton = useRef<HTMLButtonElement>(null);
  const triggers = useRef<Partial<Record<NavPanelId, HTMLButtonElement | null>>>({});
  const timer = useRef<number | undefined>(undefined);

  // Scroll: solid once the title has settled (or, with reduced motion or without a settle, after
  // the opening's first few pixels); the direction of travel; and an open drop-down closes once
  // the page moves on under it. Where the browser has no scroll-driven animation, the settle's
  // values are written here, once per frame the page moves.
  useEffect(() => {
    let last = window.scrollY;
    let frame = 0;
    const reduced = window.matchMedia(REDUCED);
    const settles = () => overlay && settledBy !== undefined && !reduced.matches;
    const byHand = settledBy !== undefined && !scrollTimelines();
    const write = () => {
      frame = 0;
      const node = header.current;
      if (!node || settledBy === undefined) return;
      const on = settles();
      const values = settleValues((window.scrollY - solidAfter) / (settledBy - solidAfter));
      for (const [key, value] of Object.entries(values)) {
        if (on) node.style.setProperty(`--insc-${key}`, value.toFixed(4));
        else node.style.removeProperty(`--insc-${key}`);
      }
    };
    const update = () => {
      const y = window.scrollY;
      if (overlay) setSolid(settles() ? y >= settledBy! : y > solidAfter);
      if (byHand && !frame) frame = requestAnimationFrame(write);
      if (Math.abs(y - last) > 6) {
        setDirection(y > last ? "down" : "up");
        if (Math.abs(y - last) > 24) setPanel(null);
        last = y;
      }
    };
    // While the title settles, the stylesheet scales the large mark down to the small one: the
    // ratio of their two sizes, measured again whenever the window changes size.
    const measure = () => {
      const node = header.current;
      if (!node) return;
      const style = getComputedStyle(node);
      const tall = parseFloat(style.getPropertyValue("--insc-mark-tall"));
      const small = parseFloat(style.getPropertyValue("--insc-mark-small"));
      if (tall > 0 && small > 0) node.style.setProperty("--insc-k", (small / tall).toFixed(5));
    };
    measure();
    update();
    window.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", measure);
    reduced.addEventListener("change", update);
    return () => {
      cancelAnimationFrame(frame);
      window.removeEventListener("scroll", update);
      window.removeEventListener("resize", measure);
      reduced.removeEventListener("change", update);
    };
  }, [overlay, solidAfter, settledBy]);

  const clearTimer = () => window.clearTimeout(timer.current);

  /** A pointer resting on a panel's button opens it after a short pause (no flicker in passing). */
  const hoverOpened = useRef({ id: null as NavPanelId | null, at: 0 });
  const hoverOpen = useCallback((id: NavPanelId) => {
    clearTimer();
    timer.current = window.setTimeout(() => {
      hoverOpened.current = { id, at: performance.now() };
      setPanel(id);
    }, 90);
  }, []);

  /** Leaving the button and the panel closes it a moment later (time to cross the gap). */
  const hoverLeave = useCallback(() => {
    clearTimer();
    timer.current = window.setTimeout(() => setPanel(null), 260);
  }, []);

  const hoverStay = useCallback(() => clearTimer(), []);

  // A click that follows the pointer's own opening (the visitor points, the panel opens, then they
  // click as they would on any button) keeps the panel open instead of closing it again.
  const togglePanel = useCallback((id: NavPanelId) => {
    clearTimer();
    const hovered = hoverOpened.current;
    const justOpened = hovered.id === id && performance.now() - hovered.at < 1500;
    hoverOpened.current = { id: null, at: 0 };
    setPanel((current) => (current === id ? (justOpened ? id : null) : id));
  }, []);

  const openPanel = useRef<NavPanelId | null>(null);
  useEffect(() => {
    openPanel.current = panel;
  }, [panel]);

  // Focus handed back to the bar never moves the page: the bar is always in view, but it sits
  // inside the page's 150px scroll padding (globals.css), so a plain focus() would scroll the page
  // to bring it "out from under the header" (about 480px up at 1536x900).
  const closePanel = useCallback((returnFocus = false) => {
    clearTimer();
    const current = openPanel.current;
    if (current && returnFocus) triggers.current[current]?.focus({ preventScroll: true });
    setPanel(null);
  }, []);

  useEffect(() => () => clearTimer(), []);

  // Escape closes the open drop-down; a click anywhere outside the header closes it too.
  useEffect(() => {
    if (!panel) return;
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") closePanel(true);
    };
    const onDown = (event: PointerEvent) => {
      const target = event.target as Node | null;
      if (target && !(target as Element).closest?.("header")) closePanel();
    };
    document.addEventListener("keydown", onKey);
    document.addEventListener("pointerdown", onDown);
    return () => {
      document.removeEventListener("keydown", onKey);
      document.removeEventListener("pointerdown", onDown);
    };
  }, [panel, closePanel]);

  // The narrow window's menu sheet.
  useEffect(() => {
    if (!menuOpen) return;
    const onKey = (event: KeyboardEvent) => {
      if (event.key !== "Escape") return;
      const target = event.target;
      if (target instanceof HTMLOptionElement) return;
      if (target instanceof HTMLSelectElement && CSS.supports("selector(:open)")) {
        if (target.matches(":open")) return;
      }
      setMenuOpen(false);
      menuButton.current?.focus({ preventScroll: true });
    };
    const desktop = window.matchMedia(DESKTOP_QUERY);
    const onDesktop = () => {
      if (desktop.matches) setMenuOpen(false);
    };
    document.addEventListener("keydown", onKey);
    desktop.addEventListener("change", onDesktop);
    const unlock = lockPageScroll();
    return () => {
      document.removeEventListener("keydown", onKey);
      desktop.removeEventListener("change", onDesktop);
      unlock();
    };
  }, [menuOpen]);

  /** Focus leaving the header closes whatever it has open (never focus on a hidden page). */
  const onHeaderBlur = (event: FocusEvent<HTMLElement>) => {
    const next = event.relatedTarget;
    if (!(next instanceof Node) || event.currentTarget.contains(next)) return;
    if (menuOpen) setMenuOpen(false);
    if (panel) closePanel();
  };

  /** Props for a drop-down's button: wire it with `{...triggerProps("products")}`. */
  const triggerProps = (id: NavPanelId) => ({
    ref: (node: HTMLButtonElement | null) => {
      triggers.current[id] = node;
    },
    type: "button" as const,
    "aria-expanded": panel === id,
    "aria-controls": `nav-panel-${id}`,
    onClick: () => togglePanel(id),
    onPointerEnter: (event: React.PointerEvent) => {
      if (event.pointerType === "mouse") hoverOpen(id);
    },
    onPointerLeave: (event: React.PointerEvent) => {
      if (event.pointerType === "mouse") hoverLeave();
    },
  });

  /** Props for a drop-down's panel. */
  const panelProps = (id: NavPanelId) => ({
    id: `nav-panel-${id}`,
    "data-open": panel === id ? "" : undefined,
    inert: panel !== id,
    onPointerEnter: (event: React.PointerEvent) => {
      if (event.pointerType === "mouse") hoverStay();
    },
    onPointerLeave: (event: React.PointerEvent) => {
      if (event.pointerType === "mouse") hoverLeave();
    },
  });

  return {
    header,
    solid,
    direction,
    panel,
    setPanel,
    closePanel,
    triggerProps,
    panelProps,
    menuOpen,
    setMenuOpen,
    menuButton,
    onHeaderBlur,
  };
}

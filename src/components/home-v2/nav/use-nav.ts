"use client";

import { useCallback, useEffect, useRef, useState, type FocusEvent } from "react";
import { lockPageScroll } from "../lock-scroll";
import type { NavPanelId } from "./nav-data";

/** The bar holds every link from this width up; under it the links are the phone/tablet menu. */
export const DESKTOP_QUERY = "(min-width: 1101px)";

/**
 * What every menu bar option shares, so the three designs differ in looks, not in manners:
 *
 * - `solid`: the page has scrolled past `solidAfter` (the bar leaves the opening painting).
 * - `direction`: the last scroll direction, for a bar that steps aside while you read down.
 * - `panel`: the desktop drop-down that is open (Products or Science). A pointer opens it after a
 *   short pause and closes it a moment after leaving both the button and the panel; a click or
 *   Enter toggles it; Escape closes it and hands focus back to its button; focus leaving the
 *   header closes it; scrolling the page closes it.
 * - `menuOpen`: the narrow window's menu sheet. While it is open the page under it stays put,
 *   Escape closes it (focus back to its button), and it closes when the window grows into the bar.
 */
export function useNav({ overlay, solidAfter }: { overlay: boolean; solidAfter: number }) {
  const [solid, setSolid] = useState(!overlay);
  const [direction, setDirection] = useState<"up" | "down">("up");
  const [panel, setPanel] = useState<NavPanelId | null>(null);
  const [menuOpen, setMenuOpen] = useState(false);
  const menuButton = useRef<HTMLButtonElement>(null);
  const triggers = useRef<Partial<Record<NavPanelId, HTMLButtonElement | null>>>({});
  const timer = useRef<number | undefined>(undefined);

  // Scroll: solid after the opening's first few pixels; the direction of travel; and an open
  // drop-down closes once the page moves on under it.
  useEffect(() => {
    let last = window.scrollY;
    const update = () => {
      const y = window.scrollY;
      if (overlay) setSolid(y > solidAfter);
      if (Math.abs(y - last) > 6) {
        setDirection(y > last ? "down" : "up");
        if (Math.abs(y - last) > 24) setPanel(null);
        last = y;
      }
    };
    update();
    window.addEventListener("scroll", update, { passive: true });
    return () => window.removeEventListener("scroll", update);
  }, [overlay, solidAfter]);

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

  const closePanel = useCallback((returnFocus = false) => {
    clearTimer();
    const current = openPanel.current;
    if (current && returnFocus) triggers.current[current]?.focus();
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
      menuButton.current?.focus();
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

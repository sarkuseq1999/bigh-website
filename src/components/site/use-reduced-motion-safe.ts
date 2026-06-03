"use client";

import { useEffect, useState } from "react";
import { useReducedMotion } from "motion/react";

/**
 * Hydration-safe reduced-motion: returns false on the server and on the first
 * client render (matching SSR), then the real preference after mount. This
 * prevents the SSR/client divergence that motion's `initial` styles cause when
 * the rendered output is branched on the reduced-motion preference.
 */
export function useReducedMotionSafe(): boolean {
  const reduce = useReducedMotion();
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);
  return mounted ? reduce ?? false : false;
}

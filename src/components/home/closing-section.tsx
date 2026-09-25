"use client";

import Image from "next/image";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { ArrowRight } from "lucide-react";
import { useEffect, useRef, useSyncExternalStore } from "react";
import { useCopy } from "@/i18n/use-copy";
import {
  closing,
  closingDesigns,
  closingImages,
  defaultClosing,
  type ClosingDesign,
} from "./closing-data";
import styles from "./closing-section.module.css";
import { useReducedMotion } from "./use-reduced-motion";

// The closing invitation, "Start with your cells.": the last block before the footer. Three looks
// for Mo's review, picked with `?closing=1|2|3`:
//   1 space — the hero's deep-space cell returns, small and calm, so the page ends where it began.
//   2 light — the NuriCell bottle stands in the warm gold light of the science section.
//   3 field — the statement alone over a living field of tiny cells that brighten near the pointer.
// Each rises into view once; with reduced motion everything is simply there.
type Props = { onDiscover: () => void };

// The look comes from the address (`?closing=2`); the server renders the default one.
function subscribeToAddress(callback: () => void) {
  window.addEventListener("popstate", callback);
  return () => window.removeEventListener("popstate", callback);
}
function pickedDesign(): ClosingDesign {
  const pick = new URLSearchParams(window.location.search).get("closing");
  return (pick && closingDesigns[pick]) || defaultClosing;
}

export function ClosingSection({ onDiscover }: Props) {
  const design = useSyncExternalStore(subscribeToAddress, pickedDesign, () => defaultClosing);
  return (
    <section
      id="start"
      className={styles.section}
      aria-labelledby="closing-title"
      data-design={design}
    >
      {design === "space" && <ClosingSpace onDiscover={onDiscover} />}
      {design === "light" && <ClosingLight onDiscover={onDiscover} />}
      {design === "field" && <ClosingField onDiscover={onDiscover} />}
    </section>
  );
}

// The words, shared by the three looks. In English, "your cells." is set in the italic serif the
// hero uses; other languages keep the whole line in one voice.
function Words({ onDiscover }: Props) {
  const copy = useCopy();
  const title = copy(closing.title);
  const at = title.indexOf("your cells.");
  return (
    <div className={styles.words} data-words>
      <h2 id="closing-title" className={styles.title}>
        {at > 0 ? (
          <>
            {title.slice(0, at)}
            <em className={styles.cells}>{title.slice(at)}</em>
          </>
        ) : (
          title
        )}
      </h2>
      <p className={styles.text}>{copy(closing.text)}</p>
      <div className={styles.actions}>
        <button type="button" className={styles.primary} onClick={onDiscover}>
          {copy(closing.primary)} <ArrowRight size={19} aria-hidden="true" />
        </button>
        <a href="#products" className={styles.secondary}>
          {copy(closing.secondary)}
        </a>
      </div>
    </div>
  );
}

// Rise into view once, then stay. Returns the gsap context for cleanup.
function reveal(root: HTMLElement, extra?: (timeline: gsap.core.Timeline) => void) {
  gsap.registerPlugin(ScrollTrigger);
  return gsap.context(() => {
    const timeline = gsap.timeline({
      scrollTrigger: { trigger: root, start: "top 72%", once: true },
    });
    timeline.fromTo(
      "[data-words] > *",
      { y: 22, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.9, stagger: 0.12, ease: "power3.out" },
      0.1,
    );
    extra?.(timeline);
  }, root);
}

// 1 · The deep-space cell, centered and softened at the edges, drifting a little and turning
// toward the pointer.
function ClosingSpace({ onDiscover }: Props) {
  const reducedMotion = useReducedMotion();
  const root = useRef<HTMLDivElement>(null);
  const scene = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const element = root.current;
    const picture = scene.current;
    if (!element || !picture || reducedMotion) return;
    const context = reveal(element, (timeline) => {
      timeline.fromTo(
        picture,
        { scale: 0.92, opacity: 0 },
        { scale: 1, opacity: 1, duration: 1.6, ease: "power2.out" },
        0,
      );
    });
    const toX = gsap.quickTo(picture.firstElementChild, "x", { duration: 1.2, ease: "power2.out" });
    const toY = gsap.quickTo(picture.firstElementChild, "y", { duration: 1.2, ease: "power2.out" });
    function point(event: PointerEvent) {
      const box = element!.getBoundingClientRect();
      toX(((event.clientX - box.left) / box.width - 0.5) * -28);
      toY(((event.clientY - box.top) / box.height - 0.5) * -18);
    }
    element.addEventListener("pointermove", point, { passive: true });
    return () => {
      element.removeEventListener("pointermove", point);
      context.revert();
    };
  }, [reducedMotion]);
  return (
    <div ref={root} className={styles.space} data-reduced={reducedMotion}>
      <div ref={scene} className={styles.spaceScene} aria-hidden="true">
        <div className={styles.spaceDrift}>
          <Image
            src={closingImages.space}
            alt=""
            fill
            sizes="(max-width: 899px) 100vw, 760px"
            className={styles.spaceImage}
          />
        </div>
      </div>
      <Words onDiscover={onDiscover} />
    </div>
  );
}

// 2 · The bottle in warm light. The light comes on as the block arrives; the bottle settles and
// then tilts gently toward the pointer.
function ClosingLight({ onDiscover }: Props) {
  const reducedMotion = useReducedMotion();
  const root = useRef<HTMLDivElement>(null);
  const bottle = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const element = root.current;
    const object = bottle.current;
    if (!element || !object || reducedMotion) return;
    const context = reveal(element, (timeline) => {
      timeline
        .fromTo(
          "[data-glow]",
          { opacity: 0, scale: 0.8 },
          { opacity: 1, scale: 1, duration: 1.6, ease: "power2.out" },
          0,
        )
        .fromTo(
          object,
          { y: 44, opacity: 0 },
          { y: 0, opacity: 1, duration: 1.3, ease: "power3.out" },
          0.15,
        );
    });
    const tiltX = gsap.quickTo(object, "rotationX", { duration: 0.9, ease: "power2.out" });
    const tiltY = gsap.quickTo(object, "rotationY", { duration: 0.9, ease: "power2.out" });
    function point(event: PointerEvent) {
      const box = element!.getBoundingClientRect();
      tiltY(((event.clientX - box.left) / box.width - 0.5) * 14);
      tiltX(((event.clientY - box.top) / box.height - 0.5) * -8);
    }
    function leave() {
      tiltX(0);
      tiltY(0);
    }
    element.addEventListener("pointermove", point, { passive: true });
    element.addEventListener("pointerleave", leave);
    return () => {
      element.removeEventListener("pointermove", point);
      element.removeEventListener("pointerleave", leave);
      context.revert();
    };
  }, [reducedMotion]);
  return (
    <div ref={root} className={styles.light} data-reduced={reducedMotion}>
      <Words onDiscover={onDiscover} />
      <div className={styles.stage} aria-hidden="true">
        <span className={styles.glow} data-glow />
        <div ref={bottle} className={styles.bottle}>
          <Image
            {...closingImages.bottle}
            alt=""
            sizes="(max-width: 899px) 44vw, 300px"
            className={styles.bottleImage}
          />
          <Image
            {...closingImages.bottle}
            alt=""
            sizes="(max-width: 899px) 44vw, 300px"
            className={styles.reflection}
          />
        </div>
        <span className={styles.shadow} />
      </div>
    </div>
  );
}

// 3 · A living field: rows of tiny cells on a slow wave, gold near the front, that brighten and
// lift near the pointer. Drawn on a canvas; still with reduced motion.
function ClosingField({ onDiscover }: Props) {
  const reducedMotion = useReducedMotion();
  const root = useRef<HTMLDivElement>(null);
  const canvas = useRef<HTMLCanvasElement>(null);
  useEffect(() => {
    const element = root.current;
    const surface = canvas.current;
    if (!element || !surface) return;
    const context = reducedMotion ? null : reveal(element);
    const stop = drawField(surface, element, reducedMotion);
    return () => {
      stop();
      context?.revert();
    };
  }, [reducedMotion]);
  return (
    <div ref={root} className={styles.field} data-reduced={reducedMotion}>
      <Words onDiscover={onDiscover} />
      <canvas ref={canvas} className={styles.fieldCanvas} aria-hidden="true" />
    </div>
  );
}

function drawField(surface: HTMLCanvasElement, area: HTMLElement, still: boolean) {
  const ctx = surface.getContext("2d");
  if (!ctx) return () => undefined;
  const rows = 15;
  let width = 0;
  let height = 0;
  let cols = 0;
  let dpr = 1;
  const pointer = { x: -1e4, y: -1e4, light: 0, wantLight: 0 };
  let frame = 0;
  let start = performance.now();

  function fit() {
    width = surface.clientWidth;
    height = surface.clientHeight;
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    surface.width = Math.round(width * dpr);
    surface.height = Math.round(height * dpr);
    cols = Math.max(24, Math.round(width / 15));
    if (still) paint(0);
  }

  function paint(seconds: number) {
    ctx!.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx!.clearRect(0, 0, width, height);
    for (let j = 0; j < rows; j++) {
      const t = j / (rows - 1); // 0 far, 1 near
      const spread = 0.62 + 0.38 * t;
      const baseY = 22 + Math.pow(t, 1.35) * (height - 60);
      const sway = still ? 0 : Math.sin(seconds * 0.5 + t * 2.6) * 6 * t;
      for (let i = 0; i < cols; i++) {
        const u = (i + 0.5) / cols - 0.5;
        const x = width / 2 + u * width * spread;
        const wave = still ? 0 : Math.sin(u * 9 + seconds * 0.8 + t * 3) * (4 + 9 * t);
        let y = baseY + wave + sway;
        const dx = x - pointer.x;
        const dy = y - pointer.y;
        const near = Math.exp(-(dx * dx + dy * dy) / 26000) * pointer.light;
        y -= near * 14;
        const size = 0.9 + 2.3 * t + near * 2.4;
        const shimmer = still ? 0 : 0.08 * Math.sin(seconds * 1.7 + i * 0.6 + j * 1.1);
        const alpha = Math.min(1, 0.28 + 0.5 * t + shimmer + near * 0.6);
        // Cream gold far away, warm gold near the front, lime where the pointer is.
        const r = Math.round(232 - near * 90);
        const g = Math.round(176 + near * 40);
        const b = Math.round(72 + near * 20);
        ctx!.fillStyle = `rgba(${r} ${g} ${b} / ${alpha.toFixed(3)})`;
        ctx!.beginPath();
        ctx!.arc(x, y, size, 0, Math.PI * 2);
        ctx!.fill();
      }
    }
  }

  function tick(now: number) {
    frame = requestAnimationFrame(tick);
    pointer.light += (pointer.wantLight - pointer.light) * 0.08;
    paint((now - start) / 1000);
  }

  function move(event: PointerEvent) {
    const box = surface.getBoundingClientRect();
    pointer.x = event.clientX - box.left;
    pointer.y = event.clientY - box.top;
    pointer.wantLight = 1;
    if (still) {
      pointer.light = 1;
      paint(0);
    }
  }
  function leave() {
    pointer.wantLight = 0;
    if (still) {
      pointer.light = 0;
      paint(0);
    }
  }

  fit();
  const resize = new ResizeObserver(fit);
  resize.observe(surface);
  area.addEventListener("pointermove", move, { passive: true });
  area.addEventListener("pointerleave", leave);
  const visibility = new IntersectionObserver(([entry]) => {
    if (still) return;
    if (entry.isIntersecting && !frame) {
      start = performance.now() - 1000;
      frame = requestAnimationFrame(tick);
    }
    if (!entry.isIntersecting && frame) {
      cancelAnimationFrame(frame);
      frame = 0;
    }
  });
  visibility.observe(surface);
  return () => {
    cancelAnimationFrame(frame);
    visibility.disconnect();
    resize.disconnect();
    area.removeEventListener("pointermove", move);
    area.removeEventListener("pointerleave", leave);
  };
}

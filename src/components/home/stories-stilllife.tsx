"use client";

import Image from "next/image";
import gsap from "gsap";
import { useEffect, useRef, useState, type CSSProperties } from "react";
import { stories } from "./stories-data";
import styles from "./stories-stilllife.module.css";
import { useReducedMotion } from "./use-reduced-motion";

// Still life: each story is a small arrangement of everyday things around the real product bottle.
// Pieces float at different depths, drift against the cursor, and scatter and regather between stories.
type Piece = {
  src: string;
  w: number;
  h: number;
  x: number; // center, % of stage width
  y: number; // center, % of stage height
  size: number; // width, % of stage width
  depth: number; // parallax strength and stacking order
  rotate: number; // resting tilt, degrees
};

const V2 = "/images/stories/v2";
const nuricell = { src: `${V2}/bottle-nuricell.webp`, w: 493, h: 900 };
const propolis = { src: `${V2}/bottle-propolis.webp`, w: 492, h: 900 };

const arrangements: Record<(typeof stories)[number]["id"], Piece[]> = {
  lisa: [
    { ...nuricell, x: 27, y: 38, size: 20, depth: 0.7, rotate: -6 },
    {
      src: `${V2}/piece-toast.webp`,
      w: 900,
      h: 796,
      x: 76,
      y: 24,
      size: 27,
      depth: 0.8,
      rotate: 12,
    },
    { src: `${V2}/piece-mug.webp`, w: 900, h: 834, x: 54, y: 57, size: 44, depth: 1, rotate: -3 },
    {
      src: `${V2}/piece-clementine.webp`,
      w: 900,
      h: 811,
      x: 82,
      y: 75,
      size: 23,
      depth: 1.3,
      rotate: 9,
    },
    {
      src: `${V2}/piece-keys.webp`,
      w: 900,
      h: 757,
      x: 22,
      y: 80,
      size: 26,
      depth: 1.5,
      rotate: -16,
    },
  ],
  michael: [
    { ...nuricell, x: 79, y: 30, size: 19, depth: 0.7, rotate: 7 },
    {
      src: `${V2}/piece-teacup.webp`,
      w: 900,
      h: 779,
      x: 23,
      y: 27,
      size: 28,
      depth: 0.8,
      rotate: -5,
    },
    {
      src: `${V2}/object-michael.webp`,
      w: 1400,
      h: 1018,
      x: 50,
      y: 60,
      size: 64,
      depth: 1,
      rotate: -3,
    },
    {
      src: `${V2}/piece-magnifier.webp`,
      w: 890,
      h: 900,
      x: 80,
      y: 80,
      size: 28,
      depth: 1.5,
      rotate: 18,
    },
  ],
  susan: [
    { ...propolis, x: 24, y: 36, size: 20, depth: 0.7, rotate: -7 },
    { src: `${V2}/piece-bee.webp`, w: 864, h: 899, x: 80, y: 20, size: 17, depth: 1.7, rotate: 8 },
    {
      src: `${V2}/object-susan.webp`,
      w: 1400,
      h: 1125,
      x: 55,
      y: 58,
      size: 58,
      depth: 1,
      rotate: -4,
    },
    {
      src: `${V2}/piece-honeycomb.webp`,
      w: 900,
      h: 827,
      x: 82,
      y: 79,
      size: 24,
      depth: 1.3,
      rotate: 10,
    },
    {
      src: `${V2}/piece-sprig.webp`,
      w: 815,
      h: 900,
      x: 18,
      y: 78,
      size: 24,
      depth: 1.2,
      rotate: -28,
    },
  ],
};

export function StillLifeStage({ selected }: { selected: number }) {
  const reducedMotion = useReducedMotion();
  const stage = useRef<HTMLDivElement>(null);
  const [shown, setShown] = useState(selected);
  const [inView, setInView] = useState(false);
  const current = reducedMotion ? selected : shown;
  const story = stories[current];

  // Arrive only once the stage is on screen, so the first assembly is actually seen.
  useEffect(() => {
    const element = stage.current;
    if (!element) return;
    const observer = new IntersectionObserver(([entry]) => {
      if (!entry.isIntersecting) return;
      setInView(true);
      observer.disconnect();
    });
    observer.observe(element);
    return () => observer.disconnect();
  }, []);

  // A new story: the current arrangement scatters, then the next one assembles (see below).
  useEffect(() => {
    const element = stage.current;
    if (!element || reducedMotion || selected === shown) return;
    const pieces = element.querySelectorAll<HTMLElement>("[data-piece]");
    const tween = gsap.to(pieces, {
      x: (_, target: HTMLElement) => (parseFloat(target.style.left) - 50) * 4,
      y: (_, target: HTMLElement) => (parseFloat(target.style.top) - 50) * 3 - 40,
      rotation: "+=24",
      scale: 0.8,
      autoAlpha: 0,
      duration: 0.42,
      ease: "power2.in",
      stagger: 0.035,
      onComplete: () => setShown(selected),
    });
    // Failsafe: a throttled tab can stall requestAnimationFrame; finish the exit so the story still changes.
    const settle = window.setTimeout(() => tween.progress(1), 900);
    return () => {
      window.clearTimeout(settle);
      tween.kill();
    };
  }, [selected, shown, reducedMotion]);

  // Assemble: pieces fly in from the edges and settle, then bob gently at their own pace.
  useEffect(() => {
    const element = stage.current;
    if (!element || reducedMotion) return;
    let settle = 0;
    const context = gsap.context(() => {
      const pieces = gsap.utils.toArray<HTMLElement>("[data-piece]");
      const bobs = gsap.utils.toArray<HTMLElement>("[data-bob]");
      gsap.set(pieces, { xPercent: -50, yPercent: -50 });
      if (!inView) {
        gsap.set(pieces, { autoAlpha: 0 });
        return;
      }
      const arrive = gsap.fromTo(
        pieces,
        {
          x: (_, target: HTMLElement) => (parseFloat(target.style.left) - 50) * 5,
          y: (_, target: HTMLElement) => (parseFloat(target.style.top) - 50) * 4 + 60,
          rotation: (index) => (index % 2 ? 28 : -28),
          scale: 0.6,
          autoAlpha: 0,
        },
        {
          x: 0,
          y: 0,
          rotation: 0,
          scale: 1,
          autoAlpha: 1,
          duration: 1.15,
          ease: "expo.out",
          stagger: 0.08,
        },
      );
      // Failsafe: never leave pieces half-arrived if animation frames are throttled.
      settle = window.setTimeout(() => arrive.progress(1), 2400);
      bobs.forEach((bob, index) => {
        gsap.to(bob, {
          y: index % 2 ? 12 : -12,
          rotation: index % 2 ? -2.5 : 2.5,
          duration: gsap.utils.random(2.6, 4.2),
          delay: gsap.utils.random(0, 1.2),
          ease: "sine.inOut",
          yoyo: true,
          repeat: -1,
        });
      });
    }, element);
    return () => {
      window.clearTimeout(settle);
      context.revert();
    };
  }, [current, inView, reducedMotion]);

  return (
    <div ref={stage} className={styles.stage} aria-hidden="true">
      <span className={styles.orbit} />
      <span className={`${styles.orbit} ${styles.orbitInner}`} />
      {arrangements[story.id].map((piece, index) => (
        <div
          key={`${story.id}-${index}`}
          data-piece
          className={styles.piece}
          style={
            {
              left: `${piece.x}%`,
              top: `${piece.y}%`,
              width: `${piece.size}%`,
              zIndex: Math.round(piece.depth * 10),
              "--depth": piece.depth,
              "--rot": `${piece.rotate}deg`,
            } as CSSProperties
          }
        >
          <div data-bob className={styles.bob}>
            <Image
              src={piece.src}
              width={piece.w}
              height={piece.h}
              sizes="(max-width: 899px) 48vw, 22vw"
              alt=""
            />
          </div>
        </div>
      ))}
    </div>
  );
}

"use client";

import Image from "next/image";
import gsap from "gsap";
import { Sun, Sunrise, Sunset } from "lucide-react";
import { useEffect, useRef, useState, type CSSProperties } from "react";
import { useCopy } from "@/i18n/use-copy";
import { stories } from "./stories-data";
import styles from "./stories-daylight.module.css";
import { useReducedMotion } from "./use-reduced-motion";

// Daylight: one window, one day. Each story is a time of day; the sun travels across the sky,
// the colors change, and the object's shadow on the sill swings with the light.
const moments = [
  {
    label: "Morning",
    Icon: Sunrise,
    angle: 150,
    top: "#8db5ee",
    bottom: "#ffd6ae",
    sun: "#ffe7a6",
    glow: "rgba(255, 196, 120, 0.7)",
  },
  {
    label: "Afternoon",
    Icon: Sun,
    angle: 74,
    top: "#3f7cdb",
    bottom: "#c5e3ff",
    sun: "#fffbea",
    glow: "rgba(255, 246, 214, 0.75)",
  },
  {
    label: "Golden hour",
    Icon: Sunset,
    angle: 28,
    top: "#5874c4",
    bottom: "#ffc585",
    sun: "#ffd479",
    glow: "rgba(255, 164, 84, 0.7)",
  },
] as const;

const HORIZON = 76; // % from the top of the window, where the sill begins

function sunPlace(angle: number) {
  const radians = (angle * Math.PI) / 180;
  return { left: 50 + 41 * Math.cos(radians), top: HORIZON - 56 * Math.sin(radians) };
}

function shadowFor(angle: number) {
  const radians = (angle * Math.PI) / 180;
  const low = 1 - Math.sin(radians); // 0 at noon, larger near the horizon
  return { x: -Math.cos(radians) * 46, scaleX: 1 + low * 0.9, opacity: 0.42 - low * 0.12 };
}

export function DaylightStage({ selected }: { selected: number }) {
  const copy = useCopy();
  const reducedMotion = useReducedMotion();
  const frame = useRef<HTMLDivElement>(null);
  const sun = useRef<HTMLSpanElement>(null);
  const shadow = useRef<HTMLSpanElement>(null);
  const object = useRef<HTMLDivElement>(null);
  const angle = useRef({ value: moments[selected].angle });
  const [shown, setShown] = useState(selected);
  // React paints the first light only; after that GSAP owns sun, sky and shadow, so a re-render
  // mid-animation can't snap them. With reduced motion React follows the selection directly.
  const [initial] = useState(selected);
  const light = moments[reducedMotion ? selected : initial];
  const current = reducedMotion ? selected : shown;
  const story = stories[current];
  const moment = moments[selected];
  const place = sunPlace(light.angle);
  const cast = shadowFor(light.angle);

  // Travel to the new time of day: the sun along its arc, the sky colors, and the shadow.
  // Depends on `selected` only, so swapping the object mid-way can't cut the sky short.
  useEffect(() => {
    const element = frame.current;
    if (!element || reducedMotion) return;
    const target = moments[selected];
    const next = shadowFor(target.angle);
    const timeline = gsap.timeline({ defaults: { ease: "power2.inOut", duration: 1.5 } });
    timeline
      .to(
        angle.current,
        {
          value: target.angle,
          onUpdate: () => {
            const spot = sunPlace(angle.current.value);
            sun.current?.style.setProperty("left", `${spot.left}%`);
            sun.current?.style.setProperty("top", `${spot.top}%`);
          },
        },
        0,
      )
      .to(
        element,
        {
          "--sky-top": target.top,
          "--sky-bottom": target.bottom,
          "--sun": target.sun,
          "--glow": target.glow,
        },
        0,
      )
      .to(shadow.current, { x: next.x, scaleX: next.scaleX, opacity: next.opacity }, 0);
    const settle = window.setTimeout(() => timeline.progress(1), 2400);
    return () => {
      window.clearTimeout(settle);
      timeline.kill();
    };
  }, [selected, reducedMotion]);

  // The current object slides off the sill; the next one follows (below).
  useEffect(() => {
    if (reducedMotion || selected === shown || !object.current) return;
    const tween = gsap.to(object.current, {
      x: -70,
      autoAlpha: 0,
      duration: 0.45,
      ease: "power2.in",
      onComplete: () => setShown(selected),
    });
    const settle = window.setTimeout(() => tween.progress(1), 900);
    return () => {
      window.clearTimeout(settle);
      tween.kill();
    };
  }, [selected, shown, reducedMotion]);

  // The next object slides in along the sill.
  useEffect(() => {
    if (reducedMotion || !object.current) return;
    const tween = gsap.fromTo(
      object.current,
      { x: 90, autoAlpha: 0 },
      { x: 0, autoAlpha: 1, duration: 0.9, ease: "expo.out" },
    );
    const settle = window.setTimeout(() => tween.progress(1), 1600);
    return () => {
      window.clearTimeout(settle);
      tween.kill();
    };
  }, [current, reducedMotion]);

  return (
    <div
      ref={frame}
      className={styles.window}
      aria-hidden="true"
      style={
        {
          "--sky-top": light.top,
          "--sky-bottom": light.bottom,
          "--sun": light.sun,
          "--glow": light.glow,
        } as CSSProperties
      }
    >
      <span className={styles.sky} />
      <span
        ref={sun}
        className={styles.sun}
        style={{ left: `${place.left}%`, top: `${place.top}%` }}
      />
      <span className={`${styles.cloud} ${styles.cloudA}`} />
      <span className={`${styles.cloud} ${styles.cloudB}`} />
      <span className={`${styles.cloud} ${styles.cloudC}`} />
      <svg className={styles.hills} viewBox="0 0 400 60" preserveAspectRatio="none">
        <path d="M0 42 C 60 18, 120 20, 180 34 S 300 12, 400 30 L 400 60 L 0 60 Z" />
        <path d="M0 50 C 80 34, 150 40, 230 46 S 340 34, 400 44 L 400 60 L 0 60 Z" />
      </svg>
      <span className={styles.sill} />
      <span
        ref={shadow}
        className={styles.shadow}
        style={{
          transform: `translateX(${cast.x}px) scaleX(${cast.scaleX})`,
          opacity: cast.opacity,
        }}
      />
      <div ref={object} className={styles.object} key={story.id}>
        <Image
          src={story.object}
          width={story.objectSize.width}
          height={story.objectSize.height}
          sizes="(max-width: 899px) 70vw, 30vw"
          alt=""
        />
      </div>
      <span className={styles.time}>
        <moment.Icon size={17} aria-hidden="true" />
        {copy(moment.label)}
      </span>
    </div>
  );
}

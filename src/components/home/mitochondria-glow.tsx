"use client";

import Image from "next/image";
import { Pause, Play } from "lucide-react";
import { useEffect, useId, useRef, useState, type CSSProperties, type ReactNode } from "react";
import { useCopy } from "@/i18n/use-copy";
import styles from "./mitochondria-glow.module.css";

// Fixed positions avoid random changes during hydration or playback updates.
const particles = [
  [38, 18, 4, 22, -4],
  [48, 75, 7, 26, -15],
  [62, 27, 3, 19, -8],
  [82, 82, 5, 24, -11],
  [93, 36, 8, 29, -19],
  [71, 61, 3, 21, -5],
  [57, 91, 6, 25, -17],
  [89, 12, 4, 23, -10],
] as const;

export function MitochondriaGlow({ children }: { children: ReactNode }) {
  const copy = useCopy();
  const filterId = useId();
  const artwork = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);
  const [paused, setPaused] = useState(false);

  useEffect(() => {
    const element = artwork.current;
    if (!element) return;
    let intersects = false;
    const syncVisibility = () => setVisible(intersects && !document.hidden);
    const observer = new IntersectionObserver(
      ([entry]) => {
        intersects = entry.isIntersecting;
        syncVisibility();
      },
      { threshold: 0.1 },
    );
    observer.observe(element);
    document.addEventListener("visibilitychange", syncVisibility);
    return () => {
      observer.disconnect();
      document.removeEventListener("visibilitychange", syncVisibility);
    };
  }, []);

  return (
    <div ref={artwork} className={styles.artwork} data-running={visible && !paused}>
      <svg className={styles.filters} width="0" height="0" aria-hidden="true">
        <defs>
          <filter
            id={filterId}
            x="-10%"
            y="-10%"
            width="120%"
            height="120%"
            colorInterpolationFilters="sRGB"
          >
            {/* Isolate amber pixels so only the inner folds emit the golden glow. */}
            <feColorMatrix
              type="matrix"
              values="1.6 0 0 0 0  0 1.25 0 0 0  0 0 0.8 0 0  4 0 -3 0 -0.5"
              result="warmFolds"
            />
            <feGaussianBlur in="warmFolds" stdDeviation="22" result="softHalo" />
            <feComponentTransfer in="softHalo" result="halo">
              <feFuncA type="linear" slope="2" />
            </feComponentTransfer>
            <feGaussianBlur in="warmFolds" stdDeviation="3" result="bloom" />
            <feMerge>
              <feMergeNode in="halo" />
              <feMergeNode in="bloom" />
              <feMergeNode in="warmFolds" />
            </feMerge>
          </filter>
        </defs>
      </svg>
      <div className={styles.viewport}>
        <div className={styles.drift}>
          {children}
          <Image
            src="/images/science/comparison/01-inside-cell.webp"
            alt=""
            aria-hidden="true"
            fill
            unoptimized
            sizes="100vw"
            className={styles.glow}
            style={{ filter: `url(#${filterId})` }}
          />
        </div>
        <div className={styles.atmosphere} aria-hidden="true">
          <div className={styles.currents} />
          {particles.map(([x, y, size, duration, delay], index) => (
            <span
              key={index}
              className={styles.particle}
              style={
                {
                  left: `${x}%`,
                  top: `${y}%`,
                  width: size,
                  height: size,
                  animationDuration: `${duration}s`,
                  animationDelay: `${delay}s`,
                } as CSSProperties
              }
            />
          ))}
        </div>
      </div>
      <button type="button" className={styles.control} onClick={() => setPaused((value) => !value)}>
        {paused ? <Play size={12} aria-hidden="true" /> : <Pause size={12} aria-hidden="true" />}
        {copy(paused ? "Play motion" : "Pause motion")}
      </button>
    </div>
  );
}

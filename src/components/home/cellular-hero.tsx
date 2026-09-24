"use client";

import Image from "next/image";
import { ArrowRight, Pause, Play } from "lucide-react";
import { useEffect, useRef, useState, useSyncExternalStore } from "react";
import styles from "./cellular-hero.module.css";

const motionQuery = "(prefers-reduced-motion: reduce)";

const floatingLights = [
  [8, 24, 3, 19, -3],
  [19, 73, 4, 23, -12],
  [34, 12, 3, 21, -8],
  [43, 84, 4, 26, -17],
  [52, 29, 3, 20, -11],
  [59, 69, 5, 25, -5],
  [72, 10, 4, 22, -14],
  [84, 77, 3, 18, -7],
  [93, 31, 5, 24, -16],
  [96, 61, 3, 27, -9],
];

function subscribeToMotionPreference(callback: () => void) {
  const query = window.matchMedia(motionQuery);
  query.addEventListener("change", callback);
  return () => query.removeEventListener("change", callback);
}

function getMotionPreference() {
  return window.matchMedia(motionQuery).matches;
}

function getServerMotionPreference() {
  return true;
}

export function CellularHero({ onDiscover }: { onDiscover: () => void }) {
  const reducedMotion = useSyncExternalStore(
    subscribeToMotionPreference,
    getMotionPreference,
    getServerMotionPreference,
  );
  const video = useRef<HTMLVideoElement>(null);
  const artwork = useRef<HTMLDivElement>(null);
  const pausedByVisitor = useRef(false);
  const [playing, setPlaying] = useState(false);
  const [videoFailed, setVideoFailed] = useState(false);

  useEffect(() => {
    const player = video.current;
    const visual = artwork.current;
    if (!player || !visual || reducedMotion || videoFailed) return;

    let inView = false;
    const syncPlayback = () => {
      if (inView && !document.hidden && !pausedByVisitor.current) {
        // Autoplay can be declined by the browser; the poster and play control remain usable.
        void player.play().catch(() => {});
      } else {
        player.pause();
      }
    };

    const observer = new IntersectionObserver(
      ([entry]) => {
        inView = entry.isIntersecting;
        syncPlayback();
      },
      { threshold: 0.15 },
    );
    observer.observe(visual);
    document.addEventListener("visibilitychange", syncPlayback);
    return () => {
      observer.disconnect();
      document.removeEventListener("visibilitychange", syncPlayback);
      player.pause();
    };
  }, [reducedMotion, videoFailed]);

  function togglePlayback() {
    const player = video.current;
    if (!player) return;
    if (player.paused) {
      pausedByVisitor.current = false;
      void player.play().catch(() => {});
    } else {
      pausedByVisitor.current = true;
      player.pause();
    }
  }

  return (
    <section
      id="home"
      aria-labelledby="hero-title"
      className={styles.hero}
      data-motion={playing && !reducedMotion && !videoFailed ? "running" : "paused"}
    >
      <div className={styles.atmosphere} aria-hidden="true">
        <div className={styles.lightVeil} />
        <div className={styles.lightVeilSecondary} />
        {floatingLights.map(([left, top, size, duration, delay], index) => (
          <span
            key={index}
            className={styles.floatingLight}
            style={{
              left: `${left}%`,
              top: `${top}%`,
              width: size,
              height: size,
              animationDuration: `${duration}s`,
              animationDelay: `${delay}s`,
            }}
          />
        ))}
      </div>
      <div ref={artwork} className={styles.artwork}>
        <div className={styles.media} aria-hidden="true">
          <Image
            src="/media/hero/cell-sculpture-v1.png"
            alt=""
            fill
            preload
            sizes="100vw"
            className={styles.image}
          />
          {!reducedMotion && !videoFailed && (
            <video
              id="cell-hero-video"
              ref={video}
              className={styles.video}
              poster="/media/hero/cell-sculpture-v1.png"
              muted
              loop
              playsInline
              preload="none"
              tabIndex={-1}
              onPlay={() => setPlaying(true)}
              onPause={() => setPlaying(false)}
              onError={() => setVideoFailed(true)}
            >
              <source
                src="/media/hero/cell-sculpture-motion-v2.mp4"
                type="video/mp4"
                onError={() => setVideoFailed(true)}
              />
            </video>
          )}
        </div>
        {!reducedMotion && !videoFailed && (
          <button
            type="button"
            className={styles.motionControl}
            onClick={togglePlayback}
            aria-label={playing ? "Pause hero animation" : "Play hero animation"}
            aria-controls="cell-hero-video"
          >
            {playing ? (
              <Pause size={15} aria-hidden="true" />
            ) : (
              <Play size={15} aria-hidden="true" />
            )}
            <span>{playing ? "Pause motion" : "Play motion"}</span>
          </button>
        )}
      </div>

      <div className={styles.content}>
        <h1 id="hero-title" className={styles.title}>
          <span>Good health</span> <span>starts with</span>{" "}
          <span className={styles.cellLine}>your cells.</span>
        </h1>
        <p className={styles.description}>
          Developed by scientists with deep expertise in cellular health and aging, BiGH’s key
          formulas share one purpose: helping you stay sharp, stay active, and live fully.
        </p>
        <div className={styles.actions}>
          <button type="button" onClick={onDiscover} className={styles.primary}>
            Discover NuriCell <ArrowRight size={19} aria-hidden="true" />
          </button>
          <a href="#scientists" className={styles.secondary}>
            Meet our scientists <ArrowRight size={18} aria-hidden="true" />
          </a>
        </div>
      </div>
    </section>
  );
}

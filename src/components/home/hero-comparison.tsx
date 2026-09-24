"use client";

import { useCopy } from "@/i18n/use-copy";

import Image from "next/image";
import { ArrowRight, Pause, Play } from "lucide-react";
import { useEffect, useRef, useState, useSyncExternalStore } from "react";
import styles from "./hero-comparison.module.css";

const motionQuery = "(prefers-reduced-motion: reduce)";

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

export function DeepSpaceHero({ onDiscover }: { onDiscover: () => void }) {
  const copy = useCopy();
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
        // Keep the still artwork and play control if the browser declines autoplay.
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
      <div ref={artwork} className={styles.artwork}>
        <div className={styles.scene} aria-hidden="true">
          <Image
            src="/media/hero/deep-space-background-v1.png"
            alt=""
            fill
            sizes="100vw"
            preload
            className={styles.image}
          />
          {!reducedMotion && !videoFailed && (
            <video
              id="deep-space-hero-video"
              ref={video}
              className={styles.video}
              muted
              loop
              playsInline
              preload="none"
              tabIndex={-1}
              onLoadedData={(event) => {
                event.currentTarget.dataset.ready = "true";
              }}
              onPlaying={() => setPlaying(true)}
              onPause={() => setPlaying(false)}
              onError={() => setVideoFailed(true)}
            >
              <source
                src="/media/hero/deep-space-motion-v2.mp4"
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
            aria-label={copy(playing ? "Pause hero motion" : "Play hero motion")}
            aria-controls="deep-space-hero-video"
          >
            {playing ? (
              <Pause size={14} aria-hidden="true" />
            ) : (
              <Play size={14} aria-hidden="true" />
            )}
            {copy(playing ? "Pause motion" : "Play motion")}
          </button>
        )}
      </div>

      <div className={styles.copy}>
        <h1 id="hero-title" className={styles.title}>
          <span>{copy("Good health")}</span> <span>{copy("starts with")}</span>{" "}
          <span className={styles.cellLine}>{copy("your cells.")}</span>
        </h1>
        <p className={styles.description}>
          {copy(
            "Developed by scientists with deep expertise in cellular health and aging, BiGH’s key formulas share one purpose: helping you stay sharp, stay active, and live fully.",
          )}
        </p>
        <div className={styles.actions}>
          <button type="button" onClick={onDiscover} className={styles.primary}>
            {copy("Discover NuriCell")} <ArrowRight size={20} aria-hidden="true" />
          </button>
          <a href="#scientists" className={styles.secondary}>
            {copy("Meet our scientists")} <ArrowRight size={18} aria-hidden="true" />
          </a>
        </div>
      </div>
    </section>
  );
}

"use client";

import Image from "next/image";
import { ArrowLeft, ArrowRight, ArrowUpRight, Pause, Play } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { useCopy } from "@/i18n/use-copy";
import { stories, type StoriesDesignProps } from "./stories-data";
import styles from "./stories-moments.module.css";
import { useReducedMotion } from "./use-reduced-motion";

const tones = ["navy", "paper", "cobalt"] as const;

// Design 2 — a swipeable reel: looping everyday moments beside big, easy-to-read quotes.
export function StoriesMoments({ onOpenProduct }: StoriesDesignProps) {
  const copy = useCopy();
  const root = useRef<HTMLDivElement>(null);
  const track = useRef<HTMLDivElement>(null);
  const bar = useRef<HTMLSpanElement>(null);
  const videos = useRef<(HTMLVideoElement | null)[]>([]);
  const visible = useRef<boolean[]>([]);
  const reducedMotion = useReducedMotion();
  // Reduced motion starts with the videos still; the visitor can still press play.
  const [pausedByVisitor, setPausedByVisitor] = useState<boolean | null>(null);
  const paused = pausedByVisitor ?? reducedMotion;
  const [entered, setEntered] = useState(false);
  const waiting = !reducedMotion && !entered;

  // Play only the videos that are on screen, and only while not paused.
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          const index = videos.current.indexOf(entry.target as HTMLVideoElement);
          if (index < 0) continue;
          visible.current[index] = entry.isIntersecting;
          const video = entry.target as HTMLVideoElement;
          if (entry.isIntersecting && !paused) void video.play().catch(() => undefined);
          else video.pause();
        }
      },
      { threshold: 0.55 },
    );
    videos.current.forEach((video) => video && observer.observe(video));
    videos.current.forEach((video, index) => {
      if (!video) return;
      if (paused) video.pause();
      else if (visible.current[index]) void video.play().catch(() => undefined);
    });
    return () => observer.disconnect();
  }, [paused]);

  // One-time entrance: the reel slides in the first time the section is on screen.
  useEffect(() => {
    const element = root.current;
    if (!element || reducedMotion) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting) return;
        setEntered(true);
        observer.disconnect();
      },
      { threshold: 0.15 },
    );
    observer.observe(element);
    return () => observer.disconnect();
  }, [reducedMotion]);

  function measure() {
    const element = track.current;
    if (!element || !bar.current) return;
    const seen = (element.scrollLeft + element.clientWidth) / element.scrollWidth;
    bar.current.style.transform = `scaleX(${Math.min(1, seen).toFixed(3)})`;
  }

  useEffect(() => {
    measure();
    window.addEventListener("resize", measure);
    return () => window.removeEventListener("resize", measure);
  }, []);

  function step(direction: 1 | -1) {
    const element = track.current;
    const first = element?.firstElementChild as HTMLElement | null;
    if (!element || !first) return;
    const gap = parseFloat(getComputedStyle(element).columnGap) || 0;
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    element.scrollBy({
      left: direction * (first.offsetWidth + gap),
      behavior: reduce ? "auto" : "smooth",
    });
  }

  return (
    <div
      ref={root}
      className={styles.moments}
      data-waiting={waiting || undefined}
      data-entered={entered || undefined}
    >
      <div className={styles.inner}>
        <header className={styles.head}>
          <div>
            <h2 id="stories-title">{copy("In their own words.")}</h2>
            <p>{copy("The routines, questions, and choices behind everyday wellbeing.")}</p>
            <p className={styles.note}>
              {copy(
                "Design draft — all testimonials and reviewer names below are fictional samples.",
              )}
            </p>
          </div>
          <div className={styles.controls}>
            <button
              type="button"
              className={styles.pause}
              aria-pressed={paused}
              onClick={() => setPausedByVisitor(!paused)}
            >
              {paused ? (
                <Play size={18} aria-hidden="true" />
              ) : (
                <Pause size={18} aria-hidden="true" />
              )}
              <span>{paused ? copy("Play videos") : copy("Pause videos")}</span>
            </button>
            <button
              type="button"
              aria-label={copy("Previous sample story")}
              onClick={() => step(-1)}
            >
              <ArrowLeft size={22} aria-hidden="true" />
            </button>
            <button type="button" aria-label={copy("Next sample story")} onClick={() => step(1)}>
              <ArrowRight size={22} aria-hidden="true" />
            </button>
          </div>
        </header>
      </div>

      <div
        ref={track}
        className={styles.track}
        onScroll={measure}
        tabIndex={0}
        role="region"
        aria-labelledby="stories-title"
      >
        {stories.map((story, index) => (
          <article
            key={story.id}
            className={styles.spread}
            data-tone={tones[index]}
            style={{ ["--i" as string]: index }}
            aria-label={copy("Sample story {number} of {count}: {name}", {
              number: index + 1,
              count: stories.length,
              name: story.name,
            })}
          >
            <div className={styles.media}>
              <video
                ref={(element) => {
                  videos.current[index] = element;
                }}
                muted
                loop
                playsInline
                preload="none"
                poster={story.still}
                aria-hidden="true"
                tabIndex={-1}
              >
                <source src={story.video} type="video/mp4" />
              </video>
              <span className={styles.topic}>{copy(story.topic)}</span>
              <span className={styles.mediaNote}>{copy("Illustrative video")}</span>
            </div>
            <div className={styles.card}>
              <blockquote>
                <p className={styles.title}>“{copy(story.title)}”</p>
                <p className={styles.quote}>{copy(story.quote)}</p>
              </blockquote>
              <div className={styles.footer}>
                <p className={styles.byline}>
                  <span>{story.name}</span>
                  <span className={styles.tag}>{copy("Fictional sample")}</span>
                </p>
                <button
                  type="button"
                  className={styles.cta}
                  onClick={() => onOpenProduct(story.productIndex)}
                >
                  <span className={styles.bottle}>
                    <Image src={story.productImage} width={96} height={96} sizes="48px" alt="" />
                  </span>
                  <span>{copy("Discover {name}", { name: story.product })}</span>
                  <ArrowUpRight size={19} aria-hidden="true" />
                </button>
              </div>
            </div>
          </article>
        ))}
      </div>

      <div className={styles.inner}>
        <div className={styles.progress} aria-hidden="true">
          <span ref={bar} />
        </div>
      </div>
    </div>
  );
}

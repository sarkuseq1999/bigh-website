"use client";

import Image from "next/image";
import gsap from "gsap";
import { SplitText } from "gsap/SplitText";
import { ArrowUpRight, Pause, Play } from "lucide-react";
import { useEffect, useRef, useState, type KeyboardEvent, type PointerEvent } from "react";
import { useCopy } from "@/i18n/use-copy";
import { DaylightStage } from "./stories-daylight";
import { stories, type StoriesDesignProps, type Story } from "./stories-data";
import styles from "./stories-portraits.module.css";
import { ShowroomStage } from "./stories-showroom";
import { StillLifeStage } from "./stories-stilllife";
import { useReducedMotion } from "./use-reduced-motion";

// Mo's chosen layout: a cobalt field, one story at a time, a big serif quote, and a product link.
// `visual` decides what holds the stage. Customer photos, photo-real invented people, and drawn people
// are ruled out. Round 3 (Sept 24) builds on everyday objects: still life, daylight, and showroom.
export type PortraitVisual =
  | "stilllife"
  | "daylight"
  | "showroom"
  | "hands"
  | "object"
  | "words"
  | "drawing";

const artLabel: Record<PortraitVisual, string | null> = {
  stilllife: "Illustrative photo",
  daylight: "Illustrative photo",
  showroom: "Illustrative photo",
  hands: "Illustrative video",
  object: "Illustrative photo",
  drawing: "Illustrative portrait",
  words: null,
};

function thumbnail(item: Story, visual: PortraitVisual) {
  if (visual === "hands") return item.sceneThumb;
  if (visual === "drawing") return item.face;
  if (visual === "words") return null;
  return item.objectThumb;
}

export function StoriesPortraits({
  onOpenProduct,
  visual = "hands",
}: StoriesDesignProps & { visual?: PortraitVisual }) {
  const copy = useCopy();
  const [selected, setSelected] = useState(0);
  const root = useRef<HTMLDivElement>(null);
  const people = useRef<HTMLDivElement>(null);
  const video = useRef<HTMLVideoElement>(null);
  const frame = useRef(0);
  const reducedMotion = useReducedMotion();
  // Reduced motion starts with the loop still; the visitor can still press play.
  const [pausedByVisitor, setPausedByVisitor] = useState<boolean | null>(null);
  const paused = pausedByVisitor ?? reducedMotion;
  const story = stories[selected];
  const label = artLabel[visual];

  useEffect(() => () => cancelAnimationFrame(frame.current), []);

  // Each new quote rises in word by word behind a mask (GSAP SplitText).
  useEffect(() => {
    if (reducedMotion) return;
    const target = root.current?.querySelector<HTMLElement>("[data-title-text]");
    if (!target) return;
    gsap.registerPlugin(SplitText);
    const split = SplitText.create(target, { type: "words", mask: "words" });
    const tween = gsap.from(split.words, {
      yPercent: 110,
      duration: 0.9,
      ease: "expo.out",
      stagger: 0.06,
    });
    const settle = window.setTimeout(() => tween.progress(1), 1800);
    return () => {
      window.clearTimeout(settle);
      tween.kill();
      split.revert();
    };
  }, [selected, visual, reducedMotion]);

  // The loop plays only while it is on screen and not paused.
  useEffect(() => {
    const element = video.current;
    if (!element) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !paused) void element.play().catch(() => undefined);
        else element.pause();
      },
      { threshold: 0.4 },
    );
    observer.observe(element);
    return () => observer.disconnect();
  }, [paused, selected, visual]);

  // Gentle pointer parallax on the pictured object or drawing. Mouse only; off for reduced motion via CSS.
  function drift(event: PointerEvent<HTMLDivElement>) {
    if (event.pointerType !== "mouse") return;
    const element = root.current;
    if (!element) return;
    const bounds = element.getBoundingClientRect();
    const x = (event.clientX - bounds.left) / bounds.width - 0.5;
    const y = (event.clientY - bounds.top) / bounds.height - 0.5;
    cancelAnimationFrame(frame.current);
    frame.current = requestAnimationFrame(() => {
      element.style.setProperty("--px", x.toFixed(3));
      element.style.setProperty("--py", y.toFixed(3));
    });
  }

  function choose(event: KeyboardEvent<HTMLButtonElement>, index: number) {
    const keys: Record<string, number> = {
      ArrowRight: (index + 1) % stories.length,
      ArrowDown: (index + 1) % stories.length,
      ArrowLeft: (index + stories.length - 1) % stories.length,
      ArrowUp: (index + stories.length - 1) % stories.length,
      Home: 0,
      End: stories.length - 1,
    };
    if (!(event.key in keys)) return;
    event.preventDefault();
    setSelected(keys[event.key]);
    people.current?.querySelectorAll<HTMLButtonElement>("button")[keys[event.key]]?.focus();
  }

  return (
    <div ref={root} className={styles.portraits} data-visual={visual} onPointerMove={drift}>
      <div className={styles.inner}>
        <header className={styles.head}>
          <h2 id="stories-title">{copy("In their own words.")}</h2>
          <p>{copy("The routines, questions, and choices behind everyday wellbeing.")}</p>
        </header>
        <p className={styles.note}>
          {copy("Design draft — all testimonials and reviewer names below are fictional samples.")}
        </p>

        {/* The selector comes before the story in reading order: choose a person, then read. */}
        <div
          ref={people}
          className={styles.people}
          role="group"
          aria-label={copy("Choose a sample story")}
        >
          {stories.map((item, index) => {
            const thumb = thumbnail(item, visual);
            return (
              <button
                key={item.id}
                type="button"
                aria-pressed={selected === index}
                aria-controls="portrait-story"
                onClick={() => setSelected(index)}
                onKeyDown={(event) => choose(event, index)}
              >
                {thumb && (
                  <span className={styles.face}>
                    <Image src={thumb} width={128} height={128} sizes="64px" alt="" />
                  </span>
                )}
                <span className={styles.person}>
                  <strong>{item.name}</strong>
                  <small>{copy(item.topic)}</small>
                </span>
              </button>
            );
          })}
        </div>

        {visual === "stilllife" && <StillLifeStage selected={selected} />}
        {visual === "daylight" && <DaylightStage selected={selected} />}
        {visual === "showroom" && <ShowroomStage selected={selected} onSelect={setSelected} />}

        {visual === "hands" && (
          <figure className={styles.arch} key={`hands-${story.id}`}>
            <video
              ref={video}
              muted
              loop
              playsInline
              preload="metadata"
              poster={story.still}
              aria-hidden="true"
              tabIndex={-1}
            >
              <source src={story.video} type="video/mp4" />
            </video>
            <button
              type="button"
              className={styles.pause}
              aria-pressed={paused}
              onClick={() => setPausedByVisitor(!paused)}
            >
              {paused ? (
                <Play size={17} aria-hidden="true" />
              ) : (
                <Pause size={17} aria-hidden="true" />
              )}
              <span>{paused ? copy("Play videos") : copy("Pause videos")}</span>
            </button>
          </figure>
        )}

        {visual === "object" && (
          <figure className={styles.object} key={`object-${story.id}`}>
            <span className={styles.disc} aria-hidden="true" />
            <div className={styles.drift}>
              <Image
                src={story.object}
                width={story.objectSize.width}
                height={story.objectSize.height}
                sizes="(max-width: 899px) 86vw, 40vw"
                alt=""
              />
            </div>
          </figure>
        )}

        {visual === "drawing" && (
          <figure className={styles.figure} key={`figure-${story.id}`}>
            <div className={styles.drift}>
              <Image
                src={story.portrait}
                width={story.portraitSize.width}
                height={story.portraitSize.height}
                sizes="(max-width: 899px) 62vw, 30vw"
                alt=""
              />
            </div>
          </figure>
        )}

        <article className={styles.story} id="portrait-story" aria-live="polite" key={story.id}>
          <blockquote>
            <p className={styles.title}>
              <span className={styles.mark} aria-hidden="true">
                “
              </span>
              <span data-title-text>{copy(story.title)}</span>
            </p>
            <p className={styles.quote}>{copy(story.quote)}</p>
          </blockquote>
          <p className={styles.byline}>
            <span>{story.name}</span>
            <span className={styles.tag}>{copy("Fictional sample")}</span>
            {label && <span className={styles.art}>{copy(label)}</span>}
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
            <ArrowUpRight size={20} aria-hidden="true" />
          </button>
        </article>
      </div>
    </div>
  );
}

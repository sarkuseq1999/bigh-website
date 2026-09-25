"use client";

import Image from "next/image";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { ArrowDown, ArrowRight, ArrowUpRight } from "lucide-react";
import { useEffect, useRef } from "react";
import { useCopy } from "@/i18n/use-copy";
import { formulas, iris, liu, liuNumbers, opening, pathStops } from "./science-content";
import type { OpeningProps } from "./science-page";
import styles from "./look-golden.module.css";

// The AI illustrations made for this look (public/images/science-page/). Each one carries a
// visible "Illustration" label. Alt texts are DRAFT.
const HERO = {
  src: "/images/science-page/golden-desk.webp",
  alt: "Illustration: a scientist’s desk by a window at sunset, with a notebook, a microscope and glass flasks.", // DRAFT
};
const PICTURES: Record<string, { src: string; alt: string }> = {
  Okayama: {
    src: "/images/science-page/golden-okayama.webp",
    alt: "Illustration: a study desk at dusk with old books and an open brain atlas.", // DRAFT
  },
  "1994": {
    src: "/images/science-page/golden-berkeley.webp",
    alt: "Illustration: a laboratory bench with test tubes in evening light, trees outside.", // DRAFT
  },
  "2002": {
    src: "/images/science-page/golden-journal.webp",
    alt: "Illustration: an open science journal with reading glasses and a cup of tea.", // DRAFT
  },
  "2025": {
    src: "/images/science-page/golden-academy.webp",
    alt: "Illustration: a grand academy hall with sunlight falling through tall windows.", // DRAFT
  },
};

const photoStops = pathStops.filter((stop) => PICTURES[stop.mark]);
const today = pathStops.find((stop) => !PICTURES[stop.mark]) ?? pathStops[pathStops.length - 1];

// Look D, "Golden hour": late-afternoon sun in a quiet lab. Parchment and espresso, amber light,
// film grain, slow camera moves.
//   1. The hero: an illustrated desk at sunset, full-bleed in a rounded frame (Timeline's heroes).
//      It drifts slowly under light that breathes, and softens as you scroll away.
//   2. Dr. Liu, as in look A: centered, his photograph coming into focus as it arrives, window
//      light sliding across the parchment behind it. His face is never altered: only the frame
//      moves, comes into focus and catches light at its edge.
//   3. His record: three gold numbers on an espresso band (280 counts up; the years stay).
//   4. His path as a film strip, as in look B: pinned on wide screens, it slides sideways; each
//      stop is a tall picture that comes into focus in the middle of the screen while a gold line
//      fills along the bottom. "Today" ends it with the two formulas and their credits, then
//      Dr. Iris Wang in words. Phones and reduced motion get the same stops top to bottom.
export function LookGolden({ onStory }: OpeningProps) {
  const copy = useCopy();
  const root = useRef<HTMLElement>(null);

  useEffect(() => {
    const element = root.current;
    if (!element) return;
    gsap.registerPlugin(ScrollTrigger);
    const q = (selector: string) => [...element.querySelectorAll<HTMLElement>(selector)];
    const media = gsap.matchMedia();

    media.add(
      { motion: "(prefers-reduced-motion: no-preference)", wide: "(min-width: 901px)" },
      (context) => {
        const { motion, wide } = context.conditions ?? {};
        if (!motion) return;

        // 1. The sun comes up on the desk; the words rise out of soft focus.
        gsap.fromTo(
          q("[data-hero-image]"),
          { scale: 1.1, filter: "brightness(0.42) saturate(0.8)" },
          { scale: 1, filter: "brightness(1) saturate(1)", duration: 3, ease: "power2.out" },
        );
        gsap.fromTo(
          q("[data-hero-light]"),
          { opacity: 0 },
          { opacity: 1, duration: 3.2, delay: 0.8, ease: "sine.inOut" },
        );
        gsap.fromTo(
          q("[data-hero-rise]"),
          { y: 36, opacity: 0, filter: "blur(10px)" },
          {
            y: 0,
            opacity: 1,
            filter: "blur(0px)",
            duration: 1.7,
            ease: "power3.out",
            stagger: 0.16,
            delay: 0.35,
            clearProps: "filter",
          },
        );
        // Scrolling away: the picture slides, softens and recedes a little; the words drift up.
        gsap
          .timeline({
            scrollTrigger: {
              trigger: q("[data-hero]")[0],
              start: "top top",
              end: "bottom top",
              scrub: true,
            },
          })
          .fromTo(
            q("[data-hero-media]"),
            { yPercent: 0, filter: "blur(0px) brightness(1)" },
            { yPercent: 8, filter: "blur(7px) brightness(0.78)", ease: "none" },
            0,
          )
          .fromTo(q("[data-hero-frame]"), { scale: 1 }, { scale: 0.95, ease: "none" }, 0)
          .fromTo(q("[data-hero-copy]"), { y: 0 }, { y: -90, ease: "none" }, 0);

        // 2. Dr. Liu: the photograph comes into focus as it arrives (at once if already in view).
        gsap.fromTo(
          q("[data-photo]"),
          { filter: "blur(18px) saturate(0.7)", scale: 1.12 },
          {
            filter: "blur(0px) saturate(1)",
            scale: 1,
            duration: 2,
            ease: "power2.out",
            scrollTrigger: { trigger: q("[data-portrait]")[0], start: "top 88%", once: true },
          },
        );
        gsap.from(q("[data-liu-copy] > *"), {
          y: 28,
          opacity: 0,
          duration: 1,
          ease: "power2.out",
          stagger: 0.09,
          scrollTrigger: { trigger: q("[data-liu-copy]")[0], start: "top 86%", once: true },
        });
        // The window light slides across the wall behind him as you pass.
        gsap.fromTo(
          q("[data-sun]"),
          { xPercent: -14 },
          {
            xPercent: 14,
            ease: "none",
            scrollTrigger: {
              trigger: q("[data-liu]")[0],
              start: "top bottom",
              end: "bottom top",
              scrub: true,
            },
          },
        );

        // 3. His record: the late sun crosses the dark band too; the numbers rise; 280 counts up
        // (the years stay as they are).
        gsap.fromTo(
          q("[data-record-light]"),
          { xPercent: -18 },
          {
            xPercent: 18,
            ease: "none",
            scrollTrigger: {
              trigger: q("[data-record]")[0],
              start: "top bottom",
              end: "bottom top",
              scrub: true,
            },
          },
        );
        const numbers = q("[data-numbers]")[0];
        gsap.from(q("[data-number]"), {
          y: 34,
          opacity: 0,
          duration: 1,
          ease: "power2.out",
          stagger: 0.14,
          scrollTrigger: { trigger: numbers, start: "top 82%", once: true },
        });
        q("[data-count]").forEach((node) => {
          const target = Number(node.dataset.count);
          const state = { value: 0 };
          gsap.to(state, {
            value: target,
            duration: 1.9,
            ease: "power2.out",
            scrollTrigger: { trigger: numbers, start: "top 82%", once: true },
            onUpdate: () => {
              node.textContent = String(Math.round(state.value));
            },
          });
        });

        // 4. The film strip.
        const film = q("[data-film]")[0];
        const track = q("[data-track]")[0];
        const fill = q("[data-fill]")[0];
        if (!film || !track || !fill) return;

        if (!wide) {
          // Phones: each picture comes into focus as it arrives.
          q("[data-card-media]").forEach((node) => {
            gsap.fromTo(
              node,
              { filter: "blur(12px) brightness(0.8)", scale: 1.1 },
              {
                filter: "blur(0px) brightness(1)",
                scale: 1,
                duration: 1.6,
                ease: "power2.out",
                scrollTrigger: { trigger: node, start: "top 86%", once: true },
              },
            );
          });
          return;
        }

        const stops = q("[data-stop]");
        const ticks = q("[data-tick]");
        const distance = () => Math.max(0, track.scrollWidth - film.clientWidth);
        // Where each stop sits along the line: the moment its middle reaches the screen's middle.
        let marks: number[] = [];
        const place = () => {
          const span = distance();
          const half = film.clientWidth / 2;
          marks = stops.map((stop) => {
            const middle = stop.offsetLeft + stop.offsetWidth / 2;
            return span ? gsap.utils.clamp(0, 1, (middle - half) / span) : 0;
          });
          ticks.forEach((tick, index) => {
            tick.style.left = `${(marks[index] ?? 1) * 100}%`;
          });
        };
        const light = (progress: number) => {
          gsap.set(fill, { scaleX: progress });
          ticks.forEach((tick, index) => {
            tick.toggleAttribute("data-on", progress >= (marks[index] ?? 1) - 0.004);
          });
        };

        const slide = gsap.to(track, {
          x: () => -distance(),
          ease: "none",
          scrollTrigger: {
            trigger: film,
            start: "top top",
            end: () => `+=${distance()}`,
            pin: true,
            scrub: 0.9,
            invalidateOnRefresh: true,
            onRefresh: (self) => {
              place();
              light(self.progress);
            },
            onUpdate: (self) => light(self.progress),
          },
        });

        // Each picture is soft at the sides of the screen and sharp in the middle.
        q("[data-card-media]").forEach((node) => {
          gsap
            .timeline({
              scrollTrigger: {
                trigger: node,
                containerAnimation: slide,
                start: "left right",
                end: "right left",
                scrub: true,
              },
            })
            .fromTo(
              node,
              { filter: "blur(12px) brightness(0.7) saturate(0.85)", scale: 1.16 },
              {
                filter: "blur(0px) brightness(1) saturate(1)",
                scale: 1.02,
                duration: 1,
                ease: "sine.out",
              },
            )
            .to(node, { duration: 0.7 })
            .to(node, {
              filter: "blur(6px) brightness(0.8) saturate(0.9)",
              scale: 1,
              duration: 1,
              ease: "sine.in",
            });
        });
        // The bottles catch the light as "Today" arrives.
        gsap.fromTo(
          q("[data-bottle]"),
          { filter: "brightness(0.8) saturate(0.9)", y: 18 },
          {
            filter: "brightness(1.04) saturate(1)",
            y: 0,
            ease: "none",
            stagger: 0.1,
            scrollTrigger: {
              trigger: q("[data-today]")[0],
              containerAnimation: slide,
              start: "left 95%",
              end: "center 55%",
              scrub: true,
            },
          },
        );
        // Words light up as their stop reaches the middle.
        // (The last one, Dr. Iris Wang, ends the strip near the right edge.)
        stops.forEach((stop, index) => {
          ScrollTrigger.create({
            trigger: stop,
            containerAnimation: slide,
            start: index === stops.length - 1 ? "left 88%" : "left 62%",
            onEnter: () => (stop.dataset.lit = "true"),
            onLeaveBack: () => delete stop.dataset.lit,
          });
        });
      },
    );
    return () => media.revert();
  }, []);

  return (
    <section id="scientists" ref={root} className={styles.golden} data-tone="light">
      {/* 1. The hero: a desk at sunset, full-bleed in a rounded frame. */}
      <div className={styles.hero} data-hero>
        <div className={styles.heroFrame} data-hero-frame>
          <div className={styles.heroMedia} data-hero-media>
            <div className={styles.heroDrift}>
              <Image
                src={HERO.src}
                alt={copy(HERO.alt)}
                fill
                priority
                sizes="(max-width: 900px) 230vh, 100vw"
                className={styles.heroImage}
                data-hero-image
              />
            </div>
          </div>
          <div className={styles.heroLight} aria-hidden="true" data-hero-light>
            <span className={styles.sunGlow} />
            <span className={styles.sunBeam} />
          </div>
          <div className={styles.heroShade} aria-hidden="true" />
          <span className={styles.grain} aria-hidden="true" />
          <div className={styles.heroCopy} data-hero-copy>
            <p className={styles.heroEyebrow} data-hero-rise>
              {copy(opening.eyebrow)}
            </p>
            <h1 className={styles.heroTitle}>
              <span data-hero-rise>{copy(opening.titleLead)}</span>{" "}
              <span className={styles.heroAccent} data-hero-rise>
                {copy(opening.titleAccent)}
              </span>
            </h1>
          </div>
          <span className={styles.label}>{copy("Illustration")}</span>
          <a href="#dr-liu" className={styles.cue}>
            <span className={styles.cueIcon}>
              <ArrowDown size={20} />
            </span>
            {copy(liu.name)}
          </a>
        </div>
      </div>

      {/* 2. Dr. Liu, centered, coming into focus. */}
      <div id="dr-liu" className={styles.liu} data-liu>
        <div className={styles.window} aria-hidden="true">
          <div className={styles.windowLight} data-sun />
          <span className={styles.grain} />
        </div>
        <figure className={styles.portrait} data-portrait>
          <Image
            src={liu.photo.src}
            alt={copy(liu.name)}
            fill
            sizes="(max-width: 900px) 78vw, 440px"
            className={styles.photo}
            data-photo
          />
        </figure>
        <div className={styles.liuCopy} data-liu-copy>
          <p className={styles.eyebrow}>{copy(liu.role)}</p>
          <h2 className={styles.name}>{copy(liu.name)}</h2>
          <p className={styles.statement}>{copy(liu.headline)}</p>
          <p className={styles.body}>{copy(liu.intro)}</p>
          <button type="button" className={styles.storyButton} onClick={onStory}>
            {copy(liu.button)} <ArrowRight size={20} />
          </button>
        </div>
      </div>

      {/* 3. His record, in gold on espresso. */}
      <div className={styles.record} data-tone="dark" data-record>
        <span className={styles.recordLight} aria-hidden="true" data-record-light />
        <span className={styles.grain} aria-hidden="true" />
        <p className={styles.recordEyebrow}>{copy("His record") /* DRAFT */}</p>
        <div className={styles.numbers} data-numbers>
          {liuNumbers.map((item) => (
            <div key={item.value} className={styles.number} data-number>
              <p className={styles.value}>
                <span data-count={item.suffix ? item.value : undefined}>{item.value}</span>
                {item.suffix}
              </p>
              <p className={styles.numberLabel}>{copy(item.label)}</p>
              <a href={item.url} target="_blank" rel="noreferrer" className={styles.darkSource}>
                {copy("Source")} <ArrowUpRight size={16} />
              </a>
            </div>
          ))}
        </div>
        <p className={styles.tribute}>
          {copy(liu.highlights[2].text)}{" "}
          <a href={liu.highlights[2].url} target="_blank" rel="noreferrer">
            {copy(liu.highlights[2].link)} <ArrowUpRight size={16} />
          </a>
        </p>
      </div>

      {/* 4. His path: a film strip that slides sideways on wide screens. */}
      <div className={styles.film} data-film>
        <span className={styles.grain} aria-hidden="true" />
        <div className={styles.track} data-track>
          <div className={styles.lead}>
            <div className={styles.leadFrame}>
              <p className={styles.eyebrow}>{copy("His path")}</p>
              <h2 className={styles.leadTitle}>{copy("A life in cell science.")}</h2>
            </div>
            <p className={styles.hint}>
              {copy("Scroll to follow it")} <ArrowRight size={18} />
            </p>
          </div>

          {photoStops.map((stop) => {
            const picture = PICTURES[stop.mark];
            return (
              <article key={stop.mark} className={styles.stop} data-stop>
                <div className={styles.card}>
                  <div className={styles.cardMedia} data-card-media>
                    <Image
                      src={picture.src}
                      alt={copy(picture.alt)}
                      fill
                      sizes="(max-width: 900px) 92vw, 440px"
                    />
                  </div>
                  <div className={styles.cardShade} aria-hidden="true" />
                  <span className={styles.cardLabel}>{copy("Illustration")}</span>
                  <div className={styles.cardWords}>
                    <p className={styles.mark}>{copy(stop.mark)}</p>
                    <h3 className={styles.cardTitle}>{copy(stop.title)}</h3>
                  </div>
                </div>
                <div className={styles.stopCopy}>
                  <p className={styles.stopText}>{copy(stop.text)}</p>
                  {stop.url && (
                    <a href={stop.url} target="_blank" rel="noreferrer" className={styles.source}>
                      {copy(stop.link)} <ArrowUpRight size={16} />
                    </a>
                  )}
                </div>
              </article>
            );
          })}

          <article className={`${styles.stop} ${styles.today}`} data-stop data-today>
            <div className={styles.todayPanel} aria-hidden="true">
              <span className={styles.todayBeam} />
            </div>
            <div className={styles.todayWords}>
              <p className={`${styles.mark} ${styles.todayMark}`}>{copy(today.mark)}</p>
              <h3 className={styles.todayTitle}>{copy(today.title)}</h3>
              <p className={`${styles.stopText} ${styles.todayText}`}>{copy(today.text)}</p>
            </div>
            {formulas.map((formula) => (
              <figure key={formula.name} className={styles.formula}>
                <div className={styles.bottle} data-bottle>
                  <Image
                    src={formula.image}
                    alt={copy("{name} bottle", { name: formula.name })}
                    fill
                    sizes="(max-width: 900px) 40vw, 240px"
                  />
                </div>
                <figcaption className={styles.credit}>
                  <strong>{formula.name}</strong>
                  <span>{copy(formula.credit)}</span>
                </figcaption>
              </figure>
            ))}
          </article>

          {/* Dr. Iris Wang in words only: her card is her name, in the same window light. */}
          <article className={styles.stop} data-stop>
            <div className={styles.irisCard}>
              <span className={styles.irisLight} aria-hidden="true" />
              <p className={styles.irisRole}>{copy(iris.role)}</p>
              <div>
                <h3 className={styles.irisName}>{copy(iris.name)}</h3>
                <p className={styles.irisText}>{copy(iris.text)}</p>
              </div>
            </div>
          </article>
        </div>

        <div className={styles.rail} aria-hidden="true">
          <div className={styles.railLine}>
            <div className={styles.railFill} data-fill />
          </div>
          {[...photoStops, today].map((stop) => (
            <span key={stop.mark} className={styles.tick} data-tick>
              {copy(stop.mark)}
            </span>
          ))}
        </div>
      </div>
    </section>
  );
}

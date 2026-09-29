"use client";

import Image from "next/image";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { ArrowRight, ArrowUpRight } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { useReducedMotion } from "@/components/home/use-reduced-motion";
import { useCopy } from "@/i18n/use-copy";
import { formulas, iris, liu, opening, questions } from "./science-content";
import type { OpeningProps } from "./science-page";
import styles from "./look-dark.module.css";

// Where the droplets rest beside the cell (percent of the picture's row) and their size. On
// phones the cell is wider than the screen, so they wait above and below it instead (--px, --py).
const DROPS = [
  { "--x": "21%", "--y": "26%", "--px": "18%", "--py": "10%", "--s": "clamp(54px, 6vw, 92px)" },
  { "--x": "80%", "--y": "70%", "--px": "84%", "--py": "80%", "--s": "clamp(64px, 7vw, 110px)" },
  { "--x": "85%", "--y": "24%", "--px": "64%", "--py": "6%", "--s": "clamp(40px, 4.2vw, 66px)" },
];

// Look C, "From the dark": the homepage's night palette. Dr. Liu's studio photograph already has a
// dark ground, so it dissolves into the page with no box around it. Then his three research themes
// play out on one glass mitochondrion, re-rendered on a dark ground (a second render in the same
// style, reference/science-page/originals/sp-dark-cell.png). Every change to the cell is a change
// to the render's own pixels (light, saturation), never a shape pasted on top.
export function LookDark({ onStory }: OpeningProps) {
  const copy = useCopy();
  const root = useRef<HTMLElement>(null);
  const reduced = useReducedMotion();
  const [chapter, setChapter] = useState(0);

  useEffect(() => {
    const element = root.current;
    if (!element || reduced) return;
    gsap.registerPlugin(ScrollTrigger);
    const context = gsap.context(() => {
      // He steps out of the dark.
      gsap.fromTo(
        "[data-portrait] img",
        { filter: "brightness(0.05) blur(10px)", scale: 1.06 },
        {
          filter: "brightness(1) blur(0px)",
          scale: 1,
          duration: 2.4,
          ease: "power2.out",
          delay: 0.2,
        },
      );
      gsap.from("[data-rise]", {
        y: 34,
        opacity: 0,
        duration: 1.2,
        ease: "power3.out",
        stagger: 0.12,
        delay: 0.35,
      });

      // One cell, three questions: light, balance, age.
      const cell = "[data-cell]";
      const story = gsap.timeline({
        scrollTrigger: {
          trigger: "[data-cell-track]",
          start: "top top",
          end: "bottom bottom",
          scrub: 0.7,
          onUpdate: (self) => setChapter(Math.min(2, Math.floor(self.progress * 3))),
        },
      });
      story
        .fromTo(
          cell,
          { filter: "brightness(0.82) saturate(1) sepia(0)" },
          { filter: "brightness(1.12) saturate(1.08) sepia(0)", duration: 1, ease: "sine.inOut" },
        )
        .fromTo(
          "[data-halo]",
          { opacity: 0.45, scale: 0.92 },
          { opacity: 1, scale: 1.08, duration: 1 },
          0,
        )
        .to("[data-lime]", { opacity: 1, duration: 0.6 }, 1.05)
        .to("[data-halo]", { opacity: 0.55, duration: 0.6 }, 1.05)
        .fromTo(
          "[data-drop]",
          { opacity: 0, scale: 0.55, yPercent: 30 },
          { opacity: 1, scale: 1, yPercent: 0, duration: 0.6, stagger: 0.12, ease: "power2.out" },
          1.05,
        )
        .to(
          "[data-drop]",
          { opacity: 0, scale: 0.7, yPercent: -20, duration: 0.45, stagger: 0.06 },
          1.95,
        )
        .to("[data-lime]", { opacity: 0, duration: 0.5 }, 2.0)
        .to(cell, { filter: "brightness(0.58) saturate(0.4) sepia(0.28)", duration: 0.9 }, 2.05)
        .to("[data-halo]", { opacity: 0.12, scale: 0.9, duration: 0.9 }, 2.05)
        .to({}, { duration: 0.1 });

      gsap.from("[data-highlight]", {
        y: 30,
        opacity: 0,
        duration: 0.9,
        ease: "power2.out",
        stagger: 0.12,
        scrollTrigger: { trigger: "[data-highlights]", start: "top 78%" },
      });
      gsap.from("[data-bottle]", {
        y: 50,
        opacity: 0,
        duration: 1.1,
        ease: "power3.out",
        stagger: 0.15,
        scrollTrigger: { trigger: "[data-together]", start: "top 75%" },
      });
    }, element);
    return () => context.revert();
  }, [reduced]);

  const jumpTo = (index: number) => {
    const track = root.current?.querySelector<HTMLElement>("[data-cell-track]");
    if (!track) return;
    const top = track.getBoundingClientRect().top + window.scrollY;
    const room = track.offsetHeight - window.innerHeight;
    window.scrollTo({
      top: top + room * ((index + 0.5) / 3),
      behavior: reduced ? "auto" : "smooth",
    });
  };

  return (
    <section
      id="scientists"
      ref={root}
      className={`${styles.dark} ${reduced ? styles.still : ""}`}
      data-tone="dark"
    >
      <div className={styles.hero}>
        <div className={styles.heroCopy}>
          <p className={styles.eyebrow} data-rise>
            {copy(opening.eyebrow)}
          </p>
          <h1 className={styles.title}>
            <span data-rise>{copy(opening.titleLead)}</span>{" "}
            <span className={styles.accent} data-rise>
              {copy(opening.titleAccent)}
            </span>
          </h1>
          <div className={styles.person} data-rise>
            <p className={styles.name}>{copy(liu.name)}</p>
            <p className={styles.role}>{copy(liu.role)}</p>
          </div>
          <button type="button" className={styles.storyButton} onClick={onStory} data-rise>
            {copy(liu.button)} <ArrowRight size={20} />
          </button>
        </div>
        <figure className={styles.portrait} data-portrait>
          <span className={styles.backlight} aria-hidden="true" />
          <Image
            src={liu.photo.src}
            alt={copy(liu.name)}
            fill
            priority
            sizes="(max-width: 900px) 80vw, 520px"
          />
        </figure>
      </div>

      <div className={styles.statementBlock}>
        <p className={styles.statement}>{copy(liu.headline)}</p>
        <p className={styles.body}>{copy(liu.intro)}</p>
      </div>

      <div className={styles.cellTrack} data-cell-track>
        <div className={styles.stage}>
          <div className={styles.stageHead}>
            <p className={styles.eyebrow}>{copy("His research")}</p>
            <h2 className={styles.stageTitle}>{copy("One cell, three questions.")}</h2>
            <div className={styles.tabs} role="group" aria-label={copy("Topics")}>
              {questions.map((question, index) => (
                <button
                  key={question.topic}
                  type="button"
                  aria-pressed={chapter === index}
                  onClick={() => jumpTo(index)}
                >
                  <span>{index + 1}</span> {copy(question.topic)}
                </button>
              ))}
            </div>
          </div>
          <div className={styles.cellWrap}>
            <span className={styles.halo} data-halo aria-hidden="true" />
            <Image
              src="/images/science-page/dark-cell.webp"
              alt={copy("A mitochondrion, shown as warm-gold glass")}
              width={1920}
              height={1086}
              sizes="(max-width: 900px) 110vw, 72vw"
              className={styles.cell}
              data-cell
            />
            <span className={styles.lime} data-lime aria-hidden="true" />
            {/* Balance: three antioxidant droplets, the homepage's lime-glass render, float in
                beside the glass (never on it) and leave again for Aging. */}
            {DROPS.map((drop, index) => (
              <Image
                key={index}
                src="/images/science/antioxidant.webp"
                alt=""
                width={512}
                height={512}
                className={styles.drop}
                style={drop as React.CSSProperties}
                data-drop
              />
            ))}
          </div>
          <div className={styles.chapters}>
            {questions.map((question, index) => (
              <div
                key={question.topic}
                className={styles.chapter}
                data-active={chapter === index ? "true" : undefined}
                aria-hidden={reduced ? undefined : chapter !== index}
              >
                <h3>{copy(question.title)}</h3>
                <p>{copy(question.text)}</p>
                {index === 2 && (
                  <p className={styles.note}>{copy("Illustration, not a measurement")}</p>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className={styles.highlights} data-highlights>
        <p className={styles.eyebrow}>{copy("A few highlights of his work and recognition")}</p>
        <div className={styles.highlightRow}>
          {liu.highlights.map((item, index) => (
            <div key={item.url} className={styles.highlight} data-highlight>
              <span className={styles.count}>{String(index + 1).padStart(2, "0")}</span>
              <p>{copy(item.text)}</p>
              <a href={item.url} target="_blank" rel="noreferrer">
                {copy(item.link)} <ArrowUpRight size={16} />
              </a>
            </div>
          ))}
        </div>
      </div>

      <div className={styles.together} data-together>
        <div className={styles.iris}>
          <p className={styles.eyebrow}>{copy(iris.role)}</p>
          <h2 className={styles.irisName}>{copy(iris.name)}</h2>
          <p className={styles.body}>{copy(iris.text)}</p>
        </div>
        <div className={styles.formulas}>
          {formulas.map((formula) => (
            <figure key={formula.name} className={styles.formula} data-bottle>
              <div className={styles.bottle}>
                <Image
                  src={formula.image}
                  alt={copy("{name} bottle", { name: formula.name })}
                  fill
                  sizes="(max-width: 900px) 40vw, 220px"
                />
              </div>
              <figcaption>
                <strong>{formula.name}</strong>
                <span>{copy(formula.credit)}</span>
              </figcaption>
            </figure>
          ))}
        </div>
      </div>
    </section>
  );
}
